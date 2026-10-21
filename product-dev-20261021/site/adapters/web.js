// Data layer for pd.oct26brand.com: the same calls the page makes on the artifact database
// (collection, doc().set, add, orderBy, limit, onSnapshot), served by /api on Cloudflare Pages + D1.
// Snapshots refresh every 15 s, when the tab comes back into view, and right after this browser writes.
const API = "/api";
const DB_OFFLINE = "ยังเชื่อมต่อฐานข้อมูลไม่ได้ ที่เห็นคือค่าเริ่มต้นจาก brand.py ลองเปิดหน้าใหม่อีกครั้ง";
let PASS = "";
try { PASS = localStorage.getItem("pd-pass") || ""; } catch {}

function askPass(wrong) {
  const note = $("#dbnote");
  const input = el("input", {id: "pd-pass", type: "password", autocomplete: "current-password", placeholder: "รหัสทีม", style: "max-width:220px"});
  const ok = el("button", {class: "btn primary", type: "submit", text: "ใช้รหัสนี้"});
  const form = el("form", {class: "row"}, input, ok);
  form.addEventListener("submit", e => {
    e.preventDefault(); PASS = input.value.trim();
    try { localStorage.setItem("pd-pass", PASS); } catch {}
    note.hidden = true;
  });
  note.replaceChildren(el("p", {text: wrong ? "รหัสทีมไม่ถูก ใส่ใหม่อีกครั้ง แล้วกดบันทึกอีกที" : "ดูได้ทุกคน การบันทึกและการส่งความเห็นต้องใช้รหัสทีม ขอรหัสจากพ่อเบ"}), form);
  note.hidden = false;
}

function makeApiDb() {
  const listeners = {};
  async function refresh(col) {
    const r = await fetch(`${API}/${col}`, {headers: {accept: "application/json"}});
    if (!r.ok) throw Object.assign(new Error("read " + r.status), {code: "unavailable"});
    const rows = await r.json();
    for (const fn of listeners[col] || []) fn(rows);
  }
  const refreshAll = () => Object.keys(listeners).forEach(c => refresh(c).catch(() => {}));
  setInterval(() => { if (document.visibilityState === "visible") refreshAll(); }, 15000);
  document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible") refreshAll(); });
  async function write(method, url, data) {
    const r = await fetch(url, {method, headers: {"content-type": "application/json", "x-pd-code": PASS}, body: JSON.stringify(data)});
    if (r.status === 401) { askPass(!!PASS); throw Object.assign(new Error("passcode"), {code: "invalid_argument"}); }
    if (!r.ok) throw Object.assign(new Error("write " + r.status), {code: r.status === 429 ? "resource_exhausted" : "unavailable"});
    return r.json();
  }
  function query(col, ord, lim) {
    return {
      orderBy: (field, dir = "asc") => query(col, [field, dir], lim),
      limit: n => query(col, ord, n),
      doc: id => ({ set: async data => { await write("PUT", `${API}/${col}/${encodeURIComponent(id)}`, data); refresh(col).catch(() => {}); } }),
      add: async data => { const r = await write("POST", `${API}/${col}`, data); refresh(col).catch(() => {}); return r; },
      onSnapshot(next, error) {
        const fn = rows => {
          let r = rows.slice();
          if (ord) { const [f, dir] = ord; r.sort((a, b) => { const x = a.data[f] ?? "", y = b.data[f] ?? ""; return (x < y ? -1 : x > y ? 1 : 0) * (dir === "desc" ? -1 : 1); }); }
          if (lim) r = r.slice(0, lim);
          next({docs: r.map(x => ({id: x.id, exists: true, data: () => x.data}))});
        };
        (listeners[col] ||= new Set()).add(fn);
        refresh(col).catch(e => error && error(e));
        return () => listeners[col].delete(fn);
      },
    };
  }
  return {collection: col => query(col, null, null)};
}

async function getDb() {
  let cfg;
  try { const r = await fetch(`${API}/config`); if (!r.ok) return null; cfg = await r.json(); } catch { return null; }
  if (cfg.passcode && !PASS) askPass(false);
  return makeApiDb();
}
