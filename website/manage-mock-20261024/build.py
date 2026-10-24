"""Mock of the product manager page (24 Oct 2026): the owner edits what website/catalog.py holds from a phone.

    python3 website/manage-mock-20261024/build.py     # template.html + catalog.py -> index.html, thumbs/

The mock keeps drafts in the viewer's browser only and sends nothing; the real page would save them in the artifact's
database and hand them to a Claude session that edits catalog.py and opens a PR (see README.md).
"""
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(HERE)
sys.path.insert(0, WEB)
import catalog as C

os.makedirs(os.path.join(HERE, "thumbs"), exist_ok=True)
photos = sorted({ph for p in C.PRODUCTS for ph in p["photos"]})
for ph in photos:
    im = Image.open(os.path.join(WEB, "assets", "img", ph + ".jpg")).convert("RGB")
    s = min(im.size); x, y = (im.width - s) // 2, (im.height - s) // 2
    im.crop((x, y, x + s, y + s)).resize((240, 240), Image.LANCZOS).save(os.path.join(HERE, "thumbs", ph + ".jpg"), quality=82)

data = dict(
    products=[dict(id=p["id"], name=p["name"], seo=p["seo"], price=p["price"], size=p["size"], lead=p["lead"],
                   uses=p["uses"], photos=p["photos"], food=p["food"], kind=p["kind"], code=p["code"], status="on")
              for p in C.PRODUCTS],
    shop=dict(fair=C.BOOTH["fair"], place=C.BOOTH["place"], dates=C.BOOTH["dates"], hours=C.BOOTH["hours"],
              until=C.BOOTH["until"], shopee="", shopeeName=C.SHOPEE_NAME, lineId=C.LINE_ID),
    alt=C.ALT)
tpl = open(os.path.join(HERE, "template.html")).read()
open(os.path.join(HERE, "index.html"), "w").write(tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)))
print("mock ->", os.path.join(HERE, "index.html"), "+", len(photos), "thumbs")
