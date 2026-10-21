"""Mock-up of the customer website for the booth (21 Oct 2026): only the 7 single-piece SKUs that are on sale.

Follows the shared status doc "OCT. 26 สถานะล่าสุด": 7 SKUs (01 22 24 26 27 28 29), no 06, no joined products,
no "no-sew" claim, no pattern play. Real photos come from the owner: on the published page an editor uploads them
from the phone (assets capability, resized in the browser) and picks one per slot; the choice lives in the page's
database (collection "photos": hero, p01..p29). Nothing here touches website/ (the live site) until the owner says
"แก้เว็บจริงเลยครับ".

python3 website-mock-20261021/build.py -> website-mock-20261021/index.html (publish as an Artifact)
"""
import html, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BRAND_DIR = os.path.join(REPO, "brand-20261014")
sys.path.insert(0, BRAND_DIR)
import brand as B


def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


S = _load("brand_site", os.path.join(BRAND_DIR, "site", "build.py"))
W = _load("site_build", os.path.join(REPO, "website", "build.py"))
E = html.escape

# the 7 SKUs on sale, from the status doc (prices are drafts there, same as brand.py)
SKU = {1: "OC-01-01", 22: "OC-01-22", 24: "OC-02-24", 26: "OC-03-26", 27: "OC-04-27", 28: "OC-05-28", 29: "OC-MX-29"}
MATERIAL = "หนังวัวแท้จากเศษหนัง หนา 1.0–1.2 มม. สีและลายแต่ละชิ้นไม่ซ้ำกัน"


def products():
    out = []
    for n, sku in SKU.items():
        p = next(q for q in B.PRODUCTS if q["n"] == n)
        out.append(dict(n=f"{n:02d}", sku=sku, name=p["name"], price=p["price"], size=p["size"], hook=p["hook"],
                        steps=p["steps"], who=p["who"], extra=p["extra"][0] if p["extra"] else ""))
    return out


CSS = """
:root{--mock:#FFC23C}
[hidden]{display:none!important}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.mockbar{margin:0 calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:var(--s2) max(16px,env(safe-area-inset-left,0px));
  background:var(--mock);color:#1C1B22;font-family:var(--display);font-size:14px;display:flex;gap:var(--s3);align-items:center;justify-content:space-between;flex-wrap:wrap}
.mockbar button{min-height:36px;padding:var(--s1) var(--s3);font-size:14px;background:#1C1B22;color:#FFF6EC;border-color:#1C1B22}
.mockbar button[aria-pressed="true"]{background:#FFFFFF;color:#1C1B22}
.site nav a[aria-current="page"]{background:var(--ink);color:var(--bg)}
.ph{position:relative;background:var(--chip);border-radius:var(--s3);overflow:hidden;aspect-ratio:4/5;display:flex;align-items:center;justify-content:center;max-width:100%}
.ph img{width:100%;height:100%;object-fit:cover;display:block}
.ph .wait{font-family:var(--display);font-size:14px;color:var(--muted);text-align:center;padding:var(--s3)}
.ph.hero{aspect-ratio:4/3}
.ph .pick{position:absolute;inset:auto var(--s2) var(--s2) auto;min-height:36px;padding:var(--s1) var(--s3);font-size:13px;background:var(--mock);color:#1C1B22;border-color:#1C1B22}
.hero2{display:grid;gap:var(--s4);grid-template-columns:minmax(0,1fr)}
@media (min-width:760px){.hero2{grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);align-items:center}}
.hero2 h1{font-size:clamp(var(--t3),8vw,46px)}
.strip{background:var(--cobalt);color:#FFFFFF;border-radius:var(--s3);padding:var(--s3) var(--s4);display:flex;flex-direction:column;gap:2px}
.strip b{font-family:var(--display);font-size:16px}.strip span{font-size:14px;opacity:.9}
.grid7{display:grid;gap:var(--s3);grid-template-columns:repeat(2,minmax(0,1fr))}
@media (min-width:760px){.grid7{grid-template-columns:repeat(4,minmax(0,1fr))}}
.grid7 a{min-width:0;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;gap:4px}
.grid7 .nm{font-family:var(--display);font-size:15px;line-height:1.3}
.ok{font-family:var(--display);font-size:12px;line-height:1;padding:4px 8px;border-radius:99px;background:var(--mint);color:#1C1B22;align-self:flex-start}
.steps3{display:grid;gap:var(--s2);grid-template-columns:minmax(0,1fr)}
@media (min-width:640px){.steps3{grid-template-columns:repeat(3,minmax(0,1fr))}}
.steps3 div{background:var(--paper);border:1px solid var(--line);border-radius:var(--s3);padding:var(--s3) var(--s4);display:flex;flex-direction:column;gap:2px}
.steps3 b{font-family:var(--logo);font-weight:500;font-size:22px;color:var(--tomato);line-height:1.2}
.steps3 span{font-family:var(--display);font-size:16px}.steps3 small{font-size:14px;color:var(--muted)}
.chan{display:flex;gap:var(--s2);flex-wrap:wrap}
.soon{font-size:12px;opacity:.8}
.pd{display:grid;gap:var(--s4);grid-template-columns:minmax(0,1fr)}
@media (min-width:760px){.pd{grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start}}
.pd .ph{aspect-ratio:1/1}
.kv{display:grid;grid-template-columns:auto minmax(0,1fr);gap:var(--s1) var(--s4);font-size:15px}
.kv dt{color:var(--muted)}.kv dd{margin:0}
.more{display:flex;gap:var(--s3);overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.more a{flex:none;width:120px;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;gap:4px;font-size:14px}
.buy{position:fixed;left:0;right:0;bottom:0;z-index:6;background:var(--ink);color:var(--bg);
  padding:var(--s2) max(16px,env(safe-area-inset-right,0px)) calc(var(--s2) + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px))}
.buy .in{max-width:987px;margin:0 auto;display:flex;gap:var(--s2);align-items:center}
.buy .pr{font-family:var(--logo);font-weight:500;font-size:20px;margin-right:auto;white-space:nowrap}
.buy .btn{min-height:44px;padding:var(--s1) var(--s3);font-size:15px}
.buy .line{background:#06C755;border-color:#06C755;color:#FFFFFF;opacity:.55}
.note{border-left:4px solid var(--mock);background:var(--paper);border-radius:0 var(--s3) var(--s3) 0;padding:var(--s3) var(--s4);font-size:15px}
.notes{margin:0;padding-left:1.3em;display:flex;flex-direction:column;gap:4px;font-size:15px}
.tray{position:fixed;inset:auto 0 0 0;z-index:8;background:var(--paper);border-top:2px solid var(--mock);max-height:70vh;overflow:auto;
  padding:var(--s4) max(16px,env(safe-area-inset-right,0px)) calc(var(--s4) + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px))}
.tray .in{max-width:987px;margin:0 auto;display:flex;flex-direction:column;gap:var(--s3)}
.tray .pics{display:grid;gap:var(--s2);grid-template-columns:repeat(auto-fill,minmax(96px,1fr))}
.tray .pics button{padding:0;border-radius:var(--s2);overflow:hidden;aspect-ratio:1/1;min-height:0;background:var(--chip)}
.tray .pics img{width:100%;height:100%;object-fit:cover;display:block}
.toast{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(76px + env(safe-area-inset-bottom,0px));z-index:9;background:var(--cobalt);color:#FFFFFF;
  font-family:var(--display);font-size:14px;padding:var(--s2) var(--s4);border-radius:99px;max-width:calc(100% - 32px)}
main{padding-bottom:var(--s6)}
"""

JS = r"""
const P = /*P*/[];
const CFG = /*CFG*/{};
const $ = (s, el=document) => el.querySelector(s);
const use = n => (window.claude && window.claude.use) ? window.claude.use(n).catch(()=>null) : Promise.resolve(null);
const photos = {};          // slot -> asset id
let tray = [];              // [{id, at}]
let db = null, assets = null, editing = false, picking = null;
const src = id => "/_blob/" + id;
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

function ph(slot, cls, label){
  const id = photos[slot];
  const img = id ? `<img src="${src(id)}" alt="${esc(label)}" loading="lazy">` : `<span class="wait">รูปจริง<br>${esc(label)}</span>`;
  const pick = editing ? `<button type="button" class="pick" data-slot="${slot}">${id?"เปลี่ยนรูป":"เลือกรูป"}</button>` : "";
  return `<div class="ph ${cls||""}">${img}${pick}</div>`;
}

function home(){
  const cards = P.map(p => `<a href="#p${p.n}">${ph("p"+p.n,"",p.name)}<span class="ok">พร้อมส่ง</span><span class="nm">${esc(p.name)}</span><span class="price">${p.price} บาท</span></a>`).join("");
  return `
<section class="hero2" style="padding-top:var(--s4)">${ph("hero","hero","คนในบ้านกับของจริง")}
<div class="intro"><span class="eyebrow">our crafted things.</span><h1>ของใช้จากเศษหนังแท้ ทำกันเองทั้งบ้าน</h1>
<p class="lead">${esc(CFG.line)}</p>
<div class="row"><a class="btn primary" href="#shop">ดูสินค้า ${P.length} แบบ</a><a class="btn order" href="${CFG.ig}" target="_blank" rel="noopener">ทักไอจี</a></div></div></section>
<section id="booth" style="padding-top:var(--s4)"><div class="strip"><b>เจอกันที่${esc(CFG.fair)}</b>
<span>${esc(CFG.place)} · ${esc(CFG.weekends)} · ${esc(CFG.hours)}</span></div></section>
<section id="shop"><span class="eyebrow">สินค้า</span><h2>มีของพร้อมส่ง ${P.length} แบบ</h2>
<p class="cap">ที่รองแก้ว ป้ายห้อย และที่เก็บสายชาร์จ ชิ้นเดียวจบ ใช้ได้ทันที ราคา ${Math.min(...P.map(p=>p.price))}–${Math.max(...P.map(p=>p.price))} บาท</p>
<div class="grid7">${cards}</div></section>
<section id="how"><span class="eyebrow">สั่งยังไง</span><h2>สั่งง่าย สามขั้น</h2>
<div class="steps3"><div><b>1</b><span>ทักแชทบอกชิ้นที่ชอบ</span><small>ไอจี @${esc(CFG.handle)} · LINE เร็ว ๆ นี้</small></div>
<div><b>2</b><span>ร้านยืนยันของ แล้วโอนพร้อมเพย์</span><small>สีหนังแต่ละชิ้นไม่ซ้ำ ส่งรูปให้ดูก่อนได้</small></div>
<div><b>3</b><span>ส่งไปรษณีย์ หรือรับที่บูธ</span><small>ค่าส่งแจ้งในแชท</small></div></div>
<div class="chan"><a class="btn order" href="${CFG.ig}" target="_blank" rel="noopener">ทักไอจี</a>
<span class="btn" aria-disabled="true">LINE <span class="soon">รอลิงก์</span></span><span class="btn" aria-disabled="true">Shopee <span class="soon">รอลิงก์</span></span></div></section>
<section id="story"><span class="eyebrow">เรื่องของเรา</span><h2>26 ตุลาคม</h2><p class="lead">${esc(CFG.story)}</p></section>`;
}

function product(n){
  const p = P.find(x => x.n === n) || P[0];
  const others = P.filter(x => x !== p).map(x => `<a href="#p${x.n}">${ph("p"+x.n,"",x.name)}<span>${esc(x.name)}</span><span class="price">${x.price} บาท</span></a>`).join("");
  const steps = p.steps.map(s => `<li>${esc(s)}</li>`).join("");
  return `
<div class="pd" style="padding-top:var(--s4)">${ph("p"+p.n,"",p.name)}
<div class="stack"><span class="ok">พร้อมส่ง</span><h1>${esc(p.name)}</h1><p class="lead">${esc(p.hook)}</p>
<p class="price big">${p.price} บาท</p>
<dl class="kv"><dt>ขนาด</dt><dd>${esc(p.size)}</dd><dt>วัสดุ</dt><dd>${esc(CFG.material)}${p.extra?" + "+esc(p.extra):""}</dd>
<dt>เหมาะกับ</dt><dd>${esc(p.who)}</dd><dt>รหัส</dt><dd>${esc(p.sku)}</dd><dt>ดูแล</dt><dd>เช็ดด้วยผ้าแห้ง เลี่ยงน้ำและแดดจัด</dd></dl>
<h2 style="font-size:var(--t2)">วิธีใช้</h2><ol>${steps}</ol>
<div class="note">ส่งยังไง: ไปรษณีย์ทั่วประเทศ หรือรับที่บูธ · จ่ายพร้อมเพย์ · ทักแชทแล้วร้านยืนยันของก่อนโอนทุกครั้ง</div></div></div>
<section><span class="eyebrow">ชิ้นอื่น</span><h2 style="font-size:var(--t2)">ดูต่อ</h2><div class="more">${others}</div></section>
<div class="buy"><div class="in"><span class="pr">${p.price}.-</span>
<a class="btn order" href="${CFG.ig}" target="_blank" rel="noopener" data-ask="สนใจ ${esc(p.sku)} ${esc(p.name)} ${p.price} บาท">สั่งทางไอจี</a>
<span class="btn line" aria-disabled="true">LINE</span></div></div>`;
}

const NOTES = `<section id="notes"><span class="eyebrow">หมายเหตุ mock</span><h2 style="font-size:var(--t2)">ต่างจากเว็บจริงตรงไหน</h2>
<ol class="notes"><li>เหลือ 7 สินค้าที่ขายจริง ไม่มี 06 ไม่มีของที่ต้องต่อชิ้น ไม่มีคำว่าไม่ต้องเย็บ</li>
<li>ใช้รูปจริงแทนโปสเตอร์ (กด “ใส่รูปจริง” แถบเหลืองด้านบน)</li><li>เอาหน้าต่อลายออกจากเมนู</li>
<li>ปุ่มสั่งติดล่างจอในหน้าสินค้า กดแล้วคัดลอกข้อความสั่งให้ด้วย</li><li>เพิ่มกล่องสั่งยังไง สามขั้น · LINE และ Shopee รอลิงก์</li>
<li>ประกาศบูธเป็นแถบสั้น ไม่กินจอ</li></ol></section>`;

let toastT;
function toast(t){ const el=$("#toast"); el.textContent=t; el.hidden=false; clearTimeout(toastT); toastT=setTimeout(()=>el.hidden=true,2200); }

function render(){
  const h = location.hash.slice(1);
  const isP = /^p\d\d$/.test(h);
  $("#view").innerHTML = (isP ? product(h.slice(1)) : home()) + NOTES;
  document.querySelectorAll(".site nav a").forEach(a => a.removeAttribute("aria-current"));
  if(isP) window.scrollTo(0,0);
  else if(h) requestAnimationFrame(() => { const t = document.getElementById(h); if(t) t.scrollIntoView(); });
}
window.addEventListener("hashchange", render);

document.addEventListener("click", e => {
  const ask = e.target.closest("[data-ask]");
  if(ask){ try{ navigator.clipboard.writeText(ask.dataset.ask).then(()=>toast("คัดลอกข้อความแล้ว วางในแชทได้เลย"),()=>{}); }catch(_){} }
  const pk = e.target.closest(".pick");
  if(pk){ e.preventDefault(); openTray(pk.dataset.slot); }
});

/* ---------- photos: editors upload from the phone, resized here, then pick one per slot ---------- */
async function shrink(file){
  const bmp = await createImageBitmap(file, {imageOrientation:"from-image"});
  const k = Math.min(1, 1600 / Math.max(bmp.width, bmp.height));
  const c = document.createElement("canvas"); c.width = Math.round(bmp.width*k); c.height = Math.round(bmp.height*k);
  c.getContext("2d").drawImage(bmp, 0, 0, c.width, c.height);
  return await new Promise(r => c.toBlob(r, "image/jpeg", .85));
}
async function addFiles(files){
  let done = 0;
  for(const f of files){
    try{
      toast(`กำลังใส่รูป ${done+1}/${files.length}`);
      const r = await assets.upload(await shrink(f), {type:"image/jpeg"});
      await db.collection("tray").doc(r.id).set({at: Date.now()});
      done++;
    }catch(e){ toast(e && e.code==="quota_or_state" ? "ที่เก็บรูปเต็ม" : "ใส่รูปไม่ได้ ลองอีกครั้ง"); break; }
  }
  if(done) toast(`ใส่รูปแล้ว ${done} รูป`);
}
function slotName(slot){ if(slot==="hero") return "รูปใหญ่หน้าแรก"; const p=P.find(x=>"p"+x.n===slot); return p?p.name:slot; }
function openTray(slot){
  picking = slot;
  $("#trayTitle").textContent = "เลือกรูปให้: " + slotName(slot);
  const box = $("#pics"); box.innerHTML = "";
  for(const t of tray){
    const b = document.createElement("button"); b.type = "button"; b.dataset.id = t.id;
    b.innerHTML = `<img src="${src(t.id)}" alt="รูปที่ใส่ไว้">`; box.appendChild(b);
  }
  $("#noPics").hidden = !!tray.length;
  $("#tray").hidden = false;
}
async function choose(id){
  const slot = picking; $("#tray").hidden = true; if(!slot) return;
  photos[slot] = id; render();
  try{ await db.collection("photos").doc(slot).set({id, at: Date.now()}); toast("บันทึกรูปแล้ว"); }catch(_){ toast("บันทึกไม่ได้ ลองอีกครั้ง"); }
}

async function start(){
  render();
  db = await use("db"); assets = await use("assets");
  if(!db) return;
  db.collection("photos").onSnapshot(s => {
    for(const k of Object.keys(photos)) delete photos[k];
    for(const d of s.docs){ const v = d.data(); if(v && /^[0-9a-f]{32}$/.test(v.id)) photos[d.id] = v.id; }
    render();
  }, ()=>{});
  if(!assets) return;
  $("#edit").hidden = false;
  db.collection("tray").orderBy("at","desc").limit(60).onSnapshot(s => { tray = s.docs.filter(d=>/^[0-9a-f]{32}$/.test(d.id)).map(d => ({id:d.id})); if(!$("#tray").hidden && picking) openTray(picking); }, ()=>{});
  $("#edit").addEventListener("click", () => { editing = !editing; $("#edit").setAttribute("aria-pressed", String(editing)); $("#upRow").hidden = !editing; render(); });
  $("#files").addEventListener("change", e => { const fs=[...e.target.files]; e.target.value=""; if(fs.length) addFiles(fs); });
  $("#pics").addEventListener("click", e => { const b=e.target.closest("button[data-id]"); if(b) choose(b.dataset.id); });
  $("#closeTray").addEventListener("click", () => { $("#tray").hidden = true; picking = null; });
}
start();
"""


def page():
    bo = B.BOOTH
    cfg = dict(ig=W.ORDER, handle=W.H, line=B.BRAND["line"], story=B.STORY_SHORT, material=MATERIAL,
               fair=bo["fair"], place=f'{bo["place"]} {bo["hall"]} โซน{bo["zone"]}',
               weekends=f'{bo["weekends"][0]} และ {bo["weekends"][1]}', hours=bo["hours"])
    js = JS.replace("/*P*/[]", json.dumps(products(), ensure_ascii=False)).replace("/*CFG*/{}", json.dumps(cfg, ensure_ascii=False))
    return f"""<title>OCT. 26 Website Mock</title>
<meta name="claude:viewport-fit-sides" content="cover">
{S.FONT_LINK}<style>{S.CSS}{W.SITE_CSS}{CSS}</style>
<div class="mockbar"><span><b>MOCK</b> ยังไม่ใช่เว็บจริง · 7 สินค้าตามสถานะล่าสุด</span>
<button type="button" id="edit" aria-pressed="false" hidden>ใส่รูปจริง</button></div>
<div class="mockbar" id="upRow" hidden><label for="files">ใส่รูปจากมือถือ (เลือกได้หลายรูป) แล้วกด “เลือกรูป” บนแต่ละช่อง</label>
<input type="file" id="files" accept="image/*" multiple></div>
<header class="site"><div class="in"><a class="mark" href="#" aria-label="OCT. 26 หน้าแรก">
{W.logo_svg("oct-wordmark.svg", "mark-light")}{W.logo_svg("oct-wordmark-reverse.svg", "mark-dark")}</a>
<nav aria-label="เมนู"><a href="#shop">สินค้า</a><a href="#how">สั่งยังไง</a><a href="#booth">ออกบูธ</a><a href="#story">เรื่องของเรา</a></nav></div></header>
<div class="wrap"><main id="view"></main></div>
<div class="tray" id="tray" hidden><div class="in"><div class="row" style="justify-content:space-between"><b id="trayTitle"></b>
<button type="button" id="closeTray">ปิด</button></div><p class="cap" id="noPics">ยังไม่มีรูป ใส่รูปจากแถบเหลืองด้านบนก่อน</p><div class="pics" id="pics"></div></div></div>
<div class="toast" id="toast" role="status" hidden></div>
<script>{js}</script>
"""


if __name__ == "__main__":
    open(os.path.join(HERE, "index.html"), "w").write(page())
    print("wrote", os.path.join(HERE, "index.html"))
