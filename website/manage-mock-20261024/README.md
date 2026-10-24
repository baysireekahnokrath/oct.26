# Product manager mock (24 Oct 2026)

The owner asked (24 Oct) for a page to manage products. This is the mock, before any real change: a claude.ai Artifact
https://claude.ai/artifact/B9RyXagkt8KCB43kaLk3Hd built from `website/catalog.py`.

    python3 website/manage-mock-20261024/build.py     # template.html + catalog.py -> index.html, thumbs/

What the mock shows, all on a phone:
- product list with status (ขายอยู่ / ของหมด / ซ่อน), price and an unsent-draft dot
- one product open: status, name, price, size, page text, the three uses, photo order (first photo = card and share
  image, add from phone), search title with a live Google preview; the "ไม่ใช่ภาชนะใส่อาหาร" note is locked on coasters
- shop tab: Shopee link (empty until the owner gives it), booth notice text and end date
- send tab: every change as old -> new, words the status doc rules out block the send (ไม่ต้องเย็บ, ต่อเองได้, ฟอกฝาด,
  ใส่/ใช้กับ/สัมผัสอาหาร, food safe/grade, ของเล่น, แพตเทิร์น 06), and the four steps after sending
- request a new product (name, pattern, price, photo)

Mock limits: drafts live in this browser only and "ส่งขึ้นเว็บ" sends nothing.

The real page, if approved, replaces the paused `website/builder/` (which edits the old brand.py table):
- drafts and requests in the artifact's database (owner and Editors write), same flow as builder/APPLY.md
- a Claude session applies a request to `catalog.py` only, runs `website/build.py` (prerender included), checks, pushes
  to one branch and opens a PR; the owner merges; Cloudflare deploys `main`
- needs in `catalog.py`/`app.js`: a `status` per product (sold out shows "ของหมด ทัก LINE ถามรอบหน้า" instead of the
  order bar; hidden leaves the home page and its address redirects home), and a Shopee link that turns into a button
