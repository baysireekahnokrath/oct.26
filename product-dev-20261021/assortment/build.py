"""Build assortment/index.html: the range in three tiers (tiers.py) as a page, Thai, phone first."""
import html, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import assortment as AS, skucode, tiers as TR
E = html.escape
GEO = json.load(open(os.path.join(ROOT, "single50", "single50.json")))["geo"]
DRAFT = skucode.drafts_for(AS.A)
DRAFT.update(skucode.drafts([a["key"] for a in TR.ALL]))     # same numbers as the PD page tab ตรวจผ่าน
PD_REVIEW = "https://claude.ai/artifact/SfbLavVZF6JAnZKXP75EFy#review"
# real numbers the owner had given when this page was built (PD database, reviews, 22 Oct 05:48 UTC); live list on the PD page
TICKED = {"0001": 260001, "0002": 260002, "0003": 260003, "0004": 260004, "0005": 260005, "0006": 260006,
          "0008": 260007, "0009": 260008}
_, dropped, _ = AS.summary()

def thumb(code, size=44):
    g = GEO[code]; x, y, w, h = map(float, g["vb"].split()); m = max(w, h)
    return (f'<svg class="th" width="{size}" height="{size}" viewBox="{x - 3} {y - 3} {m + 6} {m + 6}" aria-hidden="true">'
            f'<path d="{g["d"]}"/></svg>')

def thumbs(pieces, size=None):
    codes = [c for c, _ in pieces][:6]
    return "".join(thumb(c, size or (28 if len(codes) > 1 else 44)) for c in codes)

def real_tag(key):
    d = DRAFT[key]
    return (f'<span class="real num">ผ่านแล้ว {skucode.real(TICKED[d])}</span>' if d in TICKED else
            '<span class="wait">รอติ๊ก</span>')

def line(a):
    pcs = " + ".join(f"{c} × {q}" for c, q in a["pieces"]) or "ใช้กับชิ้นไหนก็ได้"
    ex = (" · " + " · ".join(f"{E(n)} {t:g} บาท" for n, t in a["extras"])) if a["extras"] else ""
    uses = ""
    if a["tier"] == 1:
        uses = '<p class="small">ใช้ทำ: ' + " · ".join(E(u) for u, _ in TR.USES[a["pieces"][0][0]]) + "</p>"
    note = f'<p class="small muted">{E(a["note"])}</p>' if a["note"] else ""
    return (f'<li class="line"><div class="ths">{thumbs(a["pieces"] or [("05", 1)])}</div><div class="txt">'
            f'<p class="eyebrow"><span class="draftno">ร่าง {DRAFT[a["key"]]}</span> {real_tag(a["key"])}</p>'
            f'<b>{E(a["name"])}</b><p class="small">{E(a["how"])}</p>{uses}'
            f'<p class="small muted num">{E(pcs)}{ex}</p>{note}</div>'
            f'<div class="price num"><b>{a["price"]}</b><span>ทุน {a["cost"]:.2f}</span><span>{round(a["margin"] * 100)}%</span></div></li>')

TIER_INFO = {
    "t1": "ลายละ 1 SKU ลูกค้าเลือกเองว่าจะเอากี่ชิ้น ลายไหน และเอาไปทำอะไร ที่บูธแผ่นละ 30 บาท เป็นราคาบูธอย่างเดียว ไม่ลดตามจำนวน (เจ้าของ 22 ต.ค.)",
    "t2": "มีของจริงเพิ่มในถุง เริ่มลายละแบบเดียว ถ้าขายได้ค่อยเพิ่มลายอื่น ของเพิ่มซื้อได้ทั่วไป",
    "t2r": "ยังไม่ทำ เก็บไว้เพิ่มเมื่อมีคนถาม หรือเมื่อมีบล็อกปั๊มตัวอักษร",
    "t3": "ชุดที่จัดไว้แล้วไม่เกิน 2 แบบ เป็นของขวัญพร้อมให้ ไม่ต้องคิดเอง",
}
TIER_HTML = "".join(
    f'<section class="tier" id="{g}"><h3>{E(label)} <span class="count">{len(its)}</span></h3><p class="muted">{E(TIER_INFO[g])}</p>'
    f'<ul class="lines">{"".join(line(a) for a in its)}</ul></section>' for g, label, its in TR.TIERS)

# what each piece can do: the A4 idea folder
PATTERN_NAME = {a["pieces"][0][0]: a["name"] for a in TR.T1}
USES_HTML = "".join(
    f'<li class="use"><div class="ths">{thumb(c, 52)}</div><div><b>{E(PATTERN_NAME[c])}</b><ol>'
    + "".join(f"<li><b>{E(u)}</b> {E(h)}</li>" for u, h in TR.USES[c]) + "</ol></div></li>" for c in TR.USES)
FIX_HTML = "".join(f"<li><b>{E(a)}</b> · {E(b)}</li>" for a, b in TR.FOLDER_FIX)

# where the 43 old lines went
KEPT = {a["key"]: a for a in TR.ALL}
GROUP_NAME = {g: label.split(" · ")[0] for g, label, _ in TR.TIERS}
moves = []
for old in AS.A:
    k = old["code"]
    if k in KEPT: to = f'อยู่ต่อ · {GROUP_NAME[KEPT[k]["group"]]} · {E(KEPT[k]["name"])}'
    else:
        why, t = TR.RETIRED[k]
        to = f'{E(why)} → {E(KEPT[t]["name"])}'
    gone = f' <span class="real gone num">{skucode.real(TICKED[DRAFT[k]])} ยกเลิก</span>' if k not in KEPT and DRAFT[k] in TICKED else ""
    moves.append((DRAFT[k], f'<tr><td class="num">{DRAFT[k]}</td><td>{E(old["name"])} <span class="muted num">{old["price"]}</span></td><td>{to}{gone}</td></tr>'))
MOVES = "".join(r for _, r in sorted(moves))

DROPS = "".join(f'<tr><td>{E(i)}</td><td>{E(n)}</td><td><span class="why {"w-food" if r == AS.FOOD else "w-kids" if r == AS.KIDS else "w-load"}">{E(r)}</span></td><td>{E(d)}</td></tr>'
                for i, r, d, n in dropped)
DROPS += "".join(f'<tr><td>สินค้าเดิม {n}</td><td>{E(d)}</td><td><span class="why {"w-food" if r == AS.FOOD else "w-kids"}">{E(r)}</span></td><td>กฎใหม่ 22 ต.ค.</td></tr>'
                 for n, (r, d) in AS.DROP_OLD.items())
RULES = "".join(f'<li><b>{E(a)}</b><p>{E(b)}</p><span class="src">{E(c)}</span></li>' for a, b, c in AS.RULES)
QS = "".join(f"<li>{E(q)}</li>" for q in TR.QUESTIONS + AS.QUESTIONS)
start = len(TR.T1) + len(TR.T2) + len(TR.T3)
ticked_kept = sum(DRAFT[a["key"]] in TICKED for a in TR.ALL)

PAGE = f'''<title>OCT. 26 Product Range</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@500;600&family=IBM+Plex+Sans+Thai:wght@400;600&family=Jost:wght@400;500&display=swap">
<style>
:root{{
  /* One 987px column: the three tiers first, then the idea folder, then where the old list went. Brand Book v2 nature palette. */
  --bg:#F4F0E8;--card:#FFFFFF;--ink:#2A2725;--muted:#5E5953;--line:#E2DACB;--chip:#EBE4D6;
  --red:#A9442B;--green:#5E7A3A;--sun:#E9A825;--violet:#B9A3D6;--indigo:#2E4A7D;--leather:#B8743A;
  --good:#4E6B2E;--bad:#A9442B;
  --display:"Anuphan","IBM Plex Sans Thai",system-ui,sans-serif;--body:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;--latin:"Jost",system-ui,sans-serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1C1A18;--card:#26231F;--ink:#F4F0E8;--muted:#C9C1B4;--line:#3A3530;--chip:#332F2A;--indigo:#8FA7D6;--green:#9DBA72;--good:#9DBA72;--bad:#E08A70;--red:#E08A70;--leather:#D9965A;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#1C1A18;--card:#26231F;--ink:#F4F0E8;--muted:#C9C1B4;--line:#3A3530;--chip:#332F2A;--indigo:#8FA7D6;--green:#9DBA72;--good:#9DBA72;--bad:#E08A70;--red:#E08A70;--leather:#D9965A;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.618;margin:0;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:34px 55px}}
.wrap{{max-width:987px;margin:0 auto;display:grid;gap:55px}}
h1,h2,h3{{font-family:var(--display);font-weight:600;line-height:1.236;text-wrap:balance;margin:0}}
h1{{font-size:clamp(26px,6vw,33px)}}h2{{font-size:26px}}h3{{font-size:20px}}
p{{margin:0}}.muted{{color:var(--muted)}}.small{{font-size:12.6px}}.num{{font-variant-numeric:tabular-nums}}
.eyebrow{{font-family:var(--latin);font-size:12.6px;letter-spacing:.06em;color:var(--muted)}}
section{{display:grid;gap:21px}}
.verdict{{background:var(--ink);color:var(--bg);border-radius:21px;padding:21px;display:grid;gap:8px}}
.verdict b{{font-family:var(--display);font-size:20px}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:13px}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px 21px;display:grid;gap:2px}}
.stat b{{font-family:var(--latin);font-weight:500;font-size:33px;line-height:1.1}}
.flow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:13px}}
.flow > div{{background:var(--card);border:1px solid var(--line);border-top:5px solid var(--c);border-radius:13px;padding:13px 21px;display:grid;gap:6px;align-content:start}}
.flow b{{font-family:var(--display);font-size:18px}}
.flow .eg{{font-size:12.6px;color:var(--muted)}}
.tier{{gap:13px}}.tier h3 .count{{font-family:var(--latin);font-weight:500;color:var(--muted)}}
ul.lines,ul.uses{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}
.line,.use{{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px;display:grid;grid-template-columns:64px 1fr auto;gap:13px;align-items:start}}
.use{{grid-template-columns:64px 1fr}}
.line > *,.use > *{{min-width:0}}
.use ol{{margin:6px 0 0;padding-left:1.2em;display:grid;gap:4px;font-size:14px}}
.ths{{display:flex;flex-wrap:wrap;gap:2px}}
.th path{{fill:var(--chip);stroke:var(--leather);stroke-width:2}}
.price{{display:grid;justify-items:end;font-size:12px;color:var(--muted)}}.price b{{font-family:var(--latin);font-weight:500;font-size:20px;color:var(--ink)}}
.draftno{{background:var(--chip);color:var(--ink);border-radius:6px;padding:0 6px;letter-spacing:.06em}}
.real{{color:var(--good);font-weight:600}}.real.gone{{color:var(--bad);text-decoration:line-through}}.wait{{color:var(--muted)}}
.cta{{display:inline-block;background:var(--ink);color:var(--bg);border-radius:999px;padding:8px 18px;text-decoration:none;font-weight:600}}
.figure{{background:var(--card);border:1px solid var(--line);border-radius:21px;padding:13px 21px;display:grid;gap:8px}}
ul.rules{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:13px}}
ul.rules li{{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px 21px;display:grid;gap:4px}}
ul.rules p{{font-size:12.6px;color:var(--muted)}}.src{{font-size:12px;color:var(--red);font-weight:600}}
.scroll{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-size:12.6px}}
th,td{{text-align:left;vertical-align:top;padding:8px;border-bottom:1px solid var(--line)}}
th{{font-family:var(--display)}}
.why{{font-size:12px;font-weight:600;border-radius:999px;padding:1px 8px}}
.w-food{{background:var(--red);color:#fff}}.w-kids{{background:var(--sun);color:#2A2725}}.w-load{{background:var(--chip)}}
details summary{{cursor:pointer;font-family:var(--display);font-weight:600;font-size:18px}}
ol{{margin:0;padding-left:1.3em;display:grid;gap:8px}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:13px;background:var(--chip);padding:1px 6px;border-radius:4px;word-break:break-all}}
@media (max-width:480px){{.line{{grid-template-columns:44px 1fr}} .price{{grid-column:2;justify-items:start;grid-auto-flow:column;gap:8px}} .use{{grid-template-columns:52px 1fr}}}}
</style>
<div class="wrap">
<header style="display:grid;gap:13px">
  <p class="eyebrow">OCT. 26 · PRODUCT DEVELOPMENT · 22 ต.ค. 2569</p>
  <h1>สินค้า 3 ชั้น: ชิ้นเปล่า · ชิ้นบวกของเพิ่ม · ชุด</h1>
  <div class="verdict"><b>เริ่มขาย {start} SKU จาก 43 เดิม (สำรองอีก {len(TR.T2_RESERVE)})</b>
    <p>ชิ้นเดียวกันที่เคยตั้งชื่อหลายแบบ รวมเป็นชิ้นเปล่า SKU เดียว การใช้งานแบบต่างๆ ย้ายไปเป็นไอเดียบนการ์ดและในแฟ้ม A4 SKU ใหม่มีเมื่อของในถุงต่างกันจริงเท่านั้น
      เลขจริงที่เจ้าของติ๊กไว้ {len(TICKED)} ตัว อยู่ต่อ {ticked_kept} ตัว อีก 1 ตัวเป็นชิ้นเดียวกันจึงยกเลิก</p>
    <p><a class="cta" href="{PD_REVIEW}" target="_blank" rel="noopener">ไปติ๊กผ่าน / ไม่ผ่าน ในหน้า PD</a></p></div>
</header>

<section>
  <h2>3 ชั้นคืออะไร</h2>
  <div class="flow">
    <div style="--c:var(--indigo)"><span class="eyebrow">ชั้น 1</span><b>ชิ้นเปล่า</b><p>ลายละ 1 SKU ขายตามจำนวน ซื้อ 01 ห้าชิ้น 02 เจ็ดชิ้น ก็คือ 2 SKU ในบิลเดียว</p><p class="eg">ไอเดียการใช้อยู่บนการ์ด ไม่ใช่ SKU</p></div>
    <div style="--c:var(--green)"><span class="eyebrow">ชั้น 2</span><b>ชิ้น + ของเพิ่มจริง</b><p>เชือก ไม้ไผ่ ริบบิ้น ยางยืด การ์ด แม่เหล็ก หรือการปั๊ม ของในถุงต่างกัน จึงเป็น SKU ใหม่</p><p class="eg">เริ่มลายละแบบเดียว ขายได้ค่อยเพิ่มลาย</p></div>
    <div style="--c:var(--sun)"><span class="eyebrow">ชั้น 3</span><b>ชุดที่จัดไว้แล้ว</b><p>ไม่เกิน 2 ชุด เป็นของขวัญพร้อมให้ ลูกค้าที่อยากคละเองซื้อชั้น 1 ตามจำนวน</p><p class="eg">เก็บสต็อกเป็นชิ้น จัดชุดตอนขาย</p></div>
  </div>
  <div class="stats num">
    <div class="stat"><span class="small muted">ชั้น 1 ชิ้นเปล่า</span><b>{len(TR.T1)}</b><span class="small muted">บูธ 23 ต.ค. ขาย 01–05</span></div>
    <div class="stat"><span class="small muted">ชั้น 2 เริ่มก่อน</span><b>{len(TR.T2)}</b><span class="small muted">สำรอง {len(TR.T2_RESERVE)}</span></div>
    <div class="stat"><span class="small muted">ชั้น 3 ชุด</span><b>{len(TR.T3)}</b><span class="small muted">ขายอยู่ 1 ชุด</span></div>
    <div class="stat"><span class="small muted">SKU เดิมที่รวมหรือเลิก</span><b>{len(TR.RETIRED)}</b><span class="small muted">จาก 43</span></div>
  </div>
</section>

<section>
  <h2>ทุก SKU แยกตามชั้น</h2>
  <p class="muted small">เลขร่างไม่เปลี่ยน เลขจริงคือที่เจ้าของติ๊กผ่านแล้ว ณ ตอนทำหน้านี้ ดูล่าสุดในหน้า PD แท็บตรวจผ่าน ราคาทุกตัวยังเป็นราคาร่าง</p>
  {TIER_HTML}
</section>

<section>
  <h2>ชิ้นหนังแต่ละลายเอาไปทำอะไรได้</h2>
  <p class="muted">สำหรับแฟ้มไอเดีย A4 ที่บูธ (ฝ่าย PD สรุปแทนตัวอย่างเดิม) และการ์ดสินค้า ทุกข้อใช้ชิ้นเดียว ไม่ต่อชิ้น ไม่ห้อยหรือรับแรง ไม่โดนอาหาร ไม่ใช่ของเด็กเล็ก</p>
  <ul class="uses">{USES_HTML}</ul>
  <div class="figure"><b>ต้องแก้ในแฟ้ม A4 เดิม</b><ul class="small" style="margin:0;padding-left:1.2em">{FIX_HTML}</ul>
    <p class="small muted">ไฟล์แฟ้มอยู่ในกิ่ง claude/vigilant-faraday-00e92g · print-20261022/build.py (ตัวแปร IDEAS) ทีมที่ทำไฟล์นั้นเอารายการข้างบนไปแทนได้เลย</p></div>
</section>

<section>
  <h2>ให้เจ้าของตัดสิน</h2>
  <ol>{QS}</ol>
</section>

<section>
  <details><summary>43 SKU เดิมไปอยู่ไหน</summary>
  <div class="scroll figure" style="margin-top:13px"><table><thead><tr><th>ร่าง</th><th>เดิม</th><th>ตอนนี้</th></tr></thead><tbody>{MOVES}</tbody></table></div>
  </details>
</section>

<section>
  <h2>กติกาที่ยังใช้อยู่</h2>
  <ul class="rules">{RULES}</ul>
  <details><summary>ไอเดียที่ตัดออกตามกฎ</summary>
  <div class="scroll figure" style="margin-top:13px"><table><thead><tr><th>เดิม</th><th>ชื่อ</th><th>เหตุผล</th><th>รายละเอียด</th></tr></thead><tbody>{DROPS}</tbody></table></div>
  </details>
</section>

<section>
  <h2>ไฟล์และขั้นต่อไป</h2>
  <ul class="rules">
    <li><b><code>product-dev-20261021/assortment/tiers.py</code></b><p>รายการ 3 ชั้น ไอเดียการใช้ของแต่ละลาย และ 43 เดิมไปไหน หน้านี้กับแท็บตรวจผ่านสร้างจากไฟล์นี้</p></li>
    <li><b><code>assortment/skucode.py</code> · <code>draft_numbers.json</code></b><p>เลขร่างและเลขจริงแบบ IKEA เลขร่างไม่เลื่อน เลขจริงไม่ใช้ซ้ำ</p></li>
  </ul>
  <ol>
    <li>ตอบคำถามข้างบน</li>
    <li>ติ๊กชั้น 2 และชิ้น 03 ในหน้า PD แท็บตรวจผ่าน</li>
    <li>26–29 ต.ค. ลองชั้น 2 ทั้ง {len(TR.T2)} แบบกับชิ้นจริง ซื้อเชือก ไม้ไผ่ ริบบิ้น ยางยืด การ์ด</li>
    <li>ทีมการตลาดเอาไอเดียการใช้ไปใส่แฟ้ม A4 และการ์ด งานบัญชีรวม 2 หน้าใน Shopee ที่เป็นชิ้น 01 เดียวกัน</li>
  </ol>
</section>
</div>
'''
open(os.path.join(HERE, "index.html"), "w").write(PAGE)
print("assortment/index.html", len(PAGE), "bytes")
