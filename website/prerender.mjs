// Writes what app.js draws into each built HTML file, so search engines and chat previews get the full text without
// running scripts. Run by build.py:  node website/prerender.mjs website/public
// Also draws the square logo as a PNG for the Organization JSON-LD (Google does not take SVG logos).
import { createServer } from "node:http";
import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join, extname } from "node:path";
import { createRequire } from "node:module";

const OUT = process.argv[2];
const { chromium } = createRequire(import.meta.url)("playwright");
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".webp": "image/webp", ".png": "image/png" };

// same addressing as Cloudflare's extensionless html_handling: /p/OC-04-27 -> p/OC-04-27.html, / -> index.html
const server = createServer((req, res) => {
  let f = join(OUT, decodeURIComponent(new URL(req.url, "http://x").pathname));
  if (f.endsWith("/")) f += "index.html";
  else if (!extname(f)) f += ".html";
  if (!existsSync(f)) { res.writeHead(404).end(); return; }
  res.writeHead(200, { "content-type": TYPES[extname(f)] || "application/octet-stream" }).end(readFileSync(f));
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}`;

const pages = ["index.html", ...readdirSync(join(OUT, "p")).map(f => "p/" + f)];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
// fonts and anything else off-site are not needed to read the text
await page.route("**/*", r => r.request().url().startsWith(base) ? r.continue() : r.abort());
try {
  for (const f of pages) {
    const file = join(OUT, f), src = readFileSync(file, "utf8");
    if (!src.includes("<!--prerender-->")) continue;
    await page.goto(base + "/" + f.replace(/(index)?\.html$/, ""));
    await page.waitForSelector("#view footer");
    // the 3D simulator is built by app.js on every load; leave its slot empty
    const drawn = await page.evaluate(() => { const v = document.querySelector("#view").cloneNode(true);
      v.querySelectorAll(".sim-slot").forEach(s => s.replaceChildren()); return v.innerHTML; });
    writeFileSync(file, src.replace(/<main id="view" class="d2"><!--prerender-->.*?<\/main>/s, () => `<main id="view" class="d2">${drawn}</main>`));
  }
  await page.setViewportSize({ width: 512, height: 512 });
  await page.goto(base + "/assets/logo/square-light.svg");
  await page.evaluate(() => { const s = document.documentElement; s.setAttribute("width", "512"); s.setAttribute("height", "512"); });
  await page.screenshot({ path: join(OUT, "assets", "logo", "square-light.png"), clip: { x: 0, y: 0, width: 512, height: 512 } });
} finally {
  await browser.close(); server.close();
}
console.log("prerendered", pages.length, "pages");
