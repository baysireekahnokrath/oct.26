// node render.cjs -> social/*.png (1080 x 1350, stories 1080 x 1920) and print/*.pdf (A4) from html/ and jobs.json
const { chromium } = require("playwright");
const fs = require("node:fs"), path = require("node:path");
(async () => {
  const jobs = JSON.parse(fs.readFileSync(path.join(__dirname, "jobs.json"), "utf8"));
  for (const d of ["social", "print"]) fs.mkdirSync(path.join(__dirname, d), { recursive: true });
  const b = await chromium.launch();
  for (const j of jobs) {
    const url = "file://" + path.join(__dirname, "html", j.name + ".html");
    const p = await b.newPage({ viewport: { width: j.w || 1080, height: j.h || 1350 } });
    await p.goto(url); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(__dirname, "social", j.name + ".png") });
    if (j.png_only) { await p.close(); continue; }
    await p.setViewportSize({ width: 794, height: 1123 }); await p.waitForTimeout(200);
    await p.pdf({ path: path.join(__dirname, "print", j.name + "-A4.pdf"), width: "210mm", height: "297mm", printBackground: true });
    await p.close();
  }
  await b.close();
})();
