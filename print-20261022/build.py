"""A4 print set for the booth on 23 Oct, home printer only (owner, 22 Oct). Mock-up for the owner to check.

The booth sells the five cut pieces 01–05 as they are, 30 THB each; what each piece can become goes in an A4 idea
folder for customers to flip through, to be filled by Product Development (PD). Every sheet is A4 with crop marks
where it needs cutting. No 06, no joining or no-sew claim.
python3 print-20261022/build.py && node print-20261022/render.mjs -> oct26-print-a4.pdf, preview/pNN.png, site/
"""
import html, importlib.util, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BRAND = os.path.join(REPO, "brand-20261014")
sys.path.insert(0, BRAND)
import brand as B


def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


PB = _load("posters_build", os.path.join(BRAND, "posters", "build.py"))
S = _load("brand_site", os.path.join(BRAND, "site", "build.py"))
E = html.escape
C = B.C
FONTS = "file://" + os.path.join(BRAND, "fonts")
PRICE = 30
H = B.BRAND["handle"]
LINE_QR = "file://" + os.path.join(BRAND, "line", "L_gainfriends_2dbarcodes_BW.png")
SIZE = {"01": "10.4", "02": "9", "03": "9", "04": "9", "05": "9"}          # cm, from the die files
PIECES = [(c, B.PIECE_NAME[c].rsplit(" ", 1)[0]) for c in ("01", "02", "03", "04", "05")]
# examples only, single pieces, until PD decides (status doc 21 Oct: nothing joined, no 06)
IDEAS = {
    "01": ["ที่รองแก้ว", "ที่เก็บสายชาร์จ: พันสายรอบหัว เหน็บปลายเข้าร่อง", "เขียนชื่อ ห้อยกระเป๋า"],
    "02": ["ที่รองแก้ว", "ที่พันสายหูฟังหรือด้าย", "รองแจกันหรือกระถางเล็ก"],
    "03": ["ป้ายห้อยของขวัญ: เขียนชื่อ ร้อยเชือกผ่านร่อง", "ที่รองแก้วเล็ก", "ที่คั่นหนังสือ"],
    "04": ["ที่รองแก้ว", "ที่รองถ้วยชาหรือแก้วเทียน", "แปะโน้ตบนโต๊ะทำงาน"],
    "05": ["ที่รองแก้ว", "รองกระถางต้นไม้เล็ก", "ฐานรองของจุกจิกบนโต๊ะ"],
}
ACC = {"01": C["pink"], "02": C["sun"], "03": C["mint"], "04": C["cobalt"], "05": C["tomato"]}

CSS = f"""
@font-face{{font-family:Anuphan;font-weight:500;src:url({FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url({FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Plex;font-weight:400;src:url({FONTS}/IBMPlexSansThai-Regular.ttf)}}
@font-face{{font-family:Plex;font-weight:600;src:url({FONTS}/IBMPlexSansThai-SemiBold.ttf)}}
@page{{size:210mm 297mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Plex,sans-serif;color:{C['ink']};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{position:relative;width:210mm;height:297mm;overflow:hidden;page-break-after:always;background:#fff}}
.cell{{position:absolute;overflow:hidden}}
.mk{{position:absolute;background:#000}}
.note{{position:absolute;font-size:2.6mm;color:#777;font-family:Plex}}
.pc svg{{width:100%;height:auto;display:block}}
h1,h2{{font-family:Anuphan;font-weight:500;line-height:1.15}}
.jost{{font-family:Jost;font-weight:500}}
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


def piece(code, mm, fill=C["leather"]):
    return f'<div class="pc" style="width:{mm}mm">{PB.icon(code, fill, "#FFFFFF")}</div>'


def word(mm, rev=False):
    return f'<div style="width:{mm}mm">{PB._logo("oct-wordmark-reverse.svg" if rev else "oct-wordmark.svg")}</div>'


# ------------------------------------------------------------------ sheet 1: price sign, two A5 per A4
def price_sign():
    row = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:1.5mm;width:34mm">'
                  f'{piece(c, 31 if c == "01" else 28)}<div class="jost" style="font-size:4mm">{c}</div>'
                  f'<div style="font-size:3.5mm;text-align:center;line-height:1.2">{E(n)}</div></div>' for c, n in PIECES)
    one = (f'<div style="position:absolute;inset:14mm 14mm 16mm;display:flex;flex-direction:column;justify-content:space-between">'
           f'<div style="display:flex;justify-content:space-between;align-items:center">{word(40)}'
           f'<span style="font-size:3.4mm;color:#555">หนังวัวแท้ หนา 1.0–1.2 มม.</span></div>'
           f'<div style="display:flex;align-items:baseline;gap:5mm"><h1 style="font-size:14mm">ชิ้นหนังวัวแท้</h1>'
           f'<div style="margin-left:auto;background:{C["tomato"]};color:#fff;border-radius:99mm;padding:2mm 7mm;display:flex;align-items:baseline;gap:2mm">'
           f'<span style="font-size:4.5mm">แผ่นละ</span><b class="jost" style="font-size:13mm;line-height:1">{PRICE}</b><span style="font-size:4.5mm">บาท</span></div></div>'
           f'<div style="display:flex;justify-content:space-between">{row}</div>'
           f'<div style="font-size:4.2mm;line-height:1.45;color:#333">สีและลายแต่ละแผ่นไม่ซ้ำกัน เลือกได้เลย · '
           f'<b>ไปทำอะไรได้บ้าง เปิดดูในแฟ้มได้เลย</b></div></div>')
    cells = "".join(f'<div class="cell" style="left:0;top:{y}mm;width:210mm;height:148.5mm">{one}</div>' for y in (0, 148.5))
    return f'<div class="page">{cells}{marks(ys=(148.5,))}</div>'


# ------------------------------------------------------------------ sheet 2: basket labels 90 x 55, ten per A4
def labels():
    w, h, x0, y0 = 90, 55, 15, 11
    cells = []
    for i in range(10):
        c, n = PIECES[i // 2]
        x, y = x0 + (i % 2) * w, y0 + (i // 2) * h
        cells.append(
            f'<div class="cell" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm;display:flex;align-items:center;gap:5mm;padding:0 7mm">'
            f'<div style="position:absolute;left:0;top:0;bottom:0;width:2.5mm;background:{ACC[c]}"></div>'
            f'{piece(c, 32 if c == "01" else 30)}'
            f'<div style="display:flex;flex-direction:column;gap:1mm"><div class="jost" style="font-size:4mm;color:#555">แบบ {c} · {SIZE[c]} ซม.</div>'
            f'<h2 style="font-size:6.2mm">{E(n)}</h2>'
            f'<div style="display:flex;align-items:baseline;gap:1.5mm;color:{C["tomato"]}"><b class="jost" style="font-size:10mm;line-height:1">{PRICE}</b>'
            f'<span style="font-size:4mm">บาท / แผ่น</span></div></div></div>')
    xs = (x0, x0 + w, x0 + 2 * w)
    ys = tuple(y0 + k * h for k in range(6))
    scale = ('<div class="note" style="left:25mm;bottom:5.5mm;display:flex;align-items:center;gap:2mm">'
             '<div style="width:50mm;height:1.2mm;background:#000"></div>ตรวจขนาด: แถบนี้ต้องยาว 50 มม.</div>')
    return f'<div class="page">{"".join(cells)}{marks(xs, ys)}{scale}</div>'


# ------------------------------------------------------------------ sheet 3: LINE QR cards A6, four per A4
def line_cards():
    one = (f'<div style="position:absolute;inset:9mm;display:flex;flex-direction:column;align-items:center;gap:3.5mm;text-align:center">'
           f'{word(34)}<h2 style="font-size:7mm;margin-top:2mm">แอด LINE ไว้นะ</h2>'
           f'<div style="font-size:3.7mm;line-height:1.4;color:#333">มีลายใหม่ ไอเดียใหม่<br>และรอบบูธหน้า จะบอกทางนี้</div>'
           f'<img src="{LINE_QR}" style="width:52mm;height:52mm;image-rendering:pixelated">'
           f'<div class="jost" style="font-size:4.4mm;color:#06C755">{B.SOCIAL["line_id"]}</div></div>')
    cells = "".join(f'<div class="cell" style="left:{x}mm;top:{y}mm;width:105mm;height:148.5mm">{one}</div>'
                    for y in (0, 148.5) for x in (0, 105))
    return f'<div class="page">{cells}{marks((105,), (148.5,))}</div>'


# ------------------------------------------------------------------ sheets 4–10: idea folder, no cutting
def folder_cover():
    pcs = "".join(f'<div style="position:absolute;left:{x}mm;top:{y}mm;transform:rotate({r}deg)">{piece(c, 55 if c == "01" else 50)}</div>'
                  for c, x, y, r in (("01", 20, 150, -10), ("02", 88, 170, 8), ("03", 145, 150, -6), ("04", 40, 215, 12), ("05", 115, 220, -4)))
    return (f'<div class="page"><div style="position:absolute;left:20mm;right:20mm;top:24mm;display:flex;flex-direction:column;gap:6mm">'
            f'{word(70)}<h1 style="font-size:15mm;margin-top:8mm">ชิ้นหนังหนึ่งแผ่น<br>ไปเป็นอะไรได้บ้าง</h1>'
            f'<p style="font-size:5mm;line-height:1.5;color:#333">พลิกดูทีละแบบ เลือกแผ่นที่ชอบ แล้วเอาไปใช้ตามไอเดีย<br>'
            f'ชิ้นหนังวัวแท้ แผ่นละ {PRICE} บาท</p></div>{pcs}'
            f'<div class="note" style="left:20mm;bottom:12mm;font-size:3.4mm">ร่าง · ไอเดียในแฟ้มเป็นตัวอย่าง รอฝ่ายพัฒนาสินค้าสรุป</div></div>')


def folder_page(c, n):
    ideas = "".join(f'<li style="margin-bottom:3mm">{E(t)}</li>' for t in IDEAS[c])
    return (f'<div class="page"><div style="position:absolute;left:0;top:0;bottom:0;width:6mm;background:{ACC[c]}"></div>'
            f'<div style="position:absolute;left:20mm;right:20mm;top:20mm;display:flex;justify-content:space-between;align-items:baseline">'
            f'<div><div class="jost" style="font-size:6mm;color:#555">แบบ {c}</div><h1 style="font-size:14mm">{E(n)}</h1></div>'
            f'<div style="text-align:right"><b class="jost" style="font-size:14mm;color:{C["tomato"]}">{PRICE}</b><div style="font-size:4mm">บาท / แผ่น</div></div></div>'
            f'<div style="position:absolute;left:0;right:0;top:62mm;display:flex;flex-direction:column;align-items:center;gap:3mm">'
            f'{piece(c, float(SIZE[c]) * 10 * (1.03 if c == "01" else 1.0))}'
            f'<div style="font-size:3.6mm;color:#555">ขนาดจริง {SIZE[c]} ซม. · วางชิ้นหนังทับดูได้</div></div>'
            f'<div style="position:absolute;left:20mm;right:20mm;top:190mm;display:flex;flex-direction:column;gap:4mm">'
            f'<h2 style="font-size:7.5mm">ไปเป็นอะไรได้บ้าง</h2>'
            f'<ul style="font-size:5.2mm;line-height:1.45;padding-left:6mm">{ideas}</ul>'
            f'<div style="border:0.4mm dashed #999;border-radius:3mm;padding:4mm;font-size:3.8mm;color:#666;height:24mm">'
            f'รูปจริงและวิธีทำ: รอฝ่ายพัฒนาสินค้าสรุป</div></div>'
            f'<div class="note" style="left:20mm;bottom:12mm;font-size:3.4mm">ร่าง · @{H} · LINE {B.SOCIAL["line_id"]}</div></div>')


def folder_back():
    return (f'<div class="page"><div style="position:absolute;inset:40mm 25mm;display:flex;flex-direction:column;align-items:center;gap:7mm;text-align:center">'
            f'{word(60)}<h1 style="font-size:11mm;margin-top:6mm">เลือกได้กี่แผ่นก็ได้<br>แผ่นละ {PRICE} บาท</h1>'
            f'<p style="font-size:5mm;line-height:1.5;color:#333">ลองแต่งชิ้นหนังที่บูธได้ เขียนชื่อหรือวาดลาย<br>แล้วแอด LINE ไว้ มีไอเดียใหม่จะส่งไปให้</p>'
            f'<img src="{LINE_QR}" style="width:60mm;height:60mm;image-rendering:pixelated">'
            f'<div class="jost" style="font-size:5mm;color:#06C755">LINE {B.SOCIAL["line_id"]}</div>'
            f'<div class="jost" style="font-size:4.5mm;color:#555">IG @{H} · facebook.com/oct26brand</div></div></div>')


SHEETS = [  # (title, how many to print, cutting, html)
    ("ป้ายราคา A5", "1 แผ่น ได้ 2 ป้าย", "ตัดครึ่งตามขีดกลางแผ่น ใส่กรอบอะคริลิก A5", price_sign),
    ("ป้ายชื่อแบบ 9 × 5.5 ซม.", "1 แผ่น ได้ 10 ป้าย (แบบละ 2)", "ตัดตามขีดทุกเส้น หนีบไม้หนีบผ้าที่ตะกร้าแต่ละลาย", labels),
    ("การ์ด QR LINE A6", "1 แผ่น ได้ 4 ใบ", "ตัดตามขีดกลางทั้งแนวตั้งและแนวนอน วางโต๊ะจ่ายเงินและจุด DIY", line_cards),
    ("แฟ้มไอเดีย: ปก", "1 แผ่น", "ไม่ต้องตัด ใส่แฟ้มซองใส A4", folder_cover),
] + [(f"แฟ้มไอเดีย: แบบ {c}", "1 แผ่น", "ไม่ต้องตัด ใส่แฟ้ม · ชิ้นหนังขนาดจริง", (lambda c=c, n=n: folder_page(c, n))) for c, n in PIECES] + [
    ("แฟ้มไอเดีย: ปกหลัง", "1 แผ่น", "ไม่ต้องตัด ใส่แฟ้ม", folder_back),
]


def summary(n_pages):
    rows = "".join(f'<tr><td class="mono">{i}</td><td><b>{E(t)}</b></td><td>{E(q)}</td><td>{E(cut)}</td></tr>'
                   for i, (t, q, cut, _) in enumerate(SHEETS, 1))
    figs = "".join(f'<figure style="margin:0;display:flex;flex-direction:column;gap:6px"><img src="p{i:02d}.png" alt="{E(t)}" loading="lazy" '
                   f'style="border:1px solid var(--line);border-radius:6px;background:#fff"><figcaption class="cap">{i} · {E(t)}</figcaption></figure>'
                   for i, (t, *_) in enumerate(SHEETS, 1))
    return f"""{S.head("OCT. 26 ไฟล์พิมพ์ A4")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">บูธ 23 ต.ค. · ร่างให้ตรวจ</span><h1>ไฟล์พิมพ์ A4 สำหรับบูธ</h1>
<p class="lead">ขายชิ้นหนัง 5 แบบ แผ่นละ {PRICE} บาท พิมพ์จากเครื่องที่บ้านได้ทั้งหมด {n_pages} แผ่น A4
ตัดตามขีดที่ขอบกระดาษ ไอเดียในแฟ้มเป็นตัวอย่าง รอฝ่ายพัฒนาสินค้าสรุป</p></header>
<section><h2>วิธีพิมพ์</h2><div class="card"><ol>
<li>เปิด PDF แล้วสั่งพิมพ์ <b>ขนาดจริง 100%</b> (Actual size) ห้ามเลือกพอดีหน้า (Fit)</li>
<li>พิมพ์หน้า 2 ก่อน วัดแถบตรวจขนาดที่ขอบล่าง ต้องยาว 50 มม. ถ้าไม่ใช่ ตั้งค่าใหม่</li>
<li>ขีดดำสั้น ๆ ที่ขอบกระดาษคือเส้นตัด วางไม้บรรทัดต่อขีดสองฝั่งแล้วตัดด้วยคัตเตอร์</li>
<li>กระดาษหนา 160–200 แกรมจะตั้งได้ดีกว่า ถ้ามีแค่ 80 แกรม ป้ายชื่อและการ์ด LINE ให้ติดบนเศษฟิวเจอร์บอร์ด</li></ol></div></section>
<section><h2>รายการพิมพ์</h2><div class="tbl"><table><thead><tr><th>หน้า</th><th>อะไร</th><th>ได้กี่ชิ้น</th><th>ตัด / ใช้</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section><h2>ตัวอย่างทุกหน้า</h2><div class="grid">{figs}</div></section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>
<li>ราคาแผ่นละ {PRICE} บาท ตามที่พ่อเบสั่ง 22 ต.ค. ใช้แทนราคา 7 แบบเดิม</li>
<li>5 แบบคือ 01 หัวหมี · 02 กังหัน · 03 กากบาทแคปซูล · 04 สี่เหลี่ยมมน · 05 วงกลม (ไม่มี 06 และยังไม่ใส่ 07)</li>
<li>ไอเดียในแฟ้มเป็นตัวอย่างใช้ชิ้นเดียว ไม่มีการต่อชิ้น ฝ่ายพัฒนาสินค้าจะส่งไอเดียจริงพร้อมรูปมาแทน</li>
<li>QR LINE ในไฟล์เปิด lin.ee/O9AePgp สแกนดูอีกครั้งว่าขึ้นบัญชี OCT. 26</li></ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">print-20261022/oct26-print-a4.pdf</td><td>ไฟล์พิมพ์ทั้งหมด {n_pages} หน้า</td></tr>
<tr><td class="mono" style="white-space:nowrap">print-20261022/build.py</td><td>แก้ราคา ข้อความ หรือไอเดียที่นี่แล้วรันใหม่</td></tr>
</tbody></table></div></section></div>{S.COPY_JS}"""


if __name__ == "__main__":
    body = "".join(fn() for *_, fn in SHEETS)
    open(os.path.join(HERE, "print.html"), "w").write(
        f'<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(summary(len(SHEETS)))
    print("wrote print.html and site/index.html,", len(SHEETS), "pages")
