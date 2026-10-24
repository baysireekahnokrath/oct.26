// node posts/render.cjs -> posts/ep01-0..4.png (1080 x 1350) and posts/ep01-story-0..4.png (1080 x 1920)
const { chromium } = require("playwright");
const path = require("node:path");
(async () => {
  const b = await chromium.launch();
  for (const kind of ["post", "story"]) {
    const h = kind === "story" ? 1920 : 1350;
    for (let i = 0; i <= 4; i++) {
      const p = await b.newPage({ viewport: { width: 1080, height: h } });
      await p.goto("file://" + path.join(__dirname, "frame.html") + `#${kind}-${i}`);
      await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
      await p.screenshot({ path: path.join(__dirname, kind === "story" ? `ep01-story-${i}.png` : `ep01-${i}.png`) });
      await p.close();
    }
  }
  await b.close();
})();
