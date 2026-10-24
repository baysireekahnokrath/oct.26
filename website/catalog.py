"""What oct26brand.com sells and says. The products, booth notice, Shopee link and photo descriptions live in
catalog.json, which the owner edits from the product manager page (website/manage/, https://claude.ai/artifact/B9RyXagkt8KCB43kaLk3Hd);
this file loads it and keeps what does not change from there (site address, LINE, IG, FB, old addresses).

Follows the shared status doc "OCT. 26 สถานะล่าสุด" (22 Oct 2026): 7 SKUs, Brand Book v2 product names (pattern number
first), no 06, no joined products, no "no-sew" wording, coasters marked as not a food container. After a change run
`python3 website/build.py`, commit, open a PR to main; Cloudflare deploys main after the owner merges.

catalog.json, per product: id, seo (search title), name, price (THB), size, img (main photo), cut (cut-out for cards),
food (coaster note), kind, code (pattern), lead, uses, photos, cuts, optional note / set_cuts, and status:
"on" sells, "out" sold out (page stays, ordering turns into asking about the next batch), "off" hidden (no page, the
address goes home). shop: shopee (shop link, "" until given), booth (notice text, hidden after `until`).
"""
import json, os

SITE = "https://oct26brand.com"
LINE = "https://line.me/R/ti/p/@155riuqj"
LINE_ID = "@155riuqj"
IG = "https://www.instagram.com/oct.26_brand/"
IG_HANDLE = "@oct.26_brand"
FB = "https://www.facebook.com/oct26brand"
SHOPEE_NAME = "OCT.26 - Our crafted things."     # the site names the shop for search until catalog.json has its link

_D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog.json")))
PRODUCTS = _D["products"]
BOOTH = _D["shop"]["booth"]
SHOPEE = _D["shop"]["shopee"]
ALT = _D["alt"]
STATUS = ("on", "out", "off")

# words the status doc rules out in anything the site says (joins untested, chemically tanned, no food contact, 07 not 06)
BANNED = [("ไม่ต้องเย็บ", "ข้อต่อยังไม่ผ่านการทดสอบ"), ("ต่อเองได้", "ข้อต่อยังไม่ผ่านการทดสอบ"), ("ต่อชิ้นเอง", "ข้อต่อยังไม่ผ่านการทดสอบ"),
          ("ฟอกฝาด", "หนังฟอกด้วยสารเคมี"), ("ใส่อาหาร", "ห้ามโดนอาหาร"), ("ใช้กับอาหาร", "ห้ามโดนอาหาร"),
          ("สัมผัสอาหาร", "ห้ามโดนอาหาร"), ("food safe", "ห้ามโดนอาหาร"), ("food grade", "ห้ามโดนอาหาร"), ("ฟู้ดเกรด", "ห้ามโดนอาหาร"),
          ("ของเล่น", "ไม่ทำของเด็กเล็ก"), ("แพตเทิร์น 06", "ใช้ 07 แทน 06")]


def banned_in(text):
    """The ruled-out words in text; the coaster note "ไม่ใช่ภาชนะใส่อาหาร" itself is allowed."""
    t = str(text).lower().replace("ไม่ใช่ภาชนะใส่อาหาร", "")
    return [b for b in BANNED if b[0].lower() in t]


def problems(products=None, shop=None, alt=None):
    """Everything in the catalog that must not reach the site, as Thai sentences (empty list = fine)."""
    products, shop, alt = products or PRODUCTS, shop or _D["shop"], alt or ALT
    here = os.path.dirname(os.path.abspath(__file__))
    out, seen = [], set()
    for p in products:
        who = p.get("name") or p.get("id")
        if p["id"] in seen: out.append(f"{who}: รหัส {p['id']} ซ้ำ")
        seen.add(p["id"])
        if p.get("status") not in STATUS: out.append(f"{who}: สถานะต้องเป็น on, out หรือ off")
        if not str(p["name"]).strip() or len(p["name"]) > 40: out.append(f"{who}: ชื่อต้องมี 1–40 ตัวอักษร")
        if not isinstance(p["price"], int) or isinstance(p["price"], bool) or not 1 <= p["price"] <= 9999: out.append(f"{who}: ราคาเป็นบาทเต็ม 1–9,999")
        if len(p["lead"]) > 160: out.append(f"{who}: ข้อความหน้าสินค้ายาวเกิน 160 ตัวอักษร")
        if not str(p["seo"]).strip(): out.append(f"{who}: ไม่มีชื่อสำหรับค้นหา")
        if not p["photos"]: out.append(f"{who}: ต้องมีรูปอย่างน้อย 1 รูป")
        for ph in p["photos"]:
            if not os.path.exists(os.path.join(here, "assets", "img", ph + ".jpg")): out.append(f"{who}: ไม่มีไฟล์รูป {ph}.jpg")
            if ph not in alt: out.append(f"{who}: รูป {ph} ไม่มีคำบรรยาย")
        for f in ("name", "seo", "lead", "size"):
            for b in banned_in(p[f]): out.append(f'{who}: ใช้คำว่า "{b[0]}" ไม่ได้ ({b[1]})')
        for u in p["uses"]:
            for b in banned_in(u): out.append(f'{who}: ใช้คำว่า "{b[0]}" ไม่ได้ ({b[1]})')
    if not any(p.get("status") != "off" for p in products): out.append("ต้องมีสินค้าแสดงบนเว็บอย่างน้อย 1 ชิ้น")
    s = shop.get("shopee", "")
    if s and not s.startswith(("https://shopee.co.th/", "https://s.shopee.co.th/")): out.append("ลิงก์ Shopee ต้องขึ้นต้นด้วย https://shopee.co.th/")
    for k in ("fair", "place", "dates", "hours", "blank"):
        for b in banned_in(shop["booth"].get(k, "")): out.append(f'บูธ: ใช้คำว่า "{b[0]}" ไม่ได้ ({b[1]})')
    return out

# old product pages (p/NN.html, 30 products) -> the page that sells the same thing now; everything else goes home
OLD = {1: "OC-01-01", 22: "OC-01-22", 24: "OC-02-24", 26: "OC-03-26", 27: "OC-04-27", 28: "OC-05-28", 29: "OC-MX-29"}
