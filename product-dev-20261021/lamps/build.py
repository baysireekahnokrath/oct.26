"""Build lamps/index.html: hanging and floor lamps from the cut pieces (owner, 27 Oct). Thai, phone first.

Radius of a pattern = what decides how big a woven lamp gets. Two pieces of the same die join wing-in-slit, so their
centres sit (slit distance + wing distance) apart: the pitch. Neighbours turn 90 deg, so a ring needs an even count.
  drum   N pieces round, M rows high: radius N * pitch / 2 pi, height (M - 1) * pitch + piece size
  globe  rows down a sphere of radius R, each row as many pieces (even) as fit its circle; the poles stay open
Distances come from the die files (cross3d/geom.py). Only 07 has been joined in real leather (owner, 23 Oct).
python3 lamps/build.py -> lamps/index.html
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import geom

COST = {"01": 3.89, "02": 3.71, "03": 3.61, "04": 4.22, "05": 3.84, "07": 3.45}       # sheet, 22 Oct
STOCK = {"01": 369, "02": 150, "03": 150, "04": 150, "05": 150, "07": 200}
NAME = {"01": "หัวหมี", "02": "กังหัน", "03": "กากบาทแคปซูล", "04": "สี่เหลี่ยมมน", "05": "วงกลม", "07": "กากบาทข้อต่อวงกลม"}
NOTE = {"01": "หูอยู่ขวาและบน ร่องอยู่ซ้ายและล่าง หมีทุกตัวหันทางเดียวกัน ไม่ต้องสลับ วงไม่ต้องเป็นเลขคู่ · ยังไม่ได้ลองต่อจริง · 01 มีมากที่สุด 369 ชิ้น",
        "02": "ไม่มีปีก ต่อแบบร่องไขว้ ลองจริง 21 ต.ค. แล้วหลุด ใช้ทำโคมไม่ได้",
        "03": "ระยะสั้นที่สุด ลายถี่ ใช้ชิ้นเยอะ ยังไม่ได้ลองต่อจริง",
        "04": "ข้อต่ออยู่ที่มุม ต้องหมุนชิ้น 45 องศา ยังไม่ได้ลองต่อจริง",
        "05": "ช่องไฟระหว่างวงกลมสวย ยังไม่ได้ลองต่อจริง",
        "07": "ต่อจริงแล้ว 23 ต.ค. (ที่ห้อยกระเป๋า ปลอกขวดน้ำ กระเป๋า) แนะนำเริ่มที่ลายนี้"}

def die(code):
    g = geom.load(code); P = g["poly"]
    cx = cy = 0.0                                   # the die file's origin is the piece centre (01: centre of the head, not the box)
    pts = [(P[0][0] - cx, P[0][1] - cy)]
    for x, y in P[1:]:
        if math.dist((x - cx, y - cy), pts[-1]) > 0.7: pts.append((x - cx, y - cy))
    out = dict(code=code, rout=max(math.hypot(*p) for p in pts), rin=min(math.hypot(*p) for p in pts),
               area=0.5 * abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))))
    sl = [v for v in g["feats"].values() if v.get("kind") == "slit"]; tb = [v for v in g["feats"].values() if v.get("kind") == "tab"]
    mid = lambda v: ((v["a"][0] + v["b"][0]) / 2 - cx, (v["a"][1] + v["b"][1]) / 2 - cy)
    if sl and tb:
        out["slit"] = math.hypot(*mid(sl[0])); out["tab"] = math.hypot(*mid(tb[0]))
        out["pitch"] = out["slit"] + out["tab"]
        # 01 has its slits left and below, its ears right and above: bears all face the same way and join in a plain grid.
        # The others carry slits on one axis and wings on the other: turn the slit arms to point up and alternate 90 deg.
        out["alt"] = code != "01"
        sx, sy = mid(sl[0]); out["turn"] = math.pi / 2 - math.atan2(sy, sx) if out["alt"] else 0.0
        c, s_ = math.cos(out["turn"]), math.sin(out["turn"])
        feats = [(v["kind"], mid(v)) for v in sl + tb]
        rot = lambda q: (q[0] * c - q[1] * s_, q[0] * s_ + q[1] * c)
        out["up"] = max(rot(m)[1] for _, m in feats); out["down"] = -min(rot(m)[1] for _, m in feats)
        out["upkind"] = next(k for k, m in feats if abs(rot(m)[1] - out["up"]) < 1e-6)
        ys_ = [rot(q)[1] for q in pts]; out["ext"] = max(ys_) - min(ys_); out["top"] = max(ys_); out["bottom"] = -min(ys_)
        out["slitlen"] = math.dist(sl[0]["a"], sl[0]["b"]); out["tablen"] = math.dist(tb[0]["a"], tb[0]["b"])
    else:                                                                       # 02: half slots only
        h = list(g["feats"].values())[0]; out["half"] = math.hypot(h["inner"][0] - cx, h["inner"][1] - cy)
    out["poly"] = [[round(x, 1), round(y, 1)] for x, y in pts]
    out["cuts"] = [[[round(a[0] - cx, 1), round(a[1] - cy, 1)], [round(b[0] - cx, 1), round(b[1] - cy, 1)]] for a, b in g["cuts"]]
    return out

DIES = {c: die(c) for c in COST}
even = lambda x: max(2, 2 * round(x / 2))

def drum(d, n, m):
    p = d["pitch"]; R = n * p / (2 * math.pi); pcs = []
    for r in range(m):
        z = (r - (m - 1) / 2) * p
        for j in range(n):
            f = 2 * math.pi * j / n
            pcs.append([R * math.cos(f), R * math.sin(f), z, -math.sin(f), math.cos(f), 0, 0, 0, 1, (r + j) % 2 if d["alt"] else 0, (r + j) % 2])   # last two: turn 90 deg, colour
    half = (m - 1) / 2 * p                         # rings sit on the free joint lines of the top and bottom rows
    return dict(R=R, H=2 * half + d["ext"], n=len(pcs), pieces=pcs, rings=[[half + d["up"], R], [-half - d["down"], R]], rows=[n] * m)

def globe(d, R):
    p = d["pitch"]; K = max(3, round(math.pi * R / p)); pcs = []; rows = []; th = []
    for k in range(K):
        t = (k + 0.5) * math.pi / K; x = 2 * math.pi * R * math.sin(t) / p; n = even(x) if d["alt"] else max(1, round(x))
        if n < 6: continue                                                    # leave the poles open: fitter on top, bulb from below
        rows.append(n); th.append(t)
        for j in range(n):
            f = 2 * math.pi * j / n + (math.pi / n if k % 2 else 0)
            st, ct = math.sin(t), math.cos(t)
            pcs.append([R * st * math.cos(f), R * st * math.sin(f), R * ct, -math.sin(f), math.cos(f), 0,
                        -ct * math.cos(f), -ct * math.sin(f), st, (k + j) % 2 if d["alt"] else 0, (k + j) % 2])
    edge = lambda t: [R * math.cos(t), R * math.sin(t)]
    t0, t1 = th[0] - d["up"] / R, th[-1] + d["down"] / R
    return dict(R=R, H=R * (math.cos(t0) - math.cos(t1)), n=len(pcs), pieces=pcs, rings=[edge(t0), edge(t1)],
                rows=rows, open_top=2 * R * math.sin(t0), open_bottom=2 * R * math.sin(math.pi - t1))

# four lamps (owner, 28 Oct: table, floor and hanging; start with 01 and 07). Sizes keep the bulb at least 10 cm from the leather:
# table lamps take a small E14 LED, the others an A60 E27 LED.
TARGET = {"table-drum": (250, 200), "pendant-drum": (290, 260), "pendant-globe": (300, None), "floor-drum": (360, 300)}   # mm across, tall
SHOW = ("01", "07")
LAMPS = {}
for c in SHOW:
    d = DIES[c]; p = d["pitch"]
    count = lambda w: even(w * math.pi / p) if d["alt"] else round(w * math.pi / p)
    rows_for = lambda h: max(2, round((h - d["ext"]) / p) + 1)                 # rows so the shade is about h mm tall
    LAMPS[c] = {k: (globe(d, w / 2) if h is None else drum(d, count(w), rows_for(h))) for k, (w, h) in TARGET.items()}

def rnd(o):
    if isinstance(o, float): return round(o, 1)
    if isinstance(o, list): return [rnd(x) for x in o]
    if isinstance(o, dict): return {k: rnd(v) for k, v in o.items()}
    return o
DATA = dict(dies={c: {k: DIES[c][k] for k in ("poly", "cuts", "turn", "pitch", "up", "down", "ext", "alt", "upkind")} for c in LAMPS},
            lamps=LAMPS, names=NAME)

E = lambda s: s.replace("&", "&amp;").replace("<", "&lt;")
# radius table: every die
rows = ""
for c, d in DIES.items():
    if "pitch" in d:
        joint = f'{d["slit"]:.1f} / {d["tab"]:.1f}'; pitch = f'{d["pitch"]:.1f}'
        fit = f'{d["slitlen"] - d["tablen"]:.1f}'
    else:
        joint, pitch, fit = f'ร่องครึ่ง {d["half"]:.1f}', "–", "–"
    rows += (f'<tr class="{"ok" if c in SHOW else ("no" if c == "02" else "")}"><th>{c} {E(NAME[c])}</th><td>{d["rout"] / 10:.1f}</td>'
             f'<td>{joint}</td><td><b>{pitch}</b></td><td>{fit}</td><td>{d["area"] / 100:.0f}</td><td class="note">{E(NOTE[c])}</td></tr>')
RADIUS = rows

# ring table: diameter for an even count round, for the dies that can make a lamp
counts = list(range(8, 26, 2))
ring = "".join(f'<tr><th>{c}</th>' + "".join(f'<td>{n * DIES[c]["pitch"] / math.pi / 10:.1f}</td>' for n in counts) + "</tr>"
               for c in ("01", "07", "05", "04", "03"))
RING = f'<thead><tr><th>ลาย</th>{"".join(f"<th>{n} ชิ้น</th>" for n in counts)}</tr></thead><tbody>{ring}</tbody>'

KIND = {"table-drum": "โคมตั้งโต๊ะ", "pendant-drum": "โคมแขวนทรงกระบอก", "pendant-globe": "โคมแขวนทรงกลม", "floor-drum": "โคมตั้งพื้น"}
spec = ""
for c in SHOW:
    for k, L in LAMPS[c].items():
        size = (f'Ø {2 * L["R"] / 10:.1f} × สูง {L["H"] / 10:.1f} ซม.' if "drum" in k else
                f'Ø {2 * L["R"] / 10:.0f} ซม. ช่องบน {L["open_top"] / 10:.0f} ล่าง {L["open_bottom"] / 10:.0f} ซม.')
        layout = (f'{L["rows"][0]} ชิ้นรอบ × {len(L["rows"])} แถว' if "drum" in k else " · ".join(map(str, L["rows"])) + " ชิ้นต่อแถว")
        enough = L["n"] <= STOCK[c]
        spec += (f'<tr><th>{c}</th><td>{KIND[k]}</td><td class="num">{size}</td><td class="num">{layout}</td>'
                 f'<td class="num"><b>{L["n"]}</b></td><td class="num">{L["n"] * COST[c]:.0f}</td>'
                 f'<td class="num {"" if enough else "warn"}">{STOCK[c] // L["n"]} ใบ</td></tr>')
SPEC = spec

PAGE = open(os.path.join(HERE, "template.html")).read()
for k, v in {"__DATA__": json.dumps(rnd(DATA), separators=(",", ":"), ensure_ascii=False), "__RADIUS__": RADIUS, "__RING__": RING,
             "__SPEC__": SPEC}.items():
    PAGE = PAGE.replace(k, v)
open(os.path.join(HERE, "index.html"), "w").write(PAGE)
for c in SHOW:
    for k, L in LAMPS[c].items(): print(c, k, f'R {L["R"]:.0f} H {L["H"]:.0f} n {L["n"]}', L["rows"])
print("lamps/index.html", len(PAGE), "bytes")
