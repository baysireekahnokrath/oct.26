// node render.cjs -> OCT26-booth-game-signs-A4.pdf and preview-1.png, preview-2.png
const { chromium } = require("playwright");
const path = require("node:path");
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto("file://" + path.join(__dirname, "sign.html"));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.pdf({ path: path.join(__dirname, "OCT26-booth-game-signs-A4.pdf"), format: "A4", printBackground: true });
  const pages = await p.$$(".pg");
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(__dirname, `preview-${i + 1}.png`) });
  await b.close();
})();
