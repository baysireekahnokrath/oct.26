// ------------------------------------------------------------ 3D crossing ideas (tab "ไขว้ 3D")
// X3D comes from cross3d/catalogue.py: die outlines (mm) and 50 checked assemblies with each piece's rotation R and position t.
const X3D = __X3D__;
const X3D_COLORS = ["#B8743A", "#2449D8", "#FF5A36", "#2EC4A0", "#FFC23C", "#FF8AC4", "#8A5A2B", "#1C1B22"];
let THREEP = null, xFilter = "all", xRenderer = null;

function loadThree() {
  if (!THREEP) THREEP = new Promise((ok, bad) => {
    if (window.THREE) return ok(window.THREE);
    const s = document.createElement("script");
    s.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
    s.onload = () => ok(window.THREE); s.onerror = () => { THREEP = null; bad(new Error("three")); };
    document.head.append(s);
  });
  return THREEP;
}

function x3dGroup(T, item) {
  const g = new T.Group();
  const geos = {};
  const centre = new T.Vector3(...item.centre);
  item.place.forEach((p, j) => {
    if (!geos[p.c]) {
      const sh = new T.Shape(X3D.geo[p.c].poly.map(q => new T.Vector2(q[0], q[1])));
      const geo = new T.ExtrudeGeometry(sh, {depth: 2, bevelEnabled: false}); geo.translate(0, 0, -1);
      geos[p.c] = geo;
    }
    const mesh = new T.Mesh(geos[p.c], new T.MeshStandardMaterial({color: X3D_COLORS[j % X3D_COLORS.length], roughness: .85, metalness: 0}));
    const R = p.R, t = p.t, M = new T.Matrix4();
    M.set(R[0], R[1], R[2], t[0], R[3], R[4], R[5], t[1], R[6], R[7], R[8], t[2], 0, 0, 0, 1);
    const piece = new T.Group(); piece.add(mesh);
    const cutMat = new T.LineBasicMaterial({color: 0x1C1B22});
    for (const [a, b] of X3D.geo[p.c].cuts) for (const z of [1.15, -1.15])
      piece.add(new T.Line(new T.BufferGeometry().setFromPoints([new T.Vector3(a[0], a[1], z), new T.Vector3(b[0], b[1], z)]), cutMat));
    piece.applyMatrix4(M);
    piece.userData.home = piece.position.clone(); piece.userData.dir = new T.Vector3(t[0], t[1], t[2]).sub(centre);
    if (piece.userData.dir.length() < 1) piece.userData.dir.set(R[2], R[5], R[8]);
    piece.userData.dir.normalize();
    g.add(piece);
  });
  return g;
}

function x3dScene(T, group, item) {
  const scene = new T.Scene();
  scene.add(new T.HemisphereLight(0xffffff, 0x8a6a50, 0.95));
  const dl = new T.DirectionalLight(0xffffff, 0.55); dl.position.set(90, -140, 200); scene.add(dl);
  const floor = new T.Mesh(new T.CircleGeometry(item.radius * 1.6, 48), new T.MeshBasicMaterial({color: 0x000000, transparent: true, opacity: .06}));
  floor.position.set(item.centre[0], item.centre[1], -0.5); scene.add(floor);
  scene.add(group);
  return scene;
}
function x3dCamera(T, item, aspect, yaw = -0.75, pitch = 0.5, zoom = 1) {
  const cam = new T.PerspectiveCamera(30, aspect, 1, 5000);
  const d = item.radius * 3.4 * zoom, c = item.centre;
  cam.up.set(0, 0, 1);
  cam.position.set(c[0] + d * Math.cos(pitch) * Math.cos(yaw), c[1] + d * Math.cos(pitch) * Math.sin(yaw), c[2] + d * Math.sin(pitch));
  cam.lookAt(c[0], c[1], c[2]);
  return cam;
}

async function x3dThumbs() {
  let T;
  try { T = await loadThree(); } catch { $("#x-status").textContent = "โหลดภาพ 3D ไม่ได้ ตรวจอินเทอร์เน็ตแล้วเปิดแท็บนี้อีกครั้ง"; return; }
  $("#x-status").textContent = "";
  if (!xRenderer) {
    xRenderer = new T.WebGLRenderer({antialias: true, preserveDrawingBuffer: true, alpha: true});
    xRenderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1)); xRenderer.setSize(220, 220);
  }
  const todo = [...document.querySelectorAll("img.x-thumb:not([data-done])")];
  const step = () => {
    const img = todo.shift(); if (!img) return;
    const item = X3D.items.find(i => i.id === img.dataset.id);
    const scene = x3dScene(T, x3dGroup(T, item), item);
    xRenderer.render(scene, x3dCamera(T, item, 1));
    img.src = xRenderer.domElement.toDataURL("image/png"); img.dataset.done = "1";
    requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

function x3dCards() {
  const kinds = [...new Set(X3D.items.map(i => i.group))];
  const chip = (key, label, n) => el("button", {class: "chip", type: "button", "aria-pressed": String(xFilter === key), onclick: () => { xFilter = key; x3dCards(); }}, `${label} ${n}`);
  $("#x-filters").replaceChildren(chip("all", "ทั้งหมด", X3D.items.length), ...kinds.map(k => chip(k, k, X3D.items.filter(i => i.group === k).length)));
  const shown = X3D.items.filter(i => xFilter === "all" || i.group === xFilter);
  $("#x-cards").replaceChildren(...shown.map(i => el("button", {class: "xcard", type: "button", onclick: () => x3dOpen(i.id)},
    el("img", {class: "x-thumb", "data-id": i.id, alt: "", width: "220", height: "220", src: "data:image/gif;base64,R0lGODlhAQABAAAAACw="}),
    el("div", {},
      el("span", {class: "eyebrow", text: `${i.id} · ${i.group}`}),
      el("span", {class: "name", text: i.name}),
      el("span", {class: "meta num", text: `${i.pieces.length} ชิ้น · ล็อก ${i.locks} จุด · ${i.dims}`}),
      el("span", {class: "meta num", text: `${i.price} บาท · กำไร ${Math.round(i.margin * 100)}%`}),
      i.real === "fail" ? el("span", {class: "blk", text: "ลองจริงแล้วหลุด · พักไว้"}) : null,
      i.no06 ? el("span", {class: "blk", text: "ใช้ 06 ที่ยังไม่ได้ตัด · ห้ามใช้ตอนนี้"}) : null))));
  x3dThumbs();
}

function x3dOpen(id) {
  const i = X3D.items.find(x => x.id === id); if (!i) return;
  const canvas = el("canvas", {class: "x-canvas", "aria-label": `ภาพ 3D ${i.name} ลากเพื่อหมุน`});
  const slider = el("input", {id: "x-explode", type: "range", min: "0", max: "100", value: "0"});
  const msg = el("span");
  const send = el("button", {class: "btn primary", type: "button", disabled: !canWrite, text: "ส่งเข้าบอร์ดเป็นไอเดีย"});
  send.addEventListener("click", async () => {
    send.disabled = true; msg.className = ""; msg.textContent = "กำลังส่ง…";
    const parts = Object.entries(i.pieces.reduce((a, c) => (a[c] = (a[c] || 0) + 1, a), {}));
    try {
      await db.collection("items").doc("x-" + i.id).set({kind: "idea", name: `${i.name} (${i.id})`, who: i.who, price: i.price, parts,
        joints: i.locks, extra: 0, pack: i.pack, stage: "idea", blocker: "", note: `ไขว้ 3D ${i.id}: ${i.dims}, ล็อก ${i.locks} จุด`, x3d: i.id, updated: new Date().toISOString()});
      msg.className = "saved"; msg.textContent = "อยู่ในบอร์ดแล้ว ขั้นไอเดีย";
    } catch { msg.className = "err"; msg.textContent = "ส่งไม่ได้ ลองใหม่อีกครั้ง หรือขอสิทธิ์แก้ไขจากเจ้าของหน้า"; send.disabled = !canWrite; }
  });
  if (i.no06) { send.disabled = true; msg.className = "err"; msg.textContent = "ส่งเข้าบอร์ดไม่ได้ เพราะใช้ 06"; }
  const inBoard = !!over["x-" + i.id];
  if (inBoard) { send.disabled = true; msg.className = "saved"; msg.textContent = "อยู่ในบอร์ดแล้ว"; }
  $("#dlg-body").replaceChildren(
    el("div", {class: "dlg-head x-head"},
      el("div", {}, el("p", {class: "eyebrow", text: `${i.id} · ${i.group}`}), el("h3", {id: "d-name", text: i.name}), el("p", {class: "small muted", text: i.use})),
      el("button", {class: "x", type: "button", "aria-label": "ปิด", onclick: () => $("#dlg").close(), text: "×"})),
    el("div", {class: "x-stage"}, canvas, el("p", {class: "small muted x-hint", id: "x-hint", text: "กำลังโหลดภาพ 3D…"})),
    el("label", {for: "x-explode"}, "แยกชิ้นดูวิธีประกอบ", slider),
    el("dl", {class: "spec num"},
      el("dt", {text: "ชิ้นส่วน"}), el("dd", {text: i.piecesTxt}),
      el("dt", {text: "ล็อก"}), el("dd", {text: `${i.locks} จุด (${i.locksTxt})`}),
      el("dt", {text: "ขนาดเมื่อต่อเสร็จ"}), el("dd", {text: i.dims}),
      el("dt", {text: "ขายแบบ"}), el("dd", {text: i.sell}),
      el("dt", {text: "ราคา / ต้นทุน"}), el("dd", {text: `${i.price} / ${i.cost.toFixed(2)} บาท · กำไรขั้นต้น ${Math.round(i.margin * 100)}%`}),
      el("dt", {text: "คนซื้อ"}), el("dd", {text: i.who}),
      el("dt", {text: "ผลตรวจ"}), el("dd", {class: "x-pass", text: "รูปทรงผ่าน: ปีกพอดีร่อง ร่องไม่ใช้ซ้ำ ชิ้นไม่ทะลุกัน วงปิดตรง"}),
      i.real === "fail" ? el("dt", {text: "ลองกับหนังจริง"}) : null,
      i.real === "fail" ? el("dd", {class: "err", text: "หลุด: ร่องของ 02 จับหนังด้วยกันไม่อยู่ พักไว้จนกว่าจะลองบล็อก 02 รุ่น B"}) : null,
      i.no06 ? el("dt", {text: "ใช้ได้ไหม"}) : null, i.no06 ? el("dd", {class: "err", text: D.no06}) : null),
    el("div", {}, el("p", {class: "small muted", text: "วิธีต่อ"}), el("ol", {class: "steps"}, ...i.steps.map(s => el("li", {text: s})))),
    el("div", {class: "row"}, send, msg),
    (openThread = commentsBlock(i.id, "ความเห็นต่อแบบนี้ ลองแล้วเป็นอย่างไร")));
  if (!$("#dlg").open) $("#dlg").showModal();
  x3dViewer(canvas, slider, i);
}

async function x3dViewer(canvas, slider, item) {
  let T;
  try { T = await loadThree(); } catch { $("#x-hint").textContent = "โหลดภาพ 3D ไม่ได้"; return; }
  $("#x-hint").textContent = "ลากเพื่อหมุน · หมุนล้อหรือบีบนิ้วเพื่อซูม";
  const rect = canvas.getBoundingClientRect(); const W = Math.max(260, rect.width), H = Math.max(240, rect.height);
  const r = new T.WebGLRenderer({canvas, antialias: true, alpha: true});
  r.setPixelRatio(Math.min(2, window.devicePixelRatio || 1)); r.setSize(W, H, false);
  const group = x3dGroup(T, item); const scene = x3dScene(T, group, item);
  let yaw = -0.75, pitch = 0.5, zoom = 1, spin = !matchMedia("(prefers-reduced-motion: reduce)").matches, alive = true;
  const pts = new Map(); let pinch = 0;
  canvas.addEventListener("pointerdown", e => { canvas.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]); spin = false; });
  canvas.addEventListener("pointermove", e => {
    if (!pts.has(e.pointerId)) return;
    const [x0, y0] = pts.get(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]);
    if (pts.size === 1) { yaw -= (e.clientX - x0) * 0.01; pitch = Math.max(-0.2, Math.min(1.45, pitch + (e.clientY - y0) * 0.01)); }
    else { const [a, b] = [...pts.values()]; const d = Math.hypot(a[0] - b[0], a[1] - b[1]); if (pinch) zoom = Math.max(.45, Math.min(2.2, zoom * pinch / d)); pinch = d; }
  });
  const up = e => { pts.delete(e.pointerId); if (pts.size < 2) pinch = 0; };
  canvas.addEventListener("pointerup", up); canvas.addEventListener("pointercancel", up);
  canvas.addEventListener("wheel", e => { e.preventDefault(); zoom = Math.max(.45, Math.min(2.2, zoom * (e.deltaY > 0 ? 1.08 : 0.93))); }, {passive: false});
  slider.addEventListener("input", () => {
    const k = slider.value / 100;
    group.children.forEach(p => p.position.copy(p.userData.home).addScaledVector(p.userData.dir, k * item.radius * 0.9));
  });
  $("#dlg").addEventListener("close", () => { alive = false; r.dispose(); }, {once: true});
  const frame = () => {
    if (!alive) return;
    if (spin) yaw += 0.004;
    r.render(scene, x3dCamera(T, item, W / H, yaw, pitch, zoom));
    requestAnimationFrame(frame);
  };
  frame();
}
