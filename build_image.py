#!/usr/bin/env python3
"""Draws entry.png: one front page that sums up Tuesday 17 November 2026.

Stories (verified against five independent day-briefs of 2026-11-17):
  hero  Ukraine strikes the Kerch Bridge again; a road span collapses;
        Russia hits Kyiv's Dnipro bridges; 1,336 drones intercepted.
  col 1 Tankers hit mines in the Strait of Hormuz; a third US carrier arrives.
  col 2 Xi, Trump and Putin to meet in Shenzhen (confirmed for Thursday);
        Trump opens his Asia trip in Manila.
  col 3 Nvidia reels after Jensen Huang's exit; US closes an AI-chip loophole.
  wire  Vulcan rocket failure destroys 40 Amazon Leo satellites;
        JPMorgan blames a software bug for the banking outage;
        Pentagon fails its financial audit for the ninth straight year.

Deterministic: pure PIL drawing, no randomness, no network.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_BOOK = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (246, 239, 221)
INK = (22, 22, 22)
RED = (179, 49, 42)
NAVY = (34, 74, 99)
SEA = (40, 83, 107)
SKY_TOP = (216, 148, 84)
SKY_BOT = (243, 205, 148)
SMOKE = (96, 99, 105)
FIRE = (224, 110, 44)
GOLD = (214, 164, 60)
WHITE = (250, 248, 240)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w, min_size=14):
    """Largest font size <= size whose text fits max_w."""
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, min_size)


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, f, fill):
    draw.text((cx - draw.textlength(text, font=f) / 2, y), text, font=f, fill=fill)


# ---------------------------------------------------------------- masthead
def masthead(d):
    d.rectangle([0, 0, W, H], fill=PAPER)
    d.line([36, 26, 988, 26], fill=INK, width=3)
    f_small = font(SANS, 25)
    centered(d, 512, 36, "T H E   W O R L D   I N   O N E   D A Y", f_small, INK)
    f_date = fit(d, "TUESDAY 17 NOVEMBER 2026", SERIF, 66, 952)
    centered(d, 512, 66, "TUESDAY 17 NOVEMBER 2026", f_date, INK)
    d.line([36, 140, 988, 140], fill=RED, width=5)
    d.line([36, 149, 988, 149], fill=INK, width=2)


# ---------------------------------------------------------------- hero scene
def hero(d):
    x0, y0, x1, y1 = 36, 162, 988, 452
    for i in range(y1 - y0):  # dawn sky
        t = i / (y1 - y0)
        c = tuple(int(SKY_TOP[j] + (SKY_BOT[j] - SKY_TOP[j]) * t) for j in range(3))
        d.line([x0, y0 + i, x1, y0 + i], fill=c)
    sea_y = y0 + 208
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for wx in range(x0 + 18, x1 - 30, 64):  # wave ticks
        d.arc([wx, sea_y + 34, wx + 30, sea_y + 52], 0, 180, fill=(120, 170, 190), width=3)
        d.arc([wx + 26, sea_y + 62, wx + 56, sea_y + 80], 0, 180, fill=(120, 170, 190), width=3)
    # bridge: piers, deck, arch truss
    deck_y = y0 + 168
    for px in (x0 + 90, x0 + 300, x0 + 560, x0 + 790):
        d.rectangle([px, deck_y, px + 16, sea_y + 66], fill=(52, 52, 58))
    d.rectangle([x0 + 8, deck_y - 10, x0 + 470, deck_y + 4], fill=(52, 52, 58))
    d.rectangle([x0 + 640, deck_y - 10, x1 - 8, deck_y + 4], fill=(52, 52, 58))
    for tx in range(x0 + 30, x0 + 450, 42):  # truss diagonals, intact side
        d.line([tx, deck_y - 10, tx + 21, deck_y - 44], fill=(52, 52, 58), width=5)
        d.line([tx + 21, deck_y - 44, tx + 42, deck_y - 10], fill=(52, 52, 58), width=5)
    d.line([x0 + 20, deck_y - 44, x0 + 470, deck_y - 44], fill=(52, 52, 58), width=5)
    # the fallen span: tilted deck sinking between the gap piers
    d.polygon([(x0 + 486, deck_y - 2), (x0 + 624, deck_y + 52), (x0 + 618, deck_y + 68),
               (x0 + 482, deck_y + 14)], fill=(40, 40, 46))
    # explosion burst at the break + splash arcs where the span hit the water
    bx, by = x0 + 500, deck_y - 8
    for a in range(0, 360, 30):
        import math
        r1 = 26 if a % 60 == 0 else 16
        d.line([bx, by, bx + int(r1 * math.cos(math.radians(a))),
                by + int(r1 * math.sin(math.radians(a)))], fill=FIRE, width=6)
    d.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=GOLD)
    for sx in (x0 + 520, x0 + 566, x0 + 612):
        d.arc([sx, sea_y + 6, sx + 44, sea_y + 34], 180, 360, fill=WHITE, width=4)
    # smoke plume (kept inside the panel)
    for cx, cy, r in ((x0 + 540, deck_y - 52, 26), (x0 + 566, deck_y - 92, 36),
                      (x0 + 600, deck_y - 122, 44)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    # two drones
    for dx, dy in ((x0 + 320, y0 + 44), (x0 + 790, y0 + 30)):
        d.line([dx - 22, dy, dx + 22, dy], fill=INK, width=5)
        d.line([dx, dy - 8, dx, dy + 8], fill=INK, width=5)
        d.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=INK)
    # kicker tag
    d.rectangle([x0 + 14, y0 + 12, x0 + 236, y0 + 48], fill=RED)
    d.text((x0 + 26, y0 + 17), "EUROPE · THE WAR", font=font(SANS, 22), fill=WHITE)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)


def hero_text(d):
    f = fit(d, "UKRAINE STRIKES THE KERCH BRIDGE AGAIN", SANS, 47, 952)
    centered(d, 512, 464, "UKRAINE STRIKES THE KERCH BRIDGE AGAIN", f, INK)
    sub = ("Second strike in 24 hours: a road span drops into the sea, as Russia "
           "hits Kyiv's bridges and 1,336 drones are intercepted.")
    f_sub = font(SANS_BOOK, 23)
    y = 522
    for line in wrap(d, sub, f_sub, 940):
        centered(d, 512, y, line, f_sub, (60, 58, 52))
        y += 30
    d.line([36, 592, 988, 592], fill=INK, width=3)


# ---------------------------------------------------------------- columns
def col_hormuz(d, x0):
    y0 = 612
    d.rectangle([x0, y0, x0 + 296, y0 + 108], fill=SEA)
    # tanker hull + superstructure
    d.polygon([(x0 + 30, y0 + 66), (x0 + 250, y0 + 66), (x0 + 228, y0 + 88),
               (x0 + 52, y0 + 88)], fill=(30, 30, 34))
    d.rectangle([x0 + 56, y0 + 48, x0 + 210, y0 + 66], fill=(120, 60, 40))
    d.rectangle([x0 + 196, y0 + 30, x0 + 224, y0 + 66], fill=(70, 70, 76))
    # fire + smoke amidships (kept inside the panel)
    d.ellipse([x0 + 118, y0 + 26, x0 + 158, y0 + 58], fill=FIRE)
    d.ellipse([x0 + 128, y0 + 16, x0 + 150, y0 + 40], fill=GOLD)
    d.ellipse([x0 + 130, y0 + 2, x0 + 172, y0 + 30], fill=SMOKE)
    # mine
    d.ellipse([x0 + 238, y0 + 78, x0 + 262, y0 + 102], fill=INK)
    for a in range(0, 360, 45):
        import math
        dx = int(15 * math.cos(math.radians(a)))
        dy = int(15 * math.sin(math.radians(a)))
        d.line([x0 + 250 + dx // 2, y0 + 90 + dy // 2, x0 + 250 + dx, y0 + 90 + dy], fill=INK, width=3)
    # carrier silhouette on the horizon
    d.rectangle([x0 + 18, y0 + 8, x0 + 96, y0 + 16], fill=(40, 48, 60))
    d.rectangle([x0 + 62, y0 + 0, x0 + 78, y0 + 8], fill=(40, 48, 60))
    d.rectangle([x0, y0, x0 + 296, y0 + 108], outline=INK, width=3)
    return "MIDDLE EAST · THE GULF", "TANKERS HIT MINES IN THE STRAIT OF HORMUZ", \
        "Iran says two tankers ablaze; a third US carrier arrives."


def col_summit(d, x0):
    y0 = 612
    d.rectangle([x0, y0, x0 + 296, y0 + 108], fill=(233, 224, 198))
    flags = [(196, 40, 44, (196, 40, 44)), (36, 58, 120, (36, 58, 120)), (238, 238, 238, (238, 238, 238))]
    # three flag poles: China red, US navy w/ star field suggestion, Russia white-blue-red
    poles = [x0 + 58, x0 + 148, x0 + 238]
    # China
    d.rectangle([poles[0] - 3, y0 + 12, poles[0] + 3, y0 + 84], fill=INK)
    d.rectangle([poles[0] + 3, y0 + 12, poles[0] + 63, y0 + 48], fill=(196, 40, 44))
    d.ellipse([poles[0] + 10, y0 + 18, poles[0] + 22, y0 + 30], fill=GOLD)
    # USA (stripes + blue canton)
    d.rectangle([poles[1] - 3, y0 + 12, poles[1] + 3, y0 + 84], fill=INK)
    for i in range(6):
        col = (178, 34, 52) if i % 2 == 0 else (240, 240, 240)
        d.rectangle([poles[1] + 3, y0 + 12 + i * 6, poles[1] + 63, y0 + 18 + i * 6], fill=col)
    d.rectangle([poles[1] + 3, y0 + 12, poles[1] + 27, y0 + 30], fill=(60, 59, 110))
    # Russia
    d.rectangle([poles[2] - 3, y0 + 12, poles[2] + 3, y0 + 84], fill=INK)
    d.rectangle([poles[2] + 3, y0 + 12, poles[2] + 63, y0 + 24], fill=(240, 240, 240))
    d.rectangle([poles[2] + 3, y0 + 24, poles[2] + 63, y0 + 36], fill=(30, 60, 160))
    d.rectangle([poles[2] + 3, y0 + 36, poles[2] + 63, y0 + 48], fill=(200, 40, 50))
    # table line + three chairs under the flags
    d.rectangle([x0 + 40, y0 + 90, x0 + 256, y0 + 98], fill=(110, 74, 44))
    for cx in poles:
        d.rectangle([cx - 13, y0 + 74, cx + 13, y0 + 90], fill=(70, 70, 76))
    d.rectangle([x0, y0, x0 + 296, y0 + 108], outline=INK, width=3)
    return "ASIA · DIPLOMACY", "XI, TRUMP & PUTIN MEET IN SHENZHEN", \
        "China confirms Thursday's first three-way summit."


def col_nvidia(d, x0):
    y0 = 612
    d.rectangle([x0, y0, x0 + 296, y0 + 108], fill=(24, 30, 38))
    # circuit traces
    for sx, sy, ex, ey in ((16, 20, 110, 20), (110, 20, 110, 52), (16, 88, 84, 88),
                           (196, 88, 268, 88), (268, 88, 268, 40), (30, 54, 66, 54)):
        d.line([x0 + sx, y0 + sy, x0 + ex, y0 + ey], fill=(90, 200, 120), width=3)
        d.ellipse([x0 + ex - 4, y0 + ey - 4, x0 + ex + 4, y0 + ey + 4], fill=(90, 200, 120))
    # the chip
    d.rectangle([x0 + 108, y0 + 28, x0 + 188, y0 + 88], outline=GOLD, width=4)
    for px in range(x0 + 118, x0 + 184, 16):
        d.line([px, y0 + 18, px, y0 + 28], fill=GOLD, width=3)
        d.line([px, y0 + 88, px, y0 + 98], fill=GOLD, width=3)
    # falling chart line cracking through
    pts = [(x0 + 116, y0 + 44), (x0 + 140, y0 + 52), (x0 + 158, y0 + 48), (x0 + 182, y0 + 76)]
    d.line(pts, fill=(230, 70, 60), width=5)
    d.polygon([(x0 + 182, y0 + 76), (x0 + 168, y0 + 72), (x0 + 176, y0 + 62)], fill=(230, 70, 60))
    d.rectangle([x0, y0, x0 + 296, y0 + 108], outline=INK, width=3)
    return "TECH · MARKETS", "NVIDIA REELS AFTER HUANG'S EXIT", \
        "Earnings land as the US closes an AI-chip loophole."


def column(d, x0, kicker, headline, sub):
    f_k = font(SANS, 17)
    d.text((x0, 726), kicker, font=f_k, fill=RED)
    f_h = font(SANS, 25)
    y = 750
    for line in wrap(d, headline, f_h, 292)[:3]:
        d.text((x0, y), line, font=f_h, fill=INK)
        y += 31
    f_s = font(SANS_BOOK, 20)
    y += 4
    for line in wrap(d, sub, f_s, 292)[:2]:
        d.text((x0, y), line, font=f_s, fill=(60, 58, 52))
        y += 26


# ---------------------------------------------------------------- wire band
def wire(d):
    y0 = 906
    d.rectangle([0, y0, W, H], fill=INK)
    f_t = font(SANS, 21)
    text = ("ALSO TODAY · A Vulcan rocket failure destroys 40 Amazon Leo satellites · "
            "JPMorgan blames a software bug for the banking outage · "
            "The Pentagon fails its financial audit for the ninth straight year")
    y = y0 + 14
    for line in wrap(d, text, f_t, 952):
        centered(d, 512, y, line, f_t, WHITE)
        y += 29


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    hero(d)
    hero_text(d)
    k1 = col_hormuz(d, 36)
    k2 = col_summit(d, 364)
    k3 = col_nvidia(d, 692)
    column(d, 36, *k1)
    column(d, 364, *k2)
    column(d, 692, *k3)
    d.line([348, 612, 348, 884], fill=(190, 180, 158), width=2)
    d.line([676, 612, 676, 884], fill=(190, 180, 158), width=2)
    wire(d)
    img.save("entry.png", optimize=True)
    print("entry.png written")


if __name__ == "__main__":
    main()
