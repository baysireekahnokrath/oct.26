"""Facebook kit for the first booth: what is left to set up on the Page, Messenger replies, and the posts from
22 Oct to 2 Nov with captions and pictures.

Follows the status doc "OCT. 26 สถานะล่าสุด" (21 Oct): only the 7 single-piece SKUs, no 06, no joining or no-sew
claim; the booth DIY is decorating a single piece. Profile picture, cover and Intro are done (owner, 21 Oct).
python3 facebook-20261021/cards.py && node brand-20261014/tools/render.mjs facebook-20261021/cards/jobs.json
python3 facebook-20261021/build.py   -> site/index.html (+ card and banner PNGs) and copy.txt for the Google Doc
"""
import html, importlib.util, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "brand-20261014"))
sys.path.insert(0, HERE)
import brand as B
from cards import SKU, SALE


def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


S = _load("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
SB = _load("social_build", os.path.join(REPO, "social-20261021", "build.py"))
E = html.escape
P = {p["n"]: p for p in SALE}
SHOP = f"Shopee ร้าน {B.SHOP_NAME}"
BOOTH = f"บูธ OCT. 26 โซน{SB.ZONE}\n{SB.WHERE}"
TAGS = "#OCT26 #ourcraftedthings #หนังแท้ #ของขวัญ #งานแฮนด์เมด #หนูทดลองKidsMarket #บ้านและสวนแฟร์2026"
COLL = {"soi2": "#SOI02", "love": "#ห้าหมี #FiveBears"}
INTRO = "ของใช้จากเศษหนังวัวแท้ ทำกันเองทั้งบ้าน พ่อ แม่ และลูกสามคน · SOI. 02 · ห้าหมี FIVE BEARS"
assert len(INTRO) <= 101, len(INTRO)          # Facebook Intro limit


def product_post(p, extra=""):
    return (f"{p['hook']}\n\n"
            f"{p['name']} · {p['price']} บาท\n"
            f"หนังวัวแท้ {p['pieces_txt']} · ขนาด {p['size']}\n\n"
            f"วิธีใช้\n{B._steps(p)}\n\n"
            f"{extra}มีขายที่{BOOTH}\n\nสั่งออนไลน์: {SHOP}\n\n{TAGS} {COLL[p['coll']]}")


def coaster_pair():
    a, b = P[27], P[28]
    return ("ที่รองแก้วหนังวัวแท้ สองทรง เลือกได้ตามโต๊ะ\n\n"
            f"{a['name']} · {a['price']} บาท · ขนาด {a['size']}\n{b['name']} · {b['price']} บาท · ขนาด {b['size']}\n"
            "หนังแต่ละชิ้นสีและลายไม่ซ้ำกัน หยิบออกจากถุงแล้ววางแก้วได้เลย\n\n"
            f"สัปดาห์ที่สองเริ่มวันนี้ มีขายที่{BOOTH}\n\nสั่งออนไลน์: {SHOP}\n\n{TAGS} #SOI02")


LAUNCH = SB.COPY[0][2]
REELS = dict(SB.VIDEO_COPY)["Facebook / Instagram Reels"]
BIRTHDAY = (f"26 ตุลาคม\n\n{B.STORY_LONG[0][1]}\n\n"
            "ขอบคุณทุกคนที่แวะมาที่บูธเมื่อสุดสัปดาห์ที่ผ่านมา สุดสัปดาห์นี้ลูก ๆ จะกลับไปอีกรอบ "
            f"{SB.WEEKENDS[1]} โซน{SB.ZONE}\n\n#OCT26 #ourcraftedthings")
DAY1 = (f"วันนี้วันแรก เจอกันที่{BOOTH}\n\n"
        "มาลองแต่งชิ้นหนังแท้ของตัวเอง เขียนชื่อหรือวาดลาย แล้วรับกลับบ้าน ลูก ๆ รอสอนอยู่\n\n"
        f"{TAGS}")
LAST = (f"วันสุดท้ายแล้ว ใครยังไม่ได้แวะ วันนี้ถึง 17:00\n\n{BOOTH}\n\n"
        f"หลังงานยังสั่งได้ที่ {SHOP}\n\n{TAGS}")
THANKS = ("ขอบคุณทุกคนที่แวะมาที่บูธ OCT. 26 ทั้งสองสุดสัปดาห์\n\n"
          "งานแรกของบ้านเรา ลูก ๆ ได้ขายเอง ทอนเงินเอง และได้เจอคนใจดีเยอะมาก\n\n"
          f"ของที่เหลือสั่งได้ที่ {SHOP}\n\n#OCT26 #ourcraftedthings")

# (date, time, what, picture, caption) · times are suggestions for a family audience
POSTS = [
    ("พฤ. 22 ต.ค.", "19:00", "โพสต์เชิญมาบูธ แล้วปักหมุดไว้บนสุด", "banner", LAUNCH),
    ("ศ. 23 ต.ค.", "08:30", "วันแรก", "รูปบูธจริงตอนจัดเสร็จ", DAY1),
    ("ศ. 23 ต.ค.", "19:00", "Reels คลิปลูก ๆ แต่งชิ้นหนัง", "คลิปแนวตั้ง 15 วินาที", REELS),
    ("ส. 24 ต.ค.", "12:00", "สินค้า: ชุดที่รองแก้ว 4 ลาย", "OC-MX-29", product_post(P[29])),
    ("อา. 25 ต.ค.", "12:00", "สินค้า: ที่เก็บสายชาร์จหมี", "OC-01-01", product_post(P[1])),
    ("จ. 26 ต.ค.", "19:00", "วันเกิดแบรนด์", "รูปครอบครัวที่บูธ (ไม่เห็นหน้าลูกก็ได้)", BIRTHDAY),
    ("อ. 27 ต.ค.", "19:00", "สินค้า: ที่รองแก้วหมี", "OC-01-22", product_post(P[22])),
    ("พ. 28 ต.ค.", "19:00", "สินค้า: ที่รองแก้วกังหัน", "OC-02-24", product_post(P[24])),
    ("พฤ. 29 ต.ค.", "19:00", "สินค้า: ป้ายห้อยของขวัญ", "OC-03-26", product_post(P[26])),
    ("ศ. 30 ต.ค.", "08:30", "สัปดาห์ที่สอง + ที่รองแก้วสองทรง", "OC-04-27 + OC-05-28", coaster_pair()),
    ("อา. 1 พ.ย.", "09:00", "วันสุดท้าย", "รูปบูธหรือชิ้นงานที่ลูกค้าแต่ง", LAST),
    ("จ. 2 พ.ย.", "19:00", "ขอบคุณ", "รูปรวมสองสุดสัปดาห์", THANKS),
]

SETUP = [
    ("ชื่อผู้ใช้เพจ", f"เสร็จแล้ว 21 ต.ค.: {B.SOCIAL['facebook']}"),
    ("ปุ่มบนเพจ", "ตอนนี้ใช้ปุ่ม ส่งข้อความ ได้ลิงก์ร้าน Shopee แล้วค่อยเปลี่ยนเป็น ซื้อเลย ลิงก์ไปร้าน"),
    ("เชื่อม Instagram", f"Meta Business Suite → การตั้งค่า → บัญชี Instagram → เชื่อม @{B.BRAND['handle']} "
     "จะตอบข้อความ FB กับ IG ได้ในที่เดียว และโพสต์พร้อมกันได้"),
    ("เช็ก Intro", f"ข้อความที่แนะนำ ({len(INTRO)} ตัวอักษร): {INTRO} · ถ้าของเดิมมีคำว่า ไม่ต้องเย็บ หรือ ต่อเอง ให้เปลี่ยน"),
    ("ข้อมูลติดต่อ", f"เว็บไซต์ https://{B.SOCIAL['web']} · Instagram · YouTube · ไม่ต้องใส่ที่อยู่บ้าน"),
]
GREETING = "สวัสดีครับ OCT. 26 ของใช้จากเศษหนังวัวแท้ ทำกันเองทั้งบ้าน ทักมาถามได้เลยครับ"
INSTANT = (f"ขอบคุณที่ทักมาครับ ช่วงนี้เราอาจอยู่ที่บูธ จะรีบตอบนะครับ\n"
           f"ระหว่างนี้ดูสินค้าและสั่งได้ที่ {SHOP}")
FAQ = [
    ("บูธอยู่ที่ไหน วันไหน", BOOTH),
    ("สั่งออนไลน์ได้ไหม", f"ได้ครับ ที่ {SHOP} มีครบทั้ง 7 แบบ"),
    ("มีอะไรบ้าง ราคาเท่าไร", "\n".join(f"{p['name']} {p['price']} บาท" for p in SALE)),
    ("ทำจากอะไร", "เศษหนังวัวแท้ หนา 1.0–1.2 มม. ตัดด้วยบล็อกแล้วทำกันเองทั้งบ้าน แต่ละชิ้นสีและลายไม่ซ้ำกัน"),
]
CHECK = [
    "ราคา 7 แบบยังเป็นราคาร่างตามหน้าสถานะ ยืนยันก่อนลงโพสต์สินค้าวันที่ 24 ต.ค.",
    "DIY ที่บูธเขียนไว้ว่า เลือกชิ้นหนัง เขียนชื่อหรือวาดลาย แล้วรับกลับบ้าน ถ้ากิจกรรมจริงต่างจากนี้ บอกได้ จะแก้ข้อความให้",
    "รูปลูก: ถ่ายมือเป็นหลัก ไม่บอกชื่อจริง ไม่ใส่ชุดหรือป้ายโรงเรียน และถามลูกก่อนโพสต์",
    "แท็กเพจผู้จัดในโพสต์เชิญและโพสต์วันแรก เขาอาจแชร์ต่อ",
    "การ์ดสินค้าในชุดนี้ใช้แทนโปสเตอร์ How-to เดิม เพราะโปสเตอร์เดิมเขียนว่า ไม่ต้องเย็บ ห้ามใช้ตามหน้าสถานะ "
    "รวมถึงภาพปกใน Shopee ที่ดึงโปสเตอร์เดิมไป ควรเปลี่ยนเป็นการ์ดชุดนี้ใน Seller Centre",
]


def picture(pic):
    if pic == "banner":
        return '<img src="launch-post-1080x1350.png" alt="แบนเนอร์เชิญมาบูธ" loading="lazy">'
    codes = [c for c in pic.split(" + ") if c in SKU.values()]
    if codes:
        return "".join(f'<img src="{c}.png" alt="การ์ดสินค้า {c}" loading="lazy">' for c in codes)
    return f'<div class="shot">{E(pic)}</div>'


def page():
    setup = "".join(f"<li><b>{E(t)}</b><br>{E(d)}</li>" for t, d in SETUP)
    faq = "".join(S.copybox(f"q{i}", a, q) for i, (q, a) in enumerate(FAQ))
    posts = "".join(
        f'<article class="card post"><div class="pic">{picture(pic)}</div><div class="body">'
        f'<div class="when"><span class="chip">{E(d)} · {E(t)}</span><h3>{E(what)}</h3></div>'
        f'{S.copybox(f"p{i}", cap, "แคปชัน")}</div></article>'
        for i, (d, t, what, pic, cap) in enumerate(POSTS))
    cards = "".join(f'<figure><img src="{SKU[p["n"]]}.png" alt="{E(p["name"])}" loading="lazy">'
                    f'<figcaption class="cap">{SKU[p["n"]]} · {E(p["name"])} · {p["price"]} บาท</figcaption></figure>'
                    for p in SALE)
    check = "".join(f"<li>{E(c)}</li>" for c in CHECK)
    return f"""{S.head("OCT. 26 Facebook")}
<style>
.post{{display:grid;grid-template-columns:minmax(0,233px) minmax(0,1fr);gap:var(--s4);align-items:start}}
.post .pic{{display:flex;flex-direction:column;gap:var(--s2)}}.post .pic img{{border-radius:var(--s3);border:1px solid var(--line)}}
.post .body{{display:flex;flex-direction:column;gap:var(--s3);min-width:0}}.post .when{{display:flex;flex-direction:column;align-items:flex-start;gap:var(--s2)}}
.shot{{aspect-ratio:4/5;border:2px dashed var(--line);border-radius:var(--s3);display:flex;align-items:center;justify-content:center;
  text-align:center;padding:var(--s3);color:var(--muted);font-size:14px}}
.cards{{display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fill,minmax(144px,1fr))}}.cards figure{{margin:0;display:flex;flex-direction:column;gap:var(--s2);min-width:0}}
.cards img{{border-radius:var(--s3);border:1px solid var(--line)}}
@media (max-width:600px){{.post{{grid-template-columns:1fr}}.post .pic{{max-width:233px}}}}
</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · 21 ต.ค. 2569</span><h1>Facebook OCT. 26</h1>
<p class="lead">สิ่งที่เหลือบนเพจ ข้อความตอบอัตโนมัติ และโพสต์ {len(POSTS)} โพสต์ตั้งแต่ 22 ต.ค. ถึง 2 พ.ย. ทำตามหน้าสถานะล่าสุด:
ขายเฉพาะ 7 แบบชิ้นเดียว ไม่มี 06 และไม่พูดว่าต่อเองหรือไม่ต้องเย็บ</p></header>
<section><span class="eyebrow">ตั้งค่าเพจ</span><h2>ที่ยังเหลือ</h2>
<p class="cap">รูปโปรไฟล์ ภาพปก และ Intro ทำแล้ว</p><div class="card"><ol>{setup}</ol></div></section>
<section><span class="eyebrow">Messenger</span><h2>ข้อความตอบอัตโนมัติ</h2>
<p class="cap">Meta Business Suite → กล่องข้อความ → การทำงานอัตโนมัติ</p>
<div class="card">{S.copybox("g", GREETING, "ข้อความทักทาย")}{S.copybox("i", INSTANT, "ตอบกลับทันที")}</div>
<h3>คำถามที่พบบ่อย 4 ข้อ</h3><div class="card">{faq}</div></section>
<section><span class="eyebrow">22 ต.ค.–2 พ.ย.</span><h2>แผนโพสต์</h2>
<p class="cap">ตั้งเวลาโพสต์ล่วงหน้าได้ใน Meta Business Suite → แพลนเนอร์ · ช่องเส้นประคือรูปที่ต้องถ่ายเอง</p>{posts}</section>
<section><span class="eyebrow">รูป</span><h2>การ์ดสินค้า 7 แบบ</h2><p class="cap">1080 × 1350 · กดค้างที่รูปเพื่อบันทึกลงมือถือ</p>
<div class="cards">{cards}</div></section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>{check}</ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">facebook-20261021/cards/*.png</td><td>การ์ดสินค้า 7 แบบ</td></tr>
<tr><td class="mono" style="white-space:nowrap">social-20261021/banners/*.png</td><td>แบนเนอร์เชิญ (แก้แล้ว ไม่มีชิ้น 06)</td></tr>
<tr><td class="mono" style="white-space:nowrap">facebook-20261021/build.py</td><td>ข้อความทั้งหมดในหน้านี้ แก้แล้วรันใหม่</td></tr>
<tr><td>Google Doc "OCT. 26 Facebook โพสต์และตั้งค่าเพจ"</td><td>ข้อความชุดเดียวกัน ในโฟลเดอร์ OCT. 26 ไฟล์งาน</td></tr>
</tbody></table></div></section>
</div>{S.COPY_JS}"""


def text():
    out = ["OCT. 26 Facebook โพสต์และตั้งค่าเพจ (21 ต.ค. 2569)", "",
           "ตั้งค่าเพจที่ยังเหลือ"] + [f"- {t}: {d}" for t, d in SETUP]
    out += ["", "Messenger ข้อความทักทาย", GREETING, "", "Messenger ตอบกลับทันที", INSTANT, "", "คำถามที่พบบ่อย"]
    for q, a in FAQ:
        out += [f"ถาม: {q}", f"ตอบ: {a}", ""]
    out += ["แผนโพสต์", ""]
    for d, t, what, pic, cap in POSTS:
        out += [f"{d} {t} · {what}", f"รูป: {'แบนเนอร์เชิญ 1080 × 1350' if pic == 'banner' else pic}", "", cap, "", "-----", ""]
    out += ["ต้องเช็ก"] + [f"- {c}" for c in CHECK]
    return "\n".join(out)


if __name__ == "__main__":
    site = os.path.join(HERE, "site"); os.makedirs(site, exist_ok=True)
    for p in SALE:
        shutil.copyfile(os.path.join(HERE, "cards", SKU[p["n"]] + ".png"), os.path.join(site, SKU[p["n"]] + ".png"))
    shutil.copyfile(os.path.join(REPO, "social-20261021", "banners", "launch-post-1080x1350.png"),
                    os.path.join(site, "launch-post-1080x1350.png"))
    for word in ("เย็บ", "กาว", "ต่อเอง"):
        assert all(word not in cap for *_, cap in POSTS), word
    open(os.path.join(site, "index.html"), "w").write(page())
    open(os.path.join(HERE, "copy.txt"), "w").write(text())
    print("wrote site/index.html and copy.txt,", len(POSTS), "posts")
