#!/usr/bin/env python3
"""Post-process every root HTML page: rebuild <head>, nav state, logo, footer; regenerate sitemap.xml.

Run after build_pages.py:  python3 scripts/build_pages.py && python3 scripts/enhance.py
Idempotent. Reads title/description from each page's existing <head>.
"""
import datetime
import glob
import html
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://dmvthrowers.club/YYBC-YoYo-Boomer-Club-/"
NAME = "YoYo Boomer Club"
OG_ALT = "YoYo Boomer Club. Boomer is a state of mind."
CSP = ("default-src 'self'; script-src 'none'; style-src 'self'; img-src 'self' data:; "
       "font-src 'self'; base-uri 'self'; form-action 'none'; object-src 'none'")
EVENT_PAGES = {"faf-2024.html", "mrm-2024.html", "2a-pril-2024.html", "5a-may-2024.html",
               "one-july-2024.html", "faf-2026.html", "mrm-2026.html"}

FOOTER = """  <footer class="site-footer">
    <div class="wrap">
      <p>Peace, Love, and Chicken Grease.</p>
      <p><a href="https://forums.yoyoexpert.com/t/yoyo-boomers-club/381535">YYE thread</a> · <a href="https://www.youtube.com/@YoYoBoomerClub">YouTube</a> · <a href="https://www.instagram.com/boomeryoyoclub">Instagram</a> · <a href="https://linktr.ee/yoyoboomerclub">Linktree</a> · <a href="mailto:yoyoboomerclub@gmail.com">yoyoboomerclub@gmail.com</a></p>
      <p><a href="projects.html">Projects</a> · <a href="history.html">History</a> · <a href="art.html">Art</a> · <a href="faq.html">FAQ</a> · <a href="privacy.html">Privacy</a></p>
    </div>
  </footer>"""


def a(s):
    return html.escape(s, quote=True)


def ld(obj, ident):
    return f'  <script type="application/ld+json" id="{ident}">{json.dumps(obj, ensure_ascii=False)}</script>'


def meta_content(src, attr, key):
    m = re.search(r'<meta %s="%s" content="([^"]*)"' % (attr, re.escape(key)), src)
    return html.unescape(m.group(1)) if m else None


def build_head(fn, src):
    is404 = fn == "404.html"
    title = html.unescape(re.search(r"<title>(.*?)</title>", src, re.S).group(1))
    desc = meta_content(src, "name", "description")
    og_title = meta_content(src, "property", "og:title") or title
    og_desc = meta_content(src, "property", "og:description") or desc
    url = BASE if fn == "index.html" else BASE + fn
    pre = "/YYBC-YoYo-Boomer-Club-/" if is404 else ""
    img = BASE + "assets/images/og.png"
    csp = CSP + "; frame-src https://www.youtube-nocookie.com" if fn == "watch.html" else CSP
    L = ['  <meta charset="utf-8">',
         '  <meta name="viewport" content="width=device-width, initial-scale=1">',
         f'  <meta http-equiv="Content-Security-Policy" content="{a(csp)}">',
         f"  <title>{a(title)}</title>"]
    if desc:
        L.append(f'  <meta name="description" content="{a(desc)}">')
    L += [f'  <meta name="robots" content="{"noindex" if is404 else "index, follow"}">',
          f'  <meta name="author" content="{NAME}">',
          '  <meta name="theme-color" content="#111111">']
    if not is404:
        L.append(f'  <link rel="canonical" href="{url}">')
        L += ['  <meta property="og:type" content="website">',
              f'  <meta property="og:site_name" content="{NAME}">',
              '  <meta property="og:locale" content="en_US">',
              f'  <meta property="og:title" content="{a(og_title)}">',
              f'  <meta property="og:description" content="{a(og_desc)}">',
              f'  <meta property="og:url" content="{url}">',
              f'  <meta property="og:image" content="{img}">',
              '  <meta property="og:image:width" content="1200">',
              '  <meta property="og:image:height" content="630">',
              f'  <meta property="og:image:alt" content="{a(OG_ALT)}">',
              '  <meta name="twitter:card" content="summary_large_image">',
              f'  <meta name="twitter:title" content="{a(og_title)}">',
              f'  <meta name="twitter:description" content="{a(og_desc)}">',
              f'  <meta name="twitter:image" content="{img}">',
              f'  <meta name="twitter:image:alt" content="{a(OG_ALT)}">']
    L += [f'  <link rel="icon" type="image/png" sizes="32x32" href="{pre}assets/images/favicon-32.png">',
          f'  <link rel="icon" type="image/png" sizes="16x16" href="{pre}assets/images/favicon-16.png">',
          f'  <link rel="apple-touch-icon" href="{pre}assets/images/apple-touch-icon.png">',
          f'  <link rel="manifest" href="{pre}assets/site.webmanifest">']
    if not is404:
        for f in ("alfa-slab-one", "special-elite"):
            L.append(f'  <link rel="preload" href="assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>')
    L.append(f'  <link rel="stylesheet" href="{pre}assets/css/main.css">')
    if fn == "index.html":
        L.append(ld({"@context": "https://schema.org", "@graph": [
            {"@type": "Organization", "@id": BASE + "#org", "name": NAME, "alternateName": "YYBC",
             "url": BASE, "logo": BASE + "assets/images/icon-512.png",
             "foundingDate": "2023-07-31", "email": "yoyoboomerclub@gmail.com",
             "description": "A free online yo-yo club that started on the YoYoExpert forum.",
             "sameAs": ["https://forums.yoyoexpert.com/t/yoyo-boomers-club/381535",
                        "https://www.youtube.com/@YoYoBoomerClub",
                        "https://www.instagram.com/boomeryoyoclub",
                        "https://linktr.ee/yoyoboomerclub"]},
            {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": NAME,
             "publisher": {"@id": BASE + "#org"}}]}, "ld-site"))
    elif not is404:
        short = title.split(" | ")[0]
        L.append(ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": short, "item": url}]}, "ld-breadcrumb"))
    return "<head>\n" + "\n".join(L) + "\n</head>"


def current_href(fn):
    if fn in EVENT_PAGES:
        return "events.html"
    return fn


def process(fn):
    path = os.path.join(ROOT, fn)
    src = open(path, encoding="utf-8").read()
    out = re.sub(r"<head>.*?</head>", lambda m: build_head(fn, src), src, count=1, flags=re.S)
    # nav: aria-current on the matching item (index anchors are never "current")
    out = re.sub(r' aria-current="page"', "", out)
    cur = current_href(fn)
    if fn != "index.html":
        out = out.replace(f'<li><a href="{cur}">', f'<li><a href="{cur}" aria-current="page">')
    out = out.replace('<main id="main">', '<main id="main" tabindex="-1">')
    # logo: WebP with PNG fallback
    out = re.sub(r'<picture>.*?</picture>', '<img src="assets/images/yybc-logo.png" alt="Yo-Yo Boomer Club" width="800" height="300">', out, flags=re.S)
    out = out.replace('<img src="assets/images/yybc-logo.png" alt="Yo-Yo Boomer Club" width="800" height="300">',
                      '<picture><source srcset="assets/images/yybc-logo.webp" type="image/webp">'
                      '<img src="assets/images/yybc-logo.png" alt="Yo-Yo Boomer Club" width="800" height="300"></picture>')
    if fn != "404.html":
        out = re.sub(r'  <footer class="site-footer">.*?</footer>', lambda m: FOOTER, out, flags=re.S)
    if out != src:
        open(path, "w", encoding="utf-8").write(out)


def lastmod(fn):
    try:
        d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", fn], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    except OSError:
        d = ""
    return d or datetime.date.today().isoformat()


def sitemap(pages):
    prio = {"index.html": ("weekly", "1.0"), "yovember.html": ("weekly", "0.9"),
            "events.html": ("monthly", "0.8"), "watch.html": ("monthly", "0.7"), "fundraisers.html": ("monthly", "0.8"),
            "workhorse.html": ("monthly", "0.7"), "projects.html": ("monthly", "0.7"), "sponsors.html": ("monthly", "0.7"),
            "charter.html": ("yearly", "0.6"), "art.html": ("yearly", "0.5"), "history.html": ("monthly", "0.6"), "faq.html": ("monthly", "0.6"), "privacy.html": ("yearly", "0.3")}
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for fn in pages:
        cf, pr = prio.get(fn, ("yearly", "0.5"))
        loc = BASE if fn == "index.html" else BASE + fn
        rows.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod(fn)}</lastmod>\n"
                    f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>")
    rows.append("</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(rows))


def main():
    pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
    for fn in pages:
        process(fn)
    order = ["index.html", "events.html", "watch.html", "fundraisers.html", "workhorse.html", "sponsors.html",
             "yovember.html", "projects.html", "charter.html", "history.html", "art.html", "faq.html", "privacy.html"]
    rest = [p for p in pages if p not in order and p != "404.html"]
    sitemap([p for p in order if p in pages] + rest)
    print(f"enhanced {len(pages)} pages")


if __name__ == "__main__":
    main()
