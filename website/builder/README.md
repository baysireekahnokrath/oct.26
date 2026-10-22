# OCT.26 Web Builder (21 Oct 2026)

**Paused since 22 Oct**: the site now reads `website/catalog.py`; the builder still edits the old brand.py table. See APPLY.md.

The owner's editor for the customer website, a claude.ai Artifact: https://claude.ai/artifact/NrAfdYHGTETkYWbMjT9QXG
(private; share it from the page's Share menu, Editor level, to let someone else edit).

On the page: tap a product to change its name, price, sales line (hook, also printed on the poster) or size, hide it, or
mark it sold out; set the date the booth notice shows until. Every edit is saved at once as a draft in the page's
database (`drafts/p01`..`p30`, `drafts/booth`); the site does not change yet. "ขึ้นเว็บ" shows the list of changes,
saves it as `requests/<id>` and starts a Claude Code session in the OCT.26 environment (the page's Claude Code Remote
connector, `create_session`) that follows `APPLY.md`: apply, rebuild, push to the branch `web-builder` and open (or
update) one PR to `main`. The owner approves by merging it; Cloudflare deploys `main` in a few minutes, and the page
is republished from `main` with its new baseline. If the page cannot start the session it shows the message to paste into Claude Code.

    python3 website/builder/apply.py drafts.json [--write]   # check / apply drafts -> brand.py, website/build.py, posters, site
    python3 website/builder/build.py                          # index.html (the page) + live.json (what the site shows now)

- `apply.py` — checks each value (text length, whole-baht price, date) and replaces the literals in brand.py's `P` table and
  `BOOTH` with `ast` positions, so comments stay; HIDE and SOLD sets in `website/build.py`. Re-renders only the posters
  whose name, hook or price changed (and their 360 × 450 thumbnails), then rebuilds the website and this page.
- `build.py` — the page: brand CSS from `brand-20261014/site/build.py`, the wordmark SVGs, live.json embedded as the
  baseline. Publish with `thumbs/NN.jpg` from `brand-20261014/posters/thumb/`.
- `APPLY.md` — the steps the Claude session follows for one request.
- `site/index.html` — the Thai summary page for the owner: https://claude.ai/artifact/Ri5KftRrBj95dX1cjRMWvP

Database rules: everyone the page is shared with reads; only the owner and Editors write.
