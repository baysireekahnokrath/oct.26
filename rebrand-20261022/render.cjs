// node render.cjs -> social/*.png, print/*.pdf (and print/*.png previews) from html/ and jobs.json
const { chromium } = require("playwright");
const fs = require("node:fs"), path = require("node:path");
(async () => {
  const jobs = JSON.parse(fs.readFileSync(path.join(__dirname, "jobs.json"), "utf8"));
  for (const d of ["social", "print"]) fs.mkdirSync(path.join(__dirname, d), { recursive: true });
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w || 1123, height: j.h || 1587 } });
    await p.goto("file://" + path.join(__dirname, "html", j.name + ".html"));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    if (j.kind === "png") {
      await p.screenshot({ path: path.join(__dirname, "social", j.name + ".png"), clip: { x: 0, y: 0, width: j.w, height: j.h } });
    } else {
      const land = j.kind === "pdf-land";
      await p.pdf({ path: path.join(__dirname, "print", j.name + ".pdf"), format: "A4", landscape: land, printBackground: true });
      await p.setViewportSize(land ? { width: 1123, height: 794 } : { width: 794, height: 1123 });
      await p.screenshot({ path: path.join(__dirname, "print", j.name + "-preview.png"), clip: { x: 0, y: 0, width: land ? 1123 : 794, height: land ? 794 : 1123 } });
    }
    await p.close();
  }
  await b.close();
})();
