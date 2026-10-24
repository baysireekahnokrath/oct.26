"""What oct26brand.com sells and says: one place for the 7 single-piece products, their pages and the shop's links.

Follows the shared status doc "OCT. 26 สถานะล่าสุด" (22 Oct 2026): 7 SKUs, Brand Book v2 product names (pattern number
first), no 06, no joined products, no "no-sew" wording, coasters marked as not a food container. Change a price or a
line here, run `python3 website/build.py`, commit, open a PR to main; Cloudflare deploys main after the owner merges.
"""

SITE = "https://oct26brand.com"
LINE = "https://line.me/R/ti/p/@155riuqj"
LINE_ID = "@155riuqj"
IG = "https://www.instagram.com/oct.26_brand/"
IG_HANDLE = "@oct.26_brand"
FB = "https://www.facebook.com/oct26brand"
SHOPEE_NAME = "OCT.26 - Our crafted things."     # shop is open, link not given yet: the site names it for search

BOOTH = dict(fair="บ้านและสวนแฟร์ Living Festival 2026", place="อิมแพ็ค เมืองทองธานี ชาเลนเจอร์ 2–3",
             dates="23–25 ต.ค. และ 30 ต.ค.–1 พ.ย.", hours="10:00–17:00", until="2026-11-01",
             blank="ที่บูธมีชิ้นหนังเปล่า 01–05 แผ่นละ 30 บาท แต่งเอง วาดหน้า เขียนชื่อได้")

# id, seo (the search title: name + what people type), name, price (THB), size, main photo, cut-out for cards, food note, kind, pattern, page lead, uses, photos, cut-outs, note
PRODUCTS = [
    dict(id="OC-01-22", seo="01 ที่รองแก้วหนังวัวแท้ ทรงหมี แฮนด์เมด", name="01 ที่รองแก้ว", price=59, size="10.4 ซม.", img="bears", cut="01-1", food=True, kind="coaster", code="01",
         lead="ที่รองแก้วหนังวัวแท้ แพตเทิร์น 01 วางใต้แก้วบนโต๊ะทำงานหรือโต๊ะข้างเตียง",
         uses=["รองแก้วบนโต๊ะ", "รองแจกันหรือกระถางเล็ก", "วางกุญแจ นาฬิกา ของชิ้นเล็ก"], photos=["bears"], cuts=["01-1", "01-2"]),
    dict(id="OC-01-01", seo="01 ที่เก็บสายชาร์จหนังวัวแท้ ทรงหมี แฮนด์เมด", name="01 ที่เก็บสายชาร์จ", price=59, size="10.4 ซม.", img="bear01-close", cut="01-2", food=False, kind="other", code="01",
         lead="ชิ้นหนังแพตเทิร์น 01 สำหรับเก็บสายชาร์จ พันสายรอบชิ้น แล้วเหน็บปลายเข้าร่อง สายไม่พันกันในกระเป๋า",
         uses=["พันสายชาร์จหรือหูฟัง", "เก็บสายในกระเป๋าหรือลิ้นชัก", "วางบนโต๊ะเป็นที่พักสาย"], photos=["bear01-close"], cuts=["01-2"]),
    dict(id="OC-02-24", seo="02 ที่รองแก้วหนังวัวแท้ ทรงกังหัน แฮนด์เมด", name="02 ที่รองแก้ว", price=49, size="9 ซม.", img="die02", cut=None, food=True, kind="coaster", code="02",
         lead="ที่รองแก้วหนังวัวแท้ แพตเทิร์น 02 ขอบหยักสี่กลีบ",
         uses=["รองแก้วบนโต๊ะ", "รองแจกันหรือกระถางเล็ก", "วางของชิ้นเล็ก"], photos=["die02"], cuts=[],
         note="ภาพแรกเป็นบล็อกตัดของแพตเทิร์น 02 รูปถ่ายชิ้นจริงตามมาเร็ว ๆ นี้"),
    dict(id="OC-03-26", seo="03 ป้ายห้อยของขวัญหนังวัวแท้ เขียนชื่อได้", name="03 ป้ายห้อยของขวัญ", price=39, size="9 ซม.", img="clover03", cut="03-1", food=False, kind="other", code="03",
         lead="ป้ายหนังแพตเทิร์น 03 เขียนชื่อผู้รับ แล้วร้อยเชือกหรือริบบิ้นผ่านร่อง ผูกกับถุงหรือกล่องของขวัญ",
         uses=["ป้ายชื่อของขวัญ", "ป้ายห้อยถุงผ้า", "ที่คั่นหน้าหนังสือ"], photos=["clover03"], cuts=["03-1", "03-2"]),
    dict(id="OC-04-27", seo="04 ที่รองแก้วหนังวัวแท้ สี่เหลี่ยมมุมมน แฮนด์เมด", name="04 ที่รองแก้ว", price=49, size="9 ซม.", img="squares", cut="04-3", food=True, kind="coaster", code="04",
         lead="ที่รองแก้วหนังวัวแท้ แพตเทิร์น 04 สี่เหลี่ยมมุมมน",
         uses=["รองแก้วบนโต๊ะ", "รองแจกันหรือกระถางเล็ก", "วางกุญแจ นาฬิกา ของชิ้นเล็ก"], photos=["squares"], cuts=["04-1", "04-3"]),
    dict(id="OC-05-28", seo="05 ที่รองแก้วหนังวัวแท้ วงกลม แฮนด์เมด", name="05 ที่รองแก้ว", price=49, size="9 ซม.", img="circles", cut="05-3", food=True, kind="coaster", code="05",
         lead="ที่รองแก้วหนังวัวแท้ แพตเทิร์น 05 วงกลม",
         uses=["รองแก้วบนโต๊ะ", "รองแจกันหรือกระถางเล็ก", "วางกุญแจ นาฬิกา ของชิ้นเล็ก"], photos=["circles", "hand05"], cuts=["05-1", "05-3"]),
    dict(id="OC-MX-29", seo="ชุดที่รองแก้วหนังวัวแท้ 4 ชิ้น 4 แพตเทิร์น ของขวัญขึ้นบ้านใหม่", name="ชุดที่รองแก้ว 01 · 02 · 04 · 05", price=179, size="9–10.4 ซม.", img="squares", cut=None, food=True, kind="set", code="01",
         set_cuts=["01-2", "02", "04-1", "05-1"],
         lead="ชุดที่รองแก้ว 4 ชิ้น 4 แพตเทิร์น 01 · 02 · 04 · 05 คละสีหนัง เป็นของขวัญขึ้นบ้านใหม่ได้",
         uses=["ของขวัญขึ้นบ้านใหม่", "แยกแก้วของแต่ละคน", "รองแก้วบนโต๊ะรับแขก"], photos=["squares", "bears", "circles"], cuts=[]),
]

# old product pages (p/NN.html, 30 products) -> the page that sells the same thing now; everything else goes home
OLD = {1: "OC-01-01", 22: "OC-01-22", 24: "OC-02-24", 26: "OC-03-26", 27: "OC-04-27", 28: "OC-05-28", 29: "OC-MX-29"}

# what each photo shows, for image search and screen readers
ALT = {"bears": "ชิ้นหนังวัวแท้แพตเทิร์น 01 ทรงหมี 4 ชิ้น 4 สี ดำ ครีม น้ำตาลอ่อน น้ำตาลเทา",
       "bear01-close": "ชิ้นหนังวัวแท้แพตเทิร์น 01 ทรงหมี ระยะใกล้ เห็นผิวหนังจริง",
       "circles": "ที่รองแก้วหนังวัวแท้แพตเทิร์น 05 วงกลม 6 ชิ้นคละสี",
       "hand05": "ที่รองแก้วหนังวัวแท้แพตเทิร์น 05 วางบนมือ เทียบขนาดจริง",
       "clover03": "ป้ายหนังวัวแท้แพตเทิร์น 03 กากบาทแคปซูล 7 ชิ้นคละสี",
       "die02": "ภาพแพตเทิร์น 02 กังหันขอบหยักสี่กลีบ จากบล็อกตัด",
       "squares": "ที่รองแก้วหนังวัวแท้แพตเทิร์น 04 สี่เหลี่ยมมุมมน 6 ชิ้นคละสี",
       "joint07": "ชิ้นหนังวัวแท้แพตเทิร์น 07 กากบาทข้อต่อวงกลม 6 ชิ้นคละสี"}
