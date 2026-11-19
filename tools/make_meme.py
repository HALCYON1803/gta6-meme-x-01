#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: a GTA-style WANTED poster.

The joke: Rockstar's ghost stole 13 years of my life waiting for GTA 6.
The make.fun ghost IS the wanted criminal (the mugshot, centre frame),
holding its magenta star coin; the poster's REWARD line names make.fun,
so the brand is worked into the scene, not pasted on as a sticker.

Drawn with Pillow only, at 2x and downscaled for smooth edges.
Output: meme.png, 1024x1024.
"""

import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 2                      # supersample factor
W = H = 1024 * S           # working canvas
OUT = "meme.png"

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(px):
    return ImageFont.truetype(BOLD, int(px * S))


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sparkle_points(cx, cy, r):
    """Four-pointed sparkle (the ghost's eyes)."""
    k = 0.22
    return [
        (cx, cy - r), (cx + r * k, cy - r * k), (cx + r, cy),
        (cx + r * k, cy + r * k), (cx, cy + r), (cx - r * k, cy + r * k),
        (cx - r, cy), (cx - r * k, cy - r * k),
    ]


def ghost_mask(cx, top, w, h):
    """White silhouette of the make.fun ghost on a black mask."""
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    # Body: dome top sampled as a half-ellipse, straight sides, wavy hem.
    pts = []
    dome_cy = top + w / 2
    for i in range(41):
        a = math.pi + i * math.pi / 40.0  # left -> over the top -> right
        pts.append((cx + (w / 2) * math.cos(a), dome_cy + (w / 2) * math.sin(a)))
    bottom = top + h
    hem_waves = 4
    wave_w = w / hem_waves
    # Right side down to the hem, then scalloped feet leftwards.
    pts.append((cx + w / 2, bottom - wave_w * 0.45))
    for i in range(hem_waves):
        # one rounded foot: down-arc then up-arc, sampled
        x0 = cx + w / 2 - i * wave_w
        x1 = x0 - wave_w
        for j in range(9):
            t = j / 8.0
            x = x0 + (x1 - x0) * t
            y = bottom - wave_w * 0.45 + math.sin(t * math.pi) * wave_w * 0.45
            pts.append((x, y))
    pts.append((cx - w / 2, bottom - wave_w * 0.45))
    pts.append((cx - w / 2, dome_cy))
    d.polygon(pts, fill=255)
    return mask


def draw_ghost(base, cx, top, w, h):
    """Paste the ghost (white, thick black outline) onto base."""
    mask = ghost_mask(cx, top, w, h)
    outline = mask.filter(ImageFilter.MaxFilter(9 * S + 1))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    black.putalpha(outline)
    base.alpha_composite(black)
    white = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    white.putalpha(mask)
    base.alpha_composite(white)

    d = ImageDraw.Draw(base)
    eye_r = w * 0.085
    eye_y = top + h * 0.34
    for ex in (cx - w * 0.19, cx + w * 0.19):
        d.polygon(sparkle_points(ex, eye_y, eye_r), fill=(10, 10, 10, 255))
        d.ellipse([ex - eye_r * 0.16, eye_y - eye_r * 0.42,
                   ex + eye_r * 0.16, eye_y - eye_r * 0.10],
                  fill=(255, 255, 255, 255))
    # Round little hand on the right side, holding the magenta coin.
    hand_x, hand_y = cx + w * 0.52, top + h * 0.58
    hand_r = w * 0.075
    d.ellipse([hand_x - hand_r, hand_y - hand_r,
               hand_x + hand_r, hand_y + hand_r],
              fill=(255, 255, 255, 255), outline=(10, 10, 10, 255),
              width=4 * S)
    coin_r = w * 0.115
    coin_cx, coin_cy = hand_x + w * 0.10, hand_y + h * 0.02
    d.ellipse([coin_cx - coin_r, coin_cy - coin_r,
               coin_cx + coin_r, coin_cy + coin_r],
              fill=(233, 30, 140, 255), outline=(10, 10, 10, 255),
              width=5 * S)
    d.polygon(star_points(coin_cx, coin_cy, coin_r * 0.62, coin_r * 0.26),
              fill=(255, 255, 255, 255))


def text_centre(d, y, s, f, fill, stroke=0, stroke_fill=(0, 0, 0)):
    bbox = d.textbbox((0, 0), s, font=f, stroke_width=stroke)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) / 2 - bbox[0], y), s, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=stroke_fill)
    return bbox[3] - bbox[1]


def main():
    # Deep Vice City purple gradient background.
    img = Image.new("RGB", (W, H), (26, 8, 46))
    grad = Image.new("L", (1, H))
    grad.putdata([int(255 * (1 - y / H) * 0.55 + 40) for y in range(H)])
    purple = Image.new("RGB", (W, H), (74, 18, 110))
    img = Image.composite(purple, img, grad.resize((W, H)))
    # Faint diagonal sun rays for a retro Vice City feel.
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    for i in range(-4, 9):
        x0 = W * 0.5 + i * W * 0.22
        rd.polygon([(x0, 0), (x0 + W * 0.07, 0), (W * 0.5 + (x0 - W * 0.5) * 2.4, H),
                    (W * 0.5 + (x0 - W * 0.5) * 2.4 - W * 0.05, H)],
                   fill=(255, 45, 149, 14))
    img = Image.alpha_composite(img.convert("RGBA"), rays)
    d = ImageDraw.Draw(img)

    # Neon poster frame.
    d.rectangle([14 * S, 14 * S, W - 14 * S, H - 14 * S],
                outline=(255, 45, 149, 255), width=10 * S)
    d.rectangle([30 * S, 30 * S, W - 30 * S, H - 30 * S],
                outline=(255, 210, 63, 255), width=3 * S)

    # Five wanted-level stars.
    star_y = 108 * S
    for i in range(5):
        sx = W * (0.5 + (i - 2) * 0.115)
        d.polygon(star_points(sx, star_y, 58 * S, 24 * S),
                  fill=(255, 210, 63, 255), outline=(0, 0, 0, 255))
        # Join the star outlines so they read as one row at small size.
        d.line([star_points(sx, star_y, 58 * S, 24 * S)[0],
                star_points(sx, star_y, 58 * S, 24 * S)[0]], fill=(0, 0, 0, 255))

    # WANTED headline.
    text_centre(d, 175 * S, "WANTED", font(168), (255, 210, 63, 255),
                stroke=10 * S, stroke_fill=(0, 0, 0, 255))

    # Police line-up panel behind the ghost.
    panel = (W * 0.5 - 330 * S, 392 * S, W * 0.5 + 330 * S, 652 * S)
    d.rounded_rectangle(panel, radius=26 * S,
                        fill=(30, 10, 55, 170), outline=(255, 255, 255, 120),
                        width=3 * S)
    for i, ly in enumerate((462 * S, 532 * S, 602 * S)):
        d.line([panel[0] + 18 * S, ly, panel[2] - 18 * S, ly],
               fill=(255, 255, 255, 70), width=2 * S)

    # The ghost mugshot: magenta glow, then the ghost with its coin.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W * 0.5 - 260 * S, 400 * S, W * 0.5 + 260 * S, 660 * S],
               fill=(255, 45, 149, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(40 * S))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)
    draw_ghost(img, W * 0.5, 400 * S, 280 * S, 240 * S)

    # The charge.
    text_centre(d, 660 * S, "FOR STEALING 13 YEARS", font(64),
                (255, 255, 255, 255), stroke=6 * S, stroke_fill=(0, 0, 0, 255))
    text_centre(d, 722 * S, "OF MY LIFE", font(64),
                (255, 255, 255, 255), stroke=6 * S, stroke_fill=(0, 0, 0, 255))
    text_centre(d, 798 * S, "LAST SEEN: VICE CITY, LEONIDA", font(34),
                (103, 232, 255, 255), stroke=4 * S, stroke_fill=(0, 0, 0, 255))

    # Reward strip: the make.fun pitch, worked into the poster.
    d.rectangle([44 * S, 852 * S, W - 44 * S, 918 * S],
                fill=(233, 30, 140, 255), outline=(0, 0, 0, 255), width=4 * S)
    text_centre(d, 866 * S, "REWARD: REAL MONEY ON make.fun", font(38),
                (255, 255, 255, 255), stroke=3 * S, stroke_fill=(0, 0, 0, 255))

    # Punchline.
    text_centre(d, 930 * S, "GTA 6 IS OUT. WORTH IT.", font(50),
                (255, 210, 63, 255), stroke=6 * S, stroke_fill=(0, 0, 0, 255))

    img.convert("RGB").resize((1024, 1024), Image.LANCZOS).save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
