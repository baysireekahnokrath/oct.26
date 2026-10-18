"""Catalog sheet for the 15 recommended die-01 products, drawn like a furniture catalog: isometric renders in three
leather colours with the price, then three outline steps that show how the bears join.

Every bear is the real die outline (../../diecut-leather-20261014/svg/01-bear-head.svg) placed on a plane in 3-D with
an affine SVG transform. Joints follow the die: right ear -> left cheek slit of the next bear, top ear -> chin slit of
the bear above, 71.4 mm apart. "ซ่อน" draws the ear behind the next bear, "โชว์" draws it on the next bear's face.

python3 catalog01/build.py -> catalog01/site/index.html and catalog01/svg/*.svg
"""
import html, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
E = html.escape
OUT = os.path.join(HERE, "site"); os.makedirs(OUT, exist_ok=True)
SVGD = os.path.join(HERE, "svg"); os.makedirs(SVGD, exist_ok=True)

s = open(os.path.join(ROOT, "..", "diecut-leather-20261014", "svg", "01-bear-head.svg")).read()
BEAR = re.search(r'<g id="CUT".*?<path d="([^"]+)"', s, re.S).group(1)
SLITS = [tuple(map(float, m)) for m in re.findall(r'x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"', s)]
NECK_X, NECK_Y, SLIT_X, SLIT_Y, P = 82.59, 21.77, 11.2, 93.16, 71.39   # ear necks, slits, pitch (mm)
CX, CY, R = 41.685, 62.675, 41.69                                       # head circle
C30, S30 = math.cos(math.radians(30)), 0.5

KX, KY = 0.32, 0.62                        # oblique depth: front faces keep their true shape, the table top reads from above

def iso(p):
    """x right, y towards the viewer, z up -> screen. Things nearer the viewer move down and slightly left."""
    x, y, z = p
    return (x - y * KX, -z + y * KY)

def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k, a[2] + b[2] * k)

_UID = [0]

class Scene:
    def __init__(self):
        self.el, self.pts = [], []
    def track(self, *pts3):
        self.pts += [iso(p) for p in pts3]
    def plane(self, O, U, V):
        """Affine matrix that maps die mm (u, v) onto the plane O + u*U + v*V, then to the screen."""
        o, u, v = iso(O), iso(U), iso(V)
        return f"matrix({u[0]:.4f},{u[1]:.4f},{v[0]:.4f},{v[1]:.4f},{o[0]:.2f},{o[1]:.2f})"
    def bear(self, O, U, V, fill, cut_right=False, cut_top=False, only_ear=None, text=None, thick=True, slits=True):
        m = self.plane(O, U, V)
        _UID[0] += 1; cid = f"k{_UID[0]}"
        x1 = NECK_X if cut_right else 110
        y0 = NECK_Y if cut_top else -5
        if only_ear == "right":
            clip = f'<clipPath id="{cid}"><rect x="{NECK_X}" y="-5" width="40" height="120"/></clipPath>'
        elif only_ear == "top":
            clip = f'<clipPath id="{cid}"><rect x="-5" y="-5" width="120" height="{NECK_Y + 5}"/></clipPath>'
        else:
            clip = f'<clipPath id="{cid}"><rect x="-5" y="{y0}" width="{x1 + 5}" height="{115 - y0}"/></clipPath>'
        sl = "" if only_ear or not slits else "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" class="sl"/>' for a, b, c, d in SLITS)
        tx = (f'<text x="{CX}" y="{CY + 7}" class="stamp" text-anchor="middle">{E(text)}</text>' if text and not only_ear else "")
        edge = ""
        if thick and not only_ear:
            edge = f'<path d="{BEAR}" class="edge" transform="translate(0,2.2)" clip-path="url(#{cid})"/>'
        self.el.append(f'<g transform="{m}"><defs>{clip}</defs>{edge}<path d="{BEAR}" class="b" style="fill:{fill}" clip-path="url(#{cid})"/>{sl}{tx}</g>')
        for u, v in ((0, 0), (104.4, 0), (0, 104.4), (104.4, 104.4)):
            self.track(add(add(O, U, u), V, v))
    def raw(self, svg, *pts2):
        self.el.append(svg); self.pts += list(pts2)
    def line3(self, pts3, cls="aux"):
        q = [iso(p) for p in pts3]; self.pts += q
        self.el.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in q)}" class="{cls}"/>')
    def poly3(self, pts3, cls="aux"):
        q = [iso(p) for p in pts3]; self.pts += q
        self.el.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in q)}" class="{cls}"/>')
    def arrow3(self, a3, b3, bend=12):
        a, b = iso(a3), iso(b3); self.pts += [a, b]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = -(b[1] - a[1]), b[0] - a[0]; L = math.hypot(nx, ny) or 1
        self.el.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} Q{mx + nx / L * bend:.1f},{my + ny / L * bend:.1f} {b[0]:.1f},{b[1]:.1f}" class="arr" marker-end="url(#ah)"/>')
    def svg(self, label, pad=10):
        xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]
        x0, y0, x1, y1 = min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad
        return (f'<svg viewBox="{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{E(label)}">'
                f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" class="ahh"/></marker></defs>{"".join(self.el)}</svg>')

# planes
WALL_U, WALL_V = (1, 0, 0), (0, 0, -1)          # front wall: die x -> right, die y -> down
FLOOR_U, FLOOR_V = (1, 0, 0), (0, 1, 0)         # on the table: die y -> towards the viewer
OUTLINE = "var(--paper)"

def row(sc, n, O, U, V, fills, look="ซ่อน", gap=0.0, text=None, joined=True):
    """n bears in a row along U. joined=False lays them apart (gap in mm)."""
    pitch = P if joined else 104.4 + gap
    order = range(n - 1, -1, -1) if look == "ซ่อน" else range(n)
    for i in order:
        o = add(O, U, i * pitch)
        sc.bear(o, U, V, fills[i % len(fills)], cut_right=joined and i < n - 1, text=(text[i] if text and i < len(text) else None))
    if joined and look == "โชว์":
        for i in range(n - 1):
            sc.bear(add(O, U, i * pitch), U, V, fills[i % len(fills)], only_ear="right")

def grid(sc, cols, rows_, O, U, V, fills, look="ซ่อน", fill_at=None):
    """cols x rows on a plane; row 0 is the top (furthest) row. fill_at(c, r) picks a colour."""
    f = fill_at or (lambda c, r: fills[(c + r) % len(fills)])
    rs = range(rows_) if look == "ซ่อน" else range(rows_ - 1, -1, -1)
    cs = (lambda: range(cols - 1, -1, -1)) if look == "ซ่อน" else (lambda: range(cols))
    for r in rs:
        for c in cs():
            o = add(add(O, U, c * P), V, r * P)
            sc.bear(o, U, V, f(c, r), cut_right=c < cols - 1, cut_top=r > 0)
    if look == "โชว์":
        for r in range(rows_):
            for c in range(cols):
                o = add(add(O, U, c * P), V, r * P)
                if c < cols - 1: sc.bear(o, U, V, f(c, r), only_ear="right")
                if r > 0: sc.bear(o, U, V, f(c, r), only_ear="top")

def ring(sc, n, fills, look="ซ่อน", z0=0.0, rows_=1, center=(0, 0), ears_up=True):
    """n bears per course round a regular polygon of side P, standing on the table. Back faces first."""
    Rr = P / (2 * math.sin(math.pi / n))
    verts = [(center[0] + Rr * math.cos(2 * math.pi * k / n + math.pi / n), center[1] + Rr * math.sin(2 * math.pi * k / n + math.pi / n)) for k in range(n)]
    faces = []
    for k in range(n):
        a, b = verts[k], verts[(k + 1) % n]
        U = ((b[0] - a[0]) / P, (b[1] - a[1]) / P, 0)
        depth = (a[1] + b[1]) / 2                         # larger = nearer the viewer
        faces.append((depth, k, a, U))
    faces.sort()
    H = 104.4 - NECK_Y
    for depth, k, a, U in faces:
        for r in range(rows_):
            top_z = z0 + (rows_ - r) * P + (NECK_Y if not ears_up else 0) + 20
            O = (a[0] - U[0] * SLIT_X, a[1] - U[1] * SLIT_X, z0 + H + (rows_ - 1 - r) * P + NECK_Y)
            sc.bear(O, U, WALL_V, fills[(k + r) % len(fills)], cut_right=True, cut_top=r > 0)
            if look == "โชว์":
                sc.bear(O, U, WALL_V, fills[(k + r) % len(fills)], only_ear="right")
    return verts

# ---------------------------------------------------------------- props (outline style, drawn in 3-D)
def keyring(sc, at, r=9):
    pts = [add(at, (math.cos(t) * r, 0, math.sin(t) * r)) for t in [i / 24 * 2 * math.pi for i in range(25)]]
    sc.line3(pts, "metal")

def clasp(sc, at):
    keyring(sc, at, 6)
    x, y, z = at
    sc.line3([(x, y, z + 6), (x, y, z + 14), (x - 4, y, z + 22), (x, y, z + 32), (x + 4, y, z + 22), (x, y, z + 14)], "metal")

def cord(sc, pts3):
    sc.line3(pts3, "cord")

def jar(sc, r, h, center=(0, 0)):
    cx, cy = center
    ring_ = lambda z: [(cx + r * math.cos(t), cy + r * math.sin(t), z) for t in [i / 36 * 2 * math.pi for i in range(37)]]
    sc.line3(ring_(h), "aux"); sc.line3(ring_(0), "aux faint")
    for t in (math.radians(135), math.radians(-45)):
        sc.line3([(cx + r * math.cos(t), cy + r * math.sin(t), 0), (cx + r * math.cos(t), cy + r * math.sin(t), h)], "aux faint")

def pens(sc, center, top):
    cx, cy = center
    for i, (dx, dy, hh) in enumerate([(-10, 4, 60), (6, -8, 75), (12, 10, 50), (-4, -12, 68)]):
        sc.line3([(cx + dx, cy + dy, top - 30), (cx + dx * 1.3, cy + dy * 1.3, top + hh)], "pen")

def pot(sc, center, r=46, h=40):
    cx, cy = center
    sc.raw("", )
    jar(sc, r, h, center)

# ---------------------------------------------------------------- the 15 products
TAN, CHESTNUT, BLACK = "#C68A4E", "#7B4A2B", "#2B2A2E"
COLOURS = [("น้ำตาลอ่อน", TAN), ("น้ำตาลเข้ม", CHESTNUT), ("ดำ", BLACK)]
FAMILY = ["#2449D8", "#FF5A36", "#FFC23C", "#2EC4A0", "#FF8AC4"]

def solo_charm(fills, text=None, hw="ring"):
    sc = Scene()
    sc.bear((0, 0, 104.4), WALL_U, WALL_V, fills[0], text=text)
    at = (SLIT_X - 2, 0, 104.4 - 62)
    if hw == "ring": keyring(sc, (CX, 0, 104.4 + 8), 10)
    else: clasp(sc, (CX, 0, 104.4 + 4))
    return sc

def p_keychain(f, step=None):
    sc = Scene()
    if step == 1:
        sc.bear((0, 0, 0), FLOOR_U, FLOOR_V, f[0], text="B"); return sc
    if step == 2:
        sc.bear((0, 0, 104.4), WALL_U, WALL_V, f[0], text="B")
        keyring(sc, (CX, -1, 104.4 - SLIT_Y - 6), 10)
        sc.arrow3((CX + 40, 0, -10), (CX + 10, 0, 104.4 - SLIT_Y - 4)); return sc
    sc.bear((0, 0, 104.4), WALL_U, WALL_V, f[0], text="B")
    keyring(sc, (CX, -1, 104.4 - SLIT_Y - 6), 10)
    sc.line3([(CX, -1, 104.4 - SLIT_Y - 16), (CX + 3, -1, -40)], "metal")
    return sc

def p_namecharm(f, step=None):
    sc = Scene()
    if step == 1:
        sc.bear((0, 0, 0), FLOOR_U, FLOOR_V, f[0], text="BENE"); return sc
    sc.bear((0, 0, 104.4), WALL_U, WALL_V, f[0], text="BENE")
    if step == 2:
        sc.arrow3((-40, 0, 140), (SLIT_X, 0, 104.4 - 62)); clasp(sc, (-40, 0, 150)); return sc
    clasp(sc, (SLIT_X - 4, -1, 104.4 - 55))
    return sc

def p_hug(f, step=None, text=None):
    sc = Scene()
    if step == 1:
        row(sc, 2, (0, 0, 104.4), WALL_U, WALL_V, f, joined=False, gap=20, text=text); return sc
    if step == 2:
        row(sc, 2, (0, 0, 104.4), WALL_U, WALL_V, f, joined=False, gap=20, text=text)
        sc.arrow3((NECK_X + 14, 0, 104.4 - 62), (104.4 + 20 + SLIT_X, 0, 104.4 - 66), 18); return sc
    row(sc, 2, (0, 0, 104.4), WALL_U, WALL_V, f, look="โชว์", text=text)
    keyring(sc, (CX, -1, 104.4 - SLIT_Y - 6), 9)
    return sc

def p_idcard(f, step=None):
    sc = Scene()
    sc.bear((0, 0, 104.4), WALL_U, WALL_V, f[0], text="BEIYA")
    if step == 1:
        return sc
    top = (CX, 0, 104.4 + 120)
    if step == 2:
        cord(sc, [(SLIT_X, -1, 104.4 - 62), (SLIT_X - 10, -1, 104.4 + 20), (CX - 30, 0, 104.4 + 90)])
        sc.arrow3((SLIT_X - 30, 0, 104.4 - 40), (SLIT_X, 0, 104.4 - 60)); return sc
    cord(sc, [(SLIT_X, -1, 104.4 - 62), (SLIT_X - 14, -1, 104.4 + 10), (CX - 18, -1, 104.4 + 110), (CX + 18, -1, 104.4 + 110), (CX + 2, -1, 104.4 - SLIT_Y + 6)])
    return sc

def p_cable(f, step=None):
    sc = Scene()
    n = 1 if step in (1, 2) else 3
    for i in range(n):
        O = (i * 125, 0, 0)
        sc.bear(O, FLOOR_U, FLOOR_V, f[i % len(f)])
        if step != 1:
            for k in range(3):
                rr = 48 + k * 2.5
                sc.line3([add(O, (CX + rr * math.cos(t), CY + rr * 0.42 * math.sin(t), 2 + k * 0.6)) for t in [j / 30 * 2 * math.pi for j in range(31)]], "cable")
    if step == 2:
        sc.arrow3((SLIT_X - 34, 62, 10), (SLIT_X, 62, 2))
    return sc

def p_penjar(f, step=None):
    sc = Scene()
    if step == 1:
        row(sc, 4, (0, 0, 0), FLOOR_U, FLOOR_V, f, look="ซ่อน"); return sc
    if step == 2:
        row(sc, 4, (0, 0, 0), FLOOR_U, FLOOR_V, f, look="ซ่อน")
        sc.arrow3((3 * P + 90, 40, 0), (3 * P + 40, 40, 70), -20); sc.arrow3((-10, 40, 0), (30, 40, 70), 20); return sc
    jar(sc, 32, 98)
    ring(sc, 4, f, look="ซ่อน")
    pens(sc, (0, 0), 100)
    return sc

def p_coasters(f, step=None):
    sc = Scene()
    fam = f if len(f) >= 5 else [f[0]] * 5
    if step == 1:
        for i in range(5):
            sc.bear((i * 60, i * 18, 0), FLOOR_U, FLOOR_V, fam[i])
        return sc
    for i in range(5):
        sc.bear((0, 0, i * 3), FLOOR_U, FLOOR_V, fam[i])
    if step == 2:
        sc.line3([(CX - 50, CY, 2), (CX, CY, 18), (CX + 50, CY, 2)], "cord"); return sc
    jar(sc, 30, 70, (CX + 150, CY))
    sc.bear((110, 0, 0), FLOOR_U, FLOOR_V, fam[0])
    return sc

def p_trivet(f, step=None):
    sc = Scene()
    if step == 1:
        row(sc, 2, (0, 0, 0), FLOOR_U, FLOOR_V, f, look="ซ่อน", joined=False, gap=24)
        sc.arrow3((NECK_X + 10, CY - 10, 4), (104.4 + 24 + SLIT_X, CY, 2)); return sc
    if step == 2:
        row(sc, 2, (0, P, 0), FLOOR_U, FLOOR_V, f[1:] + f[:1])
        row(sc, 2, (0, -40, 0), FLOOR_U, FLOOR_V, f)
        sc.arrow3((CX, P + NECK_Y - 2, 2), (CX, -40 + SLIT_Y, 2), 10); return sc
    grid(sc, 2, 2, (0, 0, 0), FLOOR_U, FLOOR_V, f, look="ซ่อน")
    jar(sc, 52, 50, (P / 2 + CX, P / 2 + CY))
    return sc

def p_garland(f, step=None, n=5, text=None, look="ซ่อน"):
    sc = Scene()
    fills = FAMILY if f is None else f
    if step == 1:
        row(sc, n, (0, 0, 104.4), WALL_U, WALL_V, fills, joined=False, gap=14, text=text); return sc
    if step == 2:
        row(sc, 2, (0, 0, 104.4), WALL_U, WALL_V, fills, joined=False, gap=14, text=text)
        sc.arrow3((NECK_X + 10, 0, 104.4 - 62), (104.4 + 14 + SLIT_X, 0, 104.4 - 64), 16); return sc
    row(sc, n, (0, 0, 104.4), WALL_U, WALL_V, fills, look=look, text=text)
    L = (n - 1) * P
    cord(sc, [(CX, -1, 104.4 - NECK_Y + 6), (L / 2 + CX, -1, 104.4 + 50), (L + CX, -1, 104.4 - NECK_Y + 6)])
    return sc

def p_wall(f, step=None):
    sc = Scene()
    fam = lambda c, r: FAMILY[(c + r) % 5]
    if step == 1:
        row(sc, 5, (0, 0, 104.4), WALL_U, WALL_V, [FAMILY[i] for i in range(5)]); return sc
    if step == 2:
        grid(sc, 5, 2, (0, 0, 104.4 + P), WALL_U, WALL_V, None, fill_at=fam)
        sc.arrow3((2 * P + CX, 0, -60), (2 * P + CX, 0, 0), 0); return sc
    grid(sc, 5, 5, (0, 0, 104.4 + 4 * P), WALL_U, WALL_V, None, fill_at=fam)
    zt = 104.4 + 4 * P + 30
    sc.line3([(-20, -6, zt), (4 * P + 124, -6, zt)], "rod")
    sc.line3([(-10, -6, zt), (2 * P + CX, -6, zt + 60), (4 * P + 114, -6, zt)], "cord")
    return sc

def p_crown(f, step=None):
    sc = Scene()
    fills = f
    if step == 1:
        row(sc, 8, (0, 0, 0), FLOOR_U, FLOOR_V, fills, look="โชว์"); return sc
    if step == 2:
        row(sc, 8, (0, 0, 0), FLOOR_U, FLOOR_V, fills, look="โชว์")
        sc.arrow3((7 * P + 90, 60, 0), (7 * P + 30, 60, 90), -30); sc.arrow3((-20, 60, 0), (40, 60, 90), 30); return sc
    ring(sc, 8, fills, look="โชว์")
    return sc

def p_kit(f, step=None):
    sc = Scene()
    fam = FAMILY
    if step == 1:
        import random
        rnd = random.Random(7)
        for i in range(12):
            sc.bear((rnd.uniform(0, 320), rnd.uniform(0, 200), i * 0.5), FLOOR_U, FLOOR_V, fam[i % 5])
        return sc
    if step == 2:
        grid(sc, 2, 2, (0, 0, 0), FLOOR_U, FLOOR_V, fam, look="โชว์")
        return sc
    grid(sc, 2, 2, (0, 0, 0), FLOOR_U, FLOOR_V, fam, look="โชว์")
    row(sc, 3, (0, 260, 0), FLOOR_U, FLOOR_V, fam[2:], look="โชว์")
    return sc

def p_ornament(f, step=None):
    sc = Scene()
    sc.bear((0, 0, 104.4), WALL_U, WALL_V, f[0], text="2026")
    if step == 1:
        return sc
    if step == 2:
        cord(sc, [(SLIT_X, -1, 104.4 - 54), (SLIT_X - 20, -1, 104.4 + 10), (SLIT_X + 10, -1, 104.4 + 40)])
        sc.arrow3((SLIT_X - 40, 0, 104.4 - 70), (SLIT_X, 0, 104.4 - 60)); return sc
    cord(sc, [(SLIT_X, -1, 104.4 - 54), (SLIT_X - 4, -1, 104.4 + 60), (SLIT_X + 18, -1, 104.4 - 54)])
    sc.line3([(SLIT_X - 4, -1, 104.4 + 60), (SLIT_X - 60, -1, 104.4 + 64)], "branch")
    return sc

PRODUCTS = [
 # (code, name, spec, price, look, colours mode, draw fn, steps captions)
 ("LV-K1", "พวงกุญแจหมีปั๊มอักษรย่อ", "หมี 1 ตัว · 10.4 × 10.4 ซม. · ห่วงโลหะ", 99, "—", "leather", p_keychain,
  ["ปั๊มอักษรย่อกลางหน้าหมี", "สอดห่วงโลหะเข้าร่องคาง", "คล้องกุญแจ"]),
 ("LV-K2", "ที่ห้อยกระเป๋าหมีปั๊มชื่อ", "หมี 1 ตัว · 10.4 × 10.4 ซม. · ห่วงก้ามปู", 129, "—", "leather", p_namecharm,
  ["ปั๊มชื่อ", "เกี่ยวห่วงก้ามปูที่ร่องแก้ม", "ห้อยกับกระเป๋า"]),
 ("LV-K3", "ห้อยกระเป๋าหมีกอด 2 ตัว", "หมี 2 ตัว · กว้าง 17.6 ซม. · โชว์ปลาย · ห่วงโลหะ", 199, "โชว์", "pair", p_hug,
  ["วางหมีสองตัวคู่กัน", "สอดหูขวาจากด้านหลัง ออกร่องแก้มตัวที่สอง", "หูโผล่บนแก้มเหมือนกอด คล้องห่วง"]),
 ("LV-K4", "บัตรห้อยคอเด็ก", "หมี 1 ตัว · ชื่อหน้า เบอร์พ่อแม่หลัง · สายคล้องคอแบบหลุดได้", 199, "—", "leather", p_idcard,
  ["ปั๊มชื่อหน้า เขียนเบอร์ด้านหลัง", "ร้อยสายเข้าร่องแก้ม", "ร้อยปลายอีกข้างเข้าร่องคาง แล้วคล้องคอ"]),
 ("LV-H1", "ชุดเก็บสาย 3 ตัว", "หมี 3 ตัว · สายชาร์จ หูฟัง นาฬิกา", 149, "—", "leather3", p_cable,
  ["วางหมีบนโต๊ะ", "พันสายรอบหัว เหน็บปลายเข้าร่อง", "ครบชุดสามตัว"]),
 ("LV-H2", "ปลอกโหลใส่ปากกา", "หมี 4 ตัว · วง 4 · ในกว้าง 7 ซม. · ซ่อนปลาย · โหลแก้ว", 390, "ซ่อน", "leather", p_penjar,
  ["ต่อหมี 4 ตัวเป็นแถว ซ่อนปลาย", "ม้วนเป็นวง ต่อตัวสุดท้ายเข้าตัวแรก", "สวมโหลแก้ว ใส่ปากกา"]),
 ("LV-T1", "ชุดที่รองแก้วห้าสีครอบครัว", "หมี 5 ตัว · สีละตัว · เชือกมัด", 249, "—", "family", p_coasters,
  ["ห้าสี ห้าคนในบ้าน", "ซ้อนกัน มัดเชือก", "แก้วใครแก้วมัน"]),
 ("LV-T2", "ที่รองหม้อร้อน 2 × 2", "หมี 4 ตัว · 17.6 × 17.6 ซม. · ซ่อนปลาย", 199, "ซ่อน", "leather", p_trivet,
  ["ต่อหูขวาเข้าร่องแก้มตัวข้าง", "ต่อแถวที่สอง หูบนเข้าร่องคาง", "วางหม้อได้เลย"]),
 ("LV-D1", "ราวหมีห้าตัว", "หมี 5 ตัว · ยาว 39 ซม. · ซ่อนหรือโชว์ปลาย · เชือก", 349, "เลือกได้", "family", lambda f, step=None: p_garland(f, step),
  ["วางหมีห้าตัวเรียงกัน", "สอดหูขวาเข้าร่องแก้มตัวถัดไป", "ผูกเชือกแล้วแขวน"]),
 ("LV-D2", "ราวชื่อหมี", "ตัวอักษรละ 1 ตัว · 6 ตัว ยาว 46 ซม. · โชว์ปลาย", 390, "โชว์", "leather", lambda f, step=None: p_garland(f, step, 6, "BEANA♥", "โชว์"),
  ["ปั๊มตัวอักษรตัวละหนึ่งตัว", "สอดหูจากด้านหลัง โผล่บนแก้มตัวถัดไป", "ผูกเชือกแขวนหัวเตียง"]),
 ("LV-D3", "ผ้าแขวนผนังครอบครัว 5 × 5", "หมี 25 ตัว · 39 × 39 ซม. · ไล่ห้าสี · ไม้แขวน", 1290, "เลือกได้", "fixed", p_wall,
  ["ต่อแถวแรกห้าตัว", "ต่อแถวถัดไป หูบนเข้าร่องคาง", "ครบห้าแถว แขวนกับไม้"]),
 ("LV-F1", "มงกุฎวันเกิดหมี", "หมี 8 ตัว · รอบหัว 57 ซม. (เด็กใช้ 7 ตัว) · โชว์ปลาย", 590, "โชว์", "leather", p_crown,
  ["ต่อหมี 8 ตัวเป็นแถว โชว์ปลาย", "ม้วนเป็นวง ต่อตัวสุดท้ายเข้าตัวแรก", "หูบนชี้ขึ้นเป็นยอดมงกุฎ"]),
 ("LV-F2", "ชุดตัวต่อหมี 20 ตัว", "หมี 20 ตัว · ห้าสี · ต่อเป็นแถว ตาราง วง", 590, "เลือกได้", "fixed", p_kit,
  ["เทหมีออกจากถุง", "ต่อเป็นตาราง 2 × 2", "ต่อแถว ตาราง และวง ได้เอง"]),
 ("LV-S1", "ของแขวนต้นคริสต์มาสหมี", "หมี 1 ตัว · ปั๊มปี · ริบบิ้น", 79, "—", "leather", p_ornament,
  ["ปั๊มปีหรือชื่อ", "ร้อยริบบิ้นเข้าร่องแก้ม", "ผูกเป็นห่วง แขวนกับกิ่ง"]),
 ("LV-W1", "ของชำร่วยหมีคู่ปั๊มชื่อบ่าวสาว", "หมี 2 ตัว · โชว์ปลาย · ห่วงโลหะ · สั่ง 100 ชิ้นขึ้นไป", 89, "โชว์", "pair", lambda f, step=None: p_hug(f, step, ["A", "B"]),
  ["ปั๊มอักษรบ่าวสาว ตัวละคน", "สอดหูจากด้านหลัง โผล่บนแก้มอีกตัว", "คล้องห่วง ใส่ซองพร้อมการ์ด"]),
]

def variants(mode):
    if mode == "leather": return [(n, [c]) for n, c in COLOURS]
    if mode == "leather3": return [(n, [c, c, c]) for n, c in COLOURS]
    if mode == "pair": return [("น้ำตาลอ่อน + น้ำตาลเข้ม", [TAN, CHESTNUT]), ("น้ำตาลเข้ม + ดำ", [CHESTNUT, BLACK]), ("ดำ + น้ำตาลอ่อน", [BLACK, TAN])]
    if mode == "family": return [("ห้าสีครอบครัว", FAMILY), ("น้ำตาลอ่อน", [TAN]), ("น้ำตาลเข้ม", [CHESTNUT])]
    return [("ห้าสีครอบครัว", FAMILY)]

def build():
    cards = []
    for code, name, spec, price, look, mode, fn, caps in PRODUCTS:
        vs = []
        for i, (vn, fills) in enumerate(variants(mode)):
            svg = fn(fills).svg(f"{name} สี{vn}")
            if i == 0:
                open(os.path.join(SVGD, f"{code}.svg"), "w").write(svg.replace("<svg ", "<svg style=\"--paper:#fff;--ink:#1C1B22\" ", 1).replace("</svg>", f"<style>{SVG_CSS}</style></svg>"))
            vs.append(f'<figure class="v"><div class="pic">{svg}</div><figcaption><span class="cn">{E(vn)}</span>'
                      f'<span class="pr">{price:,}.-</span></figcaption></figure>')
        steps = []
        for k in (1, 2, 3):
            svg = fn([OUTLINE, OUTLINE, OUTLINE, OUTLINE, OUTLINE], step=k).svg(f"{name} ขั้นที่ {k}")
            steps.append(f'<figure class="st"><div class="pic out">{svg}</div><figcaption><b>{k}</b> {E(caps[k - 1])}</figcaption></figure>')
        lk = f'<span class="lk">{E(look)}ปลาย</span>' if look in ("ซ่อน", "โชว์") else (f'<span class="lk">ซ่อนหรือโชว์ปลาย</span>' if look == "เลือกได้" else "")
        cards.append(f"""<article class="prod" id="{code}">
<header><h2>{E(name)}</h2><p class="spec"><span class="code">{code}</span> · {E(spec)} {lk}</p></header>
<div class="vs">{''.join(vs)}</div>
<p class="how">วิธีต่อ</p>
<div class="sts">{''.join(steps)}</div>
</article>""")
    page = HEAD + "".join(cards) + FOOT
    open(os.path.join(OUT, "index.html"), "w").write(page)
    print("products", len(PRODUCTS))

SVG_CSS = """.b{stroke:var(--ink);stroke-width:.55;stroke-linejoin:round}.edge{fill:var(--ink);opacity:.35}
.sl{stroke:var(--ink);stroke-width:.8}.stamp{font:600 15px Jost,'IBM Plex Sans Thai',sans-serif;fill:var(--ink);opacity:.55;letter-spacing:.5px}
.aux{fill:none;stroke:var(--ink);stroke-width:.9}.aux.faint{opacity:.35}.metal{fill:none;stroke:var(--ink);stroke-width:1.8}
.cord{fill:none;stroke:var(--ink);stroke-width:1.4}.cable{fill:none;stroke:var(--ink);stroke-width:1.6}.pen{stroke:var(--ink);stroke-width:3;stroke-linecap:round}
.rod{stroke:var(--ink);stroke-width:5;stroke-linecap:round}.branch{stroke:var(--ink);stroke-width:4;stroke-linecap:round}
.arr{fill:none;stroke:var(--accent,#2449D8);stroke-width:1.6}.ahh{fill:var(--accent,#2449D8)}"""

HEAD = f"""<title>FIVE BEARS Catalog 01</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500&family=Mitr:wght@400;500&family=IBM+Plex+Sans+Thai:wght@400;600&display=swap">
<style>
/* layout: a furniture-catalog sheet, one product per band: name and spec, three colourways with price, three outline steps */
:root{{
  --paper:#FFFFFF; --ink:#1C1B22; --muted:#6B6670; --rule:#C9C4BC; --accent:#2449D8; --tag:#FF8AC4;
  --display:'Mitr','IBM Plex Sans Thai',sans-serif; --body:'IBM Plex Sans Thai',sans-serif; --latin:'Jost','IBM Plex Sans Thai',sans-serif;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--paper:#141318;--ink:#F2EDE6;--muted:#ADA7A0;--rule:#3A3740;--accent:#8FA6FF;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#141318;--ink:#F2EDE6;--muted:#ADA7A0;--rule:#3A3740;--accent:#8FA6FF;color-scheme:dark}}
body{{background:var(--paper);color:var(--ink);font:400 15px/1.6 var(--body)}}
.wrap{{max-width:960px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:34px 89px}}
.top{{display:flex;justify-content:space-between;align-items:flex-start;gap:13px;padding-bottom:21px;border-bottom:1.5px solid var(--ink)}}
h1{{font:400 clamp(30px,7vw,52px)/1.05 var(--latin);letter-spacing:.06em;margin:0}}
h1 small{{display:block;font:400 15px/1.6 var(--body);letter-spacing:0;color:var(--muted);margin-top:8px}}
.badge{{flex:none;width:92px;height:92px;border-radius:50%;background:var(--tag);color:#1C1B22;display:grid;place-items:center;text-align:center;font:500 13px/1.25 var(--display)}}
.prod{{padding:34px 0;border-bottom:1.5px dashed var(--rule);display:flex;flex-direction:column;gap:13px}}
.prod header h2{{font:500 26px/1.25 var(--display);margin:0;text-wrap:balance}}
.spec{{margin:4px 0 0;font-size:13.5px;color:var(--muted)}}
.code{{font-family:var(--latin);letter-spacing:.06em;color:var(--ink)}}
.lk{{display:inline-block;margin-left:6px;font-size:12px;border:1px solid var(--ink);border-radius:999px;padding:0 8px;color:var(--ink)}}
.vs,.sts{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:13px}}
@media (max-width:560px){{.vs{{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}} .sts{{grid-template-columns:1fr}}}}
figure{{margin:0;display:flex;flex-direction:column;gap:6px;min-width:0}}
.pic{{aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;max-width:100%}}
.pic svg{{width:100%;height:100%}}
.v figcaption{{display:flex;flex-direction:column}}
.cn{{font-size:12.5px;color:var(--muted);line-height:1.35}}
.pr{{font:400 22px/1.2 var(--latin);color:var(--accent);font-variant-numeric:tabular-nums}}
.how{{margin:8px 0 0;font:500 12.6px var(--latin);letter-spacing:.14em;color:var(--muted)}}
.st .pic{{border:1px solid var(--rule);border-radius:4px;padding:8px}}
.st figcaption{{font-size:14px}} .st figcaption b{{font-family:var(--latin);font-weight:500;color:var(--accent);margin-right:4px}}
.foot{{padding-top:34px;display:flex;flex-direction:column;gap:8px;font-size:14px;color:var(--muted);max-width:70ch}}
{SVG_CSS}
</style>
<div class="wrap">
<div class="top"><h1>FIVE BEARS<small>ห้าหมี by OCT. 26 · 15 สินค้าจากแม่พิมพ์หัวหมี 01 · ราคาเสนอ ยังไม่ยืนยัน</small></h1><div class="badge">ต่อเอง<br>ไม่ใช้กาว</div></div>
"""
FOOT = """<div class="foot">
<p>ภาพทุกชิ้นวาดจากเส้นแม่พิมพ์หัวหมีจริง ระยะต่อ 71.4 มม. ทั้งแนวนอนและแนวตั้ง สีหนังจริงขึ้นกับเศษที่ได้มาแต่ละล็อต สีครอบครัวห้าสีใช้เมื่อหาเศษสีนั้นได้</p>
<p>ซ่อนปลาย: สอดหูจากหน้าไปหลัง หูหายไปหลังตัวถัดไป · โชว์ปลาย: สอดหูจากหลังมาหน้า หูโผล่บนแก้มตัวถัดไป</p>
<p>ต่อหมีจริง 2 × 2 ตัวก่อนสั่งผลิต เพื่อยืนยันระยะต่อและหน้าตาทั้งสองแบบ ของที่แขวนหรือถูกดึงใช้หนังหนา 2 มม. ขึ้นไป</p>
</div></div>
"""

if __name__ == "__main__":
    build()
