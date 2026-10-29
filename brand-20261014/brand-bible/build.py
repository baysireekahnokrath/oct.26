"""OCT. 26 Brand Bible (28 Oct 2026), laid out after the ASE Brand Bible the owner shared as the model.

Part A, Brand Strategy Development: situation, competition, brand shift, value, value links, differentiation,
new possibilities, inspiring visuals.  Part B, Brand Artistic Development: brand idea, naming, roles, logo, type,
colour, architecture, pattern library, photography, applications, rules.
Everything states what is true in the status doc on 28 Oct; open decisions are marked as waiting.

python3 build.py -> bible.html;  node render.cjs -> OCT26-Brand-Bible.pdf and preview/pNN.png
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.dirname(HERE)
ROOT = os.path.dirname(BRAND)
sys.path.insert(0, os.path.join(BRAND, "brandbook-v2"))
from palette import BASE, FAMILY, C, BAND  # noqa: E402

FONTS = os.path.join(BRAND, "fonts")
LOGO = os.path.join(BRAND, "brandbook-v2", "logo", "svg")
DRAW = os.path.join(ROOT, "pattern-intro-20261022", "drawings")
PLAN = os.path.join(HERE, "assets", "plan")
A = os.path.join(HERE, "assets")
DATE = "29 ต.ค. 2569"


def f(path):
    """file:// URL; screenshots from other folders get a small JPG copy in assets/app so the PDF stays light."""
    if path.endswith(".png") and not path.startswith(A):
        from PIL import Image
        out = os.path.join(A, "app", os.path.basename(path)[:-4] + ".jpg")
        if not os.path.exists(out):
            os.makedirs(os.path.dirname(out), exist_ok=True)
            im = Image.open(path).convert("RGB")
            im.thumbnail((1000, 1000))
            im.save(out, quality=82)
        path = out
    return "file://" + path


def asset(name):
    return f(os.path.join(A, name + ".jpg"))


def logo(name, cls="lg"):
    s = open(os.path.join(LOGO, name + ".svg")).read()
    return re.sub(r' width="[\d.]+" height="[\d.]+"', f' class="{cls}"', s, count=1)


def drawing(code, kind="line"):
    n = {"01": "bear", "02": "pinwheel", "03": "capsule-cross", "04": "rounded-square", "05": "circle", "07": "round-joint-cross"}[code]
    s = open(os.path.join(DRAW, f"pattern-{code}-{n}-{kind}.svg")).read()
    return re.sub(r' width="[\d.]+mm" height="[\d.]+mm"', ' class="dr"', s, count=1)


def band(h="2.2mm", w="100%"):
    return f'<div class="band" style="height:{h};width:{w}">' + "".join(f'<i style="background:{c}"></i>' for c in BAND) + "</div>"


PATTERNS = [("01", "หมี", "Bear", "104 × 104"), ("02", "กังหัน", "Pinwheel", "90 × 90"), ("03", "กากบาทแคปซูล", "Capsule cross", "90 × 90"),
            ("04", "สี่เหลี่ยมมน", "Rounded square", "90 × 90"), ("05", "วงกลม", "Circle", "90 × 90"), ("07", "กากบาทข้อต่อวงกลม", "Round-joint cross", "90 × 90")]

CSS = f"""
@font-face{{font-family:Jost;src:url({f(FONTS + '/alt/Jost-Regular.ttf')})}}
@font-face{{font-family:Jost;font-weight:500;src:url({f(FONTS + '/alt/Jost-Medium.ttf')})}}
@font-face{{font-family:Anuphan;font-weight:500;src:url({f(FONTS + '/alt/Anuphan-Medium.ttf')})}}
@font-face{{font-family:Plex;src:url({f(FONTS + '/IBMPlexSansThai-Regular.ttf')})}}
@font-face{{font-family:Plex;font-weight:600;src:url({f(FONTS + '/IBMPlexSansThai-SemiBold.ttf')})}}
@page{{size:297mm 210mm;margin:0}}
*{{box-sizing:border-box}} html,body{{margin:0}}
body{{font-family:Plex,sans-serif;color:{C['charcoal']};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.p{{width:297mm;height:210mm;position:relative;overflow:hidden;background:#FBF9F5;page-break-after:always}}
.p:last-child{{page-break-after:auto}}
.run{{position:absolute;top:6mm;left:0;right:0;text-align:center;font-family:Jost;font-weight:500;font-size:2.1mm;letter-spacing:.3em;color:{C['stone']}}}
.rule{{position:absolute;top:11mm;left:14mm;right:14mm;border-top:.25mm solid {C['charcoal']}}}
.no{{position:absolute;bottom:6mm;left:0;right:0;text-align:center;font-family:Jost;font-size:2.4mm;color:{C['stone']}}}
.side{{position:absolute;left:14mm;top:15mm;width:62mm;display:grid;gap:1mm}}
.side b{{font-family:Jost;font-weight:500;font-size:4.4mm;line-height:1.05;letter-spacing:.02em;text-transform:uppercase}}
.side span{{font-family:Anuphan;font-weight:500;font-size:3.2mm;color:{C['stone']}}}
.side small{{font-family:Jost;font-size:2.2mm;letter-spacing:.12em;color:{C['stone']};text-transform:uppercase;line-height:1.5}}
.body{{position:absolute;left:84mm;right:14mm;top:15mm;bottom:15mm}}
.body.full{{left:14mm;top:34mm}}
.pill{{display:inline-block;border:.3mm solid {C['charcoal']};border-radius:4mm;padding:1.6mm 4mm;font-family:Anuphan;font-weight:500;font-size:3.6mm;line-height:1.3}}
.pill em{{display:block;font-style:normal;font-family:Jost;font-size:2.4mm;color:{C['stone']}}}
h2{{font-family:Anuphan;font-weight:500;font-size:7mm;line-height:1.2;margin:0}}
h3{{font-family:Anuphan;font-weight:500;font-size:4.2mm;margin:0;line-height:1.3}}
p{{margin:0;font-size:3.1mm;line-height:1.65}}
.muted{{color:{C['stone']}}}
.latin{{font-family:Jost}}
ul{{margin:0;padding-left:4.5mm;font-size:3.1mm;line-height:1.65}}
.grid{{display:grid;gap:5mm}}
.card{{background:#fff;border:.25mm solid #DCD4C7;border-radius:3mm;padding:4mm 5mm;display:grid;gap:1.6mm;align-content:start}}
.dark{{background:{C['charcoal']};color:{C['cotton']}}}
.dark .run,.dark .no{{color:#A9A39A}} .dark .rule{{border-color:#6E6A64}}
.dark .side span,.dark .side small{{color:#A9A39A}}
.ph{{background-size:cover;background-position:center}}
.band{{display:flex}} .band i{{flex:1}}
.lg{{display:block}}
.dr{{display:block;width:100%;height:100%}}
.big{{font-family:Jost;font-size:9mm;line-height:1.15;letter-spacing:-.01em}}
.th-big{{font-family:Anuphan;font-weight:500;font-size:8mm;line-height:1.25}}
.num{{font-family:Jost;font-weight:500;font-size:11mm;line-height:1}}
.tag{{display:inline-block;font-size:2.4mm;border-radius:2mm;padding:.4mm 2mm;background:{C['cotton']};border:.25mm dashed {C['stone']}}}
table{{border-collapse:collapse;width:100%;font-size:3mm}}
td,th{{border-top:.25mm solid #DCD4C7;padding:2.4mm 2mm;text-align:left;vertical-align:top}}
th{{font-family:Jost;font-weight:500;font-size:2.4mm;letter-spacing:.1em;color:{C['stone']};text-transform:uppercase;border-top:.35mm solid {C['charcoal']}}}
"""

A_SIDE = ("Brand Strategy<br>Development", "การพัฒนากลยุทธ์แบรนด์")
B_SIDE = ("OCT. 26", "New possibilities · brand identity and brand communication guideline")
pages = []


def page(body, side=A_SIDE, cls="", topic=None, full=False):
    n = len(pages) + 1
    s = ""
    if side:
        if side is B_SIDE:
            s = f'<div class="side"><b>{side[0]}</b><small>{side[1]}</small>{f"<small style=margin-top:3mm>{topic}</small>" if topic else ""}</div>'
        else:
            s = f'<div class="side"><b>{side[0]}</b><span>{side[1]}</span></div>'
    pages.append(f'<section class="p {cls}"><div class="run">OCT. 26 BRAND BIBLE</div><div class="rule"></div>{s}'
                 f'<div class="body{" full" if full else ""}">{body}</div><div class="no">{n:02d}</div></section>')


def raw(html):
    pages.append(html)


def topic(th, en):
    return f'<div class="pill">{th}<em>{en}</em></div>'


# ------------------------------------------------------------------ cover
raw(f'''<section class="p" style="background:{C['cotton']}">
<div style="position:absolute;left:30mm;top:50mm;width:62mm;height:62mm">{logo("square-light")}</div>
<div style="position:absolute;left:30mm;top:50mm;width:62mm;height:62mm;outline:.3mm solid {C['charcoal']}"></div>
<div style="position:absolute;left:104mm;top:52mm;display:grid;gap:3mm">
<p class="latin" style="font-size:3mm;letter-spacing:.3em;color:{C['stone']}">BRAND BIBLE</p>
<h2 style="font-size:12mm">คัมภีร์แบรนด์ OCT. 26</h2>
<p class="latin" style="font-size:5mm">quiet outside, family inside.</p>
<p style="font-family:Anuphan;font-size:4.6mm">เรียบข้างนอก บ้านอยู่ข้างใน</p></div>
<div style="position:absolute;left:30mm;bottom:22mm;display:grid;gap:1mm"><p class="muted">ฉบับ {DATE} · ต่อจาก Brand Book v2 (22 ต.ค.) · จัดเล่มตามแบบ Brand Bible ของ ASE</p></div>
<div style="position:absolute;left:0;right:0;bottom:0">{band("6mm")}</div></section>''')

# ------------------------------------------------------------------ A divider
page(f'''<div style="position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr;gap:12mm;align-items:center">
<div><p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">PART A</p><h2 style="font-size:10mm">A) BRAND STRATEGY<br>DEVELOPMENT</h2><p style="font-family:Anuphan;font-size:5mm;margin-top:2mm">การพัฒนากลยุทธ์แบรนด์</p></div>
<div class="grid" style="gap:2.6mm">
{"".join(topic(t, e) for t, e in [("วิเคราะห์ความเป็นปัจจุบันของแบรนด์", "Current Situation Analysis"), ("ความท้าทายทางการแข่งขัน", "Competitive Challenges"),
 ("การเปลี่ยนนิยามของแบรนด์", "Brand Shift"), ("คุณค่าที่โดดเด่นและความได้เปรียบ", "Value Uniqueness and Competitive Advantages"),
 ("การเชื่อมโยงคุณค่าอย่างมีความหมาย", "Brand Meaningful Value Connecting"), ("กลยุทธ์ความแตกต่างและคุณค่าที่ยั่งยืน", "Strategic Differentiation & Sustainable Value Proposition"),
 ("ความเป็นไปได้ใหม่ของแบรนด์", "Brand New Possibilities : Portfolio and Experience"), ("ภาพแห่งแรงบันดาลใจของแบรนด์", "Brand Inspiring Visuals")])}
</div></div>''', side=None, full=True)

# ------------------------------------------------------------------ A1 situation in brief
facts = [("ต.ค. 2569", "เริ่มขายครั้งแรก ที่บูธ KIDS MARKET งานบ้านและสวนแฟร์ อิมแพ็ค"), ("6", "แพตเทิร์นที่ตัดจริง 01–05 และ 07 (ไม่มี 06)"),
         ("1,169", "ชิ้นหนังที่ตัดรอบแรก · หนังเหลืออีก 7 กก."), ("3.45–4.22", "บาท ต้นทุนชิ้นหนังต่อชิ้น"),
         ("8,313", "บาท เงินที่ลงไปแล้ว (หนัง บล็อกตัด ค่าตัด)"), ("6", "ช่องทาง: บูธ · Shopee · LINE OA · IG · Facebook · oct26brand.com")]
page(f'''{topic("วิเคราะห์ความเป็นปัจจุบันของแบรนด์ (แบบกระชับ)", "Current Situation Analysis : in brief")}
<div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:7mm;gap:5mm">
{"".join(f'<div class="card"><span class="num">{n}</span><p>{t}</p></div>' for n, t in facts)}</div>
<p style="margin-top:6mm;max-width:170mm">OCT. 26 คือแบรนด์ของครอบครัว ชื่อมาจากวันเกิดของแม่ (คุณบิ๊ง) ทำของใช้ชิ้นเล็กจากเศษหนังวัวแท้ที่เหลือจากโรงงาน พ่อเบออกแบบแพตเทิร์นและบล็อกตัด ทั้งบ้านช่วยกันคัดหนัง แพ็ก และขาย ตอนนี้ขายเป็นชิ้นเดียว (ชิ้นหนังเปล่าและที่รองแก้ว) ส่วนสินค้าที่ต้องต่อชิ้นยังไม่ผ่านการทดสอบ</p>''')

# ------------------------------------------------------------------ A1 in depth
page(f'''{topic("วิเคราะห์ความเป็นปัจจุบันของแบรนด์ (เชิงลึก)", "Current Situation Analysis : in depth")}
<div class="grid" style="grid-template-columns:1fr 1fr;margin-top:7mm">
<div class="card"><h3>สิ่งที่เรามี</h3><ul>
<li>หนังวัวแท้ ทุกชิ้นสีและผิวไม่ซ้ำกัน เพราะมาจากหนังคนละผืน</li>
<li>บล็อกตัดของเราเอง 6 แบบ ขนาดแม่นทุกชิ้น มีเลข 01–07 จำง่าย</li>
<li>เรื่องจริงของครอบครัว 5 คน 5 สี ทำกันเองทั้งบ้าน</li>
<li>ต้นทุนชิ้นต่ำ ขายราคาเข้าถึงได้ (ชิ้นหนังที่บูธ 30 บาท)</li>
<li>เครื่องมือพร้อม: เว็บ หน้าขายของหน้างาน บัญชีและสต็อก เกมบูธ LINE</li></ul></div>
<div class="card"><h3>สิ่งที่ยังติด</h3><ul>
<li>ข้อต่อชิ้นยังไม่ผ่านการทดสอบ 5 ข้อ ขายได้แค่สินค้าชิ้นเดียว</li>
<li>หนังผ่านการฟอกด้วยสารเคมี ห้ามโดนอาหาร เครื่องดื่ม หรือปาก และไม่ทำของเด็กเล็ก</li>
<li>คนยังรู้จักน้อย ลิงก์ร้าน Shopee ยังไม่มี เพื่อนใน LINE ยังไม่ได้บรอดแคสต์</li>
<li>ยังไม่มีรูปจริงของ 02 · ความหมายของ SOI. 02 รอตัดสิน</li>
<li>ทีมคือครอบครัว เวลาทำงานมีจำกัด</li></ul></div></div>''')

# ------------------------------------------------------------------ A2 competition
page(f'''{topic("ความท้าทายทางการแข่งขัน", "Competitive Challenges")}
<div class="grid" style="grid-template-columns:repeat(3,1fr);margin-top:7mm">
<div class="card"><h3>ของจิ๋วหนังเทียมราคาถูก</h3><p>ที่รองแก้วและพวงกุญแจหนัง PU ในร้านออนไลน์ ราคาต่ำกว่าเรา</p><p class="muted">เราชนะด้วย: หนังแท้ ผิวจริง ไม่ซ้ำสักชิ้น และเรื่องของบ้าน</p></div>
<div class="card"><h3>เครื่องหนังแฮนด์เมดเย็บมือ</h3><p>กระเป๋าและของใช้หนังงานเย็บ ราคาสูง คนซื้อเพราะฝีมือช่าง</p><p class="muted">เราไม่แข่งงานเย็บ เราขายชิ้นที่ตัดแม่น ราคาเริ่มต้นต่ำ ซื้อเป็นของขวัญเล็ก ๆ ได้</p></div>
<div class="card"><h3>เวิร์กช็อปงานคราฟต์</h3><p>คลาสทำของเองที่ต้องจองและจ่ายค่าเรียน</p><p class="muted">เราให้ชิ้นหนังสำเร็จที่แต่งต่อได้ทันที ที่บูธหรือที่บ้าน</p></div></div>
<div class="card" style="margin-top:6mm;background:{C['cotton']}"><h3>ความท้าทายหลัก</h3><p>ทำให้คนจำว่า "ชิ้นหนังเลข 01–07 ของ OCT. 26" ไม่ใช่ "ที่รองแก้วหนังทั่วไป" และทำให้ราคาเล็กกลายเป็นการซื้อซ้ำจนครบชุด</p></div>''')

# ------------------------------------------------------------------ A3 brand shift
rows = [("คุณค่าใหม่ที่สอดคล้อง", "Honest / Numbered / Quiet", "วัสดุจริง / มีเลข มีระบบ / เรียบ ไม่ตะโกน"),
        ("คำมั่นสัญญาใหม่", "Real leather / One of a kind / Made at home", "หนังแท้ / ไม่ซ้ำสักชิ้น / ทำกันเองทั้งบ้าน"),
        ("นิยามเดิมที่เก็บไว้", "Leftover / Hand-picked / Family", "เศษหนังจากโรงงาน / คัดทีละชิ้น / ครอบครัว")]
page(f'''<div style="text-align:center;display:grid;gap:2mm;margin-top:4mm"><p class="latin" style="font-size:4.6mm;font-weight:500">OCT. 26</p><p class="muted">จากเศษหนังโรงงาน สู่ป้ายงานคราฟต์ของครอบครัว (shifting to a family craft label)</p></div>
<div class="grid" style="margin:8mm auto 0;max-width:150mm;gap:5mm">
{"".join(f'<div class="card" style="text-align:center;border-radius:6mm"><p style="color:{C["dad"]};font-family:Anuphan;font-size:3.4mm">{a}</p><p class="latin" style="font-size:4.4mm;font-weight:500">{b}</p><p class="muted">({c})</p></div>' for a, b, c in rows)}
</div>''')

# ------------------------------------------------------------------ A4 value uniqueness
vals = [("หนังวัวแท้จากเศษหนัง", "ของที่เหลือจากโรงงาน ได้ใช้ต่อแทนการทิ้ง"), ("บล็อกตัดของเราเอง", "6 แบบ ขนาดแม่น ชิ้นเหมือนกันทุกครั้ง เลขเดียวกันคือรูปเดียวกัน"),
        ("ทุกชิ้นไม่ซ้ำ", "สี ผิว และลายหนังต่างกันทุกชิ้น ลูกค้าได้ชิ้นของตัวเอง"), ("ระบบเลขที่สะสมได้", "01–07 ทำให้เก็บครบชุด ซื้อซ้ำ และเล่าต่อได้ง่าย"),
        ("เรื่องของบ้าน", "ห้าคน ห้าสี ซ่อนอยู่หลังป้าย ในการ์ด และในจุดสีเขียวของโลโก้")]
page(f'''{topic("คุณค่าที่โดดเด่นและความได้เปรียบทางการแข่งขัน", "Value Uniqueness and Competitive Advantages")}
<div class="grid" style="grid-template-columns:repeat(5,1fr);margin-top:8mm;gap:4mm">
{"".join(f'<div class="card"><span class="latin muted" style="font-size:2.6mm">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(vals))}</div>
<div style="margin-top:7mm;display:grid;grid-template-columns:repeat(6,1fr);gap:4mm">{"".join(f'<div style="aspect-ratio:1;background:url({f(os.path.join(PLAN, n + ".png"))}) center/contain no-repeat"></div>' for n in ("01-3", "03-1", "04-2", "05-6", "07-2", "05-4"))}</div>''')

# ------------------------------------------------------------------ A5 meaningful value
tri = f'''<svg viewBox="-30 0 260 170" style="width:100%;height:auto">
<polygon points="100,18 22,150 178,150" fill="none" stroke="{C['charcoal']}" stroke-width=".7"/>
<circle cx="100" cy="18" r="5" fill="{C['mom']}"/><circle cx="22" cy="150" r="5" fill="{C['beiya']}"/><circle cx="178" cy="150" r="5" fill="{C['bene']}"/>
<text x="100" y="8" text-anchor="middle" font-family="Anuphan" font-size="7">Brand Belief</text>
<text x="22" y="165" text-anchor="middle" font-family="Anuphan" font-size="7">Customer Connecting Value</text>
<text x="178" y="165" text-anchor="middle" font-family="Anuphan" font-size="7">Brand Connecting Value</text>
<text x="100" y="105" text-anchor="middle" font-family="Jost" font-size="9">our crafted things.</text></svg>'''
page(f'''{topic("การเชื่อมโยงคุณค่าอย่างมีความหมายของแบรนด์", "Brand Meaningful Value Connecting")}
<div style="display:grid;grid-template-columns:78mm 1fr;gap:8mm;margin-top:6mm;align-items:start"><div>{tri}</div>
<div class="grid" style="gap:3.5mm">
<div class="card"><p class="latin muted" style="font-size:2.6mm">BRAND BELIEF</p><h3>ของดีไม่ต้องดัง</h3><p>วัสดุจริงและการทำอย่างตั้งใจ พูดแทนเราได้ ไม่ต้องแต่งเกินจริง ไม่ต้องใช้หน้าการ์ตูน</p></div>
<div class="card"><p class="latin muted" style="font-size:2.6mm">CUSTOMER CONNECTING VALUE</p><h3>ชิ้นเล็กที่เป็นของคุณคนเดียว</h3><p>ของใช้ทุกวันที่ไม่ซ้ำใคร แต่งเองได้ เก็บสะสมได้ และให้เป็นของขวัญได้</p></div>
<div class="card"><p class="latin muted" style="font-size:2.6mm">BRAND CONNECTING VALUE</p><h3>บ้านที่ทำด้วยกัน</h3><p>ทุกชิ้นผ่านมือครอบครัว ลูกค้ามาที่บูธแล้วได้แต่งชิ้นหนังกับเรา เป็นส่วนหนึ่งของบ้าน</p></div>
<div class="card dark" style="text-align:center"><p class="latin" style="font-size:5.4mm">"quiet outside, family inside."</p><p style="color:#D8D2C8">เรียบข้างนอก บ้านอยู่ข้างใน</p></div>
</div></div>''')

# ------------------------------------------------------------------ A6 differentiation
axes = f'''<svg viewBox="0 0 220 160" style="width:100%;height:auto">
<line x1="20" y1="140" x2="210" y2="140" stroke="{C['charcoal']}" stroke-width=".6" marker-end="url(#a)"/>
<line x1="20" y1="140" x2="20" y2="10" stroke="{C['charcoal']}" stroke-width=".6" marker-end="url(#a)"/>
<defs><marker id="a" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{C['charcoal']}"/></marker></defs>
<circle cx="45" cy="120" r="10" fill="{C['stone']}" opacity=".5"/><text x="60" y="124" font-family="Plex" font-size="6.5">เศษหนังขายเป็นกิโล</text>
<circle cx="170" cy="35" r="14" fill="{C['mom']}"/><text x="170" y="38" text-anchor="middle" font-family="Jost" font-size="7" fill="{C['cotton']}">OCT. 26</text>
<path d="M55 112 Q110 90 156 44" fill="none" stroke="{C['charcoal']}" stroke-width=".5" stroke-dasharray="2 2"/>
<text x="24" y="16" font-family="Plex" font-size="6">คุณค่าในการทำ</text><text x="200" y="152" text-anchor="end" font-family="Plex" font-size="6">คุณค่าสู่ลูกค้า</text></svg>'''
page(f'''{topic("กลยุทธ์ความแตกต่างและจุดยืนอันทรงคุณค่าที่ยั่งยืน", "Brand Strategic Differentiation & Sustainable Brand Value Proposition")}
<div style="display:grid;grid-template-columns:90mm 1fr;gap:8mm;margin-top:6mm"><div>{axes}</div><div class="grid" style="gap:4mm">
<div><h3>เส้นตั้ง: คุณค่าในการทำ</h3><p>ยกจาก "เศษหนังที่เหลือจากโรงงาน" ไปสู่ "ชิ้นหนังที่ออกแบบด้วยบล็อกตัดของเราเอง มีเลข มีขนาดแม่น"</p></div>
<div><h3>เส้นขวาง: คุณค่าสู่ลูกค้า</h3><p>ยกจาก "ของถูกที่ใช้แล้วทิ้ง" ไปสู่ "ของใช้ชิ้นเล็กที่มีเรื่อง ใช้ได้นาน และเป็นของคุณคนเดียว"</p></div>
<div class="card" style="background:{C['cotton']}"><p class="latin" style="font-size:5mm;font-weight:500">Real leather. Numbered pieces. Made at home.</p><p>หนังแท้ ชิ้นมีเลข ทำกันเองที่บ้าน</p></div>
<p class="muted">ยั่งยืน: ใช้เศษหนังที่มีอยู่ให้ครบก่อนซื้อเพิ่ม (หนังเหลือ 7 กก.) ใช้หนังได้จริง 37% ของน้ำหนัก ส่วนที่เหลือเก็บไว้ทำชิ้นเล็กรอบต่อไป ไม่ทาสีขอบ</p></div></div>''')

# ------------------------------------------------------------------ A7 new possibilities
node = lambda t, s="", dark=False: f'<div class="card" style="text-align:center;padding:2.6mm 3mm;{"background:" + C["charcoal"] + ";color:" + C["cotton"] if dark else ""}"><h3 style="font-size:3.6mm">{t}</h3>{f"<p style=font-size:2.6mm>{s}</p>" if s else ""}</div>'
page(f'''{topic("ความเป็นไปได้ใหม่ของแบรนด์", "Brand New Possibilities : Brand Portfolio and Brand Experience")}
<div style="display:grid;gap:4mm;margin-top:6mm">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;align-items:start">
<div class="grid" style="gap:3mm">{node("OCT. 26", "แบรนด์ของแม่ แบรนด์เดียว", True)}
{node("SOI. 02 · คอลเลกชันแรก", "ความหมายรอเจ้าของเลือก (เสนอ: ชุดบล็อกตัด 01–07)")}
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3mm">{node("ชั้น 1", "ชิ้นเปล่า ลายละ 1 SKU")}{node("ชั้น 2", "ชิ้น + ของเพิ่มจริง")}{node("ชั้น 3", "ชุดที่จัดไว้ ไม่เกิน 2")}</div></div>
<div class="grid" style="gap:3mm">{node("แบรนด์ของลูก (ร่าง)", "ชื่อเสนอ บีสาม B3 · ตัวละคร นิทาน เกม · รอเด็ก ๆ ยืนยัน")}
{node("ประสบการณ์ของแบรนด์", "บูธ DIY แต่งชิ้นหนัง · เกมบนเว็บ + LINE · Shopee · oct26brand.com")}
{node("หลังผ่านการทดสอบข้อต่อ", "โคมไฟแขวน · ถาด 07 · กล่อง · ปลอกขวดน้ำ · กระเป๋า (สายใช้ของสำเร็จ)")}</div></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm">{"".join(f'<div style="height:44mm;border-radius:2mm" class="ph" title="{t}" ><div class="ph" style="height:100%;border-radius:2mm;background-image:url({asset(n)})"></div></div>' for n, t in [("proto-1-box-04-two-tone", "กล่องสองสี"), ("proto-2-bucket-bag", "กระเป๋าทรงถัง"), ("proto-3-tumbler-sleeve-07", "ปลอกขวดน้ำ"), ("proto-5-charm-07-four-piece", "ที่ห้อย")])}</div>
<p class="muted" style="font-size:2.6mm">ภาพต้นแบบที่เจ้าของลองทำ 23 ต.ค. ยังไม่ผ่านการทดสอบ 5 ข้อ ห้ามโฆษณาว่าต่อเองได้ไม่ต้องเย็บ</p></div>''')

# ------------------------------------------------------------------ inspiring visuals
raw(f'''<section class="p dark"><div class="run">OCT. 26 BRAND BIBLE</div><div class="rule"></div>
<div style="position:absolute;left:14mm;top:84mm"><h2 style="font-size:9mm;color:{C['cotton']}">ภาพแห่งแรงบันดาลใจของแบรนด์<br><span class="latin" style="font-size:6mm">(Brand Inspiring Visuals)</span></h2></div>
<div class="no">{len(pages) + 1:02d}</div></section>''')

collage = lambda names, cols, h: f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:2.5mm">' + "".join(f'<div class="ph" style="height:{h}mm;background-image:url({asset(n)})"></div>' for n in names) + "</div>"
page(f'''<p class="th-big" style="font-size:6mm">วัสดุพูดเอง <span class="latin muted" style="font-size:4mm">· the material speaks</span></p>
<div style="margin-top:5mm">{collage(["raw-04a", "raw-05", "raw-01", "raw-04b", "raw-03", "raw-05b"], 3, 64)}</div>''')
plan_grid = "".join(f'<div style="aspect-ratio:1;background:url({f(os.path.join(PLAN, n + ".png"))}) center/contain no-repeat"></div>'
                    for n in ["01-1", "01-2", "01-3", "01-4", "03-1", "03-2", "03-3", "03-4", "04-1", "04-2", "04-3", "04-5", "04-6", "04-9",
                              "05-1", "05-3", "05-4", "05-6", "05-8", "07-1", "07-2", "07-3", "07-4", "07-6"])
page(f'''<p class="th-big" style="font-size:6mm">ชิ้นมีเลข <span class="latin muted" style="font-size:4mm">· numbered pieces</span></p>
<div style="margin-top:5mm;display:grid;grid-template-columns:repeat(8,1fr);gap:3mm;background:{C['cotton']};padding:5mm;border-radius:3mm">{plan_grid}</div>''')
page(f'''<p class="th-big" style="font-size:6mm">ทำกันเองที่บ้าน <span class="latin muted" style="font-size:4mm">· made at home</span></p>
<div style="margin-top:5mm;display:grid;grid-template-columns:1.1fr 1fr 1fr 1fr;gap:2.5mm">
{"".join(f'<div class="ph" style="height:128mm;background-image:url({asset(n)})"></div>' for n in ["raw-hand", "proto-2-bucket-bag", "proto-5-charm-07-four-piece", "proto-1-box-04-two-tone"])}</div>''')

# ------------------------------------------------------------------ B divider
page(f'''<div style="position:absolute;inset:0;display:grid;align-content:center;gap:3mm">
<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">PART B</p><h2 style="font-size:10mm">B) BRAND ARTISTIC DEVELOPMENT</h2>
<p class="latin" style="font-size:4mm;letter-spacing:.1em">NEW POSSIBILITIES</p><p class="muted">Brand identity and brand communication guideline · อัตลักษณ์และแนวทางการสื่อสารแบรนด์</p>
<div style="margin-top:6mm;width:60mm">{band("3mm")}</div></div>''', side=None, full=True)

# ------------------------------------------------------------------ hero
raw(f'''<section class="p dark"><div class="ph" style="position:absolute;inset:0;background-image:url({asset("raw-hand")});background-position:center 60%;opacity:.85"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(42,39,37,.85),rgba(42,39,37,.15))"></div>
<div class="run" style="color:#D8D2C8">OCT. 26 BRAND BIBLE</div>
<div style="position:absolute;left:18mm;top:80mm;display:grid;gap:3mm"><p class="latin" style="font-size:12mm;line-height:1.05">quiet outside,<br>family inside.</p><p style="font-family:Anuphan;font-size:6mm">เรียบข้างนอก บ้านอยู่ข้างใน</p></div>
<div class="no" style="color:#D8D2C8">{len(pages) + 1:02d}</div></section>''')

# ------------------------------------------------------------------ core idea
page(f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:10mm;margin-top:4mm">
<div class="ph" style="height:160mm;background-image:url({asset("raw-05")})"></div>
<div style="display:grid;gap:5mm;align-content:center"><p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">CORE BRAND IDEA</p>
<p class="latin" style="font-size:6mm;line-height:1.35">Quiet is not empty.<br>It is what is left when everything else has been chosen with care.</p>
<p>OCT. 26 makes small, useful things from real leather offcuts, cut with our own dies, numbered, and finished at home by one family.</p>
<p style="font-family:Anuphan;font-size:4mm;line-height:1.6">เรียบไม่ได้แปลว่าว่างเปล่า แต่คือสิ่งที่เหลืออยู่เมื่อทุกอย่างถูกเลือกมาอย่างตั้งใจ OCT. 26 ทำของใช้ชิ้นเล็กจากเศษหนังวัวแท้ ตัดด้วยบล็อกของเราเอง มีเลขทุกแบบ และเสร็จด้วยมือของครอบครัวเดียว</p></div></div>''', side=B_SIDE)

# ------------------------------------------------------------------ naming and three layers
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">OCT. 26 NAMING MEANING</p>
<h2 style="margin-top:2mm">OCT. 26 · our crafted things.</h2><p class="muted">ชื่อแบรนด์คือวันเกิดของแม่ (คุณบิ๊ง) · ระบบสามชั้นที่แนะนำ (Recommended Three-Layer System)</p>
<div class="grid" style="gap:4mm;margin-top:6mm">
{"".join(f'<div class="card" style="grid-template-columns:48mm 1fr 62mm;align-items:center;border-radius:6mm"><span class="muted">{a}</span><span class="latin" style="font-size:4.6mm;font-weight:500">{b}</span><span>{c}</span></div>' for a, b, c in [
 ("Consumer Recall", "OCT. 26 · our crafted things.", "คำจำหลักที่คนทั่วไปเข้าใจได้ทันที"),
 ("Brand Communication Positioning", "quiet outside, family inside.", "เรียบข้างนอก บ้านอยู่ข้างใน พาแบรนด์จากเศษหนังไปสู่งานคราฟต์ของบ้าน"),
 ("Internal / Design DNA", "Honest. Useful. Hidden colour. Small batches.", "วัสดุพูดเอง · ใช้งานก่อน · สีซ่อนอยู่ · ทำทีละน้อย ใช้เป็นหลักคิดในการออกแบบ")])}
</div>''', side=B_SIDE)

# ------------------------------------------------------------------ naming breakdown
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">OCT. 26 NAMING MEANING</p>
<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:6mm;margin-top:6mm">
<div class="card"><span class="num">OCT.</span><h3>ตุลาคม เดือนของแม่</h3><ul><li>เดือนเกิดของแม่ เจ้าของแบรนด์</li><li>เดือนที่แบรนด์ขายครั้งแรก (ต.ค. 2569)</li><li>อ่านง่ายทั้งไทยและต่างชาติ</li></ul></div>
<div class="card"><span class="num">26</span><h3>ตัวเลขที่เป็นชื่อ</h3><ul><li>วันที่ 26 วันเกิดของแม่</li><li>แบรนด์ที่ใช้เลขเป็นชื่อ เข้ากับสินค้าที่ใช้เลขเป็นชื่อ (01 ที่รองแก้ว)</li><li>เลขจำง่ายกว่าคำบรรยาย</li></ul></div>
<div class="card"><span class="num" style="color:{C['mom']}">.</span><h3>จุดสีเขียวใบตอง</h3><ul><li>จุดในโลโก้คือสีของแม่ สีบ้านที่ซ่อนอยู่</li><li>หยุด จบ ไม่ต้องพูดเยอะ ตรงกับความเรียบของแบรนด์</li><li>บนพื้นดำใช้เขียวอ่อน #9DB777</li></ul></div></div>''', side=B_SIDE)

# ------------------------------------------------------------------ roles
roles = [("Maker", "ผู้ตัด", "บล็อกตัดของเราเอง ขนาดแม่น ชิ้นเหมือนกันทุกครั้ง"), ("Family", "บ้าน", "ห้าคน ห้าสี ทำกันเองทั้งบ้าน ลูกค้ามาแต่งชิ้นกับเราได้"),
         ("Pattern Library", "คลังแพตเทิร์น", "01–07 เลขที่จำได้ สะสมได้ ต่อยอดได้"), ("Second Life", "ชีวิตที่สองของหนัง", "เศษหนังจากโรงงาน ได้เป็นของใช้ที่อยู่ได้นาน")]
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">BRAND ROLE OF COMMUNICATION AND MESSAGING PILLARS</p>
<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:8mm">
{"".join(f'<div class="card" style="background:{C["cotton"]};min-height:90mm"><p class="latin" style="font-size:6mm;font-weight:500">{e}</p><h3>{t}</h3><p>{d}</p></div>' for e, t, d in roles)}</div>''', side=B_SIDE)
for (e, t, d, img), (e2, t2, d2, img2) in [((*roles[0], "raw-04a"), (*roles[1], "raw-hand")), ((*roles[2], "raw-03"), (*roles[3], "proto-2-bucket-bag"))]:
    half = lambda e, t, d, img: (f'<div style="position:relative;overflow:hidden"><div class="ph" style="position:absolute;inset:0;background-image:url({asset(img)})"></div>'
                                 f'<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(42,39,37,.88),rgba(42,39,37,.05) 60%)"></div>'
                                 f'<div style="position:absolute;left:10mm;right:10mm;bottom:16mm;display:grid;gap:1.5mm;color:{C["cotton"]}"><p class="latin" style="font-size:9mm">{e}</p><h3>{t}</h3><p>{d}</p></div></div>')
    raw(f'<section class="p dark"><div style="position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr">{half(e, t, d, img)}{half(e2, t2, d2, img2)}</div>'
        f'<div class="run" style="color:#D8D2C8">OCT. 26 BRAND BIBLE</div><div class="no" style="color:#D8D2C8">{len(pages) + 1:02d}</div></section>')

# ------------------------------------------------------------------ logo concept
raw(f'''<section class="p dark"><div class="run">OCT. 26 BRAND BIBLE</div><div class="rule"></div>
<div style="position:absolute;left:0;right:0;top:12mm;bottom:12mm;display:grid;grid-template-columns:1fr 1fr">
<div style="display:grid;place-items:center;border-right:.25mm solid #6E6A64"><div style="width:72mm">{logo("square-dark")}</div><p class="muted" style="margin-top:3mm;font-size:2.6mm;color:#A9A39A">โลโก้หลัก · สี่เหลี่ยม</p></div>
<div style="display:grid;place-items:center"><div style="width:100mm">{logo("line-dark")}</div><p class="muted" style="font-size:2.6mm;color:#A9A39A">โลโก้บรรทัดเดียว · ใช้ที่แคบ</p></div></div>
<div class="no">{len(pages) + 1:02d}</div></section>''')

S, M, H = 461.14, 61.80, 100
guides = (f'<svg viewBox="0 0 {S} {S}" style="position:absolute;inset:0;width:100%;height:100%">'
          f'<g stroke="{C["dad"]}" stroke-width="1.2" fill="none">'
          f'<line x1="{M}" y1="0" x2="{M}" y2="{S}"/><line x1="{S - M}" y1="0" x2="{S - M}" y2="{S}"/>'
          f'<line x1="0" y1="{199.67 - H}" x2="{S}" y2="{199.67 - H}"/><line x1="0" y1="199.67" x2="{S}" y2="199.67"/>'
          f'<line x1="0" y1="{361.47 - H}" x2="{S}" y2="{361.47 - H}"/><line x1="0" y1="361.47" x2="{S}" y2="361.47"/></g>'
          f'<g font-family="Jost" font-size="13" fill="{C["dad"]}"><text x="{M + 4}" y="20">M = H / φ</text><text x="6" y="{199.67 - H / 2}">H</text></g></svg>')
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">LOGO DEVELOPMENT · CONSTRUCTION</p>
<div style="display:grid;grid-template-columns:110mm 1fr;gap:10mm;margin-top:6mm;align-items:center">
<div style="position:relative;width:110mm;height:110mm;outline:.3mm solid {C['charcoal']}">{logo("square-light")}{guides}</div>
<div class="grid" style="gap:4mm"><h2>Proportion made for calm</h2>
<ul><li>OCT. อยู่เหนือ 26 ความสูงตัวอักษร (H) เท่ากันทั้งสองบรรทัด</li><li>ระยะขอบ M = H ÷ φ (อัตราส่วนทองคำ 1.618)</li><li>ด้านสี่เหลี่ยม 461.1 หน่วย ทุกขนาดคูณจากค่านี้</li><li>เส้นตัวอักษรหนาเท่ากันทุกตัว ไม่มีเงา ไม่มีขอบหนา</li><li>จุดหลัง OCT สีเขียวใบตอง (สีแม่) เป็นสีเดียวในโลโก้</li></ul>
<p class="muted">ไฟล์ต้นฉบับ: brand-20261014/brandbook-v2/logo/svg และโฟลเดอร์ Drive "OCT26-images/1-logo-svg"</p></div></div>''', side=B_SIDE)

variants = [("square-light", "หลัก บนพื้นสว่าง"), ("square-dark", "บนพื้นดำถ่าน"), ("square-leaf", "บนพื้นเขียวใบตอง"), ("square-family", "แบบมีห้าสี ใช้หลังป้าย การ์ด"),
            ("square-mono", "สีเดียว งานพิมพ์ ปั๊ม"), ("square-mono-white", "สีเดียวขาว บนรูปหรือพื้นเข้ม")]
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">LOGO VARIATIONS</p>
<div class="grid" style="grid-template-columns:repeat(6,1fr);gap:4mm;margin-top:8mm">
{"".join(f'<div style="display:grid;gap:2mm"><div style="aspect-ratio:1;padding:{0 if "mono" not in n else 3}mm;background:{C["charcoal"] if n == "square-mono-white" else "transparent"};outline:.25mm solid #DCD4C7">{logo(n)}</div><p style="font-size:2.6mm">{t}</p></div>' for n, t in variants)}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:8mm">
<div style="padding:6mm;outline:.25mm solid #DCD4C7"><div style="width:80mm">{logo("line-light")}</div></div>
<div style="padding:6mm;background:{C['charcoal']}"><div style="width:80mm">{logo("line-dark")}</div></div></div>''', side=B_SIDE)

donts = ["ห้ามยืดหรือบีบ", "ห้ามเปลี่ยนสีนอกพาเลต", "ห้ามใส่เงาหรือเส้นขอบ", "ห้ามวางบนรูปที่ลายเยอะจนอ่านไม่ออก", "ห้ามใส่หน้าหมี หัวใจ หรือโลโก้ห้าหมี", "ห้ามเขียนชื่อแบรนด์ใหม่ด้วยฟอนต์อื่น"]
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">CLEAR SPACE · MINIMUM SIZE · DON'TS</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10mm;margin-top:6mm">
<div class="grid" style="gap:4mm"><div style="position:relative;width:70mm;height:70mm;margin:12mm"><div style="position:absolute;inset:-12mm;border:.3mm dashed {C['dad']}"></div>{logo("square-light")}</div>
<p>พื้นที่ว่างรอบโลโก้อย่างน้อย = ความสูงตัวอักษร (H) ทุกด้าน</p><p>เล็กสุด: สี่เหลี่ยม 10 มม. บนงานพิมพ์ · 48 px บนจอ · บรรทัดเดียว 20 มม. / 96 px</p></div>
<div class="grid" style="grid-template-columns:repeat(2,1fr);gap:3mm;align-content:start">{"".join(f'<div class="card" style="border-color:{C["dad"]}"><p style="color:{C["dad"]};font-family:Jost;font-size:3mm">✕</p><p>{d}</p></div>' for d in donts)}</div></div>''', side=B_SIDE)

# ------------------------------------------------------------------ typography
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">TYPOGRAPHY</p>
<div style="display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:8mm;margin-top:6mm">
<div><p class="muted" style="font-size:2.6mm">Primary English & numbers · Jost 400 / 500</p><p class="latin" style="font-size:12mm;line-height:1.05">ABCDEFGHIJ<br>KLMNOPQRST<br>UVWXYZ</p><p class="latin" style="font-size:7mm;margin-top:2mm">0123456789</p><p class="latin" style="font-size:4mm;margin-top:2mm">our crafted things. 01 Coaster · SOI. 02</p></div>
<div><p class="muted" style="font-size:2.6mm">หัวข้อภาษาไทย · Anuphan Medium</p><p style="font-family:Anuphan;font-size:11mm;line-height:1.2">กขคง จฉชซ<br>เรียบข้างนอก</p><p style="font-family:Anuphan;font-size:5mm;margin-top:2mm">บ้านอยู่ข้างใน</p></div>
<div><p class="muted" style="font-size:2.6mm">เนื้อความ · IBM Plex Sans Thai 400 / 600</p><p style="font-size:5mm;line-height:1.5">กขคงจฉชซ<br>ABCDEFG abcdefg<br>0123456789</p><p style="margin-top:2mm">ใช้กับข้อความยาว ป้าย ราคา และหน้าเว็บ อ่านง่ายทั้งไทยและอังกฤษ</p></div></div>
<p class="muted" style="margin-top:8mm">ไม่ใช้ Mitr และฟอนต์ลายมือในงาน OCT. 26 (ฟอนต์ลายมือ Mali ใช้เฉพาะแบรนด์ของลูก)</p>''', side=B_SIDE)

# ------------------------------------------------------------------ colour
sw = lambda h, n, t, s, fg=C['charcoal']: f'<div style="display:grid;gap:1.4mm"><div style="height:30mm;background:{h};outline:.25mm solid #DCD4C7"></div><p style="font-family:Anuphan;font-size:3.4mm">{n}</p><p class="latin" style="font-size:2.6mm">{h}</p><p class="muted" style="font-size:2.5mm">{t}</p><p style="font-size:2.5mm">{s}</p></div>'
base_sw = "".join(sw(h, th, src.replace("หนังวัวฟอกฝาด", "หนังวัวแท้"), use) for _, th, h, src, use, _ in BASE)
fam_sw = "".join(sw(h, name, f"{who} · {bd}", src) for _, who, bd, name, h, src in FAMILY)
ratio = "".join(f'<div style="flex:{p};background:{h}"></div>' for h, p in [(C['cotton'], 60), (C['charcoal'], 20), (C['hide'], 15)]) + "".join(f'<div style="flex:1;background:{h}"></div>' for h in BAND)
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">BRAND COLOUR · สีจากธรรมชาติ</p>
<div class="grid" style="grid-template-columns:repeat(5,1fr);gap:4mm;margin-top:4mm">{base_sw}</div>
<p class="muted" style="margin-top:4mm;font-size:2.6mm">ห้าสีของบ้าน (ใช้ไม่เกิน 5% ซ่อนอยู่หลังป้าย ในการ์ด เส้นคาด)</p>
<div class="grid" style="grid-template-columns:repeat(5,1fr);gap:4mm;margin-top:2mm">{fam_sw}</div>
<div style="display:flex;height:6mm;margin-top:4mm;outline:.25mm solid #DCD4C7">{ratio}</div><p class="muted" style="font-size:2.6mm;margin-top:1mm">สัดส่วน 60 ขาวฝ้าย · 20 ดำถ่าน · 15 สีหนัง · 5 ห้าสีของบ้าน · ไม่ทาสีขอบหนัง ผิวและขอบปล่อยตามธรรมชาติ</p>''', side=B_SIDE)

# ------------------------------------------------------------------ architecture
skus = ["01 ที่รองแก้ว", "02 ที่รองแก้ว", "03 ป้ายห้อยของขวัญ", "04 ที่รองแก้ว", "05 ที่รองแก้ว", "ชุดที่รองแก้ว 01 · 02 · 04 · 05", "01 ที่เก็บสายชาร์จ"]
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">RECOMMENDED BRAND ARCHITECTURE</p>
<div class="grid" style="gap:0;margin-top:6mm">
{"".join(f'<div style="display:grid;grid-template-columns:80mm 1fr;gap:6mm;align-items:center;border-top:.3mm solid {C["charcoal"]};padding:4mm 0"><p class="latin" style="font-size:8mm;line-height:1">{a}</p><div><h3>{b}</h3><p>{c}</p></div></div>' for a, b, c in [
 ("OCT. 26", "แบรนด์หลัก แบรนด์เดียว", "ทุกสินค้าใช้โลโก้สี่เหลี่ยมเดียวกัน ไม่มีแบรนด์ย่อยแยกหน้าตา"),
 ("SOI. 02", "คอลเลกชันแรก (ความหมายรอตัดสิน)", "เสนอ A: ชุดบล็อกตัด 01–07 ที่เกิดในบ้านซอย 2 · ห้ามเขียนว่าเป็นรอบผลิต"),
 ("01–07", "แพตเทิร์น หนึ่งบล็อก หนึ่งเลข", "ไม่มี 06 (ไม่ได้ตัด ใช้ 07 แทนทุกที่)"),
 ("[เลข] + [หน้าที่]", "ชื่อสินค้า", " · ".join(skus)),
 ("B3 (ร่าง)", "แบรนด์ของลูก", "แยกจาก OCT. 26 เขียนเล็ก ๆ ว่าลูก ๆ ของ OCT. 26 · รอเด็ก ๆ ยืนยันชื่อ สี แพตเทิร์น")])}</div>''', side=B_SIDE)

# ------------------------------------------------------------------ colour variations on backgrounds
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">COLOUR VARIATIONS</p>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:6mm">
<div style="height:150mm;background:{C['cotton']};display:grid;place-items:center"><div style="width:42mm">{logo("square-light")}</div></div>
<div style="height:150mm;background:{C['charcoal']};display:grid;place-items:center"><div style="width:42mm">{logo("square-dark")}</div></div>
<div style="height:150mm;background:{C['mom']};display:grid;place-items:center"><div style="width:42mm">{logo("square-leaf")}</div></div>
<div class="ph" style="height:150mm;background-image:url({asset("raw-04b")});display:grid;place-items:center"><div style="width:42mm">{logo("square-mono-white")}</div></div></div>''', side=B_SIDE)

# ------------------------------------------------------------------ pattern library
cells = "".join(f'''<div class="card" style="gap:2mm;justify-items:center;text-align:center;min-width:0;padding:3mm"><div style="width:24mm;height:24mm">{drawing(c)}</div>
<div style="width:24mm;height:24mm;background:url({f(os.path.join(PLAN, (c + "-1.png") if c != "02" else "05-1.png"))}) center/contain no-repeat;{"opacity:0" if c == "02" else ""}"></div>
<span class="num" style="font-size:7mm">{c}</span><h3 style="font-size:3.4mm">{th}</h3><p class="latin muted" style="font-size:2.5mm">{en} · {mm} มม.</p>{'<span class="tag">ยังไม่มีรูปจริง</span>' if c == "02" else ""}</div>'''
                for c, th, en, mm in PATTERNS)
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">PATTERN LIBRARY · คลังแพตเทิร์น</p>
<div class="grid" style="grid-template-columns:repeat(6,1fr);gap:3mm;margin-top:5mm">{cells}</div>
<p class="muted" style="margin-top:4mm;font-size:2.6mm">ลายเส้นจากบล็อกตัดจริง 1:1 · รูปชิ้นจริงมุมแปลน สเกลเดียวกัน (OCT26-images/4-product-drawings-svg และ 5-pattern-pieces-webp) · ไม่มีเลข 06</p>''', side=B_SIDE)

# ------------------------------------------------------------------ photography
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">VISUAL EXPRESSION · ภาพถ่าย</p>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1.1fr;gap:4mm;margin-top:6mm">
<div class="ph" style="height:120mm;background-image:url({asset("raw-04a")})"></div>
<div style="height:120mm;background:{C['cotton']} url({f(os.path.join(PLAN, '05-6.png'))}) center/80% no-repeat"></div>
<div class="ph" style="height:120mm;background-image:url({asset("raw-hand")})"></div>
<div class="grid" style="gap:2.4mm;align-content:start"><h3>กติกาภาพ</h3><ul>
<li>วางบนกระดาษขาว A4 ทั้งแผ่น ชิ้นไม่ล้นขอบ</li><li>ถ่ายตรงจากด้านบน แสงจากหน้าต่าง ไม่เปิดแฟลช</li><li>ปรับสีโดยเทียบกับกระดาษขาว ไม่แต่งสีหนังเกินจริง</li>
<li>มือกับชิ้นหนังได้ ไม่ถ่ายหน้าเด็ก</li><li>ไม่ใช้ภาพที่ AI สร้าง เพราะไม่เหมือนของจริง</li><li>รูปลูกค้าต้องขออนุญาตก่อนลงเว็บ</li></ul></div></div>''', side=B_SIDE)

# ------------------------------------------------------------------ applications
RB = os.path.join(ROOT, "rebrand-20261022")
img = lambda p, h, contain=False: f'<div style="height:{h}mm;background:#fff url({f(p)}) center/{"contain" if contain else "cover"} no-repeat;outline:.25mm solid #DCD4C7"></div>'
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">BRAND APPLICATION · งานพิมพ์</p>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:6mm">
<div class="grid" style="gap:2mm">{img(os.path.join(RB, "print/tags-55x89-preview.png"), 120, True)}<p>ป้ายห้อย 55 × 89 มม. หลังป้ายมีห้าสี</p></div>
<div class="grid" style="gap:2mm">{img(os.path.join(RB, "print/insert-cards-89x55-preview.png"), 120, True)}<p>การ์ดในซอง 89 × 55 มม. วิธีดูแลและ QR LINE</p></div>
<div class="grid" style="gap:2mm">{img(os.path.join(RB, "print/stickers-34mm-preview.png"), 120, True)}<p>สติกเกอร์ 34 มม. ปิดซอง</p></div></div>''', side=B_SIDE)
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">BRAND APPLICATION · โซเชียล</p>
<div style="display:grid;grid-template-columns:1fr 1fr .62fr 1fr;gap:4mm;margin-top:6mm;align-items:start">
<div class="grid" style="gap:2mm">{img(os.path.join(RB, "social/card-OC-03-26.png"), 110, True)}<p>การ์ดสินค้า 1080 × 1350</p></div>
<div class="grid" style="gap:2mm">{img(os.path.join(ROOT, "pattern-intro-20261022/social/pattern-07.png"), 110, True)}<p>การ์ดแนะนำแพตเทิร์น</p></div>
<div class="grid" style="gap:2mm">{img(os.path.join(RB, "social/story-OC-05-28.png"), 110, True)}<p>สตอรี่ 1080 × 1920</p></div>
<div class="grid" style="gap:2mm">{img(os.path.join(RB, "social/fb-cover-1640x624.png"), 40, True)}<p>ปกเพจ Facebook</p>{img(os.path.join(RB, "social/profile-1080.png"), 50, True)}<p>รูปโปรไฟล์</p></div></div>''', side=B_SIDE)
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">BRAND APPLICATION · เว็บและบูธ</p>
<div style="display:grid;grid-template-columns:1.6fr .5fr 1fr;gap:5mm;margin-top:6mm;align-items:start">
<div class="grid" style="gap:2mm">{img(os.path.join(RB, "website-v2/preview-desk.png"), 120)}<p>เว็บ oct26brand.com</p></div>
<div class="grid" style="gap:2mm">{img(os.path.join(RB, "website-v2/preview-phone.png"), 120)}<p>บนมือถือ</p></div>
<div class="grid" style="gap:2mm">{img(os.path.join(ROOT, "booth-game-20261025/preview-1.png"), 120, True)}<p>ป้ายบูธ เพิ่มเพื่อน LINE รับชิ้นหนัง</p></div></div>''', side=B_SIDE)

# ------------------------------------------------------------------ rules
page(f'''<p class="latin muted" style="font-size:2.6mm;letter-spacing:.2em">BRAND RULES · กติกาที่ทุกทีมต้องรู้</p>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:6mm;margin-top:6mm">
<div class="card"><h3>สินค้า</h3><ul>
<li>ไม่ทำสินค้าที่โดนอาหาร เครื่องดื่ม หรือปาก · ที่รองแก้วขายได้ ป้ายเขียนว่าไม่ใช่ภาชนะใส่อาหาร</li>
<li>ไม่ทำของเล่นหรือของใช้เด็กเล็ก (อายุที่นับเป็นเด็กเล็กรอตัดสิน)</li>
<li>ใช้ 07 แทน 06 ทุกที่ · 06 ไม่ได้ตัด</li>
<li>ข้อต่อชิ้นยังไม่ผ่านการทดสอบ ขายเฉพาะชิ้นเดียว</li>
<li>ไม่ทาสีขอบหนัง</li></ul></div>
<div class="card"><h3>การสื่อสาร</h3><ul>
<li>ห้ามเขียน "ต่อเองได้ ไม่ต้องเย็บ" จนกว่าข้อต่อจะผ่าน</li>
<li>คำที่ห้ามใช้: ไม่ต้องเย็บ · ฟอกฝาด · ใช้กับอาหารได้</li>
<li>หมีเป็นสินค้าเด่น ไม่ใช่สัญลักษณ์แบรนด์ · ห้ามใส่หน้าหมี หัวใจ หรือโลโก้ห้าหมีในงานใหม่</li>
<li>SOI. 02 ห้ามเขียนว่าเป็นรอบผลิต</li>
<li>กิจกรรมไม่สุ่มรางวัล ไม่ให้แท็กเพื่อน ไม่บังคับรีวิวดี ไม่ใช้รูปที่เห็นหน้าเด็ก</li></ul></div></div>''', side=B_SIDE)

# ------------------------------------------------------------------ back cover
raw(f'''<section class="p dark"><div style="position:absolute;left:0;right:0;top:0;bottom:6mm;display:grid;place-items:center;align-content:center;gap:6mm">
<div style="width:56mm">{logo("square-dark")}</div><p class="latin" style="font-size:4.4mm">our crafted things.</p>
<p style="font-size:3mm;color:#D8D2C8">oct26brand.com · IG @oct.26_brand · FB oct26brand · LINE @155riuqj</p></div>
<div style="position:absolute;left:0;right:0;bottom:0">{band("6mm")}</div></section>''')

if __name__ == "__main__":
    html = f"<!doctype html><html lang='th'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
    open(os.path.join(HERE, "bible.html"), "w", encoding="utf-8").write(html)
    print(len(pages), "pages")
