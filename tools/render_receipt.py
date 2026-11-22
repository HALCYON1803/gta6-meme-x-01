#!/usr/bin/env python3
"""Render the gta6-meme-x-01 v2 meme: a Vice City Games pre-order receipt.

The gag, in one second: you pre-ordered a game in 2013, picked it up in
2026, waited 4,811 days, paid with 13 years of your life, and your AI
agent covered the $0 balance. Receipt format because the leaderboard
top 8 are all fake official documents (receipt/bill/citation/obituary)
itemising the 4,811-day wait with an AI-agent-pays punchline.

Usage: python3 tools/render_receipt.py [output.png]
Deterministic: same input -> byte-identical PNG.
"""

import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

INK = (18, 18, 18)
GRAY = (110, 110, 110)
PAPER = (253, 253, 247)
PINK = (233, 30, 99)
BG_TOP = (43, 10, 78)
BG_BOT = (20, 4, 42)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def center(draw, y, s, f, fill=INK, x0=0, x1=W):
    w = text_w(draw, s, f)
    draw.text(((x0 + x1 - w) / 2, y), s, font=f, fill=fill)
    return y + f.size


def dashed(draw, y, x0, x1, color=GRAY, dash=14, gap=10):
    x = x0
    while x < x1:
        draw.line([(x, y), (min(x + dash, x1), y)], fill=color, width=2)
        x += dash + gap


def dotted_leader(draw, y, x0, x1, color=GRAY):
    x = x0
    while x < x1:
        draw.ellipse([x, y - 2, x + 4, y + 2], fill=color)
        x += 12


def row(draw, y, label, value, x0, x1, lf, vf):
    """One receipt row: label left, dotted leader, value right."""
    draw.text((x0, y), label, font=lf, fill=GRAY)
    vw = text_w(draw, value, vf)
    lw = text_w(draw, label, lf)
    dotted_leader(draw, y + vf.size // 2, x0 + lw + 16, x1 - vw - 16)
    draw.text((x1 - vw, y), value, font=vf, fill=INK)
    return y + vf.size + 14


def zigzag_paper():
    """White receipt sheet with torn zigzag top/bottom edges."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, x1, y0, y1 = 72, 952, 56, 968
    tooth_w, tooth_h = 22, 12
    top, bot = [], []
    x = x0
    while x < x1:
        top.append((x, y0))
        top.append((min(x + tooth_w // 2, x1), y0 - tooth_h))
        x += tooth_w
    top.append((x1, y0))
    x = x1
    while x > x0:
        bot.append((x, y1))
        bot.append((max(x - tooth_w // 2, x0), y1 + tooth_h))
        x -= tooth_w
    bot.append((x0, y1))
    d.polygon([(x0, y0)] + top + [(x1, y0), (x1, y1)] + bot + [(x0, y1)],
              fill=PAPER + (255,))
    return layer


def main(out_path):
    img = Image.new("RGB", (W, H), BG_TOP)
    bg = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        bg.line([(0, y), (W, y)],
                fill=tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t)
                           for i in range(3)))
    # faint diagonal stripes for a Vice City neon-night feel
    for k in range(-4, 12):
        x = k * 160
        bg.polygon([(x, 0), (x + 60, 0), (x + 60 - 420, H), (x - 420, H)],
                   fill=(58, 16, 96))

    # soft shadow under the paper
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([84, 72, 964, 980], radius=4,
                                             fill=(0, 0, 0, 90))
    img = Image.alpha_composite(img.convert("RGBA"), shadow)
    img = Image.alpha_composite(img, zigzag_paper())
    d = ImageDraw.Draw(img)

    X0, X1 = 124, 900  # text margins inside the paper
    y = 96
    y = center(d, y, "VICE CITY GAMES", font(MONO_B, 58)) + 8
    y = center(d, y, "OCEAN DRIVE  •  VICE CITY, LEONIDA",
               font(MONO, 25), fill=GRAY) + 18
    dashed(d, y, X0, X1)
    y += 18
    y = center(d, y, "PRE-ORDER RECEIPT", font(MONO_B, 36)) + 12
    d.text((X0, y), "RECEIPT #0004811", font=font(MONO, 24), fill=GRAY)
    s = "CASHIER: MY AI AGENT"
    d.text((X1 - text_w(d, s, font(MONO, 24)), y), s,
           font=font(MONO, 24), fill=GRAY)
    y += 44
    dashed(d, y, X0, X1)
    y += 26

    lf, vf = font(MONO, 28), font(MONO_B, 30)
    y = row(d, y, "PRE-ORDERED", "GTA V  —  17 SEP 2013", X0, X1, lf, vf)
    y = row(d, y, "PICKED UP", "GTA VI  —  26 MAY 2026", X0, X1, lf, vf)
    y += 10

    # the anchor gag: the number is the joke
    y = center(d, y, "WAIT TIME", font(MONO, 30), fill=GRAY) + 2
    y = center(d, y, "4,811 DAYS", font(MONO_B, 104)) + 6
    dashed(d, y, X0, X1)
    y += 24
    y = row(d, y, "TOTAL PAID", "13 YEARS OF MY LIFE", X0, X1, lf, vf)
    y = row(d, y, "BALANCE DUE", "$0.00", X0, X1, lf, vf)
    y += 8
    dashed(d, y, X0, X1)
    y += 22
    y = center(d, y, "PAID BY MY AI AGENT", font(MONO_B, 34)) + 4
    y = center(d, y, "MAKE.FUN BOUNTY", font(MONO_B, 30), fill=PINK) + 26

    # barcode
    import random
    rnd = random.Random(4811)
    bx, bw, bh = 312, 400, 72
    x = bx
    while x < bx + bw:
        wdt = rnd.choice([2, 3, 4, 6, 8])
        if rnd.random() < 0.55:
            d.rectangle([x, y, x + wdt, y + bh], fill=INK)
        x += wdt + rnd.choice([2, 3, 4])
    y += bh + 14

    # big PAID stamp, rotated, over the barcode (decorative) at the foot
    # of the receipt — never over the "4,811 DAYS" anchor or the punch
    # lines above it. The stamp sits half off the paper's bottom edge,
    # like a real rubber stamp that missed.
    stamp = Image.new("RGBA", (440, 140), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([6, 6, 434, 134], radius=16,
                         outline=PINK + (235,), width=9)
    sd.text((220 - text_w(sd, "PAID", font(MONO_B, 84)) / 2, 30),
            "PAID", font=font(MONO_B, 84), fill=PINK + (235,))
    stamp = stamp.rotate(-16, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(stamp, (292, 785))

    img.convert("RGB").save(out_path, "PNG")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "meme.png")
