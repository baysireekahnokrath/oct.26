
const FAM = [["พ่อ","แดงดินลูกรัง","#A9442B"],["แม่","เขียวใบตอง","#5E7A3A"],["ลูกคนโต","เหลืองทานตะวัน","#E9A825"],["ลูกคนกลาง","ม่วงดอกอินทนิล","#B9A3D6"],["ลูกคนเล็ก","น้ำเงินคราม","#2E4A7D"]];
const LEATHER = [["ดำ","#2D2926"],["ช็อกโกแลต","#4B3328"],["คอนญัก","#7A4330"],["น้ำตาลหนัง","#B07A4A"],["ทราย","#C9A77E"],["ครีม","#E5DAC4"],["เทาตุ่น","#857A71"],["น้ำเงินหม่น","#3E4A5D"]];
const INK = [["ขาว","#FBF7EE"],["ดำ","#24201E"],["แดงดิน","#A9442B"],["เขียวใบตอง","#5E7A3A"],["เหลือง","#E9A825"],["ม่วง","#B9A3D6"],["คราม","#2E4A7D"]];
const FACES = [["none","ไม่แต่ง"],["smile","ยิ้ม"],["sleep","หลับตา"],["wow","ว้าว"],["wink","ขยิบตา"],["tongue","แลบลิ้น"],["shy","เขิน"]];
// where a face sits on each cut-out photo: centre x, y and width, in % of the image
const ANCHOR = {"01-1":[45,59,48],"01-2":[45,58,48],"03-1":[50,50,42],"03-2":[50,50,42],"04-1":[50,50,50],"04-3":[50,50,50],"05-1":[50,50,54],"05-3":[50,50,54],"07-1":[50,50,40],"07-2":[50,50,40]};
// same, on the die drawings (mm): 01 sits on the round head, not the ears
const ANCHOR_MM = {"01":[41.7,63,46],"02":[45,45,40],"03":[45,45,40],"04":[45,45,46],"05":[45,45,48],"07":[45,45,38]};
const $ = (s, el=document) => el.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const band = () => `<div class="band" aria-hidden="true">${FAM.map(f=>`<span style="background:${f[2]}"></span>`).join("")}</div>`;
let toastT; function toast(t){ const el=$("#toast"); el.textContent=t; el.hidden=false; clearTimeout(toastT); toastT=setTimeout(()=>el.hidden=true,2400); }

/* ---------- die shapes ---------- */
function pathD(code){ const s=SH[code]; return [s.outline,...s.holes].map(p=>"M"+p.map(q=>q[0]+" "+q[1]).join("L")+"Z").join(""); }
function clipD(code){ const s=SH[code]; return "M"+s.outline.map(p=>(p[0]/s.w).toFixed(4)+" "+(p[1]/s.h).toFixed(4)).join("L")+"Z"; }
function sil(code, fill, opts={}){
  const s=SH[code], sw=opts.stroke?`stroke="${opts.stroke}" stroke-width="${opts.sw||1}" vector-effect="non-scaling-stroke" stroke-linejoin="round"`:"";
  const slits = opts.slits===false?"":s.slits.map(l=>`<line x1="${l[0]}" y1="${l[1]}" x2="${l[2]}" y2="${l[3]}" stroke="${opts.slit||"rgba(0,0,0,.45)"}" stroke-width="${opts.sw||1}" vector-effect="non-scaling-stroke"/>`).join("");
  const f = opts.face ? (()=>{ const a=ANCHOR_MM[code]; return `<g transform="translate(${a[0]-a[2]/2} ${a[1]-a[2]/2}) scale(${a[2]/100})">${faceG(opts.face[0],opts.face[1])}</g>`; })() : "";
  return `<svg viewBox="0 0 ${s.w} ${s.h}" aria-hidden="true" class="${opts.cls||""}" style="overflow:visible"><path d="${pathD(code)}" fill="${fill}" fill-rule="evenodd" ${sw}/>${slits}${f}</svg>`;
}
const CODES = ["01","02","03","04","05","07"];

/* ---------- painted faces: drawn like acrylic paint on leather (wobbly edges via #paint) ---------- */
function faceG(style, ink, cheek="#D9765F", filt=true){
  if(style==="none") return "";
  const sw=(w=5)=>`fill="none" stroke="${ink}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"`, st=sw();
  const ck=`<circle cx="22" cy="60" r="${style==="shy"?11:8}" fill="${cheek}" opacity=".6"/><circle cx="78" cy="60" r="${style==="shy"?11:8}" fill="${cheek}" opacity=".6"/>`;
  const dot=(x,y,r=5)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${ink}"/>`;
  const nose=`<path d="M48 52 Q50 56 52 52" ${sw(4)}/>`;
  let g="";
  if(style==="smile") g=dot(33,42)+dot(67,42)+nose+`<path d="M37 64 Q50 77 63 64" ${st}/>`;
  if(style==="sleep") g=`<path d="M25 42 Q33 49 41 42" ${st}/><path d="M59 42 Q67 49 75 42" ${st}/>`+nose+`<path d="M42 66 Q50 72 58 66" ${st}/>`;
  if(style==="wow") g=`<circle cx="33" cy="41" r="8" ${sw(4)}/><circle cx="67" cy="41" r="8" ${sw(4)}/>`+dot(33,42,3)+dot(67,42,3)+`<ellipse cx="50" cy="68" rx="6" ry="8" ${sw(4)}/>`;
  if(style==="wink") g=dot(33,42)+`<path d="M60 44 L68 39 L76 44" ${st}/>`+nose+`<path d="M37 63 Q50 76 63 63" ${st}/>`;
  if(style==="tongue") g=dot(33,42)+dot(67,42)+`<path d="M36 63 Q50 74 64 63" ${st}/><path d="M46 69 Q50 80 55 69" fill="#D9765F" stroke="${ink}" stroke-width="3"/>`;
  if(style==="shy") g=dot(34,43,4)+dot(66,43,4)+`<path d="M45 64 Q50 67 55 64" ${sw(4)}/>`;
  return `<g ${filt?'filter="url(#paint)"':""}>${ck}${g}</g>`;
}
function faceSvg(style, ink, w){ return `<svg class="face" viewBox="0 0 100 100" style="${w}" aria-hidden="true">${faceG(style,ink)}</svg>`; }
// a cut-out photo with an optional painted face
function pc(cut, face, extra="", alt=""){
  const a=ANCHOR[cut]||[50,50,48];
  const f=face&&face[0]!=="none"?faceSvg(face[0],face[1],`left:${a[0]}%;top:${a[1]}%;width:${a[2]}%`):"";
  return `<span class="pc" ${extra}><img src="/assets/cut/${cut}.webp" alt="${esc(alt)}" loading="lazy">${f}</span>`;
}

/* ---------- craft textures, built once from the die files ---------- */
(function textures(){
  const grain=`<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .4  0 0 0 .55 0'/></filter><rect width='220' height='220' filter='url(%23n)'/></svg>`;
  const stamp=(codes,col)=>{ let g=""; codes.forEach((c,i)=>{ const s=SH[c], k=46/Math.max(s.w,s.h), x=(i%2)*75+14, y=Math.floor(i/2)*75+14;
    g+=`<g transform='translate(${x} ${y}) rotate(${i*17} 23 23) scale(${k.toFixed(3)})'><path d='${pathD(c)}' fill='none' stroke='${col}' stroke-width='${(2.2/k).toFixed(2)}' fill-rule='evenodd'/></g>`; });
    return `url("data:image/svg+xml,${encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='150' height='150'>${g}</svg>`)}")`; };
  const css=`:root{--grain:url("data:image/svg+xml,${grain.replace(/#/g,"%23").replace(/"/g,"'").replace(/</g,"%3C").replace(/>/g,"%3E")}")}
.p-stamp{--stamp:${stamp(["05","07","03","04"],"rgba(42,39,37,.13)")}}
.bg-dad.p-stamp,.bg-mom.p-stamp,.bg-bene.p-stamp,.bg-charcoal.p-stamp,.bg-hide.p-stamp,.bg-teak.p-stamp{--stamp:${stamp(["07","05","04","03"],"rgba(244,240,232,.18)")}}`;
  const st=document.createElement("style"); st.textContent=css; document.head.appendChild(st);
})();

/* ---------- shared content ---------- */
// the booth notice takes itself down after the last fair day
const boothOn = () => Date.now() <= Date.parse(BOOTH.until+"T23:59:59+07:00");
function booth(){ return `<div class="booth"><b>ออกบูธ ${esc(BOOTH.fair)}</b><span>${esc(BOOTH.place)} · ${esc(BOOTH.dates)} · ${esc(BOOTH.hours)}</span>
<span class="cap">${esc(BOOTH.blank)}</span></div>`; }
function storyText(){ return `<p class="lead">OCT. 26 คือวันเกิดของแม่ เราเริ่มจากเศษหนังวัวแท้ที่เกือบถูกขายทิ้ง ตัดเป็นแพตเทิร์นเรียบ ๆ ด้วยบล็อกขนาดจริง แล้วทำกันเองทั้งบ้าน พ่อ แม่ และลูกสามคน</p>
<p>ห้าสีในหน้านี้คือสีของคนในบ้าน แดงดินลูกรัง เขียวใบตอง เหลืองทานตะวัน ม่วงดอกอินทนิล น้ำเงินคราม ส่วนขอบหนังเราไม่ทาสี ให้เห็นเนื้อหนังจริง</p>`; }
function famRow(){ return `<div class="row" style="gap:var(--s3)">${FAM.map(f=>`<span class="cap" style="display:flex;align-items:center;gap:6px;opacity:1"><i style="width:16px;height:16px;border-radius:50%;background:${f[2]};display:inline-block;box-shadow:0 0 0 2px var(--sbg),0 0 0 3px currentColor"></i>${f[0]} · ${f[1]}</span>`).join("")}</div>`; }
function facts(){ return `<div class="row" style="gap:var(--s5)">${[["6","แพตเทิร์น 01–05 และ 07"],["1.0–1.2","มม. หนังวัวแท้"],["0","สีทาขอบ เห็นเนื้อหนังจริง"]].map(f=>`<div><div class="latin" style="font-size:40px;font-weight:300;line-height:1">${f[0]}</div><div class="cap">${f[1]}</div></div>`).join("")}</div>`; }
// buying besides LINE: the Shopee shop link once catalog.json has it, else the shop's name to search for
const shopee = () => LINK.shopeeUrl ? `<a href="${esc(LINK.shopeeUrl)}" target="_blank" rel="noopener">ซื้อใน Shopee</a>` : `ค้นหาร้าน ${esc(LINK.shopee)} ใน Shopee`;
const DIYNOTE = `<p class="cap">สินค้าทุกชิ้นเป็นชิ้นเรียบ ไม่ได้วาดหน้า · สั่งทาง LINE ${LINK.lineId} ไอจี ${LINK.igHandle} หรือ${shopee()}</p>`;
// what a card shows: the cut-out, else the photo; only a die drawing (no real photo yet) becomes the die outline
function piece(x, note){
  if(x.cut) return pc(x.cut,null,"",`${x.name} หนังวัวแท้`);
  if(x.kind==="set") return pc("05-1",null);
  if(!x.img.startsWith("die")) return `<img src="/assets/img/${x.img}.jpg" alt="${esc(ALT[x.img]||x.name)}" loading="lazy">`;
  return `<span class="pc" style="width:62%">${sil(x.n,"#B07A4A",{slit:"rgba(0,0,0,.3)"})}</span>${note?'<span class="note02">ยังไม่มีรูปจริง</span>':""}`;
}

function media(p, mode, t){
  const bg=t?`style="--t:${t}"`:"";
  if(mode==="photo") return `<div class="media" ${bg}><img src="/assets/img/${p.img}.jpg" alt="${esc(ALT[p.img]||p.name)}" loading="lazy">${p.n==="02"?'<span class="note02">ภาพจากบล็อกตัด</span>':""}</div>`;
  if(p.kind==="set") return `<div class="media mx" ${bg}>${p.cuts.map(c=>c==="02"?sil("02","#B07A4A",{slit:"rgba(0,0,0,.3)"}):pc(c,null)).join("")}</div>`;
  if(mode==="shape"){
    const inner = p.cut?`<image href="/assets/cut/${p.cut}.webp" x="-.06" y="-.06" width="1.12" height="1.12" preserveAspectRatio="xMidYMid slice"/>`:`<rect width="1" height="1" fill="#B07A4A"/>`;
    const a=ANCHOR_MM[p.n], s=SH[p.n];
    return `<div class="media"><svg class="shaped" viewBox="0 0 1 1" aria-label="${esc(p.name)}" style="overflow:visible"><defs><clipPath id="cp${p.id}" clipPathUnits="objectBoundingBox"><path d="${clipD(p.n)}"/></clipPath></defs>
      <g clip-path="url(#cp${p.id})"><rect width="1" height="1" fill="#C89A6A"/>${inner}</g>
      <g transform="translate(${(a[0]-a[2]/2)/s.w} ${(a[1]-a[2]/2)/s.h}) scale(${a[2]/s.w/100} ${a[2]/s.h/100})">${faceG(p.face[0],p.face[1])}</g></svg><span class="tagdiy">ตัวอย่างแต่ง</span></div>`;
  }
  // product cards always show the plain piece: what the customer receives
  return `<div class="media" ${bg}>${piece(p,true)}</div>`;
}
function card(p, mode, t){
  const food = p.food?`<span class="food">ไม่ใช่ภาชนะใส่อาหาร</span>`:"";
  const ask = `สนใจ ${p.id} ${p.name} ${p.price} บาท`;
  const buy = `<a class="buy" href="${LINK.line}" target="_blank" rel="noopener" data-copy="${esc(ask)}">ทัก LINE</a>`;
  if(mode==="editorial") return `<article class="card">${media(p,"photo",t)}<span class="no">${p.n==="MX"?"SET":p.n}</span><h3>${esc(p.name)}</h3><span class="spec">${p.size}</span>${food}<span class="price">${p.price}.-</span>${buy}</article>`;
  if(mode==="swatch") return `<article class="card">${media(p,"cut",t)}<div class="lab"><span class="code">${p.id}</span><h3>${esc(p.name)}</h3><span class="spec">${p.size}</span>${food}<div class="row" style="justify-content:space-between"><span class="price">${p.price}.-</span>${buy}</div></div></article>`;
  if(mode==="tile") return `<article class="card" data-kind="${p.kind}">${media(p,"tile",t)}<h3>${esc(p.name)}</h3><span class="spec">${p.size}</span>${food}<div class="row"><span class="price">${p.price}.-</span>${buy}</div></article>`;
  if(mode==="shape") return `<article class="card">${media(p,"shape")}<h3>${esc(p.name)}</h3>${food}<div class="pill"><span class="price">${p.price}.-</span>${buy}</div></article>`;
  return `<article class="card"><a class="plink" href="/p/${p.id}">${media(p,mode,t)}<h3>${esc(p.name)}</h3></a><span class="spec">${p.size} · หนังวัวแท้จากเศษหนัง</span>${food}${p.out?'<span class="soldout">ของหมด</span>':""}<span class="price">${p.price} บาท</span><a class="buy" href="/p/${p.id}">ดูรายละเอียด</a></article>`;
}
function shop(mode, tints){ return `<div class="shop">${PROD.map((p,i)=>card(p,mode,tints?tints[i%tints.length]:null)).join("")}</div>${DIYNOTE}`; }

function corp(){ return `<div class="split"><div class="stack">
<p class="lead">ของที่ระลึกจากหนังแท้ สำหรับงานสัมมนา งานเปิดตัว และของขวัญลูกค้า เลือกแพตเทิร์น โทนหนัง และหน้าที่วาด การ์ดในซองพิมพ์ข้อความหรือโลโก้องค์กร</p>
<ul class="ticks"><li>เลือกจาก 6 แพตเทิร์น 01–05 และ 07 ใช้แบบที่เลือกในตัวจำลองได้เลย</li><li>วาดหน้า หรือเขียนชื่อพนักงานทีละชิ้น (ไอเดีย รอยืนยัน)</li><li>ห่อในซองพร้อมการ์ด แจกได้ทันที</li></ul>
<div class="steps"><div>บอกจำนวน และวันที่ใช้</div><div>ส่งตัวอย่างสีหนัง ให้เลือก</div><div>ผลิต ห่อ และส่ง</div></div>
<div class="row"><a class="btn solid" href="${LINK.line}" target="_blank" rel="noopener" data-corp="1">ขอใบเสนอราคาทาง LINE</a></div>
<p class="cap">จำนวนขั้นต่ำ ราคา และระยะผลิต คุยกันทาง LINE ตามงานของคุณ</p></div>
<div class="panel"><div class="field"><label for="org">ลองใส่ชื่อองค์กร ดูการ์ดในซอง</label><input id="org" maxlength="40" value="บริษัทของคุณ" autocomplete="off"></div>
<div class="ncard">${LOGO.light}<div><b data-org>บริษัทของคุณ</b><small>ขอบคุณที่มาร่วมงาน · ทำจากเศษหนังวัวแท้</small></div>${band()}</div>
<p class="cap" data-pick style="opacity:1;color:#6E6A64"></p></div></div>`; }

function work(){ return `<div class="split"><div class="stack">
<p class="lead">เวิร์กช็อปแต่งชิ้นหนังของตัวเอง เลือกแพตเทิร์น วาดหน้า เขียนชื่อ ระบายสีด้วยสีสำหรับหนัง แล้วได้ชิ้นที่แต่งเองกลับบ้าน</p>
<div class="row" style="gap:var(--s3)">${[["01-2",["smile","#24201E"]],["05-3",["wink","#FBF7EE"]],["07-2",["tongue","#24201E"]],["04-3",["sleep","#FBF7EE"]]].map(x=>`<span style="width:66px">${pc(x[0],x[1])}</span>`).join("")}</div>
<ul class="ticks"><li>ครอบครัว ทำด้วยกันที่บูธหรือที่งานอีเวนต์</li><li>ทีมงานองค์กร กิจกรรมสั้น ๆ ระหว่างสัมมนา</li><li>ร้านค้าและคาเฟ่ จัดเป็นกิจกรรมให้ลูกค้า</li></ul>
<p class="cap">ระยะเวลาและราคา คุยกันทาง LINE · เป็นการแต่งชิ้นหนัง ไม่ต่อชิ้น</p></div>
<form class="panel" data-book><div class="field"><label>แบบเวิร์กช็อป</label><div class="opts" data-one>
<button type="button" aria-pressed="true">ครอบครัว</button><button type="button" aria-pressed="false">ทีมองค์กร</button><button type="button" aria-pressed="false">อีเวนต์ / ร้านค้า</button></div></div>
<div class="field"><label>จำนวนคน</label><div class="stepper"><button type="button" data-st="-1" aria-label="ลด">−</button><output>6</output><button type="button" data-st="1" aria-label="เพิ่ม">+</button></div></div>
<div class="field"><label for="wdate">วันที่สะดวก</label><input id="wdate" type="date"></div>
<div class="field"><label for="wname">ชื่อผู้ติดต่อ</label><input id="wname" autocomplete="name" placeholder="ชื่อ"></div>
<div class="row"><button type="submit" class="btn solid">ขอจองเวิร์กช็อป</button></div></form></div>`; }

const sim = () => `<div class="sim-slot"></div>`;
function foot(cls="bg-charcoal stitch"){ return `<footer class="sec mfoot gut ${cls}"><div class="in">
<div>${LOGO.light}</div>
<div class="col"><b>สั่งซื้อ</b><a href="${LINK.line}" target="_blank" rel="noopener">LINE ${LINK.lineId}</a>${LINK.shopeeUrl?`<a href="${esc(LINK.shopeeUrl)}" target="_blank" rel="noopener">Shopee</a>`:`<span>Shopee: ${esc(LINK.shopee)}</span>`}</div>
<div class="col"><b>ติดตาม</b><a href="${LINK.ig}" target="_blank" rel="noopener">Instagram ${LINK.igHandle}</a><a href="${LINK.fb}" target="_blank" rel="noopener">Facebook oct26brand</a></div>
<div class="col"><b>OCT. 26</b><span>our crafted things.</span>${band()}<span class="cap">© 2569 OCT. 26</span></div></div></footer>`; }
// links work from any page: the home sections live at /#id
const BASE = PAGE.type==="home"?"":"/";
function head(){ const h=id=>`${BASE}#${id}`; return `<header class="mhead"><a href="/" aria-label="OCT. 26 หน้าแรก">${LOGO.light}</a><nav aria-label="เมนู"><a href="${h("story")}">เรื่องของเรา</a><a href="${h("sim")}">ลองแต่ง</a><a href="${h("shop")}">ของพร้อมส่ง</a><a href="${h("corp")}">องค์กร</a><a href="${h("work")}">เวิร์กช็อป</a></nav></header>`; }
const sec = (id, cls, eyebrow, title, body, who) => `<section class="sec gut ${cls}" id="${id}"><div class="in"><span class="eyebrow">${who!==undefined?`<span class="who-tag"><i></i>สีของ${FAM[who][0]} · ${FAM[who][1]}</span> · `:""}${eyebrow}</span><h2>${title}</h2>${body}</div></section>`;
const strip = (cls, body) => `<section class="sec gut ${cls}" style="padding-block:var(--s5)"><div class="in">${body}</div></section>`;

/* ---------- home ---------- */
function home(){
  const pool=["01-1","01-2","03-1","03-2","04-1","04-3","05-1","05-3","07-1","07-2"], fs=["smile","sleep","wow","wink","tongue","shy"];
  const dark=c=>["01-1","03-2","04-3","05-3","07-1"].includes(c);
  const lab={"01":"01 หมี","03":"03 กากบาทแคปซูล","04":"04 สี่เหลี่ยมมน","05":"05 วงกลม","07":"07 กากบาทข้อต่อวงกลม"};
  let faces=""; for(let i=0;i<30;i++){ const c=pool[(i*7+Math.floor(i/5)*3)%pool.length], f=fs[(i*5+2)%fs.length], r=((i*37)%23)-11;
    faces+=`<button type="button" data-lab="${lab[c.slice(0,2)]}" aria-label="${lab[c.slice(0,2)]}"><span style="display:block;transform:rotate(${r}deg)">${pc(c,[f,dark(c)?"#FBF7EE":"#24201E"])}</span></button>`; }
  return `<div class="sec gut bg-dad" style="padding-block:0">${head()}</div>
<section class="sec gut bg-dad" id="top" style="padding-block:var(--s3) var(--s7)"><div class="in"><div class="faces">${faces}</div>
<div class="hero-t"><span class="eyebrow"><span class="who-tag"><i></i>สีของพ่อ · แดงดินลูกรัง</span> · our crafted things.</span><h1>หน้าตาไม่ซ้ำกันสักชิ้น</h1>
<p class="lead">เศษหนังแต่ละชิ้นมีสีและลายของตัวเอง พอวาดหน้าลงไป ก็เหมือนคนละคน แตะชิ้นไหนก็ได้</p><p class="cap" id="faceLab">หน้าที่วาดเป็นไอเดียแต่งเองที่บูธและเวิร์กช็อป สินค้าที่ขายเป็นชิ้นเรียบ</p>
<div class="row" style="justify-content:center"><a class="btn solid" href="#shop">ดูของพร้อมส่ง</a><a class="btn" href="#sim">ลองวาดหน้า</a></div></div></div></section>
${strip("bg-charcoal stitch",booth())}
${sec("story","bg-mom p-ging","เรื่องของเรา","ห้าคน ห้าสี ในบ้านเดียว",`<div class="who">${FAM.map((f,i)=>`<div><span style="width:56px;height:56px;border-radius:50%;background:${f[2]};display:block;box-shadow:0 0 0 3px var(--cotton)"><svg viewBox="0 0 100 100" style="width:100%;height:100%">${faceG(fs[i],i===2||i===3?"#24201E":"#FBF7EE","#FBF7EE")}</svg></span>${f[0]}<br>${f[1]}</div>`).join("")}</div>`+storyText()+facts(),1)}
${sec("sim","bg-beiya stitch","ตัวจำลอง 3D","เลือกหน้าตาของชิ้นคุณ",sim(),2)}
${sec("shop","bg-beana p-dots","ของพร้อมส่ง",`ซื้อได้เลย ${PROD.filter(x=>!x.out).length} ชิ้น`,shop("cut",["#FBF9F4"]),3)}
${sec("corp","bg-bene p-stamp","ลูกค้าองค์กร","ของที่ระลึก ที่ไม่ซ้ำกันสักชิ้น",corp(),4)}
${sec("work","bg-cotton stitch","เวิร์กช็อป","มาแต่งหน้าตาให้ชิ้นของคุณ",band()+work())}${foot()}`;
}

/* ---------- product page ---------- */
const TONES = ["คละสี ร้านเลือกให้","โทนเข้ม","โทนกลาง","โทนอ่อน"];
const P = {id:null, qty:1, tone:0};

// pattern outline with its real width and height, from the die file (mm)
function diagram(code){
  const s=SH[code], pad=18, W=s.w+pad*2.2, H=s.h+pad*2.2;
  return `<svg class="diag" viewBox="${-pad} ${-pad} ${W} ${H}" aria-label="ขนาดจริง ${(s.w/10).toFixed(1)} × ${(s.h/10).toFixed(1)} ซม.">
<path d="${pathD(code)}" fill="#B07A4A" fill-rule="evenodd"/>${s.slits.map(l=>`<line x1="${l[0]}" y1="${l[1]}" x2="${l[2]}" y2="${l[3]}" stroke="rgba(0,0,0,.45)" stroke-width=".8"/>`).join("")}
<g stroke="#2A2725" stroke-width=".6" fill="none"><path d="M0 ${s.h+8}H${s.w}M0 ${s.h+5}v6M${s.w} ${s.h+5}v6"/><path d="M${s.w+8} 0V${s.h}M${s.w+5} 0h6M${s.w+5} ${s.h}h6"/></g>
<text x="${s.w/2}" y="${s.h+16}" text-anchor="middle" font-size="6" fill="#2A2725" font-family="Jost,sans-serif">${(s.w/10).toFixed(1)} cm</text>
<text x="${s.w+11}" y="${s.h/2}" font-size="6" fill="#2A2725" font-family="Jost,sans-serif" transform="rotate(90 ${s.w+11} ${s.h/2})" text-anchor="middle">${(s.h/10).toFixed(1)} cm</text></svg>`;
}
function slides(p, d){
  const out=[];
  d.photos.forEach((ph,i)=>out.push([`<img src="/assets/img/${ph}.jpg" alt="${esc(ALT[ph]||p.name)}" ${i?'loading="lazy"':""}>`, ph==="hand05"?"ขนาดเทียบมือ":ph==="die02"?"บล็อกตัด 02":"รูปจริง", `<img src="/assets/img/${ph}.jpg" alt="">`]));
  if(d.set) out.push([p.cuts.map(c=>c==="02"?sil("02","#B07A4A",{slit:"rgba(0,0,0,.3)"}):pc(c,null)).join(""),"4 ชิ้นในชุด",sil("05","#B07A4A",{slit:"rgba(0,0,0,.3)"}),"mx"]);
  d.cuts.forEach(c=>out.push([pc(c,null,"",`${p.name} ตัวอย่างสีหนัง`),"ตัวอย่างสีหนัง",`<img src="/assets/cut/${c}.webp" alt="" style="object-fit:contain;padding:6px">`]));
  if(!d.set) out.push([diagram(d.code),"ขนาดจริง",sil(d.code,"#B07A4A",{slit:"rgba(0,0,0,.3)"})]);
  return out;
}
function productPage(id){
  const p=PROD.find(x=>x.id===id)||PROD[0], d=PD[p.id], i=PROD.indexOf(p), sl=slides(p,d), s=SH[d.code];
  const prev=PROD[(i+PROD.length-1)%PROD.length], next=PROD[(i+1)%PROD.length];
  const others=PROD.filter(x=>x!==p).map(x=>`<a href="/p/${x.id}"><div class="media">${piece(x)}</div><b style="font-family:var(--th);font-weight:500;font-size:15px">${esc(x.name)}</b><span class="latin">${x.price}.-</span></a>`).join("");
  return `<div class="sec gut bg-dad" style="padding-block:0">${head()}</div>
<section class="sec gut bg-cotton" id="top" style="padding-block:var(--s4) var(--s6)"><div class="in">
<nav class="crumb" aria-label="ตำแหน่ง"><a href="/">หน้าแรก</a><span>›</span><a href="/#shop">ของพร้อมส่ง</a><span>›</span><span>${esc(p.name)}</span></nav>
<div class="pp"><div><div class="gal" id="gal">${sl.map(x=>`<figure class="${x[3]||""}">${x[0]}<figcaption>${x[1]}</figcaption></figure>`).join("")}</div>
<div class="thumbs" role="group" aria-label="รูปสินค้า">${sl.map((x,k)=>`<button type="button" data-slide="${k}" aria-pressed="${k===0}" aria-label="รูปที่ ${k+1}">${x[2]}</button>`).join("")}</div></div>
<div class="pinfo"><span class="eyebrow">${p.id} · แพตเทิร์น ${d.set?"01 · 02 · 04 · 05":d.code+" "+s.name}</span><h1>${esc(p.name)}</h1>
<div class="row">${p.out?'<span class="chip out">ของหมด</span>':'<span class="chip">● พร้อมส่ง</span>'}${p.food?'<span class="chip food">ไม่ใช่ภาชนะใส่อาหาร</span>':""}</div>
<p class="lead">${esc(d.lead)}</p><div class="bigprice">${p.price}.-<span class="cap" style="font-family:var(--body);font-size:14px"> / ${d.set?"ชุด":"ชิ้น"}</span></div>
${p.out?`<p class="cap">ตอนนี้หมดชั่วคราว ทัก LINE ถามรอบหน้าได้ เราตอบว่าจะมีเมื่อไร</p>
<div class="row"><a class="btn solid" href="${LINK.line}" target="_blank" rel="noopener" data-order="1">ถามรอบหน้าทาง LINE</a></div>`:`<div class="field"><label>โทนสีหนังที่อยากได้</label><div class="opts" data-tone>${TONES.map((t,k)=>`<button type="button" data-t="${k}" aria-pressed="${k===P.tone}">${t}</button>`).join("")}</div></div>
<p class="cap">เศษหนังแต่ละชิ้นสีไม่ซ้ำกัน เราส่งรูปชิ้นจริงให้ดูในแชทก่อนโอนทุกครั้ง</p>
<div class="field"><label>จำนวน</label><div class="qty"><button type="button" data-q="-1" aria-label="ลด">−</button><output id="qty">${P.qty}</output><button type="button" data-q="1" aria-label="เพิ่ม">+</button></div></div>
<div class="row"><a class="btn solid" href="${LINK.line}" target="_blank" rel="noopener" data-order="1">สั่งทาง LINE</a></div>
<p class="cap">หรือ${shopee()} · ค่าส่งแจ้งในแชท</p>`}${d.note?`<p class="cap">${esc(d.note)}</p>`:""}
<div class="row cap"><a href="/p/${prev.id}">‹ ${esc(prev.name)}</a><span style="flex:1"></span><a href="/p/${next.id}">${esc(next.name)} ›</a></div></div></div></div></section>
${sec("detail","bg-mom p-ging","รายละเอียด","ชิ้นนี้ทำจากอะไร",`<table class="spec"><tbody>
<tr><th>รหัส</th><td>${p.id}</td></tr><tr><th>แพตเทิร์น</th><td>${d.set?"01 หมี · 02 กังหัน · 04 สี่เหลี่ยมมน · 05 วงกลม":d.code+" "+s.name}</td></tr>
<tr><th>ขนาด</th><td>${p.size}${d.set?" (4 ชิ้น)":` · ${(s.w/10).toFixed(1)} × ${(s.h/10).toFixed(1)} ซม. ตามบล็อกตัด`}</td></tr>
<tr><th>ความหนา</th><td>1.0–1.2 มม.</td></tr><tr><th>วัสดุ</th><td>หนังวัวแท้จากเศษหนัง สีและลายแต่ละชิ้นไม่ซ้ำ</td></tr>
<tr><th>ขอบ</th><td>ไม่ทาสี เห็นเนื้อหนังจริง</td></tr><tr><th>ดูแล</th><td>เช็ดด้วยผ้าแห้ง เลี่ยงน้ำขังและแดดจัด</td></tr>
${p.food?"<tr><th>หมายเหตุ</th><td>ไม่ใช่ภาชนะใส่อาหาร ใช้รองใต้แก้วเท่านั้น</td></tr>":""}
<tr><th>ในกล่อง</th><td>${d.set?"4 ชิ้น":"1 ชิ้น"} · การ์ดในซอง มีห้าสีของบ้านอยู่ข้างใน</td></tr></tbody></table>
<h3>ใช้ทำอะไรได้</h3><div class="uses">${d.uses.map(u=>`<div>${u}</div>`).join("")}</div>`,1)}
${sec("sim","bg-beiya stitch","ตัวจำลอง 3D","ลองดูชิ้นนี้ในสีหนังอื่น",sim()+'<p class="cap">ภาพจำลองจากไฟล์บล็อกตัดขนาดจริง หน้าที่วาดเป็นไอเดียแต่งเองที่บูธ สินค้าที่ส่งเป็นชิ้นเรียบ</p>',2)}
${sec("howto","bg-beana p-dots","สั่งยังไง","สั่ง จ่าย รับของ",`<div class="steps"><div>กดสั่งทาง LINE ข้อความสั่งถูกคัดลอกไว้ให้แล้ว</div><div>ร้านส่งรูปชิ้นจริงให้เลือก แล้วโอนพร้อมเพย์</div><div>ส่งไปรษณีย์${boothOn()?" หรือรับที่บูธ":""}</div></div>
<ul class="ticks"><li>ค่าส่งแจ้งในแชท ตามจำนวนชิ้น</li>${boothOn()?`<li>รับที่บูธ: ${esc(BOOTH.fair)} ${esc(BOOTH.dates)} ${esc(BOOTH.hours)}</li>`:""}<li>สั่งจำนวนมากหรือของที่ระลึกองค์กร <a href="/#corp">ดูบริการองค์กร</a></li></ul>`,3)}
${sec("more","bg-bene p-stamp","ชิ้นอื่น","ดูต่ออีก "+(PROD.length-1)+" ชิ้น",`<div class="more">${others}</div>`,4)}
${foot()}
<div class="buybar" role="region" aria-label="สั่งซื้อ"><div class="in">${p.out?`<div class="tot"><b>ของหมด</b><small>${esc(p.name)}</small></div>
<a class="btn" href="${LINK.line}" target="_blank" rel="noopener" data-order="1">ถามรอบหน้า</a>`:`<div class="tot"><b id="tot">${p.price*P.qty}.-</b><small id="totd">${esc(p.name)} × ${P.qty}</small></div>
<a class="btn" href="${LINK.line}" target="_blank" rel="noopener" data-order="1">สั่งทาง LINE</a>`}</div></div>`;
}
function orderText(){ const p=PROD.find(x=>x.id===P.id); if(p.out) return `สอบถาม ${p.id} ${p.name} ที่หมดอยู่ รอบหน้ามีเมื่อไรครับ`; return `สนใจ ${p.id} ${p.name} × ${P.qty} ${p.kind==="set"?"ชุด":"ชิ้น"} · ${TONES[P.tone]} · รวม ${p.price*P.qty} บาท`; }
function updTotal(){ const p=PROD.find(x=>x.id===P.id); if(!p) return; $("#qty").textContent=P.qty; $("#tot").textContent=(p.price*P.qty)+".-"; $("#totd").textContent=`${p.name} × ${P.qty}`; }
// on a product page the piece opens plain, the way it ships; faces stay one tap away as a DIY idea
function simSet(code){ S.face="none"; simEl.querySelectorAll("[data-face]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.face==="none"))); S.code=code; simEl.querySelectorAll("[data-code]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.code===code))); if(S.three) buildMesh(); else if(S.three===false) flat(); simText(); }

/* ---------- 3D simulator with painted faces ---------- */
const S = {code:"01", leather:2, face:"smile", ink:0, three:null};
const simEl = document.createElement("div"); simEl.className="sim"; simEl.id="simbox";
simEl.innerHTML = `<div class="sim-stage" id="stage"><canvas id="simc" aria-label="ชิ้นหนังจำลอง 3D"></canvas><div id="flat" hidden></div><span class="hint">ลากเพื่อหมุน</span></div>
<div class="sim-ui"><span class="lbl">แพตเทิร์น</span><div class="pchips">${CODES.map(c=>`<button type="button" data-code="${c}" aria-pressed="${c===S.code}" aria-label="แพตเทิร์น ${c} ${SH[c].name}">${sil(c,"#B07A4A",{slit:"rgba(0,0,0,.35)"})}<span>${c}</span></button>`).join("")}</div>
<span class="lbl">สีหนัง · <span id="lname"></span></span><div class="swatches">${LEATHER.map((l,i)=>`<button type="button" data-i="${i}" aria-pressed="${i===S.leather}" aria-label="หนัง${l[0]}" style="background:${l[1]}"></button>`).join("")}</div>
<span class="lbl">วาดหน้า</span><div class="fchips">${FACES.map(f=>`<button type="button" data-face="${f[0]}" aria-pressed="${f[0]===S.face}" aria-label="${f[1]}"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="#B07A4A"/>${faceG(f[0],"#FBF7EE","#D9765F",false)}</svg><span>${f[1]}</span></button>`).join("")}</div>
<span class="lbl">สีที่ใช้วาด · <span id="iname"></span></span><div class="swatches ink">${INK.map((c,i)=>`<button type="button" data-ink="${i}" aria-pressed="${i===S.ink}" aria-label="สี${c[0]}" style="background:${c[1]}"></button>`).join("")}</div>
<p class="sim-info" id="info"></p>
<div class="row"><a class="btn solid" id="simbuy" href="${LINK.line}" target="_blank" rel="noopener" data-copy="">สั่งแบบนี้ทาง LINE</a></div>
<p class="cap">สีจริงแต่ละชิ้นต่างกันเล็กน้อย เพราะเป็นเศษหนังจริง · รูปทรงและรอยร่องจากไฟล์บล็อกตัดขนาดจริง · หนา 1.0–1.2 มม. ขอบไม่ทาสี · หน้าที่วาดเป็นไอเดียแต่งเอง</p></div>`;
function simText(){
  const s=SH[S.code], l=LEATHER[S.leather], cm=(Math.max(s.w,s.h)/10).toFixed(1), fn=FACES.find(f=>f[0]===S.face)[1];
  $("#lname",simEl).textContent=l[0]; $("#iname",simEl).textContent=INK[S.ink][0];
  $("#info",simEl).textContent=`${S.code} ${s.name} · หนัง${l[0]} · ${S.face==="none"?"ไม่วาดหน้า":"หน้า"+fn+" สี"+INK[S.ink][0]} · ${cm} ซม.`;
  $("#simbuy",simEl).dataset.copy=`สนใจแพตเทิร์น ${S.code} ${s.name} หนังสี${l[0]}${S.face==="none"?"":" วาดหน้า"+fn+" สี"+INK[S.ink][0]}`;
  document.querySelectorAll("[data-pick]").forEach(e=>e.textContent=`แบบที่เลือกไว้: ${S.code} ${s.name} · หนัง${l[0]}${S.face==="none"?"":" · หน้า"+fn}`);
}
function noiseTex(){
  const c=document.createElement("canvas"); c.width=c.height=256; const g=c.getContext("2d"), d=g.createImageData(256,256);
  for(let i=0;i<d.data.length;i+=4){ const v=128+(Math.random()-.5)*90; d.data[i]=d.data[i+1]=d.data[i+2]=v; d.data[i+3]=255; }
  g.putImageData(d,0,0);
  const t=new THREE.CanvasTexture(c); t.wrapS=t.wrapT=THREE.RepeatWrapping; t.repeat.set(1/45,1/45); return t;
}
function mottleTex(){
  const c=document.createElement("canvas"); c.width=c.height=512; const g=c.getContext("2d");
  g.fillStyle="#fff"; g.fillRect(0,0,512,512);
  for(let k=0;k<260;k++){ const x=Math.random()*512,y=Math.random()*512,r=10+Math.random()*60, v=200+Math.random()*55|0;
    const gr=g.createRadialGradient(x,y,0,x,y,r); gr.addColorStop(0,`rgba(${v},${v},${v},.35)`); gr.addColorStop(1,"rgba(255,255,255,0)"); g.fillStyle=gr; g.fillRect(x-r,y-r,2*r,2*r); }
  const d=g.getImageData(0,0,512,512); for(let i=0;i<d.data.length;i+=4){ const n=(Math.random()-.5)*26; d.data[i]+=n; d.data[i+1]+=n; d.data[i+2]+=n; } g.putImageData(d,0,0);
  const t=new THREE.CanvasTexture(c); t.encoding=THREE.sRGBEncoding; t.wrapS=t.wrapT=THREE.RepeatWrapping; t.repeat.set(1/70,1/70); return t;
}
// the face is painted on a thin transparent decal that sits on the grain side
function faceDecal(){
  const T=S.three; if(!T||!T.mesh) return;
  if(T.decal){ T.mesh.remove(T.decal); T.decal.geometry.dispose(); T.decal.material.map&&T.decal.material.map.dispose(); T.decal.material.dispose(); T.decal=null; }
  if(S.face==="none") return;
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="512" height="512"><defs><filter id="paint"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="2.6"/></filter></defs>${faceG(S.face,INK[S.ink][1])}</svg>`;
  const img=new Image(), want=S.face+S.ink+S.code;
  img.onload=()=>{ if(S.face+S.ink+S.code!==want||!S.three.mesh) return;
    const c=document.createElement("canvas"); c.width=c.height=512; c.getContext("2d").drawImage(img,0,0,512,512);
    const tex=new THREE.CanvasTexture(c); tex.encoding=THREE.sRGBEncoding;
    const s=SH[S.code], a=ANCHOR_MM[S.code];
    const m=new THREE.Mesh(new THREE.PlaneGeometry(a[2],a[2]),new THREE.MeshStandardMaterial({map:tex,transparent:true,roughness:.55,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-2}));
    m.position.set(a[0]-s.w/2, s.h/2-a[1], .82); if(T.decal) T.mesh.remove(T.decal); T.decal=m; T.mesh.add(m); };
  img.src="data:image/svg+xml;charset=utf-8,"+encodeURIComponent(svg);
}
function buildMesh(){
  const T=S.three, s=SH[S.code], cx=s.w/2, cy=s.h/2;
  if(T.mesh){ T.group.remove(T.mesh); T.mesh.traverse(o=>{ if(o.geometry) o.geometry.dispose(); }); T.decal=null; }
  const shp=new THREE.Shape(s.outline.map(p=>new THREE.Vector2(p[0]-cx, cy-p[1])));
  s.holes.forEach(h=>shp.holes.push(new THREE.Path(h.map(p=>new THREE.Vector2(p[0]-cx, cy-p[1])))));
  const depth=1.2, g=new THREE.ExtrudeGeometry(shp,{depth,bevelEnabled:true,bevelThickness:.18,bevelSize:.18,bevelSegments:2,curveSegments:6});
  g.translate(0,0,-depth/2);
  const m=new THREE.Mesh(g,[T.top,T.edge]);
  const slitMat=new THREE.MeshBasicMaterial({color:0x1a1513});
  s.slits.forEach(l=>{ const x1=l[0]-cx,y1=cy-l[1],x2=l[2]-cx,y2=cy-l[3], len=Math.hypot(x2-x1,y2-y1);
    const b=new THREE.Mesh(new THREE.BoxGeometry(len,.55,depth+.5),slitMat); b.position.set((x1+x2)/2,(y1+y2)/2,0); b.rotation.z=Math.atan2(y2-y1,x2-x1); m.add(b); });
  T.mesh=m; T.group.add(m); setColor(); faceDecal();
}
function setColor(){ const T=S.three; if(!T) return; const c=new THREE.Color(LEATHER[S.leather][1]).convertSRGBToLinear();
  T.top.color.copy(c); T.edge.color.copy(c.clone().lerp(new THREE.Color("#D8C2A2").convertSRGBToLinear(),.4)); }
function flat(){ const f=$("#flat",simEl); f.hidden=false; f.innerHTML=sil(S.code,LEATHER[S.leather][1],{slit:"rgba(0,0,0,.5)",face:S.face==="none"?null:[S.face,INK[S.ink][1]]}); $("#simc",simEl).hidden=true; }
function initThree(){
  if(S.three!==null) return;
  if(!window.THREE){ S.three=false; flat(); return; }
  const cv=$("#simc",simEl); let r;
  try{ r=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true}); }catch(_){ S.three=false; flat(); return; }
  r.setPixelRatio(Math.min(2,devicePixelRatio)); r.outputEncoding=THREE.sRGBEncoding;
  const scene=new THREE.Scene(), cam=new THREE.PerspectiveCamera(32,1,1,2000); cam.position.set(0,-120,190); cam.lookAt(0,0,0);
  scene.add(new THREE.HemisphereLight(0xfff3e2,0x5a4c40,.6));
  const dl=new THREE.DirectionalLight(0xffffff,.75); dl.position.set(-90,-40,150); scene.add(dl);
  const rim=new THREE.DirectionalLight(0xffe2c4,.45); rim.position.set(120,140,40); scene.add(rim);
  const top=new THREE.MeshStandardMaterial({roughness:.72,metalness:0,map:mottleTex(),bumpMap:noiseTex(),bumpScale:.55});
  const edge=new THREE.MeshStandardMaterial({roughness:.95,metalness:0});
  const group=new THREE.Group(); scene.add(group);
  S.three={r,scene,cam,group,top,edge,mesh:null,decal:null,rx:-.5,ry:.25,drag:null,visible:false};
  buildMesh();
  const stage=$("#stage",simEl);
  const size=()=>{ const w=stage.clientWidth||300; r.setSize(w,w,false); };
  size(); new ResizeObserver(size).observe(stage);
  stage.addEventListener("pointerdown",e=>{ S.three.drag={x:e.clientX,y:e.clientY,rx:S.three.rx,ry:S.three.ry}; stage.setPointerCapture(e.pointerId); stage.style.cursor="grabbing"; });
  stage.addEventListener("pointermove",e=>{ const d=S.three.drag; if(!d) return; S.three.ry=d.ry+(e.clientX-d.x)*.01; S.three.rx=Math.max(-1.4,Math.min(1.2,d.rx+(e.clientY-d.y)*.01)); });
  const up=()=>{ S.three.drag=null; stage.style.cursor=""; }; stage.addEventListener("pointerup",up); stage.addEventListener("pointercancel",up);
  new IntersectionObserver(es=>{ S.three.visible=es[0].isIntersecting; }).observe(stage);
  const still=matchMedia("(prefers-reduced-motion: reduce)").matches;
  // turntable sway rather than a full spin, so the painted face keeps facing the viewer most of the time
  let t0=performance.now();
  (function loop(now){ requestAnimationFrame(loop); const T=S.three; if(!T.visible) return;
    const sway=(!T.drag&&!still)?Math.sin((now-t0)/1600)*.55:0;
    T.group.rotation.set(T.rx,0,0); T.mesh.rotation.set(0,0,T.ry+sway); T.r.render(T.scene,T.cam); })(t0);
}
simEl.addEventListener("click",e=>{
  const upd=fn=>{ fn(); simText(); };
  const p=e.target.closest("[data-code]"); if(p) return upd(()=>{ S.code=p.dataset.code; simEl.querySelectorAll("[data-code]").forEach(b=>b.setAttribute("aria-pressed",String(b===p))); S.three?buildMesh():S.three===false&&flat(); });
  const w=e.target.closest("[data-i]"); if(w) return upd(()=>{ S.leather=+w.dataset.i; simEl.querySelectorAll("[data-i]").forEach(b=>b.setAttribute("aria-pressed",String(b===w))); S.three?setColor():S.three===false&&flat(); });
  const f=e.target.closest("[data-face]"); if(f) return upd(()=>{ S.face=f.dataset.face; simEl.querySelectorAll("[data-face]").forEach(b=>b.setAttribute("aria-pressed",String(b===f))); S.three?faceDecal():S.three===false&&flat(); });
  const k=e.target.closest("[data-ink]"); if(k) return upd(()=>{ S.ink=+k.dataset.ink; simEl.querySelectorAll("[data-ink]").forEach(b=>b.setAttribute("aria-pressed",String(b===k))); S.three?faceDecal():S.three===false&&flat(); });
});

/* ---------- page wiring ---------- */
function parallax(){
  const vh=innerHeight;
  document.querySelectorAll("#view [data-depth]").forEach(el=>{ const host=el.parentElement, r=host.getBoundingClientRect(); if(r.bottom<-200||r.top>vh+200) return;
    const off=(r.top+r.height/2-vh/2)*-(+el.dataset.depth); el.style.transform=`translate3d(0,${off.toFixed(1)}px,0) rotate(${el.dataset.rot||0}deg)`; });
}
let ticking=false; addEventListener("scroll",()=>{ if(!ticking){ ticking=true; requestAnimationFrame(()=>{ parallax(); ticking=false; }); } },{passive:true});
const still=matchMedia("(prefers-reduced-motion: reduce)").matches;
// orders, quotes and bookings go to the shop's LINE chat as a ready-made message
function copyThen(text, msg){ try{ navigator.clipboard.writeText(text).then(()=>toast(msg),()=>toast("เปิด LINE แล้วพิมพ์บอกเราได้เลย")); }catch(_){ toast("เปิด LINE แล้วพิมพ์บอกเราได้เลย"); } }
document.addEventListener("click",e=>{
  const od=e.target.closest("[data-order]"); if(od){ copyThen(orderText(),"คัดลอกข้อความแล้ว วางในแชท LINE ได้เลย"); return; }
  const cp=e.target.closest("[data-corp]"); if(cp){ const org=(($("#org")||{}).value||"").trim();
    copyThen(`สนใจของที่ระลึกองค์กร${org&&org!=="บริษัทของคุณ"?" · "+org:""} · แพตเทิร์น ${S.code} หนัง${LEATHER[S.leather][0]}`,"คัดลอกข้อความแล้ว วางในแชท LINE ได้เลย"); return; }
  const c=e.target.closest("[data-copy]"); if(c&&c.dataset.copy){ copyThen(c.dataset.copy,"คัดลอกข้อความแล้ว วางในแชท LINE ได้เลย"); }
  const q=e.target.closest("[data-q]"); if(q){ P.qty=Math.max(1,Math.min(50,P.qty+ +q.dataset.q)); updTotal(); return; }
  const tn=e.target.closest("[data-tone] button"); if(tn){ P.tone=+tn.dataset.t; tn.parentElement.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===tn))); return; }
  const th=e.target.closest("[data-slide]"); if(th){ const g=$("#gal"); g.scrollTo({left:g.clientWidth*+th.dataset.slide,behavior:still?"auto":"smooth"}); return; }
  const f=e.target.closest(".faces button"); if(f){ document.querySelectorAll(".faces button.on").forEach(b=>b.classList.remove("on")); f.classList.add("on"); const l=$("#faceLab"); if(l) l.textContent=f.dataset.lab+" · ชิ้นนี้มีชิ้นเดียว"; }
  const o=e.target.closest("[data-one] button"); if(o){ o.parentElement.querySelectorAll("button").forEach(b=>b.setAttribute("aria-pressed",String(b===o))); }
  const st=e.target.closest("[data-st]"); if(st){ const out=st.parentElement.querySelector("output"); out.textContent=Math.max(2,Math.min(60,+out.textContent+ +st.dataset.st)); }
});
document.addEventListener("input",e=>{ if(e.target.id==="org") document.querySelectorAll("[data-org]").forEach(b=>b.textContent=e.target.value.trim()||"บริษัทของคุณ"); });
document.addEventListener("submit",e=>{ if(!e.target.matches("[data-book]")) return; e.preventDefault();
  const f=e.target, kind=(f.querySelector('[data-one] [aria-pressed="true"]')||{}).textContent||"", n=f.querySelector("output").textContent,
        d=f.querySelector("#wdate").value, who=f.querySelector("#wname").value.trim();
  copyThen(`ขอจองเวิร์กช็อป · ${kind} · ${n} คน${d?" · วันที่ "+d:""}${who?" · ติดต่อ "+who:""}`,"คัดลอกคำขอแล้ว วางในแชท LINE ได้เลย");
  window.open(LINK.line,"_blank","noopener"); });

// gallery thumbnails follow the swipe
document.addEventListener("scroll",e=>{ if(e.target.id!=="gal") return; const g=e.target, k=Math.round(g.scrollLeft/g.clientWidth);
  document.querySelectorAll("[data-slide]").forEach(b=>b.setAttribute("aria-pressed",String(+b.dataset.slide===k))); },true);
// three.js (r128, MIT) is 600 KB: fetch it only when the simulator comes near the screen
function loadThree(){ return window.THREE?Promise.resolve():new Promise(r=>{ const sc=document.createElement("script"); sc.src="/assets/js/three.min.js"; sc.onload=r; sc.onerror=r; document.head.appendChild(sc); }); }
function init(){
  const v=$("#view"); v.className="d2";
  if(PAGE.type==="product"){ P.id=PAGE.id; document.body.classList.add("ppv"); v.innerHTML=productPage(PAGE.id); }
  else v.innerHTML=home();
  if(!boothOn()) document.querySelectorAll("#view .booth").forEach(b=>b.closest(".sec").remove());
  // earlier bands sit above later ones
  const bands=[...document.querySelectorAll("#view .sec")]; bands.forEach((b,i)=>b.style.zIndex=bands.length-i);
  $(".sim-slot").appendChild(simEl);
  if(PAGE.type==="product") simSet(PD[PAGE.id].code); else simText();
  if(!still) parallax(); else document.querySelectorAll("#view [data-depth]").forEach(el=>el.style.transform=`rotate(${el.dataset.rot||0}deg)`);
  new IntersectionObserver((es,o)=>{ if(es[0].isIntersecting){ o.disconnect(); loadThree().then(initThree); } },{rootMargin:"400px"}).observe(simEl);
  // land on /#section, and again once photos above it have loaded and moved it
  const toHash=()=>{ if(!location.hash) return; const t=document.getElementById(location.hash.slice(1)); if(t) t.scrollIntoView(); };
  requestAnimationFrame(toHash); addEventListener("load",toHash,{once:true});
}
init();
