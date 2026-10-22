"""Pattern introduction cards, one per pattern (22 Oct 2026): real die-cut photo, number, name, die outline, size.

Social 1080 x 1350 PNG (IG / FB / LINE / Shopee / web) and A4 portrait PDF for the booth, same layout.
02 has no photo yet, so its card uses the die outline until a photo on white paper comes in.

python3 cutout.py  -> cut/*.png  (real pieces)
python3 build.py   -> html/*.html and jobs.json;  node render.cjs -> social/*.png, print/*.pdf
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BOOK = os.path.join(ROOT, "brand-20261014", "brandbook-v2")
sys.path.insert(0, BOOK)
from palette import C, BAND  # noqa: E402

FONTS = os.path.join(ROOT, "brand-20261014", "fonts")
LOGO = os.path.join(BOOK, "logo", "svg")
DIE = {"01": "diecut-leather-20261014/svg/01-bear-head.svg", "02": "diecut-leather-20261014/svg/02-pinwheel-4-lobe.svg",
       "03": "diecut-leather-20261014/svg/03-capsule-cross.svg", "04": "diecut-leather-20261014/svg/04-rounded-square-diagonal.svg",
       "05": "diecut-leather-20261014/svg/05-circle.svg", "07": "diecut-leather-20261019/svg/07-round-joint-cross.svg"}

PATTERNS = [  # number, Thai name, English name, use now, pieces (hero first; None = no photo yet)
    ("01", "หมี", "Bear", "ที่รองแก้ว · ที่เก็บสายชาร์จ", ["01-3", "01-1", "01-2"]),
    ("02", "กังหัน", "Pinwheel", "ที่รองแก้ว", None),
    ("03", "กากบาทแคปซูล", "Capsule cross", "ป้ายห้อยของขวัญ", ["03-1", "03-4", "03-2"]),
    ("04", "สี่เหลี่ยมมน", "Rounded square", "ที่รองแก้ว", ["04-6", "04-2", "04-1"]),
    ("05", "วงกลม", "Circle", "ที่รองแก้ว", ["05-6", "05-4", "05-1"]),
    ("07", "กากบาทข้อต่อวงกลม", "Round-joint cross", "สินค้าใหม่ เร็ว ๆ นี้", ["07-2", "07-4", "07-3"]),
]


def die(code):
    """viewBox size in mm and the cut and slit paths of the real die drawing."""
    s = open(os.path.join(ROOT, DIE[code])).read()
    w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    cut = re.search(r'<g id="CUT"[^>]*>(.*?)</g>', s, re.S).group(1)
    sl = re.search(r'<g id="SLIT"[^>]*>(.*?)</g>', s, re.S).group(1)
    return w, h, cut, sl


def outline(code, cls="die"):
    w, h, cut, sl = die(code)
    return (f'<svg class="{cls}" viewBox="-1 -1 {w + 2} {h + 2}" aria-hidden="true">'
            f'<g fill="none" stroke="{C["charcoal"]}" stroke-width="0.7">{cut}</g>'
            f'<g fill="none" stroke="{C["charcoal"]}" stroke-width="0.7">{sl}</g></svg>')


def solid(code):
    """02 until it is photographed: the die shape in hide brown, slits in cotton."""
    w, h, cut, sl = die(code)
    return (f'<svg class="solid" viewBox="0 0 {w} {h}" aria-hidden="true">'
            f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#BE8A58"/>'
            f'<stop offset="1" stop-color="{C["teak"]}"/></linearGradient></defs>'
            f'<g fill="url(#g)" fill-rule="evenodd" stroke="none">{cut}</g>'
            f'<g fill="none" stroke="{C["cotton"]}" stroke-width="0.9" stroke-linecap="round">{sl}</g></svg>')


def logo(name):
    svg = open(os.path.join(LOGO, name + ".svg")).read()
    return re.sub(r' width="[\d.]+" height="[\d.]+"', ' class="logo"', svg, count=1)


def band():
    return '<div class="band">' + "".join(f'<span style="background:{c}"></span>' for c in BAND) + "</div>"


CSS = f"""
@font-face{{font-family:Jost;src:url(file://{FONTS}/alt/Jost-Regular.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url(file://{FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Anuphan;font-weight:500;src:url(file://{FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Plex;src:url(file://{FONTS}/IBMPlexSansThai-Regular.ttf)}}
*{{box-sizing:border-box}} html,body{{margin:0}}
@page{{size:A4;margin:0}}
body{{font-family:Plex,sans-serif;color:{C['charcoal']};background:{C['cotton']}}}
.c{{width:100vw;height:100vh;position:relative;overflow:hidden;background:{C['cotton']}}}
.top{{position:absolute;left:6vw;right:6vw;top:5vw;display:flex;justify-content:space-between;align-items:center}}
.logo{{width:9vw;height:9vw;display:block}}
.top span{{font-family:Jost;font-size:2.3vw;letter-spacing:.14em;text-transform:uppercase;color:{C['stone']}}}
.num{{position:absolute;left:5.4vw;top:15vw;font-family:Jost;font-weight:500;font-size:30vw;line-height:.8;letter-spacing:-.02em}}
.name{{position:absolute;left:6vw;top:42.5vw;display:grid;gap:.6vw}}
.th{{font-family:Anuphan;font-weight:500;font-size:6.6vw;line-height:1.15}}
.th.long{{font-size:5.2vw}}
.en{{font-family:Jost;font-size:3vw;color:#6E6A64}}
.stage{{position:absolute;left:0;right:0;top:56vw;bottom:23vw}}
.shot{{filter:drop-shadow(0 .5vw .7vw rgba(42,39,37,.22)) drop-shadow(0 .1vw .15vw rgba(42,39,37,.25))}}
.stage{{display:flex;align-items:center;justify-content:center}}
.p0{{width:46vw;max-height:100%;object-fit:contain}}
.side{{position:absolute;right:6vw;top:17vw;display:flex;gap:3vw;align-items:center}}
.side img{{width:16vw}}
.side img:nth-child(2){{transform:rotate(12deg)}}
.solid{{width:46vw;max-height:100%;filter:drop-shadow(0 .5vw .7vw rgba(42,39,37,.22))}}
.foot{{position:absolute;left:6vw;right:6vw;bottom:8vw;display:flex;gap:3vw;align-items:center}}
.die{{width:11vw;height:11vw;flex:none}}
.meta{{display:grid;gap:.4vw;font-size:2.5vw;line-height:1.35}}
.meta b{{font-family:Anuphan;font-weight:500;font-size:2.9vw}}
.muted{{color:#6E6A64}}
.band{{position:absolute;left:0;right:0;bottom:0;height:1.4vw;display:flex}} .band span{{flex:1}}
.tag{{position:absolute;right:6vw;top:44vw;font-size:2.2vw;color:#6E6A64;text-align:right;max-width:34vw}}
/* overview */
.ov .grid{{position:absolute;left:5vw;right:5vw;top:30vw;bottom:14vw;display:grid;grid-template-columns:1fr 1fr 1fr;gap:3vw 3vw}}
.ov .cell{{display:grid;grid-template-rows:1fr auto;gap:1.2vw;align-items:center;justify-items:center}}
.ov .cell img,.ov .cell .solid{{position:static;width:22vw;height:22vw;object-fit:contain;filter:drop-shadow(0 .4vw .5vw rgba(42,39,37,.22))}}
.ov .cap{{text-align:center;display:grid;gap:.2vw}}
.ov .cap b{{font-family:Jost;font-weight:500;font-size:4vw;line-height:1}}
.ov .cap span{{font-family:Anuphan;font-weight:500;font-size:2.6vw}}
.ov h1{{position:absolute;left:6vw;top:16vw;margin:0;font-family:Anuphan;font-weight:500;font-size:5.4vw}}
.ov .sub{{position:absolute;left:6vw;top:23.5vw;font-size:2.6vw;color:#6E6A64}}
.ov .note{{position:absolute;left:6vw;right:6vw;bottom:4.2vw;font-size:2.1vw;color:#6E6A64}}
"""


def page(body, extra=""):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{extra}</style></head><body>{body}</body></html>"


def cut(n):
    return f"file://{os.path.join(HERE, 'cut', n + '.png')}"


def card(p):
    code, th, en, use, pcs = p
    w, h, _, _ = die(code)
    size = f"{w:.0f} × {h:.0f} มม."
    if pcs:
        stage = f'<img class="p0 shot" src="{cut(pcs[0])}" alt="">'
        side = '<div class="side">' + "".join(f'<img class="shot" src="{cut(n)}" alt="">' for n in pcs[1:]) + "</div>"
        note = "ตัดจากเศษหนังวัวแท้ ทุกชิ้นสีไม่ซ้ำ"
    else:
        stage, side = solid(code), ""
        note = "ภาพจากบล็อกตัด · รอรูปจริง"
    body = (f'<div class="c"><div class="top">{logo("square-light")}<span>our patterns</span></div>'
            f'<div class="num">{code}</div>'
            f'<div class="name"><div class="th{" long" if len(th) > 8 else ""}">{th}</div><div class="en">{en}</div></div>'
            f'{side}<div class="stage">{stage}</div>'
            f'<div class="foot">{outline(code)}<div class="meta"><b>แพตเทิร์น {code} · {size}</b>'
            f'<span>ใช้ทำ {use}</span><span class="muted">{note}</span></div></div>{band()}</div>')
    return page(body)


def overview():
    cells = []
    for code, th, en, use, pcs in PATTERNS:
        pic = f'<img src="{cut(pcs[0])}" alt="">' if pcs else solid(code)
        cells.append(f'<div class="cell">{pic}<div class="cap"><b>{code}</b><span>{th}</span></div></div>')
    body = (f'<div class="c ov"><div class="top">{logo("square-light")}<span>our patterns</span></div>'
            f'<h1>แพตเทิร์นของเรา</h1><p class="sub">หนึ่งบล็อกตัด หนึ่งเลข · ชื่อสินค้าคือเลขแพตเทิร์นกับหน้าที่</p>'
            f'<div class="grid">{"".join(cells)}</div>'
            f'<p class="note">ไม่มีเลข 06 · 02 ภาพจากบล็อกตัด รอรูปจริง</p>{band()}</div>')
    return page(body)


def run():
    os.makedirs(os.path.join(HERE, "html"), exist_ok=True)
    jobs = []
    pages = [(f"pattern-{p[0]}", card(p)) for p in PATTERNS] + [("pattern-all", overview())]
    for name, html in pages:
        open(os.path.join(HERE, "html", name + ".html"), "w").write(html)
        jobs.append({"name": name})
    json.dump(jobs, open(os.path.join(HERE, "jobs.json"), "w"), indent=1)
    print(len(jobs), "pages")


if __name__ == "__main__":
    run()
