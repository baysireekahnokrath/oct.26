// A still of the pattern play for the home page hero. Usage: node website/render.mjs (after build.py), then build.py again.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'path'; import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 1200, height: 1400}});
await p.goto('file://' + path.join(here, 'public', 'play.html')); await p.evaluate(() => localStorage.clear());
await p.reload(); await p.evaluate(() => document.fonts.ready);
await p.locator('#pattern').screenshot({path: path.join(here, 'play.png')});
await b.close(); console.log('wrote website/play.png');
