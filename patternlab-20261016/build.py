"""Pattern Lab 16 Oct 2026: five new die-cut patterns that follow the SOI. 02 joint rules, two end products each.

Concept drawings only, not die files. Every piece keeps the rules of ../diecut-leather-20261014/generate.py:
  - every edge has a wing; a TAB edge narrows the wing neck with two edge slots, a SLOT edge has a slit on the fold line
  - neck = slit - 0.5 mm, slots that open onto the outline run 1.0 mm past it, all centred on the edge's centre line
  - tabs and slots are balanced on every piece, so any number of pieces join
Two joint sizes: S64 (slit 30.0 / neck 29.5, same as 04 and 05) and S30 (slit 15.0 / neck 14.5, new).

python3 build.py -> svg/*.svg and site/index.html
"""
import html, math, os
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
from shapely import affinity

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_SVG = os.path.join(HERE, "svg"); os.makedirs(OUT_SVG, exist_ok=True)
E = html.escape
S64 = dict(slit=30.0, neck=29.5, name="S64")
S30 = dict(slit=15.0, neck=14.5, name="S30")
OVERRUN = 1.0
BOX = 90.0                      # same die block as patterns 02-06

# ---------------------------------------------------------------- geometry
def regular(n, edge, rot=0.0):
    R = edge / (2 * math.sin(math.pi / n))
    return [(R * math.cos(rot + 2 * math.pi * k / n), R * math.sin(rot + 2 * math.pi * k / n)) for k in range(n)]

def wing(a, b, kind, w, depth=None):
    """Wing on edge a-b of a CCW core: circle of radius w on the edge midpoint, or a rounded petal."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    tx, ty = b[0] - a[0], b[1] - a[1]; L = math.hypot(tx, ty); tx, ty = tx / L, ty / L
    nx, ny = ty, -tx                                   # outward normal for a CCW polygon
    if kind == "circle":
        return Point(mx, my).buffer(w, 64)
    d = depth or w
    if kind == "bud":                                   # round base keeps leather round the slit tips, pointed tip for the look
        tip = Polygon([(mx - tx * w * 0.75, my - ty * w * 0.75), (mx + nx * d, my + ny * d), (mx + tx * w * 0.75, my + ty * w * 0.75)])
        return Point(mx, my).buffer(w, 64).union(tip.buffer(-1.5).buffer(1.5, 16))
    tri = Polygon([(mx - tx * w, my - ty * w), (mx + nx * d, my + ny * d), (mx + tx * w, my + ty * w)])
    return tri.buffer(-2.5).buffer(2.5, 32).union(Polygon([(mx - tx * w, my - ty * w), (mx + tx * w, my + ty * w),
                                                        (mx + tx * w - nx * 3, my + ty * w - ny * 3), (mx - tx * w - nx * 3, my - ty * w - ny * 3)]))

def piece(core, edges):
    """core: CCW points. edges: per edge (gender 'T'|'S'|None, joint, wing kind, wing half-width, depth).
    A tab's two neck slots run along the fold line from the neck out through the outline, plus OVERRUN,
    so the tab wing is free of its neighbours even where the wings overlap at a corner (as on 03)."""
    shapes = [Polygon(core)]
    for i, e in enumerate(edges):
        if e[0] is not None:
            a, b = core[i], core[(i + 1) % len(core)]
            shapes.append(wing(a, b, e[2], e[3], e[4]))
    outline = unary_union(shapes)
    folds, cuts = [], []
    for i, e in enumerate(edges):
        a, b = core[i], core[(i + 1) % len(core)]
        g, joint, kind, w, depth = e
        if g is None:
            continue
        folds.append((a, b))
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        tx, ty = b[0] - a[0], b[1] - a[1]; L = math.hypot(tx, ty); tx, ty = tx / L, ty / L
        if g == "S":
            h = joint["slit"] / 2
            cuts.append(((mx - tx * h, my - ty * h), (mx + tx * h, my + ty * h)))
        else:
            h = joint["neck"] / 2
            for s in (-1, 1):
                p0 = (mx + s * tx * h, my + s * ty * h)
                ray = LineString([p0, (mx + s * tx * 120, my + s * ty * 120)])
                inside = ray.intersection(outline.buffer(-0.05))     # strict interior: a cut along the outline is no cut
                parts = [inside] if inside.geom_type == "LineString" else list(getattr(inside, "geoms", []))
                part = min(parts, key=lambda q: q.distance(Point(p0)))
                far = max(part.coords, key=lambda q: math.dist(q, p0))
                r = math.dist(far, (mx, my)) + OVERRUN
                cuts.append((p0, (mx + s * tx * r, my + s * ty * r)))
    # centre in the die block
    minx, miny, maxx, maxy = outline.bounds
    dx, dy = (BOX - (maxx - minx)) / 2 - minx, (BOX - (maxy - miny)) / 2 - miny
    mv = lambda p: (p[0] + dx, p[1] + dy)
    return dict(outline=affinity.translate(outline, dx, dy), folds=[(mv(a), mv(b)) for a, b in folds],
                cuts=[(mv(a), mv(b)) for a, b in cuts], core=[mv(p) for p in core],
                size=(round(maxx - minx, 1), round(maxy - miny, 1)), edges=edges)

def path_d(poly):
    ring = list(poly.exterior.coords)
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in ring) + "Z"

def tagline(p):
    t = sum(1 for e in p["edges"] if e[0] == "T"); s = sum(1 for e in p["edges"] if e[0] == "S")
    return t, s

# ---------------------------------------------------------------- the five patterns
def hexcore(edge):
    return regular(6, edge, 0.0)                       # flat top: a vertex on the x axis

# sizes set so every closed slit tip keeps at least LIG mm of leather to the outline (see ligaments())
LIG = 8.0
SIZE = dict(hex_edge=32, hex_r=15.5, link_w=48, link_h=40, link_r=23, mini=32, mini_r=15.5,
            taper_top=63.6, taper_bot=48.0, taper_h=55.0, taper_r=15.5, petal_w=12, petal_d=18)

def p07():
    c = hexcore(SIZE["hex_edge"])
    return piece(c, [("T" if i % 2 == 0 else "S", S30, "circle", SIZE["hex_r"], None) for i in range(6)])

def p08():
    w, h = SIZE["link_w"], SIZE["link_h"]
    c = [(-w / 2, h / 2), (-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2)]   # CCW in y-down screen space is CW; fix below
    c = c[::-1]
    # edges after reversal: 0 top? compute by midpoint so genders land on the short ends
    edges = []
    for i in range(4):
        a, b = c[i], c[(i + 1) % 4]
        if abs(a[1] - b[1]) < 1e-6:                      # horizontal edge = an end of the link
            g = "T" if a[1] + b[1] > 0 else "S"
            edges.append((g, S64, "circle", SIZE["link_r"], None))
        else:
            edges.append((None, None, None, 0, None))
    return piece(c, edges)

def p09():
    c = hexcore(SIZE["hex_edge"])
    return piece(c, [("T", S30, "petal", SIZE["petal_w"], SIZE["petal_d"]) if i % 2 == 0 else ("S", S30, "circle", SIZE["hex_r"], None)
                     for i in range(6)])

def p10():
    c = regular(4, SIZE["mini"], math.pi / 4)
    return piece(c, [("T" if i % 2 == 0 else "S", S30, "circle", SIZE["mini_r"], None) for i in range(4)])

def p11():
    top, bot, h = SIZE["taper_top"], SIZE["taper_bot"], SIZE["taper_h"]
    c = [(-top / 2, -h / 2), (top / 2, -h / 2), (bot / 2, h / 2), (-bot / 2, h / 2)]
    if Polygon(c).exterior.is_ccw is False:
        c = c[::-1]
    edges = []
    for i in range(4):
        a, b = c[i], c[(i + 1) % 4]
        if abs(a[1] - b[1]) < 1e-6:
            edges.append((None, None, None, 0, None))
        else:
            g = "T" if a[0] + b[0] < 0 else "S"
            edges.append((g, S30, "circle", SIZE["taper_r"], None))
    return piece(c, edges)

def ligaments(p):
    """Leather left round each closed cut tip, mm: to the outline and to every other cut.
    Tips that run past the outline are skipped."""
    segs = [LineString(c) for c in p["cuts"]]
    out = []
    for i, g in enumerate(segs):
        for e in g.coords:
            P = Point(e)
            if not p["outline"].contains(P) or p["outline"].exterior.distance(P) < 0.3:
                continue
            others = [g2.distance(P) for j, g2 in enumerate(segs) if j != i]
            out.append(min([p["outline"].exterior.distance(P)] + others))
    return min(out) if out else None

# ---------------------------------------------------------------- drawing: one pattern, 1:1 in mm
def pattern_svg(p, uid):
    g = [f'<path class="cut" d="{path_d(p["outline"])}"/>']
    g += [f'<line class="fold" x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}"/>' for a, b in p["folds"]]
    g += [f'<line class="slit" x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}"/>' for a, b in p["cuts"]]
    cx = sum(x for x, _ in p["core"]) / len(p["core"]); cy = sum(y for _, y in p["core"]) / len(p["core"])
    core = p["core"]
    for i, e in enumerate(p["edges"]):
        if e[0] is None:
            continue
        a, b = core[i], core[(i + 1) % len(core)]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        lx, ly = mx + (cx - mx) * 0.32, my + (cy - my) * 0.32
        word = "ปีก" if e[0] == "T" else "ร่อง"
        g.append(f'<text class="lbl {"t" if e[0] == "T" else "s"}" x="{lx:.2f}" y="{ly + 1.1:.2f}">{word}</text>')
    return (f'<svg viewBox="0 0 {BOX:.0f} {BOX:.0f}" role="img" aria-labelledby="{uid}"><title id="{uid}">แพตเทิร์น 1:1 ในกรอบ 90 × 90 มม.</title>'
            f'<rect class="die" x="0.2" y="0.2" width="{BOX - 0.4}" height="{BOX - 0.4}" rx="2"/>{"".join(g)}</svg>')

# ---------------------------------------------------------------- drawing: end products (schematic)
LEATHER = ["var(--l1)", "var(--l2)", "var(--l3)"]

def poly_pts(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def honeycomb(cols, rows, s=30, pad=8):
    """Flat-top hex cores in a honeycomb, every piece in the same orientation."""
    hexes = []
    w = math.sqrt(3) * s
    for cI in range(cols):
        for rI in range(rows):
            cx = pad + s + cI * 1.5 * s
            cy = pad + w / 2 + rI * w + (w / 2 if cI % 2 else 0)
            hexes.append((cI, rI, [(cx + x, cy + y) for x, y in regular(6, s, 0)]))
    W = pad * 2 + s * 2 + (cols - 1) * 1.5 * s
    H = pad * 2 + w * rows + (w / 2 if cols > 1 else 0)
    return hexes, W, H

def prod_trivet():
    keep = {(1, 1), (1, 0), (1, 2), (0, 0), (0, 1), (2, 0), (2, 1)}
    hexes, W, H = honeycomb(3, 3)
    g = [f'<polygon class="lp" style="fill:{LEATHER[(c + r) % 3]}" points="{poly_pts(p)}"/>' for c, r, p in hexes if (c, r) in keep]
    return W, H, "".join(g), "ที่รองหม้อร้อนรังผึ้ง 7 ชิ้น"

def prod_runner():
    hexes, W, H = honeycomb(9, 3)
    g = [f'<polygon class="lp" style="fill:{LEATHER[(c * 2 + r) % 3]}" points="{poly_pts(p)}"/>' for c, r, p in hexes]
    return W, H, "".join(g), "ผ้ารองกลางโต๊ะรังผึ้ง 27 ชิ้น"

def link_chain(x0, y0, n, ang, w=44, h=40, scale=1.0, start=0, wscale=None):
    """n link cores end to end from (x0, y0) along angle ang (deg), as rotated rects."""
    g = []
    ws = scale if wscale is None else wscale
    for i in range(n):
        cx = x0 + math.cos(math.radians(ang)) * (h * scale) * (i + 0.5)
        cy = y0 + math.sin(math.radians(ang)) * (h * scale) * (i + 0.5)
        g.append(f'<rect class="lp" style="fill:{LEATHER[(i + start) % 3]}" x="{-w * ws / 2:.1f}" y="{-h * scale / 2:.1f}" width="{w * ws:.1f}" height="{h * scale:.1f}" rx="3" '
                 f'transform="translate({cx:.1f},{cy:.1f}) rotate({ang - 90:.1f})"/>')
    return "".join(g)

def prod_tieback():
    W, H = 380, 300
    curtain = ('<path class="cloth" d="M60,10 C80,90 70,120 150,150 C70,180 80,240 40,290 L330,290 C300,240 310,180 230,150 C310,120 300,90 320,10 Z"/>'
               '<path class="clothline" d="M120,10 C130,80 140,120 170,150 C140,190 135,240 120,290 M260,10 C250,80 240,120 210,150 C240,190 245,240 260,290"/>')
    band = link_chain(118, 150, 4, 0, scale=0.9)
    return W, H, curtain + band, "ที่รัดผ้าม่าน 6 ข้อ ปิดเป็นวง"

def prod_hanger():
    W, H = 360, 420
    top = (180, 30)
    g = [f'<circle class="ring" cx="{top[0]}" cy="{top[1] - 14}" r="12"/>']
    for x in (70, 140, 220, 290):
        ang = math.degrees(math.atan2(300 - top[1], x - top[0]))
        g.append(link_chain(top[0], top[1], 6, ang, scale=math.hypot(x - top[0], 300 - top[1]) / 240, wscale=0.42))
    g.append('<path class="pot" d="M90,300 L270,300 L250,400 L110,400 Z"/>')
    g.append('<path class="leaf" d="M180,300 C150,240 110,230 95,250 C120,255 150,270 180,300 Z M180,300 C210,230 260,225 270,245 C240,250 210,270 180,300 Z M180,300 C175,250 185,215 200,200 C200,240 190,270 180,300 Z"/>')
    return W, H, "".join(g), "ที่แขวนกระถาง ฐาน 05 + 4 สาย สายละ 6 ข้อ"

def bloom_outline(p, scale, cx, cy):
    poly = affinity.translate(affinity.scale(p["outline"], scale, scale, origin=(45, 45)), cx - 45, cy - 45)
    return path_d(poly)

def prod_coaster(p):
    W, H = 300, 300
    d = bloom_outline(p, 3.1, 150, 150)
    return W, H, (f'<path class="lp" style="fill:var(--l2)" d="{d}"/><circle class="cup" cx="150" cy="150" r="78"/>'
                  '<circle class="cupin" cx="150" cy="150" r="62"/>'), "ที่รองแก้วดอกไม้ 1 ชิ้น หรือต่อ 7 ชิ้นเป็นถาด"

def prod_curtain(p):
    W, H = 360, 440
    g = ['<rect class="rod" x="10" y="14" width="340" height="8" rx="4"/>']
    for k, x in enumerate((60, 140, 220, 300)):
        g.append(f'<line class="string" x1="{x}" y1="22" x2="{x}" y2="40"/>')
        for i in range(5 - (k % 2)):
            y = 70 + i * 74 + (k % 2) * 37
            g.append(f'<path class="lp" style="fill:{LEATHER[(i + k) % 3]}" d="{bloom_outline(p, 0.9, x, y)}"/>')
    return W, H, "".join(g), "ม่านดอกไม้แขวนหน้าต่าง 4 สาย 18 ชิ้น"

# simple oblique 3-D: x right, y depth, z up
def proj(x, y, z, k=0.42):
    return (x + 0.0 * y, -z + y * k)

def prism(n, r_bot, r_top, h, cx, cy, rot, fill_front, fill_top=None, open_top=False, scale=1.0):
    bot = [(r_bot * math.cos(rot + 2 * math.pi * i / n), r_bot * math.sin(rot + 2 * math.pi * i / n), 0) for i in range(n)]
    top = [(r_top * math.cos(rot + 2 * math.pi * i / n), r_top * math.sin(rot + 2 * math.pi * i / n), h) for i in range(n)]
    P = lambda q: (cx + proj(*q)[0] * scale, cy + proj(*q)[1] * scale)
    faces = []
    for i in range(n):
        j = (i + 1) % n
        quad = [bot[i], bot[j], top[j], top[i]]
        my = (bot[i][1] + bot[j][1]) / 2
        faces.append((my, quad, i))
    faces.sort()
    g = []
    for my, quad, i in faces:
        front = my > 0
        if not front:
            if open_top:
                g.append(f'<polygon class="inner" points="{poly_pts([P(q) for q in quad])}"/>')
            continue
        g.append(f'<polygon class="lp" style="fill:{fill_front[i % len(fill_front)]}" points="{poly_pts([P(q) for q in quad])}"/>')
    if not open_top:
        g.append(f'<polygon class="lp" style="fill:{fill_top or "var(--l1)"}" points="{poly_pts([P(q) for q in top])}"/>')
    else:
        g.append(f'<polygon class="rim" points="{poly_pts([P(q) for q in top])}"/>')
    return "".join(g)

def prod_hexbox():
    W, H = 320, 260
    R = 32.0                                            # hex side 32 = circumradius 32
    body = prism(6, R, R, 30, 160, 175, 0, LEATHER, "var(--l2)", scale=3.0)
    return W, H, body, "กล่องหกเหลี่ยม A × 2 + D × 6"

def prod_mobile():
    W, H = 360, 400
    g = ['<rect class="rod" x="40" y="20" width="280" height="7" rx="3.5"/>']
    for k, (x, L) in enumerate(((80, 120), (180, 220), (280, 160))):
        g.append(f'<line class="string" x1="{x}" y1="27" x2="{x}" y2="{L}"/>')
        g.append(prism(4, 22.6, 22.6, 32, x, L + 70, math.pi / 4 + k * 0.3, [LEATHER[(k + 1) % 3], LEATHER[k % 3]], LEATHER[(k + 2) % 3], scale=2.0))
    return W, H, "".join(g), "โมบายลูกบาศก์ 32 มม. 3 ลูก ลูกละ 6 ชิ้น"

def prod_planter():
    W, H = 320, 330
    n, top, bot, h = 4, 63.6, 48.0, 55.0
    Rt, Rb = top / math.sqrt(2), bot / math.sqrt(2)
    leaves = ('<path class="leaf" d="M160,120 C120,50 70,50 60,70 C95,75 130,95 160,120 Z M160,120 C200,45 255,45 262,68 C225,72 190,95 160,120 Z '
              'M160,120 C150,60 165,20 185,5 C188,55 172,95 160,120 Z"/>')
    body = prism(n, Rb, Rt, h, 160, 300, math.pi / 4, LEATHER, open_top=True, scale=2.7)
    return W, H, leaves + body, "ปลอกกระถาง 4 ชิ้น (กระถาง 3 นิ้ว)"

def prod_lamp():
    W, H = 320, 360
    n, e_top, e_bot, h = 8, 48.0, 63.6, 55.0
    Rt, Rb = e_top / (2 * math.sin(math.pi / n)), e_bot / (2 * math.sin(math.pi / n))
    sc = 1.55
    cord = f'<line class="string" x1="160" y1="0" x2="160" y2="{300 - h * sc:.0f}"/>'
    shade = prism(n, Rb, Rt, h, 160, 300, math.pi / 8, LEATHER, open_top=True, scale=sc)
    bulb = '<circle class="bulb" cx="160" cy="300" r="20"/>'
    return W, H, cord + bulb + shade, "โป๊ะโคมไฟ LED 8 ชิ้น"

def prod_svg(spec, uid):
    W, H, body, title = spec
    return f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-labelledby="{uid}"><title id="{uid}">{E(title)}</title>{body}</svg>'

# ---------------------------------------------------------------- content
def build():
    P = {"07": p07(), "08": p08(), "09": p09(), "10": p10(), "11": p11()}
    for k, p in P.items():
        assert p["size"][0] <= BOX + 0.01 and p["size"][1] <= BOX + 0.01, (k, p["size"])
    B = P["09"]
    D = [
        ("A", "รังผึ้ง", "Honeycomb", S30, P["07"],
         "หกเหลี่ยมด้านละ 32 มม. ปีกกับร่องสลับกันรอบชิ้น 3 + 3 ด้านตรงข้ามจึงเป็นปีกกับร่องเสมอ ทุกชิ้นวางทิศเดียวกันแล้วต่อเป็นรังผึ้งได้ทุกทิศ ไม่ต้องหมุนสลับเหมือนสี่เหลี่ยม",
         [(prod_trivet(), "7 ชิ้น · กว้างราว 16 ซม.", "ร้านอาหาร ครัวบ้าน"),
          (prod_runner(), "27 ชิ้น · ราว 15 × 42 ซม. ต่อยาวได้อีก", "โฮมเดคอร์ ของขวัญขึ้นบ้านใหม่")]),
        ("B", "ข้อโซ่", "Link", S64, P["08"],
         "ชิ้นยาว ปีกหนึ่งปลาย ร่องอีกปลาย (1 + 1) ต่อเป็นสายยาวเท่าไรก็ได้ ข้อต่อขนาด S64 เท่ากับแบบ 04 และ 05 ปลายสายจึงเสียบเข้าชิ้นสี่เหลี่ยมหรือวงกลมเดิมได้เลย",
         [(prod_tieback(), "6 ข้อ · รอบวงราว 24 ซม.", "ร้านผ้าม่าน โฮมเดคอร์"),
          (prod_hanger(), "ฐาน 05 หนึ่งชิ้น + 24 ข้อ", "ร้านต้นไม้ คาเฟ่")]),
        ("C", "ดอกพิกุล", "Bloom", S30, P["09"],
         "โครงหกเหลี่ยมเดียวกับ A แต่ปีกเป็นกลีบแหลม ข้อต่อเหมือนกันทุกมิลลิเมตร จึงต่อปนกับ A ได้ เป็นตัวอย่างว่าเปลี่ยนแค่รูปปีก ก็ได้แพตเทิร์นใหม่ที่ยังต่อกับของเดิมได้",
         [(prod_coaster(B), "1 ชิ้น · กว้างราว 8 ซม.", "คาเฟ่ ของชำร่วย"),
          (prod_curtain(B), "18 ชิ้น · ยาวตามหน้าต่าง", "ตกแต่งหน้าต่าง ร้านคาเฟ่")]),
        ("D", "สี่เหลี่ยมจิ๋ว", "Mini square", S30, P["10"],
         "สี่เหลี่ยมด้านละ 32 มม. ปีกคู่หนึ่ง ร่องคู่หนึ่ง กฎเดียวกับ 03–06 แต่ใช้เศษเล็กแค่ 63 มม. ด้านยาวเท่ากับ A และข้อต่อ S30 เหมือนกัน จึงต่อเป็นผนังของกล่องหกเหลี่ยมได้",
         [(prod_hexbox(), "ฝา-ก้น A สองชิ้น + ผนัง D หกชิ้น", "กล่องชา ขนม ของขวัญ"),
          (prod_mobile(), "18 ชิ้น · ลูกบาศก์ 3.2 ซม.", "ห้องเด็ก โฮมเดคอร์")]),
        ("E", "ทรงสอบ", "Taper", S30, P["11"],
         "สี่เหลี่ยมคางหมู บน 63.6 ล่าง 48 สูง 55 มม. ปีกด้านซ้าย ร่องด้านขวา ต่อเรียงเป็นวงรอบได้กี่ชิ้นก็ได้ 4 ชิ้นได้ทรงสี่เหลี่ยม 8 ชิ้นได้ทรงแปดเหลี่ยม ปีกที่รอยต่อตั้งเป็นครีบด้านนอก",
         [(prod_planter(), "4 ชิ้น · ปาก 6.4 ซม. ต่อด้าน", "ร้านต้นไม้ ของขวัญ"),
          (prod_lamp(), "8 ชิ้น · ปากล่างกว้างราว 17 ซม.", "ร้านไฟ คาเฟ่ ใช้หลอด LED เท่านั้น")]),
    ]
    for code, th, en, j, p, why, prods in D:
        open(os.path.join(OUT_SVG, f"{code}-{en.lower().replace(' ', '-')}.svg"), "w").write(
            '<svg xmlns="http://www.w3.org/2000/svg"' + pattern_svg(p, "t" + code)[4:].replace(
                "<title", '<style>.cut{fill:#FFF6EC;stroke:#1C1B22;stroke-width:.3}.fold{stroke:#2449D8;stroke-width:.25;stroke-dasharray:1.2 1}.slit{stroke:#FF5A36;stroke-width:.45}.die{fill:none;stroke:#ccc;stroke-width:.2}.lbl{font:2.6px sans-serif;text-anchor:middle}.t{fill:#1C1B22}.s{fill:#FF5A36}</style><title', 1))
    return D

def page(D):
    cards = []
    for code, th, en, j, p, why, prods in D:
        t, s = tagline(p)
        pr = "".join(
            f'<figure class="prod"><div class="pv">{prod_svg(spec, f"p{code}{i}")}</div>'
            f'<figcaption><b>{E(spec[3])}</b><span>{E(qty)}</span><span class="who">{E(who)}</span></figcaption></figure>'
            for i, (spec, qty, who) in enumerate(prods))
        cards.append(f"""
<article class="pat" id="p{code}">
  <header class="ph"><span class="code">{code}</span><div><h2>{E(th)} <span class="en">{E(en)}</span></h2>
  <p class="spec">ข้อต่อ {j['name']} · slit {j['slit']:.1f} / คอปีก {j['neck']:.1f} มม. · ปีก {t} ร่อง {s} · ชิ้น {p['size'][0]:g} × {p['size'][1]:g} มม.</p></div></header>
  <div class="body">
    <figure class="die-fig"><div class="dv">{pattern_svg(p, "d" + code)}</div><figcaption>ภาพ 1:1 ในกรอบแม่พิมพ์ 90 × 90 มม. เส้นดำ = ตัด · แดง = slit · ฟ้าประ = แนวพับ</figcaption></figure>
    <div class="txt"><p>{E(why)}</p></div>
  </div>
  <div class="prods">{pr}</div>
</article>""")
    compat = """
<table class="cmp"><thead><tr><th>ข้อต่อ</th><th>slit / คอปีก (มม.)</th><th>แพตเทิร์นที่ต่อกันได้</th></tr></thead><tbody>
<tr><td><b>S64</b></td><td class="n">30.0 / 29.5</td><td>04 สี่เหลี่ยมมน · 05 วงกลม · <b>B ข้อโซ่</b></td></tr>
<tr><td><b>S30</b> ใหม่</td><td class="n">15.0 / 14.5</td><td><b>A รังผึ้ง · C ดอกพิกุล · D สี่เหลี่ยมจิ๋ว · E ทรงสอบ</b></td></tr>
</tbody></table>"""
    return f"""<title>OCT. 26 Pattern Lab</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@500;600&family=IBM+Plex+Sans+Thai:wght@400;600&family=Jost:wght@400;500&display=swap">
<style>
/* layout: one column of pattern sheets; each sheet = die drawing beside its reasoning, two products below */
:root{{
  --paper:#FFF6EC; --ink:#1C1B22; --muted:#5E5A66; --line:#E8DCCB; --cobalt:#2449D8; --tomato:#FF5A36; --mint:#2EC4A0; --card:#FFFFFF;
  --l1:#B8743A; --l2:#9A5E2C; --l3:#D08F55; --leafc:#2EC4A0; --cloth:#DCE3FB; --glass:#FFFFFF; --bulb:#FFE6A6;
  --display:'Anuphan','IBM Plex Sans Thai',sans-serif; --body:'IBM Plex Sans Thai','Anuphan',sans-serif; --latin:'Jost','IBM Plex Sans Thai',sans-serif;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{
  --paper:#17161C; --ink:#F4EDE3; --muted:#B3ACA3; --line:#34313B; --cobalt:#7F9BFF; --tomato:#FF7A5C; --card:#211F27; --cloth:#2A3354; --glass:#2D2A33; color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#17161C; --ink:#F4EDE3; --muted:#B3ACA3; --line:#34313B; --cobalt:#7F9BFF; --tomato:#FF7A5C; --card:#211F27; --cloth:#2A3354; --glass:#2D2A33; color-scheme:dark}}
body{{background:var(--paper);color:var(--ink);font:400 16px/1.7 var(--body)}}
.wrap{{max-width:1040px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:34px 89px;display:flex;flex-direction:column;gap:55px}}
h1,h2{{font-family:var(--display);font-weight:600;line-height:1.25;text-wrap:balance;margin:0}}
h1{{font-size:clamp(28px,6vw,41.9px)}} h2{{font-size:25.9px}}
.eyebrow{{font:500 12.6px/1 var(--latin);letter-spacing:.14em;text-transform:uppercase;color:var(--cobalt)}}
.lead{{font-size:18px;max-width:62ch;margin:0}}
p{{margin:0}}
.intro{{display:flex;flex-direction:column;gap:13px}}
.rules{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:13px;margin:0;padding:0;list-style:none;counter-reset:r}}
.rules li{{border-top:2px solid var(--ink);padding-top:8px;font-size:15px;min-width:0}}
.rules b{{display:block;font-family:var(--display);font-weight:600;font-size:17px}}
.note{{font-size:14px;color:var(--muted);max-width:70ch}}
.pat{{display:flex;flex-direction:column;gap:21px;border-top:1px solid var(--line);padding-top:34px}}
.ph{{display:flex;gap:13px;align-items:flex-start}}
.code{{font:500 41.9px/1 var(--latin);color:var(--tomato);min-width:2.2ch}}
.en{{font:400 18px var(--latin);color:var(--muted);margin-left:4px}}
.spec{{font:400 13.5px/1.5 var(--latin);color:var(--muted);font-variant-numeric:tabular-nums;margin-top:4px}}
.body{{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:21px;align-items:start}}
@media (max-width:640px){{.body{{grid-template-columns:1fr}}}}
.die-fig,.prod{{margin:0;display:flex;flex-direction:column;gap:8px}}
.dv{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px;max-width:320px}}
.dv svg{{display:block;width:100%;height:auto}}
figcaption{{font-size:13px;color:var(--muted);line-height:1.5}}
.txt{{min-width:0;font-size:16.5px;max-width:60ch}}
.prods{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:21px}}
@media (max-width:560px){{.prods{{grid-template-columns:1fr}}}}
.pv{{background:var(--card);border:1px solid var(--line);border-radius:8px;aspect-ratio:4/3;max-width:100%;display:flex;align-items:center;justify-content:center;padding:13px}}
.pv svg{{width:100%;height:100%}}
.prod figcaption{{display:flex;flex-direction:column;gap:0}}
.prod b{{color:var(--ink);font-family:var(--display);font-weight:600;font-size:16px}}
.who{{color:var(--cobalt)}}
.cmpwrap{{overflow-x:auto}}
.cmp{{border-collapse:collapse;width:100%;font-size:15px}}
.cmp th,.cmp td{{text-align:left;padding:8px 13px 8px 0;border-bottom:1px solid var(--line);vertical-align:top}}
.cmp th{{font:500 12.6px var(--latin);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.n{{font-variant-numeric:tabular-nums;white-space:nowrap}}
.next{{display:flex;flex-direction:column;gap:13px}}
.next ol{{margin:0;padding-left:1.3em;display:flex;flex-direction:column;gap:5px;max-width:68ch}}
/* drawings */
.die{{fill:none;stroke:var(--line);stroke-width:.3}}
.cut{{fill:var(--paper);stroke:var(--ink);stroke-width:.35}}
.fold{{stroke:var(--cobalt);stroke-width:.3;stroke-dasharray:1.2 1}}
.slit{{stroke:var(--tomato);stroke-width:.55;stroke-linecap:round}}
.lbl{{font:600 2.7px var(--body);text-anchor:middle}} .lbl.t{{fill:var(--ink)}} .lbl.s{{fill:var(--tomato)}}
.lp{{stroke:var(--ink);stroke-width:1.2;stroke-linejoin:round}}
.inner{{fill:var(--l2);opacity:.55;stroke:var(--ink);stroke-width:1}}
.rim{{fill:none;stroke:var(--ink);stroke-width:1.2}}
.cloth{{fill:var(--cloth);stroke:var(--ink);stroke-width:1.2}} .clothline{{fill:none;stroke:var(--ink);stroke-width:.8;opacity:.4}}
.rod{{fill:var(--ink)}} .string{{stroke:var(--ink);stroke-width:1.4}}
.ring{{fill:none;stroke:var(--ink);stroke-width:3}}
.pot{{fill:var(--paper);stroke:var(--ink);stroke-width:1.2}}
.leaf{{fill:var(--leafc);stroke:var(--ink);stroke-width:1}}
.cup{{fill:var(--glass);stroke:var(--ink);stroke-width:1.2}} .cupin{{fill:none;stroke:var(--ink);stroke-width:.8;opacity:.4}}
.bulb{{fill:var(--bulb);stroke:var(--ink);stroke-width:1}}
a{{color:var(--cobalt)}}
a:focus-visible{{outline:2px solid var(--tomato);outline-offset:2px}}
</style>
<div class="wrap">
<section class="intro">
  <span class="eyebrow">OCT. 26 · Pattern Lab · 16 ต.ค. 2569</span>
  <h1>ห้าแพตเทิร์นใหม่ ที่ต่อกันได้ไม่จำกัด</h1>
  <p class="lead">ทุกแบบใช้กลไกเดียวกับ SOI. 02 ปีกสอดผ่านร่องแล้วกางล็อก ไม่ใช้กาว ไม่เย็บ เน้นของแต่งบ้าน แต่ละแบบมีของที่ทำได้จริงสองอย่าง</p>
  <ul class="rules">
    <li><b>ปีกกับร่องเท่ากัน</b>ทุกชิ้นมีจำนวนปีกเท่ากับร่อง ต่อกี่ชิ้นก็ไม่มีด้านเหลือ</li>
    <li><b>คอปีกเล็กกว่า slit 0.5 มม.</b>สอดผ่านได้ แต่ตัวปีกกว้างกว่า จึงกางล็อกด้านหลัง</li>
    <li><b>ต่อที่แนวพับ</b>มุมต่อได้ตั้งแต่แผ่นเรียบจนถึงกล่อง</li>
    <li><b>ข้อต่อสองขนาดมาตรฐาน</b>S64 ของเดิม และ S30 ใหม่สำหรับเศษชิ้นเล็ก</li>
    <li><b>เนื้อหนังรอบปลาย slit อย่างน้อย 8 มม.</b>ปีกจึงกว้างกว่า slit ข้างละ 8 มม. ขึ้นไป ทุกแบบในหน้านี้ผ่านเกณฑ์นี้ เท่ากับแม่พิมพ์ 01–06 ที่สั่งไปแล้ว</li>
  </ul>
  <p class="note">แบบแนวคิดใช้ตัวอักษร A–E ไม่ใช้เลข เพราะเลข 07 เป็นของแม่พิมพ์จริงแล้ว (ทรงกากบาทข้อต่อวงกลม 19 ต.ค.) นี่คือภาพแนวคิดจากเรขาคณิตจริง ยังไม่ใช่ไฟล์แม่พิมพ์ ทุกแบบต้องตัดต้นแบบ วัดความหนาหนัง และลองดึงก่อนสั่งทำบล็อก (ราว 550–600 บาทต่อแบบ ตามใบเสนอราคา 15 ต.ค.)</p>
</section>
{"".join(cards)}
<section class="next">
  <span class="eyebrow">ต่อกันข้ามแบบ</span><h2>ข้อต่อขนาดเดียวกัน ต่อกันได้ทุกแบบ</h2>
  <div class="cmpwrap">{compat}</div>
  <ol>
    <li>เริ่มที่ A รังผึ้ง กับ D สี่เหลี่ยมจิ๋ว ก่อน สองแบบนี้ใช้ข้อต่อ S30 ร่วมกัน ได้ของ 4 อย่างจากบล็อก 2 ตัว</li>
    <li>ตัดต้นแบบจากกระดาษแข็งหรือหนังเศษ ลอง slit 15 มม. กับหนังจริงว่าปีกล็อกแน่นพอ</li>
    <li>ถ้าผ่าน ทำเป็นคอลเลกชันแต่งบ้านหลังบูธ ชื่อคอลเลกชันคุยกันก่อน</li>
  </ol>
  <p class="note">ไฟล์ภาพแพตเทิร์น: <code>patternlab-20261016/svg/</code> · สร้างใหม่ด้วย <code>python3 patternlab-20261016/build.py</code></p>
</section>
</div>
"""

if __name__ == "__main__":
    D = build()
    for code, th, en, j, p, *_ in D:
        print(code, en, p["size"], tagline(p))
    open(os.path.join(HERE, "site", "index.html"), "w").write(page(D))
