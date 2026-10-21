# OCT. 26 — handoff for the next session

Read this first, then `README.md` (build order) and `/CLAUDE.md` (always publish a Thai summary page for deliverables).
State as of 16 Oct 2026. Moved from repo exact-8-bingo (branch `claude/brave-faraday-2x1ygq`, commit f07c22a) into this repo, folders unchanged.

## The project
A family leather brand, a birthday gift from the owner (พ่อเบ, CEO/designer) to his wife คุณบิ๊ง (born 26 Oct).
Booth at หนูทดลอง KIDS MARKET, บ้านและสวนแฟร์ Living Festival 2026, IMPACT Muang Thong Thani Challenger 2–3,
two weekends 23–25 Oct and 30 Oct–1 Nov 2569, Fri–Sun 10:00–17:00 (2 × 2 m, confirmed 21 Oct), brand launch on 26.10, the three kids (Beiya, Beana, Bene) sell at the booth.
Reply to the owner in Thai, short and plain. He decides fast; on logo questions he wants to talk before changes.

## Decisions already made (do not reopen)
- Master brand **OCT. 26** (our crafted things.). First collection **SOI. 02** (from our root, the home soi).
  Sub-brand **ห้าหมี FIVE BEARS by OCT. 26**, first collection **Love**. Future birthday brands MAR. 23, DEC. 07, OCT. 09, SEP. 01.
- **Golden ratio everywhere** (φ = 1.618): type steps, Fibonacci spacing, print sizes (tag 55×89, card 89×55,
  bag 130×210×80, pouch 210×340, edition card 89×89 mm). See `GOLDEN` in `brand.py`.
- **Palette #2 Soi Candy**: paper #FFF6EC, ink #1C1B22, cobalt #2449D8, tomato #FF5A36; sun, mint, pink for the family.
  Leather #B8743A is the material colour only. One colour per person (dad cobalt, mom tomato, Beiya sun, Beana mint, Bene pink).
- **Four logos, used one at a time, never side by side**: OCT. 26 (name), tag 26 (symbol), FIVE BEARS, bear.
  Each in light / dark / one-colour. Seal and combined lockups are retired. "OCT. " : "26" = φ² : 1 (word = 5 × cap).
  Round glyphs overshoot by H/φ⁸; text is placed by ink edge. Letters are drawn in `logolab/geometry.py`, not a font.
- No kraft paper anywhere. Do not promise "no-sew" at brand level.
- There is a private story note the owner keeps outside this public repo. Do not ask for it or put personal stories on any page unless he brings it up.

## Where things live
- `brand.py`: identity, palette, 30 products, costs (die prices, packaging) — single source of truth.
- `bible.py`: strategy text. `research/research.py`: bag research.
- Builders: `logo/`, `posters/`, `bible/`, `colorlab/`, `research/`, `logolab/`, `techpack/`, `deck/`, `site/build.py`.
- Die files: `../diecut-leather-20261014/` (svg, dxf, cost sheet scripts). Heart straps: `../diecut-leather-20261013/assembly-01/`.

## Social accounts (opened, given 21 Oct)
Instagram https://www.instagram.com/oct.26_brand/ · YouTube https://www.youtube.com/@OCT.26_brand · Facebook https://www.facebook.com/profile.php?id=61595850110023
Handle everywhere: oct.26_brand (`BRAND["handle"]`, `SOCIAL` in brand.py). TikTok and Shopee not open yet: print and posts name only the three above.

## Published pages (private, owner shares them)
- Summary https://claude.ai/artifact/1bBApc1D6ewCk8bpq3AydB
- Brand Book https://claude.ai/artifact/3asVqkM4vs6fGM3rihHSYp
- Brand Bible https://claude.ai/artifact/4FtQN6WRW3cUF1rATo3jvi
- Launch Kit https://claude.ai/artifact/AyvcJTzj5BY6spbPkZYQXS
- Customer website preview https://claude.ai/artifact/6CL8DCjTaKR6TRtnJCRTmD — source `../website/` (Cloudflare Pages, output `website/public`, waiting for the owner to connect)
- Pattern play mock-up https://claude.ai/artifact/AHD7ehgUYFz2AzfGhwKyQq — source `../play-20261021/` (website to go on Cloudflare Pages after sign-off)
- Launch posts (banners + copy) https://claude.ai/artifact/BFoXWUu2bicNUJ2NRuSHo7 — source `../social-20261021/build.py`
- Booth plan (บ้านและสวนแฟร์, 2 × 2 m) https://claude.ai/artifact/4DVjZ32YPCF9b9Ck8k7gz4 — source `../booth-20261019/build.py`
- Tech Pack https://claude.ai/artifact/XR5yqf6HFfA4JoJ9eQvapd (+ `techpack/oct26-techpack-a4.pdf`)
- Birthday deck (Slides type) https://claude.ai/artifact/D61pf56uCqYrktNuuFG2c6 — slides from `deck/build.py`, images are `/_blob/` assets
- Logo Lab, Color Lab, Product Lab, palettes, alternatives: see `site/urls.json`
- Cost sheet (Google Sheet): see `site/urls.json` key `sheet`
To update a page from a new session, publish with its URL as `url` (read it first).

## Numbers now
- Dies quoted 15 Oct: 01/04/06 = 600, 02/03/05 = 550 THB (3,450 total). Heart-strap die not quoted (950 estimate).
- Event stock 333 pieces, sales if sold out 32,712 THB, cost 8,283 THB (packaging 4,765 of it, estimates).

## Open items
1. Printer quotes for tag, paper bag, cotton pouch, story card, sticker → update `PACK_ITEMS` in `brand.py`, rebuild, republish.
2. Google Sheet still uses one die price (950) for all dies; owner was offered a per-die update.
3. Heart-strap die price. AirTag pouch (S2-10) has no hanging loop in its parts list. Windmill (S2-25) may not spin.
4. Real leather thickness and real assembly times from prototypes → update brand.py.
5. Test-print OCT. 26 at 34 mm wide and the tag 26 at 8 mm tall before ordering print.
