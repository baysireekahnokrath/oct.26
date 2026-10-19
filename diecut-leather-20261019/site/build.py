"""Thai summary page for pattern 07: the 1:1 outline, the show-tip circle, the numbers and the files.

python3 site/build.py -> site/index.html (reads ../svg/07-round-joint-cross.svg)
"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
s = open(os.path.join(ROOT, "svg", "07-round-joint-cross.svg")).read()
D = re.search(r'<path d="([^"]+)"', s).group(1)
SL = re.findall(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"', s)
FOLD = 73.43            # fold line of the right tab, from the left edge (y-down SVG frame is symmetric)
SLIT = 16.57            # slit line of a slit edge, from that edge
OFF = FOLD - SLIT       # where piece B starts so its slit sits on A's fold line

def piece(x, y, fill, rot=0, clip=None):
    sl = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" class="sl"/>' for a, b, c, d in SL)
    cp = f' clip-path="url(#{clip})"' if clip else ""
    return f'<g transform="translate({x},{y}) rotate({rot},45,45)"{cp}><path d="{D}" class="pc" style="fill:{fill}"/>{sl}</g>'

def pair(mode, uid):
    defs = (f'<clipPath id="{uid}c"><rect x="-5" y="-5" width="{FOLD + 5}" height="100"/></clipPath>'
            f'<clipPath id="{uid}l"><rect x="{FOLD}" y="-5" width="40" height="100"/></clipPath>')
    A_core = piece(0, 0, "var(--l1)", clip=f"{uid}c")
    A_lobe = piece(0, 0, "var(--l1)", clip=f"{uid}l")
    B = piece(OFF, 0, "var(--l2)", rot=90)
    body = (A_core + B + A_lobe) if mode == "show" else (A_lobe + B + A_core)
    ring = (f'<circle cx="{FOLD}" cy="45" r="16.57" class="ring"/>' if mode == "show" else "")
    return f'<svg viewBox="-3 -3 {OFF + 96} 96" role="img" aria-label="ต่อสองชิ้นแบบ{"โชว์" if mode == "show" else "ซ่อน"}ปลาย"><defs>{defs}</defs>{body}{ring}</svg>'

def outline():
    sl = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" class="sl"/>' for a, b, c, d in SL)
    dims = ('<line x1="0" y1="96" x2="90" y2="96" class="dm"/><text x="45" y="101" class="dt">90.00</text>'
            '<circle cx="45" cy="16.57" r="16.57" class="ghost"/><circle cx="45" cy="16.57" r="0.8" class="cm"/>'
            '<line x1="0" y1="16.57" x2="90" y2="16.57" class="fold"/>'
            '<text x="64" y="12" class="dt">R16.57</text>')
    return f'<svg viewBox="-4 -4 98 108" role="img" aria-label="แบบ 07 ขนาดจริง 90 × 90 มม."><path d="{D}" class="pc" style="fill:var(--card)"/>{sl}{dims}</svg>'

ROWS = [("ขนาดชิ้น", "90.00 × 90.00 มม. (เท่า 06)"), ("กลีบ", "ครึ่งวงกลม R16.57 × 4 จุดศูนย์กลางห่างกลางชิ้น 28.43"),
        ("แนวพับ", "ผ่านจุดศูนย์กลางกลีบ คลาดไม่เกิน 0.01 มม."), ("วงกลมเมื่อโชว์ปลาย", "เส้นผ่านศูนย์กลาง 33.15 มม. ทุกรอยต่อ"),
        ("slit (ร่อง)", "17.10 มม. × 2 (จากแบบ 16.60 เพิ่ม 0.50)"), ("คอปีก", "16.60 มม. = slit − 0.5"),
        ("รอยตัดคอปีก", "9.27 มม. × 4 (เข้าเนื้อ 8.27 + เลยขอบ 1.00)"), ("ร่องเว้าที่มุม", "R11.84 × 4 ต่อกับโคนกลีบที่แนวพับพอดี"),
        ("เนื้อหนังรอบปลาย slit", "8.02 มม. (เกณฑ์ 8.0)"), ("พื้นที่หนัง", "45.2 ตร.ซม.")]

def page():
    rows = "".join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in ROWS)
    return f"""<title>Pattern 07 Round-joint Cross</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@500;600&family=IBM+Plex+Sans+Thai:wght@400;600&family=Jost:wght@500&display=swap">
<style>
/* layout: drawing sheet feel - the 1:1 part, then the two joint looks side by side, then numbers and files */
:root{{--paper:#FFF6EC;--ink:#1C1B22;--muted:#5E5A66;--line:#E3D6C4;--cobalt:#2449D8;--tomato:#FF5A36;--card:#FFFFFF;
  --l1:#C68A4E;--l2:#7B4A2B;
  --display:'Anuphan','IBM Plex Sans Thai',sans-serif;--body:'IBM Plex Sans Thai',sans-serif;--latin:'Jost','IBM Plex Sans Thai',sans-serif}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--paper:#17161C;--ink:#F4EDE3;--muted:#B3ACA3;--line:#34313B;--cobalt:#8FA6FF;--tomato:#FF7A5C;--card:#211F27;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#17161C;--ink:#F4EDE3;--muted:#B3ACA3;--line:#34313B;--cobalt:#8FA6FF;--tomato:#FF7A5C;--card:#211F27;color-scheme:dark}}
body{{background:var(--paper);color:var(--ink);font:400 16px/1.7 var(--body)}}
.wrap{{max-width:900px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:34px 89px;display:flex;flex-direction:column;gap:34px}}
h1,h2{{font-family:var(--display);font-weight:600;line-height:1.25;margin:0;text-wrap:balance}} h1{{font-size:clamp(28px,6vw,41.9px)}} h2{{font-size:22px}}
p{{margin:0}} .eyebrow{{font:500 12.6px var(--latin);letter-spacing:.14em;color:var(--cobalt)}}
.col{{display:flex;flex-direction:column;gap:13px}}
.hero{{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:21px;align-items:center}}
@media (max-width:620px){{.hero{{grid-template-columns:1fr}}}}
.pic{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:13px;max-width:100%}}
.pic svg{{display:block;width:100%;height:auto}}
.pair{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:21px}}
@media (max-width:620px){{.pair{{grid-template-columns:1fr}}}}
figure{{margin:0;display:flex;flex-direction:column;gap:8px}} figcaption{{font-size:15px}} figcaption b{{font-family:var(--display);font-weight:600}}
.tbl{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:15px}}
th,td{{text-align:left;padding:8px 12px 8px 0;border-bottom:1px solid var(--line);vertical-align:top}} th{{font-weight:600;white-space:nowrap}}
td{{font-variant-numeric:tabular-nums}}
ul,ol{{margin:0;padding-left:1.3em;display:flex;flex-direction:column;gap:6px;max-width:68ch}}
code{{font-size:14px}}
.pc{{stroke:var(--ink);stroke-width:.45;stroke-linejoin:round}} .sl{{stroke:var(--tomato);stroke-width:.7}}
.ring{{fill:none;stroke:var(--cobalt);stroke-width:.6;stroke-dasharray:2 1.4}}
.ghost{{fill:none;stroke:var(--cobalt);stroke-width:.35;stroke-dasharray:1.5 1}} .cm{{fill:var(--cobalt)}}
.fold{{stroke:var(--cobalt);stroke-width:.3;stroke-dasharray:1.2 1}} .dm{{stroke:var(--muted);stroke-width:.3}}
.dt{{font:500 4.2px var(--latin);fill:var(--muted);text-anchor:middle}}
</style>
<div class="wrap">
<section class="hero">
  <div class="pic">{outline()}</div>
  <div class="col"><span class="eyebrow">แม่พิมพ์ 07 · ROUND-JOINT CROSS · 19 ต.ค. 2569</span>
  <h1>แบบ 07 กากบาทข้อต่อวงกลม</h1>
  <p>ปรับจาก 06 ให้กลีบทุกด้านเป็นครึ่งวงกลมพอดี และแนวพับผ่านจุดศูนย์กลางกลีบ เมื่อต่อแบบโชว์ปลาย กลีบของสองชิ้นจะชนกันเป็นวงกลมเต็มวงทุกรอยต่อ</p></div>
</section>
<section class="col"><h2>ต่อสองชิ้น เทียบซ่อนปลายกับโชว์ปลาย</h2>
  <div class="pair">
    <figure><div class="pic">{pair("show", "s")}</div><figcaption><b>โชว์ปลาย</b> สอดกลีบจากหลังมาหน้า กลีบสองชิ้นอยู่ด้านหน้า คนละฝั่งรอยต่อ ได้วงกลม Ø33.15 มม. (เส้นประน้ำเงิน)</figcaption></figure>
    <figure><div class="pic">{pair("hide", "h")}</div><figcaption><b>ซ่อนปลาย</b> สอดกลีบจากหน้าไปหลัง กลีบทั้งสองไปอยู่ด้านหลัง หน้าชิ้นเรียบ</figcaption></figure>
  </div>
  <p style="font-size:15px;color:var(--muted)">ต่อเป็นแผ่น 4 ชิ้นมาชนมุมกัน ร่องเว้าที่มุมจะประกบเป็นรูกลม Ø23.7 มม. ส่วนความหนาหนังอาจทำให้วงกลมรีเล็กน้อย ราว 1 มม. ควรดูจากต้นแบบ</p>
</section>
<section class="col"><h2>ขนาดที่ตรวจแล้ว</h2><div class="tbl"><table><tbody>{rows}</tbody></table></div>
  <p style="font-size:15px;color:var(--muted)">แก้จากไฟล์ต้นฉบับจุดเดียว: slit 16.60 เป็น 17.10 มม. ตกลงกัน 19 ต.ค. รอยตัดคอปีกเลยขอบ 1.0 มม. ตามชุดเดิม (ต้นฉบับ 1.7)</p></section>
<section class="col"><h2>ไฟล์</h2><ul>
  <li>แบบ 1:1 สำหรับร้านทำบล็อก: <code>diecut-leather-20261019/diecut-drawings-1to1-07-rev20261019.pdf</code> พิมพ์ A4 ขนาดจริง 100%</li>
  <li>DXF แยกเลเยอร์ CUT / SLIT (ส่วนโค้งเป็นโค้งจริง): <code>dxf/07-round-joint-cross.dxf</code></li>
  <li>SVG: <code>svg/07-round-joint-cross.svg</code> · ไฟล์ต้นฉบับจากผู้ออกแบบ: <code>source-20261019.pdf</code></li>
  <li>สร้างใหม่ได้ด้วย <code>python3 diecut-leather-20261019/generate07.py</code> ชุดแบบ 01–06 เดิมไม่ถูกแก้</li></ul></section>
<section class="col"><h2>ก่อนสั่งบล็อก</h2><ol>
  <li>พิมพ์แบบ 1:1 วัดไม้บรรทัด 100 มม. ในแผ่นให้ตรง แล้ววางเทียบกับเศษหนังจริง</li>
  <li>ตัดต้นแบบด้วยมือจากกระดาษแข็งหรือหนัง 2 ชิ้น ลองต่อแบบโชว์ปลาย ดูว่าวงกลมกลม และสอดผ่าน slit 17.1 ได้ไม่ฝืด</li>
  <li>ขอใบเสนอราคาบล็อก 07 (ชุดเดิม 550–600 บาทต่อแบบ)</li>
  <li>แบบแนวคิดใน Pattern Lab เปลี่ยนเป็น A–E แล้ว เลข 07 ใช้กับแบบนี้</li></ol></section>
</div>
"""

if __name__ == "__main__":
    open(os.path.join(HERE, "index.html"), "w").write(page())
    print("ok")
