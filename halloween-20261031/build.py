"""Halloween, Sat 31 Oct (owner, 24 Oct): four IG/FB posts, product ideas from the pieces, and ten activities scored on
revenue, after-value, cash cost and opportunity cost.

Brand Book v2, quiet: charcoal night, the real die-cut pieces (pattern-intro-20261022/plan-web, owner's photos), cotton
text, family yellow only as a small light. No faces, no bear face, no joining, nothing that touches food, nothing for
small children, no discount. 26 Oct is the brand's birthday, so Halloween posts start on the 27th.
python3 halloween-20261031/build.py && node halloween-20261031/render.mjs -> posts/*.png, site/
"""
import html, importlib.util, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "print-20261022", "assets"))
from palette import C, BAND

sp = importlib.util.spec_from_file_location("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
E = html.escape
FONTS = "file://" + os.path.join(REPO, "brand-20261014", "fonts")
CUT = "file://" + os.path.join(HERE, "cut")
NIGHT, COTTON, MUTED, MOON = C["charcoal"], C["cotton"], "#A8A29A", C["beiya"]
TAGS = "#OCT26 #ourcraftedthings #หนังแท้ #halloween #ฮาโลวีน"
WEB = "oct26brand.com"

POSTS = [  # (file, date, title on the page, caption)
    ("01-colours", "อ. 27 ต.ค.", "ดำ ส้ม ขาว",
     "ดำ ส้ม ขาว\nสีฮาโลวีนมีอยู่แล้วในกองเศษหนังของเรา\nแต่ละแผ่นมาจากคนละผืน อยากได้โทนไหน ทักบอกทาง LINE ได้\n\n"
     f"ดูชิ้นหนังทั้งหมด {WEB}\nLINE @155riuqj\n\n{TAGS}"),
    ("02-treat-tag", "พ. 28 ต.ค.", "03 ป้ายถุงขนม",
     "03 ป้ายห้อยของขวัญ\nคืนวันที่ 31 ใช้เป็นป้ายถุงขนม\nเขียนชื่อด้วยปากกาสีขาว ร้อยเชือกผ่านร่อง ผูกที่ปากถุง\n"
     "ขนมหมดแล้ว ป้ายยังเก็บไว้ใช้ปีหน้าได้\n\nผูกไว้ด้านนอกถุง ไม่ใส่ปนกับขนม\n\n"
     f"{WEB}\n\n{TAGS}"),
    ("03-candle", "พฤ. 29 ต.ค.", "05 รองโหลเทียน",
     "05 ที่รองแก้ว\nคืนฮาโลวีน ลองรองใต้โหลเทียน\nกันคราบเทียนและรอยบนโต๊ะไม้\n\n"
     "ใช้เทียนในโหลแก้วหรือเทียน LED ไม่วางเทียนเปลือยบนหนัง\n\n"
     f"{WEB}\n\n{TAGS}"),
    ("04-night", "ส. 31 ต.ค.", "31.10",
     "31.10\nคืนนี้จะออกไปเดินหรืออยู่บ้าน ก็ขอให้สนุก\n\nOCT. 26 · our crafted things.\n\n" + TAGS),
]
for *_, cap in POSTS:
    for word in ("ไม่ต้องเย็บ", "ต่อเอง", "ลดราคา", "หัวใจ", "06", "หน้าหมี"):
        assert word not in cap, word

# ---------------------------------------------------------------- post images, 1080 x 1350
POST_CSS = f"""
@font-face{{font-family:Anuphan;font-weight:500;src:url({FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Jost;font-weight:400;src:url({FONTS}/alt/Jost-Regular.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url({FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Plex;font-weight:400;src:url({FONTS}/IBMPlexSansThai-Regular.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;position:relative;overflow:hidden;background:{NIGHT};color:{COTTON};font-family:Plex}}
h1{{font-family:Anuphan,Jost;font-weight:500;line-height:1.15}}
.j{{font-family:Jost;font-weight:400}}.mu{{color:{MUTED}}}
.pc{{position:absolute;filter:drop-shadow(0 18px 26px rgba(0,0,0,.45))}}
.ft{{position:absolute;left:80px;right:80px;bottom:70px;display:flex;justify-content:space-between;align-items:center}}
"""


def logo(px):
    s = open(os.path.join(HERE, "cut", "square-light.svg")).read()
    s = re.sub(r'(<svg[^>]*?) width="[^"]*" height="[^"]*"', r"\1", s, count=1)
    return f'<div style="width:{px}px">{s.replace("<svg ", "<svg style=" + chr(39) + "width:100%;height:auto;display:block" + chr(39) + " ", 1)}</div>'


def band(w):
    return f'<div style="display:flex;width:{w}px;height:8px">' + "".join(f'<span style="flex:1;background:{h}"></span>' for h in BAND) + "</div>"


def piece(name, x, y, w, rot=0):
    return f'<img class="pc" src="{CUT}/{name}.webp" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'


def foot(right=""):
    return f'<div class="ft">{logo(96)}<div style="display:flex;flex-direction:column;align-items:flex-end;gap:14px"><span class="j mu" style="font-size:28px">{right}</span>{band(120)}</div></div>'


def post_colours():
    pcs = (piece("03-4", 110, 400, 300, -8) + piece("05-6", 400, 360, 300, 0) + piece("04-1", 700, 420, 270, 7)
           + piece("01-1", 150, 720, 290, 4) + piece("05-2", 430, 700, 270, 0) + piece("04-3", 700, 740, 270, -5))
    return (f'<div style="position:absolute;left:80px;top:90px"><h1 style="font-size:104px">ดำ ส้ม ขาว</h1>'
            f'<div class="mu" style="font-size:36px;margin-top:18px">สีฮาโลวีนที่มีอยู่แล้วในเศษหนังวัวแท้</div></div>{pcs}{foot(WEB)}')


def post_tag():
    string = (f'<svg style="position:absolute;left:0;top:0" width="1080" height="1350">'
              f'<path d="M 700 470 C 760 400, 820 330, 880 250 S 980 60, 1020 -20" fill="none" stroke="{COTTON}" stroke-width="5" stroke-linecap="round" opacity=".85"/></svg>')
    write = ('<div style="position:absolute;left:300px;top:640px;width:480px;text-align:center;transform:rotate(-6deg)">'
             f'<span class="j" style="font-size:64px;color:{COTTON};opacity:.92;letter-spacing:.02em">trick or treat</span></div>')
    return (f'{string}{piece("03-4", 270, 420, 540, -6)}{write}'
            f'<div style="position:absolute;left:80px;top:90px"><h1 style="font-size:84px">03 ป้ายถุงขนม</h1>'
            f'<div class="mu" style="font-size:34px;margin-top:16px;line-height:1.5">เขียนชื่อ ร้อยเชือกผ่านร่อง ผูกที่ปากถุง</div></div>'
            f'<div class="mu" style="position:absolute;left:80px;top:1040px;font-size:28px">ผูกไว้ด้านนอกถุง ไม่ใส่ปนกับขนม</div>{foot(WEB)}')


def post_candle():
    glow = (f'<div style="position:absolute;left:340px;top:300px;width:400px;height:400px;border-radius:50%;'
            f'background:radial-gradient(circle, {MOON}cc 0%, {MOON}55 18%, {MOON}00 62%)"></div>'
            f'<div style="position:absolute;left:526px;top:470px;width:28px;height:28px;border-radius:50%;background:{MOON}"></div>')
    return (f'{glow}{piece("05-6", 300, 620, 480, 0)}'
            f'<div style="position:absolute;left:80px;top:90px"><h1 style="font-size:84px">05 รองโหลเทียน</h1>'
            f'<div class="mu" style="font-size:34px;margin-top:16px;line-height:1.5">กันคราบเทียนและรอยบนโต๊ะไม้<br>ใช้เทียนในโหลแก้วหรือเทียน LED</div></div>{foot(WEB)}')


def post_night():
    moon = f'<div style="position:absolute;right:120px;top:150px;width:70px;height:70px;border-radius:50%;background:{MOON}"></div>'
    row = (piece("01-1", 70, 660, 190, -6) + piece("03-4", 265, 670, 180, 5) + piece("05-6", 455, 655, 190, 0)
           + piece("04-3", 655, 675, 170, -4) + piece("05-4", 840, 670, 170, 6))
    return (f'{moon}<div style="position:absolute;left:80px;top:120px"><div class="j" style="font-size:150px;line-height:1">31.10</div>'
            f'<div class="j mu" style="font-size:44px;margin-top:24px">happy halloween.</div></div>{row}'
            f'<div style="position:absolute;left:80px;top:1010px;font-size:36px">คืนนี้จะออกไปเดินหรืออยู่บ้าน ก็ขอให้สนุก</div>{foot("our crafted things.")}')


DRAW = {"01-colours": post_colours, "02-treat-tag": post_tag, "03-candle": post_candle, "04-night": post_night}

# ---------------------------------------------------------------- product ideas (single piece, for PD)
IDEAS = [  # (name, piece, what it is, tier / SKU, extra material, rule check)
    ("03 ป้ายถุงขนม", "03", "เขียนชื่อด้วยปากกาสีขาว ร้อยเชือกผ่านร่อง ผูกปากถุงขนม เก็บไว้ใช้ปีหน้า",
     "ไอเดียบนการ์ดของ 03 ป้ายห้อยของขวัญ (OC-03-26) ไม่ใช่ SKU ใหม่", "เชือกปอ ปากกาเขียนหนังสีขาว",
     "ผูกด้านนอกถุง ไม่โดนขนม · ชิ้นเดียว ไม่ต่อชิ้น"),
    ("05 รองโหลเทียน", "05", "รองใต้โหลเทียนหรือเทียน LED คืนฮาโลวีน กันคราบและรอยบนโต๊ะ",
     "ไอเดียบนการ์ดของ 05 ที่รองแก้ว (PD มีข้อนี้แล้ว) ไม่ใช่ SKU ใหม่", "ไม่มี",
     "เขียนว่าใช้เทียนในโหลแก้วหรือ LED ไม่วางเทียนเปลือยบนหนัง"),
    ("โทนฮาโลวีน ดำ ส้ม ขาว", "01 02 04 05", "ลูกค้าเลือกโทนหนังเป็นดำ ส้ม หรือขาว ในชุดที่รองแก้ว 4 ลายที่มีอยู่",
     "ตัวเลือกโทนในสินค้าเดิม (OC-MX-29) ไม่ใช่ SKU ใหม่ · เว็บมีตัวเลือกโทนหนังอยู่แล้ว", "ไม่มี · คัดแผ่นสีเข้มแยกไว้ 30 นาที",
     "ชั้น 3 ชุดไม่เกิน 2 ยังเท่าเดิม"),
    ("ปั๊มคำบนชิ้นหนัง", "ทุกลาย", "ปั๊มคำสั้น เช่น BOO หรือวันที่ 31.10 หรือชื่อ ลงบนชิ้นหนัง",
     "ชั้น 2 ปั๊มชื่อหรือวันที่ (PD เสนอ 20 บาทต่อชิ้น) ทดสอบได้ในรอบ 26–29 ต.ค.", "ชุดตัวปั๊มตัวอักษร (ยังไม่มีราคา)",
     "ลองกับหนัง 1.0–1.2 มม. ก่อนว่าปั๊มติดชัด"),
    ("02 คั่นหนังสือเรื่องผี", "02", "สอดมุมหน้าหนังสือเข้าร่อง คั่นนิยายสยองที่อ่านค้าง",
     "ไอเดียบนการ์ดของ 02 (PD มีข้อนี้แล้ว) ไม่ใช่ SKU ใหม่", "ไม่มี",
     "ยังไม่มีรูปจริงของ 02 ต้องถ่ายก่อนโพสต์"),
]
NOT_THESE = [
    "ชามหรือจานใส่ขนม: โดนอาหาร",
    "หน้ากาก ชุดแต่งตัว ของเล่นเด็ก: ของใช้เด็กเล็ก",
    "ป้ายแขวนประตูหรือโมบาย: ของแขวนต้องรอหนัง 2 มม. และโมบายไม่ผ่านแล้ว",
    "วาดหน้าผีหรือหน้าฟักทองบนชิ้น 01: ห้ามหน้าหมี · ลายอื่นรอพ่อเบตัดสิน",
    "ลดราคาฮาโลวีน: เล่มแบรนด์ไม่ลดราคาแรง และเพิ่งตั้งราคาไป",
]

# ---------------------------------------------------------------- activities 25–31 Oct, scored like the Sunday plan
WEIGHTS = [("รายได้ช่วงฮาโลวีน", 25), ("มูลค่าหลังงาน", 25), ("ต้นทุนเงิน", 15), ("ค่าเสียโอกาส", 20), ("ทำได้จริง", 15)]
ACTS = [  # (activity, why, cash, people and time, money, scores, note)
    ("ลงโพสต์ฮาโลวีน 4 โพสต์ IG FB", "ให้คนเห็นว่าชิ้นเดียวใช้ในคืนฮาโลวีนได้ และพาไปเว็บ", "0 บาท", "ลงวันละ 5 นาที 27–31 ต.ค.",
     "ขายผ่านเว็บและ LINE หลังเห็นโพสต์ · ได้คนติดตามเพิ่ม", (2, 4, 5, 4, 5), "รูปทำให้แล้วในหน้านี้"),
    ("ให้เลือกโทนฮาโลวีน ดำ ส้ม ขาว", "ขายชุดที่รองแก้ว 4 ลายที่มีอยู่ ด้วยเหตุผลใหม่", "0 บาท", "คัดแผ่นสีเข้มแยกไว้ 30 นาที",
     "ชุดละ 179 บาท (ต้นทุนชิ้นหนังราว 16 บาท) ไม่ต้องทำสินค้าใหม่ · ใช้แผ่นสีเข้มที่มีมาก", (4, 3, 5, 4, 4), "เว็บมีตัวเลือกโทนหนังแล้ว ใน Shopee เขียนให้ทักบอกโทน"),
    ("ส่งบรอดแคสต์ LINE 1 ข้อความ 30 ต.ค.", "เตือนเพื่อนที่แอดจากบูธก่อนวันจริง", "0 บาท", "10 นาที",
     "รายได้จากคนที่รู้จักแบรนด์แล้ว ซื้อง่ายกว่าคนใหม่", (3, 3, 5, 5, 5), "ส่งครั้งเดียว ไม่ถี่"),
    ("จัดโต๊ะโทนฮาโลวีน ถ้าไปบูธ 31 ต.ค.", "วันจริงตรงกับวันเสาร์ ถ้างานยังเปิดอยู่", "ผ้าปูโต๊ะสีเข้มที่มีอยู่ 0–100 บาท", "จัดโต๊ะใหม่ 20 นาที",
     "ยอดขายวันเสาร์ แผ่นละ 30 บาท กำไรราว 26 บาท", (4, 3, 4, 3, 3), "ต้องรู้ก่อนว่างานเปิดถึงวันไหน"),
    ("ห่อของขวัญโทนฮาโลวีน สำหรับออเดอร์ออนไลน์ 27–31 ต.ค.", "ให้คนซื้อเป็นของฝากปาร์ตี้", "ราว 5–10 บาทต่อออเดอร์ (กระดาษคราฟต์สีเข้ม เชือก)", "ห่อเพิ่ม 3 นาทีต่อออเดอร์",
     "คุ้มเมื่อมีคนซื้อเพราะห่อสวยอย่างน้อย 1 ใน 5 ออเดอร์", (3, 3, 3, 3, 4), "ใช้ป้าย 03 และสติกเกอร์ที่มี"),
    ("คลิปสั้น 15 วินาที เลือกหนังสีดำ", "Reels และ YouTube Shorts คนเห็นมากกว่าโพสต์รูป", "0 บาท", "ถ่ายและตัด 40 นาที",
     "ยังไม่ขายทันที · ได้คนเห็นมากขึ้น", (2, 4, 5, 3, 4), "ไม่ถ่ายหน้าเด็ก"),
    ("ชวนโพสต์ #OCT26ชิ้นของฉัน ธีมฮาโลวีน", "ได้รูปจริงจากลูกค้า", "0 บาท", "ตอบคอมเมนต์",
     "ไม่ขายทันที · รูปลูกค้าช่วยให้คนใหม่เชื่อ", (1, 4, 5, 5, 4), "ไม่มีของรางวัล ไม่สุ่ม ตามกติกาเดิม"),
    ("ทดสอบปั๊มคำ BOO / 31.10 ในรอบทดสอบชั้น 2", "ดูว่าปั๊มติดชัดไหม ก่อนขายเป็นบริการเสริม", "ชุดตัวปั๊ม ยังไม่มีราคา", "ทดสอบ 1 ชั่วโมงในรอบ 26–29 ต.ค.",
     "ถ้าผ่าน ได้บริการเสริมชิ้นละ 20 บาทใช้ได้ทั้งปี", (1, 4, 2, 4, 3), "ไม่ทันขายฮาโลวีนนี้ แต่ใช้ปีใหม่ได้"),
    ("ฝากขายที่ร้านกาแฟหรือร้านขนมใกล้บ้าน", "ที่รองแก้วโทนฮาโลวีนบนโต๊ะร้าน", "0 บาท", "ไปคุยกับร้าน 1–2 ชั่วโมง",
     "ได้ช่องทางขายใหม่ แต่ยังไม่มีราคาส่ง", (2, 4, 4, 2, 2), "ต้องตั้งราคาส่งก่อน"),
    ("นิทานตอนฮาโลวีนของแบรนด์เด็ก B3", "ใช้ตัวละครที่ทำไว้แล้ว", "0 บาท", "เขียนและวาด 2–3 ชั่วโมง",
     "ไม่มีรายได้ · แบรนด์เด็กยังไม่ได้ตัดสิน", (1, 3, 5, 3, 1), "รอเด็ก ๆ ยืนยันชื่อและตัวละครก่อน"),
]


def score(s):
    return round(sum(v * w for v, (_, w) in zip(s, WEIGHTS)) / 5)


RANK = sorted(range(len(ACTS)), key=lambda i: -score(ACTS[i][5]))
TOP = RANK[:4]


def page():
    posts = "".join(
        f'<article class="card post"><img src="p{i}.jpg" alt="{E(t)}" loading="lazy">'
        f'<div class="body"><span class="chip">IG / FB {i} · {E(d)}</span><h3>{E(t)}</h3>{S.copybox(f"c{i}", cap, "แคปชัน")}</div></article>'
        for i, (_, d, t, cap) in enumerate(POSTS, 1))
    bars = "".join(
        f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 44px;gap:8px;align-items:center">'
        f'<div><div style="font-size:14px;margin-bottom:4px">{k}. {E(ACTS[i][0])}</div>'
        f'<div style="height:10px;border-radius:5px;background:var(--line)"><div style="height:100%;width:{score(ACTS[i][5])}%;border-radius:5px;background:{"#2A2725" if i in TOP else "#B07A4A"}"></div></div></div>'
        f'<b class="mono" style="text-align:right">{score(ACTS[i][5])}</b></div>' for k, i in enumerate(RANK, 1))
    acts = "".join(
        f'<article class="card" style="display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between;gap:12px">'
        f'<h3>{k}. {E(a[0])}</h3><b class="mono" style="font-size:20px">{score(a[5])}</b></div>'
        f'<p><b>เพื่อ</b> {E(a[1])}</p><p><b>ต้นทุนเงิน</b> {E(a[2])} · <b>คนและเวลา</b> {E(a[3])}</p>'
        f'<p><b>เงินและโอกาส</b> {E(a[4])}</p><p class="cap">{E(a[6])}</p></article>'
        for k, a in ((k, ACTS[i]) for k, i in enumerate(RANK, 1)))
    ideas = "".join(
        f'<article class="card" style="display:flex;flex-direction:column;gap:6px"><h3>{E(n)}</h3><p>{E(w)}</p>'
        f'<p class="cap"><b>ชิ้น</b> {E(p)} · <b>เป็นสินค้าแบบไหน</b> {E(t)}</p><p class="cap"><b>ของเพิ่ม</b> {E(x)} · <b>เช็กกฎ</b> {E(r)}</p></article>'
        for n, p, w, t, x, r in IDEAS)
    w = " · ".join(f"{n} {p}%" for n, p in WEIGHTS)
    top = "".join(f"<li>{E(ACTS[i][0])}</li>" for i in TOP)
    return f"""{S.head("OCT. 26 ฮาโลวีน")}
<style>
.post{{display:grid;grid-template-columns:minmax(0,200px) minmax(0,1fr);gap:var(--s4);align-items:start}}
.post img{{border-radius:var(--s3);width:100%}}
.post .body{{display:flex;flex-direction:column;align-items:flex-start;gap:var(--s3);min-width:0}}.post .body>.ch{{align-self:stretch}}
@media (max-width:600px){{.post{{grid-template-columns:1fr}}.post img{{max-width:260px}}}}
</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · ฮาโลวีน ส. 31 ต.ค. 2569</span><h1>ฮาโลวีนแบบเงียบ ๆ</h1>
<p class="lead">โพสต์ 4 ชิ้น ไอเดียสินค้า 5 ข้อ และกิจกรรม 10 ข้อพร้อมคะแนน ใช้ชิ้นหนังจริง สีดำ ส้ม ขาวที่มีอยู่แล้ว
ไม่ทำสินค้าใหม่ ไม่ลดราคา และเริ่มโพสต์ 27 ต.ค. เพื่อไม่ทับวันเกิดแบรนด์ 26 ต.ค.</p></header>
<section><h2>ทำก่อน: 4 อันดับแรก</h2><div class="card"><ol>{top}</ol>
<p class="cap" style="margin-top:8px">สี่ข้อนี้ใช้เงินไม่เกิน 100 บาท และใช้คนวันละไม่เกินครึ่งชั่วโมง</p></div></section>
<section><span class="eyebrow">Instagram · Facebook</span><h2>โพสต์ 4 ชิ้น</h2>
<p class="cap">รูป 1080 × 1350 ใช้ได้ทั้ง IG และ FB · กดรูปค้างไว้เพื่อบันทึก</p>{posts}</section>
<section><h2>ไอเดียสินค้าจากชิ้นหนัง</h2><p class="cap">ทุกข้อใช้ชิ้นเดียว ส่วนใหญ่เป็นไอเดียบนการ์ดของสินค้าเดิม ไม่เพิ่ม SKU ส่งให้ฝ่ายพัฒนาสินค้าดูต่อ</p>
<div style="display:flex;flex-direction:column;gap:12px">{ideas}</div>
<div class="card" style="margin-top:12px"><b>ไม่ทำ</b><ul>{"".join(f"<li>{E(x)}</li>" for x in NOT_THESE)}</ul></div></section>
<section><h2>กิจกรรม 10 ข้อ: คะแนน</h2><div class="card" style="display:flex;flex-direction:column;gap:12px">{bars}</div>
<p class="cap">น้ำหนัก: {E(w)} · ต้นทุนและค่าเสียโอกาส 5 = ถูก / เสียน้อย · สีเข้ม = ทำก่อน</p>
<div style="display:flex;flex-direction:column;gap:12px;margin-top:12px">{acts}</div></section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>
<li>งานบูธเปิดถึงวันที่ 31 ต.ค. หรือไม่ ถ้าไม่เปิด ข้อจัดโต๊ะโทนฮาโลวีนตัดออก</li>
<li>ยังไม่มีรูปจริงของ 02 โพสต์ชุดนี้จึงไม่มี 02</li>
<li>คำว่า trick or treat บนรูปที่ 2 เป็นตัวอย่างการเขียนบนชิ้นหนัง ไม่ใช่ลายที่พิมพ์มากับสินค้า</li>
<li>ราคาชุดที่รองแก้ว 4 ลาย 179 บาทตามที่ลงใน Shopee</li></ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">halloween-20261031/posts/</td><td>รูปโพสต์ 4 รูป PNG</td></tr>
<tr><td class="mono" style="white-space:nowrap">halloween-20261031/captions.txt</td><td>แคปชันทั้ง 4 โพสต์</td></tr>
<tr><td class="mono" style="white-space:nowrap">halloween-20261031/build.py</td><td>แก้แคปชัน ไอเดีย คะแนน แล้วรันใหม่</td></tr>
<tr><td>Google Doc "OCT. 26 ฮาโลวีน 31 ต.ค."</td><td>ในโฟลเดอร์ OCT. 26 ไฟล์งาน</td></tr>
</tbody></table></div></section></div>{S.COPY_JS}"""


def text():
    out = ["OCT. 26 ฮาโลวีน ส. 31 ต.ค. 2569", ""]
    out += ["== ทำก่อน"] + [f"- {ACTS[i][0]}" for i in TOP] + ["", "== โพสต์ IG / FB (รูปใน repo halloween-20261031/posts/)"]
    for i, (f, d, t, cap) in enumerate(POSTS, 1):
        out += [f"-- {i} · {d} · {t} ({f}.png)", cap, ""]
    out += ["== ไอเดียสินค้า (ชิ้นเดียว)"] + [f"- {n} ({p}): {w} · {t} · ของเพิ่ม {x} · {r}" for n, p, w, t, x, r in IDEAS]
    out += ["ไม่ทำ: " + " · ".join(NOT_THESE), "", "== กิจกรรมและคะแนน (" + " · ".join(f"{n} {p}%" for n, p in WEIGHTS) + ")"]
    for k, i in enumerate(RANK, 1):
        a = ACTS[i]
        out.append(f"{k}. {a[0]} · {score(a[5])}/100 · เพื่อ {a[1]} · ต้นทุน {a[2]} · คน {a[3]} · เงิน {a[4]} · {a[6]}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "posts"), exist_ok=True)
    for f, *_ in POSTS:
        open(os.path.join(HERE, "posts", f + ".html"), "w").write(
            f'<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{POST_CSS}</style></head><body>{DRAW[f]()}</body></html>')
    open(os.path.join(HERE, "site", "index.html"), "w").write(page())
    open(os.path.join(HERE, "captions.txt"), "w").write(text())
    for k, i in enumerate(RANK, 1):
        print(k, score(ACTS[i][5]), ACTS[i][0])
