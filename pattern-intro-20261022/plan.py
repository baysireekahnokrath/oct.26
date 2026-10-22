"""Straighten the die-cut pieces to a plan (top-down) view at true scale (22 Oct 2026).

The photos were taken at a slight angle, so circles came out as ovals. Each cut piece is mapped back to its real
shape with one affine transform: its spread (second moments of the alpha mask) is made equal to that of the die
outline, with no extra rotation, and its area to the die's area at SCALE px per mm. All pieces then share one scale,
so 01 (104 mm) shows larger than the 90 mm patterns, as in real life. Squares (04) get a full perspective fit
of their four corners instead, which also squares them up.

python3 plan.py -> plan/<pattern>-<n>.png (and plan-web/*.webp); cut/ stays as it was
"""
import glob, io, os, re
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCALE = 12  # px per mm
DIE = {"01": "diecut-leather-20261014/svg/01-bear-head.svg", "02": "diecut-leather-20261014/svg/02-pinwheel-4-lobe.svg",
       "03": "diecut-leather-20261014/svg/03-capsule-cross.svg", "04": "diecut-leather-20261014/svg/04-rounded-square-diagonal.svg",
       "05": "diecut-leather-20261014/svg/05-circle.svg", "07": "diecut-leather-20261019/svg/07-round-joint-cross.svg"}


def die_mask(code):
    import cairosvg
    s = open(os.path.join(ROOT, DIE[code])).read()
    w, h = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    cut = re.search(r'<g id="CUT"[^>]*>(.*?)</g>', s, re.S).group(1)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w * SCALE}" height="{h * SCALE}">'
           f'<g fill="#000" fill-rule="evenodd" stroke="none">{cut}</g></svg>')
    png = cairosvg.svg2png(bytestring=svg.encode())
    a = np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"))[..., 3]
    return (a > 127).astype(np.float64)


def moments(m):
    ys, xs = np.nonzero(m > 0.5)
    pts = np.stack([xs, ys], 1).astype(np.float64)
    c = pts.mean(0)
    cov = np.cov((pts - c).T)
    return c, cov, len(pts)


def sqrtm(c, inv=False):
    w, v = np.linalg.eigh(c)
    w = np.power(w, -0.5 if inv else 0.5)
    return (v * w) @ v.T


def straighten(img, target_cov):
    """Affine map: piece covariance -> die covariance (symmetric, so no added rotation)."""
    a = img[..., 3].astype(np.float64) / 255
    c, cov, _ = moments(a)
    A = sqrtm(target_cov) @ sqrtm(cov, inv=True)
    corners = np.array([[0, 0], [img.shape[1], 0], [0, img.shape[0]], [img.shape[1], img.shape[0]]], np.float64)
    p = (corners - c) @ A.T
    lo, hi = p.min(0) - 8, p.max(0) + 8
    size = np.ceil(hi - lo).astype(int)
    M = np.hstack([A, (-A @ c - lo)[:, None]])
    # premultiplied alpha keeps the edge clean while resampling
    rgb = img[..., :3].astype(np.float32) * (img[..., 3:4].astype(np.float32) / 255)
    pm = np.dstack([rgb, img[..., 3].astype(np.float32)])
    out = cv2.warpAffine(pm, M, (int(size[0]), int(size[1])), flags=cv2.INTER_LANCZOS4, borderValue=0)
    al = np.clip(out[..., 3], 0, 255)
    col = np.where(al[..., None] > 0, out[..., :3] / np.maximum(al[..., None], 1e-3) * 255, 0)
    return np.dstack([np.clip(col, 0, 255), al]).astype(np.uint8)


def quad(mask):
    """Four corner points of a (rounded) square outline, ordered TL, TR, BR, BL."""
    cnt, _ = cv2.findContours((mask > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cnt, key=cv2.contourArea)
    peri = cv2.arcLength(c, True)
    for eps in np.linspace(0.01, 0.1, 40):
        q = cv2.approxPolyDP(c, eps * peri, True)
        if len(q) == 4:
            break
    q = q.reshape(4, 2).astype(np.float32)
    s, d = q.sum(1), np.diff(q, axis=1).ravel()
    return np.array([q[np.argmin(s)], q[np.argmin(d)], q[np.argmax(s)], q[np.argmax(d)]], np.float32)


def square_up(img, die):
    """04 only: a perspective (homography) fit of the four corners onto the die square."""
    src = quad(img[..., 3].astype(np.float64) / 255)
    dst = quad(die) + 10
    H = cv2.getPerspectiveTransform(src, dst)
    size = (die.shape[1] + 20, die.shape[0] + 20)
    rgb = img[..., :3].astype(np.float32) * (img[..., 3:4].astype(np.float32) / 255)
    pm = np.dstack([rgb, img[..., 3].astype(np.float32)])
    out = cv2.warpPerspective(pm, H, size, flags=cv2.INTER_LANCZOS4, borderValue=0)
    al = np.clip(out[..., 3], 0, 255)
    col = np.where(al[..., None] > 0, out[..., :3] / np.maximum(al[..., None], 1e-3) * 255, 0)
    return np.dstack([np.clip(col, 0, 255), al]).astype(np.uint8)


def run():
    for d in ("plan", "plan-web"):
        os.makedirs(os.path.join(HERE, d), exist_ok=True)
    dies = {code: die_mask(code) for code in DIE}
    covs = {code: moments(m)[1] for code, m in dies.items()}
    for f in sorted(glob.glob(os.path.join(HERE, "cut", "*.png"))):
        name = os.path.basename(f)[:-4]
        code = name.split("-")[0]
        src = np.asarray(Image.open(f).convert("RGBA"))
        out = square_up(src, dies[code]) if code == "04" else straighten(src, covs[code])
        im = Image.fromarray(out, "RGBA")
        im.save(os.path.join(HERE, "plan", name + ".png"), optimize=True)
        w = im.copy(); w.thumbnail((1200, 1200)); w.save(os.path.join(HERE, "plan-web", name + ".webp"), quality=86, method=6)
        print(name, im.size, f"{im.width / SCALE:.0f}x{im.height / SCALE:.0f} mm box")


if __name__ == "__main__":
    run()
