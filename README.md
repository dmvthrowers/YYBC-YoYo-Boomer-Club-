# YYBC-YoYo-Boomer-Club-
A club of folks that lived through a yoyo boom

## Site

Static HTML/CSS, no build step. Deployed to GitHub Pages by `.github/workflows/pages.yml` on every push to `main`.

- Live: https://dmvthrowers.club/YYBC-YoYo-Boomer-Club-/
- One-time setup: **Settings → Pages → Source: GitHub Actions**
- Preview locally: `python3 -m http.server` then open http://localhost:8000

Design: black and white, heavy system type, sharp corners, no shadows, no external fonts.

## Editing

Most pages are generated. `index.html` and `404.html` are edited by hand.

```
python3 scripts/build_pages.py   # writes the generated pages
python3 scripts/enhance.py       # head tags, JSON-LD, nav state, footer, sitemap.xml
python3 scripts/check.py         # links, anchors, alt text, canonicals, CSP, nav
```

Pull requests run the same checks. The site sets a strict Content-Security-Policy
(no scripts, no inline styles, same-origin only), so keep it that way.

Add `Sitemap: https://dmvthrowers.club/YYBC-YoYo-Boomer-Club-/sitemap.xml` to the
root `robots.txt` of the main site. Crawlers ignore a `robots.txt` in a sub-path.
