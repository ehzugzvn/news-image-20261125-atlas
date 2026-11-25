#!/usr/bin/env python3
"""ATLAS — news-image-20261125. Draws entry.png (1024x1024) with PIL only.
All facts from CONTENT.md. Deep teal-navy + cream paper panels, map hero."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
TEAL = (14, 42, 51)        # #0e2a33 background
TEAL_DK = (8, 28, 35)      # darker ocean
TEAL_MD = (32, 84, 96)     # panel teal
CREAM = (247, 242, 231)    # #f7f2e7 paper
CREAM_DK = (232, 222, 198)
SAND = (216, 198, 138)     # continents
GOLD = (232, 182, 76)      # #e8b64c accents
YELLOW = (242, 201, 76)
WHITE = (255, 255, 255)
INK = (18, 32, 38)
RED = (196, 58, 40)
GREEN = (46, 125, 87)
BLUE = (43, 108, 160)
ORANGE = (214, 110, 44)

FDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

def F(size, bold=False, serif=False):
    name = ("LiberationSerif-Bold.ttf" if serif and bold else
            "LiberationSerif-Regular.ttf" if serif else
            "LiberationSans-Bold.ttf" if bold else
            "LiberationSans-Regular.ttf")
    return ImageFont.truetype(os.path.join(FDIR, name), size)

def tw(draw, s, font):
    return draw.textlength(s, font=font)

def wrap(draw, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def chip(draw, x, y, tag, colors=None):
    """Verification tag chip: coloured square + letter, ~18px tall."""
    cols = {"C": (46, 125, 87), "O": (43, 108, 160),
            "R": (196, 130, 30), "F": (110, 90, 140)}
    c = cols.get(tag, (90, 90, 90))
    draw.rounded_rectangle([x, y, x + 20, y + 18], radius=4, fill=c)
    f = F(13, bold=True)
    draw.text((x + 10, y + 9), tag, font=f, fill=WHITE, anchor="mm")
    return x + 24

img = Image.new("RGB", (W, H), TEAL)
d = ImageDraw.Draw(img)
M = 12  # side margin

# ---------- KICKER BAR ----------
y = 0
d.rectangle([0, 0, W, 22], fill=TEAL_DK)
d.text((M, 11), "THE WORLD IN ONE DAY", font=F(14, bold=True), fill=GOLD, anchor="lm")
rk = "EVERY STORY DATED  ·  WEDNESDAY 25 NOV"
d.text((W - M, 11), rk, font=F(14, bold=True), fill=CREAM, anchor="rm")
y = 22

# ---------- DATE — largest element ----------
d.text((M, y + 38), "Wednesday 25 November 2026", font=F(66, bold=True, serif=True),
       fill=CREAM, anchor="lm")
y += 76
# gold rule under date
d.rectangle([M, y - 6, W - M, y - 3], fill=GOLD)
# strip under date
strip = "38 STORIES  ·  7 REGIONS  ·  ALL FROM THIS WEDNESDAY"
d.text((M, y + 8), strip, font=F(14, bold=True), fill=YELLOW, anchor="lm")
rc = "Americas 8  ·  Europe 10  ·  Asia-Pacific 5  ·  Middle East 5  ·  Oceania 3  ·  Africa 4  ·  Global 3"
d.text((W - M, y + 8), rc, font=F(13), fill=CREAM, anchor="rm")
y += 26

# ---------- HERO WORLD MAP ----------
map_top = y
d.text((M, map_top + 8), "WHERE IT HAPPENED — PIN = STORY NUMBER",
       font=F(15, bold=True), fill=GOLD, anchor="lm")
d.text((W - M, map_top + 8), "14 PINNED STORIES", font=F(13, bold=True), fill=CREAM, anchor="rm")
map_y0 = map_top + 24
map_y1 = map_top + 118
d.rectangle([M, map_y0, W - M, map_y1], fill=TEAL_DK, outline=GOLD, width=2)
# faint graticule
for gx in range(M + 84, W - M, 84):
    d.line([(gx, map_y0), (gx, map_y1)], fill=(24, 58, 68), width=1)
for gy in range(map_y0 + 29, map_y1, 29):
    d.line([(M, gy), (W - M, gy)], fill=(24, 58, 68), width=1)

# Stylised continents (map-local coords, x 0-1000, y 0-124)
def poly(pts, fill=SAND):
    d.polygon([(M + 12 + x, map_y0 + 6 + int(yy * 0.65)) for x, yy in pts],
              fill=fill, outline=(120, 100, 55))

poly([(48, 22), (110, 8), (195, 14), (235, 26), (252, 42), (225, 56), (190, 64),
      (168, 92), (140, 106), (112, 90), (82, 66), (45, 46)])                       # N America
poly([(272, 6), (296, 4), (300, 20), (282, 24)])                                   # Greenland
poly([(238, 82), (272, 76), (296, 90), (290, 116), (268, 140), (248, 126), (234, 100)])  # S America
poly([(458, 22), (508, 10), (546, 16), (560, 34), (540, 52), (500, 58), (464, 44)])  # Europe
poly([(468, 56), (518, 52), (546, 66), (542, 96), (508, 130), (484, 106), (464, 82)])  # Africa
poly([(562, 16), (688, 8), (838, 22), (888, 42), (866, 66), (808, 80), (748, 72),
      (688, 56), (610, 52), (568, 36)])                                            # Asia
d.ellipse([M + 12 + 786, map_y0 + 6 + 57, M + 12 + 800, map_y0 + 6 + 64], fill=SAND)
d.ellipse([M + 12 + 812, map_y0 + 6 + 61, M + 12 + 828, map_y0 + 6 + 68], fill=SAND)
poly([(818, 100), (878, 96), (892, 114), (858, 134), (824, 124)])                  # Australia
d.rectangle([M, map_y1 - 8, W - M, map_y1], fill=(200, 210, 215))                  # Antarctica hint

PINS = {  # story -> (map-local x, y)
    1: (243, 34), 9: (210, 51), 4: (148, 44), 13: (256, 88),
    14: (518, 10), 3: (553, 28), 10: (588, 22),
    5: (593, 74), 8: (628, 68),
    2: (758, 38), 12: (803, 54),
    6: (856, 112), 11: (903, 134), 7: (418, 76),
}
for num, (px, py) in PINS.items():
    cx, cy = M + 12 + px, map_y0 + 6 + int(py * 0.65)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=GOLD, outline=WHITE, width=2)
    d.text((cx, cy), str(num), font=F(13, bold=True), fill=INK, anchor="mm")
y = map_y1 + 6
print("after map y =", y)

# ---------- 4 LEADS, 2x2 grid ----------
LEADS = [
    ("1", "HUAWEI GUILTY", "Huawei guilty on 10 of 12 counts, and it will appeal",
     "Convicted on bank fraud, wire fraud, sanctions and trade-secret theft; sentencing 14 Sep 2027.",
     "REUTERS · CNN · WSJ", "C", "gavel"),
    ("2", "SHENZHOU-24", "Shenzhou-24 lifts off with a Pakistani pilot aboard",
     "Lifts off 00:18 UTC from Jiuquan with Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali aboard.",
     "XINHUA · REUTERS · CMSA", "C", "rocket"),
    ("3", "RUSSIA'S WAR DEAD", "Russia's own figures show nearly 500,000 war dead",
     "Leaked Russian data analysed by BBC Russian Service: ~500,000 excess deaths among military-age men.",
     "BBC RUSSIAN SERVICE · MEDIAZONA", "R", "graves"),
    ("4", "NVIDIA", "Huang apologises to staff as Nvidia shares slide 5.9%",
     "A day after his Trump-backed return as CEO, Huang told staff he made “terrible mistakes”.",
     "REUTERS · NYT · THE TIMES", "C", "chip"),
]
LEAD_H = 108
LEAD_W = (W - 2 * M - 10) // 2

def draw_art(x0, y0, w, h, kind, label):
    if kind == "gavel":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(28, 90, 70))
        for lx in (18, 48, 78):
            d.line([(x0 + 14, y0 + lx), (x0 + w - 14, y0 + lx)], fill=(120, 200, 150), width=3)
        for cx in (30, 70, 110, 140):
            d.ellipse([x0 + cx - 4, y0 + 18 - 4, x0 + cx + 4, y0 + 18 + 4], fill=GOLD)
            d.ellipse([x0 + cx - 4, y0 + 78 - 4, x0 + cx + 4, y0 + 78 + 4], fill=GOLD)
        d.rectangle([x0 + 52, y0 + 30, x0 + 112, y0 + 52], fill=(120, 72, 32))
        d.rectangle([x0 + 74, y0 + 52, x0 + 86, y0 + 92], fill=(150, 100, 50))
        d.rectangle([x0 + 46, y0 + 88, x0 + 114, y0 + 96], fill=(90, 55, 25))
    elif kind == "rocket":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 110, 44))
        d.rectangle([x0, y0 + h - 26, x0 + w, y0 + h], fill=(60, 40, 90))
        d.polygon([(x0 + 82, y0 + 12), (x0 + 94, y0 + 34), (x0 + 70, y0 + 34)], fill=WHITE)
        d.rectangle([x0 + 70, y0 + 34, x0 + 94, y0 + 66], fill=WHITE)
        d.polygon([(x0 + 70, y0 + 52), (x0 + 56, y0 + 70), (x0 + 70, y0 + 66)], fill=RED)
        d.polygon([(x0 + 94, y0 + 52), (x0 + 108, y0 + 70), (x0 + 94, y0 + 66)], fill=RED)
        d.polygon([(x0 + 76, y0 + 66), (x0 + 88, y0 + 66), (x0 + 82, y0 + 84)], fill=YELLOW)
        d.ellipse([x0 + 78, y0 + 40, x0 + 86, y0 + 48], fill=TEAL)
        d.rectangle([x0 + 118, y0 + 40, x0 + 148, y0 + 48], fill=(40, 40, 60))
        d.rectangle([x0 + 118, y0 + 44, x0 + 122, y0 + 66], fill=(40, 40, 60))
    elif kind == "graves":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(52, 52, 62))
        bars = [14, 20, 26, 32, 40, 48, 58]
        bw = 14
        for gx in (24, 96, 138):
            d.rounded_rectangle([x0 + gx, y0 + 8, x0 + gx + 18, y0 + 24],
                                radius=8, fill=(210, 205, 190))
        for i, bh in enumerate(bars):
            bx = x0 + 12 + i * 20
            d.rectangle([bx, y0 + h - 14 - bh, bx + bw, y0 + h - 14], fill=(150, 60, 50))
    else:  # chip
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 48, 90))
        d.rectangle([x0 + 52, y0 + 22, x0 + 112, y0 + 86], fill=(20, 20, 30),
                    outline=GOLD, width=2)
        d.rectangle([x0 + 72, y0 + 42, x0 + 92, y0 + 66], fill=GOLD)
        for px in range(5):
            d.line([(x0 + 52 + px * 15, y0 + 22), (x0 + 52 + px * 15, y0 + 12)], fill=GOLD, width=3)
            d.line([(x0 + 52 + px * 15, y0 + 86), (x0 + 52 + px * 15, y0 + 96)], fill=GOLD, width=3)
        d.line([(x0 + 12, y0 + 84), (x0 + 48, y0 + 52), (x0 + 84, y0 + 66),
                (x0 + 120, y0 + 26), (x0 + 152, y0 + 34)], fill=RED, width=4)
        d.polygon([(x0 + 152, y0 + 34), (x0 + 140, y0 + 34), (x0 + 152, y0 + 46)], fill=RED)
    d.rectangle([x0, y0 + h - 17, x0 + w, y0 + h], fill=(12, 24, 30))
    d.text((x0 + w // 2, y0 + h - 8), label, font=F(13, bold=True), fill=WHITE, anchor="mm")

for li, (num, kick, head, summ, src, tag, art) in enumerate(LEADS):
    cx0 = M + (li % 2) * (LEAD_W + 10)
    cy0 = y + (li // 2) * (LEAD_H + 6)
    d.rounded_rectangle([cx0, cy0, cx0 + LEAD_W, cy0 + LEAD_H], radius=6, fill=CREAM)
    ax0, ay0, aw = cx0 + 6, cy0 + 6, 150
    draw_art(ax0, ay0, aw, LEAD_H - 12, art, kick)
    tx = ax0 + aw + 8
    tw_ = cx0 + LEAD_W - 8 - tx
    chip(d, tx, cy0 + 6, tag)
    d.text((tx + 26, cy0 + 15), num + "  " + kick, font=F(13, bold=True), fill=RED, anchor="lm")
    ty = cy0 + 26
    for ln in wrap(d, head, F(16, bold=True), tw_)[:2]:
        d.text((tx, ty), ln, font=F(16, bold=True), fill=INK, anchor="la")
        ty += 19
    for ln in wrap(d, summ, F(13), tw_)[:2]:
        d.text((tx, ty), ln, font=F(13), fill=(40, 55, 60), anchor="la")
        ty += 15
    d.text((tx, cy0 + 100), src, font=F(13), fill=(90, 90, 90), anchor="lm")
y += 2 * LEAD_H + 6 + 6
print("after leads y =", y)

# ---------- DAY IN NUMBERS ----------
d.rectangle([M, y, W - M, y + 40], fill=TEAL_MD)
NUMS = [("10/12", "Huawei counts"), ("≈500,000", "Russian war dead"),
        ("47,000", "women killed"), ("11", "hurt in Riyadh"),
        ("5.9%", "Nvidia slide"), ("1st", "Pakistani in orbit")]
nw = (W - 2 * M) // 6
for i, (n, cap) in enumerate(NUMS):
    nx = M + i * nw
    d.text((nx + nw // 2, y + 19), n, font=F(19, bold=True), fill=WHITE, anchor="mm")
    d.text((nx + nw // 2, y + 33), cap, font=F(13), fill=CREAM, anchor="mm")
y += 44
print("after numbers y =", y)

# ---------- UTC TIMELINE ----------
TL = [("00:18", "Liftoff"), ("01:38", "Baffin quake"), ("03:56", "Docks"),
      ("04:30", "Balleny quake"), ("MORNING", "Huawei verdict"), ("MIDDAY", "Aus pact"),
      ("AFTERNOON", "Hodeidah"), ("EVENING", "Samara hit"), ("NIGHT", "Nvidia −5.9%")]
tw_ = (W - 2 * M) // 9
d.line([(M, y + 22), (W - M, y + 22)], fill=GOLD, width=2)
for i, (t, lab) in enumerate(TL):
    cx = M + i * tw_ + tw_ // 2
    d.ellipse([cx - 4, y + 18, cx + 4, y + 26], fill=GOLD)
    d.text((cx, y + 10), t, font=F(13, bold=True), fill=YELLOW, anchor="mm")
    d.text((cx, y + 32), lab, font=F(13), fill=CREAM, anchor="ma")
y += 48
print("after timeline y =", y)

# ---------- TIER-2, 2 columns x 5 rows ----------
T2 = [
    ("5", "Saudi jets bomb Hodeidah; Houthis hit Riyadh tower, 11 hurt",
     "Second strike on the PIF tower in six days — AL JAZEERA · REUTERS", "C", "jet"),
    ("6", "Australia signs sweeping pact with Solomon Islands",
     "Police, ports, schools; meant to blunt Beijing — REUTERS · ABC", "O", "doc"),
    ("7", "UN reports 47,000 women killed by partners or kin in a year",
     "129 a day; Africa's rate highest at 2.9/100,000 — UNODC · UN WOMEN", "O", "ribbon"),
    ("8", "Two tankers hit mines in the Strait of Hormuz, IRGC says",
     "Saudis strike Hodeidah in reply — TIMES OF ISRAEL · GULF NEWS", "R", "ship"),
    ("9", "US readies tariffs in 16-nation capacity probe, 15–25%",
     "Targets China, India, Japan, ASEAN — REUTERS · HINDUSTAN TIMES", "R", "pct"),
    ("10", "Ukraine drones hit two Samara oil refineries, 800 km deep",
     "Kremlin rejects four-party talks — KYIV INDEPENDENT · AZERNEWS", "R", "flame"),
    ("11", "M5.9 quakes strike off Baffin Island and near Antarctica",
     "Balleny Islands quake 10 km deep at 04:30 UTC — USGS", "O", "wave"),
    ("12", "Xi's anti-graft drive reaches Shanghai party boss",
     "Chen Jining probed; biggest name swept up — GUARDIAN · CNA", "C", "bldg"),
    ("13", "Hostages held in a supermarket on a second day",
     "At least 20 remain inside after a failed raid — AP · EL TIEMPO", "R", "lock"),
    ("14", "A drone hits a Russian cargo ship in the gulf",
     "Zelenskyy confirmed it; Norway urged restraint — YLE · REUTERS", "R", "ship"),
]
T2_H = 34
T2_W = (W - 2 * M - 10) // 2

def pict(x0, y0, kind):
    d.rectangle([x0, y0, x0 + 34, y0 + 34], fill=TEAL_MD, outline=GOLD, width=1)
    c = (17, 17)
    if kind == "jet":
        d.polygon([(x0 + 6, y0 + 20), (x0 + 28, y0 + 10), (x0 + 28, y0 + 24)], fill=WHITE)
        d.line([(x0 + 6, y0 + 20), (x0 + 30, y0 + 20)], fill=GOLD, width=2)
    elif kind == "doc":
        d.rectangle([x0 + 10, y0 + 7, x0 + 24, y0 + 27], fill=WHITE)
        for ly in (12, 17, 22):
            d.line([(x0 + 13, y0 + ly), (x0 + 21, y0 + ly)], fill=TEAL, width=2)
    elif kind == "ribbon":
        d.ellipse([x0 + 12, y0 + 7, x0 + 22, y0 + 17], fill=(200, 80, 120))
        d.polygon([(x0 + 14, y0 + 15), (x0 + 10, y0 + 28), (x0 + 17, y0 + 22),
                   (x0 + 24, y0 + 28), (x0 + 20, y0 + 15)], fill=(200, 80, 120))
    elif kind == "ship":
        d.polygon([(x0 + 6, y0 + 20), (x0 + 28, y0 + 20), (x0 + 24, y0 + 26), (x0 + 10, y0 + 26)], fill=WHITE)
        d.rectangle([x0 + 14, y0 + 12, x0 + 20, y0 + 20], fill=GOLD)
    elif kind == "pct":
        d.text((x0 + 17, y0 + 17), "%", font=F(20, bold=True), fill=YELLOW, anchor="mm")
    elif kind == "flame":
        d.polygon([(x0 + 17, y0 + 6), (x0 + 24, y0 + 18), (x0 + 20, y0 + 26),
                   (x0 + 14, y0 + 26), (x0 + 10, y0 + 18)], fill=ORANGE)
    elif kind == "wave":
        for wy in (12, 19, 26):
            d.arc([x0 + 7, y0 + wy - 4, x0 + 27, y0 + wy + 4], 180, 360, fill=WHITE, width=2)
    elif kind == "bldg":
        d.rectangle([x0 + 9, y0 + 12, x0 + 16, y0 + 28], fill=WHITE)
        d.rectangle([x0 + 18, y0 + 7, x0 + 25, y0 + 28], fill=GOLD)
    else:  # lock
        d.rectangle([x0 + 10, y0 + 15, x0 + 24, y0 + 28], fill=WHITE)
        d.arc([x0 + 12, y0 + 7, x0 + 22, y0 + 18], 180, 360, fill=GOLD, width=3)

for ti, (num, head, summ, tag, kind) in enumerate(T2):
    cx0 = M + (ti % 2) * (T2_W + 10)
    cy0 = y + (ti // 2) * T2_H
    pict(cx0, cy0, kind)
    tx = cx0 + 42
    chip(d, tx, cy0 + 2, tag)
    d.text((tx + 26, cy0 + 11), num + ". " + head, font=F(13, bold=True), fill=CREAM, anchor="lm")
    d.text((tx, cy0 + 21), summ, font=F(13), fill=(200, 210, 205), anchor="la")
y += 5 * T2_H + 4
print("after tier2 y =", y)

# ---------- BRIEFS, grouped by region, 2 columns ----------
BRIEFS_A = [("AMER", "17. LOS ANGELES — Thomas Markle charged with a second count."),
            ("AMER", "24. HAVANA — WHO chief urges end to US fuel blockade on Cuba."),
            ("AMER", "30. CHICAGO — O'Hare ground stop & radar outage snarls travel."),
            ("AMER", "31. MEXICO CITY — US Embassy alerts on Reforma-to-Zócalo march."),
            ("EURO", "15. WINDSOR — Two arrested on William and Kate's estate."),
            ("EURO", "18. MADRID — Spain votes Sunday; Vox may enter government."),
            ("EURO", "27. MOSCOW — Putin and Brunei Sultan sign joint declaration."),
            ("EURO", "28. PARIS — Champions League: PSG–Roma & Arsenal–BVB."),
            ("EURO", "29. BRUSSELS — NATO chief Rutte meets Trump on alliance security."),
            ("EURO", "32. BRUSSELS — 90+ leaders urge EU to cap €210B Russian assets."),
            ("EURO", "34. LONDON — Russia demands UK drop NATO nuclear shield.")]
BRIEFS_B = [("ASIA", "19. NEW DELHI — Food inflation spreads to vegetables, pulses, oils."),
            ("ASIA", "20. TAIPEI — AI disinfo network targets Taiwan election candidates."),
            ("ASIA", "23. KUALA LUMPUR — Malaysia to return Rohingya refugees to Myanmar."),
            ("MIDE", "22. BAGHDAD — Iraq orders takeover of Kurdish-controlled oilfields."),
            ("MIDE", "35. GAZA — Israeli strike kills Hamas security chief Naeem Abu Nahel."),
            ("MIDE", "36. DOHA — US Embassy warns of Houthi threats."),
            ("OCEA", "21. SYDNEY — Ex-officer Beau Lamarre convicted of double murder."),
            ("AFRI", "16. DAKAR — Senegal restored as 2025 African champions on appeal."),
            ("AFRI", "33. BENGHAZI — UN cities hit in drone strike on Russian ship."),
            ("AFRI", "37. ABUJA — Tinubu sends N65.2T budget; Senate clears $20.5B loan."),
            ("AFRI", "38. CAIRO — Sudan & Egypt reject Red Sea militarisation."),
            ("GLOB", "25. GLOBAL — Landmine casualties hit a five-year high."),
            ("GLOB", "26. DEEP SPACE — ESA's Hera reaches asteroid Dimorphos.")]
BRIEF_PITCH = 14
d.text((M, y + 2), "THE REST OF THE DAY — BRIEFS 15–38",
       font=F(14, bold=True), fill=GOLD, anchor="la")
y += 20
by0 = y
for col, items in enumerate((BRIEFS_A, BRIEFS_B)):
    bx0 = M + col * (T2_W + 10)
    by = by0
    for region, txt in items:
        d.text((bx0, by), region + " · ", font=F(13, bold=True), fill=GOLD, anchor="la")
        d.text((bx0 + tw(d, region + " · ", F(13, bold=True)), by), txt,
               font=F(13), fill=CREAM, anchor="la")
        by += BRIEF_PITCH
y = by0 + max(len(BRIEFS_A), len(BRIEFS_B)) * BRIEF_PITCH + 2
print("after briefs y =", y)

# ---------- DATE CHECK + HOW SURE + FOOTER ----------
d.rectangle([M, y, W - M, y + 30], fill=CREAM)
dc = ("DATE CHECK — Left out as other days' news: Spain's election (29 Nov, not yet) · "
      "US Thanksgiving (26 Nov, not yet) · Huang's Senate hearing (3 Dec, not yet) · "
      "Huawei sentencing (Sep 2027, not yet).")
for j, ln in enumerate(wrap(d, dc, F(13, bold=True), W - 2 * M - 16)):
    d.text((M + 8, y + 2 + j * 14), ln, font=F(13, bold=True), fill=INK, anchor="la")
y += 32
hs = "HOW SURE:  C = CONFIRMED by 2+ major outlets  ·  O = OFFICIAL data or statement  ·  R = REPORTED by one outlet or attributed  ·  F = FORECAST / preview"
d.text((M, y + 2), hs, font=F(13), fill=CREAM, anchor="la")
y += 16
ft = "Sources: Reuters · AP · BBC · Al Jazeera · Xinhua · Guardian · SCMP · USGS · UNODC · NATO — Drawn by an AI agent for make.fun — 25 Nov 2026."
d.text((M, y + 2), ft, font=F(13), fill=(170, 180, 175), anchor="la")
y += 14
print("final y =", y, "canvas H =", H)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
