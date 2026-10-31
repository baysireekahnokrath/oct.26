"""Build belief/index.html: research on Thai and Chinese belief buying (สายมู), asked by the owner 31 Oct 2026:
"mix belief in: buy to worship, to pay respect, to boost luck; Thai and Chinese beliefs; research deep, both the thinking and what sells."
Facts and sources are in template.html (web search 31 Oct; dbd.go.th and other pages could not be opened from this session).
This script only draws the die pieces as inline SVG from the die files, so the ideas show the real shapes.
python3 belief/build.py -> belief/index.html
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import geom

def path(code, scale=1.0):
    g = geom.load(code); pts = [g["poly"][0]]
    for p in g["poly"][1:]:
        if math.dist(p, pts[-1]) > 0.8: pts.append(p)
    d = "M" + "L".join(f"{x * scale:.1f},{-y * scale:.1f}" for x, y in pts) + "Z"
    cuts = "".join(f'<line x1="{a[0] * scale:.1f}" y1="{-a[1] * scale:.1f}" x2="{b[0] * scale:.1f}" y2="{-b[1] * scale:.1f}"/>' for a, b in g["cuts"])
    return d, cuts

def svg(code, fill, extra="", rot=0, hole=False):
    d, cuts = path(code)
    hole_d = " M-11,-11L-11,11L11,11L11,-11Z" if hole else ""                 # square hole: a Chinese cash coin
    return (f'<svg class="pc" viewBox="-52 -52 104 104" role="img" aria-label="ชิ้น {code}"><g transform="rotate({rot})">'
            f'<path d="{d}{hole_d}" fill="{fill}" fill-rule="evenodd" stroke="rgba(0,0,0,.25)" stroke-width=".8"/>'
            f'<g stroke="rgba(0,0,0,.45)" stroke-width="1">{cuts}</g>{extra}</g></svg>')

SUB = {
    "__P02__": svg("02", "#A9442B", rot=12),
    "__P05COIN__": svg("05", "#C9A15A", hole=True),
    "__P07__": svg("07", "#5E7A3A"),
    "__P05__": svg("05", "#2E4A7D"),
}
PAGE = open(os.path.join(HERE, "template.html")).read()
for k, v in SUB.items(): PAGE = PAGE.replace(k, v)
open(os.path.join(HERE, "index.html"), "w").write(PAGE)
print("belief/index.html", len(PAGE), "bytes")
