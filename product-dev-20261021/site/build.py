"""Build site/index.html, the OCT. 26 Product Development page, from pd.py and brand.py.

The page carries the static product data; stages, blockers, notes, new ideas and test results
are kept in the artifact's shared database (capability db), collections `items` and `tests`:
  items/p01..p30  {stage, blocker, note, updated}            state of an existing product
  items/i-xxxx    {kind:"idea", name, who, price, parts, joints, extra, pack, stage, blocker, note, updated}
  tests/<auto>    {item, tester, build, pull, fit, tear, photo, seconds, note, at}   result: "pass" | "fail" | ""
Publish with capabilities {"db": {}}.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); REPO = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)
import pd
B = pd.B

def outline(path):
    """Cut path, slit lines and viewBox from a 1:1 die SVG."""
    s = open(path).read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    d = re.search(r'<g id="CUT"[^>]*>\s*<path d="([^"]+)"', s).group(1)
    slits = [[float(v) for v in m] for m in re.findall(r'<line x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"', s)]
    return {"vb": vb, "d": d, "slits": slits}

SVG_DIR = os.path.join(REPO, "diecut-leather-20261014", "svg")
THUMBS = {f[:2]: outline(os.path.join(SVG_DIR, f)) for f in sorted(os.listdir(SVG_DIR)) if f.endswith(".svg")}
for size in ("200", "250"):
    THUMBS["01-S" + size] = outline(os.path.join(REPO, "diecut-leather-20261013", "assembly-01", f"01S-heart-strap-{size}.svg"))

WORDMARK = open(os.path.join(REPO, "brand-20261014", "logo", "svg", "oct-wordmark.svg")).read()
WORDMARK = (WORDMARK.replace('stroke="#1C1B22"', 'stroke="currentColor"').replace('fill="#1C1B22"', 'fill="currentColor"')
            .replace('fill="#FF5A36"', 'fill="var(--tomato)"').replace('<title>OCT. 26</title>', '')
            .replace('width="576" height="176"', 'class="wordmark" role="img" aria-label="OCT. 26"'))

products = []
for p in B.PRODUCTS:
    products.append(dict(
        n=p["n"], id=f"p{p['n']:02d}", name=p["name"], price=p["price"], stock=p["stock"], cost=p["cost"],
        parts=p["parts"], joints=p["joints"], extra=p["extra"], size=p["size"], who=p["who"], hook=p["hook"],
        steps=p["steps"], line=p["line"], pieces=p["pieces_txt"], hero=p["n"] in B.HEROES,
        check=pd.CHECK[p["n"]], blocker=pd.BLOCKERS.get(p["n"], ""), stage=pd.default_stage(p)))

DATA = dict(
    products=products,
    heroes=B.HEROES,
    stages=[dict(key=k, name=n, color=c, what=w) for k, n, c, w in pd.STAGES + [pd.PARKED]],
    gates=[dict(name=n, who=w, items=i) for n, w, i in pd.GATES],
    tests=[dict(key=k, name=n, how=h) for k, n, h in pd.TESTS],
    testers=pd.TESTERS,
    pieceCost=B.PIECE_COST, pieceName=B.PIECE_NAME, jointCost=B.JOINT_COST, packCost=B.PACK_COST,
    packs={k: dict(name=v[0], cost=sum(B.PACK_ITEMS[i][2] for i in v[1])) for k, v in B.PACK_PROFILE.items()},
    thumbs=THUMBS,
)

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

ROLES_HTML = "".join(
    f'<li class="role"><span class="dot" style="background:var(--{c})"></span><div><b>{esc(who)}</b> <span class="tag">{esc(title)}</span><p>{esc(what)}</p></div></li>'
    for who, c, title, what in pd.ROLES)
RULES_HTML = "".join(f"<li><b>{esc(a)}</b><p>{esc(b)}</p></li>" for a, b in pd.RULES)
PLAN_HTML = "".join(
    f'<li><time>{esc(d)}</time><div><b>{esc(t)}</b><p>{esc(x)}</p></div></li>' for d, t, x in pd.ROADMAP)
FILES_HTML = "".join(f"<li><code>{esc(f)}</code><span>{esc(w)}</span></li>" for f, w in pd.FILES)

TEMPLATE = open(os.path.join(HERE, "template.html")).read()
out = (TEMPLATE.replace("__DATA__", json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
       .replace("__WORDMARK__", WORDMARK).replace("__ROLES__", ROLES_HTML).replace("__RULES__", RULES_HTML)
       .replace("__PLAN__", PLAN_HTML).replace("__FILES__", FILES_HTML))
open(os.path.join(HERE, "index.html"), "w").write(out)
print("site/index.html", len(out), "bytes")
