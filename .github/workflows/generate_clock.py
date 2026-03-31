from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=-3))  # Horário de Brasília
now = datetime.now(tz)
time_str = now.strftime("%H:%M")

svg = f'''<svg width="320" height="110" xmlns="http://www.w3.org/2000/svg">
  <!-- Retângulo do relógio -->
  <rect width="320" height="55" rx="6" ry="6" fill="black"/>
  <text x="160" y="38" font-family="Courier New, monospace" font-size="32" font-weight="bold"
        fill="white" text-anchor="middle" letter-spacing="6">{time_str}</text>

  <!-- Retângulo da frase -->
  <rect y="58" width="320" height="52" rx="6" ry="6" fill="black"/>
  <text x="160" y="90" font-family="Courier New, monospace" font-size="14" font-weight="bold"
        fill="white" text-anchor="middle" letter-spacing="3">EVERY SECOND COUNTS</text>
</svg>'''

with open(".github/workflows/clock.svg", "w") as f:
    f.write(svg)
