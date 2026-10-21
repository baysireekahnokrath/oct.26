"""Place die pieces in 3D by their real joints, and check that the result can exist.

A product is a list of pieces and a tree of joints. Each joint puts a child on a parent:
  ("T", child, tab, parent, slit, flip, side)    child's tab neck goes through the parent's slit, child stands at 90 degrees
  ("S", child, slit, parent, tab, flip, side)    the reverse: the child's slit takes the parent's tab
  ("X", child, half, parent, half, flip, side)   two open slots (02 pinwheel) slide into each other, crossing at 90 degrees
flip turns the child over (which face looks which way), side picks which side of the parent the wing or the child goes to.
`close` lists extra joints between pieces already placed (rings): they must line up within 0.6 mm.

check() rules
  1. a tab only goes into a slit 0 to 1.0 mm longer than its neck (snug, not torn)
  2. every slit, tab and half slot is used at most once
  3. two pieces may only share a line where at least one of them is cut there (slit or slot); anything else is a collision
  4. parallel pieces closer than 1.5 mm must not overlap (leather is about 2 mm thick)
"""
import math
from geom import PIECES

def add(a, b): return [a[i] + b[i] for i in range(3)]
def sub(a, b): return [a[i] - b[i] for i in range(3)]
def mul(a, k): return [x * k for x in a]
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def norm(a): return math.sqrt(dot(a, a))
def unit(a): n = norm(a); return [x / n for x in a]
def mat(cols): return [[cols[j][i] for j in range(3)] for i in range(3)]        # columns -> rows
def mv(M, v): return [sum(M[i][j] * v[j] for j in range(3)) for i in range(3)]
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def tr(M): return [[M[j][i] for j in range(3)] for i in range(3)]

class Placed:
    def __init__(self, code, R, t):
        self.code, self.R, self.t = code, R, t
        self.g = PIECES[code]
    def w(self, p):                     # local 2D -> world
        return add(mv(self.R, [p[0], p[1], 0.0]), self.t)
    def loc(self, q):                   # world -> local (x, y, z)
        return mv(tr(self.R), sub(q, self.t))
    @property
    def n(self): return [self.R[0][2], self.R[1][2], self.R[2][2]]

def _frame(d, w):
    d3, w3 = [d[0], d[1], 0.0], [w[0], w[1], 0.0]
    return mat([d3, w3, cross(d3, w3)])

def attach(kind, parent, pfeat, child_code, cfeat, flip, side):
    P = parent.g["feats"][pfeat]; C = PIECES[child_code]["feats"][cfeat]
    nA = parent.n
    if kind == "T":
        assert P["kind"] == "slit" and C["kind"] == "tab", (pfeat, cfeat)
        pa, pb = parent.w(P["a"]), parent.w(P["b"]); mA = mul(add(pa, pb), .5); dA = unit(sub(pb, pa))
        dB = unit([C["b"][0] - C["a"][0], C["b"][1] - C["a"][1], 0]); mB = [(C["a"][0] + C["b"][0]) / 2, (C["a"][1] + C["b"][1]) / 2, 0]
        E = _frame(dB[:2], C["wing"])
        f1 = mul(dA, flip); f2 = mul(nA, side); F = mat([f1, f2, cross(f1, f2)])
        R = mm(F, tr(E)); t = sub(mA, mv(R, mB))
    elif kind == "S":
        assert P["kind"] == "tab" and C["kind"] == "slit", (pfeat, cfeat)
        pa, pb = parent.w(P["a"]), parent.w(P["b"]); mT = mul(add(pa, pb), .5); dT = unit(sub(pb, pa))
        wT = unit(sub(parent.w(P["wing"]), parent.w((0, 0))))
        dS = unit([C["b"][0] - C["a"][0], C["b"][1] - C["a"][1], 0]); mS = [(C["a"][0] + C["b"][0]) / 2, (C["a"][1] + C["b"][1]) / 2, 0]
        e1, e3 = dS, [0.0, 0.0, 1.0]; E = mat([e1, cross(e3, e1), e3])
        f1 = mul(dT, flip); f3 = mul(wT, side); F = mat([f1, cross(f3, f1), f3])
        R = mm(F, tr(E)); t = sub(mT, mv(R, mS))
    else:
        assert P["kind"] == "half" and C["kind"] == "half", (pfeat, cfeat)
        iA, oA = parent.w(P["inner"]), parent.w(P["outer"]); uA = unit(sub(oA, iA))
        uB = unit([C["outer"][0] - C["inner"][0], C["outer"][1] - C["inner"][1], 0])
        E = _frame(uB[:2], [-uB[1] * flip, uB[0] * flip])
        f1 = mul(uA, -1); f2 = mul(nA, side); F = mat([f1, f2, cross(f1, f2)])
        R = mm(F, tr(E)); t = sub(iA, mv(R, [C["inner"][0], C["inner"][1], 0]))
    return Placed(child_code, R, t)

def build(spec):
    root = spec.get("root", "flat")
    R0 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    placed = [Placed(spec["pieces"][0], R0, [0.0, 0.0, 0.0])]
    for (kind, child, cfeat, parent, pfeat, flip, side) in spec["joints"]:
        assert child == len(placed), "children in order"
        placed.append(attach(kind, placed[parent], pfeat, spec["pieces"][child], cfeat, flip, side))
    return placed

# ---------------------------------------------------------------- checks
def _intervals_on_line(pc, p0, d):
    """Parameters t where p0 + t d lies inside piece pc (line assumed in its plane)."""
    a, b = pc.loc(p0), mv(tr(pc.R), d)
    poly = pc.g["poly"]; ts = []
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        ex, ey = x2 - x1, y2 - y1
        den = b[0] * ey - b[1] * ex
        if abs(den) < 1e-12: continue
        t = ((x1 - a[0]) * ey - (y1 - a[1]) * ex) / den
        s = ((x1 - a[0]) * b[1] - (y1 - a[1]) * b[0]) / den
        if 0 <= s < 1: ts.append(t)
    ts.sort()
    return [(ts[k], ts[k + 1]) for k in range(0, len(ts) - 1, 2)]

def _cut_intervals(pc, p0, d, tol=0.35):
    out = []
    for a, b in pc.g["cuts"]:
        A, B = pc.w(a), pc.w(b)
        ok = True
        for Q in (A, B):
            v = sub(Q, p0); off = sub(v, mul(d, dot(v, d)))
            if norm(off) > tol: ok = False
        if ok:
            ta, tb = dot(sub(A, p0), d), dot(sub(B, p0), d)
            out.append((min(ta, tb) - 0.3, max(ta, tb) + 0.3))
    return out

def _subtract(iv, cuts):
    segs = [iv]
    for c0, c1 in cuts:
        nxt = []
        for s0, s1 in segs:
            if c1 <= s0 or c0 >= s1: nxt.append((s0, s1)); continue
            if c0 > s0: nxt.append((s0, c0))
            if c1 < s1: nxt.append((c1, s1))
        segs = nxt
    return segs

def _seg_cross(p, q, r, s):
    d = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
    if abs(d) < 1e-12: return False
    t = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / d
    u = ((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / d
    return 0 < t < 1 and 0 < u < 1

def pair_problem(A, B):
    nA, nB = A.n, B.n
    dd = cross(nA, nB)
    if norm(dd) < 1e-4:
        gap = abs(dot(sub(B.t, A.t), nA))
        if gap > 1.5: return None
        pb = [A.loc(B.w(p))[:2] for p in B.g["poly"]]; pa = A.g["poly"]
        from geom import inside
        if any(inside(pa, p) for p in pb[::4]) or any(inside(pb, p) for p in pa[::4]):
            return f"ซ้อนกันในแนวขนาน (ห่าง {gap:.1f} มม.)"
        for i in range(0, len(pa), 2):
            for j in range(0, len(pb), 2):
                if _seg_cross(pa[i], pa[(i + 2) % len(pa)], pb[j], pb[(j + 2) % len(pb)]):
                    return f"ขอบชนกันในแนวขนาน (ห่าง {gap:.1f} มม.)"
        return None
    d = unit(dd)
    # a point on both planes: solve with the third axis = d
    M = [nA, nB, d]; rhs = [dot(nA, A.t), dot(nB, B.t), 0.0]
    det = dot(nA, cross(nB, d))
    p0 = mul(add(add(mul(cross(nB, d), rhs[0]), mul(cross(d, nA), rhs[1])), mul(cross(nA, nB), rhs[2])), 1 / det)
    ia, ib = _intervals_on_line(A, p0, d), _intervals_on_line(B, p0, d)
    cuts = _cut_intervals(A, p0, d) + _cut_intervals(B, p0, d)
    worst = 0.0
    for a0, a1 in ia:
        for b0, b1 in ib:
            lo, hi = max(a0, b0), min(a1, b1)
            if hi - lo <= 0: continue
            for s0, s1 in _subtract((lo, hi), cuts):
                worst = max(worst, s1 - s0)
    return f"ชิ้นทะลุกัน {worst:.1f} มม. ตรงที่ไม่มีร่อง" if worst > 0.6 else None

def check(spec):
    problems = []
    used = {}
    pcs = spec["pieces"]
    joints = list(spec["joints"]) + [tuple(j) for j in spec.get("close", [])]
    for (kind, child, cfeat, parent, pfeat, flip, side) in joints:
        for key in ((child, cfeat), (parent, pfeat)):
            if key in used: problems.append(f"ชิ้น {key[0] + 1} ร่อง {key[1]} ถูกใช้ซ้ำ")
            used[key] = True
        if kind in "TS":
            tb, sl = ((child, cfeat), (parent, pfeat)) if kind == "T" else ((parent, pfeat), (child, cfeat))
            neck = math.dist(*(PIECES[pcs[tb[0]]]["feats"][tb[1]][k] for k in "ab"))
            slit = math.dist(*(PIECES[pcs[sl[0]]]["feats"][sl[1]][k] for k in "ab"))
            if not (0 <= slit - neck <= 1.0):
                problems.append(f"ปีก {pcs[tb[0]]} ({neck:.1f}) ไม่พอดีร่อง {pcs[sl[0]]} ({slit:.1f})")
    try:
        placed = build(spec)
    except AssertionError as e:
        return None, [f"ต่อไม่ได้: {e}"]
    for (kind, child, cfeat, parent, pfeat, flip, side) in spec.get("close", []):
        A, B = placed[parent], placed[child]
        P, C = A.g["feats"][pfeat], B.g["feats"][cfeat]
        if kind == "X":
            ok = norm(sub(A.w(P["inner"]), B.w(C["inner"]))) < 0.6 and abs(dot(unit(sub(A.w(P["outer"]), A.w(P["inner"]))), unit(sub(B.w(C["outer"]), B.w(C["inner"]))))+1) < 0.01
        else:
            ok = norm(sub(mul(add(A.w(P["a"]), A.w(P["b"])), .5), mul(add(B.w(C["a"]), B.w(C["b"])), .5))) < 0.6 and abs(dot(A.n, B.n)) < 1e-3
        if not ok: problems.append(f"วงไม่ปิด ชิ้น {child + 1} กับชิ้น {parent + 1}")
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            pr = pair_problem(placed[i], placed[j])
            if pr: problems.append(f"ชิ้น {i + 1} กับ {j + 1}: {pr}")
    return placed, problems

def bbox(placed):
    pts = [pc.w(p) for pc in placed for p in pc.g["poly"][::3]]
    lo = [min(p[k] for p in pts) for k in range(3)]; hi = [max(p[k] for p in pts) for k in range(3)]
    return lo, hi
