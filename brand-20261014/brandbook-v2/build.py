"""OCT. 26 Brand Book v2 (22 Oct 2026): quiet outside, family inside.

One brand, square logo, colours from nature, products named by pattern number. A4 landscape, Thai.
python3 logo/build.py && node logo/render.cjs   -> square logo SVG/PNG
python3 build.py                                 -> brandbook.html
node render.cjs                                  -> OCT26-BrandBook-v2.pdf + preview/pNN.png
"""
import os, re
from palette import BASE, FAMILY, C, BAND

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")
LOGO = os.path.join(HERE, "logo", "svg")

def logo(name, size, extra=""):
    svg = open(os.path.join(LOGO, name + ".svg")).read()
    svg = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{size}" height="{size}"' if name.startswith("square") else f'height="{size}"', svg, count=1)
    return svg.replace("<svg ", f'<svg {extra} ', 1)

def band(h=8, w="100%"):
    return f'<div class="band" style="height:{h}px;width:{w}">' + "".join(f'<span style="background:{c}"></span>' for c in BAND) + "</div>"

SKUS = [  # SKU, new name, pattern, size, price (draft)
    ("OC-01-22", "01 ที่รองแก้ว", "01", "10.4 ซม.", 59),
    ("OC-01-01", "01 ที่เก็บสายชาร์จ", "01", "10.4 ซม.", 59),
    ("OC-02-24", "02 ที่รองแก้ว", "02", "9 ซม.", 49),
    ("OC-03-26", "03 ป้ายห้อยของขวัญ", "03", "9 ซม.", 39),
    ("OC-04-27", "04 ที่รองแก้ว", "04", "9 ซม.", 49),
    ("OC-05-28", "05 ที่รองแก้ว", "05", "9 ซม.", 49),
    ("OC-MX-29", "ชุดที่รองแก้ว 01 · 02 · 04 · 05", "MX", "4 ชิ้น", 179),
]

def shape(code, fill=None, size=46):
    fill = fill or C["hide"]
    d = {
        "01": f'<circle cx="11" cy="11" r="6" fill="{fill}"/><circle cx="29" cy="11" r="6" fill="{fill}"/><circle cx="20" cy="23" r="13" fill="{fill}"/>',
        "02": f'<path d="M20 20 L20 5 Q31 8 20 20Z M20 20 L35 20 Q32 31 20 20Z M20 20 L20 35 Q9 32 20 20Z M20 20 L5 20 Q8 9 20 20Z" fill="{fill}"/>',
        "03": f'<path d="M15 5h10v10h10v10H25v10H15V25H5V15h10z" fill="{fill}" rx="4"/>',
        "04": f'<rect x="7" y="7" width="26" height="26" rx="7" fill="{fill}"/>',
        "05": f'<circle cx="20" cy="20" r="14" fill="{fill}"/>',
        "07": f'<path d="M14 4h12v10h10v12H26v10H14V26H4V14h10z" fill="{fill}"/>',
        "MX": f'<circle cx="11" cy="11" r="7" fill="{fill}"/><rect x="23" y="4" width="14" height="14" rx="4" fill="{fill}"/><circle cx="11" cy="29" r="7" fill="{fill}"/><circle cx="29" cy="29" r="7" fill="{fill}"/>',
    }[code]
    return f'<svg viewBox="0 0 40 40" width="{size}" height="{size}" aria-hidden="true">{d}</svg>'

# ---------------------------------------------------------------- pages
def page(n, kicker, title, body, cls=""):
    return (f'<section class="p {cls}"><header class="ph"><span class="k">{kicker}</span><span class="pn">{n:02d}</span></header>'
            f'{f"<h1>{title}</h1>" if title else ""}<div class="body">{body}</div>'
            f'<footer class="pf"><span>OCT. 26 · Brand Book v2 · 22 ต.ค. 2569</span>{band(4, "60px")}</footer></section>')

def p_cover():
    return (f'<section class="p cover"><div class="cv">{logo("square-light", 260, "class='cvlogo'")}'
            '<div class="cvt"><p class="eyebrow">Brand Book · v2</p><h1 class="cvh">เรียบข้างนอก<br>บ้านอยู่ข้างใน</h1>'
            '<p class="latin big">quiet outside, family inside.</p><p class="muted">our crafted things. · 22 ต.ค. 2569</p></div></div>'
            f'<div class="cvband">{band(14)}</div></section>')

def p_story():
    fam = "".join(f'<div class="who"><i style="background:{h}"></i><b>{who}</b><span class="latin">{bd}</span><span class="muted">{name}</span></div>'
                  for _, who, bd, name, h, _ in FAMILY)
    return page(2, "เรื่องของเรา", "บ้านหนึ่งหลัง ห้าคน หนังที่เหลือจากโรงงาน",
        f'''<div class="cols"><div class="stack">
<p class="lead">OCT. 26 คือวันเกิดของแม่ แบรนด์จึงใช้ชื่อนี้ และหน้าตาของแบรนด์เป็นแบบที่แม่ชอบ เรียบ เท่ ตั้งใจ แบบ Paul Smith ของญี่ปุ่น และของสแกนดิเนเวีย</p>
<p>เราทำของใช้จากเศษหนังวัวแท้ที่เหลือจากโรงงาน พ่อออกแบบแพตเทิร์นและบล็อกตัด ทั้งบ้านช่วยกันคัดหนัง แพ็ก และขาย ทุกชิ้นสีไม่ซ้ำกัน เพราะมาจากหนังคนละผืน</p>
<p>คนในบ้านห้าคนมีสีของตัวเอง ห้าสีนี้ไม่อยู่หน้าแบรนด์ แต่ซ่อนอยู่ในรายละเอียด คนที่พลิกดูถึงจะเจอ</p></div>
<div class="fam">{fam}</div></div>''')

def p_idea():
    pillars = [("01", "วัสดุพูดเอง", "หนังแท้ ขอบตัดจริง ไม่ทาสีทับผิว ไม่มีหน้าตาการ์ตูน ภาพถ่ายเห็นผิวหนังชัด บอกตรง ๆ ว่ามาจากเศษหนัง"),
               ("02", "ใช้งานก่อน", "ทุกชิ้นตอบได้ในประโยคเดียวว่าใช้ทำอะไร ชื่อสินค้าคือเลขแพตเทิร์นกับหน้าที่"),
               ("03", "สีซ่อนอยู่", "ห้าสีของบ้านอยู่ในที่เล็ก ๆ หลังป้าย การ์ดในซอง เส้นคาดซอง ไม่ใช้เป็นพื้นใหญ่ ผิวและขอบหนังปล่อยตามธรรมชาติ"),
               ("04", "ทำทีละรอบ", "ผลิตเป็นรอบเล็ก ตั้งชื่อรอบว่า SOI. 02, SOI. 03 บอกจำนวนจริง ไม่รีบ ไม่ลดราคาแรง")]
    pl = "".join(f'<div class="pil"><span class="latin muted">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in pillars)
    return page(3, "แกนของแบรนด์", "เรียบข้างนอก บ้านอยู่ข้างใน",
        f'''<p class="lead" style="max-width:150mm">ของดูธรรมดาตอนแรก ยิ่งดูใกล้ยิ่งเห็นความตั้งใจ เหมือนซับในลายทางของ Paul Smith ความเงียบของงานญี่ปุ่น และความใช้งานได้จริงของสแกนดิเนเวีย</p>
<div class="pils">{pl}</div>
<p class="muted">ภาษาอังกฤษ: <span class="latin">quiet outside, family inside.</span> ใช้คู่กับ <span class="latin">our crafted things.</span></p>''')

def p_arch():
    return page(4, "โครงสร้างแบรนด์", "แบรนด์เดียว",
        f'''<div class="cols"><div class="tree">
<div class="node main">{logo("square-light", 54)}<div><b>OCT. 26 · our crafted things.</b><span class="muted">แบรนด์เดียว โลโก้เดียว ทุกสินค้าอยู่ใต้ชื่อนี้</span></div></div>
<div class="branch">
<div class="node"><b>สินค้า</b><span class="muted">ตั้งชื่อด้วยเลขแพตเทิร์นกับหน้าที่ เช่น 01 ที่รองแก้ว · 05 ที่รองแก้ว · 03 ป้ายห้อยของขวัญ</span></div>
<div class="node"><b>รอบผลิต SOI. 02, SOI. 03 …</b><span class="muted">SOI. 02 คือของรอบแรกทั้งหมด ตั้งตามซอยบ้าน ใช้บอกล็อต ไม่ใช่แบรนด์ย่อย</span></div>
<div class="node"><b>สินค้าเด่น</b><span class="muted">หมี (แพตเทิร์น 01) เป็นสินค้าเด่นตัวหนึ่ง ไม่ใช่สัญลักษณ์ของแบรนด์</span></div>
</div></div>
<div class="stack">
<div class="off"><b>พักไว้</b><p><b>ห้าหมี FIVE BEARS</b> และ <b>Love</b> ไม่ใช้ในงานใหม่ ไม่มีหน้าหมี หัวใจ หรือโลโก้ห้าหมีบนสื่อของ OCT. 26</p><p class="muted">ถ้าวันหนึ่งจะทำไลน์ตัวละคร ให้เปิดเป็นแบรนด์แยก ไม่ใช้ชื่อ OCT. 26</p></div>
<div class="off"><b>เลิกใช้</b><p>โลโก้ป้ายห้อย 26 โลโก้หมี ป้าย SOI. 02 แบบเดิม สี Soi Candy และฟอนต์ Mitr</p></div>
</div></div>''')

def p_logo():
    return page(5, "โลโก้", "โลโก้สี่เหลี่ยม",
        f'''<div class="cols"><div class="logobox">{logo("square-light", 330, "class='construct'")}</div>
<div class="stack">
<p class="lead">ตัวอักษรโลโก้เดิมที่วาดจากวงกลมและเส้นตรง เรียงสองบรรทัดในกรอบจัตุรัส จุดหลัง OCT เป็นสีของแม่</p>
<ul>
<li>บรรทัดบน OCT. บรรทัดล่าง 26 ความสูงตัวอักษรและความหนาเส้นเท่ากัน ชิดซ้าย</li>
<li>ระยะขอบรอบตัวอักษร = ความสูงตัวอักษร ÷ φ (1.618) ระยะระหว่างบรรทัดเท่ากัน</li>
<li>ด้านของจัตุรัส = ความกว้าง OCT. + ระยะขอบสองข้าง</li>
<li>ห้ามวางของอื่นในจัตุรัส ห้ามพิมพ์โลโก้ใหม่ด้วยฟอนต์ ใช้ไฟล์เท่านั้น</li>
<li>เล็กสุด 12 มม. บนกระดาษ · 24 px บนจอ</li>
</ul>
<p class="muted">ไฟล์: brand-20261014/brandbook-v2/logo/svg และ png (1080 กับ 256 px)</p></div></div>''')

def p_logo2():
    items = [("square-light", "หลัก บนพื้นขาวฝ้าย"), ("square-dark", "บนพื้นเข้ม"), ("square-leaf", "รูปโปรไฟล์ พื้นเขียวใบตอง"),
             ("square-family", "แบบมีแถบห้าสี ป้ายและแพ็กเกจ"), ("square-mono", "สีเดียว ตรายาง ปั๊มหนัง"), ("square-mono-white", "สีเดียว ขาว บนภาพ")]
    cells = "".join(f'<div class="lv"><div class="lvb{" dk" if "white" in n else ""}">{logo(n, 120)}</div><span>{t}</span></div>' for n, t in items)
    line = f'<div class="lv wide"><div class="lvb">{logo("line-light", 46)}</div><span>แบบบรรทัดเดียว ใช้เฉพาะที่แคบตามแนวนอน เช่น เมนูเว็บ ใบเสร็จ</span></div>'
    donts = ["เปลี่ยนสีจุดเป็นสีอื่นนอกจากสีแม่", "ยืด บีบ หรือหมุน", "ใส่เงาหรือขอบนูน", "วางบนรูปที่ลายยุ่ง", "ใส่หน้าหมีหรือหัวใจ", "เรียงใหม่เป็น 26 OCT."]
    return page(6, "โลโก้", "แบบต่าง ๆ",
        f'<div class="lvs">{cells}{line}</div><div class="dont"><b>ห้าม</b>{"".join(f"<span>× {d}</span>" for d in donts)}</div>')

def p_color():
    sw = "".join(f'<div class="sw"><i style="background:{h};{"box-shadow:inset 0 0 0 1px #DCD4C7" if k == "cotton" else ""}"></i><b>{th}</b><span>{src}</span><span class="muted">{use}</span><span class="latin muted">{h}</span></div>'
                 for k, th, h, src, use, _ in BASE)
    ratio = "".join(f'<span style="flex:{p};background:{C[k]}"></span>' for k, _, _, _, _, p in BASE if p) + "".join(f'<span style="flex:1;background:{c}"></span>' for c in BAND)
    return page(7, "สี", "สีจากธรรมชาติ",
        f'''<div class="sws">{sw}</div>
<div class="stack" style="gap:3mm"><b>สัดส่วนบนงานหนึ่งชิ้น</b><div class="ratio">{ratio}</div>
<p class="muted">ขาวฝ้ายราว 60% · ดำถ่าน 20% · สีหนังจริง 15% · ห้าสีของบ้านรวมกันไม่เกิน 5% · น้ำตาลไม้สักและเทาหินใช้แทนดำถ่านในที่รอง</p></div>''')

def p_family():
    sw = "".join(f'<div class="fsw"><i style="background:{h}"></i><b>{who} · {name}</b><span class="latin">{bd} · {h}</span><span class="muted">{src}</span></div>'
                 for _, who, bd, name, h, src in FAMILY)
    where = ["แถบห้าสีหลังป้ายห้อย", "หลังการ์ดในซอง", "เส้นคาดซองกระดาษคราฟต์", "แถบล่างโลโก้แบบมีแถบห้าสี",
             "ป้ายหมวดสินค้าและปุ่มเล็ก ๆ บนเว็บ", "จุดหลัง OCT ใช้สีแม่เท่านั้น"]
    return page(8, "สี", "ห้าสีของบ้าน",
        f'''<div class="fsws">{sw}</div>
<div class="cols"><div class="stack"><b>ใช้ที่ไหนได้</b><ul>{"".join(f"<li>{w}</li>" for w in where)}</ul></div>
<div class="stack"><b>กติกา</b><ul><li>เรียงตามลำดับ พ่อ แม่ Beiya Beana Bene เสมอ กว้างเท่ากันทุกแถบ</li><li>ไม่ใช้สีครอบครัวเป็นพื้นใหญ่ ยกเว้นเขียวใบตองเป็นพื้นรูปโปรไฟล์และแบนเนอร์</li>
<li>ตัวหนังสือบนเหลืองและม่วงใช้ดำถ่าน บนแดง เขียว น้ำเงินใช้ขาวฝ้าย</li></ul></div></div>''')

def p_type():
    return page(9, "ตัวอักษร", "สามฟอนต์ สองน้ำหนัก",
        f'''<div class="typ">
<div><span class="muted">หัวข้อไทย · Anuphan 500</span><p class="t1">เรียบข้างนอก บ้านอยู่ข้างใน</p></div>
<div><span class="muted">เนื้อความไทย · IBM Plex Sans Thai 400 / 600</span><p class="t2">หนังวัวแท้จากเศษหนัง ตัดด้วยบล็อกที่พ่อออกแบบ ทุกชิ้นสีไม่ซ้ำกัน <b>ราคา 59 บาท</b></p></div>
<div><span class="muted">ภาษาอังกฤษและตัวเลข · Jost 400 / 500</span><p class="t3 latin">our crafted things. 01 Coaster · SOI. 02</p></div></div>
<ul><li>หัวข้อใหญ่ไม่เกินหนึ่งบรรทัดครึ่ง ใช้น้ำหนักเดียว</li><li>ไม่ใช้ตัวเอียง ไม่ใช้ตัวหนาทั้งย่อหน้า ไม่ใช้ตัวหนังสือสีครอบครัว</li><li>ทุกฟอนต์เป็น SIL Open Font License ใช้ฟรีทั้งงานพิมพ์และเว็บ</li></ul>''')

def p_names():
    rows = "".join(f'<tr><td>{shape(p, size=30)}</td><td><b>{n}</b></td><td class="latin">{s}</td><td>{z}</td><td class="r">{pr}</td></tr>' for s, n, p, z, pr in SKUS)
    return page(10, "ชื่อสินค้า", "เลขแพตเทิร์น กับหน้าที่",
        f'''<div class="cols"><div class="stack"><p class="lead">ชื่อสินค้าบอกสองอย่าง ทำจากแพตเทิร์นไหน และใช้ทำอะไร เหมือนแคตตาล็อกเฟอร์นิเจอร์</p>
<ul><li>รูปแบบ: <b>[เลขแพตเทิร์น] [หน้าที่]</b> เช่น 05 ที่รองแก้ว · ภาษาอังกฤษ <span class="latin">05 Coaster</span></li>
<li>ใช้ชื่อเดียวกันทุกช่องทาง บูธ Shopee เว็บ โพสต์ รหัส SKU เดิมไม่เปลี่ยน</li>
<li>ไม่ตั้งชื่อเล่น ไม่ใช้คำว่าหมี ห้าหมี หรือ Love ในชื่อสินค้า</li>
<li>ใช้ 07 แทน 06 ทุกที่ (06 ไม่ได้ตัด)</li></ul></div>
<table class="tb"><thead><tr><th></th><th>ชื่อ</th><th>SKU</th><th>ขนาด</th><th class="r">ราคาร่าง</th></tr></thead><tbody>{rows}</tbody></table></div>''')

def p_photo():
    do = ["แสงธรรมชาติจากหน้าต่าง ไม่ใช้แฟลช", "ถ่ายจากด้านบนตรง ๆ หรือมุม 45°", "พื้นผ้าฝ้ายดิบ ไม้สัก หรือหิน", "หนึ่งภาพหนึ่งสินค้า เว้นที่ว่างเยอะ",
          "ภาพใกล้ให้เห็นผิวหนังและขอบตัด", "มือของคนในบ้านได้ ใบหน้าไม่จำเป็น", "ใช้รูปถ่ายจริงเป็นหลัก"]
    dont = ["ฟิลเตอร์สีจัด", "ของประกอบรกเต็มภาพ", "ใส่อาหารหรือเครื่องดื่มบนสินค้า (ยกเว้นแก้วบนที่รองแก้ว)", "เด็กเล็กเล่นสินค้า", "สติกเกอร์ อีโมจิ ตัวการ์ตูนบนภาพ"]
    frames = "".join(f'<div class="fr"><div class="frb" style="background:{bg}">{shape(c, size=70)}</div><span>{t}</span></div>'
                     for c, bg, t in (("01", "#ECE6DA", "ด้านบน พื้นผ้า"), ("05", "#C9AC8A", "บนไม้สัก"), ("04", "#B9B6AF", "บนหิน")))
    return page(11, "ภาพถ่าย", "ให้หนังเป็นพระเอก",
        f'''<div class="frs">{frames}</div><div class="cols"><div class="stack"><b>ทำ</b><ul>{"".join(f"<li>{d}</li>" for d in do)}</ul></div>
<div class="stack"><b>ไม่ทำ</b><ul>{"".join(f"<li>{d}</li>" for d in dont)}</ul></div></div>''')

def p_voice():
    pairs = [("หมีเฝ้าหน้าที่อ่านค้างไว้ให้", "01 ที่คั่นหนังสือ เหน็บมุมหน้า ไม่หลุด ไม่พับกระดาษ"),
             ("แก้วนมตอนเช้ามีหมีรองอยู่", "01 ที่รองแก้ว หนังวัวแท้ 1.2 มม. ตัดจากเศษหนัง ไม่มีชิ้นไหนสีเหมือนกัน"),
             ("ลองดึงสิ ไม่หลุดเลย ไม่ต้องเย็บ", "ตัดจากบล็อกที่พ่อออกแบบ ขอบเรียบ ใช้ได้นาน"),
             ("ช่วยอุดหนุนเด็ก ๆ หน่อยนะคะ", "ทำกันเองทั้งบ้าน พลิกป้ายดูข้างหลังด้วย")]
    rows = "".join(f'<div class="vr"><span class="old">{a}</span><span>{b}</span></div>' for a, b in pairs)
    return page(12, "เสียงของแบรนด์", "พูดสั้น บอกข้อเท็จจริง",
        f'''<div class="cols"><div class="stack"><ul><li>ประโยคสั้น ข้อมูลจริง วัสดุ ขนาด ราคา</li><li>ขำได้นิดเดียวแบบแห้ง ๆ ไม่ใช้คำน่ารัก ไม่ใช้อีโมจิ</li>
<li>เล่าเรื่องบ้านได้ แต่ไม่ขอความเห็นใจ</li><li>บอกตรง ๆ ว่ามาจากเศษหนัง สีไม่เท่ากันคือเสน่ห์</li>
<li>ไม่พูดว่าต่อเองได้หรือไม่ต้องเย็บ จนกว่าข้อต่อจะผ่านการทดสอบ</li></ul></div>
<div class="vrs"><div class="vr h"><span>แบบเดิม</span><span>แบบใหม่</span></div>{rows}</div></div>''')

def tag_front(w=100):
    return (f'<div class="tag" style="--w:{w}px"><div class="hole"></div>{logo("square-light", int(w * .62))}'
            f'<span class="tt"><b>01 ที่รองแก้ว</b><br>หนังวัวแท้ 1.2 มม.<br>59.-</span></div>')

def tag_back(w=100):
    return (f'<div class="tag back" style="--w:{w}px"><div class="hole"></div><div class="tb5">' + "".join(f'<span style="background:{c}"></span>' for c in BAND)
            + '<em>ห้าคน ห้าสี<br>ทำกันเองทั้งบ้าน</em></div></div>')

def p_apps1():
    cardf = f'<div class="ncard">{logo("square-light", 52)}<span>our crafted things.</span></div>'
    cardb = '<div class="ncard back"><div class="nb">' + "".join(f'<span style="background:{c}"></span>' for c in BAND) + '</div><em>ห้าคน ห้าสี ทำกันเองทั้งบ้าน</em></div>'
    sleeve = (f'<div class="sleeve">{logo("square-mono", 80)}<div class="sb">' + "".join(f'<span style="background:{c}"></span>' for c in BAND) + '</div></div>')
    return page(13, "การใช้งาน", "ป้าย ซอง การ์ด",
        f'''<div class="apps">
<div class="app"><div class="ab">{tag_front()}{tag_back()}</div><span><b>ป้ายห้อย 55 × 89 มม.</b> หน้าเรียบ ชื่อและราคา หลังเป็นห้าสีของบ้าน กระดาษ 350 แกรม</span></div>
<div class="app"><div class="ab">{sleeve}</div><span><b>ซองคราฟต์</b> ปั๊มตรายางโลโก้สีเดียว คาดเส้นห้าสีบาง ๆ ต้นทุนต่ำ</span></div>
<div class="app"><div class="ab" style="flex-direction:column">{cardf}{cardb}</div><span><b>การ์ดในซอง 89 × 55 มม.</b> หน้าโลโก้ หลังห้าสีของบ้าน ขอบหนังไม่ทาสี ปล่อยตามธรรมชาติ</span></div>
<div class="app"><div class="ab">{logo("square-leaf", 90)}{logo("square-family", 90)}</div><span><b>สติกเกอร์ 34 มม.</b> ปิดซองและถุง ใช้แบบเขียวใบตองหรือแบบแถบห้าสี</span></div>
</div>''')

def p_apps2():
    card = (f'<div class="card"><div class="cph">{shape("01", size=90)}</div><div class="cm"><b>01 ที่รองแก้ว</b><span>หนังวัวแท้จากเศษหนัง · 10.4 ซม.</span><span>59 บาท</span></div></div>')
    banner = (f'<div class="banner"><div><b>ของใช้จากเศษหนังแท้<br>ทำกันเองทั้งบ้าน</b><span class="latin">OCT. 26 · our crafted things.</span></div>{logo("square-leaf", 96, "style='outline:2px solid #F4F0E8'")}'
              f'<div class="bb">' + "".join(f'<span style="background:{c}"></span>' for c in BAND) + '</div></div>')
    web = (f'<div class="web"><div class="wn">{logo("line-light", 16)}<span class="sp"></span><span>สินค้า</span><span>เรื่องของเรา</span><span>บูธ</span><span>Shopee</span></div>'
           f'<div class="wh"><div><b>หนังแท้จากเศษหนัง<br>ทำกันเองทั้งบ้าน</b><span class="btn">ดูสินค้า</span></div><div class="wg">{"".join(f"<div>{shape(c, size=34)}</div>" for c in ("01", "02", "04", "05"))}</div></div></div>')
    sign = (f'<div class="sign">{logo("square-light", 70)}<div><b>SOI. 02</b><span>รอบผลิตแรก · 23–25 ต.ค. 2569</span></div></div>')
    return page(14, "การใช้งาน", "ออนไลน์และบูธ",
        f'''<div class="apps">
<div class="app"><div class="ab">{card}</div><span><b>การ์ดสินค้า FB / IG / Shopee</b> รูปถ่ายจริง ชื่อเป็นเลข ราคาชัด</span></div>
<div class="app"><div class="ab">{banner}</div><span><b>แบนเนอร์ Shopee และปกเพจ</b> พื้นเขียวใบตอง โลโก้ขาว เส้นห้าสีที่ขอบล่าง</span></div>
<div class="app"><div class="ab">{web}</div><span><b>เว็บ oct26brand.com</b> พื้นขาวฝ้าย โลโก้บรรทัดเดียวที่เมนู สินค้าเรียงเป็นตาราง</span></div>
<div class="app"><div class="ab">{sign}</div><span><b>ป้ายบูธ</b> โลโก้กับชื่อรอบผลิต ไม่ต้องมีป้ายแยกคอลเลกชัน</span></div>
</div>''')

def p_rules():
    product = ["ไม่ทำสินค้าที่โดนอาหาร เครื่องดื่ม หรือปาก ที่รองแก้วขายได้ เขียนบนป้ายว่าไม่ใช่ภาชนะใส่อาหาร",
               "ไม่ทำของเล่นหรือของใช้เด็กเล็ก", "ยังไม่ขายสินค้าที่ต้องต่อชิ้น จนกว่าข้อต่อจะผ่านการทดสอบ",
               "ใช้ 07 แทน 06 ทุกที่", "หนัง 1.0–1.2 มม. ของที่รับแรงต้องรอหนัง 2 มม."]
    brand = ["โลโก้สี่เหลี่ยมจากไฟล์เท่านั้น", "ห้าสีของบ้านไม่เกิน 5% ของงาน", "ไม่มีหน้าหมี หัวใจ ห้าหมี หรือ Love บนงานใหม่",
             "ชื่อสินค้า = เลขแพตเทิร์น + หน้าที่", "สื่อที่ลงไปแล้วไม่ต้องลบ งานใหม่ใช้ Brand Book ฉบับนี้"]
    return page(15, "สรุป", "กติกาสั้น ๆ",
        f'''<div class="cols"><div class="stack"><b>แบรนด์</b><ul>{"".join(f"<li>{x}</li>" for x in brand)}</ul></div>
<div class="stack"><b>สินค้า (จากเอกสารสถานะล่าสุด 22 ต.ค.)</b><ul>{"".join(f"<li>{x}</li>" for x in product)}</ul></div></div>
<div class="end">{logo("square-family", 90)}<p class="latin">quiet outside, family inside.</p></div>''')

CSS = """
@font-face{font-family:Jost;src:url(file://F/alt/Jost-Regular.ttf)}
@font-face{font-family:Jost;font-weight:500;src:url(file://F/alt/Jost-Medium.ttf)}
@font-face{font-family:Anuphan;font-weight:500;src:url(file://F/alt/Anuphan-Medium.ttf)}
@font-face{font-family:Plex;src:url(file://F/IBMPlexSansThai-Regular.ttf)}
@font-face{font-family:Plex;font-weight:600;src:url(file://F/IBMPlexSansThai-SemiBold.ttf)}
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}
body{margin:0;background:#F4F0E8;color:#2A2725;font:13.5px/1.6 Plex,sans-serif}
.p{width:297mm;height:210mm;padding:12mm 16mm 10mm;page-break-after:always;position:relative;overflow:hidden;display:flex;flex-direction:column;gap:6mm;background:#F4F0E8}
.ph{display:flex;justify-content:space-between;font-family:Jost;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:#6E6A64}
.ph .k{font-family:Plex;letter-spacing:.04em}
h1{font-family:Anuphan;font-weight:500;font-size:30px;line-height:1.25;margin:0}
h3{font-family:Anuphan;font-weight:500;font-size:17px;margin:0}
p{margin:0} ul{margin:0;padding-left:18px;display:grid;gap:2mm}
.body{flex:1;min-height:0;display:flex;flex-direction:column;gap:6mm;padding-bottom:9mm}
.pf{position:absolute;left:16mm;right:16mm;bottom:7mm;display:flex;justify-content:space-between;align-items:center;font-size:9.5px;color:#8C8A85}
.band{display:flex} .band span{flex:1}
.latin{font-family:Jost} .muted{color:#6E6A64} .lead{font-size:16px;line-height:1.65} .big{font-size:20px}
.eyebrow{font-family:Jost;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#6E6A64}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12mm;align-items:start}
.stack{display:grid;gap:4mm;align-content:start}
.cover{justify-content:center;padding:0 24mm}
.cv{display:grid;grid-template-columns:auto 1fr;gap:18mm;align-items:center}
.cvh{font-size:44px;line-height:1.2;margin:4mm 0}
.cvt{display:grid;gap:3mm}
.cvband{position:absolute;left:0;right:0;bottom:0}
.fam{display:grid;gap:3mm}
.who{display:grid;grid-template-columns:14mm 1fr;grid-template-rows:auto auto auto;column-gap:5mm;align-items:center}
.who i{grid-row:1/4;width:14mm;height:14mm;display:block}
.who b{font-family:Anuphan;font-weight:500;font-size:15px}
.pils{display:grid;grid-template-columns:repeat(4,1fr);border-top:1.5px solid #2A2725}
.pil{padding:5mm 6mm 5mm 0;display:grid;gap:2mm;align-content:start;border-right:1px solid #DCD4C7}
.pil+.pil{padding-left:6mm} .pil:last-child{border-right:0}
.tree{display:grid;gap:4mm}
.node{border:1.3px solid #2A2725;background:#FBF8F2;padding:4mm 5mm;display:grid;gap:1mm}
.node.main{grid-template-columns:auto 1fr;gap:5mm;align-items:center}
.node.main div{display:grid}
.branch{display:grid;gap:3mm;padding-left:8mm;border-left:2px solid #DCD4C7;margin-left:6mm}
.off{border:1.3px dashed #8C8A85;padding:4mm 5mm;display:grid;gap:2mm}
.logobox{display:grid;place-items:center;background:#EAE4D9;padding:8mm}
.lvs{display:grid;grid-template-columns:repeat(6,1fr);gap:5mm}
.lv{display:grid;gap:2mm;font-size:11.5px;color:#6E6A64;align-content:start}
.lvb{background:#EAE4D9;display:grid;place-items:center;padding:5mm}
.lvb.dk{background:#8C8A85}
.lv.wide{grid-column:1/4}
.dont{display:flex;flex-wrap:wrap;gap:3mm 8mm;border-top:1px solid #DCD4C7;padding-top:4mm;font-size:12.5px}
.dont b{width:100%}
.sws{display:grid;grid-template-columns:repeat(5,1fr);gap:5mm}
.sw{display:grid;gap:1mm;font-size:12px}
.sw i{display:block;height:34mm;margin-bottom:2mm}
.sw b{font-family:Anuphan;font-weight:500;font-size:15px}
.ratio{display:flex;height:12mm;border:1px solid #DCD4C7} .ratio span{display:block}
.fsws{display:grid;grid-template-columns:repeat(5,1fr);gap:5mm}
.fsw{display:grid;gap:1mm;font-size:12px}
.fsw i{display:block;height:30mm;margin-bottom:2mm}
.fsw b{font-family:Anuphan;font-weight:500;font-size:14px}
.typ{display:grid;gap:6mm}
.typ>div{border-top:1px solid #DCD4C7;padding-top:3mm;display:grid;gap:1mm}
.t1{font-family:Anuphan;font-weight:500;font-size:34px} .t2{font-size:17px} .t3{font-size:30px;font-weight:500}
.tb{border-collapse:collapse;width:100%;font-size:12.5px}
.tb td,.tb th{padding:2.2mm 3mm;border-bottom:1px solid #DCD4C7;text-align:left;vertical-align:middle}
.tb th{font-size:10.5px;color:#6E6A64;font-weight:600} .r{text-align:right}
.frs{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm}
.fr{display:grid;gap:2mm;font-size:11.5px;color:#6E6A64}
.frb{height:42mm;display:grid;place-items:center}
.vrs{display:grid;gap:3mm}
.vr{display:grid;grid-template-columns:1fr 1fr;gap:4mm;border-bottom:1px solid #DCD4C7;padding-bottom:3mm;font-size:13px}
.vr.h{font-size:10.5px;color:#6E6A64;font-weight:600}
.old{color:#8C8A85;text-decoration:line-through}
.apps{display:grid;grid-template-columns:repeat(4,1fr);gap:6mm}
.app{display:grid;grid-template-rows:96mm auto;gap:3mm;font-size:11.5px}
.ab{background:#EAE4D9;display:flex;gap:4mm;align-items:center;justify-content:center;padding:6mm;min-height:0}
.tag{width:var(--w);height:calc(var(--w)*1.618);background:#F4F0E8;position:relative;box-shadow:0 1px 3px rgba(42,39,37,.2);display:grid;justify-items:center;align-content:start;padding-top:calc(var(--w)*.26);gap:6px;clip-path:polygon(16% 0,84% 0,100% 9%,100% 100%,0 100%,0 9%)}
.tag .hole{position:absolute;top:8px;left:50%;width:8px;height:8px;margin-left:-4px;border-radius:50%;border:1.2px solid #2A2725}
.tag .tt{font-size:9px;text-align:center;line-height:1.35}
.tag.back{background:#2A2725;padding:0}
.tag.back .hole{border-color:#F4F0E8}
.tb5{position:absolute;left:0;right:0;top:24px;bottom:0;display:flex;flex-direction:column}
.tb5 span{flex:1}
.tb5 em{font-style:normal;color:#F4F0E8;background:#2A2725;font-size:8px;text-align:center;padding:5px 3px 7px;line-height:1.35}
.sleeve{width:150px;height:110px;background:#CDB79A;position:relative;display:grid;place-items:center}
.sleeve .sb{position:absolute;left:0;right:0;bottom:12px;height:4px;display:flex} .sleeve .sb span{flex:1}
.ncard{width:150px;height:93px;background:#F4F0E8;box-shadow:0 1px 3px rgba(42,39,37,.2);display:flex;gap:10px;align-items:center;padding:0 12px;font-family:Jost;font-size:9px;color:#6E6A64}
.ncard.back{background:#2A2725;flex-direction:column;align-items:stretch;justify-content:flex-end;padding:0;gap:0}
.ncard .nb{display:flex;height:60px} .ncard .nb span{flex:1}
.ncard em{font-style:normal;font-family:Plex;color:#F4F0E8;font-size:8px;text-align:center;padding:9px 4px}
.card{width:150px;height:188px;background:#F4F0E8;box-shadow:0 1px 3px rgba(42,39,37,.18);padding:9px;display:grid;grid-template-rows:1fr auto}
.cph{background:#E3DCCF;display:grid;place-items:center}
.cm{display:grid;font-size:9px;padding-top:6px} .cm b{font-family:Jost;font-weight:500;font-size:12px}
.banner{width:100%;aspect-ratio:2/1;background:#5E7A3A;color:#F4F0E8;position:relative;display:flex;justify-content:space-between;align-items:center;padding:0 8%}
.banner b{font-family:Anuphan;font-weight:500;font-size:13px;line-height:1.35;display:block} .banner span{font-size:8px}
.bb{position:absolute;left:0;right:0;bottom:0;height:6px;display:flex} .bb span{flex:1}
.web{width:100%;background:#F4F0E8;box-shadow:0 1px 3px rgba(42,39,37,.18);font-size:8px}
.wn{display:flex;gap:8px;align-items:center;padding:6px 8px;border-bottom:1px solid #DCD4C7} .wn .sp{flex:1}
.wh{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:10px 8px;align-items:center}
.wh b{font-family:Anuphan;font-weight:500;font-size:11px;display:block;margin-bottom:6px}
.btn{background:#A9442B;color:#F4F0E8;padding:3px 8px;font-size:8px}
.wg{display:grid;grid-template-columns:1fr 1fr;gap:4px} .wg div{background:#FBF8F2;display:grid;place-items:center;aspect-ratio:1}
.sign{background:#F4F0E8;box-shadow:0 1px 3px rgba(42,39,37,.18);padding:12px;display:flex;gap:10px;align-items:center}
.sign b{font-family:Jost;font-weight:500;font-size:18px;display:block} .sign span{font-size:9px;color:#6E6A64}
.end{display:flex;gap:8mm;align-items:center;margin-top:auto}
.end p{font-size:20px}
""".replace("file://F", f"file://{FONTS}")

def build():
    pages = [p_cover(), p_story(), p_idea(), p_arch(), p_logo(), p_logo2(), p_color(), p_family(), p_type(), p_names(),
             p_photo(), p_voice(), p_apps1(), p_apps2(), p_rules()]
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
    open(os.path.join(HERE, "brandbook.html"), "w").write(html)
    print(len(pages), "pages")

if __name__ == "__main__":
    build()
