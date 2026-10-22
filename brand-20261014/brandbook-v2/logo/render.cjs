// node logo/render.cjs -> logo/png/<name>-<size>.png for every svg (1080 and 256), plus a contact sheet
const { chromium } = require("playwright");
const fs = require("node:fs"), path = require("node:path");
(async () => {
  const dir = path.join(__dirname, "svg"), out = path.join(__dirname, "png");
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith(".svg"))) {
    const svg = fs.readFileSync(path.join(dir, f), "utf8");
    const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
    const ratio = parseFloat(m[2]) / parseFloat(m[1]);
    for (const w of [1080, 256]) {
      const h = Math.round(w * ratio);
      await p.setViewportSize({ width: w, height: h });
      await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace(/width="[\d.]+" height="[\d.]+"/, `width="${w}" height="${h}"`)}</body></html>`);
      await p.screenshot({ path: path.join(out, f.replace(".svg", `-${w}.png`)), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
    }
  }
  await b.close();
})();
