"""Data for the PD page tab "ชิ้นเดียว 50": the 50 single-piece ideas with costs and die geometry for the drawings.

python3 single50/build.py -> single50/single50.json (read by ../site/build.py)
Costs: piece cost from the status doc (PIECE_REAL), 20 s of work per insert or stamp and 60 s packing at 50 THB/h
(brand.py JOINT_COST, PACK_COST), packaging from brand.py PACK_ITEMS, plus the listed extras.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "cross3d")); sys.path.insert(0, os.path.join(ROOT, "..", "brand-20261014"))
import brand as B
from geom import _path_points, inside, NAME
from single_ideas import IDEAS, PIECE_REAL
sys.path.insert(0, os.path.join(ROOT, "assortment"))
from assortment import DROP           # owner's 22 Oct rules: no food contact, nothing for young children

SVGS = {c: os.path.join(ROOT, "..", "diecut-leather-20261014", "svg", f) for c, f in
        (("01", "01-bear-head.svg"), ("02", "02-pinwheel-4-lobe.svg"), ("03", "03-capsule-cross.svg"),
         ("04", "04-rounded-square-diagonal.svg"), ("05", "05-circle.svg"))}
SVGS["07"] = os.path.join(ROOT, "..", "diecut-leather-20261019", "svg", "07-round-joint-cross.svg")

def die(path):
    s = open(path).read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    d = re.search(r'<g id="CUT"[^>]*>\s*<path d="([^"]+)"', s).group(1)
    poly = _path_points(d)
    lines = [[float(v) for v in m] for m in re.findall(r'x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', s)]
    slits, slots = [], []
    for x1, y1, x2, y2 in lines:
        a, b = inside(poly, (x1, y1)), inside(poly, (x2, y2))
        if a and b: slits.append([x1, y1, x2, y2])
        else: slots.append([x1, y1, x2, y2] if not a else [x2, y2, x1, y1])      # outer first
    return {"vb": vb, "d": d, "slits": slits, "slots": slots}

GEO = {c: die(p) for c, p in SVGS.items()}
WORK = {"plain": 0, "object": 0, "set": 0}

def cost(pieces, mech, extras, pack, stamp):
    pc = sum(PIECE_REAL[c] * q for c, q in pieces)
    steps = sum(q for _, q in pieces) * (0 if mech in WORK else 1) + (sum(q for _, q in pieces) if stamp else 0)
    packaging = sum(B.PACK_ITEMS[k][2] for k in B.PACK_PROFILE[pack][1])
    return round(pc + steps * B.JOINT_COST + B.PACK_COST + packaging + sum(t for _, t in extras), 2)

items = []
for (i, group, name, pieces, how, mech, extras, pack, who, price, load, test, stamp) in IDEAS:
    assert all(c != "06" for c, _ in pieces), i
    c = cost(pieces, mech, extras, pack, stamp)
    items.append(dict(id=i, group=group, name=name, pieces=pieces, how=how, mech=mech, extras=extras, pack=pack, who=who,
                      price=price, load=load, test=test, stamp=stamp, cost=c, margin=round((price - c) / price, 3),
                      piecesTxt=" + ".join(f"{NAME[c]} {c} × {q}" for c, q in pieces),
                      uses07="07" in [c for c, _ in pieces],
                      drop=(" · ".join(DROP[i]) if i in DROP else "")))
assert len(items) == 50 and len({x["id"] for x in items}) == 50
use = {}
for x in items:
    for c, q in x["pieces"]: use[c] = use.get(c, 0) + 1
out = {"geo": GEO, "items": items, "dieUse": use}
json.dump(out, open(os.path.join(HERE, "single50.json"), "w"), ensure_ascii=False, separators=(",", ":"))
low = [x["id"] for x in items if x["margin"] < 0.6]
print(len(items), "ideas · ideas per die", dict(sorted(use.items())), "· load items", sum(x["load"] for x in items), "· margin < 60%:", low)
print("margin range", min(x["margin"] for x in items), max(x["margin"] for x in items))
