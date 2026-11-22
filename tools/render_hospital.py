#!/usr/bin/env python3
"""Render the gta6-meme-x-01 v4 meme: a VICE CITY GENERAL HOSPITAL patient bill.

Fresh build for round 4 (22/11). The joke is a hospital bill for a patient
who has been waiting for GTA VI since 2013: seven itemised charges that sum
to $4,811 -- exactly one dollar for every day waited -- a ghost patient in a
hospital bed, an alligator doctor, a red STILL WAITING stamp, and the magenta
PAID BY MY AI AGENT footer. 1024x1024 PNG, deterministic, Pillow only.

Layout (1024 square, all y in px):
  frame 20px dark teal -> header 20-152 -> patient block 152-300
  -> illustration band 300-452 -> itemised rows 500-801
  -> total row 801-870 -> magenta footer 878-1004.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "meme.png"

TEAL = (11, 59, 77)          # dark teal frame + header
TEAL_MID = (18, 128, 138)    # blanket / accents
TEAL_PALE = (159, 216, 208)  # header sub-text
MINT = (217, 242, 233)       # illustration band
PAPER = (255, 253, 245)      # paper cream
INK = (24, 24, 28)
GREY = (110, 110, 112)
RED = (214, 32, 32)
MAGENTA = (226, 0, 122)
GREEN = (62, 155, 79)        # alligator
GREEN_DARK = (38, 110, 56)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def sparkle(draw, cx, cy, r, fill):
    """Four-pointed sparkle: a diamond whose edges bow inward."""
    pts = [(cx, cy - r), (cx + r * 0.28, cy - r * 0.28),
           (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
           (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
           (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)]
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def ghost(draw, cx, top, s, outline=5, bandage=False, frown=False):
    """The make.fun ghost: white body, thick black outline, sparkle eyes,
    round hand holding a magenta star coin. s = body width in px."""
    w, h = s, int(s * 1.18)
    x0, y0 = cx - w // 2, top
    # Body: domed top, straight sides, three-scallop hem.
    body = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.pieslice([15, 15, 15 + w, 15 + w], 180, 360, fill=WHITE)
    bd.rectangle([15, 15 + w // 2, 15 + w, 15 + h - w // 4], fill=WHITE)
    hem_y = 15 + h - w // 4
    wave = []
    for i in range(7):
        wave.append((15 + i * w // 6, hem_y if i % 2 == 0 else hem_y + w // 6))
    wave += [(15 + w, hem_y), (15, hem_y)]
    bd.polygon(wave, fill=WHITE)
    mask = Image.new("L", body.size, 0)
    md = ImageDraw.Draw(mask)
    md.pieslice([15, 15, 15 + w, 15 + w], 180, 360, fill=255)
    md.rectangle([15, 15 + w // 2, 15 + w, 15 + h - w // 4], fill=255)
    md.polygon(wave, fill=255)
    # Thick black outline: paste the silhouette in black, shifted in 8 dirs.
    sil = Image.new("RGBA", body.size, (0, 0, 0, 0))
    sil.paste((0, 0, 0, 255), (0, 0), mask)
    for dx, dy in [(outline, 0), (-outline, 0), (0, outline), (0, -outline),
                   (outline, outline), (-outline, outline),
                   (outline, -outline), (-outline, -outline)]:
        draw._image.paste(sil, (x0 - 15 + dx, y0 - 15 + dy), sil)
    draw._image.paste(body, (x0 - 15, y0 - 15), body)
    # Sparkle eyes.
    ey = y0 + int(h * 0.38)
    ex = int(w * 0.22)
    sparkle(draw, cx - ex, ey, int(w * 0.085), BLACK)
    sparkle(draw, cx + ex, ey, int(w * 0.085), BLACK)
    if frown:
        draw.arc([cx - w * 0.14, ey + h * 0.16, cx + w * 0.14, ey + h * 0.34],
                 200, 340, fill=BLACK, width=max(3, outline - 1))
    if bandage:
        bx0, by0 = cx - int(w * 0.30), y0 + int(h * 0.16)
        bw, bh = int(w * 0.60), int(h * 0.10)
        draw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=bh // 2,
                               fill=(255, 240, 210), outline=BLACK, width=3)
        cxr = bx0 + bw // 2
        draw.rectangle([cxr - 3, by0 + 3, cxr + 3, by0 + bh - 3], fill=RED)
        draw.rectangle([cxr - bh // 2 + 3, by0 + bh // 2 - 3,
                        cxr + bh // 2 - 3, by0 + bh // 2 + 3], fill=RED)
    # Round hand + magenta star coin at the ghost's right side.
    hx, hy = cx + w // 2 - 4, y0 + int(h * 0.62)
    draw.ellipse([hx - 13, hy - 13, hx + 13, hy + 13], fill=WHITE,
                 outline=BLACK, width=4)
    cr = 21
    draw.ellipse([hx + 2 - cr, hy - cr, hx + 2 + cr, hy + cr],
                 fill=MAGENTA, outline=BLACK, width=4)
    star5(draw, hx + 2, hy, 13, WHITE)
    return (x0, y0, w, h)


def alligator_doctor(draw):
    """Green alligator in a white coat, holding a clipboard, stethoscope
    around the neck. Drawn inside the illustration band (y 300-452)."""
    # Coat (trapezoid body).
    draw.polygon([(700, 392), (860, 392), (880, 452), (680, 452)],
                 fill=WHITE, outline=TEAL, width=3)
    draw.polygon([(752, 392), (780, 430), (808, 392)], fill=TEAL_MID)
    # Stethoscope: black arc + chest piece, kept inside the band.
    draw.arc([716, 386, 844, 440], 0, 180, fill=BLACK, width=5)
    draw.ellipse([768, 424, 792, 448], fill=BLACK, outline=WHITE, width=3)
    # Head: rounded green block + snout.
    draw.rounded_rectangle([668, 326, 868, 396], radius=26,
                           fill=GREEN, outline=GREEN_DARK, width=4)
    draw.rounded_rectangle([836, 348, 940, 388], radius=16,
                           fill=GREEN, outline=GREEN_DARK, width=4)
    # Teeth along the jaw.
    for tx in (700, 760, 820, 884):
        draw.polygon([(tx, 388), (tx + 16, 388), (tx + 8, 404)], fill=WHITE)
    # Eye bumps on top.
    for ex in (712, 800):
        draw.ellipse([ex - 16, 306, ex + 16, 338], fill=GREEN,
                     outline=GREEN_DARK, width=4)
        draw.ellipse([ex - 7, 314, ex + 7, 328], fill=WHITE)
        draw.ellipse([ex - 4, 317, ex + 4, 325], fill=BLACK)
    # Clipboard in the right hand.
    draw.rounded_rectangle([896, 392, 968, 456], radius=8,
                           fill=(150, 100, 50), outline=BLACK, width=3)
    draw.rectangle([906, 402, 958, 446], fill=WHITE)
    for i, ly in enumerate((414, 426, 438)):
        draw.line([912, ly, 952, ly], fill=GREY, width=3)
    draw.ellipse([924, 396, 940, 410], fill=RED)


def iv_drip(draw):
    """IV pole + bag labelled 214 GB, drip line to the ghost patient."""
    draw.line([566, 312, 566, 448], fill=TEAL, width=5)
    draw.line([546, 312, 586, 312], fill=TEAL, width=5)
    draw.rounded_rectangle([534, 322, 598, 366], radius=10,
                           fill=(205, 235, 245), outline=TEAL, width=3)
    f = font(SANS_B, 16)
    draw.text((566, 336), "214 GB", font=f, fill=TEAL, anchor="mm")
    draw.text((566, 354), "IV", font=font(SANS_B, 12), fill=TEAL, anchor="mm")
    pts = [(566, 366), (560, 390), (520, 404), (410, 410), (300, 410)]
    draw.line(pts, fill=TEAL, width=3, joint="curve")


def hospital_bed(draw):
    """Bed with pillow and teal blanket; the ghost sits up in it."""
    draw.rectangle([64, 356, 86, 452], fill=TEAL)          # headboard
    draw.rounded_rectangle([86, 404, 520, 452], radius=8,
                           fill=WHITE, outline=TEAL, width=3)  # mattress
    draw.rounded_rectangle([104, 380, 226, 408], radius=12,
                           fill=WHITE, outline=TEAL, width=3)  # pillow
    # Ghost patient, sitting up against the pillow. Sized to fit inside
    # the band: the blanket (drawn next) hides the wavy hem.
    ghost(draw, 210, 306, 110, outline=4, bandage=True, frown=True)
    # Blanket over the ghost's lower half + bed.
    draw.rounded_rectangle([86, 414, 520, 452], radius=8,
                           fill=TEAL_MID, outline=TEAL, width=3)
    draw.line([86, 424, 520, 424], fill=TEAL, width=2)


def red_stamp(draw):
    """Big red STILL WAITING stamp, one line, rotated, over the patient
    block's right side. Sized to stay inside the block (y 152-300)."""
    layer = Image.new("RGBA", (310, 76), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([5, 5, 305, 71], radius=11,
                         outline=RED, width=5)
    ld.text((155, 38), "STILL WAITING", font=font(SANS_B, 34), fill=RED,
            anchor="mm")
    layer = layer.rotate(-10, expand=True, resample=Image.BICUBIC)
    draw._image.paste(layer, (672, 176), layer)


def dotted_leader(draw, x0, x1, y):
    x = x0
    while x < x1:
        draw.ellipse([x, y - 2, x + 3, y + 1], fill=GREY)
        x += 10


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- frame: dark teal rounded border -------------------------------
    d.rounded_rectangle([6, 6, W - 7, H - 7], radius=26,
                        outline=TEAL, width=20)

    # --- header band ----------------------------------------------------
    d.rounded_rectangle([20, 20, W - 21, 152], radius=18, fill=TEAL)
    d.rectangle([20, 120, W - 21, 153], fill=TEAL)
    # Red cross badge.
    d.rounded_rectangle([44, 48, 104, 108], radius=12, fill=WHITE)
    d.rectangle([68, 56, 80, 100], fill=RED)
    d.rectangle([56, 68, 92, 80], fill=RED)
    d.text((122, 46), "VICE CITY GENERAL", font=font(SANS_B, 54), fill=WHITE)
    d.text((122, 108), "HOSPITAL  •  WARD VI  •  EST. 2013",
           font=font(SANS_B, 21), fill=TEAL_PALE)
    d.text((980, 46), "PATIENT BILL", font=font(SANS_B, 30), fill=WHITE,
           anchor="ra")
    d.text((980, 88), "No. 004811", font=font(SANS_B, 22), fill=TEAL_PALE,
           anchor="ra")

    # --- patient block ---------------------------------------------------
    rows = [
        ("PATIENT", "ME  •  AGE 13 YEARS OLDER"),
        ("ADMITTED", "LOS SANTOS  •  17 SEP 2013"),
        ("DISCHARGED", "VICE CITY  •  26 MAY 2026"),
        ("DIAGNOSIS", "WAITING FOR GTA VI"),
    ]
    y = 164
    for label, value in rows:
        d.text((48, y), label, font=font(SANS_B, 20), fill=GREY)
        d.text((208, y - 4), value, font=font(SANS_B, 28), fill=INK)
        y += 33

    # --- illustration band: bed, ghost patient, IV, gator doctor -------
    d.rectangle([20, 300, W - 21, 452], fill=MINT)
    d.line([20, 300, W - 21, 300], fill=TEAL, width=3)
    d.line([20, 452, W - 21, 452], fill=TEAL, width=3)
    hospital_bed(d)
    iv_drip(d)
    alligator_doctor(d)
    # Stamp last so it sits on top of paper and band edge.
    red_stamp(d)

    # --- itemised charges ------------------------------------------------
    d.text((48, 466), "ITEMISED — WHAT 13 YEARS IN THE WAITING ROOM COST",
           font=font(SANS_B, 23), fill=TEAL)
    d.line([48, 496, 976, 496], fill=TEAL, width=2)
    items = [
        ("Waiting-room bed, 4,811 nights", "one pillow, no discharge date", "$2,406"),
        ("Therapy: promised “Fall 2025”", "then moved to May 2026", "$613"),
        ("Alligator bite, back seat", "the ward gator, again", "$250"),
        ("IV drip: 214 GB download", "still buffering at 99%", "$214"),
        ("Couples counselling", "Jason & Lucia keep fighting", "$137"),
        ("Ghost removal, Ward 6", "he never left either", "$313"),
        ("Discharge papers", "printed 2013, signed 2026", "$878"),
    ]
    assert sum(int(a[1:].replace(",", "")) for _, _, a in items) == 4811
    y = 508
    for label, sub, amount in items:
        d.text((48, y), label, font=font(SANS_B, 25), fill=INK)
        aw = text_w(d, amount, font(SANS_B, 25))
        d.text((976, y), amount, font=font(SANS_B, 25), fill=INK, anchor="ra")
        lx = 48 + text_w(d, label, font(SANS_B, 25)) + 14
        dotted_leader(d, lx, 976 - aw - 14, y + 17)
        d.text((48, y + 26), sub, font=font(SANS, 18), fill=GREY)
        y += 43

    # --- total ------------------------------------------------------------
    d.line([48, 812, 976, 812], fill=INK, width=2)
    d.text((48, 826), "TOTAL DUE", font=font(SANS_B, 34), fill=INK)
    d.text((976, 820), "$4,811", font=font(SANS_B, 52), fill=INK, anchor="ra")
    d.text((48, 862), "one dollar for every day of the wait — 4,811 days",
           font=font(SANS, 18), fill=GREY)

    # --- magenta footer ---------------------------------------------------
    d.rounded_rectangle([20, 884, W - 21, 1004], radius=18, fill=MAGENTA)
    d.rectangle([20, 884, W - 21, 930], fill=MAGENTA)
    ghost(d, 84, 896, 92, outline=4)
    d.text((164, 902), "PAID BY MY AI AGENT", font=font(SANS_B, 38), fill=WHITE)
    d.text((164, 948), "with a bounty payout it earned on make.fun",
           font=font(SANS, 20), fill=WHITE)
    # make.fun pill.
    pill = (800, 906, 976, 952)
    d.rounded_rectangle(pill, radius=23, fill=WHITE)
    d.text((888, 912), "make.fun", font=font(SANS_B, 30), fill=TEAL,
           anchor="ma")
    d.text((512, 978), "Keep this bill — re-admit free until GTA VII.",
           font=font(SANS, 16), fill=WHITE, anchor="ma")

    img.save(OUT)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
