"""Booth plan for งานบ้านและสวน, 23–25 Oct 2569: one 2 x 2 m booth, gear that is easy to buy.

The organiser gives each booth a pallet coffee table (117 x 80 cm, 50 cm high) and two folding chairs
(site/organizer-table.jpg, their drawing, received 20 Oct). Reads products and prices from
../brand-20261014/brand.py and the page style from its site/build.py, writes site/index.html.
Run: python3 booth-20261019/build.py
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
W = D = 200            # booth, cm
TABLE = (117, 80, 50)  # organiser's pallet table w, d, h (cm), steel frame, slatted top
TX, TY = 3, D - 80 - 3 # table pushed into the front-left corner; the front-right corner is the way in
CHAIRS = 2             # organiser's folding chairs per booth (their drawing: 30 chairs for 15 tables)

# ---------------------------------------------------------------- what sells at a home fair
# People walk in to furnish a home, and the organiser's table is coffee-table height, so the front
# of it is a real coffee table: coasters, napkin ring and coffee sleeve in use. FIVE BEARS hangs on
# the right grid, next to the open corner, for gifts and kids.
FAIR_HEROES = [29, 22, 15, 4, 14, 13, 21, 23, 30]
PREORDER = [13, 14, 15]   # few in stock, take orders for sets
PRE_CHIP = ' <span class="chip mid">รับสั่งเป็นชุด</span>'

# ---------------------------------------------------------------- gear
# name, qty, where to buy, THB low, THB high, kind, note
# kind: org = organiser gives it, buy = must buy, home = take from home if you have it, opt = nice to have
GEAR = [
    ("โต๊ะพาเลท 117 × 80 ซม. สูง 50 และเก้าอี้พับ", f"1 โต๊ะ {CHAIRS} เก้าอี้", "ผู้จัดให้", 0, 0, "org",
     "ผู้จัดยืนยันแล้ว บูธละหนึ่งชุด"),
    ("แผ่นไม้อัด 4 มม. ตัดเป็นสองแผ่น 58 × 80 ซม.", "2 แผ่น", "HomePro หรือไทวัสดุ ซื้อแผ่น 120 × 240 แล้วให้ร้านตัด", 300, 500, "buy",
     "ร่องไม้พาเลทกว้าง ต้องมีแผ่นรองก่อนปูผ้า ตัดสองแผ่นจะใส่รถง่าย และรอยต่อตรงกับเส้นแบ่งโซน · ถ้าหาไม่ทัน ใช้ฟิวเจอร์บอร์ด 5 มม. แทน"),
    ("ผ้าลินินหรือผ้าดิบ สีครีม", "2 ม.", "ร้านผ้า, Shopee", 150, 300, "buy",
     "ปูทับแผ่นไม้อัด พับขอบให้ยังเห็นไม้พาเลท เศษที่เหลือคลุมกล่องสต็อก"),
    ("ตะแกรงลวดแขวนของ 60 × 150 ซม. พร้อมขาตั้ง", "2 ชุด", "Shopee, HomePro", 700, 1200, "buy",
     "ตั้งชิดผนังหลังซ้ายและขวา ไม่ต้องเจาะผนัง เป็นที่โชว์หลักระดับสายตา เพราะโต๊ะเตี้ย"),
    ("ตะขอแขวนตะแกรงและตะขอตัว S", "40 อัน", "Shopee, ร้าน 20 บาท", 100, 200, "buy", "แขวนราวหมี ที่ห้อยกระเป๋า ป้ายชื่อ"),
    ("ป้ายโรลอัพ 80 × 200 ซม. พร้อมขาตั้ง", "1 ชุด", "ร้านพิมพ์ใกล้บ้าน ส่วนใหญ่เสร็จใน 1 วัน", 600, 1000, "buy",
     "โลโก้ OCT. 26 อยู่ช่วงบน 150–200 ซม. มองเห็นจากทางเดินข้ามหัวคน"),
    ("ลังไม้เล็ก", "3 ใบ", "IKEA, Shopee, ร้านต้นไม้ · หรือกล่องรองเท้าห่อผ้า", 300, 750, "buy",
     "โต๊ะสูงแค่ 50 ซม. ซ้อนลังยกของขึ้นมาระดับมือผู้ใหญ่ 75–100 ซม."),
    ("ตะกร้าหวายหรือถาดไม้ใบเล็ก", "6 ใบ", "ร้าน 20 บาท, Daiso, จตุจักร", 300, 500, "buy",
     "แยกที่รองแก้วตามลาย ลูกค้าหยิบเลือกเองได้"),
    ("ป้ายตั้งพื้นแบบขาตั้ง A (กระดานดำหรือไวท์บอร์ด)", "1 อัน", "IKEA, Shopee, ร้านเครื่องเขียน", 300, 600, "buy",
     "ตั้งมุมหน้าขวา เขียนว่า เข้ามาลองต่อหนังได้ เปลี่ยนข้อความได้ทุกวัน"),
    ("กรอบป้ายอะคริลิกตั้งโต๊ะ A5", "4 อัน", "ร้านเครื่องเขียน, Shopee", 160, 280, "buy",
     "QR พร้อมเพย์ 2 · ป้าย SOI. 02 1 · ป้ายห้าหมี Love 1"),
    ("กรอบป้ายอะคริลิกเล็ก A7", "8 อัน", "ร้านเครื่องเขียน, Shopee", 160, 240, "buy", "ป้ายราคาตามหมวด 8 ใบในรายการพิมพ์"),
    ("โคมไฟหนีบ LED แสงวอร์ม", "3 ดวง", "HomePro, Shopee", 600, 1050, "buy",
     "หนังดูสวยใต้แสงอุ่น ดวงละไม่เกิน 10 วัตต์ ปลั๊กบูธ 5A รับได้สบาย"),
    ("ปลั๊กพ่วง มอก. ยาว 5 ม.", "1 อัน", "HomePro", 300, 500, "home", ""),
    ("กล่องพลาสติกมีฝา ซ้อนได้", "4 ใบ", "HomePro, Makro", 400, 600, "home",
     "A B C ใต้โต๊ะพาเลท D มุมหลังซ้าย คลุมผ้า"),
    ("แผ่นรองตัด A3 หรือผ้าสักหลาด", "1 แผ่น", "ร้านเครื่องเขียน", 100, 200, "buy", "พื้นจุดสาธิต"),
    ("แก้วกาแฟ ผ้าเช็ดปาก จานรอง", "1 ชุด", "จากบ้าน", 0, 0, "home", "ใช้จัดโต๊ะกาแฟ"),
    ("ต้นไม้กระถางเล็ก", "2 กระถาง", "ซื้อในงานได้เลย", 100, 200, "buy",
     "วางบนที่รองแก้วไส้ไม้ก๊อก เข้าธีมบ้านและสวน และขายที่รองแก้วไปในตัว"),
    ("ของจิปาถะ: เคเบิลไทร์ เทปสองหน้า เทปใส กรรไกร คัตเตอร์ ปากกาเมจิก ถุงขยะ ทิชชู่", "1 ถุง", "ร้าน 20 บาท, 7-Eleven",
     150, 250, "buy", ""),
    ("กล่องเงินและเงินทอน 1,500 บาท", "1 กล่อง", "จากบ้าน", 0, 0, "home", "ใบละ 20 และ 100 กับเหรียญ 10 และ 5"),
    ("ป้ายไวนิล 110 × 30 ซม.", "1 ผืน", "ร้านพิมพ์", 100, 200, "opt", "ผูกกับขาเหล็กหน้าโต๊ะด้วยเคเบิลไทร์ คนเดินชิดบูธเห็นชื่อร้าน"),
    ("กระจกตั้งโต๊ะเล็ก", "1 บาน", "ร้าน 20 บาท", 60, 120, "opt", "ลูกค้าลองห้อยที่ห้อยกระเป๋าแล้วส่องดู"),
    ("รถเข็นพับได้", "1 คัน", "ยืมหรือ HomePro", 600, 900, "opt", "ขนกล่องจากลานจอดถึงฮอลล์ทีเดียวจบ"),
]
KIND = {"org": ("ผู้จัดให้", "ok"), "buy": ("ต้องซื้อ", "ext"), "home": ("มีที่บ้านใช้ได้", "ok"), "opt": ("มีก็ดี", "mid")}
SAVED = (900, 1900)   # folding table, long tablecloth and two stools from the first plan, no longer bought

ASK = [
    ("ขยับโต๊ะได้ไหม", "ย้ายโต๊ะพาเลทไปมุมหน้าซ้ายของบูธเองได้ไหม"),
    ("บูธได้อะไรอีก", "ผนังกี่ด้าน สูงเท่าไร ป้ายชื่อหน้าบูธ ไฟสปอตไลต์"),
    ("ป้ายชื่อหน้าบูธ", "ส่งชื่อให้สะกด OCT. 26 ตัวใหญ่ มีจุด และเว้นวรรคก่อน 26"),
    ("เลขบูธ ฮอลล์ โซน", "ใส่ในโพสต์ เจอกันที่บูธ และในการ์ด"),
    ("เวลาเข้าจัดและรื้อบูธ", "ทั้งวันแรกและวันสุดท้าย และจุดขนของ ลานจอดรถ"),
    ("บัตรผู้ออกบูธ", "ได้กี่ใบ เด็กต้องมีบัตรไหม เราไปกัน 5 คน"),
    ("กฎการตกแต่ง", "ติดเทปหรือแขวนบนผนังได้ไหม ของตั้งสูงได้ไม่เกินเท่าไร ใช้ไฟของตัวเองได้ไหม"),
]

ANSWERED = [   # organiser's answers, 20 Oct
    ("โต๊ะและเก้าอี้", f"ได้บูธละ 1 ชุด: โต๊ะพาเลท 1 ตัว เก้าอี้ {CHAIRS} ตัว"),
    ("หน้าโต๊ะ", "ร่องไม้กว้าง ต้องมีแผ่นรองก่อน จึงเพิ่มแผ่นไม้อัดในรายการซื้อ"),
    ("ไฟ", "มีปลั๊ก 5A (ราว 1,100 วัตต์) ไฟหนีบ LED สามดวงกับชาร์จมือถือใช้ไม่ถึง 50 วัตต์ ห้ามเสียบกาต้มน้ำหรือไดร์เป่าผม"),
]

PLAN = [
    ("อ. 20 ต.ค.", "วันนี้", f"ถามผู้จัด {len(ASK)} ข้อด้านล่าง · สั่งของ Shopee แบบส่งด่วน (ตะแกรง ตะขอ กรอบป้าย ไฟหนีบ) · "
                         "ส่งไฟล์โรลอัพเข้าร้านพิมพ์ · ซื้อไม้อัดให้ร้านตัด ผ้า ลังไม้ ตะกร้า ป้ายตั้งพื้น ที่ HomePro, IKEA, ร้าน 20 บาท"),
    ("พ. 21 ต.ค.", "", "รับโรลอัพและงานพิมพ์ · ใส่ป้ายราคาในกรอบ · ติดป้ายห้อยสินค้า · ของ Shopee ไม่มาภายในวันนี้ ซื้อหน้าร้านแทน"),
    ("พฤ. 22 ต.ค.", "ซ้อมใหญ่", "ตีเทปกรอบ 2 × 2 ม. บนพื้นบ้าน ใช้โต๊ะกาแฟที่บ้านแทนโต๊ะพาเลท จัดตามผัง ถ่ายรูปเก็บไว้เป็นแบบ ซ้อมขาย แล้วแพ็คกล่อง A B C D"),
    ("ศ. 23 ต.ค.", "วันแรก", "ถึงก่อนเปิดอย่างน้อย 90 นาที จัดตามลำดับด้านล่าง โพสต์รูปบูธพร้อมเลขบูธก่อนงานเปิด"),
    ("23–25 ต.ค.", "ทุกเย็น", "ปิดยอด นับเงิน เทียบสมุด จดว่าตัวไหนหมด เติมของจากกล่อง D ก่อนกลับ"),
    ("อา. 25 ต.ค.", "รื้อบูธ", "เก็บตามเวลาผู้จัด คืนโต๊ะเก้าอี้ตามที่ผู้จัดบอก ถ่ายรูปบูธครั้งสุดท้าย เตรียมโพสต์ Happy 26.10 พรุ่งนี้"),
]

SETUP = [
    ("ขยับโต๊ะพาเลทไปมุมหน้าซ้าย วางไม้อัดสองแผ่น แล้วปูผ้า", "เว้นมุมหน้าขวาไว้เป็นทางเข้า · ใส่กล่อง A B C ใต้โต๊ะ"),
    ("ตั้งตะแกรงสองชุดชิดผนังหลัง ซ้ายและขวา", "ตั้งโรลอัพตรงกลางระหว่างตะแกรง"),
    ("วางเก้าอี้สองตัวหลังโต๊ะ", "ตัวซ้ายนักสาธิต ตัวขวาหัวหน้าร้าน"),
    ("ซ้อนลังไม้ที่ขอบหลังของโต๊ะ", "โซน C สูงขึ้นมาราว 75 ซม. วางห้าหมีชิ้นเล็ก และ QR"),
    ("จัดโต๊ะกาแฟที่ขอบหน้าโซน A", "แผ่นรองจาน แก้วบนที่รองแก้ว ผ้าเช็ดปากใส่ห่วงหมี ต้นไม้บนที่รองแก้วไส้ไม้ก๊อก ตะกร้าที่รองแก้วลายอื่นวางข้าง ๆ"),
    ("แขวนของบนตะแกรง", "ซ้าย SOI. 02 (กังหัน ของแขวน ปลอกแก้ว ซอง AirTag) · ขวา ราวหมีห้าตัวพาดบนสุด ที่ห้อยกระเป๋า ป้ายชื่อ"),
    ("หนีบไฟ", "ดวงละตะแกรง และหนึ่งดวงที่ลังไม้ส่องโต๊ะกาแฟ"),
    ("ป้ายราคา QR ป้ายคอลเลกชัน และป้ายตั้งพื้น", "QR ตรงจุดจ่ายเงินและโต๊ะกาแฟ · ป้ายตั้งพื้นมุมหน้าขวา: เข้ามาลองต่อหนังได้"),
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
    zw = tw / 3
    out = [rect(0, 0, W, D, "floor", 0)]
    # the open front-right corner customers step into
    out += [rect(TX + tw + 4, 118, W - TX - tw - 6, 80, "open", 6),
            text(TX + tw + (W - TX - tw) / 2 + 2, 140, "ทางเข้า", "tz"),
            text(TX + tw + (W - TX - tw) / 2 + 2, 152, "ลูกค้าเดินเข้ามา", "ts"),
            text(TX + tw + (W - TX - tw) / 2 + 2, 162, "ดูราวหมีได้", "ts")]
    # back wall: grid | roll-up | grid
    out += [rect(0, 0, 60, 7, "grid"), rect(60, 0, 80, 14, "roll"), rect(140, 0, 60, 7, "grid")]
    out += [text(30, 20, "ตะแกรง SOI. 02", "ts"), text(100, 28, "โรลอัพ OCT. 26"), text(170, 20, "ตะแกรง ห้าหมี", "ts")]
    # spare stock behind the table, left
    out += [rect(3, 66, 28, 34, "box"), text(17, 87, "D", "tz")]
    # chairs behind zones B and C
    for cx in (TX + zw * 1.5, TX + zw * 2.5 + 14):
        out.append(rect(cx - 25, 58, 50, 50, "chair", 8))
    # pallet table with slats, zones, crates on the back edge of C
    out.append(rect(TX, TY, tw, td, "pallet", 2))
    out += [f'<line x1="{X(TX+3):.1f}" y1="{Y(TY+td*i/5):.1f}" x2="{X(TX+tw-3):.1f}" y2="{Y(TY+td*i/5):.1f}" class="slat"/>' for i in range(1, 5)]
    out += [f'<line x1="{X(TX+zw*i):.1f}" y1="{Y(TY)+6:.1f}" x2="{X(TX+zw*i):.1f}" y2="{Y(TY+td)-6:.1f}" class="zl"/>' for i in (1, 2)]
    out.append(rect(TX + zw * 2 + 3, TY + 3, zw - 6, 20, "riser", 2))
    out += [text(TX + zw * .5, TY + 40, "A โต๊ะกาแฟ", "tz"), text(TX + zw * .5, TY + 52, "ของแต่งโต๊ะ", "ts"),
            text(TX + zw * 1.5, TY + 40, "B สาธิต", "tz"), text(TX + zw * 1.5, TY + 52, "เด็กลองต่อ", "ts"),
            text(TX + zw * 2.5, TY + 40, "C จ่ายเงิน", "tz"), text(TX + zw * 2.5, TY + 52, "ลังไม้ ห้าหมี", "ts"),
            text(TX + tw / 2, TY + 70, f"โต๊ะพาเลท {tw} × {td} ซม. สูง {TABLE[2]}", "ts")]
    # people
    out += [badge(TX + zw * 1.5, 83, "2", "bm"), badge(TX + zw * 2.5 + 14, 83, "1", "bs"),
            badge(176, 182, "3", "bp"), badge(50, 40, "พ", "bk")]
    # a-frame sign at the open corner
    out += [rect(184, 186, 14, 8, "sign", 1)]
    # lamps
    for lx, ly in ((30, 9), (170, 9), (TX + zw * 2 + 6, TY + 6)):
        out.append(f'<circle cx="{X(lx):.1f}" cy="{Y(ly):.1f}" r="5" class="lamp"/>')
    # dimensions
    out += [f'<line x1="{X(0):.1f}" y1="{oy-14}" x2="{X(W):.1f}" y2="{oy-14}" class="dim"/>',
            text(100, -9, "หน้ากว้าง 200 ซม.", "td"),
            f'<line x1="{ox-18}" y1="{Y(0):.1f}" x2="{ox-18}" y2="{Y(D):.1f}" class="dim"/>',
            f'<text x="{ox-26}" y="{Y(100):.1f}" class="td" text-anchor="middle" transform="rotate(-90 {ox-26} {Y(100):.1f})">ลึก 200 ซม.</text>']
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
    zw = tw / 3
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
    # bear garland and hanging items
    out.append(f'<path d="M{X(144):.1f} {Y(170):.1f} Q{X(170):.1f} {Y(158):.1f} {X(196):.1f} {Y(170):.1f}" class="garland"/>')
    out += [f'<circle cx="{X(150+i*10):.1f}" cy="{Y(166 - (2 if i in (1, 2, 3) else 0)):.1f}" r="5" class="bear"/>' for i in range(5)]
    for gx in (0, 140):
        for i in range(3):
            for j in range(3):
                out.append(f'<rect x="{X(gx+12+i*16):.1f}" y="{Y(140-j*35):.1f}" width="{8*k:.1f}" height="{10*k:.1f}" rx="3" class="item"/>')
    # chair backs behind the table
    for cx in (TX + zw * 1.5, TX + zw * 2.5 + 14):
        out.append(rect(cx - 24, 40, 48, 42, "chair", 4))
    # pallet table: steel frame, pallet deck, crates on C, coffee set on A, demo mat on B
    out.append(rect(TX + 2, 0, tw - 4, th - 12, "frame", 0))
    out.append(rect(TX, th - 12, tw, 12, "pallet", 1))
    out += [f'<line x1="{X(TX+tw*i/4):.1f}" y1="{Y(th-1):.1f}" x2="{X(TX+tw*i/4):.1f}" y2="{Y(th-11):.1f}" class="slat"/>' for i in range(1, 4)]
    cx0 = TX + zw * 2 + 4
    out += [rect(cx0, th, zw - 8, 14, "riser"), rect(cx0 + 4, th + 14, zw - 16, 14, "riser")]
    out += [rect(cx0 + 6, th + 28, 6, 8, "item"), rect(cx0 + 16, th + 28, 6, 8, "item"), rect(cx0 + 26, th + 28, 4, 10, "qr")]
    out += [rect(TX + 4, th, 32, 1.5, "item"), rect(TX + 10, th + 1.5, 9, 11, "cup"), rect(TX + 26, th, 7, 13, "plant"),
            f'<circle cx="{X(TX+29.5):.1f}" cy="{Y(th+18):.1f}" r="9" class="leaf"/>']
    out += [rect(TX + zw + 6, th, zw - 12, 1.5, "mat")]
    # a-frame sign in the open corner
    out += [f'<path d="M{X(176):.1f} {Y(0):.1f} L{X(183):.1f} {Y(62):.1f} L{X(191):.1f} {Y(62):.1f} L{X(198):.1f} {Y(0):.1f}" class="sign"/>',
            text(187, 40, "ลอง", "sign-t"), text(187, 30, "ต่อ", "sign-t")]
    # dimension marks
    for h in (0, 50, 100, 150, 200, 250):
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
.draw .open{fill:var(--chip)}
.draw .grid{fill:none;stroke:var(--ink);stroke-width:2}
.draw .roll{fill:var(--cobalt);stroke:none}
.draw .box{fill:var(--chip);stroke:var(--muted);stroke-dasharray:3 3}
.draw .pallet{fill:#D9B48C;stroke:#8A5A2B;stroke-width:1.5}
.draw .slat{stroke:#8A5A2B;stroke-width:1}
.draw .frame{fill:none;stroke:var(--ink);stroke-width:2.5}
.draw .chair{fill:#E9DFD0;stroke:#8A7A66;stroke-width:1.2}
.draw .zl{stroke:#6B4420;stroke-dasharray:3 3}
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
.draw .item{fill:#B8743A;opacity:.85}.draw .qr{fill:var(--ink)}
.draw .riser{fill:#C99A68;stroke:#8A5A2B;stroke-width:1}
.draw .cup{fill:#FFFFFF;stroke:var(--ink)}.draw .plant{fill:#B8743A}.draw .leaf{fill:#2EC4A0}
.draw .mat{fill:var(--ink)}
.draw .sign{fill:#1C1B22;stroke:#1C1B22}.draw .sign-t{font-size:12px;fill:#FFFFFF}
.draw .ground{stroke:var(--ink);stroke-width:2}
.legend{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:var(--t-1);color:var(--muted)}
.legend i{display:inline-block;width:14px;height:14px;border-radius:50%;vertical-align:-2px;margin-right:6px}
.kpi b{font-family:var(--display);font-size:24px;display:block;line-height:1.3}
.two{display:grid;gap:var(--s4);grid-template-columns:repeat(auto-fit,minmax(min(100%,377px),1fr))}
.two>*{min-width:0}
.photo{background:#FFFFFF;border-radius:var(--s3);padding:var(--s2)}
"""


# ---------------------------------------------------------------- page
def page():
    tot = B.event_totals()
    must = [g for g in GEAR if g[5] == "buy"]
    lo_buy, hi_buy = sum(g[3] for g in must), sum(g[4] for g in must)
    lo_all, hi_all = sum(g[3] for g in GEAR), sum(g[4] for g in GEAR)
    per_day_units, per_day_sales = tot["units"] / 3, tot["sales"] / 3
    tw, td, th = TABLE

    gear_rows = "".join(
        f'<tr><td><b style="font-weight:600">{E(n)}</b> <span class="cap">× {E(q)}</span>'
        f'<div class="cap">{"" if kind == "org" else "ซื้อที่ "}{E(where)}</div>'
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
    answered = "".join(f'<li><span class="chip ok">ตอบแล้ว</span> <b>{E(a)}</b> · {E(b)}</li>' for a, b in ANSWERED)
    ask = "".join(f'<li><b>{E(a)}</b> · {E(b)}</li>' for a, b in ASK)
    setup = "".join(f'<li><b>{E(a)}</b><div class="cap" style="font-size:14px">{E(b)}</div></li>' for a, b in SETUP)
    roles = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:6px"><p><span class="legend"><span><i style="background:{c}"></i>{num}</span></span></p>'
        f'<h3>{E(t)}</h3><p class="cap" style="font-size:14px">{E(w)}</p></div>'
        for num, c, t, w in [
            ("1", "#FFC23C", f"{B.KIDS_ROLES[0][0]} · {B.KIDS_ROLES[0][1]}", "นั่งเก้าอี้ขวาหลังโซน C ข้าง QR ลูกค้าที่เดินเข้ามุมขวาจ่ายเงินตรงนี้ จดยอด ส่งถุง"),
            ("2", "#2EC4A0", f"{B.KIDS_ROLES[1][0]} · {B.KIDS_ROLES[1][1]}", f"นั่งเก้าอี้ซ้ายหลังโซน B โต๊ะสูง {th} ซม. พอดีมือเด็ก ลูกค้าตัวเล็กยืนลองต่อฝั่งตรงข้ามได้"),
            ("3", "#FF8AC4", f"{B.KIDS_ROLES[2][0]} · {B.KIDS_ROLES[2][1]}", "ยืนมุมหน้าขวาข้างป้ายตั้งพื้น ยิ้ม ยื่นการ์ด ชวนลูกค้าเดินเข้ามาดูราวหมี"),
            ("พ", "var(--line)", "พ่อหรือแม่", "ยืนหลังโต๊ะฝั่งซ้าย เติมของจากกล่อง D ตอบเรื่องสั่งทำ อีกคนพาลูกที่ไม่เข้ากะไปพัก")])

    return f"""{S.head("บูธ OCT. 26 บ้านและสวน")}<style>{SVG_CSS}</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">แผนบูธ · ฝ่ายการตลาดและการขาย · อัปเดต 20 ต.ค. 2569</span>
<h1>บูธ OCT. 26 ที่{FAIR}</h1>
<p class="lead">{DATES} · บูธ 2 × 2 เมตร ผู้จัดให้โต๊ะพาเลท {tw} × {td} ซม. สูง {th} ซม. กับเก้าอี้ {CHAIRS} ตัว
โต๊ะสูงเท่าโต๊ะกาแฟในบ้าน หน้าโต๊ะจึงจัดเป็นโต๊ะกาแฟจริงที่ใช้ของ SOI. 02 ส่วนห้าหมีแขวนบนตะแกรงขวา ข้างมุมที่เปิดให้ลูกค้าเดินเข้ามา</p>
<div class="grid s">
<div class="card kpi"><p class="cap">พื้นที่</p><b class="mono">4 ตร.ม.</b></div>
<div class="card kpi"><p class="cap">ของไปงาน</p><b class="mono">{tot['units']} ชิ้น</b></div>
<div class="card kpi"><p class="cap">ขายหมด ต่อวัน</p><b class="mono">{per_day_sales:,.0f} ฿</b></div>
<div class="card kpi"><p class="cap">งบอุปกรณ์ที่ต้องซื้อ</p><b class="mono">{lo_buy/1000:.1f}–{hi_buy/1000:.1f}k ฿</b></div>
<div class="card kpi"><p class="cap">อยู่ในบูธพร้อมกัน</p><b class="mono">3–4 คน</b></div></div></header>

<section id="given"><span class="eyebrow">ของที่ผู้จัดให้</span><h2>โต๊ะพาเลทกับเก้าอี้พับ</h2>
<div class="two"><figure class="card" style="margin:0;display:flex;flex-direction:column;gap:10px">
<div class="photo"><img src="organizer-table.jpg" alt="แบบโต๊ะพาเลท 1.17 × 0.80 ม. สูง 0.50 ม. ขาเหล็ก และเก้าอี้พับผ้าใบโครงไม้ จากผู้จัด"></div>
<figcaption class="cap">แบบจากผู้จัด · ได้รับ 20 ต.ค.</figcaption></figure>
<div style="display:flex;flex-direction:column;gap:var(--s3)">
<ul><li><b>สูง {th} ซม. เท่าโต๊ะกาแฟ</b> ตรงกับไอเดียโต๊ะกาแฟจำลองพอดี และเด็กนั่งเก้าอี้สาธิตได้สบาย</li>
<li><b>เตี้ยสำหรับผู้ใหญ่</b> ซ้อนลังไม้ยกของขึ้นมา 75–100 ซม. และใช้ตะแกรงหลังบูธเป็นที่โชว์หลัก</li>
<li><b>ร่องไม้กว้าง</b> วางไม้อัด 4 มม. สองแผ่นรองก่อน แล้วปูผ้าลินินทับ พับขอบให้ยังเห็นไม้พาเลท</li>
<li><b>เล็กกว่าโต๊ะพับในแผนแรก</b> ไม่ต้องซื้อโต๊ะ ผ้าคลุมยาว และเก้าอี้ ประหยัดราว {SAVED[0]:,}–{SAVED[1]:,} บาท และได้มุมหน้าขวาเป็นทางเข้า</li></ul>
<p class="cap">ผู้จัดยืนยันแล้ว 20 ต.ค.: บูธละ 1 โต๊ะ {CHAIRS} เก้าอี้ และมีปลั๊ก 5A</p></div></div></section>

<section id="plan"><span class="eyebrow">มองจากด้านบน</span><h2>ผังบูธ</h2>
<div class="two"><div class="card">{plan_svg()}</div>
<div style="display:flex;flex-direction:column;gap:var(--s3)">
<p>โต๊ะพาเลทชิดมุมหน้าซ้าย มุมหน้าขวาเปิดให้ลูกค้าก้าวเข้ามาพ้นทางเดิน ยืนดูราวหมีและจ่ายเงินได้ไม่ขวางคนเดิน</p>
<ul><li><b>A โต๊ะกาแฟ</b> ราว 39 ซม. แก้วบนที่รองแก้ว ผ้าเช็ดปากในห่วงหมี ต้นไม้ ตะกร้าที่รองแก้วลายอื่นให้หยิบเลือก</li>
<li><b>B จุดสาธิต</b> ราว 39 ซม. ลูกนั่งต่อหนังให้ดู ขอบหน้าวางกล่องทดลองให้เด็กลองต่อ</li>
<li><b>C จ่ายเงิน</b> ราว 39 ซม. ลังไม้ซ้อนที่ขอบหลัง วางห้าหมีชิ้นเล็กกับ QR</li>
<li>ใต้โต๊ะใส่กล่อง A B C ของแต่ละโซน กล่อง D ของสำรองอยู่หลังโต๊ะฝั่งซ้าย คลุมผ้า</li></ul>
<p class="legend"><span><i style="background:#FFC23C"></i>1 หัวหน้าร้าน</span><span><i style="background:#2EC4A0"></i>2 นักสาธิต</span>
<span><i style="background:#FF8AC4"></i>3 ผู้ต้อนรับ</span><span><i style="background:var(--line)"></i>พ พ่อหรือแม่</span></p></div></div></section>

<section id="front"><span class="eyebrow">มองจากทางเดิน</span><h2>หน้าบูธ</h2>
<div class="two"><div class="card">{front_svg()}</div>
<div style="display:flex;flex-direction:column;gap:var(--s3)">
<p>บูธมีสามระดับให้คนเห็นจากระยะต่างกัน</p>
<ul><li><b>150–200 ซม.</b> โลโก้ OCT. 26 บนโรลอัพ และราวหมีห้าตัวบนตะแกรงขวา มองเห็นจากไกล</li>
<li><b>75–140 ซม.</b> ของแขวนบนตะแกรงและลังไม้บนโต๊ะ ระดับมือผู้ใหญ่</li>
<li><b>{th} ซม.</b> หน้าโต๊ะพาเลท โต๊ะกาแฟจริงกับจุดสาธิต ระดับเดียวกับเด็ก</li></ul>
<p class="cap">ป้ายตั้งพื้นมุมขวาเขียนชวนให้เข้ามาลองต่อหนัง ถ้าผู้จัดให้ผนังมา ตะแกรงตั้งชิดผนังได้เลย ไม่ต้องเจาะหรือติดเทป</p></div></div></section>

<section id="sell"><span class="eyebrow">ขายอะไรหน้าบูธ</span><h2>คนงานบ้านและสวนมาหาของแต่งบ้าน</h2>
<p class="lead">งานนี้ให้ของแต่งโต๊ะเป็นตัวหลัก ส่วนห้าหมีเป็นของขวัญ ประโยคแรกที่ใช้ทัก: “ลองวางแก้วดูได้เลยค่ะ/ครับ หนังแท้จากเศษหนัง ทำกันเองทั้งบ้าน”</p>
<div class="tbl"><table><thead><tr><th>สินค้า</th><th>ราคา ฿</th><th>เตรียมไป</th></tr></thead><tbody>{hero_rows}</tbody></table></div>
<p class="cap">แผ่นรองจาน ปลอกแก้ว และที่รองแก้วไส้ไม้ก๊อกมีของน้อย ให้วางโชว์แล้วรับสั่งทำเป็นชุด 4 หรือ 6 ชิ้น จดชื่อกับเบอร์หรือไอจีลงสมุดรับออเดอร์ และส่งราคาให้หลังงาน
ลูกค้าขอลดราคา ใช้บทเดิม: ซื้อสามชิ้นได้สติกเกอร์หมีฟรี ราคาเท่าเดิม</p></section>

<section id="gear"><span class="eyebrow">อุปกรณ์</span><h2>ของที่ต้องเตรียม</h2>
<p>ต้องซื้อจริงประมาณ <b class="mono">{lo_buy:,}–{hi_buy:,} บาท</b> ถ้าไม่มีอะไรที่บ้านเลยและซื้อครบทุกอย่าง <span class="mono">{lo_all:,}–{hi_all:,} บาท</span>
ราคาเป็นราคาประมาณ ยังไม่ได้เช็กกับร้าน ค่างานพิมพ์ป้ายราคา การ์ด สติกเกอร์ อยู่ในรายการพิมพ์ของ Launch Kit แยกต่างหาก</p>
<div class="tbl"><table><thead><tr><th>ของ</th><th>บาท</th><th></th></tr></thead><tbody>{gear_rows}</tbody></table></div></section>

<section id="ask"><span class="eyebrow">ผู้จัดงาน</span><h2>ตอบแล้ว {len(ANSWERED)} ข้อ ยังต้องถาม {len(ASK)} ข้อ</h2>
<div class="card"><ul>{answered}</ul></div>
<div class="card"><ul>{ask}</ul></div></section>

<section id="days"><span class="eyebrow">20–25 ต.ค.</span><h2>ทำอะไรวันไหน</h2>
<div class="tbl"><table><tbody>{plan_rows}</tbody></table></div></section>

<section id="setup"><span class="eyebrow">เช้าวันแรก</span><h2>ลำดับจัดบูธ {len(SETUP)} ขั้น</h2>
<div class="card"><ol>{setup}</ol></div>
<p class="cap">ทั้งหมดใช้เวลาประมาณ 60–90 นาที ถ้าซ้อมที่บ้านวันพฤหัสแล้ว</p></section>

<section id="who"><span class="eyebrow">คนในบูธ</span><h2>ใครอยู่ตรงไหน</h2>
<p>หลังโต๊ะลึกราว 115 ซม. มีเก้าอี้ผู้จัด {CHAIRS} ตัวให้นักสาธิตกับหัวหน้าร้าน อยู่ได้พร้อมกัน 3–4 คน เด็กทำกะละ 45 นาที พัก 15 นาที พ่อหรือแม่อยู่ที่บูธตลอด อีกคนพาลูกที่ไม่เข้ากะไปพักหรือเดินดูงาน</p>
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
<tr><td class="mono" style="white-space:nowrap">booth-20261019/build.py</td><td>ข้อมูลแผนบูธ: ขนาดโต๊ะ ผัง อุปกรณ์ ราคา ไทม์ไลน์ แก้ที่นี่แล้วรันใหม่</td></tr>
<tr><td class="mono" style="white-space:nowrap">booth-20261019/site/index.html</td><td>หน้านี้ (สร้างจาก build.py)</td></tr>
<tr><td class="mono" style="white-space:nowrap">booth-20261019/site/organizer-table.jpg</td><td>แบบโต๊ะพาเลทและเก้าอี้จากผู้จัด</td></tr>
<tr><td class="mono" style="white-space:nowrap">brand-20261014/brand.py</td><td>ราคาและสต็อกสินค้าอ่านจากไฟล์นี้</td></tr>
</tbody></table></div></section>

<section id="check"><span class="eyebrow">ต้องเช็ก</span><h2>ก่อนซื้อของ</h2>
<div class="card"><ol>
<li>ผู้จัดให้ย้ายโต๊ะไปมุมหน้าซ้ายได้ไหม ถ้าไม่ได้ ผังยังใช้ได้ แค่ย้ายทางเข้าไปฝั่งที่ว่าง</li>
<li>ไม้อัดสองแผ่นต้องใส่รถได้ วัดท้ายรถก่อนไปร้าน แต่ละแผ่น 58 × 80 ซม.</li>
<li>เลขบูธ เอามาใส่โพสต์ เจอกันที่บูธ</li>
<li>ไฟล์โรลอัพ 80 × 200 ซม. ส่งร้านพิมพ์วันนี้ ให้ได้รับทันวันพุธ</li>
<li>ของจาก Shopee ถ้าร้านส่งไม่ทันวันพุธ ซื้อหน้าร้านแทน</li></ol></div></section>
</div>"""


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(page())
    print("wrote site/index.html")
