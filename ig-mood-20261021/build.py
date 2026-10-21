"""Instagram: 9 mood-and-tone posts with realistic pictures, no selling (owner, 21 Oct).

The pictures are AI images made in the owner's Figma file "OCT. 26 IG mood 9 โพสต์" (gpt-image-2.5-sunburst), not
photos of real stock: shapes follow the dies 01–05 loosely, no 06, nothing joined. Full-size PNGs stay in Figma (the
asset links expire 7 days after 21 Oct); thumb/ holds 256 px previews for the summary page.
python3 ig-mood-20261021/build.py -> site/index.html and doc.html (the Google Doc in Drive is made from doc.html)
"""
import html, importlib.util, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "brand-20261014"))
import brand as B

sp = importlib.util.spec_from_file_location("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
E = html.escape
FIGMA = "https://www.figma.com/design/l1rEiJJGWi3bFY6oKf5btb"
ASSET = "https://www.figma.com/api/mcp/asset/{}.png"
TAGS = "#OCT26 #ourcraftedthings #หนังแท้ #งานแฮนด์เมด #leathercraft #slowliving"

# (posting date, figma node, asset id, scene, caption) in posting order; the grid shows the newest first
POSTS = [
    ("พ. 21 ต.ค.", "1:2", "7ec8f5ee-c080-469b-ab5c-e012822390b0", "เศษหนังหลายสีบนผ้าลินิน",
     "ทุกอย่างเริ่มจากเศษหนังชิ้นเล็ก ๆ บนโต๊ะในบ้าน\nสีไม่เหมือนกัน ลายไม่เหมือนกัน และนั่นคือสิ่งที่เราชอบ"),
    ("พฤ. 22 ต.ค.", "3:2", "8b6a6dec-3a48-46e0-ba66-63fbffcadec7", "มือเด็กถือหัวหมีหนัง",
     "มือเล็ก ๆ ที่ช่วยกันทำทุกชิ้น\nOCT. 26 คืองานแรกที่ทั้งห้าคนในบ้านทำด้วยกัน"),
    ("ศ. 23 ต.ค.", "4:2", "a6182ea7-d83f-4442-a3b6-f2d8d8755385", "ผิวหนังระยะใกล้",
     "หนังวัวแท้ หนา 1.0–1.2 มม.\nรอยเล็ก ๆ บนผิวคือเรื่องราวของหนังแต่ละชิ้น ไม่มีชิ้นไหนซ้ำกัน"),
    ("ส. 24 ต.ค.", "2:2", "6f06f772-d11c-4dbf-b460-ce42c45aaa2d", "แก้วนมบนที่รองแก้วหมี",
     "แก้วนมตอนเช้า\nกับหมีตัวเล็กที่รองอยู่ข้างใต้"),
    ("อา. 25 ต.ค.", "7:2", "1ce113e0-fba8-4ef5-a2d3-678fefddfeb6", "กาแฟบนโต๊ะทำงาน",
     "บ่ายที่โต๊ะทำงาน กาแฟหนึ่งแก้ว\nกับของชิ้นเล็กที่ทำให้วันช้าลงนิดหนึ่ง"),
    ("จ. 26 ต.ค.", "9:2", "220ae031-a40f-4f2a-a2c9-726d457cbd0b", "มือทั้งบ้านช่วยกันคัดหนัง",
     "26 ตุลาคม วันเกิดของแม่ และวันเกิดของ OCT. 26\nขอบคุณที่ทำให้บ้านเรามีกันห้าคน"),
    ("อ. 27 ต.ค.", "8:2", "1ea8142f-f1f9-4ebe-8c9f-a5c5be8a268d", "สายชาร์จพันหัวหมีในกระเป๋าผ้า",
     "สายชาร์จที่ไม่พันกันอีกแล้ว\nเรื่องเล็ก ๆ ที่ทำให้กระเป๋าเป็นระเบียบขึ้น"),
    ("พ. 28 ต.ค.", "5:2", "94dff2c9-6cd5-413d-9052-27d4e01f784d", "ที่รองแก้วสี่ทรงผูกเชือกปอ",
     "สี่ทรง สี่สี ผูกเชือกปอไว้ด้วยกัน\nพร้อมส่งต่อให้ใครสักคน"),
    ("พฤ. 29 ต.ค.", "6:2", "60f53eba-80c0-453b-ae81-a44728f85598", "ป้ายหนังผูกถุงของขวัญสีน้ำเงิน",
     "เขียนชื่อคนที่เรารัก แล้วผูกไว้กับของขวัญ\nป้ายหนังที่เก็บไว้ใช้ต่อได้อีกนาน"),
]
CAPS = [f"{cap}\n\n{TAGS}" for *_, cap in POSTS]
for c in CAPS:
    for word in ("บาท", "Shopee", "ราคา", "สั่ง", "เย็บ", "กาว", "ต่อเอง"):
        assert word not in c, (word, c[:30])          # mood only: no selling, no joining claim

CHECK = [
    "รูปทั้ง 9 เป็นภาพจาก AI ไม่ใช่รูปถ่ายของจริง ตอนโพสต์ใน IG เปิด ป้ายกำกับ AI (การตั้งค่าขั้นสูง → ป้ายกำกับ AI) "
    "คนจะได้ไม่เข้าใจว่าเป็นรูปสินค้าจริง และเมื่อมีรูปถ่ายจริงแล้วค่อยทยอยแทน",
    "รูปที่ 9 ป้ายหนังเขียนชื่อ Emma เป็นชื่อสมมุติ ถ้าอยากได้ชื่อไทย บอกได้ จะทำรูปใหม่",
    "รูปทรงชิ้นหนังในรูปใกล้เคียงบล็อก 01–05 แต่ไม่ตรงทุกเส้น ไม่มี 06 และไม่มีชิ้นที่ต่อกัน",
    "ดาวน์โหลดรูปเต็มจาก Figma: เปิดไฟล์ → เลือกรูป → Export PNG · หรือจาก Google Doc ในโฟลเดอร์",
]


def page():
    posts = "".join(
        f'<article class="card post"><img src="thumb/{i:02d}.jpg" alt="{E(scene)}" loading="lazy">'
        f'<div class="body"><span class="chip">IG {i} · {E(d)}</span><h3>{E(scene)}</h3>{S.copybox(f"c{i}", cap, "แคปชัน")}</div></article>'
        for i, ((d, _, _, scene, _), cap) in enumerate(zip(POSTS, CAPS), 1))
    grid = "".join(f'<img src="thumb/{i:02d}.jpg" alt="IG {i}">' for i in range(len(POSTS), 0, -1))
    check = "".join(f"<li>{E(c)}</li>" for c in CHECK)
    return f"""{S.head("OCT. 26 IG mood")}
<style>
.post{{display:grid;grid-template-columns:minmax(0,180px) minmax(0,1fr);gap:var(--s4);align-items:start}}
.post img{{border-radius:var(--s3);width:100%}}
.post .body{{display:flex;flex-direction:column;align-items:flex-start;gap:var(--s3);min-width:0}}.post .body>.ch{{align-self:stretch}}
.ig{{display:grid;grid-template-columns:repeat(3,1fr);gap:3px;max-width:420px}}.ig img{{aspect-ratio:3/4;object-fit:cover;width:100%}}
@media (max-width:600px){{.post{{grid-template-columns:1fr}}.post img{{max-width:233px}}}}
</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · 21 ต.ค. 2569</span><h1>IG 9 โพสต์ mood and tone</h1>
<p class="lead">รูปแนวสมจริง วันละโพสต์ 21–29 ต.ค. ไม่ขายของ ไม่มีราคา แค่ให้เห็นว่าของจากเศษหนังของเราอยู่ในชีวิตประจำวันแล้วสวยแบบไหน
รูปเต็มอยู่ใน <a href="{FIGMA}">Figma</a> และ Google Doc ในโฟลเดอร์ OCT. 26 โพสต์ FB และ IG</p></header>
<section><span class="eyebrow">หน้าโปรไฟล์หลังลงครบ</span><h2>ตาราง 3 × 3</h2><div class="ig">{grid}</div>
<p class="cap">โพสต์ล่าสุดอยู่ซ้ายบน · รูปตัวอย่างในหน้านี้ย่อเหลือ 256 px รูปจริง 1024 × 1280</p></section>
<section><span class="eyebrow">Instagram</span><h2>9 โพสต์ ตามลำดับที่ลง</h2>{posts}</section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>{check}</ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td>Figma "OCT. 26 IG mood 9 โพสต์"</td><td>รูปเต็มทั้ง 9 รูป</td></tr>
<tr><td>Google Doc "3 · Instagram mood 9 โพสต์"</td><td>รูปพร้อมแคปชัน ในโฟลเดอร์ OCT. 26 โพสต์ FB และ IG</td></tr>
<tr><td class="mono" style="white-space:nowrap">ig-mood-20261021/build.py</td><td>แคปชันและลำดับโพสต์</td></tr>
</tbody></table></div></section></div>{S.COPY_JS}"""


def doc():
    out = ["<html><body><h1>OCT. 26 Instagram mood 9 โพสต์ (21–29 ต.ค.)</h1>",
           "<p>รูปจาก AI ไม่ใช่รูปถ่ายของจริง ตอนโพสต์ให้เปิดป้ายกำกับ AI · ไม่ขายของ ไม่มีราคา · วันละโพสต์</p>"]
    for i, ((d, _, asset, scene, _), cap) in enumerate(zip(POSTS, CAPS), 1):
        out.append(f"<h2>IG {i} · {E(d)} · {E(scene)}</h2>")
        out.append(f'<p><img src="{ASSET.format(asset)}" width="320" height="400"></p>')
        out.append("<p>" + "<br>".join(E(x) for x in cap.split("\n")) + "</p><hr>")
    out.append("<h2>ต้องเช็ก</h2>" + "".join(f"<p>- {E(c)}</p>" for c in CHECK))
    return "\n".join(out) + "</body></html>"


if __name__ == "__main__":
    site = os.path.join(HERE, "site"); os.makedirs(os.path.join(site, "thumb"), exist_ok=True)
    for i in range(1, len(POSTS) + 1):
        shutil.copyfile(os.path.join(HERE, "thumb", f"{i:02d}.jpg"), os.path.join(site, "thumb", f"{i:02d}.jpg"))
    open(os.path.join(site, "index.html"), "w").write(page())
    open(os.path.join(HERE, "doc.html"), "w").write(doc())
    print("wrote site/index.html and doc.html,", len(POSTS), "posts")
