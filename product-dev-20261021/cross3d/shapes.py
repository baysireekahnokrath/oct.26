"""Name the shape of an assembly by which cube-like planes its pieces sit on, and beam-search bigger ones."""
import json, sys
from assemble import check, build, bbox, dot, sub
import explore
from explore import grow, auto_close

def align(placed):
    """Turn the whole assembly so its piece planes face the x, y, z axes (04 pieces join on diagonals)."""
    from assemble import cross, unit, Placed
    ns = [p.n for p in placed]
    n1 = ns[0]; n2 = next((n for n in ns if abs(dot(n, n1)) < 0.1), None)
    if n2 is None:
        a = [1, 0, 0] if abs(n1[0]) < 0.9 else [0, 1, 0]
        n2 = unit(cross(n1, a))
    n3 = cross(n1, n2)
    M = [n2, n3, n1]                                   # rows: world -> aligned
    mv = lambda v: [sum(M[i][k] * v[k] for k in range(3)) for i in range(3)]
    out = []
    for p in placed:
        R = [[sum(M[i][k] * p.R[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        out.append(Placed(p.code, R, mv(p.t)))
    return out

def faces(placed):
    lo, hi = bbox(placed); c = [(lo[k] + hi[k]) / 2 for k in range(3)]
    out = []
    for p in placed:
        n = p.n; ax = max(range(3), key=lambda k: abs(n[k]))
        if abs(n[ax]) < 0.99: out.append(("tilt", 0)); continue
        off = p.t[ax] - c[ax]
        out.append(("xyz"[ax], round(off)))
    return out

def kind(placed):
    placed = align(placed)
    f = faces(placed); axes = {a for a, _ in f}
    planes = set(f); n = len(placed)
    if len(planes) < n: return "stack"
    if n == 6 and len(axes) == 3 and all(len({o for a, o in planes if a == ax}) == 2 for ax in axes): return "cube"
    if n == 5 and len(axes) == 3: return "box"
    if n == 4 and len(axes) == 2 and all(len({o for a, o in planes if a == ax}) == 2 for ax in axes): return "tube"
    if n == 3 and len(axes) == 3: return "corner"
    if n == 4 and len(axes) == 3: return "corner+"
    return f"open{n}"

def beam(family, N, K=40):
    explore.FAMILY = family
    level = [{"pieces": [family[0]], "joints": [], "close": []}]
    res = []
    for size in range(2, N + 1):
        cand, keys = [], set()
        for s in level:
            for t in grow({"pieces": s["pieces"], "joints": s["joints"], "close": s["close"]}):
                placed, pr = check(t)
                if pr: continue
                lo, hi = bbox(placed); dims = [round(hi[k] - lo[k]) for k in range(3)]
                cl = auto_close(t, placed)
                key = (tuple(sorted(t["pieces"])), tuple(sorted(dims)), len(cl) + len(t["close"]), tuple(sorted(faces(placed))))
                if key in keys: continue
                keys.add(key); t["close"] = t["close"] + cl
                if cl:      # re-check with the new locks counted as used
                    placed, pr = check(t)
                    if pr: continue
                t["dims"] = dims; t["kind"] = kind(placed); cand.append(t)
        compact = sorted(cand, key=lambda t: (-len(t["close"]), t["dims"][0] * t["dims"][1] * t["dims"][2]))[:K]
        longest = sorted(cand, key=lambda t: (-max(t["dims"]), -len(t["close"])))[:K // 4]
        level = compact + [t for t in longest if t not in compact]
        res += level
        print(size, len(cand), "best closures", len(compact[0]["close"]) if compact else 0, flush=True)
    return res

if __name__ == "__main__":
    fam = sys.argv[1].split(","); N = int(sys.argv[2])
    res = beam(fam, N)
    json.dump(res, open(f"beam-{'-'.join(fam)}-{N}.json", "w"))
    from collections import Counter
    print(Counter(t["kind"] for t in res))
