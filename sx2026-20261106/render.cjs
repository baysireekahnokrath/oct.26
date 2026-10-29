// node render.cjs -> OCT26-SX2026-poster-A3.pdf, OCT26-SX2026-signs-A4.pdf and preview/*.png
const { chromium } = require("playwright");
const fs = require("node:fs"), path = require("node:path");
const jobs = [["poster", "A3", 1123, 1587], ["signs", "A4", 794, 1123]];
(async () => {
  const out = path.join(__dirname, "preview"); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const [name, format, w, h] of jobs) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto("file://" + path.join(__dirname, name + ".html"));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    const pages = await p.$$(".pg");
    for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(out, `${name}-${i + 1}.png`) });
    const over = await p.$$eval(".pg *", els => els.filter(e => { const r = e.getBoundingClientRect(), q = e.closest(".pg").getBoundingClientRect(); return r.bottom > q.bottom + 1 || r.right > q.right + 1; }).map(e => e.className || e.tagName).slice(0, 5));
    console.log(name, pages.length, "pages", over.length ? "overflow: " + over.join(",") : "");
    await p.pdf({ path: path.join(__dirname, `OCT26-SX2026-${name}-${format}.pdf`), format, printBackground: true });
    await p.close();
  }
  await b.close();
})();
