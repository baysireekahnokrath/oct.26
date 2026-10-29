// node render.cjs -> OCT26-Brand-Bible.pdf (A4 landscape) and preview/pNN.png from bible.html
const { chromium } = require("playwright");
const fs = require("node:fs"), path = require("node:path");
(async () => {
  const out = path.join(__dirname, "preview"); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1123, height: 794 } });
  await p.goto("file://" + path.join(__dirname, "bible.html"), { waitUntil: "load" });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  const pages = await p.$$(".p");
  for (let i = 0; i < pages.length; i++)
    await pages[i].screenshot({ path: path.join(out, `p${String(i + 1).padStart(2, "0")}.png`) });
  const over = await p.$$eval(".p", els => els.map((e, i) => e.scrollHeight > e.clientHeight + 1 || e.scrollWidth > e.clientWidth + 1 ? i + 1 : 0).filter(Boolean));
  console.log("pages", pages.length, "overflow", over);
  await p.pdf({ path: path.join(__dirname, "OCT26-Brand-Bible.pdf"), width: "297mm", height: "210mm", printBackground: true });
  await b.close();
})();
