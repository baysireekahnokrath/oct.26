"""LINE rich menu, large 2500 x 1686, six equal areas (LINE OA Manager template "large, 6"), Brand Book v2 (owner, 23 Oct).

A oct26brand.com · B ของพร้อมส่ง (#shop) · C ถามเรา (text) / D Instagram · E Facebook · F YouTube.
Cotton ground, charcoal text, pattern shapes in hide, the family band as a thin line at the bottom.
python3 line-20261023/richmenu.py && node line-20261023/richmenu.mjs -> richmenu.png, richmenu.jpg (under 1 MB)
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "print-20261022", "assets"))
from palette import C, BAND

FONTS = "file://" + os.path.join(REPO, "brand-20261014", "fonts")
INK, MUTED, LINE = C["charcoal"], "#6E6A64", "#DCD4C7"
W, H = 2500, 1686
CW, CH = (833, 834, 833), 843                         # LINE's own split of the six areas
AREAS = [  # (letter, label, sub, action type, action)
    ("A", "เว็บไซต์", "oct26brand.com", "ลิงก์", "https://oct26brand.com/"),
    ("B", "ของพร้อมส่ง", "ดูสินค้าทั้งหมด", "ลิงก์", "https://oct26brand.com/#shop"),
    ("C", "ถามเรา", "สั่งซื้อ · สอบถาม", "ข้อความ", "สอบถามสินค้า"),
    ("D", "Instagram", "@oct.26_brand", "ลิงก์", "https://www.instagram.com/oct.26_brand/"),
    ("E", "Facebook", "oct26brand", "ลิงก์", "https://www.facebook.com/oct26brand"),
    ("F", "YouTube", "@OCT.26_brand", "ลิงก์", "https://www.youtube.com/@OCT.26_brand"),
]


def _svg(name, px):
    s = open(os.path.join(HERE, "assets", name + ".svg")).read()
    s = re.sub(r'(<svg[^>]*?) width="[^"]*" height="[^"]*"', r"\1", s, count=1)
    return f'<div style="width:{px}px;flex:none">{s.replace("<svg ", "<svg style=" + chr(39) + "width:100%;height:auto;display:block" + chr(39) + " ", 1)}</div>'


ST = f'fill="none" stroke="{INK}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"'
ICON = {  # simple line glyphs, one colour, 260 px box
    "A": _svg("square-dark", 250),
    "B": '<div style="display:flex;gap:22px;align-items:center">' + _svg("pattern-01-solid", 118) + _svg("pattern-04-solid", 108) + _svg("pattern-05-solid", 108) + "</div>",
    "C": f'<svg viewBox="0 0 260 260" width="250"><path d="M40 60 h180 a20 20 0 0 1 20 20 v100 a20 20 0 0 1 -20 20 h-110 l-50 40 v-40 h-20 a20 20 0 0 1 -20 -20 v-100 a20 20 0 0 1 20 -20 z" {ST}/>'
         f'<circle cx="90" cy="130" r="11" fill="{INK}"/><circle cx="130" cy="130" r="11" fill="{INK}"/><circle cx="170" cy="130" r="11" fill="{INK}"/></svg>',
    "D": f'<svg viewBox="0 0 260 260" width="250"><rect x="35" y="35" width="190" height="190" rx="54" {ST}/><circle cx="130" cy="130" r="46" {ST}/><circle cx="182" cy="78" r="11" fill="{INK}"/></svg>',
    "E": f'<svg viewBox="0 0 260 260" width="250"><circle cx="130" cy="130" r="96" {ST}/><path d="M146 226 v-118 a26 26 0 0 1 26 -26 h18 M112 140 h66" {ST}/></svg>',
    "F": f'<svg viewBox="0 0 260 260" width="250"><rect x="25" y="62" width="210" height="136" rx="40" {ST}/><path d="M112 98 l52 32 l-52 32 z" fill="{INK}"/></svg>',
}


def page():
    cells, y = [], 0
    for r in range(2):
        x = 0
        for c in range(3):
            k, label, sub, *_ = AREAS[r * 3 + c]
            cells.append(f'<div class="cell" style="left:{x}px;top:{y}px;width:{CW[c]}px;height:{CH}px">'
                         f'<div class="ic">{ICON[k]}</div><div class="lb{" en" if label.isascii() else ""}">{label}</div><div class="sb">{sub}</div></div>')
            x += CW[c]
        y += CH
    lines = (f'<div style="position:absolute;left:0;right:0;top:{CH - 1}px;height:3px;background:{LINE}"></div>'
             + "".join(f'<div style="position:absolute;top:60px;bottom:80px;left:{x - 1}px;width:3px;background:{LINE}"></div>'
                       for x in (CW[0], CW[0] + CW[1])))
    band = '<div style="position:absolute;left:0;right:0;bottom:0;height:22px;display:flex">' + "".join(
        f'<span style="flex:1;background:{h}"></span>' for h in BAND) + "</div>"
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>
@font-face{{font-family:Anuphan;font-weight:500;src:url({FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Jost;font-weight:400;src:url({FONTS}/alt/Jost-Regular.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url({FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Plex;font-weight:400;src:url({FONTS}/IBMPlexSansThai-Regular.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;position:relative;background:{C['cotton']};color:{INK};overflow:hidden}}
.cell{{position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px}}
.ic{{height:260px;display:flex;align-items:center;justify-content:center}}
.lb{{font-family:Anuphan,Jost;font-weight:500;font-size:92px;line-height:1.1}}
.lb.en{{font-family:Jost;font-size:96px}}
.sb{{font-family:Jost,Plex;font-size:50px;color:{MUTED};margin-top:-14px}}
</style></head><body>{''.join(cells)}{lines}{band}</body></html>"""


if __name__ == "__main__":
    open(os.path.join(HERE, "richmenu.html"), "w").write(page())
    print("wrote richmenu.html")
