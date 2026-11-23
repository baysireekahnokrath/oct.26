// lay the rebuilt solid shapes over the brand book SVGs and count pixels that differ
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const dir = path.join(__dirname, 'ref'); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 1400 } });
  for (const [ref, mine, w, h] of [['line-light.svg', 'rebuilt-line.svg', 576.39, 190.98], ['square-mono.svg', 'rebuilt-square.svg', 461.14, 461.14]]) {
    let a = fs.readFileSync(path.join(dir, ref), 'utf8').replace(/#5E7A3A/g, '#2A2725');
    const k = 2.4, W = Math.round(w * k), H = Math.round(h * k);
    const res = await p.evaluate(async ({ a, m, W, H }) => {
      const draw = svg => new Promise(r => { const i = new Image(); i.onload = () => { const c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, W, H); x.drawImage(i, 0, 0, W, H); r(x.getImageData(0, 0, W, H).data); }; i.src = 'data:image/svg+xml;base64,' + btoa(svg); });
      const A = await draw(a), M = await draw(m); let ink = 0, diff = 0;
      for (let i = 0; i < A.length; i += 4) { const x = A[i] < 128, y = M[i] < 128; if (x) ink++; if (x !== y) diff++; }
      return { ink, diff };
    }, { a, m: fs.readFileSync(path.join(dir, mine), 'utf8'), W, H });
    console.log(ref, 'ink px', res.ink, 'differing px', res.diff, '=', (100 * res.diff / res.ink).toFixed(2) + '% of the ink');
  }
  await b.close();
})();
