"""The customer website: home with the catalogue, one page per product, and the pattern play.

Static files for Cloudflare Pages (build command: none, output directory: website/public).
Everything reads from brand-20261014/brand.py (products, prices, story, booth, accounts) and uses the
brand CSS from brand-20261014/site/build.py, so the site follows the CI the same way every brand page does.

python3 website/build.py -> website/public/ (the site) and website/preview/index.html (claude.ai preview page)
"""
import base64, html, importlib.util, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BRAND_DIR = os.path.join(REPO, "brand-20261014")
sys.path.insert(0, BRAND_DIR)
import brand as B


def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


S = _load("brand_site", os.path.join(BRAND_DIR, "site", "build.py"))
PLAY = _load("play_build", os.path.join(REPO, "play-20261021", "build.py"))
E = html.escape
OUT = os.path.join(HERE, "public")
PREVIEW = os.path.join(HERE, "preview")

SITE_URL = "https://oct26.pages.dev"      # change if the Cloudflare project gets another name or a domain
H = B.BRAND["handle"]
ORDER = f"https://ig.me/m/{H}"            # opens an Instagram chat with the shop
HIDE = set()                              # product numbers to keep off the site (a prototype that failed its test)
PRODUCTS = [p for p in B.PRODUCTS if p["n"] not in HIDE]
COLL = {"soi2": "SOI. 02", "love": "ห้าหมี Love"}

SITE_CSS = """
:root{--mat:#EFE4D6;--matline:#E2D3C1}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--mat:#2A2833;--matline:#3A3846}}
:root[data-theme="dark"]{--mat:#2A2833;--matline:#3A3846}
.site{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line);
  margin:0 calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:var(--s3) max(16px,env(safe-area-inset-left,0px))}
.site .in{max-width:987px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:var(--s3)}
.site .mark{display:block;width:144px}.site .mark svg{width:100%;height:auto;display:block}
.site nav{display:flex;gap:var(--s2);overflow-x:auto;scrollbar-width:none;max-width:100%}
.site nav a{flex:none;font-family:var(--display);font-size:15px;text-decoration:none;color:var(--ink);background:var(--chip);
  border-radius:var(--s4);padding:var(--s1) var(--s3)}
.site .mark svg.mark-dark{display:none}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .site .mark svg.mark-light{display:none}:root:not([data-theme="light"]) .site .mark svg.mark-dark{display:block}}
:root[data-theme="dark"] .site .mark svg.mark-light{display:none}:root[data-theme="dark"] .site .mark svg.mark-dark{display:block}
main{padding-top:var(--s5)}
.intro{display:flex;flex-direction:column;gap:var(--s3)}
.row{display:flex;flex-wrap:wrap;gap:var(--s2);align-items:center}
.stack{display:flex;flex-direction:column;gap:var(--s3)}
.label{font-family:var(--display);font-size:14px;color:var(--muted)}
button,.btn{font-family:var(--display);font-size:15px;border:1px solid var(--line);background:var(--chip);color:var(--ink);
  border-radius:var(--s4);padding:var(--s2) var(--s4);cursor:pointer;min-height:44px;text-decoration:none;
  display:inline-flex;align-items:center;justify-content:center;gap:var(--s2)}
button:hover,.btn:hover{border-color:var(--cobalt)}
button:disabled{opacity:.4;cursor:default;border-color:var(--line)}
button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.primary{background:var(--cobalt);color:var(--on-accent);border-color:var(--cobalt)}
.order{background:var(--tomato);color:#FFFFFF;border-color:var(--tomato)}
a:focus-visible,button:focus-visible{outline:3px solid var(--tomato);outline-offset:2px}
.hero{display:grid;gap:var(--s5);grid-template-columns:minmax(0,1fr);align-items:center}
@media (min-width:760px){.hero{grid-template-columns:minmax(0,1.618fr) minmax(0,1fr)}}
.hero h1{font-size:clamp(var(--t3),8vw,53.3px)}
.hero .pic{border-radius:var(--s4);overflow:hidden;border:1px solid var(--line)}
.booth{background:var(--cobalt);color:#FFFFFF;border-radius:var(--s4);padding:var(--s4);display:flex;flex-direction:column;gap:var(--s2)}
.booth .eyebrow{color:#FFC23C}.booth a{color:#FFFFFF}
.shop{display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fill,minmax(144px,1fr))}
.shop>a{min-width:0;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;gap:var(--s1)}
.shop img{border-radius:var(--s3);border:1px solid var(--line);aspect-ratio:4/5;object-fit:cover;width:100%}
.shop .n{font-family:var(--display);font-size:15px;line-height:1.3}
.price{font-family:var(--logo);font-weight:500;color:var(--heart)}
.fb{font-family:"Mitr",var(--display)}
.coll{display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fit,minmax(233px,1fr))}
.coll .paper{aspect-ratio:5/3}
.prod{display:grid;gap:var(--s5);grid-template-columns:minmax(0,1fr)}
@media (min-width:760px){.prod{grid-template-columns:minmax(0,1fr) minmax(0,1.618fr);align-items:start}}
.prod img{border-radius:var(--s4);border:1px solid var(--line)}
.prod .big{font-size:var(--t3)}
.pager{display:flex;justify-content:space-between;gap:var(--s3);flex-wrap:wrap}
footer.site-foot{margin-top:var(--s7);border-top:1px solid var(--line);padding-top:var(--s5);display:flex;flex-direction:column;gap:var(--s3)}
footer.site-foot .tag{width:34px}
"""


def logo_svg(f, cls=""):
    s = open(os.path.join(BRAND_DIR, "logo", "svg", f)).read()
    s = re.sub(r'<title>.*?</title>', '', s)
    s = re.sub(r' width="[\d.]+" height="[\d.]+"', '', s, count=1)
    return s.replace("<svg ", f'<svg class="{cls}" role="img" aria-label="OCT. 26" ', 1)


def head(title, desc, base, path="", img="assets/og.png", jsonld=None):
    url = SITE_URL + "/" + path
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return (f'<!doctype html><html lang="th"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{E(title)}</title><meta name="description" content="{E(desc)}">'
            f'<link rel="icon" href="{base}assets/oct-mark.svg" type="image/svg+xml"><link rel="canonical" href="{url}">'
            f'<meta property="og:type" content="website"><meta property="og:locale" content="th_TH">'
            f'<meta property="og:site_name" content="OCT. 26"><meta property="og:title" content="{E(title)}">'
            f'<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">'
            f'<meta property="og:image" content="{SITE_URL}/{img}"><meta name="twitter:card" content="summary_large_image">'
            f'{S.FONT_LINK}<style>{S.CSS}{SITE_CSS}</style>{ld}</head><body>')


def header(base):
    return (f'<header class="site"><div class="in"><a class="mark" href="{base}index.html" aria-label="OCT. 26 หน้าแรก">'
            f'{logo_svg("oct-wordmark.svg", "mark-light")}{logo_svg("oct-wordmark-reverse.svg", "mark-dark")}</a>'
            f'<nav aria-label="เมนู"><a href="{base}index.html#shop">สินค้า</a><a href="{base}play.html">ต่อลาย</a>'
            f'<a href="{base}index.html#booth">ออกบูธ</a><a href="{base}index.html#follow">ติดตาม</a></nav></div></header>')


def footer(base):
    so = B.SOCIAL
    return (f'<footer class="site-foot"><img class="tag" src="{base}assets/oct-mark.svg" alt="ป้ายห้อย 26">'
            f'<p><b>OCT. 26</b> · {E(B.BRAND["tag_en"])} {E(B.BRAND["tag_th"])}</p>'
            f'<p class="cap">ทำกันเองทั้งบ้าน พ่อ แม่ และลูกสามคน · สั่งซื้อและสอบถามทางไอจี @{H}</p>'
            f'<p class="row"><a href="{so["instagram"]}" target="_blank" rel="noopener">Instagram</a>'
            f'<a href="{so["facebook"]}" target="_blank" rel="noopener">Facebook</a>'
            f'<a href="{so["youtube"]}" target="_blank" rel="noopener">YouTube</a></p>'
            f'<p class="cap">© 2569 OCT. 26</p></footer>')


def coll_label(p):
    return '<span class="fb">ห้าหมี</span> Love' if p["coll"] == "love" else "SOI. 02"


def card(p, base):
    return (f'<a href="{base}p/{p["n"]:02d}.html" data-coll="{p["coll"]}">'
            f'<img src="{base}assets/thumbs/{p["n"]:02d}.jpg" alt="{E(p["name"])}" loading="lazy" width="360" height="450">'
            f'<span class="cap">{coll_label(p)}</span><span class="n">{E(p["name"])}</span>'
            f'<span class="price">{p["price"]} บาท</span></a>')


FILTER_JS = """<script>
document.querySelectorAll('[data-f]').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('[data-f]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
  document.querySelectorAll('.shop>a').forEach(a=>a.hidden=b.dataset.f!=='all'&&a.dataset.coll!==b.dataset.f);}));
const bo=document.getElementById('booth');if(bo&&Date.now()>Date.parse(bo.dataset.until+'T23:59:59+07:00'))bo.hidden=true;
</script>"""


def home(base=""):
    bo, so = B.BOOTH, B.SOCIAL
    cards = "".join(card(p, base) for p in PRODUCTS)
    low = min(p["price"] for p in PRODUCTS)
    n_soi, n_love = sum(p["coll"] == "soi2" for p in PRODUCTS), sum(p["coll"] == "love" for p in PRODUCTS)
    desc = f"{B.BRAND['line']} · SOI. 02 และห้าหมี FIVE BEARS · เริ่ม {low} บาท"
    body = f"""{header(base)}<div class="wrap"><main>
<section class="hero" style="padding-top:0"><div class="intro"><span class="eyebrow">{E(B.BRAND['tag_en'])}</span>
<h1>{E(B.BRAND['tag_th'])}</h1><p class="lead">{E(B.BRAND['line'])}</p>
<div class="row"><a class="btn primary" href="#shop">ดูสินค้า {len(PRODUCTS)} แบบ</a><a class="btn" href="{base}play.html">ลองต่อลาย</a></div></div>
<a class="pic" href="{base}play.html"><img src="{base}assets/play.png" alt="ลายที่ต่อจากชิ้นหนังกังหันสองสี" width="540" height="540"></a></section>

<section id="booth" data-until="{bo['until']}"><div class="booth"><span class="eyebrow">ออกบูธ</span>
<h2>เจอกันที่{E(bo['fair'])}</h2>
<p>โซน{E(bo['zone'])} · {E(bo['place'])} {E(bo['hall'])}<br>{E(bo['weekends'][0])} และ {E(bo['weekends'][1])} · {E(bo['hours'])} · เข้างานฟรี</p>
<p>มี DIY leather craft ให้ลองต่อหนังด้วยมือตัวเอง ลูก ๆ อยู่ที่บูธคอยสอน</p></div></section>

<section id="shop"><span class="eyebrow">สินค้า</span><h2>ของใช้จากเศษหนังแท้</h2>
<p class="cap">สีและลายแต่ละชิ้นต่างกันเล็กน้อย เพราะทำจากเศษหนังจริง สั่งซื้อทางไอจี เราตอบยืนยันของก่อนทุกครั้ง</p>
<div class="row" role="group" aria-label="กรองตามคอลเลกชัน"><button type="button" data-f="all" aria-pressed="true">ทั้งหมด</button>
<button type="button" data-f="soi2" aria-pressed="false">SOI. 02</button><button type="button" data-f="love" aria-pressed="false"><span class="fb">ห้าหมี</span>&nbsp;Love</button></div>
<div class="shop">{cards}</div></section>

<section id="story"><span class="eyebrow">เรื่องของเรา</span><h2>26 ตุลาคม</h2>
<p class="lead">{E(B.STORY_SHORT)}</p>
<div class="coll"><div class="card stack"><div class="paper"><img src="{base}assets/soi2-sign.svg" alt="ป้ายคอลเลกชัน SOI. 02"></div>
<h3>SOI. 02</h3><p class="cap">ของใช้ทุกวัน {n_soi} แบบ จากบ้านในซอย 2 ที่ทุกอย่างเริ่มต้น</p></div>
<div class="card stack"><div class="paper"><img src="{base}assets/love-badge.svg" alt="ป้ายคอลเลกชัน Love ของห้าหมี"></div>
<h3><span class="fb">ห้าหมี</span> FIVE BEARS · Love</h3><p class="cap">หัวหมีกับสายหัวใจ {n_love} แบบ หมีห้าตัวคือคนห้าคนในบ้าน</p></div></div></section>

<section id="follow"><span class="eyebrow">ติดตาม</span><h2>@{E(H)}</h2>
<p class="cap">ลงคลิปวิธีต่อหนังทุกสัปดาห์ สั่งซื้อ สั่งทำเป็นชุด และของชำร่วย ทักไอจีได้เลย</p>
<div class="row"><a class="btn order" href="{ORDER}" target="_blank" rel="noopener">ทักไอจี</a>
<a class="btn" href="{so['instagram']}" target="_blank" rel="noopener">Instagram</a>
<a class="btn" href="{so['facebook']}" target="_blank" rel="noopener">Facebook</a>
<a class="btn" href="{so['youtube']}" target="_blank" rel="noopener">YouTube</a></div></section>
</main>{footer(base)}</div>{FILTER_JS}"""
    return desc, body


def product(p, prev, nxt, base="../"):
    pieces = E(p["pieces_txt"]) + (" + " + E(p["extra"][0]) if p["extra"] else "")
    steps = "".join(f"<li>{E(s)}</li>" for s in p["steps"])
    ask = f"สนใจ #{p['n']:02d} {p['name']} {p['price']} บาท"
    title = f"{p['name']} · OCT. 26"
    desc = f"{p['hook']} · {p['name']} {p['price']} บาท · {p['line']} · หนังแท้จากเศษหนัง"
    img = f"assets/posters/{p['n']:02d}.png"
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "image": f"{SITE_URL}/{img}",
          "description": p["hook"], "brand": {"@type": "Brand", "name": "OCT. 26"}, "sku": f"OCT26-{p['n']:02d}",
          "offers": {"@type": "Offer", "price": p["price"], "priceCurrency": "THB", "availability": "https://schema.org/InStock",
                     "url": f"{SITE_URL}/p/{p['n']:02d}.html"}}
    body = f"""{header(base)}<div class="wrap"><main>
<div class="prod"><img src="{base}{img}" alt="วิธีต่อ{E(p['name'])}" width="1080" height="1350">
<div class="stack"><span class="eyebrow">{coll_label(p)}</span><h1>{E(p['name'])}</h1>
<p class="lead">{E(p['hook'])}</p><p class="price big">{p['price']} บาท</p>
<div class="row"><a class="btn order" href="{ORDER}" target="_blank" rel="noopener">สั่งทางไอจี</a>
<a class="btn" href="{base}play.html">ลองต่อลาย</a></div>
{S.copybox("ask", ask, "ส่งข้อความนี้ในแชท")}
<div class="tbl"><table><tbody>
<tr><th>ขนาด</th><td>{E(p['size'])}</td></tr><tr><th>ชิ้นหนัง</th><td>{pieces}</td></tr>
<tr><th>เหมาะกับ</th><td>{E(p['who'])}</td></tr><tr><th>วัสดุ</th><td>เศษหนังวัวแท้ สีและลายแต่ละชิ้นไม่ซ้ำกัน</td></tr></tbody></table></div>
<h2 style="font-size:var(--t2)">วิธีต่อ</h2><ol>{steps}</ol>
<p class="cap">ดูแล: เช็ดด้วยผ้าแห้ง เลี่ยงน้ำและแดดจัด</p></div></div>
<nav class="pager" aria-label="สินค้าอื่น" style="margin-top:var(--s5)">
<a href="{prev['n']:02d}.html">← {E(prev['name'])}</a><a href="{base}index.html#shop">สินค้าทั้งหมด</a><a href="{nxt['n']:02d}.html">{E(nxt['name'])} →</a></nav>
</main>{footer(base)}</div>{S.COPY_JS}"""
    return title, desc, img, ld, body


def play(base=""):
    shapes = [PLAY.shape(c) for c in PLAY.FILES]
    word = base64.b64encode(open(os.path.join(BRAND_DIR, "logo", "svg", "oct-wordmark-reverse.svg"), "rb").read()).decode()
    t = open(os.path.join(HERE, "play.html")).read()
    t = (t.replace("/*SHAPES*/[]", json.dumps(shapes, ensure_ascii=False)).replace("{{WORDMARK}}", "data:image/svg+xml;base64," + word)
          .replace("{{HANDLE}}", H).replace("{{ORDER}}", ORDER))
    return f'{header(base)}<div class="wrap"><main>{t}</main>{footer(base)}</div>'


def assets():
    a = os.path.join(OUT, "assets")
    for d in ("posters", "thumbs"):
        os.makedirs(os.path.join(a, d), exist_ok=True)
    for f in ("oct-mark.svg", "soi2-sign.svg", "love-badge.svg"):
        shutil.copyfile(os.path.join(BRAND_DIR, "logo", "svg", f), os.path.join(a, f))
    shutil.copyfile(os.path.join(BRAND_DIR, "logo", "png", "cover-facebook-1640x624.png"), os.path.join(a, "og.png"))
    for p in PRODUCTS:
        shutil.copyfile(os.path.join(BRAND_DIR, "posters", "png", f"{p['n']:02d}-post.png"), os.path.join(a, "posters", f"{p['n']:02d}.png"))
        shutil.copyfile(os.path.join(BRAND_DIR, "posters", "thumb", f"{p['n']:02d}.jpg"), os.path.join(a, "thumbs", f"{p['n']:02d}.jpg"))
    shot = os.path.join(HERE, "play.png")              # a still of the pattern play for the home hero (render.mjs makes it)
    if os.path.exists(shot):
        shutil.copyfile(shot, os.path.join(a, "play.png"))


if __name__ == "__main__":
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "p")); os.makedirs(PREVIEW, exist_ok=True)
    assets()
    desc, body = home()
    open(os.path.join(OUT, "index.html"), "w").write(head("OCT. 26 · our crafted things.", desc, "") + body + "</body></html>")
    # the claude.ai preview wraps its page in its own document, so it gets the same page without the outer tags
    pv = head("OCT. 26 · our crafted things.", desc, "")
    pv = pv.split("<head>", 1)[1].replace("</head><body>", "")
    open(os.path.join(PREVIEW, "index.html"), "w").write(pv + body)
    for i, p in enumerate(PRODUCTS):
        prev, nxt = PRODUCTS[i - 1], PRODUCTS[(i + 1) % len(PRODUCTS)]
        title, d, img, ld, b = product(p, prev, nxt)
        open(os.path.join(OUT, "p", f"{p['n']:02d}.html"), "w").write(head(title, d, "../", f"p/{p['n']:02d}.html", img, ld) + b + "</body></html>")
    open(os.path.join(OUT, "play.html"), "w").write(
        head("ต่อลาย · OCT. 26", "ลากชิ้นหนังจริง 6 แบบมาต่อเป็นลายใหม่ หมุน เปลี่ยนสี แล้วดูลายที่ต่อซ้ำ", "", "play.html") + play() + "</body></html>")
    open(os.path.join(OUT, "404.html"), "w").write(head("ไม่พบหน้านี้ · OCT. 26", "ไม่พบหน้านี้", "/") + header("/")
        + '<div class="wrap"><main><h1>ไม่พบหน้านี้</h1><p><a href="/index.html">กลับหน้าแรก</a></p></main></div></body></html>')
    urls = ["", "play.html"] + [f"p/{p['n']:02d}.html" for p in PRODUCTS]
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(f"<url><loc>{SITE_URL}/{u}</loc></url>" for u in urls) + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("built", len(PRODUCTS), "product pages ->", OUT)
