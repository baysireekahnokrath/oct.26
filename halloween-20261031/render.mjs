// posts/*.html -> posts/*.png (1080 x 1350) and site/pN.jpg previews
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs'; import path from 'path';
const here = path.dirname(new URL(import.meta.url).pathname);
const files = fs.readdirSync(path.join(here, 'posts')).filter(f => f.endsWith('.html')).sort();
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
for (const [i, f] of files.entries()) {
  await p.goto('file://' + path.join(here, 'posts', f)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(here, 'posts', f.replace('.html', '.png')) });
  await p.screenshot({ path: path.join(here, 'site', `p${i + 1}.jpg`), type: 'jpeg', quality: 80 });
}
await b.close(); console.log('rendered', files.length);
