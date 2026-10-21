"""X-stand banner 60 x 160 cm for the booth: sells on its own the moment it is stood up.

Top to bottom, by viewing height (the banner top stands about 170 cm off the floor):
brand block seen from the aisle, hook and starting price, QR and every channel, six products with
prices, collections band. No event name or date, so the same print works at every fair.

python3 booth-20261019/xstand/build.py          -> xstand/xstand.html
node booth-20261019/xstand/render.mjs           -> PDF (vector, fonts embedded) + JPG 100 dpi + preview
"""
import importlib.util, os, re, sys
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BRAND_DIR = os.path.join(REPO, "brand-20261014")
sys.path.insert(0, BRAND_DIR)
import brand as B

_sp = importlib.util.spec_from_file_location("posters_build", os.path.join(BRAND_DIR, "posters", "build.py"))
PB = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(PB)
P = {p["n"]: p for p in B.PRODUCTS}
C = B.C
FONTS = "file://" + os.path.join(BRAND_DIR, "fonts")

W, H = 600, 1600                     # mm
QR_URL = f"https://www.instagram.com/{B.BRAND['handle']}/"
# (product, pieces drawn for it): what a home-fair visitor picks up first, and one of each shape family
SHOW = [(29, ["01", "02", "04", "05"]), (22, ["01"]), (21, ["01"] * 5),
        (23, ["01", "01-S200"]), (15, ["05", "05"]), (30, ["06"])]


def logo(f):
    s = open(os.path.join(BRAND_DIR, "logo", "svg", f)).read()
    s = re.sub(r'<title>.*?</title>', '', s)
    return re.sub(r' width="[\d.]+" height="[\d.]+"', '', s, count=1)


def qr_svg():
    q = segno.make(QR_URL, error="m")
    return q.svg_inline(dark=C["ink"], light="#FFFFFF", border=2, scale=10, omitsize=True)


def art(codes):
    many = len(codes) > 2
    return "".join(f'<span class="pc{" s" if many else ""}{" strap" if "-S" in c else ""}">{PB.icon(c, C["leather"], C["paper"])}</span>'
                   for c in codes)


CSS = f"""
@font-face{{font-family:Anuphan;font-weight:500;src:url({FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url({FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Mitr;font-weight:500;src:url({FONTS}/Mitr-Medium.ttf)}}
@font-face{{font-family:Plex;font-weight:400;src:url({FONTS}/IBMPlexSansThai-Regular.ttf)}}
@font-face{{font-family:Plex;font-weight:600;src:url({FONTS}/IBMPlexSansThai-SemiBold.ttf)}}
@page{{size:{W}mm {H}mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}mm;height:{H}mm;background:{C['paper']};color:{C['ink']};font-family:Plex,sans-serif}}
.page{{width:{W}mm;height:{H}mm;display:flex;flex-direction:column;overflow:hidden}}
/* 1 brand: seen from the aisle, 170-130 cm off the floor */
.brand{{background:{C['cobalt']};color:{C['paper']};height:400mm;padding:60mm 45mm 0;display:flex;flex-direction:column;align-items:center}}
.brand svg{{width:470mm;height:auto;display:block}}
.brand .en{{font-family:Jost;font-weight:500;font-size:40mm;letter-spacing:.04em;margin-top:8mm}}
.brand .th{{font-family:Anuphan;font-weight:500;font-size:34mm;margin-top:4mm;margin-bottom:14mm}}
.brand .day{{margin-top:auto;margin-bottom:26mm;font-size:19mm;color:{C['sun']};text-align:center;line-height:1.35}}
/* 2 hook and price */
.hook{{height:330mm;padding:40mm 40mm 0;display:flex;flex-direction:column;gap:22mm}}
.hook h1{{font-family:Anuphan;font-weight:500;font-size:56mm;line-height:1.22}}
.hook h1 em{{font-style:normal;color:{C['tomato']}}}
.hook .row{{display:flex;align-items:center;justify-content:space-between;gap:20mm}}
.cta{{background:{C['ink']};color:{C['paper']};border-radius:40mm;padding:12mm 26mm;font-family:Anuphan;font-weight:500;font-size:30mm}}
.price{{flex:none;width:150mm;height:150mm;border-radius:50%;background:{C['tomato']};color:#FFFFFF;display:flex;flex-direction:column;
  align-items:center;justify-content:center;line-height:1;margin-top:-30mm}}
.price i{{font-style:normal;font-size:20mm}}.price b{{font-family:Jost;font-weight:500;font-size:66mm;margin:3mm 0}}
/* 3 contact: scanned from about 1 m */
.contact{{margin:0 30mm;background:#FFFFFF;border-radius:21mm;padding:20mm;display:flex;gap:20mm;align-items:center}}
.qr{{flex:none;width:200mm;text-align:center;font-size:17mm;color:#4A4A55}}
.qr svg{{width:200mm;height:200mm;display:block}}
.ch{{display:flex;flex-direction:column;gap:7mm;min-width:0}}
.ch .h{{font-family:Jost;font-weight:500;font-size:29mm;color:{C['cobalt']};letter-spacing:.01em}}
.ch .l{{font-size:17mm;line-height:1.3}}
.ch .o{{font-size:17mm;line-height:1.35;color:#4A4A55;border-top:1.2mm solid #F1DCCB;padding-top:7mm}}
/* 4 products */
.goods{{padding:30mm 30mm 0;flex:1;display:flex;flex-direction:column;gap:12mm}}
.goods .t{{font-family:Anuphan;font-weight:500;font-size:26mm;padding-left:6mm}}
.grid{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12mm}}
.cell{{background:#FFFFFF;border-radius:16mm;padding:12mm;display:flex;flex-direction:column;align-items:center;gap:4mm;height:136mm}}
.art{{height:64mm;width:100%;display:flex;align-items:center;justify-content:center;gap:3mm;flex-wrap:nowrap;overflow:hidden}}
.pc{{min-width:0;display:flex}}.pc svg{{height:62mm;width:auto;max-width:100%;display:block}}.pc.s svg{{height:34mm}}.pc.strap svg{{height:auto;width:120mm}}
.cell .n{{font-size:17mm;text-align:center;line-height:1.2}}
.cell .p{{font-family:Jost;font-weight:500;font-size:30mm;color:{C['tomato']};line-height:1}}
.cell .p small{{font-family:Plex;font-size:15mm;color:#4A4A55}}
/* 5 collections band */
.foot{{background:{C['ink']};color:{C['paper']};height:118mm;padding:0 40mm;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:4mm}}
.foot .c{{font-family:Jost;font-weight:500;font-size:24mm;letter-spacing:.04em}}
.foot .c span{{font-family:Mitr;font-weight:500}}
.foot .s{{font-size:15mm;color:#C9C4D6}}
"""


def page():
    goods = "".join(
        f'<div class="cell"><div class="art">{art(codes)}</div><div class="n">{P[n]["name"]}</div>'
        f'<div class="p">{P[n]["price"]} <small>บาท</small></div></div>' for n, codes in SHOW)
    low = min(p["price"] for p in B.PRODUCTS)
    h = B.BRAND["handle"]
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><title>OCT. 26 X-stand 60 x 160 cm</title><style>{CSS}</style></head><body>
<div class="page">
<section class="brand">{logo("oct-wordmark-reverse.svg")}
<div class="en">{B.BRAND['tag_en']}</div><div class="th">{B.BRAND['tag_th']}</div>
<div class="day">26 ตุลาคม วันเกิดของแม่<br>และวันที่แบรนด์นี้เกิด</div></section>
<section class="hook"><h1>ของใช้จาก<em>เศษหนังแท้</em><br>ทำกันเองทั้งบ้าน</h1>
<div class="row"><div class="cta">เข้ามาลองต่อเองได้</div><div class="price"><i>เริ่ม</i><b>{low}</b><i>บาท</i></div></div></section>
<section class="contact"><div class="qr">{qr_svg()}<div>สแกนติดตาม</div></div>
<div class="ch"><div class="h">@{h}</div>
<div class="l">Instagram · Facebook<br>YouTube</div>
<div class="l">ค้นหา OCT. 26</div>
<div class="o">สั่งทำเป็นชุด ของชำร่วย<br>ของขวัญองค์กร ทักไอจีได้เลย</div></div></section>
<section class="goods"><div class="t">มีอะไรขายบ้าง</div><div class="grid">{goods}</div></section>
<section class="foot"><div class="c">SOI. 02 · <span>ห้าหมี</span> FIVE BEARS</div><div class="s">หนังแท้ทุกชิ้น สีและลายไม่ซ้ำกัน เพราะทำจากเศษหนังจริง</div></section>
</div></body></html>"""


if __name__ == "__main__":
    open(os.path.join(HERE, "xstand.html"), "w").write(page())
    print("wrote xstand/xstand.html · QR ->", QR_URL)
