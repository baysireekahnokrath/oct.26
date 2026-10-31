"""Price and use signs for the home and garden fair booth (30 Oct - 1 Nov 2026).

Owner 30 Oct: people at the fair don't know what the pieces are for or what they cost, and are shy to ask
in case they then don't buy. So every sign answers both before anyone has to ask, and says it is fine to just look.
Uses are single pieces only (no joining, no food contact). Booth price is 30 baht per piece (owner 22 Oct).

Collect all six (owner 30 Oct): the sign and collector cards come from sx2026-20261106 without the SX header.

python3 build.py -> signs.html, collect.html;  node render.cjs -> OCT26-fair-price-signs-A4.pdf, OCT26-fair-collect-A4.pdf + preview/*.png
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "sx2026-20261106"))
from build import LINE, LINE_ID, REWARD_TH, logo, photo, band, qr, css, collect_doc  # noqa: E402

PRICE = 30
# code, Thai name, plan photo, uses (single piece only)
PIECES = [("01", "หมี", "01-1", ["ที่รองแก้ว", "ที่เก็บสายชาร์จ"]),
          ("02", "กังหัน", None, ["ที่รองแก้ว"]),
          ("03", "กากบาทแคปซูล", "03-1", ["ป้ายห้อยของขวัญ"]),
          ("04", "สี่เหลี่ยมมน", "04-2", ["ที่รองแก้ว"]),
          ("05", "วงกลม", "05-1", ["ที่รองแก้ว"]),
          ("07", "กากบาทข้อต่อวงกลม", "07-2", ["ที่รองแก้ว"])]
OTHERS = [("กระเป๋าซิปหนัง 3 สี", 200), ("สายห้อยข้อมือ 3 สี", 20), ("ชิ้นรูปดาว พระจันทร์ ดอกไม้", 30)]

S = 'fill="none" stroke="#2A2725" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "cup": f'<svg viewBox="0 0 100 100"><ellipse cx="50" cy="82" rx="38" ry="9" fill="#B07A4A"/><path {S} d="M30 30h40l-5 48H35z"/><path {S} d="M70 40h8a8 8 0 0 1 0 16h-10"/></svg>',
    "tag": f'<svg viewBox="0 0 100 100"><rect x="14" y="44" width="46" height="40" rx="3" {S}/><path {S} d="M14 56h46M37 44v40"/><path {S} d="M37 44c-8-12 6-16 0 0c-6-16 8-12 0 0"/><path {S} d="M60 48l14-14"/><path d="M70 22h18v18l-14 14-18-18z" fill="#B07A4A"/><circle cx="80" cy="30" r="3" fill="#F4F0E8"/></svg>',
    "pen": f'<svg viewBox="0 0 100 100"><circle cx="40" cy="58" r="30" fill="#B07A4A"/><path {S} d="M30 58c6-8 14 8 20 0"/><path {S} d="M62 18l20 20-30 30-14 4 4-14z" fill="#F4F0E8"/></svg>',
    "cable": f'<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="30" fill="#B07A4A"/><path {S} d="M10 30c20 0 20 40 40 40s20-40 40-40"/><rect x="82" y="24" width="12" height="12" rx="2" {S}/></svg>',
}

EXTRA = """
.pg{padding:14mm 14mm 0}
.logo{width:22mm;height:22mm;display:block}
.price{display:flex;align-items:baseline;gap:4mm;margin-top:8mm}
.price b{font-family:Jost;font-weight:500;font-size:52mm;line-height:.9}
.price span{font-family:Anuphan;font-size:16mm}
.h1{font-family:Anuphan;font-size:13mm;line-height:1.15;margin-top:2mm}
.collect{margin-top:5mm;background:#E9A825;border-radius:4mm;padding:4mm 6mm;display:grid;gap:1mm}
.collect b{font-family:Anuphan;font-weight:500;font-size:8mm;line-height:1.15}
.collect span{font-size:5mm}
.calm{margin-top:6mm;font-size:6.6mm;line-height:1.45;background:#FBF8F2;border-radius:4mm;padding:4mm 6mm}
.uses{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:6mm}
.use{display:grid;justify-items:center;text-align:center;gap:2mm}
.use svg{width:34mm;height:34mm}
.use b{font-family:Anuphan;font-weight:500;font-size:7.5mm}
.use span{font-size:5mm;color:#4A4542;line-height:1.35}
.others{position:absolute;left:14mm;right:14mm;bottom:12mm;display:flex;gap:6mm;align-items:center;border-top:.4mm solid #DCD4C7;padding-top:4mm}
.others ul{list-style:none;margin:0;padding:0;flex:1;display:grid;gap:1mm;font-size:5mm}
.others li{display:flex;justify-content:space-between} .others li b{font-family:Jost;font-weight:500}
.others .q{display:grid;justify-items:center;font-family:Jost;font-size:3.4mm;gap:1mm} .others .qr{width:24mm;height:24mm}
.tbl{margin-top:5mm;display:grid;gap:2.5mm}
.row{display:grid;grid-template-columns:28mm 1fr 30mm;gap:5mm;align-items:center;background:#FBF8F2;border-radius:3mm;padding:2mm 4mm}
.row .ph{width:28mm}
.row h2{font-size:7mm} .row h2 i{font-style:normal;font-family:Jost;margin-right:2mm}
.row p{font-size:5mm;margin-top:1mm;line-height:1.35}
.row .pr{font-family:Jost;font-weight:500;font-size:12mm;text-align:right}
.row .pr small{font-family:Plex;font-size:4.5mm;font-weight:400}
.foot{font-size:4mm;color:#6E6A64;margin-top:4mm}
/* basket cards: eight per sheet, cut on the dashed lines */
.cards{padding:0;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(4,1fr);background:#fff}
.card{position:relative;background:#F4F0E8;border:.3mm dashed #B8B0A4;padding:5mm 6mm;display:grid;grid-template-columns:30mm 1fr;gap:4mm;align-items:center;overflow:hidden}
.card .ph{width:30mm}
.card h3{font-size:6mm;line-height:1.15} .card h3 i{font-style:normal;font-family:Jost;margin-right:1.5mm}
.card p{font-size:4.2mm;margin-top:1mm;line-height:1.3}
.card .pr{font-family:Jost;font-weight:500;font-size:15mm;line-height:1;margin-top:2mm}
.card .pr small{font-family:Plex;font-size:5mm;font-weight:400}
.card .band{height:2mm}
.staff h2{font-family:Anuphan;font-size:7mm;margin:7mm 0 2mm}
.staff ul{margin:0;padding-left:6mm;font-size:5mm;line-height:1.6}
.staff .say{font-size:5.6mm;line-height:1.5;background:#FBF8F2;border-left:1.5mm solid #2A2725;padding:3mm 4mm;margin:2mm 0 0}
"""


def uses_txt(u):
    return " · ".join(u) + " · เขียนชื่อ วาดลายเองได้"


def build():
    uses = (f'<div class="use">{ICONS["cup"]}<b>วางแก้ว</b><span>ที่รองแก้ว หนังวัวแท้<br>ไม่ใช่ภาชนะใส่อาหาร</span></div>'
            f'<div class="use">{ICONS["tag"]}<b>ห้อยของขวัญ</b><span>ป้ายชื่อติดกล่อง<br>เขียนชื่อคนรับ</span></div>'
            f'<div class="use">{ICONS["pen"]}<b>แต่งเอง</b><span>วาดลาย เขียนชื่อ<br>ที่โต๊ะนี้ได้เลย</span></div>')
    others = "".join(f'<li>{n}<b>{p}.-</b></li>' for n, p in OTHERS)
    p1 = f'''<section class="pg">{logo()}
<div class="price"><b>{PRICE}</b><span>บาท ทุกชิ้น</span></div>
<p class="h1">ชิ้นหนังวัวแท้ เอาไปทำอะไรได้บ้าง</p>
<div class="uses">{uses}</div>
<p class="calm">หยิบดูได้ ลองจับได้ ถามได้ทุกอย่าง <b>ไม่ซื้อก็ไม่เป็นไรครับ</b></p>
<div class="collect"><b>สะสมครบ 6 ลาย {REWARD_TH}</b><span>ขอบัตรสะสมฟรีที่โต๊ะ ซื้อลายไหน พี่เซ็นช่องนั้นให้ · เลือกลายเองทุกชิ้น ไม่มีการสุ่ม</span></div>
<div class="others"><ul>{others}</ul><div class="q">{qr(LINE)}LINE {LINE_ID}</div></div>
{band()}</section>'''

    rows = "".join(f'<div class="row">{photo(c, pl)}<div><h2><i>{c}</i>{th}</h2><p>{uses_txt(u)}</p></div><p class="pr">{PRICE}<small> บาท</small></p></div>'
                   for c, th, pl, u in PIECES)
    p2 = f'''<section class="pg">{logo()}
<p class="h1" style="margin-top:6mm">ชิ้นไหน ใช้ทำอะไร</p>
<div class="tbl">{rows}</div>
<p class="foot">หนังวัวแท้จากเศษหนัง หนา 1.0–1.2 มม. · กว้างประมาณ 9–10 ซม. · ใช้รองแก้วได้ แต่ไม่ใช่ภาชนะใส่อาหาร · ไม่ใช่ของเล่นเด็กเล็ก</p>
{band()}</section>'''

    cards = [f'<div class="card">{photo(c, pl)}<div><h3><i>{c}</i>{th}</h3><p>{" · ".join(u)}</p><p class="pr">{PRICE}<small> บาท</small></p></div>{band()}</div>'
             for c, th, pl, u in PIECES]
    gen = (f'<div class="card" style="grid-template-columns:1fr;background:#E9A825"><div><h3>สะสมครบ 6 ลาย</h3>'
           f'<p>{REWARD_TH}</p><p style="margin-top:2mm">ขอบัตรสะสมฟรีที่โต๊ะ ไม่มีการสุ่ม</p></div>{band()}</div>')
    calm = (f'<div class="card" style="grid-template-columns:1fr"><div><h3>หยิบดูได้เลยครับ</h3><p>ลองจับ ลองวางแก้วได้ ถามได้ทุกอย่าง<br>ไม่ซื้อก็ไม่เป็นไรครับ</p>'
            f'<p class="pr">{PRICE}<small> บาท ทุกชิ้น</small></p></div>{band()}</div>')
    p3 = f'<section class="pg cards">{"".join(cards)}{gen}{calm}</section>'

    p4 = f'''<section class="pg staff">{logo()}<p class="h1" style="margin-top:6mm">สำหรับพี่ที่บูธ</p>
<p class="foot" style="margin-top:1mm">เก็บไว้หลังโต๊ะ ไม่ต้องตั้งโชว์</p>
<h2>ทักก่อน ภายใน 3 วินาทีที่ลูกค้าหยุดมอง</h2>
<p class="say">"หยิบดูได้เลยครับ ชิ้นละ 30 บาท หนังวัวแท้ เอาไว้รองแก้วหรือห้อยของขวัญครับ"</p>
<ul><li>บอกราคาก่อนลูกค้าถาม คนไม่กล้าถามเพราะกลัวถามแล้วไม่ซื้อ</li>
<li>ยื่นชิ้นหนังให้จับ วางแก้วน้ำให้ดูจริง</li>
<li>ถ้าลูกค้าวางคืน: "ไม่เป็นไรครับ แอด LINE เล่นเกมรับฟรี 1 ชิ้นได้นะครับ" แล้วชี้ป้าย LINE</li></ul>
<h2>วางของ</h2>
<ul><li>ป้าย 30 บาท ตั้งหันหน้าออกทางเดิน มองเห็นจากระยะ 3 เมตร</li>
<li>การ์ดเล็กวางหน้าตะกร้าทุกใบ ให้ตรงลาย</li>
<li>ตั้งแก้วน้ำ 1 ใบบนชิ้นหนังให้เห็นว่าเป็นที่รองแก้ว (แก้วเปล่า ไม่ต้องใส่น้ำ)</li>
<li>วางป้ายห้อยของขวัญที่เขียนชื่อแล้ว 1 อันบนกล่องของขวัญ ให้เห็นตัวอย่าง</li></ul>
<h2>บัตรสะสม 6 ลาย</h2>
<ul><li>แจกบัตรฟรีทุกคนที่ซื้อ หรือคนที่ขอ พร้อมบอก "ซื้อครบ 6 ลาย ได้ชิ้นที่ 7 ฟรีครับ"</li>
<li>ซื้อลายไหน เซ็นชื่อย่อกับวันที่ในช่องนั้น 1 ช่องต่อ 1 ชิ้นที่ซื้อ ลายซ้ำไม่ได้ช่องเพิ่ม · ชิ้นฟรีจากเกม LINE ไม่นับ</li>
<li>ครบ 6 ช่อง: ให้เลือกชิ้นฟรี 1 ชิ้น เขียนเลขนักสะสมบนบัตร เริ่ม 001 จดเลขกับวันที่ในสมุด แล้วขีดฆ่าบัตร</li>
<li>ไม่สุ่ม ห้ามบอกว่ามีลายลับหรือลายหายาก</li></ul>
<h2>ห้ามพูด</h2>
<ul><li>ต่อเองได้ ไม่ต้องเย็บ · ใช้กับอาหารได้ · ของเล่นเด็ก · หนังรักษ์โลก</li></ul>
</section>'''
    return (f'<!doctype html><html lang="th"><meta charset="utf-8"><title>OCT. 26 fair price signs</title>'
            f'<style>{css("A4", "210mm", "297mm", EXTRA)}</style>{p1}{p2}{p3}{p4}</html>')


# ------------------------------------------------------------------ table tents (owner 31 Oct)
# A4 portrait folded across into four 74.25 mm strips (owner 31 Oct: the long-side fold was too long, 21 cm is right).
# Owner 31 Oct: artwork in the middle, top and bottom strips fold in and overlap as the base. So strip 2 and 3 are
# the two faces (strip 2 upside down, ridge on the centre fold) and strips 1 and 4 are blank, which also means the
# Epson L3150's 3 mm unprintable edge only ever lands on blank paper. Folds at 74.25, 148.5 and 222.75 mm from the top.
TENT_CSS = """
.pg{padding:0;display:grid;grid-template-rows:repeat(4,1fr);background:#fff}
.strip{position:relative;overflow:hidden;display:grid;align-content:center;padding:0 10mm}
.face{background:#F4F0E8}
.face.flip{transform:rotate(180deg)}
.face .band{height:2.4mm}
.trow{display:flex;align-items:center;gap:5mm}
.face .logo{width:16mm;height:16mm;flex:none}
.big{font-family:Jost;font-weight:500;font-size:34mm;line-height:.8}
.unit{font-family:Anuphan;font-size:10mm;line-height:1.05}
.face b{font-family:Anuphan;font-weight:500;font-size:9mm;line-height:1.15}
.face p{font-size:4.6mm;line-height:1.35;color:#4A4542;margin-top:2mm}
.face svg.ic{width:24mm;height:24mm;flex:none;margin-left:auto}
.pcs{display:flex;gap:2.5mm;margin-top:3mm} .pcs .ph{width:15mm}
.face .qr{width:50mm;height:50mm;flex:none;margin-left:auto}
/* fold marks only: a 1 mm tick inside each side edge (past the printer's 3 mm margin) and a 1 px dot at the centre */
.tk{position:absolute;height:.2mm;width:1mm;background:#8C8A85;transform:translateY(-50%)}
.dt{position:absolute;left:105mm;width:1px;height:1px;background:#8C8A85;transform:translate(-50%,-50%)}
.pg.tent{position:relative}
.blank{justify-items:center;color:#B8B0A4;font-size:3.6mm;letter-spacing:.1em;text-align:center}
"""


def tent_face(inner, flip=False):
    return f'<div class="strip face{" flip" if flip else ""}">{inner}{band()}</div>'


def tent_page(inner):
    flap = '<div class="strip blank">{}</div>'
    marks = "".join(f'<i class="tk" style="top:{y}mm;left:4mm"></i><i class="tk" style="top:{y}mm;right:4mm"></i><i class="dt" style="top:{y}mm"></i>'
                    for y in (74.25, 148.5, 222.75))
    return (f'<section class="pg tent">{flap.format("ฐาน · พับเข้าด้านใน ซ้อนกับแถบล่างสุด แล้วติดเทป")}'
            f'{tent_face(inner, flip=True)}{tent_face(inner)}'
            f'{flap.format("ฐาน · พับเข้าด้านใน ซ้อนกับแถบบนสุด แล้วติดเทป")}{marks}</section>')


def tents():
    ic = lambda k: ICONS[k].replace("<svg ", '<svg class="ic" ', 1)
    price = (f'<div class="trow">{logo()}<span class="big">{PRICE}</span><span class="unit">บาท<br>ทุกชิ้น</span>{ic("cup")}</div>'
             f'<p><b style="font-size:6mm">ชิ้นหนังวัวแท้ รองแก้ว ห้อยของขวัญ แต่งเอง</b><br>หยิบดูได้ ถามได้ทุกอย่าง ไม่ซื้อก็ไม่เป็นไรครับ</p>')
    pieces = "".join(photo(c, pl) for c, _, pl, _ in PIECES)
    collect = (f'<div class="trow">{logo()}<div><b>สะสมครบ 6 ลาย</b><p style="margin-top:0">{REWARD_TH}</p></div></div>'
               f'<div class="pcs">{pieces}</div><p>ขอบัตรสะสมฟรีที่โต๊ะ · เลือกลายเองทุกชิ้น ไม่มีการสุ่ม</p>')
    line = (f'<div class="trow"><div><b>แอด LINE<br>รับชิ้นหนังฟรี 1 ชิ้น</b>'
            f'<p>สแกน QR → เมนู "รับชิ้นหนังฟรี"<br>→ เล่นจับคู่จบ → โชว์หน้าจอให้พี่ที่บูธ<br>คนละ 1 ชิ้น</p></div>{qr(LINE)}</div>')
    body = tent_page(price) + tent_page(collect) + tent_page(line)
    return (f'<!doctype html><html lang="th"><meta charset="utf-8"><title>OCT. 26 table tents</title>'
            f'<style>{css("A4", "210mm", "297mm", EXTRA + TENT_CSS)}</style>{body}</html>')

if __name__ == "__main__":
    open(os.path.join(HERE, "signs.html"), "w", encoding="utf-8").write(build())
    open(os.path.join(HERE, "collect.html"), "w", encoding="utf-8").write(collect_doc(event=False))
    open(os.path.join(HERE, "tent.html"), "w", encoding="utf-8").write(tents())
    print("signs.html, collect.html, tent.html")
