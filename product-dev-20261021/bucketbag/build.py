"""Build the bucket bag pattern (owner, 18 Nov 2026: "give me the pattern; I may not use the offcuts").

Read from the owner's two reference photos: a soft, unlined bucket bag, base 15 x 15 cm, 28 cm tall, one rolled strap
with a 26 cm drop, two body panels joined at the sides and across the base, boxed corners, a loose stiff base insert,
two magnet tabs inside. Every size below derives from BASE, HEIGHT and SA; change them and rebuild.

Outputs
  index.html    summary page (Thai, phone first), from template.html
  print.html    A4 pages at 1:1 (overview, body in 2 x 2 tiles, small parts)
  pattern.pdf   print.html through Chromium: node bucketbag/render.cjs
python3 bucketbag/build.py && node bucketbag/render.cjs
"""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- sizes, mm
BASE, HEIGHT, DROP = 150, 280, 260          # from the photo: 15 x 15 base, 28 tall, strap drop 26
SA = 8                                      # seam allowance, included in the cut sizes
W = 2 * BASE + 2 * SA                       # body panel: half of each side face + one full face
H = HEIGHT + BASE / 2 + SA                  # top edge is a raw cut; the base half folds under
N = BASE / 2                                # corner cut-out, measured from the cut corner
CORD, LEATHER = 5, 1.6                      # strap core and the leather this pattern assumes
STRAP_W = round((CORD + LEATHER) * math.pi + 10)      # wrap + 5 mm each side to sew and trim
STRAP_SEEN, STRAP_END = 580, 36             # seen part is 52-58 cm by the photo; each end lies 36 mm down the outside of the side seam
STRAP_L = 700                               # STRAP_SEEN + 2 ends + 40 spare
CORD_L = STRAP_L                            # cut to length after fitting; the core runs to the very end of the strap
WRAP, NWRAP = (34, 9), 6                    # bands over the strap end, three a side: 7 mm foot + over the strap + 7 mm foot
BAND_Y = (4, 15, 26)                        # top of each band below the rim
FOOT = (5, 12)                              # a band's foot runs 5-12 mm from the seam line
TAB = (44, 24); TAB_TOP = 12; MAG = (20, 10) # photo: a small bar magnet under a tab sewn at its two short ends, close under the rim
PATCH = (40, 50)
INS, INS_R, BOARD, BOARD_R = BASE - 5, 20, BASE - 11, 17
RIM = (2 * BASE * 2 + 15, 20)               # optional strip inside the rim for leather under 1.4 mm
LAYOUT = (700, 580)                         # one piece of leather that takes everything
cm = lambda v: (f"{v / 10:.1f}".rstrip("0").rstrip("."))
sqft = lambda m2: m2 * 10.7639
AREA = (2 * W * H + STRAP_L * STRAP_W + 2 * INS * INS + 2 * TAB[0] * TAB[1] + 2 * PATCH[0] * PATCH[1] + NWRAP * WRAP[0] * WRAP[1]) / 1e6

CUTS = [  # letter, name, qty, cut size, note
    ("A", "ตัวกระเป๋า", "2", f"{cm(W)} × {cm(H)}", f"ตัดมุมล่างออก 2 มุม มุมละ {cm(N)} × {cm(N)} · รวมเผื่อตะเข็บ {SA} มม. แล้ว"),
    ("B", "สาย", "1", f"{cm(STRAP_W)} × {cm(STRAP_L)}", f"หุ้มเชือกแกน {CORD} มม. ยาว {cm(CORD_L)} ซม. · ปลายทับด้านนอกตัวกระเป๋าข้างละ {cm(STRAP_END)} ซม. · ตัดหลังลองความยาว"),
    ("C", "ปลอกรัดโคนสาย", str(NWRAP), f"{cm(WRAP[1])} × {cm(WRAP[0])}", "ข้างละ 3 เส้น คาดทับสายด้านนอก เย็บปลายสองข้าง"),
    ("D", "แผ่นหุ้มแม่เหล็ก", "2", f"{cm(TAB[0])} × {cm(TAB[1])}", f"แม่เหล็กแท่ง {cm(MAG[0])} × {cm(MAG[1])} ซม. หนา 2 มม. 2 ชิ้น · เย็บเฉพาะปลายสั้นสองข้าง"),
    ("E", "แผ่นรองก้น หนัง", "2", f"{cm(INS)} × {cm(INS)}", f"มุมมน รัศมี {cm(INS_R)}"),
    ("E2", "แผ่นรองก้น ไส้แข็ง", "1", f"{cm(BOARD)} × {cm(BOARD)}", "กระดาษอัดหรือแผ่น PE หนา 1.5–2 มม."),
    ("F", "แผ่นเสริมโคนสาย", "2", f"{cm(PATCH[0])} × {cm(PATCH[1])}", "ติดด้านใน ทับตะเข็บข้าง รับรอยเย็บปลอกและสาย"),
    ("G", "แถบเสริมปาก (ถ้าหนังบางกว่า 1.4 มม.)", "1", f"{cm(RIM[1])} × {cm(RIM[0])}", "ต่อ 2 ท่อนได้ ติดด้านในรอบปาก"),
]

# ---------------------------------------------------------------- svg helpers (1 unit = 1 mm)
def dim_h(x1, x2, y, text, fs):
    t = fs * .35
    return (f'<g class="dim"><line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/><line x1="{x1}" y1="{y - t}" x2="{x1}" y2="{y + t}"/>'
            f'<line x1="{x2}" y1="{y - t}" x2="{x2}" y2="{y + t}"/><text x="{(x1 + x2) / 2}" y="{y - fs * .4}" font-size="{fs}" text-anchor="middle">{text}</text></g>')
def dim_v(x, y1, y2, text, fs, side=-1):
    t = fs * .35; tx = x + side * fs * .45; ty = (y1 + y2) / 2
    return (f'<g class="dim"><line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}"/><line x1="{x - t}" y1="{y1}" x2="{x + t}" y2="{y1}"/>'
            f'<line x1="{x - t}" y1="{y2}" x2="{x + t}" y2="{y2}"/><text x="{tx}" y="{ty}" font-size="{fs}" text-anchor="middle" '
            f'transform="rotate(-90 {tx} {ty})"{" dy=" + chr(34) + str(fs * .8) + chr(34) if side > 0 else ""}>{text}</text></g>')
def rrect(x, y, w, h, r, cls):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
def txt(x, y, s, fs, cls="lbl", anchor="middle", extra=""):
    return f'<text class="{cls}" x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}" {extra}>{s}</text>'

def body(fs, dims=False):
    """A: one body panel, cut outline, stitch line, marks. Origin = top-left cut corner."""
    b = H - N
    s = [f'<path class="pc" d="M0,0H{W}V{b}H{W - N}V{H}H{N}V{b}H0Z"/>']
    pts = [(SA, 0), (SA, b - SA), (N + SA, b - SA), (N + SA, H - SA), (W - N - SA, H - SA), (W - N - SA, b - SA), (W - SA, b - SA), (W - SA, 0)]
    s.append('<polyline class="seam" points="' + " ".join(f"{x},{y}" for x, y in pts) + '"/>')
    s.append(f'<line class="centre" x1="{W / 2}" y1="0" x2="{W / 2}" y2="{H}"/>')
    tx = (W - TAB[0]) / 2
    s.append(rrect(tx, TAB_TOP, TAB[0], TAB[1], 3, "mark") + txt(W / 2, TAB_TOP + TAB[1] + fs * 1.1, "D แม่เหล็ก (ด้านใน)", fs * .8))
    for x in (tx + 4, tx + TAB[0] - 4): s.append(f'<line class="seam" x1="{x}" y1="{TAB_TOP + 4}" x2="{x}" y2="{TAB_TOP + TAB[1] - 4}"/>')
    for sx in (1, -1):                                                    # at each side seam: patch F inside, band feet outside
        seam = SA if sx > 0 else W - SA
        s.append(rrect(min(seam, seam + sx * PATCH[0] / 2), 2, PATCH[0] / 2, PATCH[1], 0, "mark"))
        for y0 in BAND_Y:
            s.append(rrect(min(seam + sx * FOOT[0], seam + sx * FOOT[1]), y0, FOOT[1] - FOOT[0], WRAP[1], 0, "foot"))
            xm = seam + sx * (FOOT[0] + FOOT[1]) / 2
            s.append(f'<line class="seam" x1="{xm}" y1="{y0 + 1.5}" x2="{xm}" y2="{y0 + WRAP[1] - 1.5}"/>')
        s.append(txt(seam + sx * (PATCH[0] / 2 + fs * .4), 2 + PATCH[1] * .55, "ปลอก C ด้านนอก", fs * .8, anchor="start" if sx > 0 else "end"))
        s.append(txt(seam + sx * (PATCH[0] / 2 + fs * .4), 2 + PATCH[1] * .55 + fs, "F ด้านใน", fs * .8, anchor="start" if sx > 0 else "end"))
    s.append(txt(W / 2, TAB_TOP + TAB[1] + fs * 2.2, "ปากกระเป๋าเป็นขอบตัด ไม่เผื่อ", fs * .8))
    s.append(txt(W * .27, H * .42, "A", fs * 3, "big") + txt(W * .27, H * .42 + fs * 1.6, "ตัวกระเป๋า · ตัด 2 ชิ้น", fs))
    s.append(txt(W / 2, H - SA - fs * .6, "ตะเข็บก้น", fs * .8))
    s.append(txt(SA + fs * .6, b * .6, "ตะเข็บข้าง", fs * .8, extra=f'transform="rotate(-90 {SA + fs * .6} {b * .6})" dy="{fs * .8}"'))
    for sx, a in ((1, "start"), (-1, "end")):
        x0 = 0 if sx > 0 else W
        s.append(txt(x0 + sx * (SA + fs * .5), b - SA - fs * .5, "①", fs * 1.2, "num", a))
        s.append(txt(x0 + sx * (N + SA + fs * .5), H - N * .45, "②", fs * 1.2, "num", a))
        s.append(txt(x0 + sx * N / 2, b + N / 2 + fs * .35, f"ตัดออก {cm(N)}×{cm(N)}", fs * .75, "off"))
    if dims:
        s.append(dim_h(0, W, -fs * .9, f"{cm(W)} ซม.", fs))
        s.append(dim_v(-fs * .9, 0, H, f"{cm(H)} ซม.", fs))
        s.append(dim_v(W + fs * .9, 0, b, f"{cm(b)}", fs, side=1))
        s.append(dim_h(N, W - N, H + fs * 1.7, f"{cm(W - 2 * N)}", fs))
    return "".join(s)

def insert(fs, short=False):
    o = (INS - BOARD) / 2
    if short: return rrect(0, 0, INS, INS, INS_R, "pc") + rrect(o, o, BOARD, BOARD, BOARD_R, "mark") + txt(INS / 2, INS / 2, "E", fs * 3, "big") + txt(INS / 2, INS / 2 + fs * 1.6, "เส้นประ = ไส้แข็ง E2", fs)
    return (rrect(0, 0, INS, INS, INS_R, "pc") + rrect(o, o, BOARD, BOARD, BOARD_R, "mark") +
            txt(INS / 2, INS * .42, "E", fs * 3, "big") + txt(INS / 2, INS * .42 + fs * 1.6, "แผ่นรองก้น หนัง · ตัด 2", fs) +
            txt(INS / 2, INS * .42 + fs * 3, f"เส้นประ = ไส้แข็ง E2 · ตัด 1 ({cm(BOARD)} × {cm(BOARD)})", fs * .8))
def tab(fs, short=False):
    g = rrect(0, 0, TAB[0], TAB[1], 3, "pc") + rrect((TAB[0] - MAG[0]) / 2, (TAB[1] - MAG[1]) / 2, MAG[0], MAG[1], 1, "mark")
    for x in (4, TAB[0] - 4): g += f'<line class="seam" x1="{x}" y1="4" x2="{x}" y2="{TAB[1] - 4}"/>'
    return g + txt(TAB[0] / 2, TAB[1] + fs * 1.2, "D" if short else "D แผ่นหุ้มแม่เหล็ก · ตัด 2", fs if short else fs * .85)
def patch(fs, short=False):
    return (rrect(0, 0, PATCH[0], PATCH[1], 4, "pc") + f'<line class="centre" x1="{PATCH[0] / 2}" y1="0" x2="{PATCH[0] / 2}" y2="{PATCH[1]}"/>' +
            txt(PATCH[0] / 2, PATCH[1] + fs * 1.2, "F" if short else "F แผ่นเสริม · ตัด 2", fs if short else fs * .85))
def wrap(fs, short=False):
    f = FOOT[1] - FOOT[0]
    g = rrect(0, 0, WRAP[0], WRAP[1], 0, "pc") + "".join(f'<line class="mark" x1="{x}" y1="0" x2="{x}" y2="{WRAP[1]}"/>' for x in (f, WRAP[0] - f))
    return g + txt(0, WRAP[1] + fs * 1.2, "C" if short else f"C ปลอกรัดโคนสาย · ตัด {NWRAP} ({cm(WRAP[1])} × {cm(WRAP[0])} ซม.) · เส้นประ = ปลายที่เย็บติดตัวกระเป๋า", fs if short else fs * .85, anchor="start")
def strap_end(fs, show=150, short=False):
    """the last part of the strap strip: the end that lies down the outside of the side seam, under the bands"""
    s = [f'<path class="pc" d="M{show},0H0V{STRAP_W}H{show}"/>', f'<path class="tear" d="M{show},0 l-4,{STRAP_W / 4} l4,{STRAP_W / 4} l-4,{STRAP_W / 4} l4,{STRAP_W / 4}"/>']
    s.append(f'<line class="mark" x1="{STRAP_END}" y1="0" x2="{STRAP_END}" y2="{STRAP_W}"/>')
    s.append(f'<line class="cord" x1="2" y1="{STRAP_W / 2}" x2="{show}" y2="{STRAP_W / 2}"/>')
    if short: return "".join(s) + txt(0, STRAP_W + fs * 1.2, "B ปลายสาย · เส้นหนา = เชือกแกน", fs, anchor="start")
    s.append(txt(0, STRAP_W + fs * 1.2, f"ถึงเส้นประ {cm(STRAP_END)} ซม. = ช่วงที่ทับด้านนอกตัวกระเป๋า ใต้ปลอก C", fs * .8, anchor="start"))
    s.append(txt(show - 6, STRAP_W + fs * 1.2, f"B สาย · ตัด 1 · {cm(STRAP_W)} × {cm(STRAP_L)} ซม. (แสดงแค่ปลาย) · เส้นหนา = เชือกแกน", fs * .85, anchor="end"))
    return "".join(s)

def svg(inner, vb, cls="fig", label=""):
    return f'<svg class="{cls}" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" role="img" aria-label="{label}">{inner}</svg>'

# ---------------------------------------------------------------- figures for the summary page and print page 1
def fig_body(fs=13):
    return svg(body(fs, dims=True), (-fs * 2.6, -fs * 2.6, W + fs * 5.4, H + fs * 5.6), label="แพตเทิร์นตัวกระเป๋า")
def fig_parts(fs=11):
    g = (f'<g>{insert(fs, True)}</g><g transform="translate({INS + 14},0)">{patch(fs, True)}</g>'
         f'<g transform="translate({INS + 14},{PATCH[1] + 28})">{tab(fs, True)}</g>'
         f'<g transform="translate(0,{INS + 14})">{wrap(fs, True)}</g><g transform="translate(0,{INS + 42})">{strap_end(fs, 205, True)}</g>')
    return svg(g, (-5, -5, 220, INS + 42 + STRAP_W + fs * 2 + 8), label="ชิ้นเล็ก")
def fig_layout(fs=20):
    LW, LH = LAYOUT; g = [rrect(0, 0, LW, LH, 0, "hide")]; boxes = []
    def put(x, y, w, h, r=0, cls="pc"):
        boxes.append((x, y, x + w, y + h)); return rrect(x, y, w, h, r, cls)
    b = H - N
    for i in range(2):
        x = 6 + i * (W + 6); boxes.append((x, 6, x + W, 6 + H))
        g.append(f'<path class="pc" d="M{x},6H{x + W}V{6 + b}H{x + W - N}V{6 + H}H{x + N}V{6 + b}H{x}Z"/>' + txt(x + W / 2, 6 + H / 2, "A", fs * 2, "big"))
    y = 6 + H + 8
    g.append(put(0, y, STRAP_L, STRAP_W) + txt(STRAP_L / 2, y + STRAP_W / 2 + fs * .35, "B สาย", fs))
    y2 = y + STRAP_W + 8
    for i in range(2): g.append(put(6 + i * (INS + 6), y2, INS, INS, INS_R) + txt(6 + i * (INS + 6) + INS / 2, y2 + INS / 2 + fs * .4, "E", fs * 1.6, "big"))
    x3 = 6 + 2 * (INS + 6) + 6
    for i in range(2): g.append(put(x3 + i * (PATCH[0] + 6), y2, PATCH[0], PATCH[1], 4))
    g.append(txt(x3 + 2 * PATCH[0] + 12, y2 + PATCH[1] / 2 + fs * .35, "F", fs, anchor="start"))
    for i in range(2): g.append(put(x3 + 130, y2 + i * (TAB[1] + 4), TAB[0], TAB[1], 3))
    g.append(txt(x3 + 130 + TAB[0] + fs * .5, y2 + TAB[1] + fs * .5, "D", fs, anchor="start"))
    for i in range(NWRAP): g.append(put(x3 + (i % 3) * (WRAP[0] + 4), y2 + 2 * TAB[1] + 9 + (i // 3) * (WRAP[1] + 3), WRAP[0], WRAP[1]))
    g.append(txt(x3 + 3 * (WRAP[0] + 4) + fs * .2, y2 + 2 * TAB[1] + 9 + 16, "C", fs, anchor="start"))
    half = RIM[0] / 2                                   # the optional rim strip, as two halves
    for i in range(2):
        yy = y2 + INS - (2 - i) * RIM[1] - (1 - i) * 4
        g.append(put(x3, yy, half, RIM[1], 0, "pc opt") + txt(x3 + half / 2, yy + RIM[1] / 2 + fs * .28, "G แถบเสริมปาก (2 ท่อน)" if i == 0 else "G", fs * .75))
    for i, p in enumerate(boxes):
        assert p[0] >= 0 and p[1] >= 0 and p[2] <= LW and p[3] <= LH, ("off the hide", p)
        for q in boxes[i + 1:]: assert p[2] <= q[0] or q[2] <= p[0] or p[3] <= q[1] or q[3] <= p[1], ("overlap", p, q)
    g.append(dim_h(0, LW, -fs * .8, f"{cm(LW)} ซม.", fs) + dim_v(-fs * .8, 0, LH, f"{cm(LH)} ซม.", fs))
    return svg("".join(g), (-fs * 2.4, -fs * 2.4, LW + fs * 3.2, LH + fs * 3.2), label="วางชิ้นบนหนัง")
def fig_bag(fs=15):
    g = ['<path class="pc" d="M-72,0 Q-80,-2 -82,-20 C-90,-120 -100,-200 -97,-272 C-50,-248 50,-248 97,-272 C100,-200 90,-120 82,-20 Q80,-2 72,0 Z"/>',
         f'<path class="strap" d="M-98,{-272 + STRAP_END} L-96,-272 C-82,-420 -40,-535 0,-535 C40,-535 82,-420 96,-272 L98,{-272 + STRAP_END}"/>']
    for sx in (-1, 1):                                   # three bands hold each strap end on the outside, below the rim
        for y0 in BAND_Y: g.append(rrect(sx * 98 - 8, -272 + y0, 16, WRAP[1], 2, "band"))
    for sx in (-1, 1): g.append(f'<line class="stitch" x1="{sx * (TAB[0] / 2 - 4)}" y1="{-254 + TAB_TOP + 4}" x2="{sx * (TAB[0] / 2 - 4)}" y2="{-254 + TAB_TOP + TAB[1] - 4}"/>')
    g.append(dim_h(-75, 75, fs * 1.9, f"ก้น {cm(BASE)} × {cm(BASE)} ซม.", fs))
    g.append(dim_v(135, -272, 0, f"สูง {cm(HEIGHT)} ซม.", fs, side=1))
    g.append(dim_v(135, -535, -272, f"สาย {cm(DROP)} ซม.", fs, side=1))
    g.append(txt(0, -254 + TAB_TOP + TAB[1] + fs * 1.1, "รอยเย็บแผ่นแม่เหล็ก", fs * .8) + txt(-112, -250, "ปลอกรัด 3 เส้น", fs * .8, anchor="end"))
    return svg("".join(g), (-200, -560, 380, 600), label="รูปกระเป๋าและขนาด")
def fig_corner(fs=12, part=None):
    g = ['<path class="pc" d="M30,10H150V130H80V80H30Z"/>', '<line class="seam" x1="30" y1="10" x2="30" y2="80"/>', '<line class="seam" x1="80" y1="130" x2="150" y2="130"/>',
         txt(55, 74, "①", fs * 1.2, "num"), txt(88, 108, "②", fs * 1.2, "num", "start"), txt(20, 48, "ตะเข็บข้าง", fs * .8, extra='transform="rotate(-90 20 48)"'),
         txt(115, 145, "ตะเข็บก้น", fs * .8), txt(90, 0, "1 เย็บข้างและก้นแล้ว มุมเป็นรู", fs * .9),
         '<path class="arrow" d="M165,70 H200 m-8,-6 l8,6 l-8,6"/>',
         '<path class="pc" d="M220,90 L206,24 l14,5 l14,-5 l14,5 l14,-5 l14,5 l14,-5 l14,5 l14,-5 l14,5 l14,-5 l14,5 l14,-5 L360,90 Z"/>', '<line class="seam" x1="290" y1="27" x2="290" y2="90"/>', '<line class="stitchline" x1="228" y1="82" x2="352" y2="82"/>',
         txt(255, 72, "①", fs * 1.2, "num"), txt(325, 72, "②", fs * 1.2, "num"), txt(290, 46, "ตัวกระเป๋า", fs * .8, "off"), txt(290, 0, "2 จับ ① ชน ② ตะเข็บทับกัน", fs * .9),
         dim_h(220, 360, 118, f"เย็บขวาง {cm(BASE)} ซม. ซ้ำ 2 รอบ", fs * .85)]
    return svg("".join(g), {None: (0, -16, 380, 150), 1: (4, -16, 158, 166), 2: (204, -16, 176, 150)}[part], "fig" + (" half" if part else ""), "วิธีทำมุมก้น")
def fig_strap(fs=12, part=None):
    g = [txt(60, 0, "หน้าตัดสาย", fs * .9), '<circle class="cordc" cx="60" cy="50" r="18"/>',
         '<path class="leath" d="M52,104 V74 A26,26 0 1 1 68,74 V104"/>', '<line class="stitchline" x1="44" y1="80" x2="76" y2="80"/>',
         txt(60, 54, "เชือก", fs * .8), txt(92, 84, "เย็บชิดเชือก", fs * .8, anchor="start"), txt(92, 104, "ตัดครีบเหลือ 2 มม.", fs * .8, anchor="start"),
         txt(300, 0, "โคนสาย มองจากด้านนอก", fs * .9),
         '<line class="rim" x1="210" y1="50" x2="370" y2="50"/>', '<line class="seam" x1="290" y1="50" x2="290" y2="128"/>',
         rrect(270, 52, 40, 50, 4, "mark"), f'<path class="strapd" d="M290,14 V{50 + STRAP_END}"/>']
    for y0 in BAND_Y:
        g.append(rrect(290 - FOOT[1], 50 + y0, 2 * FOOT[1], WRAP[1], 2, "band"))
        for x in (290 - 8.5, 290 + 8.5): g.append(f'<line class="stitchline" x1="{x}" y1="{50 + y0 + 1.5}" x2="{x}" y2="{50 + y0 + 7.5}"/>')
    g += [txt(318, 40, f"สายทับด้านนอก {cm(STRAP_END)} ซม.", fs * .8, anchor="start"), txt(318, 62, "ปลอก C 3 เส้น คาดทับสาย", fs * .8, anchor="start"),
          txt(318, 78, "เย็บปลายปลอกสองข้าง ทะลุถึง F", fs * .8, anchor="start"), txt(318, 100, "เส้นประ = แผ่นเสริม F ด้านใน", fs * .8, anchor="start"),
          txt(216, 46, "ปากกระเป๋า", fs * .8, anchor="start"), txt(284, 124, "ตะเข็บข้าง", fs * .8, anchor="end")]
    return svg("".join(g), {None: (0, -16, 470, 150), 1: (22, -16, 180, 130), 2: (205, -16, 268, 150)}[part], "fig" + ({None: "", 1: " half", 2: " half wide"}[part]), "สายและโคนสาย")

# ---------------------------------------------------------------- print pages (A4, 1:1)
PW, PH, M = 210, 297, 10
WIN = (PW - 2 * M, PH - 2 * M)              # 190 x 277 printable window
COLS, ROWS = math.ceil(W / WIN[0]), math.ceil((H + 12) / WIN[1])
OX, OY = (COLS * WIN[0] - W) / 2, 14
FIRST = 3                                   # first tile page: 1 overview, 2 steps
NPAGES = FIRST - 1 + COLS * ROWS + 1
def tile(c, r, page):
    fs = 3.6
    g = [f'<clipPath id="w{page}"><rect x="{M}" y="{M}" width="{WIN[0]}" height="{WIN[1]}"/></clipPath>',
         f'<g clip-path="url(#w{page})"><g transform="translate({M - c * WIN[0] + OX},{M - r * WIN[1] + OY})">{body(fs)}</g></g>',
         f'<rect class="frame" x="{M}" y="{M}" width="{WIN[0]}" height="{WIN[1]}"/>']
    pg = lambda cc, rr: FIRST + rr * COLS + cc
    if c + 1 < COLS:
        x = M + WIN[0]; g.append(f'<path class="join" d="M{x},{PH / 2 - 5} l-5,5 l5,5 Z"/>' + txt(x - 3, PH / 2 - 9, f"ต่อกับหน้า {pg(c + 1, r)} ▶", 3, "pg", "end"))
    if c > 0:
        g.append(f'<path class="join" d="M{M},{PH / 2 - 5} l5,5 l-5,5 Z"/>' + txt(M + 3, PH / 2 - 9, f"◀ ต่อกับหน้า {pg(c - 1, r)}", 3, "pg", "start"))
    if r + 1 < ROWS:
        y = M + WIN[1]; g.append(f'<path class="join" d="M{PW / 2 - 5},{y} l5,-5 l5,5 Z"/>' + txt(PW / 2 + 9, y - 2, f"▼ ต่อกับหน้า {pg(c, r + 1)}", 3, "pg", "start"))
    if r > 0:
        g.append(f'<path class="join" d="M{PW / 2 - 5},{M} l5,5 l5,-5 Z"/>' + txt(PW / 2 + 9, M + 4, f"▲ ต่อกับหน้า {pg(c, r - 1)}", 3, "pg", "start"))
    g.append(txt(M, PH - 4.5, f"OCT. 26 · กระเป๋าทรงถัง · A ตัวกระเป๋า · หน้า {page}/{NPAGES} · แถว {r + 1} คอลัมน์ {c + 1} · พิมพ์ 100% ตัดตามกรอบเทา แล้วต่อชนกัน", 2.8, "pg", "start"))
    return f'<section class="page"><svg viewBox="0 0 {PW} {PH}">{"".join(g)}</svg></section>'
def scale_square(x, y):
    return (f'<rect class="scale" x="{x}" y="{y}" width="50" height="50"/>' + txt(x + 25, y + 24, "5 × 5 ซม.", 3.4) + txt(x + 25, y + 30, "วัดก่อนตัด", 3))
def parts_page(page):
    fs = 3.4
    g = [f'<g transform="translate({M + 2},{M + 4})">', f'<g>{insert(fs)}</g>', f'<g transform="translate({TAB[0] + 74},{INS + 8})">{patch(fs)}</g>',
         f'<g transform="translate(0,{INS + 8})">{tab(fs)}</g>', scale_square(TAB[0] + 12, INS + 8),
         f'<g transform="translate(0,{INS + 64})">{wrap(fs)}</g>', f'<g transform="translate(0,{INS + 78})">{strap_end(fs, 180)}</g>',
         txt(0, INS + 78 + STRAP_W + 12, f"G แถบเสริมปาก (ใช้เมื่อหนังบางกว่า 1.4 มม.): ตัดด้วยไม้บรรทัด {cm(RIM[1])} × {cm(RIM[0])} ซม. ต่อ 2 ท่อนได้", fs, anchor="start"),
         txt(0, INS + 78 + STRAP_W + 17.5, f"B สาย: ตัดด้วยไม้บรรทัด {cm(STRAP_W)} × {cm(STRAP_L)} ซม. · เชือกแกน {CORD} มม. ยาว {cm(CORD_L)} ซม.", fs, anchor="start"), '</g>',
         f'<rect class="frame" x="{M}" y="{M}" width="{WIN[0]}" height="{WIN[1]}"/>',
         txt(M, PH - 4.5, f"OCT. 26 · กระเป๋าทรงถัง · ชิ้นเล็ก ขนาดจริง · หน้า {page}/{NPAGES} · พิมพ์ 100%", 2.8, "pg", "start")]
    return f'<section class="page"><svg viewBox="0 0 {PW} {PH}">{"".join(g)}</svg></section>'

E = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;")
cut_rows = "".join(f'<tr><th>{l}</th><td>{E(n)}</td><td class="num">{q}</td><td class="num">{s}</td><td>{E(note)}</td></tr>' for l, n, q, s, note in CUTS)
STEPS = [
    "ถ้าหนังหนาเกิน 1.4 มม. ฝานหลังหนังตรงเผื่อตะเข็บให้บางลงครึ่งหนึ่ง กว้าง 1 ซม. ที่ขอบข้าง ขอบก้น และขอบ ① ② ของ A ทั้งสองชิ้น",
    "ทากาวแม่เหล็กไว้ใต้แผ่น D วางด้านในของ A ทั้งสองชิ้นตามเส้นประ ลองให้ดูดกันก่อน แล้วเย็บเฉพาะปลายสั้นสองข้างของ D ทากาวรอบแม่เหล็กกันเลื่อน",
    f"ประกบหน้าหนังเข้าหากัน เย็บตะเข็บข้างสองด้าน แล้วเย็บตะเข็บก้น ห่างขอบ {SA} มม.",
    "แบะตะเข็บออก ทากาวยาง ตอกให้เรียบ",
    f"ทำมุมก้น: จับขอบ ① ชนขอบ ② ให้ตะเข็บข้างทับตะเข็บก้น เย็บขวาง {cm(BASE)} ซม. เย็บซ้ำ 2 รอบ ทำทั้งสองมุม",
    "กลับด้านให้หน้าหนังออก",
    "ทำสาย: พับ B หุ้มเชือกแกน เย็บชิดเชือกเฉพาะช่วงกลาง 45 ซม. ก่อน เว้นปลายข้างละราว 12 ซม. ไว้ยังไม่เย็บ",
    f"ลองสายกับตัวกระเป๋า ให้ปลายสายทับด้านนอกตรงตะเข็บข้าง ลงมาจากปาก {cm(STRAP_END)} ซม. ขีดปลายสายทั้งสองข้าง เย็บหุ้มเชือกต่อจนถึงขีด ตัดครีบเหลือ 2 มม. แล้วตัดสายที่ขีด",
    "ติดแผ่นเสริม F ด้านใน ทับตะเข็บข้าง ทากาวปลายสายวางทับตะเข็บด้านนอก หันครีบเข้าหาตัวกระเป๋า เย็บมือทะลุสายและเชือกแกนเข้าตัวกระเป๋าถึงแผ่น F 3 จุด ตรงตำแหน่งปลอก",
    "คาดปลอก C ทับสาย ข้างละ 3 เส้น เย็บปลายปลอกทั้งสองข้างติดตัวกระเป๋าตามเส้นประแดง ให้ทะลุถึงแผ่น F ปลอกจะปิดรอยเย็บมือในขั้นก่อน",
    "ทำแผ่นรองก้น: ประกบ E สองชิ้น มีไส้แข็ง E2 ตรงกลาง ทากาว เย็บรอบ แล้ววางลงก้น",
]
steps_html = "".join(f"<li>{E(s)}</li>" for s in STEPS)
SHOP = [
    ("หนังวัวนิ่มลายลิ้นจี่", f"หนา 1.6–1.8 มม. ชิ้นเดียวอย่างน้อย {cm(LAYOUT[0])} × {cm(LAYOUT[1])} ซม. หรือซื้อ 5–6 ตร.ฟุต"),
    ("เชือกแกนสาย", f"ไนลอนหรือฝ้ายถัก {CORD} มม. ยาว {cm(CORD_L)} ซม."),
    ("แม่เหล็กแท่ง", f"{MAG[0]} × {MAG[1]} × 2 มม. 2 ชิ้น ขั้วอยู่ที่หน้ากว้าง"),
    ("ไส้แข็งแผ่นรองก้น", f"กระดาษอัดหรือแผ่น PE 1.5–2 มม. ขนาด {cm(BOARD)} × {cm(BOARD)} ซม."),
    ("ด้ายและเข็ม", "ด้ายไนลอนหรือโพลีเอสเตอร์เบอร์ 20 · เข็มปลายมีดขนาดที่เข้ากับด้าย ลองกับเศษหนังก่อน"),
    ("กาว", "กาวยาง สำหรับแบะตะเข็บและประกบแผ่นรองก้น"),
]
shop_rows = "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in SHOP)

SUB = {
    "__FIG_BAG__": fig_bag(), "__FIG_BODY__": fig_body(), "__FIG_PARTS__": fig_parts(), "__FIG_LAYOUT__": fig_layout(),
    "__FIG_CORNER__": fig_corner(12, 1) + fig_corner(12, 2), "__FIG_STRAP__": fig_strap(12, 1) + fig_strap(12, 2), "__CUTROWS__": cut_rows, "__STEPS__": steps_html, "__SHOPROWS__": shop_rows,
    "__NPAGES__": str(NPAGES), "__NCUT__": str(2 + 1 + NWRAP + 2 + 2 + 1 + 2), "__T1__": str(FIRST), "__T2__": str(FIRST - 1 + COLS * ROWS), "__NTILES__": str(COLS * ROWS), "__BODY__": f"{cm(W)} × {cm(H)}", "__NOTCH__": cm(N), "__SA__": str(SA),
    "__AREA__": f"{AREA:.2f}", "__SQFT__": f"{sqft(AREA):.1f}", "__LAYOUT__": f"{cm(LAYOUT[0])} × {cm(LAYOUT[1])}",
    "__STRAP__": f"{cm(STRAP_W)} × {cm(STRAP_L)}", "__BASE__": cm(BASE), "__HEIGHT__": cm(HEIGHT), "__DROP__": cm(DROP),
}
page = open(os.path.join(HERE, "template.html")).read()
for k, v in SUB.items(): page = page.replace(k, v)
open(os.path.join(HERE, "index.html"), "w").write(page)

FONTS = "../../brand-20261014/fonts"
PRINT_CSS = f"""
@font-face{{font-family:"Plex Thai";src:url("{FONTS}/IBMPlexSansThai-Regular.ttf");font-weight:400}}
@font-face{{font-family:"Plex Thai";src:url("{FONTS}/IBMPlexSansThai-SemiBold.ttf");font-weight:600}}
@font-face{{font-family:"Anuphan";src:url("{FONTS}/alt/Anuphan-Medium.ttf")}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:#fff;color:#2A2725;font-family:"Plex Thai",sans-serif}}
.page{{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;break-after:page}}
.page:last-child{{page-break-after:auto;break-after:auto}}
.page > svg{{position:absolute;inset:0;width:210mm;height:297mm}}
svg text{{font-family:"Plex Thai",sans-serif;fill:#2A2725}}
.pc{{fill:#fff;stroke:#2A2725;stroke-width:.45}}
.pc.opt{{stroke-dasharray:2 1.2}}
.hide{{fill:#F4F0E8;stroke:#8C8A85;stroke-width:.4}}
.seam,.stitchline{{fill:none;stroke:#A9442B;stroke-width:.3;stroke-dasharray:2 1.2}}
.centre{{stroke:#8C8A85;stroke-width:.25;stroke-dasharray:6 1.5 1 1.5}}
.mark{{fill:none;stroke:#2E4A7D;stroke-width:.3;stroke-dasharray:1.2 1}}
.foot{{fill:none;stroke:#2E4A7D;stroke-width:.3}}
.band{{fill:#C9A27C;stroke:#2A2725;stroke-width:.6}}
.dim line{{stroke:#2A2725;stroke-width:.25}}
.big{{font-family:"Anuphan","Plex Thai",sans-serif;fill:#8C8A85}}
.num{{fill:#A9442B;font-weight:600}}
.off{{fill:#8C8A85}}
.frame{{fill:none;stroke:#B9B5AD;stroke-width:.25}}
.join{{fill:#2A2725}}
.pg{{fill:#5E5953}}
.scale{{fill:none;stroke:#2A2725;stroke-width:.4}}
.tear{{fill:none;stroke:#2A2725;stroke-width:.3}}
.cord{{stroke:#2A2725;stroke-width:1.6;stroke-linecap:round;opacity:.55}}
.strap,.strapd{{fill:none;stroke:#2A2725;stroke-width:9;stroke-linecap:round}}
.strapd{{stroke-width:8}}
.wrapl{{stroke:#fff;stroke-width:1.6}}
.stitch{{stroke:#2A2725;stroke-width:1}}
.arrow{{fill:none;stroke:#2A2725;stroke-width:1.2}}
.rim{{stroke:#2A2725;stroke-width:1.6}}
.cordc{{fill:#E4DCCD;stroke:#2A2725;stroke-width:.8}}
.leath{{fill:none;stroke:#8B5E3C;stroke-width:5}}
.leathf{{fill:#C9A27C;stroke:#2A2725;stroke-width:.6}}
.p1{{padding:12mm 12mm 10mm;display:grid;gap:4mm;align-content:start;font-size:9.5pt;line-height:1.45}}
.p1 h1{{font-family:"Anuphan","Plex Thai",sans-serif;font-size:19pt;margin:0;font-weight:500}}
.p1 h2{{font-family:"Anuphan","Plex Thai",sans-serif;font-size:11.5pt;margin:0 0 1mm;font-weight:500}}
.p1 .eyebrow{{font-size:8pt;letter-spacing:.08em;color:#5E5953;margin:0}}
.p1 p{{margin:0}} .p1 ol{{margin:0;padding-left:5mm}} .p1 li{{margin-bottom:.6mm}}
.p1 table{{border-collapse:collapse;width:100%;font-size:8.6pt}} .p1 th,.p1 td{{border-bottom:.2mm solid #D9D2C4;padding:.9mm 1.5mm;text-align:left;vertical-align:top}}
.p1 .grid{{display:grid;grid-template-columns:76mm 1fr;gap:5mm;align-items:start}}
.p1 .grid2{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;align-items:start}}
.p1 svg.fig{{width:100%;height:auto;display:block}}
.p1 .fig .dim line{{stroke-width:.8}} .p1 .fig .pc{{stroke-width:1.2}} .p1 .fig .seam,.p1 .fig .stitchline{{stroke-width:1;stroke-dasharray:5 3}}
.p1 .fig .mark{{stroke-width:.9;stroke-dasharray:3 2.5}} .p1 .fig .foot{{stroke-width:.8}} .p1 .fig .centre{{stroke-width:.7}} .p1 .fig .hide{{stroke-width:1}}
.p1 .check{{display:flex;gap:5mm;align-items:center;border:.3mm solid #2A2725;border-radius:2mm;padding:3mm 4mm}}
.p1 .check svg{{width:50mm;height:50mm;flex:none}}
.p1 .note{{font-size:8pt;color:#5E5953}}
.p1 ol.big{{font-size:11pt;line-height:1.5}} .p1 ol.big li{{margin-bottom:1.6mm}}
.p1 .grid2 th{{white-space:nowrap}} .p1 td.num{{white-space:nowrap}}
"""
p1 = f"""<section class="page p1">
<p class="eyebrow">OCT. 26 · PRODUCT DEVELOPMENT · 18 พ.ย. 2569 · หน้า 1/{NPAGES}</p>
<h1>แพตเทิร์นกระเป๋าทรงถัง ก้น {cm(BASE)} × {cm(BASE)} สูง {cm(HEIGHT)} ซม.</h1>
<div class="check"><svg viewBox="0 0 50 50"><rect class="scale" x=".2" y=".2" width="49.6" height="49.6"/><text x="25" y="27" font-size="4" text-anchor="middle">5 × 5 ซม.</text></svg>
<div><b>ก่อนตัด:</b> พิมพ์ที่ 100% (Actual size) ห้ามเลือก Fit to page แล้ววัดสี่เหลี่ยมนี้ ต้องได้ 5 × 5 ซม. พอดี<br>
หน้า {FIRST}–{FIRST - 1 + COLS * ROWS}: ตัดตามกรอบเส้นเทา ต่อชนกันด้วยเทปใส ให้สามเหลี่ยมดำชนกันเป็นข้าวหลามตัด จะได้ชิ้น A เต็มใบ<br>
หน้า {NPAGES}: ชิ้นเล็กขนาดจริง · สาย B และแถบ G ตัดด้วยไม้บรรทัดตามตาราง<br>
ทุกชิ้นรวมเผื่อตะเข็บ {SA} มม. แล้ว · เส้นประแดง = แนวเย็บ · เส้นประน้ำเงิน = ตำแหน่งติดชิ้นอื่น</div></div>
<div class="grid"><div>{fig_body(13)}</div>
<div><h2>รายการตัด (ซม.)</h2><table><tbody>{cut_rows}</tbody></table>
<p class="note" style="margin-top:2mm">หนังที่ใช้ {AREA:.2f} ตร.ม. ({sqft(AREA):.1f} ตร.ฟุต) ไม่รวมแถบ G · แพตเทิร์นนี้คิดจากหนังหนา 1.6–1.8 มม.</p></div></div>
<div class="grid2"><div><h2>วางชิ้นบนหนัง {cm(LAYOUT[0])} × {cm(LAYOUT[1])} ซม.</h2>{fig_layout(20)}</div>
<div><h2>ของที่ต้องซื้อ</h2><table><tbody>{shop_rows}</tbody></table></div></div>
<p class="note">ขนาดอ่านจากรูปอ้างอิง 2 รูป ยังไม่ได้ทำต้นแบบ · ทำใบแรกด้วยผ้าหรือหนังเทียมก่อนตัดหนังจริง</p>
</section>"""
p2 = f"""<section class="page p1">
<p class="eyebrow">OCT. 26 · กระเป๋าทรงถัง · หน้า 2/{NPAGES}</p>
<h1>ลำดับเย็บ</h1>
<ol class="big">{steps_html}</ol>
<div style="max-width:150mm"><h2>มุมก้น</h2>{fig_corner(12)}</div>
<div style="max-width:150mm"><h2>สายและโคนสาย</h2>{fig_strap(12)}</div>
<p class="note">มุมก้นหนาที่สุด หนังซ้อน 4 ชั้น ราว 7 มม. ถ้าหนังหนา 1.6–1.8 มม. จึงต้องฝานก่อน แล้วใช้จักรตีนตะขาบหรือเย็บมือ · สายที่มองเห็นน่าจะยาว 52–58 ซม. ลองกับตัวกระเป๋าก่อนตัด · โคนสายด้านนอกทำตามรูปอ้างอิง ส่วนรอยเย็บมือใต้ปลอกเป็นวิธีที่แนะนำ รูปมองไม่เห็น<br>
ใบจริงเสร็จแล้ว ใส่ของ 3 กก. แขวนค้างคืน ดูโคนสายและมุมก้นก่อนใช้งานหรือขาย</p>
</section>"""
tiles = "".join(tile(c, r, FIRST + r * COLS + c) for r in range(ROWS) for c in range(COLS))
doc = f'<!doctype html><html lang="th"><head><meta charset="utf-8"><title>OCT. 26 แพตเทิร์นกระเป๋าทรงถัง</title><style>{PRINT_CSS}</style></head><body>{p1}{p2}{tiles}{parts_page(NPAGES)}</body></html>'
open(os.path.join(HERE, "print.html"), "w").write(doc)
print(f"bucketbag: body {W} x {H} notch {N} · strap {STRAP_W} x {STRAP_L} · tiles {COLS}x{ROWS} · pages {NPAGES} · leather {AREA:.3f} m2 = {sqft(AREA):.1f} sqft")
