# Cust2Mate — Brand Guidelines site

Static brand portal. Deployed to GitHub Pages by the workflow in `.github/workflows/pages.yml`.

## Adding or replacing imagery
1. Drop the image (PNG / JPG / WebP, any size) into the matching folder under `imagery/`:
   - `illustrations/` — product + gradient-arrow illustrations
   - `screens/` — cart-display UI shots
   - `composites/` — photography composites
   - `backgrounds/` — store environment renders
   - `elements/` — white-out product cut-outs (transparent PNG)
2. Name the file the way you want it captioned — `Aisle - low angle.jpg` shows as **Aisle - low angle**.
3. Commit and push to `main`. The workflow converts everything to 1800px WebP, writes
   `assets/imagery/manifest.json`, keeps the originals under `imagery/` for download, and publishes.

To add a new gallery, create a new folder under `imagery/` and add its title in
`index.html` → `BRAND.imagery.groups`. Unknown folders still show, titled by folder name.

## Local preview
```
pip install pillow
python3 tools/build_imagery.py
python3 -m http.server -d _site 8000
```

## One-time setup
Repository → Settings → Pages → Source: **GitHub Actions**.
