"""Step-by-step how-to sheets, A5 each, two to an A4 landscape page (print A4, cut on the dashed line).

Five products from the dies already ordered (01 bear head, 06 soft cross) that need no heart strap:
LV-21 bear garland, LV-01 cable keeper, S2-30 DIY cube kit, S2-19 brush holder, S2-20 tree ornament,
plus a sixth card that explains tabs and slits and leather care.
Every drawing uses the real die outlines from ../../diecut-leather-20261014/svg.

python3 howto/build.py && node tools/pdf.mjs howto/howto.html howto/oct26-howto-a5.pdf
"""
import html, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from brand import C, BRAND, PRODUCTS
E = html.escape
DIE = os.path.join(ROOT, "..", "diecut-leather-20261014", "svg")
BY = {p["n"]: p for p in PRODUCTS}

def die(code):
    s = open(os.path.join(DIE, code)).read()
    d = re.search(r'<g id="CUT".*?<path d="([^"]+)"', s, re.S).group(1)
    lines = [tuple(map(float, m)) for m in re.findall(r'x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"', s)]
    return d, lines

BEAR_D, BEAR_SL = die("01-bear-head.svg")
CROSS_D, CROSS_SL = die("06-soft-cross.svg")
BC = (41.685, 62.675)          # bear head centre in the die
NECK_X = 82.59                 # right ear neck line (ear meets face)
SLIT_X = 11.2                  # left cheek slit
PITCH = NECK_X - SLIT_X        # bear-to-bear spacing in the garland, 71.4 mm

LEA = ["#B8743A", "#9A5E2C", "#CF9157", "#A9692F", "#C07C42"]
INK, PAPER, TOM, COB, PINK, SUN, MINT = C["ink"], C["paper"], C["tomato"], C["cobalt"], C["pink"], C["sun"], C["mint"]

# ---------------------------------------------------------------- drawing helpers
def bear(x, y, fill, rot=0, slits=True, clip=None, scale=1.0, hl=None):
    sl = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" class="sl{" hl" if hl == i else ""}"/>' for i, (a, b, c, d) in enumerate(BEAR_SL)) if slits else ""
    cp = f' clip-path="url(#{clip})"' if clip else ""
    return (f'<g transform="translate({x},{y}) scale({scale}) rotate({rot},{BC[0]},{BC[1]})"{cp}>'
            f'<path d="{BEAR_D}" fill="{fill}" class="lea"/>{sl}</g>')

def cross(x, y, fill, rot=0, scale=1.0, folds=False, hl=None):
    sl = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" class="sl{" hl" if hl and i in hl else ""}"/>' for i, (a, b, c, d) in enumerate(CROSS_SL))
    fd = ('<rect x="15" y="15" width="60" height="60" class="fold"/>' if folds else "")
    return (f'<g transform="translate({x},{y}) scale({scale}) rotate({rot},45,45)">'
            f'<path d="{CROSS_D}" fill="{fill}" class="lea"/>{fd}{sl}</g>')

def arrow(x1, y1, x2, y2, curve=0, col=TOM):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    nx, ny = -(y2 - y1), (x2 - x1); L = math.hypot(nx, ny) or 1
    cx, cy = mx + nx / L * curve, my + ny / L * curve
    return (f'<path d="M{x1},{y1} Q{cx:.1f},{cy:.1f} {x2},{y2}" class="arr" style="stroke:{col}" marker-end="url(#ah)"/>')

def label(x, y, t, cls="lab", anchor="middle"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{E(t)}</text>'

def svg(vb, body, defs=""):
    return (f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg"><defs>'
            f'<marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{TOM}"/></marker>{defs}</defs>{body}</svg>')

def iso_box(cx, cy, s, open_top=False, lid_off=0, fills=None, ribbon=False):
    """Cube of side s in a simple oblique view."""
    fills = fills or LEA
    k = 0.5
    dx, dy = s * k * 0.9, -s * k * 0.55
    F = [(cx, cy), (cx + s, cy), (cx + s, cy - s), (cx, cy - s)]                     # front face
    R = [(cx + s, cy), (cx + s + dx, cy + dy), (cx + s + dx, cy - s + dy), (cx + s, cy - s)]
    T = [(cx, cy - s - lid_off), (cx + s, cy - s - lid_off), (cx + s + dx, cy - s + dy - lid_off), (cx + dx, cy - s + dy - lid_off)]
    P = lambda pts: " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    g = f'<polygon points="{P(F)}" fill="{fills[0]}" class="lea"/><polygon points="{P(R)}" fill="{fills[1]}" class="lea"/>'
    if open_top:
        inner = [(cx, cy - s), (cx + s, cy - s), (cx + s + dx, cy - s + dy), (cx + dx, cy - s + dy)]
        g += f'<polygon points="{P(inner)}" fill="#6B4120" class="lea"/>'
    if not open_top or lid_off:
        g += f'<polygon points="{P(T)}" fill="{fills[2]}" class="lea"/>'
    if ribbon:
        g += (f'<line x1="{cx + s / 2}" y1="{cy}" x2="{cx + s / 2}" y2="{cy - s}" class="rib"/>'
              f'<line x1="{cx + s + dx / 2}" y1="{cy + dy / 2}" x2="{cx + s + dx / 2}" y2="{cy - s + dy / 2}" class="rib"/>'
              f'<line x1="{cx + s / 2}" y1="{cy - s}" x2="{cx + s / 2 + dx}" y2="{cy - s + dy}" class="rib"/>'
              f'<line x1="{cx + dx / 2}" y1="{cy - s + dy / 2}" x2="{cx + s + dx / 2}" y2="{cy - s + dy / 2}" class="rib"/>'
              f'<path d="M{cx + s / 2 + dx / 2},{cy - s + dy / 2} C{cx + s / 2 + dx / 2 - 14},{cy - s + dy / 2 - 34} {cx + s / 2 + dx / 2 + 14},{cy - s + dy / 2 - 34} {cx + s / 2 + dx / 2},{cy - s + dy / 2}" class="rib" fill="none"/>')
    return g

# ---------------------------------------------------------------- the step drawings
def garland_steps():
    s1 = svg("-4 -4 340 112", "".join(f'<g transform="scale(0.6)">{bear(i * 112, 8, LEA[i])}</g>' for i in range(5)))
    # step 2: ear of A into slit of B, arrow
    s2 = svg("-4 -4 210 120", bear(0, 0, LEA[0]) + bear(96, 0, LEA[1], hl=0) +
             arrow(98, 36, 106, 56, -10))
    # step 3: locked pair: B drawn first, A clipped at its ear neck on top, ear hidden behind B
    clipA = f'<clipPath id="ca"><rect x="-10" y="-10" width="{NECK_X + 10}" height="130"/></clipPath>'
    s3 = svg("-4 -4 190 120", bear(PITCH, 0, LEA[1]) + bear(0, 0, LEA[0], clip="ca") +
             "", clipA)
    # step 5: full garland on a rope
    clips = "".join(f'<clipPath id="g{i}"><rect x="-10" y="-10" width="{NECK_X + 10}" height="130"/></clipPath>' for i in range(5))
    body = "".join(bear(i * PITCH, 20, LEA[i], clip=f"g{i}" if i < 4 else None) for i in reversed(range(5)))
    rope = (f'<path d="M{BC[0] - 3},{20 + 9} C60,-18 {4 * PITCH - 10},-18 {4 * PITCH + BC[0] + 3},{20 + 9}" class="rope"/>')
    s5 = svg(f"-4 -10 {4 * PITCH + 112} 140", rope + body)
    return [
        ("วางหมีห้าตัวหันด้านหน้าขึ้น ให้หูอยู่ด้านบนกับด้านขวาเหมือนกันทุกตัว", s1),
        ("งอหูขวาของตัวแรกเล็กน้อย แล้วสอดเข้าร่องแก้มซ้ายของตัวที่สอง จากด้านหน้าไปด้านหลัง", s2),
        ("ดันจนคอหูอยู่ในร่องพอดี กดหูให้แบนอยู่หลังตัวถัดไป หูจะกางล็อกเอง", s3),
        ("ต่อแบบเดียวกันจนครบห้าตัว ตัวที่สองต่อกับตัวที่สาม ไปจนถึงตัวที่ห้า", None),
        ("ผูกเชือกเป็นห่วงคล้องคอหูบนของตัวแรกและตัวสุดท้าย แล้วแขวน", s5),
    ]

def cable_steps():
    coil = "".join(f'<ellipse cx="{BC[0]}" cy="{BC[1]}" rx="{44 + i * 2.2}" ry="{12 + i * 1.2}" transform="rotate(-20 {BC[0]} {BC[1]})" class="cable"/>' for i in range(3))
    s1 = svg("-12 -6 130 120", bear(0, 0, LEA[0]) + coil)
    plug = (f'<rect x="2" y="54" width="10" height="16" rx="2" class="plug"/>'
            f'<path d="M7,70 C7,90 20,98 40,96" class="cablef"/>')
    s2 = svg("-12 -6 130 120", bear(0, 0, LEA[0], hl=0) + coil + plug + arrow(-8, 40, 4, 56, 8))
    s3 = svg("-12 -6 130 120", bear(0, 0, LEA[0], hl=1) + coil + plug +
             f'<rect x="34" y="94" width="14" height="9" rx="2" class="plug"/>' + arrow(70, 112, 50, 98, -8))
    return [
        ("พันสายชาร์จรอบหัวหมีให้พอดีมือ เหลือปลายสองข้างไว้ข้างละนิด", s1),
        ("เหน็บสายตรงโคนหัวปลั๊กเข้าร่องแก้มซ้าย ร่องจะหนีบสายไว้", s2),
        ("เหน็บอีกปลายเข้าร่องล่าง เสร็จ เวลาใช้ดึงปลายออกจากร่องแล้วคลายสาย", s3),
    ]

def cube_parts():
    """Shared steps for the soft-cross cube (6 pieces)."""
    leg = svg("-6 -6 200 116",
              cross(0, 0, LEA[0], folds=True, hl={2, 3, 4, 5}) + label(45, 104, "ปีก ซ้าย-ขวา") +
              cross(102, 0, LEA[1], folds=True, hl={0, 1}) + label(147, 104, "ร่อง บน-ล่าง"))
    pair = svg("-6 -6 190 104", cross(0, 0, LEA[0], folds=True) + cross(88, 0, LEA[1], rot=90, folds=True, hl={0, 1}) +
               arrow(84, 30, 99, 40, -8))
    ring = svg("-6 -6 398 116", "".join(cross(i * 76, 0, LEA[i], rot=90 * (i % 2), folds=True, scale=1.0) for i in range(4)) +
               "".join(label(45 + i * 76, 106, "ตั้ง" if i % 2 == 0 else "หมุน 90°") for i in range(4)))
    return leg, pair, ring

def cube_steps(kind):
    leg, pair, ring = cube_parts()
    if kind == "kit":
        fin = svg("0 -50 150 145", iso_box(20, 90, 80, lid_off=26))
        return [
            ("เทชิ้นหนังหกชิ้นออกจากถุง ดูให้ออกว่าด้านไหนเป็นปีก ด้านไหนเป็นร่อง", leg),
            ("พับกลีบทุกด้านไปทางด้านหลังตามรอยพับ ด้านหลังจะเป็นด้านในของกล่อง", None),
            ("ต่อชิ้นที่หนึ่งกับชิ้นที่สอง หมุนชิ้นที่สอง 90° แล้วสอดกลีบปีกเข้าร่องจากด้านนอกเข้าด้านใน", pair),
            ("ต่อให้ครบสี่ชิ้น สลับ ตั้ง กับ หมุน 90° แล้วม้วนเป็นวง ต่อชิ้นที่สี่เข้ากับชิ้นแรก", ring),
            ("ใส่ชิ้นที่ห้าเป็นก้น และชิ้นที่หกเป็นฝา หันปีกเข้าหาด้านที่เป็นร่อง เสร็จในห้านาที", fin),
        ]
    if kind == "brush":
        fin = svg("10 -60 150 155", iso_box(30, 90, 80, open_top=True) +
                  "".join(f'<line x1="{52 + i * 13}" y1="{-12 - (i % 2) * 18}" x2="{58 + i * 10}" y2="40" class="brush"/>'
                          f'<ellipse cx="{52 + i * 13}" cy="{-16 - (i % 2) * 18}" rx="5" ry="9" class="bristle"/>' for i in range(4)))
        return [
            ("ใช้ห้าชิ้น ดูให้ออกว่าด้านไหนเป็นปีก ด้านไหนเป็นร่อง", leg),
            ("พับกลีบทุกด้านไปทางด้านหลังตามรอยพับ ยกเว้นกลีบด้านบนของผนังทั้งสี่ ให้พับออกด้านนอกเป็นขอบโค้ง", None),
            ("ต่อผนังสี่ชิ้น สลับ ตั้ง กับ หมุน 90° สอดกลีบปีกเข้าร่องจากด้านนอกเข้าด้านใน แล้วม้วนเป็นวง", ring),
            ("ใส่ชิ้นที่ห้าเป็นก้น หันปีกเข้าหาด้านที่เป็นร่อง กดให้ก้นแบนเรียบ", pair),
            ("ตั้งแปรงในกล่อง แปรงยาวไว้ด้านหลัง", fin),
        ]
    fin = svg("10 -60 130 155", iso_box(30, 90, 70, ribbon=True, fills=[PINK, SUN, MINT]))
    return [
        ("เลือกหนังหลายสีให้ครบหกชิ้น ดูให้ออกว่าด้านไหนเป็นปีก ด้านไหนเป็นร่อง", leg),
        ("พับกลีบทุกด้านไปทางด้านหลัง แล้วต่อผนังสี่ชิ้นเป็นวง สลับ ตั้ง กับ หมุน 90°", ring),
        ("ปิดก้นและฝา สอดกลีบปีกเข้าร่องจากด้านนอกเข้าด้านใน", pair),
        ("ผูกริบบิ้นรอบลูกบาศก์แบบห่อของขวัญ ไขว้กันด้านบน แล้วผูกเป็นห่วงแขวน", fin),
    ]

# ---------------------------------------------------------------- sheets
def logo(sub):
    f = "fivebears" if sub else "oct-wordmark"
    return f'<img class="logo {"fb" if sub else "oc"}" src="../logo/svg/{f}.svg" alt="{"ห้าหมี FIVE BEARS" if sub else "OCT. 26"}">'

SHEETS = [
    (21, "love", "3 นาที", garland_steps, "ถอดได้ทุกเมื่อ งอหูกลับแล้วดึงออกจากร่อง ต่อเป็นสามตัวหรือเจ็ดตัวก็ได้"),
    (1, "love", "1 นาที", cable_steps, "ใช้ได้กับสายหูฟังและสายชาร์จนาฬิกาด้วย"),
    (30, "soi2", "5 นาที", lambda: cube_steps("kit"), "ถอดแล้วต่อใหม่ได้ ไม่ต้องใช้กาว ไม่ต้องใช้เข็ม"),
    (19, "soi2", "4 นาที", lambda: cube_steps("brush"), "ใส่ปากกาหรือดินสอสีบนโต๊ะเรียนก็ได้"),
    (20, "soi2", "5 นาที", lambda: cube_steps("ornament"), "ใช้ริบบิ้นสีประจำตัวของคนในบ้าน แขวนครบห้าลูก"),
]
PARTS = {21: [("หัวหมี 01", 5), ("เชือกแขวน", 1)], 1: [("หัวหมี 01", 1)], 30: [("ชิ้นกากบาทนุ่ม 06", 6)],
         19: [("ชิ้นกากบาทนุ่ม 06", 5)], 20: [("ชิ้นกากบาทนุ่ม 06", 6), ("ริบบิ้น", 1)]}

def sheet(n, coll, mins, steps_fn, tip):
    p = BY[n]
    sub = coll == "love"
    code = ("LV" if sub else "S2") + f"-{n:02d}"
    steps = steps_fn()
    parts = " · ".join(f"{E(a)} × {q}" for a, q in PARTS[n])
    li = []
    for i, (t, fig) in enumerate(steps, 1):
        li.append(f'<li><span class="no">{i}</span><div class="st"><p>{E(t)}</p>{f"<div class=fig>{fig}</div>" if fig else ""}</div></li>')
    return f"""<section class="a5 {'love' if sub else 'soi'}">
<header><div class="hl">{logo(sub)}</div><div class="hr"><span class="code">{code}</span><span class="cap">วิธีต่อ</span></div></header>
<h1>{E(p['name'])}</h1>
<p class="meta"><b>ใช้</b> {parts} · <b>เวลา</b> {mins} · <b>ขนาด</b> {E(p['size'])} · ไม่ใช้กาว ไม่ใช้เข็ม</p>
<ol>{''.join(li)}</ol>
<footer><p class="tip"><b>เคล็ดลับ</b> {E(tip)}</p><p class="foot">หนังแท้จากเศษ สีและลายแต่ละชิ้นไม่ซ้ำกัน · เช็ดด้วยผ้าแห้ง เลี่ยงน้ำ · @{BRAND['handle']}</p></footer>
</section>"""

def intro():
    leg = svg("-6 -6 200 120",
              cross(0, 0, LEA[0], folds=True, hl={2, 3, 4, 5}) + label(45, 100, "ปีก", "lab") + label(45, 112, "รอยตัดสั้นสองเส้นที่โคนกลีบ", "lab sm") +
              bear(104, 2, LEA[2], hl=None, scale=0.82) + label(147, 100, "ร่อง", "lab") + label(147, 112, "รอยตัดยาวเส้นเดียว", "lab sm"))
    lock = svg("0 0 200 70",
               '<rect x="10" y="30" width="80" height="6" rx="2" fill="#9A5E2C" class="lea"/>'
               '<rect x="110" y="30" width="80" height="6" rx="2" fill="#B8743A" class="lea"/>'
               '<path d="M86,33 C96,33 100,20 116,14" class="arr" style="stroke:#FF5A36" marker-end="url(#ah)"/>'
               + label(100, 60, "สอดคอปีกผ่านร่อง กลีบที่กว้างกว่าจะกางล็อกอยู่อีกด้าน", "lab sm"))
    return f"""<section class="a5 soi intro">
<header><div class="hl">{logo(False)}</div><div class="hr"><span class="cap">our crafted things.</span></div></header>
<h1>ต่อกันด้วยปีกและร่อง</h1>
<p class="lead">ทุกชิ้นของ OCT. 26 และห้าหมี ต่อกันโดยไม่ใช้กาว ไม่ใช้เข็ม แต่ละชิ้นมีปีกกับร่องจำนวนเท่ากัน จึงต่อได้เรื่อย ๆ ไม่มีด้านเหลือ</p>
<div class="fig big">{leg}</div>
<ul class="care">
<li><b>สอดปีก</b> งอปีกเล็กน้อย สอดทีละครึ่ง แล้วดันจนคอปีกอยู่ในร่องพอดี</li>
<li><b>ถอด</b> งอปีกกลับแล้วดึงออกช้า ๆ อย่ากระชากที่ปลายร่อง</li>
<li><b>ดูแล</b> เช็ดด้วยผ้าแห้ง เลี่ยงน้ำและแดดจัด สีหนังจะเข้มขึ้นตามเวลา เป็นเสน่ห์ของหนังแท้</li>
<li><b>เด็กเล็ก</b> ผู้ใหญ่ควรดูแลเมื่อเด็กเล่น ชิ้นเล็กไม่เหมาะกับเด็กต่ำกว่า 3 ปี</li>
</ul>
<footer><p class="foot">ดูคลิปวิธีต่อได้ที่ @{BRAND['handle']} · ทำโดยครอบครัวเดียวกันทั้งห้าคน</p></footer>
</section>"""

CSS = f"""
@font-face{{font-family:Anuphan;src:url(../fonts/alt/Anuphan-Medium.ttf);font-weight:500}}
@font-face{{font-family:Plex;src:url(../fonts/IBMPlexSansThai-Regular.ttf);font-weight:400}}
@font-face{{font-family:Plex;src:url(../fonts/IBMPlexSansThai-SemiBold.ttf);font-weight:600}}
@font-face{{font-family:Mitr;src:url(../fonts/Mitr-Medium.ttf);font-weight:500}}
@font-face{{font-family:Jost;src:url(../fonts/alt/Jost-Medium.ttf);font-weight:500}}
@page{{size:297mm 210mm;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:#fff}}
body{{font:400 9.6pt/1.45 Plex,sans-serif;color:{INK}}}
.sheet{{width:297mm;height:210mm;display:grid;grid-template-columns:148.5mm 148.5mm;position:relative;page-break-after:always;overflow:hidden}}
.sheet:last-child{{page-break-after:auto}}
.sheet::after{{content:"";position:absolute;left:148.5mm;top:0;bottom:0;border-left:0.3mm dashed #9C9590}}
.cut{{position:absolute;left:146mm;top:3mm;font:8pt Jost,sans-serif;color:#9C9590}}
.a5{{height:210mm;padding:9mm 10mm 8mm;display:flex;flex-direction:column;gap:2.6mm;background:{PAPER}}}
.a5.blank{{background:#fff}}
header{{display:flex;justify-content:space-between;align-items:center;height:12mm}}
.logo.oc{{height:7mm}} .logo.fb{{height:12mm}}
.hr{{display:flex;flex-direction:column;align-items:flex-end;gap:0}}
.code{{font:500 11pt Jost,sans-serif;letter-spacing:.06em}}
.cap{{font:500 7.5pt Jost,Plex,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#6E6862}}
h1{{font:500 19pt/1.2 Anuphan,sans-serif;margin:0}}
.love h1{{font-family:Mitr,sans-serif}}
.soi .code{{color:{COB}}} .love .code{{color:#D9488F}}
.meta{{margin:0;font-size:8.6pt;color:#4A4550;border-bottom:0.3mm solid #E3D6C4;padding-bottom:2mm}}
.meta b{{font-weight:600;color:{INK}}}
ol{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2.2mm;flex:1;min-height:0}}
li{{display:grid;grid-template-columns:7mm 1fr;gap:2.5mm;align-items:start}}
.st{{display:flex;gap:3mm;align-items:flex-start}} .st p{{flex:1;min-width:0}}
.st .fig{{flex:0 0 58%;margin:0}}
.no{{width:6.5mm;height:6.5mm;border-radius:50%;display:grid;place-items:center;font:500 10pt Jost,sans-serif;color:#fff;background:{COB}}}
.love .no{{background:#D9488F}}
.st p{{margin:0.6mm 0 0}}
.fig{{margin-top:1.2mm}}
.fig svg{{display:block;width:100%;height:auto;max-height:29mm}}
.fig.big svg{{max-height:44mm}}
footer{{border-top:0.3mm solid #E3D6C4;padding-top:2mm;display:flex;flex-direction:column;gap:1mm}}
.tip{{margin:0;font-size:8.8pt}} .tip b{{color:{TOM};font-weight:600}}
.foot{{margin:0;font-size:7.6pt;color:#6E6862}}
.lead{{margin:0;font-size:10pt}}
.care{{margin:0;padding-left:4.5mm;display:flex;flex-direction:column;gap:1.4mm;font-size:9pt}}
.care b{{font-weight:600;white-space:nowrap;margin-right:2mm}}
.intro .fig svg{{max-height:40mm}}
.lea{{stroke:{INK};stroke-width:0.45;stroke-linejoin:round}}
.sl{{stroke:{INK};stroke-width:0.7}} .sl.hl{{stroke:{TOM};stroke-width:1.4}}
.fold{{fill:none;stroke:{PAPER};stroke-width:0.5;stroke-dasharray:1.6 1.2}}
.arr{{fill:none;stroke-width:1.4;stroke-linecap:round}}
.lab{{font:600 11px Plex,sans-serif;fill:{INK}}} .lab.sm{{font-size:9px;font-weight:400;fill:#4A4550}}
.cable{{fill:none;stroke:{INK};stroke-width:1.6;opacity:.85}} .cablef{{fill:none;stroke:{INK};stroke-width:1.6}}
.plug{{fill:#D8D3CC;stroke:{INK};stroke-width:0.6}}
.rope{{fill:none;stroke:{INK};stroke-width:1.2}}
.rib{{stroke:{TOM};stroke-width:2.2}}
.brush{{stroke:#5B4636;stroke-width:3;stroke-linecap:round}} .bristle{{fill:{INK}}}
"""

def build():
    pages = [sheet(*s) for s in SHEETS] + [intro()]
    sheets = []
    for i in range(0, len(pages), 2):
        pair = pages[i:i + 2] + ['<section class="a5 blank"></section>'] * (2 - len(pages[i:i + 2]))
        sheets.append(f'<div class="sheet">{"".join(pair)}<span class="cut">ตัด</span></div>')
    out = f'<!doctype html><html lang="th"><head><meta charset="utf-8"><title>OCT. 26 How-to A5</title><style>{CSS}</style></head><body>{"".join(sheets)}</body></html>'
    open(os.path.join(HERE, "howto.html"), "w").write(out)
    print("sheets", len(sheets), "pages", len(pages))

if __name__ == "__main__":
    build()
