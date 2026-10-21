"""Launch posts for the first booth: invitation copy for Facebook, Instagram, YouTube (and TikTok for tonight's
demo video), and the launch banner in three sizes. No products or prices: the message is only that the booth
has DIY leather craft to try. No event booth number yet.

python3 social-20261021/build.py                          -> banners/*.html, banners/jobs.json, site/index.html
node brand-20261014/tools/render.mjs social-20261021/banners/jobs.json   -> banners/*.png
(render first, then run build.py again so the page copies the new PNGs)
"""
import html, importlib.util, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BRAND_DIR = os.path.join(REPO, "brand-20261014")
sys.path.insert(0, BRAND_DIR)
import brand as B

def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m

PB = _load("posters_build", os.path.join(BRAND_DIR, "posters", "build.py"))
S = _load("brand_site", os.path.join(BRAND_DIR, "site", "build.py"))
E = html.escape
C = B.C
FONTS = "file://" + os.path.join(BRAND_DIR, "fonts")
H = B.BRAND["handle"]

# from the organiser's post (หนูทดลอง KIDS MARKET, 21 Oct); both weekends confirmed by the owner 21 Oct.
# The DIY price stays out of every post until the owner decides it.
FAIR = "บ้านและสวนแฟร์ Living Festival 2026"
ZONE = "หนูทดลอง KIDS MARKET"
PLACE, HALL = "อิมแพ็ค เมืองทองธานี", "ชาเลนเจอร์ 2–3"
WEEKENDS = ("23–25 ต.ค.", "30 ต.ค.–1 พ.ย.")
DATES = f"{WEEKENDS[0]} และ {WEEKENDS[1]} 2569"
HOURS = "ศุกร์–อาทิตย์ 10:00–17:00"
TAGS = ("#OCT26 #ourcraftedthings #หนูทดลองKidsMarket #บ้านและสวนแฟร์ #บ้านและสวนแฟร์2026 #LivingFestival2026 "
        "#DIY #leathercraft #งานแฮนด์เมด")
# the organiser's zone is blue too, so "find the blue sign" would not stand out: point to the zone and our name instead
FIND = f"ตามหาบูธ OCT. 26 ในโซน{ZONE}"
WHERE = f"{FAIR}\n{PLACE} {HALL}\n{DATES}\n{HOURS} · เข้างานฟรี"
# leather pieces scattered as the DIY motif; the bear head (01) stays out so no FIVE BEARS mark sits next to OCT. 26
PIECES = ["02", "04", "05", "06", "02"]

# ---------------------------------------------------------------- copy
COPY = [
    ("Facebook", "โพสต์คู่กับแบนเนอร์ 1080 × 1350", f"""OCT. 26 เปิดตัวครั้งแรกที่{FAIR} ในโซน{ZONE}

ที่บูธเรามี DIY leather craft ให้ลองทำด้วยมือตัวเอง หยิบเศษหนังแท้ที่เหลือจากการผลิตโซฟา มาต่อเป็นชิ้นงาน ราว 5 นาทีก็เสร็จ เด็กทำได้ ผู้ใหญ่ก็สนุก

ลูก ๆ อยู่ที่บูธ คอยสอนทีละขั้น
{FIND} แล้วแวะมาลองกันนะ

{WHERE}

OCT. 26 · our crafted things. ของที่เราทำกันเอง
{TAGS}"""),
    ("Instagram", "แคปชันคู่กับแบนเนอร์ 1080 × 1350", f"""เปิดตัวครั้งแรก {FAIR}

มาลอง DIY leather craft ที่บูธ OCT. 26 โซน{ZONE}
ต่อเศษหนังแท้ด้วยมือตัวเอง ราว 5 นาทีเสร็จ ลูก ๆ รอสอนอยู่

{WHERE}

our crafted things. ของที่เราทำกันเอง
{TAGS} #handmade #workshop"""),
    ("Instagram Story", "สามหน้า ใช้แบนเนอร์ 1080 × 1920 เป็นหน้าแรก", f"""หน้า 1: แบนเนอร์ story
หน้า 2: คลิปมือต่อหนัง + ข้อความ: มาลองต่อหนังแท้ด้วยมือ
หน้า 3: ข้อความ: {FIND} · {PLACE} {HALL} · {DATES} + สติกเกอร์นับถอยหลังตั้งเวลา 23 ต.ค. 10:00 + แท็กเพจผู้จัด"""),
    ("YouTube · โพสต์ชุมชน", "แนบแบนเนอร์ 1080 × 1080", f"""OCT. 26 เปิดตัวครั้งแรกที่{FAIR} โซน{ZONE}
มี DIY leather craft ให้ลองต่อเศษหนังแท้ด้วยมือตัวเองที่บูธ ลูก ๆ จะอยู่สอน
{PLACE} {HALL} · {DATES} · {HOURS}

ช่องนี้จะลงคลิปเบื้องหลังวันออกบูธ ติดตามไว้ได้เลย"""),
]

VIDEO_COPY = [
    ("YouTube Shorts · ชื่อคลิป", "ลูก ๆ ต่อเศษหนังแท้ด้วยมือ | OCT. 26 DIY leather craft #Shorts"),
    ("YouTube Shorts · คำอธิบาย", f"""ลูก ๆ สาธิตการต่อเศษหนังแท้เข้าด้วยกันด้วยมือ
มาลองต่อเองได้ที่บูธ OCT. 26 โซน{ZONE}
{WHERE}

OCT. 26 · our crafted things. ของที่เราทำกันเอง
ติดตาม @{H} ได้ทุกช่องทาง
{TAGS}"""),
    ("Facebook / Instagram Reels", f"""ต่อหนังแท้ด้วยมือ ทีละชิ้น
มาลองเองได้ที่บูธ OCT. 26 โซน{ZONE}
{FAIR} · {PLACE} {HALL} · {DATES}

{TAGS} #reels"""),
    ("TikTok", f"""ลูกเราต่อเศษหนังแท้ด้วยมือ มาลองเองได้ที่บูธ OCT. 26 โซน{ZONE} {FAIR} {PLACE} {DATES} {TAGS} #DIYง่ายๆ"""),
]

SHOTS = [
    ("0–2 วิ", "เปิดด้วยชิ้นหนังที่ยังไม่ต่อ วางบนผ้าลินินสีครีม มือเด็กหยิบขึ้นมา", "ข้อความบนจอ: มาลองต่อหนังแท้ด้วยมือ"),
    ("2–10 วิ", "ถ่ายมือจากด้านบน ต่อทีละขั้น ช้า ๆ ให้เห็นทุกจังหวะ", "ไม่ต้องพูด ใช้เสียงจริงตอนหนังเข้าล็อก"),
    ("10–13 วิ", "ชูชิ้นที่ต่อเสร็จ ดึงให้ดูว่าแน่น", ""),
    ("13–15 วิ", "ภาพนิ่งชิ้นงานบนผ้า", f"ข้อความบนจอ: บ้านและสวนแฟร์ · โซน{ZONE} · {DATES}"),
]
SHOOT_TIPS = [
    "ถือมือถือแนวตั้ง 9:16 ความละเอียด 1080p หรือ 4K ที่ 30 fps ใช้คลิปเดียวลงได้ทุกช่องทาง",
    "ถ่ายใกล้หน้าต่างหรือใต้ไฟหนีบแสงวอร์มที่ซื้อไว้ ปิดไฟเพดานแสงขาวเพื่อไม่ให้สีหนังเพี้ยน",
    "ปูผ้าลินินสีครีมเป็นพื้น ใช้ผ้าผืนเดียวกับที่บูธ ภาพจะเหมือนกันทุกคลิป",
    "ถ่ายมือเป็นหลัก ไม่ต้องเห็นหน้าลูก ไม่ใส่ชุดนักเรียนหรือป้ายชื่อโรงเรียน ไม่บอกชื่อจริงในคลิป และถามลูกก่อนโพสต์",
    "อัดคนละคลิป ลงวันละคลิปถึงวันงาน แล้วเก็บไว้ลงอีกรอบก่อนสัปดาห์ที่สอง",
]

# ---------------------------------------------------------------- banners
BANNERS = [("launch-post-1080x1350", 1080, 1350, "post"), ("launch-story-1080x1920", 1080, 1920, "story"),
           ("launch-square-1080x1080", 1080, 1080, "square")]


def pieces(n, size):
    # edge positions only, so no piece touches the wordmark or its clear space
    spots = [(-4, 6, -18), (80, 0, 14), (90, 60, -8), (-6, 68, 22), (20, 90, -12)]
    out = ""
    for (x, y, r), code in list(zip(spots, PIECES))[:n]:
        out += (f'<span class="piece" style="left:{x}%;top:{y}%;width:{size}px;transform:rotate({r}deg)">'
                f'{PB.icon(code, C["leather"], C["paper"])}</span>')
    return out


def banner(kind, w, h):
    big = {"post": .94, "story": 1.2, "square": .74}[kind]
    top = {"post": 470, "story": 760, "square": 330}[kind]
    mid_pad = {"post": 50, "story": 0, "square": 34}[kind]
    word = PB._logo("oct-wordmark-reverse.svg")
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>
@font-face{{font-family:Anuphan;font-weight:500;src:url({FONTS}/alt/Anuphan-Medium.ttf)}}
@font-face{{font-family:Jost;font-weight:500;src:url({FONTS}/alt/Jost-Medium.ttf)}}
@font-face{{font-family:Plex;font-weight:400;src:url({FONTS}/IBMPlexSansThai-Regular.ttf)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{w}px;height:{h}px;background:{C['paper']};color:{C['ink']};font-family:Plex,sans-serif;overflow:hidden}}
.page{{position:relative;width:{w}px;height:{h}px;display:flex;flex-direction:column}}
.top{{position:relative;height:{top}px;background:{C['cobalt']};color:{C['paper']};display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:{int(18*big)}px;overflow:hidden}}
.pill{{background:{C['sun']};color:{C['ink']};border-radius:99px;padding:{int(10*big)}px {int(30*big)}px;
  font-family:Anuphan;font-weight:500;font-size:{int(36*big)}px}}
.top svg{{width:{int(700*big)}px;height:auto;display:block}}
.top .en{{font-family:Jost;font-weight:500;font-size:{int(52*big)}px;letter-spacing:.04em}}
.top .piece{{position:absolute;opacity:.92}}.top .piece svg{{width:100%;height:auto;display:block}}
.mid{{flex:1;padding:{mid_pad}px 89px 0;display:flex;flex-direction:column;gap:{int(26*big)}px;justify-content:{"center" if kind == "story" else "flex-start"}}}
.mid h1{{font-family:Anuphan;font-weight:500;font-size:{int(80*big)}px;line-height:1.2}}
.mid h1 b{{font-family:Jost;font-weight:500;color:{C['tomato']};display:block;font-size:{int(92*big)}px;line-height:1.1}}
.mid p{{font-size:{int(34*big)}px;line-height:1.45;color:#4A4A55}}
.when{{display:grid;grid-template-columns:1fr 1fr;gap:{int(18*big)}px;margin-top:{int(4*big)}px}}.when .w2{{grid-column:1/-1}}
.when div{{background:#FFFFFF;border-radius:21px;padding:{int(18*big)}px {int(26*big)}px;font-family:Anuphan;font-weight:500;font-size:{int(34*big)}px;line-height:1.25}}
.when small{{display:block;font-family:Plex;font-weight:400;font-size:{int(22*big)}px;color:#4A4A55}}
.foot{{background:{C['ink']};color:{C['paper']};height:{int(120*big)}px;display:flex;align-items:center;justify-content:space-between;
  padding:0 89px;font-size:{int(28*big)}px}}
.foot b{{font-family:Jost;font-weight:500;font-size:{int(32*big)}px;color:{C['paper']}}}
</style></head><body><div class="page">
<div class="top">{pieces(5 if kind != "square" else 4, int(150*big))}<span class="pill">เปิดตัวครั้งแรก</span>{word}<div class="en">{B.BRAND['tag_en']}</div></div>
<div class="mid"><h1>มาลองทำ<b>DIY leather craft</b>ด้วยมือตัวเอง</h1>
{"" if kind == "square" else f"<p>โซน{ZONE} · เข้างานฟรี</p>"}
<div class="when"><div class="w2"><small>งาน</small>{FAIR}</div><div><small>ที่</small>{PLACE}<br>{HALL}</div><div><small>ศุกร์–อาทิตย์ · 10:00–17:00</small>{WEEKENDS[0]}<br>{WEEKENDS[1]} 2569</div></div></div>
<div class="foot"><span>ตามหาบูธ OCT. 26</span><b>@{H}</b></div>
</div></body></html>"""


# ---------------------------------------------------------------- summary page
def summary():
    copy = "".join(f'<div class="card" style="display:flex;flex-direction:column;gap:8px;min-width:0"><h3>{E(t)}</h3>'
                   f'{S.copybox(f"c{i}", body, use)}</div>' for i, (t, use, body) in enumerate(COPY))
    vcopy = "".join(S.copybox(f"v{i}", body, t) for i, (t, body) in enumerate(VIDEO_COPY))
    shots = "".join(f'<tr><td class="mono" style="white-space:nowrap">{E(t)}</td><td>{E(a)}</td><td>{E(b)}</td></tr>' for t, a, b in SHOTS)
    tips = "".join(f"<li>{E(t)}</li>" for t in SHOOT_TIPS)
    figs = "".join(
        f'<figure class="card" style="margin:0;display:flex;flex-direction:column;gap:10px">'
        f'<img src="{n}.png" alt="แบนเนอร์เปิดตัว OCT. 26 ขนาด {w} × {h}" loading="lazy" style="border-radius:10px;border:1px solid var(--line)">'
        f'<figcaption class="cap">{w} × {h} · {use}</figcaption></figure>'
        for (n, w, h, _), use in zip(BANNERS, ["Facebook และ Instagram feed", "IG Story, Reels cover, TikTok", "YouTube โพสต์ชุมชน"]))
    return f"""{S.head("OCT. 26 โพสต์เปิดตัว")}
<div class="wrap"><header style="padding-top:28px;display:flex;flex-direction:column;gap:14px">
<span class="eyebrow">ฝ่ายการตลาด · 21 ต.ค. 2569</span><h1>โพสต์เปิดตัว OCT. 26</h1>
<p class="lead">แบนเนอร์เปิดตัวสามขนาด คำเชิญชวนสำหรับ Facebook, Instagram และ YouTube และแคปชันกับวิธีถ่ายคลิปสาธิตคืนนี้
ทุกชิ้นพูดเรื่องเดียว: ที่บูธมี DIY leather craft ให้ลองทำ ยังไม่พูดถึงสินค้าหรือราคา</p></header>
<section><span class="eyebrow">แบนเนอร์</span><h2>แบนเนอร์เปิดตัว</h2>
<div class="grid">{figs}</div>
<p class="cap">ไฟล์ PNG อยู่ที่ social-20261021/banners · ชื่องาน ที่ และเวลา จากโพสต์ของผู้จัด 21 ต.ค. · ไม่ใช้โลโก้ของผู้จัด ใช้แค่ชื่องาน และแท็กเพจผู้จัดตอนโพสต์</p></section>
<section><span class="eyebrow">คำเชิญชวน</span><h2>กดคัดลอกแล้ววางได้เลย</h2><div class="grid">{copy}</div></section>
<section><span class="eyebrow">คืนนี้</span><h2>คลิปสาธิตของลูก ๆ</h2>
<div class="tbl"><table><thead><tr><th>ช่วง</th><th>ภาพ</th><th>ข้อความหรือเสียง</th></tr></thead><tbody>{shots}</tbody></table></div>
<div class="card"><ul>{tips}</ul></div>
<div class="card" style="display:flex;flex-direction:column;gap:8px">{vcopy}</div></section>
<section><h2>ต้องเช็กก่อนโพสต์</h2><div class="card"><ol>
<li>ชื่อ @{H} ใช้ได้จริงทุกช่องทาง</li>
<li>ลูก ๆ โอเคกับคลิปที่จะโพสต์</li></ol></div></section>
<section><h2>ไฟล์</h2><div class="tbl"><table><tbody>
<tr><td class="mono" style="white-space:nowrap">social-20261021/build.py</td><td>ข้อความทุกช่องทางและแบนเนอร์ แก้ที่นี่แล้วรันใหม่</td></tr>
<tr><td class="mono" style="white-space:nowrap">social-20261021/banners/*.png</td><td>แบนเนอร์สามขนาด</td></tr>
<tr><td class="mono" style="white-space:nowrap">social-20261021/site/index.html</td><td>หน้านี้</td></tr></tbody></table></div></section>
</div>{S.COPY_JS}"""


if __name__ == "__main__":
    bdir, sdir = os.path.join(HERE, "banners"), os.path.join(HERE, "site")
    os.makedirs(bdir, exist_ok=True); os.makedirs(sdir, exist_ok=True)
    jobs = []
    for n, w, h, kind in BANNERS:
        open(os.path.join(bdir, n + ".html"), "w").write(banner(kind, w, h))
        jobs.append(dict(src=os.path.join(bdir, n + ".html"), out=os.path.join(bdir, n + ".png"), w=w, h=h))
        if os.path.exists(os.path.join(bdir, n + ".png")):
            shutil.copyfile(os.path.join(bdir, n + ".png"), os.path.join(sdir, n + ".png"))
    json.dump(jobs, open(os.path.join(bdir, "jobs.json"), "w"), indent=0)
    open(os.path.join(sdir, "index.html"), "w").write(summary())
    print("wrote", len(jobs), "banners and site/index.html")
