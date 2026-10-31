"""Build wallart/index.html: wall art v3, from the owner's 20 reference images (31 Oct).

v1 (flat) and v2 (3D model of 23-78 rigid 07 pieces, wallart/v2/) were both turned down: it looked computer-made,
the shapes were not pretty, too many pieces, wrong colours. What the references share instead:
  one shape repeated in one colour, leather that bends by itself, earthy tones (3 at most), calm space around it.
Three directions, each with real die pieces and few of them, in a ready-made IKEA SANNAHED 35 x 35 frame (6 cm deep):
  A  bloom   two 07 laid crosswise, centre pulled down from behind so the top lobes rise (refs 06, 01, 12; owner's charm)
  B  scales  05 circles overlapping like roof tiles, glued along the top only so the lower edge lifts (refs 04, 05, 10, 02)
  C  meadow  offcut strips pleated into waves and stood on edge (refs 20, 13, 14) - uses scrap, no sellable pieces
The page draws flat sketches (layout and count only, not a render) next to the reference photos;
reference thumbnails are published with the page as refs/*.jpg (from the owner's Drive folder, team use only).
python3 wallart/build.py -> wallart/index.html
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import geom

COST = {"07": 3.45, "05": 3.84, "03": 3.61}            # sheet, 22 Oct
FRAME = dict(name="IKEA SANNAHED 35×35", price=349, depth=60, open=350, window=240)   # ikea.com/th, 31 Oct; window = with its mount
BACK = 40                                               # felt or linen on the frame's own board, glue (estimate)
PIN = 2                                                 # split pin per bloom (estimate)
LEFT07 = 140                                            # status doc, 1 Nov

def outline(code):
    g = geom.load(code); pts = [g["poly"][0]]
    for p in g["poly"][1:]:
        if math.dist(p, pts[-1]) > 0.8: pts.append(p)
    return dict(poly=[[round(x, 1), round(y, 1)] for x, y in pts], cuts=[[[round(c, 1) for c in a], [round(c, 1) for c in b]] for a, b in g["cuts"]])

# layouts, mm from the centre of the frame opening
single = [[0, 0]]
grid = [[(i - 1) * 110, (j - 1) * 110] for j in range(3) for i in range(3)]          # 3 x 3 blooms, 110 apart: 310 of 350
scales = []
for r in range(6):                                                                     # rows 45 apart, 75 across, every other row offset
    n = 4 if r % 2 == 0 else 3
    for k in range(n):
        scales.append([(k - (n - 1) / 2) * 75, -112.5 + r * 45, r])
ROWS, PITCH, WAVE = 11, 28, 40                                                         # meadow: rows 28 apart, one wave per 40 mm
strip_len = round(330 * 1.3 / 10) * 10                                                 # pleated, a strip is about 1.3 x the width
meadow = dict(rows=ROWS, pitch=PITCH, wave=WAVE, width=330, strip=strip_len, h=25)

def money(pieces, code, pins=0, labour_h=0):
    leather = pieces * COST[code] if code else 0
    return dict(leather=round(leather), total=round(leather + FRAME["price"] + BACK + pins * PIN), hours=labour_h)

DIRS = [
    dict(id="A1", key="bloom1", name="ดอกเดียว", group="A", die="07", n=2, layout=single, mount=True, relief="2–3 ซม.",
         refs=["r06", "p4", "r01"], price=(690, 890), **money(2, "07", 1, 0.3)),
    dict(id="A2", key="bloom9", name="สวน 9 ดอก", group="A", die="07", n=18, layout=grid, mount=False, relief="2–3 ซม.",
         refs=["r12", "r01", "r10"], price=(1890, 2290), **money(18, "07", 9, 1.5)),
    dict(id="B", key="scales", name="เกล็ด", group="B", die="05", n=len(scales), layout=scales, mount=False, relief="0.5–1.5 ซม.",
         refs=["r04", "r05", "r02"], price=(1590, 1990), **money(len(scales), "05", 0, 1.5)),
    dict(id="C", key="meadow", name="ทุ่งหญ้าเศษหนัง", group="C", die=None, n=0, layout=meadow, mount=False, relief="2.5 ซม.",
         refs=["r20", "r13", "r14"], price=(1990, 2490), **money(0, None, 0, 3)),
]
DATA = dict(dies={c: outline(c) for c in ("07", "05", "03")}, dirs=DIRS, frame=FRAME)

E = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;")
rows = ""
for d in DIRS:
    count = f'{d["n"]} ชิ้น {d["die"]}' if d["die"] else f'เศษหนัง {ROWS} เส้น'
    rows += (f'<tr><th>{d["id"]} {E(d["name"])}</th><td>{count}</td><td>{d["relief"]}</td><td class="num">{d["leather"]}</td>'
             f'<td class="num">{d["total"]}</td><td class="num">{d["hours"]:g}</td><td class="num"><b>{d["price"][0]:,}–{d["price"][1]:,}</b></td></tr>')
SUB = {"__DATA__": json.dumps(DATA, separators=(",", ":"), ensure_ascii=False), "__ROWS__": rows,
       "__N07__": str(sum(d["n"] for d in DIRS if d["die"] == "07")), "__LEFT07__": str(LEFT07),
       "__NSCALE__": str(len(scales)), "__STRIP__": f'{strip_len / 10:.0f}', "__METRES__": f'{ROWS * strip_len / 1000:.1f}',
       "__FRAMEP__": str(FRAME["price"])}
PAGE = open(os.path.join(HERE, "template.html")).read()
for k, v in SUB.items(): PAGE = PAGE.replace(k, v)
open(os.path.join(HERE, "index.html"), "w").write(PAGE)
print("wallart/index.html", len(PAGE), "bytes ·", {d["id"]: (d["n"], d["total"]) for d in DIRS})
