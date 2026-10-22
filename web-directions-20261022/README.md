# Six website directions (22 Oct 2026)

Round 2, colourful: https://claude.ai/artifact/CZUKqtSgk7TUTyY6Qcucga (`template-v2.html` -> `index-v2.html`, `python3 build.py v2`).
The owner asked for more colour: every section takes a family colour (full or light) with a craft texture (saddle stitch,
punch holes, gingham, stripes, die-shape stamps, paper grain), pieces carry painted faces as DIY examples (six faces,
wobbly paint edges via an SVG displacement filter), and the 3D simulator paints a face decal in seven ink colours.
This goes past Brand Book v2 (family colours as small details) and the status doc's "no bear face" rule, at the owner's
request for this mock; both are flagged on the page's summary tab.

Round 1:

https://claude.ai/artifact/1xTex5SX5dq6MJTR1se7f7 (private) — mock-ups after the owner's six reference boards
(Spring, faces, Originality, Cupful of Joy, Rayo, Markaworks). Not the live site: `website/` is unchanged until the
owner says "แก้เว็บจริงเลยครับ".

Each direction carries the same content: brand story, a 3D simulator (pattern 01–05 / 07, eight leather tones, drag to
turn), the 7 products from the status doc, corporate gifts (live preview of the envelope card), workshop booking (mock
form). Brand Book v2: cotton/charcoal, family colours as small details, square logo, Anuphan / Jost / IBM Plex Sans Thai.
Status-doc rules: no 06 (07 instead), no joined products or "no-sew", coasters marked "not a food container", no
products for small children, workshops decorate single pieces only.

- `template.html` — the page (CSS + JS); `build.py` reads the die files (01–05 from diecut-leather-20261014, 07 from
  `src/07.svg`, copied from diecut-leather-20261019) into polygons and writes `index.html`.
- `assets/img` — real photos, `assets/cut` — flat-lay pieces on transparent ground (both from the rebrand work on
  branch claude/brand-guidelines-doc, cut-outs resized to 560 px), `assets/logo` — Brand Book v2 logos.
- 3D: three.js r128 from cdnjs; without WebGL the simulator falls back to a flat drawing of the piece.

    python3 web-directions-20261022/build.py   # -> index.html; publish with assets/img and assets/cut
