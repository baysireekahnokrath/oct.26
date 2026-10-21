"""Search small assemblies family by family and report the ones that pass check(), with loops that close by themselves."""
import itertools, math, sys
from assemble import check, build, bbox, norm, sub, mul, add, dot, unit
from geom import PIECES

def free_feats(spec):
    used = {(j[1], j[2]) for j in spec["joints"]} | {(j[3], j[4]) for j in spec["joints"]} | {(j[1], j[2]) for j in spec.get("close", [])} | {(j[3], j[4]) for j in spec.get("close", [])}
    return [(i, k, f) for i, c in enumerate(spec["pieces"]) for k, f in PIECES[c]["feats"].items() if (i, k) not in used]

def fits(tab_code, tab, slit_code, slit):
    n = math.dist(PIECES[tab_code]["feats"][tab]["a"], PIECES[tab_code]["feats"][tab]["b"])
    s = math.dist(PIECES[slit_code]["feats"][slit]["a"], PIECES[slit_code]["feats"][slit]["b"])
    return 0 <= s - n <= 1.0

def auto_close(spec, placed):
    """Free tab/slit (or half/half) pairs that already line up: extra locks the structure gets for free."""
    fr = free_feats(spec); out = []
    for (i, k, f) in fr:
        for (j, l, g) in fr:
            if i == j: continue
            A, B = placed[j], placed[i]
            if f["kind"] == "tab" and g["kind"] == "slit" and fits(spec["pieces"][i], k, spec["pieces"][j], l):
                mt = mul(add(B.w(f["a"]), B.w(f["b"])), .5); ms = mul(add(A.w(g["a"]), A.w(g["b"])), .5)
                if norm(sub(mt, ms)) < 0.6 and abs(dot(A.n, B.n)) < 1e-3:
                    out.append(("T", i, k, j, l, 1, 1))
            if f["kind"] == "half" and g["kind"] == "half" and i < j:
                if norm(sub(B.w(f["inner"]), A.w(g["inner"]))) < 0.6 and abs(dot(A.n, B.n)) < 1e-3:
                    out.append(("X", i, k, j, l, 1, 1))
    # keep each feature once
    seen, res = set(), []
    for c in out:
        if (c[1], c[2]) in seen or (c[3], c[4]) in seen: continue
        seen |= {(c[1], c[2]), (c[3], c[4])}; res.append(c)
    return res

def grow(spec):
    """All ways to add one more piece of the same codes family."""
    fr = free_feats(spec); n = len(spec["pieces"])
    for (pi, pf, P) in fr:
        for code in FAMILY:
            for cf, C in PIECES[code]["feats"].items():
                if P["kind"] == "slit" and C["kind"] == "tab" and fits(code, cf, spec["pieces"][pi], pf): kind = "T"
                elif P["kind"] == "tab" and C["kind"] == "slit" and fits(spec["pieces"][pi], pf, code, cf): kind = "S"
                elif P["kind"] == "half" and C["kind"] == "half": kind = "X"
                else: continue
                for flip in (1, -1):
                    for side in (1, -1):
                        yield {"pieces": spec["pieces"] + [code], "joints": spec["joints"] + [(kind, n, cf, pi, pf, flip, side)], "close": list(spec.get("close", []))}

if __name__ == "__main__":
    FAMILY = sys.argv[1].split(",")
    N = int(sys.argv[2])
    level = [{"pieces": [FAMILY[0]], "joints": []}]
    for size in range(2, N + 1):
        nxt, keys = [], set()
        for s in level:
            for t in grow(s):
                placed, pr = check(t)
                if pr: continue
                lo, hi = bbox(placed)
                dims = tuple(sorted(round(hi[k] - lo[k]) for k in range(3)))
                cl = auto_close(t, placed)
                key = (tuple(sorted(t["pieces"])), dims, len(cl))
                if key in keys: continue
                keys.add(key); t["close"] = cl; nxt.append(t)
        level = nxt
        loops = [t for t in level if t["close"]]
        print(size, "pieces:", len(level), "distinct shapes,", len(loops), "with self-closing loops")
        for t in loops[:6]:
            placed = build(t); lo, hi = bbox(placed)
            print("   ", t["pieces"], "close", [(c[1], c[2], c[3], c[4]) for c in t["close"]], [round(hi[k] - lo[k]) for k in range(3)])
