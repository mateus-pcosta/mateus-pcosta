from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=-3))
now = datetime.now(tz)
time_str = now.strftime("%H:%M")

W, H = 320, 110

img = Image.new("RGB", (W, H), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# Linha divisória
draw.rectangle([0, 57, W, 59], fill=(40, 40, 40))

# Tenta usar fonte monoespaçada, senão usa padrão
try:
    font_clock = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 42)
    font_text  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 15)
except:
    font_clock = ImageFont.load_default()
    font_text  = ImageFont.load_default()

# Hora
bbox = draw.textbbox((0, 0), time_str, font=font_clock)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) // 2, 6), time_str, font=font_clock, fill=(255, 255, 255))

# Frase
phrase = "EVERY SECOND COUNTS"
bbox2 = draw.textbbox((0, 0), phrase, font=font_text)
pw = bbox2[2] - bbox2[0]
draw.text(((W - pw) // 2, 68), phrase, font=font_text, fill=(255, 255, 255))

img.save(".github/workflows/clock.png")
