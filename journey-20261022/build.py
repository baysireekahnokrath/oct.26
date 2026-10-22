"""Customer journey for OCT. 26 (22 Oct 2026): what each channel is for and where we take the customer next.

LINE OA is the home base for people we have met; Shopee closes online sales; IG and FB bring people in.
Follows the status doc: 7 single-piece SKUs, no 06, no joining or no-sew claim.
python3 journey-20261022/build.py -> site/index.html and doc.html (the Google Doc in Drive)
"""
import html, importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "brand-20261014"))
import brand as B

sp = importlib.util.spec_from_file_location("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
E = html.escape

CHANNELS = [  # (channel, job, what it is not for)
    ("Instagram", "ให้คนเห็นแล้วจำได้ว่าของเราหน้าตาแบบไหน โทนเดียวกันทุกโพสต์", "ไม่ขายของในโพสต์ ลิงก์ไป LINE กับ Shopee อยู่ที่โปรไฟล์"),
    ("Facebook", "ข่าวบูธ วันเวลา สถานที่ และเรื่องของครอบครัว คนรุ่นพ่อแม่อยู่ที่นี่", "ไม่ใช้ตอบแชทยาว ๆ ตอบสั้นแล้วชวนไป LINE"),
    ("บูธ", "ให้จับของจริง ลองแต่งชิ้นหนัง คุยกับลูก ๆ และซื้อครั้งแรก", "ไม่ใช่ที่เดียวที่ขาย ทุกบิลต้องได้ LINE กลับไปด้วย"),
    ("LINE OA", "บ้านของลูกค้าที่รู้จักเราแล้ว แจ้งรอบบูธ ของใหม่ รุ่นวันเกิด ตอบคำถาม รับสั่งทำ", "ไม่ส่งข้อความถี่ เดือนละ 2–4 ครั้ง"),
    ("Shopee", "ที่จ่ายเงินและส่งของสำหรับคนที่ไม่ได้มาบูธ ได้รีวิวและความน่าเชื่อถือ", "ไม่ใช่ที่เล่าเรื่อง ทุกกล่องใส่การ์ดชวนแอด LINE"),
    ("YouTube", "คลิปเบื้องหลัง ลูก ๆ ทำงาน วันออกบูธ", "ไม่ต้องลงถี่ ลงเมื่อมีคลิปดี"),
    ("เว็บ oct26brand.com", "แคตตาล็อกและเรื่องแบรนด์สำหรับคนที่อยากรู้มากขึ้น", "ยังไม่ตรงกับ 7 แบบ ยังไม่ชี้คนไปจนกว่าจะแก้"),
]

STAGES = [  # (stage, where, what the customer does, what we do, what we count)
    ("1 · เห็น", "IG · FB · เพจผู้จัด · เดินผ่านบูธ",
     "เห็นรูปหนังสีสวย ๆ เห็นว่าเป็นของที่ครอบครัวทำ",
     "โพสต์ mood ใน IG โพสต์ข่าวบูธใน FB แท็กเพจผู้จัด X-stand หันหน้าเข้าทางเดิน",
     "ยอดเข้าถึง · ผู้ติดตามใหม่"),
    ("2 · แวะ", "บูธ",
     "หยุดดู จับหนัง ลองเขียนชื่อหรือวาดลายบนชิ้นหนัง",
     "ลูก ๆ ชวนลอง ยื่นชิ้นหนังให้จับ เล่าสั้น ๆ ว่าเศษหนังมาจากไหน",
     "คนที่แวะ · คนที่ลอง DIY"),
    ("3 · ซื้อครั้งแรก", "บูธ (เงินสด · พร้อมเพย์) หรือ Shopee",
     "เลือก 1 ชิ้นหรือชุด 4 ลาย จ่ายเงิน",
     "แนะนำชุดที่รองแก้ว 4 ลาย ห่อให้ ใส่การ์ดในถุง",
     "จำนวนบิล · ยอดต่อบิล"),
    ("4 · แอด LINE", "ตอนจ่ายเงิน · การ์ดในถุงหรือในกล่อง Shopee",
     "สแกน QR แอด LINE OA",
     "ลูก ๆ ชวนทุกบิล: แอด LINE แล้วรับ [ของที่ให้ — รอพ่อเบเลือก] และข่าวรอบบูธถัดไป",
     "เพื่อนใหม่ใน LINE เทียบกับจำนวนบิล (เป้า 3 ใน 10)"),
    ("5 · ใช้และเล่าต่อ", "บ้านลูกค้า · IG ของลูกค้า",
     "ใช้ที่รองแก้วทุกวัน ถ่ายรูปลงสตอรี่",
     "การ์ดชวนถ่ายรูปแล้วแท็ก @oct.26_brand เรารีโพสต์ลงสตอรี่และขอบคุณ",
     "จำนวนแท็ก · รีวิว Shopee"),
    ("6 · กลับมาซื้อ", "LINE OA → บูธรอบหน้า หรือ Shopee",
     "สะสมลายใหม่ ซื้อเป็นของขวัญ",
     "LINE แจ้งลายใหม่ รุ่นวันเกิด 26 ต.ค. และรอบบูธ · ชุดที่รองแก้วสะสมให้มีเหตุผลกลับมาเก็บลายที่ขาด",
     "ลูกค้าที่ซื้อครั้งที่ 2"),
    ("7 · ชวนคนอื่น", "LINE OA · ปากต่อปาก",
     "ซื้อเป็นของขวัญ ของชำร่วย ของที่ระลึกบริษัท",
     "รับสั่งทำจำนวนมากผ่าน LINE ป้ายห้อยของขวัญเขียนชื่อให้",
     "งานสั่งทำ · ลูกค้าที่มาจากการแนะนำ"),
]

PATHS = [
    ("เจอที่บูธ", ["เห็น IG/FB หรือเดินผ่าน", "แวะ ลองแต่งชิ้นหนัง", "ซื้อที่บูธ", "แอด LINE ตอนจ่ายเงิน", "LINE แจ้งของใหม่", "กลับมาซื้อ"]),
    ("เจอออนไลน์", ["เห็นโพสต์ IG", "กดลิงก์ที่โปรไฟล์", "ซื้อใน Shopee", "การ์ดในกล่องชวนแอด LINE", "LINE แจ้งของใหม่", "กลับมาซื้อ"]),
]

MAKE = [  # (what, for which stage, by when)
    ("ป้าย QR LINE ตั้งโต๊ะ A6", "4", "คืนนี้ 22 ต.ค."),
    ("การ์ดใส่ถุงและกล่อง 9 × 5.5 ซม.: QR LINE · @oct.26_brand · วิธีดูแลหนัง · ชวนแท็กรูป", "4–5", "คืนนี้ 22 ต.ค. (พิมพ์ร้านด่วน หรือพิมพ์บ้านแล้วตัด)"),
    ("ประโยคชวนแอด LINE ให้ลูก ๆ พูดตอนรับเงิน", "4", "คืนนี้ 22 ต.ค."),
    ("LINE OA: ข้อความต้อนรับ เมนูหลัก 4 ปุ่ม ตอบอัตโนมัติ", "4–6", "ก่อน 23 ต.ค. 10:00"),
    ("ใส่ลิงก์ LINE และ Shopee ในโปรไฟล์ IG และข้อมูลเพจ FB", "1–3", "ก่อน 23 ต.ค."),
    ("ข้อความ LINE ส่งครั้งแรก: ขอบคุณที่แวะบูธ + รอบ 30 ต.ค.–1 พ.ย.", "6", "จ. 27 ต.ค."),
    ("แท็กลูกค้าใน LINE ตามที่มา (บูธสัปดาห์ 1 · บูธสัปดาห์ 2 · Shopee)", "6", "ทำทุกวันที่มีเพื่อนใหม่"),
]

DECIDE = [
    "แอด LINE แล้วได้อะไร: เช่น ส่วนลดครั้งหน้า 10 บาท · เขียนชื่อบนชิ้นหนังฟรี · ได้ข่าวลายใหม่ก่อนคนอื่น (เลือก 1 อย่าง ผมแนะนำเขียนชื่อฟรี เพราะไม่ลดราคาและใช้ของที่มีอยู่แล้ว)",
    "ราคา 7 แบบ ยังเป็นราคาร่าง",
    "ชุดที่รองแก้วสะสม: จะทำบัตรสะสมลายไหม (สะสมครบ 6 ลายได้อะไร) หรือแค่บอกใน LINE ว่ามีลายใหม่",
    "ใครตอบแชท LINE ช่วงบูธ และตอบภายในกี่ชั่วโมง",
]


def svg_flow():
    w, gap, bw, bh = 975, 14, 140, 74
    rows = []
    for r, (name, steps) in enumerate(PATHS):
        y = 40 + r * 130
        rows.append(f'<text x="0" y="{y - 12}" class="lab">{E(name)}</text>')
        for i, s in enumerate(steps):
            x = i * (bw + gap + 12)
            hub = "LINE" in s
            rows.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="13" class="{"hub" if hub else "box"}"/>')
            words, lines, cur = s.split(" "), [], ""
            for wd in words:
                if len(cur + " " + wd) > 14 and cur:
                    lines.append(cur); cur = wd
                else:
                    cur = (cur + " " + wd).strip()
            lines.append(cur)
            for j, ln in enumerate(lines[:3]):
                rows.append(f'<text x="{x + bw / 2}" y="{y + bh / 2 + (j - (len(lines) - 1) / 2) * 18 + 5}" class="{"t hubt" if hub else "t"}" text-anchor="middle">{E(ln)}</text>')
            if i < len(steps) - 1:
                ax = x + bw + 4
                rows.append(f'<path d="M{ax} {y + bh / 2} h{gap + 2}" class="arr" marker-end="url(#a)"/>')
    return (f'<svg viewBox="0 -10 {w} 270" role="img" aria-label="เส้นทางลูกค้าสองทาง ทั้งสองทางมาจบที่ LINE OA">'
            '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10z" fill="var(--muted)"/></marker></defs>' + "".join(rows) + "</svg>")


def page():
    ch = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td class='cap'>{E(c)}</td></tr>" for a, b, c in CHANNELS)
    st = "".join(f"<tr><td style='white-space:nowrap'><b>{E(a)}</b><br><span class='cap'>{E(b)}</span></td><td>{E(c)}</td><td>{E(d)}</td><td class='cap'>{E(e)}</td></tr>"
                 for a, b, c, d, e in STAGES)
    mk = "".join(f"<tr><td>{E(a)}</td><td class='mono'>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in MAKE)
    dc = "".join(f"<li>{E(x)}</li>" for x in DECIDE)
    return f"""{S.head("OCT. 26 Customer Journey")}
<style>
.flow{{overflow-x:auto}}.flow svg{{min-width:900px;width:100%;height:auto}}
.flow .box{{fill:var(--paper);stroke:var(--line);stroke-width:1.5}}.flow .hub{{fill:var(--cobalt)}}
.flow .t{{font:500 14px var(--body);fill:var(--ink)}}.flow .hubt{{fill:#FFFFFF}}
.flow .lab{{font:600 15px var(--display);fill:var(--muted)}}.flow .arr{{stroke:var(--muted);stroke-width:1.5;fill:none}}
</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · 22 ต.ค. 2569</span><h1>Customer Journey ของ OCT. 26</h1>
<p class="lead">ลูกค้าเจอเราได้ 2 ทาง คือที่บูธกับออนไลน์ ทั้งสองทางพาไปจบที่ LINE OA
เพราะเป็นช่องทางเดียวที่เราทักลูกค้ากลับได้เองเมื่อมีของใหม่หรือรอบบูธถัดไป
Shopee ใช้ปิดการขายออนไลน์ ส่วน IG กับ FB ใช้พาคนใหม่เข้ามา</p></header>
<section><span class="eyebrow">ภาพรวม</span><h2>สองทาง จบที่เดียว</h2><div class="card flow">{svg_flow()}</div>
<p class="cap">กล่องสีน้ำเงินคือจุดที่ลูกค้าเข้ามาอยู่ใน LINE OA</p></section>
<section><span class="eyebrow">แต่ละช่องทาง</span><h2>ใช้ทำอะไร และไม่ใช้ทำอะไร</h2>
<div class="tbl"><table><thead><tr><th>ช่องทาง</th><th>หน้าที่</th><th>ไม่ใช้ทำ</th></tr></thead><tbody>{ch}</tbody></table></div></section>
<section><span class="eyebrow">7 ขั้น</span><h2>ลูกค้าทำอะไร เราทำอะไร นับอะไร</h2>
<div class="tbl"><table><thead><tr><th>ขั้น</th><th>ลูกค้า</th><th>เรา</th><th>นับ</th></tr></thead><tbody>{st}</tbody></table></div>
<p class="cap">ขั้นที่ 4 สำคัญที่สุดสำหรับงานนี้ คนที่ซื้อแล้วไม่ได้แอด LINE เราจะไม่มีทางทักกลับได้อีก</p></section>
<section><span class="eyebrow">ต้องทำ</span><h2>ของที่ต้องเตรียม</h2>
<div class="tbl"><table><thead><tr><th>อะไร</th><th>ขั้น</th><th>เมื่อไร</th></tr></thead><tbody>{mk}</tbody></table></div></section>
<section><h2>รอพ่อเบตัดสินใจ</h2><div class="card"><ol>{dc}</ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">journey-20261022/build.py</td><td>เนื้อหาทั้งหมดในหน้านี้</td></tr>
<tr><td>Google Doc "OCT. 26 Customer Journey"</td><td>ข้อความชุดเดียวกัน ในโฟลเดอร์ OCT. 26 ไฟล์งาน</td></tr>
<tr><td class="mono" style="white-space:nowrap">brand-20261014/line/</td><td>QR LINE OA 3 ขนาด</td></tr>
</tbody></table></div></section></div>{S.COPY_JS}"""


def doc():
    t = lambda rows, heads: ("<table border='1'><tr>" + "".join(f"<th>{E(h)}</th>" for h in heads) + "</tr>"
                             + "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>")
    return ("<html><body><h1>OCT. 26 Customer Journey (22 ต.ค. 2569)</h1>"
            "<p>ลูกค้าเจอเราได้ 2 ทาง คือที่บูธกับออนไลน์ ทั้งสองทางพาไปจบที่ LINE OA เพราะเป็นช่องทางเดียวที่เราทักลูกค้ากลับได้เอง "
            "Shopee ใช้ปิดการขายออนไลน์ ส่วน IG กับ FB ใช้พาคนใหม่เข้ามา</p>"
            "<h2>สองทาง</h2>" + "".join(f"<p><b>{E(n)}:</b> {' → '.join(E(s) for s in st)}</p>" for n, st in PATHS)
            + "<h2>แต่ละช่องทาง</h2>" + t(CHANNELS, ["ช่องทาง", "หน้าที่", "ไม่ใช้ทำ"])
            + "<h2>7 ขั้น</h2>" + t(STAGES, ["ขั้น", "ที่ไหน", "ลูกค้า", "เรา", "นับ"])
            + "<h2>ของที่ต้องเตรียม</h2>" + t(MAKE, ["อะไร", "ขั้น", "เมื่อไร"])
            + "<h2>รอพ่อเบตัดสินใจ</h2>" + "".join(f"<p>- {E(x)}</p>" for x in DECIDE) + "</body></html>")


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(page())
    open(os.path.join(HERE, "doc.html"), "w").write(doc())
    print("wrote site/index.html and doc.html")
