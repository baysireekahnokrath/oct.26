"""OCT. 26 product assortment, 22 Oct 2026: which products we sell, in which wave, and why.

Rules, in force together:
  from the status doc  no 06 (never cut) · single pieces only (joints not proven) · leather 1.0-1.2 mm, nothing that carries load
  owner, 22 Oct        nothing that touches food, drink or the mouth (tanning chemicals) · nothing for young children
Sources: the 7 booth SKUs (status doc), the 02 ideas (../pd.py PIN02_IDEAS), the 50 single-piece ideas
(../single50/single_ideas.py) and the collector coaster set the owner already approved.
Piece costs and stock: Google Sheet "OCT. 26 บัญชี SKU สต็อก และบันทึกการขาย", tab ชิ้นหนัง, read 22 Oct.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "single50"))
import pd
from single_ideas import IDEAS as S50
B = pd.B

PIECE_COST = {"01": 3.89, "02": 3.71, "03": 3.61, "04": 4.22, "05": 3.84, "07": 3.45}      # sheet, 22 Oct
STOCK = {"01": 369, "02": 150, "03": 150, "04": 150, "05": 150, "07": 200}                 # cut, none used yet
NAME = {"01": "หัวหมี", "02": "กังหัน", "03": "กากบาทแคปซูล", "04": "สี่เหลี่ยมมน", "05": "วงกลม", "07": "กากบาทข้อต่อวงกลม"}

RULES = [
    ("ไม่โดนอาหาร เครื่องดื่ม หรือปาก", "หนังผ่านการฟอกด้วยสารเคมี ห้ามทำของที่ใช้กับอาหาร ช้อนส้อม ตะเกียบ หลอด ขอบแก้ว ปากขวด ผ้าเช็ดปาก หรือของในครัว "
     "ที่รองแก้วยังขายได้ เพราะโดนแค่ก้นแก้ว ให้เขียนบนป้ายว่าไม่ใช่ภาชนะใส่อาหาร", "เจ้าของ 22 ต.ค."),
    ("ไม่ทำของสำหรับเด็กเล็ก", "ไม่ทำของเล่น เกม ของใช้โรงเรียน หรือป้ายชื่อของเด็ก ลูกค้าคือพ่อแม่และผู้ใหญ่ โซน KIDS MARKET คือเด็กเป็นคนขาย ไม่ใช่คนใช้", "เจ้าของ 22 ต.ค."),
    ("ชิ้นเดียว ไม่ต่อชิ้น", "ข้อต่อยังไม่ผ่านการทดสอบ ใช้ร่องรับของอย่างอื่นแทน เช่น ไม้ ริบบิ้น ยางยืด การ์ด เข็มกลัด", "เอกสารสถานะ"),
    ("ใช้ 07 แทน 06", "06 ยังไม่ได้ตัด ใช้ 07 แทนทุกที่", "เจ้าของ 22 ต.ค."),
    ("ไม่รับแรง", "หนังที่มีหนา 1.0–1.2 มม. ของที่ถูกดึงหรือแขวนต้องรอหนัง 2 มม. ตามมติ 16 ต.ค.", "มติ 16 ต.ค."),
]

# why an idea is out. Kitchen items go too: even outside a jar or bag they invite use near food.
FOOD, KIDS, LOAD = "โดนอาหารหรือปาก", "ของเด็ก", "รับแรง รอหนัง 2 มม."
DROP = {
    "S05": (FOOD, "ฝาปิดแก้ว หลอดผ่านหนังแล้วเข้าปาก"), "S07": (FOOD, "ของในครัวติดโหลเครื่องเทศ"),
    "S10": (FOOD, "ตะเกียบโดนอาหาร"), "S11": (FOOD, "เสียบขอบชามอาหาร"), "S12": (FOOD, "ผ้าเช็ดปากโดนปาก"),
    "S13": (FOOD, "ปิดถุงขนม ใช้กับอาหาร"), "S14": (FOOD, "หลอดเครื่องดื่ม"), "S15": (FOOD, "ติดแก้วเครื่องดื่ม"),
    "S16": (FOOD, "เสียบขอบแก้วที่ปากโดน"), "S17": (FOOD, "ปักเค้ก"), "S20": (FOOD, "ผูกคอขวดตรงที่เท"),
    "S25": (KIDS, "เกมที่เด็กเล่น"), "S26": (KIDS, "เกมจับคู่สำหรับเด็ก"), "S27": (KIDS, "กล่องข้าวเด็ก และโดนอาหาร"),
    "S28": (KIDS, "ขวดน้ำเด็ก และใกล้ปาก"), "S29": (KIDS, "ป้ายชื่อติดเสื้อเด็ก มีเข็ม"), "S31": (KIDS, "ชุดระบายสีสำหรับเด็ก"),
    "S32": (KIDS, "เหรียญรางวัลเด็ก และเป็นของแขวน"), "S34": (LOAD, "ปิ่นปักผมต้องรับแรง"),
}
# old products the new rules also take out (brand.py numbers)
DROP_OLD = {4: (FOOD, "ห่วงผ้าเช็ดปากหมี"), 11: (KIDS, "ชุดตัวต่อ 24 ชิ้นสำหรับเด็ก"), 14: (FOOD, "ปลอกแก้วกาแฟ อยู่ใกล้ปาก"),
            30: (KIDS, "ชุดต่อเองกล่องลูกบาศก์สำหรับเด็ก")}
RENAME = {"S30": ("ที่คั่นหนังสือพู่ริบบิ้น", "นักอ่าน ของขวัญ")}     # same product, sold to adults

# roles in the range
CORE, ADDON, GIFT, CUSTOM = "หลัก", "หยิบเพิ่ม", "ของขวัญ", "สั่งทำ"
FAMILIES = ["บ้านและโต๊ะ", "ต้นไม้และสวน", "โต๊ะทำงานและหนังสือ", "แต่งตัว", "ของขวัญ", "สั่งทำสำหรับร้านและงาน"]

def _single(i):
    return next(x for x in S50 if x[0] == i)

def item(code, family, role, wave, src, name=None, pieces=None, price=None, how=None, who=None, extras=None, pack="flat", stamp=False):
    """One assortment line. src is 'booth', 'set', 'pin02:<key>' or an S-number from single50."""
    if src.startswith("S"):
        i, _, n, pcs, h, mech, ex, pk, w, pr, load, test, st = _single(src)
        n, w = RENAME.get(src, (n, w))
        name, pieces, price, how, who, extras, pack, stamp = name or n, pieces or pcs, price or pr, how or h, who or w, extras if extras is not None else ex, pk, bool(st)
    elif src.startswith("pin02:"):
        k = src.split(":")[1]
        _, n, h, w, pr, cnt, ex, pk, test = next(x for x in pd.PIN02_IDEAS if x[0] == k)
        name, pieces, price, how, who, extras, pack = name or n, pieces or [("02", cnt)], price or pr, how or h, who or w, extras if extras is not None else ([ex] if ex else []), pk
    extras = extras or []
    pc = sum(PIECE_COST[c] * q for c, q in pieces)
    work = sum(q for _, q in pieces) * B.JOINT_COST * (1 if extras or stamp else 0)
    packaging = sum(B.PACK_ITEMS[k][2] for k in B.PACK_PROFILE[pack][1])
    cost = round(pc + work + B.PACK_COST + packaging + sum(t for _, t in extras), 2)
    return dict(code=code, family=family, role=role, wave=wave, src=src, name=name, pieces=pieces, price=price, how=how, who=who,
                extras=extras, cost=cost, margin=round((price - cost) / price, 3))

# wave 0 = selling now (booth weekend 1 and Shopee) · 1 = test 26-29 Oct, sell weekend 2 (30 Oct - 1 Nov)
# 2 = after the fair, needs extras or a stamp set · C = made to order, minimum quantity
A = [
 # ---- home and table: coasters lead the range
 item("OC-01-22", FAMILIES[0], CORE, 0, "booth", "ที่รองแก้วหมี", [("01", 1)], 59, "ที่รองแก้วทรงหัวหมี", "ทุกบ้าน"),
 item("OC-02-24", FAMILIES[0], CORE, 0, "booth", "ที่รองแก้วกังหัน", [("02", 1)], 49, "ที่รองแก้วทรงกังหัน", "ทุกบ้าน"),
 item("OC-04-27", FAMILIES[0], CORE, 0, "booth", "ที่รองแก้วสี่เหลี่ยม", [("04", 1)], 49, "ที่รองแก้วสี่เหลี่ยมมน", "ทุกบ้าน"),
 item("OC-05-28", FAMILIES[0], CORE, 0, "booth", "ที่รองแก้ววงกลม", [("05", 1)], 49, "ที่รองแก้ววงกลม", "ทุกบ้าน"),
 item("OC-MX-29", FAMILIES[0], GIFT, 0, "booth", "ชุดที่รองแก้ว 4 ลาย", [("01", 1), ("02", 1), ("04", 1), ("05", 1)], 179, "สี่ลายในชุดเดียว มัดเชือก", "ของขวัญขึ้นบ้านใหม่", [("เชือกมัดชุด", 1)]),
 item("OC-07-31", FAMILIES[0], CORE, 1, "S48", "ที่รองแก้วกากบาทวงกลม 07"),
 item("OC-MX-32", FAMILIES[0], GIFT, 1, "set", "ชุดที่รองแก้วสะสม 6 ลาย", [("01", 1), ("02", 1), ("03", 1), ("04", 1), ("05", 1), ("07", 1)], 249,
      "ทุกลายที่มีอย่างละชิ้น ไอเดียที่เจ้าของเลือกแล้ว (ใช้ 07 แทน 06)", "คนสะสม ของขวัญ", [("เชือกมัดชุด", 1)]),
 item("OC-04-33", FAMILIES[0], ADDON, 1, "S06", "แผ่นรองแจกันและโคมไฟ"),
 item("OC-05-34", FAMILIES[0], ADDON, 1, "S08", "ที่รองเทียนหอม"),
 item("OC-07-35", FAMILIES[0], ADDON, 1, "S38", "ถาดวางแหวนข้างเตียง"),
 # ---- plants and garden: the fair is บ้านและสวนแฟร์
 item("OC-03-36", FAMILIES[1], CORE, 1, "S01", "ป้ายปักกระถาง"),
 item("OC-07-37", FAMILIES[1], CORE, 1, "S02", "ป้ายเสียบขอบกระถาง"),
 item("OC-05-38", FAMILIES[1], ADDON, 1, "S04", "แผ่นรองกระถางแคคตัส"),
 item("OC-03-39", FAMILIES[1], GIFT, 2, "S03", "ชุดป้ายแปลงผัก 5 ชิ้น", how="ป้ายปักกระถาง 5 ชิ้น ปั๊มชื่อผัก ปักดินข้างต้น ไม่โดนส่วนที่กิน"),
 item("OC-05-40", FAMILIES[1], ADDON, 2, "S09", "ป้ายบอกรดน้ำแล้ว สองหน้า"),
 # ---- desk and books
 item("OC-01-01", FAMILIES[2], CORE, 0, "booth", "ที่เก็บสายชาร์จหมี", [("01", 1)], 59, "พันสายชาร์จรอบหัวหมี เหน็บปลายเข้าร่อง", "นักเรียน คนทำงาน"),
 item("OC-02-41", FAMILIES[2], CORE, 1, "pin02:B", "ที่พันสายชาร์จกังหัน"),
 item("OC-02-42", FAMILIES[2], ADDON, 1, "pin02:E", "ที่คั่นหนังสือมุมกังหัน"),
 item("OC-03-43", FAMILIES[2], ADDON, 2, "S30", "ที่คั่นหนังสือพู่ริบบิ้น"),
 item("OC-02-44", FAMILIES[2], GIFT, 2, "pin02:C", "ที่พันไหมปักผ้า ชุด 6"),
 item("OC-05-45", FAMILIES[2], ADDON, 2, "S44", "ที่เสียบปากกาคาดสมุด"),
 item("OC-04-46", FAMILIES[2], ADDON, 2, "S43", "ป้ายคั่นแฟ้มเอกสาร"),
 item("OC-MX-47", FAMILIES[2], GIFT, 2, "S49", "แม่เหล็กติดตู้เย็น 4 ลาย"),
 # ---- wear
 item("OC-05-48", FAMILIES[3], CORE, 2, "S33", "ที่รัดผ้าพันคอ"),
 item("OC-07-49", FAMILIES[3], CORE, 2, "S35", "เข็มกลัดหนังลายดอก"),
 item("OC-03-50", FAMILIES[3], ADDON, 1, "S36", "ที่เก็บกิ๊บติดผม"),
 item("OC-03-51", FAMILIES[3], ADDON, 2, "S39", "ที่ห่อสายนาฬิกาตอนเดินทาง"),
 # ---- gifts and wrapping
 item("OC-03-26", FAMILIES[4], CORE, 0, "booth", "ป้ายห้อยของขวัญ", [("03", 1)], 39, "ป้ายผูกเชือกปอติดของขวัญ", "ร้านของขวัญ", [("เชือกปอ", 2)]),
 item("OC-04-52", FAMILIES[4], ADDON, 2, "S18", "ตัวคาดริบบิ้นกล่องของขวัญ"),
 item("OC-04-53", FAMILIES[4], GIFT, 2, "S50", "การ์ดอวยพรหนังแท้"),
 item("OC-02-54", FAMILIES[4], GIFT, 2, "pin02:D", "กรอบรูปกังหัน 5.8 ซม."),
 item("OC-02-55", FAMILIES[4], GIFT, 2, "pin02:A", "ซองกังหันคาดเชือก", how="พับกลีบเข้ากลาง คาดเชือกผ้า เกี่ยวปลายเข้าร่อง ใส่ธนบัตรหรือการ์ด ชิ้นเดียว"),
 item("OC-05-56", FAMILIES[4], GIFT, 2, "S24", "ตัวคาดธนบัตรอั่งเปา"),
 item("OC-05-57", FAMILIES[4], GIFT, 2, "S47", "ที่รองแก้ววันเกิดปั๊มวันที่"),
 item("OC-03-58", FAMILIES[4], ADDON, 2, "S19", "ป้ายข้อความปักช่อดอกไม้"),
 # ---- made to order
 item("OC-05-C1", FAMILIES[5], CUSTOM, "C", "S22", "ของชำร่วยงานแต่งปั๊มชื่อ"),
 item("OC-04-C2", FAMILIES[5], CUSTOM, "C", "S23", "ของชำร่วยขึ้นบ้านใหม่"),
 item("OC-05-C3", FAMILIES[5], CUSTOM, "C", "S40", "ที่รองแก้วปั๊มโลโก้ร้าน"),
 item("OC-05-C4", FAMILIES[5], CUSTOM, "C", "S41", "ป้ายแบ่งไซซ์ราวเสื้อ ชุด 5"),
 item("OC-07-C5", FAMILIES[5], CUSTOM, "C", "S42", "ป้ายราคาเสียบขอบตะกร้า"),
 item("OC-05-C6", FAMILIES[5], CUSTOM, "C", "S21", "ป้ายเลขโต๊ะงานเลี้ยง"),
 item("OC-05-C7", FAMILIES[5], CUSTOM, "C", "S45", "ป้ายจองโต๊ะ"),
 item("OC-04-C8", FAMILIES[5], CUSTOM, "C", "S46", "ป้ายชื่อห้องปั๊มชื่อ"),
]
WAVES = {0: "ขายอยู่ตอนนี้", 1: "ลอง 26–29 ต.ค. ขายสุดสัปดาห์ที่สอง", 2: "หลังงาน ต้องซื้อของเสริมหรือบล็อกปั๊ม", "C": "สั่งทำ มีขั้นต่ำ"}
FIRST_RUN = 10        # units per new wave-1 SKU for weekend 2, a starting guess to size the leather

QUESTIONS = [
    "เด็กเล็กคืออายุเท่าไร ใช้เขียนบนป้ายว่า ไม่เหมาะสำหรับเด็กอายุต่ำกว่า … ปี",
    "ที่รองแก้วยังขายได้ไหม ผมเห็นว่าได้ เพราะโดนแค่ก้นแก้ว แต่ต้องเขียนบนป้ายว่าไม่ใช่ภาชนะใส่อาหาร",
    "DIY ที่บูธ (แต่งชิ้นหนัง วาดลาย) ให้เด็กอายุเท่าไรทำได้ และให้ล้างมือหลังทำไหม",
]

def summary():
    keep = [a for a in A]
    dropped = [(i, *DROP[i], _single(i)[2]) for i in DROP]
    use = {c: 0 for c in STOCK}
    for a in A:
        if a["wave"] == 1:
            for c, q in a["pieces"]: use[c] += q * FIRST_RUN
    return keep, dropped, use

if __name__ == "__main__":
    keep, dropped, use = summary()
    from collections import Counter
    print(len(keep), "SKUs", Counter(a["wave"] for a in keep), Counter(a["family"] for a in keep))
    print("dropped", len(dropped), "+ old", len(DROP_OLD))
    print("wave1 leather for", FIRST_RUN, "each:", use, "stock", STOCK)
    for a in keep: print(a["code"], a["wave"], a["role"], a["name"], a["price"], a["cost"], f"{a['margin']:.0%}")
