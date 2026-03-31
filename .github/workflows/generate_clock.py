from datetime import datetime, timezone, timedelta
import os

tz = timezone(timedelta(hours=-3))
now = datetime.now(tz)
time_str = now.strftime("%H:%M")

W, H      = 440, 148
BORDER    = 9
CLOCK_H   = 99
PANEL_GAP = 6
TEXT_Y    = CLOCK_H + PANEL_GAP
TEXT_BOT  = H - BORDER

COLOR_ON  = '#F0F0F0'
COLOR_OFF = '#0e0e0e'

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

DW, DH = 70, 76
COL_W  = 22
GAP    = 6
total_w = 4 * DW + COL_W + 3 * GAP
sx = (W - total_w) // 2
sy = BORDER + (CLOCK_H - BORDER * 2 - DH) // 2

digits = time_str.replace(':', '')
h1, h2, m1, m2 = digits[0], digits[1], digits[2], digits[3]
positions = [sx, sx+DW+GAP, sx+2*DW+2*GAP+COL_W, sx+3*DW+3*GAP+COL_W]

def seg_groups(x, y, dw, dh, char):
    t = max(5, dw // 8)
    g = 3
    active = SEGS.get(char, '')
    half = dh // 2

    defs = [
        ('a', x+g+t,    y+g,          dw-2*(g+t), t),
        ('b', x+dw-g-t, y+g+t,        t,          half-2*g-t),
        ('c', x+dw-g-t, y+half+g,     t,          half-2*g-t),
        ('d', x+g+t,    y+dh-g-t,     dw-2*(g+t), t),
        ('e', x+g,      y+half+g,     t,          half-2*g-t),
        ('f', x+g,      y+g+t,        t,          half-2*g-t),
        ('g', x+g+t,    y+half-t//2,  dw-2*(g+t), t),
    ]

    off, on = [], []
    for s, rx, ry, rw, rh in defs:
        rect = f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="2"/>'
        (on if s in active else off).append(rect)
    return off, on

all_off, all_on = [], []
for pos, ch in zip(positions, [h1, h2, m1, m2]):
    o, n = seg_groups(pos, sy, DW, DH, ch)
    all_off.extend(o)
    all_on.extend(n)

cx     = sx + 2*DW + 2*GAP + COL_W // 2
dot1_y = sy + DH // 3
dot2_y = sy + 2 * DH // 3
dot_r  = 4

text_cy = TEXT_Y + (TEXT_BOT - TEXT_Y + 13) // 2

pw   = W - 2 * BORDER
cp_h = CLOCK_H - BORDER
tp_h = TEXT_BOT - TEXT_Y

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%">
  <defs>

    <!-- white glow for active segments -->
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- metallic border gradient (top-lit) -->
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#525252"/>
      <stop offset="30%"  stop-color="#222222"/>
      <stop offset="70%"  stop-color="#1a1a1a"/>
      <stop offset="100%" stop-color="#3a3a3a"/>
    </linearGradient>

    <!-- clock face: deep black with faint bottom vignette -->
    <linearGradient id="clock-face" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#060606"/>
      <stop offset="100%" stop-color="#020202"/>
    </linearGradient>

    <!-- text panel: dark charcoal -->
    <linearGradient id="text-face" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#1c1c1c"/>
      <stop offset="100%" stop-color="#111111"/>
    </linearGradient>

    <!-- scanline pattern for realism -->
    <pattern id="scanlines" x="0" y="0" width="1" height="3" patternUnits="userSpaceOnUse">
      <rect width="1" height="2" fill="none"/>
      <rect y="2" width="1" height="1" fill="#000" opacity="0.08"/>
    </pattern>

  </defs>

  <!-- outer shell -->
  <rect width="{W}" height="{H}" rx="6" fill="#0a0a0a"/>

  <!-- clock panel: metallic frame -->
  <rect x="{BORDER-3}" y="{BORDER-3}" width="{pw+6}" height="{cp_h+6}" rx="5" fill="url(#metal)"/>
  <!-- clock panel: inner face -->
  <rect x="{BORDER+2}" y="{BORDER+2}" width="{pw-4}" height="{cp_h-4}" rx="3" fill="url(#clock-face)"/>
  <!-- scanlines overlay -->
  <rect x="{BORDER+2}" y="{BORDER+2}" width="{pw-4}" height="{cp_h-4}" rx="3" fill="url(#scanlines)"/>

  <!-- text panel: metallic frame -->
  <rect x="{BORDER-3}" y="{TEXT_Y-3}" width="{pw+6}" height="{tp_h+6}" rx="5" fill="url(#metal)"/>
  <!-- text panel: inner face -->
  <rect x="{BORDER+2}" y="{TEXT_Y+2}" width="{pw-4}" height="{tp_h-4}" rx="3" fill="url(#text-face)"/>

  <!-- dim (inactive) segments -->
  <g fill="{COLOR_OFF}">
    {''.join(all_off)}
  </g>

  <!-- active segments with glow -->
  <g fill="{COLOR_ON}" filter="url(#glow)">
    {''.join(all_on)}
  </g>

  <!-- colon -->
  <g fill="{COLOR_ON}" filter="url(#glow)">
    <circle cx="{cx}" cy="{dot1_y}" r="{dot_r}"/>
    <circle cx="{cx}" cy="{dot2_y}" r="{dot_r}"/>
  </g>

  <!-- highlight: top edge reflection on clock panel -->
  <rect x="{BORDER+2}" y="{BORDER+2}" width="{pw-4}" height="2" rx="1" fill="#fff" opacity="0.04"/>

  <!-- label -->
  <text x="{W//2}" y="{text_cy}"
        text-anchor="middle"
        font-family="Arial, Helvetica, sans-serif"
        font-weight="bold"
        font-size="13"
        letter-spacing="5"
        fill="#909090">EVERY SECOND COUNTS</text>

</svg>'''

os.makedirs("assets", exist_ok=True)
with open("assets/clock.svg", "w") as f:
    f.write(svg)
