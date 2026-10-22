"""OCT. 26 palette, brand book v2 (22 Oct 2026): every colour comes from something in nature.

Base colours carry the brand; the five family colours are hidden details (tag backs, leather edges, a thin band).
"""
BASE = [
    ("cotton",   "ขาวฝ้าย",       "#F4F0E8", "ฝ้ายดิบที่ยังไม่ฟอก", "พื้นหลัก กระดาษ ป้าย", 60),
    ("charcoal", "ดำถ่าน",        "#2A2725", "ถ่านไม้",             "ตัวหนังสือ โลโก้", 20),
    ("hide",     "สีหนังแท้",      "#B07A4A", "หนังวัวฟอกฝาด",       "ภาพสินค้าและชิ้นหนัง", 15),
    ("teak",     "น้ำตาลไม้สัก",    "#8B5E3C", "เนื้อไม้สักเก่า",       "เส้น กรอบ งานพิมพ์สีเดียวบนคราฟต์", 0),
    ("stone",    "เทาหิน",         "#8C8A85", "หินแกรนิต",           "ข้อความรอง เส้นแบ่ง", 0),
]
FAMILY = [  # order on every band: dad, mom, Beiya, Beana, Bene
    ("dad",   "พ่อเบ",          "MAR. 23", "แดงดินลูกรัง",     "#A9442B", "ดินแดงตามทางในชนบท"),
    ("mom",   "แม่ (คุณบิ๊ง)",    "OCT. 26", "เขียวใบตอง",      "#5E7A3A", "ใบตองที่ใช้ห่อขนมและทำบายศรี"),
    ("beiya", "Beiya",          "DEC. 07", "เหลืองทานตะวัน",   "#E9A825", "ดอกทานตะวันกลางทุ่ง"),
    ("beana", "Beana",          "OCT. 09", "ม่วงดอกอินทนิล",   "#B9A3D6", "ดอกอินทนิลต้นไม้ไทยริมทาง"),
    ("bene",  "Bene",           "SEP. 01", "น้ำเงินคราม",      "#2E4A7D", "ทะเลลึกและผ้าย้อมคราม"),
]
C = {k: h for k, _, h, *_ in BASE}
C.update({k: h for k, _, _, _, h, _ in FAMILY})
C["leaf_on_dark"] = "#9DB777"   # mom's green, lightened so the dot still reads on charcoal
BAND = [h for *_, h, _ in FAMILY]
