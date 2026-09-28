#!/usr/bin/env python3
"""
Generate an animated terminal-style SVG card with row-by-row reveal.
- Clean 5-row pure block ASCII art for JERRY
- Information displayed directly without labels
- Progress bars designed with matching block segments (Passion 100%, Caffeine 100%, Sleep 0%)
- Vibrant multi-color cyberpunk palette
- Row-by-row reveal animation
"""

# ─── Dimensions & Geometry ───────────────────────────────────────────────────

W = 500
TITLE_BAR_H = 34
CORNER_R = 10
PAD_X = 26

# Colors
BG = "#0d1117"
TITLE_BG = "#161b22"
BORDER = "#30363d"
DOT_RED = "#ff5f57"
DOT_YEL = "#febc2e"
DOT_GRN = "#28c840"

# Palette
C_PROMPT_ICON = "#e3b341"   # gold lightning
C_USER = "#58a6ff"          # electric blue
C_HOST = "#bc8cff"          # purple
C_PATH = "#7ee787"          # soft green
C_CMD = "#f0883e"           # warm amber
C_BULLET = "#79c0ff"        # cyan bullet
C_DIM = "#8b949e"           # dim gray
C_TEXT = "#e6edf3"          # bright white
C_BLOCK_EMPTY = "#21262d"   # dark block for 0% / empty track
C_BAR_PASSION = "#f0883e"   # amber
C_BAR_CAFFEINE = "#d2a8ff"  # electric purple
C_BAR_SLEEP = "#58a6ff"     # sky blue
C_JP = "#f0883e"            # amber

FONT_MONO = "ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono',monospace"

# ASCII gradient colors (5 rows)
ASCII_ROW_COLORS = [
    "#f0883e",  # warm orange
    "#f79a4d",  # lighter amber
    "#e3b341",  # gold
    "#d2a8ff",  # light purple
    "#bc8cff",  # purple
]

REVEAL_TIME = 2.4
REVEAL_FADE = 0.4


def escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_block_bar_svg(x_start, y_top, pct, active_color, num_blocks=24, block_w=8, block_h=11, gap=2.5, r=1):
    """
    Render progress bar as discrete retro terminal block segments matching the JERRY ASCII design.
    """
    filled_count = int(num_blocks * (pct / 100.0))
    rects = []
    for i in range(num_blocks):
        bx = x_start + i * (block_w + gap)
        color = active_color if i < filled_count else C_BLOCK_EMPTY
        rects.append(
            f'<rect x="{bx:.1f}" y="{y_top:.1f}" width="{block_w}" height="{block_h}" rx="{r}" fill="{color}"/>'
        )
    return "".join(rects)


def build_svg():
    elements = []
    
    # 1. Top prompt (Y = 62)
    elements.append({
        "y": 62,
        "svg": (
            f'<text x="{PAD_X}" y="62" font-family="{FONT_MONO}" font-size="13">'
            f'<tspan fill="{C_PROMPT_ICON}">⚡ </tspan>'
            f'<tspan fill="{C_USER}" font-weight="600">jerry</tspan>'
            f'<tspan fill="{C_DIM}">@</tspan>'
            f'<tspan fill="{C_HOST}" font-weight="600">nirvanaa</tspan>'
            f'<tspan fill="{C_DIM}">:</tspan>'
            f'<tspan fill="{C_PATH}">~</tspan>'
            f'<tspan fill="{C_DIM}">$ </tspan>'
            f'<tspan fill="{C_CMD}">neofetch</tspan>'
            f'</text>'
        )
    })

    # 2. JERRY Block ASCII (5 lines, Y = 90, 107, 124, 141, 158)
    ascii_lines = [
        "   ██   ███████  ██████   ██████   ██   ██",
        "   ██   ██       ██   ██  ██   ██   ██ ██ ",
        "   ██   █████    ██████   ██████     ███  ",
        "██ ██   ██       ██   ██  ██   ██     ██  ",
        " ████   ███████  ██   ██  ██   ██     ██  ",
    ]
    for i, line in enumerate(ascii_lines):
        y_pos = 90 + i * 17
        elements.append({
            "y": y_pos,
            "svg": (
                f'<text x="{PAD_X}" y="{y_pos}" font-family="{FONT_MONO}" font-size="13" '
                f'font-weight="bold" fill="{ASCII_ROW_COLORS[i]}" xml:space="preserve">'
                f'{escape(line)}</text>'
            )
        })

    # 3. Subtle Divider Line (Y = 186)
    elements.append({
        "y": 186,
        "svg": (
            f'<line x1="{PAD_X}" y1="186" x2="{W - PAD_X}" y2="186" '
            f'stroke="#21262d" stroke-width="1" stroke-dasharray="4 3"/>'
        )
    })

    # 4. Info Items (No "OS", "Role", "Kernel" labels)
    info_items = [
        ("✦", C_PROMPT_ICON, "Kushal Parakh", ' ("Jerry")'),
        ("✦", C_USER, "Full-Stack Developer & Builder", ""),
        ("✦", C_HOST, "Co-Founder @ Nirvanaa Studios", ""),
        ("✦", C_PATH, "B.Tech IT @ WIT, Solapur", ""),
        ("✦", C_CMD, "Cybersecurity · CTFs · Bug Bounty · IoT", ""),
        ("✦", C_BULLET, "React · Next.js · Node.js · Python · TS", ""),
        ("✦", C_BAR_CAFFEINE, "GCP · Firebase · MongoDB · Redis", ""),
        ("✦", "#e3b341", "20+ Shipped Products in Production", ""),
    ]

    for i, (icon, icon_color, main_text, sub_text) in enumerate(info_items):
        y_pos = 210 + i * 20
        sub_svg = f'<tspan fill="{C_DIM}">{escape(sub_text)}</tspan>' if sub_text else ""
        elements.append({
            "y": y_pos,
            "svg": (
                f'<text x="{PAD_X}" y="{y_pos}" font-family="{FONT_MONO}" font-size="12">'
                f'<tspan fill="{icon_color}" font-weight="bold">{icon} </tspan>'
                f'<tspan fill="{C_TEXT}">{escape(main_text)}</tspan>'
                f'{sub_svg}'
                f'</text>'
            )
        })

    # 5. Block-Style Progress Bars matching JERRY ASCII: Passion 100%, Caffeine 100%, Sleep 0%
    bars = [
        ("passion", 100, C_BAR_PASSION, 384),
        ("caffeine", 100, C_BAR_CAFFEINE, 408),
        ("sleep", 0, C_BAR_SLEEP, 432),
    ]

    BAR_X = 110
    NUM_BLOCKS = 24
    BLOCK_W = 8
    BLOCK_H = 11
    GAP = 2.8
    TOTAL_BAR_W = NUM_BLOCKS * (BLOCK_W + GAP) - GAP  # ~256px

    for name, pct, color, y_bar in bars:
        block_rects = build_block_bar_svg(
            x_start=BAR_X,
            y_top=y_bar,
            pct=pct,
            active_color=color,
            num_blocks=NUM_BLOCKS,
            block_w=BLOCK_W,
            block_h=BLOCK_H,
            gap=GAP,
            r=1
        )
        text_y = y_bar + 9.5
        elements.append({
            "y": y_bar,
            "svg": (
                f'<g>'
                # Label
                f'<text x="{PAD_X}" y="{text_y}" font-family="{FONT_MONO}" font-size="12" fill="{C_DIM}">{name}</text>'
                # Block Segments
                f'{block_rects}'
                # Percentage Text
                f'<text x="{BAR_X + TOTAL_BAR_W + 14}" y="{text_y}" font-family="{FONT_MONO}" font-size="12" font-weight="bold" fill="{color if pct > 0 else C_DIM}">{pct}%</text>'
                f'</g>'
            )
        })

    # 6. Japanese Quote & Translation (Y = 468)
    elements.append({
        "y": 468,
        "svg": (
            f'<text x="{PAD_X}" y="468" font-family="{FONT_MONO}" font-size="12">'
            f'<tspan fill="{C_JP}" font-weight="bold">七転び八起き</tspan>'
            f'<tspan fill="{C_DIM}" font-style="italic">  "Fall seven times, stand up eight."</tspan>'
            f'</text>'
        )
    })

    # 7. Active Bottom Prompt (Y = 496)
    elements.append({
        "y": 496,
        "svg": (
            f'<text x="{PAD_X}" y="496" font-family="{FONT_MONO}" font-size="13">'
            f'<tspan fill="{C_PROMPT_ICON}">⚡ </tspan>'
            f'<tspan fill="{C_USER}">jerry</tspan>'
            f'<tspan fill="{C_DIM}">@</tspan>'
            f'<tspan fill="{C_HOST}">nirvanaa</tspan>'
            f'<tspan fill="{C_DIM}">:$ </tspan>'
            f'<tspan fill="{C_USER}" class="cursor">█</tspan>'
            f'</text>'
        )
    })

    total_elements = len(elements)
    H = 520  # Total height perfectly calculated

    # ── CSS Keyframe Animation (Line by line reveal) ──
    step = REVEAL_TIME / max(total_elements - 1, 1)
    css = [
        "@keyframes rv{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}}",
        f".rw{{animation:rv {REVEAL_FADE}s cubic-bezier(0.16,1,0.3,1) both}}",
        "@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}",
        ".cursor{animation:blink 1s step-end infinite}",
    ]
    for i in range(total_elements):
        css.append(f".r{i}{{animation-delay:{i * step:.3f}s}}")

    style = f"<style>{''.join(css)}</style>"

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="Jerry Terminal Profile">'
        f'{style}'
    )

    # Window Background Frame
    parts.append(f'<rect width="{W}" height="{H}" rx="{CORNER_R}" fill="{BG}" stroke="{BORDER}" stroke-width="1"/>')

    # Window Title Bar
    parts.append(
        f'<path d="M 0,{CORNER_R} A {CORNER_R},{CORNER_R} 0 0 1 {CORNER_R},0 L {W - CORNER_R},0 '
        f'A {CORNER_R},{CORNER_R} 0 0 1 {W},{CORNER_R} L {W},{TITLE_BAR_H} L 0,{TITLE_BAR_H} Z" fill="{TITLE_BG}"/>'
    )
    parts.append(f'<line x1="0" y1="{TITLE_BAR_H}" x2="{W}" y2="{TITLE_BAR_H}" stroke="{BORDER}" stroke-width="1"/>')

    # Traffic Light Buttons
    dot_y = TITLE_BAR_H / 2
    for i, color in enumerate([DOT_RED, DOT_YEL, DOT_GRN]):
        parts.append(f'<circle cx="{18 + i * 18}" cy="{dot_y}" r="5" fill="{color}"/>')

    # Window Title
    parts.append(
        f'<text x="{W/2}" y="{dot_y + 4}" text-anchor="middle" '
        f'font-family="{FONT_MONO}" font-size="12" fill="{C_DIM}">'
        f'jerry@nirvanaa: ~ (zsh)</text>'
    )

    # Render each animated element
    for idx, el in enumerate(elements):
        parts.append(f'<g class="rw r{idx}">{el["svg"]}</g>')

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    svg = build_svg()
    out = "assets/terminal.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[OK] wrote {out} ({len(svg) / 1024:.1f} KB)")
