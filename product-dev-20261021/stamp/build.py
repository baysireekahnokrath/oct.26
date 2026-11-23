"""Artwork for a leather stamp of the OCT. 26 logo (owner, 23 Nov 2026: "make a file for a leather stamp, about 2 cm, too big?").

The brand logo (brand-20261014/brandbook-v2/logo, on branch claude/brand-guidelines-doc; copies in ref/) is drawn with
strokes and clip paths. A stamp maker needs plain filled outlines, so this script rebuilds the same letters as solid
shapes (shapely), checks them against the reference SVGs in check.cjs, and writes them at real size in millimetres.

Three layouts, black = the metal that stands proud and presses into the leather:
  line    OCT. 26 on one line
  stack   OCT. over 26, the square logo without its frame
  frame   the square logo with its frame (square-mono)
Outputs: svg/ and dxf/ (reading the right way round, plus mirror/ copies), print.html -> stamp-order.pdf, index.html.
python3 stamp/build.py && node stamp/render.cjs
"""
import math, os, sys
from shapely.geometry import Point, LineString, box, MultiPolygon, Polygon
from shapely.ops import unary_union
from shapely import affinity
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import geom

# ---------------------------------------------------------------- the letters, in logo units (cap height 100, y down)
PHI = (1 + 5 ** .5) / 2
H = 100.0; W = H / PHI ** 4; DOT = W * PHI; D = H / PHI; TW = H * PHI / 2
C_OPEN = 360 / PHI ** 3; OV = H / PHI ** 8
SEG = 48                                               # segments per quarter circle
pt = lambda cx, cy, r, deg: (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))
arc = lambda cx, cy, r, a0, a1, n=160: [pt(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
ring = lambda cx, cy, r: Point(cx, cy).buffer(r + W / 2, SEG).difference(Point(cx, cy).buffer(r - W / 2, SEG))
stroke = lambda pts: LineString(pts).buffer(W / 2, SEG, cap_style="flat", join_style="mitre", mitre_limit=4)

def g_O(x): R = H / 2 + OV; return ring(x + R, -H / 2, R - W / 2)
def g_C(x):
    R = H / 2 + OV; half = C_OPEN / 2
    return stroke(arc(x + R, -H / 2, R - W / 2, half, 360 - half))
def g_T(x): return box(x, -H, x + TW, -H + W).union(box(x + TW / 2 - W / 2, -H, x + TW / 2 + W / 2, 0))
def g_dot(x): return Point(x + DOT / 2, -DOT / 2).buffer(DOT / 2, SEG)
def g_2(x):
    rr = D / 2 - W / 2; cx, cy = x + D / 2, -H + D / 2 - OV
    s = stroke(arc(cx, cy, rr, 155, 38 + 360) + [(x + W * .3, -W * .7)])
    return s.union(box(x, -W, x + D, 0)).intersection(box(x, -H - OV, x + D, 0))
def g_6(x):
    rr = D / 2 - W / 2; cx, cy = x + D / 2, -D / 2 + OV
    ex, ey = x + D * .64, -H - W
    dist = math.hypot(ex - cx, ey - cy); base = math.degrees(math.atan2(ey - cy, ex - cx)); off = math.degrees(math.acos(rr / dist))
    tx, ty = pt(cx, cy, rr, base - off)
    if tx > cx: tx, ty = pt(cx, cy, rr, base + off)
    return ring(cx, cy, rr).union(stroke([(ex, ey), (tx, ty)])).intersection(box(x - W, -H, x + D + W, W))

# positions as in the brand book files (ref/line-light.svg, ref/square-mono.svg)
X_C, X_T, X_DOT = 170.97 - (H / 2 + OV), 224.00, 313.93
OCT = unary_union([g_O(0), g_C(X_C), g_T(X_T), g_dot(X_DOT)])
N26 = lambda x: unary_union([g_2(x), g_6(x + D + W)])
LINE = unary_union([OCT, N26(361.80)])
LEAD = H / PHI; M = H / PHI
STACK = unary_union([OCT, affinity.translate(N26(0), 0, H + LEAD)])
S = (X_DOT + DOT) + 2 * M                              # square side 461.14
FRAME_W = W / PHI
_inner = affinity.translate(STACK, M, (S - (2 * H + LEAD)) / 2 + H)
FRAME = unary_union([box(0, 0, S, S).difference(box(FRAME_W, FRAME_W, S - FRAME_W, S - FRAME_W)), _inner])
SHAPES = {"line": LINE, "stack": STACK, "frame": FRAME}
NAME = {"line": "แถวเดียว OCT. 26", "stack": "สองแถว ไม่มีกรอบ", "frame": "โลโก้สี่เหลี่ยม มีกรอบ"}

def fit(shape, width_mm):
    """scale to a given overall width, origin at the top-left of its bounding box; returns shape in mm and its size"""
    x0, y0, x1, y1 = shape.bounds; k = width_mm / (x1 - x0)
    g = affinity.scale(affinity.translate(shape, -x0, -y0), k, k, origin=(0, 0))
    return g, (width_mm, (y1 - y0) * k), k

def polys(g): return list(g.geoms) if isinstance(g, MultiPolygon) else [g]
def path_d(g, nd=3):
    d = []
    for p in polys(g):
        for r in [p.exterior] + list(p.interiors):
            c = list(r.coords)[:-1]
            d.append("M" + "L".join(f"{x:.{nd}f},{y:.{nd}f}" for x, y in c) + "Z")
    return "".join(d)
def min_gap(g):
    ps = polys(g); best = 1e9
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)): best = min(best, ps[i].distance(ps[j]))
    for p in ps:                                       # also the narrowest opening inside a letter (counter of O, 6)
        for r in p.interiors: best = min(best, 2 * math.sqrt(Polygon(r).area / math.pi) if Polygon(r).area > 0 else best)
    return best

def write_svg(path, g, size, mirror=False):
    w, h = size
    tr = f' transform="translate({w:.3f},0) scale(-1,1)"' if mirror else ""
    open(path, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}mm" height="{h:.3f}mm" viewBox="0 0 {w:.3f} {h:.3f}">'
                          f'<title>OCT. 26 leather stamp {w:g} mm{" MIRRORED" if mirror else ""}</title>'
                          f'<path{tr} d="{path_d(g)}" fill="#000" fill-rule="evenodd"/></svg>\n')
def write_dxf(path, g, size, mirror=False):
    """plain R12 DXF, closed polylines, millimetres, y up"""
    w, h = size; out = ["0", "SECTION", "2", "ENTITIES"]
    for p in polys(g):
        for r in [p.exterior] + list(p.interiors):
            out += ["0", "POLYLINE", "8", "STAMP", "66", "1", "70", "1"]
            for x, y in list(r.coords)[:-1]:
                out += ["0", "VERTEX", "8", "STAMP", "10", f"{(w - x) if mirror else x:.4f}", "20", f"{h - y:.4f}"]
            out += ["0", "SEQEND"]
    out += ["0", "ENDSEC", "0", "EOF"]
    open(path, "w").write("\n".join(out) + "\n")

# ---------------------------------------------------------------- the sizes offered
OPTIONS = [  # key, layout, width mm, where it suits, PD's view
    ("line-20", "line", 20, "ชิ้น 9 ซม. สายคล้อง ของเล็ก", "ขนาดที่พ่อเบถาม · ใช้ได้ ไม่ใหญ่ ตัวอักษรสูงแค่ 4 มม."),
    ("line-25", "line", 25, "ชิ้น 9 ซม. กระเป๋า กล่อง", "PD แนะนำถ้าทำอันเดียว · เส้นหนาขึ้น อ่านชัดบนหนังลายลิ้นจี่"),
    ("stack-15", "stack", 15, "ชิ้น 9 ซม. ของเล็ก ป้าย", "โลโก้สองแถวแบบย่อ · เส้นหนาที่สุดในขนาดเล็ก"),
    ("stack-20", "stack", 20, "กระเป๋า กล่อง ของชิ้นใหญ่", "เด่นกว่า · บนชิ้น 9 ซม. จะค่อนข้างใหญ่"),
    ("frame-20", "frame", 20, "กระเป๋า กล่อง การ์ด", "ตรงกับโลโก้สี่เหลี่ยมในเล่มแบรนด์ · เส้นกรอบบาง ต้องกดให้เรียบทั้งหน้า"),
]
os.makedirs(os.path.join(HERE, "svg", "mirror"), exist_ok=True); os.makedirs(os.path.join(HERE, "dxf", "mirror"), exist_ok=True)
OPT = {}
for key, lay, wmm, use, view in OPTIONS:
    g, size, k = fit(SHAPES[lay], wmm)
    base = f"oct26-stamp-{key}mm"
    write_svg(os.path.join(HERE, "svg", base + ".svg"), g, size); write_svg(os.path.join(HERE, "svg", "mirror", base + "-mirror.svg"), g, size, True)
    write_dxf(os.path.join(HERE, "dxf", base + ".dxf"), g, size); write_dxf(os.path.join(HERE, "dxf", "mirror", base + "-mirror.dxf"), g, size, True)
    OPT[key] = dict(key=key, lay=lay, g=g, w=size[0], h=size[1], k=k, stroke=W * k, cap=H * k, dot=DOT * k, gap=min_gap(SHAPES[lay]) * k,
                    frame=FRAME_W * k if lay == "frame" else None, use=use, view=view, file=base, area=g.area)

# reference-check artwork: the same shapes in logo units, for check.cjs to lay over the brand book SVGs
os.makedirs(os.path.join(HERE, "ref"), exist_ok=True)
pad = (M / PHI)
open(os.path.join(HERE, "ref", "rebuilt-line.svg"), "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576.39 190.98" width="576" height="191"><path transform="translate({pad:.2f},{pad + H:.2f})" d="{path_d(LINE, 2)}" fill="#2A2725" fill-rule="evenodd"/></svg>')
open(os.path.join(HERE, "ref", "rebuilt-square.svg"), "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S:.2f} {S:.2f}" width="461" height="461"><path d="{path_d(FRAME, 2)}" fill="#2A2725" fill-rule="evenodd"/></svg>')

# ---------------------------------------------------------------- html pieces
mm = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")
def art(o, cls="art", mirror=False):
    tr = f' transform="translate({o["w"]:.3f},0) scale(-1,1)"' if mirror else ""
    return f'<svg class="{cls}" viewBox="0 0 {o["w"]:.3f} {o["h"]:.3f}" style="width:{o["w"]:.3f}mm;height:{o["h"]:.3f}mm"><path{tr} d="{path_d(o["g"], 3)}" fill-rule="evenodd"/></svg>'
def art_big(o, px=None):
    return f'<svg class="art big" viewBox="{-o["w"] * .06:.3f} {-o["h"] * .12:.3f} {o["w"] * 1.12:.3f} {o["h"] * 1.24:.3f}" role="img" aria-label="{NAME[o["lay"]]} {o["w"]:g} มม."><path d="{path_d(o["g"], 3)}" fill-rule="evenodd"/></svg>'
def piece_path(code):
    g = geom.load(code); return "M" + "L".join(f"{x:.2f},{-y:.2f}" for x, y in g["poly"]) + "Z"
def on_piece(code, o, label, dy=22):
    """a real die piece at 1:1 with the stamp near its lower edge"""
    return (f'<svg class="onpiece" viewBox="-47 -46 94 96" style="width:94mm;height:96mm"><path class="pc" d="{piece_path(code)}"/>'
            f'<g transform="translate({-o["w"] / 2:.3f},{dy - o["h"] / 2:.3f})"><path class="ink" d="{path_d(o["g"], 3)}" fill-rule="evenodd"/></g>'
            f'<text x="0" y="49" text-anchor="middle" font-size="3.2">{label}</text></svg>')
def on_bag(o, label):
    """the top of one bag face, 15 cm wide, 1:1"""
    return (f'<svg class="onpiece" viewBox="-80 -6 160 42" style="width:160mm;height:42mm"><path class="pc" d="M-75,34 V0 H75 V34"/>'
            f'<line class="dash" x1="-75" y1="34" x2="75" y2="34"/><g transform="translate({-o["w"] / 2:.3f},{18 - o["h"] / 2:.3f})"><path class="ink" d="{path_d(o["g"], 3)}" fill-rule="evenodd"/></g>'
            f'<text x="0" y="-1.5" text-anchor="middle" font-size="3.2">ปากกระเป๋า หน้ากว้าง 15 ซม.</text><text x="60" y="31" text-anchor="end" font-size="3.2">{label}</text></svg>')

spec_rows = "".join(
    f'<tr><th>{o["key"]}</th><td>{NAME[o["lay"]]}</td><td class="num">{mm(o["w"])} × {mm(o["h"])}</td><td class="num">{mm(o["cap"])}</td>'
    f'<td class="num">{mm(o["stroke"])}</td><td class="num">{mm(o["gap"])}</td><td class="num">{mm(o["frame"]) if o["frame"] else "–"}</td></tr>' for o in OPT.values())
pick_rows = "".join(f'<tr><th>{o["key"]}</th><td class="num">{mm(o["w"])} × {mm(o["h"])} มม.</td><td>{o["use"]}</td><td>{o["view"]}</td></tr>' for o in OPT.values())

FONTS = "../../brand-20261014/fonts"
CSS = f"""
@font-face{{font-family:"Plex Thai";src:url("{FONTS}/IBMPlexSansThai-Regular.ttf");font-weight:400}}
@font-face{{font-family:"Plex Thai";src:url("{FONTS}/IBMPlexSansThai-SemiBold.ttf");font-weight:600}}
@font-face{{font-family:"Anuphan";src:url("{FONTS}/alt/Anuphan-Medium.ttf")}}
@page{{size:A4;margin:0}} *{{box-sizing:border-box}}
html,body{{margin:0;background:#fff;color:#2A2725;font-family:"Plex Thai",sans-serif;font-size:9.5pt;line-height:1.45}}
.page{{width:210mm;height:297mm;padding:12mm;display:grid;gap:3.5mm;align-content:start;page-break-after:always;overflow:hidden}}
.page:last-child{{page-break-after:auto}}
h1{{font-family:"Anuphan","Plex Thai",sans-serif;font-weight:500;font-size:19pt;margin:0}} h2{{font-family:"Anuphan","Plex Thai",sans-serif;font-weight:500;font-size:12pt;margin:0}}
p{{margin:0}} .eyebrow{{font-size:8pt;letter-spacing:.08em;color:#5E5953}} .note{{font-size:8pt;color:#5E5953}}
.art path{{fill:#000}} svg text{{font-family:"Plex Thai",sans-serif;fill:#5E5953}}
.opts{{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}}
.opt{{border:.3mm solid #2A2725;border-radius:2mm;padding:3mm;display:grid;gap:2mm;align-content:start}}
.opt .show{{display:flex;gap:5mm;align-items:center;min-height:24mm}}
.opt .tick{{display:flex;gap:2mm;align-items:center;font-weight:600}} .box{{width:4.5mm;height:4.5mm;border:.35mm solid #2A2725;display:inline-block}}
.cap{{font-size:7.5pt;color:#5E5953}}
table{{border-collapse:collapse;width:100%;font-size:8.6pt}} th,td{{border-bottom:.2mm solid #D9D2C4;padding:1mm 1.6mm;text-align:left;vertical-align:top}} td.num{{white-space:nowrap}}
.spec{{border:.3mm solid #2A2725;border-radius:2mm;padding:3.5mm 4.5mm}} .spec ol{{margin:1mm 0 0;padding-left:5mm}}
.check{{display:flex;gap:4mm;align-items:center}} .check svg{{width:50mm;height:10mm;flex:none}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:2mm;justify-items:center}}
.onpiece .pc{{fill:#EFE6D8;stroke:#8C8A85;stroke-width:.3}} .onpiece .ink{{fill:#5A3B27}} .onpiece .dash{{stroke:#8C8A85;stroke-width:.3;stroke-dasharray:2 1.5}}
"""
def opt_card(o):
    return (f'<div class="opt"><div class="tick"><span class="box"></span>{o["key"]} · {NAME[o["lay"]]}</div>'
            f'<div class="show"><div>{art(o)}<div class="cap">ภาพบนหนัง</div></div><div>{art(o, mirror=True)}<div class="cap">หน้าตัวตอก (กลับด้าน)</div></div></div>'
            f'<div class="cap">กว้าง {mm(o["w"])} × สูง {mm(o["h"])} มม. · เส้นหนา {mm(o["stroke"])} มม. · ช่องแคบสุด {mm(o["gap"])} มม.<br>ไฟล์ {o["file"]}.svg / .dxf</div></div>')
p1 = f"""<section class="page"><p class="eyebrow">OCT. 26 · ใบสั่งทำตัวตอกหนัง · 23 พ.ย. 2569 · หน้า 1/2</p>
<h1>ตัวตอกหนัง OCT. 26</h1>
<div class="check"><svg viewBox="0 0 50 10"><path d="M0,2V8M50,2V8M0,5H50" stroke="#2A2725" stroke-width=".3" fill="none"/><text x="25" y="3.6" font-size="3" text-anchor="middle">5 ซม.</text></svg>
<p>ภาพในหน้านี้เป็นขนาดจริง พิมพ์ที่ 100% แล้ววัดเส้นนี้ต้องได้ 5 ซม. · สีดำ = ส่วนที่นูนบนตัวตอก และกดลงเป็นร่องบนหนัง<br>ติ๊กแบบที่เลือก 1 ช่อง แล้วส่งหน้านี้ให้ร้านพร้อมไฟล์ .svg หรือ .dxf ของแบบนั้น</p></div>
<div class="opts">{"".join(opt_card(o) for o in OPT.values())}</div>
<div class="spec"><h2>สเปกที่บอกร้าน</h2><ol>
<li>วัสดุทองเหลือง ใช้กับความร้อนได้ · ตัวอักษรนูน (ส่วนสีดำในไฟล์นูนขึ้น) · แกะลึกอย่างน้อย 1.5 มม.</li>
<li>ไฟล์ที่ส่งเป็นภาพอ่านปกติ = ภาพที่ต้องการเห็นบนหนัง ให้ร้านกลับด้านเอง (ถ้าร้านขอไฟล์กลับด้านแล้ว ใช้ไฟล์ในโฟลเดอร์ mirror)</li>
<li>ขนาดตามที่ติ๊ก วัดที่ความกว้างรวมของลาย ห้ามยืดหรือเปลี่ยนสัดส่วน · ไฟล์เป็นเส้นโครงทึบทั้งหมด ไม่มีฟอนต์ ไม่มีเส้นขอบ</li>
<li>ขอบฐานตัวตอกห่างจากลายอย่างน้อย 1.5 มม. รอบด้าน และลบคมขอบฐาน กันขอบกดเป็นรอยบนหนัง</li>
<li>มีรูเกลียว M6 หรือ M8 ด้านหลัง สำหรับต่อด้ามตอกหรือหัวเครื่องปั๊มร้อน (ถามร้านว่าเครื่องที่เราจะใช้เป็นเกลียวอะไร)</li>
<li>ขอให้ร้านยืนยันว่าเส้นบางสุดและช่องแคบสุดตามตารางแกะได้คมก่อนเริ่มงาน</li></ol></div>
<table><thead><tr><th>แบบ</th><th>ลาย</th><th>กว้าง × สูง (มม.)</th><th>ตัวอักษรสูง</th><th>เส้นหนา</th><th>ช่องแคบสุด</th><th>เส้นกรอบ</th></tr></thead><tbody>{spec_rows}</tbody></table>
<p class="note">ลายมาจากโลโก้ใน Brand Book v2 (เส้นวาดเดิม แปลงเป็นรูปทึบ) · ยังไม่ได้ลองตอกบนหนังของเรา ให้ลองกับเศษหนังก่อนใช้กับของขาย</p></section>"""
p2 = f"""<section class="page"><p class="eyebrow">OCT. 26 · ตัวตอกหนัง · เทียบขนาดจริงบนชิ้นงาน · หน้า 2/2</p>
<h1>วางบนชิ้นจริงแล้วเป็นแบบไหน</h1>
<p>พิมพ์ที่ 100% ตัดออกมาทาบกับชิ้นหนังจริงได้ ชิ้นที่วาดคือ 05 วงกลม และ 04 สี่เหลี่ยมมน ขนาด 9 ซม. และปากกระเป๋าทรงถังหน้ากว้าง 15 ซม.</p>
<div class="grid2">{on_piece("05", OPT["line-20"], "05 + line-20 (กว้าง 2 ซม.)")}{on_piece("05", OPT["line-25"], "05 + line-25 (กว้าง 2.5 ซม.)")}
{on_piece("04", OPT["stack-15"], "04 + stack-15 (กว้าง 1.5 ซม.)", 24)}{on_piece("04", OPT["frame-20"], "04 + frame-20 (กว้าง 2 ซม.)", 24)}</div>
<div style="justify-self:center">{on_bag(OPT["line-25"], "กระเป๋า + line-25")}</div></section>"""
open(os.path.join(HERE, "print.html"), "w").write(f'<!doctype html><html lang="th"><head><meta charset="utf-8"><title>OCT. 26 ใบสั่งทำตัวตอกหนัง</title><style>{CSS}</style></head><body>{p1}{p2}</body></html>')

# summary page
def web_piece(code, o, label, dy=22):
    return (f'<figure><svg class="onp" viewBox="-47 -47 94 94" role="img" aria-label="{label}"><path class="pc" d="{piece_path(code)}"/>'
            f'<g transform="translate({-o["w"] / 2:.3f},{dy - o["h"] / 2:.3f})"><path class="ink" d="{path_d(o["g"], 3)}" fill-rule="evenodd"/></g></svg><figcaption>{label}</figcaption></figure>')
SUB = {"__ART_LINE__": art_big(OPT["line-25"]), "__ART_STACK__": art_big(OPT["stack-15"]), "__ART_FRAME__": art_big(OPT["frame-20"]),
       "__PIECES__": web_piece("05", OPT["line-20"], "line-20 บนชิ้น 05") + web_piece("05", OPT["line-25"], "line-25 บนชิ้น 05") +
                     web_piece("04", OPT["stack-15"], "stack-15 บนชิ้น 04", 24) + web_piece("04", OPT["stack-20"], "stack-20 บนชิ้น 04", 22) + web_piece("04", OPT["frame-20"], "frame-20 บนชิ้น 04", 24),
       "__PICK__": pick_rows, "__SPEC__": spec_rows,
       "__L20_CAP__": mm(OPT["line-20"]["cap"]), "__L20_STROKE__": mm(OPT["line-20"]["stroke"]), "__L20_H__": mm(OPT["line-20"]["h"]),
       "__L25_STROKE__": mm(OPT["line-25"]["stroke"]), "__F20_FRAME__": mm(OPT["frame-20"]["frame"]), "__S15_STROKE__": mm(OPT["stack-15"]["stroke"])}
page = open(os.path.join(HERE, "template.html")).read()
for k, v in SUB.items(): page = page.replace(k, v)
open(os.path.join(HERE, "index.html"), "w").write(page)
for o in OPT.values():
    print(f'{o["key"]:9s} {o["w"]:5.1f} x {o["h"]:5.2f} mm · cap {o["cap"]:.2f} · stroke {o["stroke"]:.2f} · min gap {o["gap"]:.2f}' + (f' · frame {o["frame"]:.2f}' if o["frame"] else "") + f' · {len(polys(o["g"]))} parts')
