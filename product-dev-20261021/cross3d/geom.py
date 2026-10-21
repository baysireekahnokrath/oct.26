"""Die geometry for 3D crossing: outline polygons and joint features read from the 1:1 die SVGs.

Coordinates: mm, y up, origin at the piece centre (the 01 face centre, the centroid for the others).
Features
  slit  closed cut inside the piece: receives one tab           {kind, a, b}
  tab   neck between two collinear open slots (03-06) or an ear neck (01): passes through a slit
        {kind, a, b, wing}  a-b is the neck chord, wing is the in-plane unit normal toward the part that goes through
  half  open slot from the outline to the centre line (02): crosses another half slot     {kind, inner, outer}
Every cut segment (slits and slots) is also kept in `cuts`: two pieces may only share a line where one of them is cut.
"""
import math, os, re
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
SVG = os.path.join(REPO, "diecut-leather-20261014", "svg")
FILES = {"01": "01-bear-head", "02": "02-pinwheel-4-lobe", "03": "03-capsule-cross",
         "04": "04-rounded-square-diagonal", "05": "05-circle", "06": "06-soft-cross"}
FILES["07"] = os.path.join("..", "..", "diecut-leather-20261019", "svg", "07-round-joint-cross")     # REV 20261019
NAME = {"01": "หัวหมี", "02": "กังหัน", "03": "กากบาทแคปซูล", "04": "สี่เหลี่ยมมน", "05": "วงกลม", "06": "กากบาทนุ่ม",
        "07": "กากบาทข้อต่อวงกลม"}

def _path_points(d, steps=16):
    toks = re.findall(r"[MCLZ]|-?\d+\.?\d*", d)
    pts, cur, i, cmd = [], None, 0, None
    while i < len(toks):
        t = toks[i]
        if t in "MCLZ":
            cmd = t; i += 1
            if t == "Z": break
            continue
        if cmd == "M":
            cur = (float(toks[i]), float(toks[i + 1])); pts.append(cur); i += 2
        elif cmd == "L":
            cur = (float(toks[i]), float(toks[i + 1])); pts.append(cur); i += 2
        elif cmd == "C":
            c1 = (float(toks[i]), float(toks[i + 1])); c2 = (float(toks[i + 2]), float(toks[i + 3])); p3 = (float(toks[i + 4]), float(toks[i + 5]))
            p0 = cur
            for k in range(1, steps + 1):
                s = k / steps; u = 1 - s
                pts.append((u**3 * p0[0] + 3 * u * u * s * c1[0] + 3 * u * s * s * c2[0] + s**3 * p3[0],
                            u**3 * p0[1] + 3 * u * u * s * c1[1] + 3 * u * s * s * c2[1] + s**3 * p3[1]))
            cur = p3; i += 6
    if math.dist(pts[0], pts[-1]) < 1e-6: pts.pop()
    return pts

def inside(poly, p):
    x, y = p; n = len(poly); c = False
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c

def load(code):
    s = open(os.path.join(SVG, FILES[code] + ".svg")).read()
    W, H = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    d = re.search(r'<g id="CUT"[^>]*><path d="([^"]+)"', s).group(1)
    raw = _path_points(d)
    lines = [tuple(float(v) for v in m) for m in re.findall(r'x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', s)]
    flip = lambda p: (p[0], H - p[1])
    poly = [flip(p) for p in raw]
    if code == "01":
        # face centre: the big circle (face R about 41.7), found as the centre of the face arc points
        C = (41.685, H - 62.675)
    else:
        a = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) / 2
        cx = sum((poly[i][0] + poly[(i + 1) % len(poly)][0]) * (poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]) for i in range(len(poly))) / (6 * a)
        cy = sum((poly[i][1] + poly[(i + 1) % len(poly)][1]) * (poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]) for i in range(len(poly))) / (6 * a)
        C = (round(cx, 3), round(cy, 3))
    sh = lambda p: (round(p[0] - C[0], 3), round(p[1] - C[1], 3))
    poly = [sh(p) for p in poly]
    if sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) < 0:
        poly.reverse()                                      # counter-clockwise
    segs = [(sh(flip(l[:2])), sh(flip(l[2:]))) for l in lines]
    cuts, slits, slots = [], [], []
    for a, b in segs:
        ia, ib = inside(poly, a), inside(poly, b)
        cuts.append((a, b))
        if ia and ib: slits.append((a, b))
        else: slots.append((b, a) if ia else (a, b))       # (outer, inner)
    feats = []
    for a, b in slits:
        feats.append({"kind": "slit", "a": a, "b": b})
    if code == "02":
        for outer, inner in slots:
            feats.append({"kind": "half", "inner": inner, "outer": outer})
    elif code == "01":
        # ear necks: chord between the two path vertices where an ear meets the face
        for a, b in (((32.995, 21.903), (50.375, 21.903)), ((82.457, 53.985), (82.457, 71.365))):
            A, B = sh(flip(a)), sh(flip(b))
            mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
            L = math.hypot(mx, my); wing = (round(mx / L, 6), round(my / L, 6))
            feats.append({"kind": "tab", "a": A, "b": B, "wing": wing, "slots": []})
    else:
        used = set()
        for i, (o1, n1) in enumerate(slots):
            for j, (o2, n2) in enumerate(slots):
                if j <= i or i in used or j in used: continue
                d1 = (n1[0] - o1[0], n1[1] - o1[1]); d2 = (n2[0] - o2[0], n2[1] - o2[1])
                cross = d1[0] * d2[1] - d1[1] * d2[0]
                col = abs((n2[0] - n1[0]) * d1[1] - (n2[1] - n1[1]) * d1[0]) / math.hypot(*d1)
                if abs(cross) < 1e-3 and col < 0.05 and (d1[0] * d2[0] + d1[1] * d2[1]) < 0:
                    used |= {i, j}
                    mx, my = (n1[0] + n2[0]) / 2, (n1[1] + n2[1]) / 2
                    L = math.hypot(mx, my); wing = (round(mx / L, 6), round(my / L, 6))
                    feats.append({"kind": "tab", "a": n1, "b": n2, "wing": wing, "slots": [(o1, n1), (o2, n2)]})
    # stable names: S1.. slits, T1.. tabs, H1.. halves, ordered by angle of the midpoint from +x
    def ang(f):
        p = f.get("inner") or ((f["a"][0] + f["b"][0]) / 2, (f["a"][1] + f["b"][1]) / 2)
        return math.atan2(p[1], p[0]) % (2 * math.pi)
    out = {}
    for kind, pre in (("slit", "S"), ("tab", "T"), ("half", "H")):
        for k, f in enumerate(sorted([f for f in feats if f["kind"] == kind], key=ang)):
            out[f"{pre}{k + 1}"] = f
    return {"code": code, "poly": poly, "cuts": cuts, "feats": out, "W": W, "H": H}

PIECES = {c: load(c) for c in FILES}

def seglen(a, b): return math.dist(a, b)

if __name__ == "__main__":
    for c, p in PIECES.items():
        print(c, NAME[c], len(p["poly"]), "pts")
        for k, f in p["feats"].items():
            if f["kind"] == "half":
                print("  ", k, "half inner", f["inner"], "outer", f["outer"], "len %.2f" % seglen(f["inner"], f["outer"]))
            else:
                print("  ", k, f["kind"], f["a"], f["b"], "len %.2f" % seglen(f["a"], f["b"]), f.get("wing", ""))
