# OCT. 26 website (customer site)

Home with the booth notice and the catalogue of every product in `brand.py`, one page per product
(`p/NN.html`, poster, price, size, pieces, how-to, order by Instagram chat), and the pattern play (`play.html`).
Styled with the brand CSS from `brand-20261014/site/build.py` (fonts, Soi Candy palette, φ type steps, Fibonacci spacing);
logos are the drawn SVGs, never typed.

    python3 website/build.py && node website/render.mjs && python3 website/build.py   # -> website/public

`render.mjs` makes `play.png`, the still of the pattern play on the home page. Change a price or a product in
`brand.py`, rebuild, commit and push: Cloudflare Pages redeploys on every push.

## Cloudflare Pages (one time, by the owner)
1. dash.cloudflare.com → Workers & Pages → Create → Pages → Connect to Git → GitHub → repo `oct.26`
2. Project name `oct26` (gives oct26.pages.dev) · Production branch: the branch that holds this folder
   · Framework preset: None · Build command: (empty) · Build output directory: `website/public`
3. Save and Deploy. If the name is taken, put the given address in `SITE_URL` in `build.py` and rebuild.

Preview before it goes live: https://claude.ai/artifact/6CL8DCjTaKR6TRtnJCRTmD (`preview/index.html` + `public/` files).
Hide a product whose prototype fails: add its number to `HIDE` in `build.py`.
The booth notice hides itself after `BOOTH["until"]` in brand.py.
