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
- Keep the index Google Doc "OCT. 26 สารบัญไฟล์และลิงก์" current (doc id 1SINc925iiXq_djJymvlbc5tvdND4MX-UpWXFgcajZFg, replaced on every update):
  every artifact link, repo path, decision and open item. The connector cannot edit a Doc in place, so upload a new
  version into the same folder and trash the old one.
- Upload files the connector can carry (Google Docs/Sheets, small text files). Large binaries (PDF, PNG, ZIP) go
  through the conversation as base64 and are not reliable; send those to the owner with the file card instead and say so.
