"""Put a photo the owner uploaded on the product manager page into the site: at most 1600 px, JPEG.

    python3 website/manage/photo.py <downloaded file> <name>    # -> website/assets/img/<name>.jpg

<name> is lowercase letters, digits and dashes, e.g. oc-04-27-2. The caller then puts <name> where "asset:<id>"
was in the request's photos and writes the photo's Thai description into the request's alt (see APPLY.md).
"""
import os, re, sys
from PIL import Image, ImageOps

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")

if __name__ == "__main__":
    src, name = sys.argv[1], sys.argv[2]
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", name): raise SystemExit("ชื่อรูปใช้ตัวเล็ก ตัวเลข และขีด")
    out = os.path.join(IMG, name + ".jpg")
    if os.path.exists(out): raise SystemExit(f"มีรูปชื่อ {name} แล้ว")
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((1600, 1600), Image.LANCZOS)
    im.save(out, quality=86, optimize=True)
    print(out, im.size)
