"""A4 print set for the booth on 23 Oct, home printer only (owner, 22 Oct). Mock-up for the owner to check.

Brand Book v2 (22 Oct): square logo from file only, nature colours (palette.py), the five family colours only as a thin
band, Anuphan / IBM Plex Sans Thai / Jost, prices as "30.-". The booth sells pattern pieces 01–05 as they are, 30 THB
each, no set price; what each piece can become comes from PD (product-dev-20261021/assortment/tiers.py USES). Every sheet
is A4 with crop marks where it needs cutting. No 06, no joining or no-sew claim, no bear face, heart or Love.
python3 print-20261022/build.py && node print-20261022/render.mjs -> oct26-print-a4.pdf, site/
"""
import html, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BRAND = os.path.join(REPO, "brand-20261014")
ASSETS = os.path.join(HERE, "assets")
sys.path.insert(0, BRAND)
sys.path.insert(0, ASSETS)
import brand as B
import segno
from palette import C, BAND


def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


S = _load("brand_site", os.path.join(BRAND, "site", "build.py"))
E = html.escape
INK, MUTED, LINE = C["charcoal"], "#6E6A64", "#DCD4C7"
FONTS = "file://" + os.path.join(BRAND, "fonts")
PRICE = 30
H = B.BRAND["handle"]
LINE_ID = B.SOCIAL["line_id"]
LINE_QR = "file://" + os.path.join(BRAND, "line", "L_gainfriends_2dbarcodes_BW.png")
PHOTO = "file://" + os.path.join(REPO, "ig-real-20261021", "ref", "bears.jpg")   # the owner's photo of real 01 pieces
NOFOOD = "ที่รองแก้วไม่ใช่ภาชนะใส่อาหาร"
SIZE = {"01": "10.4", "02": "9", "03": "9", "04": "9", "05": "9"}          # cm, from the die files
PIECES = [("01", "หมี"), ("02", "กังหัน"), ("03", "กากบาทแคปซูล"), ("04", "สี่เหลี่ยมมน"), ("05", "วงกลม")]
NAME = dict(PIECES)
USES = {  # PD, tiers.py USES (22 Oct): single piece, nothing joined
    "01": [("ที่รองแก้ว", "วางแก้วน้ำหรือแก้วกาแฟ ไม่ใช่ภาชนะใส่อาหาร"),
           ("ที่เก็บสายชาร์จ", "พันสายรอบหัว เหน็บปลายสายเข้าร่อง"),
           ("ป้ายชื่อบนกล่องของขวัญ", "เขียนชื่อคนรับ วางบนกล่องแล้วผูกริบบิ้นทับ")],
    "02": [("ที่รองแก้ว", "วางแก้วน้ำหรือแก้วกาแฟ ไม่ใช่ภาชนะใส่อาหาร"),
           ("ที่พันสายชาร์จหรือสายหูฟัง", "เสียบปลายสายเข้าร่องหนึ่ง พันรอบตัวกลาง เสียบปลายอีกข้างเข้าร่องตรงข้าม"),
           ("ที่คั่นหนังสือมุมหน้า", "สอดมุมหน้ากระดาษเข้าร่องเดียว"),
           ("แกนพันไหมปักผ้า", "พันไหมหนึ่งสีต่อชิ้น เกี่ยวปลายไหมเข้าร่อง")],
    "03": [("ป้ายของขวัญ", "เขียนชื่อ ร้อยเชือกหรือริบบิ้นผ่านร่อง ผูกกับถุงหรือกล่อง"),
           ("ที่เก็บกิ๊บติดผม", "หนีบกิ๊บเรียงตามขอบและร่อง ใส่กระเป๋าแล้วไม่กระจาย"),
           ("ที่ห่อสายนาฬิกาตอนเดินทาง", "พันสายนาฬิกาหรือกำไลรอบชิ้น เหน็บปลายเข้าร่อง")],
    "04": [("ที่รองแก้ว", "วางแก้วน้ำหรือแก้วกาแฟ ไม่ใช่ภาชนะใส่อาหาร"),
           ("แผ่นรองแจกันหรือฐานโคมไฟ", "รองใต้แจกันหรือโคมไฟบนโต๊ะไม้ กันรอยขีด"),
           ("ป้ายคั่นแฟ้มเอกสาร", "สวมร่องเข้าขอบแฟ้ม เขียนชื่อหมวด")],
    "05": [("ที่รองแก้ว", "วางแก้วน้ำหรือแก้วกาแฟ ไม่ใช่ภาชนะใส่อาหาร"),
           ("ที่รองเทียนหอมหรือกระถางเล็ก", "รองใต้โหลเทียนหรือกระถางแคคตัส กันคราบและรอยบนโต๊ะ"),
           ("ที่รัดผ้าพันคอ", "สอดชายผ้าพันคอทั้งสองข้างผ่านร่อง แทนการผูกปม"),
           ("ตัวคาดธนบัตรให้ของขวัญ", "พับธนบัตรตามยาว สอดผ่านสองร่อง")],
}

CSS = f"""
@font-face{{font-family:Anuphan;font-weight:500;src:url({FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Jost;font-weight:400;src:url({FONTS}/alt/Jost-Regular.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url({FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Plex;font-weight:400;src:url({FONTS}/IBMPlexSansThai-Regular.ttf)}}
@font-face{{font-family:Plex;font-weight:600;src:url({FONTS}/IBMPlexSansThai-SemiBold.ttf)}}
@page{{size:210mm 297mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Plex,sans-serif;color:{INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{position:relative;width:210mm;height:297mm;overflow:hidden;page-break-after:always;background:#fff}}
.page.land{{width:297mm;height:210mm;page:land}}
@page land{{size:297mm 210mm;margin:0}}
.cell{{position:absolute;overflow:hidden}}
.mk{{position:absolute;background:#000}}
.note{{position:absolute;font-size:2.6mm;color:{MUTED};font-family:Plex}}
.lg svg,.pc svg{{width:100%;height:auto;display:block}}
h1,h2{{font-family:Anuphan;font-weight:500;line-height:1.2}}
.jost{{font-family:Jost;font-weight:500}}
.jl{{font-family:Jost;font-weight:400}}
.mu{{color:{MUTED}}}
.band{{display:flex}}.band span{{flex:1}}
"""


def marks(xs=(), ys=(), inset=5, length=5):
    """Crop marks in the page margin: short lines at each cut, 5–10 mm from the paper edge (inside what home printers print)."""
    out = []
    for x in xs:
        out += [f'<div class="mk" style="left:{x - .1}mm;top:{inset}mm;width:.2mm;height:{length}mm"></div>',
                f'<div class="mk" style="left:{x - .1}mm;bottom:{inset}mm;width:.2mm;height:{length}mm"></div>']
    for y in ys:
        out += [f'<div class="mk" style="top:{y - .1}mm;left:{inset}mm;height:.2mm;width:{length}mm"></div>',
                f'<div class="mk" style="top:{y - .1}mm;right:{inset}mm;height:.2mm;width:{length}mm"></div>']
    return "".join(out)


def _svg(name):
    s = open(os.path.join(ASSETS, name + ".svg")).read()
    return re.sub(r'(<svg[^>]*?) width="[^"]*" height="[^"]*"', r"\1", s, count=1)


def logo(mm, name="square-light"):
    """Brand Book v2 logo, from the file only (never typed)."""
    return f'<div class="lg" style="width:{mm}mm;flex:none">{_svg(name)}</div>'


def real_mm(code):
    return float(re.search(r'width="([\d.]+)mm"', open(os.path.join(ASSETS, f"pattern-{code}-solid.svg")).read()).group(1))


def pattern(code, mm=None, style="solid"):
    """Pattern drawing in hide brown; mm=None draws it at real size (1:1)."""
    mm = mm or real_mm(code)
    return f'<div class="pc" style="width:{mm}mm;flex:none">{_svg(f"pattern-{code}-{style}")}</div>'


def band(h, w="100%"):
    """The five family colours in their fixed order, equal widths: a thin detail only."""
    return f'<div class="band" style="height:{h}mm;width:{w}">' + "".join(f'<span style="background:{c}"></span>' for c in BAND) + "</div>"


def price(size, unit=""):
    return f'<span class="jost" style="font-size:{size}mm;line-height:1">{PRICE}.-</span>{unit}'


def qr(url, mm):
    q = segno.make(url, error="m")
    return f'<div style="width:{mm}mm;height:{mm}mm">{q.svg_inline(dark=INK, scale=4, border=1, svgclass="q").replace("<svg ", "<svg style=" + chr(39) + "width:100%;height:100%" + chr(39) + " ", 1)}</div>'


def line_qr(mm):
    return f'<img src="{LINE_QR}" style="width:{mm}mm;height:{mm}mm;image-rendering:pixelated">'


def foot(text=""):
    """Page footer inside the printable area: small muted text and a short family band."""
    return (f'<div style="position:absolute;left:20mm;right:20mm;bottom:12mm;display:flex;justify-content:space-between;align-items:center">'
            f'<span class="jl mu" style="font-size:3.2mm">{E(text)}</span>{band(1.4, "22mm")}</div>')


# ------------------------------------------------------------------ 1: shop sign, A4 landscape
def shop_sign():
    """Its own landscape page in the PDF (named @page "land")."""
    pcs = "".join(pattern(c, 21 if c == "01" else 19.5) for c, _ in PIECES)
    inner = (f'<div style="position:absolute;left:24mm;right:24mm;top:30mm;display:flex;align-items:center;gap:16mm">'
             f'{logo(112)}<div style="display:flex;flex-direction:column;gap:6mm">'
             f'<div class="jl" style="font-size:11mm;letter-spacing:.01em">our crafted things.</div>'
             f'<h1 style="font-size:10.5mm">ของใช้จากเศษหนังวัวแท้<br>ทำกันเองทั้งบ้าน</h1>'
             f'<div class="jl mu" style="font-size:5.4mm">quiet outside, family inside.</div>'
             f'<div style="display:flex;align-items:baseline;gap:4mm;margin-top:3mm;border-top:0.3mm solid {LINE};padding-top:5mm">'
             f'<b class="jost" style="font-size:7mm">SOI. 02</b><span class="mu" style="font-size:4.4mm">คอลเลกชันแรก</span></div></div></div>'
             f'<div style="position:absolute;left:24mm;right:24mm;bottom:22mm;display:flex;justify-content:space-between;align-items:center">'
             f'<div style="display:flex;gap:7mm;align-items:center">{pcs}</div>'
             f'<span class="jl mu" style="font-size:4.6mm">IG @{H} · LINE {LINE_ID}</span></div>'
             f'<div style="position:absolute;left:24mm;right:24mm;bottom:13mm">{band(2)}</div>')
    return f'<div class="page land">{inner}</div>'


# ------------------------------------------------------------------ 2: social sign with the LINE QR
def social_sign():
    others = [("Instagram", "@" + H, B.SOCIAL["instagram"]), ("Facebook", "oct26brand", B.SOCIAL["facebook"]),
              ("YouTube", "@OCT.26_brand", B.SOCIAL["youtube"])]
    row = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:2.5mm;width:50mm">{qr(u, 40)}'
                  f'<b class="jost" style="font-size:4.8mm">{E(n)}</b><span class="jl mu" style="font-size:3.9mm">{E(h)}</span></div>'
                  for n, h, u in others)
    return (f'<div class="page"><div style="position:absolute;left:20mm;right:20mm;top:20mm;bottom:24mm;display:flex;flex-direction:column;align-items:center;gap:8mm;text-align:center">'
            f'{logo(44)}<h1 style="font-size:11mm">ติดตามเราได้ที่นี่</h1>'
            f'<div style="border:0.4mm solid {INK};padding:7mm 9mm;display:flex;align-items:center;gap:9mm;text-align:left">'
            f'{line_qr(60)}<div style="display:flex;flex-direction:column;gap:3mm"><b class="jost" style="font-size:9mm">LINE</b>'
            f'<span class="jost" style="font-size:6mm">{LINE_ID}</span>'
            f'<span style="font-size:4.4mm;line-height:1.5" class="mu">แอดไว้ มีแพตเทิร์นใหม่<br>ไอเดียใหม่ และบูธรอบหน้า<br>จะบอกทางนี้ก่อน</span></div></div>'
            f'<div style="display:flex;justify-content:space-between;width:100%;margin-top:4mm;padding-top:8mm;border-top:0.3mm solid {LINE}">{row}</div>'
            f'<div class="jl mu" style="font-size:4.4mm;margin-top:auto">{B.SOCIAL["web"]} · Shopee {E(B.SHOP_NAME)}</div></div>'
            f'{foot("OCT. 26 · our crafted things.")}</div>')


# ------------------------------------------------------------------ 3: price sign, two A5 per A4
def price_sign():
    row = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:2mm;width:32mm">'
                  f'{pattern(c, 25 if c == "01" else 23)}<div style="font-size:3.6mm;text-align:center;line-height:1.25">'
                  f'<b class="jost">{c}</b> {E(n)}</div></div>' for c, n in PIECES)
    one = (f'<div style="position:absolute;inset:15mm 16mm 15mm;display:flex;flex-direction:column;justify-content:space-between">'
           f'<div style="display:flex;justify-content:space-between;align-items:flex-start">{logo(24)}'
           f'<span class="mu" style="font-size:3.4mm;text-align:right;line-height:1.5">หนังวัวแท้จากเศษหนัง<br>หนา 1.0–1.2 มม.</span></div>'
           f'<div style="display:flex;align-items:baseline;justify-content:space-between">'
           f'<h1 style="font-size:11mm">แพตเทิร์นละ</h1>{price(22)}</div>'
           f'<div style="display:flex;justify-content:space-between;border-top:0.3mm solid {LINE};padding-top:5mm">{row}</div>'
           f'<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:6mm">'
           f'<div style="font-size:3.8mm;line-height:1.5">ราคาบูธ · สีและลายแต่ละแผ่นไม่ซ้ำกัน<br><b>ไปทำอะไรได้บ้าง เปิดดูในแฟ้มได้เลย</b>'
           f'<br><span class="mu" style="font-size:3.2mm">{NOFOOD}</span></div>{band(1.4, "22mm")}</div></div>')
    cells = "".join(f'<div class="cell" style="left:0;top:{y}mm;width:210mm;height:148.5mm">{one}</div>' for y in (0, 148.5))
    return f'<div class="page">{cells}{marks(ys=(148.5,))}</div>'


# ------------------------------------------------------------------ 4: pattern labels 90 x 55, ten per A4
def labels():
    w, h, x0, y0 = 90, 55, 15, 11
    cells = []
    for i in range(10):
        c, n = PIECES[i // 2]
        x, y = x0 + (i % 2) * w, y0 + (i // 2) * h
        cells.append(
            f'<div class="cell" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm;display:flex;align-items:center;gap:6mm;padding:0 8mm">'
            f'{pattern(c, 31 if c == "01" else 29)}'
            f'<div style="display:flex;flex-direction:column;gap:1.2mm"><b class="jost" style="font-size:9mm;line-height:1">{c}</b>'
            f'<h2 style="font-size:5.4mm">{E(n)}</h2><span class="mu" style="font-size:3.2mm">หนังวัวแท้ · {SIZE[c]} ซม.</span>'
            f'<div style="margin-top:1.5mm">{price(8.5)}</div></div>'
            f'<div style="position:absolute;right:8mm;bottom:6mm">{band(1, "14mm")}</div></div>')
    xs = (x0, x0 + w, x0 + 2 * w)
    ys = tuple(y0 + k * h for k in range(6))
    scale = ('<div class="note" style="left:25mm;bottom:5.5mm;display:flex;align-items:center;gap:2mm">'
             '<div style="width:50mm;height:1.2mm;background:#000"></div>ตรวจขนาด: แถบนี้ต้องยาว 50 มม.</div>')
    return f'<div class="page">{"".join(cells)}{marks(xs, ys)}{scale}</div>'


# ------------------------------------------------------------------ 5: LINE QR cards A6, four per A4
def line_cards():
    one = (f'<div style="position:absolute;inset:11mm 10mm;display:flex;flex-direction:column;align-items:center;gap:4mm;text-align:center">'
           f'{logo(24)}<h2 style="font-size:6.6mm;margin-top:1mm">แอด LINE ไว้นะ</h2>'
           f'<div class="mu" style="font-size:3.6mm;line-height:1.45">มีแพตเทิร์นใหม่ ไอเดียใหม่<br>และบูธรอบหน้า จะบอกทางนี้</div>'
           f'{line_qr(50)}<div class="jost" style="font-size:4.4mm">{LINE_ID}</div>'
           f'<div style="margin-top:auto">{band(1, "18mm")}</div></div>')
    cells = "".join(f'<div class="cell" style="left:{x}mm;top:{y}mm;width:105mm;height:148.5mm">{one}</div>'
                    for y in (0, 148.5) for x in (0, 105))
    return f'<div class="page">{cells}{marks((105,), (148.5,))}</div>'


# ------------------------------------------------------------------ 6: product list
def product_list():
    rows = "".join(
        f'<tr><td style="width:24mm">{pattern(c, 17 if c == "01" else 16)}</td>'
        f'<td><b class="jost" style="font-size:5mm">{c}</b> <b style="font-size:5mm">{E(n)}</b>'
        f'<span class="mu" style="font-size:3.4mm"> · {SIZE[c]} ซม.</span><br>'
        f'<span class="mu" style="font-size:3.6mm;line-height:1.5">{E(" · ".join(u for u, _ in USES[c]))}</span></td>'
        f'<td style="text-align:right;white-space:nowrap">{price(7)}</td></tr>'
        for c, n in PIECES)
    return (f'<div class="page"><div style="position:absolute;left:20mm;right:20mm;top:20mm;display:flex;flex-direction:column;gap:7mm">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start">{logo(28)}'
            f'<span class="mu" style="font-size:3.4mm">ราคาบูธ</span></div>'
            f'<h1 style="font-size:11mm">รายการสินค้า</h1>'
            f'<p style="font-size:4.4mm;line-height:1.5">ชิ้นหนังวัวแท้ตัดด้วยบล็อก 5 แพตเทิร์น<br><b>ซื้อกี่แผ่นก็แผ่นละ {PRICE} บาท</b></p>'
            f'<table style="border-collapse:collapse;width:100%">{rows}</table>'
            f'<p class="mu" style="font-size:3.6mm;line-height:1.6">หนังวัวแท้จากเศษหนัง หนา 1.0–1.2 มม. สีและลายแต่ละแผ่นไม่ซ้ำกัน · '
            f'ขอบหนังปล่อยตามธรรมชาติ · {NOFOOD}</p></div>'
            f'<style>.page table td{{border-top:0.3mm solid {LINE};padding:3.6mm 2mm;vertical-align:middle}}</style>'
            f'{foot("OCT. 26 · our crafted things.")}</div>')


# ------------------------------------------------------------------ 7: one sample: 01 coaster x 4
def product_sample():
    return (f'<div class="page"><div style="position:absolute;left:20mm;right:20mm;top:20mm;display:flex;flex-direction:column;gap:6mm">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start">{logo(24)}'
            f'<span class="mu" style="font-size:3.4mm">ตัวอย่างสินค้า 1 ชุด</span></div>'
            f'<img src="{PHOTO}" style="width:170mm;height:112mm;object-fit:cover">'
            f'<div style="display:flex;justify-content:space-between;align-items:baseline"><h1 style="font-size:11mm">01 ที่รองแก้ว × 4</h1>'
            f'<span class="jost" style="font-size:12mm;line-height:1">{4 * PRICE}.-</span></div>'
            f'<p style="font-size:4.6mm;line-height:1.55">ชิ้นหนังวัวแท้แพตเทิร์น 01 สี่แผ่น สีไม่ซ้ำกัน ใช้รองแก้วในบ้าน หรือแบ่งให้เพื่อน<br>'
            f'<span class="mu">คิดราคาแผ่นละ {PRICE} บาท ตามจำนวนแผ่น</span></p>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;font-size:4.2mm;line-height:1.55;border-top:0.3mm solid {LINE};padding-top:5mm">'
            f'<div><b>ในชุดมี</b><br>01 หมี × 4 แผ่น · {SIZE["01"]} ซม.<br>หนังวัวแท้ หนา 1.0–1.2 มม.</div>'
            f'<div><b>ใช้และดูแล</b><br>วางแก้วน้ำหรือแก้วกาแฟ<br>เช็ดด้วยผ้าแห้ง เลี่ยงน้ำขังและแดดจัด</div></div>'
            f'<p class="mu" style="font-size:3.4mm">{NOFOOD} · รูปจริงจากชิ้นที่ตัดแล้ว สีในชุดจริงต่างจากรูป เพราะทุกแผ่นไม่ซ้ำกัน</p></div>'
            f'{foot("OCT. 26 · our crafted things.")}</div>')


# ------------------------------------------------------------------ 8–14: idea folder, no cutting
def folder_cover():
    pcs = "".join(pattern(c, 27 if c == "01" else 25) for c, _ in PIECES)
    return (f'<div class="page"><div style="position:absolute;left:20mm;right:20mm;top:24mm;display:flex;flex-direction:column;gap:8mm">'
            f'{logo(56)}<h1 style="font-size:13mm;margin-top:14mm">ชิ้นหนังหนึ่งแผ่น<br>ไปเป็นอะไรได้บ้าง</h1>'
            f'<p style="font-size:4.8mm;line-height:1.6" class="mu">พลิกดูทีละแพตเทิร์น เลือกแผ่นที่ชอบ แล้วเอาไปใช้ตามไอเดีย<br>'
            f'ชิ้นหนังวัวแท้ แผ่นละ {PRICE} บาท</p></div>'
            f'<div style="position:absolute;left:20mm;right:20mm;top:190mm;display:flex;justify-content:space-between;align-items:center">{pcs}</div>'
            f'<div style="position:absolute;left:20mm;right:20mm;top:226mm;margin:0 -3.5mm;display:flex;justify-content:space-between">'
            + "".join(f'<span style="width:34mm;text-align:center;font-size:3.4mm"><b class="jost">{c}</b> {E(n)}</span>' for c, n in PIECES)
            + f'</div>{foot("ไอเดียจากฝ่ายพัฒนาสินค้า · 22 ต.ค. 2569")}</div>')


def folder_page(c, n):
    uses = "".join(f'<li style="display:grid;grid-template-columns:9mm 1fr;padding:3.2mm 0;border-top:0.3mm solid {LINE}">'
                   f'<span class="jost mu" style="font-size:4.4mm">{i}</span><div><b style="font-size:4.8mm">{E(u)}</b>'
                   f'<div class="mu" style="font-size:3.8mm;line-height:1.5">{E(how)}</div></div></li>'
                   for i, (u, how) in enumerate(USES[c], 1))
    return (f'<div class="page">'
            f'<div style="position:absolute;left:20mm;right:20mm;top:20mm;display:flex;justify-content:space-between;align-items:flex-start">'
            f'<div><b class="jost" style="font-size:16mm;line-height:1">{c}</b><h1 style="font-size:9mm;margin-top:2mm">{E(n)}</h1></div>'
            f'<div style="text-align:right">{price(12)}<div class="mu" style="font-size:3.6mm;margin-top:1.5mm">ต่อแผ่น · ราคาบูธ</div></div></div>'
            f'<div style="position:absolute;left:0;right:0;top:66mm;display:flex;flex-direction:column;align-items:center;gap:3mm">'
            f'{pattern(c)}<div class="mu" style="font-size:3.4mm">ขนาดจริง {SIZE[c]} ซม. · วางชิ้นหนังทับดูได้</div></div>'
            f'<div style="position:absolute;left:20mm;right:20mm;top:174mm">'
            f'<h2 style="font-size:6.4mm;margin-bottom:3mm">ไปเป็นอะไรได้บ้าง</h2><ul style="list-style:none">{uses}</ul>'
            f'<p class="mu" style="font-size:3.4mm;margin-top:3mm">ใช้ชิ้นเดียวตามที่ตัดมา ไม่ต้องต่อชิ้น</p></div>'
            f'{foot(f"IG @{H} · LINE {LINE_ID}")}</div>')


def folder_back():
    return (f'<div class="page"><div style="position:absolute;inset:36mm 25mm;display:flex;flex-direction:column;align-items:center;gap:7mm;text-align:center">'
            f'{logo(48)}<h1 style="font-size:10mm;margin-top:6mm">เลือกได้กี่แผ่นก็ได้<br>แผ่นละ {PRICE} บาท</h1>'
            f'<p class="mu" style="font-size:4.6mm;line-height:1.6">แอด LINE ไว้ มีไอเดียใหม่จะส่งไปให้</p>'
            f'{line_qr(58)}<div class="jost" style="font-size:5mm">LINE {LINE_ID}</div>'
            f'<div class="jl mu" style="font-size:4.2mm">IG @{H} · facebook.com/oct26brand</div></div>'
            f'{foot("quiet outside, family inside.")}</div>')


SHEETS = [  # (title, how many to print, cutting, html)
    ("ป้ายร้าน A4 แนวนอน", "1 แผ่น", "ไม่ต้องตัด ติดหน้าโต๊ะหรือตะแกรง", shop_sign),
    ("ป้ายโซเชียล A4 + QR LINE", "1 แผ่น", "ไม่ต้องตัด ใส่กรอบหรือติดตะแกรง", social_sign),
    ("ป้ายราคา A5", "1 แผ่น ได้ 2 ป้าย", "ตัดครึ่งตามขีดกลางแผ่น ใส่กรอบอะคริลิก A5", price_sign),
    ("ป้ายชื่อแพตเทิร์น 9 × 5.5 ซม.", "1 แผ่น ได้ 10 ป้าย (แบบละ 2)", "ตัดตามขีดทุกเส้น หนีบไม้หนีบผ้าที่ตะกร้าแต่ละแพตเทิร์น", labels),
    ("การ์ด QR LINE A6", "1 แผ่น ได้ 4 ใบ", "ตัดตามขีดกลางทั้งแนวตั้งและแนวนอน วางโต๊ะจ่ายเงินและจุด DIY", line_cards),
    ("รายการสินค้า", "1 แผ่น", "ไม่ต้องตัด วางโต๊ะหรือใส่แฟ้มหน้าแรก", product_list),
    ("ตัวอย่างสินค้า 1 ชุด: 01 ที่รองแก้ว × 4", "1 แผ่น", "ไม่ต้องตัด ใส่แฟ้ม", product_sample),
    ("แฟ้มไอเดีย: ปก", "1 แผ่น", "ไม่ต้องตัด ใส่แฟ้มซองใส A4", folder_cover),
] + [(f"แฟ้มไอเดีย: {c} {n}", "1 แผ่น", "ไม่ต้องตัด ใส่แฟ้ม · แพตเทิร์นขนาดจริง", (lambda c=c, n=n: folder_page(c, n))) for c, n in PIECES] + [
    ("แฟ้มไอเดีย: ปกหลัง", "1 แผ่น", "ไม่ต้องตัด ใส่แฟ้ม", folder_back),
]
for _, _, _, fn in SHEETS:   # status doc 22 Oct
    out = re.sub(r"<svg.*?</svg>|<[^>]+>", " ", fn(), flags=re.S)
    for word in ("ไม่ต้องเย็บ", "06 ", "หัวใจ", "Love", "ห้าหมี", "รอบผลิตแรก"):
        assert word not in out, (word, fn)


def summary(n_pages):
    rows = "".join(f'<tr><td class="mono">{i}</td><td><b>{E(t)}</b></td><td>{E(q)}</td><td>{E(cut)}</td></tr>'
                   for i, (t, q, cut, _) in enumerate(SHEETS, 1))
    figs = "".join(f'<figure style="margin:0;display:flex;flex-direction:column;gap:6px"><img src="p{i:02d}.png" alt="{E(t)}" loading="lazy" '
                   f'style="border:1px solid var(--line);border-radius:6px;background:#fff"><figcaption class="cap">{i} · {E(t)}</figcaption></figure>'
                   for i, (t, *_) in enumerate(SHEETS, 1))
    return f"""{S.head("OCT. 26 ไฟล์พิมพ์ A4")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">บูธ 23 ต.ค. · ร่างให้ตรวจ · Brand Book v2</span><h1>ไฟล์พิมพ์ A4 สำหรับบูธ</h1>
<p class="lead">ขายชิ้นหนัง 5 แพตเทิร์น แผ่นละ {PRICE} บาท พิมพ์จากเครื่องที่บ้านได้ทั้งหมด {n_pages} แผ่น A4
ตัดตามขีดที่ขอบกระดาษ ทำใหม่ทั้งชุดตาม Brand Book v2 (22 ต.ค.)</p></header>
<section><h2>เปลี่ยนตาม Brand Book v2</h2><div class="card"><ol>
<li>โลโก้สี่เหลี่ยม OCT. 26 จากไฟล์ แทนโลโก้และสี Soi Candy เดิม</li>
<li>สีจากธรรมชาติ: ตัวหนังสือดำถ่าน รูปแพตเทิร์นสีหนังแท้ ห้าสีของบ้านเป็นแถบเล็ก ๆ เท่านั้น ไม่มีตัวหนังสือสี</li>
<li>ฟอนต์ Anuphan หัวข้อ · IBM Plex Sans Thai เนื้อความ · Jost ตัวเลขและภาษาอังกฤษ · ราคาแบบ 30.-</li>
<li>รูปแพตเทิร์นใช้ไฟล์วาดจริง หน้าแฟ้มไอเดียพิมพ์ขนาดจริง 1:1</li>
<li>ไอเดียในแฟ้มใช้รายการจากฝ่ายพัฒนาสินค้า (ชิ้นเดียว ไม่ต่อชิ้น) ตัด "เขียนชื่อ ห้อยกระเป๋า" ออก เพราะของห้อยต้องรอหนัง 2 มม.</li>
<li>รายการสินค้าไม่มีราคาชุดแล้ว ซื้อกี่แผ่นก็แผ่นละ {PRICE} บาท · ตัวอย่างชุดเปลี่ยนเป็น "01 ที่รองแก้ว × 4" = {4 * PRICE}.-</li>
<li>ใส่ "{NOFOOD}" ทุกที่ที่พูดถึงที่รองแก้ว · ป้ายร้านใช้ "SOI. 02 คอลเลกชันแรก"</li></ol></div></section>
<section><h2>วิธีพิมพ์</h2><div class="card"><ol>
<li>เปิด PDF แล้วสั่งพิมพ์ <b>ขนาดจริง 100%</b> (Actual size) ห้ามเลือกพอดีหน้า (Fit)</li>
<li>พิมพ์หน้า 4 ก่อน วัดแถบตรวจขนาดที่ขอบล่าง ต้องยาว 50 มม. ถ้าไม่ใช่ ตั้งค่าใหม่</li>
<li>ขีดดำสั้น ๆ ที่ขอบกระดาษคือเส้นตัด วางไม้บรรทัดต่อขีดสองฝั่งแล้วตัดด้วยคัตเตอร์</li>
<li>ถ้ามีกระดาษสีครีม 160–200 แกรม ใช้แทนกระดาษขาวจะเข้ากับสีขาวฝ้ายของแบรนด์ ถ้ามีแค่ 80 แกรม ป้ายชื่อและการ์ด LINE ให้ติดบนเศษฟิวเจอร์บอร์ด</li></ol></div></section>
<section><h2>รายการพิมพ์</h2><div class="tbl"><table><thead><tr><th>หน้า</th><th>อะไร</th><th>ได้กี่ชิ้น</th><th>ตัด / ใช้</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section><h2>ตัวอย่างทุกหน้า</h2><div class="grid">{figs}</div></section>
<section><span class="eyebrow">เพิ่ม 22 ต.ค. ค่ำ</span><h2>การ์ดแบรนด์ใส่ถุง 6.3 × 6.3 ซม.</h2>
<div class="grid"><figure style="margin:0;display:flex;flex-direction:column;gap:6px"><img src="card-1.png" alt="หน้าการ์ด" loading="lazy" style="border:1px solid var(--line);border-radius:6px;background:#fff"><figcaption class="cap">หน้า · โลโก้แถบห้าสี</figcaption></figure>
<figure style="margin:0;display:flex;flex-direction:column;gap:6px"><img src="card-2.png" alt="หลังการ์ด" loading="lazy" style="border:1px solid var(--line);border-radius:6px;background:#fff"><figcaption class="cap">หลัง · QR LINE, IG, FB</figcaption></figure></div>
<div class="card"><ol>
<li>สี่เหลี่ยมจัตุรัสเหมือนโลโก้ ไม่เกิน 7 ซม. ตามที่ขอ A4 หนึ่งแผ่นได้ 12 ใบ</li>
<li>หน้า: โลโก้แบบมีแถบห้าสี กับ our crafted things. · หลัง: QR LINE (สแกนแล้วเปิดถูกบัญชี) IG @oct.26_brand FB oct26brand และแถบห้าสี "ห้าคน ห้าสี ทำกันเองทั้งบ้าน" ตามการ์ดในซองของ Brand Book v2</li>
<li>พิมพ์สองหน้า พลิกด้านยาว (Flip on long edge) ขนาดจริง 100% · ถ้าเครื่องพิมพ์สองหน้าเองไม่ได้ พิมพ์หน้า 1 แล้วใส่กระดาษกลับด้านพิมพ์หน้า 2 ลองแผ่นแรกด้วยกระดาษธรรมดาก่อน</li>
<li>ตัวการ์ดอยู่ห่างขอบการ์ด 6 มม. ถ้าหน้าหลังเหลื่อมกัน 1–2 มม. ก็ยังไม่โดนตัด</li>
<li>กระดาษ 200–250 แกรม (เท่าที่เครื่องรับได้) · เริ่ม 4 แผ่น = 48 ใบ ใส่ถุงละ 1 ใบ หมดค่อยพิมพ์เพิ่ม</li>
<li>ไฟล์ print-20261022/oct26-brand-card.pdf (2 หน้า) · แก้ที่ print-20261022/card.py</li></ol></div></section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>
<li>ป้าย A4 ในงานรีแบรนด์ (booth-sign-A4) ยังเป็นราคา 7 แบบเดิมและเขียน "SOI. 02 รอบผลิตแรก" ไม่ตรงกับแผ่นละ {PRICE} บาท บูธพรุ่งนี้ใช้ป้ายราคาหน้า 3 ของชุดนี้แทน</li>
<li>5 แพตเทิร์นคือ 01 หมี · 02 กังหัน · 03 กากบาทแคปซูล · 04 สี่เหลี่ยมมน · 05 วงกลม (07 มีของแล้ว แต่บูธนี้ขายแค่ 01–05)</li>
<li>รูปตัวอย่างสินค้าเป็นรูปจริงชิ้น 01 ที่พ่อเบถ่ายไว้ ถ้ามีรูปที่รองแก้วใช้งานจริงค่อยเปลี่ยน</li>
<li>QR LINE ในไฟล์เปิด lin.ee/O9AePgp สแกนดูอีกครั้งว่าขึ้นบัญชี OCT. 26</li></ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">print-20261022/oct26-print-a4.pdf</td><td>ไฟล์พิมพ์ทั้งหมด {n_pages} หน้า</td></tr>
<tr><td class="mono" style="white-space:nowrap">print-20261022/oct26-print-new-4.pdf</td><td>4 หน้าที่ขอ 22 ต.ค.: ป้ายร้าน ป้ายโซเชียล รายการสินค้า ตัวอย่างสินค้า</td></tr>
<tr><td class="mono" style="white-space:nowrap">print-20261022/build.py</td><td>แก้ราคา ข้อความ หรือไอเดียที่นี่แล้วรันใหม่</td></tr>
<tr><td class="mono" style="white-space:nowrap">print-20261022/assets/</td><td>โลโก้ สี และรูปแพตเทิร์นจาก Brand Book v2</td></tr>
</tbody></table></div></section></div>{S.COPY_JS}"""


if __name__ == "__main__":
    body = "".join(fn() for *_, fn in SHEETS)
    open(os.path.join(HERE, "print.html"), "w").write(
        f'<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(summary(len(SHEETS)))
    print("wrote print.html and site/index.html,", len(SHEETS), "pages")
