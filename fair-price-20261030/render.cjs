// node render.cjs -> OCT26-fair-price-signs-A4.pdf and preview/signs-N.png
const { chromium } = require("playwright");
const fs = require("node:fs"), path = require("node:path");
(async () => {
  const out = path.join(__dirname, "preview"); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto("file://" + path.join(__dirname, "signs.html"));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  const pages = await p.$$(".pg");
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(out, `signs-${i + 1}.png`) });
  await p.pdf({ path: path.join(__dirname, "OCT26-fair-price-signs-A4.pdf"), format: "A4", printBackground: true });
  await b.close();
})();
