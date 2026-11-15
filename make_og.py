#!/usr/bin/env python3
"""og.png 1200x630 — Mama Africa: jollof-warm art, overhead bowl of jollof with rice-grain
dashes, West African chevron bands top and bottom. Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os, random

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

def font(path_names, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in path_names:
            p = b + n
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    return ImageFont.load_default()

INK = (36, 29, 22); PAPER = (250, 244, 232); PAPER2 = (243, 233, 214)
JOLLOF = (196, 73, 16); JOLLOF2 = (224, 103, 31); PALM = (47, 107, 69); GOLD = (217, 164, 65)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# warm wash: deeper toward bottom-left
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(PAPER[0] - int(6 * t), PAPER[1] - int(10 * t), PAPER[2] - int(18 * t)))

random.seed(7)
# chevron textile bands, top and bottom (diamond checker in lane colors)
def chevron_band(y0, cell, alpha):
    cols = [JOLLOF, GOLD, PALM, INK]
    for row in range(2):
        yy = y0 + row * cell
        for i in range(-1, W // cell + 2):
            xx = i * cell + (row % 2) * (cell // 2)
            c = cols[(i + row * 3) % 4]
            d.polygon([(xx, yy + cell // 2), (xx + cell // 2, yy), (xx + cell, yy + cell // 2), (xx + cell // 2, yy + cell)], fill=c + (alpha,))
chevron_band(0, 26, 255)
chevron_band(H - 52, 26, 255)

# overhead jollof bowl on the right: cream bowl, jollof disc, rice-grain dashes
import math
cx, cy, R = 958, 330, 195
d.ellipse((cx - R - 24, cy - R - 24, cx + R + 24, cy + R + 24), fill=INK + (30,))          # soft shadow
d.ellipse((cx - R - 16, cy - R - 16, cx + R + 16, cy + R + 16), fill=PAPER2)                # bowl rim
d.ellipse((cx - R - 16, cy - R - 16, cx + R + 16, cy + R + 16), outline=INK, width=5)
d.ellipse((cx - R + 16, cy - R + 16, cx + R - 16, cy + R - 16), fill=JOLLOF)                # jollof
d.ellipse((cx - R + 42, cy - R + 44, cx + R - 42, cy + R - 44), fill=JOLLOF2)               # lighter center
# rice grains as short cream dashes — area-uniform annulus sampling keeps the center clean
for _ in range(240):
    a = random.uniform(0, 6.283)
    r = (R - 48) * math.sqrt(random.uniform(0.18, 1.0)) + 12
    x, y = cx + r * 0.94 * math.cos(a), cy + r * 0.87 * math.sin(a)
    a2 = random.uniform(0, 3.14)
    dx, dy = 5 * math.cos(a2), 5 * math.sin(a2)
    d.line([(x - dx, y - dy), (x + dx, y + dy)], fill=(252, 246, 230, 210), width=2)
# plantain slices: gold arcs on the rice
for (px, py) in [(cx - 78, cy - 48), (cx + 62, cy - 12), (cx - 14, cy + 70), (cx + 82, cy + 52), (cx - 92, cy + 24)]:
    d.ellipse((px - 24, py - 15, px + 24, py + 15), fill=GOLD, outline=(150, 110, 30), width=3)
# green flecks (peppers/onions)
for _ in range(30):
    a = random.uniform(0, 6.283)
    r = (R - 55) * math.sqrt(random.uniform(0.25, 1.0)) + 14
    x, y = cx + r * 0.93 * math.cos(a), cy + r * 0.86 * math.sin(a)
    d.ellipse((x - 4, y - 3, x + 4, y + 3), fill=PALM)

f_eye = font(["Arial Bold.ttf", "Helvetica.ttc"], 22)
f_title = font(["Georgia Bold.ttf", "Georgia Italic.ttf", "Georgia.ttf"], 96)
f_sub = font(["Georgia Italic.ttf", "Georgia.ttf"], 29)
f_nap = font(["Helvetica.ttc", "Arial.ttf"], 19)

TITLE = "Mama Africa"
twd = d.textlength(TITLE, font=f_title)
assert twd < 700, f"title width {twd} would collide with the bowl"
d.text((70, 66), "LOCAL BITES · 700 LOCUST ST · DOWNTOWN DES MOINES", font=f_eye, fill=INK)
d.text((66, 132), TITLE, font=f_title, fill=INK)
d.line([(70, 252), (70 + twd, 252)], fill=JOLLOF, width=6)
d.text((70, 278), "Liberian & West African kitchen", font=f_sub, fill=JOLLOF)
d.text((70, 322), "Jollof bowls built to order at lunch.", font=f_sub, fill=INK)
d.text((70, 360), "Egusi, fufu and greens at dinner.", font=f_sub, fill=INK)
d.text((70, 436), "Catering for parties, weddings and events", font=f_nap, fill=(90, 72, 52))
d.text((70, 464), "(515) 735-1141 · Des Moines, IA 50309", font=f_nap, fill=(90, 72, 52))

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
