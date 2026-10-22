"""Pattern play mock-up: drag the six real leather pieces onto an 18 x 18 cm tile, turn them, colour them,
and see the tile repeat as a pattern. Mock-up for the customer website, tried as a claude.ai page first.

Piece outlines and slits come from the die files in ../diecut-leather-20261014/svg (1:1, mm), names from brand.py.
python3 play-20261021/build.py -> site/index.html (template: play.html)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "brand-20261014"))
import brand as B

DIES = os.path.join(REPO, "diecut-leather-20261014", "svg")
FILES = {"01": "01-bear-head.svg", "02": "02-pinwheel-4-lobe.svg", "03": "03-capsule-cross.svg",
         "04": "04-rounded-square-diagonal.svg", "05": "05-circle.svg", "06": "06-soft-cross.svg",
         "07": "../../diecut-leather-20261019/svg/07-round-joint-cross.svg"}


def shape(code):
    s = open(os.path.join(DIES, FILES[code])).read()
    w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    cut = re.search(r'<g id="CUT"[^>]*>(.*?)</g>', s, re.S).group(1)
    paths = re.findall(r'<path d="([^"]+)"', cut)
    slits = [[float(v) for v in m] for m in
             re.findall(r'<line x1="([\d.-]+)" y1="([\d.-]+)" x2="([\d.-]+)" y2="([\d.-]+)"', s)]
    return dict(code=code, name=B.PIECE_NAME[code].rsplit(" ", 1)[0], w=w, h=h, d=" ".join(paths), slits=slits)


if __name__ == "__main__":
    shapes = [shape(c) for c in FILES]
    html = open(os.path.join(HERE, "play.html")).read()
    html = html.replace("/*SHAPES*/[]", json.dumps(shapes, ensure_ascii=False))
    os.makedirs(os.path.join(HERE, "site"), exist_ok=True)
    open(os.path.join(HERE, "site", "index.html"), "w").write(html)
    print("wrote site/index.html with", len(shapes), "pieces")
