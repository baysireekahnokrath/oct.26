# OCT. 26 website (oct26brand.com)

The design the owner chose on 22 Oct 2026 (direction 2 "ไม่ซ้ำสักชิ้น", mock-ups in `../web-directions-20261022/`):
home with family-colour chapters (dad, mom, eldest, middle, youngest), craft textures at the edges with text on plain
plates, painted-face DIY ideas, a 3D leather simulator, corporate gifts and workshop requests; one page per product
(`/p/OC-04-27` …) with real photos, a true-size drawing from the die file, leather tone wish, quantity and a sticky
LINE order bar that copies the full order. Brand Book v2 colours, square logo, Anuphan / Jost / IBM Plex Sans Thai.

    python3 website/build.py      # -> website/public (the Worker serves only this folder)

- `catalog.py` — the 7 products (names, prices, sizes, photos, page text), links (LINE, IG, FB, Shopee name), booth.
  Change things here, rebuild, commit, PR to `main`; the owner merges and Cloudflare deploys.
- `src/` — `app.css`, `app.js` (renders the pages in the browser), `defs.svg` (paint filter for the faces).
- `assets/` — real photos (`img/`), flat-lay pieces on transparent ground (`cut/`), Brand Book v2 logos, the 07 die
  outline, and three.js r128 (MIT, loaded only when the simulator scrolls near).
- `build.py` — reads the die files (01–05 in diecut-leather-20261014, 07 in assets/) into outlines, writes `data.js`,
  one HTML file per page with its own title, description, canonical link, share image (`assets/og/`), product
  JSON-LD and a `<noscript>` version, plus `404.html`, `sitemap.xml`, `robots.txt` and `_redirects` (old 30-product
  pages and the pattern play go to the product that sells now, or home).
- The booth notice and "รับที่บูธ" lines hide themselves after `BOOTH["until"]` in catalog.py.
- `builder/` — the Web Builder (paused: it still edits the old brand.py table).
- `summary/` — Thai summary for the owner: https://claude.ai/artifact/FZ9KmqHeKZTpBu24TnGwjo · PR https://github.com/baysireekahnokrath/oct.26/pull/3

## Cloudflare (set up by the owner)
Workers Builds from GitHub, production branch `main`, root directory `website`, build command none, deploy command
`npx wrangler deploy` (`wrangler.jsonc`: Worker `oct-26`, assets `./public`, 404 page). Live at https://oct26brand.com,
also https://oct-26.arthitbay.workers.dev.
