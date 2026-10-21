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
    booth=[dict(sku=s, n=n) for s, n in pd.BOOTH_SKUS], statusDate=pd.STATUS_DATE, no06=pd.NO_06, jointsOpen=pd.JOINTS_OPEN,
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

# ---------------------------------------------------------------- tab "ไขว้ 3D" (data from ../cross3d/catalogue.py)
X3D = json.load(open(os.path.join(ROOT, "cross3d", "x3d.json")))
for it in X3D["items"]: it.pop("spec", None)
CROSS_JS = open(os.path.join(HERE, "cross3d.js")).read().replace("__X3D__", json.dumps(X3D, ensure_ascii=False, separators=(",", ":")))
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
from geom import PIECES as XP, NAME as XNAME
import math as _m
tabs = [(c, k, _m.dist(f["a"], f["b"])) for c in sorted(XP) for k, f in XP[c]["feats"].items() if f["kind"] == "tab"]
slits = [(c, k, _m.dist(f["a"], f["b"])) for c in sorted(XP) for k, f in XP[c]["feats"].items() if f["kind"] == "slit"]
tab_n = {}; slit_n = {}
for c, _, L in tabs: tab_n[c] = L
for c, _, L in slits: slit_n[c] = L
head = "".join(f"<th>ร่อง {c}<br><span class='small muted'>{slit_n[c]:.1f}</span></th>" for c in sorted(slit_n))
rows = ""
for c in sorted(tab_n):
    cells = ""
    for d in sorted(slit_n):
        gap = slit_n[d] - tab_n[c]
        cells += f"<td class='ok'>✓ {gap:.1f}</td>" if 0 <= gap <= 1.0 else "<td class='muted'>–</td>"
    rows += f"<tr><th>ปีก {c} {XNAME[c]}<br><span class='small muted'>{tab_n[c]:.1f}</span></th>{cells}</tr>"
X_COMPAT = f"<table class='compat num'><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table>"
xi = X3D["items"]
X_STATS = "".join(f'<div class="stat"><span class="small muted">{a}</span><b>{b}</b><span class="small muted">{c}</span></div>' for a, b, c in [
    ("แบบที่รูปทรงผ่าน", len(xi), f"ลองจริงแล้วหลุด {sum(i.get('real') == 'fail' for i in xi)} · ใช้ 06 ที่ยังไม่ได้ตัด {sum(i.get('no06', False) for i in xi)}"),
    ("บล็อกใหม่ที่ต้องสั่ง", 0, "ใช้บล็อก 01–06 ที่มีอยู่"),
    ("ชิ้นต่อแบบ", f"{min(len(i['pieces']) for i in xi)}–{max(len(i['pieces']) for i in xi)}", f"ล็อก {min(i['locks'] for i in xi)}–{max(i['locks'] for i in xi)} จุด"),
    ("กำไรขั้นต้นเฉลี่ย", f"{round(sum(i['margin'] for i in xi) / len(xi) * 100)}%", f"ต่ำสุด {round(min(i['margin'] for i in xi) * 100)}%"),
])

# ---------------------------------------------------------------- tab "ชิ้นเดียว 50" (data from ../single50/build.py)
S50 = json.load(open(os.path.join(ROOT, "single50", "single50.json")))
S50_JS = open(os.path.join(HERE, "single50.js")).read().replace("__S50__", json.dumps(S50, ensure_ascii=False, separators=(",", ":")))
si = S50["items"]
S_STATS = "".join(f'<div class="stat"><span class="small muted">{a}</span><b>{v}</b><span class="small muted">{c}</span></div>' for a, v, c in [
    ("ไอเดียชิ้นเดียว", len(si), f"{len({i['group'] for i in si})} กลุ่ม"),
    ("ทำได้กับหนังที่มี", sum(not i["load"] for i in si), f"อีก {sum(i['load'] for i in si)} แบบรับแรง รอหนัง 2 มม."),
    ("ใช้ชิ้น 07", sum(i["uses07"] for i in si), "07 มี 200 ชิ้น ยังไม่มีสินค้า"),
    ("กำไรขั้นต้น", f"{round(min(i['margin'] for i in si) * 100)}–{round(max(i['margin'] for i in si) * 100)}%", "ต้นทุนชิ้นหนังตามเอกสารสถานะ"),
])

TEMPLATE = open(os.path.join(HERE, "template.html")).read()
WEB = "--web" in sys.argv            # pd.oct26brand.com (Cloudflare Pages) instead of the claude.ai Artifact
ADAPTER = open(os.path.join(HERE, "adapters", "web.js" if WEB else "artifact.js")).read()
out = (TEMPLATE.replace("__DB_ADAPTER__", ADAPTER).replace("__DATA__", json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
       .replace("__WORDMARK__", WORDMARK).replace("__ROLES__", ROLES_HTML).replace("__RULES__", RULES_HTML)
       .replace("__PLAN__", PLAN_HTML).replace("__FILES__", FILES_HTML)
       .replace("__X_STATS__", X_STATS).replace("__X_COMPAT__", X_COMPAT).replace("__CROSS3D_JS__", CROSS_JS)
       .replace("__S_STATS__", S_STATS).replace("__S50_JS__", S50_JS))
if WEB:
    out = out.replace("<title>ฝ่ายพัฒนาสินค้า OCT. 26</title>", "<title>OCT. 26 PD · ระบบงานฝ่ายพัฒนาสินค้า</title>")
    cut = out.index('<div class="wrap">')
    head_part = out[:cut].replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    out = ('<!doctype html><html lang="th"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           '<meta name="robots" content="noindex,nofollow"><meta name="color-scheme" content="light dark">'
           '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Ccircle cx=%2216%22 cy=%2216%22 r=%2213%22 fill=%22none%22 stroke=%22%231C1B22%22 stroke-width=%225%22/%3E%3Ccircle cx=%2226%22 cy=%2226%22 r=%224%22 fill=%22%23FF5A36%22/%3E%3C/svg%3E">'
           '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>'
           + head_part + '</head><body>' + out[cut:] + '</body></html>')
    dest = os.path.join(REPO, "pd-os", "public", "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
else:
    dest = os.path.join(HERE, "index.html")
open(dest, "w").write(out)
print(os.path.relpath(dest, REPO), len(out), "bytes")
