// OCT. 26 PD operation system: the /api the page talks to (Cloudflare Pages Function + D1 bound as DB).
//
//   GET  /api/config              {passcode: bool}  whether writes need the team passcode
//   GET  /api/<col>               [{id, data}] newest first, col = items | tests | comments | reviews
//   PUT  /api/items/<id>          set one board item (stage, blocker, note, or a whole idea)
//   PUT  /api/reviews/<draft>     tick a SKU ผ่าน / ไม่ผ่าน and its stage {verdict, reason, name, seq, issued, stage}; seq is its real number,
//                                 refused (409) if another SKU holds it or this SKU already has a different one
//   POST /api/tests               add a test result
//   POST /api/comments            add a comment {item, name, text}
//
// No login. If the secret PD_PASSCODE is set, every write needs header x-pd-code equal to it.
// Writes are limited per IP (WRITE_LIMIT per 10 minutes); nothing can be deleted through the API.
// The tables are created on first use, so a fresh D1 database needs no console step.

const READ_MAX = 2000, BODY_MAX = 8000, WRITE_LIMIT = 120, WINDOW_MS = 10 * 60 * 1000;
const ID = /^[A-Za-z0-9_\-:.~@+]{1,80}$/;
const DRAFT = /^[0-9]{4}$/, SEQ_MIN = 260001, SEQ_MAX = 999999;
const STAGES = new Set(["idea", "proto", "tested", "ready", "selling", "hold"]);
let ready = false;

const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status, headers: {"content-type": "application/json; charset=utf-8", "cache-control": "no-store"},
});

async function ensure(db) {
  if (ready) return;
  await db.batch([
    db.prepare("CREATE TABLE IF NOT EXISTS docs (col TEXT NOT NULL, id TEXT NOT NULL, data TEXT NOT NULL, updated TEXT NOT NULL, ip TEXT, PRIMARY KEY (col, id))"),
    db.prepare("CREATE INDEX IF NOT EXISTS docs_col_updated ON docs (col, updated)"),
    db.prepare("CREATE TABLE IF NOT EXISTS writes (ip TEXT NOT NULL, at INTEGER NOT NULL)"),
    db.prepare("CREATE INDEX IF NOT EXISTS writes_ip_at ON writes (ip, at)"),
  ]);
  ready = true;
}

const str = (v, max) => typeof v === "string" && v.length <= max;

// What each collection accepts. Returns the cleaned document or null.
function clean(col, d, now) {
  if (!d || typeof d !== "object" || Array.isArray(d)) return null;
  if (col === "comments") {
    if (!str(d.item, 80) || !str(d.name, 40) || !str(d.text, 1000)) return null;
    const name = d.name.trim(), text = d.text.trim();
    if (!name || !text) return null;
    return {item: d.item, name, text, at: now};                       // time is the server's
  }
  if (col === "tests") {
    if (!str(d.item, 80) || !str(d.tester ?? "", 40) || !str(d.note ?? "", 200)) return null;
    const out = {item: d.item, tester: d.tester || "", note: d.note || "", seconds: Math.max(0, Math.min(36000, +d.seconds || 0)), at: now};
    for (const k of ["build", "pull", "fit", "tear", "photo"]) out[k] = ["pass", "fail"].includes(d[k]) ? d[k] : "";
    return out;
  }
  if (col === "reviews") {
    if (!["", "pass", "fail"].includes(d.verdict ?? "") || !str(d.reason ?? "", 300) || !str(d.name ?? "", 40) || !str(d.issued ?? "", 40)) return null;
    if (d.stage !== undefined && !STAGES.has(d.stage)) return null;
    const seq = d.seq ?? null;
    if (seq !== null && !(Number.isInteger(seq) && seq >= SEQ_MIN && seq <= SEQ_MAX)) return null;
    return {verdict: d.verdict || "", reason: (d.reason || "").trim(), name: (d.name || "").trim(), seq, issued: seq ? (d.issued || now) : "",
      ...(d.stage ? {stage: d.stage} : {}), updated: now};
  }
  if (col === "items") {
    if (d.stage !== undefined && !STAGES.has(d.stage)) return null;
    for (const [k, v] of Object.entries(d)) {
      if (k.length > 40) return null;
      const ok = v === null || typeof v === "number" || typeof v === "boolean" || str(v, 500) ||
        (Array.isArray(v) && v.length <= 20 && v.every(x => Array.isArray(x) && x.length === 2 && str(x[0], 10) && typeof x[1] === "number"));
      if (!ok) return null;
    }
    return {...d, updated: now};
  }
  return null;
}

export async function onRequest({request, env, params}) {
  const db = env.DB;
  if (!db) return json({error: "D1 database is not bound as DB"}, 500);
  await ensure(db);
  const [col, rawId, extra] = params.path || [];
  const method = request.method;

  if (col === "config" && method === "GET") return json({passcode: !!env.PD_PASSCODE});
  if (!["items", "tests", "comments", "reviews"].includes(col) || extra !== undefined) return json({error: "not found"}, 404);

  if (method === "GET" && rawId === undefined) {
    const {results} = await db.prepare("SELECT id, data FROM docs WHERE col = ? ORDER BY updated DESC LIMIT ?").bind(col, READ_MAX).all();
    return json(results.map(r => ({id: r.id, data: JSON.parse(r.data)})));
  }

  const isPut = method === "PUT" && (col === "items" || col === "reviews") && rawId !== undefined;
  const isPost = method === "POST" && (col === "tests" || col === "comments") && rawId === undefined;
  if (!isPut && !isPost) return json({error: "method not allowed"}, 405);

  if (env.PD_PASSCODE && request.headers.get("x-pd-code") !== env.PD_PASSCODE) return json({error: "passcode"}, 401);

  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  const t = Date.now();
  const {n} = await db.prepare("SELECT COUNT(*) AS n FROM writes WHERE ip = ? AND at > ?").bind(ip, t - WINDOW_MS).first();
  if (n >= WRITE_LIMIT) return json({error: "too many writes, wait a few minutes"}, 429);

  const text = await request.text();
  if (text.length > BODY_MAX) return json({error: "too large"}, 413);
  let body; try { body = JSON.parse(text); } catch { return json({error: "bad json"}, 400); }
  const now = new Date(t).toISOString();
  const doc = clean(col, body, now);
  if (!doc) return json({error: "invalid fields"}, 400);

  let id = isPut ? decodeURIComponent(rawId) : crypto.randomUUID();
  if (!ID.test(id) || (col === "reviews" && !DRAFT.test(id))) return json({error: "bad id"}, 400);

  if (col === "reviews") {          // a real number belongs to one SKU for good
    const old = await db.prepare("SELECT json_extract(data, '$.seq') AS seq FROM docs WHERE col = 'reviews' AND id = ?").bind(id).first();
    if (old && old.seq && doc.seq !== old.seq) return json({error: "real number is permanent", seq: old.seq}, 409);
    if (doc.seq) {
      const other = await db.prepare("SELECT id FROM docs WHERE col = 'reviews' AND id != ? AND json_extract(data, '$.seq') = ?").bind(id, doc.seq).first();
      if (other) return json({error: "real number taken", by: other.id}, 409);
    }
  }

  await db.batch([
    db.prepare("INSERT INTO docs (col, id, data, updated, ip) VALUES (?, ?, ?, ?, ?) ON CONFLICT (col, id) DO UPDATE SET data = excluded.data, updated = excluded.updated, ip = excluded.ip")
      .bind(col, id, JSON.stringify(doc), now, ip),
    db.prepare("INSERT INTO writes (ip, at) VALUES (?, ?)").bind(ip, t),
    db.prepare("DELETE FROM writes WHERE at < ?").bind(t - WINDOW_MS),
  ]);
  return json({id});
}
