"""LINE OA messages with the social links (owner, 23 Oct): greeting, brand intro, auto-reply.

Brand Book v2 voice: short, plain facts, no emoji, no cute words, no joining or no-sew claim, no bear face or heart.
Website link added 23 Oct after the owner merged PR #3; no Shopee link yet. Also shows the rich menu (richmenu.py).
python3 line-20261023/build.py -> messages.txt, site/index.html
"""
import html, importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "brand-20261014"))
import brand as B
import richmenu as RM

sp = importlib.util.spec_from_file_location("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
E = html.escape
SO = B.SOCIAL
LINKS = (f"เว็บไซต์ https://oct26brand.com\n"
         f"Instagram {SO['instagram']}\n"
         f"Facebook {SO['facebook']}\n"
         f"YouTube {SO['youtube']}")

MSGS = [  # (key, title, where in LINE OA Manager, limit, text)
    ("greet", "1 · ข้อความทักทายเมื่อเพิ่มเพื่อน", "LINE OA Manager → ข้อความทักทาย (Greeting message)", 500,
     "ขอบคุณที่แอด OCT. 26\n"
     "ของใช้จากเศษหนังวัวแท้ ทำกันเองทั้งบ้าน พ่อ แม่ และลูกสามคน\n"
     "ทุกแผ่นตัดจากบล็อกที่พ่อออกแบบ สีและลายไม่ซ้ำกัน\n\n"
     "แพตเทิร์นใหม่ ไอเดียใหม่ และบูธรอบหน้า จะบอกทางนี้ก่อน\n"
     "อยากถามอะไร พิมพ์มาได้เลย\n\n"
     f"ติดตามเราได้อีกทาง\n{LINKS}"),
    ("intro", "2 · แนะนำแบรนด์ (ส่งบรอดแคสต์ หรือส่งให้ลูกค้าที่ถาม)", "LINE OA Manager → บรอดแคสต์ หรือวางในแชต", 5000,
     "OCT. 26 คือแบรนด์ของบ้านเรา\n"
     "ชื่อมาจากวันเกิดแม่ 26 ตุลาคม\n\n"
     "เราเก็บเศษหนังวัวแท้ หนา 1.0–1.2 มม. มาตัดด้วยบล็อกที่พ่อออกแบบ\n"
     "ตอนนี้มี 5 แพตเทิร์น\n"
     "01 หมี · 02 กังหัน · 03 กากบาทแคปซูล · 04 สี่เหลี่ยมมน · 05 วงกลม\n\n"
     "แผ่นเดียวใช้ได้หลายอย่าง เช่น ที่รองแก้ว ที่เก็บสายชาร์จ ป้ายของขวัญ\n"
     "หนังมาจากคนละผืน สีจึงไม่เท่ากันทุกแผ่น และนั่นคือส่วนที่เราชอบ\n\n"
     f"รูปและไอเดียใหม่ ๆ ดูได้ที่\n{LINKS}\n\n"
     "OCT. 26 · our crafted things."),
    ("auto", "3 · ตอบกลับอัตโนมัติ เมื่อพิมพ์คำว่า ไอจี / เฟซ / ช่องทาง", "LINE OA Manager → ข้อความตอบกลับ → ตั้งคำสำคัญ", 500,
     f"ช่องทางของ OCT. 26\n{LINKS}\nLINE {SO['line_id']} (ที่นี่)"),
]
for key, _, _, limit, text in MSGS:
    assert len(text) <= limit, (key, len(text))
    for word in ("ไม่ต้องเย็บ", "ต่อเอง", "หัวใจ", "06", "Shopee"):
        assert word not in text, (key, word)

CHECK = [
    "ข้อความเขียนแบบไม่มีครับหรือค่ะ ให้เป็นเสียงของแบรนด์ ถ้าคนตอบแชตเป็นคนเดียวประจำ เติมท้ายประโยคให้ตรงกับคนนั้นได้",
    "ใส่ลิงก์เว็บ oct26brand.com แล้ว (เว็บใหม่ขึ้นแล้ว 23 ต.ค.) · ยังไม่ใส่ Shopee เพราะยังไม่มีลิงก์ร้าน ได้เมื่อไหร่บอก จะเติมให้",
    "ไม่ใส่ราคา 30 บาท เพราะเป็นราคาบูธอย่างเดียว ข้อความพวกนี้ใช้ได้นานหลังบูธ",
    "ข้อความ 2 ส่งบรอดแคสต์ครั้งเดียวพอ หลังบูธวันแรกเหมาะที่สุด (มีคนแอดจากการ์ดและป้าย) และตรงกับช่วงก่อนวันที่ 26 ต.ค.",
]


def richmenu():
    rows = "".join(f'<tr><td class="mono">{k}</td><td><b>{E(label)}</b></td><td>{E(t)}</td><td class="mono" style="word-break:break-all">{E(a)}</td></tr>'
                   for k, label, _, t, a in RM.AREAS)
    steps = ["LINE OA Manager → หน้าหลัก → ริชเมนู → สร้าง", "ชื่อ: เมนูหลัก · ช่วงเวลา: เริ่มวันนี้ ไม่ต้องใส่วันจบ",
             "เลือกเทมเพลต ขนาดใหญ่ แบบ 6 ช่องเท่ากัน (2 แถว 3 ช่อง)", "อัปโหลดรูป richmenu.jpg (กดรูปข้างบนค้างไว้แล้วบันทึกได้)",
             "ตั้งการกระทำของช่อง A–F ตามตาราง (A ซ้ายบน, C ขวาบน, D ซ้ายล่าง, F ขวาล่าง)",
             "ข้อความบนแถบเมนู: เมนู · ตั้งให้ แสดงเมนู เปิดไว้ตอนเข้าแชต แล้วกดบันทึก"]
    return (f'<section><span class="eyebrow">เพิ่ม 23 ต.ค.</span><h2>ริชเมนู LINE</h2>'
            f'<img src="richmenu.jpg" alt="ริชเมนู 6 ปุ่ม" style="width:100%;border:1px solid var(--line);border-radius:6px">'
            f'<p class="cap">2500 × 1686 px ขนาดใหญ่ 6 ช่อง ไฟล์ไม่ถึง 1 MB ตามที่ LINE กำหนด</p>'
            f'<div class="tbl"><table><thead><tr><th>ช่อง</th><th>ปุ่ม</th><th>ประเภท</th><th>ลิงก์ / ข้อความ</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<div class="card"><b>วิธีตั้งใน LINE OA</b><ol>{"".join(f"<li>{E(x)}</li>" for x in steps)}</ol></div></section>')


def page():
    cards = "".join(
        f'<article class="card" style="display:flex;flex-direction:column;gap:var(--s3)"><h3>{E(t)}</h3>'
        f'<p class="cap">{E(where)} · {len(text)} / {limit} ตัวอักษร</p>{S.copybox(k, text, "ข้อความ")}</article>'
        for k, t, where, limit, text in MSGS)
    check = "".join(f"<li>{E(c)}</li>" for c in CHECK)
    return f"""{S.head("OCT. 26 ข้อความ LINE")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · 23 ต.ค. 2569</span><h1>ข้อความ LINE แนะนำแบรนด์</h1>
<p class="lead">ริชเมนู 6 ปุ่ม และ 3 ข้อความพร้อมลิงก์เว็บ IG Facebook YouTube กดคัดลอกแล้ววางใน LINE OA Manager ได้เลย
เขียนตามเสียงของแบรนด์ใน Brand Book v2: สั้น บอกข้อเท็จจริง ไม่ใช้อีโมจิ</p></header>
{richmenu()}
<section style="display:flex;flex-direction:column;gap:var(--s4)"><h2>ข้อความ 3 แบบ</h2>{cards}</section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>{check}</ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">line-20261023/messages.txt</td><td>ข้อความทั้ง 3 แบบ</td></tr>
<tr><td class="mono" style="white-space:nowrap">line-20261023/richmenu.jpg</td><td>รูปริชเมนู 2500 × 1686 อัปโหลดใน LINE OA</td></tr>
<tr><td class="mono" style="white-space:nowrap">line-20261023/richmenu.py</td><td>แก้ปุ่ม ข้อความ หรือลิงก์ในริชเมนู</td></tr>
<tr><td class="mono" style="white-space:nowrap">line-20261023/build.py</td><td>แก้ข้อความที่นี่แล้วรันใหม่</td></tr>
<tr><td>Google Doc "OCT. 26 ข้อความ LINE แนะนำแบรนด์"</td><td>ในโฟลเดอร์ OCT. 26 ไฟล์งาน</td></tr>
</tbody></table></div></section></div>{S.COPY_JS}"""


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    import shutil; shutil.copyfile(os.path.join(HERE, "richmenu.jpg"), os.path.join(HERE, "site", "richmenu.jpg"))
    open(os.path.join(HERE, "site", "index.html"), "w").write(page())
    open(os.path.join(HERE, "messages.txt"), "w").write(
        "\n\n".join(f"===== {t} ({where})\n\n{text}" for _, t, where, _, text in MSGS) + "\n")
    print("wrote site/index.html and messages.txt:", ", ".join(f"{k} {len(x)}" for k, _, _, _, x in MSGS))
