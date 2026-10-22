"""Die-cut the real leather pieces out of the 21 Oct photos and retouch them (22 Oct 2026).

Light and colour come from the white paper the pieces lie on: the paper is measured across the whole frame,
its uneven light is divided out (flat field) and it is set to neutral white, so leather colour is true to the eye.
Each piece is then cut out with GrabCut seeded from its difference to the paper, edges smoothed, and saved as
a transparent PNG at full resolution.

python3 cutout.py -> cut/<pattern>-<n>.png (no photo of 02 yet), check/<photo>.jpg (mask outlines for checking)
"""
import os, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW, CUT, CHECK = (os.path.join(HERE, d) for d in ("raw", "cut", "check"))
PHOTOS = {  # photo -> pattern
    "IMG_20261021_193050.jpg": "01",
    "IMG_20261021_194139.jpg": "03",
    "IMG_20261021_193425.jpg": "07",
    "IMG_20261021_193726.jpg": "04",
    "IMG_20261021_193754.jpg": "04",
    "IMG_20261021_194432.jpg": "05",
    "IMG_20261021_194501.jpg": "05",
}
QUAD = {  # paper corners (x, y as fractions) where the sheet is not found on its own
    "IMG_20261021_194139.jpg": [(0.039, 0.117), (0.889, 0.085), (0.935, 0.905), (0.0, 0.875), (0.0, 0.42)],
}
LONG = 3000          # working size, long edge px
PAPER = 244.0        # paper level after correction (0-255)


def load(name):
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(os.path.join(RAW, name))).convert("RGB")
    s = LONG / max(im.size)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    return cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)


def paper_mask(img, name):
    """The A4 sheet: biggest bright, low-saturation region with its holes (the pieces) filled."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if name in QUAD:
        h, w = img.shape[:2]
        m = np.zeros((h, w), np.uint8)
        cv2.fillPoly(m, [np.array([(x * w, y * h) for x, y in QUAD[name]], np.int32)], 1)
        m = cv2.erode(m, np.ones((25, 25), np.uint8))
        return m, (m > 0) & (hsv[..., 1] < 60) & (hsv[..., 2] > np.percentile(hsv[..., 2][m > 0], 50) * 0.8)
    bright = ((hsv[..., 2] > np.percentile(hsv[..., 2], 60) * 0.9) & (hsv[..., 1] < 45)).astype(np.uint8)
    bright = cv2.morphologyEx(bright, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(bright)
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
    cnt, _ = cv2.findContours((lab == k).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    m = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(m, [max(cnt, key=cv2.contourArea)], -1, 1, cv2.FILLED)  # paper plus the pieces lying on it
    return cv2.erode(m, np.ones((25, 25), np.uint8)), (lab == k)


def flat_field(img, clean_paper):
    """Divide out the paper's light so the paper is even, neutral white."""
    small = 8
    h, w = img.shape[:2]
    sm = cv2.resize(img, (w // small, h // small), interpolation=cv2.INTER_AREA).astype(np.float32)
    pm = cv2.resize(clean_paper.astype(np.uint8), (w // small, h // small), interpolation=cv2.INTER_NEAREST)
    pm = cv2.erode(pm, np.ones((5, 5), np.uint8))
    illum = np.zeros_like(sm)
    for c in range(3):
        ch = sm[..., c].copy()
        fill = cv2.inpaint(np.clip(ch, 0, 255).astype(np.uint8), (1 - pm).astype(np.uint8), 15, cv2.INPAINT_TELEA).astype(np.float32)
        illum[..., c] = cv2.GaussianBlur(fill, (0, 0), 12)
    illum = cv2.resize(illum, (w, h), interpolation=cv2.INTER_CUBIC)
    out = img.astype(np.float32) / np.maximum(illum, 1) * PAPER
    return np.clip(out, 0, 255).astype(np.uint8)


def pieces_mask(img, inside, clean):
    """Leather vs paper: Lab distance to paper white (cream leather is yellower), then GrabCut."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    ref = np.median(lab[clean & (inside > 0)].reshape(-1, 3), axis=0)
    d = lab - ref
    de = np.sqrt((d[..., 0] * 0.5) ** 2 + (d[..., 1] * 1.6) ** 2 + (d[..., 2] * 1.6) ** 2)
    fg = ((de > 9) & (inside > 0)).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    fg = fill_holes(fg)
    gc = np.full(fg.shape, cv2.GC_BGD, np.uint8)
    near = cv2.dilate(fg, np.ones((41, 41), np.uint8))
    gc[near > 0] = cv2.GC_PR_BGD
    gc[fg > 0] = cv2.GC_PR_FGD
    gc[cv2.erode(fg, np.ones((31, 31), np.uint8)) > 0] = cv2.GC_FGD
    bgm, fgm = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(img, gc, None, bgm, fgm, 4, cv2.GC_INIT_WITH_MASK)
    m = np.isin(gc, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    return split(fill_holes(m & inside), inside)


def split(m, inside):
    """Label pieces; pieces lying against each other are parted by watershed on the distance to the paper.
    Pieces touching the paper's edge (running off it) are dropped."""
    dt = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    n0, lab0 = cv2.connectedComponents(m)
    markers = np.zeros(m.shape, np.int32)
    k = 0
    for i in range(1, n0):
        blob = lab0 == i
        if blob.sum() < 2000:
            continue
        peak = dt[blob].max()
        n1, l1 = cv2.connectedComponents(((dt > 0.6 * peak) & blob).astype(np.uint8))
        for j in range(1, n1):
            k += 1
            markers[l1 == j] = k
    from skimage.segmentation import watershed
    ws = watershed(-dt, markers, mask=m > 0)
    out = np.zeros(m.shape, np.int32)
    rim = cv2.dilate(inside, np.ones((3, 3), np.uint8)) - cv2.erode(inside, np.ones((15, 15), np.uint8))
    n = 0
    for j in range(1, k + 1):
        piece = cv2.morphologyEx(((ws == j) & (m > 0)).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        if piece.sum() < 2000 or (piece & rim).any():
            continue
        n += 1
        out[piece > 0] = n
    return out


def drop_edge(m, inside):
    """Remove blobs that touch the paper's edge: the paper border and pieces running off it."""
    rim = cv2.dilate(inside, np.ones((3, 3), np.uint8)) - cv2.erode(inside, np.ones((15, 15), np.uint8))
    n, lab = cv2.connectedComponents(m)
    bad = np.unique(lab[(rim > 0) & (m > 0)])
    return (m > 0) & ~np.isin(lab, bad[bad > 0])


def fill_holes(m):
    cnt, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = np.zeros_like(m)
    cv2.drawContours(out, cnt, -1, 1, cv2.FILLED)
    return out


def smooth_alpha(m):
    """Soft, clean die edge: blur the hard mask a little and re-threshold, then a 1 px feather."""
    f = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 3)
    hard = (f > 0.5).astype(np.float32)
    return cv2.GaussianBlur(hard, (0, 0), 0.9)


def retouch(img):
    """Gentle: lift shadows slightly and add a touch of local contrast; colours stay as measured."""
    x = img.astype(np.float32) / 255
    x = x + 0.06 * x * (1 - x) * 2          # soft mid lift
    blur = cv2.GaussianBlur(x, (0, 0), 6)
    x = x + 0.25 * (x - blur)               # clarity for the grain
    return np.clip(x * 255, 0, 255).astype(np.uint8)


def run():
    for d in (CUT, CHECK):
        os.makedirs(d, exist_ok=True)
    count = {}
    for name, pat in PHOTOS.items():
        img = load(name)
        inside, clean = paper_mask(img, name)
        img = flat_field(img, clean & (inside > 0))
        lab = pieces_mask(img, inside, clean)
        n, _, st, _ = cv2.connectedComponentsWithStats((lab > 0).astype(np.uint8))
        st = np.array([[0] * 5] + [list(cv2.boundingRect((lab == i).astype(np.uint8))) + [int((lab == i).sum())] for i in range(1, lab.max() + 1)])
        areas = st[1:, cv2.CC_STAT_AREA]
        big = [i + 1 for i, a in enumerate(areas) if a > 0.25 * areas.max()]
        chk = img.copy()
        rt = retouch(img)
        for i in sorted(big, key=lambda i: (st[i, cv2.CC_STAT_TOP] // 400, st[i, cv2.CC_STAT_LEFT])):
            x, y, w, h = st[i, :4]
            pad = 12
            x0, y0 = max(x - pad, 0), max(y - pad, 0)
            x1, y1 = min(x + w + pad, img.shape[1]), min(y + h + pad, img.shape[0])
            a = smooth_alpha((lab[y0:y1, x0:x1] == i).astype(np.uint8))
            rgb = cv2.cvtColor(rt[y0:y1, x0:x1], cv2.COLOR_BGR2RGB)
            count[pat] = count.get(pat, 0) + 1
            out = np.dstack([rgb, (a * 255).astype(np.uint8)])
            from PIL import Image
            Image.fromarray(out, "RGBA").save(os.path.join(CUT, f"{pat}-{count[pat]}.png"), optimize=True)
            cnt, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(chk, cnt, -1, (0, 0, 255), 4)
            cv2.putText(chk, f"{pat}-{count[pat]}", (x + 20, y + 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 6)
        cv2.imwrite(os.path.join(CHECK, name), cv2.resize(chk, None, fx=0.4, fy=0.4), [cv2.IMWRITE_JPEG_QUALITY, 80])
        print(name, pat, len(big))


if __name__ == "__main__":
    run()
