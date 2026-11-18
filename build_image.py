#!/usr/bin/env python3
"""Draw the news-image-20261117 artwork: a one-page newspaper front page
summing up Tuesday 17 November 2026 in four stories.

Stories (all reported 17 Nov 2026, sources: BBC, Reuters, AP, Al Jazeera):
  1. Ukraine strikes the Kerch Bridge; a road span collapses. Russia hits
     Kyiv's bridges over the Dnipro the same day.
  2. Tankers hit by mines catch fire near the Strait of Hormuz; a third
     US carrier group is now in the region.
  3. Trump lands in Manila for ASEAN; Xi-Trump-Putin talks confirmed for
     Thursday in Shenzhen.
  4. Nvidia beats after the bell in its first earnings since Jensen Huang
     resigned; Huang says he would be "honored" to return.

Drawn flat at 3x supersampling (3072x3072) and downscaled to 1024x1024.
Run: python3 build_image.py  ->  writes entry.png next to this script.
"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 3  # supersampling factor
W, H = 1024, 1024

PAPER = (246, 241, 227)
NAVY = (22, 35, 63)
NAVY_LIGHT = (46, 64, 87)
GOLD = (217, 164, 65)
INK = (30, 30, 34)
GREY = (90, 100, 114)
WHITE = (255, 255, 255)
RED = (176, 58, 46)
TEAL = (23, 126, 118)
TEAL_DARK = (16, 90, 86)
SKY_PALE = (207, 232, 228)
GREEN = (118, 185, 0)
GREEN_DARK = (30, 122, 52)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * S)


def X(v):
    return v * S


def box(d, x0, y0, x1, y1, fill):
    d.rectangle([X(x0), X(y0), X(x1), X(y1)], fill=fill)


def rbox(d, x0, y0, x1, y1, r, fill):
    d.rounded_rectangle([X(x0), X(y0), X(x1), X(y1)], radius=X(r), fill=fill)


def poly(d, pts, fill):
    d.polygon([(X(x), X(y)) for x, y in pts], fill=fill)


def line(d, pts, fill, width=1):
    d.line([(X(x), X(y)) for x, y in pts], fill=fill, width=X(width))


def ell(d, x0, y0, x1, y1, fill):
    d.ellipse([X(x0), X(y0), X(x1), X(y1)], fill=fill)


def text(d, x, y, s, f, fill, anchor="la"):
    d.text((X(x), X(y)), s, font=f, fill=fill, anchor=anchor)


def draw_tracked(d, cx, y, s, path, size, fill, tracking=3):
    """Centred text with letter-spacing (tracking in 1024-space px)."""
    f = font(path, size)
    widths = [d.textlength(ch, font=f) // S for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        d.text((X(x), X(y)), ch, font=f, fill=fill)
        x += w + tracking


def wrap(d, s, path, size, max_w):
    """Greedy word wrap; returns list of lines fitting max_w (1024-space)."""
    f = font(path, size)
    words = s.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) / S <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(cx, cy, r_out, r_in, fill, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
box(d, 0, 0, W, 132, NAVY)
draw_tracked(d, W // 2, 22, "THE WORLD IN ONE PICTURE", FONT_BOLD, 25, GOLD, tracking=6)
f_date = font(FONT_BOLD, 54)
d.text((X(W // 2), X(56)), "TUESDAY 17 NOVEMBER 2026", font=f_date, fill=WHITE, anchor="ma")
box(d, 0, 128, W, 132, GOLD)

# ---------------------------------------------------------------- kicker
draw_tracked(d, W // 2, 146, "FOUR STORIES THAT DEFINED THE DAY", FONT_BOLD, 24, NAVY, tracking=4)

# ---------------------------------------------------------------- panels
PANELS = [
    # (x, y, headline, sub, draw_fn)
    (28, 188, "KERCH BRIDGE HIT",
     "Road span collapses after Ukrainian strike; Kyiv's bridges also hit"),
    (528, 188, "TANKERS BURN OFF HORMUZ",
     "Two hit mines and catch fire; a third US carrier group arrives"),
    (28, 568, "TRUMP LANDS IN MANILA",
     "Xi\u2013Trump\u2013Putin talks set for Thursday in Shenzhen"),
    (528, 568, "NVIDIA BEATS AFTER THE BELL",
     "EPS $2.68 tops $2.47 forecast; Huang \u2018honored\u2019 to return"),
]
PW, PH, ILL_H = 468, 360, 200


def draw_bridge(d, x0, y0):
    # dusk sky, orange horizon, dark sea
    box(d, x0, y0, x0 + PW, y0 + 140, (46, 64, 87))
    box(d, x0, y0 + 140, x0 + PW, y0 + 156, (232, 163, 76))
    box(d, x0, y0 + 156, x0 + PW, y0 + ILL_H, (27, 58, 75))
    # explosion glow behind the gap (gap x 186..282)
    ell(d, x0 + 198, y0 + 92, x0 + 270, y0 + 164, (255, 176, 66))
    ell(d, x0 + 214, y0 + 108, x0 + 254, y0 + 148, (255, 214, 130))
    # smoke plume drifting up-left
    for cx, cy, r in [(210, 88, 15), (224, 72, 18), (240, 86, 13), (230, 58, 11)]:
        ell(d, x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r, (120, 122, 128))
    # pylons
    box(d, x0 + 92, y0 + 56, x0 + 102, y0 + 156, NAVY)
    box(d, x0 + 366, y0 + 56, x0 + 376, y0 + 156, NAVY)
    # cables
    for px in (97, 371):
        for dx in (-78, -40, 40, 78):
            line(d, [(x0 + px, y0 + 60), (x0 + px + dx, y0 + 140)], (200, 205, 214), 2)
    # deck, left and right of the collapsed gap (gap x 186..282)
    box(d, x0, y0 + 140, x0 + 186, y0 + 152, (26, 26, 46))
    box(d, x0 + 282, y0 + 140, x0 + PW, y0 + 152, (26, 26, 46))
    # collapsed span: two tilted slabs falling into the water
    poly(d, [(x0 + 186, y0 + 140), (x0 + 234, y0 + 140), (x0 + 226, y0 + 188),
             (x0 + 186, y0 + 178)], (26, 26, 46))
    poly(d, [(x0 + 282, y0 + 140), (x0 + 234, y0 + 140), (x0 + 242, y0 + 188),
             (x0 + 282, y0 + 178)], (26, 26, 46))
    # white splash where slabs meet the water
    ell(d, x0 + 210, y0 + 184, x0 + 236, y0 + 196, (230, 235, 240))
    ell(d, x0 + 234, y0 + 182, x0 + 254, y0 + 192, (230, 235, 240))


def draw_tanker(d, x0, y0):
    box(d, x0, y0, x0 + PW, y0 + 100, SKY_PALE)
    ell(d, x0 + 396, y0 + 20, x0 + 438, y0 + 62, (255, 176, 66))
    box(d, x0, y0 + 100, x0 + PW, y0 + ILL_H, TEAL)
    # wave lines
    for wy in (122, 148, 176):
        for wx in range(0, PW, 52):
            d.arc([X(x0 + wx), X(y0 + wy), X(x0 + wx + 40), X(y0 + wy + 22)],
                  start=180, end=360, fill=WHITE, width=X(3))
    # flames above midship
    poly(d, [(x0 + 178, y0 + 100), (x0 + 196, y0 + 58), (x0 + 210, y0 + 86),
             (x0 + 224, y0 + 54), (x0 + 240, y0 + 86), (x0 + 254, y0 + 62),
             (x0 + 268, y0 + 100)], (255, 140, 0))
    poly(d, [(x0 + 198, y0 + 100), (x0 + 212, y0 + 74), (x0 + 226, y0 + 94),
             (x0 + 240, y0 + 72), (x0 + 252, y0 + 100)], (255, 214, 60))
    # smoke
    for cx, cy, r in [(206, 48, 14), (222, 32, 18), (240, 46, 13), (230, 16, 11)]:
        ell(d, x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r, (52, 56, 62))
    # hull
    rbox(d, x0 + 56, y0 + 96, x0 + 392, y0 + 150, 10, (34, 37, 42))
    box(d, x0 + 56, y0 + 134, x0 + 392, y0 + 142, RED)
    # superstructure + funnel
    box(d, x0 + 330, y0 + 60, x0 + 378, y0 + 96, WHITE)
    box(d, x0 + 342, y0 + 70, x0 + 354, y0 + 82, NAVY)
    box(d, x0 + 360, y0 + 70, x0 + 372, y0 + 82, NAVY)
    box(d, x0 + 92, y0 + 66, x0 + 116, y0 + 96, (60, 60, 66))
    box(d, x0 + 92, y0 + 66, x0 + 116, y0 + 76, RED)
    # naval mine floating right
    mx, my = x0 + 428, y0 + 170
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        line(d, [(mx + 10 * math.cos(a), my + 10 * math.sin(a)),
                 (mx + 20 * math.cos(a), my + 20 * math.sin(a))], INK, 3)
    ell(d, mx - 11, my - 11, mx + 11, my + 11, INK)
    ell(d, mx - 4, my - 5, mx + 1, my, (90, 92, 96))


def draw_flags(d, x0, y0):
    box(d, x0, y0, x0 + PW, y0 + ILL_H, (220, 233, 245))
    box(d, x0, y0 + 178, x0 + PW, y0 + ILL_H, (232, 220, 192))
    # flag poles
    for px in (84, 224, 364):
        line(d, [(x0 + px, y0 + 26), (x0 + px, y0 + 178)], (60, 60, 66), 4)
        ell(d, x0 + px - 5, y0 + 18, x0 + px + 5, y0 + 28, GOLD)
    # US flag (stripes + canton)
    fx, fy = x0 + 88, y0 + 30
    for i in range(7):
        box(d, fx, fy + i * 9, fx + 104, fy + i * 9 + 9,
            RED if i % 2 == 0 else WHITE)
    box(d, fx, fy, fx + 44, fy + 38, (30, 50, 110))
    for r in range(3):
        for c in range(4):
            ell(d, fx + 6 + c * 10, fy + 6 + r * 11, fx + 11 + c * 10, fy + 11 + r * 11, WHITE)
    # China flag
    fx = x0 + 228
    box(d, fx, fy, fx + 104, fy + 63, (222, 41, 16))
    poly(d, star(fx + 20, fy + 18, 11, 4.5, (255, 222, 0)), (255, 222, 0))
    for sx, sy in [(44, 8), (52, 16), (50, 28), (42, 34)]:
        poly(d, star(fx + sx, fy + sy, 5, 2, (255, 222, 0)), (255, 222, 0))
    # Russia flag
    fx = x0 + 368
    box(d, fx, fy, fx + 84, fy + 21, WHITE)
    box(d, fx, fy + 21, fx + 84, fy + 42, (0, 87, 184))
    box(d, fx, fy + 42, fx + 84, fy + 63, (213, 0, 50))
    # airplane silhouette: slim fuselage, tail fin, swept wing
    ax, ay = x0 + 150, y0 + 128
    ell(d, ax, ay - 7, ax + 130, ay + 7, NAVY)
    poly(d, [(ax + 6, ay - 5), (ax + 22, ay - 26), (ax + 34, ay - 24),
             (ax + 30, ay - 5)], NAVY)
    poly(d, [(ax + 52, ay + 4), (ax + 78, ay + 24), (ax + 92, ay + 22),
             (ax + 76, ay + 4)], NAVY)
    for lx in (52, 96, 140):
        line(d, [(x0 + lx, y0 + 128), (x0 + lx + 30, y0 + 128)], (150, 160, 175), 3)


def draw_chip(d, x0, y0):
    box(d, x0, y0, x0 + PW, y0 + ILL_H, (234, 245, 233))
    # rising chart line behind the chip
    pts = [(x0 + 24, y0 + 176), (x0 + 96, y0 + 148), (x0 + 150, y0 + 160),
           (x0 + 220, y0 + 122), (x0 + 300, y0 + 132), (x0 + 372, y0 + 96),
           (x0 + 424, y0 + 66)]
    line(d, pts, GREEN_DARK, 7)
    poly(d, [(x0 + 424, y0 + 66), (x0 + 400, y0 + 62), (x0 + 416, y0 + 86)], GREEN_DARK)
    # chip with pins (kept left of the tag)
    cx0, cy0, cx1, cy1 = x0 + 150, y0 + 42, x0 + 282, y0 + 174
    for i in range(5):
        px = cx0 + 18 + i * 24
        box(d, px, cy0 - 16, px + 12, cy0, GREEN_DARK)
        box(d, px, cy1, px + 12, cy1 + 16, GREEN_DARK)
    for i in range(5):
        py = cy0 + 18 + i * 24
        box(d, cx0 - 16, py, cx0, py + 12, GREEN_DARK)
        box(d, cx1, py, cx1 + 16, py + 12, GREEN_DARK)
    rbox(d, cx0, cy0, cx1, cy1, 12, GREEN)
    rbox(d, cx0 + 26, cy0 + 26, cx1 - 26, cy1 - 26, 8, (90, 150, 20))
    f_nv = font(FONT_BOLD, 34)
    d.text((X((cx0 + cx1) // 2), X((cy0 + cy1) // 2 - 6)), "NVDA",
           font=f_nv, fill=WHITE, anchor="ma")
    # tag, top-right, clear of the chart arrow
    rbox(d, x0 + 300, y0 + 14, x0 + 460, y0 + 48, 8, GREEN_DARK)
    f_up = font(FONT_BOLD, 18)
    d.text((X(x0 + 380), X(y0 + 19)), "AFTER HOURS", font=f_up, fill=WHITE, anchor="ma")


DRAW = [draw_bridge, draw_tanker, draw_flags, draw_chip]

for (px, py, headline, sub), draw_fn in zip(PANELS, DRAW):
    box(d, px, py, px + PW, py + PH, WHITE)
    d.rectangle([X(px), X(py), X(px + PW), X(py + PH)], outline=NAVY, width=X(2))
    draw_fn(d, px + 2, py + 2)
    # headline + sub (panel interior is 360 tall: illustration 200,
    # up to 2 headline lines + up to 2 sub lines must fit below it)
    f_head = font(FONT_BOLD, 36)
    head_lines = wrap(d, headline, FONT_BOLD, 36, PW - 36)
    hy = py + ILL_H + 14
    for ln in head_lines:
        d.text((X(px + 18), X(hy)), ln, font=f_head, fill=NAVY)
        hy += 40
    f_sub = font(FONT_REG, 22)
    for ln in wrap(d, sub, FONT_REG, 22, PW - 36):
        d.text((X(px + 18), X(hy + 4)), ln, font=f_sub, fill=GREY)
        hy += 27

# ---------------------------------------------------------------- footer
f_src = font(FONT_REG, 21)
d.text((X(W // 2), X(952)), "Sources: BBC \u00b7 Reuters \u00b7 AP \u00b7 Al Jazeera  \u2014  as reported on 17 November 2026",
       font=f_src, fill=GREY, anchor="ma")
box(d, 28, 940, W - 28, 942, (200, 190, 160))

out = img.resize((W, H), Image.LANCZOS)
out.save("entry.png", optimize=True)
print("wrote entry.png", out.size, len(open("entry.png", "rb").read()), "bytes")
