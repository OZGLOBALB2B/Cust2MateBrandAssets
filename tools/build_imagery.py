#!/usr/bin/env python3
"""Scan imagery/<group>/* and produce:
  _site/assets/imagery/<group>/<slug>.webp   web-size (max 1800px) versions
  _site/assets/imagery/manifest.json          list the site reads at runtime
  _site/imagery/<group>/<file>                the originals, for download
Title = filename without extension. Group = folder name.
Run locally with:  python3 tools/build_imagery.py
"""
import json, os, re, shutil, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "imagery")
SITE = os.path.join(ROOT, "_site")
MAXW = 1800
EXT = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def build():
    items = []
    for group in sorted(os.listdir(SRC)):
        gdir = os.path.join(SRC, group)
        if not os.path.isdir(gdir) or group.startswith("."): continue
        out = os.path.join(SITE, "assets", "imagery", group); os.makedirs(out, exist_ok=True)
        odir = os.path.join(SITE, "imagery", group); os.makedirs(odir, exist_ok=True)
        for f in sorted(os.listdir(gdir), key=str.lower):
            name, ext = os.path.splitext(f)
            if f.startswith("."): continue
            if ext.lower() == ".svg":  # vector: copy as-is, serve directly
                web = f"{slug(name)}.svg"
                shutil.copy2(os.path.join(gdir, f), os.path.join(out, web))
                shutil.copy2(os.path.join(gdir, f), os.path.join(odir, f))
                items.append(dict(group=group, title=name, src=f"assets/imagery/{group}/{web}", original=f"imagery/{group}/{f}", vector=True))
                print(f"  {group}/{f} -> {web} (svg)"); continue
            if ext.lower() not in EXT: continue
            im = Image.open(os.path.join(gdir, f))
            alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
            im = im.convert("RGBA" if alpha else "RGB")
            im.thumbnail((MAXW, MAXW), Image.LANCZOS)
            web = f"{slug(name)}.webp"
            im.save(os.path.join(out, web), "WEBP", quality=84, method=6)
            shutil.copy2(os.path.join(gdir, f), os.path.join(odir, f))
            items.append(dict(group=group, title=name, src=f"assets/imagery/{group}/{web}",
                              original=f"imagery/{group}/{f}", w=im.width, h=im.height))
            print(f"  {group}/{f} -> {web} ({im.width}x{im.height})")
    os.makedirs(os.path.join(SITE, "assets", "imagery"), exist_ok=True)
    json.dump(items, open(os.path.join(SITE, "assets", "imagery", "manifest.json"), "w"), indent=1)
    print(f"{len(items)} images -> manifest.json")

def copy_site():
    for f in ("index.html", "CNAME"):
        p = os.path.join(ROOT, f)
        if os.path.exists(p): shutil.copy2(p, SITE)
    a = os.path.join(ROOT, "assets")
    if os.path.isdir(a): shutil.copytree(a, os.path.join(SITE, "assets"), dirs_exist_ok=True)

if __name__ == "__main__":
    if os.path.isdir(SITE): shutil.rmtree(SITE)
    os.makedirs(SITE)
    copy_site(); build()
