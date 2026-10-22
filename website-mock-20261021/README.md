# Website mock for the booth (21 Oct 2026)

https://claude.ai/artifact/E4BtLMaiyNGmTgY9dJGakF (private). A mock only: `website/` and oct26brand.com are unchanged
until the owner says "แก้เว็บจริงเลยครับ" (see `../website/HANDOFF.md`).

Follows the shared status doc: 7 single-piece SKUs (OC-01-01, OC-01-22, OC-02-24, OC-03-26, OC-04-27, OC-05-28,
OC-MX-29), no 06, no joined products, no "no-sew" wording, no pattern play. Home and product views in one page
(`#p01` … `#p29`), order bar fixed to the bottom on product views, a three-step "how to order" box, LINE and Shopee
waiting for links.

Real photos: the owner's photos are in Drive folder 1SK8GUSby1iGN7UpnX2r49ui7F9kCCkeP (8 phone photos, 2.5–5.8 MB),
too large for the Drive connector to carry. On the page, "ใส่รูปจริง" (editors only) uploads photos from the phone,
resized in the browser to 1600 px, into the page's assets (collection `tray`), and "เลือกรูป" puts one in each slot
(collection `photos`: hero, p01, p22, p24, p26, p27, p28, p29 → asset id). Claude can fetch them later with the Artifact
tool (`read` with the asset id as `path`) to build the real site.

    python3 website-mock-20261021/build.py   # -> index.html, publish to the URL above
