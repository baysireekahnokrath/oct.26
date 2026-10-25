# OCT. 26 website (oct26brand.com)

The design the owner chose on 22 Oct 2026 (direction 2 "ไม่ซ้ำสักชิ้น", mock-ups in `../web-directions-20261022/`):
home with family-colour chapters (dad, mom, eldest, middle, youngest), craft textures at the edges with text on plain
plates, painted-face DIY ideas, a 3D leather simulator, corporate gifts and workshop requests; one page per product
(`/p/OC-04-27` …) with real photos, a true-size drawing from the die file, leather tone wish, quantity and a sticky
LINE order bar that copies the full order. Brand Book v2 colours, square logo, Anuphan / Jost / IBM Plex Sans Thai.

    python3 website/build.py      # -> website/public (the Worker serves only this folder); needs node + Playwright Chromium

- `catalog.json` — the products (status on/out/off, names, search titles `seo`, prices, sizes, photos, page text), the
  Shopee link, the booth and photo descriptions; the product manager edits it. `catalog.py` loads it, holds the fixed
  links (LINE, IG, FB), old addresses and the rules (`BANNED`, `problems()`) that build.py checks before building.
  Change things here, rebuild, commit, PR to `main`; the owner merges and Cloudflare deploys.
- `src/` — `app.css`, `app.js` (renders the pages in the browser), `defs.svg` (paint filter for the faces).
- `assets/` — real photos (`img/`), flat-lay pieces on transparent ground (`cut/`), Brand Book v2 logos, the 07 die
  outline, and three.js r128 (MIT, loaded only when the simulator scrolls near).
- `build.py` — reads the die files (01–05 in diecut-leather-20261014, 07 in assets/) into outlines, writes `data.js`,
  one HTML file per page with its own search title, description, canonical link, share image (`assets/og/`) and
  JSON-LD (Organization + WebSite on home, Product + BreadcrumbList per product), plus `404.html`, `sitemap.xml`,
  `robots.txt` and `_redirects` (old 30-product pages and the pattern play go to the product that sells now, or home).
- `prerender.mjs` — run by build.py: opens each page in Chromium and writes what app.js drew into the HTML, so search
  engines and LINE/Facebook previews read the full text without scripts (app.js redraws the same markup on load). It
  also draws `assets/logo/square-light.png` for the Organization logo.
- The booth notice hides itself in the browser after ``until` in catalog.json; rebuild once after that date so
  the written-in text drops it too.
- SEO plan (22–24 Oct): search titles per product, photo descriptions, full text in HTML, structured data. Still to do:
  Google Search Console (owner verifies the domain, then submit `sitemap.xml`), pattern pages 01–07, a leather care
  page, a workshop page and an ideas page, same keywords in Shopee titles.
- `/game` and `/game/done` — the booth game for 30 Oct–1 Nov 2026 (KIDS MARKET, from the LINE rich menu "รับชิ้นหนังฟรี"):
  match 6 pairs of real die-cut photos (`assets/game/`: the same files as the approved mock, booth-flow-20261030/site, 360 px webp with their soft shadow, ~273 KB),
  then /game/done shows the time and "โชว์หน้านี้ที่บูธ OCT. 26 · รับชิ้นหนังวัวแท้ 01 ฟรี 1 แผ่น". Page: `src/game.html`,
  cards and end time: `catalog.GAME`. Finishing loads the real address /game/done so request stats can count it. No form,
  no cookie, no storage; anyone may open /game/done directly (owner's choice). noindex, not in the sitemap or menu. After
  1 Nov 17:00 (Thai time) both pages say the booth activity has ended; rebuild once after that date so the files say it
  too. Not /play: _redirects sends that home (301). Thai summary: https://claude.ai/artifact/BYHS92GPtQr18ZFWDRQDrx (`summary-game/`).
- `manage/` — the product manager page (status, prices, text, photos, Shopee link, booth; sends a PR): https://claude.ai/artifact/B9RyXagkt8KCB43kaLk3Hd
- `builder/` — the old Web Builder, retired 24 Oct (it edited the old brand.py table).
- `summary/` — Thai summary for the owner: https://claude.ai/artifact/FZ9KmqHeKZTpBu24TnGwjo · PR https://github.com/baysireekahnokrath/oct.26/pull/3
- `summary-seo/` — Thai summary of the SEO round: https://claude.ai/artifact/Pg49fYeseXDQhsfGdsz8SN · PR https://github.com/baysireekahnokrath/oct.26/pull/4

## Cloudflare (set up by the owner)
Workers Builds from GitHub, production branch `main`, root directory `website`, build command none, deploy command
`npx wrangler deploy` (`wrangler.jsonc`: Worker `oct-26`, assets `./public`, 404 page). Live at https://oct26brand.com,
also https://oct-26.arthitbay.workers.dev.
