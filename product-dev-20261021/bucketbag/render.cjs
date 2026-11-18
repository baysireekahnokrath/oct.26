// print.html -> pattern.pdf (A4, 1:1). Run after build.py: node bucketbag/render.cjs
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.join(dir, 'print.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(dir, 'pattern.pdf'), format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true, scale: 1 });
  await b.close();
  console.log('pattern.pdf written');
})();
