// ------------------------------------------------------------ tab "ตรวจผ่าน": tick each SKU ผ่าน or ไม่ผ่าน (data from ../assortment/tiers.py)
// The range is in three tiers (owner 22 Oct): bare pieces, a piece plus a real add-on, ready-made sets.
// Old draft numbers that were merged or dropped are listed apart; a real number they already hold is never reused.
// Every SKU has a draft number (0001...). Ticking ผ่าน gives it a real number, digits only like IKEA: 260.001.CC,
// 260001 upward in the order SKUs pass, CC = ISO 7064 mod 97-10 check digits (same rule as ../assortment/skucode.py).
// A real number stays with its SKU for good: ticking ไม่ผ่าน later parks it, ผ่าน again brings the same number back.
// Shared state: reviews/<draft> = {verdict: "pass"|"fail"|"", reason, name, seq, issued, updated}.
const RV = __REVIEW__;
const REAL_START = 260001;
const reviews = {};          // draft -> doc
const issuedHere = new Set(); // drafts this browser gave a real number to, so it fixes its own clashes
let rvFilter = "all";

const realCheck = seq => 98 - (seq * 100) % 97;
const realCode = seq => { const s = String(seq).padStart(6, "0"); return `${s.slice(0, 3)}.${s.slice(3)}.${String(realCheck(seq)).padStart(2, "0")}`; };
const seqOf = r => Number.isInteger(r?.seq) && r.seq >= REAL_START ? r.seq : null;
const verdictOf = d => reviews[d]?.verdict === "pass" || reviews[d]?.verdict === "fail" ? reviews[d].verdict : "";
const nextSeq = () => Math.max(REAL_START - 1, ...Object.values(reviews).map(r => seqOf(r) || 0)) + 1;
const REASONS = ["ไม่สวย", "ราคาไม่คุ้ม", "ทำยากหรือช้า", "ไม่แข็งแรง", "ซ้ำกับตัวอื่น", "ขัดกฎ"];

async function saveReview(d, patch) {
  const cur = reviews[d] || {};
  const doc = {verdict: cur.verdict || "", reason: cur.reason || "", name: cur.name || "", seq: seqOf(cur), issued: cur.issued || "", ...patch,
    updated: new Date().toISOString()};
  if (doc.verdict === "pass" && !doc.seq) {              // first pass: take the next real number
    for (let tries = 0, floor = 0; ; tries++) {
      doc.seq = Math.max(nextSeq(), floor); doc.issued = doc.updated;
      try { await db.collection("reviews").doc(d).set(doc); issuedHere.add(d); break; }
      catch (e) { if (e?.code !== "already_exists" || tries > 5) throw e; floor = doc.seq + 1; }   // taken a moment ago: try the next one
    }
  } else await db.collection("reviews").doc(d).set(doc);
  reviews[d] = doc; renderReview();
}

// Two browsers can pass two SKUs in the same moment and take the same number. The earlier one keeps it;
// the browser that issued the later one takes a fresh number. (On pd.oct26brand.com the server refuses a clash.)
function fixClashes() {
  const by = {};
  for (const [d, r] of Object.entries(reviews)) { const s = seqOf(r); if (s) (by[s] ||= []).push(d); }
  for (const ds of Object.values(by)) {
    if (ds.length < 2) continue;
    ds.sort((a, b) => (reviews[a].issued || "").localeCompare(reviews[b].issued || "") || a.localeCompare(b));
    for (const d of ds.slice(1)) if (issuedHere.has(d) && canWrite) saveReview(d, {seq: null, issued: ""}).catch(() => {});
  }
}

function rvRow(a) {
  const d = a.draft, r = reviews[d] || {}, v = verdictOf(d), seq = seqOf(r);
  const msg = el("span", {class: "small"});
  const fail = (e, t) => { msg.className = "err"; msg.textContent = e?.code === "invalid_argument" ? "ต้องใส่รหัสทีมก่อน" : t; };
  const radios = ["pass", "fail"].map(val => {
    const id = `rv-${d}-${val}`;
    const input = el("input", {type: "radio", name: "rv-" + d, id, value: val, disabled: !canWrite});
    input.checked = v === val;
    input.addEventListener("change", async () => {
      msg.className = "small"; msg.textContent = "กำลังบันทึก…";
      try { await saveReview(d, {verdict: val, name: myName()}); }
      catch (e) { fail(e, "บันทึกไม่ได้ ลองใหม่อีกครั้ง"); input.checked = false; }
    });
    return el("label", {class: "rv-opt rv-" + val, for: id}, input, el("span", {text: val === "pass" ? "ผ่าน" : "ไม่ผ่าน"}));
  });
  const head = el("div", {class: "rv-head"},
    el("div", {class: "rv-thumbs"}, ...a.pieces.slice(0, 4).map(([c]) => thumb(c, "thumb sm"))),
    el("div", {},
      el("p", {class: "eyebrow num"}, el("span", {class: "draftno", text: "ร่าง " + d}), a.old ? ` · รหัสเดิม ${a.old}` : ""),
      el("b", {class: "rv-name", text: a.name}),
      el("p", {class: "small muted num", text: `${a.price} บาท · ทุน ${a.cost.toFixed(2)} · กำไร ${Math.round(a.margin * 100)}%`}),
      a.extras.length ? el("p", {class: "small num", text: "ของเพิ่ม: " + a.extras.join(" · ")}) : null,
      a.uses.length ? el("p", {class: "small", text: "ใช้ทำ: " + a.uses.join(" · ")}) : null,
      a.note ? el("p", {class: "small muted", text: a.note}) : null),
    seq ? el("div", {class: "realno" + (v === "pass" ? "" : " parked")},
      el("span", {class: "small", text: v === "pass" ? "เลขจริง" : "เลขจริง (พักไว้)"}), el("b", {class: "num", text: realCode(seq)})) : null);
  const fs = el("fieldset", {class: "rv-pick"}, el("legend", {class: "sr", text: `ผลตรวจ ${a.name}`}), ...radios);
  const box = el("li", {class: "rv-row" + (v ? " is-" + v : "")}, head, el("div", {class: "rv-act"}, fs, msg));
  if (v === "fail") {
    const rid = `rv-${d}-why`;
    const why = el("input", {id: rid, maxlength: "300", placeholder: "เหตุผล (ใส่หรือไม่ใส่ก็ได้)", disabled: !canWrite});
    why.value = r.reason || "";
    const save = async () => {
      if (why.value.trim() === (reviews[d]?.reason || "")) return;
      msg.className = "small"; msg.textContent = "กำลังบันทึก…";
      try { await saveReview(d, {reason: why.value.trim().slice(0, 300), name: myName() || reviews[d]?.name || ""}); }
      catch (e) { fail(e, "บันทึกเหตุผลไม่ได้"); }
    };
    why.addEventListener("change", save);
    const chips = REASONS.map(t => el("button", {class: "chip", type: "button", disabled: !canWrite, text: t,
      onclick: () => { why.value = why.value.trim() ? (why.value.includes(t) ? why.value : `${why.value.trim()} · ${t}`) : t; save(); }}));
    box.append(el("div", {class: "rv-why"}, el("label", {for: rid, class: "small", text: "ทำไมไม่ผ่าน"}), why, el("div", {class: "chips"}, ...chips)));
  }
  if (v && (r.name || r.updated)) box.append(el("p", {class: "small muted", text: `ติ๊กโดย ${r.name || "ไม่ระบุชื่อ"} · ${when(r.updated)}`}));
  return box;
}

let rvPending = false;
const typingReason = () => { const a = document.activeElement; return a && a.tagName === "INPUT" && a.type === "text" && !!a.closest("#rv-list"); };
function renderReview() {
  if (!$("#rv-list")) return;
  if (typingReason()) { rvPending = true; return; }       // a live refresh waits until the reason box loses focus
  rvPending = false;
  const all = RV.items, count = v => all.filter(a => verdictOf(a.draft) === v).length;
  const nPass = count("pass"), nFail = count("fail"), nWait = all.length - nPass - nFail;
  $("#rv-stats").replaceChildren(
    ...[["ผ่าน", nPass, "ได้เลขจริงแล้ว"], ["ไม่ผ่าน", nFail, "เก็บเหตุผลไว้"], ["รอตรวจ", nWait, `จาก ${all.length} SKU`]].map(([a, b, c]) =>
      el("div", {class: "stat"}, el("span", {class: "small muted", text: a}), el("b", {text: b}), el("span", {class: "small muted", text: c}))));
  const chip = (key, label, n) => el("button", {class: "chip", type: "button", "aria-pressed": String(rvFilter === key),
    onclick: () => { rvFilter = key; renderReview(); }}, `${label} ${n}`);
  $("#rv-filters").replaceChildren(chip("all", "ทั้งหมด", all.length), chip("", "รอตรวจ", nWait), chip("pass", "ผ่าน", nPass), chip("fail", "ไม่ผ่าน", nFail));
  const shown = all.filter(a => rvFilter === "all" || verdictOf(a.draft) === rvFilter);
  $("#rv-list").replaceChildren(...RV.groups.map(([g, label]) => {
    const its = shown.filter(a => a.group === g);
    return its.length ? el("section", {class: "rv-wave"}, el("h3", {}, label, " ", el("span", {class: "muted num", text: its.length})), el("ul", {class: "rv-rows"}, ...its.map(rvRow))) : null;
  }).filter(Boolean));
  if (!shown.length) $("#rv-list").append(el("p", {class: "muted", text: "ไม่มี SKU ในกลุ่มนี้"}));
  const held = RV.retired.filter(x => seqOf(reviews[x.draft]));
  $("#rv-retired").replaceChildren(
    el("summary", {}, `เลขร่างเดิมที่รวมหรือเลิกใช้ ${RV.retired.length} ตัว`, held.length ? ` · ${held.length} ตัวเคยได้เลขจริง` : ""),
    el("p", {class: "small muted", text: "จากรายการ 43 SKU เดิม ตัวที่เป็นชิ้นเดียวกันแต่ชื่อต่างกันย้ายไปเป็นไอเดียการใช้ ตัวที่สั่งทำเปลี่ยนเป็นชิ้นเปล่าตามจำนวนบวกการปั๊ม เลขจริงที่เคยออกให้จะยกเลิก ไม่ให้สินค้าอื่น"}),
    el("ul", {class: "rv-gone"}, ...RV.retired.map(x => {
      const s = seqOf(reviews[x.draft]);
      return el("li", {class: "small"}, el("span", {class: "draftno", text: "ร่าง " + x.draft}), ` ${x.name} → ${x.reason}`,
        x.into ? ` (ร่าง ${x.into})` : "", s ? el("b", {class: "num gone", text: ` เลขจริง ${realCode(s)} ยกเลิก`}) : null);
    })));
  const real = all.filter(a => verdictOf(a.draft) === "pass" && seqOf(reviews[a.draft])).sort((x, y) => reviews[x.draft].seq - reviews[y.draft].seq);
  $("#rv-real").replaceChildren(real.length
    ? el("table", {class: "num"}, el("thead", {}, el("tr", {}, ...["เลขจริง", "ร่าง", "ชื่อ", "ราคา"].map(t => el("th", {text: t})))),
        el("tbody", {}, ...real.map(a => el("tr", {}, el("td", {}, el("b", {text: realCode(reviews[a.draft].seq)})), el("td", {text: a.draft}), el("td", {text: a.name}), el("td", {text: a.price})))))
    : el("p", {class: "muted", text: "ยังไม่มี SKU ที่ผ่าน ติ๊กผ่านแล้วเลขจริงจะขึ้นที่นี่"}));
  $("#rv-copy").disabled = !real.length;
  $("#rv-copy").onclick = async () => {
    const tsv = ["เลขจริง\tร่าง\tรหัสเดิม\tชื่อ\tราคา", ...real.map(a => [realCode(reviews[a.draft].seq), a.draft, a.old || "", a.name, a.price].join("\t"))].join("\n");
    try { await navigator.clipboard.writeText(tsv); $("#rv-copymsg").className = "saved"; $("#rv-copymsg").textContent = "คัดลอกแล้ว วางในชีตได้เลย"; }
    catch { $("#rv-copymsg").className = "err"; $("#rv-copymsg").textContent = "คัดลอกไม่ได้ ลากเลือกตารางแทน"; }
  };
  const nm = $("#rv-name"); if (nm && document.activeElement !== nm) nm.value = myName();
}

function initReview() {
  const nm = $("#rv-name");
  nm.addEventListener("change", () => { try { localStorage.setItem("pd-name", nm.value.trim().slice(0, 40)); } catch {} });
  $("#rv-list").addEventListener("focusout", () => setTimeout(() => { if (rvPending) renderReview(); }, 0));
  renderReview();
}
