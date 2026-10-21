"""Booth plan for หนูทดลอง KIDS MARKET at บ้านและสวนแฟร์ Living Festival 2026, two weekends (23–25 Oct and
30 Oct–1 Nov 2569): one 2 x 2 m booth, gear that is easy to buy.

The organiser gives each booth a pallet coffee table (117 x 80 cm, 50 cm high) and two folding chairs
(site/organizer-table.jpg, their drawing, received 20 Oct). Reads products and prices from
../brand-20261014/brand.py and the page style from its site/build.py, writes site/index.html.
Run: python3 booth-20261019/build.py
"""
import html, importlib.util, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.join(os.path.dirname(HERE), "brand-20261014")
sys.path.insert(0, BRAND_DIR)
import brand as B

_sp = importlib.util.spec_from_file_location("brand_site", os.path.join(BRAND_DIR, "site", "build.py"))
S = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S)
E = html.escape
P = {p["n"]: p for p in B.PRODUCTS}

FAIR = "บ้านและสวนแฟร์ Living Festival 2026"
ZONE = "หนูทดลอง KIDS MARKET"
PLACE = "อิมแพ็ค เมืองทองธานี ชาเลนเจอร์ 2–3"
DATES = "23–25 ต.ค. และ 30 ต.ค.–1 พ.ย. 2569"
HOURS = "ศุกร์–อาทิตย์ 10:00–17:00"
SALE_DAYS = 6          # two weekends, confirmed 21 Oct
W = D = 200            # booth, cm
TABLE = (117, 80, 50)  # organiser's pallet table w, d, h (cm), steel frame, slatted top
TX, TY = 3, D - 80 - 3 # table pushed into the front-left corner; the front-right corner is the way in
XS = (138, 10)         # X-stand: left edge (cm from the booth's left side), banner bottom off the floor (cm)
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
    ("ฟิวเจอร์บอร์ด 5 มม. 65 × 130 ซม. และเทปผ้า", "2 แผ่น 1 ม้วน", "ร้านเครื่องเขียน, ร้านถ่ายเอกสาร", 150, 300, "buy",
     "ร่องไม้พาเลทกว้าง ต้องมีแผ่นรองก่อนปูผ้า ตัดแผ่นละ 58 × 80 ซม. ให้ลอนวิ่งขวางร่องไม้ แล้วติดเทปผ้าด้านล่างตามแนว 80 ซม. เป็นบานพับ พับเหลือ 58 × 80 ใส่รถง่าย"),
    ("ผ้าลินินหรือผ้าดิบ สีครีม", "2 ม.", "ร้านผ้า, Shopee", 150, 300, "buy",
     "ปูทับฟิวเจอร์บอร์ด พับขอบให้ยังเห็นไม้พาเลท เศษที่เหลือห่อกล่องยกของและคลุมกล่องสต็อก"),
    ("ป้าย X-stand 60 × 160 ซม. พร้อมขาตั้ง", "1 ชุด", "ร้านพิมพ์ไวนิลใกล้บ้าน ส่วนใหญ่เสร็จวันเดียว", 300, 500, "buy",
     "ไฟล์พิมพ์พร้อมส่ง: xstand/oct26-xstand-60x160.pdf · ตั้งมุมหน้าขวาติดทางเดิน ลูกค้าเห็นทั้งแผ่นและสแกน QR ได้ ตั้งได้เอง พับเก็บใส่ถุงได้"),
    ("ตะแกรงลวดแขวนของ 60 × 150 ซม. พร้อมขาตั้ง", "1 ชุด", "Shopee, HomePro", 350, 600, "buy",
     "ตั้งด้วยขาของตัวเอง กลางด้านหลัง ตะแกรงโปร่ง ลูกค้าเห็นของแขวนได้ทั้งสองฝั่ง ห้าหมีอยู่บน SOI. 02 อยู่ล่าง"),
    ("ตะขอแขวนตะแกรงและตะขอตัว S", "20 อัน", "Shopee, ร้าน 20 บาท", 50, 100, "buy", "แขวนราวหมี ที่ห้อยกระเป๋า ป้ายชื่อ"),
    ("ตะกร้าหวายหรือถาดไม้ใบเล็ก", "4 ใบ", "ร้าน 20 บาท, Daiso, จตุจักร", 200, 300, "buy",
     "แยกที่รองแก้วตามลาย ลูกค้าหยิบเลือกเองได้"),
    ("กรอบป้ายอะคริลิกตั้งโต๊ะ A5", "2 อัน", "ร้านเครื่องเขียน, Shopee", 80, 140, "buy", "QR พร้อมเพย์ จุดจ่ายเงินและโต๊ะกาแฟ"),
    ("ไม้หนีบผ้าไม้เล็ก", "12 อัน", "ร้าน 20 บาท", 20, 40, "buy", "หนีบป้ายราคาแทนกรอบอะคริลิก เข้ากับงานไม้พาเลท"),
    ("โคมไฟหนีบ LED แสงวอร์ม", "1 ดวง", "HomePro, Shopee", 200, 350, "buy",
     "หนีบที่กล่องโซน C ส่องโต๊ะกาแฟ หนังดูสวยใต้แสงอุ่น ไม่เกิน 10 วัตต์ ปลั๊กบูธ 5A รับได้สบาย"),
    ("ของจิปาถะ: เคเบิลไทร์ เทปสองหน้า เทปใส กรรไกร คัตเตอร์ ปากกาเมจิก ถุงขยะ ทิชชู่", "1 ถุง", "ร้าน 20 บาท, 7-Eleven",
     150, 200, "buy", ""),
    ("ป้ายคอลเลกชัน SOI. 02 และห้าหมี Love", "2 แผ่น", "เศษฟิวเจอร์บอร์ดที่ตัดเหลือ", 0, 0, "free",
     "พิมพ์ชื่อคอลเลกชันติดบนเศษบอร์ด วางที่โต๊ะ ข้อความชวนเข้าบูธอยู่บน X-stand แล้ว"),
    ("กล่องรองเท้าหรือกล่องกระดาษแข็ง ห่อผ้า", "2 ใบ", "จากบ้าน", 0, 0, "home",
     "แทนลังไม้ โต๊ะสูงแค่ 50 ซม. ซ้อนกล่องยกของขึ้นมาระดับมือผู้ใหญ่ 75–100 ซม."),
    ("ปลั๊กพ่วง มอก. ยาว 5 ม.", "1 อัน", "จากบ้าน", 0, 0, "home", ""),
    ("กล่องพลาสติกมีฝา ซ้อนได้", "4 ใบ", "จากบ้าน", 0, 0, "home", "A B C ใต้โต๊ะพาเลท D หลังโต๊ะฝั่งซ้าย คลุมผ้า"),
    ("ผ้าสักหลาดหรือแผ่นรองตัด", "1 แผ่น", "จากบ้าน", 0, 0, "home", "พื้นจุดสาธิต"),
    ("แก้วกาแฟ ผ้าเช็ดปาก จานรอง", "1 ชุด", "จากบ้าน", 0, 0, "home", "ใช้จัดโต๊ะกาแฟ"),
    ("ต้นไม้กระถางเล็ก", "1 กระถาง", "จากบ้าน", 0, 0, "home",
     "วางบนที่รองแก้วไส้ไม้ก๊อก เข้าธีมบ้านและสวน ถ้าที่บ้านไม่มี ซื้อในงานราว 100 บาท"),
    ("กล่องเงินและเงินทอน 1,500 บาท", "1 กล่อง", "จากบ้าน", 0, 0, "home", "บูธเปิดทุกด้าน กล่องเงินอยู่กับหัวหน้าร้านหรือพ่อแม่ตลอด ห้ามวางทิ้งบนโต๊ะ ไม่นับในงบแต่งบูธ"),
    ("โคมไฟหนีบดวงที่ 2", "1 ดวง", "HomePro, Shopee", 200, 350, "opt", "หนีบตะแกรง ถ้าแสงในฮอลล์มืด"),
    ("กระจกตั้งโต๊ะเล็ก", "1 บาน", "ร้าน 20 บาท", 60, 120, "opt", "ลูกค้าลองห้อยที่ห้อยกระเป๋าแล้วส่องดู"),
    ("รถเข็นพับได้", "1 คัน", "ยืม", 0, 0, "opt", "ขนกล่องจากลานจอดถึงฮอลล์ทีเดียวจบ"),
]
KIND = {"org": ("ผู้จัดให้", "ok"), "buy": ("ต้องซื้อ", "ext"), "home": ("มีที่บ้าน", "ok"), "free": ("ไม่ต้องซื้อ", "ok"),
        "opt": ("มีก็ดี", "mid")}
BUDGET = 3000          # owner's cap for dressing the booth, 20 Oct
assert sum(g[4] for g in GEAR if g[5] == "buy") <= BUDGET, "must-buy gear is over the booth budget"
CUTS = [   # what changed to fit the budget, 20 Oct
    ("ป้ายโรลอัพ 80 × 200", "ป้าย X-stand 60 × 160 ตั้งได้เอง เพราะบูธไม่มีผนัง"),
    ("ตะแกรง 2 ชุด", "ตะแกรง 1 ชุดกลางด้านหลัง"),
    ("ลังไม้ 3 ใบ", "กล่องจากบ้านห่อผ้า"),
    ("ป้ายตั้งพื้นขาตั้ง A", "X-stand ทำหน้าที่ชวนเข้าบูธแทน"),
    ("กรอบอะคริลิก 12 อัน", "กรอบ A5 2 อันสำหรับ QR กับไม้หนีบ"),
    ("ไฟหนีบ 3 ดวง", "1 ดวง ดวงที่ 2 ซื้อเมื่อแสงในฮอลล์มืด"),
]
SAVED = (900, 1900)   # folding table, long tablecloth and two stools from the first plan, no longer bought

ASK = [
    ("บูธติดทางเดินด้านไหน", "บูธไม่มีผนัง ลูกค้าเดินมาจากกี่ด้าน หน้าหลักหันไปทางไหน และมีป้ายชื่อบูธหรือไฟสปอตไลต์ไหม"),
    ("เก็บของข้ามคืน", "ทิ้งของไว้ในบูธข้ามคืน และระหว่างสองสัปดาห์ (จ.–พฤ.) ได้ไหม มียามไหม ถ้าไม่ได้ ขนสต็อกกลับบ้านทุกเย็น"),
    ("ป้ายชื่อหน้าบูธ", "ส่งชื่อให้สะกด OCT. 26 ตัวใหญ่ มีจุด และเว้นวรรคก่อน 26"),
    ("เลขบูธ ฮอลล์ โซน", "ใส่ในโพสต์ เจอกันที่บูธ และในการ์ด"),
    ("เวลาเข้าจัดและรื้อบูธ", "ทั้งสองสัปดาห์ จุดขนของ ลานจอดรถ"),
    ("บัตรผู้ออกบูธ", "ได้กี่ใบ เด็กต้องมีบัตรไหม เราไปกัน 5 คน"),
    ("กฎการตกแต่ง", "ของตั้งสูงได้ไม่เกินเท่าไร (X-stand 160 ซม. ตะแกรงราว 180 ซม.) ใช้ไฟของตัวเองได้ไหม"),
]

ANSWERED = [   # organiser's answers, 20 Oct
    ("โต๊ะและเก้าอี้", f"ได้บูธละ 1 ชุด: โต๊ะพาเลท 1 ตัว เก้าอี้ {CHAIRS} ตัว"),
    ("ย้ายโต๊ะ", "ย้ายโต๊ะพาเลทไปมุมหน้าซ้ายเองได้"),
    ("หน้าโต๊ะ", "ร่องไม้กว้าง ต้องมีแผ่นรองก่อน ใช้ฟิวเจอร์บอร์ดพับได้"),
    ("ผนัง", "ไม่มีผนังทั้งสี่ด้าน ใช้ป้ายและตะแกรงที่ตั้งได้เอง"),
    ("ไฟ", "มีปลั๊ก 5A (ราว 1,100 วัตต์) ไฟหนีบ LED กับชาร์จมือถือใช้ไม่ถึง 50 วัตต์ ห้ามเสียบกาต้มน้ำหรือไดร์เป่าผม"),
]

PLAN = [
    ("อ. 20 ต.ค.", "วันนี้", f"ถามผู้จัด {len(ASK)} ข้อด้านล่าง · สั่งของ Shopee แบบส่งด่วน (ตะแกรง ตะขอ ไฟหนีบ) · "
                         "ส่งไฟล์ X-stand (xstand/oct26-xstand-60x160.pdf) เข้าร้านพิมพ์ · ซื้อฟิวเจอร์บอร์ด ผ้า ตะกร้า ไม้หนีบ กรอบ A5 ที่ร้านเครื่องเขียน ร้านผ้า ร้าน 20 บาท"),
    ("พ. 21 ต.ค.", "", "รับ X-stand และงานพิมพ์ · ตัดฟิวเจอร์บอร์ดติดเทปบานพับ ทำป้ายจากเศษ · ติดป้ายห้อยสินค้า · ของ Shopee ไม่มาภายในวันนี้ ซื้อหน้าร้านแทน"),
    ("พฤ. 22 ต.ค.", "ซ้อมใหญ่", "ตีเทปกรอบ 2 × 2 ม. บนพื้นบ้าน ใช้โต๊ะกาแฟที่บ้านแทนโต๊ะพาเลท จัดตามผัง ถ่ายรูปเก็บไว้เป็นแบบ ซ้อมขาย แล้วแพ็คกล่อง A B C D"),
    ("ศ. 23 ต.ค.", "วันแรก", "ถึงก่อนเปิดอย่างน้อย 90 นาที จัดตามลำดับด้านล่าง โพสต์รูปบูธพร้อมเลขบูธก่อนงานเปิด"),
    ("ทุกวันขาย", "ทุกเย็น", "ปิดยอด นับเงิน เทียบสมุด จดว่าตัวไหนหมด เติมของจากกล่อง D ก่อนกลับ"),
    ("อา. 25 ต.ค.", "จบสัปดาห์แรก", "เก็บของตามที่ผู้จัดบอก ถ่ายรูปบูธ เตรียมโพสต์ Happy 26.10 พรุ่งนี้"),
    ("จ. 26 ต.ค.", "วันเกิดแบรนด์", "โพสต์ Happy 26.10 ขอบคุณลูกค้า สรุปยอดสัปดาห์แรกต่อสินค้า"),
    ("27–29 ต.ค.", "เติมของ", "ตัดและประกอบตัวที่ขายดีเพิ่ม ใช้เศษหนังล็อตใหญ่ที่เหลือ (หัวหมี) · โพสต์คลิปจากสัปดาห์แรก ชวนมาสัปดาห์ที่สอง"),
    ("30 ต.ค.–1 พ.ย.", "สัปดาห์ที่สอง", "ที่เดิม เวลาเดิม ย้ายตัวที่ขายดีไปหน้าโต๊ะ อาทิตย์เย็นรื้อบูธ คืนโต๊ะเก้าอี้ ถ่ายรูปบูธครั้งสุดท้าย"),
]

SETUP = [
    ("ขยับโต๊ะพาเลทไปมุมหน้าซ้าย กางฟิวเจอร์บอร์ด แล้วปูผ้า", "เว้นมุมหน้าขวาไว้เป็นทางเข้า · ใส่กล่อง A B C ใต้โต๊ะ"),
    ("ตั้งตะแกรงกลางด้านหลัง และ X-stand มุมหน้าขวา", "หันหน้า X-stand ไปทางเดินหลัก ถ้ามีลมแอร์แรง ถ่วงขาด้วยถุงทรายหรือขวดน้ำ"),
    ("วางเก้าอี้สองตัวหลังโต๊ะ", "ตัวซ้ายนักสาธิต ตัวขวาหัวหน้าร้าน"),
    ("ซ้อนกล่องห่อผ้าที่ขอบหลังของโต๊ะ", "โซน C สูงขึ้นมาราว 75 ซม. วางห้าหมีชิ้นเล็ก และ QR"),
    ("จัดโต๊ะกาแฟที่ขอบหน้าโซน A", "แผ่นรองจาน แก้วบนที่รองแก้ว ผ้าเช็ดปากใส่ห่วงหมี ต้นไม้บนที่รองแก้วไส้ไม้ก๊อก ตะกร้าที่รองแก้วลายอื่นวางข้าง ๆ"),
    ("แขวนของบนตะแกรง", "ราวหมีห้าตัวพาดบนสุด ที่ห้อยกระเป๋า ป้ายชื่อ · แถวล่าง SOI. 02 (กังหัน ของแขวน ปลอกแก้ว ซอง AirTag)"),
    ("หนีบไฟ", "ที่กล่องโซน C ส่องโต๊ะกาแฟ"),
    ("ป้ายราคา QR และป้ายคอลเลกชัน", "QR พร้อมเพย์ในกรอบ A5 ตรงจุดจ่ายเงินและโต๊ะกาแฟ · ป้ายราคาหนีบไม้หนีบ · ป้ายคอลเลกชันบนโต๊ะ"),
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
    # no walls: one free-standing grid at the back in the middle, X-stand at the front-right corner facing the aisle
    out += [rect(70, 0, 60, 7, "grid"), text(100, 20, "ตะแกรง ห้าหมี · SOI. 02", "ts")]
    out += [rect(XS[0], 190, 60, 4, "roll", 1),
            f'<line x1="{X(XS[0]+6):.1f}" y1="{Y(176):.1f}" x2="{X(XS[0]+54):.1f}" y2="{Y(188):.1f}" class="leg"/>',
            f'<line x1="{X(XS[0]+54):.1f}" y1="{Y(176):.1f}" x2="{X(XS[0]+6):.1f}" y2="{Y(188):.1f}" class="leg"/>',
            text(XS[0] + 30, 172, "X-stand", "tz")]
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
            text(TX + zw * 2.5, TY + 40, "C จ่ายเงิน", "tz"), text(TX + zw * 2.5, TY + 52, "กล่อง ห้าหมี", "ts"),
            text(TX + tw / 2, TY + 70, f"โต๊ะพาเลท {tw} × {td} ซม. สูง {TABLE[2]}", "ts")]
    # people
    out += [badge(TX + zw * 1.5, 83, "2", "bm"), badge(TX + zw * 2.5 + 14, 83, "1", "bs"),
            badge(XS[0] - 8, 176, "3", "bp"), badge(50, 40, "พ", "bk")]
    # lamps
    for lx, ly in ((TX + zw * 2 + 6, TY + 6),):
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
    out = []
    # no walls: one free-standing grid at the back in the middle, X-stand at the front-right corner
    for gx, label in ((70, "ห้าหมี · SOI. 02"),):
        out.append(rect(gx + 3, 30, 54, 150, "grid"))
        out += [f'<line x1="{X(gx+3+i*9):.1f}" y1="{Y(180):.1f}" x2="{X(gx+3+i*9):.1f}" y2="{Y(30):.1f}" class="mesh"/>' for i in range(1, 6)]
        out += [f'<line x1="{X(gx+3):.1f}" y1="{Y(30+i*15):.1f}" x2="{X(gx+57):.1f}" y2="{Y(30+i*15):.1f}" class="mesh"/>' for i in range(1, 10)]
        out.append(text(gx + 30, 186, f"ตะแกรง {label}", "ts"))
    # bear garland and hanging items
    out.append(f'<path d="M{X(74):.1f} {Y(170):.1f} Q{X(100):.1f} {Y(158):.1f} {X(126):.1f} {Y(170):.1f}" class="garland"/>')
    out += [f'<circle cx="{X(80+i*10):.1f}" cy="{Y(166 - (2 if i in (1, 2, 3) else 0)):.1f}" r="5" class="bear"/>' for i in range(5)]
    for gx in (70,):
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
    # the X-stand itself, drawn from its print preview, standing at the front-right corner
    x0, h0 = XS
    out += [f'<line x1="{X(x0+4):.1f}" y1="{Y(0):.1f}" x2="{X(x0+30):.1f}" y2="{Y(h0+10):.1f}" class="leg"/>',
            f'<line x1="{X(x0+56):.1f}" y1="{Y(0):.1f}" x2="{X(x0+30):.1f}" y2="{Y(h0+10):.1f}" class="leg"/>',
            f'<image href="xstand-preview.png" x="{X(x0):.1f}" y="{Y(h0+160):.1f}" width="{60*k:.1f}" height="{160*k:.1f}" preserveAspectRatio="none"/>',
            f'<rect x="{X(x0):.1f}" y="{Y(h0+160):.1f}" width="{60*k:.1f}" height="{160*k:.1f}" class="xs-edge"/>',
            text(x0 + 30, h0 + 166, "X-stand 60 × 160", "ts")]
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
.draw .leg{stroke:var(--ink);stroke-width:1.5}.draw .xs-edge{fill:none;stroke:var(--ink);stroke-width:1}
.draw .mesh{stroke:var(--muted);stroke-width:.6;opacity:.6}
.draw .logo{font-family:"Jost","Anuphan",sans-serif;font-weight:500;font-size:22px;fill:#FFFFFF}
.draw .logo-s{font-size:10px;fill:#FFFFFF}
.draw .garland{fill:none;stroke:#B8743A;stroke-width:1.5}.draw .bear{fill:#B8743A}
.draw .item{fill:#B8743A;opacity:.85}.draw .qr{fill:var(--ink)}
.draw .riser{fill:#C99A68;stroke:#8A5A2B;stroke-width:1}
.draw .cup{fill:#FFFFFF;stroke:var(--ink)}.draw .plant{fill:#B8743A}.draw .leaf{fill:#2EC4A0}
.draw .mat{fill:var(--ink)}
.draw .sign{fill:#FFFFFF;stroke:var(--ink)}.draw .fb{fill:#FFFFFF;stroke:var(--ink);stroke-width:1.2}.draw .fb-t{font-size:13px;font-weight:600;fill:#2449D8}
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
    _, big, small = B.piece_usage()
    LOT_BIG_LEFT, LOT_SMALL_NEED, LOT_SMALL_CAP = B.LOT_CAPACITY["ใหญ่"] - big, small, B.LOT_CAPACITY["เล็ก"]
    per_day_units, per_day_sales = tot["units"] / SALE_DAYS, tot["sales"] / SALE_DAYS
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
    cuts = "".join(f'<li><s>{E(a)}</s> → {E(b)}</li>' for a, b in CUTS)
    answered = "".join(f'<li><span class="chip ok">ตอบแล้ว</span> <b>{E(a)}</b> · {E(b)}</li>' for a, b in ANSWERED)
    ask = "".join(f'<li><b>{E(a)}</b> · {E(b)}</li>' for a, b in ASK)
    setup = "".join(f'<li><b>{E(a)}</b><div class="cap" style="font-size:14px">{E(b)}</div></li>' for a, b in SETUP)
    roles = "".join(
        f'<div class="card" style="display:flex;flex-direction:column;gap:6px"><p><span class="legend"><span><i style="background:{c}"></i>{num}</span></span></p>'
        f'<h3>{E(t)}</h3><p class="cap" style="font-size:14px">{E(w)}</p></div>'
        for num, c, t, w in [
            ("1", "#FFC23C", f"{B.KIDS_ROLES[0][0]} · {B.KIDS_ROLES[0][1]}", "นั่งเก้าอี้ขวาหลังโซน C ข้าง QR ลูกค้าที่เดินเข้ามุมขวาจ่ายเงินตรงนี้ จดยอด ส่งถุง"),
            ("2", "#2EC4A0", f"{B.KIDS_ROLES[1][0]} · {B.KIDS_ROLES[1][1]}", f"นั่งเก้าอี้ซ้ายหลังโซน B โต๊ะสูง {th} ซม. พอดีมือเด็ก ลูกค้าตัวเล็กยืนลองต่อฝั่งตรงข้ามได้"),
            ("3", "#FF8AC4", f"{B.KIDS_ROLES[2][0]} · {B.KIDS_ROLES[2][1]}", "ยืนมุมหน้าขวาข้าง X-stand ยิ้ม ยื่นการ์ด ชวนลูกค้าเดินเข้ามาดูราวหมี"),
            ("พ", "var(--line)", "พ่อหรือแม่", "ยืนหลังโต๊ะฝั่งซ้าย ดูด้านหลังกับกล่อง D เพราะบูธเปิดทุกด้าน เก็บกล่องเงิน ตอบเรื่องสั่งทำ อีกคนพาลูกที่ไม่เข้ากะไปพัก")])

    LOW, HANDLE = min(p["price"] for p in B.PRODUCTS), B.BRAND["handle"]
    return f"""{S.head("บูธ OCT. 26 บ้านและสวน")}<style>{SVG_CSS}</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">แผนบูธ · ฝ่ายการตลาดและการขาย · อัปเดต 20 ต.ค. 2569</span>
<h1>บูธ OCT. 26 ที่บ้านและสวนแฟร์</h1>
<p class="lead">โซน{ZONE} · {FAIR} · {PLACE} · {DATES} · {HOURS} รวม {SALE_DAYS} วันขาย · บูธ 2 × 2 เมตร ผู้จัดให้โต๊ะพาเลท {tw} × {td} ซม. สูง {th} ซม. กับเก้าอี้ {CHAIRS} ตัว
โต๊ะสูงเท่าโต๊ะกาแฟในบ้าน หน้าโต๊ะจึงจัดเป็นโต๊ะกาแฟจริงที่ใช้ของ SOI. 02 ส่วนห้าหมีแขวนบนตะแกรงกลางด้านหลัง และ X-stand มุมหน้าขวาขายของแทนเราตลอดเวลา</p>
<div class="grid s">
<div class="card kpi"><p class="cap">พื้นที่</p><b class="mono">4 ตร.ม.</b></div>
<div class="card kpi"><p class="cap">ของไปงาน</p><b class="mono">{tot['units']} ชิ้น</b></div>
<div class="card kpi"><p class="cap">ขายหมด ต่อวัน</p><b class="mono">{per_day_sales:,.0f} ฿</b></div>
<div class="card kpi"><p class="cap">งบแต่งบูธ (คิดราคาสูงสุด)</p><b class="mono">{hi_buy:,} / {BUDGET:,} ฿</b></div>
<div class="card kpi"><p class="cap">อยู่ในบูธพร้อมกัน</p><b class="mono">3–4 คน</b></div></div></header>

<section id="given"><span class="eyebrow">ของที่ผู้จัดให้</span><h2>โต๊ะพาเลทกับเก้าอี้พับ</h2>
<div class="two"><figure class="card" style="margin:0;display:flex;flex-direction:column;gap:10px">
<div class="photo"><img src="organizer-table.jpg" alt="แบบโต๊ะพาเลท 1.17 × 0.80 ม. สูง 0.50 ม. ขาเหล็ก และเก้าอี้พับผ้าใบโครงไม้ จากผู้จัด"></div>
<figcaption class="cap">แบบจากผู้จัด · ได้รับ 20 ต.ค.</figcaption></figure>
<div style="display:flex;flex-direction:column;gap:var(--s3)">
<ul><li><b>สูง {th} ซม. เท่าโต๊ะกาแฟ</b> ตรงกับไอเดียโต๊ะกาแฟจำลองพอดี และเด็กนั่งเก้าอี้สาธิตได้สบาย</li>
<li><b>เตี้ยสำหรับผู้ใหญ่</b> ซ้อนกล่องห่อผ้ายกของขึ้นมา 75–100 ซม. และใช้ตะแกรงกับ X-stand เป็นจุดที่มองจากไกล</li>
<li><b>ร่องไม้กว้าง</b> กางฟิวเจอร์บอร์ดพับได้รองก่อน แล้วปูผ้าลินินทับ พับขอบให้ยังเห็นไม้พาเลท</li>
<li><b>เล็กกว่าโต๊ะพับในแผนแรก</b> ไม่ต้องซื้อโต๊ะ ผ้าคลุมยาว และเก้าอี้ ประหยัดราว {SAVED[0]:,}–{SAVED[1]:,} บาท และได้มุมหน้าขวาเป็นทางเข้า</li></ul>
<p class="cap">ผู้จัดยืนยันแล้ว 20 ต.ค.: บูธละ 1 โต๊ะ {CHAIRS} เก้าอี้ ย้ายโต๊ะเองได้ และมีปลั๊ก 5A</p></div></div></section>

<section id="plan"><span class="eyebrow">มองจากด้านบน</span><h2>ผังบูธ</h2>
<div class="two"><div class="card">{plan_svg()}</div>
<div style="display:flex;flex-direction:column;gap:var(--s3)">
<p>โต๊ะพาเลทชิดมุมหน้าซ้าย มุมหน้าขวาเปิดให้ลูกค้าก้าวเข้ามาพ้นทางเดิน ยืนดูราวหมีและจ่ายเงินได้ไม่ขวางคนเดิน</p>
<ul><li><b>A โต๊ะกาแฟ</b> ราว 39 ซม. แก้วบนที่รองแก้ว ผ้าเช็ดปากในห่วงหมี ต้นไม้ ตะกร้าที่รองแก้วลายอื่นให้หยิบเลือก</li>
<li><b>B จุดสาธิต</b> ราว 39 ซม. ลูกนั่งต่อหนังให้ดู ขอบหน้าวางกล่องทดลองให้เด็กลองต่อ</li>
<li><b>C จ่ายเงิน</b> ราว 39 ซม. กล่องห่อผ้าซ้อนที่ขอบหลัง วางห้าหมีชิ้นเล็กกับ QR</li>
<li>ใต้โต๊ะใส่กล่อง A B C ของแต่ละโซน กล่อง D ของสำรองอยู่หลังโต๊ะฝั่งซ้าย คลุมผ้า</li></ul>
<p class="legend"><span><i style="background:#FFC23C"></i>1 หัวหน้าร้าน</span><span><i style="background:#2EC4A0"></i>2 นักสาธิต</span>
<span><i style="background:#FF8AC4"></i>3 ผู้ต้อนรับ</span><span><i style="background:var(--line)"></i>พ พ่อหรือแม่</span></p></div></div></section>

<section id="front"><span class="eyebrow">มองจากทางเดิน</span><h2>หน้าบูธ</h2>
<div class="two"><div class="card">{front_svg()}</div>
<div style="display:flex;flex-direction:column;gap:var(--s3)">
<p>บูธมีสามระดับให้คนเห็นจากระยะต่างกัน</p>
<ul><li><b>140–180 ซม.</b> โลโก้ OCT. 26 บน X-stand และราวหมีห้าตัวบนตะแกรงกลางด้านหลัง มองเห็นจากไกล</li>
<li><b>75–140 ซม.</b> ของแขวนบนตะแกรงและกล่องบนโต๊ะ ระดับมือผู้ใหญ่</li>
<li><b>{th} ซม.</b> หน้าโต๊ะพาเลท โต๊ะกาแฟจริงกับจุดสาธิต ระดับเดียวกับเด็ก</li></ul>
<p class="cap">บูธไม่มีผนัง ทุกอย่างตั้งได้ด้วยขาของตัวเอง ตะแกรงโปร่ง คนที่เดินผ่านด้านหลังหรือด้านข้างก็เห็นของแขวน X-stand มุมหน้าขวาชวนให้เข้ามาลองต่อ</p></div></div></section>

<section id="xstand"><span class="eyebrow">ป้ายที่ขายของได้เอง</span><h2>X-stand 60 × 160 ซม.</h2>
<div class="two"><figure class="card" style="margin:0;display:flex;justify-content:center">
<img src="xstand-preview.png" alt="แบบ X-stand OCT. 26: โลโก้บนพื้นโคบอลต์ ข้อความ ของใช้จากเศษหนังแท้ ทำกันเองทั้งบ้าน ราคาเริ่ม {LOW} บาท QR ไอจี สินค้าหกอย่างพร้อมราคา" style="max-height:640px;width:auto"></figure>
<div style="display:flex;flex-direction:column;gap:var(--s3)">
<p>ตั้งแล้วขายได้เลย เรียงจากบนลงล่างตามระดับที่คนมอง ขอบบนป้ายสูงจากพื้นราว 170 ซม.</p>
<ol><li><b>แบรนด์ (170–130 ซม.)</b> โลโก้ OCT. 26 บนพื้นโคบอลต์ our crafted things. ของที่เราทำกันเอง และเรื่อง 26 ตุลาคม ให้จำได้</li>
<li><b>ขายตั้งแต่ไกล</b> ของใช้จากเศษหนังแท้ ทำกันเองทั้งบ้าน วงกลมสีมะเขือเทศ เริ่ม {LOW} บาท และ เข้ามาลองต่อเองได้</li>
<li><b>ติดต่อ (ราว 100 ซม.)</b> QR ขนาด 20 ซม. สแกนได้จากราว 2 เมตร ไปไอจี @{HANDLE} พร้อมทุกช่องทาง Shopee และรับสั่งทำของชำร่วย</li>
<li><b>สินค้าที่ขาย</b> หกอย่างพร้อมราคา วาดจากรูปทรงชิ้นหนังจริง</li>
<li><b>คอลเลกชัน</b> SOI. 02 · ห้าหมี FIVE BEARS</li></ol>
<p class="cap">ไม่มีชื่องานหรือวันที่ ใช้ซ้ำได้ทุกงาน · ส่งร้าน: ไฟล์ PDF แบบเวกเตอร์ ฝังฟอนต์แล้ว หรือ JPG 100 dpi ขนาด 2363 × 6299 พิกเซล · ขอบมุมทั้งสี่เว้นไว้ให้ตาไก่ของขาตั้ง</p></div></div></section>

<section id="sell"><span class="eyebrow">ขายอะไรหน้าบูธ</span><h2>คนงานบ้านและสวนมาหาของแต่งบ้าน</h2>
<p class="lead">งานนี้ให้ของแต่งโต๊ะเป็นตัวหลัก ส่วนห้าหมีเป็นของขวัญ ประโยคแรกที่ใช้ทัก: “ลองวางแก้วดูได้เลยค่ะ/ครับ หนังแท้จากเศษหนัง ทำกันเองทั้งบ้าน”</p>
<div class="tbl"><table><thead><tr><th>สินค้า</th><th>ราคา ฿</th><th>เตรียมไป</th></tr></thead><tbody>{hero_rows}</tbody></table></div>
<p class="cap">แผ่นรองจาน ปลอกแก้ว และที่รองแก้วไส้ไม้ก๊อกมีของน้อย ให้วางโชว์แล้วรับสั่งทำเป็นชุด 4 หรือ 6 ชิ้น จดชื่อกับเบอร์หรือไอจีลงสมุดรับออเดอร์ และส่งราคาให้หลังงาน
ลูกค้าขอลดราคา ใช้บทเดิม: ซื้อสามชิ้นได้สติกเกอร์หมีฟรี ราคาเท่าเดิม</p></section>

<section id="gear"><span class="eyebrow">อุปกรณ์</span><h2>ของที่ต้องเตรียม</h2>
<p>ต้องซื้อจริงประมาณ <b class="mono">{lo_buy:,}–{hi_buy:,} บาท</b> อยู่ในงบแต่งบูธ {BUDGET:,} บาท แม้คิดราคาสูงสุด ของที่เหลือใช้ของที่บ้าน
ราคาเป็นราคาประมาณ ยังไม่ได้เช็กกับร้าน ค่างานพิมพ์ป้ายราคา การ์ด สติกเกอร์ อยู่ในรายการพิมพ์ของ Launch Kit แยกต่างหาก</p>
<div class="tbl"><table><thead><tr><th>ของ</th><th>บาท</th><th></th></tr></thead><tbody>{gear_rows}</tbody></table></div>
<div class="card"><h3>ปรับอะไรให้อยู่ในงบ</h3><ul style="margin-top:6px">{cuts}</ul></div></section>

<section id="ask"><span class="eyebrow">ผู้จัดงาน</span><h2>ตอบแล้ว {len(ANSWERED)} ข้อ ยังต้องถาม {len(ASK)} ข้อ</h2>
<div class="card"><ul>{answered}</ul></div>
<div class="card"><ul>{ask}</ul></div></section>

<section id="days"><span class="eyebrow">20 ต.ค.–1 พ.ย.</span><h2>ทำอะไรวันไหน</h2>
<div class="tbl"><table><tbody>{plan_rows}</tbody></table></div></section>

<section id="setup"><span class="eyebrow">เช้าวันแรก</span><h2>ลำดับจัดบูธ {len(SETUP)} ขั้น</h2>
<div class="card"><ol>{setup}</ol></div>
<p class="cap">ทั้งหมดใช้เวลาประมาณ 60–90 นาที ถ้าซ้อมที่บ้านวันพฤหัสแล้ว</p></section>

<section id="who"><span class="eyebrow">คนในบูธ</span><h2>ใครอยู่ตรงไหน</h2>
<p>หลังโต๊ะลึกราว 115 ซม. มีเก้าอี้ผู้จัด {CHAIRS} ตัวให้นักสาธิตกับหัวหน้าร้าน อยู่ได้พร้อมกัน 3–4 คน เด็กทำกะละ 45 นาที พัก 15 นาที พ่อหรือแม่อยู่ที่บูธตลอด อีกคนพาลูกที่ไม่เข้ากะไปพักหรือเดินดูงาน</p>
<div class="grid">{roles}</div></section>

<section id="target"><span class="eyebrow">เป้า</span><h2>ตัวเลขที่ต้องจดทุกเย็น</h2>
<div class="grid s">
<div class="card kpi"><p class="cap">ขายหมดทั้ง {SALE_DAYS} วัน</p><b class="mono">{tot['sales']:,.0f} ฿</b></div>
<div class="card kpi"><p class="cap">เฉลี่ยต่อวัน</p><b class="mono">{per_day_units:.0f} ชิ้น</b></div>
<div class="card kpi"><p class="cap">ยอดต่อวัน</p><b class="mono">{per_day_sales:,.0f} ฿</b></div>
<div class="card kpi"><p class="cap">ต้นทุนของ+แพ็ค</p><b class="mono">{tot['cost']:,.0f} ฿</b></div></div>
<p class="cap">ทุกเย็นจดสามอย่าง: ยอดเงิน จำนวนชิ้นต่อสินค้า และจำนวนออเดอร์สั่งทำ วันที่สองย้ายตัวที่ขายดีไปไว้หน้าสุด</p>
<div class="card"><h3>สต็อกสำหรับสองสัปดาห์</h3><ul style="margin-top:6px">
<li>ของ {tot["units"]} ชิ้นที่เตรียมไว้ ต้องพอ {SALE_DAYS} วัน เฉลี่ยวันละราว {per_day_units:.0f} ชิ้น สัปดาห์แรกอย่าเพิ่งเอาออกหมด เก็บราวหนึ่งในสามไว้ที่บ้าน</li>
<li>จันทร์ 26 ดูยอดจริงต่อสินค้า แล้ว 27–29 ทำเพิ่มเฉพาะตัวที่หมดหรือใกล้หมด</li>
<li>เศษหนังล็อตใหญ่ (หัวหมี) ยังเหลือราว {LOT_BIG_LEFT} ชิ้น ทำที่รองแก้วหมี ที่เก็บสายชาร์จ ที่ห้อยกระเป๋าเพิ่มได้</li>
<li>เศษหนังล็อตเล็ก (แพตเทิร์น 02–06 ของ SOI. 02) แผนสต็อกเดิมต้องใช้ {LOT_SMALL_NEED} ชิ้น แต่ล็อตที่ซื้อได้ {LOT_SMALL_CAP} ชิ้น ต้องซื้อเศษเพิ่ม หรือลดจำนวน SOI. 02 ลง</li></ul></div></section>

<section id="files"><span class="eyebrow">ไฟล์</span><h2>ไฟล์ที่ส่ง</h2>
<div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">booth-20261019/build.py</td><td>ข้อมูลแผนบูธ: ขนาดโต๊ะ ผัง อุปกรณ์ ราคา ไทม์ไลน์ แก้ที่นี่แล้วรันใหม่</td></tr>
<tr><td class="mono" style="white-space:nowrap">booth-20261019/site/index.html</td><td>หน้านี้ (สร้างจาก build.py)</td></tr>
<tr><td class="mono" style="white-space:nowrap">booth-20261019/xstand/oct26-xstand-60x160.pdf</td><td>ไฟล์ X-stand ส่งร้านพิมพ์ (มี .jpg ด้วย) สร้างจาก xstand/build.py</td></tr>
<tr><td class="mono" style="white-space:nowrap">booth-20261019/site/organizer-table.jpg</td><td>แบบโต๊ะพาเลทและเก้าอี้จากผู้จัด</td></tr>
<tr><td class="mono" style="white-space:nowrap">brand-20261014/brand.py</td><td>ราคาและสต็อกสินค้าอ่านจากไฟล์นี้</td></tr>
</tbody></table></div></section>

<section id="check"><span class="eyebrow">ต้องเช็ก</span><h2>ก่อนซื้อของ</h2>
<div class="card"><ol>
<li>ฟิวเจอร์บอร์ดวางบนโต๊ะที่บ้านแล้วกดดู ถ้ายวบตรงร่อง เพิ่มอีกชั้นหรือใช้ 5 มม. สองชั้น</li>
<li>เลขบูธ เอามาใส่โพสต์ เจอกันที่บูธ</li>
<li>สแกน QR บนป้ายด้วยมือถือก่อนส่งพิมพ์ ต้องเปิดไอจี @{HANDLE} ได้จริง</li>
<li>ไฟล์ X-stand ส่งร้านพิมพ์วันนี้ ให้ได้รับทันวันพุธ</li>
<li>บูธติดทางเดินด้านไหน ถ้าหน้าหลักไม่ใช่ด้านที่วาดไว้ หมุนผังทั้งชุดให้โต๊ะหันหาทางเดินหลัก</li>
<li>ของจาก Shopee ถ้าร้านส่งไม่ทันวันพุธ ซื้อหน้าร้านแทน</li></ol></div></section>
</div>"""


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "xstand", "preview.png"), os.path.join(HERE, "site", "xstand-preview.png"))
    open(os.path.join(HERE, "site", "index.html"), "w").write(page())
    print("wrote site/index.html")
