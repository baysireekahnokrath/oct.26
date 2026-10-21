// ------------------------------------------------------------ tab "ชิ้นเดียว 50": single-piece ideas (data from ../single50/build.py)
// Each drawing is the real die outline with what the piece holds drawn over it: a stick, ribbon, straw, card,
// elastic or pin through the two slits, a rim in an open slot, or an object on top.
const S50 = __S50__;
let sFilter = "all";

function s50Svg(item, big = false) {
  const code = item.pieces[0][0], g = S50.geo[code];
  const [vx, vy, vw, vh] = g.vb.split(" ").map(Number), pad = 22;
  const svg = document.createElementNS(SVGNS, "svg");
  svg.setAttribute("viewBox", `${vx - pad} ${vy - pad} ${vw + 2 * pad} ${vh + 2 * pad}`);
  svg.setAttribute("class", big ? "s50 big" : "s50"); svg.setAttribute("aria-hidden", "true");
  const add = (tag, attrs) => { const n = document.createElementNS(SVGNS, tag); for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v); svg.append(n); return n; };
  const piece = (dx = 0, dy = 0, s = 1) => {
    const grp = add("g", {transform: `translate(${dx} ${dy}) scale(${s})`});
    const p = document.createElementNS(SVGNS, "path"); p.setAttribute("d", g.d); p.setAttribute("class", "hide"); grp.append(p);
    for (const [x1, y1, x2, y2] of [...g.slits, ...g.slots]) {
      const l = document.createElementNS(SVGNS, "line"); Object.entries({x1, y1, x2, y2}).forEach(([k, v]) => l.setAttribute(k, v)); l.setAttribute("class", "cut"); grp.append(l);
    }
    return grp;
  };
  const cx = vx + vw / 2, cy = vy + vh / 2;
  if (item.mech === "set" && item.pieces.reduce((a, [, q]) => a + q, 0) > 1) {
    const codes = item.pieces.flatMap(([c, q]) => Array(Math.min(q, 3)).fill(c)).slice(0, 4);
    codes.forEach((c, k) => {
      const gg = S50.geo[c], [, , w, h] = gg.vb.split(" ").map(Number);
      const grp = add("g", {transform: `translate(${vx + (k % 2) * vw / 2 + 4} ${vy + Math.floor(k / 2) * vh / 2 + 4}) scale(${0.44 * Math.min(vw / w, vh / h)})`});
      const p = document.createElementNS(SVGNS, "path"); p.setAttribute("d", gg.d); p.setAttribute("class", "hide"); grp.append(p);
    });
    const n = item.pieces.reduce((a, [, q]) => a + q, 0);
    add("text", {x: vx + vw, y: vy + vh + 14, class: "s50txt end"}).textContent = `× ${n}`;
    return svg;
  }
  piece();
  const mid = s => [(s[0] + s[2]) / 2, (s[1] + s[3]) / 2];
  const two = g.slits.length >= 2 ? [mid(g.slits[0]), mid(g.slits[1])] : null;
  const len = s => Math.hypot(s[2] - s[0], s[3] - s[1]);
  const slitLen = g.slits.length ? len(g.slits[0]) : 20;
  const through = (cls, w, ext) => {                      // in at slit A, under the bridge, out at slit B
    if (!two) return;
    let [[ax, ay], [bx, by]] = two; const L = Math.hypot(bx - ax, by - ay), ux = (bx - ax) / L, uy = (by - ay) / L;
    add("line", {x1: ax - ux * ext, y1: ay - uy * ext, x2: ax, y2: ay, class: cls, "stroke-width": w});
    add("line", {x1: ax, y1: ay, x2: bx, y2: by, class: cls + " behind", "stroke-width": w});
    add("line", {x1: bx, y1: by, x2: bx + ux * ext, y2: by + uy * ext, class: cls, "stroke-width": w});
  };
  const m = item.mech;
  if (m === "stick") through("stick", 3, 34);
  if (m === "hook") through("stick", 2, 14);
  if (m === "straw") { through("straw", 6, 40); }
  if (m === "ribbon") through("ribbon", Math.min(slitLen - 3, 22), 30);
  if (m === "card") through("card", Math.min(slitLen - 4, 24), 26);
  if (m === "elastic") { through("elastic", 2, 30); }
  if (m === "pin") { through("pin", 1.6, 4); if (two) add("circle", {cx: two[0][0], cy: two[0][1], r: 2.6, class: "pinhead"}); }
  if (m === "twist" && g.slits.length) {
    const s = g.slits[0], [mx, my] = mid(s), L = len(s), nx = -(s[3] - s[1]) / L, ny = (s[2] - s[0]) / L;
    add("path", {d: `M${mx - (s[2] - s[0]) / 3},${my - (s[3] - s[1]) / 3} L${mx + nx * 26 - 10},${my + ny * 26} L${mx + nx * 26 + 10},${my + ny * 26} L${mx + (s[2] - s[0]) / 3},${my + (s[3] - s[1]) / 3} Z`, class: "twist"});
  }
  if (m === "slot" && g.slots.length) {
    const s = g.slots.reduce((a, b) => len(b) > len(a) ? b : a), L = len(s), ux = (s[2] - s[0]) / L, uy = (s[3] - s[1]) / L;
    add("line", {x1: s[0] - ux * 26, y1: s[1] - uy * 26, x2: s[2], y2: s[3], class: "rim", "stroke-width": 3.2});
  }
  if (m === "clips") for (const [x1, y1, x2, y2] of g.slits) add("path", {d: `M${x1},${y1} L${x2},${y2}`, class: "clip"});
  if (m === "object") add("circle", {cx, cy, r: Math.min(vw, vh) * 0.3, class: "obj"});
  if (item.stamp) add("text", {x: cx, y: cy + 4, class: "s50txt"}).textContent = item.stamp;
  return svg;
}

function s50Cards() {
  const groups = [...new Set(S50.items.map(i => i.group))];
  const chip = (key, label, n) => el("button", {class: "chip", type: "button", "aria-pressed": String(sFilter === key), onclick: () => { sFilter = key; s50Cards(); }}, `${label} ${n}`);
  $("#s-filters").replaceChildren(chip("all", "ทั้งหมด", S50.items.length), chip("ready", "ทำได้กับหนังที่มี", S50.items.filter(i => !i.load).length),
    chip("07", "ใช้ 07", S50.items.filter(i => i.uses07).length), ...groups.map(g => chip(g, g, S50.items.filter(i => i.group === g).length)));
  const shown = S50.items.filter(i => sFilter === "all" || (sFilter === "ready" && !i.load) || (sFilter === "07" && i.uses07) || i.group === sFilter);
  $("#s-cards").replaceChildren(...shown.map(i => el("button", {class: "xcard scard", type: "button", onclick: () => s50Open(i.id)},
    el("div", {class: "s50wrap"}, s50Svg(i)),
    el("div", {},
      el("span", {class: "eyebrow", text: `${i.id} · ${i.group}`}),
      el("span", {class: "name", text: i.name}),
      el("span", {class: "meta num", text: `${i.piecesTxt}`}),
      el("span", {class: "meta num", text: `${i.price} บาท · กำไร ${Math.round(i.margin * 100)}%`}),
      i.load ? el("span", {class: "blk", text: "รับแรง รอหนัง 2 มม."}) : null))));
}

function s50Open(id) {
  const i = S50.items.find(x => x.id === id); if (!i) return;
  const msg = el("span");
  const send = el("button", {class: "btn primary", type: "button", disabled: !canWrite, text: "ส่งเข้าบอร์ดเป็นไอเดีย"});
  send.addEventListener("click", async () => {
    send.disabled = true; msg.className = ""; msg.textContent = "กำลังส่ง…";
    try {
      await db.collection("items").doc("s-" + i.id).set({kind: "idea", name: `${i.name} (${i.id})`, who: i.who, price: i.price, parts: i.pieces,
        joints: 0, extra: i.extras.reduce((a, [, t]) => a + t, 0), pack: i.pack, stage: "idea", blocker: i.load ? "รับแรง ต้องใช้หนัง 2 มม." : "",
        note: `${i.how} · ลองแบบนี้: ${i.test}`, s50: i.id, updated: new Date().toISOString()});
      msg.className = "saved"; msg.textContent = "อยู่ในบอร์ดแล้ว ขั้นไอเดีย";
    } catch { msg.className = "err"; msg.textContent = "ส่งไม่ได้ ลองใหม่อีกครั้ง"; send.disabled = !canWrite; }
  });
  if (over["s-" + i.id]) { send.disabled = true; msg.className = "saved"; msg.textContent = "อยู่ในบอร์ดแล้ว"; }
  $("#dlg-body").replaceChildren(
    el("div", {class: "dlg-head x-head"},
      el("div", {}, el("p", {class: "eyebrow", text: `${i.id} · ${i.group}`}), el("h3", {id: "d-name", text: i.name}), el("p", {class: "small muted", text: i.who})),
      el("button", {class: "x", type: "button", "aria-label": "ปิด", onclick: () => $("#dlg").close(), text: "×"})),
    el("div", {class: "s50big"}, s50Svg(i, true)),
    el("p", {text: i.how}),
    el("dl", {class: "spec num"},
      el("dt", {text: "ชิ้นหนัง"}), el("dd", {text: i.piecesTxt}),
      el("dt", {text: "ของเสริม"}), el("dd", {text: i.extras.length ? i.extras.map(([n, t]) => `${n} ${t} บาท`).join(" · ") : "ไม่มี"}),
      el("dt", {text: "ราคา / ต้นทุน"}), el("dd", {text: `${i.price} / ${i.cost.toFixed(2)} บาท · กำไรขั้นต้น ${Math.round(i.margin * 100)}%`}),
      el("dt", {text: "หนัง"}), el("dd", {class: i.load ? "err" : "x-pass", text: i.load ? "ของนี้รับแรงหรือแขวน ตามมติ 16 ต.ค. ต้องใช้หนัง 2 มม. ขึ้นไป หนังที่มี (1.0–1.2) ยังใช้ไม่ได้" : "ไม่รับแรง ใช้หนัง 1.0–1.2 มม. ที่มีได้"}),
      el("dt", {text: "ลองแบบนี้"}), el("dd", {text: i.test})),
    el("div", {class: "row"}, send, msg),
    (openThread = commentsBlock(i.id, "ความเห็นต่อแบบนี้")));
  if (!$("#dlg").open) $("#dlg").showModal();
}
