"""Thai summary page for the Shopee upload files -> shopee-20261021/site/index.html (publish with posters/thumb as t/NN.jpg)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "brand-20261014"))
import brand as B
from build import SHOPEE_STOCK, HEAVY, IMG, HOLD_PIECES, SKU, split

ready, held = split()
hold_names = " ".join(B.PIECE_NAME[c] for c in sorted(HOLD_PIECES))


def card(p):
    return (f'<li><img src="t/{p["n"]:02d}.jpg" alt="{p["name"]}" width="360" height="450" loading="lazy">'
            f'<b>{p["name"]}</b><span class="meta">{SKU[p["n"]]} · ชิ้นเดียว ไม่ต้องต่อ</span>'
            f'<span class="row"><span class="price">฿{p["price"]}</span>'
            f'<span>คลัง {min(p["stock"], SHOPEE_STOCK)} · {0.2 if p["n"] in HEAVY else 0.1} กก.</span></span></li>')


def line(p):
    return f'<li><span>{SKU[p["n"]]}</span> {p["name"]} <em>฿{p["price"]}</em></li>'


html = f"""<title>OCT. 26 Shopee Upload</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@500;700&family=IBM+Plex+Sans+Thai:wght@400;600&family=Jost:wght@500;700&display=swap">
<style>
/* one column, phone first: what was made, the 13 products, what to check, then the 17 on hold */
:root{{--paper:#FFF6EC;--ink:#1C1B22;--soft:#5B5866;--line:#E9DCCB;--card:#FFFFFF;--cobalt:#2449D8;--tomato:#FF5A36;--sun:#FFC83D;--mint:#3CC8A0;
--th:"Anuphan","IBM Plex Sans Thai",system-ui,sans-serif;--body:"IBM Plex Sans Thai",system-ui,sans-serif;--lat:"Jost","IBM Plex Sans Thai",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#16151B;--ink:#FFF6EC;--soft:#B9B3C2;--line:#2E2C36;--card:#201F27;--cobalt:#7F9BFF;--tomato:#FF7A5C;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#16151B;--ink:#FFF6EC;--soft:#B9B3C2;--line:#2E2C36;--card:#201F27;--cobalt:#7F9BFF;--tomato:#FF7A5C;color-scheme:dark}}
body{{background:var(--paper);color:var(--ink);font:400 16px/1.7 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
main{{max-width:760px;margin:0 auto;padding-block:34px 55px;display:grid;gap:34px}}
h1,h2{{font-family:var(--th);text-wrap:balance;margin:0;line-height:1.25}}
h1{{font-size:clamp(28px,7vw,42px)}} h2{{font-size:22px}}
.eyebrow{{font:700 13px/1 var(--lat);letter-spacing:.12em;text-transform:uppercase;color:var(--cobalt)}}
p{{margin:0;max-width:62ch}} section{{display:grid;gap:13px}}
.nums{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}}
.nums div{{border:1.5px solid var(--ink);border-radius:13px;padding:13px;display:grid;gap:2px}}
.nums b{{font:700 30px/1.1 var(--lat);font-variant-numeric:tabular-nums}} .nums span{{color:var(--soft);font-size:14px}}
.files{{display:grid;gap:8px;margin:0;padding:0;list-style:none}}
.files li{{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px;display:grid;gap:3px;min-width:0}}
code{{font:500 14px/1.4 var(--lat);overflow-wrap:anywhere}} .files .ok{{color:var(--mint);font-weight:600}} .files .hold{{color:var(--tomato);font-weight:600}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:13px;margin:0;padding:0;list-style:none}}
.grid li{{display:grid;gap:3px;min-width:0}} .grid img{{width:100%;height:auto;border-radius:8px;background:var(--line)}}
.grid b{{font-family:var(--th);font-size:15px;line-height:1.35}} .meta{{font:500 12px/1.3 var(--lat);color:var(--soft)}}
.row{{display:flex;justify-content:space-between;gap:8px;font-size:13px;color:var(--soft)}} .price{{color:var(--tomato);font:700 16px/1.2 var(--lat)}}
.cols{{overflow-x:auto}} table{{border-collapse:collapse;font-size:14px;min-width:420px;width:100%}}
td,th{{text-align:left;padding:8px;border-bottom:1px solid var(--line);vertical-align:top}} th{{font:600 13px/1.3 var(--lat);color:var(--soft)}}
ol.check{{margin:0;padding-left:1.3em;display:grid;gap:8px}}
.later{{columns:2 220px;margin:0;padding:0;list-style:none;font-size:14px}} .later li{{break-inside:avoid;padding:3px 0}}
.later span{{font:600 12px var(--lat);color:var(--soft)}} .later em{{font-style:normal;color:var(--tomato);font-family:var(--lat)}}
</style>
<main>
<header style="display:grid;gap:8px">
<span class="eyebrow">Shopee · {B.SHOP_NAME}</span>
<h1>ไฟล์ลงสินค้า Shopee พร้อมอัป</h1>
<p>กรอกในฟอร์มของ Shopee ที่พ่อเบส่งมา (แบบพื้นฐาน 21 ต.ค.) ใส่เฉพาะสินค้าชิ้นเดียวตามหน้า "OCT. 26 สถานะล่าสุด" เพราะข้อต่อยังไม่ผ่านการทดสอบ และ 06 ไม่ได้ตัด SKU ตรงกับ Google Sheet บัญชี ภาพปกเป็นโปสเตอร์ How-to บน {B.SOCIAL["web"]}</p>
</header>
<div class="nums">
<div><b>{len(ready)}</b><span>ชิ้น พร้อมอัปตอนนี้</span></div>
<div><b>{len(held)}</b><span>ชิ้น พักไว้ ใช้ {hold_names}</span></div>
<div><b>{SHOPEE_STOCK}</b><span>คลังต่อชิ้น (แบ่งจากบูธ)</span></div>
</div>
<section><h2>ไฟล์</h2>
<ul class="files">
<li><code>shopee-20261021/oct26-shopee-ready.xlsx</code><span class="ok">อัปไฟล์นี้ก่อน · {len(ready)} ชิ้น</span></li>
<li><code>shopee-20261021/build.py</code><span>รายการ SKU ที่ขายอยู่ในไฟล์นี้ แก้แล้วรันใหม่ ได้ไฟล์ใหม่ทันที</span></li>
<li><span>Google Sheet สำหรับเปิดดู "OCT. 26 Shopee สินค้าที่จะลง" ในโฟลเดอร์ OCT. 26 ไฟล์งาน</span></li>
</ul></section>
<section><h2>{len(ready)} ชิ้นในไฟล์ ready</h2>
<ul class="grid">{"".join(card(p) for p in ready)}</ul></section>
<section><h2>กรอกอะไรไว้บ้าง</h2>
<div class="cols"><table>
<tr><th>ช่อง</th><th>ใส่อะไร</th></tr>
<tr><td>ชื่อสินค้า</td><td>ชื่อ + หนังวัวแท้ งานแฮนด์เมด OCT. 26 + คอลเลกชัน (62–80 ตัวอักษร) ไม่มีคำว่า ต่อเอง หรือ ไม่ต้องเย็บ</td></tr>
<tr><td>รายละเอียด</td><td>ประโยคเปิด วัสดุ (หนา 1.0–1.2 มม.) ชิ้นที่ใช้ ขนาด เหมาะกับใคร วิธีใช้ การดูแล ไม่มีลิงก์ภายนอก</td></tr>
<tr><td>ราคา · SKU</td><td>ราคาร่างตามหน้าสถานะ (รอยืนยัน) · OC-01-01, OC-01-22, OC-03-26, OC-04-27, OC-05-28</td></tr>
<tr><td>ภาพปก</td><td><code>{IMG.format(1)}</code> ฯลฯ</td></tr>
<tr><td>น้ำหนัก</td><td>0.1 กก. ทุกชิ้น</td></tr>
<tr><td>ส่งธรรมดา</td><td>เปิด</td></tr>
<tr><td>เว้นว่าง</td><td>หมวดหมู่ (ให้ Shopee แนะนำตอนตรวจ) ขนาดกล่อง ตัวเลือกสินค้า พรีออเดอร์</td></tr>
</table></div></section>
<section><h2>ต้องเช็กก่อนกดอัป</h2>
<ol class="check">
<li>เปิด <code>{IMG.format(1)}</code> บนมือถือให้ขึ้นรูปก่อน Shopee ดึงภาพจากลิงก์นี้ ถ้าไม่ขึ้นภาพจะว่าง</li>
<li>Seller Centre → สินค้าของฉัน → เพิ่มสินค้าหลายรายการ → อัปโหลดไฟล์ ready แล้วดูหน้าตรวจ ถ้า Shopee ขอหมวดหมู่ ให้เลือก ของใช้ในบ้าน หรือ เครื่องเขียน ตามสินค้า</li>
<li>คลังตั้งไว้ {SHOPEE_STOCK} ชิ้นต่อแบบ เพราะใช้ของชุดเดียวกับบูธ 23 ต.ค.–1 พ.ย. หลังงานค่อยเพิ่ม</li>
<li>น้ำหนักเป็นค่าประมาณ ชั่งของจริงพร้อมซองแล้วแก้ใน Seller Centre ค่าส่งจะตรง</li>
<li>ภาพปกเป็นแนวตั้ง 4:5 Shopee จะครอปเป็นจัตุรัส ภายหลังถ่ายรูปสินค้าจริงเพิ่มได้ในช่องรูปภาพ 1–8</li>
<li>ราคายังเป็นราคาร่าง ยืนยันแล้วแก้ใน Seller Centre หรือบอกให้ทำไฟล์ใหม่</li>
<li>หน้าสถานะเขียนว่างานเว็บและหน้าร้านออนไลน์ควรรอเรื่องแบรนด์ และยังไม่มีรูปถ่ายสินค้าจริง ตัดสินใจก่อนว่าจะเปิด Shopee ตอนนี้หรือรอ</li>
</ol></section>
<section><h2>{len(held)} ชิ้นที่พักไว้ เพราะใช้ {hold_names}</h2>
<p>พ่อเบสั่งให้เอาสินค้าที่ใช้ {hold_names} ออก แต่หน้าสถานะยังนับ 2 ชิ้นนี้ในของขายที่บูธ ถ้าจะขายใน Shopee ด้วย บอกได้ จะใส่กลับให้</p>
<ul class="later">{"".join(line(p) for p in held)}</ul></section>
</main>
"""
os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
open(os.path.join(HERE, "site", "index.html"), "w").write(html)
print("wrote site/index.html")
