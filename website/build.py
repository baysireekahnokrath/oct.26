"""The customer website oct26brand.com: home and one page per product, in the design the owner chose on 22 Oct 2026
(direction 2 "ไม่ซ้ำสักชิ้น": family-colour chapters, craft textures, painted-face DIY ideas, a 3D leather simulator).

Static files for the Cloudflare Worker (wrangler.jsonc: assets ./public). Content comes from website/catalog.py,
piece outlines from the die files (1:1 mm), the page itself from src/ (app.css, app.js, defs.svg).

    python3 website/build.py      # -> website/public

Pages are rendered in the browser by app.js. prerender.mjs then opens each page in Chromium and writes what app.js drew
into the HTML file, so search engines and chat previews read the full text without running scripts; app.js redraws the
same markup on load. Each file also carries its search title, description, canonical link, share image and JSON-LD
(Organization and WebSite on home; Product and BreadcrumbList on product pages).
"""
import datetime, hashlib, html, json, os, re, shutil, subprocess, time
from PIL import Image

import catalog as C

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "public")
SRC = os.path.join(HERE, "src")
A = os.path.join(HERE, "assets")
E = html.escape
DIES = {"01": os.path.join(REPO, "diecut-leather-20261014", "svg", "01-bear-head.svg"),
        "02": os.path.join(REPO, "diecut-leather-20261014", "svg", "02-pinwheel-4-lobe.svg"),
        "03": os.path.join(REPO, "diecut-leather-20261014", "svg", "03-capsule-cross.svg"),
        "04": os.path.join(REPO, "diecut-leather-20261014", "svg", "04-rounded-square-diagonal.svg"),
        "05": os.path.join(REPO, "diecut-leather-20261014", "svg", "05-circle.svg"),
        "07": os.path.join(A, "07-round-joint-cross.svg")}        # copied from diecut-leather-20261019
NAMES = {"01": "หมี", "02": "กังหัน", "03": "กากบาทแคปซูล", "04": "สี่เหลี่ยมมน", "05": "วงกลม", "07": "กากบาทข้อต่อวงกลม"}


def polys(d):
    """Absolute M/L/C/Z paths (all the die files use) -> closed polygons, curves sampled in 10 steps."""
    toks = re.findall(r"[MLCZ]|-?[\d.]+", d)
    out, cur, i, cmd, pt = [], [], 0, None, (0, 0)
    while i < len(toks):
        if toks[i] in "MLCZ":
            cmd = toks[i]; i += 1
            if cmd == "Z":
                if cur: out.append(cur); cur = []
                continue
        if cmd == "M":
            if cur: out.append(cur)
            pt = (float(toks[i]), float(toks[i + 1])); cur = [pt]; i += 2; cmd = "L"
        elif cmd == "L":
            pt = (float(toks[i]), float(toks[i + 1])); cur.append(pt); i += 2
        elif cmd == "C":
            c = [float(t) for t in toks[i:i + 6]]; i += 6
            for k in range(1, 11):
                t = k / 10; u = 1 - t
                cur.append((u**3*pt[0] + 3*u*u*t*c[0] + 3*u*t*t*c[2] + t**3*c[4], u**3*pt[1] + 3*u*u*t*c[1] + 3*u*t*t*c[3] + t**3*c[5]))
            pt = (c[4], c[5])
    if cur: out.append(cur)
    return [[(round(x, 2), round(y, 2)) for x, y in p] for p in out]


def shape(code):
    s = open(DIES[code]).read()
    w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    cut = re.search(r'<g id="CUT"[^>]*>(.*?)</g>', s, re.S).group(1)
    ps = [p for d in re.findall(r'<path d="([^"]+)"', cut) for p in polys(d)]
    ps.sort(key=lambda p: -len(p))
    slits = [[float(v) for v in m] for m in re.findall(r'<line x1="([\d.-]+)" y1="([\d.-]+)" x2="([\d.-]+)" y2="([\d.-]+)"', s)]
    return dict(code=code, name=NAMES[code], w=w, h=h, outline=ps[0], holes=ps[1:], slits=slits)


def logo(name):
    s = open(os.path.join(A, "logo", name + ".svg")).read()
    s = re.sub(r"<title>.*?</title>", "", s)
    s = re.sub(r' width="[\d.]+" height="[\d.]+"', "", s, count=1)
    return s.replace("<svg ", f'<svg class="lg" role="img" aria-label="OCT. 26" ', 1)


# hidden products get no page and leave the home page; sold-out ones keep their page
SHOWN = [p for p in C.PRODUCTS if p["status"] != "off"]


def data_js():
    prod = [dict(n="MX" if p["kind"] == "set" else p["code"], id=p["id"], name=p["name"], price=p["price"], size=p["size"],
                 img=p["img"], cut=p["cut"], food=p["food"], kind=p["kind"], cuts=p.get("set_cuts", []), out=p["status"] == "out")
            for p in SHOWN]
    pd = {p["id"]: dict(code=p["code"], lead=p["lead"], uses=p["uses"], photos=p["photos"], cuts=p["cuts"],
                        note=p.get("note", ""), set=p["kind"] == "set") for p in SHOWN}
    link = dict(line=C.LINE, lineId=C.LINE_ID, ig=C.IG, igHandle=C.IG_HANDLE, fb=C.FB, shopee=C.SHOPEE_NAME, shopeeUrl=C.SHOPEE)
    j = lambda v: json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    return ("// built by website/build.py from catalog.py and the die files; do not edit\n"
            f"const SH={j({c: shape(c) for c in DIES})};\nconst LOGO={j(dict(light=logo('square-light'), dark=logo('square-dark')))};\n"
            f"const PROD={j(prod)};\nconst PD={j(pd)};\nconst LINK={j(link)};\nconst BOOTH={j(C.BOOTH)};\nconst ALT={j(C.ALT)};\n")


def stamp(path):
    return hashlib.sha1(open(path, "rb").read()).hexdigest()[:8]


def page(title, desc, path, img, page_js, noscript, ld=None):
    url = C.SITE + path
    v = {f: stamp(os.path.join(OUT, "assets", f)) for f in ("app.css", "app.js", "data.js")}
    ldj = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>' if ld else ""
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}">
<link rel="icon" href="/assets/logo/square-light.svg" type="image/svg+xml"><meta name="theme-color" content="#A9442B">
<meta property="og:type" content="website"><meta property="og:locale" content="th_TH"><meta property="og:site_name" content="OCT. 26">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{C.SITE}/assets/og/{img}.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@500&family=IBM+Plex+Sans+Thai:wght@400;600&family=Jost:wght@300;400;500&display=swap">
<link rel="stylesheet" href="/assets/app.css?v={v['app.css']}">{ldj}</head><body>
{open(os.path.join(SRC, "defs.svg")).read()}
<main id="view" class="d2"><!--prerender--><noscript>{noscript}</noscript></main>
<div class="toast" id="toast" role="status" hidden></div>
<script>const PAGE={json.dumps(page_js)};</script>
<script src="/assets/data.js?v={v['data.js']}" defer></script><script src="/assets/app.js?v={v['app.js']}" defer></script>
</body></html>"""


def game_pages():
    """/game (the matching game) and /game/done (show at the booth), noindex, not in the sitemap or menu. Built ended
    after GAME["until"]; before that the browser switches to the ended view itself at that time."""
    ended = time.time() > datetime.datetime.fromisoformat(C.GAME["until"]).timestamp()
    names = {k: f"แพตเทิร์น {k} {NAMES[k]}" for k in C.GAME["cards"]}
    svgs = json.load(open(os.path.join(SRC, "game-cards.json")))
    tpl = open(os.path.join(SRC, "game.html")).read()
    os.makedirs(os.path.join(OUT, "game"), exist_ok=True)
    for kind, path, title in (("game", "game.html", "จับคู่ชิ้นหนัง"), ("done", os.path.join("game", "done.html"), "เล่นจบแล้ว")):
        show = "ended" if ended else kind
        imgs = [] if ended or kind == "game" else ["01-3"]
        s = tpl
        for k, v in {"title": title if not ended else "กิจกรรมจบแล้ว", "kind": kind, "ig": C.IG, "fb": C.FB,
                     "preload": "".join(f'<link rel="preload" as="image" href="/assets/game/{i}.webp">' for i in imgs),
                     "hide_game": "" if show == "game" else "hidden", "hide_done": "" if show == "done" else "hidden",
                     "hide_ended": "" if show == "ended" else "hidden",
                     "config": json.dumps(dict(kind=kind, cards=C.GAME["cards"], names=names, until=C.GAME["until"],
                                             svgs={k: svgs[k] for k in C.GAME["cards"]} if kind == "game" else {}), ensure_ascii=False)}.items():
            s = s.replace("{{" + k + "}}", v)
        open(os.path.join(OUT, path), "w").write(s)


def og(name, photos):
    """1200 x 630 share image: one photo cropped to fill, or several side by side."""
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#F4F0E8"); w = W // len(photos)
    for i, ph in enumerate(photos):
        p = Image.open(os.path.join(A, "img", ph + ".jpg")).convert("RGB")
        k = max(w / p.width, H / p.height); p = p.resize((round(p.width * k), round(p.height * k)), Image.LANCZOS)
        x, y = (p.width - w) // 2, (p.height - H) // 2
        im.paste(p.crop((x, y, x + w, y + H)), (i * w, 0))
    im.save(os.path.join(OUT, "assets", "og", name + ".jpg"), quality=84)


if __name__ == "__main__":
    bad = C.problems()
    if bad:
        raise SystemExit("ใช้ไม่ได้:\n" + "\n".join(bad))
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "p")); os.makedirs(os.path.join(OUT, "assets", "og"))
    for d in ("img", "cut", "logo", "js", "game"):
        shutil.copytree(os.path.join(A, d), os.path.join(OUT, "assets", d))
    shutil.copyfile(os.path.join(SRC, "app.css"), os.path.join(OUT, "assets", "app.css"))
    shutil.copyfile(os.path.join(SRC, "app.js"), os.path.join(OUT, "assets", "app.js"))
    open(os.path.join(OUT, "assets", "data.js"), "w").write(data_js())

    low, high = min(p["price"] for p in SHOWN), max(p["price"] for p in SHOWN)
    og("home", ["bears", "circles", "clover03"])
    items = "".join(f'<li><a href="/p/{p["id"]}">{E(p["name"])}</a> · {p["price"]} บาท{" · ของหมด" if p["status"] == "out" else ""}</li>' for p in SHOWN)
    shopee = f'<a href="{E(C.SHOPEE)}">Shopee</a>' if C.SHOPEE else f"Shopee ร้าน {E(C.SHOPEE_NAME)}"
    contact = f'<p>สั่งซื้อทาง LINE <a href="{C.LINE}">{C.LINE_ID}</a> · Instagram <a href="{C.IG}">{C.IG_HANDLE}</a> · {shopee}</p>'
    org = {"@type": "Organization", "@id": C.SITE + "/#org", "name": "OCT. 26", "alternateName": C.SHOPEE_NAME, "url": C.SITE + "/",
           "logo": C.SITE + "/assets/logo/square-light.png", "description": "ของใช้แฮนด์เมดจากเศษหนังวัวแท้ ทำกันเองทั้งบ้าน",
           "sameAs": [C.IG, C.FB, C.LINE] + ([C.SHOPEE] if C.SHOPEE else [])}
    site = {"@type": "WebSite", "@id": C.SITE + "/#site", "name": "OCT. 26", "url": C.SITE + "/", "inLanguage": "th", "publisher": {"@id": C.SITE + "/#org"}}
    open(os.path.join(OUT, "index.html"), "w").write(page(
        "OCT. 26 · ของใช้หนังวัวแท้แฮนด์เมดจากเศษหนัง ที่รองแก้ว ป้ายห้อยของขวัญ",
        f"งานหนังแฮนด์เมดจากเศษหนังวัวแท้ ทำกันเองทั้งบ้าน ที่รองแก้วหนัง ป้ายห้อยของขวัญ ที่เก็บสายชาร์จ {len(SHOWN)} แบบ {low}–{high} บาท"
        " ของขวัญ ของที่ระลึกองค์กร และเวิร์กช็อปแต่งชิ้นหนัง สั่งทาง LINE",
        "/", "home", {"type": "home"},
        f"<h1>OCT. 26 · our crafted things.</h1><p>ของใช้จากเศษหนังวัวแท้ ทำกันเองทั้งบ้าน</p><ul>{items}</ul>{contact}",
        {"@context": "https://schema.org", "@graph": [org, site]}))
    for p in SHOWN:
        out = p["status"] == "out"
        og(p["id"], [p["photos"][0]])
        url = f"{C.SITE}/p/{p['id']}"
        prod = {"@type": "Product", "name": p["name"], "sku": p["id"], "description": p["lead"],
                "image": [f"{C.SITE}/assets/img/{ph}.jpg" for ph in p["photos"]], "brand": {"@type": "Brand", "name": "OCT. 26"},
                "material": "หนังวัวแท้", "size": p["size"], "itemCondition": "https://schema.org/NewCondition",
                "additionalProperty": [{"@type": "PropertyValue", "name": "ความหนา", "value": "1.0–1.2 มม."}],
                "offers": {"@type": "Offer", "price": p["price"], "priceCurrency": "THB", "availability": "https://schema.org/" + ("OutOfStock" if out else "InStock"),
                           "url": url, "seller": {"@type": "Organization", "name": "OCT. 26", "url": C.SITE + "/"}}}
        crumbs = {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "หน้าแรก", "item": C.SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": p["name"], "item": url}]}
        ld = {"@context": "https://schema.org", "@graph": [prod, crumbs]}
        open(os.path.join(OUT, "p", p["id"] + ".html"), "w").write(page(
            f"{p['seo']} · OCT. 26", f"{p['lead']} · {p['price']} บาท · งานหนังแฮนด์เมดจากเศษหนังวัวแท้ · " + ("ของหมด ทัก LINE ถามรอบหน้า" if out else "สั่งทาง LINE"),
            f"/p/{p['id']}", p["id"], {"type": "product", "id": p["id"]},
            f"<h1>{E(p['name'])}</h1><p>{E(p['lead'])}</p><p>{p['price']} บาท · {E(p['size'])}" + (" · ของหมด" if out else "")
            + (" · ไม่ใช่ภาชนะใส่อาหาร" if p["food"] else "") + f"</p>{contact}<p><a href=\"/\">หน้าแรก</a></p>", ld))
    game_pages()
    open(os.path.join(OUT, "404.html"), "w").write(
        '<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>ไม่พบหน้านี้ · OCT. 26</title><link rel="icon" href="/assets/logo/square-light.svg" type="image/svg+xml">'
        '<style>body{margin:0;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;'
        'background:#A9442B;color:#F4F0E8;font-family:"IBM Plex Sans Thai",system-ui,sans-serif;text-align:center;padding:24px}'
        'a{color:#F4F0E8}.lg{width:96px}</style></head><body>' + logo("square-light") +
        '<h1 style="font-weight:500;margin:0">ไม่พบหน้านี้</h1><p>สินค้าอาจย้ายไปแล้ว <a href="/#shop">ดูของพร้อมส่งทั้งหมด</a></p></body></html>')
    # old addresses (30-product site, pattern play) -> what sells now
    red = ["/play.html / 301", "/play / 301"]
    for n in range(1, 31):
        to = f"/p/{C.OLD[n]}" if n in C.OLD and any(p["id"] == C.OLD[n] for p in SHOWN) else "/"
        red += [f"/p/{n:02d}.html {to} 301", f"/p/{n:02d} {to} 301"]
    # hidden products: their address goes home for now (302, they may come back)
    red += [f"/p/{p['id']}{x} / 302" for p in C.PRODUCTS if p["status"] == "off" for x in ("", ".html")]
    open(os.path.join(OUT, "_redirects"), "w").write("\n".join(red) + "\n")
    urls = ["/"] + [f"/p/{p['id']}" for p in SHOWN]
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{C.SITE}{u}</loc><lastmod>{datetime.date.today()}</lastmod></url>" for u in urls) + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {C.SITE}/sitemap.xml\n")
    # write the drawn pages into the HTML (needs node + the Playwright Chromium these sessions have)
    subprocess.run(["node", os.path.join(HERE, "prerender.mjs"), OUT], check=True)
    print("built home +", len(SHOWN), "product pages ->", OUT)
