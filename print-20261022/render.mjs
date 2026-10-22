// print.html -> oct26-print-a4.pdf (A4, no margins); or: node render.mjs <in.html> <out.pdf>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'path';
const here = path.dirname(new URL(import.meta.url).pathname);
const [src = 'print.html', out = 'oct26-print-a4.pdf'] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage();
await p.goto('file://' + path.join(here, src)); await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: path.join(here, out), width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
await b.close(); console.log('pdf done', out);
