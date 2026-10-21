"""Intro post for Facebook (today, 21 Oct) and the first 9 Instagram posts, with pictures and captions.

Four new brand pictures (intro sneak peek, the leather, 26 October, five bears) plus the launch banner and the
product cards from facebook-20261021. Follows the status doc of 21 Oct: only the 7 single-piece SKUs, no 06,
no joining or no-sew claim. One logo per picture.
python3 intro-20261021/build.py && node brand-20261014/tools/render.mjs intro-20261021/img/jobs.json
python3 intro-20261021/build.py      (again, so the page and the Drive doc pick up the PNGs)
"""
import html, importlib.util, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BRAND_DIR = os.path.join(REPO, "brand-20261014")
sys.path.insert(0, BRAND_DIR)
sys.path.insert(0, os.path.join(REPO, "facebook-20261021"))
import brand as B
from cards import SKU, SALE


def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


PB = _load("posters_build", os.path.join(BRAND_DIR, "posters", "build.py"))
S = _load("brand_site", os.path.join(BRAND_DIR, "site", "build.py"))
SB = _load("social_build", os.path.join(REPO, "social-20261021", "build.py"))
E = html.escape
C = B.C
H = B.BRAND["handle"]
FONTS = "file://" + os.path.join(BRAND_DIR, "fonts")
P = {p["n"]: p for p in SALE}
# the repo is public, so Google Docs can fetch the pictures from GitHub when the Drive doc is made
RAW = "https://raw.githubusercontent.com/baysireekahnokrath/oct.26/claude/vigilant-faraday-00e92g/"
FIRST = f"เจอกันครั้งแรก {SB.WEEKENDS[0]} · บ้านและสวนแฟร์"
LEATHER = ["#B8743A", "#8E5428", "#C98E55", "#6F4120", "#A8652F"]   # material tones of the scrap lot, not brand colours


def piece(code, x, y, size, rot, fill=C["leather"], slit=C["paper"]):
    return (f'<span class="pc" style="left:{x}px;top:{y}px;width:{size}px;transform:rotate({rot}deg)">'
            f'{PB.icon(code, fill, slit)}</span>')


def frame(body, bg, extra_css=""):
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>
@font-face{{font-family:Anuphan;font-weight:500;src:url({FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url({FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Plex;font-weight:400;src:url({FONTS}/IBMPlexSansThai-Regular.ttf)}}
@font-face{{font-family:Mitr;font-weight:600;src:url({FONTS}/Mitr-SemiBold.ttf)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;background:{bg};color:{C['ink']};font-family:Plex,sans-serif;overflow:hidden}}
.page{{position:relative;width:1080px;height:1350px;overflow:hidden}}
.pc{{position:absolute;display:block}}.pc svg{{width:100%;height:auto;display:block}}
.pill{{display:inline-block;border-radius:99px;padding:10px 30px;font-family:Anuphan;font-weight:500;font-size:34px}}
h1{{font-family:Anuphan;font-weight:500;line-height:1.18}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:110px;background:{C['ink']};color:{C['paper']};display:flex;
  align-items:center;justify-content:space-between;padding:0 89px;font-size:28px}}
.foot b{{font-family:Jost;font-weight:500;font-size:32px}}
{extra_css}</style></head><body><div class="page">{body}</div></body></html>"""


def intro():
    word = PB._logo("oct-wordmark-reverse.svg")
    # the pieces sit half below the frame: a peek at what is coming, not the products themselves
    peek = "".join(piece(c, x, 1020, 300, r) for c, x, r in (("02", 40, -14), ("04", 300, 9), ("05", 560, -6), ("03", 800, 16)))
    body = f"""<div class="top"><span class="pill" style="background:{C['sun']}">แอบดูก่อน · SNEAK PEEK</span>{word}
<div class="en">{B.BRAND['tag_en']}</div></div>
<div class="mid"><h1>สวัสดีครับ<br>เราคือ <span class="o">OCT. 26</span></h1>
<p>ครอบครัวห้าคน พ่อ แม่ และลูกสามคน<br>ทำของใช้จากเศษหนังวัวแท้ด้วยกัน</p></div>
{peek}<div class="foot"><span>{FIRST}</span><b>@{H}</b></div>"""
    css = f""".top{{height:560px;background:{C['cobalt']};color:{C['paper']};display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:22px}}.top svg{{width:640px;height:auto}}
.top .en{{font-family:Jost;font-weight:500;font-size:48px;letter-spacing:.04em}}
.mid{{padding:70px 89px 0;display:flex;flex-direction:column;gap:30px}}.mid h1{{font-size:96px}}
.mid h1 .o{{font-family:Jost;color:{C['tomato']}}}.mid p{{font-size:40px;line-height:1.5;color:#4A4A55}}"""
    return frame(body, C["paper"], css)


def leather():
    spots = [("02", 60, 90, 230, -20), ("05", 300, 40, 200, 10), ("04", 520, 110, 240, 24), ("03", 790, 50, 210, -8),
             ("05", 30, 330, 190, 30), ("03", 230, 280, 250, 14), ("02", 480, 330, 220, -30), ("04", 720, 300, 260, -12),
             ("04", 110, 520, 200, 6), ("02", 360, 520, 210, 40), ("05", 600, 560, 190, -18), ("03", 840, 540, 200, 22)]
    pile = "".join(piece(c, x, y, s, r, LEATHER[i % len(LEATHER)]) for i, (c, x, y, s, r) in enumerate(spots))
    body = f"""{pile}<div class="txt"><span class="pill" style="background:{C['mint']}">เรื่องของเรา · 1</span>
<h1>เศษหนังที่เกือบถูก<br>ขายเหมาเป็นกระสอบ</h1>
<p>ชิ้นเล็กแค่ฝ่ามือ แต่เป็นหนังวัวแท้ทุกชิ้น<br>เราเลยตัดเป็นของใช้ ทีละชิ้น สีและลายไม่ซ้ำกัน</p></div>
<div class="foot"><span>OCT. 26 · {B.BRAND['tag_en']}</span><b>@{H}</b></div>"""
    css = """.txt{position:absolute;left:89px;right:89px;top:800px;display:flex;flex-direction:column;align-items:flex-start;gap:26px}
.txt h1{font-size:76px}.txt p{font-size:36px;line-height:1.5;color:#4A4A55}"""
    return frame(body, C["paper"], css)


def october():
    body = f"""<div class="big">26</div><div class="mo">ตุลาคม</div>
<div class="txt"><span class="pill" style="background:{C['sun']};color:{C['ink']}">เรื่องของเรา · 2</span>
<h1>ชื่อแบรนด์คือ<br>วันเกิดของแม่</h1>
<p>ทุกปีในวันนี้ เราจะออกรุ่นวันเกิดหนึ่งชุด<br>เลขรุ่นคืออายุของแม่ในปีนั้น</p></div>
<div class="foot"><span>OCT. 26 · {B.BRAND['tag_en']}</span><b>@{H}</b></div>"""
    css = f""".big{{position:absolute;left:60px;top:-40px;font-family:Jost;font-weight:500;font-size:640px;line-height:1;color:{C['paper']}}}
.big::after{{content:"";position:absolute;width:90px;height:90px;border-radius:50%;background:{C['tomato']};right:-110px;bottom:150px}}
.mo{{position:absolute;left:89px;top:600px;font-family:Anuphan;font-weight:500;font-size:64px;color:{C['sun']}}}
.txt{{position:absolute;left:89px;right:89px;top:760px;display:flex;flex-direction:column;align-items:flex-start;gap:26px;color:{C['paper']}}}
.txt h1{{font-size:84px}}.txt p{{font-size:36px;line-height:1.5;opacity:.92}}"""
    return frame(body, C["cobalt"], css)


def bears():
    fam = PB._logo("family.svg", "0 55 1000 205")
    fam = fam[:fam.index("</g>", fam.rindex('<g transform="translate(')) + 4] + "</svg>"   # the five bears without the lockup text
    body = f"""<div class="fam">{fam}</div>
<div class="txt"><span class="pill" style="background:{C['pink']};color:{C['ink']}">เรื่องของเรา · 3</span>
<h1><span class="m">ห้าหมี</span><br>เพราะบ้านเรามีห้าคน</h1>
<p>หัวใจตรงกลางหมีคือแม่<br>คอลเลกชันแรกของห้าหมีชื่อ Love</p></div>
<div class="foot"><span>ห้าหมี FIVE BEARS · by OCT. 26</span><b>@{H}</b></div>"""
    css = f""".fam{{position:absolute;left:60px;right:60px;top:250px}}.fam svg{{width:100%;height:auto;display:block}}
.txt{{position:absolute;left:89px;right:89px;top:620px;display:flex;flex-direction:column;align-items:flex-start;gap:26px}}
.txt h1{{font-size:80px}}.txt h1 .m{{font-family:Mitr;font-weight:600;font-size:120px}}.txt p{{font-size:38px;line-height:1.5}}"""
    return frame(body, C["paper"], css)


ART = {"intro": intro, "leather": leather, "october": october, "bears": bears}

TAGS_IG = "#OCT26 #ourcraftedthings #หนังแท้ #งานแฮนด์เมด #ของขวัญ #leathercraft #handmade"
BOOTH = f"บูธ OCT. 26 โซน{SB.ZONE}\n{SB.FAIR}\n{SB.PLACE} {SB.HALL}\n{SB.DATES} · {SB.HOURS}"

FB_INTRO = (f"สวัสดีครับ เราคือ OCT. 26\n\n"
            "ครอบครัวห้าคน พ่อ แม่ และลูกสามคน เราเอาเศษหนังวัวแท้ที่เกือบถูกขายเหมาเป็นกระสอบ "
            "มาตัดเป็นของใช้ชิ้นเล็ก ๆ ทีละชิ้น ทุกชิ้นสีและลายไม่ซ้ำกัน\n\n"
            "ชื่อแบรนด์มาจากวันเกิดของแม่ 26 ตุลาคม และลูก ๆ ทั้งสามช่วยกันทุกขั้น ตั้งแต่เลือกหนังจนถึงขายเอง\n\n"
            f"นี่แค่แอบดูนะครับ ของจริงเจอกันครั้งแรกที่{BOOTH}\n\n"
            f"ติดตามเราได้ที่ IG @{H} และ YouTube @OCT.26_brand\n\n#OCT26 #ourcraftedthings #หนังแท้ #งานแฮนด์เมด")


def product_ig(p):
    return (f"{p['hook']}\n\n{p['name']} · {p['price']} บาท\nหนังวัวแท้ {p['pieces_txt']} · {p['size']}\n"
            f"{' → '.join(p['steps'])}\n\n"
            f"มีที่บูธ OCT. 26 โซน{SB.ZONE} {SB.DATES}\nสั่งออนไลน์: Shopee ร้าน {B.SHOP_NAME} (ลิงก์ในโปรไฟล์)\n\n"
            f"{TAGS_IG} {'#ห้าหมี #FiveBears' if p['coll'] == 'love' else '#SOI02'}")


COASTERS = [P[22], P[24], P[27], P[28]]
IG = [  # (date, time, title, pictures, caption) in posting order; the grid shows the newest first
    ("พ. 21 ต.ค.", "20:00", "แนะนำตัว (แอบดู)", ["img/intro.png"],
     f"สวัสดีครับ เราคือ OCT. 26\nครอบครัวห้าคน พ่อ แม่ และลูกสามคน ทำของใช้จากเศษหนังวัวแท้ด้วยกัน\n\n"
     f"นี่แค่แอบดู ของจริงเจอกัน {SB.WEEKENDS[0]} ที่{SB.FAIR}\n\n{TAGS_IG}"),
    ("พฤ. 22 ต.ค.", "12:00", "เรื่องของเรา 1 · เศษหนัง", ["img/leather.png"],
     "เศษหนังวัวแท้ที่เหลือจากการตัดกระเป๋าและรองเท้า เกือบถูกขายเหมาไปเป็นกระสอบ\n"
     "ชิ้นเล็กแค่ฝ่ามือ แต่เป็นหนังดีทุกชิ้น เราเลยตัดเป็นของใช้ ทีละชิ้น\n"
     "สีและลายแต่ละชิ้นไม่ซ้ำกัน ทุกชิ้นมีชิ้นเดียว\n\n" + TAGS_IG + " #upcycle"),
    ("พฤ. 22 ต.ค.", "19:00", "เชิญมาบูธ", ["img/launch-post-1080x1350.png"], SB.COPY[1][2]),
    ("ศ. 23 ต.ค.", "12:00", "สินค้า · ชุดที่รองแก้ว 4 ลาย", [f"img/{SKU[29]}.png"], product_ig(P[29])),
    ("ส. 24 ต.ค.", "12:00", "เรื่องของเรา 3 · ห้าหมี", ["img/bears.png"],
     "ห้าหมี FIVE BEARS\nหัวหมีชิ้นแรกที่ตัดออกมากลายเป็นห้าหมี เพราะบ้านเรามีห้าคน และหัวใจตรงกลางหมีคือแม่\n"
     "คอลเลกชันแรกของห้าหมีชื่อ Love\n\n#ห้าหมี #FiveBears #LoveCollection " + TAGS_IG),
    ("อา. 25 ต.ค.", "12:00", "สินค้า · ที่เก็บสายชาร์จหมี", [f"img/{SKU[1]}.png"], product_ig(P[1])),
    ("จ. 26 ต.ค.", "09:00", "เรื่องของเรา 2 · 26 ตุลาคม (วันเกิดแบรนด์)", ["img/october.png"],
     "26 ตุลาคม\nแบรนด์นี้ตั้งชื่อตามวันเกิดของแม่ และเกิดในวันเดียวกัน\n"
     "ทุกปีในวันนี้ เราจะออกรุ่นวันเกิดหนึ่งชุด เลขรุ่นคืออายุของแม่ในปีนั้น\n\n"
     f"สุดสัปดาห์นี้ลูก ๆ กลับไปที่บูธอีกรอบ {SB.WEEKENDS[1]}\n\n#OCT26 #ourcraftedthings"),
    ("อ. 27 ต.ค.", "19:00", "สินค้า · ที่รองแก้ว 4 ทรง (ปัดดู 4 รูป)", [f"img/{SKU[p['n']]}.png" for p in COASTERS],
     "ที่รองแก้วหนังวัวแท้ เลือกทรงที่ชอบ ปัดดูได้ 4 แบบ\n"
     + "\n".join(f"{p['name']} {p['price']} บาท · {p['size']}" for p in COASTERS)
     + f"\nหยิบออกจากถุงแล้ววางแก้วได้เลย\n\nสัปดาห์นี้ที่บูธ {SB.WEEKENDS[1]} หรือ Shopee ร้าน {B.SHOP_NAME}\n\n{TAGS_IG} #SOI02"),
    ("พ. 28 ต.ค.", "19:00", "สินค้า · ป้ายห้อยของขวัญ", [f"img/{SKU[26]}.png"], product_ig(P[26])),
]


def check_copy():
    for *_, cap in IG + [("", "", "", [], FB_INTRO)]:
        for word in ("เย็บ", "กาว", "ต่อเอง", "ต่อหนัง", "ต่อชิ้น"):
            assert word not in cap, (word, cap[:40])


def page():
    fb = (f'<article class="card post"><div class="pic"><img src="img/intro.png" alt="รูปแนะนำตัว OCT. 26" loading="lazy"></div>'
          f'<div class="body"><span class="chip">วันนี้ · พ. 21 ต.ค. · 19:00</span><h3>Facebook · แนะนำตัว</h3>'
          f'{S.copybox("fb", FB_INTRO, "แคปชัน")}</div></article>')
    ig = "".join(
        f'<article class="card post"><div class="pic">'
        + "".join(f'<img src="{src}" alt="{E(t)}" loading="lazy">' for src in pics[:1])
        + (f'<span class="cap">+ อีก {len(pics) - 1} รูปในโพสต์นี้</span>' if len(pics) > 1 else "")
        + f'</div><div class="body"><span class="chip">IG {i} · {E(d)} · {E(tm)}</span><h3>{E(t)}</h3>'
          f'{S.copybox(f"ig{i}", cap, "แคปชัน")}</div></article>'
        for i, (d, tm, t, pics, cap) in enumerate(IG, 1))
    grid = "".join(f'<img src="{pics[0]}" alt="IG {i}">' for i, (_, _, _, pics, _) in reversed(list(enumerate(IG, 1))))
    return f"""{S.head("OCT. 26 แนะนำตัวและ IG")}
<style>
.post{{display:grid;grid-template-columns:minmax(0,233px) minmax(0,1fr);gap:var(--s4);align-items:start}}
.post .pic{{display:flex;flex-direction:column;gap:var(--s2)}}.post img{{border-radius:var(--s3);border:1px solid var(--line)}}
.post .body{{display:flex;flex-direction:column;align-items:flex-start;gap:var(--s3);min-width:0}}.post .body>.ch{{align-self:stretch}}
.ig{{display:grid;grid-template-columns:repeat(3,1fr);gap:3px;max-width:420px}}
.ig img{{aspect-ratio:3/4;object-fit:cover;width:100%;height:auto}}
@media (max-width:600px){{.post{{grid-template-columns:1fr}}.post .pic{{max-width:233px}}}}
</style>
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · 21 ต.ค. 2569</span><h1>แนะนำตัว และ IG 9 โพสต์แรก</h1>
<p class="lead">โพสต์ Facebook วันนี้ 1 โพสต์ แนะนำครอบครัวและแอบดูชิ้นหนังก่อนถึงโพสต์เชิญพรุ่งนี้ กับ Instagram 9 โพสต์
พร้อมรูปและแคปชัน รูปใหม่ 4 แบบ ที่เหลือใช้แบนเนอร์เชิญและการ์ดสินค้าชุดเดิม</p></header>
<section><span class="eyebrow">วันนี้</span><h2>Facebook</h2>{fb}</section>
<section><span class="eyebrow">หน้าโปรไฟล์ IG หลังลงครบ 9 โพสต์</span><h2>ตาราง 3 × 3</h2><div class="ig">{grid}</div>
<p class="cap">โพสต์ล่าสุดอยู่ซ้ายบน · หน้าโปรไฟล์ตัดรูปเป็น 3:4 ข้อความทุกรูปอยู่ในส่วนที่ไม่โดนตัด</p></section>
<section><span class="eyebrow">Instagram</span><h2>9 โพสต์ ตามลำดับที่ลง</h2>{ig}</section>
<section><h2>ต้องเช็ก</h2><div class="card"><ol>
<li>ราคาในโพสต์สินค้ายังเป็นราคาร่างตามหน้าสถานะ ยืนยันก่อนวันที่ 23 ต.ค.</li>
<li>ใส่ลิงก์ร้าน Shopee ในโปรไฟล์ IG ก่อนโพสต์สินค้าแรก</li>
<li>รูปลูก ถ้าจะเพิ่มเอง ถ่ายมือเป็นหลัก ไม่บอกชื่อจริง และถามลูกก่อน</li></ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">intro-20261021/img/*.png</td><td>รูปทั้งหมด 1080 × 1350</td></tr>
<tr><td class="mono" style="white-space:nowrap">intro-20261021/build.py</td><td>รูปใหม่และแคปชัน แก้แล้วรันใหม่</td></tr>
<tr><td>Google Drive โฟลเดอร์ "OCT. 26 โพสต์ FB และ IG"</td><td>เอกสารรูปพร้อมแคปชัน ในโฟลเดอร์ OCT. 26 ไฟล์งาน</td></tr>
</tbody></table></div></section></div>{S.COPY_JS}"""


def doc_html(posts, title):
    """HTML for a Google Doc: Drive converts it and fetches each picture from GitHub."""
    out = [f"<html><body><h1>{E(title)}</h1>"]
    for head, pics, cap in posts:
        out.append(f"<h2>{E(head)}</h2>")
        out += [f'<p><img src="{RAW}intro-20261021/{src}" width="300" height="375"></p>' for src in pics]
        out.append("<p>" + "<br>".join(E(line) for line in cap.split("\n")) + "</p><hr>")
    return "\n".join(out) + "</body></html>"


if __name__ == "__main__":
    check_copy()
    img = os.path.join(HERE, "img"); os.makedirs(img, exist_ok=True)
    jobs = []
    for name, fn in ART.items():
        open(os.path.join(img, name + ".html"), "w").write(fn())
        jobs.append(dict(src=os.path.join(img, name + ".html"), out=os.path.join(img, name + ".png"), w=1080, h=1350))
    json.dump(jobs, open(os.path.join(img, "jobs.json"), "w"), indent=0)
    for p in SALE:
        shutil.copyfile(os.path.join(REPO, "facebook-20261021", "cards", SKU[p["n"]] + ".png"), os.path.join(img, SKU[p["n"]] + ".png"))
    shutil.copyfile(os.path.join(REPO, "social-20261021", "banners", "launch-post-1080x1350.png"),
                    os.path.join(img, "launch-post-1080x1350.png"))
    site = os.path.join(HERE, "site"); os.makedirs(site, exist_ok=True)
    open(os.path.join(site, "index.html"), "w").write(page())
    open(os.path.join(HERE, "doc-fb.html"), "w").write(
        doc_html([("Facebook · วันนี้ พ. 21 ต.ค. 19:00 · แนะนำตัว", ["img/intro.png"], FB_INTRO)], "OCT. 26 Facebook โพสต์แนะนำตัว"))
    open(os.path.join(HERE, "doc-ig.html"), "w").write(
        doc_html([(f"IG {i} · {d} {tm} · {t}", pics, cap) for i, (d, tm, t, pics, cap) in enumerate(IG, 1)],
                 "OCT. 26 Instagram 9 โพสต์แรก"))
    print("wrote", len(jobs), "pictures to render, site/index.html, doc-fb.html, doc-ig.html")
