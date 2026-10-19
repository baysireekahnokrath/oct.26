"""Full 1:1 die-cut set 01-07, REV 20261019: one PDF (7 sheets) and one all-patterns DXF.

01-06 are drawn exactly as in REV 20261014 (same source, same slits, same notes); only the set adds 07.
07 comes from generate07.py (source-20261019.pdf, slit 17.1). Material line uses the owner's leather, 1.0-1.2 mm.

python3 generate_set.py -> diecut-drawings-1to1-rev20261019.pdf, dxf/all-patterns-rev20261019.dxf
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PREV = os.path.join(HERE, "..", "diecut-leather-20261014")
sys.path.insert(0, PREV); sys.path.insert(0, HERE)
import extract as X
import generate as G
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

P = X.load(G.SRC)                                # 01-06 first, before generate07 changes X.ORDER
import generate07 as S07                         # adds 07 rules to G.alignment
P.append(S07.P07)

SOURCE = {"07": ("20261019_pattern-leather-2.pdf", "2026-10-19")}
SOURCE_DEFAULT = ("20261014_pattern-leather-cre.pdf", "2026-10-14")
_cur = {"code": None}

def frame(c, sheet, total, title, sub):
    src, date = SOURCE.get(_cur["code"], SOURCE_DEFAULT)
    c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0); c.setLineWidth(0.5)
    c.rect(8 * mm, 8 * mm, 194 * mm, 281 * mm); c.rect(10 * mm, 10 * mm, 190 * mm, 34 * mm)
    c.setLineWidth(0.3)
    for xx in (110, 150): c.line(xx * mm, 10 * mm, xx * mm, 44 * mm)
    c.line(10 * mm, 27 * mm, 200 * mm, 27 * mm)
    c.setFont("Helvetica-Bold", 12); c.drawString(13 * mm, 35 * mm, title)
    c.setFont("Helvetica", 8); c.drawString(13 * mm, 30 * mm, sub.replace("REV 20261014", "REV 20261019"))
    c.setFont("Helvetica", 7)
    c.drawString(13 * mm, 22 * mm, "Project: Leather no-sew interlocking patterns  |  REV 20261019 (set 01-07)")
    c.drawString(13 * mm, 17.5 * mm, f"Source: {src} (vector, exact geometry)")
    c.drawString(13 * mm, 13 * mm, "Material: leather 1.0-1.2 mm  |  Process: steel-rule / clicker die")
    c.drawString(113 * mm, 37 * mm, "SCALE"); c.setFont("Helvetica-Bold", 11); c.drawString(113 * mm, 31 * mm, "1 : 1")
    c.setFont("Helvetica", 7); c.drawString(113 * mm, 22 * mm, "UNITS: mm")
    c.drawString(113 * mm, 17.5 * mm, "TOL: +/-0.2 mm"); c.drawString(113 * mm, 13 * mm, "PAPER: A4 (print 100%)")
    c.drawString(153 * mm, 37 * mm, f"DATE: {date}"); c.drawString(153 * mm, 31 * mm, f"SHEET: {sheet} / {total}")
    c.drawString(153 * mm, 22 * mm, "DRAWN: Claude Code"); c.drawString(153 * mm, 17.5 * mm, "CHECKED: ________")
    c.drawString(153 * mm, 13 * mm, "APPROVED: ________")

G.frame = frame

NOTES = dict(G.NOTES)
NOTES["07"] = S07.NOTES + [f"Slit lengthened 16.6 -> 17.1 (agreed 19 Oct). Leather left at slit tips: {S07.ligament(S07.P07):.2f} mm (min 8.0)."]

def main():
    c = canvas.Canvas(os.path.join(HERE, "diecut-drawings-1to1-rev20261019.pdf"), pagesize=A4)
    c.setTitle("Leather die-cut drawings 1:1 - patterns 01-07 - REV 20261019 - print at 100%")
    for i, p in enumerate(P, 1):
        _cur["code"] = p["code"]
        G.pattern_page(c, p, i, len(P), NOTES.get(p["code"], [])); c.showPage()
    c.save()
    allp = G.new_doc(); amsp = allp.modelspace()
    for i, p in enumerate(P):
        ox, oy = (i % 3) * 125, -(i // 3) * 125
        G.dxf_add(amsp, p, ox, oy)
        rev = "REV20261019" if p["code"] == "07" else "REV20261014"
        amsp.add_text(f"{p['code']} {p['name']} {p['W']:.2f}x{p['H']:.2f} {rev}", height=3.5,
                      dxfattribs={"layer": "NOTE_NOT_CUT"}).set_placement((ox, oy + p["H"] + 5))
    os.makedirs(os.path.join(HERE, "dxf"), exist_ok=True)
    allp.saveas(os.path.join(HERE, "dxf", "all-patterns-rev20261019.dxf"))
    for p in P:
        print(p["code"], p["name"], f"{p['W']:.2f}x{p['H']:.2f}", len(G.final_slits(p)), "slit lines")

if __name__ == "__main__":
    main()
