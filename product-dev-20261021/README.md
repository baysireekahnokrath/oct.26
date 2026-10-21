# OCT. 26 — ฝ่ายพัฒนาสินค้า (Product Development, 21 Oct 2026)

How a product goes from idea to the booth table: 5 stages, 4 gates, a 5-point test on real leather,
a live board of the 30 products and a cost calculator for new ideas.

- `pd.py` — stages, gates, test protocol, what to try each product with, known blockers, roles, rules, 12-month plan.
  Products, prices and costs stay in `../brand-20261014/brand.py`.
- `site/build.py` + `site/template.html` → `site/index.html` (run `python3 site/build.py`).
- Page: https://claude.ai/artifact/SfbLavVZF6JAnZKXP75EFy (private; share from the page's Share menu).
  Publish with capabilities `{"db": {}}`. The live board is in the page's database:
  `items/p01..p30` (stage, blocker, note), `items/i-*` (new ideas), `tests/*` (test results).
  A product with no `items` document shows its starting stage from brand.py (พร้อมผลิต → ready, otherwise proto).

Starting state (21 Oct): 8 of 30 products ready, 22 still in prototype, 4 of the 8 booth heroes not ready
(21 ราวหมีห้าตัว, 23 ที่ห้อยกระเป๋าหมีหัวใจ, 18 กล่องของชำร่วยงานแต่ง, 5 ซองอั่งเปา),
183 of 333 booth pieces (22,862 of 32,712 THB sales) not yet tested.
