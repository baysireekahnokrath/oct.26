"""Apply Brand Book v2 to the brand's working files (22 Oct 2026).

Social: profile 1080, Facebook cover 1640 x 624, Shopee banner 1200 x 600, seven product cards 1080 x 1350 from real photos.
Print (PDF, A4, 100%): hang tags 55 x 89 front and back, insert cards 89 x 55 front and back, 34 mm square stickers,
booth price sign A4 landscape.

python3 build.py  -> html/*.html and jobs.json;  node render.cjs -> social/*.png and print/*.pdf
"""
import base64, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, "..", "brand-20261014", "brandbook-v2")
sys.path.insert(0, BOOK)
from palette import C, BAND

FONTS = os.path.join(HERE, "..", "brand-20261014", "fonts")
LOGO = os.path.join(BOOK, "logo", "svg")
PH = os.path.join(HERE, "photos")

PRODUCTS = [  # SKU, name, spec, size, price, photo, food note
    ("OC-01-22", "01 ที่รองแก้ว", "หนังวัวแท้จากเศษหนัง", "10.4 ซม.", 59, "bears", True),
    ("OC-01-01", "01 ที่เก็บสายชาร์จ", "หนังวัวแท้จากเศษหนัง", "10.4 ซม.", 59, "bear01-close", False),
    ("OC-02-24", "02 ที่รองแก้ว", "หนังวัวแท้จากเศษหนัง", "9 ซม.", 49, "die02", True),
    ("OC-03-26", "03 ป้ายห้อยของขวัญ", "หนังวัวแท้จากเศษหนัง", "9 ซม.", 39, "clover03", False),
    ("OC-04-27", "04 ที่รองแก้ว", "หนังวัวแท้จากเศษหนัง", "9 ซม.", 49, "squares", True),
    ("OC-05-28", "05 ที่รองแก้ว", "หนังวัวแท้จากเศษหนัง", "9 ซม.", 49, "circles", True),
    ("OC-MX-29", "ชุดที่รองแก้ว 01 · 02 · 04 · 05", "4 ชิ้น 4 แบบ คละสี", "9–10.4 ซม.", 179, "MX", True),
]
CONTACT = [("IG", "@oct.26_brand"), ("FB", "oct26brand"), ("LINE", "@155riuqj")]

def logo(name, size):
    svg = open(os.path.join(LOGO, name + ".svg")).read()
    return re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{size}" height="{size}"', svg, count=1)

def band():
    return "".join(f'<span style="background:{c}"></span>' for c in BAND)

def img(name):
    return "file://" + os.path.join(PH, name + (".jpg" if name != "line-qr" else ".png"))

def photo(p, cls="ph"):
    if p == "MX":
        return f'<div class="{cls} mx">' + "".join(f'<div style="background-image:url({img(n)})"></div>' for n in ("bears", "die02", "squares", "circles")) + "</div>"
    return f'<div class="{cls}" style="background-image:url({img(p)})"></div>'

BASE_CSS = f"""
@font-face{{font-family:Jost;src:url(file://{FONTS}/alt/Jost-Regular.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url(file://{FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Anuphan;font-weight:500;src:url(file://{FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Plex;src:url(file://{FONTS}/IBMPlexSansThai-Regular.ttf)}}
@font-face{{font-family:Plex;font-weight:600;src:url(file://{FONTS}/IBMPlexSansThai-SemiBold.ttf)}}
*{{box-sizing:border-box}} html,body{{margin:0}}
body{{font-family:Plex,sans-serif;color:{C['charcoal']};background:{C['cotton']}}}
.latin{{font-family:Jost}} .band{{display:flex}} .band span{{flex:1}}
"""

def doc(css, body, page=None):
    pg = f"@page{{size:{page};margin:0}}" if page else ""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE_CSS}{pg}{css}</style></head><body>{body}</body></html>"

# ---------------------------------------------------------------- social
def card(p, h=1350):
    """Post 1080 x 1350, or story 1080 x 1920 (h=1920): the photo takes the extra height."""
    sku, name, spec, size, price, ph, food = p
    story = h > 1350  # keep clear of the app's top and bottom bars (about 250 px each)
    top, photo_h, price_b = (200, 1080, 300) if story else (64, 860, 96)
    css = f"""
.c{{width:1080px;height:{h}px;background:{C['cotton']};position:relative;padding:{top}px 64px 0}}
.top{{display:flex;justify-content:space-between;align-items:center;height:96px}}
.top span{{font-family:Jost;font-size:26px;letter-spacing:.06em;color:{C['stone']}}}
.ph{{height:{photo_h}px;margin-top:24px;background-size:cover;background-position:center}}
.mx{{display:grid;grid-template-columns:1fr 1fr;gap:10px}} .mx div{{background-size:cover;background-position:center}}
.meta{{padding-top:40px;display:grid;gap:6px}}
.n{{font-family:Anuphan;font-weight:500;font-size:60px;line-height:1.15}}
.s{{font-size:28px;color:#6E6A64}}
.p{{position:absolute;right:64px;bottom:{price_b}px;font-family:Jost;font-weight:500;font-size:56px}}
.band{{position:absolute;left:0;right:0;bottom:0;height:14px}}
"""
    body = (f'<div class="c"><div class="top">{logo("square-light", 96)}<span>our crafted things.</span></div>{photo(ph)}'
            f'<div class="meta"><div class="n">{name}</div><div class="s">{spec} · {size}</div></div>'
            f'<div class="p">{price} บาท</div><div class="band">{band()}</div></div>')
    return doc(css, body)

def profile():
    return doc(".w{width:1080px;height:1080px}", f'<div class="w">{logo("square-leaf", 1080)}</div>')

def cover(w, h, lines, sub):
    css = f"""
.w{{width:{w}px;height:{h}px;background:{C['mom']};color:{C['cotton']};position:relative;display:flex;align-items:center;justify-content:space-between;padding:0 {int(w * .08)}px}}
.t{{font-family:Anuphan;font-weight:500;font-size:{int(h * .1)}px;line-height:1.3}}
.s{{font-family:Jost;font-size:{int(h * .045)}px;letter-spacing:.06em;opacity:.85;margin-top:{int(h * .04)}px}}
.lg{{outline:{max(2, int(h * .006))}px solid {C['cotton']}}}
.band{{position:absolute;left:0;right:0;bottom:0;height:{int(h * .025)}px}}
"""
    body = (f'<div class="w"><div><div class="t">{lines}</div><div class="s">{sub}</div></div>'
            f'<div class="lg">{logo("square-leaf", int(h * .5))}</div><div class="band">{band()}</div></div>')
    return doc(css, body)

# ---------------------------------------------------------------- print
MM = "mm"
def crop_grid(cells, cols, rows, cw, ch, page_w=210, page_h=297):
    """Cells laid edge to edge, centred on the page, with crop marks outside the block."""
    gw, gh = cols * cw, rows * ch
    x0, y0 = (page_w - gw) / 2, (page_h - gh) / 2
    marks = []
    for i in range(cols + 1):
        x = x0 + i * cw
        marks += [f'<i style="left:{x:.2f}mm;top:{y0 - 7:.2f}mm;width:.15mm;height:5mm"></i>', f'<i style="left:{x:.2f}mm;top:{y0 + gh + 2:.2f}mm;width:.15mm;height:5mm"></i>']
    for j in range(rows + 1):
        y = y0 + j * ch
        marks += [f'<i style="top:{y:.2f}mm;left:{x0 - 7:.2f}mm;height:.15mm;width:5mm"></i>', f'<i style="top:{y:.2f}mm;left:{x0 + gw + 2:.2f}mm;height:.15mm;width:5mm"></i>']
    out = []
    for k, c in enumerate(cells):
        cx, cy = x0 + (k % cols) * cw, y0 + (k // cols) * ch
        out.append(f'<div class="cell" style="left:{cx:.2f}mm;top:{cy:.2f}mm;width:{cw}mm;height:{ch}mm">{c}</div>')
    return "".join(out) + "".join(marks)

PRINT_CSS = f"""
.pg{{width:210mm;height:297mm;position:relative;page-break-after:always;background:#fff;overflow:hidden}}
.pg.land{{width:297mm;height:210mm}}
.pg i{{position:absolute;background:#000;display:block}}
.cell{{position:absolute;overflow:hidden}}
.lbl{{position:absolute;left:12mm;bottom:2.5mm;font-size:7.5pt;color:#888}}
"""

def tag_front(p):
    sku, name, spec, size, price, _, food = p
    note = '<div class="fn">ไม่ใช่ภาชนะใส่อาหาร</div>' if food else ""
    return (f'<div class="tf"><div class="hole"></div><div class="lg">{logo("square-light", 92)}</div>'
            f'<div class="nm">{name}</div><div class="sp">{spec}<br>{size}</div><div class="pr">{price}.-</div>{note}<div class="sku latin">{sku}</div></div>')

def tag_back():
    return (f'<div class="tb"><div class="hole"></div><div class="bd">{band()}</div><div class="tx">ห้าคน ห้าสี<br>ทำกันเองทั้งบ้าน</div></div>')

TAG_CSS = f"""
.tf,.tb{{width:55mm;height:89mm;position:relative;background:{C['cotton']};display:flex;flex-direction:column;align-items:center}}
.hole{{position:absolute;top:5mm;left:50%;width:4mm;height:4mm;margin-left:-2mm;border-radius:50%;border:.25mm solid {C['charcoal']}}}
.tf .lg{{margin-top:13mm;width:24mm;height:24mm}} .tf .lg svg{{width:24mm;height:24mm}}
.nm{{font-family:Anuphan;font-weight:500;font-size:10.5pt;margin-top:5mm;text-align:center;padding:0 3mm;line-height:1.25}}
.sp{{font-size:7pt;color:#6E6A64;text-align:center;margin-top:1.5mm;line-height:1.35}}
.pr{{font-family:Jost;font-weight:500;font-size:15pt;margin-top:3mm}}
.fn{{font-size:6pt;color:#6E6A64;margin-top:1mm}}
.sku{{position:absolute;bottom:4mm;font-size:6pt;color:{C['stone']};letter-spacing:.06em}}
.tb{{background:{C['charcoal']}}} .tb .hole{{border-color:{C['cotton']}}}
.tb .bd{{position:absolute;left:0;right:0;top:14mm;height:52mm;display:flex;flex-direction:column}} .tb .bd span{{flex:1}}
.tb .tx{{position:absolute;bottom:7mm;left:0;right:0;text-align:center;color:{C['cotton']};font-size:8pt;line-height:1.5}}
"""

def tags_pdf():
    fronts = [tag_front(p) for p in PRODUCTS] + [tag_front(PRODUCTS[0]), tag_front(PRODUCTS[4])]
    backs = [tag_back()] * 9
    body = (f'<div class="pg"><div class="lbl">ป้ายห้อย 55 × 89 มม. · ด้านหน้า · พิมพ์ 100% กระดาษ 350 แกรม · ตัดตามเส้น · เจาะรูตามวงกลม</div>{crop_grid(fronts, 3, 3, 55, 89)}</div>'
            f'<div class="pg"><div class="lbl">ป้ายห้อย · ด้านหลัง (พิมพ์หลังแผ่นเดียวกัน)</div>{crop_grid(backs, 3, 3, 55, 89)}</div>')
    return doc(PRINT_CSS + TAG_CSS, body, "A4")

INSERT_CSS = f"""
.if,.ib{{width:89mm;height:55mm;position:relative;background:{C['cotton']}}}
.if .lg{{position:absolute;left:7mm;top:7mm;width:22mm;height:22mm}} .if .lg svg{{width:22mm;height:22mm}}
.if .t{{position:absolute;left:34mm;top:8mm;right:6mm;font-size:7.5pt;line-height:1.5}}
.if .t b{{font-family:Anuphan;font-weight:500;font-size:9pt}}
.if .ct{{position:absolute;left:7mm;bottom:6mm;right:24mm;font-family:Jost;font-size:6.5pt;color:#6E6A64;letter-spacing:.02em;line-height:1.5}}
.if .qr{{position:absolute;right:6mm;bottom:5mm;width:15mm;height:15mm}}
.ib{{background:{C['charcoal']}}} .ib .bd{{position:absolute;left:0;right:0;top:0;height:40mm;display:flex}} .ib .bd span{{flex:1}}
.ib .tx{{position:absolute;bottom:4.5mm;left:0;right:0;text-align:center;color:{C['cotton']};font-size:7.5pt}}
"""

def inserts_pdf():
    ct = " · ".join(f"{a} {b}" for a, b in CONTACT)
    f = (f'<div class="if"><div class="lg">{logo("square-light", 80)}</div><div class="t"><b>ขอบคุณที่อุดหนุน</b><br>หนังวัวแท้จากเศษหนังที่เหลือจากโรงงาน '
         f'สีและผิวไม่ซ้ำกันทุกชิ้น เช็ดด้วยผ้าแห้ง เก็บให้พ้นแดดและน้ำ</div><div class="ct">{ct}</div><img class="qr" src="{img("line-qr")}"></div>')
    b = f'<div class="ib"><div class="bd">{band()}</div><div class="tx">ห้าคน ห้าสี ทำกันเองทั้งบ้าน · OCT. 26</div></div>'
    body = (f'<div class="pg"><div class="lbl">การ์ดในซอง 89 × 55 มม. · ด้านหน้า · พิมพ์ 100% กระดาษ 300 แกรม</div>{crop_grid([f] * 10, 2, 5, 89, 55)}</div>'
            f'<div class="pg"><div class="lbl">การ์ดในซอง · ด้านหลัง</div>{crop_grid([b] * 10, 2, 5, 89, 55)}</div>')
    return doc(PRINT_CSS + INSERT_CSS, body, "A4")

def stickers_pdf():
    names = ["square-leaf", "square-family", "square-light"]
    cells = [f'<div style="width:34mm;height:34mm">{logo(names[k % 3], 129).replace("<svg ", "<svg style=\'width:34mm;height:34mm\' ", 1)}</div>' for k in range(35)]
    body = f'<div class="pg"><div class="lbl">สติกเกอร์ 34 × 34 มม. · ไดคัทตามเส้น · พิมพ์ 100%</div>{crop_grid(cells, 5, 7, 34, 34)}</div>'
    return doc(PRINT_CSS, body, "A4")

def sign_pdf():
    rows = "".join(f'<tr><td>{n}</td><td class="r latin">{pr}.-</td></tr>' for _, n, _, _, pr, _, _ in PRODUCTS)
    css = f"""
.s{{width:297mm;height:210mm;background:{C['cotton']};position:relative;padding:18mm 20mm;display:grid;grid-template-columns:1fr 1.15fr;gap:16mm}}
.l{{display:flex;flex-direction:column;gap:7mm}}
.l svg{{width:62mm;height:62mm}}
.h{{font-family:Jost;font-weight:500;font-size:30pt;letter-spacing:.02em}}
.sub{{font-size:12pt;color:#6E6A64;line-height:1.6}}
.qr{{display:flex;gap:5mm;align-items:center;font-family:Jost;font-size:10pt;margin-top:auto}} .qr img{{width:28mm;height:28mm}}
table{{border-collapse:collapse;width:100%;font-size:17pt;align-self:center}}
td{{padding:4mm 0;border-bottom:.3mm solid #DCD4C7}} td:first-child{{font-family:Anuphan;font-weight:500}}
.r{{text-align:right;font-weight:500}}
.note{{font-size:9.5pt;color:#6E6A64;margin-top:5mm}}
.band{{position:absolute;left:0;right:0;bottom:0;height:5mm}}
"""
    body = (f'<div class="s"><div class="l">{logo("square-light", 234)}<div><div class="h">SOI. 02</div><div class="sub">รอบผลิตแรก · หนังวัวแท้จากเศษหนัง<br>ทุกชิ้นสีไม่ซ้ำกัน ทำกันเองทั้งบ้าน</div></div>'
            f'<div class="qr"><img src="{img("line-qr")}"><div>LINE @155riuqj<br>IG @oct.26_brand<br>FB oct26brand</div></div></div>'
            f'<div style="align-self:center"><table>{rows}</table><div class="note">ที่รองแก้วไม่ใช่ภาชนะใส่อาหาร · โอนผ่านพร้อมเพย์ได้</div></div><div class="band">{band()}</div></div>')
    return doc(css, body, "A4 landscape")

def build():
    os.makedirs(os.path.join(HERE, "html"), exist_ok=True)
    jobs = []
    def put(name, html, kind, w=None, h=None):
        open(os.path.join(HERE, "html", name + ".html"), "w").write(html)
        jobs.append({"name": name, "kind": kind, "w": w, "h": h})
    for p in PRODUCTS:
        put("card-" + p[0], card(p), "png", 1080, 1350)
        put("story-" + p[0], card(p, 1920), "png", 1080, 1920)
    put("profile-1080", profile(), "png", 1080, 1080)
    put("fb-cover-1640x624", cover(1640, 624, "ของใช้จากเศษหนังแท้<br>ทำกันเองทั้งบ้าน", "OCT. 26 · our crafted things."), "png", 1640, 624)
    put("shopee-banner-1200x600", cover(1200, 600, "หนังวัวแท้จากเศษหนัง<br>สีไม่ซ้ำกันทุกชิ้น", "OCT. 26 · our crafted things."), "png", 1200, 600)
    put("tags-55x89", tags_pdf(), "pdf")
    put("insert-cards-89x55", inserts_pdf(), "pdf")
    put("stickers-34mm", stickers_pdf(), "pdf")
    put("booth-sign-A4", sign_pdf(), "pdf-land")
    json.dump(jobs, open(os.path.join(HERE, "jobs.json"), "w"), indent=1)
    print(len(jobs), "jobs")

if __name__ == "__main__":
    build()
