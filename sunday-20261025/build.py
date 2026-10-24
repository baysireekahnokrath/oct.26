"""Sunday 25 Oct, last booth day: ten objectives with activities, scored on revenue, future value, cash cost and
opportunity cost (owner, 24 Oct).

Facts from the status doc (24 Oct): booth price 30 THB a piece, no quantity discount; piece cost 3.45–4.22 THB (leather +
cut, already paid); stock 01 369, 02–05 150 each (07 not sold at the booth); 8,313 THB spent so far, booth fee, print
and packaging not included; LINE game gives one piece per person; 26 Oct is mum's birthday and the brand's.
The booth POS has no sales recorded, so Friday and Saturday sales are unknown: numbers here are per piece, not totals.
python3 sunday-20261025/build.py -> site/index.html, plan.txt
"""
import html, importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sp = importlib.util.spec_from_file_location("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
E = html.escape

PRICE, COST = 30, 4                 # THB; piece cost rounded up from 3.45–4.22
MARGIN = PRICE - COST
SPENT = 8313
STOCK = {"01": 369, "02": 150, "03": 150, "04": 150, "05": 150}
WEIGHTS = [("รายได้วันนี้", 25), ("มูลค่าหลังงาน", 25), ("ต้นทุนเงิน", 15), ("ค่าเสียโอกาส", 20), ("ทำได้จริงพรุ่งนี้", 15)]
# for cost and opportunity cost, 5 = cheap / low

OBJ = [  # (objective, activity, cash cost, people and time, money effect, measure, scores, note)
    ("รู้ตัวเลขจริงของงานนี้",
     "จดทุกบิลในแอปขายของ (ตอนนี้ยังไม่มีบันทึกสักบิล) · นับสต็อกตอนเปิดและปิดบูธ · ยอดศุกร์เสาร์จดย้อนหลังเท่าที่จำได้",
     "0 บาท", "คนเก็บเงิน 10 วินาทีต่อบิล + นับของ 15 นาที",
     "ไม่ได้เพิ่มยอดวันนี้ แต่ใช้ตัดสินว่าบูธหน้าคุ้มไหม ลายไหนขายดี ควรตัดเพิ่มลายไหน",
     "บันทึกครบทุกบิล · สต็อกปิดบูธ", (1, 5, 5, 5, 5), ""),
    ("ขายเพิ่มต่อคน",
     "จัดโต๊ะตามการใช้ (ที่รองแก้ว · สายชาร์จ · ป้ายของขวัญ) แทนการจัดตามลาย · เปิดหน้า \"01 ที่รองแก้ว × 4\" ในแฟ้มให้เห็น · ชวนด้วยประโยคเดียว \"ใช้เป็นที่รองแก้วทั้งบ้าน หลายคนเลือกคนละสี\"",
     "0 บาท", "ไม่ต้องเพิ่มคน",
     f"ทุกแผ่นที่เพิ่มในบิล = +{PRICE} บาท (กำไรราว {MARGIN} บาท) · ไม่ลดราคาตามจำนวนตามที่ตั้งไว้",
     "แผ่นต่อบิล", (5, 3, 5, 4, 5), ""),
    ("ระบายลาย 01 ที่มีมากที่สุด",
     f"วาง 01 ไว้หน้าสุดของโต๊ะ · ใช้ 01 เป็นชิ้นที่แจกในเกม · ตัวอย่างชุดใช้ 01 (มี {STOCK['01']} แผ่น ลายอื่นลายละ 150)",
     "0 บาท", "ไม่ต้องเพิ่มคน",
     "ไม่เพิ่มยอดรวมมาก แต่ทำให้สต็อกสมดุล ลายอื่นเหลือไว้ขายออนไลน์",
     "01 ขายได้กี่แผ่นเทียบลายอื่น", (4, 2, 5, 5, 5), ""),
    ("เพิ่มเพื่อน LINE OA",
     "เกมที่เตรียมไว้แล้ว: แอด LINE โชว์ข้อความทักทาย เล่นเกมจับคู่จบ ได้ชิ้นหนัง 1 ชิ้น คนละ 1 ชิ้น",
     f"ราว {COST} บาทต่อชิ้นที่แจก (จ่ายไปแล้วตอนตัด)", "ผู้ใหญ่ 1 คนดูเกมช่วงคนเยอะ",
     "ค่าเสียโอกาสจริงคือคนที่จะซื้ออยู่แล้วแต่ได้ฟรีแทน (เสียราว 26 บาท) · ลดได้ด้วยการแจก 01 และให้เล่นหลังจ่ายเงิน หรือแจกชิ้นที่มีรอย",
     "เพื่อน LINE เพิ่มกี่คน (ดูใน LINE OA ตอนเปิดและปิดบูธ)", (2, 5, 4, 3, 5), "ตั้งข้อความทักทายตามไฟล์ booth-game ก่อนเปิดบูธ"),
    ("ปูทางวันเกิดแบรนด์ 26 ต.ค. (จันทร์)",
     "บอกลูกค้าทุกคนสั้น ๆ \"พรุ่งนี้วันเกิดแม่ และวันเกิด OCT. 26\" ชวนแอด LINE ไว้ · คืนอาทิตย์หรือเช้าจันทร์ส่งข้อความแนะนำแบรนด์ (แบบที่ 2) และโพสต์ IG FB",
     "0 บาท", "พูดตอนเก็บเงิน ไม่เพิ่มคน",
     "รายได้มาหลังงานผ่านเว็บและ LINE · ไม่จัดลดราคาวันเกิด (เล่มแบรนด์: ไม่ลดราคาแรง)",
     "คนเปิดอ่านบรอดแคสต์ · ข้อความเข้า LINE วันจันทร์", (1, 4, 5, 5, 4), ""),
    ("ฟังลูกค้า: ซื้อไปทำอะไร",
     "ถามคนจ่ายเงินคำถามเดียว \"เอาไปใช้ทำอะไร\" แล้วขีดในกระดาษ 4 ช่อง (ที่รองแก้ว · สายชาร์จ · ของขวัญ · อื่น ๆ) · จดคำถามที่ถูกถามซ้ำ",
     "0 บาท", "ถามตอนทอนเงิน",
     "ไม่เพิ่มยอดวันนี้ · ส่งให้ฝ่ายพัฒนาสินค้าใช้ทดสอบสินค้าชั้น 2 วันที่ 26–29 ต.ค. แทนการเดา",
     "จำนวนคำตอบ (เป้า 30 คน)", (1, 5, 5, 4, 5), ""),
    ("ให้คนหยุดที่บูธนานขึ้น (DIY แต่งชิ้น)",
     "มุมเล็กเขียนชื่อหรือวาดลายบนชิ้นที่ซื้อ ฟรีกับคนที่ซื้อ · ชิ้นเดียว ไม่ต่อชิ้น",
     "ปากกาเขียนหนังราว 100–200 บาท ถ้ายังไม่มี", "ผู้ใหญ่ 1 คน + พื้นที่โต๊ะ คิวอาจช้าลงตอนคนเยอะ",
     f"คุ้มเมื่อขายเพิ่มได้ 4–8 แผ่นจากคนที่หยุดเพราะมุมนี้ (200 ÷ {MARGIN}) · ได้ของขวัญที่มีชื่อ คนซื้อเพิ่มให้คนอื่น",
     "คนที่แต่งชิ้น · แผ่นต่อบิลของคนกลุ่มนี้", (3, 3, 3, 2, 4), "ปิดมุมนี้ช่วงคิวยาว"),
    ("เก็บคอนเทนต์จริงไว้ลงสัปดาห์หน้า",
     "มือถือ 1 เครื่อง ถ่ายมือหยิบชิ้นหนัง การเขียนชื่อ โต๊ะทั้งบูธ วิดีโอสั้น 15 วินาที 5 คลิป · ขออนุญาตก่อนถ่ายลูกค้า ไม่ถ่ายหน้าเด็ก",
     "0 บาท", "ถ่ายช่วงคนน้อย",
     "ไม่เพิ่มยอดวันนี้ · ได้รูปจริงแทนรูป AI ลง IG FB YouTube ได้ทั้งสัปดาห์",
     "รูปและคลิปที่ใช้ได้", (1, 4, 5, 4, 4), ""),
    ("วัดความสนใจสินค้าต่อชิ้นก่อนลงทุน",
     "วางตัวอย่าง 07 ปลอกขวดน้ำและที่ห้อยกระเป๋าเขียนว่า \"กำลังทดสอบ ยังไม่ขาย\" · ใครสนใจให้แอด LINE แล้วพิมพ์ 07 · ห้ามบอกว่าต่อเองได้หรือไม่ต้องเย็บ",
     "0 บาท", "ต้องอธิบายลูกค้าเพิ่ม",
     "ไม่มีรายได้วันนี้ · ได้รายชื่อคนรอซื้อ ช่วยตัดสินว่าจะทดสอบ 5 ข้อและผลิตไหม",
     "คนพิมพ์ 07 ใน LINE", (1, 4, 5, 4, 3), "ขัดกฎ \"ไม่โฆษณาการต่อชิ้น\" ได้ถ้าพูดเกิน · ปลอกขวดต้องไม่ถึงปากขวด"),
    ("หาลูกค้าองค์กรและของชำร่วย",
     "ป้าย A5 \"รับทำของที่ระลึก ของชำร่วย จำนวนมาก คุยทาง LINE\" · จดชื่อและจำนวนที่คนถาม",
     "ราว 5 บาท (พิมพ์ป้าย)", "คุยกับคนที่ถาม",
     f"งานเดียวอาจได้ 100 แผ่น = {100 * PRICE:,} บาท แต่ไม่แน่นอน · ยังไม่มีราคาส่ง ต้องให้พ่อเบตั้งก่อนตอบ",
     "จำนวนรายชื่อที่ได้", (1, 4, 5, 4, 3), "ราคาส่งยังไม่ได้ตั้ง"),
]


def score(s):
    return round(sum(v * w for v, (_, w) in zip(s, WEIGHTS)) / 5)


RANK = sorted(range(len(OBJ)), key=lambda i: -score(OBJ[i][6]))
TOP = RANK[:5]
for o in OBJ:
    for word in ("ไม่ต้องเย็บ\"", "ส่วนลด", "หัวใจ"):
        assert word not in o[1], word


def page():
    w = " · ".join(f"{n} {p}%" for n, p in WEIGHTS)
    rows = "".join(
        f'<tr><td class="mono">{k}</td><td><b>{E(OBJ[i][0])}</b></td><td class="mono">{score(OBJ[i][6])}</td>'
        + "".join(f'<td class="mono">{v}</td>' for v in OBJ[i][6]) + "</tr>"
        for k, i in enumerate(RANK, 1))
    bars = "".join(
        f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 44px;gap:8px;align-items:center">'
        f'<div><div style="font-size:14px;margin-bottom:4px">{k}. {E(OBJ[i][0])}</div>'
        f'<div style="height:10px;border-radius:5px;background:var(--line)"><div style="height:100%;width:{score(OBJ[i][6])}%;border-radius:5px;background:{"#2A2725" if i in TOP else "#B07A4A"}"></div></div></div>'
        f'<b class="mono" style="text-align:right">{score(OBJ[i][6])}</b></div>'
        for k, i in enumerate(RANK, 1))
    cards = "".join(
        f'<article class="card" style="display:flex;flex-direction:column;gap:8px">'
        f'<div style="display:flex;justify-content:space-between;gap:12px;align-items:baseline"><h3>{k}. {E(o[0])}</h3><b class="mono" style="font-size:20px">{score(o[6])}</b></div>'
        f'<p><b>ทำอะไร</b> {E(o[1])}</p><p><b>ต้นทุนเงิน</b> {E(o[2])} · <b>คนและเวลา</b> {E(o[3])}</p>'
        f'<p><b>เงินและโอกาส</b> {E(o[4])}</p><p class="cap"><b>วัดผล</b> {E(o[5])}'
        + (f' · <b>ระวัง</b> {E(o[7])}' if o[7] else "") + "</p></article>"
        for k, o in ((k, OBJ[i]) for k, i in enumerate(RANK, 1)))
    top = "".join(f"<li>{E(OBJ[i][0])}</li>" for i in TOP)
    return f"""{S.head("OCT. 26 แผนวันอาทิตย์")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · บูธวันสุดท้าย อา. 25 ต.ค.</span><h1>พรุ่งนี้ทำอะไร เพื่ออะไร</h1>
<p class="lead">10 เป้าหมายพร้อมกิจกรรม ให้คะแนนเต็ม 100 จากรายได้วันนี้ มูลค่าหลังงาน ต้นทุนเงิน และค่าเสียโอกาส
ข้อเสนอคือทำ 5 อันดับแรกพร้อมกัน เพราะไม่ต้องใช้เงินเพิ่มและไม่ต้องเพิ่มคน</p></header>
<section><h2>ตัวเลขที่ใช้คิด</h2><div class="grid">
<div class="card"><span class="cap">ราคาบูธต่อแผ่น</span><div style="font-size:28px" class="mono">{PRICE} บาท</div><span class="cap">ต้นทุนชิ้นหนัง 3.45–4.22 บาท · กำไรราว {MARGIN} บาท</span></div>
<div class="card"><span class="cap">ลงทุนไปแล้ว</span><div style="font-size:28px" class="mono">{SPENT:,} บาท</div><span class="cap">ต้องขายราว {-(-SPENT // PRICE)} แผ่นที่ {PRICE} บาทจึงคืนทุน ยังไม่รวมค่าบูธ งานพิมพ์ ถุง</span></div>
<div class="card"><span class="cap">ชิ้นหนัง 01–05 ก่อนเปิดบูธ</span><div style="font-size:28px" class="mono">{sum(STOCK.values())} แผ่น</div><span class="cap">01 มี {STOCK['01']} · ลายอื่นลายละ 150 · 07 มี 200 ยังไม่ขายที่บูธ</span></div>
</div>
<div class="card" style="margin-top:12px"><b>ค่าเสียโอกาสของชิ้นหนัง</b><p>ชิ้นหนังจ่ายเงินตัดไปแล้ว การแจก 1 ชิ้นวันนี้จึงไม่ได้เสียเงินเพิ่ม
ที่เสียจริงคือโอกาสขายแผ่นนั้น ของยังเหลือหลายร้อยแผ่น โอกาสนี้จึงต่ำ ยกเว้นคนที่ตั้งใจจะซื้ออยู่แล้วแต่ได้ฟรีแทน
ส่วนที่เสียมากที่สุดของพรุ่งนี้คือ<b>เวลาของคนในบูธ</b> ทุกกิจกรรมที่ดึงผู้ใหญ่ออกจากโต๊ะขาย ต้องได้คืนมากกว่าแผ่นที่ขายไม่ทัน</p></div>
<p class="cap">แอปขายของยังไม่มีบันทึกการขายสักบิล จึงยังไม่รู้ยอดศุกร์กับเสาร์ ตัวเลขในหน้านี้เลยคิดเป็นต่อแผ่น ถ้าพ่อเบบอกยอดสองวันแรกได้ จะคิดเป้าวันอาทิตย์เป็นบาทให้</p></section>
<section><h2>อันดับคะแนน</h2><div class="card" style="display:flex;flex-direction:column;gap:12px">{bars}</div>
<p class="cap">น้ำหนัก: {E(w)} · ต้นทุนและค่าเสียโอกาส 5 = ถูก / เสียน้อย · สีเข้ม = 5 อันดับที่แนะนำ</p></section>
<section><h2>ทำพรุ่งนี้: 5 อันดับแรก</h2><div class="card"><ol>{top}</ol>
<p class="cap" style="margin-top:8px">ห้าข้อนี้ใช้เงินรวมไม่เกินค่าชิ้นหนังที่แจก และใช้คนเท่าเดิม ข้ออื่นทำเมื่อมีคนว่าง (คอนเทนต์ ช่วงคนน้อย) หรือรอพ่อเบตัดสิน (ราคาส่ง การโชว์ของต่อชิ้น)</p></div></section>
<section><h2>รายละเอียดทีละข้อ</h2><div style="display:flex;flex-direction:column;gap:12px">{cards}</div></section>
<section><h2>คะแนนย่อย</h2><div class="tbl"><table><thead><tr><th>#</th><th>เป้าหมาย</th><th>รวม</th>{"".join(f"<th>{E(n)}</th>" for n, _ in WEIGHTS)}</tr></thead><tbody>{rows}</tbody></table></div></section>
<section><h2>ไม่แนะนำ</h2><div class="card"><ul>
<li>ลดราคาท้ายงานหรือแถมตามจำนวน: ราคา 30 บาทต่ำอยู่แล้ว และขัดกับที่ตั้งไว้ว่าไม่ลดตามจำนวน</li>
<li>ขายหรือรับจองของต่อชิ้น: ข้อต่อยังไม่ผ่านการทดสอบ 5 ข้อ</li></ul></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">sunday-20261025/build.py</td><td>แก้คะแนน น้ำหนัก หรือกิจกรรมที่นี่แล้วรันใหม่</td></tr>
<tr><td class="mono" style="white-space:nowrap">sunday-20261025/plan.txt</td><td>สรุปแบบข้อความ</td></tr>
<tr><td>Google Doc "OCT. 26 แผนบูธวันอาทิตย์ 25 ต.ค."</td><td>ในโฟลเดอร์ OCT. 26 ไฟล์งาน</td></tr>
</tbody></table></div></section></div>"""


def text():
    out = ["OCT. 26 แผนบูธวันอาทิตย์ 25 ต.ค. (วันสุดท้าย)", "",
           f"ราคา {PRICE} บาท/แผ่น · ต้นทุนชิ้นหนัง 3.45–4.22 บาท (จ่ายแล้ว) · กำไรราว {MARGIN} บาท/แผ่น · ลงทุนแล้ว {SPENT:,} บาท = ขายราว {-(-SPENT // PRICE)} แผ่นจึงคืนทุน (ยังไม่รวมค่าบูธ)",
           "แอปขายของยังไม่มีบันทึกการขาย ยอดศุกร์เสาร์ยังไม่รู้", "",
           "น้ำหนักคะแนน: " + " · ".join(f"{n} {p}%" for n, p in WEIGHTS), ""]
    for k, i in enumerate(RANK, 1):
        o = OBJ[i]
        out += [f"{k}. {o[0]} · {score(o[6])}/100" + ("  [ทำพรุ่งนี้]" if i in TOP else ""),
                f"   ทำอะไร: {o[1]}", f"   ต้นทุน: {o[2]} · คน: {o[3]}", f"   เงินและโอกาส: {o[4]}", f"   วัดผล: {o[5]}"]
        if o[7]:
            out.append(f"   ระวัง: {o[7]}")
        out.append("")
    out += ["ไม่แนะนำ: ลดราคาท้ายงาน/แถมตามจำนวน · ขายหรือรับจองของต่อชิ้น",
            "หน้าสรุป: https://claude.ai/artifact/GUb7bmsk1xRUHPYNYFx5yC"]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(page())
    open(os.path.join(HERE, "plan.txt"), "w").write(text())
    for k, i in enumerate(RANK, 1):
        print(k, score(OBJ[i][6]), OBJ[i][0])
