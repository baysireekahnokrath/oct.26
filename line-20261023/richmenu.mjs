// richmenu.html -> richmenu.png (2500 x 1686)
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'path';
const here = path.dirname(new URL(import.meta.url).pathname);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2500, height: 1686 } });
await p.goto('file://' + path.join(here, 'richmenu.html')); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(here, 'richmenu.png') });
await b.close(); console.log('png done');
