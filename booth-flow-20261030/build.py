"""Booth giveaway flow for 30 Oct–1 Nov, MOCK for the owner to check (owner, 25 Oct: "ตามที่เสนอ ขอดู mock ก่อน").

Flow: scan the LINE QR at the booth -> the greeting says tap the rich menu -> "รับชิ้นหนังฟรี" sends a keyword, the
auto-reply sends the game link oct26brand.com/game -> play the pattern memory game (real die-cut photos) -> the end
screen says show this at the booth, with IG and FB as an invitation only -> get one 01 piece, draw on it at the DIY
corner -> staff photograph hands and piece only on the A4 backdrop, with consent, and send the photo in the LINE chat.
Decided 25 Oct: piece 01, a separate booth rich menu with a display period, the existing matching game, staff take
the photo, no duplicate check beyond the end screen. No personal data, no children's faces, no forced follow or post.

python3 booth-flow-20261030/build.py && node booth-flow-20261030/render.mjs
  -> richmenu-booth.png/.jpg, print.html -> booth-flow-a4.pdf (sign, backdrop, staff card), site/ (mock page)
"""
import html, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "print-20261022", "assets"))
from palette import C, BAND

def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m

S = _load("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
RM = _load("richmenu", os.path.join(REPO, "line-20261023", "richmenu.py"))
E = html.escape
FONTS = "file://" + os.path.join(REPO, "brand-20261014", "fonts")
IMG = "file://" + os.path.join(HERE, "img")
INK, COTTON, MUTED, LINE = C["charcoal"], C["cotton"], "#6E6A64", "#DCD4C7"

IG, FB, WEB = "https://www.instagram.com/oct.26_brand/", "https://www.facebook.com/oct26brand", "https://oct26brand.com"
PLAY = "https://oct26brand.com/game"
KEYWORD = "รับชิ้นหนังฟรี"
PIECE = "01"
BOOTH = "บูธ KIDS MARKET งานบ้านและสวนแฟร์ อิมแพ็ค เมืองทองธานี ฮอลล์ชาเลนเจอร์ 2–3"
WHEN = "30 ต.ค.–1 พ.ย. 2569 · 10:00–17:00"
TAG, HASH = "@oct.26_brand", "#OCT26ชิ้นของฉัน"
CARDS = ["01-3", "03-1", "04-2", "05-6", "07-4", "05-2"]     # six pairs, real die-cut photos (no real photo of 02)

MSG = {  # LINE texts, pasted into LINE OA Manager by the owner
    "greeting": ("ข้อความทักทาย ช่วงบูธ 30 ต.ค.–1 พ.ย.",
                 "ขอบคุณที่แอด OCT. 26\n\n"
                 f"ถ้าอยู่ที่บูธ กดปุ่ม \"{KEYWORD}\" ในเมนูด้านล่าง เล่นเกมจับคู่ให้จบ แล้วโชว์หน้าจอที่บูธ "
                 f"รับชิ้นหนังวัวแท้ {PIECE} ฟรี 1 แผ่น (คนละ 1 แผ่น)\n\n"
                 f"{BOOTH}\n{WHEN}\n\nดูของทั้งหมด oct26brand.com"),
    "reply": (f"ตอบกลับอัตโนมัติ เมื่อมีคำว่า \"{KEYWORD}\"",
              f"เกมจับคู่ชิ้นหนัง 6 คู่ ใช้เวลาราว 1 นาที\n{PLAY}\n\n"
              f"เล่นจบแล้วโชว์หน้าจอที่บูธ รับชิ้นหนัง {PIECE} ฟรี 1 แผ่น\n"
              "คนละ 1 แผ่น รับที่บูธเท่านั้น ถึง 1 พ.ย. 17:00"),
    "photo": ("ส่งพร้อมรูป หลังถ่ายที่บูธ (คนในบูธส่งเองในแชต)",
              "รูปชิ้นของคุณจากบูธวันนี้ เก็บไว้ได้เลย\n"
              f"ถ้าโพสต์ แท็ก {TAG} {HASH} ได้ เราจะตามไปดู\n"
              "ถ้าไม่อยากให้เราลงรูปนี้ในเพจ บอกในแชตนี้ได้\n\nขอบคุณที่แวะมา"),
    "thanks": ("บรอดแคสต์ขอบคุณ 2 พ.ย.",
               "ขอบคุณที่แวะบูธ OCT. 26 ที่งานบ้านและสวนแฟร์\n"
               "ชิ้นหนังที่ได้ไป ใช้เป็นที่รองแก้ว ป้ายของขวัญ หรือที่เก็บสายชาร์จก็ได้\n\n"
               f"ไอเดียและของทั้งหมด {WEB}\nInstagram {IG}\nFacebook {FB}"),
}
for _, t in MSG.values():
    for word in ("ไม่ต้องเย็บ", "ต่อเอง", "หัวใจ", "แท็กเพื่อน", "สุ่ม"):
        assert word not in t, word

END = {  # end screen of the game page
    "title": "เล่นจบแล้ว",
    "show": "โชว์หน้านี้ที่บูธ OCT. 26",
    "get": f"รับชิ้นหนังวัวแท้ {PIECE} ฟรี 1 แผ่น",
    "diy": "ที่บูธมีมุมวาดลายหรือเขียนชื่อบนชิ้นหนัง",
    "follow": "ระหว่างรอ ฝากติดตามเราด้วย",
    "note": "ไม่ติดตามก็รับได้ · คนละ 1 แผ่น",
}

# ------------------------------------------------------------------ booth rich menu: large, 1 top + 3 bottom
def richmenu_booth():
    top = (f'<div style="position:absolute;left:0;top:0;width:2500px;height:843px;display:flex;align-items:center;gap:90px;padding:0 150px">'
           f'<img src="{IMG}/01-3.webp" style="width:520px;filter:drop-shadow(0 18px 24px rgba(42,39,37,.25))">'
           f'<div style="display:flex;flex-direction:column;gap:30px"><div class="lb" style="font-size:150px">{KEYWORD}</div>'
           f'<div class="sb" style="font-size:66px;margin:0">เล่นเกมจับคู่ · รับชิ้นหนัง {PIECE} ที่บูธ 1 แผ่น</div>'
           f'<div class="sb" style="font-size:54px;margin:0">30.10–01.11 · KIDS MARKET อิมแพ็ค</div></div></div>')
    cells, x = [], 0
    for k, label, sub in (("A", "เว็บไซต์", "oct26brand.com"), ("D", "Instagram", "@oct.26_brand"), ("E", "Facebook", "oct26brand")):
        w = RM.CW[len(cells)]
        cells.append(f'<div class="cell" style="left:{x}px;top:843px;width:{w}px;height:843px">'
                     f'<div class="ic">{RM.ICON[k]}</div><div class="lb{" en" if label.isascii() else ""}">{label}</div><div class="sb">{sub}</div></div>')
        x += w
    lines = (f'<div style="position:absolute;left:0;right:0;top:842px;height:3px;background:{LINE}"></div>'
             + "".join(f'<div style="position:absolute;top:903px;bottom:80px;left:{x - 1}px;width:3px;background:{LINE}"></div>'
                       for x in (RM.CW[0], RM.CW[0] + RM.CW[1])))
    band = '<div style="position:absolute;left:0;right:0;bottom:0;height:22px;display:flex">' + "".join(
        f'<span style="flex:1;background:{h}"></span>' for h in BAND) + "</div>"
    base = RM.page()
    head = base[:base.index("<body>")]
    return f'{head}<body><div style="position:absolute;inset:0 0 auto 0;height:843px;background:#EAE4D8"></div>{top}{"".join(cells)}{lines}{band}</body></html>'


RICH_AREAS = [("A (บนเต็มแถว)", KEYWORD, "ข้อความ", KEYWORD), ("B (ล่างซ้าย)", "เว็บไซต์", "ลิงก์", WEB + "/"),
              ("C (ล่างกลาง)", "Instagram", "ลิงก์", IG), ("D (ล่างขวา)", "Facebook", "ลิงก์", FB)]

# ------------------------------------------------------------------ A4 prints: sign, photo backdrop, staff card
PRINT_CSS = f"""
@font-face{{font-family:Anuphan;font-weight:500;src:url({FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Jost;font-weight:400;src:url({FONTS}/alt/Jost-Regular.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url({FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Plex;font-weight:400;src:url({FONTS}/IBMPlexSansThai-Regular.ttf)}}
@font-face{{font-family:Plex;font-weight:600;src:url({FONTS}/IBMPlexSansThai-SemiBold.ttf)}}
@page{{size:210mm 297mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Plex;color:{INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{position:relative;width:210mm;height:297mm;overflow:hidden;page-break-after:always;background:#fff}}
h1,h2{{font-family:Anuphan;font-weight:500;line-height:1.15}}
.j{{font-family:Jost;font-weight:500}}.mu{{color:{MUTED}}}
.lg svg{{width:100%;height:auto;display:block}}
"""


def logo(mm):
    s = open(os.path.join(HERE, "img", "square-light.svg")).read()
    s = re.sub(r'(<svg[^>]*?) width="[^"]*" height="[^"]*"', r"\1", s, count=1)
    return f'<div class="lg" style="width:{mm}mm;flex:none">{s}</div>'


def band(h, w):
    return f'<div style="display:flex;height:{h}mm;width:{w}">' + "".join(f'<span style="flex:1;background:{c}"></span>' for c in BAND) + "</div>"


def sign():
    steps = [("สแกน QR แอด LINE", "LINE OA @155riuqj"), (f"กดเมนู \"{KEYWORD}\"", "ปุ่มใหญ่ด้านล่างของแชต"),
             ("เล่นเกมจับคู่ให้จบ", "6 คู่ ราว 1 นาที"), ("โชว์หน้าจอที่บูธ", f"รับชิ้นหนัง {PIECE} แล้ววาดลายที่มุม DIY")]
    li = "".join(f'<li style="display:grid;grid-template-columns:13mm 1fr;gap:5mm;align-items:center">'
                 f'<b class="j" style="width:13mm;height:13mm;border-radius:50%;background:{INK};color:{COTTON};display:grid;place-items:center;font-size:6mm">{i}</b>'
                 f'<div><div style="font-size:6.4mm;font-weight:600">{E(a)}</div><div class="mu" style="font-size:4.4mm">{E(b)}</div></div></li>'
                 for i, (a, b) in enumerate(steps, 1))
    return (f'<div class="page"><div style="position:absolute;inset:16mm 18mm 18mm;display:flex;flex-direction:column;gap:9mm">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start">{logo(28)}'
            f'<img src="{IMG}/01-3.webp" style="width:52mm;filter:drop-shadow(0 2mm 3mm rgba(42,39,37,.25))"></div>'
            f'<h1 style="font-size:15mm">รับชิ้นหนังวัวแท้<br>ฟรี 1 แผ่น</h1>'
            f'<div style="display:flex;gap:10mm;align-items:center"><ol style="list-style:none;display:grid;gap:6mm;flex:1">{li}</ol>'
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:2mm"><img src="{IMG}/line-qr.png" style="width:58mm;height:58mm;image-rendering:pixelated">'
            f'<span class="j" style="font-size:5mm">LINE @155riuqj</span></div></div>'
            f'<div class="mu" style="margin-top:auto;font-size:4mm;line-height:1.6;border-top:0.3mm solid {LINE};padding-top:4mm">'
            f'คนละ 1 แผ่น · ไม่ต้องกดติดตามก็รับได้ · ถ่ายรูปเฉพาะมือกับชิ้นหนัง เมื่อคุณอนุญาต<br>{E(WHEN)}</div>'
            f'{band(1.6, "30mm")}</div></div>')


def backdrop(sample=False):
    corners = "".join(f'<div style="position:absolute;{v}:{70 if v == "top" else 80}mm;{h}:35mm;width:8mm;height:8mm;'
                      f'border-{v}:0.4mm solid {LINE};border-{h}:0.4mm solid {LINE}"></div>'
                      for v in ("top", "bottom") for h in ("left", "right"))
    pc = f'<img src="{IMG}/01-1.webp" style="position:absolute;left:62mm;top:98mm;width:86mm;transform:rotate(-6deg);filter:drop-shadow(0 2mm 3mm rgba(42,39,37,.3))">' if sample else ""
    return (f'<div class="page" style="background:{COTTON if sample else "#fff"}">'
            f'<div style="position:absolute;left:24mm;top:22mm">{logo(26)}</div>{corners}{pc}'
            f'<div style="position:absolute;left:24mm;right:24mm;bottom:24mm;display:flex;justify-content:space-between;align-items:flex-end">'
            f'<span class="j mu" style="font-size:4.4mm;font-weight:400">our crafted things. · 30.10–01.11.2026</span>{band(1.6, "30mm")}</div></div>')


def staff():
    do = [("ดูหน้าจอ", "หน้าจอ \"เล่นจบแล้ว\" ในมือถือ ไม่ต้องดูว่ากดติดตาม IG หรือไม่"),
          ("ให้ชิ้น 01", "คนละ 1 แผ่น เลือกสีได้ · ขีดในช่องนับด้านล่าง"),
          ("ชวนไปมุม DIY", "\"วาดลายหรือเขียนชื่อได้ที่มุมนี้นะ\""),
          ("ขอถ่ายรูป", "\"ขอถ่ายรูปมือกับชิ้นนี้ได้ไหม\" · ถ่ายบนแผ่นพื้นหลัง เห็นแค่มือกับชิ้นหนัง ไม่ถ่ายหน้า โดยเฉพาะเด็ก"),
          ("ส่งรูปใน LINE", "เปิดแชตของลูกค้าในแอป LINE OA ส่งรูป + ข้อความ \"ส่งพร้อมรูป\" ที่บันทึกไว้"),
          ("ถามเรื่องลงเพจ", "\"ขอเอารูปนี้ไปลงเพจได้ไหม\" · ได้ = ขีดช่องอนุญาต · ไม่ได้ = ไม่ลง")]
    li = "".join(f'<li style="display:grid;grid-template-columns:9mm 34mm 1fr;gap:3mm;padding:3.4mm 0;border-top:0.3mm solid {LINE}">'
                 f'<b class="j" style="font-size:5mm">{i}</b><b style="font-size:4.6mm">{E(a)}</b><span style="font-size:4.2mm;line-height:1.5">{E(b)}</span></li>'
                 for i, (a, b) in enumerate(do, 1))
    tally = "".join(f'<div style="border:0.3mm solid {LINE};padding:3mm;height:30mm"><b style="font-size:4mm">{E(t)}</b></div>'
                    for t in ("ชิ้น 01 ที่แจก (ขีดทีละ 1)", "รูปที่ลูกค้าอนุญาตให้ลงเพจ", "เพื่อน LINE เช้า / เย็น"))
    return (f'<div class="page"><div style="position:absolute;inset:16mm 18mm">'
            f'<div style="display:flex;justify-content:space-between;align-items:center">{logo(18)}<span class="mu" style="font-size:3.8mm">สำหรับคนในบูธ · ไม่ต้องวางให้ลูกค้าเห็น</span></div>'
            f'<h1 style="font-size:10mm;margin:8mm 0 4mm">การ์ดคนในบูธ: รับชิ้นหนังฟรี</h1><ol style="list-style:none">{li}</ol>'
            f'<div class="mu" style="font-size:3.8mm;line-height:1.6;margin:5mm 0">ไม่บังคับโพสต์ ไม่บังคับติดตาม ไม่มีของเพิ่มสำหรับคนที่โพสต์ · ถ้ามีคนมารับซ้ำ ให้ไปเถอะ ไม่ต้องเถียง</div>'
            f'<h2 style="font-size:6mm;margin:4mm 0 3mm">ช่องนับ</h2><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3mm">{tally}</div></div></div>')


SHEETS = [("ป้าย A4 รับชิ้นหนังฟรี", sign), ("แผ่นพื้นหลังถ่ายรูป A4", backdrop), ("การ์ดคนในบูธ + ช่องนับ", staff)]

# ------------------------------------------------------------------ the mock page: a phone you can tap through
def mock():
    msgs = {k: E(t).replace("\n", "<br>") for k, (_, t) in MSG.items()}
    cards = json.dumps(CARDS)
    rows = "".join(f'<tr><td>{E(a)}</td><td><b>{E(l)}</b></td><td>{E(t)}</td><td class="mono" style="word-break:break-all">{E(v)}</td></tr>' for a, l, t, v in RICH_AREAS)
    texts = "".join(f'<article class="card" style="display:flex;flex-direction:column;gap:8px"><h3>{E(t)}</h3>{S.copybox("m-" + k, body, "ข้อความ")}</article>'
                    for k, (t, body) in MSG.items())
    prints = "".join(f'<figure style="margin:0;display:flex;flex-direction:column;gap:6px"><img src="a4-{i}.png" alt="{E(t)}" loading="lazy" '
                     f'style="border:1px solid var(--line);border-radius:6px;background:#fff"><figcaption class="cap">{E(t)}</figcaption></figure>'
                     for i, (t, _) in enumerate(SHEETS, 1))
    return f"""{S.head("OCT. 26 รับชิ้นหนังฟรี mock")}
<style>
.phone{{width:100%;max-width:360px;margin:0 auto;border:10px solid #2A2725;border-radius:34px;overflow:hidden;background:#fff;box-shadow:0 10px 30px rgba(42,39,37,.18)}}
.scr{{height:640px;display:flex;flex-direction:column;position:relative}}
.scr[hidden]{{display:none}}
.lhead{{background:#2A2725;color:#F4F0E8;padding:12px 14px;font:500 15px Jost,sans-serif;display:flex;gap:10px;align-items:center}}
.lhead img{{width:26px;height:26px;border-radius:50%;background:#F4F0E8}}
.chat{{flex:1;overflow:auto;background:#C9D4DE;padding:12px;display:flex;flex-direction:column;gap:10px}}
.b{{max-width:84%;padding:10px 12px;border-radius:16px;font-size:13.5px;line-height:1.5;background:#fff;color:#2A2725;align-self:flex-start}}
.b.me{{align-self:flex-end;background:#A8E28A}}
.b a{{color:#2E4A7D;word-break:break-all}}
.rich{{display:block;width:100%;border:0;padding:0;background:none;cursor:pointer}}
.rich img{{display:block;width:100%}}
.rbar{{background:#fff;border-top:1px solid #ddd;text-align:center;font-size:12px;padding:6px;color:#6E6A64}}
.web{{flex:1;overflow:auto;background:#F4F0E8;padding:18px 16px;display:flex;flex-direction:column;gap:12px;color:#2A2725}}
.url{{background:#eee;font:12px Jost,sans-serif;padding:6px 10px;color:#555}}
.board{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.cd{{aspect-ratio:1;border:0;border-radius:10px;background:#2A2725;color:#F4F0E8;font:500 12px Jost,sans-serif;cursor:pointer;padding:6px;display:grid;place-items:center}}
.cd img{{width:100%;height:100%;object-fit:contain;display:none}}
.cd.open,.cd.done{{background:#fff}}.cd.open img,.cd.done img{{display:block}}.cd.open span,.cd.done span{{display:none}}
.cd.done{{outline:2px solid #5E7A3A}}
.btn{{display:block;text-align:center;border-radius:999px;padding:12px;font-weight:600;font-size:14px;border:0;cursor:pointer;text-decoration:none}}
.btn.dark{{background:#2A2725;color:#F4F0E8}}.btn.line{{background:#fff;color:#2A2725;border:1px solid #DCD4C7}}
.steps{{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:12px 0}}
.steps button{{border:1px solid var(--line);background:var(--paper);border-radius:999px;padding:4px 10px;font-size:12px;cursor:pointer}}
.steps button.on{{background:#2A2725;color:#F4F0E8}}
</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · mock ให้ตรวจ · บูธ 30 ต.ค.–1 พ.ย.</span><h1>รับชิ้นหนังฟรีผ่าน LINE</h1>
<p class="lead">ลองกดในโทรศัพท์ข้างล่างได้เลย ตั้งแต่แอด LINE จนได้รูปกลับมาในแชต ยังไม่ได้แก้เว็บหรือ LINE จริง
ถ้าผ่านแล้วจะทำหน้า oct26brand.com/game จริงเป็น PR ให้กด Merge</p></header>
<section><h2>ลองกด</h2>
<div class="steps" id="steps"></div>
<div class="phone">
<div class="scr" id="s1"><div class="lhead"><img src="logo.svg" alt="">OCT. 26</div>
<div class="chat" id="chat"><div class="b">{msgs["greeting"]}</div></div>
<button class="rich" id="rich" type="button" aria-label="ริชเมนู กดรับชิ้นหนังฟรี"><img src="richmenu-booth.jpg" alt="ริชเมนูช่วงบูธ"></button>
<div class="rbar">แตะช่องบน "{KEYWORD}"</div></div>
<div class="scr" id="s2" hidden><div class="url">oct26brand.com/game</div><div class="web">
<img src="logo.svg" alt="OCT. 26" style="width:56px">
<h2 style="font-size:24px">จับคู่ชิ้นหนัง</h2><p style="font-size:14px;color:#6E6A64">เปิดการ์ดทีละ 2 ใบ หาชิ้นหนังที่เหมือนกันให้ครบ 6 คู่</p>
<div class="board" id="board"></div><p style="font-size:13px;color:#6E6A64">เปิดไป <b id="moves">0</b> ครั้ง · ได้ <b id="pairs">0</b> / 6 คู่</p>
<button class="btn line" id="skip" type="button">ข้ามเกม (เฉพาะ mock)</button></div></div>
<div class="scr" id="s3" hidden><div class="url">oct26brand.com/game</div><div class="web" style="text-align:center;align-items:center">
<img src="logo.svg" alt="OCT. 26" style="width:56px"><h2 style="font-size:30px;margin-top:6px">{E(END["title"])}</h2>
<p style="font-size:14px;color:#6E6A64" id="took"></p>
<div style="background:#fff;border:2px solid #2A2725;border-radius:16px;padding:14px;width:100%">
<b style="font-size:17px">{E(END["show"])}</b><br><span style="font-size:15px">{E(END["get"])}</span>
<img src="01-3.webp" alt="ชิ้นหนัง 01" style="width:110px;display:block;margin:10px auto 0"></div>
<p style="font-size:13px">{E(END["diy"])}</p>
<p style="font-size:13px;color:#6E6A64;margin-top:4px">{E(END["follow"])}</p>
<div style="display:flex;gap:8px;width:100%"><a class="btn dark" style="flex:1" href="{IG}" target="_blank" rel="noopener">Instagram</a>
<a class="btn line" style="flex:1" href="{FB}" target="_blank" rel="noopener">Facebook</a></div>
<p style="font-size:12px;color:#6E6A64">{E(END["note"])}</p>
<button class="btn line" id="tobooth" type="button" style="width:100%">ถัดไป: ที่บูธ (mock)</button></div></div>
<div class="scr" id="s4" hidden><div class="lhead"><img src="logo.svg" alt="">OCT. 26</div>
<div class="chat"><div class="b me" style="font-size:12px">(ที่บูธ: รับชิ้น 01 · วาดลาย · คนในบูธถ่ายรูปมือกับชิ้นหนัง)</div>
<div class="b" style="padding:4px"><img src="photo-sample.jpg" alt="ตัวอย่างรูปที่ส่งให้ลูกค้า" style="width:100%;border-radius:12px;display:block"></div>
<div class="b">{msgs["photo"]}</div></div>
<div class="rbar"><button class="btn line" id="again" type="button" style="display:inline-block;padding:6px 14px">เริ่มใหม่</button></div></div>
</div>
<p class="cap" style="text-align:center;margin-top:8px">หน้าตาแชตเป็นแบบจำลอง ของจริงคือแอป LINE · รูปในขั้นสุดท้ายเป็นตัวอย่าง ของจริงคือรูปมือถือชิ้นหนังบนแผ่นพื้นหลัง</p></section>
<section><h2>ริชเมนูช่วงบูธ</h2><img src="richmenu-booth.jpg" alt="ริชเมนูช่วงบูธ" style="width:100%;border:1px solid var(--line);border-radius:6px">
<div class="tbl" style="margin-top:10px"><table><thead><tr><th>ช่อง</th><th>ปุ่ม</th><th>ประเภท</th><th>ตั้งเป็น</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="cap">LINE OA Manager → ริชเมนู → สร้าง → เทมเพลตขนาดใหญ่ แบบช่องบน 1 ช่องล่าง 3 · ตั้งช่วงเวลาแสดง 30 ต.ค. 09:00 – 1 พ.ย. 18:00 แล้วเมนูปกติ 6 ปุ่มกลับมาเอง</p></section>
<section><h2>ข้อความ LINE 4 ข้อความ</h2><div style="display:flex;flex-direction:column;gap:12px">{texts}</div>
<p class="cap">ตั้งค่าการตอบกลับใน LINE OA ให้เปิดทั้งแชตและข้อความตอบกลับอัตโนมัติ ไม่อย่างนั้นปุ่มจะไม่ส่งลิงก์</p></section>
<section><h2>ของพิมพ์ A4</h2><div class="grid">{prints}</div>
<p class="cap">พิมพ์จากเครื่องที่บ้าน ขนาดจริง 100% · แผ่นพื้นหลังถ้ามีกระดาษสีครีมจะเข้ากับแบรนด์ที่สุด</p></section>
<section><h2>คำสั่งสำหรับทีมเว็บ</h2><p class="cap">กดคัดลอกแล้วส่งให้ session เว็บได้เลย · เกมอยู่ที่ /game เพราะ /play ถูกตั้งให้เด้งไปหน้าแรกอยู่แล้ว</p>
{S.copybox("brief", open(os.path.join(HERE, "WEB-BRIEF.md")).read(), "คำสั่ง")}</section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>
<li>ชิ้นที่แจกคือ 01 เลือกสีได้ (มี 369 แผ่น)</li>
<li>ใครในบูธเป็นคนถ่ายรูปและส่งในแชต ต้องล็อกอินแอป LINE OA ในมือถือเครื่องนั้น</li>
<li>หน้าเกมจริงไม่เก็บชื่อ เบอร์ หรือข้อมูลใด ๆ นับแค่จำนวนคนเล่นจบจากสถิติเว็บ</li>
<li>ถ้าผ่าน mock: ทำหน้า /game จริง (PR) ริชเมนู ข้อความ และไฟล์พิมพ์ PDF ให้เสร็จภายใน 28 ต.ค. ลองกับมือถือจริง 29 ต.ค.</li></ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">booth-flow-20261030/WEB-BRIEF.md</td><td>คำสั่งสำหรับทีมเว็บ</td></tr>
<tr><td class="mono" style="white-space:nowrap">booth-flow-20261030/build.py</td><td>ข้อความ ปุ่ม และของพิมพ์ทั้งหมด</td></tr>
<tr><td class="mono" style="white-space:nowrap">booth-flow-20261030/richmenu-booth.jpg</td><td>รูปริชเมนูช่วงบูธ 2500 × 1686</td></tr>
<tr><td class="mono" style="white-space:nowrap">booth-flow-20261030/booth-flow-a4.pdf</td><td>ป้าย แผ่นพื้นหลัง การ์ดคนในบูธ</td></tr>
</tbody></table></div></section></div>
<script>
const CARDS = {cards};
const $ = id => document.getElementById(id);
const SCR = ["s1", "s2", "s3", "s4"], NAMES = ["1 แชต LINE", "2 เกม", "3 จบเกม", "4 รูปในแชต"];
function show(id){{ SCR.forEach(s => $(s).hidden = s !== id); [...$("steps").children].forEach((b, i) => b.classList.toggle("on", SCR[i] === id)); }}
$("steps").innerHTML = NAMES.map((n, i) => `<button type="button" data-s="${{SCR[i]}}">${{n}}</button>`).join("");
$("steps").addEventListener("click", e => {{ const b = e.target.closest("button"); if (!b) return; if (b.dataset.s === "s2") deal(); if (b.dataset.s === "s3") $("took").textContent = ""; show(b.dataset.s); }});
let asked = false;
$("rich").addEventListener("click", () => {{
  if (asked) return; asked = true;
  const c = $("chat");
  c.insertAdjacentHTML("beforeend", `<div class="b me">{E(KEYWORD)}</div>`);
  setTimeout(() => {{ c.insertAdjacentHTML("beforeend", `<div class="b">{msgs["reply"].replace("https://oct26brand.com/game", '<a href="#" id="playlink">https://oct26brand.com/game</a>')}</div>`);
    c.scrollTop = c.scrollHeight; $("playlink").addEventListener("click", e => {{ e.preventDefault(); deal(); show("s2"); }}); }}, 500);
  c.scrollTop = c.scrollHeight;
}});
let open = [], moves = 0, pairs = 0, lock = false;
function deal(){{
  const deck = [...CARDS, ...CARDS];
  for (let i = deck.length - 1; i > 0; i--){{ const j = Math.floor(Math.random() * (i + 1)); [deck[i], deck[j]] = [deck[j], deck[i]]; }}
  open = []; moves = 0; pairs = 0; lock = false; $("moves").textContent = 0; $("pairs").textContent = 0;
  $("board").innerHTML = deck.map((k, i) => `<button class="cd" type="button" data-k="${{k}}" aria-label="การ์ดใบที่ ${{i + 1}}"><span>OCT. 26</span><img src="${{k}}.webp" alt=""></button>`).join("");
}}
function win(){{ $("took").textContent = moves ? `จับคู่ครบใน ${{moves}} ครั้ง · ` + new Date().toLocaleTimeString("th-TH", {{hour: "2-digit", minute: "2-digit"}}) : ""; show("s3"); }}
$("board").addEventListener("click", e => {{
  const c = e.target.closest(".cd"); if (!c || lock || c.classList.contains("open") || c.classList.contains("done")) return;
  c.classList.add("open"); open.push(c); if (open.length < 2) return;
  moves++; $("moves").textContent = moves; const [a, b] = open;
  if (a.dataset.k === b.dataset.k){{ a.classList.replace("open", "done"); b.classList.replace("open", "done"); open = []; pairs++; $("pairs").textContent = pairs; if (pairs === 6) setTimeout(win, 500); }}
  else {{ lock = true; setTimeout(() => {{ a.classList.remove("open"); b.classList.remove("open"); open = []; lock = false; }}, 750); }}
}});
$("skip").addEventListener("click", () => {{ moves = 0; win(); }});
$("tobooth").addEventListener("click", () => show("s4"));
$("again").addEventListener("click", () => {{ asked = false; $("chat").innerHTML = `<div class="b">{msgs["greeting"]}</div>`; show("s1"); }});
show("s1");
</script>{S.COPY_JS}"""


if __name__ == "__main__":
    open(os.path.join(HERE, "richmenu-booth.html"), "w").write(richmenu_booth())
    body = "".join(fn() for _, fn in SHEETS) + backdrop(sample=True)
    open(os.path.join(HERE, "print.html"), "w").write(
        f'<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{PRINT_CSS}</style></head><body>{body}</body></html>')
    open(os.path.join(HERE, "site", "index.html"), "w").write(mock())
    open(os.path.join(HERE, "messages.txt"), "w").write("\n\n".join(f"===== {t}\n\n{b}" for t, b in MSG.values()) + "\n")
    print("wrote richmenu-booth.html, print.html, site/index.html, messages.txt")
