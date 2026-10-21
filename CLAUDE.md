# Working notes for Claude

## Project summary page (always)
When a project or task produces a deliverable, also publish a summary web page as a claude.ai Artifact and send the owner the link:
- What was made, with visuals of the work (inline SVG or images)
- Key numbers and specs
- Files delivered and where they live
- What to check, and next steps
- Written in Thai and readable on a phone
- Artifacts start private; the owner shares the link from the page's Share menu
- Keep the page's source (e.g. `site/index.html`) next to the project files so it can be updated and republished to the same URL

## Google Drive (always)
The owner keeps project files in Google Drive: folder "DIY Leather Craft" > "OCT. 26 ไฟล์งาน"
(https://drive.google.com/drive/folders/16CqzwUpTLz8fELqZM2Q0jNzrxPhFIg4v, id 16CqzwUpTLz8fELqZM2Q0jNzrxPhFIg4v).
After every deliverable, update it there through the Google Drive connector:
- Keep the index Google Doc "OCT. 26 สารบัญไฟล์และลิงก์" current (doc id 1SINc925iiXq_djJymvlbc5tvdND4MX-UpWXFgcajZFg):
  every artifact link, repo path, decision and open item. Edit it in place with the Google Docs connector
  (update_doc, replaceAllText or insertText); only if that connector is missing, upload a new version and trash the old.
- Upload files the connector can carry (Google Docs/Sheets, small text files). Large binaries (PDF, PNG, ZIP) go
  through the conversation as base64 and are not reliable; send those to the owner with the file card instead and say so.

## Status doc (always, every session)
Short shared status for every session and team (web, marketing, product development): Google Doc "OCT. 26 สถานะล่าสุด"
(doc id 1294g6UX5TfVL2ZSYksFvKMiuYQ2naGqTOMmB2aHtl-w, in the Drive folder below).
- Before starting any task, read it with the Google Drive connector's read_file_content (it is about one page; do not
  read the full index doc just to learn the current state). What it says overrides older notes in the repo or in other docs.
- When your work changes a fact in it (stock, prices, costs, what may or may not be used, decisions), edit the matching
  item under "สถานะตอนนี้" in place and add one line at the top of "บันทึกการเปลี่ยนแปลง": date · which work · what changed.
  Keep the log to the 10 newest lines and the page to about one page; move older lines into the index doc.
- Write it in Thai, short and plain.
