// node render.cjs -> OCT26-fair-price-signs-A4.pdf, OCT26-fair-collect-A4.pdf, OCT26-fair-table-tents-A4.pdf and preview/*.png
const { chromium } = require("playwright");
const fs = require("node:fs"), path = require("node:path");
(async () => {
  const out = path.join(__dirname, "preview"); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const [name, pdf, land] of [["signs", "OCT26-fair-price-signs-A4.pdf"], ["collect", "OCT26-fair-collect-A4.pdf"], ["tent", "OCT26-fair-table-tents-A4.pdf", true]]) {
    const p = await b.newPage({ viewport: land ? { width: 1123, height: 794 } : { width: 794, height: 1123 } });
    await p.goto("file://" + path.join(__dirname, name + ".html"));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    const pages = await p.$$(".pg");
    for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(out, `${name}-${i + 1}.png`) });
    await p.pdf({ path: path.join(__dirname, pdf), format: "A4", landscape: !!land, printBackground: true });
    await p.close();
  }
  await b.close();
})();
