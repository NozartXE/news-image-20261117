#!/usr/bin/env python3
"""Draw 'The Daily Edition — Tuesday 17 November 2026' (upgrade round).

A denser broadsheet front page that sums up the world news of
Tuesday 17 November 2026 in one 1024x1024 image.  The first edition of
this page was drawn mid-day from five briefs; this upgrade rebuilds it
from the COMPLETED day, cross-verified across the evening and next-day
briefs (Majik evening update, NPR 6pm ET, UN News, OneTurn, The
Profiler Brief, Daily Buzz, Auranik, The Daily Spark, AP/Reuters
wires): the Kerch Bridge hero with the completed facts (second strike
in 24 hours, a record 1,441-drone barrage, the seven-stage operation),
three columns (Kyiv's bridges hit in reply, the first Trump-Xi-Putin
trilateral, Nvidia's beat and the board barring Huang's return), a
schematic world-map panel with story pins on six continents, an
eight-number DAY IN NUMBERS strip and an eighteen-item wire band —
30 distinct story items in total.  Every element is drawn
deterministically with Pillow from the string constants below: no
randomness, no network, no external assets beyond system fonts.
Running this file rewrites entry.png next to it, byte for byte the
same on every run.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W = H = 1024
PAPER = (247, 242, 231)
INK = (24, 22, 20)
FADED = (92, 84, 72)
ACCENT = (156, 38, 24)
NAVY = (18, 38, 66)
GOLD = (198, 148, 42)
TAN = (236, 228, 208)
SEA = (206, 222, 232)
LAND = (104, 124, 100)
LAND_LINE = (70, 88, 66)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SERIF = str(FONT_DIR / "DejaVuSerif.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")
SANS_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    box = draw.textbbox((0, 0), s, font=fnt)
    return box[2] - box[0]


def centred(draw, cx, y, s, fnt, fill=INK):
    draw.text((cx - text_w(draw, s, fnt) / 2, y), s, font=fnt, fill=fill)


def wrap(draw, s, fnt, width):
    """Greedy word wrap measured against the real font metrics."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, s, fnt, width, leading, fill=INK):
    """Draw wrapped text, return the y just below it."""
    for line in wrap(draw, s, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- scenes
def hero_scene(draw, x0, y0, x1, y1):
    """Dawn over the Kerch Strait: the bridge, one arch down in the sea.

    Laid out from the scene height so the deck, the fallen section,
    the smoke and the caption strip always stay inside the frame.
    """
    hh = y1 - y0
    sea_y = y0 + int(hh * 0.46)
    # sky: horizontal bands from deep pre-dawn blue down to ember orange
    sky_top = (38, 34, 62)
    sky_mid = (140, 58, 46)
    sky_low = (228, 132, 60)
    for yy in range(y0, sea_y):
        t = (yy - y0) / max(1, sea_y - y0)
        if t < 0.55:
            k = t / 0.55
            col = tuple(int(sky_top[i] + (sky_mid[i] - sky_top[i]) * k) for i in range(3))
        else:
            k = (t - 0.55) / 0.45
            col = tuple(int(sky_mid[i] + (sky_low[i] - sky_mid[i]) * k) for i in range(3))
        draw.line([(x0, yy), (x1, yy)], fill=col)
    # low sun disc on the left horizon
    sun_cx, sun_cy, sun_r = x0 + 96, sea_y - 14, 22
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
                 fill=(246, 196, 96))
    # sea
    draw.rectangle([x0, sea_y, x1, y1], fill=(24, 42, 64))
    for i, yy in enumerate(range(sea_y + 12, y1 - 32, 12)):
        off = 18 if i % 2 else 0
        for xx in range(x0 + 14 + off, x1 - 60, 92):
            draw.line([(xx, yy), (xx + 34, yy)], fill=(72, 102, 130), width=2)
    # the bridge: two headlands, a deck on piers, one section dropped
    deck_y = sea_y - 16
    draw.polygon([(x0, sea_y + 6), (x0, deck_y - 4), (x0 + 90, deck_y - 2),
                  (x0 + 110, sea_y + 6)], fill=(28, 24, 26))          # left shore
    draw.polygon([(x1 - 110, sea_y + 6), (x1 - 90, deck_y - 2),
                  (x1, deck_y - 4), (x1, sea_y + 6)], fill=(28, 24, 26))  # right shore
    gap0, gap1 = x0 + 400, x0 + 520                     # the missing span
    draw.line([(x0 + 84, deck_y), (gap0, deck_y)], fill=(14, 14, 16), width=7)
    draw.line([(gap1, deck_y), (x1 - 84, deck_y)], fill=(14, 14, 16), width=7)
    for px in range(x0 + 130, x1 - 120, 78):            # piers
        if gap0 - 30 < px < gap1 + 10:
            continue
        draw.line([(px, deck_y + 3), (px, sea_y + 16)], fill=(14, 14, 16), width=5)
    # the arch over the navigation span, broken at the gap
    draw.arc([x0 + 300, deck_y - 52, gap0 + 26, deck_y + 18], 180, 342,
             fill=(14, 14, 16), width=5)
    draw.arc([gap1 - 26, deck_y - 52, x0 + 640, deck_y + 18], 198, 0,
             fill=(14, 14, 16), width=5)
    # the fallen section: a deck slab tilted into the strait
    draw.polygon([(gap0 + 6, deck_y + 4), (gap1 - 16, deck_y + 26),
                  (gap1 - 6, deck_y + 36), (gap0 + 16, deck_y + 14)],
                 fill=(16, 16, 18))
    for sx in (gap0 + 30, gap0 + 62, gap0 + 92):        # splash marks
        draw.line([(sx, sea_y + 22), (sx - 5, sea_y + 12)], fill=(190, 210, 224), width=2)
        draw.line([(sx, sea_y + 22), (sx + 5, sea_y + 12)], fill=(190, 210, 224), width=2)
    # strike burst + smoke in the gap, at deck level
    bx, by = gap0 + 58, deck_y - 12
    for dx, dy in [(-26, 0), (26, 0), (0, -17), (-19, -12), (19, -12), (-29, -5)]:
        draw.line([(bx, by), (bx + dx, by + dy)], fill=(250, 214, 110), width=4)
    draw.ellipse([bx - 9, by - 7, bx + 9, by + 7], fill=(252, 232, 150))
    for i, (sx, sy, sr) in enumerate([(bx + 28, by - 22, 8), (bx + 50, by - 28, 11),
                                      (bx + 74, by - 32, 13)]):
        shade = 100 - i * 9
        draw.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2],
                     fill=(shade, shade - 6, shade - 2))
    # drones as small chevrons crossing the upper sky
    for cx, cy in [(x0 + 250, y0 + 20), (x0 + 330, y0 + 34), (x0 + 700, y0 + 24)]:
        draw.polygon([(cx - 15, cy + 5), (cx, cy - 6), (cx + 15, cy + 5),
                      (cx + 4, cy + 5), (cx, cy + 1), (cx - 4, cy + 5)],
                     fill=(16, 14, 18))
    # caption strip inside the scene
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(14, 14, 16))
    centred(draw, (x0 + x1) // 2, y1 - 21,
            "THE KERCH STRAIT AT DAWN — THE BRIDGE AND ITS FALLEN ARCH",
            font(SANS_BOLD, 14), fill=(238, 232, 218))


def bridge_icon(draw, x, y):
    """A simple suspension span with one section dropped."""
    draw.line([(x, y + 34), (x + 62, y + 34)], fill=NAVY, width=4)
    draw.line([(x + 84, y + 44), (x + 150, y + 30)], fill=NAVY, width=4)
    for tx in (x + 14, x + 128):
        draw.line([(tx, y), (tx, y + 46)], fill=NAVY, width=4)
    draw.line([(x, y + 8), (x + 150, y + 2)], fill=NAVY, width=2)
    draw.line([(x + 92, y + 44), (x + 118, y + 53)], fill=ACCENT, width=4)


def flags_icon(draw, x, y):
    """Three flag poles side by side — a summit of three powers."""
    for i, col in enumerate([ACCENT, NAVY, GOLD]):
        px = x + 18 + i * 48
        draw.line([(px, y + 4), (px, y + 52)], fill=INK, width=3)
        draw.polygon([(px, y + 4), (px + 30, y + 11), (px, y + 19)], fill=col)
    draw.line([(x + 4, y + 52), (x + 146, y + 52)], fill=INK, width=3)


def chip_icon(draw, x, y):
    """A microchip: a square die with pins on all four sides."""
    bx, by, bs = x + 48, y + 6, 44
    for i in range(4):
        off = 8 + i * 10
        draw.line([(bx + off, by - 7), (bx + off, by)], fill=NAVY, width=3)
        draw.line([(bx + off, by + bs), (bx + off, by + bs + 7)], fill=NAVY, width=3)
        draw.line([(bx - 7, by + off), (bx, by + off)], fill=NAVY, width=3)
        draw.line([(bx + bs, by + off), (bx + bs + 7, by + off)], fill=NAVY, width=3)
    draw.rectangle([bx, by, bx + bs, by + bs], outline=NAVY, width=4)
    draw.rectangle([bx + 13, by + 13, bx + bs - 13, by + bs - 13], fill=NAVY)


# ---------------------------------------------------------------- world map
# Schematic continent outlines as (lon, lat) points, hand-drawn for this
# page.  Equirectangular projection: lon -180..180 across, lat 85..-55 down.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-110, 73), (-95, 80), (-85, 73),
     (-75, 72), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-81, 26), (-90, 21), (-95, 16), (-100, 16), (-105, 20),
     (-110, 24), (-117, 32), (-125, 40), (-125, 48), (-135, 58),
     (-150, 60), (-165, 60), (-168, 66)],                                    # N America
    [(-79, 9), (-72, 11), (-62, 10), (-55, 6), (-50, 0), (-44, -3),
     (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-55, -34), (-62, -40),
     (-68, -50), (-70, -55), (-73, -50), (-73, -40), (-72, -30),
     (-75, -20), (-80, -12), (-81, -5), (-80, 0), (-79, 9)],                 # S America
    [(-17, 15), (-16, 20), (-10, 30), (-5, 35), (10, 37), (20, 32),
     (30, 31), (35, 28), (40, 20), (43, 12), (48, 11), (51, 10), (46, 5),
     (40, -5), (40, -15), (36, -22), (32, -28), (26, -34), (19, -35),
     (15, -30), (12, -18), (13, -10), (9, -1), (9, 4), (-8, 5),
     (-13, 8), (-17, 15)],                                                    # Africa
    [(-10, 36), (-9, 43), (-2, 48), (-4, 49), (0, 50), (3, 52), (5, 58),
     (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (30, 70), (35, 68), (40, 67), (45, 65), (40, 60), (35, 55), (30, 50),
     (28, 45), (23, 40), (19, 42), (12, 44), (8, 44), (3, 42), (-1, 37),
     (-6, 36), (-10, 36)],                                                    # Europe
    [(30, 70), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 76), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 70), (170, 67), (178, 65), (170, 60), (162, 58), (158, 52),
     (150, 45), (142, 40), (135, 35), (128, 33), (122, 30), (120, 22),
     (112, 15), (108, 10), (104, 8), (100, 10), (98, 15), (92, 16),
     (88, 22), (85, 20), (80, 13), (76, 8), (72, 20), (68, 23), (62, 25),
     (58, 26), (54, 26), (50, 28), (48, 30), (44, 29), (40, 32), (36, 36),
     (33, 38), (30, 40), (30, 45), (28, 50), (30, 55), (30, 62),
     (30, 70)],                                                               # Asia
    [(113, -22), (114, -30), (115, -35), (120, -34), (126, -32),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
     (146, -19), (142, -11), (137, -12), (132, -12), (126, -14),
     (122, -17), (117, -20), (113, -22)],                                     # Australia
]

# Story locations pinned on the map: Kerch, Kyiv, Hormuz, Gaza, Antalya,
# Shenzhen, Manila, Ulaanbaatar, Warsaw, Dhaka, DR Congo, Lima,
# North Carolina, Phillip Island.
# The Black Sea / eastern-Mediterranean pins are nudged a few degrees
# apart so the cluster stays readable at this scale.
PINS = [(37.6, 45.2), (30.5, 50.4), (56.5, 26.3), (34.3, 31.4),
        (30.7, 36.9), (114.1, 22.5), (121.0, 14.6), (106.9, 47.9),
        (21.0, 52.2), (90.4, 23.8), (29.5, 1.6), (-77.0, -12.0),
        (-79.0, 35.5), (145.3, -38.5)]

# Continent labels, placed on the sea beside each landmass so no pin
# sits on a word; dark ink on the pale sea.
MAP_LABELS = [("N. AMERICA", -118, 45), ("S. AMERICA", -72, -38),
              ("EUROPE", -25, 50), ("AFRICA", 32, -38), ("ASIA", 110, 80),
              ("OCEANIA", 132, -38)]


def map_panel(draw, x0, y0, x1, y1):
    """Schematic world map with a pin per story region, six continents."""
    draw.rectangle([x0, y0, x1, y1], fill=TAN, outline=INK, width=2)
    centred(draw, (x0 + x1) // 2, y0 + 9, "THE WORLD TODAY",
            font(SANS_BOLD, 15))
    mx0, my0 = x0 + 8, y0 + 34
    mw, mh = (x1 - x0) - 16, 100
    draw.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=SEA, outline=INK, width=1)

    def proj(lon, lat):
        return (mx0 + (lon + 180) / 360 * mw,
                my0 + (85 - lat) / 140 * mh)

    for poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly],
                     fill=LAND, outline=LAND_LINE)
    for name, lon, lat in MAP_LABELS:
        px, py = proj(lon, lat)
        centred(draw, int(px), int(py), name, font(SANS_BOLD, 9),
                fill=INK)
    for lon, lat in PINS:
        px, py = proj(lon, lat)
        r = 3
        draw.ellipse([px - r - 1, py - r - 1, px + r + 1, py + r + 1],
                     fill=PAPER)
        draw.ellipse([px - r, py - r, px + r, py + r], fill=ACCENT)
    cy = my0 + mh + 8
    centred(draw, (x0 + x1) // 2, cy, "14 STORIES · 6 CONTINENTS",
            font(SANS_BOLD, 10))
    centred(draw, (x0 + x1) // 2, cy + 16, "KERCH · KYIV · HORMUZ",
            font(SANS_BOLD, 10))
    centred(draw, (x0 + x1) // 2, cy + 31, "SHENZHEN · CONGO · GAZA",
            font(SANS_BOLD, 10))
    centred(draw, (x0 + x1) // 2, cy + 46, "LIMA · DHAKA · MANILA",
            font(SANS_BOLD, 10))


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 34                      # page margin
    R = W - M                   # right edge of the text area

    # outer frame
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)
    d.rectangle([20, 20, W - 20, H - 20], outline=INK, width=1)

    # ---- masthead ------------------------------------------------------
    y = 28
    centred(d, W // 2, y, "THE DAILY EDITION", font(SERIF_BOLD, 58))
    y += 74
    d.line([(M, y), (R, y)], fill=INK, width=3)
    d.line([(M, y + 5), (R, y + 5)], fill=INK, width=1)
    y += 11
    d.rectangle([M, y, R, y + 48], fill=INK)
    centred(d, W // 2, y + 6, "TUESDAY 17 NOVEMBER 2026",
            font(SANS_BOLD, 35), fill=(250, 247, 238))
    y += 58
    centred(d, W // 2, y, "One day's world news in one image  ·  No. 321  ·  Price: the truth",
            font(SERIF, 15), fill=FADED)
    y += 27
    d.line([(M, y), (R, y)], fill=INK, width=2)

    # ---- hero ----------------------------------------------------------
    y += 10
    centred(d, W // 2, y, "KERCH BRIDGE DOWN:",
            font(SERIF_BOLD, 41), fill=ACCENT)
    y += 52
    centred(d, W // 2, y, "ARCH FALLS TO 1,441 DRONES",
            font(SERIF_BOLD, 41), fill=ACCENT)
    y += 56
    centred(d, W // 2, y,
            "Second strike in 24 hours  ·  A seven-stage operation  ·  Two days before Shenzhen",
            font(SANS_BOLD, 16))
    y += 28
    hero_scene(d, M, y, R, y + 130)
    y += 130 + 9
    y = block(d, M, y,
              "Ukraine's seven-stage strike — Palianytsia drones, Neptune missiles, a Flamingo "
              "final blow — dropped the main road arch into the strait. Two killed in Crimea; "
              "trains are rolling again on one track.",
              font(SANS, 15), R - M, 20)
    y += 7
    d.line([(M, y), (R, y)], fill=INK, width=2)

    # ---- columns + world map ------------------------------------------
    top = y + 11
    row_h = 215
    map_x = R - 204
    col_gap = 16
    col_w = (map_x - M - col_gap - 2 * col_gap) // 3

    columns = [
        ("UKRAINE WAR", "RUSSIA HITS KYIV'S BRIDGES IN REPLY", bridge_icon,
         "Russian ballistic missiles struck the North and South bridges "
         "over the Dnipro late Monday; heating and water were "
         "knocked out."),
        ("SHENZHEN SUMMIT", "TRUMP, XI, PUTIN: A FIRST TRILATERAL", flags_icon,
         "China confirmed a first Trump–Xi–Putin meeting for Thursday "
         "at APEC in Shenzhen: nuclear arms, Iran — and Seoul's "
         "'second Yalta' warning."),
        ("SILICON VALLEY", "NVIDIA BEATS BIG; HUANG BARRED", chip_icon,
         "First report since Huang's exit: $115.8bn revenue, $130bn "
         "guide, shares +4% late. The board bars his return; Congress "
         "hears him in December."),
    ]
    for i, (kicker, head, icon, body) in enumerate(columns):
        cx = M + i * (col_w + col_gap)
        d.text((cx, top), kicker, font=font(SANS_BOLD, 13), fill=ACCENT)
        yy = block(d, cx, top + 19, head, font(SERIF_BOLD, 18), col_w, 22)
        icon(d, cx + 6, yy + 2)
        block(d, cx, yy + 58, body, font(SANS, 14), col_w, 18)
        if i < 2:
            vx = cx + col_w + col_gap // 2
            d.line([(vx, top), (vx, top + row_h)], fill=FADED, width=1)

    map_panel(d, map_x, top, R, top + row_h)

    # ---- day in numbers strip ------------------------------------------
    ny = top + row_h + 8
    strip_h = 54
    d.rectangle([M, ny, R, ny + strip_h], fill=TAN, outline=INK, width=2)
    numbers = [
        ("1,441", "drones in one night, a record"),
        ("19 km", "Kerch Bridge, Europe's longest"),
        ("11,000+", "Ebola cases in DR Congo"),
        ("5,400", "Ebola deaths (UN)"),
        ("$115.8bn", "Nvidia quarterly revenue"),
        ("$130bn", "Nvidia's guide next quarter"),
        ("150,000", "Gaza tents urged in"),
        ("1,390", "Sudan civilians killed (UN)"),
    ]
    head_w = 110
    cell_w = (R - M - head_w) / 8
    d.text((M + 8, ny + 11), "DAY IN", font=font(SANS_BOLD, 11), fill=INK)
    d.text((M + 8, ny + 25), "NUMBERS", font=font(SANS_BOLD, 11), fill=INK)
    for i, (big, label) in enumerate(numbers):
        cx = M + head_w + i * cell_w
        if i:
            d.line([(cx - 2, ny + 6), (cx - 2, ny + strip_h - 6)],
                   fill=FADED, width=1)
        d.text((cx + 6, ny + 6), big, font=font(SERIF_BOLD, 17), fill=ACCENT)
        block(d, cx + 6, ny + 28, label, font(SANS, 10), cell_w - 12, 12)

    # ---- wire band ------------------------------------------------------
    wy = ny + strip_h + 8
    d.rectangle([M, wy, R, H - 30], fill=NAVY)
    d.text((M + 16, wy + 9), "THE WIRE — AROUND THE WORLD IN A DAY",
           font=font(SANS_BOLD, 16), fill=(246, 240, 224))
    right = "18 STORIES · 6 CONTINENTS"
    d.text((R - 16 - text_w(d, right, font(SANS_BOLD, 12)), wy + 12), right,
           font=font(SANS_BOLD, 12), fill=GOLD)
    wire = [
        "HORMUZ: third U.S. carrier arrives; tanker ablaze, crew safe",
        "EBOLA: WHO clears vaccine trials as toll tops 11,000 cases",
        "GAZA: Board of Peace gives bleak ceasefire report to UN",
        "OUTAGES: FAA pauses router type tied to last week's stop",
        "N. CAROLINA: Democrat Smith unseats Rep. Murphy, barely",
        "CANADA: Carney–Xi deal cuts tariff on $400m pork, seafood",
        "RWANDA: five EU states unveil hub; UN rights chief objects",
        "COP31: Antalya draft seeks phaseout, $120bn adaptation",
        "MONGOLIA: president to resign over $25m railway claims",
        "POLAND: three teenagers held over neo-Nazi terror plot",
        "DHAKA: world's most polluted city; air index at 292",
        "HEALTH: lung-cancer 5-year survival hits 31%, was 18%",
        "MIAMI: city readies for GTA VI; Heat wear Vice City kits",
        "SPACE: Vulcan failure loses 40 Amazon Leo satellites",
        "BANKING: JPMorgan software bug knocks services offline",
        "PENTAGON: fails its ninth straight financial audit",
        "POPE LEO XIV: ends 12-day South America tour in Rome",
        "AUSTRALIA: curlew chicks hatch, first time in 50 years",
    ]
    cell_w = (R - M - 32) // 2
    for i, item in enumerate(wire):
        cx = M + 16 + (i % 2) * cell_w
        cy = wy + 34 + (i // 2) * 14
        d.rectangle([cx, cy + 3, cx + 7, cy + 10], fill=GOLD)
        d.text((cx + 14, cy), item, font=font(SANS_BOLD, 12),
               fill=(240, 238, 228))

    return img


def main():
    out = Path(__file__).with_name("entry.png")
    build().save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
