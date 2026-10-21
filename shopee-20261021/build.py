"""Fill Shopee's mass upload template (basic, 21 Oct 2026) with OCT. 26 products from brand.py.

openpyxl cannot open Shopee's file (sheetView activePane="bottom_left" is invalid), so rows are written straight into
xl/worksheets/sheet2.xml (form "แบบฟอร์มการลงสินค้า", data from row 7) and every other part is copied byte for byte.
python3 shopee-20261021/build.py -> oct26-shopee-ready.xlsx (READY + EXTRA) and oct26-shopee-prototype.xlsx (PROTO);
products using a piece in HOLD_PIECES are left out of both.
"""
import os, re, sys, zipfile
from xml.sax.saxutils import escape
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "brand-20261014"))
import brand as B

TEMPLATE = os.path.join(HERE, "template.xlsx")
IMG = "https://" + B.SOCIAL["web"] + "/assets/posters/{:02d}.png"   # How-to posters on the live site, 1080x1350, < 120 KB
SHOPEE_STOCK = 5          # booth and Shopee share stock until 1 Nov; raise in Seller Centre after the fair
HEAVY = {11, 13, 21, 29, 30}  # sets and large pieces, 0.2 kg packed; the rest 0.1 kg
HOLD_PIECES = {"02"}      # owner, 21 Oct: piece 02 (กังหัน) is not usable yet, so no product with it goes to Shopee


def row(p):
    title, desc = B.shopee(p)
    assert 20 <= len(title) <= 120 and 60 <= len(desc) <= 5000, p["n"]
    sku = f"OCT26-{p['n']:02d}"
    return {"B": title, "C": desc, "I": sku, "P": str(p["price"]), "Q": str(min(p["stock"], SHOPEE_STOCK)),
            "R": sku, "V": IMG.format(p["n"]), "AE": "0.2" if p["n"] in HEAVY else "0.1", "AI": "เปิด"}


def col_index(c):
    n = 0
    for ch in c:
        n = n * 26 + ord(ch) - 64
    return n


def build(products, out):
    z = zipfile.ZipFile(TEMPLATE)
    sheet = z.read("xl/worksheets/sheet2.xml").decode()
    shared = z.read("xl/sharedStrings.xml").decode()
    styles = {int(a): s for a, b, s in re.findall(r'<col [^>]*max="(\d+)" min="(\d+)" style="(\d+)"', sheet) if a == b}
    count = int(re.search(r'uniqueCount="(\d+)"', shared).group(1))
    new_si, rows = [], []
    for r, p in enumerate(products, start=7):
        cells = []
        for c, v in sorted(row(p).items(), key=lambda kv: col_index(kv[0])):
            new_si.append(f'<si><t xml:space="preserve">{escape(v)}</t></si>')
            cells.append(f'<c r="{c}{r}" s="{styles.get(col_index(c), 0)}" t="s"><v>{count + len(new_si) - 1}</v></c>')
        rows.append(f'<row r="{r}">{"".join(cells)}</row>')
    last = 6 + len(products)
    sheet = sheet.replace("</sheetData>", "".join(rows) + "</sheetData>", 1)
    sheet = sheet.replace('<dimension ref="A1">', f'<dimension ref="A1:AK{last}">', 1)
    total = count + len(new_si)
    shared = re.sub(r'count="\d+" uniqueCount="\d+"', f'count="{total}" uniqueCount="{total}"', shared, count=1)
    shared = shared.replace("</sst>", "".join(new_si) + "</sst>")
    with zipfile.ZipFile(out, "w") as o:
        for info in z.infolist():
            data = z.read(info.filename)
            if info.filename == "xl/worksheets/sheet2.xml":
                data = sheet.encode()
            elif info.filename == "xl/sharedStrings.xml":
                data = shared.encode()
            o.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED)
    print(f"wrote {os.path.basename(out)}: {len(products)} products, rows 7-{last}")


def split():
    held = [p for p in B.PRODUCTS if HOLD_PIECES & {c for c, _ in p["parts"]}]
    rest = [p for p in B.PRODUCTS if p not in held]
    return [p for p in rest if p["status"] != B.PROTO], [p for p in rest if p["status"] == B.PROTO], held


if __name__ == "__main__":
    ready, proto, held = split()
    build(ready, os.path.join(HERE, "oct26-shopee-ready.xlsx"))
    build(proto, os.path.join(HERE, "oct26-shopee-prototype.xlsx"))
