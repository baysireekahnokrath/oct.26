"""One-page website preview in Brand Book v2 (22 Oct 2026). Not deployed: the live site is website/ on main.

python3 build.py -> index.html (uses img/ next to it; logos inlined from brandbook-v2/logo/svg)
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from build import PRODUCTS, CONTACT, LOGO, C, BAND  # noqa: E402

BOOTH = [("งาน", "บ้านและสวนแฟร์ Living Festival 2026"), ("โซน", "หนูทดลอง KIDS MARKET"),
         ("ที่", "อิมแพ็ค เมืองทองธานี ฮอลล์ชาเลนเจอร์ 2–3"),
         ("วัน", "23–25 ต.ค. และ 30 ต.ค.–1 พ.ย. 2569"), ("เวลา", "ศุกร์–อาทิตย์ 10:00–17:00")]
LINKS = {"IG": "https://www.instagram.com/oct.26_brand/", "FB": "https://www.facebook.com/oct26brand",
         "LINE": "https://line.me/R/ti/p/@155riuqj"}


def logo(name, w=None):
    svg = open(os.path.join(LOGO, name + ".svg")).read()
    svg = re.sub(r' width="[\d.]+" height="[\d.]+"', "", svg, count=1)
    return svg.replace("<svg ", f'<svg class="lg-{name}" ', 1)


def band():
    return '<div class="band" aria-hidden="true">' + "".join(f"<span style=\"background:{c}\"></span>" for c in BAND) + "</div>"


def photo(p, alt):
    if p == "MX":
        return '<div class="ph mx">' + "".join(f'<img src="img/{n}.jpg" alt="" loading="lazy">' for n in ("bears", "pinwheels", "squares", "circles")) + "</div>"
    return f'<div class="ph"><img src="img/{p}.jpg" alt="{alt}" loading="lazy"></div>'


def product(p):
    sku, name, spec, size, price, ph, food = p
    note = '<p class="food">ไม่ใช่ภาชนะใส่อาหาร</p>' if food else ""
    return (f'<article class="prod">{photo(ph, name)}<div class="pm"><h3>{name}</h3>'
            f'<p class="spec">{spec} · {size}</p>{note}<p class="price latin">{price} บาท</p></div></article>')


CSS = f"""
:root{{--cotton:{C['cotton']};--charcoal:{C['charcoal']};--hide:{C['hide']};--stone:{C['stone']};--leaf:{C['mom']};
--line:#DCD4C7;--muted:#6E6A64;--card:#FBF8F2;
--display:"Anuphan","IBM Plex Sans Thai",system-ui,sans-serif;--body:"IBM Plex Sans Thai",system-ui,sans-serif;--latin:"Jost",system-ui,sans-serif;color-scheme:light}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--cotton);color:var(--charcoal);font:16px/1.7 var(--body)}}
a{{color:inherit}}
.latin{{font-family:var(--latin)}}
.w{{max-width:1080px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
nav{{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--cotton) 92%,transparent);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}}
nav .w{{display:flex;align-items:center;gap:20px;height:56px}}
nav svg{{height:22px;width:auto;display:block}}
nav .sp{{flex:1}} nav a{{text-decoration:none;font-size:.95rem}}
@media(max-width:560px){{nav .opt{{display:none}}}}
h1,h2,h3{{font-family:var(--display);font-weight:600;margin:0;line-height:1.3;text-wrap:balance}}
h1{{font-size:clamp(2rem,6vw,3.2rem)}} h2{{font-size:1.5rem}} h3{{font-size:1.15rem;font-weight:500}}
p{{margin:0}}
.band{{display:flex;height:4px;width:120px}} .band span{{flex:1}}
.eyebrow{{font-family:var(--latin);font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
.hero{{padding:56px 0 40px;display:grid;gap:28px;grid-template-columns:1.1fr 1fr;align-items:center}}
.hero .t{{display:grid;gap:16px}} .hero .lead{{font-size:1.1rem;max-width:34ch}}
.hero img{{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}}
.btn{{display:inline-block;justify-self:start;background:var(--charcoal);color:var(--cotton);text-decoration:none;padding:10px 22px;font-size:.95rem}}
@media(max-width:760px){{.hero{{grid-template-columns:1fr;padding-top:32px}}}}
section{{padding:56px 0;border-top:1px solid var(--line);display:grid;gap:24px}}
.grid{{display:grid;gap:28px 20px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}}
.prod{{display:grid;gap:12px;align-content:start}}
@media(max-width:560px){{.grid{{grid-template-columns:1fr 1fr;gap:24px 12px}} h3{{font-size:1rem}}}}
.ph{{aspect-ratio:4/5;overflow:hidden;background:var(--card)}}
.ph img{{width:100%;height:100%;object-fit:cover;display:block}}
.mx{{display:grid;grid-template-columns:1fr 1fr;gap:4px}}
.pm{{display:grid;gap:2px}} .spec{{color:var(--muted);font-size:.9rem}} .food{{color:var(--stone);font-size:.8rem}}
.price{{font-weight:500;font-size:1.1rem;margin-top:4px}}
.story{{display:grid;gap:32px;grid-template-columns:1fr 1fr;align-items:start}}
.story .tx{{display:grid;gap:14px;max-width:60ch}}
.story img{{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}}
@media(max-width:760px){{.story{{grid-template-columns:1fr}}}}
dl{{margin:0;display:grid;grid-template-columns:auto 1fr;gap:8px 20px}}
dt{{color:var(--muted)}} dd{{margin:0}}
.two{{display:grid;gap:32px;grid-template-columns:1fr 1fr}}
@media(max-width:760px){{.two{{grid-template-columns:1fr}}}}
ul.care{{margin:0;padding-left:1.2em;display:grid;gap:6px}}
.contact{{display:flex;gap:28px;align-items:center;flex-wrap:wrap}}
.contact ul{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}
.contact b{{font-family:var(--latin);font-weight:500;display:inline-block;width:48px;color:var(--muted)}}
.qr{{width:120px;height:120px;display:block}}
footer{{background:var(--charcoal);color:var(--cotton);padding:40px 0 0;margin-top:24px}}
footer .w{{display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding-bottom:32px}}
footer svg{{width:72px;height:72px;display:block}}
footer .band{{width:100%;height:8px}}
"""

HEAD = """<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OCT. 26</title><meta name="description" content="OCT. 26 ของใช้จากหนังวัวแท้ เศษหนังจากโรงงาน ทำกันเองทั้งบ้าน">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@500;600&family=IBM+Plex+Sans+Thai:wght@400;600&family=Jost:wght@400;500&display=swap">
"""


def page():
    prods = "".join(product(p) for p in PRODUCTS)
    booth = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in BOOTH)
    contact = "".join(f'<li><b>{k}</b><a href="{LINKS[k]}">{v}</a></li>' for k, v in CONTACT)
    return f"""{HEAD}<style>{CSS}</style></head><body>
<nav><div class="w"><a href="#top" aria-label="OCT. 26">{logo("line-light")}</a><span class="sp"></span>
<a href="#products">สินค้า</a><a class="opt" href="#story">เรื่องของเรา</a><a href="#booth">บูธ</a><a href="#contact">ติดต่อ</a></div></nav>
<main class="w" id="top">
<div class="hero"><div class="t"><p class="eyebrow">SOI. 02 · รอบผลิตแรก</p>
<h1>หนังแท้จากเศษหนัง<br>ทำกันเองทั้งบ้าน</h1>
<p class="lead">ของใช้ชิ้นเล็กจากหนังวัวแท้ที่เหลือจากโรงงาน ทุกชิ้นสีไม่ซ้ำกัน</p>{band()}
<a class="btn" href="#products">ดูสินค้า</a></div>
<img src="img/squares.jpg" alt="ที่รองแก้วหนังสี่เหลี่ยมหลายสี"></div>

<section id="products"><div style="display:grid;gap:8px"><p class="eyebrow">Products</p><h2>สินค้า 7 แบบ</h2>
<p class="spec">ชื่อสินค้าคือเลขแพตเทิร์นกับหน้าที่ ราคาบาท</p></div>
<div class="grid">{prods}</div></section>

<section id="story"><div class="story"><div class="tx"><p class="eyebrow">Our story</p><h2>เรียบข้างนอก บ้านอยู่ข้างใน</h2>
<p>OCT. 26 คือวันเกิดของแม่ แบรนด์จึงใช้ชื่อนี้ และหน้าตาของแบรนด์เป็นแบบที่แม่ชอบ เรียบ เท่ ตั้งใจ</p>
<p>เราทำของใช้จากเศษหนังวัวแท้ที่เหลือจากโรงงาน พ่อออกแบบแพตเทิร์นและบล็อกตัด ทั้งบ้านช่วยกันคัดหนัง แพ็ก และขาย ผิวและขอบหนังปล่อยตามธรรมชาติ</p>
<p>คนในบ้านห้าคนมีสีของตัวเอง ห้าสีนี้ซ่อนอยู่ในรายละเอียด หลังป้าย ในการ์ดในซอง คนที่พลิกดูถึงจะเจอ</p>{band()}</div>
<img src="img/02.jpg" alt="ชิ้นหนังแพตเทิร์น 02 หลายสี" loading="lazy"></div></section>

<section id="booth"><div class="two"><div style="display:grid;gap:16px"><p class="eyebrow">Booth</p><h2>มาเจอกันที่บูธ</h2><dl>{booth}</dl></div>
<div style="display:grid;gap:16px;align-content:start"><p class="eyebrow">Care</p><h2>ดูแลง่าย</h2><ul class="care">
<li>เช็ดด้วยผ้าแห้ง เลี่ยงน้ำและแดดจัด</li><li>หนังจะเข้มขึ้นและนุ่มขึ้นตามเวลา</li>
<li>ที่รองแก้วไม่ใช่ภาชนะใส่อาหาร</li></ul></div></div></section>

<section id="contact"><div style="display:grid;gap:8px"><p class="eyebrow">Contact</p><h2>ติดต่อและสั่งซื้อ</h2></div>
<div class="contact"><ul>{contact}</ul><img class="qr" src="img/line-qr.png" alt="QR LINE @155riuqj"></div></section>
</main>
<footer><div class="w">{logo("square-dark")}<p class="latin">our crafted things. · oct26brand.com</p></div>{band()}</footer>
</body></html>"""


if __name__ == "__main__":
    open(os.path.join(HERE, "index.html"), "w").write(page())
    print("index.html")
