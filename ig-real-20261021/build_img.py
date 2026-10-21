"""Crop the owner's photos (21 Oct, Drive folder 1SK8GUSby1iGN7UpnX2r49ui7F9kCCkeP) to 1080x1350 for Instagram.

Only light edits: neutral white balance from the paper, a little contrast, 4:5 crop. No retouching of the leather.
"""
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import os
HERE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    return ImageOps.exif_transpose(Image.open(os.path.join(HERE, "src", f"IMG_20261021_{name}.jpg"))).convert("RGB")

def balance(im):
    a = np.asarray(im).astype(np.float32)
    lum = a.mean(2); sat = a.max(2) - a.min(2)
    paper = (lum > np.percentile(lum, 70)) & (sat < 40)
    ref = np.median(a[paper], axis=0)
    target = np.array([246, 244, 240], np.float32)        # warm white paper
    a = np.clip(a * (target / ref), 0, 255).astype(np.uint8)
    im = Image.fromarray(a)
    return ImageEnhance.Contrast(im).enhance(1.06)

def pieces_box(im):
    a = np.asarray(im.resize((im.width // 8, im.height // 8))).astype(np.int16)
    lum = a.mean(2); sat = a.max(2) - a.min(2)
    paper = (lum > 200) & (sat < 30)
    rows = np.where(paper.mean(1) > .25)[0]; cols = np.where(paper.mean(0) > .25)[0]
    py0, py1, px0, px1 = rows[0], rows[-1], cols[0], cols[-1]          # the sheet of paper
    sub = ~paper[py0:py1, px0:px1]
    ys, xs = np.where(sub)
    # trim stray dark pixels at the paper edge
    y0, y1 = np.percentile(ys, [1, 99]); x0, x1 = np.percentile(xs, [1, 99])
    return [int(v * 8) for v in (px0 + x0, py0 + y0, px0 + x1, py0 + y1, px0, py0, px1, py1)]

def crop45(im, box, pad=0.08, zoom=1.0):
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) * (1 + pad * 2) / zoom, (y1 - y0) * (1 + pad * 2) / zoom
    if w / h > 0.8: h = w / 0.8
    else: w = h * 0.8
    if w > im.width: w, h = im.width, im.width / 0.8
    if h > im.height: w, h = im.height * 0.8, im.height
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    l = min(max(cx - w / 2, 0), im.width - w); t = min(max(cy - h / 2, 0), im.height - h)
    return im.crop((int(l), int(t), int(l + w), int(t + h))).resize((1080, 1350), Image.LANCZOS)

CREAM = (255, 246, 236)   # brand paper colour, the frame around group shots

def framed(im, b, inset=0.025):
    """Group shots stay whole: the sheet of paper with the pieces, set on a cream 4:5 page like a print."""
    px0, py0, px1, py1 = b[4:]
    dx, dy = (px1 - px0) * inset, (py1 - py0) * inset
    photo = im.crop((int(px0 + dx), int(py0 + dy), int(px1 - dx), int(py1 - dy)))
    w = 960; h = round(w * photo.height / photo.width)
    page = Image.new("RGB", (1080, 1350), CREAM)
    page.paste(photo.resize((w, h), Image.LANCZOS), (60, (1350 - h) // 2))
    return page

# name, how: "auto" fits the pieces, or an explicit (x0, y0, x1, y1) box in pixels
SHOTS = [   # in posting order
    ("01", "193050", "auto"),                      # four bears
    ("02", "194442", "full"),                      # a circle in the hand
    ("03", "194139", "auto"),                      # seven pinwheels (02)
    ("04", "194139", (1130, 300, 2970, 2600)),     # close: the middle of the pinwheels
    ("05", "193726", "auto"),                      # six rounded squares
    ("06", "193050", (2300, 1500, 3500, 3000)),    # close: the taupe bear, for 26 October
    ("07", "194432", "auto"),                      # six circles
    ("08", "193425", "auto"),                      # six round-joint crosses (07, still being tried)
    ("09", "194501", "auto"),                      # three circles
]

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "img"), exist_ok=True)
    for out, src, how in SHOTS:
        im = balance(load(src))
        if how == "auto":
            im2 = framed(im, pieces_box(im))
        elif how == "full":
            im2 = crop45(im, (0, 0, im.width, im.height), pad=0)
        else:
            im2 = crop45(im, how, pad=0)
        im2.save(os.path.join(HERE, "img", f"{out}.jpg"), quality=90)
        print(out, src, im.size)
