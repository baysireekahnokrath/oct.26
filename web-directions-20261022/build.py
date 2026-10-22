"""Six website directions for OCT. 26 (22 Oct 2026), after the owner's six reference boards.

Mock-ups only: website/ and oct26brand.com stay as they are until the owner says "แก้เว็บจริงเลยครับ".
Every direction carries the same content (brand story, 3D piece simulator with leather tones, ready-made products,
corporate orders, workshop booking) in Brand Book v2: cotton and charcoal, family colours as small hidden details,
square logo, Anuphan / Jost / IBM Plex Sans Thai. Follows the shared status doc: 01–05 and 07 (no 06), single pieces
only (no joining, no "no-sew"), no food contact, no products for small children.

Die outlines are read 1:1 (mm) from the cutting files and sampled into polygons for the simulator and the shaped cards.
python3 web-directions-20261022/build.py -> index.html (publish with assets/)
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DIES = {"01": os.path.join(REPO, "diecut-leather-20261014", "svg", "01-bear-head.svg"),
        "02": os.path.join(REPO, "diecut-leather-20261014", "svg", "02-pinwheel-4-lobe.svg"),
        "03": os.path.join(REPO, "diecut-leather-20261014", "svg", "03-capsule-cross.svg"),
        "04": os.path.join(REPO, "diecut-leather-20261014", "svg", "04-rounded-square-diagonal.svg"),
        "05": os.path.join(REPO, "diecut-leather-20261014", "svg", "05-circle.svg"),
        "07": os.path.join(HERE, "src", "07.svg")}           # from diecut-leather-20261019 (brand-guidelines-doc)
NAMES = {"01": "หมี", "02": "กังหัน", "03": "กากบาทแคปซูล", "04": "สี่เหลี่ยมมน", "05": "วงกลม", "07": "กากบาทข้อต่อวงกลม"}


def bez(p0, p1, p2, p3, n=10):
    out = []
    for i in range(1, n + 1):
        t = i / n; u = 1 - t
        out.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return out


def polys(d):
    """Absolute M/L/C/Z paths (the die files use only these) -> list of closed polygons."""
    toks = re.findall(r"[MLCZ]|-?[\d.]+", d)
    out, cur, i, cmd, pt = [], [], 0, None, (0, 0)
    num = lambda: float(toks[i])
    while i < len(toks):
        if toks[i] in "MLCZ":
            cmd = toks[i]; i += 1
            if cmd == "Z":
                if cur: out.append(cur); cur = []
                continue
        if cmd == "M":
            if cur: out.append(cur)
            pt = (float(toks[i]), float(toks[i + 1])); cur = [pt]; i += 2; cmd = "L"
        elif cmd == "L":
            pt = (float(toks[i]), float(toks[i + 1])); cur.append(pt); i += 2
        elif cmd == "C":
            c = [float(t) for t in toks[i:i + 6]]; i += 6
            cur += bez(pt, c[0:2], c[2:4], c[4:6]); pt = (c[4], c[5])
    if cur: out.append(cur)
    return [[(round(x, 2), round(y, 2)) for x, y in p] for p in out]


def shape(code):
    s = open(DIES[code]).read()
    w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    cut = re.search(r'<g id="CUT"[^>]*>(.*?)</g>', s, re.S).group(1)
    ps = []
    for d in re.findall(r'<path d="([^"]+)"', cut):
        ps += polys(d)
    slits = [[float(v) for v in m] for m in
             re.findall(r'<line x1="([\d.-]+)" y1="([\d.-]+)" x2="([\d.-]+)" y2="([\d.-]+)"', s)]
    ps.sort(key=lambda p: -len(p))
    return dict(code=code, name=NAMES[code], w=w, h=h, outline=ps[0], holes=ps[1:], slits=slits)


def logo(name):
    s = open(os.path.join(HERE, "assets", "logo", name + ".svg")).read()
    s = re.sub(r"<title>.*?</title>", "", s)
    s = re.sub(r' width="[\d.]+" height="[\d.]+"', "", s, count=1)
    return s.replace("<svg ", f'<svg class="lg lg-{name}" role="img" aria-label="OCT. 26" ', 1)


if __name__ == "__main__":
    shapes = {c: shape(c) for c in DIES}
    t = open(os.path.join(HERE, "template.html")).read()
    t = (t.replace("/*SHAPES*/{}", json.dumps(shapes, ensure_ascii=False, separators=(",", ":")))
          .replace("{{LOGO_LIGHT}}", logo("square-light")).replace("{{LOGO_DARK}}", logo("square-dark")))
    open(os.path.join(HERE, "index.html"), "w").write(t)
    print("wrote index.html", len(t) // 1024, "KB;", {c: len(s["outline"]) for c, s in shapes.items()})
