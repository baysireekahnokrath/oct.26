// Render the X-stand: vector PDF for the print shop, 100 dpi JPG for shops that want an image, small preview.
// Usage: node booth-20261019/xstand/render.mjs
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'path';
import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const src = 'file://' + path.join(here, 'xstand.html');
const W = 600, H = 1600, DPI = 100;                     // mm, print resolution for the JPG
const px = mm => Math.round(mm / 25.4 * 96);            // CSS px at 96 per inch
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: px(W), height: px(H) }, deviceScaleFactor: DPI / 96 });
await page.goto(src, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: path.join(here, 'oct26-xstand-60x160.pdf'), width: `${W}mm`, height: `${H}mm`, printBackground: true });
await page.screenshot({ path: path.join(here, 'oct26-xstand-60x160.jpg'), type: 'jpeg', quality: 92, fullPage: false });
const small = await browser.newPage({ viewport: { width: px(W), height: px(H) }, deviceScaleFactor: 0.25 });
await small.goto(src, { waitUntil: 'networkidle' });
await small.evaluate(() => document.fonts.ready);
await small.screenshot({ path: path.join(here, 'preview.png') });
await browser.close();
console.log('wrote oct26-xstand-60x160.pdf, oct26-xstand-60x160.jpg, preview.png');
