"""Fabric cover for one booth pallet table: pattern sheets for the tailor (Thai), 3 pages A4 landscape.

Table 117 x 80 x 50 cm (owner's drawing, 22 Oct 2026). The cover hides the top, the front (117 side) and both
80 cm sides (front and side skirts are separate pieces). The back is a flap that closes with hook-and-loop tape onto the sides and rolls up with two ties.
One cover. Fabric 120 cm wide.

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
HEM_EDGE = 2                                      # free vertical edges, folded 1 + 1
WING = 4                                          # back flap wraps this far round each back corner onto the side
VELCRO_W = 2.5                                    # hook-and-loop tape width
TIE = (5, 92)                                     # tie strip cut size, folded in four to 1.25 cm wide
FABRIC_W = 120
WASTE = 1.05                                      # 5% for shrinkage and cutting

L = TABLE_L + EASE                                # finished top length 119
D = TABLE_D + EASE                                # finished top depth 82
DROP = TABLE_H - FLOOR_GAP                        # finished drop 48

TOP_CUT = (L + 2 * SEAM, D + 2 * SEAM)            # 122 x 85: seams on all four sides
FRONT_LEN = SEAM + L + SEAM                       # 122, front skirt, seamed to both sides at the corners
SIDE_LEN = SEAM + D + HEM_EDGE                    # 85.5, side skirt: corner seam at the front, hem at the back
SKIRT_H = SEAM + DROP + HEM_BOTTOM                # 53.5, all skirt pieces and the back flap
FLAP_LEN = HEM_EDGE + WING + L + WING + HEM_EDGE  # 131
FLAP_NOTCH = (HEM_EDGE + WING, HEM_EDGE + WING + L)
VELCRO_LEN = DROP - 2                             # per strip, 2 cm short of the hem
COL_A = FRONT_LEN + SIDE_LEN                      # two columns of skirt pieces side by side across the fabric
COL_B = FLAP_LEN + SIDE_LEN
LENGTH_USED = TOP_CUT[0] + max(COL_A, COL_B)      # top row, then the two columns
BUY = math.ceil(LENGTH_USED * WASTE / 50) * 0.5   # rounded up to the half metre

assert SKIRT_H * 2 <= FABRIC_W - 6 and TOP_CUT[1] + TIE[0] * 2 <= FABRIC_W - 4
assert TIE[1] <= TOP_CUT[0]

def f(x):
    return f"{x:g}"

# ---------------------------------------------------------------- drawing helpers
INK, MUTED, FILL, FILL2, FILL3, ACC, VEL = "#1C1B22", "#6E6660", "#EFE6DA", "#E2D3BF", "#D9E2EC", "#C8442A", "#3D6FB6"

def txt(x, y, t, size=13, anchor="middle", color=INK, weight=400, rot=None):
    tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}"{tr}>{t}</text>'

def dim(x1, y1, x2, y2, t, vertical=False, left=False):
    a = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="0.9" marker-start="url(#a)" marker-end="url(#a)"/>'
    if vertical:
        mx, my = x1 + (-18 if left else 14), (y1 + y2) / 2
        return a + txt(mx, my, t, rot=90)
    return a + txt((x1 + x2) / 2, y1 - 6, t)

def grain(x, y, w, label="แนวเส้นด้ายตามความยาวผ้า"):
    return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x + w:.1f}" y2="{y:.1f}" stroke="{INK}" stroke-width="1.2" marker-start="url(#a)" marker-end="url(#a)"/>'
            + txt(x + w / 2, y - 6, label, size=11, color=MUTED))

def notch(x, y, label=None):
    s = f'<path d="M{x - 7:.1f} {y} L{x:.1f} {y + 12} L{x + 7:.1f} {y}Z" fill="{ACC}"/>'
    return s + (txt(x, y - 8, label, size=12, color=ACC) if label else "")

def velcro(x, y, w, h, label=None, size=11):
    s = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{VEL}" fill-opacity=".22" stroke="{VEL}" stroke-width="1" stroke-dasharray="3 2"/>'
    return s + (txt(x + w / 2, y + h / 2, label, size=size, color=VEL, rot=-90) if label else "")

DEFS = (f'<svg width="0" height="0" style="position:absolute"><defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,1 L9,5 L0,9" fill="none" stroke="{INK}" stroke-width="1.4"/></marker></defs></svg>')

# ---------------------------------------------------------------- page 1 sketches
def iso_sketch():
    """Front (y = D) and right side (x = L) face the viewer; the back flap is at y = 0."""
    s, c30, s30 = 1.5, math.cos(math.radians(30)), math.sin(math.radians(30))
    def P(x, y, z):
        return ((x - y) * c30 * s, (x + y) * s30 * s - z * s)
    H, Z0 = TABLE_H, FLOOR_GAP
    faces = [
        ([(0, D, H), (L, D, H), (L, D, Z0), (0, D, Z0)], FILL),        # front
        ([(L, 0, H), (L, D, H), (L, D, Z0), (L, 0, Z0)], FILL2),       # right side
        ([(0, 0, H), (L, 0, H), (L, D, H), (0, D, H)], "#F7F1E8"),     # top
    ]
    pts = [P(*p) for fc in faces for p in fc[0]]
    minx, maxx = min(p[0] for p in pts) - 70, max(p[0] for p in pts) + 150
    miny, maxy = min(p[1] for p in pts) - 40, max(p[1] for p in pts) + 40
    out = []
    for poly, fill in faces:
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in (P(*p) for p in poly))
        out.append(f'<polygon points="{d}" fill="{fill}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    # back flap wing wrapping onto the right side, with its tape
    w = [P(L, 0, H), P(L, WING, H), P(L, WING, Z0), P(L, 0, Z0)]
    out.append('<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in w) + f'" fill="{FILL3}" stroke="{VEL}" stroke-width="1.2"/>')
    def label(x, y, z, t, anchor="middle", color=INK, size=15, weight=600, dy=0):
        a, b = P(x, y, z)
        return txt(a, b + dy, t, size=size, anchor=anchor, color=color, weight=weight)
    out += [label(L / 2, D / 2, H, "บน"), label(L / 2, D, H / 2, "หน้า"), label(L, D / 2 + 6, H / 2, "ข้าง"),
            label(L, 0, H, "ผ้าหลังเปิดปิดได้", color=VEL, size=13, dy=-14, anchor="start"),
            label(L / 2, D, Z0, f"ยาว {f(L)}", size=13, weight=400, anchor="end", dy=26),
            label(L, D / 2, Z0, f"ลึก {f(D)}", size=13, weight=400, anchor="start", dy=26),
            label(0, D, H / 2, f"สูง {f(DROP)}", anchor="end", size=13, weight=400)]
    return f'<svg viewBox="{minx:.0f} {miny:.0f} {maxx - minx:.0f} {maxy - miny:.0f}" class="iso">{"".join(out)}</svg>'

def back_views():
    """Back elevation: flap closed (tape onto both sides) and flap rolled up and tied."""
    sc = 1.15
    W, Hh = (L + 2 * WING) * sc, DROP * sc
    def frame(x0, y0, title):
        g = [txt(x0 + W / 2, y0 - 12, title, size=13, weight=600),
             f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{W:.1f}" height="{Hh:.1f}" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 4"/>']
        return g
    g = []
    x0, y0 = 20, 30
    g += frame(x0, y0, "ผ้าหลัง ปิด")
    g.append(txt(x0 + W / 2, y0 + Hh + 14, "ติดตีนตุ๊กแกที่มุมหลังสองข้าง", size=11, color=MUTED))
    g.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{W:.1f}" height="{Hh:.1f}" fill="{FILL3}" stroke="{INK}" stroke-width="1.4"/>')
    for vx in (x0, x0 + W - WING * sc):
        g.append(velcro(vx, y0 + 2, WING * sc, Hh - 6))
    for tx in (x0 + W * 0.25, x0 + W * 0.75):
        g.append(f'<line x1="{tx:.1f}" y1="{y0:.1f}" x2="{tx:.1f}" y2="{y0 + 16:.1f}" stroke="{INK}" stroke-width="2"/>')
    x1 = x0 + W + 40
    g += frame(x1, y0, "ผ้าหลัง เปิด")
    g.append(txt(x1 + W / 2, y0 + Hh + 14, "แกะตีนตุ๊กแก ม้วนขึ้น ผูกเชือก", size=11, color=MUTED))
    g.append(f'<rect x="{x1:.1f}" y="{y0:.1f}" width="{W:.1f}" height="16" rx="8" fill="{FILL3}" stroke="{INK}" stroke-width="1.4"/>')
    for tx in (x1 + W * 0.25, x1 + W * 0.75):
        g.append(f'<path d="M{tx:.1f} {y0 - 2:.1f} v20 M{tx - 6:.1f} {y0 + 22:.1f} l6 -4 l6 4" stroke="{INK}" stroke-width="2" fill="none"/>')
    g.append(txt(x1 + W / 2, y0 + Hh / 2 + 10, "เก็บของใต้โต๊ะได้", size=12, color=MUTED))
    return f'<svg viewBox="0 0 {x1 + W + 20:.0f} {y0 + Hh + 24:.0f}" class="back">{"".join(g)}</svg>'

# ---------------------------------------------------------------- page 2 pieces
def piece_top():
    w, h = TOP_CUT
    sc = 2.55
    W, Hh = w * sc, h * sc
    x0, y0 = 40, 34
    g = [f'<rect x="{x0}" y="{y0}" width="{W:.1f}" height="{Hh:.1f}" fill="{FILL}" stroke="{INK}" stroke-width="1.6"/>',
         f'<rect x="{x0 + SEAM * sc:.1f}" y="{y0 + SEAM * sc:.1f}" width="{(w - 2 * SEAM) * sc:.1f}" height="{(h - 2 * SEAM) * sc:.1f}" fill="none" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="7 5"/>']
    for cx in (x0 + SEAM * sc, x0 + W - SEAM * sc):
        for cy in (y0 + SEAM * sc, y0 + Hh - SEAM * sc):
            g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="{ACC}"/>')
    for tx in (x0 + SEAM * sc + L * 0.25 * sc, x0 + SEAM * sc + L * 0.75 * sc):
        g.append(f'<path d="M{tx:.1f} {y0 + 2:.1f} v14" stroke="{INK}" stroke-width="2.2"/>')
    g += [txt(x0 + W / 2, y0 + Hh / 2 - 6, "ชิ้นบน · ตัด 1", size=18, weight=600),
          txt(x0 + W / 2, y0 + Hh / 2 + 16, f"สำเร็จ {f(L)} × {f(D)}", size=13, color=MUTED),
          grain(x0 + W / 2 - 80, y0 + Hh / 2 + 44, 160),
          txt(x0 + W / 2, y0 - 8, "ขอบหลัง: เย็บติดผ้าหลัง + สอดเชือก 2 เส้นที่ ¼ และ ¾", size=11.5),
          txt(x0 + W / 2, y0 + Hh + 16, "ขอบหน้า: เย็บติดผ้าหน้า", size=11.5),
          txt(x0 - 10, y0 + Hh / 2, f"ทุกด้านกันเย็บ {f(SEAM)}", size=11.5, rot=-90),
          dim(x0, y0 + Hh + 40, x0 + W, y0 + Hh + 40, f"ตัด {f(w)}"),
          dim(x0 + W + 22, y0, x0 + W + 22, y0 + Hh, f"ตัด {f(h)}", vertical=True)]
    return f'<svg viewBox="0 0 {x0 + W + 56:.0f} {y0 + Hh + 50:.0f}" class="piece">{"".join(g)}</svg>'

def piece_flap():
    w, h = FLAP_LEN, SKIRT_H
    sc = 2.55
    W, Hh = w * sc, h * sc
    x0, y0 = 20, 50
    g = [f'<rect x="{x0}" y="{y0}" width="{W:.1f}" height="{Hh:.1f}" fill="{FILL3}" stroke="{INK}" stroke-width="1.6"/>',
         f'<line x1="{x0 + FLAP_NOTCH[0] * sc:.1f}" y1="{y0 + SEAM * sc:.1f}" x2="{x0 + FLAP_NOTCH[1] * sc:.1f}" y2="{y0 + SEAM * sc:.1f}" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="7 5"/>',
         f'<line x1="{x0}" y1="{y0 + Hh - HEM_BOTTOM * sc:.1f}" x2="{x0 + W:.1f}" y2="{y0 + Hh - HEM_BOTTOM * sc:.1f}" stroke="{MUTED}" stroke-dasharray="3 4"/>']
    for e in (x0 + HEM_EDGE * sc, x0 + W - HEM_EDGE * sc):
        g.append(f'<line x1="{e:.1f}" y1="{y0}" x2="{e:.1f}" y2="{y0 + Hh:.1f}" stroke="{MUTED}" stroke-dasharray="3 4"/>')
    for i, n in enumerate(FLAP_NOTCH):
        g.append(notch(x0 + n * sc, y0, f"บาก {f(n)}"))
    vy, vh = y0 + SEAM * sc + 2, VELCRO_LEN * sc
    g.append(velcro(x0 + HEM_EDGE * sc, vy, VELCRO_W * sc, vh))
    g.append(velcro(x0 + W - HEM_EDGE * sc - VELCRO_W * sc, vy, VELCRO_W * sc, vh))
    g += [txt(x0 + W / 2, y0 + Hh / 2 - 4, "ผ้าหลัง (เปิดปิดได้) · ตัด 1", size=17, weight=600),
          txt(x0 + W / 2, y0 + Hh / 2 + 16, f"ปีกข้างละ {f(WING)} ซม. อ้อมมุมไปติดผ้าข้าง", size=12, color=MUTED),
          grain(x0 + W / 2 - 80, y0 + Hh / 2 + 40, 160),
          txt(x0 + W / 2, y0 - 22, f"ขอบบน: เย็บติดขอบหลังชิ้นบนเฉพาะช่วงระหว่างรอยบาก ({f(L)} ซม.)", size=11.5),
          txt(x0 + W / 2, y0 + Hh + 18, f"ตีนตุ๊กแกด้านขน (นิ่ม) ด้านในปีก ข้างละ {f(VELCRO_W)} × {f(VELCRO_LEN)}", size=11.5, color=VEL),
          dim(x0, y0 + Hh + 42, x0 + W, y0 + Hh + 42, f"ตัด {f(w)}"),
          dim(x0 + W + 22, y0, x0 + W + 22, y0 + Hh, f"{f(h)}", vertical=True)]
    return f'<svg viewBox="0 0 {x0 + W + 50:.0f} {y0 + Hh + 52:.0f}" class="piece">{"".join(g)}</svg>'

def piece_skirt():
    """Front skirt and one side skirt (cut 2) at the same scale."""
    sc = 2.55
    x0, y0 = 20, 46
    Hh = SKIRT_H * sc
    g = []
    def body(x, w, fill):
        W = w * sc
        out = [f'<rect x="{x:.1f}" y="{y0}" width="{W:.1f}" height="{Hh:.1f}" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>',
               f'<line x1="{x:.1f}" y1="{y0 + Hh - HEM_BOTTOM * sc:.1f}" x2="{x + W:.1f}" y2="{y0 + Hh - HEM_BOTTOM * sc:.1f}" stroke="{MUTED}" stroke-dasharray="3 4"/>']
        return out, W
    # front: seams on top, left and right
    out, Wf = body(x0, FRONT_LEN, FILL2)
    g += out
    g.append(f'<path d="M{x0 + SEAM * sc:.1f} {y0 + Hh - HEM_BOTTOM * sc:.1f} V{y0 + SEAM * sc:.1f} H{x0 + Wf - SEAM * sc:.1f} V{y0 + Hh - HEM_BOTTOM * sc:.1f}" fill="none" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="7 5"/>')
    g += [txt(x0 + Wf / 2, y0 + Hh / 2 - 4, "ผ้าหน้า · ตัด 1", size=17, weight=600),
          txt(x0 + Wf / 2, y0 + Hh / 2 + 16, f"สำเร็จ {f(L)} × {f(DROP)}", size=12, color=MUTED),
          grain(x0 + Wf / 2 - 70, y0 + Hh / 2 + 40, 140),
          txt(x0 + Wf / 2, y0 - 10, "ขอบบนเย็บติดชิ้นบน · ขอบซ้ายขวาเย็บติดผ้าข้าง", size=11.5),
          dim(x0, y0 + Hh + 24, x0 + Wf, y0 + Hh + 24, f"ตัด {f(FRONT_LEN)}"),
          dim(x0 + Wf + 18, y0, x0 + Wf + 18, y0 + Hh, f"{f(SKIRT_H)}", vertical=True)]
    # side: seam on top and on the front end, hem and tape at the back end
    xs = x0 + Wf + 70
    out, Ws = body(xs, SIDE_LEN, FILL2)
    g += out
    g.append(f'<path d="M{xs + SEAM * sc:.1f} {y0 + Hh - HEM_BOTTOM * sc:.1f} V{y0 + SEAM * sc:.1f} H{xs + Ws - HEM_EDGE * sc:.1f}" fill="none" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="7 5"/>')
    g.append(f'<line x1="{xs + Ws - HEM_EDGE * sc:.1f}" y1="{y0}" x2="{xs + Ws - HEM_EDGE * sc:.1f}" y2="{y0 + Hh:.1f}" stroke="{MUTED}" stroke-dasharray="3 4"/>')
    g.append(velcro(xs + Ws - HEM_EDGE * sc - VELCRO_W * sc, y0 + SEAM * sc + 2, VELCRO_W * sc, VELCRO_LEN * sc))
    g += [txt(xs + Ws / 2, y0 + Hh / 2 - 4, "ผ้าข้าง · ตัด 2", size=17, weight=600),
          txt(xs + Ws / 2, y0 + Hh / 2 + 16, f"สำเร็จ {f(D)} × {f(DROP)}", size=12, color=MUTED),
          grain(xs + Ws / 2 - 60, y0 + Hh / 2 + 40, 120),
          txt(xs + 4, y0 - 10, "ปลายหน้า: เย็บติดผ้าหน้า", size=11.5, anchor="start"),
          txt(xs + Ws, y0 - 26, "ปลายหลัง: พับ 1 + 1", size=11.5, anchor="end"),
          txt(xs + Ws / 2, y0 + Hh + 44, f"ตีนตุ๊กแกด้านหนาม ด้านนอก ที่ปลายหลัง {f(VELCRO_W)} × {f(VELCRO_LEN)}", size=11.5, color=VEL),
          txt(xs + Ws / 2, y0 + Hh + 60, "ซ้ายกับขวากลับด้านกัน: เย็บตีนตุ๊กแกด้านนอกของแต่ละข้าง", size=11, color=MUTED),
          dim(xs, y0 + Hh + 24, xs + Ws, y0 + Hh + 24, f"ตัด {f(SIDE_LEN)}"),
          dim(xs + Ws + 18, y0, xs + Ws + 18, y0 + Hh, f"{f(SKIRT_H)}", vertical=True)]
    return f'<svg viewBox="0 0 {xs + Ws + 50:.0f} {y0 + Hh + 70:.0f}" class="piece">{"".join(g)}</svg>'

# ---------------------------------------------------------------- page 3 layout
def layout():
    sc = 2.0
    x0, y0 = 44, 30
    FW = FABRIC_W * sc
    tot = LENGTH_USED * sc
    g = [f'<rect x="{x0}" y="{y0}" width="{tot:.1f}" height="{FW:.1f}" fill="#FBF8F3" stroke="{INK}" stroke-width="1.4"/>']
    def box(x, y, w, h, fill, t1, t2):
        return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w * sc:.1f}" height="{h * sc:.1f}" fill="{fill}" stroke="{INK}" stroke-width="1.2"/>'
                + txt(x + w * sc / 2, y + h * sc / 2 + 2, t1, size=14, weight=600) + txt(x + w * sc / 2, y + h * sc / 2 + 19, t2, size=11, color=MUTED))
    g.append(box(x0, y0, *TOP_CUT, FILL, "ชิ้นบน", f"{f(TOP_CUT[0])} × {f(TOP_CUT[1])}"))
    ty = y0 + TOP_CUT[1] * sc + 4
    for k in range(2):
        g.append(f'<rect x="{x0:.1f}" y="{ty + k * (TIE[0] * sc + 4):.1f}" width="{TIE[1] * sc:.1f}" height="{TIE[0] * sc:.1f}" fill="#F3E9DD" stroke="{INK}" stroke-width="1"/>')
        g.append(txt(x0 + TIE[1] * sc / 2, ty + k * (TIE[0] * sc + 4) + TIE[0] * sc / 2 + 4, f"เชือก {k + 1} · {f(TIE[0])} × {f(TIE[1])}", size=10))
    x = x0 + TOP_CUT[0] * sc
    yb = y0 + SKIRT_H * sc
    g.append(box(x, y0, FRONT_LEN, SKIRT_H, FILL2, "ผ้าหน้า", f"{f(FRONT_LEN)} × {f(SKIRT_H)}"))
    g.append(box(x + FRONT_LEN * sc, y0, SIDE_LEN, SKIRT_H, FILL2, "ผ้าข้าง 1", f"{f(SIDE_LEN)} × {f(SKIRT_H)}"))
    g.append(box(x, yb, FLAP_LEN, SKIRT_H, FILL3, "ผ้าหลัง", f"{f(FLAP_LEN)} × {f(SKIRT_H)}"))
    g.append(box(x + FLAP_LEN * sc, yb, SIDE_LEN, SKIRT_H, FILL2, "ผ้าข้าง 2", f"{f(SIDE_LEN)} × {f(SKIRT_H)}"))
    g += [dim(x0, y0 + FW + 22, x0 + tot, y0 + FW + 22, f"ใช้ผ้ายาว {f(LENGTH_USED)} ซม. ({LENGTH_USED / 100:.2f} ม.)"),
          dim(x0 - 6, y0, x0 - 6, y0 + FW, f"หน้าผ้า {FABRIC_W}", vertical=True, left=True)]
    return f'<svg viewBox="0 0 {x0 + tot + 20:.0f} {y0 + FW + 40:.0f}" class="lay">{"".join(g)}</svg>'

# ---------------------------------------------------------------- page
STEPS = [
    "ซักหรือแช่ผ้าก่อนตัด ถ้าเป็นผ้าฝ้ายหรือผ้าแคนวาส กันผ้าหดหลังซัก",
    f"ตัด 7 ชิ้นตามหน้า 2 ให้ด้านยาวของทุกชิ้นอยู่ตามแนวยาวของผ้า บากที่ผ้าหลัง ({f(FLAP_NOTCH[0])} และ {f(FLAP_NOTCH[1])} ซม.)",
    "โพ้งริมผ้าทุกด้าน กันผ้ารุ่ย",
    f"เชือก: พับครึ่งตามยาว พับริมเข้าหากันอีกครั้ง ได้กว้าง {TIE[0] / 4:g} ซม. แล้วเย็บทับตลอดเส้น",
    f"เย็บผ้าข้างสองชิ้นติดกับปลายซ้ายและขวาของผ้าหน้า กันเย็บ {f(SEAM)} ซม. ได้ผ้ากระโปรง 3 ด้าน แล้วรีดตะเข็บแยก",
    "พับริมปลายหลังของผ้าข้างทั้งสองชิ้นและริมข้างผ้าหลัง แบบพับ 1 + 1 ซม. แล้วเย็บ",
    f"เย็บตีนตุ๊กแกด้านหนามที่ด้านนอกปลายหลังของผ้าข้างทั้งสองข้าง และด้านขนที่ด้านในปีกผ้าหลังทั้งสองข้าง ยาว {f(VELCRO_LEN)} ซม. เริ่มใต้เส้นเย็บบน",
    f"ประกบผ้ากระโปรงกับชิ้นบน ด้านถูกเข้าหากัน ให้ตะเข็บมุมตรงมุมหน้าของชิ้นบน เย็บกันเย็บ {f(SEAM)} ซม. ถึงมุมให้หยุดที่ปลายตะเข็บมุม หมุนผ้าแล้วเย็บต่อ",
    f"ประกบผ้าหลังกับขอบหลังชิ้นบนเฉพาะช่วงระหว่างรอยบาก สอดกลางเชือกทั้ง 2 เส้นไว้ในตะเข็บที่ ¼ และ ¾ ของความกว้าง ให้ปลายเชือกห้อยทั้งด้านนอกและด้านใน ปีกผ้าหลังปล่อยอิสระ",
    "พับชายล่างผ้ากระโปรงและผ้าหลัง 2 + 2 ซม. แล้วเย็บ",
    f"ลองคลุมโต๊ะจริง: ปีกผ้าหลังต้องอ้อมมุมไปทับตีนตุ๊กแกบนผ้าข้างพอดี ขอบล่างลอยจากพื้นประมาณ {f(FLOOR_GAP)} ซม.",
]

def page():
    css = f"""
@font-face{{font-family:Plex;src:url(file://{FONTS}/IBMPlexSansThai-Regular.ttf)}}
@font-face{{font-family:Plex;font-weight:600;src:url(file://{FONTS}/IBMPlexSansThai-SemiBold.ttf)}}
@page{{size:A4 landscape;margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:Plex,sans-serif;color:{INK};font-size:12.5px;line-height:1.5}}
svg text{{font-family:Plex,sans-serif}}
.p{{width:297mm;height:210mm;padding:11mm 14mm 10mm;page-break-after:always;display:flex;flex-direction:column;gap:5mm;position:relative;overflow:hidden}}
h1{{font-size:23px;margin:0;font-weight:600}} h2{{font-size:17px;margin:0;font-weight:600}}
.sub{{color:{MUTED}}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:9mm;flex:1;min-height:0}}
.iso,.back,.lay{{width:100%;height:auto}}
table{{border-collapse:collapse;width:100%}} td,th{{padding:3px 8px;border-bottom:1px solid #E3D9CC;text-align:left;vertical-align:top}}
th{{font-weight:600;color:{MUTED};font-size:11.5px}} .r{{text-align:right;white-space:nowrap}}
.box{{border:1.5px solid {ACC};border-radius:6px;padding:7px 12px}}
.piece{{height:100%;width:auto;max-width:100%}}
ol{{margin:0;padding-left:18px;display:grid;gap:1px;font-size:12px;line-height:1.42}}
.foot{{position:absolute;bottom:6mm;left:14mm;right:14mm;display:flex;justify-content:space-between;color:{MUTED};font-size:10.5px}}
.legend{{display:flex;gap:18px;flex-wrap:wrap;color:{MUTED};font-size:11.5px}}
.legend i{{display:inline-block;width:26px;border-top:2px dashed {ACC};vertical-align:middle;margin-right:6px}}
.legend u{{display:inline-block;width:26px;border-top:2px dotted {MUTED};vertical-align:middle;margin-right:6px}}
.legend b{{display:inline-block;width:22px;height:10px;background:{VEL}33;border:1px dashed {VEL};vertical-align:middle;margin-right:6px}}
"""
    foot = lambda n: f'<div class="foot"><span>OCT. 26 · ผ้าคลุมโต๊ะพาเลทบูธ 1 ตัว · 22 ต.ค. 2569</span><span>หน้า {n}/3 · หน่วย ซม.</span></div>'
    p1 = f"""<section class="p">
<div><h1>แพทเทิร์นผ้าคลุมโต๊ะพาเลท 1 ตัว</h1><div class="sub">โต๊ะ {TABLE_L} × {TABLE_D} × สูง {TABLE_H} ซม. · คลุมด้านบน ด้านหน้า ด้านข้างสองข้าง และด้านหลังแบบเปิดปิดได้ · ผ้าหน้ากว้าง {FABRIC_W} ซม.</div></div>
<div class="cols"><div style="display:grid;gap:4mm;align-content:start">{iso_sketch()}{back_views()}</div>
<div style="display:grid;gap:4mm;align-content:start">
<table><tr><th>ขนาดสำเร็จ</th><th class="r">ซม.</th></tr>
<tr><td>ด้านบน (ยาว × ลึก) เผื่อหลวมข้างละ 1 ซม.</td><td class="r">{f(L)} × {f(D)}</td></tr>
<tr><td>ผ้าหน้า ข้าง และหลัง สูงจากขอบบน · ลอยจากพื้น</td><td class="r">{f(DROP)} · {f(FLOOR_GAP)}</td></tr></table>
<table><tr><th>ชิ้นผ้า</th><th class="r">ขนาดตัด</th><th class="r">จำนวน</th></tr>
<tr><td>ชิ้นบน</td><td class="r">{f(TOP_CUT[0])} × {f(TOP_CUT[1])}</td><td class="r">1</td></tr>
<tr><td>ผ้าหน้า</td><td class="r">{f(FRONT_LEN)} × {f(SKIRT_H)}</td><td class="r">1</td></tr>
<tr><td>ผ้าข้าง</td><td class="r">{f(SIDE_LEN)} × {f(SKIRT_H)}</td><td class="r">2</td></tr>
<tr><td>ผ้าหลัง เปิดปิดได้</td><td class="r">{f(FLAP_LEN)} × {f(SKIRT_H)}</td><td class="r">1</td></tr>
<tr><td>เชือกผูกม้วนผ้าหลัง</td><td class="r">{f(TIE[0])} × {f(TIE[1])}</td><td class="r">2</td></tr></table>
<table><tr><th>ของที่ต้องซื้อ</th><th class="r">จำนวน</th></tr>
<tr><td>ผ้าหน้า {FABRIC_W} ซม. (ใช้จริง {LENGTH_USED / 100:.2f} ม. เผื่อหดและตัดเสีย)</td><td class="r"><b>{BUY:g} ม.</b></td></tr>
<tr><td>ตีนตุ๊กแก กว้าง {f(VELCRO_W)} ซม. (ด้านหนามและด้านขน ด้านละ 2 เส้น เส้นละ {f(VELCRO_LEN)} ซม.)</td><td class="r"><b>1 ม. คู่</b></td></tr></table>
<div class="box">ขนาดตัดรวมกันเย็บ {f(SEAM)} ซม. ชายล่าง {f(HEM_BOTTOM)} ซม. (พับ 2 + 2) และริมปลาย {f(HEM_EDGE)} ซม. (พับ 1 + 1) แล้ว ตัดตามตัวเลขได้เลย</div>
</div></div>{foot(1)}</section>"""
    p2 = f"""<section class="p">
<div><h2>ชิ้นผ้าและขนาดตัด</h2><div class="sub">ภาพย่อส่วน ใช้ตัวเลขที่เขียนกำกับ · ด้านยาวของทุกชิ้นวางตามแนวยาวของผ้า · ทุกชิ้นใช้มาตราส่วนเดียวกัน</div></div>
<div style="display:grid;grid-template-columns:1fr 1.18fr;gap:6mm;height:76mm"><div style="display:flex;justify-content:center">{piece_top()}</div><div style="display:flex;justify-content:center;align-items:center">{piece_flap()}</div></div>
<div style="height:64mm;margin-top:3mm;display:flex;justify-content:center">{piece_skirt()}</div>
<div class="legend"><span><i></i>เส้นเย็บ</span><span><u></u>เส้นพับริม</span><span><b></b>ตีนตุ๊กแก</span><span style="color:{ACC}">▼ รอยบาก ตรงกับมุมของชิ้นบน</span><span>▮ ตำแหน่งเชือก</span><span>ชายล่างทุกชิ้นพับ 2 + 2 · ริมปลายพับ 1 + 1</span></div>
{foot(2)}</section>"""
    steps = "".join(f"<li>{s}</li>" for s in STEPS)
    p3 = f"""<section class="p">
<div><h2>วางผ้าบนหน้ากว้าง {FABRIC_W} ซม. และขั้นตอนเย็บ</h2><div class="sub">ด้านยาวของทุกชิ้นวางตามแนวยาวของผ้า ริมผ้าอยู่ขอบบนและล่างของภาพ · เชือก 2 เส้นตัดจากแถบข้างชิ้นบน</div></div>
<div style="width:66%">{layout()}</div>
<div class="cols" style="grid-template-columns:1.55fr 1fr"><div><h2 style="font-size:15px;margin-bottom:3px">ขั้นตอนเย็บ</h2><ol>{steps}</ol></div>
<div style="display:grid;gap:4mm;align-content:start"><div class="box">ใช้งาน: ปิด กดปีกผ้าหลังติดตีนตุ๊กแกที่มุมหลังทั้งสองข้าง · เปิด แกะตีนตุ๊กแก ม้วนผ้าหลังขึ้นไปถึงขอบโต๊ะ แล้วผูกเชือกทั้ง 2 เส้นรอบม้วน</div>
<div class="box" style="border-color:{MUTED}">ตรวจก่อนตัด: วัดโต๊ะจริงอีกครั้ง ถ้าขนาดต่างจาก {TABLE_L} × {TABLE_D} × {TABLE_H} เกิน 1 ซม. ให้แก้ขนาดตัดตามโต๊ะ</div></div></div>
{foot(3)}</section>"""
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{DEFS}{p1}{p2}{p3}</body></html>"

if __name__ == "__main__":
    open(os.path.join(HERE, "pattern.html"), "w").write(page())
    print("top", TOP_CUT, "front", FRONT_LEN, "side", SIDE_LEN, SKIRT_H, "flap", FLAP_LEN, FLAP_NOTCH, "ties", TIE,
          "velcro", VELCRO_LEN, "length", LENGTH_USED, "buy", BUY)
