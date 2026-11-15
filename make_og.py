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
cx, cy, R = 905, 320, 235
d.ellipse((cx - R - 26, cy - R - 26, cx + R + 26, cy + R + 26), fill=INK + (30,))          # soft shadow
d.ellipse((cx - R - 18, cy - R - 18, cx + R + 18, cy + R + 18), fill=PAPER2)                # bowl rim
d.ellipse((cx - R - 18, cy - R - 18, cx + R + 18, cy + R + 18), outline=INK, width=5)
d.ellipse((cx - R + 18, cy - R + 18, cx + R - 18, cy + R - 18), fill=JOLLOF)                # jollof
d.ellipse((cx - R + 40, cy - R + 42, cx + R - 40, cy + R - 42), fill=JOLLOF2)               # lighter center
# rice grains as short cream dashes
for _ in range(300):
    a = random.uniform(0, 6.283); r = random.uniform(0, R - 55)
    x, y = cx + r * 0.97 * __import__("math").cos(a), cy + r * 0.9 * __import__("math").sin(a)
    a2 = random.uniform(0, 3.14)
    dx, dy = 6 * __import__("math").cos(a2), 6 * __import__("math").sin(a2)
    d.line([(x - dx, y - dy), (x + dx, y + dy)], fill=(252, 246, 230, 210), width=2)
# plantain slices: gold arcs on the rice
for (px, py) in [(cx - 90, cy - 60), (cx + 70, cy - 20), (cx - 20, cy + 85), (cx + 95, cy + 60), (cx - 105, cy + 30)]:
    d.ellipse((px - 26, py - 16, px + 26, py + 16), fill=GOLD, outline=(150, 110, 30), width=3)
# green flecks (peppers/onions)
for _ in range(34):
    a = random.uniform(0, 6.283); r = random.uniform(20, R - 60)
    x, y = cx + r * 0.95 * __import__("math").cos(a), cy + r * 0.88 * __import__("math").sin(a)
    d.ellipse((x - 4, y - 3, x + 4, y + 3), fill=PALM)

f_eye = font(["Arial Bold.ttf", "Helvetica.ttc"], 22)
f_title = font(["Georgia Bold.ttf", "Georgia Italic.ttf", "Georgia.ttf"], 118)
f_sub = font(["Georgia Italic.ttf", "Georgia.ttf"], 29)
f_nap = font(["Helvetica.ttc", "Arial.ttf"], 19)

d.text((70, 66), "LOCAL BITES · 700 LOCUST ST · DOWNTOWN DES MOINES", font=f_eye, fill=INK)
d.text((66, 128), "Mama Africa", font=f_title, fill=INK)
d.line([(70, 268), (520, 268)], fill=JOLLOF, width=6)
d.text((70, 292), "Liberian & West African kitchen", font=f_sub, fill=JOLLOF)
d.text((70, 336), "Jollof bowls built to order at lunch.", font=f_sub, fill=INK)
d.text((70, 374), "Egusi, fufu and greens at dinner.", font=f_sub, fill=INK)
d.text((70, 440), "Catering for parties, weddings and events", font=f_nap, fill=(90, 72, 52))
d.text((70, 468), "(515) 735-1141 · Des Moines, IA 50309", font=f_nap, fill=(90, 72, 52))

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
