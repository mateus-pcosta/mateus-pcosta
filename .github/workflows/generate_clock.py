from datetime import datetime, timezone, timedelta
import os

tz = timezone(timedelta(hours=-3))
now = datetime.now(tz)
time_str = now.strftime("%H:%M")

# Canvas
W, H       = 420, 138
BORDER     = 8
CLOCK_H    = 95   # y where clock panel ends
PANEL_GAP  = 5
TEXT_Y     = CLOCK_H + PANEL_GAP
TEXT_BOT   = H - BORDER

COLOR_ON   = '#00CCEE'
COLOR_OFF  = '#00141C'

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

DW, DH = 66, 72
COL_W  = 20
GAP    = 5
total_w = 4 * DW + COL_W + 3 * GAP
sx = (W - total_w) // 2
sy = BORDER + (CLOCK_H - BORDER * 2 - DH) // 2

digits = time_str.replace(':', '')
h1, h2, m1, m2 = digits[0], digits[1], digits[2], digits[3]

positions = [
    sx,
    sx + DW + GAP,
    sx + 2*DW + 2*GAP + COL_W,
    sx + 3*DW + 3*GAP + COL_W,
]

def seg_groups(x, y, dw, dh, char):
    t = max(4, dw // 9)
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
        r = f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="2" fill="{{c}}"/>'
        if s in active:
            on.append(r.replace('{c}', COLOR_ON))
        else:
            off.append(r.replace('{c}', COLOR_OFF))
    return off, on

all_off, all_on = [], []
for pos, ch in zip(positions, [h1, h2, m1, m2]):
    o, n = seg_groups(pos, sy, DW, DH, ch)
    all_off.extend(o)
    all_on.extend(n)

cx     = sx + 2*DW + 2*GAP + COL_W // 2
dot_r  = 4
dot1_y = sy + DH // 3
dot2_y = sy + 2 * DH // 3

text_cy = TEXT_Y + (TEXT_BOT - TEXT_Y + 14) // 2

# Panel geometry
pw = W - 2*BORDER
cp_h = CLOCK_H - BORDER
tp_h = TEXT_BOT - TEXT_Y

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%">
  <defs>
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#3e3e3e"/>
      <stop offset="45%"  stop-color="#1a1a1a"/>
      <stop offset="100%" stop-color="#303030"/>
    </linearGradient>
    <linearGradient id="text-panel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#0f2448"/>
      <stop offset="100%" stop-color="#091830"/>
    </linearGradient>
  </defs>

  <!-- background -->
  <rect width="{W}" height="{H}" rx="6" fill="#0d0d0d"/>

  <!-- clock frame (metallic border) -->
  <rect x="{BORDER-2}" y="{BORDER-2}" width="{pw+4}" height="{cp_h+4}" rx="5" fill="url(#metal)"/>
  <!-- clock face -->
  <rect x="{BORDER+2}" y="{BORDER+2}" width="{pw-4}" height="{cp_h-4}" rx="3" fill="#040404"/>

  <!-- text frame -->
  <rect x="{BORDER-2}" y="{TEXT_Y-2}" width="{pw+4}" height="{tp_h+4}" rx="5" fill="url(#metal)"/>
  <!-- text face -->
  <rect x="{BORDER+2}" y="{TEXT_Y+2}" width="{pw-4}" height="{tp_h-4}" rx="3" fill="url(#text-panel)"/>

  <!-- dim segments -->
  {''.join(all_off)}

  <!-- active segments (glow) -->
  <g filter="url(#glow)">
    {''.join(all_on)}
  </g>

  <!-- colon -->
  <g filter="url(#glow)">
    <circle cx="{cx}" cy="{dot1_y}" r="{dot_r}" fill="{COLOR_ON}"/>
    <circle cx="{cx}" cy="{dot2_y}" r="{dot_r}" fill="{COLOR_ON}"/>
  </g>

  <!-- label -->
  <text x="{W//2}" y="{text_cy}"
        text-anchor="middle"
        font-family="Arial, Helvetica, sans-serif"
        font-weight="bold"
        font-size="14"
        letter-spacing="4"
        fill="#bbc8d4">EVERY SECOND COUNTS</text>
</svg>'''

os.makedirs("assets", exist_ok=True)
with open("assets/clock.svg", "w") as f:
    f.write(svg)
