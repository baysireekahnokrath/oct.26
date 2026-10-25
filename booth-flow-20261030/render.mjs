// richmenu-booth.html -> richmenu-booth.png; print.html -> booth-flow-a4.pdf (pages 1-3) + previews; page 4 = photo sample
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'path';
const here = path.dirname(new URL(import.meta.url).pathname);
const b = await chromium.launch();
let p = await b.newPage({ viewport: { width: 2500, height: 1686 } });
await p.goto('file://' + path.join(here, 'richmenu-booth.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({ path: path.join(here, 'richmenu-booth.png') });
p = await b.newPage();
await p.goto('file://' + path.join(here, 'print.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
await p.pdf({ path: path.join(here, 'all.pdf'), preferCSSPageSize: true, printBackground: true });
await b.close(); console.log('done');
