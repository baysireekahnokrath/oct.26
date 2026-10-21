# OCT. 26 — ฝ่ายพัฒนาสินค้า (Product Development, 21 Oct 2026)

How a product goes from idea to the booth table: 5 stages, 4 gates, a 5-point test on real leather,
a live board of the 30 products and a cost calculator for new ideas.

- `pd.py` — stages, gates, test protocol, what to try each product with, known blockers, roles, rules, 12-month plan.
  Products, prices and costs stay in `../brand-20261014/brand.py`.
- `cross3d/` — the "ไขว้ 3D" lab: 50 slot-together 3D products from the six existing dies, no new die.
  - `geom.py` reads each die SVG: outline, slits, tab necks (01 ear necks, 03–06 wing necks), 02 half slots.
  - `assemble.py` places pieces by real joints (T: tab through slit, S: the reverse, X: 02 half slots crossing) and checks
    fit (slit 0–1.0 mm longer than the neck), each cut used once, no piece passing through another where neither is cut,
    and that closing loops line up.
  - `explore.py` / `shapes.py` search shapes family by family (`python3 shapes.py 05 8` → `beam-05-8.json`).
  - `ideas.py` names the 50 picks (use, buyer, how sold, price); `catalogue.py` re-checks them and writes `x3d.json`.
  - Fits found: 01 ↔ 06 (ears 17.4 / wings 17.0 into 17.9 / 17.5 slits), 03 ↔ 03, 04 ↔ 05; 02 crosses only 02.
    Six flat pieces of 05, 03, 02, 06 or 04 (or 04 + 05) close all twelve locks into a ball without folding.
- `site/build.py` + `site/template.html` + `site/cross3d.js` → `site/index.html` (run `python3 cross3d/catalogue.py` then `python3 site/build.py`).
- Page: https://claude.ai/artifact/SfbLavVZF6JAnZKXP75EFy (private; share from the page's Share menu).
  Publish with capabilities `{"db": {}}`. The live board is in the page's database:
  `items/p01..p30` (stage, blocker, note), `items/i-*` (new ideas), `items/x-X01..` (3D ideas sent to the board), `tests/*` (test results).
  A product with no `items` document shows its starting stage from brand.py (พร้อมผลิต → ready, otherwise proto).

Starting state (21 Oct): 8 of 30 products ready, 22 still in prototype, 4 of the 8 booth heroes not ready
(21 ราวหมีห้าตัว, 23 ที่ห้อยกระเป๋าหมีหัวใจ, 18 กล่องของชำร่วยงานแต่ง, 5 ซองอั่งเปา),
183 of 333 booth pieces (22,862 of 32,712 THB sales) not yet tested.
