"""Booth story and signs for Sustainability Expo 2026 (SX2026, 6-15 Nov 2026, QSNCC).

Story: leftover real cowhide from a factory, cut at home with our own dies 01-07, finished by one family.
Honest on purpose: the hide is ordinary chemical tanning, so we never say eco leather, natural tanning or food safe.
Game (owner 29 Oct): collect all six patterns (01-05, 07), get something extra. The customer picks every piece,
nothing is random. No stamp at the booth (owner 29 Oct), so staff tick the card with a pen and sign it.

python3 build.py -> poster.html (A3) and signs.html (A4);  node render.cjs -> PDFs + preview/*.png
"""
import io, os, re
import qrcode
import qrcode.image.svg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, "brand-20261014", "fonts")
LOGO = os.path.join(ROOT, "brand-20261014", "brandbook-v2", "logo", "svg")
DRAW = os.path.join(ROOT, "pattern-intro-20261022", "drawings")
PLAN = os.path.join(ROOT, "brand-20261014", "brand-bible", "assets", "plan")
LINE, LINE_ID = "https://lin.ee/PKopJND", "@155riuqj"
WEB = "oct26brand.com"
BAND = ["#A9442B", "#5E7A3A", "#E9A825", "#B9A3D6", "#2E4A7D"]

# Pattern code, Thai name, English name, plan photo (02 has no real photo yet, so it uses the die drawing).
PATTERNS = [("01", "หมี", "Bear", "01-1"), ("02", "กังหัน", "Pinwheel", None), ("03", "กากบาทแคปซูล", "Capsule cross", "03-1"),
            ("04", "สี่เหลี่ยมมน", "Rounded square", "04-2"), ("05", "วงกลม", "Circle", "05-1"), ("07", "กากบาทข้อต่อวงกลม", "Round-joint cross", "07-2")]
NAMES = {"01": "bear", "02": "pinwheel", "03": "capsule-cross", "04": "rounded-square", "05": "circle", "07": "round-joint-cross"}

# The reward for a full card. Owner to confirm; change here and rebuild.
REWARD_TH = "รับชิ้นที่ 7 ฟรี เลือกลายเอง + เลขนักสะสมประจำตัว"
REWARD_EN = "a 7th piece free, your pick, and your own collector number"

STORY_TH = ("OCT. 26 เป็นแบรนด์ของครอบครัวหนึ่ง ชื่อมาจากวันเกิดของแม่ เรารับเศษหนังวัวแท้ที่เหลือจากโรงงาน "
            "มาตัดด้วยบล็อกที่พ่อออกแบบเอง ทุกแบบมีเลข 01–07 ตัดได้ขนาดเท่ากันทุกชิ้น ลูกสามคนช่วยคัดหนัง แพ็ก และขาย")
STORY_EN = ("OCT. 26 is one family's label, named after Mum's birthday. We take real cowhide left over at a factory, "
            "cut it at home with dies Dad designed, and number every shape 01–07.")
HONEST_TH = ("เราไม่ได้บอกว่าหนังนี้รักษ์โลก หนังผ่านการฟอกแบบทั่วไป ไม่ใช่ภาชนะใส่อาหาร "
             "สิ่งที่เราทำคือใช้หนังที่มีอยู่แล้วให้คุ้มที่สุดก่อนซื้อใหม่ และไม่ทาสีขอบ")
HONEST_EN = "We don't call it eco leather. It is ordinary tanned hide. We just use what already exists, all the way, before buying more."
FACTS = [("01–07", "บล็อกตัดของเราเอง 6 แบบ", "our own six cutting dies"),
         ("37%", "ของน้ำหนักเศษหนัง ตัดเป็นชิ้นได้ ที่เหลือเก็บไว้ตัดชิ้นเล็ก", "of the offcut weight becomes pieces; the rest waits for smaller dies"),
         ("7 กก.", "เศษหนังที่ยังเหลือ ใช้ให้หมดก่อนซื้อเพิ่ม", "of offcuts left to use before we buy more")]


def qr(url, cls="qr"):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    buf = io.BytesIO(); img.save(buf)
    s = re.sub(r"<\?xml[^>]*>", "", buf.getvalue().decode())
    s = re.sub(r'width="[^"]*" height="[^"]*"', "", s, count=1)
    return s.replace("<svg ", f'<svg class="{cls}" ', 1)


def logo(name="square-light", cls="logo"):
    s = open(os.path.join(LOGO, name + ".svg")).read()
    return re.sub(r' width="[\d.]+(mm|px)?" height="[\d.]+(mm|px)?"', f' class="{cls}"', s, count=1)


def drawing(code, kind="line", cls="dr"):
    s = open(os.path.join(DRAW, f"pattern-{code}-{NAMES[code]}-{kind}.svg")).read()
    return re.sub(r' width="[\d.]+mm" height="[\d.]+mm"', f' class="{cls}"', s, count=1)


def photo(code, plan):
    if plan is None:
        return f'<div class="ph">{drawing(code, "solid")}</div>'
    return f'<div class="ph" style="background-image:url(file://{os.path.join(PLAN, plan + ".png")})"></div>'


def band():
    return '<div class="band">' + "".join(f'<i style="background:{c}"></i>' for c in BAND) + "</div>"


CSS = """
@font-face{font-family:Anuphan;font-weight:500;src:url(file://__FONTS__/alt/Anuphan-Medium.ttf)}
@font-face{font-family:Plex;src:url(file://__FONTS__/IBMPlexSansThai-Regular.ttf)}
@font-face{font-family:Plex;font-weight:600;src:url(file://__FONTS__/IBMPlexSansThai-SemiBold.ttf)}
@font-face{font-family:Jost;font-weight:400;src:url(file://__FONTS__/alt/Jost-Regular.ttf)}
@font-face{font-family:Jost;font-weight:500;src:url(file://__FONTS__/alt/Jost-Medium.ttf)}
@page{size:__SIZE__;margin:0} *{box-sizing:border-box} html,body{margin:0}
body{font-family:Plex,sans-serif;color:#2A2725;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:__W__;height:__H__;position:relative;background:#F4F0E8;page-break-after:always;overflow:hidden}
.pg:last-child{page-break-after:auto}
.band{display:flex;position:absolute;left:0;right:0;bottom:0;height:4mm} .band i{flex:1}
.latin{font-family:Jost} .muted{color:#6E6A64}
h1,h2,h3{font-family:Anuphan;font-weight:500;margin:0;line-height:1.15}
p{margin:0}
.ph{aspect-ratio:1;background:center/contain no-repeat;display:grid;place-items:center}
.ph svg{width:82%;height:82%} .ph svg path,.ph svg circle,.ph svg rect{fill:#8B5E3C}
.qr{display:block;background:#fff;padding:1.5mm}
"""


def css(size, w, h, extra):
    return CSS.replace("__FONTS__", FONTS).replace("__SIZE__", size).replace("__W__", w).replace("__H__", h) + extra


# ------------------------------------------------------------------ A3 poster
POSTER_CSS = """
.pg{padding:22mm 22mm 0}
.top{display:flex;justify-content:space-between;align-items:flex-start}
.logo{width:40mm;height:40mm;display:block}
.ev{font-family:Jost;font-size:5mm;letter-spacing:.18em;text-align:right;line-height:1.6;color:#6E6A64}
.head{margin-top:12mm}
.head h1{font-size:20mm;line-height:1.08}
.head .en{font-family:Jost;font-size:11mm;margin-top:4mm}
.grid{display:grid;grid-template-columns:repeat(3,52mm);justify-content:space-between;gap:5mm 0;margin-top:12mm}
.cell{display:grid;gap:1.5mm}
.cell .ph{background-color:#FBF8F2;border-radius:3mm}
.cell b{font-family:Jost;font-weight:500;font-size:9mm;line-height:1}
.cell span{font-size:4.4mm}
.story{margin-top:10mm;font-size:5.8mm;line-height:1.55;max-width:240mm}
.story .en{font-family:Jost;font-size:5mm;color:#4A4542;margin-top:3mm;line-height:1.5}
.foot{position:absolute;left:22mm;right:22mm;bottom:16mm;display:flex;gap:8mm;align-items:center}
.foot .qr{width:34mm;height:34mm}
.foot p{font-size:5.4mm;line-height:1.45}
"""


def poster():
    cells = "".join(f'<div class="cell">{photo(c, pl)}<b>{c}</b><span>{th} · <span class="latin">{en}</span></span></div>'
                    for c, th, en, pl in PATTERNS)
    body = f'''<section class="pg">
<div class="top">{logo()}<p class="ev">SUSTAINABILITY EXPO 2026<br>6–15 NOV · QSNCC</p></div>
<div class="head"><h1>หนังที่เหลือ<br>ได้ชีวิตที่สอง</h1><p class="en">Leftover leather, a second life.</p></div>
<div class="grid">{cells}</div>
<div class="story"><p>{STORY_TH}</p></div>
<div class="foot">{qr(LINE)}<p><b>สะสมครบ 6 ลาย {REWARD_TH}</b><br>เพิ่มเพื่อน LINE {LINE_ID} · {WEB}</p></div>
{band()}</section>'''
    return f'<!doctype html><html lang="th"><meta charset="utf-8"><title>OCT. 26 SX2026 poster</title><style>{css("A3", "297mm", "420mm", POSTER_CSS)}</style>{body}</html>'


# ------------------------------------------------------------------ A4 signs
SIGN_CSS = """
.pg{padding:16mm 16mm 0}
.logo{width:26mm;height:26mm;display:block}
.ev{position:absolute;right:16mm;top:18mm;font-family:Jost;font-size:3.6mm;letter-spacing:.16em;text-align:right;line-height:1.6;color:#6E6A64}
h1{font-size:15mm;margin-top:14mm}
.en{font-family:Jost;font-size:6mm;margin-top:2mm}
.body{font-size:5.2mm;line-height:1.6;margin-top:8mm}
.body .en{font-size:4.2mm;color:#4A4542;line-height:1.5;margin-top:2mm}
.facts{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:9mm}
.fact{background:#FBF8F2;border-radius:3mm;padding:4mm}
.fact b{font-family:Jost;font-weight:500;font-size:10mm;display:block;line-height:1.1}
.fact p{font-size:3.9mm;line-height:1.45;margin-top:1.5mm}
.fact .en{font-size:3.2mm;color:#6E6A64;margin-top:1mm}
.honest{margin-top:8mm;border-left:1.6mm solid #2A2725;padding:2mm 0 2mm 5mm;font-size:4.4mm;line-height:1.55}
.honest .en{font-size:3.6mm;color:#6E6A64;margin-top:1.5mm}
.row6{display:grid;grid-template-columns:repeat(6,1fr);gap:3mm;margin-top:9mm}
.row6 div{display:grid;gap:1mm;justify-items:center;font-family:Jost;font-weight:500;font-size:6mm}
.row6 .ph{width:100%;background-color:#FBF8F2;border-radius:2mm}
.steps{margin:9mm 0 0;padding:0;list-style:none;display:grid;gap:5mm}
.steps li{display:grid;grid-template-columns:11mm 1fr;gap:4mm;align-items:start;font-size:5.6mm;line-height:1.4}
.steps li>b{font-family:Jost;font-weight:500;background:#2A2725;color:#F4F0E8;border-radius:50%;width:11mm;height:11mm;display:grid;place-items:center;font-size:5.4mm}
.steps .en{display:block;font-family:Jost;font-size:4mm;color:#6E6A64;margin-top:.5mm}
.prize{margin-top:9mm;background:#E9A825;border-radius:4mm;padding:6mm 7mm}
.prize h2{font-size:9mm}
.prize p{font-size:4.6mm;margin-top:2mm}
.note{font-size:3.8mm;color:#6E6A64;margin-top:5mm;line-height:1.5;max-width:135mm}
.lineq{position:absolute;right:16mm;bottom:16mm;display:grid;justify-items:center;gap:1.5mm;font-family:Jost;font-size:4mm}
.lineq .qr{width:30mm;height:30mm}
/* collector cards: four A6 cards per sheet, cut on the dashed lines */
.cards{padding:0;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;background:#fff}
.card{position:relative;background:#F4F0E8;padding:7mm 7mm 0;border:.3mm dashed #B8B0A4;overflow:hidden}
.card .logo{width:15mm;height:15mm}
.card h3{font-size:6.6mm;margin-top:4mm}
.card .en{font-size:3.4mm;margin-top:.5mm;color:#6E6A64}
.slots{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:5mm}
.slot{background:#FBF8F2;border:.35mm solid #DCD4C7;border-radius:2mm;padding:1.5mm 1.5mm 2mm;display:grid;justify-items:center;gap:.5mm}
.slot svg{width:13mm;height:13mm}
.slot svg *{stroke:#8C8A85!important}
.slot b{font-family:Jost;font-weight:500;font-size:4mm;line-height:1}
.slot i{font-style:normal;font-size:2.4mm;color:#8C8A85;border-top:.25mm solid #DCD4C7;width:100%;text-align:center;padding-top:.8mm}
.card .rw{margin-top:4mm;font-size:3.2mm;line-height:1.45}
.card .no{margin-top:2.5mm;font-family:Jost;font-size:3.4mm}
.card .band{height:2.4mm}
/* staff card */
.staff h2{font-size:6.4mm;margin:7mm 0 2mm}
.staff ul{margin:0;padding-left:6mm;font-size:4.5mm;line-height:1.6}
.staff .say{font-size:4.8mm;line-height:1.5;background:#FBF8F2;border-left:1.5mm solid #2A2725;padding:3mm 4mm;margin:0}
"""


def ev():
    return '<p class="ev">SUSTAINABILITY EXPO 2026<br>6–15 NOV · QSNCC</p>'


def signs():
    facts = "".join(f'<div class="fact"><b>{n}</b><p>{th}</p><p class="en">{en}</p></div>' for n, th, en in FACTS)
    row6 = "".join(f'<div>{photo(c, pl)}{c}</div>' for c, _, _, pl in PATTERNS)
    p1 = f'''<section class="pg">{logo()}{ev()}
<h1>หนังที่เหลือ ได้ชีวิตที่สอง</h1><p class="en">Leftover leather, a second life.</p>
<div class="body"><p>{STORY_TH}</p><p class="en">{STORY_EN}</p></div>
<div class="facts">{facts}</div>
<div class="honest" style="max-width:135mm"><p>{HONEST_TH}</p><p class="en">{HONEST_EN}</p></div>
<div class="lineq">{qr(LINE)}LINE {LINE_ID}</div>
{band()}</section>'''

    p2 = f'''<section class="pg">{logo()}{ev()}
<h1>สะสมครบ 6 ลาย</h1><p class="en">Collect all six patterns.</p>
<div class="row6">{row6}</div>
<ol class="steps">
<li><b>1</b><span>รับบัตรสะสมที่บูธ ฟรี<span class="en">Take a free collector card.</span></span></li>
<li><b>2</b><span>ซื้อชิ้นหนัง เลือกลายเองทุกชิ้น พี่ที่บูธเซ็นช่องลายนั้นให้<span class="en">Pick any pattern you buy. We sign its box.</span></span></li>
<li><b>3</b><span>ครบ 01 02 03 04 05 07 เมื่อไร ยื่นบัตรที่บูธ<span class="en">Fill all six boxes, bring the card back.</span></span></li>
</ol>
<div class="prize"><h2>{REWARD_TH}</h2><p class="latin">Full card: {REWARD_EN}.</p></div>
<p class="note">ไม่มีการสุ่ม ทุกคนเลือกลายเองและสะสมครบได้ · บัตรใช้ได้ทุกบูธของ OCT. 26 · ถ่ายรูปบัตรเก็บไว้ หรือส่งใน LINE กันบัตรหาย</p>
<div class="lineq">{qr(LINE)}LINE {LINE_ID}</div>
{band()}</section>'''

    slots = "".join(f'<div class="slot">{drawing(c)}<b>{c}</b><i>เซ็น · วันที่</i></div>' for c, _, _, _ in PATTERNS)
    card = f'''<div class="card">{logo()}<h3>บัตรสะสม 6 ลาย</h3><p class="en">Collector card · 01–07</p>
<div class="slots">{slots}</div>
<p class="rw"><b>ครบ 6 ช่อง:</b> {REWARD_TH}</p>
<p class="no">No. ______ · {WEB} · LINE {LINE_ID}</p>{band()}</div>'''
    p3 = f'<section class="pg cards">{card * 4}</section>'

    p4 = f'''<section class="pg staff">{logo()}<h1 style="margin-top:8mm;font-size:12mm">สำหรับพี่ที่บูธ</h1><p class="note" style="margin-top:2mm">เก็บไว้หลังโต๊ะ ไม่ต้องตั้งโชว์</p>
<h2>บัตรสะสม</h2>
<ul><li>แจกบัตรฟรีให้คนที่ซื้อชิ้นแรก หรือคนที่ขอ</li>
<li>ซื้อชิ้นไหน เซ็นชื่อย่อกับวันที่ในช่องเลขนั้น 1 ช่องต่อ 1 ชิ้น ลายซ้ำไม่ได้ช่องเพิ่ม</li>
<li>บัตรครบ 6 ช่อง: ให้เลือกชิ้นฟรี 1 ชิ้น เขียนเลขนักสะสมบนบัตรเรียงจาก 001 แล้วจดเลขกับวันที่ในสมุดบูธ ขีดฆ่าบัตรว่าใช้แล้ว</li>
<li>ไม่สุ่ม ไม่ต้องลุ้น ห้ามบอกว่ามีลายลับหรือลายหายาก</li></ul>
<h2>ถ้ามีคนถามเรื่องความยั่งยืน ตอบตามนี้</h2>
<p class="say">หนังวัวแท้ที่เหลือจากโรงงานครับ เราเอามาตัดเป็นชิ้นด้วยบล็อกของเราเอง หนังฟอกแบบทั่วไป ไม่ได้รักษ์โลกพิเศษ แต่เราใช้ของที่มีอยู่แล้วให้คุ้มก่อนซื้อใหม่ ใช้รองแก้วได้ แต่ไม่ใช่ภาชนะใส่อาหาร</p>
<h2>คำที่ห้ามพูด</h2>
<ul><li>หนังรักษ์โลก หนังออร์แกนิก ฟอกธรรมชาติ ฟอกฝาด ย่อยสลายได้ ปลอดสารเคมี</li>
<li>ใช้กับอาหารได้ ต่อเองได้ไม่ต้องเย็บ ของเล่นเด็ก</li>
<li>Zero waste หรือตัวเลขลดคาร์บอน (เราไม่ได้วัด)</li></ul>
<p class="note">ตัวเลขที่พูดได้: เศษหนังที่ยังเหลือ 7 กก. · ตัดเป็นชิ้นได้ 37% ของน้ำหนัก · ต้นทุนชิ้นละ 3.45–4.22 บาท (ไม่ต้องบอกลูกค้า)</p>
</section>'''
    body = p1 + p2 + p3 + p4
    return f'<!doctype html><html lang="th"><meta charset="utf-8"><title>OCT. 26 SX2026 signs</title><style>{css("A4", "210mm", "297mm", SIGN_CSS)}</style>{body}</html>'


if __name__ == "__main__":
    open(os.path.join(HERE, "poster.html"), "w", encoding="utf-8").write(poster())
    open(os.path.join(HERE, "signs.html"), "w", encoding="utf-8").write(signs())
    print("poster.html, signs.html")
