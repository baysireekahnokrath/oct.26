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
STRAP_SEEN, STRAP_END = 580, 40             # arch over a 26 cm drop; flat end sewn inside
STRAP_L = 700                               # STRAP_SEEN + 2 ends + 40 spare
CORD_L = STRAP_SEEN + 2 * 15                # the core runs 15 mm into each sewn end
WRAP = (150, 6)
TAB = (48, 24); TAB_TOP = 30                # magnet tab, its top edge 30 below the rim
PATCH = (40, 50)
INS, INS_R, BOARD, BOARD_R = BASE - 5, 15, BASE - 11, 12
RIM = (2 * BASE * 2 + 15, 20)               # optional strip inside the rim for leather under 1.4 mm
LAYOUT = (700, 580)                         # one piece of leather that takes everything
cm = lambda v: (f"{v / 10:.1f}".rstrip("0").rstrip("."))
sqft = lambda m2: m2 * 10.7639
AREA = (2 * W * H + STRAP_L * STRAP_W + 2 * INS * INS + 2 * TAB[0] * TAB[1] + 2 * PATCH[0] * PATCH[1] + 2 * WRAP[0] * WRAP[1]) / 1e6

CUTS = [  # letter, name, qty, cut size, note
    ("A", "ตัวกระเป๋า", "2", f"{cm(W)} × {cm(H)}", f"ตัดมุมล่างออก 2 มุม มุมละ {cm(N)} × {cm(N)} · รวมเผื่อตะเข็บ {SA} มม. แล้ว"),
    ("B", "สาย", "1", f"{cm(STRAP_W)} × {cm(STRAP_L)}", f"หุ้มเชือกแกน {CORD} มม. ยาว {cm(CORD_L)} ซม. · ตัดปลายทิ้งตอนติด"),
    ("C", "ปลอกพันโคนสาย", "2", f"{cm(WRAP[1])} × {cm(WRAP[0])}", "พันข้างละ 3 รอบ"),
    ("D", "แผ่นหุ้มแม่เหล็ก", "2", f"{cm(TAB[0])} × {cm(TAB[1])}", "แม่เหล็กกลม 18 × 2 มม. 2 เม็ด"),
    ("E", "แผ่นรองก้น หนัง", "2", f"{cm(INS)} × {cm(INS)}", f"มุมมน รัศมี {cm(INS_R)}"),
    ("E2", "แผ่นรองก้น ไส้แข็ง", "1", f"{cm(BOARD)} × {cm(BOARD)}", "กระดาษอัดหรือแผ่น PE หนา 1.5–2 มม."),
    ("F", "แผ่นเสริมโคนสาย", "2", f"{cm(PATCH[0])} × {cm(PATCH[1])}", "ติดด้านใน ทับตะเข็บข้าง"),
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
    for x in (SA, W - SA - PATCH[0] / 2):
        s.append(rrect(x, 6, PATCH[0] / 2, PATCH[1], 0, "mark"))
    s.append(txt(SA + PATCH[0] / 2 + fs * .4, 6 + PATCH[1] / 2, "F + สาย", fs * .8, anchor="start"))
    s.append(txt(W - SA - PATCH[0] / 2 - fs * .4, 6 + PATCH[1] / 2, "F + สาย", fs * .8, anchor="end"))
    s.append(txt(W / 2, fs * 1.3, "ปากกระเป๋า ขอบตัด ไม่เผื่อ", fs * .8))
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
    return (rrect(0, 0, TAB[0], TAB[1], 3, "pc") + rrect(3, 3, TAB[0] - 6, TAB[1] - 6, 1.5, "seam") +
            f'<circle class="mark" cx="{TAB[0] / 2}" cy="{TAB[1] / 2}" r="9"/>' + txt(TAB[0] / 2, TAB[1] + fs * 1.2, "D" if short else "D แผ่นหุ้มแม่เหล็ก · ตัด 2", fs if short else fs * .85))
def patch(fs, short=False):
    return (rrect(0, 0, PATCH[0], PATCH[1], 4, "pc") + f'<line class="centre" x1="{PATCH[0] / 2}" y1="0" x2="{PATCH[0] / 2}" y2="{PATCH[1]}"/>' +
            txt(PATCH[0] / 2, PATCH[1] + fs * 1.2, "F" if short else "F แผ่นเสริม · ตัด 2", fs if short else fs * .85))
def wrap(fs, short=False):
    return rrect(0, 0, WRAP[0], WRAP[1], 0, "pc") + txt(0, WRAP[1] + fs * 1.2, "C" if short else f"C ปลอกพันโคนสาย · ตัด 2 ({cm(WRAP[1])} × {cm(WRAP[0])} ซม.)", fs if short else fs * .85, anchor="start")
def strap_end(fs, show=150, short=False):
    """the last 150 mm of the strap strip: where the core stops, where the flat end is sewn"""
    s = [f'<path class="pc" d="M{show},0H0V{STRAP_W}H{show}"/>', f'<path class="tear" d="M{show},0 l-4,{STRAP_W / 4} l4,{STRAP_W / 4} l-4,{STRAP_W / 4} l4,{STRAP_W / 4}"/>']
    s.append(f'<line class="mark" x1="{STRAP_END}" y1="0" x2="{STRAP_END}" y2="{STRAP_W}"/>')
    s.append(f'<line class="cord" x1="{STRAP_END - 15}" y1="{STRAP_W / 2}" x2="{show}" y2="{STRAP_W / 2}"/>')
    if short: return "".join(s) + txt(0, STRAP_W + fs * 1.2, "B ปลายสาย · เส้นหนา = เชือกแกน", fs, anchor="start")
    s.append(txt(STRAP_END / 2 - 3, STRAP_W * .3, "ปลายแบน", fs * .8) + txt(STRAP_END / 2, STRAP_W + fs * 1.2, f"เย็บติดด้านใน {cm(STRAP_END)} ซม.", fs * .8))
    s.append(txt(show - 6, STRAP_W + fs * 1.2, f"B สาย · ตัด 1 · {cm(STRAP_W)} × {cm(STRAP_L)} ซม. (รูปนี้แสดงแค่ปลาย) · เส้นหนา = เชือกแกน", fs * .85, anchor="end"))
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
    LW, LH = LAYOUT; g = [rrect(0, 0, LW, LH, 0, "hide")]
    b = H - N
    for i in range(2):
        x = 6 + i * (W + 6)
        g.append(f'<path class="pc" d="M{x},6H{x + W}V{6 + b}H{x + W - N}V{6 + H}H{x + N}V{6 + b}H{x}Z"/>' + txt(x + W / 2, 6 + H / 2, "A", fs * 2, "big"))
    y = 6 + H + 8
    g.append(rrect(0, y, STRAP_L, STRAP_W, 0, "pc") + txt(STRAP_L / 2, y + STRAP_W / 2 + fs * .35, "B สาย", fs))
    y2 = y + STRAP_W + 8
    for i in range(2): g.append(rrect(6 + i * (INS + 6), y2, INS, INS, INS_R, "pc") + txt(6 + i * (INS + 6) + INS / 2, y2 + INS / 2 + fs * .4, "E", fs * 1.6, "big"))
    x3 = 6 + 2 * (INS + 6) + 6
    for i in range(2): g.append(rrect(x3 + i * (PATCH[0] + 6), y2, PATCH[0], PATCH[1], 4, "pc"))
    g.append(txt(x3 + PATCH[0] + 3, y2 + PATCH[1] + fs, "F", fs))
    for i in range(2): g.append(rrect(x3 + 100 + i * 0, y2 + i * (TAB[1] + 6), TAB[0], TAB[1], 3, "pc"))
    g.append(txt(x3 + 100 + TAB[0] + fs * .6, y2 + TAB[1] + 8, "D", fs, anchor="start"))
    for i in range(2): g.append(rrect(x3, y2 + PATCH[1] + fs * 1.6 + i * 12, WRAP[0], WRAP[1], 0, "pc"))
    g.append(txt(x3 + WRAP[0] + fs * .5, y2 + PATCH[1] + fs * 1.6 + 14, "C", fs, anchor="start"))
    g.append(rrect(x3, y2 + INS - RIM[1], LW - x3 - 6, RIM[1], 0, "pc opt") + txt(x3 + (LW - x3 - 6) / 2, y2 + INS - RIM[1] / 2 + fs * .35, "G แถบเสริมปาก (ต่อ 2 ท่อน)", fs * .8))
    g.append(dim_h(0, LW, -fs * .8, f"{cm(LW)} ซม.", fs) + dim_v(-fs * .8, 0, LH, f"{cm(LH)} ซม.", fs))
    return svg("".join(g), (-fs * 2.4, -fs * 2.4, LW + fs * 3.2, LH + fs * 3.2), label="วางชิ้นบนหนัง")
def fig_bag(fs=15):
    g = ['<path class="strap" d="M-95,-262 C-80,-420 -40,-535 0,-535 C40,-535 80,-420 95,-262"/>',
         '<path class="pc" d="M-72,0 Q-80,-2 -82,-20 C-90,-120 -100,-200 -97,-272 C-50,-248 50,-248 97,-272 C100,-200 90,-120 82,-20 Q80,-2 72,0 Z"/>']
    for sx in (-1, 1):
        for k in range(3): g.append(f'<line class="wrapl" x1="{sx * 89}" y1="{-276 - k * 8}" x2="{sx * 101}" y2="{-274 - k * 8}"/>')
        g.append(f'<line class="stitch" x1="{sx * 20}" y1="-226" x2="{sx * 20}" y2="-212"/>')
    g.append(dim_h(-75, 75, fs * 1.9, f"ก้น {cm(BASE)} × {cm(BASE)} ซม.", fs))
    g.append(dim_v(125, -272, 0, f"สูง {cm(HEIGHT)} ซม.", fs, side=1))
    g.append(dim_v(125, -535, -272, f"สาย {cm(DROP)} ซม.", fs, side=1))
    g.append(txt(0, -200, "รอยเย็บแม่เหล็ก", fs * .8) + txt(-108, -300, "ปลอกพัน", fs * .8, anchor="end"))
    return svg("".join(g), (-190, -560, 370, 600), label="รูปกระเป๋าและขนาด")
def fig_corner(fs=12, part=None):
    g = ['<path class="pc" d="M30,10H150V130H80V80H30Z"/>', '<line class="seam" x1="30" y1="10" x2="30" y2="80"/>', '<line class="seam" x1="80" y1="130" x2="150" y2="130"/>',
         txt(55, 74, "①", fs * 1.2, "num"), txt(88, 108, "②", fs * 1.2, "num", "start"), txt(20, 48, "ตะเข็บข้าง", fs * .8, extra='transform="rotate(-90 20 48)"'),
         txt(115, 145, "ตะเข็บก้น", fs * .8), txt(90, 0, "1 เย็บข้างและก้นแล้ว มุมเป็นรู", fs * .9),
         '<path class="arrow" d="M165,70 H200 m-8,-6 l8,6 l-8,6"/>',
         '<path class="pc" d="M220,90 L206,24 l14,5 l14,-5 l14,5 l14,-5 l14,5 l14,-5 l14,5 l14,-5 l14,5 l14,-5 l14,5 l14,-5 L360,90 Z"/>', '<line class="seam" x1="290" y1="27" x2="290" y2="90"/>', '<line class="stitchline" x1="228" y1="82" x2="352" y2="82"/>',
         txt(255, 72, "①", fs * 1.2, "num"), txt(325, 72, "②", fs * 1.2, "num"), txt(290, 46, "ตัวกระเป๋า", fs * .8, "off"), txt(290, 0, "2 จับ ① ชน ② ตะเข็บทับกันตรงกลาง", fs * .9),
         dim_h(220, 360, 118, f"เย็บขวาง {cm(BASE)} ซม. ซ้ำ 2 รอบ", fs * .85)]
    return svg("".join(g), {None: (0, -16, 380, 150), 1: (4, -16, 158, 166), 2: (204, -16, 176, 150)}[part], "fig" + (" half" if part else ""), "วิธีทำมุมก้น")
def fig_strap(fs=12, part=None):
    g = [txt(60, 0, "หน้าตัดสาย", fs * .9), '<circle class="cordc" cx="60" cy="50" r="18"/>',
         '<path class="leath" d="M52,104 V74 A26,26 0 1 1 68,74 V104"/>', '<line class="stitchline" x1="44" y1="80" x2="76" y2="80"/>',
         txt(60, 54, "เชือก", fs * .8), txt(92, 84, "เย็บชิดเชือก", fs * .8, anchor="start"), txt(92, 104, "ตัดครีบเหลือ 2 มม.", fs * .8, anchor="start"),
         txt(290, 0, "โคนสาย มองจากด้านในกระเป๋า", fs * .9),
         '<line class="rim" x1="210" y1="50" x2="370" y2="50"/>', '<line class="seam" x1="290" y1="50" x2="290" y2="128"/>',
         rrect(270, 56, 40, 50, 4, "pc"), rrect(276, 54, 28, 40, 2, "leathf"), '<path class="stitchline" d="M279,60 H301 V90 H279 Z M279,60 L301,90 M301,60 L279,90"/>',
         '<path class="strapd" d="M290,54 V14"/>']
    for k in range(3): g.append(f'<line class="wrapl" x1="282" y1="{44 - k * 7}" x2="298" y2="{42 - k * 7}"/>')
    g += [txt(318, 34, "ปลอกพัน 3 รอบ", fs * .8, anchor="start"), txt(318, 78, "ปลายแบน เย็บกรอบ+กากบาท", fs * .8, anchor="start"), txt(318, 100, "แผ่นเสริม F", fs * .8, anchor="start"),
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
    g = [f'<g transform="translate({M + 2},{M + 4})">', f'<g>{insert(fs)}</g>', f'<g transform="translate({INS + 6},0)">{patch(fs)}</g>',
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
    "เย็บแผ่นหุ้มแม่เหล็ก D ติดด้านในของ A ทั้งสองชิ้น ตามเส้นประ ใส่แม่เหล็กไว้ข้างใน ลองให้ดูดกันก่อนเย็บ",
    f"ประกบหน้าหนังเข้าหากัน เย็บตะเข็บข้างสองด้าน แล้วเย็บตะเข็บก้น ห่างขอบ {SA} มม.",
    "แบะตะเข็บออก ทากาวยาง ตอกให้เรียบ",
    f"ทำมุมก้น: จับขอบ ① ชนขอบ ② ให้ตะเข็บข้างทับตะเข็บก้น เย็บขวาง {cm(BASE)} ซม. เย็บซ้ำ 2 รอบ ทำทั้งสองมุม",
    "กลับด้านให้หน้าหนังออก",
    f"ทำสาย: พับ B หุ้มเชือกแกน เย็บชิดเชือก ตัดครีบเหลือ 2 มม. เว้นปลายข้างละ {cm(STRAP_END)} ซม. ไว้แบน",
    "ลองความยาวสายกับตัวกระเป๋าก่อน แล้วติดแผ่นเสริม F ด้านใน ทับตะเข็บข้าง เย็บปลายสายเป็นกรอบสี่เหลี่ยมมีกากบาท ให้ฝีเข็มแรกเย็บทับปลายเชือกแกน",
    "พันปลอก C รอบโคนสาย 3 รอบ ทากาวปลายซ่อนไว้ด้านใน",
    "ทำแผ่นรองก้น: ประกบ E สองชิ้น มีไส้แข็ง E2 ตรงกลาง ทากาว เย็บรอบ แล้ววางลงก้น",
]
steps_html = "".join(f"<li>{E(s)}</li>" for s in STEPS)
SHOP = [
    ("หนังวัวนิ่มลายลิ้นจี่", f"หนา 1.6–1.8 มม. ชิ้นเดียวอย่างน้อย {cm(LAYOUT[0])} × {cm(LAYOUT[1])} ซม. หรือซื้อ 5–6 ตร.ฟุต"),
    ("เชือกแกนสาย", f"ไนลอนหรือฝ้ายถัก {CORD} มม. ยาว {cm(CORD_L)} ซม."),
    ("แม่เหล็กกลม", "18 × 2 มม. 2 เม็ด"),
    ("ไส้แข็งแผ่นรองก้น", f"กระดาษอัดหรือแผ่น PE 1.5–2 มม. ขนาด {cm(BOARD)} × {cm(BOARD)} ซม."),
    ("ด้ายและเข็ม", "ด้ายไนลอนหรือโพลีเอสเตอร์เบอร์ 20 · เข็มจักรปลายมีด เบอร์ 18–19"),
    ("กาว", "กาวยาง สำหรับแบะตะเข็บและประกบแผ่นรองก้น"),
]
shop_rows = "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in SHOP)

SUB = {
    "__FIG_BAG__": fig_bag(), "__FIG_BODY__": fig_body(), "__FIG_PARTS__": fig_parts(), "__FIG_LAYOUT__": fig_layout(),
    "__FIG_CORNER__": fig_corner(12, 1) + fig_corner(12, 2), "__FIG_STRAP__": fig_strap(12, 1) + fig_strap(12, 2), "__CUTROWS__": cut_rows, "__STEPS__": steps_html, "__SHOPROWS__": shop_rows,
    "__NPAGES__": str(NPAGES), "__T1__": str(FIRST), "__T2__": str(FIRST - 1 + COLS * ROWS), "__NTILES__": str(COLS * ROWS), "__BODY__": f"{cm(W)} × {cm(H)}", "__NOTCH__": cm(N), "__SA__": str(SA),
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
.p1 .fig .mark{{stroke-width:.9;stroke-dasharray:3 2.5}} .p1 .fig .centre{{stroke-width:.7}} .p1 .fig .hide{{stroke-width:1}}
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
<div><h2>มุมก้น</h2>{fig_corner(12)}</div>
<div><h2>สายและโคนสาย</h2>{fig_strap(12)}</div>
<p class="note">มุมก้นหนาที่สุด หนังซ้อน 4 ชั้น ใช้จักรตีนตะขาบหรือเย็บมือ · ลองความยาวสายกับเชือกจริงก่อนเย็บติด · วิธีติดโคนสายเป็นวิธีที่แนะนำ รูปอ้างอิงมองไม่เห็นด้านใน<br>
ใบจริงเสร็จแล้ว ใส่ของ 3 กก. แขวนค้างคืน ดูโคนสายและมุมก้นก่อนใช้งานหรือขาย</p>
</section>"""
tiles = "".join(tile(c, r, FIRST + r * COLS + c) for r in range(ROWS) for c in range(COLS))
doc = f'<!doctype html><html lang="th"><head><meta charset="utf-8"><title>OCT. 26 แพตเทิร์นกระเป๋าทรงถัง</title><style>{PRINT_CSS}</style></head><body>{p1}{p2}{tiles}{parts_page(NPAGES)}</body></html>'
open(os.path.join(HERE, "print.html"), "w").write(doc)
print(f"bucketbag: body {W} x {H} notch {N} · strap {STRAP_W} x {STRAP_L} · tiles {COLS}x{ROWS} · pages {NPAGES} · leather {AREA:.3f} m2 = {sqft(AREA):.1f} sqft")
