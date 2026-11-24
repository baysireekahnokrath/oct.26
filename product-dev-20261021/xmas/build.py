"""Christmas 2026 products (owner, 24 Nov: "Christmas, we need products out", with a photo of a knotted-cord tree charm).

Three things from the pieces already cut, drawn as flat sketches from the die files (layout and count only, not renders):
  tree     three 07 on one cord. The taper comes from the die's own joint: button a lobe through the slit of the
           lobe next to it and the flat cross closes into a cone. Two closures = steep top tier, one = middle tier,
           none = the wide bottom tier. The cord carries the weight, the leather carries none. NOT yet tried in leather.
  hang     one piece + a red cord loop: tree ornaments from the slow stock (01-05)
  tag      03 gift tag on a red cord (already a product, OC-03-26)
python3 xmas/build.py -> xmas/index.html
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import geom

ARM = 45.0                                   # centre to the tip of a lobe on 07, mm
COST = {"01": 3.89, "02": 3.71, "03": 3.61, "04": 4.22, "05": 3.84, "07": 3.45}       # sheet, 22 Oct
STOCK = {"01": 369, "02": 150, "03": 150, "04": 150, "05": 150, "07": 140}             # 07: 140 left (status doc, 1 Nov)
NAME = {"01": "หมี", "02": "กังหัน", "03": "กากบาทแคปซูล", "04": "สี่เหลี่ยมมน", "05": "วงกลม", "07": "กากบาทข้อต่อวงกลม"}

def cone(k):
    """a cross with k lobes buttoned onto their neighbours: each closure takes a quarter turn out of the flat piece"""
    f = (360 - 90 * k) / 360
    return ARM * f, ARM * math.sqrt(1 - f * f)                 # base radius, height
TIERS = [cone(2), cone(1), (41.0, 20.0)]                       # the flat bottom piece droops; drawn as a shallow cup (a guess)
TREE_N = 3
TREE_PRICE, HANG_PRICE, HANG_SET, TAG_SET = 249, 49, 129, 99   # proposals, from the booth ladder (charm S 149 / M 209, piece 30)

def outline(code):
    g = geom.load(code); return "M" + "L".join(f"{x:.1f},{-y:.1f}" for x, y in g["poly"]) + "Z", g
def cuts(g): return "".join(f'<line class="cut" x1="{a[0]:.1f}" y1="{-a[1]:.1f}" x2="{b[0]:.1f}" y2="{-b[1]:.1f}"/>' for a, b in g["cuts"])
def svg(inner, vb, label, cls="fig"): return f'<svg class="{cls}" viewBox="{vb}" role="img" aria-label="{label}">{inner}</svg>'

def fig_tree():
    """side view: three cones on a red cord, ring on top, two tails with metal ends"""
    g = ['<path class="cord" d="M-3,-78 C-16,-60 -10,-44 0,-40 C10,-44 16,-60 3,-78"/>', '<circle class="ring" cx="0" cy="-84" r="9"/>']
    y = -30; tops = []
    for i, (r, h) in enumerate(TIERS):
        tops.append((y, r, h)); y += h - 8                       # the next tier's tip tucks 8 mm up under this one
    g.append(f'<path class="cord" d="M0,-40 V{tops[-1][0] + tops[-1][2] + 6:.1f}"/>')
    for i, (y0, r, h) in reversed(list(enumerate(tops))):                       # bottom tier first, so upper tiers overlap it
        b = y0 + h; s = 9
        g.append(f'<path class="leaf t{i}" d="M0,{y0:.1f} L{-r:.1f},{b:.1f} Q{-r * .66:.1f},{b + s:.1f} {-r * .33:.1f},{b:.1f} Q0,{b + s:.1f} {r * .33:.1f},{b:.1f} '
                 f'Q{r * .66:.1f},{b + s:.1f} {r:.1f},{b:.1f} Z"/>')
    yb = tops[-1][0] + tops[-1][2]
    g.append(f'<circle class="knot" cx="0" cy="{yb + 8:.1f}" r="4.2"/>')
    g.append(f'<path class="cord" d="M-1.5,{yb + 10:.1f} C-6,{yb + 40:.1f} -12,{yb + 62:.1f} -13,{yb + 84:.1f}"/><path class="cord" d="M1.5,{yb + 10:.1f} C5,{yb + 36:.1f} 9,{yb + 50:.1f} 10,{yb + 66:.1f}"/>')
    g.append(f'<rect class="tip" x="-16.2" y="{yb + 84:.1f}" width="6.4" height="13" rx="1.2"/><rect class="tip" x="6.8" y="{yb + 66:.1f}" width="6.4" height="13" rx="1.2"/>')
    g.append(f'<circle class="ring thin" cx="24" cy="{yb + 30:.1f}" r="3.2"/><path class="star" transform="translate(24,{yb + 44:.1f})" d="M0,-9L2.3,-3.1L8.6,-2.8L3.7,1.2L5.3,7.3L0,3.9L-5.3,7.3L-3.7,1.2L-8.6,-2.8L-2.3,-3.1Z"/>'
             f'<path class="cordthin" d="M1.5,{yb + 12:.1f} C12,{yb + 16:.1f} 22,{yb + 20:.1f} 24,{yb + 27:.1f}"/>')
    for (y0, r, h), t in zip(tops, ("ชั้นบน · ติด 2 จุด", "ชั้นกลาง · ติด 1 จุด", "ชั้นล่าง · ไม่ติด")):
        g.append(f'<line class="lead" x1="{r + 4:.1f}" y1="{y0 + h * .55:.1f}" x2="62" y2="{y0 + h * .55:.1f}"/><text x="65" y="{y0 + h * .55 + 3.5:.1f}" font-size="10">{t}</text>')
    g.append('<text x="14" y="-81" font-size="10">ห่วงทองเหลือง</text>' + f'<text x="34" y="{yb + 47:.1f}" font-size="10">จี้เล็ก ๆ</text><text x="-22" y="{yb + 94:.1f}" font-size="10" text-anchor="end">ปลายเชือกโลหะ</text>')
    return svg("".join(g), f"-95 -100 255 {yb + 205:.0f}", "ภาพร่างต้นสนจากชิ้น 07 สามชิ้น")

def fig_tier(k):
    """top view of one 07: which lobes button onto which slit"""
    d, g = outline("07"); s = [f'<path class="pc" d="{d}"/>', cuts(g)]
    arrows = [("M-34,-10 C-36,-30 -22,-38 -8,-31", "กลีบซ้าย → ร่องบน"), ("M34,10 C36,30 22,38 8,31", "กลีบขวา → ร่องล่าง")][:k]
    for a, _ in arrows:
        s.append(f'<path class="arrow" d="{a}" marker-end="url(#ah)"/>')
    if k: s.append('<circle class="hit" cx="-28.4" cy="0" r="11"/>' + ('<circle class="hit" cx="28.4" cy="0" r="11"/>' if k == 2 else ""))
    s.append('<circle class="hole" cx="0" cy="0" r="2.2"/>')
    cap = ["ชั้นล่าง: ไม่ติด ปล่อยแบน", "ชั้นกลาง: ติด 1 จุด", "ชั้นบน: ติด 2 จุด"][k]
    r, h = cone(k)
    sub = "กว้าง 9 ซม." if k == 0 else f"หุบเป็นกรวย กว้าง ~{2 * r / 10:.1f} สูง ~{h / 10:.1f} ซม."
    return (f'<figure>{svg("<defs><marker id=ah viewBox=&quot;0 0 10 10&quot; refX=8 refY=5 markerWidth=6 markerHeight=6 orient=auto><path d=&quot;M0,0L10,5L0,10Z&quot; class=ahead /></marker></defs>".replace("&quot;", chr(34)) + "".join(s), "-52 -52 104 104", cap)}'
            f'<figcaption><b>{cap}</b><br>{sub}</figcaption></figure>')

def fig_hang(code, cord="red"):
    d, g = outline(code); pts = g["poly"]
    if code == "01":                                   # the die has its ears to the right and up: turn it 45 deg so both ears sit on top
        c = math.sqrt(.5); pts = [(x * c - y * c, x * c + y * c) for x, y in pts]
        d = "M" + "L".join(f"{x:.1f},{-y:.1f}" for x, y in pts) + "Z"
    xs = [p[0] for p in pts]; ys = [-p[1] for p in pts]
    cx = 0.0; P = list(zip(xs, ys)); hits = []                                    # top edge straight above the centre
    for (x1, y1), (x2, y2) in zip(P, P[1:] + P[:1]):
        if (x1 - cx) * (x2 - cx) <= 0 and x1 != x2: hits.append(y1 + (y2 - y1) * (cx - x1) / (x2 - x1))
    top = min(hits)
    hole = top + 8
    s = (f'<path class="cord {cord}" d="M{cx - 1.5},{hole} C{cx - 14},{top - 26} {cx - 6},{top - 44} {cx},{top - 46} C{cx + 6},{top - 44} {cx + 14},{top - 26} {cx + 1.5},{hole}"/>'
         f'<path class="pc" d="{d}"/><circle class="hole" cx="{cx}" cy="{hole}" r="2.2"/>')
    return f'<figure>{svg(s, f"{min(xs) - 6:.0f} {top - 52:.0f} {max(xs) - min(xs) + 12:.0f} {max(ys) - top + 58:.0f}", f"ของประดับ {code}")}<figcaption><b>{code}</b> {NAME[code]}</figcaption></figure>'

def fig_star():
    d, g = outline("07")
    s = (f'<path class="cord red" d="M-1.5,-36 C-14,-62 -6,-80 0,-82 C6,-80 14,-62 1.5,-36"/><path class="pc dark" d="{d}"/><g transform="rotate(45) scale(.86)"><path class="pc" d="{d}"/></g>'
         '<circle class="rivet" cx="0" cy="0" r="3.4"/><circle class="hole" cx="0" cy="-37" r="2.2"/>')
    return f'<figure>{svg(s, "-52 -90 104 142", "ดาวจาก 07 สองชิ้น")}<figcaption><b>ดาว</b> 07 สองชิ้นไขว้ 45° ตรึงหมุดกลาง</figcaption></figure>'

def fig_tag():
    d, g = outline("03")
    s = (f'<path class="cord red" d="M-1.5,-34 C-22,-58 -34,-70 -50,-74 M1.5,-34 C10,-58 28,-72 50,-70"/><path class="pc" d="{d}"/><circle class="hole" cx="0" cy="-36" r="2.2"/>'
         '<text x="0" y="2" text-anchor="middle" font-size="9" class="hand">ถึง ...</text><line class="rule" x1="-18" y1="14" x2="18" y2="14"/>')
    return f'<figure>{svg(s, "-56 -82 112 132", "ป้ายห้อยของขวัญ 03")}<figcaption><b>03 ป้ายห้อยของขวัญ</b> ผูกเชือกแดง เขียนชื่อได้</figcaption></figure>'

E = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;")
tree_cost = TREE_N * COST["07"]
max_trees = STOCK["07"] // TREE_N
rows = [
    ("ต้นสน 07", f"07 × {TREE_N}", f"{tree_cost:.0f}", f"{TREE_PRICE}", f"07 เหลือ {STOCK['07']} ทำได้สูงสุด {max_trees} ต้น ถ้าไม่ขาย 07 อย่างอื่นเลย"),
    ("ของประดับชิ้นเดียว", "01–05 อย่างละ 1", "4", f"{HANG_PRICE} · ชุด 3 ชิ้น {HANG_SET}", f"ชิ้น 01–05 มี {sum(STOCK[c] for c in ('01','02','03','04','05'))} ชิ้น ขายช้า"),
    ("ป้ายห้อยของขวัญ 03", "03 × 1", f"{COST['03']:.0f}", f"39 (ราคาเดิม) · ชุด 3 ใบ {TAG_SET}", f"03 มี {STOCK['03']} ชิ้น เป็นสินค้าเดิม OC-03-26"),
]
row_html = "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td><td class='num'>{c}</td><td class='num'>{d}</td><td>{E(e)}</td></tr>" for a, b, c, d, e in rows)
SUB = {"__FIG_TREE__": fig_tree(), "__TIERS__": fig_tier(0) + fig_tier(1) + fig_tier(2),
       "__HANGS__": "".join(fig_hang(c) for c in ("05", "04", "02", "01")) + fig_star(), "__TAG__": fig_tag(), "__ROWS__": row_html,
       "__TREE_PRICE__": str(TREE_PRICE), "__TREE_COST__": f"{tree_cost:.0f}", "__MAX_TREES__": str(max_trees), "__LEFT07__": str(STOCK["07"]),
       "__TOPW__": f"{2 * cone(2)[0] / 10:.1f}", "__MIDW__": f"{2 * cone(1)[0] / 10:.1f}"}
page = open(os.path.join(HERE, "template.html")).read()
for k, v in SUB.items(): page = page.replace(k, v)
open(os.path.join(HERE, "index.html"), "w").write(page)
print("xmas/index.html", len(page), "bytes · tiers (r, h):", [(round(r, 1), round(h, 1)) for r, h in TIERS], f"· leather per tree {tree_cost:.2f} baht · max {max_trees} trees")
