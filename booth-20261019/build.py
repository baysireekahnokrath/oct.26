"""Booth plan for งานบ้านและสวน, 23–25 Oct 2569: one 2 x 2 m booth, gear that is easy to buy.

Reads products and prices from ../brand-20261014/brand.py and the page style from its site/build.py,
writes site/index.html. Run: python3 booth-20261019/build.py
"""
import html, importlib.util, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.join(os.path.dirname(HERE), "brand-20261014")
sys.path.insert(0, BRAND_DIR)
import brand as B

_sp = importlib.util.spec_from_file_location("brand_site", os.path.join(BRAND_DIR, "site", "build.py"))
S = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S)
E = html.escape
P = {p["n"]: p for p in B.PRODUCTS}

FAIR = "งานบ้านและสวน"
DATES = "23–25 ต.ค. 2569"
W = D = 200          # booth, cm
TABLE = (180, 60, 75)  # folding table w, d, h (cm)

# ---------------------------------------------------------------- what sells at a home fair
# People walk in to furnish a home, so the front of the table is a small set coffee table:
# coasters, napkin ring and coffee sleeve in use. FIVE BEARS stays on the right for gifts and kids.
FAIR_HEROES = [29, 22, 15, 4, 14, 13, 21, 23, 30]
PREORDER = [13, 14, 15]   # few in stock, take orders for sets
PRE_CHIP = ' <span class="chip mid">รับสั่งเป็นชุด</span>'

# ---------------------------------------------------------------- gear
# name, qty, where to buy, THB low, THB high, kind, note
# kind: buy = must buy, home = take from home if you have it, opt = nice to have
GEAR = [
    ("โต๊ะพับ 180 × 60 ซม. สูง 75", "1 ตัว", "ถามผู้จัดก่อน มักมีให้ · HomePro, Makro, Shopee", 900, 1500, "home",
     "ถ้าผู้จัดให้โต๊ะ 120 ซม. ตัดโซนกลางเหลือ 40 ซม."),
    ("ผ้าคลุมโต๊ะยาวถึงพื้น สีครีม", "3 ม.", "ร้านผ้า, Shopee (ผ้าดิบหรือแคนวาส)", 250, 400, "buy",
     "คลุมกล่องสต็อกใต้โต๊ะให้มิด"),
    ("ตะแกรงลวดแขวนของ 60 × 150 ซม. พร้อมขาตั้ง", "2 ชุด", "Shopee, HomePro", 700, 1200, "buy",
     "ตั้งชิดผนังหลังซ้ายและขวา ไม่ต้องเจาะผนัง"),
    ("ตะขอแขวนตะแกรงและตะขอตัว S", "40 อัน", "Shopee, ร้าน 20 บาท", 100, 200, "buy", "แขวนราวหมี ที่ห้อยกระเป๋า ป้ายชื่อ"),
    ("ป้ายโรลอัพ 80 × 200 ซม. พร้อมขาตั้ง", "1 ชุด", "ร้านพิมพ์ใกล้บ้าน ส่วนใหญ่เสร็จใน 1 วัน", 600, 1000, "buy",
     "โลโก้ OCT. 26 อยู่ช่วงบน 150–200 ซม. มองเห็นจากทางเดินข้ามหัวคน"),
    ("ลังไม้เล็ก ยกระดับสินค้าบนโต๊ะ", "3 ใบ", "IKEA, Shopee, ร้านต้นไม้ · หรือกล่องรองเท้าห่อผ้า", 300, 750, "buy",
     "วางคว่ำ ทำเป็นขั้นบันได 3 ระดับ"),
    ("ตะกร้าหวายหรือถาดไม้ใบเล็ก", "6 ใบ", "ร้าน 20 บาท, Daiso, จตุจักร", 300, 500, "buy",
     "แยกที่รองแก้วตามลาย ลูกค้าหยิบเลือกเองได้"),
    ("กรอบป้ายอะคริลิกตั้งโต๊ะ A5", "4 อัน", "ร้านเครื่องเขียน, Shopee", 160, 280, "buy",
     "QR พร้อมเพย์ 2 · ป้าย SOI. 02 1 · ป้ายห้าหมี Love 1"),
    ("กรอบป้ายอะคริลิกเล็ก A7", "8 อัน", "ร้านเครื่องเขียน, Shopee", 160, 240, "buy", "ป้ายราคาตามหมวด 8 ใบในรายการพิมพ์"),
    ("โคมไฟหนีบ LED แสงวอร์ม", "3 ดวง", "HomePro, Shopee", 600, 1050, "buy",
     "หนังดูสวยใต้แสงอุ่น ใช้ได้เมื่อบูธมีปลั๊ก (ถามผู้จัด)"),
    ("ปลั๊กพ่วง มอก. ยาว 5 ม.", "1 อัน", "HomePro", 300, 500, "home", ""),
    ("กล่องพลาสติกมีฝา ซ้อนได้", "4 ใบ", "HomePro, Makro", 400, 600, "home", "กล่อง A B C D ตามโซน (ดูลำดับจัดบูธ)"),
    ("เก้าอี้พับหรือสตูล", "2 ตัว", "ถามผู้จัดก่อน", 0, 400, "home", "สำหรับคนสาธิตกับคนเก็บเงิน"),
    ("แผ่นรองตัด A3 หรือผ้าสักหลาด", "1 แผ่น", "ร้านเครื่องเขียน", 100, 200, "buy", "พื้นจุดสาธิต"),
    ("แก้วกาแฟ ผ้าเช็ดปาก จานรอง", "1 ชุด", "จากบ้าน", 0, 0, "home", "ใช้จัดโต๊ะกาแฟจำลอง"),
    ("ต้นไม้กระถางเล็ก", "2 กระถาง", "ซื้อในงานได้เลย", 100, 200, "buy",
     "วางบนที่รองแก้วไส้ไม้ก๊อก เข้าธีมบ้านและสวน และขายที่รองแก้วไปในตัว"),
    ("ของจิปาถะ: เคเบิลไทร์ เทปสองหน้า เทปใส กรรไกร คัตเตอร์ ปากกาเมจิก ถุงขยะ ทิชชู่", "1 ถุง", "ร้าน 20 บาท, 7-Eleven",
     150, 250, "buy", ""),
    ("กล่องเงินและเงินทอน 1,500 บาท", "1 กล่อง", "จากบ้าน", 0, 0, "home", "ใบละ 20 และ 100 กับเหรียญ 10 และ 5"),
    ("ป้ายไวนิลหน้าโต๊ะ 180 × 40 ซม.", "1 ผืน", "ร้านพิมพ์", 150, 300, "opt", "ติดผ้าคลุมด้วยตัวหนีบ คนเดินผ่านเห็นชื่อร้านระดับเข่า"),
    ("กระจกตั้งโต๊ะเล็ก", "1 บาน", "ร้าน 20 บาท", 60, 120, "opt", "ลูกค้าลองห้อยที่ห้อยกระเป๋าแล้วส่องดู"),
    ("รถเข็นพับได้", "1 คัน", "ยืมหรือ HomePro", 600, 900, "opt", "ขนกล่องจากลานจอดถึงฮอลล์ทีเดียวจบ"),
]
KIND = {"buy": ("ต้องซื้อ", "ext"), "home": ("มีที่บ้านใช้ได้", "ok"), "opt": ("มีก็ดี", "mid")}

ASK = [
    ("บูธได้อะไรมาบ้าง", "ผนังกี่ด้าน สูงเท่าไร โต๊ะ เก้าอี้ ป้ายชื่อหน้าบูธ ไฟสปอตไลต์ และปลั๊กไฟกี่วัตต์"),
    ("ป้ายชื่อหน้าบูธ", "ส่งชื่อให้สะกด OCT. 26 ตัวใหญ่ มีจุด และเว้นวรรคก่อน 26"),
    ("เลขบูธ ฮอลล์ โซน", "ใส่ในโพสต์ เจอกันที่บูธ และในการ์ด"),
    ("เวลาเข้าจัดและรื้อบูธ", "ทั้งวันแรกและวันสุดท้าย และจุดขนของ ลานจอดรถ"),
    ("บัตรผู้ออกบูธ", "ได้กี่ใบ เด็กต้องมีบัตรไหม เราไปกัน 5 คน"),
    ("กฎการตกแต่ง", "ติดเทปหรือแขวนบนผนังได้ไหม ของตั้งสูงได้ไม่เกินเท่าไร ใช้ไฟของตัวเองได้ไหม"),
]

PLAN = [
    ("จ. 19 ต.ค.", "วันนี้", "ถามผู้จัด 6 ข้อด้านล่าง · สั่งของ Shopee (ตะแกรง ตะขอ กรอบป้าย ไฟหนีบ) · ส่งไฟล์โรลอัพเข้าร้านพิมพ์"),
    ("อ. 20 ต.ค.", "", "ซื้อของหน้าร้าน HomePro, IKEA, ร้าน 20 บาท (ผ้า ลังไม้ ตะกร้า กล่อง) · ถ้าของ Shopee ส่งไม่ทันวันพุธ ซื้อหน้าร้านแทน"),
    ("พ. 21 ต.ค.", "", "รับโรลอัพและงานพิมพ์ · ใส่ป้ายราคาในกรอบ · ติดป้ายห้อยสินค้า"),
    ("พฤ. 22 ต.ค.", "ซ้อมใหญ่", "ตีเทปกรอบ 2 × 2 ม. บนพื้นบ้าน จัดบูธจริงตามผัง ถ่ายรูปเก็บไว้เป็นแบบ ซ้อมขาย แล้วแพ็คกล่อง A B C D"),
    ("ศ. 23 ต.ค.", "วันแรก", "ถึงก่อนเปิดอย่างน้อย 90 นาที จัดตามลำดับ 8 ขั้น โพสต์รูปบูธพร้อมเลขบูธก่อนงานเปิด"),
    ("23–25 ต.ค.", "ทุกเย็น", "ปิดยอด นับเงิน เทียบสมุด จดว่าตัวไหนหมด เติมของจากกล่อง D ก่อนกลับ"),
    ("อา. 25 ต.ค.", "รื้อบูธ", "เก็บตามเวลาผู้จัด ถ่ายรูปบูธครั้งสุดท้าย เตรียมโพสต์ Happy 26.10 พรุ่งนี้"),
]

SETUP = [
    ("กาง โต๊ะ ชิดขอบหน้าบูธ แล้วคลุมผ้า", "วางกล่อง A B C ใต้โต๊ะตามโซนของมัน"),
    ("ตั้งตะแกรงสองชุดชิดผนังหลัง ซ้ายและขวา", "ตั้งโรลอัพตรงกลางระหว่างตะแกรง"),
    ("หนีบไฟ", "ดวงละตะแกรง และหนึ่งดวงส่องโต๊ะกาแฟจำลอง"),
    ("วางลังไม้เป็นขั้นบันได", "ฝั่งขวา (ห้าหมี) สูงสุดอยู่ด้านหลัง"),
    ("จัดโต๊ะกาแฟจำลองฝั่งซ้าย", "แผ่นรองจาน แก้วบนที่รองแก้ว ผ้าเช็ดปากใส่ห่วงหมี ต้นไม้บนที่รองแก้วไส้ไม้ก๊อก"),
    ("แขวนของบนตะแกรง", "ซ้าย SOI. 02 (กังหัน ของแขวน ปลอกแก้ว ซอง AirTag) · ขวา ราวหมีห้าตัวพาดบนสุด ที่ห้อยกระเป๋า ป้ายชื่อ"),
    ("ป้ายราคา QR และป้ายคอลเลกชัน", "QR หนึ่งอันตรงจุดจ่ายเงิน อีกอันตรงโต๊ะกาแฟ"),
    ("ถ่ายรูปบูธจากทางเดิน", "โพสต์สตอรี่ เจอกันที่บูธ พร้อมเลขบูธ"),
]


# ---------------------------------------------------------------- drawings
def plan_svg():
    """Top view, aisle at the bottom. 1 cm = 2.4 px."""
    k, ox, oy = 2.4, 56, 34
    X = lambda cm: ox + cm * k
    Y = lambda cm: oy + cm * k

    def rect(x, y, w, h, cls, rx=3):
        return f'<rect x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*k:.1f}" height="{h*k:.1f}" rx="{rx}" class="{cls}"/>'

    def text(x, y, s, cls="t", anchor="middle"):
        return f'<text x="{X(x):.1f}" y="{Y(y):.1f}" class="{cls}" text-anchor="{anchor}">{E(s)}</text>'

    def badge(x, y, s, cls="bk"):
        return (f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="14" class="{cls}"/>'
                f'<text x="{X(x):.1f}" y="{Y(y)+5:.1f}" class="tb" text-anchor="middle">{s}</text>')

    tw, td, _ = TABLE
    tx, ty = (W - tw) / 2, D - td
    out = [rect(0, 0, W, D, "floor", 0)]
    # back wall: grid | roll-up | grid
    out += [rect(0, 0, 60, 7, "grid"), rect(60, 0, 80, 14, "roll"), rect(140, 0, 60, 7, "grid")]
    out += [text(30, 20, "ตะแกรง SOI. 02", "ts"), text(100, 28, "โรลอัพ OCT. 26"), text(170, 20, "ตะแกรง ห้าหมี", "ts")]
    # spare stock and people zone
    out += [rect(166, 34, 30, 30, "box"), text(181, 53, "D", "tz")]
    out += [text(70, 66, "หลังร้าน ลึก 130 ซม.", "ts"), text(70, 76, "พ่อแม่เติมของ", "ts")]
    # table and zones
    out += [rect(tx, ty, tw, td, "table")]
    z1, z2 = tx + 60, tx + 120
    out += [f'<line x1="{X(z):.1f}" y1="{Y(ty)+6:.1f}" x2="{X(z):.1f}" y2="{Y(D)-6:.1f}" class="zl"/>' for z in (z1, z2)]
    out += [text(tx + 30, ty + 24, "A โต๊ะกาแฟ", "tz"), text(tx + 30, ty + 36, "ของแต่งโต๊ะ", "ts"),
            text(tx + 90, ty + 24, "B สาธิต", "tz"), text(tx + 90, ty + 36, "เด็กลองต่อ", "ts"),
            text(tx + 150, ty + 24, "C ห้าหมี", "tz"), text(tx + 150, ty + 36, "จ่ายเงินขวาสุด", "ts")]
    # stools and people
    out += [f'<circle cx="{X(100):.1f}" cy="{Y(122):.1f}" r="{14*k/2:.1f}" class="stool"/>',
            f'<circle cx="{X(176):.1f}" cy="{Y(122):.1f}" r="{14*k/2:.1f}" class="stool"/>']
    out += [badge(100, 122, "2", "bm"), badge(176, 122, "1", "bs"), badge(22, 128, "3", "bp"), badge(56, 100, "พ", "bk")]
    # lamps
    for lx, ly in ((30, 9), (170, 9), (tx + 4, ty + 4)):
        out.append(f'<circle cx="{X(lx):.1f}" cy="{Y(ly):.1f}" r="5" class="lamp"/>')
    # dimensions
    out += [f'<line x1="{X(0):.1f}" y1="{oy-14}" x2="{X(W):.1f}" y2="{oy-14}" class="dim"/>',
            text(100, -9, "หน้ากว้าง 200 ซม.", "td"),
            f'<line x1="{ox-18}" y1="{Y(0):.1f}" x2="{ox-18}" y2="{Y(D):.1f}" class="dim"/>',
            f'<text x="{ox-26}" y="{Y(100):.1f}" class="td" text-anchor="middle" transform="rotate(-90 {ox-26} {Y(100):.1f})">ลึก 200 ซม.</text>',
            text(tx + 90, ty - 4, f"โต๊ะ {tw} × {td} ซม.", "ts")]
    # aisle
    ay = Y(D) + 30
    out += [f'<rect x="{X(0)-40:.1f}" y="{Y(D)+8:.1f}" width="{W*k+80:.1f}" height="44" class="aisle"/>',
            f'<line x1="{X(10):.1f}" y1="{ay:.1f}" x2="{X(70):.1f}" y2="{ay:.1f}" class="arw" marker-end="url(#ah)"/>',
            f'<line x1="{X(190):.1f}" y1="{ay:.1f}" x2="{X(130):.1f}" y2="{ay:.1f}" class="arw" marker-end="url(#ah)"/>',
            f'<text x="{X(100):.1f}" y="{ay+5:.1f}" class="tz" text-anchor="middle">ทางเดินลูกค้า</text>']
    vb_w, vb_h = ox + W * k + 46, Y(D) + 60
    return (f'<svg class="draw" viewBox="0 0 {vb_w:.0f} {vb_h:.0f}" role="img" aria-label="ผังบูธ 2 × 2 เมตร มองจากด้านบน">'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10z" class="arh"/></marker></defs>' + "".join(out) + "</svg>")


def front_svg():
    """Front view from the aisle. 1 cm = 1.8 px, ground at the bottom."""
    k, ox, gy = 1.8, 52, 30 + 250 * 1.8
    X = lambda cm: ox + cm * k
    Y = lambda h: gy - h * k

    def rect(x, h0, w, h, cls, rx=2):
        return f'<rect x="{X(x):.1f}" y="{Y(h0 + h):.1f}" width="{w*k:.1f}" height="{h*k:.1f}" rx="{rx}" class="{cls}"/>'

    def text(x, h, s, cls="t"):
        return f'<text x="{X(x):.1f}" y="{Y(h):.1f}" class="{cls}" text-anchor="middle">{E(s)}</text>'

    tw, _, th = TABLE
    tx = (W - tw) / 2
    out = [rect(0, 0, W, 250, "wall", 0)]
    # grids with mesh, roll-up
    for gx, label in ((0, "SOI. 02"), (140, "ห้าหมี")):
        out.append(rect(gx + 3, 30, 54, 150, "grid"))
        out += [f'<line x1="{X(gx+3+i*9):.1f}" y1="{Y(180):.1f}" x2="{X(gx+3+i*9):.1f}" y2="{Y(30):.1f}" class="mesh"/>' for i in range(1, 6)]
        out += [f'<line x1="{X(gx+3):.1f}" y1="{Y(30+i*15):.1f}" x2="{X(gx+57):.1f}" y2="{Y(30+i*15):.1f}" class="mesh"/>' for i in range(1, 10)]
        out.append(text(gx + 30, 186, f"ตะแกรง {label}", "ts"))
    out.append(rect(60, 0, 80, 200, "roll"))
    out += [f'<text x="{X(100):.1f}" y="{Y(176):.1f}" class="logo" text-anchor="middle">OCT. 26</text>',
            f'<text x="{X(100):.1f}" y="{Y(164):.1f}" class="logo-s" text-anchor="middle">our crafted things.</text>',
            f'<text x="{X(100):.1f}" y="{Y(140):.1f}" class="logo-s" text-anchor="middle">SOI. 02 · ห้าหมี</text>']
    # bear garland on the right grid
    out.append(f'<path d="M{X(144):.1f} {Y(170):.1f} Q{X(170):.1f} {Y(158):.1f} {X(196):.1f} {Y(170):.1f}" class="garland"/>')
    out += [f'<circle cx="{X(150+i*10):.1f}" cy="{Y(166 - (2 if i in (1, 2, 3) else 0)):.1f}" r="5" class="bear"/>' for i in range(5)]
    # hanging items
    for gx in (0, 140):
        for i in range(3):
            for j in range(2):
                out.append(f'<rect x="{X(gx+12+i*16):.1f}" y="{Y(140-j*40):.1f}" width="{8*k:.1f}" height="{10*k:.1f}" rx="3" class="item"/>')
    # table, cloth, front banner, risers, coffee set
    out.append(rect(tx, 0, tw, th, "cloth", 3))
    out.append(rect(tx + 10, 22, tw - 20, 32, "banner", 2))
    out.append(f'<text x="{X(100):.1f}" y="{Y(32):.1f}" class="banner-t" text-anchor="middle">OCT. 26</text>')
    out += [rect(132, th, 30, 12, "riser"), rect(142, th + 12, 28, 12, "riser"), rect(152, th + 24, 24, 12, "riser")]
    out += [rect(18, th, 38, 2, "item"), rect(26, th + 2, 9, 11, "cup"), rect(42, th, 7, 13, "plant"),
            f'<circle cx="{X(46):.1f}" cy="{Y(th+18):.1f}" r="9" class="leaf"/>']
    out += [rect(86, th, 28, 2, "mat")]
    # dimension marks
    for h in (0, 75, 150, 200, 250):
        out.append(f'<text x="{ox-8}" y="{Y(h)+4:.1f}" class="td" text-anchor="end">{h}</text>')
    out.append(f'<text x="{ox-8}" y="{Y(250)-12:.1f}" class="td" text-anchor="end">ซม.</text>')
    out.append(f'<line x1="{X(0)-30:.1f}" y1="{gy:.1f}" x2="{X(W)+10:.1f}" y2="{gy:.1f}" class="ground"/>')
    out.append(text(100, -14, "ระดับสายตาคนเดิน 150–170 ซม.", "ts"))
    return (f'<svg class="draw" viewBox="0 0 {ox + W*k + 20:.0f} {gy + 40:.0f}" role="img" aria-label="หน้าบูธมองจากทางเดิน">'
            + "".join(out) + "</svg>")


SVG_CSS = """
.draw{width:100%;height:auto;display:block}
.draw text{font-family:var(--body);fill:var(--ink)}
.draw .t{font-size:17px}.draw .ts{font-size:14px;fill:var(--muted)}.draw .tz{font-size:16px;font-weight:600}
.draw .td{font-size:14px;fill:var(--muted)}.draw .tb{font-size:14px;font-weight:600;fill:#1C1B22}
.chip{white-space:nowrap}
.draw .floor{fill:var(--paper);stroke:var(--ink);stroke-width:1.5;stroke-dasharray:6 4}
.draw .grid{fill:none;stroke:var(--ink);stroke-width:2}
.draw .roll{fill:var(--cobalt);stroke:none}
.draw .box{fill:var(--chip);stroke:var(--muted);stroke-dasharray:3 3}
.draw .table{fill:var(--chip);stroke:var(--ink);stroke-width:1.5}
.draw .zl{stroke:var(--muted);stroke-dasharray:3 3}
.draw .stool{fill:none;stroke:var(--muted);stroke-width:1.2}
.draw .bk{fill:var(--line)}.draw .bs{fill:#FFC23C}.draw .bm{fill:#2EC4A0}.draw .bp{fill:#FF8AC4}
.draw .lamp{fill:#FFC23C;stroke:var(--ink);stroke-width:1}
.draw .dim{stroke:var(--muted);stroke-width:1}
.draw .aisle{fill:var(--line);opacity:.6}
.draw .arw{stroke:var(--tomato);stroke-width:2.5}.draw .arh{fill:var(--tomato)}
.draw .wall{fill:var(--paper);stroke:var(--line)}
.draw .mesh{stroke:var(--muted);stroke-width:.6;opacity:.6}
.draw .logo{font-family:"Jost","Anuphan",sans-serif;font-weight:500;font-size:22px;fill:#FFFFFF}
.draw .logo-s{font-size:10px;fill:#FFFFFF}
.draw .garland{fill:none;stroke:#B8743A;stroke-width:1.5}.draw .bear{fill:#B8743A}
.draw .item{fill:#B8743A;opacity:.85}
.draw .cloth{fill:#FFF6EC;stroke:var(--ink);stroke-width:1.2}
.draw .banner{fill:#2449D8}.draw .banner-t{font-family:"Jost","Anuphan",sans-serif;font-weight:500;font-size:16px;fill:#FFFFFF}
.draw .riser{fill:#D9B48C;stroke:#8A5A2B;stroke-width:1}
.draw .cup{fill:#FFFFFF;stroke:var(--ink)}.draw .plant{fill:#B8743A}.draw .leaf{fill:#2EC4A0}
.draw .mat{fill:var(--ink)}
.draw .ground{stroke:var(--ink);stroke-width:2}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:var(--t-1);color:var(--muted)}
.legend i{display:inline-block;width:14px;height:14px;border-radius:50%;vertical-align:-2px;margin-right:6px}
.kpi b{font-family:var(--display);font-size:24px;display:block;line-height:1.3}
.two{display:grid;gap:var(--s4);grid-template-columns:repeat(auto-fit,minmax(min(100%,377px),1fr))}
.two>*{min-width:0}
"""


# ---------------------------------------------------------------- page
def page():
    tot = B.event_totals()
    must = [g for g in GEAR if g[5] == "buy"]
    lo_buy, hi_buy = sum(g[3] for g in must), sum(g[4] for g in must)
    lo_all, hi_all = sum(g[3] for g in GEAR), sum(g[4] for g in GEAR)
    per_day_units, per_day_sales = tot["units"] / 3, tot["sales"] / 3

    gear_rows = "".join(
        f'<tr><td><b style="font-weight:600">{E(n)}</b> <span class="cap">× {E(q)}</span><div class="cap">ซื้อที่ {E(where)}</div>'
        f'{f"<div class=cap>{E(note)}</div>" if note else ""}</td>'
        f'<td class="n">{"–" if hi == 0 else (f"{lo:,}–{hi:,}" if lo else f"0–{hi:,}")}</td>'
        f'<td><span class="chip {KIND[kind][1]}">{KIND[kind][0]}</span></td></tr>'
        for n, q, where, lo, hi, kind, note in GEAR)

    hero_rows = "".join(
        f'<tr><td>{E(P[n]["name"])}{PRE_CHIP if n in PREORDER else ""}'
        f'<div class="cap mono">#{n:02d} · {"ห้าหมี Love" if P[n]["coll"] == "love" else "SOI. 02"}</div></td>'
        f'<td class="n">{P[n]["price"]}</td><td class="n">{P[n]["stock"]}</td></tr>'
        for n in FAIR_HEROES)

    plan_rows = "".join(f'<tr><td style="white-space:nowrap"><b>{E(d)}</b><div class="cap">{E(tag)}</div></td><td>{E(t)}</td></tr>'
                        for d, tag, t in PLAN)
    ask = "".join(f'<li><b>{E(a)}</b> · {E(b)}</li>' for a, b in ASK)
    setup = "".join(f'<li><b>{E(a)}</b><div class="cap" style="font-size:14px">{E(b)}</div></li>' for a, b in SETUP)
    roles = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:6px"><p><span class="legend"><span><i style="background:{c}"></i>{num}</span></span></p>'
        f'<h3>{E(t)}</h3><p class="cap" style="font-size:14px">{E(w)}</p></div>'
        for num, c, t, w in [
            ("1", "#FFC23C", f"{B.KIDS_ROLES[0][0]} · {B.KIDS_ROLES[0][1]}", "นั่งสุดขวาของโต๊ะ ข้างป้าย QR ดูกล่องเงิน จดยอด ส่งถุง"),
            ("2", "#2EC4A0", f"{B.KIDS_ROLES[1][0]} · {B.KIDS_ROLES[1][1]}", "นั่งกลางโต๊ะ โซน B ต่อหนังให้ลูกค้าดู ยื่นให้ลองดึง"),
            ("3", "#FF8AC4", f"{B.KIDS_ROLES[2][0]} · {B.KIDS_ROLES[2][1]}", "ยืนด้านในฝั่งซ้าย ข้างโต๊ะกาแฟจำลอง ยิ้ม ยื่นการ์ด ชวนลองวางแก้ว"),
            ("พ", "var(--line)", "พ่อหรือแม่", "อยู่หลังร้านตลอด เติมของจากกล่อง D ตอบเรื่องสั่งทำ อีกคนพาลูกที่ไม่เข้ากะไปพัก")])

    return f"""{S.head("บูธ OCT. 26 บ้านและสวน")}<style>{SVG_CSS}</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">แผนบูธ · ฝ่ายการตลาดและการขาย · 19 ต.ค. 2569</span>
<h1>บูธ OCT. 26 ที่{FAIR}</h1>
<p class="lead">{DATES} · บูธ 2 × 2 เมตร โต๊ะตัวเดียว ของหาซื้อได้ที่ HomePro, IKEA, ร้าน 20 บาท และ Shopee
คนมางานนี้มาหาของแต่งบ้าน หน้าบูธจึงจัดเป็นโต๊ะกาแฟจำลองที่ใช้ของ SOI. 02 จริง ส่วนห้าหมีอยู่ฝั่งขวาสำหรับของขวัญและเด็ก</p>
<div class="grid s">
<div class="card kpi"><p class="cap">พื้นที่</p><b class="mono">4 ตร.ม.</b></div>
<div class="card kpi"><p class="cap">ของไปงาน</p><b class="mono">{tot['units']} ชิ้น</b></div>
<div class="card kpi"><p class="cap">ขายหมด ต่อวัน</p><b class="mono">{per_day_sales:,.0f} ฿</b></div>
<div class="card kpi"><p class="cap">งบอุปกรณ์ที่ต้องซื้อ</p><b class="mono">{lo_buy/1000:.1f}–{hi_buy/1000:.1f}k ฿</b></div>
<div class="card kpi"><p class="cap">อยู่ในบูธพร้อมกัน</p><b class="mono">3–4 คน</b></div></div></header>

<section id="plan"><span class="eyebrow">มองจากด้านบน</span><h2>ผังบูธ</h2>
<div class="two"><div class="card">{plan_svg()}</div>
<div style="display:flex;flex-direction:column;gap:var(--s3)">
<p>ลูกค้าเดินมาจากทั้งสองทาง เห็นโรลอัพกับราวหมีก่อน แล้วหยุดที่โต๊ะ ซ้ายไปขวาเรียงเป็น <b>ดู · ลองต่อ · จ่ายเงิน</b></p>
<ul><li><b>A โต๊ะกาแฟจำลอง</b> 60 ซม. ลูกค้าวางแก้วบนที่รองแก้วได้จริง ที่รองแก้วลายอื่นแยกใส่ตะกร้าให้หยิบเลือก</li>
<li><b>B จุดสาธิต</b> 60 ซม. ลูกต่อหนังให้ดู ขอบหน้าโต๊ะวางกล่องทดลองให้เด็กลองต่อ</li>
<li><b>C ห้าหมี Love</b> 60 ซม. ลังไม้สามขั้น และจุดจ่ายเงินสุดขวา</li>
<li>ใต้โต๊ะซ่อนกล่อง A B C ของแต่ละโซน กล่อง D เป็นของสำรองอยู่มุมหลังขวา</li></ul>
<p class="legend"><span><i style="background:#FFC23C"></i>1 หัวหน้าร้าน</span><span><i style="background:#2EC4A0"></i>2 นักสาธิต</span>
<span><i style="background:#FF8AC4"></i>3 ผู้ต้อนรับ</span><span><i style="background:var(--line)"></i>พ พ่อหรือแม่</span></p></div></div></section>

<section id="front"><span class="eyebrow">มองจากทางเดิน</span><h2>หน้าบูธ</h2>
<div class="two"><div class="card">{front_svg()}</div>
<div style="display:flex;flex-direction:column;gap:var(--s3)">
<p>บูธมีสามระดับให้คนเห็นจากระยะต่างกัน</p>
<ul><li><b>150–200 ซม.</b> โลโก้ OCT. 26 บนโรลอัพ และราวหมีห้าตัวบนตะแกรงขวา มองเห็นจากไกล</li>
<li><b>75–110 ซม.</b> สินค้าบนโต๊ะและลังไม้ ระดับมือหยิบ</li>
<li><b>20–55 ซม.</b> ป้ายไวนิลหน้าโต๊ะ (มีก็ดี) คนที่เดินชิดบูธยังเห็นชื่อร้าน</li></ul>
<p class="cap">ถ้าผู้จัดให้ผนังมาแล้ว ตะแกรงตั้งชิดผนังได้เลย ไม่ต้องเจาะหรือติดเทปผนัง</p></div></div></section>

<section id="sell"><span class="eyebrow">ขายอะไรหน้าบูธ</span><h2>คนงานบ้านและสวนมาหาของแต่งบ้าน</h2>
<p class="lead">งานนี้ให้ของแต่งโต๊ะเป็นตัวหลัก ส่วนห้าหมีเป็นของขวัญ ประโยคแรกที่ใช้ทัก: “ลองวางแก้วดูได้เลยค่ะ/ครับ หนังแท้จากเศษหนัง ทำกันเองทั้งบ้าน”</p>
<div class="tbl"><table><thead><tr><th>สินค้า</th><th>ราคา ฿</th><th>เตรียมไป</th></tr></thead><tbody>{hero_rows}</tbody></table></div>
<p class="cap">แผ่นรองจาน ปลอกแก้ว และที่รองแก้วไส้ไม้ก๊อกมีของน้อย ให้วางโชว์แล้วรับสั่งทำเป็นชุด 4 หรือ 6 ชิ้น จดชื่อกับเบอร์หรือไอจีลงสมุดรับออเดอร์ และส่งราคาให้หลังงาน
ลูกค้าขอลดราคา ใช้บทเดิม: ซื้อสามชิ้นได้สติกเกอร์หมีฟรี ราคาเท่าเดิม</p></section>

<section id="gear"><span class="eyebrow">อุปกรณ์</span><h2>ของที่ต้องเตรียม</h2>
<p>ต้องซื้อจริงประมาณ <b class="mono">{lo_buy:,}–{hi_buy:,} บาท</b> ถ้าไม่มีอะไรที่บ้านเลยและซื้อครบทุกอย่าง <span class="mono">{lo_all:,}–{hi_all:,} บาท</span>
ราคาเป็นราคาประมาณ ยังไม่ได้เช็กกับร้าน ค่างานพิมพ์ป้ายราคา การ์ด สติกเกอร์ อยู่ในรายการพิมพ์ของ Launch Kit แยกต่างหาก</p>
<div class="tbl"><table><thead><tr><th>ของ</th><th>บาท</th><th></th></tr></thead><tbody>{gear_rows}</tbody></table></div></section>

<section id="ask"><span class="eyebrow">วันนี้</span><h2>ถามผู้จัดงาน 6 ข้อ</h2>
<div class="card"><ul>{ask}</ul></div></section>

<section id="days"><span class="eyebrow">19–25 ต.ค.</span><h2>ทำอะไรวันไหน</h2>
<div class="tbl"><table><tbody>{plan_rows}</tbody></table></div></section>

<section id="setup"><span class="eyebrow">เช้าวันแรก</span><h2>ลำดับจัดบูธ 8 ขั้น</h2>
<div class="card"><ol>{setup}</ol></div>
<p class="cap">ทั้งหมดใช้เวลาประมาณ 60–90 นาที ถ้าซ้อมที่บ้านวันพฤหัสแล้ว</p></section>

<section id="who"><span class="eyebrow">คนในบูธ</span><h2>ใครอยู่ตรงไหน</h2>
<p>หลังโต๊ะกว้าง 130 ซม. อยู่ได้พร้อมกัน 3–4 คน เด็กทำกะละ 45 นาที พัก 15 นาที พ่อหรือแม่อยู่ที่บูธตลอด อีกคนพาลูกที่ไม่เข้ากะไปพักหรือเดินดูงาน</p>
<div class="grid">{roles}</div></section>

<section id="target"><span class="eyebrow">เป้า</span><h2>ตัวเลขที่ต้องจดทุกเย็น</h2>
<div class="grid s">
<div class="card kpi"><p class="cap">ขายหมดทั้งงาน</p><b class="mono">{tot['sales']:,.0f} ฿</b></div>
<div class="card kpi"><p class="cap">เฉลี่ยต่อวัน</p><b class="mono">{per_day_units:.0f} ชิ้น</b></div>
<div class="card kpi"><p class="cap">ยอดต่อวัน</p><b class="mono">{per_day_sales:,.0f} ฿</b></div>
<div class="card kpi"><p class="cap">ต้นทุนของ+แพ็ค</p><b class="mono">{tot['cost']:,.0f} ฿</b></div></div>
<p class="cap">ทุกเย็นจดสามอย่าง: ยอดเงิน จำนวนชิ้นต่อสินค้า และจำนวนออเดอร์สั่งทำ วันที่สองย้ายตัวที่ขายดีไปไว้หน้าสุด</p></section>

<section id="files"><span class="eyebrow">ไฟล์</span><h2>ไฟล์ที่ส่ง</h2>
<div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">booth-20261019/build.py</td><td>ข้อมูลแผนบูธ: ผัง อุปกรณ์ ราคา ไทม์ไลน์ แก้ที่นี่แล้วรันใหม่</td></tr>
<tr><td class="mono" style="white-space:nowrap">booth-20261019/site/index.html</td><td>หน้านี้ (สร้างจาก build.py)</td></tr>
<tr><td class="mono" style="white-space:nowrap">brand-20261014/brand.py</td><td>ชื่องานในโพสต์เปลี่ยนเป็น {FAIR} แล้ว ราคาและสต็อกสินค้าอ่านจากไฟล์นี้</td></tr>
</tbody></table></div></section>

<section id="check"><span class="eyebrow">ต้องเช็ก</span><h2>ก่อนซื้อของ</h2>
<div class="card"><ol>
<li>คำตอบจากผู้จัด โดยเฉพาะ โต๊ะ เก้าอี้ ผนัง และปลั๊กไฟ ถ้าผู้จัดให้ครบ งบลดลงได้อีกราว 1,000–2,000 บาท</li>
<li>เลขบูธ เอามาใส่โพสต์ เจอกันที่บูธ</li>
<li>ไฟล์โรลอัพ 80 × 200 ซม. ส่งร้านพิมพ์ภายในวันอังคาร ให้ได้รับทันวันพุธ</li>
<li>ของจาก Shopee ถ้าร้านส่งไม่ทันวันพุธ ซื้อหน้าร้านแทน</li></ol></div></section>
</div>"""


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(page())
    print("wrote site/index.html")
