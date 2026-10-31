"""Build wallart/index.html: framed 3D wall pieces (owner, 31 Oct), priced by frame size, pieces counted to fit.

The pieces join wing-in-slit into a flat woven panel (07: neighbours turned 90 deg, 56.86 mm apart, the way the bag charm
was made; 01: every bear the same way, 71.3 mm apart). Each panel is an n x n grid set in an IKEA SANNAHED deep frame,
which is sold for 3D motifs. Drawings are to scale from the die files (cross3d/geom.py).
python3 wallart/build.py -> wallart/index.html
"""
import html, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import geom
E = html.escape

COST = {"01": 3.89, "07": 3.45}                                   # sheet, 22 Oct
PITCH = {"01": 30.5 + 40.8, "07": 2 * 28.43}                      # slit + wing distance from the piece centre (lamps/build.py)
ALT = {"01": False, "07": True}
# IKEA Thailand SANNAHED deep frame, prices found 31 Oct (search results; check in store)
FRAMES = [("S", 250, 279, 2), ("M", 350, 349, 3), ("L", 500, 590, 5)]   # size, frame mm, price THB, grid n x n
PRICE = {"S": (690, 890), "M": (1290, 1590), "L": (2690, 3290)}         # proposed shelf price, THB

def outline(code):
    g = geom.load(code); pts = [g["poly"][0]]
    for p in g["poly"][1:]:
        if math.dist(p, pts[-1]) > 0.7: pts.append(p)
    return "M" + " L".join(f"{x:.1f},{-y:.1f}" for x, y in pts) + "Z", g["cuts"], pts

SHAPE = {c: outline(c) for c in COST}

def panel(code, n):
    p = PITCH[code]; path, cuts, pts = SHAPE[code]
    xs = [x for x, _ in pts]; ys = [-y for _, y in pts]
    cells = [((i - (n - 1) / 2) * p, (j - (n - 1) / 2) * p, i, j) for j in range(n) for i in range(n)]
    span_x = (n - 1) * p + max(xs) - min(xs); span_y = (n - 1) * p + max(ys) - min(ys)
    cx = (max(xs) + min(xs)) / 2; cy = (max(ys) + min(ys)) / 2           # 01's box is off its centre: centre the drawing
    g = ""
    for x, y, i, j in cells:
        odd = (i + j) % 2
        rot = 90 if (ALT[code] and odd) else 0
        fill = "var(--b)" if odd else "var(--a)"
        g += (f'<g transform="translate({x - cx:.1f} {y - cy:.1f}) rotate({rot})"><path d="{path}" style="fill:{fill}" class="pc"/>'
              + "".join(f'<line x1="{a[0]}" y1="{-a[1]}" x2="{b[0]}" y2="{-b[1]}" class="cut"/>' for a, b in cuts) + "</g>")
    return g, span_x, span_y

def framed(code, size, frame_mm, n):
    g, sx, sy = panel(code, n)
    rail = frame_mm * 0.07; half = frame_mm / 2
    return (f'<svg class="art" viewBox="{-half:.0f} {-half:.0f} {frame_mm} {frame_mm}" role="img" '
            f'aria-label="กรอบ {frame_mm // 10} ซม. ลาย {code} {n * n} ชิ้น">'
            f'<rect x="{-half}" y="{-half}" width="{frame_mm}" height="{frame_mm}" class="frame"/>'
            f'<rect x="{-half + rail:.1f}" y="{-half + rail:.1f}" width="{frame_mm - 2 * rail:.1f}" height="{frame_mm - 2 * rail:.1f}" class="back"/>'
            f'<g filter="url(#lift)">{g}</g></svg>'), sx, sy

cards, rows = "", ""
for code, label in (("07", "07 กากบาทข้อต่อวงกลม · สองสีสลับ"), ("01", "01 หัวหมี · หันทางเดียวกัน")):
    figs = ""
    for size, mm, fprice, n in FRAMES:
        svg, sx, sy = framed(code, size, mm, n)
        pcs = n * n; leather = pcs * COST[code]; lo, hi = PRICE[size]
        margin = (mm - max(sx, sy)) / 2 / 10
        figs += (f'<figure class="card">{svg}<figcaption><b>{size} · กรอบ {mm // 10}×{mm // 10} ซม.</b>'
                 f'<span class="num">{pcs} ชิ้น ({n}×{n}) · งานกว้าง {max(sx, sy) / 10:.0f} ซม. · ขอบเหลือ ~{margin:.0f} ซม.</span>'
                 f'<span class="num price">{lo:,}–{hi:,} ฿</span></figcaption></figure>')
        rows += (f'<tr><th>{size} {code}</th><td class="num">{mm // 10}×{mm // 10}</td><td class="num">{pcs}</td>'
                 f'<td class="num">{leather:.0f}</td><td class="num">{fprice}</td><td class="num"><b>{leather + fprice:.0f}</b></td>'
                 f'<td class="num">{lo:,}–{hi:,}</td><td class="num">{round((1 - (leather + fprice) / lo) * 100)}–{round((1 - (leather + fprice) / hi) * 100)}%</td></tr>')
    cards += f'<section class="set"><h3>{E(label)}</h3><div class="grid">{figs}</div></section>'

PAGE = open(os.path.join(HERE, "template.html")).read().replace("__CARDS__", cards).replace("__ROWS__", rows)
open(os.path.join(HERE, "index.html"), "w").write(PAGE)
print("wallart/index.html", len(PAGE), "bytes")
