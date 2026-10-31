"""OCT. 26 business model, from the first two booths (owner, 31 Oct: "คิด business model").

Evidence: the sales sheet (31 Oct) 4,440 THB in 20 bills: 07 pieces 60 x 30 = 1,800 · zip pouches 7 x 200 = 1,400 ·
straps 130 · 01 x 6 = 180 · 03 x 1 = 30 · flower 30 · not yet split 870. 01–05 stock was 969 pieces; 07 was 200.
Owner 31 Oct: joined pieces sell because people see them finished; DIY drawing does not; ready-to-buy goods.
Costs from the status doc: 8,313 spent (leather, dies, cutting), piece cost 3.45–4.22, booth fees not counted.
python3 bizmodel-20261101/build.py -> site/index.html, plan.txt
"""
import html, importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sp = importlib.util.spec_from_file_location("brand_site", os.path.join(REPO, "brand-20261014", "site", "build.py"))
S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
E = html.escape

SALES = [  # (what, baht) from the sheet, 23 Oct–31 Oct
    ("07 ชิ้นหนัง (ลูกค้าซื้อไปต่อตามตัวอย่าง) 60 แผ่น", 1800),
    ("กระเป๋าซิปหนัง 7 ใบ (ของสปอนเซอร์ ASE)", 1400),
    ("ยังไม่ได้แยกสินค้า (DIY และอื่น ๆ จากใบจดมือ)", 870),
    ("01 หมี 6 แผ่น · 03 1 แผ่น · ดอกไม้ 1", 240),
    ("สายคล้อง", 130),
]
TOTAL = sum(v for _, v in SALES)
SPENT, GROSS = 8313, 4110

LEARN = [
    ("คนซื้อของที่เห็นเสร็จแล้ว", "07 ขาย 60 แผ่นจาก 200 เพราะต่อให้ดูเป็นปลอกแก้ว ถาด charm · ชิ้นแบน 01–05 มี 969 แผ่น ขายได้ 7 แผ่น"),
    ("ของราคา 200 ขายได้", "กระเป๋าซิป 200 บาทขาย 7 ใบ เท่ากับ 1 ใน 3 ของยอด · คนพร้อมจ่ายหลักร้อยถ้าเห็นว่าใช้ทำอะไร"),
    ("DIY วาดรูปไม่คุ้มเวลา", "กินเวลาคนในบูธ ไม่ทำให้ยอดขึ้น (เจ้าของ 31 ต.ค.) · แต่การเขียนชื่อให้ (ป้ายชื่อสัตว์เลี้ยง) เป็นของขายได้"),
    ("ต้นทุนจริงคือเวลาประกอบ", "ชิ้นหนังราว 4 บาท ของ 300 บาทใช้หนังไม่ถึง 60 บาท · ที่จำกัดคือชั่วโมงของคนในบ้าน และ 07 ที่เหลือ 140 แผ่น"),
]

CANVAS = [  # Business Model Canvas, short
    ("ลูกค้า", ["คนเดินงานแฟร์ 25–45 ซื้อของใช้หรือของขวัญ 150–700 บาท", "คนรักสัตว์ (ป้ายชื่อน้อง)", "ร้านกาแฟ บริษัท งานแต่ง (สั่งจำนวน)", "คนแต่งบ้าน (โคม ภาพติดผนัง สั่งจองก่อน)"]),
    ("คุณค่าที่ให้", ["ของหนังวัวแท้จากเศษหนัง ทุกชิ้นสีไม่ซ้ำ", "ระบบชิ้นต่อกันได้ ทำได้หลายทรง หลายขนาด", "เขียนชื่อให้ เป็นของเฉพาะคน", "ครอบครัวทำเอง เรื่องเล่าจริง"]),
    ("ช่องทาง", ["บูธแฟร์: หาลูกค้าใหม่ ได้เงินสด", "LINE OA: สั่งซ้ำ สั่งทำ สั่งจอง", "เว็บ: แค็ตตาล็อกและหน้าจอง", "Shopee: ของพร้อมส่ง (ยังไม่มีลิงก์ร้าน)"]),
    ("ความสัมพันธ์", ["บัตรสะสมครบ 6 ลาย", "ส่งรูปของจริงทาง LINE", "รอบจองแบบทำทีละรอบ"]),
    ("รายได้", ["ของพร้อมใช้ 149–669", "เขียนชื่อ +30 ต่อชื่อ", "สั่งทำขนาดพิเศษ", "สั่งจำนวนให้ร้านและบริษัท", "ของแต่งบ้านสั่งจอง 990–4,990", "ชิ้นหนัง 30 สำหรับคนอยากทำเอง"]),
    ("ทรัพยากรหลัก", ["บล็อกตัด 01–07 (จ่ายแล้ว)", "เศษหนังเหลือ 7 กก.", "มือและเวลาของคนในบ้าน", "แบรนด์และเรื่องเล่าห้าคน"]),
    ("กิจกรรมหลัก", ["ออกแบบทรงใหม่จาก 07 03 04 05", "ประกอบของพร้อมใช้", "ออกบูธ เล่าเรื่อง", "ถ่ายรูปของจริงลง LINE IG"]),
    ("พาร์ตเนอร์", ["ร้านตัดหนัง", "ASE (กระเป๋าซิป สายคล้อง)", "ผู้จัดงานแฟร์", "ร้านกาแฟ โรงแรม (ที่โชว์ของ)"]),
    ("ต้นทุน", ["ลงไปแล้ว 8,313 (หนัง บล็อก ค่าตัด)", "ค่าบูธ (ยังไม่ได้ลงบัญชี)", "สาย ห่วง ถุง ป้าย", "เวลาประกอบ (ยังไม่ได้คิดเป็นเงิน)"]),
]

LADDER = [  # (rung, what, price, who, role)
    ("1 ลองก่อน", "ชิ้นหนังแผ่นละ 30 · ชิ้นฟรีจากเกม LINE", "0–30", "คนเดินผ่าน", "ดึงคนเข้าบูธ ได้เพื่อน LINE"),
    ("2 ของเล็กพร้อมใช้", "charm S/M · ป้ายชื่อสัตว์เลี้ยง · ปลอกแก้ว 1 ชั้น", "149–209", "ซื้อเองหรือเป็นของขวัญ", "ขายมากที่สุด ทำเร็ว"),
    ("3 ของใช้ในบ้าน", "ปลอกแก้ว 2–3 ชั้น · ตะกร้า · ช่อดอกไม้", "299–669", "คนแต่งบ้าน", "กำไรต่อชิ้นสูง ใช้เวลาประกอบมากขึ้น"),
    ("4 สั่งทำ สั่งจำนวน", "ขนาดพิเศษ · ของชำร่วย · ของขวัญบริษัทปลายปี · ร้านกาแฟ", "ตามจำนวน", "บริษัท ร้าน งานแต่ง", "ยอดก้อนใหญ่ ต้องตั้งราคาส่ง"),
    ("5 ของแต่งบ้านสั่งจอง", "โคมไฟ · ภาพติดผนัง 3D", "990–4,990", "คนรักงานดีไซน์ โรงแรม คาเฟ่", "รับเงินจองก่อนผลิต ไม่ต้องลงเงินก่อน"),
]

UNIT = [  # (item, price, pieces, material ~, note)
    ("charm M", 209, 5, 5 * 4 + 15, "สาย ห่วง ราว 15 (ประมาณ)"),
    ("ปลอกแก้ว 2 ชั้น", 309, 9, 9 * 4, ""),
    ("ตะกร้า ก้น 2×3", 519, 16, 16 * 4, ""),
    ("ป้ายชื่อสัตว์เลี้ยง", 149, 3, 3 * 4 + 15, "รวมสาย"),
]

PLAN = [
    ("พ.ย. สัปดาห์ 1–2", "SX2026 6–15 พ.ย. (ถ้าได้บูธ)", ["ขายของพร้อมใช้เป็นหลัก ชิ้นแผ่นละ 30 เป็นตัวเสริม", "จดทุกบิลแยกสินค้าในแอปขายของ", "จับเวลาประกอบแต่ละแบบ"]),
    ("พ.ย. สัปดาห์ 3–4", "ออนไลน์และสั่งตัด", ["เปลี่ยน Shopee และเว็บจากชิ้นแบนเป็นของพร้อมใช้ 4–5 แบบ", "สั่งตัด 07 เพิ่ม (เหลือ 140)", "ทำแผ่นราคาของขวัญบริษัทปลายปี ส่งให้คนรู้จัก 20 ราย"]),
    ("ธ.ค.", "ของขวัญปีใหม่", ["ชุดของขวัญ 2 ชุด (ตามกฎชั้น 3 ไม่เกิน 2)", "รับสั่งจำนวนจากบริษัท ร้าน", "เปิดจองโคมรอบแรก"]),
    ("ม.ค.–ก.พ.", "ของแต่งบ้าน", ["ผลิตโคมและภาพติดผนังตามยอดจอง", "เตรียมบูธ Bangkok Design Week 18–28 ก.พ."]),
]

DECIDE = [
    "ให้ของพร้อมใช้เป็นสินค้าหลัก และชิ้นแบน 01–05 เป็นตัวเสริม ใช่ไหม",
    "ยกเลิกหรือปรับกฎ \"ยังไม่ขายของที่ต่อชิ้น\" (ทดสอบ 5 ข้อ) และ \"ของห้อยต้องใช้หนัง 2 มม.\" หรือไม่ เพราะตอนนี้ขายจริงแล้ว",
    "ใครประกอบ ได้กี่ชั่วโมงต่อสัปดาห์ (ตัวนี้กำหนดว่าขายได้เดือนละเท่าไร)",
    "กระเป๋าซิปจาก ASE: ได้ฟรีครั้งเดียว หรือรับมาขายต่อได้ ถ้าขายต่อ แบ่งรายได้อย่างไร",
    "ชิ้น 01–05 ที่เหลือราว 900 แผ่น: ทำเป็นตะกร้าและปลอกจาก 03 04 05 (ต่อได้ตามที่ PD คำนวณ) หรือขายเป็นชุดที่รองแก้วของขวัญ",
]


def target(month_baht, avg_price, minutes):
    units = -(-month_baht // avg_price)
    return units, round(units * minutes / 60)


TARGETS = [(10000, 250, 15), (20000, 250, 15), (30000, 300, 20)]


def page():
    sales = "".join(f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 60px;gap:8px;align-items:center">'
                    f'<div><div style="font-size:14px;margin-bottom:4px">{E(w)}</div><div style="height:10px;border-radius:5px;background:var(--line)">'
                    f'<div style="height:100%;width:{v / TOTAL * 100:.0f}%;border-radius:5px;background:#2A2725"></div></div></div>'
                    f'<b class="mono" style="text-align:right">{v:,}</b></div>' for w, v in SALES)
    learn = "".join(f'<li><b>{E(a)}</b> {E(b)}</li>' for a, b in LEARN)
    canvas = "".join(f'<div class="card"><b>{E(t)}</b><ul style="margin-top:6px">{"".join(f"<li>{E(x)}</li>" for x in xs)}</ul></div>' for t, xs in CANVAS)
    ladder = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:4px"><div style="display:flex;justify-content:space-between;gap:10px">'
                     f'<b>{E(r)}</b><b class="mono" style="white-space:nowrap">{E(p)}</b></div><div>{E(w)}</div>'
                     f'<div class="cap">{E(c)} · {E(role)}</div></div>' for r, w, p, c, role in LADDER)
    unit = "".join(f'<tr><td>{E(n)}</td><td class="mono">{p}</td><td class="mono">{k}</td><td class="mono">~{m}</td><td class="mono">{(p - m) / p:.0%}</td><td>{E(note)}</td></tr>' for n, p, k, m, note in UNIT)
    tg = "".join(f'<tr><td class="mono">{b:,}</td><td class="mono">{a}</td><td class="mono">{target(b, a, m)[0]}</td><td class="mono">{m}</td><td class="mono">{target(b, a, m)[1]}</td></tr>' for b, a, m in TARGETS)
    plan = "".join(f'<div class="card"><span class="cap">{E(w)}</span><h3>{E(t)}</h3><ul>{"".join(f"<li>{E(x)}</li>" for x in xs)}</ul></div>' for w, t, xs in PLAN)
    decide = "".join(f"<li>{E(d)}</li>" for d in DECIDE)
    return f"""{S.head("OCT. 26 Business Model")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · 1 พ.ย. 2569 · จากยอดขายจริง 2 บูธ</span><h1>Business model</h1>
<p class="lead">เปลี่ยนจากขายชิ้นหนังแบน เป็นขายของพร้อมใช้จากระบบชิ้นต่อกันได้ ใช้เศษหนังเหมือนเดิม แต่ขายเวลาและดีไซน์ ไม่ได้ขายแผ่นหนัง</p></header>
<section><h2>ข้อมูลจริง: ยอดขาย {TOTAL:,} บาท 20 บิล</h2><div class="card" style="display:flex;flex-direction:column;gap:10px">{sales}</div>
<p class="cap">จากชีตบันทึกการขาย 23–31 ต.ค. · กำไรขั้นต้นราว {GROSS:,} บาท เทียบกับเงินที่ลงไป {SPENT:,} บาท (ยังไม่รวมค่าบูธ) คืนทุนแล้วราวครึ่งหนึ่ง</p></section>
<section><h2>เรียนรู้อะไร</h2><div class="card"><ol>{learn}</ol></div></section>
<section><h2>โมเดลที่เสนอ: บันได 5 ขั้น</h2><p class="cap">ทุกขั้นใช้ชิ้นหนังจากบล็อกเดิม ขั้นล่างดึงคนเข้ามา ขั้นบนทำเงิน</p>
<div style="display:flex;flex-direction:column;gap:10px">{ladder}</div></section>
<section><h2>กำไรต่อชิ้น</h2><div class="tbl"><table><thead><tr><th>ของ</th><th>ราคา</th><th>ชิ้น</th><th>ค่าวัสดุ</th><th>เหลือ</th><th></th></tr></thead><tbody>{unit}</tbody></table></div>
<p class="cap">เหลือหลังค่าวัสดุ 80–90% แต่ยังไม่หักเวลาประกอบ ค่าบูธ และค่าส่ง · ที่จำกัดการขายคือชั่วโมงประกอบ ไม่ใช่หนัง</p></section>
<section><h2>อยากได้เดือนละเท่าไร ต้องทำแค่ไหน</h2><div class="tbl"><table><thead><tr><th>ยอดต่อเดือน</th><th>ราคาเฉลี่ย</th><th>ต้องขาย (ชิ้น)</th><th>นาที/ชิ้น</th><th>ชั่วโมงประกอบ</th></tr></thead><tbody>{tg}</tbody></table></div>
<p class="cap">ตัวเลขนาทีต่อชิ้นเป็นสมมติฐาน ช่วยจับเวลาจริงตอนประกอบ แล้วผมจะแก้ตารางนี้ให้</p></section>
<section><h2>ภาพรวมโมเดล (Business Model Canvas)</h2><div class="grid">{canvas}</div></section>
<section><h2>แผน 4 เดือน</h2><div class="grid">{plan}</div></section>
<section><h2>ต้องตัดสิน</h2><div class="card"><ol>{decide}</ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">bizmodel-20261101/build.py</td><td>แก้ตัวเลข สมมติฐาน แผน แล้วรันใหม่</td></tr>
<tr><td>Google Doc "OCT. 26 Business Model"</td><td>ในโฟลเดอร์ OCT. 26 ไฟล์งาน</td></tr></tbody></table></div></section></div>"""


def text():
    out = ["OCT. 26 Business Model (1 พ.ย. 2569, จากยอดขายจริง 2 บูธ)", "", f"ยอดขาย {TOTAL:,} บาท 20 บิล"]
    out += [f"- {w}: {v:,}" for w, v in SALES]
    out += [f"กำไรขั้นต้นราว {GROSS:,} เทียบลงทุน {SPENT:,} (ไม่รวมค่าบูธ)", "", "เรียนรู้"] + [f"- {a}: {b}" for a, b in LEARN]
    out += ["", "บันได 5 ขั้น"] + [f"- {r}: {w} · {p} · {c} · {role}" for r, w, p, c, role in LADDER]
    out += ["", "Business Model Canvas"] + [f"- {t}: " + " · ".join(xs) for t, xs in CANVAS]
    out += ["", "แผน 4 เดือน"] + [f"- {w} {t}: " + " · ".join(xs) for w, t, xs in PLAN]
    out += ["", "ต้องตัดสิน"] + [f"{i}. {d}" for i, d in enumerate(DECIDE, 1)]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(page())
    open(os.path.join(HERE, "plan.txt"), "w").write(text())
    print(TOTAL, [target(*t) for t in TARGETS])
