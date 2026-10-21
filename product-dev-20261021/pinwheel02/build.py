"""Build pinwheel02/index.html: what to sell die 02 as, after the real test showed crossed 02 pieces fall apart.

Text and numbers come from ../pd.py (PIN02_*), costs from brand.py, the drawings from the real 02 die outline.
"""
import html, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import pd
from geom import PIECES
E = html.escape
G = PIECES["02"]

def path():
    return "M" + " L".join(f"{x:.2f},{-y:.2f}" for x, y in G["poly"]) + " Z"
P = path()
SLOTS = [(f["outer"], f["inner"]) for f in G["feats"].values()]
def slots(cls="slot"):
    return "".join(f'<line class="{cls}" x1="{o[0]:.2f}" y1="{-o[1]:.2f}" x2="{i[0]:.2f}" y2="{-i[1]:.2f}"/>' for o, i in SLOTS)
def svg(inner, vb="-52 -52 104 104", label=""):
    return f'<svg viewBox="{vb}" role="img" aria-label="{E(label)}">{inner}</svg>'
PIECE = f'<path class="leather" d="{P}"/>'
SQ = '<rect class="fold" x="-27.05" y="-27.05" width="54.1" height="54.1"/>'

# why: one lobe swings open on its hinge (the uncut half of the side) when another piece is pushed in
WHY = svg(
    f'{PIECE}{slots()}'
    '<path class="hinge" d="M27.05,0 L27.05,27.05"/>'
    '<path class="arrow" d="M38,-14 q14,-6 10,-24" marker-end="url(#ah)"/>'
    '<text x="22" y="-42" class="lbl">กลีบเปิดออก</text>'
    '<text x="-25" y="4" class="lbl">ตัวกลาง 54 มม.</text>'
    '<text x="-48" y="49" class="lbl red">เส้นแดง: ร่อง 27 มม. · เส้นน้ำเงิน: บานพับของกลีบ</text>'
    '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahd"/></marker></defs>',
    label="บล็อก 02: ร่องสี่เส้นตัดแยกกลีบออกจากตัวกลาง กลีบจึงพับเปิดได้")

# 03-06 compared: a wing wider than the slit sits behind, 02 has nothing behind
LOCK = svg(
    '<rect class="leather" x="-48" y="-6" width="40" height="4"/><rect class="leather" x="-30" y="-30" width="4" height="40"/>'
    '<rect class="wing" x="-38" y="-2" width="20" height="4"/><text x="-50" y="22" class="lbl">03–06 ปีกค้ำด้านหลัง</text>'
    '<rect class="leather" x="8" y="-6" width="40" height="4"/><rect class="leather" x="26" y="-30" width="4" height="34"/>'
    '<path class="arrow" d="M28,8 v14" marker-end="url(#ah2)"/><text x="10" y="22" class="lbl red">02 ดึงก็หลุด</text>'
    '<defs><marker id="ah2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahd"/></marker></defs>',
    vb="-52 -34 104 62", label="เทียบการล็อก: ปีกของ 03–06 ค้ำอยู่หลังร่อง ส่วน 02 ไม่มีอะไรค้ำ")

ART = {
    "A": svg(f'{PIECE}{SQ}{slots()}<path class="cord" d="M-46,0 H46"/><path class="cord" d="M0,-46 V46"/>'
             '<circle class="knot" cx="27.05" cy="-14" r="2.4"/><circle class="knot" cx="-27.05" cy="14" r="2.4"/>'
             '<text x="-48" y="-36" class="lbl">พับกลีบเข้ากลาง แล้วคาดเชือก</text>', label="ซองกังหันคาดเชือก"),
    "B": svg(f'{PIECE}{slots()}<path class="cable" d="M27.05,-12 L27.05,-27.05 L-27.05,27.05 L-27.05,12"/>'
             '<path class="cable" d="M33,-21 L-21,33" opacity=".55"/><path class="cable" d="M21,-33 L-33,21" opacity=".55"/>'
             '<path class="plug" d="M27.05,-12 v-6"/><text x="-48" y="-40" class="lbl">ปลายสายเสียบร่อง พันผ่านรอยเว้า</text>', label="ที่พันสายชาร์จกังหัน"),
    "C": svg(f'<g transform="translate(-24,-8) scale(.5)"><path class="leather" d="{P}"/>{slots()}<path class="floss c1" d="M27,-27 L-27,27 M33,-21 L-21,33 M21,-33 L-33,21"/></g>'
             f'<g transform="translate(24,-8) scale(.5)"><path class="leather" d="{P}"/>{slots()}<path class="floss c2" d="M27,-27 L-27,27 M33,-21 L-21,33 M21,-33 L-33,21"/></g>'
             f'<g transform="translate(0,30) scale(.5)"><path class="leather" d="{P}"/>{slots()}<path class="floss c3" d="M27,-27 L-27,27 M33,-21 L-21,33 M21,-33 L-33,21"/></g>',
             label="ที่พันไหมปักผ้า ชุด 6 ชิ้น"),
    "D": svg(f'{PIECE}<rect class="card" x="-29" y="-29" width="58" height="58"/>'
             f'{slots()}<text x="0" y="-2" class="cardtxt" text-anchor="middle">Beiya</text><text x="0" y="10" class="cardsub" text-anchor="middle">ป้ายชื่อ · ราคา · รูป</text>',
             label="กรอบรูปกังหัน 5.8 ซม."),
    "E": svg(f'<path class="page" d="M-50,-50 H50 V50 Z"/>{PIECE}{slots()}<text x="-48" y="44" class="lbl">มุมกระดาษสอดเข้าร่องเดียว</text>',
             label="ที่คั่นหนังสือมุมกังหัน"),
    "F": svg(f'{PIECE}<circle class="ring" cx="0" cy="0" r="22"/><circle class="ring" cx="2" cy="1" r="18"/>', label="ที่รองแก้วกังหัน"),
}

def card(i):
    key, name, how, who, price, n, extra, pack, test = i
    cost = pd.pin02_cost(n, extra, pack); margin = round((price - cost) / price * 100)
    return f'''<article class="idea">
  <div class="art">{ART[key]}</div>
  <div class="txt">
    <p class="eyebrow">{key} · ใช้ 02 × {n}{(" + " + E(extra[0])) if extra else ""}</p>
    <h3>{E(name)}</h3>
    <p>{E(how)}</p>
    <dl class="num"><dt>คนซื้อ</dt><dd>{E(who)}</dd><dt>ราคา / ต้นทุน</dt><dd>{price} / {cost:.2f} บาท · กำไรขั้นต้น {margin}%</dd>
    <dt>ลองแบบนี้</dt><dd>{E(test)}</dd></dl>
  </div>
</article>'''

WHY_LIST = "".join(f"<li><b>{E(a)}</b><p>{E(b)}</p></li>" for a, b in pd.PIN02_WHY)
IDEAS = "".join(card(i) for i in pd.PIN02_IDEAS)
FIX = "".join(f"<li>{E(x)}</li>" for x in pd.PIN02_FIX)
booth = [p for p in pd.B.PRODUCTS if p["n"] in (5, 6, 7)]
BOOTH = "".join(f"<tr><td>{p['n']}. {E(p['name'])}</td><td class='num'>{p['stock']}</td><td class='num'>{p['price']}</td></tr>" for p in booth)
BOOTH_N = sum(p["stock"] for p in booth); BOOTH_THB = sum(p["stock"] * p["price"] for p in booth)

PAGE = f'''<title>02 กังหัน ขายเป็นอะไรดี</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anuphan:wght@500;600&family=IBM+Plex+Sans+Thai:wght@400;600&family=Jost:wght@400;500&display=swap">
<style>
:root{{
  /* Layout: one 987px reading column; each idea pairs a drawing of the real 02 outline with its numbers. Palette Soi Candy. */
  --bg:#FFF6EC;--card:#FFFFFF;--ink:#1C1B22;--muted:#5A5664;--line:#F1DCCB;--chip:#FBE9DA;
  --cobalt:#2449D8;--tomato:#FF5A36;--sun:#FFC23C;--mint:#2EC4A0;--pink:#FF8AC4;--leather:#B8743A;--leather-fill:#E9C9A6;
  --good:#138A6C;--bad:#D63A17;
  --t-1:12.6px;--t0:16px;--t1:20.4px;--t2:25.9px;--t3:32.9px;
  --s2:8px;--s3:13px;--s4:21px;--s5:34px;--s6:55px;
  --display:"Anuphan","IBM Plex Sans Thai",system-ui,sans-serif;--body:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;--latin:"Jost",system-ui,sans-serif;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#14131A;--card:#1F1E27;--ink:#FFF6EC;--muted:#C2BDCF;--line:#34323F;--chip:#2A2833;--cobalt:#7C97FF;--leather:#D9965A;--leather-fill:#5A3E28;--good:#4FD6B2;--bad:#FF7A5C;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#14131A;--card:#1F1E27;--ink:#FFF6EC;--muted:#C2BDCF;--line:#34323F;--chip:#2A2833;--cobalt:#7C97FF;--leather:#D9965A;--leather-fill:#5A3E28;--good:#4FD6B2;--bad:#FF7A5C;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:var(--t0);line-height:1.618;margin:0;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:var(--s5) var(--s6)}}
.wrap{{max-width:987px;margin:0 auto;display:grid;gap:var(--s6)}}
h1,h2,h3{{font-family:var(--display);font-weight:600;line-height:1.236;text-wrap:balance;margin:0}}
h1{{font-size:clamp(var(--t2),6vw,var(--t3))}}h2{{font-size:var(--t2)}}h3{{font-size:var(--t1)}}
p{{margin:0}}
.eyebrow{{font-family:var(--latin);font-size:var(--t-1);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}
.muted{{color:var(--muted)}}.small{{font-size:var(--t-1)}}.num{{font-variant-numeric:tabular-nums}}
section{{display:grid;gap:var(--s4)}}
.verdict{{background:var(--ink);color:var(--bg);border-radius:21px;padding:var(--s4);display:grid;gap:var(--s2)}}
.verdict b{{font-family:var(--display);font-size:var(--t1)}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:var(--s4);align-items:start}}
.two > *{{min-width:0}}
svg{{width:100%;height:auto;display:block;overflow:visible}}
.figure{{background:var(--card);border:1px solid var(--line);border-radius:21px;padding:var(--s3)}}
.leather{{fill:var(--leather-fill);stroke:var(--leather);stroke-width:.8}}
.slot{{stroke:var(--tomato);stroke-width:1.4;stroke-linecap:round}}
.fold{{fill:none;stroke:var(--leather);stroke-width:.5;stroke-dasharray:2 2}}
.hinge{{stroke:var(--cobalt);stroke-width:2.4}}
.arrow{{fill:none;stroke:var(--cobalt);stroke-width:1.2}}.ahd{{fill:var(--cobalt)}}
.wing{{fill:var(--good)}}
.lbl{{font-size:4.6px;fill:var(--ink);font-family:var(--body)}}.lbl.red{{fill:var(--bad)}}
.cord{{fill:none;stroke:var(--cobalt);stroke-width:1.6;stroke-linecap:round}}.cord.back{{stroke-dasharray:2 2;opacity:.5}}
.knot{{fill:var(--cobalt)}}
.cable{{fill:none;stroke:var(--ink);stroke-width:3;stroke-linecap:round}}.plug{{stroke:var(--muted);stroke-width:4.5}}
.floss{{fill:none;stroke-width:3.4;stroke-linecap:round}}.c1{{stroke:var(--tomato)}}.c2{{stroke:var(--mint)}}.c3{{stroke:var(--cobalt)}}
.card{{fill:var(--card);stroke:var(--muted);stroke-width:.6;stroke-dasharray:1.5 1.5}}
.cardtxt{{font-family:var(--display);font-size:9px;fill:var(--ink);font-weight:600}}.cardsub{{font-size:4.2px;fill:var(--muted)}}
.page{{fill:var(--card);stroke:var(--line);stroke-width:.6}}
.ring{{fill:none;stroke:var(--cobalt);stroke-width:.7;opacity:.5}}
ul.why{{list-style:none;margin:0;padding:0;display:grid;gap:var(--s3)}}
ul.why p{{font-size:var(--t-1);color:var(--muted)}}
.ideas{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:var(--s4)}}
.idea{{background:var(--card);border:1px solid var(--line);border-radius:21px;padding:var(--s4);display:grid;grid-template-columns:130px 1fr;gap:var(--s4);align-items:start}}
.idea > *{{min-width:0}}
.idea .txt{{display:grid;gap:var(--s2)}}
.idea p{{font-size:var(--t-1)}}
dl{{display:grid;gap:2px;margin:0;font-size:var(--t-1)}}dt{{color:var(--muted);margin-top:4px}}dd{{margin:0}}
table{{border-collapse:collapse;width:100%;font-size:var(--t-1)}}td,th{{text-align:left;padding:8px;border-bottom:1px solid var(--line)}}
th{{font-family:var(--display)}}
ol{{margin:0;padding-left:1.3em;display:grid;gap:var(--s2)}}
.tags{{display:flex;flex-wrap:wrap;gap:var(--s2)}}.tag{{background:var(--chip);border-radius:999px;padding:2px 10px;font-size:var(--t-1)}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:13px;background:var(--chip);padding:1px 6px;border-radius:4px;word-break:break-all}}
@media (max-width:420px){{.idea{{grid-template-columns:1fr}} .idea .art{{max-width:160px}}}}
</style>
<div class="wrap">
<header style="display:grid;gap:var(--s3)">
  <p class="eyebrow">OCT. 26 · Product Development · บล็อก 02 กังหัน</p>
  <h1>02 ไขว้กันแล้วหลุด เราจะขายเป็นอะไรดี</h1>
  <div class="verdict"><b>{E(pd.PIN02_TURN)}</b>
    <p>บล็อกเดิมยังใช้ต่อได้ ไม่ต้องทิ้ง ทุกแบบในหน้านี้เป็นสินค้าชิ้นเดียว ไม่ต้องต่อกับชิ้นอื่น จึงไม่ติดเรื่องข้อต่อที่ยังไม่ผ่าน</p></div>
</header>

<section>
  <h2>ทำไมหลุด</h2>
  <div class="two">
    <div class="figure">{WHY}</div>
    <ul class="why">{WHY_LIST}</ul>
  </div>
  <div class="figure" style="max-width:560px">{LOCK}</div>
</section>

<section>
  <h2>งานแฟร์สองสุดสัปดาห์</h2>
  <p>ตามเอกสารสถานะ {E(pd.STATUS_DATE)} งานนี้ขาย 7 SKU ชิ้นเดียว ในนั้นมีที่รองแก้วกังหัน (OC-02-24) กับชุดที่รองแก้ว 4 ลาย (OC-MX-29) ที่ใช้ 02 อยู่แล้ว ส่วนซอง 5 6 7 ไม่ได้ขายงานนี้</p>
  <div class="figure" style="overflow-x:auto"><table class="num"><thead><tr><th>ช่วง</th><th>ทำอะไรกับ 02</th></tr></thead><tbody>
  <tr><td>23–25 ต.ค.</td><td>ขายที่รองแก้ว 24 และ 29 ตามเดิม จดว่าลูกค้าหยิบกังหันไปทำอะไร</td></tr>
  <tr><td>26–29 ต.ค.</td><td>ลองไอเดีย A B D E ด้วยชิ้น 02 ที่เหลือจาก 150 ชิ้น ตามข้อ "ลองแบบนี้"</td></tr>
  <tr><td>30 ต.ค.–1 พ.ย.</td><td>ถ้าแบบไหนผ่านและเจ้าของอนุมัติ เพิ่มเป็น SKU ชิ้นเดียวในสุดสัปดาห์ที่สอง</td></tr>
  </tbody></table></div>
  <p class="small muted">{E(pd.JOINTS_OPEN)}</p>
</section>

<section>
  <h2>สินค้าที่ทำจาก 02 ได้เลย</h2>
  <p class="muted">ราคาเป็นร่าง ต้นทุนคิดแบบเดียวกับ brand.py ซึ่งยังใช้ต้นทุนชิ้นหนังเก่า (02 ชิ้นละ 2.38 บาท) เอกสารสถานะบอกว่าต้นทุนจริง 3.45–4.22 บาทต่อชิ้น กำไรจริงจะต่ำกว่าที่เห็นราว 2 บาทต่อชิ้น ทุกแบบยังต้องลองกับหนังจริงตามข้อ "ลองแบบนี้" ก่อนขาย</p>
  <div class="ideas">{IDEAS}</div>
</section>

<section>
  <h2>ถ้ายังอยากให้ 02 ไขว้กันเป็น 3D</h2>
  <p>ลองแก้กับชิ้นที่ตัดไว้แล้วก่อน ยังไม่ต้องสั่งบล็อกใหม่</p>
  <ol>{FIX}</ol>
  <div class="tags">{"".join(f'<span class="tag">{x} พักไว้</span>' for x in pd.PIN02_3D)}</div>
</section>

<section>
  <h2>ไฟล์และขั้นต่อไป</h2>
  <ul class="why">
    <li><b><code>product-dev-20261021/pd.py</code></b><p>PIN02_WHY, PIN02_IDEAS, PIN02_FIX เหตุผล สินค้า และวิธีลองแก้ หน้านี้สร้างจากไฟล์นี้</p></li>
    <li><b><code>product-dev-20261021/pinwheel02/build.py</code></b><p>สร้างหน้านี้ ภาพวาดจากรูปทรงบล็อก 02 จริง</p></li>
    <li><b>หน้า PD และแท็บไขว้ 3D</b><p>สินค้า 5 6 7 ขึ้นว่าติดเรื่องคาดเชือก แบบ 3D ที่ใช้ 02 ขึ้นป้ายลองจริงแล้วหลุด ไอเดีย A–E อยู่ในบอร์ดขั้นไอเดีย</p></li>
  </ul>
  <ol>
    <li>26–29 ต.ค.: ลองที่พันสาย (B) คั่นหนังสือ (E) และซองคาดเชือก (A) ใช้ชิ้นที่ตัดไว้แล้ว ไม่มีต้นทุนเพิ่ม</li>
    <li>26–29 ต.ค.: ลองกรอบรูป (D) หาขนาดการ์ด</li>
    <li>เจ้าของเลือกว่าจะเพิ่มแบบไหนเป็น SKU ในสุดสัปดาห์ที่สอง แล้วแก้ในเอกสารสถานะ</li>
    <li>ลองแก้ร่องตามขั้นข้างบน ก่อนตัดสินว่าจะสั่ง 02 รุ่น B ไหม</li>
  </ol>
</section>
</div>
'''
open(os.path.join(HERE, "index.html"), "w").write(PAGE)
print("pinwheel02/index.html", len(PAGE), "bytes")
