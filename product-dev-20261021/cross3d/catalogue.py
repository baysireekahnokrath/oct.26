"""50 crossing (ไขว้ 3D) product ideas built from the six existing dies, every one checked by assemble.check().

Each idea names a shape found by the search (shapes.py, saved as beam-*.json) or written out by hand,
plus what it is for, who buys it, how it is sold and the booth price. Cost uses the same formula as brand.py:
pieces + locks x 20 s of work + 60 s packing + packaging (+ extras).
Run: python3 catalogue.py  -> x3d.json (read by ../site/build.py) and a printed check report.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "brand-20261014"))
import brand as B
from assemble import check, bbox, build, dot, sub
from geom import PIECES, NAME
from shapes import kind as shape_kind, align, faces

FEAT_NAME = {
    "01": {"T1": "หูขวา", "T2": "หูบน", "S1": "ร่องแก้ม", "S2": "ร่องคาง"},
    "02": {"H1": "ร่องไขว้ 1", "H2": "ร่องไขว้ 2", "H3": "ร่องไขว้ 3", "H4": "ร่องไขว้ 4"},
    "03": {"S1": "ร่องซ้าย", "S2": "ร่องขวา", "T1": "ปีกบน", "T2": "ปีกล่าง"},
    "04": {"S1": "ร่องมุมซ้ายบน", "S2": "ร่องมุมขวาล่าง", "T1": "ปีกมุมขวาบน", "T2": "ปีกมุมซ้ายล่าง"},
    "05": {"S1": "ร่องบน", "S2": "ร่องล่าง", "T1": "ปีกขวา", "T2": "ปีกซ้าย"},
    "06": {"S1": "ร่องบน", "S2": "ร่องล่าง", "T1": "ปีกขวา", "T2": "ปีกซ้าย"},
}
SELL = {"ประกอบแล้ว": "wrap", "ชุดต่อเอง": "kit"}

_BEAMS = {}
def beam(fam):
    """Every search result saved for this family (beam-<fam>-<N>.json), merged."""
    if fam not in _BEAMS:
        import re
        pat = re.compile(r"beam-" + re.escape(fam.replace(",", "-")) + r"-(\d+)\.json$")
        _BEAMS[fam] = [t for f in sorted(os.listdir(HERE)) if pat.match(f) for t in json.load(open(os.path.join(HERE, f)))]
    return _BEAMS[fam]

_KIND = {}
def _kind(t):
    """Shape kind, worked out again on the aligned assembly (older search files stored it unaligned)."""
    k = json.dumps([t["pieces"], t["joints"]])
    if k not in _KIND: _KIND[k] = shape_kind(build(t))
    return _KIND[k]

def pick(fam, kind=None, n=None, rank=0, pieces=None, longest=False):
    """A shape from the search: filter by kind / piece count / exact piece list, most locks first."""
    c = [t for t in beam(fam) if (n is None or len(t["pieces"]) == n) and (pieces is None or sorted(t["pieces"]) == sorted(pieces))]
    if kind is not None:
        c = [t for t in c if _kind(t) == kind]
    key = (lambda t: (-max(t["dims"]), -len(t["close"]))) if longest else (lambda t: (-len(t["close"]), t["dims"][0] * t["dims"][1] * t["dims"][2]))
    c.sort(key=key)
    seen, uniq = set(), []
    for t in c:
        k = (tuple(t["pieces"]), tuple(sorted(t["dims"])), len(t["close"]), tuple((j[0], j[2], j[4]) for j in t["joints"]))
        if k not in seen: seen.add(k); uniq.append(t)
    t = uniq[rank]
    return {"pieces": t["pieces"], "joints": [tuple(j) for j in t["joints"]], "close": [tuple(j) for j in t["close"]]}

# ---------------------------------------------------------------- orientation: rest it on the table the low way
def _rot_to_up(ax):
    """Rotation that turns world axis `ax` (e.g. "+x") into +z."""
    s = 1 if ax[0] == "+" else -1; a = "xyz".index(ax[1])
    if a == 2: return [[1, 0, 0], [0, 1, 0], [0, 0, 1]] if s > 0 else [[1, 0, 0], [0, -1, 0], [0, 0, -1]]
    if a == 0: return [[0, 0, -s], [0, 1, 0], [s, 0, 0]]
    return [[1, 0, 0], [0, 0, -s], [0, s, 0]]

def _apply(M, v): return [sum(M[i][k] * v[k] for k in range(3)) for i in range(3)]
def _mm(A, Bm): return [[sum(A[i][k] * Bm[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

def orient(placed, up=None):
    pts = [(pc, [pc.w(p) for p in pc.g["poly"][::4]]) for pc in placed]
    best = None
    for ax in ([up] if up else ["+z", "-z", "+x", "-x", "+y", "-y"]):
        M = _rot_to_up(ax)
        zs = [_apply(M, q)[2] for _, ps in pts for q in ps]
        lo = min(zs); com = sum(zs) / len(zs) - lo
        if best is None or com < best[0] - 1.0: best = (com, ax, M)
    M = best[2]
    out = []
    for pc in placed:
        R = _mm(M, pc.R); t = _apply(M, pc.t)
        out.append((pc.code, R, t))
    allp = [_apply(M, q) for _, ps in pts for q in ps]
    lo = [min(p[k] for p in allp) for k in range(3)]; hi = [max(p[k] for p in allp) for k in range(3)]
    shift = [-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]]
    out = [(c, R, [t[k] + shift[k] for k in range(3)]) for c, R, t in out]
    dims = [hi[k] - lo[k] for k in range(3)]
    return out, dims, best[1]

def natural_up(aligned, kind):
    """Cups open upward, sleeves stand with the open middle upright; everything else rests the low way."""
    f = faces(aligned)
    if kind == "tube":
        used = {a for a, _ in f}
        return "+" + next(a for a in "zyx" if a not in used)
    if kind == "box":
        for a in "zyx":
            offs = {o for ax, o in f if ax == a}
            if len(offs) == 1:
                return ("+" if next(iter(offs)) < 0 else "-") + a
    return None

def steps_text(spec):
    pcs = spec["pieces"]; fn = lambda i, f: FEAT_NAME[pcs[i]][f]
    out = [f"วางชิ้น 1 ({NAME[pcs[0]]} {pcs[0]}) เป็นหลัก"]
    for (k, c, cf, p, pf, _, _) in spec["joints"]:
        if k == "T": out.append(f"ชิ้น {c + 1}: สอด{fn(c, cf)}เข้า{fn(p, pf)}ของชิ้น {p + 1} ให้ตั้งฉากกัน")
        elif k == "S": out.append(f"ชิ้น {c + 1}: เอา{fn(c, cf)}สวม{fn(p, pf)}ของชิ้น {p + 1} ให้ตั้งฉากกัน")
        else: out.append(f"ชิ้น {c + 1}: ไขว้{fn(c, cf)}เข้ากับ{fn(p, pf)}ของชิ้น {p + 1} ดันจนสุดร่อง")
    if spec.get("close"):
        locks = []
        for (k, c, cf, p, pf, _, _) in spec["close"]:
            if k == "X": locks.append(f"{fn(c, cf)}ชิ้น {c + 1} กับ{fn(p, pf)}ชิ้น {p + 1}")
            else:
                tab, slit = ((c, cf), (p, pf)) if PIECES[pcs[c]]["feats"][cf]["kind"] == "tab" else ((p, pf), (c, cf))
                locks.append(f"{fn(*tab)}ชิ้น {tab[0] + 1} เข้า{fn(*slit)}ชิ้น {slit[0] + 1}")
        out.append("ล็อกที่เหลือจะมาตรงร่องพอดี สอดให้ครบ: " + " · ".join(locks))
    return out

def cost(pieces, locks, sell, extra=0.0):
    pc = sum(B.PIECE_COST[c] for c in pieces)
    pack = sum(B.PACK_ITEMS[k][2] for k in B.PACK_PROFILE[SELL[sell]][1])
    return round(pc + locks * B.JOINT_COST + B.PACK_COST + pack + extra, 2)

# ---------------------------------------------------------------- the 50 ideas
def make():
    from ideas import IDEAS
    items, report = [], []
    for k, idea in enumerate(IDEAS, 1):
        spec = idea["spec"]
        placed, problems = check(spec)
        if problems:
            report.append(f"X{k:02d} {idea['name']}: " + "; ".join(problems)); continue
        kind = shape_kind(placed)
        aligned = align(placed)
        place, dims, up = orient(aligned, idea.get("up") or natural_up(aligned, kind))
        locks = len(spec["joints"]) + len(spec.get("close", []))
        c = cost(spec["pieces"], locks, idea["sell"], idea.get("extra", (None, 0))[1])
        from collections import Counter
        cnt = Counter(spec["pieces"])
        allp = [t for _, _, t in place]
        centre = [0.0, 0.0, dims[2] / 2]
        items.append({
            "id": f"X{k:02d}", "group": idea["group"], "name": idea["name"], "use": idea["use"], "who": idea["who"],
            "sell": idea["sell"], "pack": SELL[idea["sell"]], "price": idea["price"], "cost": c, "margin": round((idea["price"] - c) / idea["price"], 3),
            "pieces": spec["pieces"], "piecesTxt": " + ".join(f"{NAME[code]} {code} × {q}" for code, q in sorted(cnt.items())),
            "locks": locks, "locksTxt": f"ต่อ {len(spec['joints'])} + ปิดวง {len(spec.get('close', []))}",
            "dims": f"{dims[0] / 10:.1f} × {dims[1] / 10:.1f} × สูง {dims[2] / 10:.1f} ซม.", "shape": kind, "up": up,
            "centre": centre, "radius": round(math.sqrt(sum(d * d for d in dims)) / 2, 1),
            "place": [{"c": code, "R": [round(R[i][j], 5) for i in range(3) for j in range(3)], "t": [round(v, 2) for v in t]} for code, R, t in place],
            "steps": steps_text(spec), "spec": spec,
            # real-leather result: 02 pieces crossed into each other fall apart (owner's test, 21 Oct 2026)
            "real": "fail" if "02" in spec["pieces"] else "",
            # 06 was never cut, so it may not be used in new products for now (status doc, 21 Oct 2026)
            "no06": "06" in spec["pieces"],
        })
    return items, report

if __name__ == "__main__":
    items, report = make()
    geo = {c: {"poly": [[round(x, 2), round(y, 2)] for x, y in p["poly"][::2 if len(p["poly"]) > 150 else 1]],
               "cuts": [[[round(v, 2) for v in a], [round(v, 2) for v in b]] for a, b in p["cuts"]]} for c, p in PIECES.items()}
    json.dump({"geo": geo, "items": items}, open(os.path.join(HERE, "x3d.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(items), "ideas pass,", len(report), "fail")
    for r in report: print("  FAIL", r)
    low = [i for i in items if i["margin"] < 0.6]
    for i in items:
        print(f"{i['id']} {i['group']:<10} {i['name']:<34} {len(i['pieces']):2d} ชิ้น ล็อก {i['locks']:2d} {i['shape']:<8} {i['dims']:<28} {i['price']:4d} บาท ทุน {i['cost']:6.2f} กำไร {i['margin']:.0%}")
    if low: print("margin < 60%:", [i["id"] for i in low])
