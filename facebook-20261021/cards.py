"""Facebook product cards for the 7 event SKUs: the How-to poster layout without the no-sew and joining claims.

The shared posters (brand-20261014/posters) still say วิธีต่อ ไม่ต้องเย็บ; the status doc of 21 Oct forbids that claim
until joints pass testing, so these cards relabel it and use the SKU codes from the accounting sheet.
python3 facebook-20261021/cards.py && node brand-20261014/tools/render.mjs facebook-20261021/cards/jobs.json
"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "brand-20261014"))
import brand as B

sp = importlib.util.spec_from_file_location("posters_build", os.path.join(REPO, "brand-20261014", "posters", "build.py"))
PB = importlib.util.module_from_spec(sp); sp.loader.exec_module(PB)

# status doc "OCT. 26 สถานะล่าสุด", 21 Oct: the only SKUs on sale, codes as in the accounting sheet
SKU = {1: "OC-01-01", 22: "OC-01-22", 24: "OC-02-24", 26: "OC-03-26", 27: "OC-04-27", 28: "OC-05-28", 29: "OC-MX-29"}
SALE = [p for p in B.PRODUCTS if p["n"] in SKU]


def card(p):
    html = PB.page(p, 1080, 1350, False)
    for old, new in ((f"HOW TO {p['n']:02d}", SKU[p["n"]]), ("วิธีต่อ ไม่ต้องเย็บ", "วิธีใช้"),
                     ("หนังแท้ · ไม่เย็บ · ไม่ใช้กาว", "หนังวัวแท้ · ทำมือทั้งบ้าน"),
                     ("Shopee OCT. 26", f"Shopee {B.SHOP_NAME}")):
        assert old in html, (p["n"], old)
        html = html.replace(old, new)
    assert "เย็บ" not in html and "กาว" not in html, p["n"]
    return html


if __name__ == "__main__":
    out = os.path.join(HERE, "cards"); os.makedirs(out, exist_ok=True)
    jobs = []
    for p in SALE:
        name = SKU[p["n"]]
        open(os.path.join(out, name + ".html"), "w").write(card(p))
        jobs.append(dict(src=os.path.join(out, name + ".html"), out=os.path.join(out, name + ".png"), w=1080, h=1350))
    json.dump(jobs, open(os.path.join(out, "jobs.json"), "w"), indent=0)
    print(len(jobs), "cards")
