"""Instagram: 9 mood posts from the owner's own photos (21 Oct), no selling.

Replaces the AI set in ig-mood-20261021, which the owner found fake and unlike the real pieces.
python3 ig-real-20261021/build_img.py   (photos in src/, from Drive folder 1SK8GUSby1iGN7UpnX2r49ui7F9kCCkeP)
python3 ig-real-20261021/build.py       -> site/index.html and doc.html for the Google Doc
"""
import html, importlib.util, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sp = importlib.util.spec_from_file_location("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
E = html.escape
RAW = "https://raw.githubusercontent.com/baysireekahnokrath/oct.26/claude/vigilant-faraday-00e92g/ig-real-20261021/img/"
TAGS = "#OCT26 #ourcraftedthings #หนังแท้ #งานแฮนด์เมด #leathercraft #slowliving"

POSTS = [  # (date, picture, caption) in posting order; img/NN.jpg matches the order
    ("พ. 21 ต.ค.", "หมีสี่ตัว", "หมีสี่ตัว สี่สี จากหนังคนละผืน\nไม่มีตัวไหนเหมือนกันเลย"),
    ("พฤ. 22 ต.ค.", "วงกลมในมือ", "ชิ้นที่เพิ่งตัดเสร็จ ถือแล้วรู้ว่าเป็นหนังแท้\nหนังวัว หนา 1.0–1.2 มม."),
    ("ศ. 23 ต.ค.", "กังหันเจ็ดชิ้น", "เจ็ดชิ้น เจ็ดเฉดสี\nจากเศษหนังที่เกือบถูกขายเหมาเป็นกระสอบ"),
    ("ส. 24 ต.ค.", "ผิวหนังระยะใกล้", "มองใกล้ ๆ จะเห็นผิวหนังจริง\nรอยย่น รูขุมขน และลายที่ไม่มีชิ้นไหนซ้ำ"),
    ("อา. 25 ต.ค.", "สี่เหลี่ยมหกสี", "กรมท่า ดำ ครีม เทา น้ำตาล\nเศษหนังจากงานจริง สีเลยหลากหลายแบบนี้"),
    ("จ. 26 ต.ค.", "หมีระยะใกล้", "26 ตุลาคม วันเกิดของแม่ และวันเกิดของ OCT. 26\nหมีตัวแรกของบ้านเรา"),
    ("อ. 27 ต.ค.", "วงกลมหกวง", "วงกลมหกวง หกอารมณ์\nจะไปอยู่ใต้แก้วของใครดี"),
    ("พ. 28 ต.ค.", "รูปทรงที่กำลังลอง", "อีกรูปทรงที่เรากำลังลองอยู่\nยังไม่เสร็จดี แต่ชอบสีชุดนี้มาก"),
    ("พฤ. 29 ต.ค.", "วงกลมสามสี", "เทา เทาเข้ม น้ำตาลอมเทา\nสีที่หาไม่ได้จากหนังผืนใหม่"),
]
CAPS = [f"{cap}\n\n{TAGS}" for *_, cap in POSTS]
for c in CAPS:
    for word in ("บาท", "Shopee", "ราคา", "สั่ง", "เย็บ", "กาว", "ต่อเอง"):
        assert word not in c, (word, c[:30])          # mood only: no selling, no joining claim

CHECK = [
    "รูปที่ 8 เป็นชิ้นทรงกากบาทเอวคอด ผมเข้าใจว่าเป็นแบบ 07 (06 ไม่ได้ตัด) แคปชันจึงเขียนว่า กำลังลองอยู่ ถ้าไม่อยากโชว์แบบนี้ บอกได้ จะสลับรูป",
    "ปรับแค่แสงขาวให้กระดาษเป็นสีขาว ครอปเป็น 4:5 ไม่ได้แต่งสีหนัง · รูปกลุ่มวางบนกรอบสีครีมให้เห็นครบทุกชิ้น",
    "รูปเก็บใน GitHub ของโปรเจกต์ (repo เปิดสาธารณะ) เพื่อให้ Google Doc ดึงรูปได้ ไฟล์ต้นฉบับ 4096 px ไม่ได้อัปขึ้น",
    "ชุดรูป AI ก่อนหน้าเลิกใช้แล้ว",
]


def page():
    posts = "".join(
        f'<article class="card post"><img src="img/{i:02d}.jpg" alt="{E(t)}" loading="lazy">'
        f'<div class="body"><span class="chip">IG {i} · {E(d)}</span><h3>{E(t)}</h3>{S.copybox(f"c{i}", cap, "แคปชัน")}</div></article>'
        for i, ((d, t, _), cap) in enumerate(zip(POSTS, CAPS), 1))
    grid = "".join(f'<img src="img/{i:02d}.jpg" alt="IG {i}">' for i in range(len(POSTS), 0, -1))
    check = "".join(f"<li>{E(c)}</li>" for c in CHECK)
    return f"""{S.head("OCT. 26 IG รูปจริง")}
<style>
.post{{display:grid;grid-template-columns:minmax(0,200px) minmax(0,1fr);gap:var(--s4);align-items:start}}
.post img{{border-radius:var(--s3);width:100%;border:1px solid var(--line)}}
.post .body{{display:flex;flex-direction:column;align-items:flex-start;gap:var(--s3);min-width:0}}.post .body>.ch{{align-self:stretch}}
.ig{{display:grid;grid-template-columns:repeat(3,1fr);gap:3px;max-width:420px}}.ig img{{aspect-ratio:3/4;object-fit:cover;width:100%}}
@media (max-width:600px){{.post{{grid-template-columns:1fr}}.post img{{max-width:233px}}}}
</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · 21 ต.ค. 2569</span><h1>IG 9 โพสต์ จากรูปจริง</h1>
<p class="lead">รูปที่พ่อเบถ่ายเมื่อเย็นนี้ 8 รูป ครอปเป็น 9 โพสต์ วันละโพสต์ 21–29 ต.ค. แนว mood ไม่ขายของ ไม่มีราคา
ให้เห็นสีและผิวหนังของจริง</p></header>
<section><span class="eyebrow">หน้าโปรไฟล์หลังลงครบ</span><h2>ตาราง 3 × 3</h2><div class="ig">{grid}</div>
<p class="cap">โพสต์ล่าสุดอยู่ซ้ายบน</p></section>
<section><span class="eyebrow">Instagram</span><h2>9 โพสต์ ตามลำดับที่ลง</h2>{posts}</section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>{check}</ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">ig-real-20261021/img/*.jpg</td><td>รูป 1080 × 1350 ทั้ง 9 รูป</td></tr>
<tr><td>Google Doc "4 · Instagram รูปจริง 9 โพสต์"</td><td>รูปพร้อมแคปชัน ในโฟลเดอร์ OCT. 26 โพสต์ FB และ IG</td></tr>
<tr><td class="mono" style="white-space:nowrap">ig-real-20261021/build_img.py</td><td>วิธีครอปและปรับแสง</td></tr>
</tbody></table></div></section></div>{S.COPY_JS}"""


def doc():
    out = ["<html><body><h1>OCT. 26 Instagram 9 โพสต์ จากรูปจริง (21–29 ต.ค.)</h1>",
           "<p>รูปจริงที่ถ่ายวันที่ 21 ต.ค. · แนว mood ไม่ขายของ ไม่มีราคา · วันละโพสต์ · กดลิงก์ใต้รูปเพื่อเปิดรูปเต็ม 1080 × 1350 แล้วบันทึก</p>"]
    for i, ((d, t, _), cap) in enumerate(zip(POSTS, CAPS), 1):
        url = f"{RAW}{i:02d}.jpg"
        out.append(f"<h2>IG {i} · {E(d)} · {E(t)}</h2>")
        out.append(f'<p><img src="{url}" width="320" height="400"></p><p><a href="{url}">รูปเต็ม IG {i}</a></p>')
        out.append("<p>" + "<br>".join(E(x) for x in cap.split("\n")) + "</p><hr>")
    out.append("<h2>ต้องเช็ก</h2>" + "".join(f"<p>- {E(c)}</p>" for c in CHECK))
    return "\n".join(out) + "</body></html>"


if __name__ == "__main__":
    site = os.path.join(HERE, "site"); os.makedirs(os.path.join(site, "img"), exist_ok=True)
    for i in range(1, len(POSTS) + 1):
        shutil.copyfile(os.path.join(HERE, "img", f"{i:02d}.jpg"), os.path.join(site, "img", f"{i:02d}.jpg"))
    open(os.path.join(site, "index.html"), "w").write(page())
    open(os.path.join(HERE, "doc.html"), "w").write(doc())
    print("wrote site/index.html and doc.html,", len(POSTS), "posts")
