"""Fabric cover for the booth pallet tables: pattern sheets for the tailor (Thai), 3 pages A4 landscape.

Table 117 x 80 x 50 cm (owner's drawing, 22 Oct 2026). The cover hides the top, the front (117 side) and both
80 cm sides; the back stays open for storage. Fabric 120 cm wide.

python3 build.py  -> pattern.html, then node render.cjs -> table-cover-pattern.pdf + preview PNGs
"""
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "brand-20261014", "fonts")

# ---------------------------------------------------------------- numbers (cm)
TABLE_L, TABLE_D, TABLE_H = 117, 80, 50          # front length, side depth, height
EASE = 2                                          # added to length and depth so the cover slips on
FLOOR_GAP = 2                                     # skirt stops this far above the floor
SEAM = 1.5                                        # seam allowance on joined edges
HEM_BOTTOM = 4                                    # bottom hem, folded 2 + 2
HEM_BACK = 2                                      # back edges, folded 1 + 1
FABRIC_W = 120

L = TABLE_L + EASE                                # finished top length 119
D = TABLE_D + EASE                                # finished top depth 82
DROP = TABLE_H - FLOOR_GAP                        # finished skirt height 48

TOP_CUT = (L + 2 * SEAM, D + SEAM + HEM_BACK)     # 122 x 85.5
SKIRT_LEN = HEM_BACK + D + L + D + HEM_BACK       # 287, one strip wraps side-front-side
SKIRT_H = SEAM + DROP + HEM_BOTTOM                # 53.5
NOTCH = (HEM_BACK + D, HEM_BACK + D + L)          # corner marks on the skirt, from the left end

BAND = 2 * TOP_CUT[0] + SKIRT_LEN                 # fabric for two covers: 2 tops + 2 skirts side by side
WASTE = 1.05                                      # 5% for shrinkage and cutting
def metres(n):
    raw = n * TOP_CUT[0] + math.ceil(n / 2) * SKIRT_LEN
    return raw / 100, math.ceil(raw * WASTE / 100)

assert SKIRT_H * 2 <= FABRIC_W - 6 and TOP_CUT[1] <= FABRIC_W - 6

def f(x):
    return f"{x:g}"

# ---------------------------------------------------------------- drawings
INK, MUTED, FILL, FILL2, ACC = "#1C1B22", "#6E6660", "#EFE6DA", "#E2D3BF", "#C8442A"

def iso_sketch():
    """Front (y = D) and right side (x = L) face the viewer; the back (y = 0) is the open side."""
    s, c30, s30 = 1.55, math.cos(math.radians(30)), math.sin(math.radians(30))
    def P(x, y, z):
        return ((x - y) * c30 * s, (x + y) * s30 * s - z * s)
    H, Z0 = TABLE_H, FLOOR_GAP
    faces = [
        ([(0, 0, H), (0, 0, Z0), (0, D, Z0), (0, D, H)], "none", MUTED, True),      # left side, hidden
        ([(0, 0, H), (L, 0, H), (L, 0, Z0), (0, 0, Z0)], "none", ACC, True),        # back: open
        ([(0, D, H), (L, D, H), (L, D, Z0), (0, D, Z0)], FILL, INK, False),          # front
        ([(L, 0, H), (L, D, H), (L, D, Z0), (L, 0, Z0)], FILL2, INK, False),         # right side
        ([(0, 0, H), (L, 0, H), (L, D, H), (0, D, H)], "#F7F1E8", INK, False),      # top
    ]
    pts = [P(*p) for fc in faces for p in fc[0]]
    minx, maxx = min(p[0] for p in pts) - 90, max(p[0] for p in pts) + 90
    miny, maxy = min(p[1] for p in pts) - 50, max(p[1] for p in pts) + 50
    out = []
    for poly, fill, stroke, dash in faces:
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in (P(*p) for p in poly))
        out.append(f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="1.6" stroke-linejoin="round"'
                   + (' stroke-dasharray="6 5"' if dash else '') + '/>')
    def label(x, y, z, t, anchor="middle", color=INK, size=15, weight=600, dy=0):
        a, b = P(x, y, z)
        return f'<text x="{a:.1f}" y="{b + dy:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{t}</text>'
    out += [label(L / 2, D / 2, H, "บน"), label(L / 2, D, H / 2, "หน้า"), label(L, D / 2, H / 2, "ข้าง"),
            label(L / 2, 0, H, "ด้านหลังเปิด เก็บของได้", color=ACC, size=14, dy=-26),
            label(L / 2, D, Z0, f"ยาว {f(L)}", size=13, weight=400, anchor="end", dy=26),
            label(L, D / 2, Z0, f"ลึก {f(D)}", size=13, weight=400, anchor="start", dy=26),
            label(0, D, H / 2, f"สูง {f(DROP)}", anchor="end", size=13, weight=400, dy=0)]
    return f'<svg viewBox="{minx:.0f} {miny:.0f} {maxx - minx:.0f} {maxy - miny:.0f}" class="iso">{"".join(out)}</svg>'

def piece_top():
    w, h = TOP_CUT
    sc = 4.2
    W, Hh = w * sc, h * sc
    x0, y0 = 70, 40
    st = f'stroke="{INK}" stroke-width="1.6"'
    g = [f'<rect x="{x0}" y="{y0}" width="{W:.1f}" height="{Hh:.1f}" fill="{FILL}" {st}/>']
    # stitch line: seams on left, right and front (bottom in drawing); back (top in drawing) is a hem
    sx, sy = x0 + SEAM * sc, y0 + HEM_BACK * sc
    g.append(f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{(w - 2 * SEAM) * sc:.1f}" height="{(h - SEAM - HEM_BACK) * sc:.1f}" fill="none" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="7 5"/>')
    for cx in (sx, x0 + W - SEAM * sc):                                   # front corner dots
        g.append(f'<circle cx="{cx:.1f}" cy="{y0 + Hh - SEAM * sc:.1f}" r="4" fill="{ACC}"/>')
    g += [f'<text x="{x0 + W / 2:.1f}" y="{y0 + Hh / 2 - 6:.1f}" text-anchor="middle" font-size="22" font-weight="600">ชิ้นบน · ตัด 1 ชิ้นต่อโต๊ะ</text>',
          f'<text x="{x0 + W / 2:.1f}" y="{y0 + Hh / 2 + 22:.1f}" text-anchor="middle" font-size="15" fill="{MUTED}">สำเร็จ {f(L)} × {f(D)} ซม.</text>',
          grain(x0 + W / 2 - 110, y0 + Hh / 2 + 52, 220),
          f'<text x="{x0 + W / 2:.1f}" y="{y0 - 10:.1f}" text-anchor="middle" font-size="13">ขอบหลัง: พับริม 1 + 1 ซม.</text>',
          f'<text x="{x0 + W / 2:.1f}" y="{y0 + Hh + 20:.1f}" text-anchor="middle" font-size="13">ขอบหน้า: เย็บติดผ้ากระโปรง กันเย็บ {f(SEAM)}</text>',
          f'<text x="{x0 - 10:.1f}" y="{y0 + Hh / 2:.1f}" text-anchor="middle" font-size="13" transform="rotate(-90 {x0 - 10:.1f} {y0 + Hh / 2:.1f})">ขอบข้าง: เย็บติดผ้ากระโปรง กันเย็บ {f(SEAM)}</text>',
          dim(x0, y0 + Hh + 42, x0 + W, y0 + Hh + 42, f"ตัด {f(w)} ซม."),
          dim(x0 + W + 34, y0, x0 + W + 34, y0 + Hh, f"ตัด {f(h)} ซม.", vertical=True)]
    return f'<svg viewBox="0 0 {x0 + W + 90:.0f} {y0 + Hh + 70:.0f}" class="piece">{"".join(g)}</svg>'

def piece_skirt():
    w, h = SKIRT_LEN, SKIRT_H
    sc = 3.25
    W, Hh = w * sc, h * sc
    x0, y0 = 30, 46
    st = f'stroke="{INK}" stroke-width="1.6"'
    g = [f'<rect x="{x0}" y="{y0}" width="{W:.1f}" height="{Hh:.1f}" fill="{FILL2}" {st}/>']
    # stitch line along the top, fold lines for hems
    g.append(f'<line x1="{x0 + HEM_BACK * sc:.1f}" y1="{y0 + SEAM * sc:.1f}" x2="{x0 + W - HEM_BACK * sc:.1f}" y2="{y0 + SEAM * sc:.1f}" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="7 5"/>')
    g.append(f'<line x1="{x0}" y1="{y0 + Hh - HEM_BOTTOM * sc:.1f}" x2="{x0 + W:.1f}" y2="{y0 + Hh - HEM_BOTTOM * sc:.1f}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 4"/>')
    for e in (x0 + HEM_BACK * sc, x0 + W - HEM_BACK * sc):
        g.append(f'<line x1="{e:.1f}" y1="{y0}" x2="{e:.1f}" y2="{y0 + Hh:.1f}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 4"/>')
    prev = x0 + HEM_BACK * sc
    names = [f"ข้างซ้าย {f(D)}", f"หน้า {f(L)}", f"ข้างขวา {f(D)}"]
    stops = [x0 + n * sc for n in NOTCH] + [x0 + W - HEM_BACK * sc]
    for i, xx in enumerate(stops):
        if i < 2:
            g.append(f'<path d="M{xx - 7:.1f} {y0} L{xx:.1f} {y0 + 12} L{xx + 7:.1f} {y0}Z" fill="{ACC}"/>')
            g.append(f'<line x1="{xx:.1f}" y1="{y0}" x2="{xx:.1f}" y2="{y0 + Hh:.1f}" stroke="{ACC}" stroke-width="0.8" stroke-dasharray="2 4"/>')
            g.append(f'<text x="{xx:.1f}" y="{y0 - 22:.1f}" text-anchor="middle" font-size="12" fill="{ACC}">บากมุม {f(NOTCH[i])} ซม.</text>')
        g.append(f'<text x="{(prev + xx) / 2:.1f}" y="{y0 + Hh / 2:.1f}" text-anchor="middle" font-size="17" font-weight="600">{names[i]}</text>')
        prev = xx
    g += [f'<text x="{x0 + W / 2:.1f}" y="{y0 + Hh / 2 + 26:.1f}" text-anchor="middle" font-size="14" fill="{MUTED}">ผ้ากระโปรง (หน้า + ข้าง 2 ด้าน ต่อเป็นผืนเดียว) · ตัด 1 ชิ้นต่อโต๊ะ · สำเร็จสูง {f(DROP)} ซม.</text>',
          grain(x0 + W / 2 - 130, y0 + Hh / 2 + 44, 260),
          f'<text x="{x0 + 6:.1f}" y="{y0 - 6:.1f}" font-size="12">ขอบบน: เย็บติดชิ้นบน กันเย็บ {f(SEAM)}</text>',
          f'<text x="{x0 + W - 6:.1f}" y="{y0 + Hh - 6:.1f}" text-anchor="end" font-size="12">ชายล่าง: พับ 2 + 2 ซม.</text>',
          f'<text x="{x0 + 6:.1f}" y="{y0 + Hh - 6:.1f}" font-size="12">ปลายสองข้าง: พับริม 1 + 1</text>',
          dim(x0, y0 + Hh + 26, x0 + W, y0 + Hh + 26, f"ตัด {f(w)} ซม."),
          dim(x0 + W + 26, y0, x0 + W + 26, y0 + Hh, f"{f(h)}", vertical=True)]
    return f'<svg viewBox="0 0 {x0 + W + 60:.0f} {y0 + Hh + 50:.0f}" class="piece">{"".join(g)}</svg>'

def layout():
    sc = 1.62
    x0, y0 = 40, 34
    FW = FABRIC_W * sc
    tot = BAND * sc
    g = [f'<rect x="{x0}" y="{y0}" width="{tot:.1f}" height="{FW:.1f}" fill="#FBF8F3" stroke="{INK}" stroke-width="1.4"/>']
    x = x0
    for k in (1, 2):
        g.append(f'<rect x="{x:.1f}" y="{y0}" width="{TOP_CUT[0] * sc:.1f}" height="{TOP_CUT[1] * sc:.1f}" fill="{FILL}" stroke="{INK}" stroke-width="1.2"/>')
        g.append(f'<text x="{x + TOP_CUT[0] * sc / 2:.1f}" y="{y0 + TOP_CUT[1] * sc / 2 + 5:.1f}" text-anchor="middle" font-size="14" font-weight="600">ชิ้นบน {k}</text>')
        g.append(f'<text x="{x + TOP_CUT[0] * sc / 2:.1f}" y="{y0 + TOP_CUT[1] * sc / 2 + 23:.1f}" text-anchor="middle" font-size="11" fill="{MUTED}">{f(TOP_CUT[0])} × {f(TOP_CUT[1])}</text>')
        g.append(f'<text x="{x + TOP_CUT[0] * sc / 2:.1f}" y="{y0 + (TOP_CUT[1] + (FABRIC_W - TOP_CUT[1]) / 2) * sc + 4:.1f}" text-anchor="middle" font-size="11" fill="{MUTED}">เศษ {f(FABRIC_W - TOP_CUT[1])} ซม. (ทำเชือกผูกได้)</text>')
        x += TOP_CUT[0] * sc
    for k in (1, 2):
        yy = y0 + (k - 1) * SKIRT_H * sc
        g.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{SKIRT_LEN * sc:.1f}" height="{SKIRT_H * sc:.1f}" fill="{FILL2}" stroke="{INK}" stroke-width="1.2"/>')
        g.append(f'<text x="{x + SKIRT_LEN * sc / 2:.1f}" y="{yy + SKIRT_H * sc / 2 + 5:.1f}" text-anchor="middle" font-size="14" font-weight="600">ผ้ากระโปรง {k} · {f(SKIRT_LEN)} × {f(SKIRT_H)}</text>')
    g += [dim(x0, y0 + FW + 22, x0 + tot, y0 + FW + 22, f"ผ้า {f(BAND)} ซม. ({BAND / 100:.2f} ม.) = ผ้าคลุม 2 ตัว"),
          dim(x0 - 6, y0, x0 - 6, y0 + FW, "หน้าผ้า 120", vertical=True, left=True)]
    return f'<svg viewBox="0 0 {x0 + tot + 20:.0f} {y0 + FW + 46:.0f}" class="lay">{"".join(g)}</svg>'

def dim(x1, y1, x2, y2, t, vertical=False, left=False):
    a = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="0.9" marker-start="url(#a)" marker-end="url(#a)"/>'
    if vertical:
        mx, my = x1 + (-18 if left else 14), (y1 + y2) / 2
        return a + f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" font-size="13" transform="rotate(90 {mx:.1f} {my:.1f})">{t}</text>'
    return a + f'<text x="{(x1 + x2) / 2:.1f}" y="{y1 - 6:.1f}" text-anchor="middle" font-size="13">{t}</text>'

def grain(x, y, w, label="แนวเส้นด้ายตามความยาวผ้า"):
    return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + w:.1f}" y2="{y:.1f}" stroke="{INK}" stroke-width="1.2" marker-start="url(#a)" marker-end="url(#a)"/>'
            f'<text x="{x + w / 2:.1f}" y="{y - 6:.1f}" text-anchor="middle" font-size="11" fill="{MUTED}">{label}</text>')

DEFS = (f'<svg width="0" height="0" style="position:absolute"><defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,1 L9,5 L0,9" fill="none" stroke="{INK}" stroke-width="1.4"/></marker></defs></svg>')

# ---------------------------------------------------------------- page
def qty_rows():
    rows = ""
    for n, note in ((1, ""), (6, "ชุดที่ทำเพิ่ม"), (9, "ชุดเดิม"), (15, "รวมทั้งหมด")):
        raw, buy = metres(n)
        rows += f"<tr><td>{n} ตัว{f' · {note}' if note else ''}</td><td class='r'>{raw:.1f} ม.</td><td class='r'><b>{buy} ม.</b></td></tr>"
    return rows

STEPS = [
    "ซักหรือแช่ผ้าก่อนตัด ถ้าเป็นผ้าฝ้ายหรือผ้าแคนวาส กันผ้าหดหลังซัก",
    f"ตัดชิ้นบน {f(TOP_CUT[0])} × {f(TOP_CUT[1])} ซม. และผ้ากระโปรง {f(SKIRT_LEN)} × {f(SKIRT_H)} ซม. ให้ด้านยาวทั้งสองชิ้นอยู่ตามแนวยาวของผ้า",
    f"บากมุมบนผ้ากระโปรงที่ {f(NOTCH[0])} และ {f(NOTCH[1])} ซม. จากปลายซ้าย และทำจุดมุมหน้าบนชิ้นบน ห่างขอบ {f(SEAM)} ซม.",
    "โพ้งริมผ้าทุกด้าน กันผ้ารุ่ย",
    f"พับริมปลายผ้ากระโปรงทั้งสองข้าง และขอบหลังของชิ้นบน แบบพับ 1 + 1 ซม. แล้วเย็บ",
    f"วางผ้ากระโปรงประกบชิ้นบน ด้านถูกเข้าหากัน ให้รอยบากตรงกับมุมหน้า เย็บกันเย็บ {f(SEAM)} ซม. พอถึงมุมให้ตัดเฉียงเข้าถึงเส้นเย็บ แล้วหมุนผ้าเย็บต่อ",
    "พับชายล่างผ้ากระโปรง 2 + 2 ซม. แล้วเย็บ",
    f"ลองคลุมโต๊ะจริง 1 ตัวก่อนตัดชุดที่เหลือ ขอบล่างควรลอยจากพื้นประมาณ {f(FLOOR_GAP)} ซม.",
]

def page():
    css = f"""
@font-face{{font-family:Plex;src:url(file://{FONTS}/IBMPlexSansThai-Regular.ttf)}}
@font-face{{font-family:Plex;font-weight:600;src:url(file://{FONTS}/IBMPlexSansThai-SemiBold.ttf)}}
@page{{size:A4 landscape;margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:Plex,sans-serif;color:{INK};font-size:12.5px;line-height:1.5}}
svg text{{font-family:Plex,sans-serif;fill:{INK}}}
.p{{width:297mm;height:210mm;padding:12mm 14mm 10mm;page-break-after:always;display:flex;flex-direction:column;gap:6mm;position:relative}}
h1{{font-size:24px;margin:0;font-weight:600}} h2{{font-size:17px;margin:0;font-weight:600}}
.sub{{color:{MUTED}}}
.cols{{display:grid;grid-template-columns:1.05fr 1fr;gap:10mm;flex:1;min-height:0}}
.iso{{width:100%;height:auto}}
table{{border-collapse:collapse;width:100%}} td,th{{padding:4px 8px;border-bottom:1px solid #E3D9CC;text-align:left;vertical-align:top}}
th{{font-weight:600;color:{MUTED};font-size:11.5px}} .r{{text-align:right}}
.box{{border:1.5px solid {ACC};border-radius:6px;padding:8px 12px;color:{INK}}}
.piece{{height:100%;width:auto;max-width:100%}} .lay{{width:100%;height:auto}}
ol{{margin:0;padding-left:18px;display:grid;gap:3px}}
.foot{{position:absolute;bottom:6mm;left:14mm;right:14mm;display:flex;justify-content:space-between;color:{MUTED};font-size:10.5px}}
.legend{{display:flex;gap:18px;flex-wrap:wrap;color:{MUTED};font-size:11.5px}}
.legend i{{display:inline-block;width:26px;border-top:2px dashed {ACC};vertical-align:middle;margin-right:6px}}
.legend u{{display:inline-block;width:26px;border-top:2px dotted {MUTED};vertical-align:middle;margin-right:6px}}
"""
    foot = lambda n: f'<div class="foot"><span>OCT. 26 · ผ้าคลุมโต๊ะพาเลทบูธ · 22 ต.ค. 2569</span><span>หน้า {n}/3 · หน่วย ซม.</span></div>'
    p1 = f"""<section class="p">
<div><h1>แพทเทิร์นผ้าคลุมโต๊ะพาเลท</h1><div class="sub">โต๊ะ {TABLE_L} × {TABLE_D} × สูง {TABLE_H} ซม. · คลุมด้านบน ด้านหน้า และด้านข้างสองข้าง · ด้านหลังเปิด เก็บของใต้โต๊ะได้ · ผ้าหน้ากว้าง {FABRIC_W} ซม.</div></div>
<div class="cols"><div>{iso_sketch()}</div>
<div style="display:grid;gap:5mm;align-content:start">
<table><tr><th>ขนาดสำเร็จ</th><th class="r">ซม.</th></tr>
<tr><td>ด้านบน (ยาว × ลึก) เผื่อหลวมข้างละ 1 ซม.</td><td class="r">{f(L)} × {f(D)}</td></tr>
<tr><td>ผ้าด้านหน้าและด้านข้าง สูงจากขอบบน</td><td class="r">{f(DROP)}</td></tr>
<tr><td>ชายผ้าลอยจากพื้น</td><td class="r">{f(FLOOR_GAP)}</td></tr></table>
<table><tr><th>ชิ้นผ้าต่อโต๊ะ 1 ตัว</th><th class="r">ขนาดตัด</th><th class="r">จำนวน</th></tr>
<tr><td>ชิ้นบน</td><td class="r">{f(TOP_CUT[0])} × {f(TOP_CUT[1])}</td><td class="r">1</td></tr>
<tr><td>ผ้ากระโปรง หน้า + ข้าง 2 ด้าน (ผืนเดียว)</td><td class="r">{f(SKIRT_LEN)} × {f(SKIRT_H)}</td><td class="r">1</td></tr></table>
<table><tr><th>ผ้าที่ต้องซื้อ (หน้า {FABRIC_W})</th><th class="r">ใช้จริง</th><th class="r">ซื้อ (+5%)</th></tr>{qty_rows()}</table>
<div class="box">ขนาดตัดรวมกันเย็บ {f(SEAM)} ซม. ชายล่าง {f(HEM_BOTTOM)} ซม. (พับ 2 + 2) และริมด้านหลัง {f(HEM_BACK)} ซม. (พับ 1 + 1) แล้ว ตัดตามตัวเลขได้เลย</div>
</div></div>{foot(1)}</section>"""
    p2 = f"""<section class="p">
<div><h2>ชิ้นผ้าและขนาดตัด</h2><div class="sub">ภาพย่อส่วน ไม่ใช่ขนาดจริง ใช้ตัวเลขที่เขียนกำกับ · ด้านยาวของทั้งสองชิ้นวางตามแนวยาวของผ้า</div></div>
<div style="display:grid;grid-template-columns:1fr;gap:4mm;flex:1;min-height:0">
<div style="height:92mm;display:flex;justify-content:center">{piece_top()}</div>
<div style="height:62mm;display:flex;justify-content:center">{piece_skirt()}</div></div>
<div class="legend"><span><i></i>เส้นเย็บ</span><span><u></u>เส้นพับริม</span><span style="color:{ACC}">▼ รอยบากมุม ตรงกับมุมหน้าของชิ้นบน</span></div>
{foot(2)}</section>"""
    steps = "".join(f"<li>{s}</li>" for s in STEPS)
    p3 = f"""<section class="p">
<div><h2>วางผ้าบนหน้ากว้าง {FABRIC_W} ซม. และขั้นตอนเย็บ</h2><div class="sub">ทุก {BAND / 100:.2f} ม. ได้ผ้าคลุม 2 ตัว · ด้านยาวของทุกชิ้นวางตามแนวยาวของผ้า ริมผ้าอยู่ขอบบนและล่างของภาพ · ผ้ากระโปรง 2 ผืนวางคู่กัน ({f(2 * SKIRT_H)} ซม.)</div></div>
{layout()}
<div class="cols" style="grid-template-columns:1.4fr 1fr"><div><h2 style="font-size:15px;margin-bottom:4px">ขั้นตอนเย็บ</h2><ol>{steps}</ol></div>
<div style="display:grid;gap:4mm;align-content:start"><div class="box">ด้านหลังไม่มีผ้า ผ้าด้านข้างจะห้อยอิสระที่มุมหลัง ถ้าลมแรงหรืออยากให้เรียบ เย็บเชือกผูกที่มุมหลังด้านละ 1 คู่ ใช้เศษผ้าจากแถวชิ้นบนได้</div>
<div class="box" style="border-color:{MUTED}">ตรวจก่อนตัดทั้งหมด: วัดโต๊ะจริงอีกครั้ง โต๊ะเดิมกับโต๊ะที่ทำเพิ่มต้องขนาดเท่ากัน ถ้าต่างกันเกิน 1 ซม. ให้แก้ขนาดตัดตามโต๊ะ</div></div></div>
{foot(3)}</section>"""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{DEFS}{p1}{p2}{p3}</body></html>"

if __name__ == "__main__":
    open(os.path.join(HERE, "pattern.html"), "w").write(page())
    for n in (1, 6, 9, 15):
        print(n, "covers:", metres(n))
    print("top cut", TOP_CUT, "skirt", SKIRT_LEN, "x", SKIRT_H, "notches", NOTCH, "band", BAND)
