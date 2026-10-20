# Booth plan — งานบ้านและสวน, 23–25 Oct 2569

One 2 × 2 m booth with the organiser's pallet table (117 × 80 cm, 50 cm high) and two folding chairs
(`site/organizer-table.jpg`); other gear from HomePro, IKEA, 20-baht shops and Shopee.
Products, prices and stock come from `../brand-20261014/brand.py`; the page style from `../brand-20261014/site/build.py`.

    python3 booth-20261019/build.py      # writes site/index.html

Page (private, owner shares it): https://claude.ai/artifact/4DVjZ32YPCF9b9Ck8k7gz4
Booth dressing budget is capped at 3,000 THB (`BUDGET`, the build fails if must-buy gear goes over); no roll-up. The booth has no walls, so signage is a free-standing 60 × 160 cm X-stand. Gear prices are estimates, not shop quotes. Organiser confirmed 20 Oct: one table and two chairs per booth, 5A power, table can be moved, wide slat gaps (folding 5 mm future-board top). Booth number and hall are still open.

X-stand 60 × 160 cm (brand, hook and starting price, QR to Instagram with every channel, six products with prices,
collections; no event name, so it is reused at every fair):

    python3 booth-20261019/xstand/build.py && node booth-20261019/xstand/render.mjs

Print files: `xstand/oct26-xstand-60x160.pdf` (vector, fonts embedded) and `xstand/oct26-xstand-60x160.jpg` (100 dpi).
Run `xstand/render.mjs` before `build.py` so the page picks up the new `xstand/preview.png`.
