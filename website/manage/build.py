"""The product manager page: the owner edits what website/catalog.json holds, from a phone (claude.ai Artifact).

    python3 website/manage/build.py     # template.html + catalog.json -> index.html, thumbs/ (and prints the publish files)

The page embeds what main's catalog.json says now as its baseline, so republish it after every merge (APPLY.md step 9).
Drafts, new-product requests and send requests live in the page's database; see README.md.
"""
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(HERE)
sys.path.insert(0, WEB)
import catalog as C

URL = "https://claude.ai/artifact/B9RyXagkt8KCB43kaLk3Hd"   # this page: sessions read and republish it
ENV = "env_01WKXaiUwedx7f5o3VCkUxPz"                       # Claude Code environment "OCT.26"
REPO = "https://github.com/baysireekahnokrath/oct.26"
BASE = "main"                                              # Cloudflare deploys main; the owner merges each change into it
WORK = "manage-products"                                   # sessions push here and keep one PR from it to main
FIELDS = ("status", "name", "price", "size", "lead", "uses", "photos", "seo")


def thumbs():
    """240 px squares of every catalog photo -> thumbs/<name>.jpg; returns the publish map for the Artifact tool."""
    os.makedirs(os.path.join(HERE, "thumbs"), exist_ok=True)
    names = sorted({ph for p in C.PRODUCTS for ph in p["photos"]})
    for ph in names:
        out = os.path.join(HERE, "thumbs", ph + ".jpg")
        im = Image.open(os.path.join(WEB, "assets", "img", ph + ".jpg")).convert("RGB")
        s = min(im.size); x, y = (im.width - s) // 2, (im.height - s) // 2
        im.crop((x, y, x + s, y + s)).resize((240, 240), Image.LANCZOS).save(out, quality=82)
    return {f"thumbs/{ph}.jpg": os.path.join(HERE, "thumbs", ph + ".jpg") for ph in names}


if __name__ == "__main__":
    data = dict(
        products=[dict({f: p[f] for f in FIELDS}, id=p["id"], food=p["food"], kind=p["kind"], code=p["code"]) for p in C.PRODUCTS],
        shop=dict(shopee=C.SHOPEE, **{k: C.BOOTH[k] for k in ("fair", "place", "dates", "hours", "until")},
                  shopeeName=C.SHOPEE_NAME, lineId=C.LINE_ID),
        alt=C.ALT, banned=C.BANNED,
        cfg=dict(url=URL, env=ENV, repo=REPO, base=BASE, work=WORK, site=C.SITE))
    files = thumbs()
    tpl = open(os.path.join(HERE, "template.html")).read()
    open(os.path.join(HERE, "index.html"), "w").write(tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)))
    print(json.dumps({k: os.path.relpath(v, HERE) for k, v in files.items()}, ensure_ascii=False))
