# OCT. 26 website (customer site)

Home with the booth notice and the catalogue of every product in `brand.py`, one page per product
(`p/NN.html`, poster, price, size, pieces, how-to, order by Instagram chat), and the pattern play (`play.html`).
Styled with the brand CSS from `brand-20261014/site/build.py` (fonts, Soi Candy palette, φ type steps, Fibonacci spacing);
logos are the drawn SVGs, never typed.

    python3 website/build.py && node website/render.mjs && python3 website/build.py   # -> website/public

`render.mjs` makes `play.png`, the still of the pattern play on the home page. Change a price or a product in
`brand.py`, rebuild, commit and push: Cloudflare Pages redeploys on every push.

## Cloudflare (one time, by the owner)
Cloudflare's "Create an app" now makes a Worker with static assets, set up by `wrangler.jsonc` in this folder.
1. dash.cloudflare.com → Workers & Pages → Create → connect GitHub → repo `oct.26`
2. Project name `oct-26` (must match `name` in wrangler.jsonc) · Build command: (empty) · Deploy command: `npx wrangler deploy`
   · Advanced settings → Path: `website` · API token: let it create one
3. Deploy. The Worker builds from the production branch: it must be a branch that holds this folder
   (Settings → Build → Branch control). Live at https://oct-26.arthitbay.workers.dev (Settings → Domains & Routes → workers.dev must be enabled). A domain later: put it in `SITE_URL` and rebuild.

Preview before it goes live: https://claude.ai/artifact/6CL8DCjTaKR6TRtnJCRTmD (`preview/index.html` + `public/` files).
Hide a product whose prototype fails: add its number to `HIDE` in `build.py`.
The booth notice hides itself after `BOOTH["until"]` in brand.py.
