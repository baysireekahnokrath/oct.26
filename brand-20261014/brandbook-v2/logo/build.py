"""Square logo OCT. 26 (brand book v2): the drawn letters of the original name, stacked in a square.

"OCT." on the first line, "26" on the second, same cap height and stroke, flush left. Side of the square =
width of "OCT." + 2 x margin, margin = cap / phi. The dot is mom's leaf green. Writes svg/*.svg.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); BOOK = os.path.dirname(HERE); ROOT = os.path.dirname(BOOK)
sys.path.insert(0, os.path.join(ROOT, "logolab")); sys.path.insert(0, BOOK)
import geometry as G
from palette import C, BAND

H, PHI = G.H, G.PHI
M = H / PHI                                   # margin round the text block
LEAD = H / PHI                                # space between the two lines
_, W_OCT = G.word("OCT.", "#000", "#000", "m")
S = W_OCT + 2 * M                             # square side
BLOCK_H = 2 * H + LEAD
TOP = (S - BLOCK_H) / 2

def stack(ink, dot, uid):
    a, _ = G.word("OCT.", ink, dot, uid + "a")
    b, _ = G.word("26", ink, dot, uid + "b")
    y1, y2 = TOP + H, TOP + 2 * H + LEAD
    return f'<g transform="translate({M:.2f},{y1:.2f})">{a}</g><g transform="translate({M:.2f},{y2:.2f})">{b}</g>'

def square(name, bg, ink, dot, frame=None, band=False):
    uid = name.replace("-", "")
    body = f'<rect width="{S:.2f}" height="{S:.2f}" fill="{bg}"/>' if bg else ""
    if frame:
        sw = G.W / PHI
        body += f'<rect x="{sw / 2:.2f}" y="{sw / 2:.2f}" width="{S - sw:.2f}" height="{S - sw:.2f}" fill="none" stroke="{frame}" stroke-width="{sw:.2f}"/>'
    body += stack(ink, dot, uid)
    if band:
        bh = M / PHI
        w = S / len(BAND)
        body += "".join(f'<rect x="{i * w:.2f}" y="{S - bh:.2f}" width="{w + .3:.2f}" height="{bh:.2f}" fill="{c}"/>' for i, c in enumerate(BAND))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S:.2f} {S:.2f}" width="{S:.0f}" height="{S:.0f}"><title>OCT. 26</title>{body}</svg>'
    open(os.path.join(HERE, "svg", name + ".svg"), "w").write(svg)
    return svg

def line(name, ink, dot):
    s, w, _ = G.wordmark(ink, dot, name.replace("-", ""))
    pad = M / PHI
    vw, vh = w + 2 * pad, H + 2 * pad + G.W
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw:.2f} {vh:.2f}" width="{vw:.0f}" height="{vh:.0f}"><title>OCT. 26</title>'
           f'<g transform="translate({pad:.2f},{pad + H:.2f})">{s}</g></svg>')
    open(os.path.join(HERE, "svg", name + ".svg"), "w").write(svg)

VARIANTS = {   # name: (background, letters, dot, frame, band)
    "square-light":  (C["cotton"], C["charcoal"], C["mom"], None, False),
    "square-dark":   (C["charcoal"], C["cotton"], C["leaf_on_dark"], None, False),
    "square-leaf":   (C["mom"], C["cotton"], C["cotton"], None, False),
    "square-family": (C["cotton"], C["charcoal"], C["mom"], None, True),
    "square-mono":   (None, C["charcoal"], C["charcoal"], C["charcoal"], False),
    "square-mono-white": (None, "#FFFFFF", "#FFFFFF", "#FFFFFF", False),
}

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)
    for n, v in VARIANTS.items():
        square(n, *v)
    line("line-light", C["charcoal"], C["mom"])
    line("line-dark", C["cotton"], C["leaf_on_dark"])
    print(f"square side {S:.1f} (cap {H}, margin {M:.1f}, block {W_OCT:.1f} x {BLOCK_H:.1f})")
