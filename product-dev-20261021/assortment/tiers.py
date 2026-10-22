"""The range in three tiers (owner, 22 Oct), replacing the 43-SKU list in assortment.py.

  Tier 1  bare pieces, one SKU per pattern. The customer picks how many and what to do with them.
          A new use of the same piece is an idea on the card (USES), never a new SKU.
  Tier 2  a piece plus something real in the bag: string, bamboo stick, ribbon, elastic, card, magnet, a stamp.
          One pattern each to start; more patterns only when it sells.
  Tier 3  ready-made sets, at most two.

Draft numbers stay with the same physical item (keys are the old OC codes, see draft_numbers.json), so the owner's
ticks of 22 Oct keep their real numbers. Old SKUs that were the same piece under another name are RETIRED with
where they went; a real number already given to one of them is never reused.
Status doc 22 Oct: the booth sells pieces 01-05 at 30 baht each, ideas in an A4 folder waiting for PD.
"""
import assortment as AS
B = AS.B

BOOTH_PRICE = 30                       # owner, 22 Oct: every piece, booth price only, no quantity discount
AT_BOOTH = ("01", "02", "03", "04", "05")
OLD = {a["code"]: a for a in AS.A}

# What each piece can do as it is: the A4 idea folder and the cards. Single piece, nothing joined,
# nothing hung or pulled (16 Oct, leather 1.0-1.2 mm), nothing touching food or the mouth, nothing for small children.
USES = {
    "01": [("ที่รองแก้ว", "วางแก้วน้ำหรือแก้วกาแฟ ไม่ใช่ภาชนะใส่อาหาร"),
           ("ที่เก็บสายชาร์จ", "พันสายรอบหัวหมี เหน็บปลายสายเข้าร่อง"),
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
    "07": [("ที่รองแก้ว", "วางแก้วน้ำหรือแก้วกาแฟ ไม่ใช่ภาชนะใส่อาหาร"),
           ("ถาดวางแหวนข้างเตียง", "วางแหวน ต่างหู นาฬิกาก่อนนอน"),
           ("ป้ายเสียบขอบกระถาง", "ดันร่องเปิดข้างชิ้นสวมขอบกระถาง เขียนชื่อต้นไม้"),
           ("ป้ายราคาเสียบขอบตะกร้า", "สำหรับร้าน สวมขอบตะกร้า เขียนราคา")],
}
# ideas in the marketing A4 folder (branch claude/vigilant-faraday-00e92g, print-20261022) that break a rule
FOLDER_FIX = [("01 เขียนชื่อ ห้อยกระเป๋า", "ของห้อยถูกดึงทุกวัน ต้องใช้หนัง 2 มม. (มติ 16 ต.ค.) ใช้ป้ายชื่อบนกล่องของขวัญแทน")]


def _t(key, tier, group, name, pieces, price, how, extras=(), pack="flat", merged=(), note="", stamp=False):
    """One line in the range; cost from the sheet's piece cost (assortment.PIECE_COST) plus extras and packing."""
    pc = sum(AS.PIECE_COST[c] * q for c, q in pieces)
    if not pieces:
        cost = B.JOINT_COST * 4                               # a service: labour only, stamp set not included
    elif tier == 1:
        cost = pc + B.PACK_COST                               # loose at the booth: no sleeve, no tag
    else:
        work = sum(q for _, q in pieces) * B.JOINT_COST if (extras or stamp) else 0
        packaging = sum(B.PACK_ITEMS[k][2] for k in B.PACK_PROFILE[pack][1])
        cost = pc + work + B.PACK_COST + packaging + sum(t for _, t in extras)
    cost = round(cost, 2)
    return dict(key=key, tier=tier, group=group, name=name, pieces=list(pieces), extras=list(extras), price=price,
                how=how, cost=cost, margin=round((price - cost) / price, 3), merged=list(merged), note=note)


def _from_old(key, group, name, note=""):
    """A tier-2 line that was already in the 43-SKU list: same piece, same extras, same draft number."""
    a = OLD[key]
    return _t(key, 2, group, name, a["pieces"], a["price"], a["how"], a["extras"], note=note)


SHOPEE = "30 บาทเป็นราคาบูธอย่างเดียว ไม่ลดตามจำนวน · Shopee ขายเป็นที่รองแก้ว 49–59 บาท"
T1 = [
    _t("OC-01-22", 1, "t1", "01 หัวหมี · ชิ้นหนัง", [("01", 1)], BOOTH_PRICE, "ชิ้นหนังหัวหมี 10.4 ซม.", merged=["OC-01-01"], note=SHOPEE),
    _t("OC-02-24", 1, "t1", "02 กังหัน · ชิ้นหนัง", [("02", 1)], BOOTH_PRICE, "ชิ้นหนังกังหัน 9 ซม.", note=SHOPEE),
    _t("P-03", 1, "t1", "03 กากบาทแคปซูล · ชิ้นหนัง", [("03", 1)], BOOTH_PRICE, "ชิ้นหนังกากบาทแคปซูล 9 ซม."),
    _t("OC-04-27", 1, "t1", "04 สี่เหลี่ยมมน · ชิ้นหนัง", [("04", 1)], BOOTH_PRICE, "ชิ้นหนังสี่เหลี่ยมมน 9 ซม.", note=SHOPEE),
    _t("OC-05-28", 1, "t1", "05 วงกลม · ชิ้นหนัง", [("05", 1)], BOOTH_PRICE, "ชิ้นหนังวงกลม 9 ซม.", note=SHOPEE),
    _t("OC-07-31", 1, "t1", "07 กากบาทข้อต่อวงกลม · ชิ้นหนัง", [("07", 1)], BOOTH_PRICE, "ชิ้นหนังกากบาทข้อต่อวงกลม 9 ซม.",
       note="มี 200 ชิ้น บูธ 23 ต.ค. ยังขายแค่ 01–05"),
]
T2 = [
    _from_old("OC-03-26", "t2", "03 ป้ายห้อยของขวัญ", note="ขายอยู่ใน Shopee"),
    _from_old("OC-03-36", "t2", "03 ป้ายปักกระถาง", note="ปักช่อดอกไม้ก็ได้ เข้ากับงานบ้านและสวน"),
    _from_old("OC-03-43", "t2", "03 ที่คั่นหนังสือพู่ริบบิ้น"),
    _from_old("OC-05-45", "t2", "05 ที่เสียบปากกาคาดสมุด"),
    _from_old("OC-02-55", "t2", "02 ซองคาดเชือก", note="แบบ 02 ชิ้นเดียว รอทดสอบ"),
    _from_old("OC-04-53", "t2", "04 การ์ดอวยพรหนัง"),
]
T2_RESERVE = [
    _from_old("OC-02-54", "t2r", "02 กรอบรูป 5.8 ซม.", note="แบบ 02 ชิ้นเดียว รอทดสอบ"),
    _from_old("OC-04-52", "t2r", "04 ตัวคาดริบบิ้นกล่องของขวัญ"),
    _t("P2-MAG", 2, "t2r", "05 แม่เหล็กติดตู้เย็น", [("05", 1)], 39, "แปะแผ่นแม่เหล็กมีกาวหลังชิ้น ติดโน้ตหรือรูปบนตู้เย็น",
       [("แผ่นแม่เหล็กมีกาว", 3)], note="แทนชุดแม่เหล็ก 4 ลาย ลายอื่นเพิ่มเมื่อขายได้"),
    _from_old("OC-07-49", "t2r", "07 เข็มกลัดหนัง"),
    _t("P2-STAMP", 2, "t2r", "ปั๊มชื่อหรือวันที่ (เพิ่มกับชิ้นไหนก็ได้)", [], 20, "ปั๊มตัวอักษรลงชิ้นหนัง คิดเพิ่มต่อชิ้น",
       stamp=True, note="ต้องซื้อบล็อกปั๊มตัวอักษรก่อน · งานสั่งทำ (ของชำร่วย ป้ายร้าน) คือชิ้นเปล่าตามจำนวน + ปั๊ม"),
]
T3 = [
    dict(_t("OC-MX-29", 3, "t3", "ชุดที่รองแก้ว 01 · 02 · 04 · 05", OLD["OC-MX-29"]["pieces"], OLD["OC-MX-29"]["price"],
            "สี่ลายในชุดเดียว มัดเชือก ใส่การ์ด", OLD["OC-MX-29"]["extras"]), note="ขายอยู่ใน Shopee"),
    _t("OC-MX-32", 3, "t3", "ชุดสะสม 6 ลาย 01–07", OLD["OC-MX-32"]["pieces"], OLD["OC-MX-32"]["price"],
       "ทุกลายอย่างละชิ้น มัดเชือก ใส่การ์ด", OLD["OC-MX-32"]["extras"], note="เจ้าของเลือกไอเดียนี้แล้ว"),
]
TIERS = [("t1", "ชั้น 1 · ชิ้นเปล่า", T1), ("t2", "ชั้น 2 · ชิ้น + ของเพิ่ม เริ่มก่อน", T2),
         ("t2r", "ชั้น 2 · สำรอง เพิ่มเมื่อมีคนถาม", T2_RESERVE), ("t3", "ชั้น 3 · ชุดที่จัดไว้แล้ว", T3)]
ALL = T1 + T2 + T2_RESERVE + T3

# where each line stands today (stages of ../pd.py); the PD page keeps changes in its database
STAGE = {"OC-01-22": "selling", "OC-02-24": "selling", "P-03": "selling", "OC-04-27": "selling", "OC-05-28": "selling",
         "OC-07-31": "ready", "OC-03-26": "selling", "OC-MX-29": "selling", "OC-MX-32": "ready"}
for _a in ALL:
    _a["stage"] = STAGE.get(_a["key"], "hold" if _a["group"] == "t2r" else "idea")

# the first board (brand.py, 30 products) in the new structure: in the range, an idea still to try,
# waiting for a joint that passes, or out under the 22 Oct rules (assortment.DROP_OLD)
BOARD_IN_RANGE = {1: "OC-01-22", 2: "OC-01-22", 22: "OC-01-22", 24: "OC-02-24", 26: "OC-03-26", 27: "OC-04-27",
                  28: "OC-05-28", 29: "OC-MX-29"}
BOARD_TRY = {25: "ชิ้นเดียว + ไม้เสียบ ต้องลองก่อนว่าหมุนได้จริง ถ้าได้เข้าชั้น 2"}
BOARD_NOTE = {2: "เป็นไอเดียการใช้ของชิ้น 01"}

def board_place(p):
    """'range' | 'try' | 'joint' | 'out' for one brand.py product."""
    n = p["n"]
    if n in AS.DROP_OLD: return "out"
    if n in BOARD_IN_RANGE: return "range"
    if n in BOARD_TRY: return "try"
    return "joint" if p["joints"] else "try"

# every old SKU that is not a line above, and where it went
_USE = "ไอเดียการใช้ของชิ้น {}"
RETIRED = {
    "OC-01-01": ("รวมกับ 01 ชิ้นหนัง (ชิ้นเดียวกัน)", "OC-01-22"),
    "OC-04-33": (_USE.format("04"), "OC-04-27"), "OC-05-34": (_USE.format("05"), "OC-05-28"),
    "OC-07-35": (_USE.format("07"), "OC-07-31"), "OC-07-37": (_USE.format("07"), "OC-07-31"),
    "OC-05-38": (_USE.format("05"), "OC-05-28"), "OC-02-41": (_USE.format("02"), "OC-02-24"),
    "OC-02-42": (_USE.format("02"), "OC-02-24"), "OC-02-44": ("ซื้อชิ้น 02 ตามจำนวน", "OC-02-24"),
    "OC-04-46": (_USE.format("04"), "OC-04-27"), "OC-05-48": (_USE.format("05"), "OC-05-28"),
    "OC-03-50": (_USE.format("03"), "P-03"), "OC-03-51": (_USE.format("03"), "P-03"),
    "OC-05-56": (_USE.format("05"), "OC-05-28"),
    "OC-03-39": ("ซื้อ 03 ป้ายปักกระถาง ตามจำนวน", "OC-03-36"),
    "OC-05-40": ("รวมกับ ป้ายปักกระถาง (ของเพิ่มเหมือนกัน)", "OC-03-36"),
    "OC-03-58": ("รวมกับ ป้ายปักกระถาง (ของเพิ่มเหมือนกัน)", "OC-03-36"),
    "OC-MX-47": ("เปลี่ยนเป็นแม่เหล็กทีละชิ้น", "P2-MAG"),
    "OC-05-57": ("ชิ้นเปล่า + ปั๊ม", "P2-STAMP"),
    **{k: ("สั่งทำ = ชิ้นเปล่าตามจำนวน + ปั๊ม", "P2-STAMP") for k in
       ("OC-05-C1", "OC-04-C2", "OC-05-C3", "OC-05-C7", "OC-04-C8")},
    **{k: ("สั่งทำ = ชิ้นเปล่าตามจำนวน", t) for k, t in (("OC-05-C4", "OC-05-28"), ("OC-07-C5", "OC-07-31"), ("OC-05-C6", "OC-05-28"))},
}

QUESTIONS = [
    "Shopee ตอนนี้มี 2 หน้าเป็นชิ้น 01 เดียวกัน (ที่รองแก้วหมี กับ ที่เก็บสายชาร์จหมี) ควรรวมเป็นหน้าเดียว แล้วเขียนการใช้ทั้งสองแบบ",
]

assert {a["key"] for a in ALL}.isdisjoint(RETIRED), "a key is both kept and retired"
assert set(OLD) <= {a["key"] for a in ALL} | set(RETIRED), set(OLD) - {a["key"] for a in ALL} - set(RETIRED)

if __name__ == "__main__":
    for g, label, its in TIERS:
        print(label)
        for a in its: print(f"  {a['key']:9} {a['name']:40} {a['price']:>4} ทุน {a['cost']:6.2f} {a['margin']:.0%}  {a['note']}")
    print(len(T1) + len(T2) + len(T3), "SKUs to start,", len(T2_RESERVE), "reserve,", len(RETIRED), "old retired")
