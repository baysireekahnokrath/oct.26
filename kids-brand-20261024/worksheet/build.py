"""Character worksheet for Beiya, Beana and Bene (24 Oct 2026). A4 portrait, print at 100%.

p1      pick a shape: all six patterns side by side
p2-p7   one page per pattern: the real outline at 1:1 (9 cm, 01 is 10.4) to colour or trace, colours to choose,
        and lines for name, personality, likes and best friend
p8      the family sheet: each child's final name, colour and pattern, for a parent to fill in and photograph

python3 worksheet/build.py -> worksheet/worksheet.html;  node worksheet/render.cjs -> worksheet/OCT26-kids-character-worksheet-A4.pdf
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIDS = os.path.dirname(HERE)
sys.path.insert(0, KIDS)
from kit import PATTERNS, CHARS, shape_svg, INK, PAPER  # noqa: E402

FONTS = os.path.join(KIDS, "fonts")
PLEX = os.path.join(os.path.dirname(KIDS), "brand-20261014", "fonts", "IBMPlexSansThai-Regular.ttf")
JOST = os.path.join(os.path.dirname(KIDS), "brand-20261014", "fonts", "alt", "Jost-Medium.ttf")
FAMILY = [("#A9442B", "แดงดินลูกรัง"), ("#5E7A3A", "เขียวใบตอง"), ("#E9A825", "เหลืองทานตะวัน"),
          ("#B9A3D6", "ม่วงดอกอินทนิล"), ("#2E4A7D", "น้ำเงินคราม")]
ORDER = ["01", "02", "03", "04", "05", "07"]

CSS = f"""
@font-face{{font-family:Mali;font-weight:700;src:url(file://{FONTS}/Mali-Bold.ttf)}}
@font-face{{font-family:Mali;font-weight:500;src:url(file://{FONTS}/Mali-Medium.ttf)}}
@font-face{{font-family:Plex;src:url(file://{PLEX})}}
@font-face{{font-family:Jost;font-weight:500;src:url(file://{JOST})}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}} html,body{{margin:0}}
body{{font-family:Mali,Plex,sans-serif;color:{INK};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;position:relative;overflow:hidden;background:#fff;page-break-after:always;padding:14mm 14mm 16mm}}
.pg:last-child{{page-break-after:auto}}
.hd{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:.6mm solid {INK};padding-bottom:2.5mm}}
.hd b{{font-weight:700;font-size:8.5mm;line-height:1.1}}
.hd span{{font-family:Jost;font-size:3.4mm;letter-spacing:.12em;color:#6E6A64}}
.sub{{font-family:Plex;font-size:3.6mm;color:#6E6A64;margin:3mm 0 0}}
.band{{position:absolute;left:0;right:0;bottom:0;height:4mm;display:flex}} .band i{{flex:1}}
.foot{{position:absolute;left:14mm;right:14mm;bottom:7mm;font-family:Plex;font-size:2.8mm;color:#6E6A64;display:flex;justify-content:space-between}}
/* p1 */
.grid6{{display:grid;grid-template-columns:repeat(3,1fr);gap:8mm 6mm;margin-top:10mm}}
.cell{{display:grid;justify-items:center;gap:2mm}}
.cell svg{{width:50mm;height:50mm}}
.cell .no{{font-family:Jost;font-size:6mm}}
.cell .nm{{font-size:4.6mm}}
.cell .tick{{width:7mm;height:7mm;border:.5mm solid {INK};border-radius:50%}}
.who{{margin-top:12mm;display:grid;gap:5mm;font-size:5mm}}
.who div{{display:flex;gap:4mm;align-items:flex-end}} .who u{{flex:1;border-bottom:.4mm dashed {INK};height:7mm;text-decoration:none}}
/* p2-7 */
.top{{display:grid;gap:8mm;margin-top:7mm;align-items:start}}
.real svg{{display:block}}
.real p{{font-family:Plex;font-size:3mm;color:#6E6A64;margin:2mm 0 0}}
.colors{{display:grid;gap:3mm}}
.colors h3,.lines h3,.box h3{{font-weight:700;font-size:5mm;margin:0}}
.dots{{display:grid;grid-template-columns:repeat(4,1fr);gap:2.5mm 2mm}}
.dot{{display:grid;justify-items:center;gap:1mm;font-family:Plex;font-size:2.5mm;text-align:center;line-height:1.2}}
.dot i{{width:11mm;height:11mm;border-radius:50%;display:block;border:.4mm solid {INK}}}
.dot i.blank{{background:#fff;border-style:dashed}}
.lines{{margin-top:6mm;display:grid;gap:3.6mm}}
.ln{{display:flex;gap:3mm;align-items:flex-end;font-size:4.4mm}}
.ln span{{white-space:nowrap}}
.ln u{{flex:1;border-bottom:.35mm dashed {INK};height:6.5mm;text-decoration:none}}
.box{{position:absolute;left:14mm;right:14mm;bottom:16mm;border:.5mm solid {INK};border-radius:4mm;padding:3mm 4mm}}
.box p{{font-family:Plex;font-size:3.2mm;color:#6E6A64;margin:1mm 0 0}}
/* p8 */
table{{width:100%;border-collapse:collapse;margin-top:8mm;font-size:4.4mm}}
th,td{{border:.4mm solid {INK};padding:3mm;text-align:left;vertical-align:top}}
th{{background:#F4F0E8;font-weight:700}}
td{{height:30mm}}
.kid{{font-family:Jost;font-size:5mm}}
.ck{{display:inline-flex;gap:2mm;align-items:center;font-size:3.6mm;margin-top:2mm}} .ck i{{width:4.5mm;height:4.5mm;border:.4mm solid {INK};display:inline-block}}
.rules{{margin-top:8mm;font-family:Plex;font-size:3.5mm;line-height:1.6}}
.rules li{{margin-bottom:1mm}}
"""


def band():
    return '<div class="band">' + "".join(f'<i style="background:{c}"></i>' for c, _ in FAMILY) + "</div>"


def foot(n):
    return f'<div class="foot"><span>แบรนด์ของเด็ก ๆ (ชื่อยังไม่ตัดสิน) · ลูก ๆ ของ OCT. 26</span><span>{n}/8</span></div>'


def outline(code, mm, stroke=0.6):
    p = PATTERNS[code]
    s = mm / max(p["w"], p["h"])
    return (f'<svg width="{p["w"] * s:.1f}mm" height="{p["h"] * s:.1f}mm" viewBox="-1 -1 {p["w"] + 2} {p["h"] + 2}">'
            f'{shape_svg(code, "none", INK, INK, stroke)}</svg>')


def p_choose():
    cells = "".join(f'<div class="cell">{outline(c, 46, .9)}<span class="no">{c}</span><span class="nm">{PATTERNS[c]["th"]}</span>'
                    f'<i class="tick"></i></div>' for c in ORDER)
    return (f'<section class="pg"><div class="hd"><b>เลือกรูปร่างของฉัน</b><span>MY SHAPE</span></div>'
            f'<p class="sub">รูปทั้งหมดคือชิ้นหนังจริงที่บ้านเราตัด วงกลมรูปที่ชอบที่สุด แล้วไปต่อหน้าของรูปนั้น (หน้า 2–7) ไม่มีเลข 06</p>'
            f'<div class="grid6">{cells}</div>'
            f'<div class="who"><div><span>ฉันชื่อ</span><u></u></div><div><span>รูปที่ฉันเลือกคือเลข</span><u></u><span>เพราะ</span><u></u></div></div>'
            f'{foot(1)}{band()}</section>')


def p_pattern(code, n):
    p = PATTERNS[code]
    w = p["w"]  # 1:1 at true size
    dots = "".join(f'<div class="dot"><i style="background:{c}"></i>{nm}</div>' for c, nm in FAMILY)
    dots += '<div class="dot"><i class="blank"></i>สีอื่นที่ชอบ</div>' * 3
    lines = "".join(f'<div class="ln"><span>{t}</span><u></u></div>' for t in
                    ["ชื่อตัวละคร", "เป็นตัวแทนของ (ชื่อฉัน)", "สีของตัวละคร", "นิสัย 1", "นิสัย 2", "นิสัย 3",
                     "ชอบ", "ไม่ชอบ", "ของประจำตัว", "เพื่อนรัก"])
    top = (f'<div class="top" style="grid-template-columns:{w + 2:.0f}mm 1fr"><div class="real">{outline(code, max(p["w"], p["h"]), .6)}'
           f'<p>ขนาดจริง {p["w"]:.0f} × {p["h"]:.0f} มม. เท่าชิ้นหนัง วาดหน้า ลงสี หรือตัดไปทาบได้</p></div>'
           f'<div class="colors"><h3>เลือกสีของฉัน</h3><div class="dots">{dots}</div></div></div>')
    return (f'<section class="pg"><div class="hd"><b>ตัวละครของฉัน · {code} {p["th"]}</b><span>PATTERN {code}</span></div>'
            f'{top}<div class="lines">{lines}</div>'
            f'<div class="box" style="top:{14 + 12 + 7 + max(p["h"], 90) + 9 + 10 * 10.2 + 6:.0f}mm"><h3>ตัวละครของฉันกำลังทำอะไรอยู่</h3><p>วาดรูปให้ดู</p></div>'
            f'{foot(n)}{band()}</section>')


def p_family():
    rows = "".join(f'<tr><td><span class="kid">{c["kid"]}</span></td><td></td><td></td><td></td>'
                   f'<td><span class="ck"><i></i>ตกลง</span></td></tr>' for c in CHARS["characters"])
    return (f'<section class="pg"><div class="hd"><b>ตัวละครของบ้านเรา</b><span>FAMILY SHEET</span></div>'
            f'<p class="sub">พ่อหรือแม่กรอกหลังเด็ก ๆ เลือกเสร็จ แล้วถ่ายรูปหน้านี้ส่งมา พร้อมรูปหน้าที่เด็ก ๆ วาด</p>'
            f'<table><tr><th style="width:20%">ใคร</th><th>ชื่อตัวละคร</th><th style="width:18%">สี</th><th style="width:16%">เลขแพตเทิร์น</th><th style="width:14%">ตกลงแล้ว</th></tr>{rows}</table>'
            f'<p class="sub" style="margin-top:8mm">ชื่อแบรนด์ที่เด็ก ๆ ชอบ (เลือก 1 หรือคิดใหม่)</p>'
            f'<div class="who" style="margin-top:3mm"><div><span class="ck"><i></i>บีสาม B3</span><span class="ck"><i></i>Little OCT.</span><span class="ck"><i></i>ชิ้นเล็ก</span><span>ชื่ออื่น</span><u></u></div></div>'
            f'<ul class="rules"><li>รูปวาดของเด็กใช้เป็นต้นแบบตัวละคร ไม่ใช้รูปหน้าจริงของลูกในแบรนด์</li>'
            f'<li>สองคนเลือกรูปร่างหรือสีซ้ำกันได้ แต่จะจำยากขึ้น ถ้าซ้ำ ลองให้ต่างกันที่อีกอย่าง</li>'
            f'<li>01 หมี: ถ้าเลือก ต้องให้พ่อเบตัดสินก่อน เพราะตอนนี้ห้ามใส่หน้าหมีในงานของ OCT. 26</li></ul>'
            f'{foot(8)}{band()}</section>')


if __name__ == "__main__":
    pages = [p_choose()] + [p_pattern(c, i + 2) for i, c in enumerate(ORDER)] + [p_family()]
    html = f"<!doctype html><html lang='th'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
    open(os.path.join(HERE, "worksheet.html"), "w", encoding="utf-8").write(html)
    print(len(pages), "pages")
