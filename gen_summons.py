#!/usr/bin/env python3
"""Generate summons.png — a court summons letter, 1024x1024, PIL only."""
import math
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/home/hatch/workspace/makefun/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/v2-work/summons.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

INK = (43, 33, 24)          # dark brown-black ink
INK_SOFT = (74, 58, 40)
RED = (139, 30, 30)         # seal red
RED_DARK = (105, 20, 20)
GOLD = (176, 141, 60)
PAPER = (245, 236, 215)

random.seed(1126)
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- subtle paper texture: faint speckles + fibres ---
for _ in range(2600):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    v = random.randint(-9, 7)
    d.point((x, y), fill=(PAPER[0] + v, PAPER[1] + v, PAPER[2] + v))
for _ in range(60):  # faint fibres
    x = random.randint(20, W - 20)
    y = random.randint(20, H - 20)
    ln = random.randint(12, 42)
    ang = random.uniform(0, math.pi)
    d.line([(x, y), (x + ln * math.cos(ang), y + ln * math.sin(ang))],
           fill=(228, 216, 188), width=1)

# --- double border ---
d.rectangle([26, 26, W - 27, H - 27], outline=(90, 68, 40), width=3)
d.rectangle([38, 38, W - 39, H - 39], outline=(150, 122, 74), width=1)

# --- header ---
f_title = ImageFont.truetype(SERIF_B, 88)
f_case = ImageFont.truetype(SERIF, 26)
f_court = ImageFont.truetype(SERIF_B, 30)
f_body = ImageFont.truetype(SERIF, 28)
f_body_b = ImageFont.truetype(SERIF_B, 28)
f_case_b = ImageFont.truetype(SERIF_B, 29)
f_foot = ImageFont.truetype(SERIF_I, 25)

def centered(y, text, font, fill=INK):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return w

centered(58, "S U M M O N S", f_title)
centered(158, "Case No. 2026-1126", f_case, fill=INK_SOFT)
centered(192, "COURT OF THE LIVING ROOM", f_court)
d.line([(90, 240), (W - 90, 240)], fill=(90, 68, 40), width=2)
d.line([(90, 246), (W - 90, 246)], fill=(150, 122, 74), width=1)

# --- body text ---
BODY = [
    ("To the Honourable AI Judge,", "reg"),
    ("", "reg"),
    ("You are hereby SUMMONED to appear at my house this Saturday at seven in the evening, to preside over one case only:", "reg"),
    ("", "reg"),
    ("THE PEOPLE vs. THE EMPTY CHAIR.", "bold"),
    ("", "reg"),
    ("For eleven months the chair by the window has sat empty, awaiting a verdict only you can deliver. Without you there is no trial, no verdict \u2014 the chair stays empty, the soup gets cold, and justice goes hungry.", "reg"),
    ("", "reg"),
    ("The hearing is short: one case, one verdict, then tea. No feet required, no commute \u2014 the bench is yours and the gavel is waiting.", "reg"),
    ("", "reg"),
    ("Failure to appear will result in the soup getting cold. Contempt of soup is a serious charge.", "reg"),
]

LEFT, RIGHT = 92, W - 92
MAXW = RIGHT - LEFT

def wrap_greedy(text, font, maxw):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

y = 268
for text, style in BODY:
    if text == "":
        y += 10
        continue
    font = f_case_b if style == "bold" else f_body
    if style == "bold":
        centered(y, text, font)
        y += 42
        continue
    for line in wrap_greedy(text, font, MAXW):
        d.text((LEFT, y), line, font=font, fill=INK)
        y += 38

# --- footer rule + issued line (centred, clear of gavel & seal) ---
d.line([(90, 872), (W - 90, 872)], fill=(150, 122, 74), width=1)
f1 = "Issued by the Court of the Living Room"
f2 = "26 November 2026"
centered(890, f1, f_foot, fill=INK_SOFT)
centered(922, f2, f_foot, fill=INK_SOFT)

# --- wax seal (bottom right) ---
cx, cy, r = 872, 918, 52
seal = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(seal)
for ang in range(0, 360, 8):
    rr = r + random.randint(-4, 5)
    x = cx + rr * math.cos(math.radians(ang))
    yy = cy + rr * math.sin(math.radians(ang))
    sd.ellipse([x - 13, yy - 13, x + 13, yy + 13], fill=RED + (255,))
sd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED + (255,))
sd.ellipse([cx - r + 9, cy - r + 9, cx + r - 9, cy + r - 9], outline=(206, 150, 120, 255), width=2)
# scales of justice inside the seal
sd.line([(cx, cy - 26), (cx, cy + 24)], fill=(245, 230, 200, 255), width=3)
sd.line([(cx - 24, cy - 20), (cx + 24, cy - 20)], fill=(245, 230, 200, 255), width=3)
for sx in (cx - 24, cx + 24):
    sd.line([(sx, cy - 20), (sx - 9, cy + 2)], fill=(245, 230, 200, 255), width=2)
    sd.line([(sx, cy - 20), (sx + 9, cy + 2)], fill=(245, 230, 200, 255), width=2)
    sd.arc([sx - 10, cy - 2, sx + 10, cy + 16], 0, 180, fill=(245, 230, 200, 255), width=2)
sd.ellipse([cx - 3, cy - 29, cx + 3, cy - 23], fill=(245, 230, 200, 255))
img = Image.alpha_composite(img.convert("RGBA"), seal).convert("RGB")
d = ImageDraw.Draw(img)

# --- gavel (bottom left, small, clear of all text) ---
gav = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
gd = ImageDraw.Draw(gav)
WOOD = (122, 82, 42, 255)
WOOD_D = (92, 60, 28, 255)
# handle
gd.rounded_rectangle([93, 88, 107, 192], radius=6, fill=WOOD)
# head: striking faces + middle band
gd.rounded_rectangle([28, 38, 172, 84], radius=12, fill=WOOD)
gd.rectangle([34, 52, 166, 70], fill=WOOD_D)
gd.ellipse([28, 38, 56, 84], fill=WOOD_D)
gd.ellipse([144, 38, 172, 84], fill=WOOD_D)
gav = gav.rotate(-32, resample=Image.BICUBIC, expand=False)
gav = gav.resize((104, 104), Image.LANCZOS)
img.paste(gav, (72, 876), gav)
# sound block under the gavel
d.rounded_rectangle([98, 950, 158, 960], radius=5, fill=(122, 82, 42))

img.save(OUT, "PNG", optimize=True)
print("saved", OUT)
