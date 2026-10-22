// node render.cjs -> OCT26-BrandBook-v2.pdf and preview/pNN.png from brandbook.html
const { chromium } = require("playwright");
const path = require("node:path"), fs = require("node:fs");
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1123, height: 794 } });
  await p.goto("file://" + path.join(__dirname, "brandbook.html"));
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(__dirname, "OCT26-BrandBook-v2.pdf"), format: "A4", landscape: true, printBackground: true });
  fs.mkdirSync(path.join(__dirname, "preview"), { recursive: true });
  const secs = await p.$$("section.p");
  for (let i = 0; i < secs.length; i++) await secs[i].screenshot({ path: path.join(__dirname, "preview", `p${String(i + 1).padStart(2, "0")}.png`) });
  await b.close();
})();
