"""OCT.26 Web Builder: the owner's no-code editor for the customer website, published as a claude.ai Artifact.

The page shows every product as the site shows it now (live.json, read from brand.py and website/build.py) and
keeps the owner's edits as drafts in the Artifact's database (collection "drafts": p01..p30 and booth).
"ขึ้นเว็บ" saves a request (collection "requests") holding the reviewed drafts and starts a Claude Code session
in the OCT.26 environment that follows APPLY.md: apply.py -> rebuild -> PR to main. The owner approves each change by
merging it (website/HANDOFF.md); after the merge the page is republished with the new baseline.

python3 website/builder/build.py -> website/builder/index.html (publish with the thumbs in FILES below)
"""
import html, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(HERE)
REPO = os.path.dirname(WEB)
BRAND_DIR = os.path.join(REPO, "brand-20261014")
sys.path.insert(0, BRAND_DIR)
import brand as B


def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


S = _load("brand_site", os.path.join(BRAND_DIR, "site", "build.py"))
W = _load("site_build", os.path.join(WEB, "build.py"))
A = _load("builder_apply", os.path.join(HERE, "apply.py"))
E = html.escape

URL = "https://claude.ai/artifact/NrAfdYHGTETkYWbMjT9QXG"   # this page: the session reads and republishes it
ENV = "env_01WKXaiUwedx7f5o3VCkUxPz"                # Claude Code environment "OCT.26"
REPO_URL = "https://github.com/baysireekahnokrath/oct.26"
BASE = "main"                                       # the branch Cloudflare deploys; the owner merges each change into it
WORK = "web-builder"                                # the session pushes here and opens (or updates) one PR to main
# published path -> source, for the Artifact publish (thumbnails of every product)
FILES = {f"thumbs/{p['n']:02d}.jpg": os.path.join(BRAND_DIR, "posters", "thumb", f"{p['n']:02d}.jpg") for p in B.PRODUCTS}

CSS = """
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--line);
  margin:0 calc(-1*max(16px,env(safe-area-inset-left,0px)));padding:var(--s3) max(16px,env(safe-area-inset-left,0px))}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.top .in{max-width:987px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:var(--s3)}
.top .btn{min-height:40px;padding:var(--s1) var(--s3);font-size:14px;flex:none}
.top .mark svg.mark-dark{display:none}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .top .mark svg.mark-light{display:none}:root:not([data-theme="light"]) .top .mark svg.mark-dark{display:block}}
:root[data-theme="dark"] .top .mark svg.mark-light{display:none}:root[data-theme="dark"] .top .mark svg.mark-dark{display:block}
.top .mark{display:flex;align-items:center;gap:var(--s2);text-decoration:none;color:var(--ink);min-width:0;flex-wrap:wrap}
.top .mark svg{width:96px;height:auto}
.top .tool{font-family:var(--logo);font-weight:500;font-size:var(--t-1);letter-spacing:.12em;text-transform:uppercase;color:var(--cobalt)}
.sum{display:grid;gap:var(--s3);grid-template-columns:repeat(auto-fit,minmax(144px,1fr))}
.sum div{background:var(--paper);border:1px solid var(--line);border-radius:var(--s3);padding:var(--s3) var(--s4)}
.sum b{display:block;font-family:var(--logo);font-weight:500;font-size:var(--t3);line-height:1.2;font-variant-numeric:tabular-nums}
.sum span{font-size:14px;color:var(--muted)}
.sum .hot b{color:var(--tomato)}
.note{border-radius:var(--s3);padding:var(--s3) var(--s4);background:var(--chip);font-size:15px}
.note.warn{background:var(--paper);border:1px solid var(--tomato)}
.chips{display:flex;gap:var(--s2);overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.chips button{flex:none;min-height:36px;padding:var(--s1) var(--s3);font-size:14px}
.list{display:flex;flex-direction:column;gap:var(--s2)}
.item{background:var(--paper);border:1px solid var(--line);border-radius:var(--s3)}
.item[open]{border-color:var(--cobalt)}
.item summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:56px minmax(0,1fr) auto;gap:var(--s3);align-items:center;padding:var(--s2)}
.item summary::-webkit-details-marker{display:none}
.item summary img{width:56px;height:70px;object-fit:cover;border-radius:var(--s2);background:var(--chip)}
.item .t{min-width:0;display:flex;flex-direction:column;gap:2px}
.item .t b{font-family:var(--display);font-weight:600;font-size:16px;line-height:1.3;overflow-wrap:anywhere}
.item .t small{font-size:13px;color:var(--muted)}
.item .p{font-family:var(--logo);font-weight:500;color:var(--heart);font-variant-numeric:tabular-nums;white-space:nowrap}
.tags{display:flex;gap:4px;flex-wrap:wrap}
.tag{font-family:var(--display);font-size:12px;line-height:1;padding:4px 8px;border-radius:99px;background:var(--chip);color:var(--ink)}
.tag.ed{background:var(--sun);color:#1C1B22}.tag.off{background:var(--ink);color:var(--bg)}.tag.so{background:var(--tomato);color:#FFFFFF}
.form{display:flex;flex-direction:column;gap:var(--s3);padding:0 var(--s3) var(--s3);border-top:1px solid var(--line);padding-top:var(--s3)}
.f{display:flex;flex-direction:column;gap:4px;min-width:0}
.f label{font-family:var(--display);font-size:14px;color:var(--muted)}
.f input,.f textarea{font:inherit;font-size:16px;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:var(--s2);
  padding:var(--s2) var(--s3);width:100%;min-height:44px}
.f textarea{min-height:76px;resize:vertical}
.f input:focus-visible,.f textarea:focus-visible{outline:3px solid var(--cobalt);outline-offset:1px}
.f .was{font-size:13px;color:var(--tomato)}
.f.ch input,.f.ch textarea{border-color:var(--sun);border-width:2px}
.price-row{display:flex;gap:var(--s2);align-items:stretch}
.price-row input{text-align:center;font-family:var(--logo);font-weight:500;font-size:20px;font-variant-numeric:tabular-nums}
.price-row button{flex:none;min-width:56px;padding:0 var(--s3)}
.sw{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);min-height:44px;font-family:var(--display);font-size:15px}
.sw input{appearance:none;-webkit-appearance:none;width:52px;height:30px;border-radius:99px;background:var(--line);position:relative;cursor:pointer;flex:none;margin:0;transition:background .15s}
.sw input::after{content:"";position:absolute;top:3px;left:3px;width:24px;height:24px;border-radius:50%;background:#FFFFFF;transition:transform .15s}
.sw input:checked{background:var(--mint)}.sw input:checked::after{transform:translateX(22px)}
.sw input.inv:checked{background:var(--tomato)}
.sw input:focus-visible{outline:3px solid var(--cobalt);outline-offset:2px}
.sw.ch span::after{content:" · แก้แล้ว";color:var(--tomato);font-size:13px}
.links{display:flex;gap:var(--s3);flex-wrap:wrap;font-size:14px}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:6;background:var(--ink);color:var(--bg);
  padding:var(--s3) max(16px,env(safe-area-inset-right,0px)) calc(var(--s3) + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px))}
.bar .in{max-width:987px;margin:0 auto;display:flex;gap:var(--s3);align-items:center;justify-content:space-between}
.bar b{font-family:var(--display);font-size:16px}.bar small{display:block;font-size:13px;opacity:.75}
.bar .primary{background:var(--tomato);border-color:var(--tomato);color:#FFFFFF}
.review{display:flex;flex-direction:column;gap:var(--s3)}
.review ol{margin:0;padding-left:1.4em;display:flex;flex-direction:column;gap:4px}
.review li{overflow-wrap:anywhere}
.review del{color:var(--muted)}.review ins{text-decoration:none;font-weight:600}
.reqs{display:flex;flex-direction:column;gap:var(--s2)}
.req{background:var(--paper);border:1px solid var(--line);border-radius:var(--s3);padding:var(--s3);display:flex;flex-direction:column;gap:4px}
.req .h{display:flex;justify-content:space-between;gap:var(--s2);flex-wrap:wrap;align-items:center}
.pill{font-family:var(--display);font-size:13px;padding:2px 10px;border-radius:99px;background:var(--chip)}
.pill.waiting{background:var(--sun);color:#1C1B22}.pill.working{background:var(--cobalt);color:#FFFFFF}
.pill.review{background:var(--pink);color:#1C1B22}.pill.live{background:var(--mint);color:#1C1B22}.pill.failed{background:var(--tomato);color:#FFFFFF}
.req small{color:var(--muted);font-size:13px}
.toast{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(84px + env(safe-area-inset-bottom,0px));z-index:7;background:var(--cobalt);color:#FFFFFF;
  font-family:var(--display);font-size:14px;padding:var(--s2) var(--s4);border-radius:99px;max-width:calc(100% - 32px)}
.empty{color:var(--muted);font-size:15px}
pre.msg{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--bg);border:1px solid var(--line);border-radius:var(--s2);padding:var(--s3);margin:0;font:inherit;font-size:15px}
@media (prefers-reduced-motion:reduce){.sw input,.sw input::after{transition:none}}
"""

JS = r"""
const LIVE = /*LIVE*/{};
const CFG = /*CFG*/{};
const FIELDS = ["name","price","hook","size","hide","sold"];
const NS = Object.keys(LIVE.products).sort();   // "10" sorts before "01" as an object key, so keep our own order
const LABEL = {name:"ชื่อ",price:"ราคา",hook:"ประโยคขาย",size:"ขนาด",hide:"แสดงบนเว็บ",sold:"หมดชั่วคราว"};
const $ = (s, el=document) => el.querySelector(s);
const drafts = {};                  // "p01" -> body, "booth" -> {until}
let db = null, canWrite = false, me = null, filter = "all", reqs = [];
const use = name => (window.claude && window.claude.use) ? window.claude.use(name).catch(()=>null) : Promise.resolve(null);

function eff(n){ return Object.assign({}, LIVE.products[n], pick(drafts["p"+n])); }
function pick(d){ if(!d) return {}; const o={}; for(const f of FIELDS) if(f in d) o[f]=d[f]; return o; }
function diff(n){ const l=LIVE.products[n], e=eff(n); return FIELDS.filter(f=>e[f]!==l[f]); }
function boothUntil(){ return (drafts.booth && drafts.booth.until) || LIVE.booth.until; }
function show(v,f){ if(f==="hide") return v?"ซ่อน":"แสดง"; if(f==="sold") return v?"หมด":"มีของ"; if(f==="price") return v+" บาท"; return v; }
function changes(){
  const out=[];
  for(const n of NS) for(const f of diff(n)){
    const l=LIVE.products[n][f], e=eff(n)[f];
    out.push({n, f, from:show(l,f), to:show(e,f), name:eff(n).name});
  }
  if(boothUntil()!==LIVE.booth.until) out.push({n:"บูธ", f:"until", from:thaiDate(LIVE.booth.until), to:thaiDate(boothUntil()), name:"ประกาศออกบูธ"});
  return out;
}
function thaiDate(s){ try{ return new Date(s+"T12:00:00+07:00").toLocaleDateString("th-TH",{day:"numeric",month:"short",year:"numeric"}); }catch(_){ return s; } }
function changeText(c){ return c.n==="บูธ" ? `ประกาศออกบูธ แสดงถึง ${c.from} → ${c.to}` : `#${c.n} ${c.name}: ${LABEL[c.f]} ${c.from} → ${c.to}`; }

let toastT;
function toast(t){ const el=$("#toast"); el.textContent=t; el.hidden=false; clearTimeout(toastT); toastT=setTimeout(()=>el.hidden=true,1800); }

/* ---------- product list, built once; values refreshed in place so typing keeps focus ---------- */
function build(){
  const list=$("#list");
  for(const n of NS){
    const p=LIVE.products[n];
    const d=document.createElement("details"); d.className="item"; d.id="it"+n; d.dataset.n=n; d.dataset.coll=p.coll;
    d.innerHTML=`<summary><img src="thumbs/${n}.jpg" alt="" width="56" height="70" loading="lazy">
      <span class="t"><b></b><small>#${n} · ${p.coll==="love"?"ห้าหมี Love":"SOI. 02"}</small><span class="tags"></span></span><span class="p"></span></summary>
      <div class="form">
        <div class="f" data-f="name"><label for="name${n}">ชื่อสินค้า</label><input id="name${n}" maxlength="60" autocomplete="off"><span class="was" hidden></span></div>
        <div class="f" data-f="price"><label for="price${n}">ราคา (บาท)</label>
          <div class="price-row"><button type="button" data-step="-10" aria-label="ลด 10 บาท">−10</button>
          <input id="price${n}" inputmode="numeric" pattern="[0-9]*" maxlength="5" autocomplete="off">
          <button type="button" data-step="10" aria-label="เพิ่ม 10 บาท">+10</button></div><span class="was" hidden></span></div>
        <div class="f" data-f="hook"><label for="hook${n}">ประโยคขาย (โชว์ใต้ชื่อและบนโปสเตอร์)</label><textarea id="hook${n}" maxlength="160"></textarea><span class="was" hidden></span></div>
        <div class="f" data-f="size"><label for="size${n}">ขนาด</label><input id="size${n}" maxlength="60" autocomplete="off"><span class="was" hidden></span></div>
        <label class="sw" data-f="hide" for="show${n}"><span>แสดงบนเว็บ</span><input type="checkbox" id="show${n}" role="switch"></label>
        <label class="sw" data-f="sold" for="sold${n}"><span>หมดชั่วคราว (ยังโชว์ แต่บอกลูกค้าว่าหมด)</span><input type="checkbox" class="inv" id="sold${n}" role="switch"></label>
        <div class="links"><a href="${CFG.site}/p/${n}.html" target="_blank" rel="noopener">ดูหน้านี้บนเว็บ</a>
          <button type="button" class="reset" hidden>คืนค่าเดิมของสินค้านี้</button></div>
      </div>`;
    list.appendChild(d);
    for(const f of ["name","hook","size"]) $("#"+f+n,d).addEventListener("input",e=>edit(n,f,e.target.value));
    $("#price"+n,d).addEventListener("input",e=>{ const v=e.target.value.replace(/\D/g,""); if(v!==e.target.value) e.target.value=v; if(v) edit(n,"price",+v); });
    d.querySelectorAll("[data-step]").forEach(b=>b.addEventListener("click",()=>{ const v=Math.max(1,Math.min(99999,eff(n).price+ +b.dataset.step)); edit(n,"price",v,true); }));
    $("#show"+n,d).addEventListener("change",e=>edit(n,"hide",!e.target.checked,true));
    $("#sold"+n,d).addEventListener("change",e=>edit(n,"sold",e.target.checked,true));
    $(".reset",d).addEventListener("click",()=>{ for(const f of FIELDS) pending[n]=Object.assign(pending[n]||{}, {[f]:LIVE.products[n][f]}); flush(n); paint(); });
  }
}

function paint(){
  for(const n of NS){
    const d=$("#it"+n), e=eff(n), l=LIVE.products[n], ch=diff(n);
    $("summary b",d).textContent=e.name; $(".p",d).textContent=e.price+" ฿";
    const tags=[]; if(ch.length) tags.push('<span class="tag ed">แก้แล้ว</span>'); if(e.hide) tags.push('<span class="tag off">ซ่อน</span>'); if(e.sold) tags.push('<span class="tag so">หมด</span>');
    $(".tags",d).innerHTML=tags.join("");
    for(const f of ["name","price","hook","size"]){
      const inp=$("#"+f+n,d), box=inp.closest(".f"), was=$(".was",box);
      if(document.activeElement!==inp) inp.value=String(e[f]);
      box.classList.toggle("ch", e[f]!==l[f]); was.hidden = e[f]===l[f]; was.textContent="เดิม: "+show(l[f],f);
    }
    $("#show"+n,d).checked=!e.hide; $("#sold"+n,d).checked=e.sold;
    d.querySelector('.sw[data-f="hide"]').classList.toggle("ch",e.hide!==l.hide);
    d.querySelector('.sw[data-f="sold"]').classList.toggle("ch",e.sold!==l.sold);
    $(".reset",d).hidden=!ch.length||!canWrite;
    d.hidden = !(filter==="all" || filter===d.dataset.coll || (filter==="ed"&&ch.length) || (filter==="off"&&e.hide) || (filter==="so"&&e.sold));
    d.querySelectorAll("input,textarea,.form button").forEach(x=>x.disabled=!canWrite);
  }
  const bu=$("#until"); if(document.activeElement!==bu) bu.value=boothUntil();
  bu.disabled=!canWrite; $("#boothWas").hidden=boothUntil()===LIVE.booth.until; $("#boothWas").textContent="เดิม: "+thaiDate(LIVE.booth.until);
  $("#boothState").textContent = Date.parse(boothUntil()+"T23:59:59+07:00")<Date.now() ? "ตอนนี้ประกาศซ่อนอยู่" : "ประกาศโชว์บนหน้าแรกถึง "+thaiDate(boothUntil());
  const all=NS.map(eff);
  $("#nShow").textContent=all.filter(p=>!p.hide).length; $("#nOff").textContent=all.filter(p=>p.hide).length; $("#nSold").textContent=all.filter(p=>p.sold).length;
  const cs=changes(); $("#nEd").textContent=cs.length;
  $("#bar").hidden=!cs.length||!canWrite;
  $("#barN").textContent=`แก้ไว้ ${cs.length} อย่าง`;
  const ol=$("#chList"); ol.innerHTML="";
  for(const c of cs){ const li=document.createElement("li"); li.textContent=changeText(c); ol.appendChild(li); }
  $("#review").hidden = $("#review").hidden || !cs.length;
  $("#noCh").hidden=!!cs.length;
}

/* ---------- drafts: one write at a time per document, coalesced per pause ---------- */
const pending={}, timers={}, busy={};
function edit(n,f,v,now){
  if(!canWrite) return;
  if(f!=="price"||(Number.isInteger(v)&&v>=1&&v<=99999)) pending[n]=Object.assign(pending[n]||{},{[f]:v});
  paintSoon(n,f,v);
  clearTimeout(timers[n]); timers[n]=setTimeout(()=>flush(n), now?0:700);
}
function paintSoon(n,f,v){ const d=drafts["p"+n]||{}; drafts["p"+n]=Object.assign({},LIVE.products[n],pick(d),{[f]:v}); paint(); }
async function flush(n){
  if(busy[n]){ timers[n]=setTimeout(()=>flush(n),300); return; }
  const p=pending[n]; if(!p) return; delete pending[n];
  const body=Object.assign({},LIVE.products[n],pick(drafts["p"+n]),p);
  for(const f of ["name","hook","size"]) if(!String(body[f]).trim()){ toast(LABEL[f]+"ว่างไม่ได้ ใช้ค่าเดิมไว้ก่อน"); body[f]=LIVE.products[n][f]; }
  delete body.coll; drafts["p"+n]=body; paint();
  const same=FIELDS.every(f=>body[f]===LIVE.products[n][f]);
  busy[n]=true;
  try{
    if(same) await db.doc("drafts/p"+n).delete();
    else await db.doc("drafts/p"+n).set(Object.assign({},pick(body),{at:Date.now(),by:me||""}));
    toast("บันทึกร่างแล้ว");
  }catch(e){ failWrite(e); }
  busy[n]=false;
}
function failWrite(e){
  if(e&&e.code==="invalid_argument"){ canWrite=false; paint(); $("#ro").hidden=false; }
  else toast("บันทึกไม่ได้ตอนนี้ ลองอีกครั้ง");
}
let boothBusy=false;
async function saveBooth(v){
  if(!canWrite||!/^20\d\d-\d\d-\d\d$/.test(v)||boothBusy) return;
  drafts.booth={until:v}; paint(); boothBusy=true;
  try{ if(v===LIVE.booth.until) await db.doc("drafts/booth").delete(); else await db.doc("drafts/booth").set({until:v,at:Date.now(),by:me||""}); toast("บันทึกร่างแล้ว"); }
  catch(e){ failWrite(e); }
  boothBusy=false;
}

/* ---------- send: a request with the reviewed drafts, then a Claude Code session that applies it ---------- */
function snapshotDrafts(){
  const products={};
  for(const n of NS){ const ch=diff(n); if(ch.length){ const e=eff(n); products[n]={}; for(const f of ch) products[n][f]=e[f]; } }
  const out={products}; if(boothUntil()!==LIVE.booth.until) out.booth={until:boothUntil()};
  return out;
}
async function send(){
  const btn=$("#go"); btn.disabled=true; $("#fallback").hidden=true;
  for(const n of Object.keys(pending)) await flush(n);
  const cs=changes(); if(!cs.length){ btn.disabled=false; return; }
  const ref=db.collection("requests").doc();
  const req={at:Date.now(),by:me||"",status:"waiting",changes:cs.map(changeText),drafts:snapshotDrafts(),note:$("#memo").value.trim().slice(0,300),boothBase:CFG.boothBase};
  try{ await ref.set(req); }catch(e){ failWrite(e); btn.disabled=false; return; }
  $("#sentId").textContent=ref.id;
  const msg=`ขึ้นเว็บตาม OCT.26 Web Builder คำขอ ${ref.id}\nทำตาม website/builder/APPLY.md · หน้า Web Builder: ${CFG.url}`;
  $("#msg").textContent=msg;
  const mcp=await use("mcp");
  if(!mcp){ $("#fallback").hidden=false; $("#why").textContent="หน้านี้สั่ง Claude เองไม่ได้ในมุมมองนี้"; btn.disabled=false; return; }
  $("#sending").hidden=false;
  try{
    const r=await mcp.callTool("Claude Code Remote","create_session",{environment_id:CFG.env,source_url:CFG.repo,source_revision:CFG.base,outcome_branch:CFG.work,
      title:"OCT.26 Web Builder · "+ref.id,prompt:msg});
    const sid=(JSON.stringify(r.payload??r).match(/session_[A-Za-z0-9]+/)||[])[0]||"";
    try{ await ref.update({status:"working",session:sid,startedAt:Date.now()}); }catch(_){}
    toast("ส่งให้ Claude แล้ว");
    $("#review").hidden=true;
  }catch(e){
    const why={server_not_connected:"ยังไม่ได้เพิ่ม Claude Code Remote ใน claude.ai Settings → Connectors",needs_reauth:"ต้องเชื่อม Claude Code Remote ใหม่ใน claude.ai Settings → Connectors",
      approval_required:"ต้องกดอนุญาตให้หน้านี้สั่ง Claude Code ก่อน กดขึ้นเว็บอีกครั้งแล้วเลือกอนุญาต",not_in_manifest:"หน้านี้ยังไม่ได้รับอนุญาตให้สั่ง Claude Code",
      server_unavailable:"Claude Code ไม่ตอบตอนนี้ อาจเริ่มไปแล้ว ดูสถานะด้านล่างก่อนกดใหม่",upstream_error:"Claude Code ไม่ตอบตอนนี้ อาจเริ่มไปแล้ว ดูสถานะด้านล่างก่อนกดใหม่"}[e&&e.code];
    $("#why").textContent=(why||"สั่ง Claude Code ไม่สำเร็จ")+" หรือวางข้อความนี้ใน Claude Code (สภาพแวดล้อม OCT.26) เอง";
    $("#fallback").hidden=false;
  }
  $("#sending").hidden=true; btn.disabled=false;
}

function paintReqs(){
  const box=$("#reqs"); box.innerHTML="";
  $("#noReq").hidden=!!reqs.length;
  const word={waiting:"รอ Claude",working:"Claude กำลังทำ",review:"รอกด Merge",live:"ขึ้นเว็บแล้ว",failed:"ไม่ผ่าน"};
  for(const r of reqs){
    const d=r.data(), el=document.createElement("div"); el.className="req";
    const h=document.createElement("div"); h.className="h";
    const t=document.createElement("b"); t.textContent=new Date(d.at||0).toLocaleString("th-TH",{dateStyle:"medium",timeStyle:"short"});
    const pl=document.createElement("span"); const st=word[d.status]?d.status:"waiting"; pl.className="pill "+st; pl.textContent=word[st];
    h.append(t,pl); el.appendChild(h);
    const s=document.createElement("small"); s.textContent=`คำขอ ${r.id} · ${(d.changes||[]).length} อย่าง`+(d.commit?` · commit ${String(d.commit).slice(0,7)}`:""); el.appendChild(s);
    for(const c of (d.changes||[]).slice(0,6)){ const li=document.createElement("small"); li.textContent="• "+c; el.appendChild(li); }
    if(d.result){ const p=document.createElement("p"); p.style.fontSize="14px"; p.textContent=d.result; el.appendChild(p); }
    if(d.pr&&/^https:\/\/github\.com\//.test(d.pr)){ const a=document.createElement("a"); a.href=d.pr; a.target="_blank"; a.rel="noopener"; a.textContent=d.status==="review"?"เปิด GitHub แล้วกด Merge":"ดูใน GitHub"; a.className=d.status==="review"?"btn order":""; a.style.fontSize="14px"; a.style.alignSelf="flex-start"; el.appendChild(a); }
    if(d.session){ const a=document.createElement("a"); a.href="https://claude.ai/code/"+encodeURIComponent(d.session); a.target="_blank"; a.rel="noopener"; a.textContent="ดูที่ Claude ทำ"; a.style.fontSize="14px"; el.appendChild(a); }
    box.appendChild(el);
  }
}

async function start(){
  build(); paint();
  document.querySelectorAll("[data-filter]").forEach(b=>b.addEventListener("click",()=>{ filter=b.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach(x=>x.setAttribute("aria-pressed",String(x===b))); paint(); }));
  $("#until").addEventListener("change",e=>saveBooth(e.target.value));
  $("#hideNow").addEventListener("click",()=>{ const d=new Date(Date.now()+7*3600e3-864e5).toISOString().slice(0,10); saveBooth(d); });
  $("#openReview").addEventListener("click",()=>{ $("#review").hidden=false; paint(); $("#review").scrollIntoView({behavior:"smooth",block:"start"}); });
  $("#go").addEventListener("click",send);
  $("#clear").addEventListener("click",()=>{ $("#clearAsk").hidden=false; });
  $("#clearNo").addEventListener("click",()=>{ $("#clearAsk").hidden=true; });
  $("#clearYes").addEventListener("click",async()=>{ $("#clearAsk").hidden=true;
    for(const k of Object.keys(drafts)){ try{ await db.doc("drafts/"+k).delete(); }catch(e){ failWrite(e); break; } delete drafts[k]; }
    paint(); toast("ล้างร่างแล้ว"); });
  $("#copy").addEventListener("click",()=>{ const t=$("#msg").textContent, b=$("#copy");
    const sel=()=>{ const r=document.createRange(); r.selectNodeContents($("#msg")); const w=getSelection(); w.removeAllRanges(); w.addRange(r); b.textContent="เลือกข้อความแล้ว กดคัดลอก"; };
    try{ navigator.clipboard.writeText(t).then(()=>{ b.textContent="คัดลอกแล้ว"; },sel); }catch(_){ sel(); } });

  db = await use("db");
  const user = await use("user");
  if(!db){ $("#ro").hidden=false; return; }
  me = user ? await user.id().catch(()=>null) : null;
  const w = user ? await Promise.resolve(user.can("data.write")).catch(()=>null) : null;
  canWrite = w!==false; $("#ro").hidden=canWrite;
  db.collection("drafts").onSnapshot(s=>{
    for(const k of Object.keys(drafts)) if(!s.docs.some(d=>d.id===k) && !pending[k.slice(1)] && !busy[k.slice(1)]) delete drafts[k];
    for(const d of s.docs){ const n=d.id.slice(1); if(pending[n]||busy[n]) continue; drafts[d.id]=d.data(); }
    paint();
  },()=>{});
  db.collection("requests").orderBy("at","desc").limit(8).onSnapshot(s=>{ reqs=s.docs; paintReqs(); $("#inReview").hidden=!reqs.some(r=>r.data().status==="review"); },()=>{});
  paint();
}
start();
"""


def page():
    live = A.live()
    for n, p in live["products"].items():
        p["coll"] = next(q["coll"] for q in B.PRODUCTS if q["n"] == int(n))
    cfg = dict(url=URL, env=ENV, repo=REPO_URL, base=BASE, work=WORK, site=W.SITE_URL, boothBase=B.BOOTH["until"])
    js = JS.replace("/*LIVE*/{}", json.dumps(live, ensure_ascii=False)).replace("/*CFG*/{}", json.dumps(cfg))
    n = len(live["products"])
    return f"""<title>OCT.26 Web Builder</title>
<meta name="claude:viewport-fit-sides" content="cover">
{S.FONT_LINK}<style>{S.CSS}{W.SITE_CSS}{CSS}</style>
<header class="top"><div class="in"><a class="mark" href="{W.SITE_URL}" target="_blank" rel="noopener" aria-label="เปิดเว็บ OCT. 26">
{W.logo_svg("oct-wordmark.svg", "mark-light")}{W.logo_svg("oct-wordmark-reverse.svg", "mark-dark")}<span class="tool">Web Builder</span></a>
<a class="btn" href="{W.SITE_URL}" target="_blank" rel="noopener">เปิดเว็บจริง</a></div></header>
<div class="wrap"><main>
<section style="padding-top:var(--s5)"><span class="eyebrow">แก้เว็บเองได้ ไม่ต้องเขียนโค้ด</span>
<h1>แก้ราคา ชื่อ และของหมด แล้วกดขึ้นเว็บ</h1>
<p class="lead">แตะสินค้าเพื่อแก้ ทุกอย่างบันทึกเป็นร่างทันที เว็บจริงยังไม่เปลี่ยน กด “ขึ้นเว็บ” แล้ว Claude ทำโปสเตอร์และเว็บใหม่ ส่งมาให้กด Merge ที่ GitHub กดแล้วเว็บเปลี่ยน</p>
<p class="note warn" id="ro" hidden>เปิดหน้านี้ในบัญชี claude.ai ของเจ้าของร้านเพื่อแก้ไข ตอนนี้ดูได้อย่างเดียว</p>
<div class="sum"><div><b id="nShow">{n}</b><span>สินค้าที่โชว์บนเว็บ</span></div><div><b id="nOff">0</b><span>ซ่อนอยู่</span></div>
<div><b id="nSold">0</b><span>หมดชั่วคราว</span></div><div class="hot"><b id="nEd">0</b><span>แก้ไว้ ยังไม่ขึ้นเว็บ</span></div></div></section>

<section id="booth"><span class="eyebrow">หน้าแรก</span><h2>ประกาศออกบูธ</h2>
<div class="card stack"><p id="boothState" class="cap"></p>
<div class="f"><label for="until">แสดงประกาศถึงวันที่ (หายเองหลังเที่ยงคืนวันนั้น)</label><input type="date" id="until"><span class="was" id="boothWas" hidden></span></div>
<div class="row"><button type="button" id="hideNow">ซ่อนประกาศตั้งแต่วันนี้</button></div></div></section>

<section id="shop"><span class="eyebrow">สินค้า {n} แบบ</span><h2>สินค้าบนเว็บ</h2>
<div class="chips" role="group" aria-label="กรองสินค้า">
<button type="button" data-filter="all" aria-pressed="true">ทั้งหมด</button><button type="button" data-filter="soi2" aria-pressed="false">SOI. 02</button>
<button type="button" data-filter="love" aria-pressed="false"><span class="fb">ห้าหมี</span>&nbsp;Love</button>
<button type="button" data-filter="ed" aria-pressed="false">แก้แล้ว</button><button type="button" data-filter="off" aria-pressed="false">ซ่อน</button>
<button type="button" data-filter="so" aria-pressed="false">หมด</button></div>
<div class="list" id="list"></div></section>

<section id="review" hidden><span class="eyebrow">ตรวจก่อนขึ้นเว็บ</span><h2>สิ่งที่จะเปลี่ยน</h2>
<div class="card review"><ol id="chList"></ol><p class="empty" id="noCh" hidden>ยังไม่มีอะไรแก้</p>
<p class="cap">เปลี่ยนชื่อ ราคา หรือประโยคขาย Claude จะทำโปสเตอร์สินค้านั้นใหม่ด้วย ราคาในแผนบูธจะเปลี่ยนตามเพราะใช้ข้อมูลชุดเดียวกัน</p>
<div class="f"><label for="memo">ฝากบอก Claude (ไม่ใส่ก็ได้)</label><textarea id="memo" maxlength="300"></textarea></div>
<div class="row"><button type="button" class="primary order" id="go">ขึ้นเว็บ</button><button type="button" id="clear">ล้างร่างทั้งหมด</button></div>
<div class="note warn" id="clearAsk" hidden><p>ล้างร่างทั้งหมด แล้วกลับไปเหมือนเว็บตอนนี้?</p>
<div class="row" style="margin-top:var(--s2)"><button type="button" id="clearYes">ล้างเลย</button><button type="button" id="clearNo">ไม่ล้าง</button></div></div>
<p class="note" id="inReview" hidden>มีงานรอกด Merge อยู่ ส่งเพิ่มได้ Claude จะรวมไว้ในงานเดียวกัน กด Merge ครั้งเดียวขึ้นเว็บทั้งหมด</p>
<p class="note" id="sending" hidden>กำลังส่งให้ Claude … หน้าต่างขออนุญาตอาจขึ้นมาครั้งแรก</p>
<div class="note warn stack" id="fallback" hidden><p>บันทึกคำขอ <b id="sentId"></b> แล้ว <span id="why"></span></p>
<pre class="msg" id="msg"></pre><div class="row"><button type="button" id="copy">คัดลอกข้อความ</button></div></div></div></section>

<section id="history"><span class="eyebrow">ประวัติ</span><h2>การขึ้นเว็บ</h2>
<p class="cap">Claude ใช้เวลาราว 5–10 นาที ทำโปสเตอร์และเว็บใหม่ แล้วเปิดงานให้กด Merge ที่ GitHub พอกด Merge แล้ว Cloudflare เปลี่ยนเว็บในไม่กี่นาที</p>
<p class="empty" id="noReq">ยังไม่เคยขึ้นเว็บจากหน้านี้ คำขอแรกจะขึ้นที่นี่พร้อมสถานะ</p>
<div class="reqs" id="reqs"></div></section>
</main></div>
<div class="bar" id="bar" hidden><div class="in"><div><b id="barN"></b><small>ร่างบันทึกแล้ว เว็บจริงยังไม่เปลี่ยน</small></div>
<button type="button" class="primary" id="openReview">ตรวจแล้วขึ้นเว็บ</button></div></div>
<div class="toast" id="toast" role="status" hidden></div>
<script>{js}</script>
"""


if __name__ == "__main__":
    open(os.path.join(HERE, "index.html"), "w").write(page())
    json.dump(A.live(), open(A.LIVE, "w"), ensure_ascii=False, indent=1)
    print("wrote", os.path.join(HERE, "index.html"))
