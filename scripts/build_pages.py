#!/usr/bin/env python3
"""Generates the YYBC archive pages (events, fundraisers, Workhorse, sponsors, Yovember, FAQ, privacy)
into the repo root. Facts come from the YYE forum threads and the club's own reference docs.

Usage:  python3 scripts/build_pages.py   then   python3 scripts/enhance.py
index.html and 404.html are edited by hand; enhance.py keeps every page's head, nav state
and footer consistent."""
import html, json, sys, pathlib

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
SITE = "https://dmvthrowers.club/YYBC-YoYo-Boomer-Club-/"
YYE = "https://forums.yoyoexpert.com/t/"
e = html.escape

NAV = """<li><a href="index.html#about">ABOUT</a></li>
          <li><a href="events.html">EVENTS</a></li>
          <li><a href="fundraisers.html">FUNDRAISERS</a></li>
          <li><a href="workhorse.html">WORKHORSE</a></li>
          <li><a href="sponsors.html">SPONSORS</a></li>
          <li><a href="charter.html">CHARTER</a></li>
          <li><a href="index.html#join">JOIN</a></li>"""

def page(fname, title, desc, body):
    doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} | YYBC</title>
  <meta name="description" content="{e(desc)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)} | YoYo Boomer Club">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{SITE}assets/images/og.png">
  <meta property="og:url" content="{SITE}{fname}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="assets/images/favicon.png">
  <link rel="stylesheet" href="assets/css/main.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="index.html"><img src="assets/images/yybc-logo.png" alt="Yo-Yo Boomer Club" width="800" height="300"></a>
      <nav class="nav" aria-label="Main">
        <ul>
          {NAV}
        </ul>
      </nav>
    </div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <p>Peace, Love, and Chicken Grease.</p>
      <p><a href="https://forums.yoyoexpert.com/t/yoyo-boomers-club/381535">YYE thread</a> · <a href="https://www.youtube.com/@YoYoBoomerClub">YouTube</a> · <a href="https://www.instagram.com/boomeryoyoclub">Instagram</a> · <a href="https://linktr.ee/yoyoboomerclub">Linktree</a> · <a href="mailto:yoyoboomerclub@gmail.com">yoyoboomerclub@gmail.com</a></p>
    </div>
  </footer>
</body>
</html>
"""
    (OUT / fname).write_text(doc)


def ld(obj):
    return '    <script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

def head(kicker, h1, lede):
    return f"""    <div class="page-head">
      <div class="wrap">
        <span class="tag stamp">{e(kicker)}</span>
        <h1>{e(h1)}</h1>
        <p>{lede}</p>
      </div>
    </div>"""

def ext(url, text):
    return f'<a href="{e(url)}">{e(text)}</a>'

def thread(slug, text="Read the thread on YoYoExpert"):
    return ext(YYE + slug, text)

def section(h2, inner, sid=""):
    i = f' id="{sid}"' if sid else ""
    return f"""    <section{i}>
      <div class="wrap">
        <h2>{e(h2)}</h2>
{inner}
      </div>
    </section>"""

def cards(items):
    out = ['        <div class="grid">']
    for era, h3, p in items:
        out.append(f'          <article class="card">\n            <p class="era">{e(era)}</p>\n            <h3>{e(h3)}</h3>\n            <p>{p}</p>\n          </article>')
    out.append("        </div>")
    return "\n".join(out)

def checklist(lines):
    return '        <ul class="checklist">\n' + "\n".join(f"          <li>{l}</li>" for l in lines) + "\n        </ul>"

def ladder(tricks):
    """tricks: list of (name, who or None, url or None)"""
    rows = []
    for name, who, url in tricks:
        n = ext(url, name) if url else e(name)
        w = f" <span class='by'>{e(who)}</span>" if who else ""
        rows.append(f"          <li>{n}{w}</li>")
    return '        <ol class="ladder">\n' + "\n".join(rows) + "\n        </ol>"


def fig(src, alt, caption, w, h, cls=""):
    c = f' class="pic {cls}"' if cls else ' class="pic"'
    return f'        <figure{c}><img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy"><figcaption>{caption}</figcaption></figure>'

def pics(figs):
    return '        <div class="pics">\n' + "\n".join(figs) + "\n        </div>"

def logo_wall(items):
    out = ['        <ul class="logos">']
    for href, src, alt, w, h in items:
        out.append(f'          <li><a href="{e(href)}"><img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy"></a></li>')
    out.append("        </ul>")
    return "\n".join(out)

def more_links(links):
    return '        <p class="links">' + " · ".join(links) + "</p>"

BACK = '        <p class="links"><a href="events.html">&larr; All events</a></p>'

# ---------------------------------------------------------------- FAF 2024
faf24_weeks = [
    ("Week 1", "Feb 1, 2024", [("Trapeze Stall", None, None), ("Undermount Stall", None, None), ("Brother Stall", None, None), ("Lunar Stall", None, None)], "Jerrod Chitwood: Mysto Set", "fixed-axle-february-2024-week-1/393429"),
    ("Week 2", "Feb 8, 2024", [("Zipper Stalls", None, None), ("Makin' Da Zines", None, None), ("Double or Nothing Stall", None, None), ("Bucket Stall", None, None)], "Ed Haponik: Interrupted Breakaway Finger Flip", "fixed-axle-february-2024-week-2/393968"),
    ("Week 3", "Feb 15, 2024", [("Dumptrucks", None, None), ("Kickflip", None, None), ("Backhand Balance to Lunar Landing", None, None), ("Stop'n'Go", None, None)], "Nate Marstoff", "fixed-axle-february-2024-week-3/394507"),
    ("Week 4", "Feb 22, 2024", [("Windshield Wipers 2", None, None), ("Reverse Stall", None, None), ("Double or Nothing Chopsticks Stall", None, None), ("Varial", None, None)], "DocPop", "fixed-axle-february-2024-week-4/395040"),
]
inner = ['        <div class="grid">']
for wk, date, tricks, guest, slug in faf24_weeks:
    li = "".join(f"<li>{e(t[0])}</li>" for t in tricks)
    inner.append(f'          <article class="card">\n            <p class="era">{e(wk)} · {e(date)}</p>\n            <ol class="mini">{li}</ol>\n            <p><b>Guest trick:</b> {e(guest)}</p>\n            <p>{thread(slug, "Week thread")}</p>\n          </article>')
inner.append("        </div>")
faf24 = head("February 2024 · Our first event", "Fixed Axle February 2024",
    "The club's first big event. Four weeks, four tricks a week, one celebrity guest trick each week, all on a fixed axle.") + "\n" + \
    section("The Art", pics([
        fig("assets/images/events/faf-2024-butterfly.png", "Fixed Axle February 2024 logo: a butterfly drawn as a fixed axle yo-yo, wings outlined in black, with YYBC and 2024 on its body.", "The 2024 event logo.", 720, 720),
        fig("assets/images/events/faf-2024-banner.jpg", "Fixed Axle February banner: a station wagon in white line art on black, with the words Fixed Axle February, presented by the Yo-Yo Boomers Club.", "The station wagon banner.", 690, 388),
    ])) + "\n" + \
    section("How it worked", checklist([
        "Four tricks a week, posted to the YoYoExpert thread.",
        "Complete one trick, get one entry in that week's drawing. Complete all four, get one more entry.",
        "Each week's guest trick had its own prize drawing.",
        "Videos were due by 12:01 AM Pacific every Thursday, and you could only win one prize all event.",
        "Every video started with the sponsor page.",
    ])) + "\n" + section("The trick lists", "\n".join(inner)) + "\n" + \
    section("Where it lives", "        <p>The weekly threads have the tutorial videos and every entry.</p>\n" + more_links([thread("fixed-axle-february-2024-week-1/393429", "Week 1"), thread("fixed-axle-february-2024-week-2/393968", "Week 2"), thread("fixed-axle-february-2024-week-3/394507", "Week 3"), thread("fixed-axle-february-2024-week-4/395040", "Week 4")]) + "\n" + BACK)

# ---------------------------------------------------------------- MRM 2024
mrm24 = head("March 2024", "Modern Responsive March 2024",
    "Same four-week Trick-a-Week format, this time on modern responsive yo-yos.") + "\n" + \
    section("How it worked", checklist([
        "Four tricks a week and a celebrity guest trick, same as Fixed Axle February.",
        "Same rules: post your video in the thread, sponsor page up front, one prize per person.",
        "Part of why the club exists is to pin down what \"modern responsive\" even means. This was the excuse to test it.",
    ])) + "\n" + \
    section("Where it lives", "        <p>Each week has its own thread with the tricks and tutorials.</p>\n" + more_links([thread("modern-responsive-march-2024-week-1/395527", "Week 1"), thread("modern-responsive-march-2024-week-2/396012", "Week 2"), thread("modern-responsive-march-2024-week-3/396581", "Week 3"), thread("modern-responsive-march-2024-week-4/397107", "Week 4")]) + "\n" + BACK)

# ---------------------------------------------------------------- 2A-pril 2024
a24 = head("April 2024", "2A-pril 2024",
    "A looping event. Three weeks of two-hand tricks, with guest tricks from some of the best loopers around.") + "\n" + \
    section("How it worked", checklist([
        "Start with the sponsor banner. Post the video link in the YoYoExpert thread.",
        "Every trick you finish is one entry. List the tricks in your post or your video description.",
        "Parents could submit their kids' videos under their own username.",
        "Kickoff was April 8. The event closed April 29, 11:59 PM left-coast time, and winners were drawn May 1.",
    ])) + "\n" + \
    section("Guest tricks", checklist([
        "Luke Renner: Riding the Horse, Async Planet Hops, Lunar Tower Stall",
        "Ross Levine: On the Floor, Vertical Hop the Fence",
        "Josh Yee: Butterfly Wrap Exit",
        "Vitalliispinstar and Dazzling Dave: how to Two Hand Loop, for the beginners",
    ])) + "\n" + \
    section("Where it lives", "        <p>All three weeks of tricks live in one thread.</p>\n" + more_links([thread("2april-2024-a-looping-event/398341", "The 2A-pril thread")]) + "\n" + BACK)

# ---------------------------------------------------------------- 5A May 2024
fam = [
    ("Week 1", "Kickoff May 1", ["360", "Windmill", "Basic Stall"], "5A Essentials: 1 Trick = 4 Results", "5amay-2024-week-1/399869"),
    ("Week 2", "", ["Double or Nothing", "Aerial 360", "Spirals"], "Gerbil Wheel", "5amay-2024-week-2/400494"),
    ("Week 3", "", ["Butterfly", "Electric Fan", "Bee Sting"], "Stance Switch", "5amay-2024-week-3/400977"),
    ("Week 4", "", ["Shoulder Pop", "360 Green Triangle", "Tangler", "Nunchucks"], "Meltdown", "5a-may-2024-week-4/401674"),
]
inner = ['        <div class="grid">']
for wk, date, tricks, taw, slug in fam:
    li = "".join(f"<li>{e(t)}</li>" for t in tricks)
    inner.append(f'          <article class="card">\n            <p class="era">{e(wk)}{(" · " + e(date)) if date else ""}</p>\n            <p><b>Beginner ladder</b></p>\n            <ol class="mini">{li}</ol>\n            <p><b>Trick of the week:</b> {e(taw)}</p>\n            <p>{thread(slug, "Week thread")}</p>\n          </article>')
inner.append("        </div>")
may24 = head("May 2024", "5A May 2024",
    "Counterweight month. A beginner ladder, a trick of the week, and a freeform round, run with Josh Yee and Mable.") + "\n" + \
    section("Three ways to play", checklist([
        "Beginner Trick Ladder: three or four beginner tricks a week. One trick is one entry, finishing the whole week is one more.",
        "Trick-a-Week: post the week's trick, get an entry.",
        "FreeForm: post up to two minutes of freestyle, a tutorial, or a production. One entry.",
        "Weekly deadlines were Tuesday at 11:59 PM Pacific. The event closed May 31.",
    ])) + "\n" + section("The trick lists", "\n".join(inner)) + "\n" + \
    section("Where it lives", more_links([thread("5amay-2024-week-1/399869", "Week 1"), thread("5amay-2024-week-2/400494", "Week 2"), thread("5amay-2024-week-3/400977", "Week 3"), thread("5a-may-2024-week-4/401674", "Week 4")]) + "\n" + BACK)

# ---------------------------------------------------------------- ONE July 2024
july = head("July 2024", "ONE July 2024",
    "Pick one yo-yo. Throw it all month. Find out if you regret your decisions (spelling on purpose).") + "\n" + \
    section("The rules", checklist([
        "Choose one yo-yo and share it in the thread. (My preciousssss.)",
        "A pair for 2A or 3A counts as one.",
        "If you smash it, you can swap to a backup. Post photos of the damage.",
        "Weekly questions started July 1. There was no prize. The pain was the prize.",
    ])) + "\n" + \
    section("Where it lives", more_links([thread("get-ready-for-one-july-2024/403962", "The ONE July thread")]) + "\n" + BACK)

# ---------------------------------------------------------------- FAF 2026
faf26_tricks = [
    ("Kickflip", "Xanadu", "https://youtu.be/GzsQPunt3e0"),
    ("Makin Da Zines (3 reps)", "GnarlyCharlie", "https://youtu.be/ukNmPM50ZVI"),
    ("Backhand Balance to Lunar", "GnarlyCharlie", "https://youtu.be/QAmUg3g9LoU"),
    ("Shoot the Moon to Lunar", "bheinz63", "https://youtu.be/CeaniycOLf0"),
    ("UFO Recapture", "TryCatchThrow", "https://youtu.be/dWxszMQCoMU"),
    ("Zipper Stalls", "Ardeus", "https://youtu.be/kPtNENmtqAA"),
    ("Varial", "Xanadu", "https://youtu.be/hXj2giRlGZo"),
]
faf26 = head("February 2026", "Fixed Axle February 2026",
    "Back to basics. One trick ladder for the whole month, no weekly deadlines, no stress. Straight-up blue box Kraft.") + "\n" + \
    section("Thank You, Sponsors", pics([
        fig("assets/images/events/faf-2026-sponsors.jpg", "Fixed Axle February 2026 thank-you banner showing the sponsors Boise Wood Works, Layer Infinity, Return Bottoms and Throw-Yo, with their prizes, and the YoYo Boomer Club logo.", "The Fixed Axle February 2026 sponsor banner.", 1100, 619, "wide"),
    ])) + "\n" + \
    section("How it worked", checklist([
        "Seven tricks, all month. Do them in any order you like.",
        "One video per trick, one video for all of them, or anything in between.",
        "One completed trick is one point, and one point is one raffle entry.",
        "Throw-Yo teased an Eco-Friendly Reusable Juice Box as a prize. Only three exist.",
        "A Discord help channel was open for anybody stuck on a trick.",
    ])) + "\n" + section("The trick list", ladder(faf26_tricks) + "\n        <p>Tricks are presented by club members. Click a trick for the tutorial.</p>") + "\n" + \
    section("Where it lives", "        <p>The thread has every entry. Throw-Yo kicked in the prize.</p>\n" + more_links([thread("fixed-axle-february-2026-presented-by-yybc/440253", "The event thread"), ext("https://throw-yo.com/", "Throw-Yo")]) + "\n" + BACK)

# ---------------------------------------------------------------- MRM 2026
mrm26_tricks = [
    ("Pop the Clutch", None, "https://www.youtube.com/watch?v=9sVcOulMIWA"),
    ("Stop and Go", None, "https://www.youtube.com/watch?v=P6Ac1hKC-IA"),
    ("Ripcord", None, "https://www.youtube.com/watch?v=n1BOtswRudA"),
    ("Zipper (2-3 times)", None, "https://youtu.be/azDoXdPVphc"),
    ("Rewind", None, "https://www.youtube.com/watch?v=h24LR0nd44Y"),
    ("Split the Atom (2-3 rotations)", None, "https://www.youtube.com/watch?v=Y6T-0YtZ8XI"),
    ("Atomic Bomb (2-3 times)", None, "https://www.youtube.com/watch?v=5wT1cwFK4ts"),
    ("Hydrogen Bomb", None, "https://youtu.be/Pq67C2z3nOw"),
    ("Cold Fusion (responsive)", None, "https://www.youtube.com/watch?v=6vW2bMtd17c"),
]
mrm26 = head("March 2026", "Modern Responsive March 2026",
    "The wasteland is quiet. The dust has settled. A month-long, nine-trick, old-school ladder with a Fallout theme and a lot of atomic puns.") + "\n" + \
    section("The setup", checklist([
        "Same relaxed month-long format as Fixed Axle February 2026.",
        "Theme: Fallout. The thread greeted everyone with \"Welcome, fellow dwellers.\"",
        "The trick list was called Radioactive: old-school tricks with names to match.",
        "Prizes came from ZGRT, Sickburn Yo-Yo Workshop / Return Bottoms, and Throw-Yo.",
        "A member built a mobile-friendly trick reference app for the ladder.",
    ])) + "\n" + section("The trick list: Radioactive", ladder(mrm26_tricks) + "\n        <p>Click a trick for the tutorial.</p>") + "\n" + \
    section("Where it lives", more_links([thread("modern-responsive-march-2026-presented-by-yybc/441659", "The event thread"), ext("https://mrm2026.netlify.app", "The trick reference app")]) + "\n" + BACK)

# ---------------------------------------------------------------- Events hub
def entry(date, name, blurb, href, ext_link=False):
    link = ext(href, name) if ext_link else f'<a href="{e(href)}">{e(name)}</a>'
    return (date, link, blurb)

def hub_cards(items):
    out = ['        <div class="grid">']
    for date, link, blurb in items:
        out.append(f'          <article class="card">\n            <p class="era">{e(date)}</p>\n            <h3>{link}</h3>\n            <p>{blurb}</p>\n          </article>')
    out.append("        </div>")
    return "\n".join(out)

y2026 = [
    entry("Starts Nov 1, 2026", "Yovember", "Grow a stash, talk yo-yo, throw tricks, raise money for men's health.", "yovember.html"),
    entry("February 2026", "Fixed Axle February", "Seven tricks, one month, no weekly panic.", "faf-2026.html"),
    entry("March 2026", "Modern Responsive March", "Fallout theme, nine old-school tricks, Radioactive ladder.", "mrm-2026.html"),
]
y2025 = [
    entry("February 2025", "Fixed Axle February", "The final-week thread from the 2025 run.", YYE + "fixed-axle-february-2025-is-here-week-4/418307", True),
    entry("March 2025", "Modern Responsive March", "The 2025 event thread.", YYE + "modern-responsive-march-2025/420805", True),
    entry("April 2025", "The Workhorse drops", "Our club yo-yo with G Squared goes into production.", "workhorse.html"),
]
y2024 = [
    entry("Feb 2024", "Fixed Axle February", "Our first big event. Four weeks, guest tricks, sponsor pages.", "faf-2024.html"),
    entry("Mar 2024", "Modern Responsive March", "Modern responsive yo-yos, same four-week format.", "mrm-2024.html"),
    entry("Apr 2024", "2A-pril", "Two-hand looping, three weeks, guest tricks.", "2a-pril-2024.html"),
    entry("May 2024", "5A May", "Counterweights, a beginner ladder and a freeform round.", "5a-may-2024.html"),
    entry("Jul 2024", "ONE July", "One yo-yo all month. No swapping unless you smash it.", "one-july-2024.html"),
    entry("Nov 2024", "Yovember", "Our Movember team, plus a club-sponsored competition.", "fundraisers.html#yovember"),
    entry("Dec 2024", "Holiday fundraiser", "$1,300 for Toys for Tots.", "fundraisers.html#2024"),
]
y2023 = [
    entry("Jul 31, 2023", "The club starts", "Cody posts the call for charter members. First reply: \u201cSign me up or whatever.\u201d", YYE + "yoyo-boomers-club/381535", True),
    entry("Nov–Dec 2023", "Holiday fundraiser", "$130 for Toys for Tots, 52 yo-yos.", "fundraisers.html#2023"),
]
events = head("The archive", "Events", "What's coming, and every challenge we've run, with the trick lists and the threads, so you can still do them on your own time.") + "\n" + \
    section("2026", hub_cards(y2026), "y2026") + "\n" + section("2025", hub_cards(y2025), "y2025") + "\n" + \
    section("2024", hub_cards(y2024), "y2024") + "\n" + section("2023", hub_cards(y2023), "y2023") + "\n" + \
    section("Want one run again?", '        <p class="lead">The trick lists never expire. Pick a month, grab your yo-yo, and post in the thread when you land one.</p>\n' + more_links([ext("https://addevent.com/calendar/fW654456", "The club calendar"), ext("https://linktr.ee/yoyoboomerclub", "Linktree")]))

# ---------------------------------------------------------------- Fundraisers
fund = head("Fundraisers", "Boomers for Toys for Tots",
    "Every holiday season we team up with Throw-Yo and YoYoExpert and sell stuff so kids get yo-yos. It's now an annual tradition.") + "\n" + \
    section("2023: $130", checklist([
        "A holiday apparel sale from Throw-Yo and YYBC, including a hoodie and a lawnmower shirt.",
        "Every dollar went to YoYoExpert's Toys for Tots drive.",
        "$130 bought 52 yo-yos, donated in five batches.",
    ]) + "\n" + more_links([thread("yo-yo-boomers-club-x-throw-yo-holiday-fundraising-collab-its-over-130-raised/388710", "The 2023 thread")]), "2023") + "\n" + \
    section("2024: $1,300", checklist([
        "Same team: YYBC, Throw-Yo and YoYoExpert.",
        "Four fundraiser items, three holiday SOLUTIONS strings, and $5 from every SOLUTIONS product sold.",
        "The YYBC x G2 Auctions on December 9 took the total to $1,300. Last year's $130, in the dust.",
        "Early on, at $150, the thread called it \"60 yo-yos worth.\"",
    ]) + "\n" + more_links([thread("2024-yo-yo-boomers-club-x-throw-yo-holiday-fundraising-collab/414528", "The 2024 thread")]), "2024") + "\n" + \
    section("Yovember", checklist([
        "Yovember 2026 starts November 1: grow a stash, talk yo-yo, throw tricks, support men's health.",
        "In November 2024 the club ran a Movember team. The club called it a challenge, not a production event, in the spirit of ONE July.",
        "Yo-yo community fundraising for men's health.",
    ]) + "\n" + more_links(['<a href="yovember.html">Yovember 2026</a>', ext("https://us.movember.com/team/2406538", "The 2024 team page")]), "yovember") + "\n" + \
    section("AYYC2: ALL IN", checklist([
        "In November 2024 the club was a Bronze Level Sponsor of AYYC2: ALL IN, the Ante Yoyo Championship.",
        "The club's first confirmed sponsorship of a competition run by somebody else.",
    ]) + "\n" + more_links([ext("https://anteyoyo.com", "Ante Yoyo")]) + "\n" + BACK.replace("All events", "All events"), "ayyc2")

# ---------------------------------------------------------------- Workhorse
specs = [
    ("Style", "0A and 1A"), ("Diameter", "55 mm"), ("Width", "31.85 mm"), ("Weight", "53.3 g"),
    ("Material", "6061 aluminum"), ("Bearing", "Slim D, or a bearing blank (5 mm and 4 mm also supported)"), ("Response", "G2 Respawn pads"),
]
spec_li = "\n".join(f"          <li><b>{e(k)}:</b> {e(v)}</li>" for k, v in specs)
timeline = [
    ("Oct 2023", "Responsive prototype sent off for fabrication."),
    ("Dec 2023", "V1 prototypes land at G Squared HQ."),
    ("Jan 22, 2024", "Prototypes released into the wild for testing."),
    ("Apr 2024", "Unresponsive prototype ordered."),
    ("Jul 2024", "V2 prototype arrives."),
    ("Nov 2024", "Production order placed."),
    ("Apr 2025", "Production release."),
]
tl = "\n".join(f"          <li><b>{e(a)}:</b> {e(b)}</li>" for a, b in timeline)
work = head("G Squared × YYBC", "The Workhorse",
    "A yo-yo built by the club with G Squared. One yo-yo that plays both 0A and 1A, with weights you can tune. Prototype to production, and yes, there's a Space Wagon.") + "\n" + \
    section("The Yo-Yo", pics([
        fig("assets/images/workhorse.webp", "A folding table covered in rows of Workhorse yo-yos in red, black and blue.", "Workhorse yo-yos in the wild. Photo via The Yoyo Archive.", 375, 500),
    ])) + "\n" + \
    section("What it is", """        <p>G Squared's design team wanted one yo-yo that plays two styles well and shows what "modern responsive" can mean. You can run it on a 5 mm or 4 mm bearing, or on a bearing blank for the Post Modern Responsive setup, and add 1 to 10 grams of weight rings to tune it.</p>
        <p>The redistributed weight made the biggest difference between V1 and V2. Same size, different feel.</p>""") + "\n" + \
    section("Specs", f'        <ul class="checklist">\n{spec_li}\n        </ul>\n        <p>Measured specs from the production listing.</p>') + "\n" + \
    section("Colorways", checklist([
        "Founder's Edition: 15 made.",
        "Space Wagon: 35 made, club members only.",
        "Offroad: 14 made, club members only.",
        "Gotham.",
        "Cherry Bomb.",
    ])) + "\n" + \
    section("From prototype to production", f'        <ul class="checklist">\n{tl}\n        </ul>\n' + more_links([ext("https://yoyoarchive.org/products/workhorse", "The Workhorse at The Yoyo Archive"), thread("yoyo-boomers-club-work-horse-prototype-v1-review/401093", "The V1 prototype review")])) + "\n" + \
    section("Get one", '        <p class="lead">Check The Yoyo Archive listing for what is still available. Ask in the club thread if you want to buy, sell, or trade.</p>\n' + more_links([ext("https://forums.yoyoexpert.com/t/yoyo-boomers-club/381535", "The club thread")]))


# ---------------------------------------------------------------- Yovember 2026
yov = head("Starts November 1", "Yovember",
    "Our Movember team, with yo-yos. Grow a stash, talk yo-yo, throw tricks, and raise money for men's health.") + "\n" + \
    section("The deal", checklist([
        "It starts November 1 and runs all month.",
        "Grow a stash.",
        "Talk yo-yo. Tell us what you're throwing and why.",
        "Throw tricks and share them with the club.",
        "Every dollar raised supports men's health, same as past years.",
    ])) + "\n" + \
    section("How to play along", checklist([
        "Say you're in on the club thread, and post your progress there all month.",
        "Follow the club Linktree and calendar for team links and dates.",
        "Like ONE July, this is a challenge, not a production event. Nobody's judging your stash.",
    ]) + "\n" + more_links([thread("yoyo-boomers-club/381535", "The club thread"), ext("https://linktr.ee/yoyoboomerclub", "Linktree"), ext("https://addevent.com/calendar/fW654456", "The club calendar")])) + "\n" + \
    ld({"@context": "https://schema.org", "@type": "Event", "name": "Yovember 2026",
        "description": "The YoYo Boomer Club's November fundraiser: grow a stash, talk yo-yo, throw tricks and support men's health.",
        "startDate": "2026-11-01", "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
        "location": {"@type": "VirtualLocation", "url": "https://forums.yoyoexpert.com/t/yoyo-boomers-club/381535"},
        "organizer": {"@type": "Organization", "name": "YoYo Boomer Club", "url": SITE},
        "isAccessibleForFree": True}) + "\n" + \
    section("Last Time: The 2024 Challenge Board", """        <p class="lead">Set a challenge. Tell the thread. Follow through. The sillier, the better.</p>
        <p>In November 2024 the club ran Yovember all month. Everybody picked their own challenge, and you could attempt other people's too. Some of the board:</p>""" + checklist([
        "Grow a Mo. Mustache only, no beards allowed.",
        "No Shave November. Let your inner caveman show.",
        "One yo-yo for the month. Or one string, if you like the Fragile Wear-Down Challenge.",
        "Shorten your string an inch a day. Or grow it until you can go fishing.",
        "Learn a trick a day. Post a yo-yo meme a day. Tell a dad joke a day.",
        "Play off-hand all month, or front style only.",
        "A head grind a day. The \u201cI Love Ibuprofen Challenge.\u201d",
        "Online YoYo Horse in the thread.",
        "Eat a Twinkie a day. Walk a mile a day. Do both at once.",
        "Light your yo-yo on fire. We warned you not to do this one.",
    ])) + "\n" + \
    section("Last Time: The Rewards", """        <p>Two ways to win in 2024:</p>""" + checklist([
        "<strong>Option 1:</strong> finish your own challenge and walk away with a glorious sense of accomplishment.",
        "<strong>Option 2:</strong> join the YYBC Movember team and raise $20. You earned the chance to buy the G Squared Relic Prototype, engraved for the event, for $50 plus shipping.",
        "Mo Your Own Way counts. No shaving, fitness challenges and more all count toward the team.",
        "Throw-Yo made event merch. Tagged #YovemberMovember, #MoAndThrow and #StillMightTalkAboutLawns.",
    ]) + "\n" + more_links([ext("https://us.movember.com/team/2406538", "The 2024 team page"), '<a href="fundraisers.html">All our fundraisers</a>', '<a href="sponsors.html">Sponsors</a>']) + "\n" + BACK)


# ---------------------------------------------------------------- Sponsors
def sponsor_cards(items):
    out = ['        <div class="grid">']
    for name, url, blurb in items:
        h = ext(url, name) if url else e(name)
        out.append(f'          <article class="card">\n            <h3>{h}</h3>\n            <p>{e(blurb)}</p>\n          </article>')
    out.append("        </div>")
    return "\n".join(out)

club_sponsors = [
    ("G Squared Yoyos", "https://gsquaredyoyos.com", "Our annual club sponsor and the other half of the Workhorse."),
    ("Throw-Yo", "https://throw-yo.com", "Annual club sponsor. Hosts our merch, strings and fundraiser items."),
    ("YoYoExpert", "https://yoyoexpert.com", "Annual club sponsor and home of the club thread."),
]
sponsors_2026 = [
    ("Boise Wood Works", None, "Fixed Axle February 2026."),
    ("Layer Infinity", None, "Fixed Axle February 2026."),
    ("ZGRT", "https://zgrt.ca", "Modern Responsive March 2026."),
    ("Sickburn Yo-Yo Workshop / Return Bottoms", "https://returnbottoms.com", "Fixed Axle February and Modern Responsive March 2026."),
    ("Throw-Yo", "https://throw-yo.com", "Fixed Axle February and Modern Responsive March 2026."),
]
logos_2026 = [
    ("https://zgrt.ca", "assets/images/sponsors/zgrt.png", "ZGRT logo", 560, 259),
    ("https://returnbottoms.com", "assets/images/sponsors/return-bottoms.jpg", "Return Bottoms logo: a peach with a heart-shaped bottom", 640, 387),
    ("https://throw-yo.com", "assets/images/sponsors/throw-yo.jpg", "Throw-Yo logo", 640, 166),
]
past = [
    ("A Round Square", None), ("DMV Throwers", "https://dmvthrowers.club"), ("DocPop", None), ("Ded Hed Designs", "https://dedheddesigns.com"),
    ("Duncan", None), ("Freshly Dirty", None), ("Krom Kendama", None), ("Layer Infinity", None),
    ("LKGlass", None), ("MK1", "https://mk1yoyos.com"), ("NoCity3D", None), ("One Drop", None),
    ("Project44", None), ("Rain City Skills", None), ("Spinworthy", None), ("TimCo", None),
    ("Unprld", None), ("Vosun", None), ("Yoyo King", None), ("Yoyo String Lab", None), ("Zipline", None),
]
past_li = [ (ext(u, n) if u else e(n)) for n, u in past ]
spons = head("Thank you", "Sponsors",
    "These folks put real yo-yos, strings and money behind a club that started as a joke on a forum. Go buy their stuff.") + "\n" + \
    section("Club sponsors", sponsor_cards(club_sponsors) + "\n        <p>Annual sponsors who back everything we do.</p>", "club") + "\n" + \
    section("This year: 2026", logo_wall(logos_2026) + "\n" + sponsor_cards(sponsors_2026), "now") + "\n" + \
    section("Past event sponsors and donors", "        <p>Prizes, strings and counterweights donated to our earlier events.</p>\n" + checklist(past_li) + "\n        <p>Plus the club members who donated 3D-printed counterweights and other prizes of their own. You know who you are.</p>", "past") + "\n" + \
    section("Sponsor the club", """        <p class="lead">Every prize in a drawing was a company saying yes to a very silly idea.</p>
        <ul class="checklist">
          <li><b>Event Donor</b> (a product under $100): a mention in the thread and the event video credits.</li>
          <li><b>Event Sponsor</b> ($100 or more in product or funds): your logo on the event video banners, a thread and social post, and a Linktree link for the event. Ideally you ship prizes straight to the winners.</li>
          <li><b>Club Sponsor</b> (an annual commitment of $500 or more): your logo on every banner all year, a year-round Linktree spot, and social posts.</li>
        </ul>
        <p>Say hi at <a href="mailto:yoyoboomerclub@gmail.com">yoyoboomerclub@gmail.com</a>.</p>""")


# ---------------------------------------------------------------- FAQ
faq_items = [
    ("Do I have to be old to be a Yoyo Boomer?", "No. Boomer is a state of mind, not an age. Claim the title and you're a Boomer."),
    ("What does it cost?", "Nothing. No dues, no age check, no tryouts."),
    ("How do I join?", "Post in the club thread on the YoYoExpert forums and say you're in. We'll say welcome to the club."),
    ("Where does the club meet?", "Online. The club thread on the YoYoExpert forums is home base. We also use Discord for chat, YouTube for event videos and Instagram for photos. The Linktree has all the links."),
    ("What is Yovember?", "Our November fundraiser. It starts November 1: grow a stash, talk yo-yo, throw tricks and support men's health."),
    ("Can I do the old challenges?", "Yes. The events archive has the trick lists for every challenge we've run. Do them whenever you like and post in the thread."),
    ("Where does the money go?", "Our holiday fundraiser supports YoYoExpert's Toys for Tots drive, and Yovember supports men's health. Money from club pins and stickers goes back into the club."),
    ("Is there a club yo-yo?", "Yes, the Workhorse, built with G Squared Yoyos. It plays both 0A and 1A."),
    ("How do I sponsor the club?", "Email yoyoboomerclub@gmail.com. The sponsors page has the options."),
    ("Is this the same as DMV Throwers?", "No. DMV Throwers is a separate, free, in-person yo-yo club in DC, Maryland and Virginia. Some Boomers are also Throwers."),
]
faq_html = "\n".join(f'        <h3>{e(q)}</h3>\n        <p>{e(a)}</p>' for q, a in faq_items)
faq_ld = ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_items]})
faq = head("Questions", "FAQ", "Short answers to the things people ask before they claim the title.") + "\n" + \
    section("The short answers", faq_html + '\n        <p class="links"><a href="events.html">Events</a> · <a href="fundraisers.html">Fundraisers</a> · <a href="workhorse.html">The Workhorse</a> · <a href="sponsors.html">Sponsors</a></p>') + "\n" + faq_ld

# ---------------------------------------------------------------- Privacy
privacy = head("Effective October 2026", "Privacy", "This site doesn't collect anything about you. Here is the short version, and the details.") + "\n" + \
    section("What we collect", checklist([
        "Nothing. The site has no forms, no accounts, no comments and no sign-ups.",
        "No cookies, no analytics and no ad trackers. The site runs no scripts at all.",
        "Fonts and images load from this site, not from a third party.",
    ])) + "\n" + \
    section("Who else sees your visit", "        <p>The site is hosted on GitHub Pages, and GitHub may keep ordinary server logs of visits under its own privacy policy. Links on this site go to other places like YouTube, Instagram, YoYoExpert, Linktree and Throw-Yo. Once you click through, their policies apply, not ours.</p>") + "\n" + \
    section("If you email us", "        <p>If you email <a href=\"mailto:yoyoboomerclub@gmail.com\">yoyoboomerclub@gmail.com</a>, we read it and answer it. We don't sell or share your email address.</p>\n        <p>Questions about this page? Same email.</p>")

# ---------------------------------------------------------------- Charter
charter = head("Adopted January 24, 2024", "The Charter", "\u201cWhere Gravity Takes a Break, and So Do We Occasionally.\u201d Eight articles, one lawn.") + "\n" + \
    section("The short version", checklist([
        "<strong>Who:</strong> all ages, any yo-yo, anyone who shares the club's values.",
        "<strong>Meetings:</strong> around once a month, online, for ease of access.",
        "<strong>Activities:</strong> workshops, themed challenges, casual talk about yo-yo techniques, and bourbon.",
        "<strong>Culture:</strong> open-minded, funny, helpful and courteous. Set a good example.",
        "<strong>Decisions:</strong> by consensus on the YYE forum or at the monthly meets. Everyone's input is welcome.",
    ])) + "\n" + \
    section("The Good Clauses", """        <div class="grid">
          <article class="card">
            <p class="era">Article II, Section 3</p>
            <h3>\u201cGet Off My Lawn\u201d</h3>
            <p>Members are allowed to throw in a \u201cget off my lawn\u201d remark when necessary to add to the \u201cBoomer\u201d spirit.</p>
          </article>
          <article class="card">
            <p class="era">Article II, Section 3.5</p>
            <h3>\u201c\u2026and Don\u2019t Come Back\u201d</h3>
            <p>Leave any time with no burned bridges. The YYBC will welcome you back with open arms.</p>
          </article>
          <article class="card">
            <p class="era">Article VI</p>
            <h3>Amendments</h3>
            <p>The charter may be amended on a whim or when deemed necessary. Most importantly, have fun, love your throws, and your people.</p>
          </article>
          <article class="card">
            <p class="era">Article VII, Section 3</p>
            <h3>Splitting the Atom</h3>
            <p>If the Arm Chair Quarterback / Camp Counselor(s) ever change, the club picks a volunteering exemplary or founding member to pass the \u201cYoyo Club Baton.\u201d We are forever!</p>
          </article>
        </div>""") + "\n" + \
    section("Founding Fathers / Declaration Daughters", """        <p>The forum members who signed on when the charter was adopted, January 24, 2024.</p>
        <p>AaronW, Abyss, adamantiumpops, archiesdad, Ardeus, Awiggs, Big Billipo, blacklabel9567, Bobparty, Captrogers, Chrizsmh13, cobrajs, ConnorWilkerson, cowmamba, davis25565, digitalcharlie, Doctor_Filthy, fos1, G2-Jake, GnarlyCharlie, Grendel, Hojo-Yoyo, Jdyo, Jhonaker, Joe77, JSERR, kretzschmar, Ksnow, MattC, mattd, Nwarda, Overtinkering, Pun1sh3R, QuickAt0m, RaRa, RBT, redzaku, rizki_yoist, rkalajian, safetypin, Sam, Shapapy, Slestak75, Son-of-Morris, TryCatchThrow, Veedo, vinniekowalski, Woodyrson, Yodaddyo</p>""") + "\n" + \
    section("Read the Whole Thing", """        <p>Three pages, signed off by the founding members.</p>
        <p><a class="btn btn-light" href="assets/documents/YYBC-Charter-2024.pdf">Charter (PDF)</a></p>
        <p class="links"><a href="faq.html">FAQ</a> \u00b7 <a href="sponsors.html">Sponsors</a> \u00b7 <a href="index.html#join">Join the club</a></p>""") 

# ---------------------------------------------------------------- Art
A = "assets/images/art/"
art = head("From the idea folder", "The Art Department",
    "Sketches, mascots and mock logos from the club's archived ideas. Every club logo starts as a bad idea in a notebook.") + "\n" + \
    section("Mascot Contenders", pics([
        fig(A + "turtle-sketch.webp", "Pencil sketch of a turtle with mechanical arms and the letters Y.Y.B.C. above it, next to two red yo-yos and some pens.", "The turtle mascot. It had fans on the forum on day one.", 900, 676),
        fig(A + "ninja-turtle.webp", "Color drawing of a green ninja turtle in an orange mask, sitting on a cloud and holding a red yo-yo on a string.", "Ninja turtle, with a yo-yo.", 750, 1000),
        fig(A + "ninja-turtle-2.webp", "Color drawing of the ninja turtle on a cloud with a red yo-yo and a ball of string, with Y.Y.B.C. in green letters above and the artist's signature in the corner.", "Ninja turtle, take two, signed by the artist.", 750, 1000),
        fig(A + "skull-and-tools.webp", "Pencil sketch of a skull over crossed wrenches and a screwdriver, with the letters YYBC in a burst behind it.", "Skull and tools.", 900, 769),
    ])) + "\n" + \
    section("Bombs and Lawns", pics([
        fig(A + "bomb-sketch.webp", "Pencil sketch of a round black bomb with a lit fuse, circled by the words Yoyo Boomer Club inside a spiky explosion burst.", "A bomb, as in boomer.", 900, 761),
        fig(A + "bomb-platter.webp", "Black and white sketch of a bomb on a serving platter under a cloche lid, with the letters YY BC beside it.", "Bomb on a platter.", 810, 1000),
        fig(A + "off-my-lawn.webp", "White silhouette of a person pushing a lawn mower on black, with the letters YYBC and the words Get off my lawn.", "Get off my lawn.", 900, 916),
        fig(A + "boomer-mower-logo.webp", "Mock logo: a black ring yo-yo with a string, and the words Yo-Yo boomer Club beside a tiny lawn mower marked Get off my lawn.", "A mock logo with a mower.", 900, 676),
    ])) + "\n" + \
    section("The Real Thing", "        <p>The logo we ended up with is at the top of every page. Some of these ideas are still floating around on pins and stickers.</p>\n" + more_links(['<a href="charter.html">The charter</a>', '<a href="sponsors.html">Sponsors</a>', '<a href="index.html#join">Join the club</a>']))

pages = {
    "events.html": ("Events", "What's coming up and every YoYo Boomer Club challenge since 2023, with trick lists and threads.", events),
    "faf-2024.html": ("Fixed Axle February 2024", "The club's first event: four weeks of fixed axle tricks and guest tricks.", faf24),
    "mrm-2024.html": ("Modern Responsive March 2024", "Four weeks of modern responsive tricks from the YoYo Boomer Club.", mrm24),
    "2a-pril-2024.html": ("2A-pril 2024", "Three weeks of looping tricks and guest tricks.", a24),
    "5a-may-2024.html": ("5A May 2024", "Counterweight month with a beginner ladder, trick of the week and freeform round.", may24),
    "one-july-2024.html": ("ONE July 2024", "Pick one yo-yo and throw it all month.", july),
    "faf-2026.html": ("Fixed Axle February 2026", "Seven tricks, all month, no weekly deadlines.", faf26),
    "mrm-2026.html": ("Modern Responsive March 2026", "A Fallout-themed, nine-trick, month-long ladder.", mrm26),
    "faq.html": ("FAQ", "Short answers about the YoYo Boomer Club: who can join, what it costs, where it meets, Yovember and more.", faq),
    "art.html": ("The Art Department", "Sketches, mascots and mock logos from the YoYo Boomer Club's archived ideas: turtles, bombs and lawn mowers.", art),
    "charter.html": ("Charter", "The YoYo Boomer Club charter, adopted January 24, 2024: who we are, how we meet, and the get-off-my-lawn clause.", charter),
    "privacy.html": ("Privacy", "The YoYo Boomer Club site collects nothing about you: no forms, cookies, analytics or trackers.", privacy),
    "sponsors.html": ("Sponsors", "The companies behind the YoYo Boomer Club: club sponsors, this year's event sponsors, and past event sponsors and donors.", spons),
    "yovember.html": ("Yovember", "Yovember starts November 1: grow a stash, talk yo-yo, throw tricks and raise money for men's health.", yov),
    "fundraisers.html": ("Boomers for Toys for Tots", "$130 in 2023. $1,300 in 2024. Our annual holiday fundraiser with Throw-Yo and YoYoExpert.", fund),
    "workhorse.html": ("The Workhorse", "The YYBC and G Squared collaboration yo-yo: specs, colorways and the road from prototype to production.", work),
}
for fname, (t, d, b) in pages.items():
    page(fname, t, d, b)
print("wrote", ", ".join(pages))
