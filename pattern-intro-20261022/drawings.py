"""Clean pattern drawings for every medium (22 Oct 2026): the real die outline at 1:1 mm, slits included.

line  = charcoal outline on clear background (print, web, guides)
solid = hide-brown shape with cotton slits (icons, stickers, small sizes)

python3 drawings.py -> drawings/pattern-<n>-<name>-line.svg and -solid.svg
"""
import os
from build import HERE, PATTERNS, C, die

NAMES = {"01": "bear", "02": "pinwheel", "03": "capsule-cross", "04": "rounded-square", "05": "circle", "07": "round-joint-cross"}


def svg(code, kind):
    w, h, cut, sl = die(code)
    title = next(f"{p[0]} {p[1]} {p[2]}" for p in PATTERNS if p[0] == code)
    if kind == "line":
        body = (f'<g fill="none" stroke="{C["charcoal"]}" stroke-width="0.5" stroke-linejoin="round">{cut}</g>'
                f'<g fill="none" stroke="{C["charcoal"]}" stroke-width="0.5" stroke-linecap="round">{sl}</g>')
    else:
        body = (f'<g fill="{C["hide"]}" fill-rule="evenodd" stroke="none">{cut}</g>'
                f'<g fill="none" stroke="{C["cotton"]}" stroke-width="0.8" stroke-linecap="round">{sl}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="-0.5 -0.5 {w + 1} {h + 1}">'
            f'<title>OCT. 26 pattern {title} - {w:.0f} x {h:.0f} mm</title>{body}</svg>\n')


if __name__ == "__main__":
    out = os.path.join(HERE, "drawings")
    os.makedirs(out, exist_ok=True)
    for code, n in NAMES.items():
        for kind in ("line", "solid"):
            open(os.path.join(out, f"pattern-{code}-{n}-{kind}.svg"), "w").write(svg(code, kind))
    print(sorted(os.listdir(out)))
