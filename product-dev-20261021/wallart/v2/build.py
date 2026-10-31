"""Build wallart/index.html: framed 3D wall pieces with volume (owner, 31 Oct: flat is not special; make it a mound,
a flower, a bush, a dreamy swaying meadow).

Three pieces, each in a deep box frame, every leather piece a 07 die drawn from the die file (cross3d/geom.py):
  flower  S  petals in three rings, the outer ones lying back, the inner ones standing up, on a 2 x 2 woven disc
  bush    M  five woven domes of different sizes pushed together (the bag body, woven the same way)
  meadow  L  stems of stacked 07 standing up from a ground strip in three rows of depth, tall at the back; they sway
Stems join the ground strip at 90 degrees wing-in-slit, the joint the 07 die was cut for. 07 pieces sit 56.86 mm apart.
The page shows them in 3D with real shadows; the numbers below the model are counted here.
python3 wallart/v2/build.py -> wallart/v2/index.html (ฉบับ 2 ไม่ผ่าน 31 ต.ค. เก็บไว้ดูย้อนหลัง)
"""
import json, math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import geom

P, J = 2 * 28.43, 28.43                         # 07 pitch and joint distance, mm
COST07 = 3.45                                   # sheet, 22 Oct
even = lambda x: max(4, 2 * round(x / 2))

def outline():
    g = geom.load("07"); pts = [g["poly"][0]]
    for p in g["poly"][1:]:
        if math.dist(p, pts[-1]) > 0.8: pts.append(p)
    return [[round(x, 1), round(y, 1)] for x, y in pts], [[list(a), list(b)] for a, b in g["cuts"]]

def piece(c, u, v, role, turn=0, col=-1):
    """centre, in-plane axes u and v (unit), colour role, extra turn in degrees, sway column"""
    return [round(c[0], 1), round(c[1], 1), round(c[2], 1)] + [round(x, 4) for x in u + v] + [role, turn, col]

def flower(cx=0.0, cy=0.0, scale=1.0):
    out = []
    for i, (x, y) in enumerate([(-P / 2, -P / 2), (P / 2, -P / 2), (-P / 2, P / 2), (P / 2, P / 2)]):   # 2 x 2 woven disc behind
        out.append(piece((cx + x, cy + y, 4), [1, 0, 0], [0, 1, 0], "base", 90 * (i in (1, 2))))
    for n, r, tilt, z, role, phase in ((9, 54, 20, 12, "petal1", 0), (6, 32, 46, 24, "petal2", .5), (4, 14, 66, 34, "petal3", .25)):
        t = math.radians(tilt)
        for k in range(n):
            f = 2 * math.pi * (k + phase) / n
            radial = [math.cos(f), math.sin(f), 0]; tang = [-math.sin(f), math.cos(f), 0]
            v = [radial[0] * math.cos(t), radial[1] * math.cos(t), math.sin(t)]
            out.append(piece((cx + r * scale * radial[0], cy + r * scale * radial[1], z), tang, v, role, 90 * (k % 2)))
    return out

def dome(cx, cy, R, roles):
    K = max(1, round((math.pi / 2) * R / P)); out = []
    for k in range(K):
        th = (k + 0.6) * (math.pi / 2) / (K + 0.2); n = even(2 * math.pi * R * math.sin(th) / P)
        for j in range(n):
            f = 2 * math.pi * (j + .5 * (k % 2)) / n
            pos = (cx + R * math.sin(th) * math.cos(f), cy + R * math.sin(th) * math.sin(f), R * math.cos(th) * .9)
            u = [-math.sin(f), math.cos(f), 0]; v = [-math.cos(th) * math.cos(f), -math.cos(th) * math.sin(f), math.sin(th)]
            out.append(piece(pos, u, v, roles[(j + k) % len(roles)], 90 * ((j + k) % 2)))
    out.append(piece((cx, cy, R * .9 + 2), [1, 0, 0], [0, 1, 0], roles[0], 45))                          # cap
    return out

def bush():
    out = []
    for cx, cy, R, roles in ((-58, -38, 78, ("bushA", "bushB")), (62, -52, 64, ("bushB", "bushC")), (8, 52, 66, ("bushA", "bushC")),
                             (-82, 66, 46, ("bushC", "bushB")), (96, 48, 44, ("bushB", "bushA"))):
        out += dome(cx, cy, R, roles)
    for cx, cy, z in ((-34, -6, 86), (52, 26, 74)):                                                       # two little blooms tucked in
        out.append(piece((cx, cy, z), [1, 0, 0], [0, 1, 0], "accent", 45))
    return out

def meadow(inner):
    rnd = random.Random(26)
    ground = -inner / 2 + 6; out = []; cols = []
    rows = [(14, 7, (4, 6)), (36, 6, (2, 4)), (58, 7, (1, 2))]           # depth from the back board, columns, pieces tall
    for depth, n, (lo, hi) in rows:
        for i in range(n):
            x = (i - (n - 1) / 2) * (inner - 70) / (n - 1) + rnd.uniform(-10, 10)
            yaw = math.radians(rnd.uniform(-25, 25)); h = rnd.randint(lo, hi)
            u = [math.cos(yaw), 0, -math.sin(yaw)]; v = [0, 1, 0]
            col = len(cols); cols.append(dict(x=round(x, 1), y=round(ground, 1), z=depth, phase=round(rnd.uniform(0, 6.28), 2), amp=round(rnd.uniform(3, 7), 1)))
            out.append(piece((x, ground + .8, depth), [1, 0, 0], [0, 0, 1], "ground", 90 * (i % 2)))   # flat in the ground strip
            for k in range(h):                                                                           # stacked stem, relative to its base
                role = "head" if k == h - 1 else ("stem2" if k >= h / 2 else "stem1")
                out.append(piece((0, J + k * P, 0), u, v, role, 90 * (k % 2), col))
    return out, cols

FRAMES = {"flower": dict(size="S", W=300, D=80, title="ดอกไม้", price=(990, 1290)),
          "bush": dict(size="M", W=350, D=110, title="พุ่ม", price=(1890, 2390)),
          "meadow": dict(size="L", W=500, D=90, title="ทุ่งหญ้าแห่งความฝัน", price=(3990, 4990))}
poly, cuts = outline()
PIECES = {"flower": flower(), "bush": bush()}
PIECES["meadow"], COLS = meadow(FRAMES["meadow"]["W"] - 40)
for k, f in FRAMES.items():
    f["n"] = len(PIECES[k]); f["leather"] = round(f["n"] * COST07)
DATA = dict(poly=poly, cuts=cuts, frames=FRAMES, pieces=PIECES, cols=COLS)

rows = ""
for k, f in FRAMES.items():
    lo, hi = f["price"]
    rows += (f'<tr><th>{f["size"]} {f["title"]}</th><td class="num">{f["W"] // 10}×{f["W"] // 10}</td><td class="num">{f["D"] // 10}</td>'
             f'<td class="num"><b>{f["n"]}</b></td><td class="num">{f["leather"]}</td><td class="num">{lo:,}–{hi:,}</td></tr>')
PAGE = (open(os.path.join(HERE, "template.html")).read().replace("__DATA__", json.dumps(DATA, separators=(",", ":"), ensure_ascii=False))
        .replace("__ROWS__", rows).replace("__N07__", str(sum(f["n"] for f in FRAMES.values()))))
open(os.path.join(HERE, "index.html"), "w").write(PAGE)
print("wallart/index.html", len(PAGE), "bytes ·", {k: f["n"] for k, f in FRAMES.items()})
