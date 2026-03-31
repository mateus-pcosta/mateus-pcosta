from datetime import datetime, timezone, timedelta
import os

tz = timezone(timedelta(hours=-3))
now = datetime.now(tz)
time_str = now.strftime("%H:%M")

# Canvas
W, H      = 520, 210
BORDER    = 10
PANEL_GAP = 6
CLOCK_H   = 138

COLOR_ON  = '#00B9E1'
COLOR_OFF = '#001C26'

SEGS = {
    '0': 'abcdef',
    '1': 'bc',
    '2': 'abdeg',
    '3': 'abcdg',
    '4': 'bcfg',
    '5': 'acdfg',
    '6': 'acdefg',
    '7': 'abc',
    '8': 'abcdefg',
    '9': 'abcdfg',
}

def digit_rects(x, y, dw, dh, char):
    t = max(5, dw // 7)
    g = 3
    active = SEGS.get(char, '')

    def c(s):
        return COLOR_ON if s in active else COLOR_OFF

    return '\n  '.join([
        f'<rect x="{x+g+t}"    y="{y+g}"            width="{dw-2*(g+t)}"      height="{t}"              rx="2" fill="{c("a")}"/>',
        f'<rect x="{x+dw-g-t}" y="{y+g+t}"          width="{t}"               height="{dh//2-2*g-t}"    rx="2" fill="{c("b")}"/>',
        f'<rect x="{x+dw-g-t}" y="{y+dh//2+g}"      width="{t}"               height="{dh//2-2*g-t}"    rx="2" fill="{c("c")}"/>',
        f'<rect x="{x+g+t}"    y="{y+dh-g-t}"       width="{dw-2*(g+t)}"      height="{t}"              rx="2" fill="{c("d")}"/>',
        f'<rect x="{x+g}"      y="{y+dh//2+g}"      width="{t}"               height="{dh//2-2*g-t}"    rx="2" fill="{c("e")}"/>',
        f'<rect x="{x+g}"      y="{y+g+t}"          width="{t}"               height="{dh//2-2*g-t}"    rx="2" fill="{c("f")}"/>',
        f'<rect x="{x+g+t}"    y="{y+dh//2-t//2}"  width="{dw-2*(g+t)}"      height="{t}"              rx="2" fill="{c("g")}"/>',
    ])

# Digit positions
DW, DH = 82, 105
COL_W  = 26
GAP    = 6
total_w = 4 * DW + COL_W + 3 * GAP
sx = (W - total_w) // 2
sy = BORDER + (CLOCK_H - BORDER * 2 - DH) // 2

digits = time_str.replace(':', '')
h1, h2, m1, m2 = digits[0], digits[1], digits[2], digits[3]

x_h1 = sx
x_h2 = sx + DW + GAP
x_m1 = sx + 2*DW + 2*GAP + COL_W
x_m2 = sx + 3*DW + 3*GAP + COL_W

cx      = sx + 2*DW + 2*GAP + COL_W // 2
dot1_cy = sy + DH // 3
dot2_cy = sy + 2 * DH // 3

text_y      = CLOCK_H + PANEL_GAP
panel_h     = H - BORDER - text_y
text_svg_y  = text_y + (panel_h + 14) // 2

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%">
  <rect width="{W}" height="{H}" fill="#121212"/>
  <rect x="{BORDER}" y="{BORDER}" width="{W-2*BORDER}" height="{CLOCK_H-BORDER}" rx="4" fill="#060606" stroke="#323232" stroke-width="2"/>
  <rect x="{BORDER}" y="{text_y}" width="{W-2*BORDER}" height="{H-BORDER-text_y}" rx="4" fill="#0E2240" stroke="#323232" stroke-width="2"/>

  {digit_rects(x_h1, sy, DW, DH, h1)}
  {digit_rects(x_h2, sy, DW, DH, h2)}
  <circle cx="{cx}" cy="{dot1_cy}" r="5" fill="{COLOR_ON}"/>
  <circle cx="{cx}" cy="{dot2_cy}" r="5" fill="{COLOR_ON}"/>
  {digit_rects(x_m1, sy, DW, DH, m1)}
  {digit_rects(x_m2, sy, DW, DH, m2)}

  <text x="{W//2}" y="{text_svg_y}"
        text-anchor="middle"
        font-family="'DejaVu Sans', Arial, sans-serif"
        font-weight="bold"
        font-size="19"
        letter-spacing="3"
        fill="#D2D7DC">EVERY SECOND COUNTS</text>
</svg>'''

os.makedirs("assets", exist_ok=True)
with open("assets/clock.svg", "w") as f:
    f.write(svg)
