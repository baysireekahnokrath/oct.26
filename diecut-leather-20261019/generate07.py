"""Pattern 07 (Round-joint cross) - 1:1 die drawing, DXF and SVG, REV 20261019.

Source: the designer's vector PDF of 2026-10-19 (source-20261019.pdf, black 0.75 pt = CUT, red 0.5 pt = SLIT).
Built with the same helpers and rules as ../diecut-leather-20261014/generate.py so the sheet matches 01-06.
The 01-06 files of REV 20261014 are not touched.

Design intent (designer, 19 Oct): with the tips shown on the front, the tab lobe of one piece and the lobe of the
next piece meet across the joint and make one full circle. That needs every lobe to be a half circle whose centre
sits on the fold line. Checked: lobes R16.58, centres 28.43 from the piece centre, slit line 28.47 (0.04 apart).

Change from the source, agreed with the designer on 19 Oct: receiving slit 16.6 -> 17.1 so the tab neck (16.6)
is 0.5 smaller than the slit, the rule used on 01-06. Fold lines are put through the lobe centres.

python3 generate07.py -> diecut-drawings-1to1-07-rev20261019.pdf, dxf/07-*.dxf, svg/07-*.svg
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PREV = os.path.join(HERE, "..", "diecut-leather-20261014")
sys.path.insert(0, PREV)
import extract as X
import generate as G
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

SRC = os.path.join(HERE, "source-20261019.pdf")
CODE, NAME = "07", "Round-joint cross"
SLIT_07 = 17.1
G.DATE = "2026-10-19"
G.SLIT[CODE] = SLIT_07

# ---------------------------------------------------------------- geometry from the designer's file
X.ORDER = [(CODE, 5, NAME)]                      # drawing 5 on the page is the cut outline
P07 = X.load(SRC)[0]

# ---------------------------------------------------------------- slits: same rules as 03-06
_orig_alignment = G.alignment

def alignment(p):
    if p["code"] != CODE:
        return _orig_alignment(p)
    groups = G.circles(p)
    lobes = sorted(groups, key=lambda g_: -g_["r"])[:4]
    C = (round(sum(g_["c"][0] for g_ in lobes) / 4, 2), round(sum(g_["c"][1] for g_ in lobes) / 4, 2))
    cx, cy = C
    h = round(sum(math.dist(g_["c"], C) for g_ in lobes) / 4, 2)          # fold line through the lobe centres
    R = sum(g_["r"] for g_ in lobes) / 4
    L = SLIT_07; neck = round(L - G.CLEARANCE, 2)
    slits, folds, recv = [], [], []

    def receiver(M, u, name):
        a, b = G._add(M, -L / 2, u), G._add(M, L / 2, u)
        slits.append({"a": a, "b": b, "kind": "slit", "note": f"receiving slit {L:.2f}, centred on CL"})
        recv.append({"M": M, "u": u, "L": L, "name": name})

    def tab_fold(M, u, name):
        P1, P2 = G._hit(p, M, u), G._hit(p, M, (-u[0], -u[1]))
        for Pq, sg in ((P1, 1), (P2, -1)):
            d = (u[0] * sg, u[1] * sg)
            outer = G._add(Pq, G.OVERRUN, d); inner = G._add(M, neck / 2, d)
            slits.append({"a": outer, "b": inner, "kind": "slot",
                          "note": f"slot {math.dist(Pq, inner):.2f} in + {G.OVERRUN:.1f} past cut"})
        folds.append({"M": M, "u": u, "neck": neck, "P1": P1, "P2": P2, "name": name})

    receiver((cx, cy + h), (1, 0), "top"); receiver((cx, cy - h), (1, 0), "bottom")
    tab_fold((cx + h, cy), (0, 1), "right"); tab_fold((cx - h, cy), (0, 1), "left")
    f0 = folds[0]; chord = math.dist(f0["P1"], f0["P2"])
    off = max(abs(math.dist(g_["c"], C) - h) for g_ in lobes)
    checks = [("lobes: half circles, fold through centres", f"R{R:.2f} at {h:.2f} from centre ({off:.2f} off)"),
              ("shown tips make a circle", f"dia. {2 * R:.2f} at every joint"),
              ("receiving slit", f"{L:.2f}, centred on CL (designer 16.60, +0.50)"),
              ("tab neck = slit - 0.5", f"{neck:.2f}, centred on CL (0.00)"),
              ("slot inside the piece", f"{(chord - neck) / 2:.2f} each side, chord {chord:.2f}"),
              ("overrun past cut", f"{G.OVERRUN:.2f} (designer 1.70)")]
    return {"C": C, "slits": slits, "checks": checks, "folds": folds, "recv": recv, "diag": False, "h": h, "R": R}

G.alignment = alignment

# ---------------------------------------------------------------- title block for this revision
def frame(c, sheet, total, title, sub):
    c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0); c.setLineWidth(0.5)
    c.rect(8 * mm, 8 * mm, 194 * mm, 281 * mm); c.rect(10 * mm, 10 * mm, 190 * mm, 34 * mm)
    c.setLineWidth(0.3)
    for xx in (110, 150): c.line(xx * mm, 10 * mm, xx * mm, 44 * mm)
    c.line(10 * mm, 27 * mm, 200 * mm, 27 * mm)
    c.setFont("Helvetica-Bold", 12); c.drawString(13 * mm, 35 * mm, title)
    c.setFont("Helvetica", 8); c.drawString(13 * mm, 30 * mm, sub.replace("REV 20261014", "REV 20261019"))
    c.setFont("Helvetica", 7)
    c.drawString(13 * mm, 22 * mm, "Project: Leather no-sew interlocking patterns  |  REV 20261019 (adds 07)")
    c.drawString(13 * mm, 17.5 * mm, "Source: 20261019_pattern-leather-2.pdf (vector, exact geometry)")
    c.drawString(13 * mm, 13 * mm, "Material: leather 1.2-2.0 mm  |  Process: steel-rule / clicker die")
    c.drawString(113 * mm, 37 * mm, "SCALE"); c.setFont("Helvetica-Bold", 11); c.drawString(113 * mm, 31 * mm, "1 : 1")
    c.setFont("Helvetica", 7); c.drawString(113 * mm, 22 * mm, "UNITS: mm")
    c.drawString(113 * mm, 17.5 * mm, "TOL: +/-0.2 mm"); c.drawString(113 * mm, 13 * mm, "PAPER: A4 (print 100%)")
    c.drawString(153 * mm, 37 * mm, f"DATE: {G.DATE}"); c.drawString(153 * mm, 31 * mm, f"SHEET: {sheet} / {total}")
    c.drawString(153 * mm, 22 * mm, "DRAWN: Claude Code"); c.drawString(153 * mm, 17.5 * mm, "CHECKED: ________")
    c.drawString(153 * mm, 13 * mm, "APPROVED: ________")

G.frame = frame

NOTES = [
    "Tips shown on the front: the two lobes meet across each joint as one circle. Joins with 07 (mixing with 06 untested).",
]

def ligament(p):
    from shapely.geometry import Point, LineString
    from extract import sample
    from shapely.geometry import Polygon
    poly = Polygon(sample(p["segs"], 200)).buffer(0)
    segs = [LineString([s["a"], s["b"]]) for s in G.final_slits(p)]
    out = []
    for i, g in enumerate(segs):
        for e in g.coords:
            P = Point(e)
            if poly.contains(P) and poly.exterior.distance(P) > 0.3:
                out.append(min([poly.exterior.distance(P)] + [g2.distance(P) for j, g2 in enumerate(segs) if j != i]))
    return min(out)

def main():
    p = P07
    c = canvas.Canvas(os.path.join(HERE, "diecut-drawings-1to1-07-rev20261019.pdf"), pagesize=A4)
    c.setTitle("Leather die-cut drawing 1:1 - pattern 07 - REV 20261019 - print at 100%")
    G.pattern_page(c, p, 1, 1, NOTES + [f"Slit lengthened 16.6 -> 17.1 (agreed 19 Oct). Leather left at slit tips: {ligament(p):.2f} mm (min 8.0)."])
    c.showPage(); c.save()
    os.makedirs(os.path.join(HERE, "dxf"), exist_ok=True); os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)
    slug = f"{CODE}-{NAME.lower().replace(' ', '-')}"
    doc = G.new_doc(); G.dxf_add(doc.modelspace(), p); doc.saveas(os.path.join(HERE, "dxf", slug + ".dxf"))
    G.write_svg(p, os.path.join(HERE, "svg", slug + ".svg"))
    A = G.alignment(p)
    print(CODE, NAME, p["W"], "x", p["H"], "segs", len(p["segs"]), "dropped", p["dropped"])
    for k, v in A["checks"]:
        print(" ", k, ":", v)
    for i, s in enumerate(G.final_slits(p), 1):
        print(f"  S{i} {s['a']} -> {s['b']} L={math.dist(s['a'], s['b']):.2f} {s['note']}")
    print("  ligament", round(ligament(p), 2))

if __name__ == "__main__":
    main()
