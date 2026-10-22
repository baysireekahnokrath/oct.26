"""Build assortment/index.html: the product range as a page (Thai, phone first) from assortment.py."""
import html, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import assortment as AS
E = html.escape
GEO = json.load(open(os.path.join(ROOT, "single50", "single50.json")))["geo"]
keep, dropped, use = AS.summary()

def thumb(code, size=44):
    g = GEO[code]; x, y, w, h = map(float, g["vb"].split()); m = max(w, h)
    return (f'<svg class="th" width="{size}" height="{size}" viewBox="{x - 3} {y - 3} {m + 6} {m + 6}" aria-hidden="true">'
            f'<path d="{g["d"]}"/></svg>')

def thumbs(pieces):
    codes = []
    for c, q in pieces: codes += [c] * min(q, 1)
    return "".join(thumb(c, 30 if len(codes) > 1 else 44) for c in codes[:6])

ROLE_CLS = {AS.CORE: "r-core", AS.ADDON: "r-add", AS.GIFT: "r-gift", AS.CUSTOM: "r-custom"}
WAVE_ORDER = [0, 1, 2, "C"]

# ---- matrix: families x waves
cells = ""
for fam in AS.FAMILIES:
    row = f'<tr><th scope="row">{E(fam)}</th>'
    for w in WAVE_ORDER:
        its = [a for a in keep if a["family"] == fam and a["wave"] == w]
        row += "<td>" + "".join(f'<span class="sku {ROLE_CLS[a["role"]]}">{E(a["name"])}</span>' for a in its) + "</td>"
    cells += row + "</tr>"
MATRIX = (f'<table class="matrix"><thead><tr><th></th>' + "".join(f"<th>{E(AS.WAVES[w])}</th>" for w in WAVE_ORDER) +
          f"</tr></thead><tbody>{cells}</tbody></table>")

# ---- price ladder (retail lines only), drawn to scale
retail = [a for a in keep if a["wave"] != "C"]
prices = sorted({a["price"] for a in retail})
counts = {p: sum(a["price"] == p for a in retail) for p in prices}
cmax = max(counts.values()); bw, gap, ch = 34, 10, 120
W = len(prices) * (bw + gap) + 20
bars = ""
for k, p in enumerate(prices):
    h = counts[p] / cmax * ch; x = 10 + k * (bw + gap)
    bars += (f'<rect class="bar" x="{x}" y="{20 + ch - h:.1f}" width="{bw}" height="{h:.1f}" rx="3"/>'
             f'<text class="v" x="{x + bw / 2}" y="{14 + ch - h:.1f}">{counts[p]}</text>'
             f'<text class="l" x="{x + bw / 2}" y="{ch + 36}">{p}</text>')
LADDER = f'<svg class="chart" viewBox="0 0 {W} {ch + 46}" role="img" aria-label="จำนวน SKU ตามราคา">{bars}</svg>'

# ---- leather: stock vs what wave 1 needs at FIRST_RUN each
lw, lh = 300, 18; rows = ""
smax = max(AS.STOCK.values())
for k, c in enumerate(AS.STOCK):
    y = 8 + k * (lh + 16)
    s = AS.STOCK[c] / smax * lw; u = use[c] / smax * lw
    rows += (f'<text class="l left" x="0" y="{y + 13}">{c}</text>'
             f'<rect class="stock" x="26" y="{y}" width="{s:.1f}" height="{lh}" rx="3"/>'
             f'<rect class="need" x="26" y="{y}" width="{u:.1f}" height="{lh}" rx="3"/>'
             f'<text class="v left" x="{30 + s:.1f}" y="{y + 13}">{use[c]} / {AS.STOCK[c]}</text>')
LEATHER = f'<svg class="chart" viewBox="0 0 {lw + 110} {len(AS.STOCK) * (lh + 16) + 8}" role="img" aria-label="ชิ้นหนังที่ใช้ในระลอก 1 เทียบกับที่มี">{rows}</svg>'

def line(a):
    pcs = " + ".join(f"{AS.NAME[c]} {c} × {q}" for c, q in a["pieces"])
    ex = (" · " + " · ".join(f"{E(n)} {t:g} บาท" for n, t in a["extras"])) if a["extras"] else ""
    return (f'<li class="line"><div class="ths">{thumbs(a["pieces"])}</div><div class="txt">'
            f'<p class="eyebrow">{E(a["code"])} · {E(a["family"])} · <span class="{ROLE_CLS[a["role"]]} tagrole">{E(a["role"])}</span></p>'
            f'<b>{E(a["name"])}</b><p class="small">{E(a["how"])}</p>'
            f'<p class="small muted num">{E(pcs)}{ex}</p></div>'
            f'<div class="price num"><b>{a["price"]}</b><span>ทุน {a["cost"]:.2f}</span><span>{round(a["margin"] * 100)}%</span></div></li>')

WAVE_LISTS = "".join(
    f'<section class="wave"><h3>{E(AS.WAVES[w])} <span class="count">{sum(a["wave"] == w for a in keep)}</span></h3><ul class="lines">'
    + "".join(line(a) for a in keep if a["wave"] == w) + "</ul></section>" for w in WAVE_ORDER)

DROPS = "".join(f'<tr><td>{E(i)}</td><td>{E(n)}</td><td><span class="why {"w-food" if r == AS.FOOD else "w-kids" if r == AS.KIDS else "w-load"}">{E(r)}</span></td><td>{E(d)}</td></tr>'
                for i, r, d, n in dropped)
DROPS += "".join(f'<tr><td>สินค้าเดิม {n}</td><td>{E(d)}</td><td><span class="why {"w-food" if r == AS.FOOD else "w-kids"}">{E(r)}</span></td><td>กฎใหม่ 22 ต.ค.</td></tr>'
                 for n, (r, d) in AS.DROP_OLD.items())
RULES = "".join(f'<li><b>{E(a)}</b><p>{E(b)}</p><span class="src">{E(c)}</span></li>' for a, b, c in AS.RULES)
QS = "".join(f"<li>{E(q)}</li>" for q in AS.QUESTIONS)
n = {w: sum(a["wave"] == w for a in keep) for w in WAVE_ORDER}
mr = [a["margin"] for a in keep]

PAGE = f'''<title>OCT. 26 Product Assortment</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@500;600&family=IBM+Plex+Sans+Thai:wght@400;600&family=Jost:wght@400;500&display=swap">
<style>
:root{{
  /* Layout: one 987px column; the range reads as a matrix first (families x waves), then the lines per wave. Soi Candy palette. */
  --bg:#FFF6EC;--card:#FFFFFF;--ink:#1C1B22;--muted:#5A5664;--line:#F1DCCB;--chip:#FBE9DA;
  --cobalt:#2449D8;--tomato:#FF5A36;--sun:#FFC23C;--mint:#2EC4A0;--pink:#FF8AC4;--leather:#B8743A;
  --good:#138A6C;--bad:#D63A17;
  --display:"Anuphan","IBM Plex Sans Thai",system-ui,sans-serif;--body:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;--latin:"Jost",system-ui,sans-serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#14131A;--card:#1F1E27;--ink:#FFF6EC;--muted:#C2BDCF;--line:#34323F;--chip:#2A2833;--cobalt:#7C97FF;--leather:#D9965A;--good:#4FD6B2;--bad:#FF7A5C;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#14131A;--card:#1F1E27;--ink:#FFF6EC;--muted:#C2BDCF;--line:#34323F;--chip:#2A2833;--cobalt:#7C97FF;--leather:#D9965A;--good:#4FD6B2;--bad:#FF7A5C;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.618;margin:0;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:34px 55px}}
.wrap{{max-width:987px;margin:0 auto;display:grid;gap:55px}}
h1,h2,h3{{font-family:var(--display);font-weight:600;line-height:1.236;text-wrap:balance;margin:0}}
h1{{font-size:clamp(26px,6vw,33px)}}h2{{font-size:26px}}h3{{font-size:20px}}
p{{margin:0}}.muted{{color:var(--muted)}}.small{{font-size:12.6px}}.num{{font-variant-numeric:tabular-nums}}
.eyebrow{{font-family:var(--latin);font-size:12.6px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
section{{display:grid;gap:21px}}
.verdict{{background:var(--ink);color:var(--bg);border-radius:21px;padding:21px;display:grid;gap:8px}}
.verdict b{{font-family:var(--display);font-size:20px}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:13px}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px 21px;display:grid;gap:2px}}
.stat b{{font-family:var(--latin);font-weight:500;font-size:33px;line-height:1.1}}
ul.rules{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:13px}}
ul.rules li{{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px 21px;display:grid;gap:4px}}
ul.rules li:nth-child(-n+2){{border-color:var(--tomato)}}
ul.rules p{{font-size:12.6px;color:var(--muted)}}.src{{font-size:12px;color:var(--tomato);font-weight:600}}
.scroll{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-size:12.6px}}
th,td{{text-align:left;vertical-align:top;padding:8px;border-bottom:1px solid var(--line)}}
th{{font-family:var(--display)}}
.matrix{{min-width:720px}}.matrix td{{min-width:140px}}
.sku{{display:inline-block;margin:0 4px 4px 0;padding:2px 9px;border-radius:999px;background:var(--chip);font-size:12px}}
.r-core{{background:var(--cobalt);color:#fff}}.r-add{{background:var(--chip)}}.r-gift{{background:var(--pink);color:#1C1B22}}.r-custom{{background:transparent;border:1px solid var(--muted)}}
.legend{{display:flex;flex-wrap:wrap;gap:8px;font-size:12px}}
.tagrole{{padding:0 6px;border-radius:999px;font-size:11px;text-transform:none;letter-spacing:0}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:21px;align-items:start}}
.figure{{background:var(--card);border:1px solid var(--line);border-radius:21px;padding:13px 21px;display:grid;gap:8px}}
.chart{{width:100%;height:auto;display:block}}
.chart .bar{{fill:var(--cobalt)}}.chart .stock{{fill:var(--chip)}}.chart .need{{fill:var(--tomato)}}
.chart text{{font:12px var(--latin);fill:var(--ink);text-anchor:middle}}.chart text.left{{text-anchor:start}}.chart .l{{fill:var(--muted)}}
.wave h3 .count{{font-family:var(--latin);font-weight:500;color:var(--muted)}}
ul.lines{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}
.line{{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px;display:grid;grid-template-columns:64px 1fr auto;gap:13px;align-items:start}}
.line > *{{min-width:0}}
.ths{{display:flex;flex-wrap:wrap;gap:2px}}
.th path{{fill:var(--chip);stroke:var(--leather);stroke-width:2}}
.price{{display:grid;justify-items:end;font-size:12px;color:var(--muted)}}.price b{{font-family:var(--latin);font-weight:500;font-size:20px;color:var(--ink)}}
.why{{font-size:12px;font-weight:600;border-radius:999px;padding:1px 8px}}
.w-food{{background:var(--tomato);color:#fff}}.w-kids{{background:var(--sun);color:#1C1B22}}.w-load{{background:var(--chip)}}
ol{{margin:0;padding-left:1.3em;display:grid;gap:8px}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:13px;background:var(--chip);padding:1px 6px;border-radius:4px;word-break:break-all}}
@media (max-width:480px){{.line{{grid-template-columns:44px 1fr}} .price{{grid-column:2;justify-items:start;grid-auto-flow:column;gap:8px}}}}
</style>
<div class="wrap">
<header style="display:grid;gap:13px">
  <p class="eyebrow">OCT. 26 · Product Development · 22 ต.ค. 2569</p>
  <h1>Product assortment ชุดใหม่ ไม่โดนอาหาร ไม่ใช่ของเด็ก</h1>
  <div class="verdict"><b>{len(keep)} SKU ใน 6 กลุ่ม ทุกตัวเป็นชิ้นเดียว ใช้ 07 แทน 06 ไม่รับแรง ไม่โดนอาหาร และไม่ใช่ของเด็ก</b>
    <p>ที่รองแก้วยังเป็นสินค้าหลัก เพิ่มของแต่งบ้าน ต้นไม้ โต๊ะทำงาน แต่งตัว และของขวัญ ให้เข้ากับงานบ้านและสวนแฟร์ ตัดไอเดียเดิมที่โดนอาหารหรือเป็นของเด็กออก 19 แบบ และสินค้าเดิมอีก 4 แบบ</p></div>
</header>

<div class="stats num">
  <div class="stat"><span class="small muted">ขายอยู่ตอนนี้</span><b>{n[0]}</b><span class="small muted">7 SKU บูธและ Shopee</span></div>
  <div class="stat"><span class="small muted">ลองแล้วขายสุดสัปดาห์ที่สอง</span><b>{n[1]}</b><span class="small muted">ไม่ต้องซื้ออะไรเพิ่มมาก</span></div>
  <div class="stat"><span class="small muted">หลังงาน</span><b>{n[2]}</b><span class="small muted">ต้องมีของเสริมหรือบล็อกปั๊ม</span></div>
  <div class="stat"><span class="small muted">สั่งทำ</span><b>{n["C"]}</b><span class="small muted">มีจำนวนขั้นต่ำ</span></div>
  <div class="stat"><span class="small muted">กำไรขั้นต้น</span><b>{round(min(mr) * 100)}–{round(max(mr) * 100)}%</b><span class="small muted">ต้นทุนชิ้นจากชีตบัญชี</span></div>
</div>

<section>
  <h2>กติกา 5 ข้อ</h2>
  <ul class="rules">{RULES}</ul>
</section>

<section>
  <h2>ภาพรวมทั้งชุด</h2>
  <div class="legend"><span class="sku r-core">หลัก</span><span class="sku r-add">หยิบเพิ่ม</span><span class="sku r-gift">ของขวัญ</span><span class="sku r-custom">สั่งทำ</span></div>
  <div class="scroll figure">{MATRIX}</div>
</section>

<section class="two">
  <div class="figure"><h3>ราคา</h3><p class="small muted">จำนวน SKU ตามราคาขาย (ไม่นับสั่งทำ) ราคาร่าง รอยืนยัน</p>{LADDER}</div>
  <div class="figure"><h3>ชิ้นหนังที่ระลอก 1 ใช้</h3><p class="small muted">ถ้าทำ SKU ใหม่ของระลอก 1 แบบละ {AS.FIRST_RUN} ชิ้น (แดง) เทียบกับชิ้นที่ตัดไว้ (ทั้งแถบ) ยังไม่หักของที่ใช้ขายสุดสัปดาห์แรก</p>{LEATHER}</div>
</section>

<section>
  <h2>ทุก SKU แยกตามระลอก</h2>
  {WAVE_LISTS}
</section>

<section>
  <h2>ตัดออกตามกฎใหม่</h2>
  <div class="scroll figure"><table><thead><tr><th>เดิม</th><th>ชื่อ</th><th>เหตุผล</th><th>รายละเอียด</th></tr></thead><tbody>{DROPS}</tbody></table></div>
</section>

<section>
  <h2>ให้เจ้าของตัดสิน</h2>
  <ol>{QS}</ol>
</section>

<section>
  <h2>ไฟล์และขั้นต่อไป</h2>
  <ul class="rules">
    <li><b><code>product-dev-20261021/assortment/assortment.py</code></b><p>กติกา รายการ SKU ระลอก ต้นทุนจริง สิ่งที่ตัดออก หน้านี้สร้างจากไฟล์นี้ด้วย build.py</p></li>
    <li><b>หน้า PD แท็บชิ้นเดียว 50</b><p>ไอเดียที่ตัดออกขึ้นป้ายแดงพร้อมเหตุผล</p></li>
  </ul>
  <ol>
    <li>ตอบคำถาม 4 ข้อข้างบน โดยเฉพาะอายุเด็กกับคำบนป้าย</li>
    <li>26–29 ต.ค. ลอง {n[1]} SKU ของระลอก 1 ด้วยชิ้นที่ตัดไว้แล้ว ใช้ 07 มากที่สุด</li>
    <li>ตัวที่ผ่าน งานบัญชีเพิ่มเข้าแท็บ SKU ในชีต และงานการตลาดทำการ์ดสินค้า ก่อนสุดสัปดาห์ที่สอง</li>
  </ol>
</section>
</div>
'''
open(os.path.join(HERE, "index.html"), "w").write(PAGE)
print("assortment/index.html", len(PAGE), "bytes")
