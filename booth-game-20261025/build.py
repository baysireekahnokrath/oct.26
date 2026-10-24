"""Booth giveaway game and table signs (25 Oct 2026).

Step 1: follow IG or FB, play the pattern memory game, get one leather piece.
Step 2 (optional, no extra prize; owner 24 Oct: one piece per person): post a photo of the finished piece
(public, tag @oct.26_brand, #OCT26ชิ้นของฉัน) so we can share it as a review.
No chance draw, no tagging friends, no data from children; the game only counts finished rounds on the device.

python3 build.py -> index.html (kiosk game) and sign.html;  node render.cjs -> OCT26-booth-game-signs-A4.pdf + previews
"""
import io, os, re, sys
import qrcode
import qrcode.image.svg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "kids-brand-20261024"))
from kit import PATTERNS, shape_svg  # noqa: E402

IG = "https://www.instagram.com/oct.26_brand/"
FB = "https://www.facebook.com/oct26brand"
TAG, HASH = "@oct.26_brand", "#OCT26ชิ้นของฉัน"
LOGO = os.path.join(ROOT, "brand-20261014", "brandbook-v2", "logo", "svg", "square-light.svg")
FONTS = os.path.join(ROOT, "brand-20261014", "fonts")


def qr(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    buf = io.BytesIO(); img.save(buf)
    s = buf.getvalue().decode()
    s = re.sub(r"<\?xml[^>]*>", "", s)
    s = re.sub(r'width="[^"]*" height="[^"]*"', "", s, count=1)
    return s.replace("<svg ", '<svg class="qr" ', 1)


def logo():
    s = open(LOGO).read()
    return re.sub(r' width="[\d.]+" height="[\d.]+"', ' class="logo"', s, count=1)


def piece(code, fill):
    p = PATTERNS[code]
    return f'<svg viewBox="-2 -2 {p["w"] + 4} {p["h"] + 4}" aria-hidden="true">{shape_svg(code, fill)}</svg>'


FILLS = {"01": "#B07A4A", "02": "#A9442B", "03": "#B9A3D6", "04": "#2E4A7D", "05": "#E9A825", "07": "#5E7A3A"}

SIGN_CSS = f"""
@font-face{{font-family:Anuphan;font-weight:500;src:url(file://{FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Plex;src:url(file://{FONTS}/IBMPlexSansThai-Regular.ttf)}}
@font-face{{font-family:Plex;font-weight:600;src:url(file://{FONTS}/IBMPlexSansThai-SemiBold.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url(file://{FONTS}/alt/Jost-Medium.ttf)}}
@page{{size:A4;margin:0}} *{{box-sizing:border-box}} html,body{{margin:0}}
body{{font-family:Plex,sans-serif;color:#2A2725;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;position:relative;background:#F4F0E8;padding:16mm 16mm 0;page-break-after:always;overflow:hidden}}
.pg:last-child{{page-break-after:auto}}
.logo{{width:26mm;height:26mm;display:block}}
h1{{font-family:Anuphan;font-weight:500;font-size:19mm;line-height:1.08;margin:28mm 0 3mm}}
.sub{{font-size:6mm;margin:0;color:#4A4542}}
.steps{{margin:10mm 0 0;padding:0;list-style:none;display:grid;gap:5mm}}
.steps li{{display:grid;grid-template-columns:12mm 1fr;gap:4mm;align-items:start;font-size:6.2mm;line-height:1.35}}
.steps b{{font-family:Jost;font-weight:500;background:#2A2725;color:#F4F0E8;border-radius:50%;width:12mm;height:12mm;display:grid;place-items:center;font-size:6mm}}
.qrs{{display:flex;gap:10mm;margin-top:10mm}}
.qrs div{{display:grid;gap:2mm;justify-items:center;font-family:Jost;font-size:5mm}}
.qr{{width:46mm;height:46mm;background:#fff;padding:2mm;display:block}}
.pieces{{position:absolute;right:12mm;top:14mm;display:grid;grid-template-columns:repeat(3,22mm);gap:3mm}}
.pieces svg{{width:22mm;height:22mm}}
.tag{{font-family:Jost;font-size:9mm;margin:8mm 0 0}}
.note{{position:absolute;left:16mm;right:16mm;bottom:14mm;font-size:3.6mm;color:#6E6A64;line-height:1.5}}
.band{{position:absolute;left:0;right:0;bottom:0;height:6mm;display:flex}} .band i{{flex:1}}
"""
BAND = '<div class="band">' + "".join(f'<i style="background:{c}"></i>' for c in ("#A9442B", "#5E7A3A", "#E9A825", "#B9A3D6", "#2E4A7D")) + "</div>"


def sign():
    pieces = "".join(piece(c, f) for c, f in FILLS.items())
    p1 = (f'<section class="pg">{logo()}<div class="pieces">{pieces}</div>'
          f'<h1>Follow · เล่นเกม<br>รับชิ้นหนังฟรี</h1><p class="sub">เกมจับคู่แพตเทิร์น เล่นจบได้ทุกคน ไม่ต้องลุ้น</p>'
          f'<ol class="steps"><li><b>1</b><span>Follow IG หรือ Facebook ของเรา (ช่องทางไหนก็ได้)</span></li>'
          f'<li><b>2</b><span>โชว์หน้าจอให้พี่ที่บูธดู แล้วเล่นเกมจับคู่ 6 ลาย</span></li>'
          f'<li><b>3</b><span>เล่นจบ เลือกชิ้นหนังที่ชอบ 1 ชิ้น ไปแต่งต่อที่โต๊ะได้เลย</span></li></ol>'
          f'<div class="qrs"><div>{qr(IG)}IG {TAG}</div><div>{qr(FB)}FB oct26brand</div></div>'
          f'<p class="note">คนละ 1 ครั้งต่อวัน · ไม่ต้องกรอกชื่อหรือเบอร์ · ชิ้นหนังวัวแท้จากเศษหนัง ไม่ใช่ของเล่นสำหรับเด็กเล็ก</p>{BAND}</section>')
    p2 = (f'<section class="pg">{logo()}<div class="pieces">{pieces}</div>'
          f'<h1>ถ่ายรูป · โพสต์<br>อวดผลงาน</h1><p class="sub">แต่งชิ้นหนังเสร็จแล้ว ช่วยถ่ายรูปบอกต่อหน่อยนะ</p>'
          f'<ol class="steps"><li><b>1</b><span>ถ่ายรูปชิ้นที่แต่งเสร็จ (ถ่ายมือกับชิ้นหนังก็สวย)</span></li>'
          f'<li><b>2</b><span>โพสต์ลง IG หรือ Facebook แบบสาธารณะ แท็กเรา และใส่แฮชแท็ก</span></li>'
          f'<li><b>3</b><span>เราจะกดไลก์และแชร์ผลงานเด่นในเพจ (ถามเจ้าของโพสต์ก่อนทุกครั้ง)</span></li></ol>'
          f'<p class="tag">{TAG}<br>{HASH}</p>'
          f'<p class="note">เขียนรีวิวตามจริงได้เลย ไม่ต้องชมก็ได้ · ถ้าเราอยากเอารูปไปลงเว็บ จะทักขออนุญาตก่อนทุกครั้ง และไม่ใช้รูปที่เห็นหน้าเด็ก </p>{BAND}</section>')
    return f"<!doctype html><html lang='th'><head><meta charset='utf-8'><style>{SIGN_CSS}</style></head><body>{p1}{p2}</body></html>"


def kiosk():
    tpl = open(os.path.join(HERE, "kiosk.tpl.html"), encoding="utf-8").read()
    cards = {c: piece(c, f) for c, f in FILLS.items()}
    import json
    return (tpl.replace("__QR_IG__", qr(IG)).replace("__QR_FB__", qr(FB)).replace("__LOGO__", logo())
               .replace("__CARDS__", json.dumps(cards, ensure_ascii=False)).replace("__TAG__", TAG).replace("__HASH__", HASH))


if __name__ == "__main__":
    open(os.path.join(HERE, "sign.html"), "w", encoding="utf-8").write(sign())
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(kiosk())
    print("sign.html index.html")
