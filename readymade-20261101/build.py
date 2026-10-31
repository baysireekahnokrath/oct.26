"""Price cards for ready-made 07 pieces at the booth, 1 Nov (owner, 31 Oct: joined pieces sell because people see them
finished; DIY drawing does not; make ready-to-buy goods: see it, see the price, pick it up, pay).

Owner's construction (31 Oct): cup sleeve = 4 pieces a tier + 1 for the bottom, 1–3 tiers by cup height; basket = a base
of a x b pieces and one wall tier (two tiers sag, the leather is soft). Price rule proposed: 30 a piece as at the booth
plus about 30 for assembly, ending in 9. A4, six cards 95 x 90 mm with crop marks; the bouquet card has a blank price.
python3 readymade-20261101/build.py && node print-20261022/render.mjs ../readymade-20261101/cards.html ../readymade-20261101/oct26-readymade-cards.pdf
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "print-20261022"))
import build as P

E = P.E
W, H, COLS, ROWS = 95, 90, 2, 3
X0, Y0 = (210 - COLS * W) / 2, (297 - ROWS * H) / 2


def sleeve_pieces(tiers):
    return 4 * tiers + 1


def basket_pieces(a, b):
    return a * b + 2 * (a + b)


def price(pieces, extra=0):
    """30 a piece + about 30 for assembly + extras, rounded up to end in 9."""
    p = pieces * 30 + 30 + extra
    return p + (9 - p % 10) % 10


SLEEVE = [(f"{t} ชั้น", sleeve_pieces(t), price(sleeve_pieces(t))) for t in (1, 2, 3)]
BASKET = [(f"ก้น {a} × {b}", basket_pieces(a, b), price(basket_pieces(a, b))) for a, b in ((2, 2), (2, 3), (3, 3))]
CHARM_S, CHARM_M = price(3, 20), price(5, 20)          # with one cord
PET = price(3, 20)                                    # three names on three pieces, cord, writing included

CARDS = [  # (title, sub, rows [(label, price)], note)
    ("07 ปลอกแก้ว", "ชั้นละ 4 ชิ้น + ก้น 1 ชิ้น เลือกตามความสูงของแก้ว",
     [(f"{l} · {n} ชิ้น", p) for l, n, p in SLEEVE], "ไม่สูงถึงขอบแก้ว · ไม่ใช่ภาชนะใส่อาหาร"),
    ("07 ตะกร้าใส่ของ", "ขอบชั้นเดียว ทรงอยู่ตัว เลือกขนาดก้น",
     [(f"{l} · {n} ชิ้น", p) for l, n, p in BASKET], "ขนาดอื่นสั่งทำได้ ทัก LINE @155riuqj"),
    ("07 charm คล้องกระเป๋า", "ชิ้นหนังเรียงเส้น พร้อมสายคล้อง",
     [("S · 3 ชิ้น", CHARM_S), ("M · 5 ชิ้น", CHARM_M)], "ของตกแต่ง ไม่ใช่ที่แขวนของหนัก"),
    ("07 ป้ายชื่อสัตว์เลี้ยง", "เขียนชื่อให้ที่บูธ ห้อยรถเข็น กรง หรือกระเป๋า",
     [("3 ชื่อ · 3 ชิ้น", PET), ("เพิ่มชื่อละ", 30)], "รอเขียนแป๊บเดียว"),
    ("07 ช่อดอกไม้", "ห้อยกระเป๋า หรือแขวนประดับ ทุกช่อไม่ซ้ำกัน",
     [("ช่อนี้", None)], "ของตกแต่ง ไม่ใช่ที่แขวนของหนัก"),
    ("ของพร้อมใช้", "จ่ายที่โต๊ะ โอนหรือเงินสด",
     [], "ชิ้นหนังแผ่นละ 30.- ยังมีให้เลือกไปทำเอง"),
]


def card(title, sub, rows, note):
    lines = "".join(
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:1.6mm 0;border-top:0.3mm solid {P.LINE}">'
        f'<span style="font-size:4mm">{E(l)}</span>'
        + (f'<span class="jost" style="font-size:7mm">{p}.-</span>' if p is not None
           else f'<span style="font-size:4mm;border-bottom:0.3mm solid {P.INK};width:30mm;text-align:right">.-</span>')
        + '</div>' for l, p in rows)
    big = (f'<div class="jost" style="font-size:11mm;line-height:1;margin-top:4mm">หยิบได้เลย</div>' if not rows else "")
    return (f'<div style="position:absolute;inset:7mm 8mm;display:flex;flex-direction:column;gap:2mm">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start">{P.logo(12)}{P.band(1, "16mm")}</div>'
            f'<h2 style="font-size:6.6mm;margin-top:1mm">{E(title)}</h2><div class="mu" style="font-size:3.4mm;line-height:1.4">{E(sub)}</div>'
            f'{big}<div style="margin-top:2mm">{lines}</div>'
            f'<div class="mu" style="margin-top:auto;font-size:3mm">{E(note)}</div></div>')


def sheet():
    cells = "".join(f'<div class="cell" style="left:{X0 + (i % COLS) * W}mm;top:{Y0 + (i // COLS) * H}mm;width:{W}mm;height:{H}mm">{card(*c)}</div>'
                    for i, c in enumerate(CARDS))
    xs = tuple(X0 + k * W for k in range(COLS + 1))
    ys = tuple(Y0 + k * H for k in range(ROWS + 1))
    return f'<div class="page">{cells}{P.marks(xs, ys, inset=3, length=6)}</div>'


def summary():
    import importlib.util
    sp = importlib.util.spec_from_file_location("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
    S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
    rows = "".join(f"<tr><td>{E(c[0])}</td><td>{E(' · '.join(f'{l} {p}.-' if p is not None else f'{l} เขียนราคาเอง' for l, p in c[2]))}</td></tr>" for c in CARDS[:5])
    return f"""{S.head("OCT. 26 ป้ายราคาของพร้อมใช้")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">บูธวันสุดท้าย 1 พ.ย. · ร่างให้ตรวจ</span><h1>ป้ายราคาของพร้อมใช้</h1>
<p class="lead">ของที่ต่อชิ้นเสร็จแล้ว เห็นแบบ เห็นราคา หยิบ จ่าย · A4 แผ่นเดียวได้ 6 ป้าย ตัดตามขีด</p></header>
<section><img src="cards.png" alt="ป้ายราคา 6 ใบ" style="width:100%;max-width:520px;border:1px solid var(--line);border-radius:6px;background:#fff"></section>
<section><h2>ราคา</h2><div class="tbl"><table><tbody>{rows}</tbody></table></div>
<p class="cap">สูตร: ชิ้นละ 30 + ค่าประกอบราว 30 (+ สาย 20) ปัดลงท้าย 9 · ปลอกแก้วชั้นละ 4 ชิ้น + ก้น 1 · ตะกร้า ก้น a × b + ขอบชั้นเดียว 2(a + b) ชิ้น (เจ้าของ 31 ต.ค.: 2 ชั้นย้วยเพราะหนังนิ่ม)</p></section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>
<li>สูตรนับชิ้นของตะกร้าเป็นการคำนวณ ถ้าของจริงใช้ไม่เท่านี้ บอกจำนวนจริง จะแก้ราคาให้</li>
<li>ช่อดอกไม้เว้นราคาไว้ให้เขียนเอง เพราะแต่ละช่อใช้ชิ้นไม่เท่ากัน</li>
<li>charm และป้ายชื่อห้อยกับกระเป๋า รอพ่อเบยืนยันว่ายกเว้นกฎของห้อยต้องใช้หนัง 2 มม.</li></ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono">readymade-20261101/oct26-readymade-cards.pdf</td><td>พิมพ์ขนาดจริง 100%</td></tr>
<tr><td class="mono">readymade-20261101/build.py</td><td>แก้ราคาหรือข้อความแล้วรันใหม่</td></tr></tbody></table></div></section></div>"""


if __name__ == "__main__":
    for t, s, rows, n in CARDS:
        for word in ("ไม่ต้องเย็บ", "ต่อเอง", "หัวใจ"):
            assert word not in t + s + n, word
    open(os.path.join(HERE, "cards.html"), "w").write(
        f'<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{P.CSS}</style></head><body>{sheet()}</body></html>')
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(summary())
    print("sleeve", SLEEVE, "basket", BASKET, "charm", CHARM_S, CHARM_M, "pet", PET)
