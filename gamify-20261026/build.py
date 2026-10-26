"""Gamification ideas and a gamified revenue model (owner, 26 Oct: "วางขายแล้ว เหงามาก").

Facts from the status doc (26 Oct): online prices 39–59 a piece, 179 for the 4-pattern coaster set (Shopee and web), booth
30; piece cost 3.45–4.22 THB; patterns 01–05 on sale, 07 cut but not sold yet; the 01–07 collector set is approved;
LINE OA is the main channel; no Shopee shop link yet; no draws or random prizes, no forced posts or friend tags, no heavy
discounts (Brand Book v2), no data from children. Nothing here is a chance game: every reward is earned, not drawn.
python3 gamify-20261026/build.py -> site/index.html, plan.txt
"""
import html, importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sp = importlib.util.spec_from_file_location("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
E = html.escape

WEIGHTS = [("ยอดขาย 30 วัน", 25), ("ซื้อซ้ำและสะสม", 25), ("ต้นทุนเงิน", 15), ("ค่าเสียโอกาส", 15), ("เข้ากับแบรนด์และกฎ", 20)]
# cost and opportunity cost: 5 = cheap / little time

IDEAS = [  # (name, game mechanic, what it moves, how money comes in, cash, time, first step, scores, watch out)
    ("บัตรสะสมแพตเทิร์นใน LINE", "สะสมให้ครบ (collection)",
     "ซื้อซ้ำ",
     "ใช้บัตรสะสมแต้มที่มีใน LINE OA อยู่แล้ว ซื้อ 1 แพตเทิร์นได้ 1 แต้ม ครบ 5 ลาย (01–05) รับปั๊มชื่อฟรี 1 ชิ้น และได้ชื่อในหน้า \"นักสะสม\" บนเว็บ (ถ้าลูกค้ายินยอม) · ใช้ได้ทั้งออนไลน์และบูธ 30 ต.ค. (ลูกค้าสแกน QR แต้มที่โต๊ะ)",
     "0 บาท · ของรางวัลเป็นบริการ ไม่ใช่ส่วนลด", "ตั้ง 30 นาที", "ตั้งบัตรใน LINE OA วันนี้ ใช้ทันทีที่บูธ",
     (4, 5, 5, 4, 5), "เพิ่ม 07 เป็นช่องที่ 6 เมื่อเริ่มขาย 07 · ต้องมีตัวปั๊มก่อนให้รางวัล"),
    ("เติมให้ครบชุด", "เห็นช่องว่างแล้วอยากเติม (completion)",
     "ยอดต่อบิล",
     "หลังลูกค้าซื้อแผ่นเดียว ส่ง LINE รูปชุด 4 ลายที่มีช่องว่าง \"มี 01 แล้ว ขาดอีก 3 ลายก็ครบชุดที่รองแก้ว\" ใช้ราคาชุดเดิม 179 (แยกซื้อ 4 แผ่นราว 196) ไม่ได้ลดราคาเพิ่ม",
     "0 บาท", "ส่งข้อความทีละคน 1 นาที", "ทำรูปช่องว่าง 4 ลาย 1 รูป ใช้ซ้ำได้",
     (4, 3, 5, 5, 5), "ส่งครั้งเดียวต่อคน ไม่ตามซ้ำ"),
    ("ไลฟ์จองชิ้นเดียวในโลก", "ใครเร็วได้ก่อน (ไม่ใช่การสุ่ม)",
     "ซื้อครั้งแรก",
     "ไลฟ์ IG หรือ FB 20 นาที ยกชิ้นหนังทีละแผ่น บอกเลขชิ้นและขนาด คนดูพิมพ์ \"จอง + เลข\" คนแรกได้ไป จ่ายผ่าน LINE ทุกแผ่นสีไม่ซ้ำกันจึงเหมาะกับแบบนี้",
     "0 บาท", "ไลฟ์ 20 นาที + แพ็กของ", "ไลฟ์ครั้งแรกคืนวันพุธ 28 ต.ค. 20:00 ประกาศใน LINE ก่อน 1 วัน",
     (5, 3, 5, 3, 4), "ต้องมีวิธีจ่ายเงินและค่าส่งชัดก่อนไลฟ์ · ไม่ถ่ายหน้าเด็ก"),
    ("ปลดล็อกแพตเทิร์นใหม่ด้วยยอดจอง", "เป้าหมายร่วมกัน (progress bar)",
     "เงินก่อนผลิต",
     "ประกาศ \"ถ้าจองครบ 30 แผ่น เราจะตัดแพตเทิร์น 08\" มีแถบความคืบหน้าบนเว็บและใน LINE ครบเป้าค่อยสั่งบล็อกและตัด ไม่ครบคืนเงินทั้งหมด ตรงกับเล่มแบรนด์ \"ทำทีละรอบ\"",
     "บล็อกใหม่ราว 570 บาท จ่ายหลังครบเป้า", "ออกแบบลาย + ตั้งหน้าเว็บ 1–2 วัน", "PD เสนอ 08 มา 2–3 แบบ ให้คนใน LINE เลือก",
     (3, 4, 4, 3, 5), "ต้องตั้งราคาและวันส่งให้ชัด · คืนเงินถ้าไม่ครบ"),
    ("ระดับนักสะสม", "ขั้นและตรา (levels, badges)",
     "ซื้อซ้ำ",
     "ซื้อ 1 ลาย = มือใหม่ · 3 ลาย = ช่างเศษหนัง · 5 ลาย = นักสะสม ระดับสูงสุดได้เลือกสีหนังก่อนลงขาย 24 ชั่วโมง ใช้ป้ายกำกับเพื่อนใน LINE OA แยกกลุ่ม",
     "0 บาท", "ติดป้ายกำกับในแชตหลังขาย", "ใช้ร่วมกับบัตรสะสม ข้อ 1",
     (2, 5, 5, 3, 4), "ทำมือได้ตอนลูกค้ายังน้อย ถ้ามากต้องหาระบบ"),
    ("ภารกิจประจำสัปดาห์", "ท้าทายเป็นธีม (challenge)",
     "คนเห็นแบรนด์",
     "ทุกสัปดาห์หนึ่งธีม เช่น \"ชิ้นหนังบนโต๊ะทำงาน\" ชวนโพสต์ #OCT26ชิ้นของฉัน เราเลือกรูปมาลงเพจและเว็บพร้อมเครดิต ไม่มีของรางวัล ไม่สุ่ม",
     "0 บาท", "คัดรูปและลงเพจ 20 นาทีต่อสัปดาห์", "ธีมแรกใช้ฮาโลวีน 27–31 ต.ค. ที่ทำไว้แล้ว",
     (1, 4, 5, 4, 5), "ขออนุญาตก่อนลงรูป · ไม่ใช้รูปที่เห็นหน้าเด็ก"),
    ("บอกจำนวนที่เหลือตามจริง", "ของมีจำกัด (scarcity)",
     "ตัดสินใจซื้อเร็วขึ้น",
     "บนเว็บและ Shopee บอกว่าแต่ละลายเหลือกี่แผ่นในโทนสีนั้น ตัวเลขจริงจากชีตสต็อก ไม่สร้างความเร่งปลอม",
     "0 บาท", "อัปเดตสต็อกทุกครั้งที่ขาย", "ให้ทีมเว็บเพิ่มช่อง \"เหลือ\" ในหน้าจัดการสินค้า",
     (3, 2, 5, 3, 4), "ต้องอัปเดตจริง ถ้าตัวเลขผิดเสียความเชื่อใจ"),
    ("เกมบนเว็บต่อหลังบูธ", "เล่นจบรับบริการเพิ่ม (skill game)",
     "ซื้อครั้งแรก",
     "ใช้หน้า /game ต่อหลัง 1 พ.ย. เล่นจบได้คูปองใน LINE \"ปั๊มชื่อฟรีกับคำสั่งซื้อถัดไป\" เป็นเกมใช้ฝีมือ ไม่ใช่จับรางวัล",
     "ตัวปั๊มยังไม่มีราคา", "ทีมเว็บแก้หน้า /game ครึ่งวัน", "รอผลทดสอบตัวปั๊มในรอบชั้น 2",
     (2, 3, 3, 3, 4), "ต้องมีตัวปั๊มก่อน"),
    ("ชวนเพื่อน", "แนะนำแล้วได้ทั้งคู่ (referral)",
     "ลูกค้าใหม่",
     "เพื่อนที่มาจากการแนะนำซื้อครั้งแรก ทั้งสองคนได้ปั๊มชื่อฟรี 1 ชิ้น บอกชื่อคนแนะนำในแชต",
     "ค่าปั๊ม 2 ชิ้นต่อคู่", "จดชื่อคนแนะนำเอง", "รอหลังมีลูกค้าซื้อแล้วอย่างน้อย 20 คน",
     (2, 3, 4, 3, 2), "ใกล้กับกฎ \"ไม่ให้แท็กเพื่อน\" ทำแบบส่วนตัวในแชตเท่านั้น"),
    ("สมาชิกรายเดือน", "รอของใหม่ทุกเดือน (subscription)",
     "รายได้ประจำ",
     "เดือนละราคาเดียว ได้ 2 แผ่นสีที่เลือก + ไอเดียการใช้ 1 ใบ รู้ล่วงหน้าว่าได้อะไร ไม่ใช่กล่องสุ่ม",
     "ต้องมีลายใหม่ต่อเนื่อง", "แพ็กส่งทุกเดือน", "รอให้มีลายใหม่อย่างน้อย 3 ลายก่อน",
     (1, 5, 3, 2, 3), "ตอนนี้มีแค่ 5 ลาย คนจะเบื่อเร็ว"),
]
NOT_THESE = [
    "กล่องสุ่มหรือจับฉลากรางวัล: การจับรางวัลเพื่อขายของต้องขออนุญาตก่อน กล่องสุ่มถูกจับตาเรื่องคุ้มครองผู้บริโภค งานนี้มีเด็กเยอะ และขัดกฎ \"ไม่สุ่ม\" ที่ตั้งไว้",
    "Flash sale ลดแรงหรือแจกโค้ดลดราคาเยอะ: เล่มแบรนด์ไม่ลดราคาแรง และทำให้ราคาปกติดูแพง",
    "บังคับติดตามหรือแชร์เพื่อรับของ: ขัดกติกา Facebook และกฎที่เราตั้งไว้",
]
CHECK_FIRST = [
    ("ลิงก์ร้าน Shopee ยังไม่มี", "ถ้าคนหาร้านไม่เจอ เกมก็ช่วยไม่ได้ ใส่ลิงก์ในเว็บ ริชเมนู LINE และโปรไฟล์ IG FB ก่อนอย่างอื่น"),
    ("เพื่อน LINE จากบูธยังไม่ได้รับข่าว", "ส่งบรอดแคสต์แนะนำแบรนด์ (ทำไว้แล้ว) คืนนี้ วันเกิดแบรนด์ 26 ต.ค. เหมาะที่สุด"),
    ("ยังไม่รู้ตัวเลข", "ดูว่าสัปดาห์นี้มีคนเข้าเว็บกี่คน (Cloudflare) เปิดหน้าสินค้า Shopee กี่ครั้ง และทักแชตกี่คน จะได้รู้ว่าเงียบเพราะไม่มีคนเห็น หรือเห็นแล้วไม่ซื้อ"),
]
FUNNEL = [("เห็นแบรนด์", "ภารกิจประจำสัปดาห์ · ไลฟ์"), ("แอด LINE", "เกมที่บูธ · ไลฟ์"), ("ซื้อครั้งแรก", "ไลฟ์จองชิ้นเดียวในโลก"),
          ("ซื้อเพิ่มในบิล", "เติมให้ครบชุด"), ("ซื้อซ้ำ", "บัตรสะสม · ระดับนักสะสม"), ("จองรอบใหม่", "ปลดล็อกแพตเทิร์น 08")]


def score(s):
    return round(sum(v * w for v, (_, w) in zip(s, WEIGHTS)) / 5)


RANK = sorted(range(len(IDEAS)), key=lambda i: -score(IDEAS[i][7]))
TOP = RANK[:4]


def page():
    bars = "".join(
        f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 44px;gap:8px;align-items:center">'
        f'<div><div style="font-size:14px;margin-bottom:4px">{k}. {E(IDEAS[i][0])}</div>'
        f'<div style="height:10px;border-radius:5px;background:var(--line)"><div style="height:100%;width:{score(IDEAS[i][7])}%;border-radius:5px;background:{"#2A2725" if i in TOP else "#B07A4A"}"></div></div></div>'
        f'<b class="mono" style="text-align:right">{score(IDEAS[i][7])}</b></div>' for k, i in enumerate(RANK, 1))
    cards = "".join(
        f'<article class="card" style="display:flex;flex-direction:column;gap:6px"><div style="display:flex;justify-content:space-between;gap:12px">'
        f'<h3>{k}. {E(d[0])}</h3><b class="mono" style="font-size:20px">{score(d[7])}</b></div>'
        f'<p class="cap">{E(d[1])} · ขยับ: {E(d[2])}</p><p>{E(d[3])}</p>'
        f'<p><b>ต้นทุนเงิน</b> {E(d[4])} · <b>เวลา</b> {E(d[5])}</p><p><b>เริ่มยังไง</b> {E(d[6])}</p><p class="cap"><b>ระวัง</b> {E(d[8])}</p></article>'
        for k, d in ((k, IDEAS[i]) for k, i in enumerate(RANK, 1)))
    funnel = "".join(f'<div style="display:grid;grid-template-columns:28px minmax(0,1fr);gap:10px;align-items:start;padding:8px 0;border-top:1px solid var(--line)">'
                     f'<b class="mono">{k}</b><div><b>{E(a)}</b><div class="cap">{E(b)}</div></div></div>' for k, (a, b) in enumerate(FUNNEL, 1))
    check = "".join(f"<li><b>{E(a)}</b> {E(b)}</li>" for a, b in CHECK_FIRST)
    top = "".join(f"<li>{E(IDEAS[i][0])}</li>" for i in TOP)
    w = " · ".join(f"{n} {p}%" for n, p in WEIGHTS)
    return f"""{S.head("OCT. 26 เกมช่วยขาย")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · 26 ต.ค. 2569</span><h1>เกมช่วยขาย</h1>
<p class="lead">10 ไอเดีย gamification พร้อมคะแนน และโมเดลรายได้แบบเกม ทุกข้อเป็นรางวัลที่ได้จากการทำ ไม่มีการสุ่ม และไม่ลดราคาแรง</p></header>
<section><h2>เช็ก 3 ข้อนี้ก่อน</h2><div class="card"><ol>{check}</ol>
<p class="cap" style="margin-top:8px">เกมช่วยให้คนที่มาแล้วซื้อมากขึ้นและกลับมาซื้อซ้ำ แต่ถ้ายังไม่มีคนเห็นร้าน ต้องแก้เรื่องคนเห็นก่อน</p></div></section>
<section><h2>โมเดลรายได้: สะสมครบลาย + ปลดล็อกรอบใหม่</h2>
<div class="card"><p>ลูกค้าแต่ละคนเดินผ่าน 6 ขั้น แต่ละขั้นมีเกมหนึ่งอย่างดันไปขั้นถัดไป รายได้มาจากขั้น 3–6</p>{funnel}
<p class="cap" style="margin-top:8px">ตัวอย่าง: ลูกค้าคนหนึ่งเก็บครบ 5 ลายออนไลน์ ราว 230–250 บาท ต้นทุนชิ้นหนังราว 20 บาท (ยังไม่รวมค่าส่งและค่าธรรมเนียม) · รอบปลดล็อกได้เงินก่อนสั่งบล็อก จึงไม่ต้องลงเงินก่อน</p></div></section>
<section><h2>ทำก่อน: 4 อันดับแรก</h2><div class="card"><ol>{top}</ol></div></section>
<section><h2>คะแนน 10 ไอเดีย</h2><div class="card" style="display:flex;flex-direction:column;gap:12px">{bars}</div>
<p class="cap">น้ำหนัก: {E(w)} · ต้นทุนและค่าเสียโอกาส 5 = ถูก / ใช้เวลาน้อย · สีเข้ม = ทำก่อน</p>
<div style="display:flex;flex-direction:column;gap:12px;margin-top:12px">{cards}</div></section>
<section><h2>ไม่แนะนำ</h2><div class="card"><ul>{"".join(f"<li>{E(x)}</li>" for x in NOT_THESE)}</ul></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">gamify-20261026/build.py</td><td>แก้ไอเดีย คะแนน แล้วรันใหม่</td></tr>
<tr><td>Google Doc "OCT. 26 เกมช่วยขาย"</td><td>ในโฟลเดอร์ OCT. 26 ไฟล์งาน</td></tr>
</tbody></table></div></section></div>"""


def text():
    out = ["OCT. 26 เกมช่วยขาย (26 ต.ค. 2569)", "", "เช็กก่อน:"] + [f"- {a}: {b}" for a, b in CHECK_FIRST]
    out += ["", "โมเดลรายได้: สะสมครบลาย + ปลดล็อกรอบใหม่"] + [f"{k}. {a} ← {b}" for k, (a, b) in enumerate(FUNNEL, 1)]
    out += ["", "น้ำหนัก: " + " · ".join(f"{n} {p}%" for n, p in WEIGHTS), ""]
    for k, i in enumerate(RANK, 1):
        d = IDEAS[i]
        out += [f"{k}. {d[0]} · {score(d[7])}/100" + ("  [ทำก่อน]" if i in TOP else ""), f"   {d[1]} · ขยับ {d[2]}", f"   {d[3]}",
                f"   ต้นทุน {d[4]} · เวลา {d[5]} · เริ่ม {d[6]} · ระวัง {d[8]}", ""]
    out += ["ไม่แนะนำ:"] + [f"- {x}" for x in NOT_THESE]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(page())
    open(os.path.join(HERE, "plan.txt"), "w").write(text())
    for k, i in enumerate(RANK, 1):
        print(k, score(IDEAS[i][7]), IDEAS[i][0])
