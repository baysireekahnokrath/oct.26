"""Build giftbox/index.html: a real-leather box for two 55 x 55 x 15 cm pillows, a wedding gift from the owner
to a senior designer (12 Nov 2026).

Design: a rigid lid-and-base box (3 mm greyboard) covered in one colour of leather, quiet outside.
Two ribbons of woven 07 pieces cross on the lid in two colours, one for each of the couple, and meet in one piece
in the middle. The ribbons are glued on and carry no load, so the box does not depend on the untested joints.
07 pieces sit 56.86 mm apart, so a ribbon of 13 pieces runs over the 58 cm lid, down both sides and tucks under the edge.
Inside: lining, a 05 leather tag with the couple's names on the pillows.

Every size comes from the pillow size below; change PILLOW and rebuild once the real pillows are measured.
python3 giftbox/build.py -> giftbox/index.html, giftbox/drawing.svg (print sheet for the box maker)
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import geom

# ---------------------------------------------------------------- sizes, mm
PILLOW = (550, 550, 150); NPILLOW = 2          # owner, 12 Nov: 55 x 55 cm, about 15 cm thick, two of them
EASE_W, EASE_H = 5, 20                          # 5 mm round the sides, 2 cm on top: pillows are soft and puff
BOARD, LEATHER, CLEAR = 3.0, 1.2, 2.0           # greyboard, leather (1.0-1.2), lid-to-base gap each side
LID_H = 80                                      # lid skirt height
TURN = 20                                       # leather folded over the board edge to the inside
P = 2 * 28.43                                   # 07 joint pitch
COST07 = 3.45
SHEET = (787, 1092)                             # greyboard 31 x 43 in

W = PILLOW[0] + 2 * EASE_W                      # inside, 560
H = NPILLOW * PILLOW[2] + EASE_H                # inside height, 320
base_board = W + 2 * BOARD                      # 566: bottom board, long walls
base_out = base_board + 2 * LEATHER             # 568.4
base_h = H + BOARD                              # board height incl. bottom, 323
lid_in = base_out + 2 * CLEAR                   # 572.4
lid_board = lid_in + 2 * BOARD                  # 578.4
lid_out = lid_board + 2 * LEATHER               # 580.8
lid_wall = LID_H - BOARD                        # 77
total_h = base_h + LEATHER + BOARD + LEATHER    # closed: lid top rests on the base walls

# ribbon: from the middle of the lid, over the edge, down the skirt and under its bottom edge
half_path = lid_out / 2 + LID_H + LEATHER       # to the bottom edge of the skirt
N_SIDE = math.ceil((half_path - 45 + 4) / P)    # pieces each side of the centre so the last lobe reaches under the edge
N_BAND = 2 * N_SIDE + 1
N07 = 2 * N_BAND - 1                            # two bands share the centre piece
tuck = N_SIDE * P + 45 - half_path              # how far the last lobe goes under the skirt edge

def outline(code):
    g = geom.load(code); pts = [g["poly"][0]]
    for p in g["poly"][1:]:
        if math.dist(p, pts[-1]) > 0.8: pts.append(p)
    return dict(poly=[[round(x, 2), round(y, 2)] for x, y in pts], cuts=[[[round(c, 2) for c in a], [round(c, 2) for c in b]] for a, b in g["cuts"]])
D07, D05 = outline("07"), outline("05")

# ---------------------------------------------------------------- cut lists
r = lambda v: round(v, 1)
BOARDS = [  # name, w, h, qty
    ("ฝา แผ่นบน", lid_board, lid_board, 1),
    ("ฝา ผนังยาว", lid_board, lid_wall, 2),
    ("ฝา ผนังสั้น", lid_in, lid_wall, 2),
    ("ตัวกล่อง ก้น", base_board, base_board, 1),
    ("ตัวกล่อง ผนังยาว", base_board, H, 2),
    ("ตัวกล่อง ผนังสั้น", W, H, 2),
]
lid_cover = lid_out + 2 * (LID_H + LEATHER + TURN)                 # one cross-shaped piece, corners cut out
lid_notch = LID_H + LEATHER + TURN
wall_cover = (base_out + 15, base_h + LEATHER + TURN + 15)         # 15 mm overlap at the corner and under the bottom
LEATHERS = [
    ("ฝา แบบชิ้นเดียว", lid_cover, lid_cover, 1, f"ตัดมุมออก 4 มุม มุมละ {r(lid_notch)} × {r(lid_notch)}"),
    ("ฝา แบบ 4 ชิ้น", lid_cover / 2, lid_cover / 2, 4, f"ใช้แทนแบบชิ้นเดียวถ้าหนังไม่พอ ต่อกลางฝา ตะเข็บอยู่ใต้ริบบิ้น · ตัดมุมนอก {r(lid_notch)} × {r(lid_notch)}"),
    ("ผนังตัวกล่อง", wall_cover[0], wall_cover[1], 4, "เกยกันที่มุม 15 พับใต้ก้น 15"),
]
area_lid = lid_cover ** 2 - 4 * lid_notch ** 2           # one-piece lid; the 4-piece lid uses about the same
area_wall = 4 * wall_cover[0] * wall_cover[1]
area = (area_lid + area_wall) / 1e6
area_buy = area * 1.15
sqft = area_buy * 10.7639
LINING = [("ก้นด้านใน", W, W, 1), ("ผนังด้านใน", W, H - TURN, 4), ("ใต้ฝา", lid_in, lid_in, 1), ("ใต้ก้น (สักหลาด)", base_board, base_board, 1)]

# greyboard sheets: simple shelf packing, largest first
def pack(items, sw, sh, gap=6):
    sheets = []
    for name, w, h in sorted(items, key=lambda t: -t[1] * t[2]):
        placed = False
        for s in sheets:
            for shelf in s["shelves"]:
                if shelf["h"] >= h and shelf["x"] + w <= sw:
                    s["parts"].append((name, shelf["x"], shelf["y"], w, h)); shelf["x"] += w + gap; placed = True; break
            if placed: break
            if s["y"] + h <= sh and w <= sw:
                s["shelves"].append(dict(y=s["y"], h=h, x=w + gap)); s["parts"].append((name, 0, s["y"], w, h)); s["y"] += h + gap; placed = True; break
        if not placed:
            sheets.append(dict(y=h + gap, shelves=[dict(y=0, h=h, x=w + gap)], parts=[(name, 0, 0, w, h)]))
    return sheets
items = [(n, w, h) for n, w, h, q in BOARDS for _ in range(q)]
SHEETS = pack(items, *SHEET)

# ---------------------------------------------------------------- drawings (SVG, mm)
E = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;")
def dpath(d, cx, cy, rot, scale=1.0):
    c, s = math.cos(rot), math.sin(rot)
    pts = [(cx + (x * c - y * s) * scale, cy - (x * s + y * c) * scale) for x, y in d["poly"]]
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
def dim(x1, y1, x2, y2, text, off=0, vertical=False):
    if vertical:
        x = x1 + off
        return (f'<g class="dim"><line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}"/><line x1="{x - 6}" y1="{y1}" x2="{x + 6}" y2="{y1}"/>'
                f'<line x1="{x - 6}" y1="{y2}" x2="{x + 6}" y2="{y2}"/><text x="{x - 8}" y="{(y1 + y2) / 2}" transform="rotate(-90 {x - 8} {(y1 + y2) / 2})" text-anchor="middle">{text}</text></g>')
    y = y1 + off
    return (f'<g class="dim"><line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/><line x1="{x1}" y1="{y - 6}" x2="{x1}" y2="{y + 6}"/>'
            f'<line x1="{x2}" y1="{y - 6}" x2="{x2}" y2="{y + 6}"/><text x="{(x1 + x2) / 2}" y="{y - 8}" text-anchor="middle">{text}</text></g>')
cm = lambda v: f"{v / 10:.1f}".rstrip("0").rstrip(".") + " ซม."

def ribbon_net():
    """lid seen from above with the skirt folded out flat; dashed = fold lines; the ribbons laid on it"""
    half = lid_out / 2; sk = LID_H + LEATHER; R = half + sk + 40
    s = [f'<svg class="dwg" viewBox="{-R} {-R} {2 * R} {2 * R}" role="img" aria-label="ริบบิ้น 07 บนฝา มองจากบน คลี่ขอบฝาออก">']
    s.append(f'<path class="skirt" d="M{-half},{-half - sk}H{half}V{-half}H{half + sk}V{half}H{half}V{half + sk}H{-half}V{half}H{-half - sk}V{-half}H{-half}Z"/>')
    s.append(f'<rect class="lidtop" x="{-half}" y="{-half}" width="{2 * half}" height="{2 * half}"/>')
    for k in range(-N_SIDE, N_SIDE + 1):
        for band in (0, 1):
            if band == 1 and k == 0: continue
            x, y = (k * P, 0) if band == 0 else (0, k * P)
            rot = math.pi / 2 if abs(k) % 2 else 0
            cls = "pc-c" if k == 0 else ("pc-a" if band == 0 else "pc-b")
            s.append(f'<path class="{cls}" d="{dpath(D07, x, y, rot)}"/>')
            c, sn = math.cos(rot), math.sin(rot)
            for a, b in D07["cuts"]:
                ax, ay = a[0] * c - a[1] * sn, a[0] * sn + a[1] * c; bx, by = b[0] * c - b[1] * sn, b[0] * sn + b[1] * c
                s.append(f'<line class="cut" x1="{x + ax:.1f}" y1="{-(y + ay):.1f}" x2="{x + bx:.1f}" y2="{-(y + by):.1f}"/>')
    s.append(f'<rect class="fold" x="{-half}" y="{-half}" width="{2 * half}" height="{2 * half}"/>')
    s.append(f'<rect class="fold" x="{-half - sk}" y="{-half - sk}" width="{2 * (half + sk)}" height="{2 * (half + sk)}"/>')
    s.append(dim(-half, -half - sk - 10, half, -half - sk - 10, f"ฝา {cm(lid_out)}"))
    s.append(f'<text class="lbl" x="{half + sk / 2}" y="{-half - sk / 2}" text-anchor="middle">ขอบฝา {cm(sk)}</text>')
    s.append('</svg>')
    return "".join(s)

def elevation():
    """front view, closed, with sizes; pillows drawn dashed inside"""
    w0, h0 = lid_out, total_h; pad = 90
    x0 = -w0 / 2; base_x = -base_out / 2
    s = [f'<svg class="dwg" viewBox="{x0 - pad} {-h0 - 60} {w0 + 2 * pad} {h0 + 120}" role="img" aria-label="ด้านหน้า ขนาดกล่อง">']
    s.append(f'<rect class="box" x="{base_x}" y="{-(base_h + LEATHER)}" width="{base_out}" height="{base_h + LEATHER}"/>')
    s.append(f'<rect class="lid" x="{x0}" y="{-h0}" width="{w0}" height="{LID_H + LEATHER}"/>')
    for i in range(NPILLOW):
        y = -(BOARD + LEATHER + (i + 1) * PILLOW[2])
        s.append(f'<rect class="pillow" x="{-PILLOW[0] / 2}" y="{y}" width="{PILLOW[0]}" height="{PILLOW[2]}" rx="40"/>')
    s.append(f'<rect class="rib" x="-45" y="{-h0 - 2.4}" width="90" height="{LID_H + 4}"/>')
    s.append(dim(x0, -h0 - 18, -x0, -h0 - 18, f"ฝา {cm(lid_out)}"))
    s.append(dim(base_x, 30, -base_x, 30, f"ตัวกล่อง {cm(base_out)}"))
    s.append(dim(-x0 + 30, -h0, -x0 + 30, 0, f"สูงรวม {cm(total_h)}", vertical=True))
    s.append(dim(x0 - 34, -h0, x0 - 34, -h0 + LID_H + LEATHER, f"ฝา {cm(LID_H)}", vertical=True))
    s.append(f'<text class="lbl" x="0" y="{-(BOARD + PILLOW[2] / 2)}" text-anchor="middle">หมอน {PILLOW[0] // 10}×{PILLOW[1] // 10}×{PILLOW[2] // 10} × {NPILLOW}</text>')
    s.append('</svg>')
    return "".join(s)

def sheets_svg():
    out = []
    for i, sh in enumerate(SHEETS):
        s = [f'<svg class="dwg sheet" viewBox="-20 -20 {SHEET[0] + 40} {SHEET[1] + 60}" role="img" aria-label="แผ่นจั่วปัง {i + 1}">',
             f'<rect class="sheetbg" x="0" y="0" width="{SHEET[0]}" height="{SHEET[1]}"/>']
        for name, x, y, w, h in sh["parts"]:
            s.append(f'<rect class="part" x="{x}" y="{y}" width="{w}" height="{h}"/>')
            fs = 26 if min(w, h) > 120 else 20
            s.append(f'<text class="plbl" x="{x + w / 2}" y="{y + h / 2 - (14 if h > 120 else 0)}" text-anchor="middle" font-size="{fs}">{E(name)}</text>')
            s.append(f'<text class="pdim" x="{x + w / 2}" y="{y + h / 2 + (22 if h > 120 else 20)}" text-anchor="middle" font-size="{fs}">{r(w)} × {r(h)}</text>')
        s.append(f'<text class="lbl" x="0" y="{SHEET[1] + 34}" font-size="26">แผ่น {i + 1} · 787 × 1092 มม. (31 × 43 นิ้ว)</text></svg>')
        out.append("".join(s))
    return out

def lid_leather_svg():
    L = lid_cover; n = lid_notch; pad = 60
    s = [f'<svg class="dwg" viewBox="{-pad} {-pad} {L + 2 * pad} {L + 2 * pad}" role="img" aria-label="หนังหุ้มฝา">',
         f'<path class="hide" d="M{n},0H{L - n}V{n}H{L}V{L - n}H{L - n}V{L}H{n}V{L - n}H0V{n}H{n}Z"/>',
         f'<rect class="fold" x="{n}" y="{n}" width="{L - 2 * n}" height="{L - 2 * n}"/>',
         f'<rect class="fold" x="{TURN}" y="{TURN}" width="{L - 2 * TURN}" height="{L - 2 * TURN}"/>',
         f'<line class="seam" x1="{L / 2}" y1="0" x2="{L / 2}" y2="{L}"/><line class="seam" x1="0" y1="{L / 2}" x2="{L}" y2="{L / 2}"/>',
         dim(0, -24, L, -24, cm(L)), dim(L - n, L + 30, L, L + 30, cm(n)),
         f'<text class="lbl" x="{L / 2}" y="{L / 2 - 20}" text-anchor="middle" font-size="30">บนฝา {cm(lid_out)}</text>',
         f'<text class="lbl" x="{L / 2}" y="{L / 2 + 26}" text-anchor="middle" font-size="22">เส้นจุด = ถ้าต่อ 4 ชิ้น ตะเข็บอยู่ใต้ริบบิ้น</text>',
         '</svg>']
    return "".join(s)

# ---------------------------------------------------------------- page data
DATA = dict(d07=D07, d05=D05, P=P, nside=N_SIDE, lid_out=lid_out, lid_h=LID_H + LEATHER, base_out=base_out, base_h=base_h + LEATHER,
            wall=BOARD + LEATHER, pillow=PILLOW, npillow=NPILLOW, total_h=total_h, inner=W, inner_h=H)
board_rows = "".join(f'<tr><td>{E(n)}</td><td class="num">{r(w)} × {r(h)}</td><td class="num">{q}</td></tr>' for n, w, h, q in BOARDS)
leather_rows = "".join(f'<tr><td>{E(n)}</td><td class="num">{r(w)} × {r(h)}</td><td class="num">{q}</td><td>{E(note)}</td></tr>' for n, w, h, q, note in LEATHERS)
lining_rows = "".join(f'<tr><td>{E(n)}</td><td class="num">{r(w)} × {r(h)}</td><td class="num">{q}</td></tr>' for n, w, h, q in LINING)
SUB = {
    "__DATA__": json.dumps(DATA, separators=(",", ":"), ensure_ascii=False),
    "__INNER__": f"{W / 10:g} × {W / 10:g} × {H / 10:g}", "__OUTER__": f"{lid_out / 10:.1f} × {lid_out / 10:.1f} × {total_h / 10:.1f}",
    "__N07__": str(N07), "__NBAND__": str(N_BAND), "__NSIDE__": str(N_SIDE), "__TUCK__": f"{tuck / 10:.1f}",
    "__COST07__": f"{N07 * COST07:.0f}", "__AREA__": f"{area_buy:.2f}", "__SQFT__": f"{sqft:.0f}", "__NSHEET__": str(len(SHEETS)),
    "__BOARDROWS__": board_rows, "__LEATHERROWS__": leather_rows, "__LININGROWS__": lining_rows,
    "__NET__": ribbon_net(), "__ELEV__": elevation(), "__SHEETS__": "".join(sheets_svg()), "__LIDLEATHER__": lid_leather_svg(),
    "__PITCH__": f"{P:.2f}", "__LIDCM__": f"{lid_out / 10:.1f}",
}
PAGE = open(os.path.join(HERE, "template.html")).read()
for k, v in SUB.items(): PAGE = PAGE.replace(k, v)
open(os.path.join(HERE, "index.html"), "w").write(PAGE)

# print sheet for the box maker: drawings + cut lists on one tall SVG page
style = ('<style>text{font-family:"IBM Plex Sans Thai","Noto Sans Thai",sans-serif;fill:#2A2725}.dim line{stroke:#2A2725;stroke-width:1.5}'
         '.dim text{font-size:22px}.lbl{font-size:22px;fill:#5E5953}.box,.lid,.lidtop,.skirt,.hide{fill:#efe6d8;stroke:#2A2725;stroke-width:2}'
         '.pillow{fill:none;stroke:#8C8A85;stroke-width:2;stroke-dasharray:10 8}.rib{fill:#B07A4A;opacity:.6}.fold{fill:none;stroke:#5E7A3A;stroke-width:2;stroke-dasharray:10 7}'
         '.seam{stroke:#A9442B;stroke-width:2;stroke-dasharray:3 6}.pc-a{fill:#E8DCC6;stroke:#2A2725;stroke-width:1}.pc-b{fill:#8B5E3C;stroke:#2A2725;stroke-width:1}'
         '.pc-c{fill:#B07A4A;stroke:#2A2725;stroke-width:1}.cut{stroke:#2A2725;stroke-width:1.6}.sheetbg{fill:#f7f3ec;stroke:#2A2725;stroke-width:2}'
         '.part{fill:#e4dccd;stroke:#2A2725;stroke-width:2}.plbl,.pdim{fill:#2A2725}</style>')
parts = [elevation(), ribbon_net(), lid_leather_svg()] + sheets_svg()
y = 0; body = []
for p in parts:
    vb = [float(v) for v in p.split('viewBox="')[1].split('"')[0].split()]
    w = 900; h = w * vb[3] / vb[2]
    body.append(p.replace('<svg class="dwg', f'<svg x="50" y="{y + 80}" width="{w}" height="{h:.0f}" class="dwg', 1)); y += h + 60
head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{y + 120:.0f}" viewBox="0 0 1000 {y + 120:.0f}">{style}'
        f'<rect width="1000" height="{y + 120:.0f}" fill="#fff"/><text x="50" y="50" font-size="30">OCT. 26 · กล่องหนังใส่หมอน 2 ใบ · แบบสำหรับช่าง · หน่วย มม.</text>')
open(os.path.join(HERE, "drawing.svg"), "w").write(head + "".join(body) + "</svg>")
print("giftbox/index.html", len(PAGE), "bytes · outer", r(lid_out), "x", r(total_h), "· 07", N07, f"({N_BAND}/band, tuck {tuck:.1f} mm)",
      f"· leather {area_buy:.2f} m2 = {sqft:.1f} sqft · sheets {len(SHEETS)}")
