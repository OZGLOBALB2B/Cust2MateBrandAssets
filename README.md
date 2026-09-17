# Cust2Mate — Brand Guidelines site

Static site. `index.html` + `assets/` is everything; no build step.

## Deploy (GitHub Pages)
Settings → Pages → Source: **GitHub Actions**. Every push to `main` publishes via `.github/workflows/pages.yml`.

## Editing
- **Imagery download link** — the "Download all Images" button in `index.html` points to the Google Drive folder; search for `drive.google.com` to change it.
- **Bento images** — the 9 representative images live in `assets/imagery/`. To swap one, replace the file (same name) or edit the `bento` list in `brand.json` and rebuild with the brand-guidelines-site skill.
- **Content** — `brand.json` is the source of truth for all copy, colors, type scale and usage rules.
