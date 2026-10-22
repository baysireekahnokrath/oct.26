// node render.cjs -> table-cover-pattern.pdf and preview-1..3.png from pattern.html
const { chromium } = require("playwright");
const path = require("node:path");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1123, height: 794 } });
  await page.goto("file://" + path.join(__dirname, "pattern.html"));
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(__dirname, "table-cover-pattern.pdf"), format: "A4", landscape: true, printBackground: true });
  const pages = await page.$$("section.p");
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(__dirname, `preview-${i + 1}.png`) });
  await browser.close();
})();
