"""Brand card for the bag, 63 x 63 mm, twelve per A4, two-sided (owner, 22 Oct: no side over 7 cm).

Square like the logo. Front: square-family logo and "our crafted things."; back: LINE QR, IG and FB, the five family
colours as a band (Brand Book v2: the card in the bag has the family colours on the back). The grid is centred, so the
back lines up when the printer flips on the long edge; every card is the same, so mirroring does not matter.
python3 print-20261022/card.py && node print-20261022/render.mjs card.html oct26-brand-card.pdf
"""
import os
import build as P

E = P.E
W, COLS, ROWS = 63, 3, 4
X0, Y0 = (210 - COLS * W) / 2, (297 - ROWS * W) / 2           # 10.5, 22.5 mm: inside what home printers print
XS = tuple(X0 + k * W for k in range(COLS + 1))
YS = tuple(Y0 + k * W for k in range(ROWS + 1))


def front():
    return (f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3.5mm">'
            f'{P.logo(36, "square-family")}<span class="jl" style="font-size:3.6mm">our crafted things.</span></div>')


def back():
    return (f'<div style="position:absolute;inset:6mm;display:flex;flex-direction:column;justify-content:space-between">'
            f'<div style="display:flex;gap:3.5mm;align-items:center">{P.line_qr(25)}'
            f'<div style="display:flex;flex-direction:column;gap:1.3mm;font-size:2.7mm;line-height:1.25">'
            f'<b style="font-size:3.2mm">ติดตามเรา</b>'
            f'<span><span class="jost">LINE</span><br><span class="jl">{P.LINE_ID}</span></span>'
            f'<span><span class="jost">IG</span><br><span class="jl">@{P.H}</span></span>'
            f'<span><span class="jost">FB</span><br><span class="jl">oct26brand</span></span></div></div>'
            f'<div style="display:flex;flex-direction:column;gap:1.8mm">{P.band(2.2)}'
            f'<span style="font-size:2.9mm">ห้าคน ห้าสี ทำกันเองทั้งบ้าน</span></div></div>')


def sheet(face):
    cells = "".join(f'<div class="cell" style="left:{X0 + c * W}mm;top:{Y0 + r * W}mm;width:{W}mm;height:{W}mm">{face()}</div>'
                    for r in range(ROWS) for c in range(COLS))
    return f'<div class="page">{cells}{P.marks(XS, YS, inset=3, length=6)}</div>'


if __name__ == "__main__":
    body = sheet(front) + sheet(back)
    open(os.path.join(P.HERE, "card.html"), "w").write(
        f'<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{P.CSS}</style></head><body>{body}</body></html>')
    print("wrote card.html, 2 pages,", COLS * ROWS, "cards per sheet")
