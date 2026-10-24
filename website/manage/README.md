# Product manager (24 Oct 2026)

The owner's page for what oct26brand.com sells, a claude.ai Artifact: https://claude.ai/artifact/B9RyXagkt8KCB43kaLk3Hd
(private; the owner shares it from the page's Share menu, Editor level, to let someone else edit). It replaces the Web
Builder in `../builder/`, which edited the old 30-product table. Mock first: `../manage-mock-20261024/`.

On the page, from a phone:
- **สินค้า**: each product's status (ขายอยู่ / ของหมด / ซ่อน), name, price, size, page text, three uses, photo order and
  new photos (uploaded to the page's asset store), search title with a Google preview. Coasters keep "ไม่ใช่ภาชนะใส่อาหาร".
  "+ ขอเพิ่มสินค้าใหม่" records a new single-piece product with a photo.
- **ร้านและบูธ**: the Shopee shop link (a Shopee button appears on every page once set) and the booth notice.
- **ส่งขึ้นเว็บ**: every change as old -> new; words the status doc rules out (`catalog.BANNED`) block the send. Sending
  saves a request and starts a Claude Code session (Claude Code Remote connector, `create_session`) that follows
  `APPLY.md`: `apply.py` edits `../catalog.json`, `../build.py` rebuilds and checks the site, one PR from
  `manage-products` to `main`. The owner merges; Cloudflare deploys; the session republishes this page and clears the
  drafts that went live. The latest requests show their state and the PR button.

    python3 website/manage/build.py                   # template.html + catalog.json -> index.html, thumbs/ (prints the files map)
    python3 website/manage/apply.py request.json [--write]
    python3 website/manage/photo.py <file> <name>     # an uploaded photo -> website/assets/img/<name>.jpg

Every edit is a draft in the page's database at once (`drafts/<SKU>`, `drafts/shop`, `adds/<id>`; requests in
`requests/<id>`); nothing reaches the site before a merge. While someone types, the field they are in is never redrawn
(a redrawn input closes the phone keyboard): only the counters, warnings and preview around it are patched.

Publish (first time, or when capabilities change): Artifact publish `website/manage/index.html` with `url` above, the
thumbs `files` map that build.py prints, and
`capabilities = {db: {rules: [drafts, adds, requests: read "view", write "admin"]}, user: {}, assets: {},
mcp: {servers: [{server: "Claude Code Remote", tools: ["create_session"]}]}}`. After a merge, republish without
`capabilities` (they stay).
