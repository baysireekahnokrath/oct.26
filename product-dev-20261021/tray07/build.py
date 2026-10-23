"""Build tray07/index.html: the owner's tray idea (23 Oct) in 3D, every piece a 07 die.

Owner: base 2 x 4 pieces, the rim two pieces high, then fold back and tuck so it ends one tier high.
How the model reads that, from the 07 die itself (cross3d/geom.py):
  * a joint sits 28.43 mm from a piece's centre, so joined pieces are 56.86 mm apart, each turned 90 deg from its
    neighbour so that a wing always meets a slit; the flat pattern is therefore a plus-shaped grid at that pitch:
    base 4 x 2, two rows on each long side, two columns on each short side, 32 pieces;
  * lifting the rim turns the base's outer joints into 90 deg tab-in-slit joints, and the rim corners meet the same way;
  * the second rim row folds 180 deg into the tray about the joint line between the rows, its far wings reaching the base.
python3 tray07/build.py -> tray07/index.html
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "cross3d"))
import geom

G = geom.load("07")
pts = [G["poly"][0]]
for p in G["poly"][1:]:
    if math.dist(p, pts[-1]) > 0.6: pts.append(p)
JOINT = 28.43                         # slit and wing neck, from the piece centre (die 07, 19 Oct)
P = round(2 * JOINT, 2)               # 56.86 mm between joined pieces
COLS, ROWS, RIM = 4, 2, 2
N_BASE, N_RIM = COLS * ROWS, 2 * (COLS + ROWS) * RIM
N = N_BASE + N_RIM
COST_07, STOCK_07 = 3.45, 200         # sheet, 22 Oct
inner_l, inner_w = (COLS - 1) * P + 2 * JOINT, (ROWS - 1) * P + 2 * JOINT
DATA = dict(poly=[[round(x, 2), round(y, 2)] for x, y in pts], cuts=[[list(a), list(b)] for a, b in G["cuts"]],
            P=P, J=JOINT, cols=COLS, rows=ROWS)

# flat pattern (top view), the net before the rim is lifted
def net_cells():
    xs = [(i - (COLS - 1) / 2) * P for i in range(COLS)]
    ys = [(j - (ROWS - 1) / 2) * P for j in range(ROWS)]
    cells = [(x, y, "base") for x in xs for y in ys]
    for r in range(RIM):
        off = (ROWS - 1) / 2 * P + (r + 1) * P
        cells += [(x, s * off, f"rim{r}") for x in xs for s in (-1, 1)]
        off = (COLS - 1) / 2 * P + (r + 1) * P
        cells += [(s * off, y, f"rim{r}") for y in ys for s in (-1, 1)]
    return cells

path = "M" + " L".join(f"{x:.1f},{-y:.1f}" for x, y in pts) + "Z"
cells = net_cells()
ext_x = max(abs(c[0]) for c in cells) + 46; ext_y = max(abs(c[1]) for c in cells) + 46
FILL = {"base": "var(--leather-a)", "rim0": "var(--leather-b)", "rim1": "var(--leather-c)"}
net = []
for x, y, kind in cells:
    gx, gy = round(x / P + (COLS - 1) / 2), round(y / P + (ROWS - 1) / 2)     # grid cell; neighbours turn 90 deg
    rot = 90 if (gx + gy) % 2 else 0
    net.append(f'<g transform="translate({x:.1f} {-y:.1f}) rotate({rot})"><path d="{path}" class="pc" style="fill:{FILL[kind]}"/>'
               + "".join(f'<line x1="{a[0]}" y1="{-a[1]}" x2="{b[0]}" y2="{-b[1]}" class="cut"/>' for a, b in G["cuts"]) + "</g>")
NET = (f'<svg class="net" viewBox="{-ext_x:.0f} {-ext_y:.0f} {2 * ext_x:.0f} {2 * ext_y:.0f}" role="img" '
       f'aria-label="แพตเทิร์นคลี่แบนของถาด 07 จำนวน {N} ชิ้น">{"".join(net)}'
       f'<rect x="{-(COLS - 1) / 2 * P - JOINT:.1f}" y="{-(ROWS - 1) / 2 * P - JOINT:.1f}" width="{inner_l:.1f}" height="{inner_w:.1f}" class="fold"/>'
       f'</svg>')

PAGE = open(os.path.join(HERE, "template.html")).read()
for k, v in {"__DATA__": json.dumps(DATA, separators=(",", ":")), "__NET__": NET, "__N__": str(N), "__NBASE__": str(N_BASE),
             "__NRIM__": str(N_RIM), "__NRIMROW__": str(N_RIM // RIM), "__INNER__": f"{inner_l / 10:.1f} × {inner_w / 10:.1f}",
             "__WALL__": f"{P / 10:.1f}", "__PITCH__": f"{P:.2f}", "__COST__": f"{N * COST_07:.0f}", "__MAKE__": str(STOCK_07 // N),
             "__LOBE__": f"{(45 - JOINT) / 10:.1f}"}.items():
    PAGE = PAGE.replace(k, v)
open(os.path.join(HERE, "index.html"), "w").write(PAGE)
print("tray07/index.html", len(PAGE), "bytes ·", N, "pieces · inside", f"{inner_l:.1f} x {inner_w:.1f} mm")
