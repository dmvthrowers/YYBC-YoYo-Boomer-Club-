#!/usr/bin/env python3
"""Static checks for the site. Exit 1 on any failure. Run: python3 scripts/check.py"""
import glob
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://dmvthrowers.club/YYBC-YoYo-Boomer-Club-/"
errs = []


def err(fn, msg):
    errs.append(f"{fn}: {msg}")


pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
src = {fn: open(os.path.join(ROOT, fn), encoding="utf-8").read() for fn in pages}
ids = {fn: set(re.findall(r'\bid="([^"]+)"', s)) for fn, s in src.items()}
navs = {}

for fn, s in src.items():
    live = fn != "404.html"
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    if not t:
        err(fn, "missing <title>")
    elif len(html.unescape(t.group(1))) > 65:
        err(fn, "title over 65 chars")
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    if live and not d:
        err(fn, "missing meta description")
    elif d and len(html.unescape(d.group(1))) > 170:
        err(fn, "description over 170 chars")
    if live:
        want = BASE if fn == "index.html" else BASE + fn
        m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not m or m.group(1) != want:
            err(fn, f"canonical should be {want}")
        if 'property="og:image:alt"' not in s:
            err(fn, "missing og:image:alt")
    if "Content-Security-Policy" not in s:
        err(fn, "missing CSP meta")
    if '<html lang="en">' not in s:
        err(fn, "missing html lang")
    if s.count("<h1") != 1:
        err(fn, f"expected one h1, found {s.count('<h1')}")
    for img in re.findall(r"<img\b[^>]*>", s):
        if not re.search(r'\balt="', img):
            err(fn, f"img without alt: {img[:60]}")
    if re.search(r"<script(?![^>]*ld\+json)", s) or re.search(r'\sstyle="|<style', s):
        err(fn, "inline script or style (blocked by CSP)")
    for fr in re.findall(r"<iframe\b[^>]*>", s):
        if fn != "watch.html" or 'src="https://www.youtube-nocookie.com/embed/' not in fr or "title=" not in fr:
            err(fn, f"unexpected iframe: {fr[:70]}")
    if re.search(r'\son\w+="', s):
        err(fn, "inline event handler")
    for blk in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
        try:
            json.loads(blk)
        except ValueError as ex:
            err(fn, f"bad JSON-LD: {ex}")
    nav = re.search(r'<nav class="nav".*?</nav>', s, re.S)
    if nav:
        navs[fn] = re.sub(r' aria-current="page"', "", nav.group(0))
    for href in re.findall(r'<a [^>]*href="([^"]*)"', s):
        if re.match(r"(https?:|mailto:|tel:)", href):
            continue
        if href.startswith("/") and fn != "404.html":
            err(fn, f"absolute internal link {href}")
        target, _, frag = href.partition("#")
        tgt = fn if not target else target.lstrip("/").replace("YYBC-YoYo-Boomer-Club-/", "") or "index.html"
        if not os.path.exists(os.path.join(ROOT, tgt)):
            err(fn, f"broken link {href}")
        elif frag and tgt.endswith(".html") and frag not in ids.get(tgt, set()):
            err(fn, f"missing anchor {href}")

if len(set(navs.values())) > 1:
    err("nav", "navigation differs between pages")

for fn in pages:
    if fn == "404.html":
        continue
    loc = BASE if fn == "index.html" else BASE + fn
    smap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    if f"<loc>{loc}</loc>" not in smap:
        err("sitemap.xml", f"missing {fn}")
try:
    ET.parse(os.path.join(ROOT, "sitemap.xml"))
except ET.ParseError as ex:
    err("sitemap.xml", str(ex))

css = open(os.path.join(ROOT, "assets/css/main.css"), encoding="utf-8").read()
if any(v.strip() != "none" for v in re.findall(r"box-shadow\s*:([^;}]*)", css)) or \
        any(v.strip() not in ("0", "0 !important") for v in re.findall(r"border-radius\s*:([^;}]*)", css)):
    err("main.css", "shadow or rounded corner")

if errs:
    print("\n".join(errs))
    sys.exit(1)
print(f"ok: {len(pages)} pages")
