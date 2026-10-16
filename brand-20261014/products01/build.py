"""50 product ideas for die 01 (bear head), priced up to 1,500 THB, with two ways to show each joint.

Joint geometry, measured from ../../diecut-leather-20261014/svg/01-bear-head.svg:
  right ear -> left cheek slit of the bear to the right, top ear -> chin slit of the bear above, both at 71.4 mm,
  so bears join in rows, columns, grids and rings. Costs use brand.py (piece, joint, packing) plus estimated extras.

python3 products01/build.py -> products01/site/index.html
"""
import html, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import brand as B
E = html.escape
OUT = os.path.join(HERE, "site"); os.makedirs(OUT, exist_ok=True)

s = open(os.path.join(ROOT, "..", "diecut-leather-20261014", "svg", "01-bear-head.svg")).read()
BEAR_D = re.search(r'<g id="CUT".*?<path d="([^"]+)"', s, re.S).group(1)
SL = [tuple(map(float, m)) for m in re.findall(r'x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"', s)]
NECK_X, TOP_NECK_Y, PITCH = 82.59, 21.77, 71.39

PC, JC, LAB = B.PIECE_COST["01"], B.JOINT_COST, B.PACK_COST
PACK = {k: sum(B.PACK_ITEMS[x][2] for x in v[1]) for k, v in B.PACK_PROFILE.items()}

# look: ซ่อน = tips hidden behind (clean), โชว์ = tips shown on the front (bears peeking), เลือกได้ = sold in both looks, — = no joint
# (group, name, bears, joints, extras THB, extras note, pack, price, look, why, star)
G = [
 ("ห้อยกระเป๋าและพกติดตัว", "กระแสที่ห้อยกระเป๋าจากไทยไปทั่วโลก และของปั๊มชื่อ ราคาตลาดพวงกุญแจหนังแท้ 59–119 บาท", [
  ("พวงกุญแจหมีปั๊มอักษรย่อ", 1, 0, 6, "ห่วงโลหะ", "flat", 99, "—", "ราคาเปิดประตู เท่ากับตลาดพวงกุญแจหนังแท้", True),
  ("ที่ห้อยกระเป๋าหมีปั๊มชื่อ", 1, 0, 8, "ห่วงก้ามปู", "flat", 129, "—", "ของปั๊มชื่อคือแกนของตลาดของขวัญปีนี้", True),
  ("ห้อยกระเป๋าหมีกอด 2 ตัว", 2, 1, 8, "ห่วงก้ามปู", "flat", 199, "โชว์", "หูโผล่บนแก้มอีกตัวเหมือนกอดกัน ขายคู่รักและเพื่อนซี้", True),
  ("ห้อยกระเป๋าหมีครอบครัว 3 ตัว", 3, 2, 8, "ห่วงก้ามปู", "flat", 249, "เลือกได้", "ต่อลงเป็นสาย ปั๊มชื่อพ่อ แม่ ลูก", False),
  ("ห้อยกระเป๋าหมีครอบครัว 5 ตัว", 5, 4, 8, "ห่วงก้ามปู", "flat", 349, "เลือกได้", "ห้าหมีห้าสีของบ้านเรา เป็นเรื่องเล่าของแบรนด์", False),
  ("บัตรห้อยคอเด็ก ชื่อ + เบอร์พ่อแม่", 1, 0, 15, "สายคล้องคอแบบหลุดได้", "flat", 199, "—", "ของปลอดภัยสำหรับพาลูกเที่ยว ใช้ที่บูธได้ทันที", True),
  ("ป้ายชื่อกระเป๋านักเรียน", 1, 0, 6, "สายผ้า 15 มม.", "flat", 149, "—", "ขายช่วงเปิดเทอม ร้อยสายผ่านร่องทั้งสอง", False),
  ("ป้ายชื่อสัตว์เลี้ยง", 1, 0, 0, "", "flat", 129, "—", "ร้อยปลอกคอเดิมผ่านร่อง ตลาดสัตว์เลี้ยงโตทุกปี", False),
 ]),
 ("โต๊ะทำงานและของใช้ทุกวัน", "ของขวัญปีนี้เน้นใช้ได้จริงและมีคุณค่าทางใจ งบจับฉลาก 300–500 บาท", [
  ("ที่เก็บสายชาร์จหมี", 1, 0, 0, "", "flat", 59, "—", "ปัญหาที่ทุกคนมี ราคาหยิบง่าย", False),
  ("ชุดเก็บสาย 3 ตัว", 3, 0, 2, "เชือกมัด", "flat", 149, "—", "สายชาร์จ หูฟัง นาฬิกา ครบชุด ของขวัญจับฉลาก", True),
  ("ที่คั่นหนังสือหมี", 1, 0, 0, "", "flat", 59, "—", "ต้องลองวิธีเหน็บมุมกระดาษกับต้นแบบก่อน", False),
  ("ปลอกโหลใส่ปากกา วง 4", 4, 4, 25, "โหลแก้ว", "wrap", 390, "ซ่อน", "โต๊ะทำงานดูอบอุ่น ซ่อนปลายให้ผิวเรียบ", True),
  ("ที่ใส่ปากกาทรงสูง วง 4 × 2 ชั้น", 8, 12, 25, "แก้วทรงสูง", "wrap", 490, "โชว์", "หูโผล่สองชั้นเป็นลาย ใส่ไม้บรรทัดได้", False),
  ("ปลอกแก้วกาแฟ วง 5", 5, 5, 0, "", "flat", 249, "ซ่อน", "คาเฟ่ปั๊มโลโก้ได้ ใช้ร่วมกับแก้วกระดาษ 16 ออนซ์", False),
  ("ปลอกแก้วเก็บความเย็น วง 5 × 2 ชั้น", 10, 15, 0, "", "wrap", 590, "เลือกได้", "แก้วเก็บความเย็นเป็นของขวัญยอดฮิต ขายปลอกให้เข้าชุด", False),
  ("แผ่นรองเมาส์ ตาราง 3 × 3", 9, 12, 0, "", "wrap", 490, "ซ่อน", "หน้าเรียบไม่สะดุดเมาส์ หลังหนังกันลื่น", False),
 ]),
 ("โต๊ะอาหารและครัว", "ของแต่งบ้านงานมือและวัสดุมีผิวสัมผัสเป็นเทรนด์ปี 2026", [
  ("ที่รองแก้วหมี", 1, 0, 0, "", "flat", 59, "—", "ขายง่ายที่สุด ซื้อเพิ่มเป็นชุดได้", False),
  ("ชุดที่รองแก้วห้าสีครอบครัว", 5, 0, 2, "เชือกมัด", "wrap", 249, "—", "ห้าคนห้าสี ไม่ต้องจำว่าแก้วไหนของใคร", True),
  ("ที่รองหม้อร้อน ตาราง 2 × 2", 4, 4, 0, "", "wrap", 199, "ซ่อน", "ทดสอบกลไกตารางหมีได้ก่อนตัวใหญ่", True),
  ("แผ่นรองจาน ตาราง 3 × 4", 12, 17, 0, "", "wrap", 450, "เลือกได้", "ซ่อนปลายดูหรู โชว์ปลายดูสนุก ขายได้สองแบบ", False),
  ("ผ้ารองกลางโต๊ะ ตาราง 3 × 10", 30, 47, 0, "", "kit", 990, "ซ่อน", "ชิ้นใหญ่ราคาสูง เหมาะร้านอาหารและของขึ้นบ้านใหม่", False),
  ("ห่วงผ้าเช็ดปากหมี (ร้อยเชือก)", 1, 0, 3, "เชือกหนัง", "flat", 79, "—", "ใช้เชือกแทนสายหัวใจที่ยังไม่มีบล็อก", False),
  ("ถาดกลีบหมี 5 ตัว", 5, 4, 0, "", "wrap", 290, "โชว์", "พับกลีบขึ้น หูโผล่เป็นขอบ ใส่กุญแจหรือเครื่องประดับ", False),
 ]),
 ("ของแต่งบ้านและผนัง", "งานผ้าและงานแขวนผนังทำมือกำลังมา คนซื้อเพราะเรื่องราวมากกว่าความเป๊ะ", [
  ("ราวหมีห้าตัว", 5, 4, 5, "เชือก", "wrap", 349, "เลือกได้", "สินค้าเดิมหน้าบูธ ขายสองแบบ ซ่อนกับโชว์ปลาย", True),
  ("ราวชื่อหมี 6 ตัวอักษร", 6, 5, 5, "เชือก", "wrap", 390, "โชว์", "ตัวอักษรละ 59 บาท เพิ่มได้ ของขวัญห้องเด็ก", True),
  ("ราว HAPPY BIRTHDAY", 13, 12, 5, "เชือก", "wrap", 790, "โชว์", "ใช้ซ้ำทุกปี ตรงกับแบรนด์วันเกิด", False),
  ("ผ้าแขวนผนังครอบครัว 5 × 5", 25, 40, 40, "ไม้แขวน", "kit", 1290, "เลือกได้", "ไล่สีห้าคน ชิ้นเรือธงของห้าหมี", True),
  ("กรอบรูปหมี 4 × 4 เว้นกลาง", 12, 12, 45, "แผ่นหลังและแผ่นใส", "wrap", 690, "โชว์", "ขอบหูโผล่รอบรูป ของขวัญรับปริญญาและวันเกิด", False),
  ("ป้ายหน้าประตูบ้าน 3 × 3 เว้นกลาง", 8, 8, 60, "ป้ายไม้ชื่อบ้าน", "wrap", 590, "ซ่อน", "ของขวัญขึ้นบ้านใหม่", False),
  ("ปลอกแจกัน วง 5 × 2 ชั้น", 10, 15, 0, "", "wrap", 590, "ซ่อน", "ปลอกขวดหรือโหลเก่า เข้ากับเรื่องของเหลือใช้", False),
  ("ปลอกกระถางแคคตัส วง 4", 4, 4, 0, "", "wrap", 290, "ซ่อน", "ของชำร่วยกับต้นไม้เล็กกำลังนิยม", False),
  ("ตะกร้าหมี 4 × 4 ตัดมุม", 12, 12, 0, "", "kit", 690, "โชว์", "ผนังเอนเหมือนกลีบ ใส่ผลไม้หรือของจิปาถะ", False),
  ("โป๊ะโคมไฟ วง 6 × 2 ชั้น (LED)", 12, 18, 150, "ชุดสายไฟและหลอด LED", "kit", 1190, "ซ่อน", "แสงลอดรอยต่อเป็นลายหมี ใช้ LED เท่านั้น", False),
  ("ม่านหน้าต่างหมี 4 สาย × 8 ตัว", 32, 28, 30, "ราวแขวน", "kit", 790, "โชว์", "ม่านเล็กหน้าต่างครัว ใช้หมีน้อยกว่าม่านประตู", False),
 ]),
 ("เด็กและครอบครัว", "พ่อแม่มองหาของเล่นที่มีประโยชน์และเป็นมิตรกับโลก", [
  ("มงกุฎวันเกิดหมี 7–8 ตัว", 8, 8, 0, "", "wrap", 590, "โชว์", "หูบนชี้ขึ้นเป็นยอดมงกุฎ ใส่ถ่ายรูปวันเกิด", True),
  ("ไม้วัดส่วนสูงลูก 21 ตัว", 21, 20, 40, "ไม้แขวน", "kit", 1290, "ซ่อน", "ของขวัญที่อยู่กับบ้านนานหลายปี ปั๊มตัวเลขหลังต่อจริง", False),
  ("โมบายแขวนเปล 5 ตัว", 5, 0, 40, "ห่วงไม้และด้าย", "kit", 490, "—", "สีครอบครัวห้าสี แขวนให้พ้นมือเด็ก", False),
  ("ชุดตัวต่อหมี 20 ตัว", 20, 0, 0, "", "kit", 590, "เลือกได้", "เด็กเลือกเองว่าจะซ่อนหรือโชว์ปลาย เป็นของเล่นฝึกมือ", True),
  ("เกมจับคู่ความจำ 16 ตัว", 16, 0, 0, "", "kit", 390, "—", "ปั๊มสัญลักษณ์ 8 คู่ ไม่ต้องต่อ", False),
  ("ป้ายประตูห้องลูก 2 × 2", 4, 4, 5, "เชือก", "wrap", 290, "โชว์", "ปั๊มชื่อลูกตัวละตัวอักษร", False),
  ("ชุดรับขวัญเด็กแรกเกิด", 12, 8, 70, "กล่องและอุปกรณ์", "kit", 1290, "เลือกได้", "บัตรชื่อ ราวชื่อ โมบาย ในกล่องเดียว", False),
 ]),
 ("เทศกาล", "ความต้องการของขวัญพุ่งช่วงเทศกาล บูธจบแล้วต่อด้วยคริสต์มาสและปีใหม่", [
  ("ของแขวนต้นคริสต์มาสหมี", 1, 0, 3, "ริบบิ้น", "flat", 79, "—", "ราคาจับง่าย ซื้อหลายตัว", True),
  ("ปฏิทินนับถอยหลัง 4 สาย × 6 ตัว", 24, 20, 60, "ราวแขวนและริบบิ้น", "kit", 1190, "โชว์", "ผูกของขวัญที่ร่องแก้มที่ว่าง ใช้ได้ทุกปี", False),
  ("ป้ายห้อยของขวัญหมี", 1, 0, 2, "เชือกปอ", "flat", 49, "—", "เขียนชื่อผู้รับ ใช้ต่อเป็นพวงกุญแจได้", False),
  ("ที่ห้อยกระจกรถหมี", 1, 0, 6, "เชือกถัก", "flat", 149, "—", "ปั๊มชื่อหรือคำมงคล ขายช่วงปีใหม่และตรุษจีน", False),
 ]),
 ("งานแต่งและองค์กร (สั่งจำนวน)", "ของชำร่วยที่ใช้ได้จริงกำลังนิยม และองค์กรมองหาของขวัญยั่งยืนที่ดูเหมือนของขายในร้าน", [
  ("ของชำร่วย หมีคู่ปั๊มชื่อบ่าวสาว (100 ชิ้นขึ้นไป)", 2, 1, 6, "ห่วงโลหะ", "flat", 89, "โชว์", "หมีสองตัวกอดกันแทนคู่บ่าวสาว ใช้ห้อยกุญแจได้จริง", True),
  ("ของชำร่วย ที่รองแก้วปั๊มวันที่ (100 ชิ้นขึ้นไป)", 1, 0, 0, "", "flat", 45, "—", "ต้นทุนต่ำ ปั๊มชื่อกับวันที่งาน", False),
  ("ของขวัญองค์กร ชุดเก็บสาย + ที่รองแก้ว (50 ชุดขึ้นไป)", 3, 0, 5, "ปั๊มโลโก้", "wrap", 169, "—", "เล่าเรื่องเศษหนังที่ไม่ถูกทิ้ง ตรงกับนโยบายความยั่งยืน", False),
  ("ของขวัญองค์กร ปลอกแก้วปั๊มโลโก้ (50 ชิ้นขึ้นไป)", 5, 5, 5, "ปั๊มโลโก้", "flat", 219, "ซ่อน", "ใช้ทุกวัน โลโก้ลูกค้าอยู่บนโต๊ะ", False),
  ("ชุดต่อเองหมี 10 ตัว + การ์ดวิธีต่อ", 10, 0, 0, "", "kit", 390, "เลือกได้", "เวิร์กช็อปองค์กรหรือบูธ ต่อเองในห้านาที", False),
 ]),
]

def cost(b, j, ex, pk):
    return b * PC + j * JC + LAB + PACK[pk] + ex

# ---------------------------------------------------------------- the presentation drawings (real die outline)
def bear(x, y, fill, clip=None, dash=False):
    cp = f' clip-path="url(#{clip})"' if clip else ""
    cls = "lea dash" if dash else "lea"
    sl = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" class="sl"/>' for a, b, c, d in SL)
    return f'<g transform="translate({x},{y})"{cp}><path d="{BEAR_D}" fill="{fill}" class="{cls}"/>{sl}</g>'

def clips(uid):
    return (f'<clipPath id="{uid}f"><rect x="-5" y="-5" width="{NECK_X + 5}" height="120"/></clipPath>'
            f'<clipPath id="{uid}e"><rect x="{NECK_X}" y="-5" width="40" height="120"/></clipPath>')

def look_hidden():
    return (f'<svg viewBox="-4 -4 186 116" role="img" aria-label="ต่อแบบซ่อนปลาย"><defs>{clips("h")}</defs>'
            + bear(PITCH, 0, "var(--l2)") + bear(0, 0, "var(--l1)", clip="hf") + "</svg>")

def look_shown():
    return (f'<svg viewBox="-4 -4 186 116" role="img" aria-label="ต่อแบบโชว์ปลาย"><defs>{clips("s")}</defs>'
            + bear(0, 0, "var(--l1)", clip="sf") + bear(PITCH, 0, "var(--l2)")
            + f'<g transform="translate(0,0)" clip-path="url(#se)"><path d="{BEAR_D}" fill="var(--l1)" class="lea"/></g></svg>')

def edge_tucked():
    # ears folded behind: show the face only, ears as dashed outlines behind
    cl = (f'<clipPath id="tf"><path d="M0,0 H{NECK_X} V{TOP_NECK_Y} H0 Z M0,{TOP_NECK_Y} H{NECK_X} V110 H0 Z"/></clipPath>'
          f'<clipPath id="tb"><rect x="-5" y="{TOP_NECK_Y}" width="{NECK_X + 5}" height="100"/></clipPath>')
    return (f'<svg viewBox="-4 -4 116 116" role="img" aria-label="หูริมพับเก็บหลัง"><defs>{cl}</defs>'
            + bear(0, 0, "none", dash=True) + bear(0, 0, "var(--l3)", clip="tb") + "</svg>")

def edge_shown():
    return f'<svg viewBox="-4 -4 116 116" role="img" aria-label="หูริมโชว์">{bear(0, 0, "var(--l3)")}</svg>'

def page():
    rows, n, all_rows = [], 0, []
    for gname, gwhy, items in G:
        body = []
        for name, b, j, ex, exn, pk, price, look, why, star in items:
            n += 1
            c = cost(b, j, ex, pk); m = (price - c) / price
            all_rows.append((n, name, b, price, m, look, star, gname))
            lk = {"ซ่อน": "hid", "โชว์": "show", "เลือกได้": "both"}.get(look, "none")
            body.append(f'<tr><td class="n">{n}</td><td><b>{E(name)}</b>{" <span class=star>แนะนำ</span>" if star else ""}'
                        f'<span class="why">{E(why)}</span></td><td class="n">{b}</td>'
                        f'<td><span class="lk {lk}">{E(look)}</span></td><td class="n">{price:,}</td><td class="n">{c:,.0f}</td><td class="n">{m:.0%}</td></tr>')
        rows.append(f'<section class="grp"><h3>{E(gname)}</h3><p class="gwhy">{E(gwhy)}</p>'
                    f'<div class="tbl"><table><thead><tr><th>#</th><th>สินค้า</th><th>หมี</th><th>หน้าตา</th><th>ราคา</th><th>ต้นทุน</th><th>เหลือ</th></tr></thead>'
                    f'<tbody>{"".join(body)}</tbody></table></div></section>')
    stars = [r for r in all_rows if r[6]]
    top = "".join(f'<li><b>{E(r[1])}</b> <span class="muted">· {r[3]:,} บาท · {r[2]} ตัว · เหลือ {r[4]:.0%}</span></li>' for r in stars)
    total_bears = sum(r[2] for r in all_rows)
    star_bears = sum(r[2] for r in stars)
    return f"""<title>Bear 01 Product Range</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mitr:wght@500&family=IBM+Plex+Sans+Thai:wght@400;600&family=Jost:wght@500&display=swap">
<style>
/* layout: thesis + the two ways to join, then the shortlist, then the full 50 in seven market groups */
:root{{
  --paper:#FFF6EC; --ink:#1C1B22; --muted:#5E5A66; --line:#E8DCCB; --cobalt:#2449D8; --tomato:#FF5A36; --pink:#C2367A; --card:#FFFFFF;
  --l1:#B8743A; --l2:#9A5E2C; --l3:#CF9157; --hid:#E6ECFF; --show:#FFE3EE; --both:#FFF0C8;
  --display:'Mitr','IBM Plex Sans Thai',sans-serif; --body:'IBM Plex Sans Thai',sans-serif; --latin:'Jost','IBM Plex Sans Thai',sans-serif;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--paper:#17161C;--ink:#F4EDE3;--muted:#B3ACA3;--line:#34313B;--cobalt:#8FA6FF;--tomato:#FF7A5C;--pink:#FF8AC4;--card:#211F27;--hid:#26304F;--show:#4A2436;--both:#43391F;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#17161C;--ink:#F4EDE3;--muted:#B3ACA3;--line:#34313B;--cobalt:#8FA6FF;--tomato:#FF7A5C;--pink:#FF8AC4;--card:#211F27;--hid:#26304F;--show:#4A2436;--both:#43391F;color-scheme:dark}}
body{{background:var(--paper);color:var(--ink);font:400 16px/1.7 var(--body)}}
.wrap{{max-width:1040px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:34px 89px;display:flex;flex-direction:column;gap:44px}}
h1,h2,h3{{font-family:var(--display);font-weight:500;line-height:1.25;text-wrap:balance;margin:0}}
h1{{font-size:clamp(28px,6vw,41.9px)}} h2{{font-size:25.9px}} h3{{font-size:20.4px}}
p{{margin:0}}
.eyebrow{{font:500 12.6px/1 var(--latin);letter-spacing:.14em;text-transform:uppercase;color:var(--pink)}}
.lead{{font-size:18px;max-width:64ch}}
.muted{{color:var(--muted)}}
.col{{display:flex;flex-direction:column;gap:13px}}
.res{{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:8px;max-width:72ch}}
.looks{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:21px}}
.look{{display:flex;flex-direction:column;gap:8px;min-width:0}}
.look .pic{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:13px;max-width:100%}}
.look svg{{display:block;width:100%;height:auto;max-height:150px}}
.look b{{font-family:var(--display);font-weight:500;font-size:17px}}
.look p{{font-size:15px}}
.lea{{stroke:var(--ink);stroke-width:.6;stroke-linejoin:round}} .lea.dash{{fill:none;stroke-dasharray:2 1.6;opacity:.6}}
.sl{{stroke:var(--ink);stroke-width:.9}}
.top{{margin:0;padding-left:1.3em;columns:2 260px;column-gap:34px}}
.top li{{break-inside:avoid;margin-bottom:6px}}
.grp{{display:flex;flex-direction:column;gap:8px}}
.gwhy{{font-size:15px;color:var(--muted);max-width:72ch}}
.tbl{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-size:15px;min-width:620px}}
th,td{{text-align:left;padding:8px 10px 8px 0;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font:500 12.6px var(--latin);letter-spacing:.08em;color:var(--muted)}}
td.n{{font-variant-numeric:tabular-nums;white-space:nowrap;text-align:right}}
th:nth-child(n+5){{text-align:right}} th:nth-child(3){{text-align:right}}
.why{{display:block;font-size:13.5px;color:var(--muted);line-height:1.5}}
.star{{font:600 11px var(--body);color:#fff;background:var(--pink);border-radius:4px;padding:1px 6px;margin-left:4px;white-space:nowrap}}
.lk{{font-size:13px;padding:2px 8px;border-radius:999px;white-space:nowrap}}
.lk.hid{{background:var(--hid)}} .lk.show{{background:var(--show)}} .lk.both{{background:var(--both)}} .lk.none{{color:var(--muted)}}
.note{{font-size:14px;color:var(--muted);max-width:72ch}}
a{{color:var(--cobalt)}}
.src{{font-size:13.5px;margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:3px}}
</style>
<div class="wrap">
<section class="col">
  <span class="eyebrow">ห้าหมี FIVE BEARS · แม่พิมพ์ 01 · 16 ต.ค. 2569</span>
  <h1>50 สินค้าจากหัวหมีชิ้นเดียว</h1>
  <p class="lead">หูขวาของหมีเสียบร่องแก้มซ้ายของตัวข้าง ๆ หูบนเสียบร่องคางของตัวบน ห่างกัน 71.4 มม. เท่ากันทั้งสองแนว หมีจึงต่อเป็นสาย ตาราง วง และกล่องเปิดได้ และทุกรอยต่อเลือกได้ว่าจะซ่อนปลายหรือโชว์ปลาย</p>
</section>

<section class="col">
  <h2>วิธีนำเสนอ 4 แบบจากรอยต่อเดียว</h2>
  <div class="looks">
    <div class="look"><div class="pic">{look_hidden()}</div><b>ซ่อนปลาย · แบบเรียบ</b><p>สอดหูจากหน้าไปหลัง หูหายไปหลังตัวถัดไป หน้าเรียบ ขอบหน้าตัวแรกทับตัวถัดไป ดูหรู เหมาะของใช้บนโต๊ะและงานองค์กร</p></div>
    <div class="look"><div class="pic">{look_shown()}</div><b>โชว์ปลาย · หมีโผล่</b><p>สอดหูจากหลังมาหน้า หูไปโผล่บนแก้มตัวถัดไปเหมือนกอดกัน ดูสนุก เหมาะของเด็กและของขวัญ ใช้หนังสีตัดกันให้หูเด่นขึ้น</p></div>
    <div class="look"><div class="pic">{edge_tucked()}</div><b>หูริมพับเก็บ</b><p>หูที่ไม่ได้ต่อตรงขอบชิ้น พับไปหลังตัวเอง ขอบชิ้นงานจะกลมเรียบ เหมาะแผ่นรองและกรอบรูป</p></div>
    <div class="look"><div class="pic">{edge_shown()}</div><b>หูริมโชว์</b><p>ปล่อยหูริมชี้ออก เป็นขอบหยักรอบชิ้น หรือเป็นยอดมงกุฎ ร่องที่ว่างตรงขอบใช้ร้อยเชือก ริบบิ้น หรือห้อยป้ายได้</p></div>
  </div>
  <p class="note">เลือกเพิ่มได้อีกสองอย่าง คือหันหน้าหนังหรือหลังหนัง (ผิวเรียบหรือผิวสัก) ออกด้านนอก และสลับซ่อนกับโชว์ทีละแถว จะได้ลายคล้ายงานถัก สินค้าเดียวจึงขายได้สองแบบโดยไม่ต้องทำบล็อกใหม่</p>
</section>

<section class="col">
  <h2>สิ่งที่ตลาดบอก</h2>
  <ul class="res">
    <li><b>ที่ห้อยกระเป๋ายังมาแรง</b> กระแสเริ่มจากไทยในปี 2025 และปี 2026 ขยับไปทางของปั๊มชื่อและของมีความหมาย</li>
    <li><b>ราคาพวงกุญแจหนังแท้ในไทยอยู่ราว 59–119 บาท</b> ส่วนงานสั่งจำนวน 500 ชิ้นขึ้นไปอยู่ที่ 51–100 บาท ราคาเปิดของเราจึงตั้งที่ 99–129 บาท</li>
    <li><b>ของขวัญปีนี้เน้นใช้ได้จริงและมีคุณค่าทางใจ</b> งบจับฉลากปีใหม่ที่คนพูดถึงคือ 300–500 บาท</li>
    <li><b>ของแต่งบ้านงานมือ งานผ้า และงานแขวนผนังเป็นเทรนด์ปี 2026</b> คนซื้อเพราะเรื่องราวของชิ้นงาน</li>
    <li><b>องค์กรมองหาของขวัญที่ยั่งยืนและดูเหมือนของขายในร้าน</b> เรื่องเศษหนังที่ไม่ถูกทิ้งตอบโจทย์นี้</li>
    <li><b>ระวัง:</b> บน Etsy คำว่า "leather gift" มีคู่แข่งราว 950,000 รายการ และคนค้นลดลง 33% ในหนึ่งปี ของเราจึงต้องขายจุดต่างคือ ต่อเองได้ ไม่ใช้กาว และหมีห้าตัวของครอบครัว ไม่ใช่ขายแค่ว่าเป็นหนังแท้</li>
  </ul>
  <p class="note">ไม่พบข้อมูลยอดขายจริงรายสินค้าของ Shopee ไทยปี 2026 ตัวเลขข้างบนมาจากบทความและร้านค้าที่ค้นเจอ เป็นทิศทางตลาด ไม่ใช่ยอดขาย</p>
</section>

<section class="col">
  <h2>{len(stars)} ตัวที่แนะนำให้เริ่ม</h2>
  <p class="note">เลือกจากราคาที่ตลาดรับได้ เรื่องเล่าของแบรนด์ และขายต่อได้ช่วงคริสต์มาสถึงปีใหม่หลังบูธ ทั้งหมดใช้หมีรวม {star_bears} ตัวถ้าทำอย่างละชิ้น</p>
  <ul class="top">{top}</ul>
</section>

<section class="col">
  <h2>ทั้ง 50 แบบ</h2>
  <p class="note">ต้นทุนคิดจาก brand.py ค่าชิ้นหมี {PC:.2f} บาท ค่าต่อ {JC:.2f} บาทต่อรอยต่อ บรรจุภัณฑ์ บวกของเสริมที่ประมาณเอง ราคาเป็นราคาที่ผมเสนอ ยังไม่ได้ยืนยัน ทำทั้ง 50 แบบอย่างละชิ้นใช้หมี {total_bears} ตัว</p>
  {"".join(rows)}
</section>

<section class="col">
  <h2>ก่อนตัดสินใจ</h2>
  <ul class="res">
    <li>ต่อหมีจริง 2 × 2 ตัว ดูว่าหูกับร่องตรงกันทั้งสองแนว แล้วลองทั้งแบบซ่อนและโชว์ปลาย</li>
    <li>ของที่แขวนหรือถูกดึงใช้หนังหนา 2 มม. ขึ้นไป ตามกฎที่ตกลงกัน</li>
    <li>เศษหนังชิ้นใหญ่เหลือราว 245 ชิ้นหลังเตรียมของบูธ ต้องเลือกตัวที่จะทำก่อน</li>
    <li>ชื่อกลุ่มสินค้าแต่งบ้านยังรอคุยกัน</li>
  </ul>
  <span class="eyebrow" style="color:var(--muted)">แหล่งข้อมูล</span>
  <ul class="src">
    <li><a href="https://fashionmagazine.com/style/bag-charm-trend/">Fashion Magazine: bag charm trend</a> · <a href="https://www.accio.com/business/bag-charms-trend-2026">Accio: bag charms trend 2026</a> · <a href="https://sourcy.ai/product-catalogs/keychain/collectible-critter-charms">Sourcy: collectible critter charms</a></li>
    <li><a href="https://embed.wionews.com/web-stories/luxury-and-lifestyle/what-is-labubu-and-why-its-2025s-hottest-bag-charm-trend-9001294">WION: Labubu 2025 bag charm trend</a> · <a href="https://usa.10magazine.com/who-is-labubu/">10 Magazine: Who is Labubu</a></li>
    <li><a href="https://sabuykapao.com/keychain/">Sabuykapao: พวงกุญแจหนังแท้</a> · <a href="https://dudeepremium.com/product/leather-keychain-5/">Dudee Premium: พวงกุญแจหนัง (สั่งจำนวน)</a> · <a href="https://www.iduckyofficial-pricelists.com/">iDucky: ราคาพวงกุญแจปักลาย</a></li>
    <li><a href="https://www.rankhero.com/keywords/leather-gift">RankHero: keyword "leather gift" มี.ค. 2026</a> · <a href="https://www.outfy.com/blog/?p=19797">Outfy: Etsy trends 2026</a></li>
    <li><a href="https://www.ktc.co.th/article/shopping/budgeted-new-year-gift-ideas">KTC: ของขวัญ 500 บาท</a> · <a href="https://thestandard.co/?p=55547">The Standard: ไอเดียของขวัญ</a> · <a href="https://shopee.co.th/blog/idea-useful-wedding-favors">Shopee: ของชำร่วยใช้ได้จริง</a></li>
    <li><a href="https://www.artfinder.com/blog/post/interior-trends-2026/">Artfinder: interior trends 2026</a> · <a href="https://es.espiritu.com/blogs/style-trends/interior-design-trends-set-to-define-2026">Espiritu: design trends 2026</a> · <a href="https://usadrop.com/?p=25545">USAdrop: home decor products 2026</a></li>
    <li><a href="https://www.imarcgroup.com/thailand-toys-market">IMARC: Thailand toys market</a> · <a href="https://seller.alibaba.com/blogs/2026/southeast-asia/promotional-business-gifts/export-strategy-white-paper">Alibaba: SEA business gifts 2026</a> · <a href="https://thailand.go.th/event-detail/sustainable-luxury-is-here-">Thailand.go.th: Sustainable Craft</a></li>
    <li><a href="https://www.bigseller.pro/blog/articleDetails/4222/how-to-select-in-demand-products-for-shopee-southeast-asia-2026.htm">BigSeller: Shopee SEA 2026</a> · <a href="https://julesjenn.com/en/collections/produits-upcycles">Jules &amp; Jenn: upcycled leather</a></li>
  </ul>
</section>
</div>
"""

if __name__ == "__main__":
    n = sum(len(g[2]) for g in G)
    assert n == 50, n
    over = [it[1] for g in G for it in g[2] if it[6] > 1500]
    assert not over, over
    open(os.path.join(OUT, "index.html"), "w").write(page())
    print("products", n)
