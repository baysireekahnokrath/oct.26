# Website handoff — for the OCT.26 Web Builder session

State on 21 Oct 2026, from the marketing and sales session. Read `/CLAUDE.md` (publish a Thai summary page for
every deliverable) and `brand-20261014/HANDOFF.md` (brand decisions not to reopen). Reply to the owner in Thai, short.

## Live
- **https://oct26brand.com** works (custom domain on the Cloudflare Worker `oct-26`, account arthitbay@gmail.com).
- `www.oct26brand.com`: not working yet. The owner was told to add it as a second custom domain
  (Worker → Domains → Add Domain); if Cloudflare says a `www` record exists, delete it in DNS → Records first.
- Also answers at https://oct-26.arthitbay.workers.dev.
- This container's network cannot open these hosts (proxy 403), so the live site cannot be checked from here;
  ask the owner for a screenshot.

## How it deploys
- Cloudflare Workers Builds from GitHub `baysireekahnokrath/oct.26`, production branch `main`.
  Build command: none · Deploy command: `npx wrangler deploy` · Root directory: `website`
  (`website/wrangler.jsonc`: name `oct-26`, assets `./public`, 404 page). `npx -y wrangler@4 deploy --dry-run`
  in `website/` checks the config without deploying.
- `website/public/` is committed (no build step on Cloudflare). Change → `python3 website/build.py`
  (and `node website/render.mjs` then build again if the pattern play's look changes) → commit → PR to `main`
  → the owner merges → Cloudflare deploys. The owner wants to approve each change by merging.
- PR #2 (https://github.com/baysireekahnokrath/oct.26/pull/2, canonical links, share images and sitemap at
  oct26brand.com) is merged into `main` (c711375).

## Web Builder (21 Oct, session "OCT.26 Web Builder")
- https://claude.ai/artifact/NrAfdYHGTETkYWbMjT9QXG, source `website/builder/` (start with its README.md). The owner
  edits name, price, hook, size, hide, sold out and the booth notice date on the phone; edits are drafts in the page's
  database. "ขึ้นเว็บ" starts a Claude Code session that follows `website/builder/APPLY.md`: `apply.py` patches
  brand.py / website/build.py, re-renders the changed posters, rebuilds, pushes to `web-builder` and opens one PR to
  `main`. The owner merges it, so every change is still approved by merging. Thai summary:
  https://claude.ai/artifact/Ri5KftRrBj95dX1cjRMWvP
- `website/build.py` gained `SOLD` (sold-out label on cards and product pages, OutOfStock in the JSON-LD).
- Works only once `website/builder/` is on `main` (branch `claude/funny-tesla-4dkwm7`, PR not opened yet).
  The button's Claude session itself has not been tried yet: the first real "ขึ้นเว็บ" is the test.

## Where things come from
- All content from `brand-20261014/brand.py`: products and prices (`PRODUCTS`), story, `BOOTH` (the booth notice
  hides itself after `BOOTH["until"]`), `SOCIAL` (instagram, youtube, facebook, `web` = oct26brand.com),
  `SHOP_NAME` (Shopee shop "OCT.26 - Our crafted things.").
- Look from the brand CSS in `brand-20261014/site/build.py` (`CSS`, `FONT_LINK`): Soi Candy palette, φ type steps,
  Fibonacci spacing, Anuphan / Jost / IBM Plex Sans Thai, Mitr for ห้าหมี. Logos are the drawn SVGs in
  `brand-20261014/logo/svg`, never typed. Prices and order buttons in tomato.
- Pattern play: `website/play.html` (template), piece outlines and slits read at 1:1 from
  `diecut-leather-20261014/svg` through `play-20261021/build.py`. Leather swatches are material tones, not brand colours.
- Product images are the How-to posters (`brand-20261014/posters/png`, thumbs in `posters/thumb`).
- Claude.ai preview of the site: https://claude.ai/artifact/6CL8DCjTaKR6TRtnJCRTmD (`website/preview/index.html`
  plus `website/public` files).

## Open items the owner raised or was told about
1. Add `www.oct26brand.com`. Merge the Web Builder branch, then try one real "ขึ้นเว็บ".
2. Shopee: shop exists, link not given yet. When the owner sends `shopee.co.th/...`, add it to `SOCIAL` and make a
   Shopee button on the home page and product pages.
3. 17 products are still "ลองต้นแบบก่อน" in brand.py; all are listed because orders go through Instagram chat.
   Hide one that fails its test on the Web Builder (or add its number to `HIDE` in `website/build.py`).
4. Posters' footer reads "Shopee OCT. 26"; the shop's real name is "OCT.26 - Our crafted things.". The owner has not
   said whether to re-render them. A Web Builder edit re-renders that product's poster with the same footer.
5. Pattern play snaps to a 7.5 mm grid; snapping a lobe into a neighbour's slit was offered for later.
6. The repo is public, so costs and margins in brand.py are visible. The owner was advised to make it private
   (Cloudflare builds private repos too).
7. Brand rule: "OCT. 26" has a dot and a space; the Shopee shop name "OCT.26" has no space (owner told, no decision).
