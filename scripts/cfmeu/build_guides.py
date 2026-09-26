#!/usr/bin/env python3
"""Render the /guides pages from data/cfmeu-figures.json.

Every dollar figure and effective date on the guides comes from the JSON file, so a
figure never has to be edited in HTML. Run from the repo root:

    python scripts/cfmeu/build_guides.py

The page shell (SVG defs, nav, footer) is lifted from public/eba-payroll-software.html
so the guides always match the rest of the site.
"""
import io
import json
import os
import re
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PUB = os.path.join(ROOT, "public")
DATA = os.path.join(ROOT, "data", "cfmeu-figures.json")

F = json.load(io.open(DATA, encoding="utf-8"))
W, A, S, R = F["wages"], F["allowances"], F["site_allowance"], F["rdo"]
E = json.load(io.open(os.path.join(ROOT, "data", "cfmeu-employers.json"), encoding="utf-8"))  # built by fwc_employers.py

src = io.open(os.path.join(PUB, "eba-payroll-software.html"), "r", encoding="utf-8", newline="").read()
NL = "\r\n" if "\r\n" in src[:3000] else "\n"


def block(pattern):
    m = re.search(pattern, src, re.S)
    assert m, pattern[:40]
    return m.group(0)


SVG = block(r'<svg class="svg-defs".*?</svg>')
NAV = block(r'<nav class="nav" aria-label="Main">.*?</nav>').replace('src="paykicker-logo.svg"', 'src="/paykicker-logo.svg"')
FOOT = block(r'<footer class="foot">.*?</footer>')
assert '/guides/' in NAV and '/guides/' in FOOT, "nav/footer on the landing page must carry the Guides link"

# ---------------------------------------------------------------- formatting helpers

def money(s):
    """'2239.56' -> '$2,239.56'; '280' -> '$280'; '0.60' -> '$0.60'."""
    s = str(s)
    if "." in s:
        whole, frac = s.split(".")
        return "$" + f"{int(whole):,}" + "." + frac
    return "$" + f"{int(s):,}"


def d_short(iso):  # 1 Feb 2026
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b')} {d.year}"


def d_long(iso):  # 1 February 2026
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B')} {d.year}"


def day_before_long(iso):
    d = date.fromisoformat(iso)
    d = date.fromordinal(d.toordinal() - 1)
    return f"{d.day} {d.strftime('%B')} {d.year}"


def fig(key, text):
    return f'<span data-fig="{key}">{text}</span>'


def m_(section, key):  # money figure with its data-fig marker
    return fig(f"{section}.{key}", money(F[section][key]))


def millions(s):
    s = str(s)
    return "$" + (f"{float(s):,.1f}" if "." in s else f"{int(s):,}") + " million"


# ---------------------------------------------------------------- page shell

HEAD = '''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="/paykicker-icon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/paykicker-icon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/paykicker-icon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/paykicker-icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#12293f">
<link rel="canonical" href="https://paykicker.com.au{path}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="article">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://paykicker.com.au{path}">
<meta property="og:locale" content="en_AU">
<meta property="og:site_name" content="PayKicker">
<meta property="og:image" content="https://paykicker.com.au/paykicker-og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://paykicker.com.au/paykicker-og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Stencil+Display:wght@700;800&family=Archivo:wght@400;500;600&family=Courier+Prime:wght@400;700&family=Zilla+Slab:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="/css/setout.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-4DGX8VDBNH"></script>
<script src="/js/gtag.js"></script>
<script src="/js/pixels.js"></script>
{jsonld}
<style>
  .guide-list{{list-style:none;padding:0;margin-top:26px;max-width:760px}}
  .guide-list li{{border-top:1px solid var(--string);padding:22px 0}}
  .guide-list li:last-child{{border-bottom:1px solid var(--string)}}
  .guide-list h2{{font-size:clamp(24px,2.6vw,32px);max-width:none;margin:0 0 8px}}
  .guide-list p{{max-width:66ch}}
  .guide-list .when{{font-size:13.5px;color:var(--ink2);margin-top:8px}}
  .cal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:0 28px;margin-top:18px;max-width:900px}}
  .cal div{{padding:12px 0;border-bottom:1px solid var(--string-soft)}}
  .cal b{{display:block;font-family:var(--disp);font-weight:800;font-size:17px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px}}
  .cal span{{display:block;font-size:15px;line-height:1.5}}
  .cal span.ph{{color:var(--ink2);font-size:13.5px}}
  .src{{font-size:13.5px;color:var(--ink2);max-width:72ch;margin-top:12px}}
  .stamp{{display:inline-block;font-family:var(--disp);font-weight:800;font-size:14px;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--navy);padding:4px 10px;margin:0 0 12px}}
  .tbl td.n{{white-space:nowrap;font-variant-numeric:tabular-nums}}
  .guide-list h2 a{{text-decoration:none}}
  .guide-list h2 a:hover{{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px}}
  .emp-filter{{margin-top:22px;max-width:560px}}
  .emp-filter label{{display:block;font-family:var(--disp);font-weight:800;font-size:15px;letter-spacing:.1em;text-transform:uppercase}}
  .emp-filter input{{display:block;width:100%;margin-top:6px;padding:11px 12px;border:1px solid var(--string);border-radius:2px;background:var(--chalk);color:var(--navy);font:inherit;font-size:16px}}
  .emp-filter input:focus{{outline:2px solid var(--navy);outline-offset:1px}}
  .emp-filter .cnt{{display:block;margin-top:8px;font-size:14px;color:var(--ink2);font-variant-numeric:tabular-nums}}
  .emp-jump{{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:18px;font-size:14.5px;line-height:1.5;max-width:none;color:var(--ink2)}}
  .emp-jump a{{white-space:nowrap}}
  .emp-sec h3{{display:flex;align-items:baseline;gap:10px;margin-top:34px;scroll-margin-top:110px}}
  .emp-sec h3 .n{{font-family:var(--mono);font-size:15px;font-weight:400;color:var(--ink2)}}
  .prose ul.emp{{list-style:none;padding:0;margin:8px 0 0;max-width:900px;columns:2;column-gap:36px}}
  .emp li{{break-inside:avoid;margin:0;padding:7px 0;border-bottom:1px solid var(--string-soft);font-size:15px;line-height:1.4;display:flex;justify-content:space-between;gap:12px}}
  .emp li + li{{margin-top:0}}
  .emp .nm{{min-width:0}}
  .emp .dt{{flex:none;font-family:var(--mono);font-size:12.5px;color:var(--ink2);white-space:nowrap;padding-top:3px}}
  .emp .dt.old{{color:var(--orange)}}
  .emp li[hidden],.emp-sec[hidden],.emp-jump[hidden]{{display:none}}
  @media(max-width:860px){{.emp{{columns:1}}}}
  @media(max-width:640px){{.tbl td.n{{white-space:normal}} .tbl th,.tbl td{{font-size:14px;padding-right:0}} .emp li{{flex-direction:column;gap:2px}} .emp .dt{{padding-top:0}}}}
</style>
</head>
<body>
'''


def section(letter, name, sid, inner):
    return (f'<section class="sheet prose" id="{sid}">{NL}  <div class="wrap">{NL}'
            f'    <div class="mark"><span class="bub" aria-hidden="true">{letter}</span><span class="name">{name}</span><span class="string" aria-hidden="true"></span></div>{NL}'
            f'    <div class="body">{NL}{inner}{NL}      <div class="rule" aria-hidden="true"></div>{NL}    </div>{NL}  </div>{NL}</section>{NL}{NL}')


def tiles(items):
    """Four figure tiles under the lede: [(big, small_suffix_or_None, caption), ...]."""
    out = []
    for big, small, cap in items:
        out.append(f'    <div class="tile"><b>{big}{("<small>" + small + "</small>") if small else ""}</b><span class="cap">{cap}</span></div>')
    return f'  <div class="tiles">{NL}' + NL.join(out) + f'{NL}  </div>{NL}'


def head_section(name, h1, lede, toc, extra=""):
    inner = f'      <h1>{h1}</h1>{NL}{NL}  <p class="lede">{lede}</p>{NL}{extra}'
    if toc:
        items = NL.join(f'      <li data-b="{b}"><a href="#{a}">{t}</a></li>' for b, a, t in toc)
        inner += f'{NL}  <nav class="toc" aria-label="On this page">{NL}    <p class="toc-h">On this page</p>{NL}    <ol>{NL}{items}{NL}    </ol>{NL}  </nav>'
    return (f'<section class="sheet prose page-head" id="top">{NL}  <div class="wrap">{NL}'
            f'    <div class="mark"><span class="bub" aria-hidden="true">A</span><span class="name">{name}</span><span class="string" aria-hidden="true"></span></div>{NL}'
            f'    <div class="body">{NL}{inner}{NL}      <div class="rule" aria-hidden="true"></div>{NL}    </div>{NL}  </div>{NL}</section>{NL}{NL}')


DEMO = '''      <h2>See your own agreement running in it</h2>
      <p>PayKicker encodes the clauses above once and applies them to every timesheet, then hands MYOB a file with the hours already classified. Bring your enterprise agreement and a recent pay run to a 30-minute demo and we will show the same period calculated both ways.</p>
      <div class="cta-act"><a class="spray" href="/#contact">Book a demo</a></div>
      <p class="related">Related:
    {related}</p>
      <p class="indep">PayKicker is independent software and is not affiliated with or endorsed by the CFMEU or MYOB. This guide is general information for a subcontractor's office, not legal or industrial relations advice; the agreement and the union's published sheets are the source, and figures change at every wage increase.</p>'''

DEMO_JOBS = '''      <h2>If your company is on this list</h2>
      <p>Every company above runs payroll under the same agreement: a 36-hour week with RDOs banked daily, site allowance by the hour, fares by the day, and a wage sheet that changes three times a year. PayKicker encodes those clauses once, classifies every timesheet against them, and hands MYOB a file with the hours already sorted. Bring your agreement and a recent pay run to a 30-minute demo and we will show the same period calculated both ways.</p>
      <div class="cta-act"><a class="spray" href="/#contact">Book a demo</a></div>
      <p class="related">Related:
    {related}</p>
      <p class="indep">PayKicker is independent software and is not affiliated with or endorsed by the CFMEU, the Fair Work Commission or MYOB, and it is not a recruiter: it does not place workers and has no relationship with the companies listed. This guide is general information for people looking for work and for the companies that employ them, not legal, industrial or careers advice. Company names are as they appear on the Commission's lists; an agreement's existence says nothing about whether a company is hiring.</p>'''

TAIL = NL + "</main>" + NL + NL + FOOT + NL + NL + "</body>" + NL + "</html>" + NL


def page(path, title, ogtitle, desc, jsonld, body):
    html = HEAD.format(title=title, ogtitle=ogtitle, desc=desc, path=path, jsonld=jsonld) + NL + SVG + NL + NL + NAV + NL + NL + '<main class="guide">' + NL + body + TAIL
    html = html.replace("\r\n", "\n").replace("\n", NL)
    out = os.path.join(PUB, path.strip("/").replace("/", os.sep))
    out = os.path.join(out, "index.html") if path.endswith("/") else out + ".html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8", newline="").write(html)
    print("wrote", os.path.relpath(out, ROOT), len(html))


def article_ld(path, headline, desc, published, modified):
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{headline}",
  "description": "{desc}",
  "url": "https://paykicker.com.au{path}",
  "datePublished": "{published}",
  "dateModified": "{modified}",
  "inLanguage": "en-AU",
  "articleSection": "Guides",
  "author": {{ "@id": "https://paykicker.com.au/#organization" }},
  "publisher": {{ "@id": "https://paykicker.com.au/#organization" }},
  "mainEntityOfPage": "https://paykicker.com.au{path}"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "PayKicker", "item": "https://paykicker.com.au/" }},
    {{ "@type": "ListItem", "position": 2, "name": "Guides", "item": "https://paykicker.com.au/guides/" }},
    {{ "@type": "ListItem", "position": 3, "name": "{headline}", "item": "https://paykicker.com.au{path}" }}
  ]
}}
</script>'''


PUBLISHED = "2026-09-25"
AS_AT = F["as_at"]

# ---------------------------------------------------------------- RDO calendar block

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def wd(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%a')} {d.day}"


def join_and(items):
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def ranges(isos):
    """Consecutive dates collapse to 'Tue 29 to Thu 31'."""
    out, run = [], []
    for iso in sorted(isos):
        if run and date.fromisoformat(iso).toordinal() == date.fromisoformat(run[-1]).toordinal() + 1:
            run.append(iso)
        else:
            if run:
                out.append(run)
            run = [iso]
    if run:
        out.append(run)
    return [wd(r[0]) if len(r) == 1 else f"{wd(r[0])} to {wd(r[-1])}" for r in out]


def month_grids(year, y):
    """Twelve month grids, Monday first: RDOs filled, public holidays ringed, close-down shaded, lockdown weekends underlined."""
    import calendar
    yr = int(year)
    kind = {}
    for d in y["rdo"]:
        kind[d] = "rdo"
    for p in y["public_holidays"]:
        kind[p["date"]] = "ph"
    for d in y.get("annual_leave", []):
        kind.setdefault(d, "al")
    for d in y.get("lockdown_weekends", []):
        kind.setdefault(d, "lk")
    for o in y.get("other", []):
        kind.setdefault(o["date"], "oth")
    out = []
    for mi, mname in enumerate(MONTHS, 1):
        cells = [f'<i>{d}</i>' for d in ("M", "T", "W", "T", "F", "S", "S")]
        for week in calendar.Calendar(firstweekday=0).monthdayscalendar(yr, mi):
            for wd_i, day in enumerate(week):
                if day == 0:
                    cells.append('<b class="e"></b>')
                    continue
                iso = f"{yr}-{mi:02d}-{day:02d}"
                cls = kind.get(iso, "we" if wd_i >= 5 else "")
                cells.append(f'<b class="{cls}">{day}</b>' if cls else f'<b>{day}</b>')
        names = [f"{p['name']} {wd(p['date'])}" for p in y["public_holidays"] if int(p["date"][5:7]) == mi]
        names += [f"{o['name'].split(' (')[0]} {wd(o['date'])}" for o in y.get("other", []) if int(o["date"][5:7]) == mi]
        names_html = f'<p class="ph-names">{"; ".join(names)}</p>' if names else ""
        out.append(f'        <div class="mon"><h4>{mname}</h4><div class="days">{"".join(cells)}</div>{names_html}</div>')
    return NL.join(out)


CAL_KEY = ('      <p class="cal-key"><span><b class="rdo" style="background:var(--navy);color:var(--chalk)">12</b> RDO</span>'
           '<span><b style="box-shadow:inset 0 0 0 1.5px var(--navy)">9</b> public holiday</span>'
           '<span><b style="background:var(--cured)">2</b> close-down, annual leave</span>'
           '<span><b style="text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:2px">3</b> lockdown weekend</span>'
           '<span><b style="box-shadow:inset 0 0 0 1px var(--string-soft)">15</b> other industry day</span></p>')


def calendar_block(year, y):
    rows = []
    for mi, mname in enumerate(MONTHS, 1):
        rdo = [wd(d) for d in y["rdo"] if int(d[5:7]) == mi]
        dated = [(p["date"], f"{p['name']} {wd(p['date'])}") for p in y["public_holidays"] if int(p["date"][5:7]) == mi]
        for o in y.get("other", []):
            if int(o["date"][5:7]) == mi:
                name = o["name"]
                if "(" in name:  # 'West Gate Memorial (not a public holiday)' -> 'West Gate Memorial Thu 15 (not a public holiday)'
                    base, paren = name.split("(", 1)
                    dated.append((o["date"], f"{base.strip()} {wd(o['date'])} ({paren}"))
                else:
                    dated.append((o["date"], f"{name} {wd(o['date'])}"))
        notes = [t for _, t in sorted(dated)]
        al = [d for d in y.get("annual_leave", []) if int(d[5:7]) == mi]
        if al:
            notes.append("Annual leave " + join_and(ranges(al)))
        rows.append(f'        <div><b>{mname}</b><span>RDO: {", ".join(rdo) if rdo else "none"}</span>' + (f'<span class="ph">{"; ".join(notes)}</span>' if notes else "") + "</div>")
    lock = y.get("lockdown_weekends", [])
    by_month = {}
    for d in lock:
        by_month.setdefault(int(d[5:7]), []).append(str(int(d[8:10])))
    lock_txt = ", ".join(f"{join_and(v)} {MONTHS[k-1]}" for k, v in sorted(by_month.items()))
    return NL.join(rows), lock_txt, len(lock)


# ---------------------------------------------------------------- RDO guide

RDO_PATH = "/guides/cfmeu-rdo-calendar-2026"
years = sorted(R["years"].keys())
Y0 = years[-1]  # the newest published calendar leads
RDO_TITLE = f"CFMEU RDO Calendar {Y0} and the 36-Hour Week, Explained for Payroll | PayKicker"
RDO_OG = f"CFMEU RDO calendar {Y0} and the 36-hour week, explained for payroll"
RDO_DESC = f"The {Y0} Victorian on-site RDO dates, how RDOs accrue under a CFMEU construction EBA (0.8 hours a day, 26 a year), what a worked RDO pays, and where payroll gets it wrong."

RDO_FAQ = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{ "@type": "Question", "name": "How do RDOs accrue under the CFMEU Victorian construction EBA?", "acceptedAnswer": {{ "@type": "Answer", "text": "The ordinary week is 36 hours worked as 8-hour days. Each 8-hour day, 0.8 of an hour is banked toward a rostered day off, so nine working days bank the tenth. That gives 26 RDOs a year. Paid leave and public holidays count as days worked for accrual; overtime, weekends and the RDO itself do not." }} }},
    {{ "@type": "Question", "name": "What does a worker get paid for working on an RDO?", "acceptedAnswer": {{ "@type": "Answer", "text": "It depends on consultation. If the workers and their union representative were given written notice beforehand, the day is paid at the ordinary rate and the banked RDO is kept. If they were not consulted, the day is paid at 250% with a four-hour minimum. The RDO attached to a designated long weekend is paid at 250% either way." }} }},
    {{ "@type": "Question", "name": "Where are the {Y0} CFMEU RDO dates published?", "acceptedAnswer": {{ "@type": "Answer", "text": "The CFMEU Victoria branch publishes the {Y0} Victoria on-site RDO calendar as a PDF and an ICS calendar file at vic.cfmeu.org/rdo-calendars. The dates on this page are taken from that ICS file." }} }}
  ]
}}
</script>'''

RDO_TOC = [("B", "week", "The 36-hour week"), ("C", "accrue", "How an RDO accrues"), ("D", "dates", f"{Y0} RDO dates"),
           ("E", "worked", "Working on an RDO"), ("F", "payroll", "Where payroll gets it wrong"), ("G", "figures", "Current figures, dated"), ("H", "demo", "See it running")]

body = head_section("RDOs", f"CFMEU RDO calendar {Y0} and the 36&#8209;hour week, explained for payroll",
    f"If your crew is on a CFMEU Victorian Construction and General Division enterprise agreement, the week is 36 hours, not 38, and every eighth hour of a working day is banked toward a rostered day off. This guide sets out the {Y0} on-site RDO dates the union publishes, how the accrual works clause by clause, what a worked RDO pays, and the four places office payroll gets it wrong.",
    RDO_TOC,
    f'  <p class="note">Written 25 September 2026, figures checked {fig("as_at", d_long(AS_AT))}, for the 2024&ndash;2027 agreements. Clause numbers are the formwork subcontractors\' agreement; the crane, steelfixing and other trade agreements share the same skeleton with their own numbering.</p>{NL}'
    + tiles([("36", " hrs", "the ordinary week, worked as five 8-hour days"), ("26", None, f"paid RDOs on the {Y0} calendar, on top of leave and holidays"),
             ("0.8", " hr", "banked toward the next RDO on every ordinary day worked"), ("250", "%", "for an RDO worked without consultation, four-hour minimum")]))

body += section("B", "36 hours", "s-week", '''      <h2 id="week">The 36-hour week</h2>
      <p>Ordinary hours are the first 8 hours worked between 6:00am and 6:00pm, Monday to Friday, and the notional week is 36 hours (cl 36.1, cl 36.2(a)). The crew still turns up for five 8-hour days: 40 hours are worked in the week, 36 are paid as ordinary time, and the 4 remaining hours (0.8 a day) are banked. Every second Monday, or whichever day the industry calendar names, the bank is spent on a paid day off.</p>
      <p>That is the whole mechanism, and it is why a payroll system set up for a 38-hour week is wrong every single week. Under a 38-hour default, overtime starts two hours too late and nothing is banked at all.</p>
      <p>The union puts it plainly on its wage sheets: the 36-hour week was won in 2000 and gives workers 26 paid days off a year on top of leave and public holidays. Those 26 days are the RDOs (cl 38.3).</p>''')

body += section("C", "Accrual", "s-accrue", '''      <h2 id="accrue">How an RDO accrues</h2>
      <p>The cycle is ten working days over two weeks: 8 hours on each of nine days, with 0.8 of an hour banked each day toward the tenth (cl 38.1). Nine days of 0.8 is 7.2 hours, plus the 0.8 that would have been banked on the day itself, and the RDO is paid as an 8-hour day.</p>
      <h3>What counts as a day worked for accrual</h3>
      <ul>
        <li><b>Ordinary hours worked</b>: 0.1 of an hour for every ordinary hour, so 0.8 on a full day.</li>
        <li><b>Paid leave and public holidays</b>: the agreement says these count as a day worked for accrual purposes (cl 38.4), so a week with Cup Day in it still banks the full 4 hours.</li>
      </ul>
      <h3>What does not accrue</h3>
      <ul>
        <li>Overtime hours and weekend work. Only ordinary hours bank.</li>
        <li>The RDO itself. A day off does not bank toward the next day off.</li>
        <li>Casual employees. Casuals are paid a loading on ordinary hours instead of banking RDOs.</li>
      </ul>
      <div class="aside chalk">
        <p><b>Two ways to hold the bank.</b> Some payroll setups treat RDOs as a leave balance that is topped up by hand; the agreement treats them as an accrual that runs off the hours actually worked. The second is the only one that survives a part week, a week with leave in it, or a worker who starts mid-cycle. In PayKicker the accrual is exported with the timesheet hours and MYOB runs the bank and prints it on the payslip.</p>
      </div>''')

dates_inner = f'''      <h2 id="dates">The {Y0} on-site RDO dates</h2>
      <p>These are the rostered days off on the CFMEU Victoria <b>{Y0} Victoria On-Site RDO calendar</b>, taken from the ICS calendar file the branch publishes. Most fall on a Monday; the ones that do not sit beside a public holiday so the crew gets a run of days off. The calendar also marks the Christmas and New Year close-down as annual leave and the "lockdown" weekends, which matter for pay if anyone works them (see the next section).</p>'''
for yr in reversed(years):
    rows, lock_txt, nlock = calendar_block(yr, R["years"][yr])
    if len(years) > 1:
        dates_inner += f'{NL}      <h3>{yr}</h3>'
    dates_inner += f'''
      <div class="months">
{month_grids(yr, R["years"][yr])}
      </div>
{CAL_KEY}
      <p>RDO dates in list form: {"; ".join(f"{MONTHS[m - 1]} {', '.join(wd(d) for d in R['years'][yr]['rdo'] if int(d[5:7]) == m)}" for m in range(1, 13) if any(int(d[5:7]) == m for d in R['years'][yr]['rdo']))}.</p>
      <p>Lockdown weekends on the {yr} calendar ({nlock}): {lock_txt}.</p>'''
dates_inner += f'''
      <p class="src">Source: CFMEU Victoria, Victoria On-Site RDO calendar (ICS file), <a href="{R["source_url"]}" rel="noopener">vic.cfmeu.org/rdo-calendars</a>. Public holidays as marked on that calendar. Companies can agree different RDO dates with their crew under the agreement; if yours has, your own calendar governs.</p>'''
body += section("D", f"{Y0} dates", "s-dates", dates_inner)

body += section("E", "Worked RDO", "s-worked", '''      <h2 id="worked">Working on an RDO</h2>
      <p>Crews do work RDOs, usually because a pour or a crane lift will not wait. The agreement sets two different rates for the same day, and which one applies turns on one fact: were the workers consulted (cl 38.8)?</p>
      <div class="tbl"><table>
        <thead><tr><th>Situation</th><th>Rate for the day</th><th>Clause</th></tr></thead>
        <tbody>
          <tr><td>Workers <b>were</b> consulted beforehand</td><td>Ordinary rate, and the banked RDO is kept</td><td class="n">38.8(e)</td></tr>
          <tr><td>Workers were <b>not</b> consulted</td><td>250%, minimum four hours (public-holiday money)</td><td class="n">38.8(f), 38.10</td></tr>
          <tr><td>The RDO attached to a designated long weekend (a "lockdown" weekend on the union calendar)</td><td>250%, consulted or not</td><td class="n">38.8(k)</td></tr>
          <tr><td>Casual, not consulted</td><td>275% (250% plus the casual loading)</td><td class="n">38.8(g), 14.10</td></tr>
        </tbody>
      </table></div>
      <p>Consultation means written notice to the affected workers <b>and</b> their union representative before the day (cl 38.8(c)). A text to the leading hand the night before is not consultation, and the difference on a Saturday pour is the whole day at 250%.</p>
      <p>Hours past eight on a consulted RDO are ordinary overtime. Hours on an unconsulted one are all at the penalty rate.</p>
      <p>One more case that catches offices: a training day that lands on a scheduled RDO is paid as an ordinary day, and the worker is owed a substitute day off (cl 15.4). The RDO stays banked.</p>''')

body += section("F", "Payroll", "s-payroll", '''      <h2 id="payroll">Where payroll gets it wrong</h2>
      <ol class="steps">
        <li><b>The 38-hour default.</b> Off-the-shelf payroll assumes 38 ordinary hours and overtime after that. Under the agreement, ordinary time is 8 hours a day and 36 a week; the fix is a 36-hour week with daily overtime, not a weekly threshold.</li>
        <li><b>RDOs as a leave balance.</b> A hand-maintained balance drifts within a month. The bank should accrue from the hours actually classified as ordinary, week by week, so a part week or a week of leave lands correctly without anyone touching it.</li>
        <li><b>No accrual on leave and holidays.</b> Cl 38.4 counts paid leave and public holidays as days worked for accrual. A system that banks only on hours keyed in short-changes every worker who took a day off.</li>
        <li><b>A worked RDO paid as "base hourly".</b> When a worked RDO is paid on the ordinary pay item, the payslip cannot show that it was an RDO or that the crew was consulted. Put worked RDOs on their own pay item, named for what they are, so the dispute never starts.</li>
      </ol>
      <p>The RDO bank is the thing an office is least able to reconstruct after the fact. If you are auditing a period, start from the classified hours and rebuild the accrual; do not start from the balance.</p>''')

body += section("G", "Figures", "s-figures", f'''      <h2 id="figures">Current figures, dated</h2>
      <p class="stamp">As at {fig("as_at", d_long(AS_AT))}</p>
      <p>These come from the CFMEU Victoria wage sheets. They change at every wage increase, so treat the date on this page as part of the figure.</p>
      <div class="tbl"><table>
        <thead><tr><th>Item</th><th>Figure</th><th>From</th></tr></thead>
        <tbody>
          <tr><td>CW3 carpenter, tile-layer, plasterer, bricklayer (100%)</td><td class="n">{m_("wages","cw3_hour")} per hour, {m_("wages","cw3_week")} per 36-hour week</td><td class="n">{fig("wages.rates_from", d_short(W["rates_from"]))}</td></tr>
          <tr><td>CW2 scaffolder, steel fixer, concrete finisher (96%)</td><td class="n">{m_("wages","cw2_hour")} per hour, {m_("wages","cw2_week")} per week</td><td class="n">{fig("wages.rates_from", d_short(W["rates_from"]))}</td></tr>
          <tr><td>CW1 trades labourer, concrete gang (92.4%)</td><td class="n">{m_("wages","cw1_hour")} per hour, {m_("wages","cw1_week")} per week</td><td class="n">{fig("wages.rates_from", d_short(W["rates_from"]))}</td></tr>
          <tr><td>Superannuation</td><td class="n">{m_("wages","super_weekly")} per week or {fig("wages.super_pct", W["super_pct"])}% of ordinary time earnings, whichever is greater</td><td class="n">{fig("wages.benefits_from", d_short(W["benefits_from"]))}</td></tr>
          <tr><td>Incolink redundancy contribution</td><td class="n">{m_("wages","incolink_weekly")} per week</td><td class="n">{fig("wages.benefits_from", d_short(W["benefits_from"]))}</td></tr>
          <tr><td>Travel allowance (fares and travel)</td><td class="n">{m_("wages","travel_daily")} per day</td><td class="n">{fig("wages.benefits_from", d_short(W["benefits_from"]))}</td></tr>
        </tbody>
      </table></div>
      <p class="src">Source: CFMEU Victoria, <i>{W["source_title"]}</i> (rates from {fig("wages.rates_from", d_long(W["rates_from"]))}; other benefits from {fig("wages.benefits_from", d_long(W["benefits_from"]))}), <a href="{W["source_url"]}" rel="noopener">vic.cfmeu.org/wages</a>. Weekly rates are the hourly rate times 36. Site allowance, fares and the other daily and hourly extras are covered in the <a href="/guides/cfmeu-site-allowance-fares-travel-2026">site allowance, fares and travel guide</a>.</p>''')

body += section("H", "Demo", "demo", DEMO.format(related='<a href="/guides/cfmeu-site-allowance-fares-travel-2026">Site allowance, fares and travel 2026</a> &middot; <a href="/guides/cfmeu-eba-jobs-victoria">CFMEU EBA jobs and the list of EBA companies</a> &middot; <a href="/eba-payroll-software">EBA payroll software</a> &middot; <a href="/guides/">All guides</a>'))

page(RDO_PATH, RDO_TITLE, RDO_OG, RDO_DESC, article_ld(RDO_PATH, RDO_OG, RDO_DESC, PUBLISHED, AS_AT) + NL + RDO_FAQ, body)

# ---------------------------------------------------------------- Site allowance guide

SA_PATH = "/guides/cfmeu-site-allowance-fares-travel-2026"
SA_TITLE = "CFMEU Site Allowance, Fares and Travel 2026: Rates and Rules | PayKicker"
SA_OG = "CFMEU site allowance, fares and travel 2026: the rates and when they apply"
SA_DESC = f"Site allowance bands from {d_long(S['applies_from'])}, the {money(W['travel_daily'])} daily fares and travel allowance, multi-storey and leading hand rates, and the rules for when each applies under a CFMEU Victorian construction EBA."

SA_TOC = [("B", "site", "What site allowance is"), ("C", "table", f"Site allowance from {d_short(S['applies_from'])}"), ("D", "fares", "Fares and travel"),
          ("E", "extras", "Multi-storey, leading hand and the rest"), ("F", "payslip", "How they land on a payslip"), ("G", "demo", "See it running")]

body = head_section("Allowances", "CFMEU site allowance, fares and travel 2026: the rates and when they apply",
    "Under a CFMEU Victorian Construction and General Division enterprise agreement, a worker's hourly rate is only part of the day. Site allowance rides on every hour worked on a project over the value threshold, fares and travel is a flat daily amount, and a dozen smaller allowances attach to particular work. This guide gives the current published figures with their dates, the clauses that switch each one on, and the mistakes that show up in a subcontractor's pay run.",
    SA_TOC,
    f'  <p class="note">Written 25 September 2026, figures checked {fig("as_at", d_long(AS_AT))}, for the 2024&ndash;2027 agreements. Figures are the CFMEU Victoria sheets\' and are dated; clause numbers are the formwork subcontractors\' agreement.</p>{NL}'
    + tiles([(m_("site_allowance", "inner_new"), " /hr", f"site allowance, Melbourne inner suburbs, new project, from {d_short(S['applies_from'])}"),
             (m_("wages", "travel_daily"), " /day", f"fares and travel on every day attended, from {d_short(W['benefits_from'])}"),
             (fig("site_allowance.threshold_m", "$" + S["threshold_m"] + "m"), None, "project value from which site allowance applies"),
             (fig("site_allowance.cpi_pct", S["cpi_pct"]), "%", f"Melbourne CPI applied to the rates and bands on the {d_short(S['applies_from'])} sheet")]))

body += section("B", "Site allowance", "s-site", f'''      <h2 id="site">What site allowance is, and when it applies</h2>
      <p>Site allowance is an hourly amount paid for every hour worked on a qualifying project, ordinary and overtime alike (Appendix C, para 4). It compensates for the conditions of a large site, so it is set by the project, not the worker: everyone on the job gets the same figure, and a worker on two sites in one day earns each site's allowance on the hours worked there.</p>
      <ul>
        <li><b>The threshold.</b> Site allowance applies to projects at or above the indexed value threshold, which is {fig("site_allowance.threshold_m", millions(S["threshold_m"]))} on the table that applies from {fig("site_allowance.applies_from", d_long(S["applies_from"]))}. Below that, the Award's special rates apply instead (Appendix C, paras 2 and 3).</li>
        <li><b>New work or renovation.</b> New projects and renovation, restoration or refurbishment projects carry different rates. Where a job mixes the two, the new-projects rate applies when the value of the new work is more than 33% of the total project value.</li>
        <li><b>Where the site is.</b> Melbourne inner suburbs and shopping centres have one flat rate for projects up to {fig("site_allowance.inner_cap_m", millions(S["inner_cap_m"]))}; elsewhere the rate steps up through value bands.</li>
        <li><b>Indexation.</b> Both the rates and the value bands move with Melbourne CPI each year, so the band a project sits in can change mid-job.</li>
      </ul>''')

band_max = max(float(b["rate"]) for b in S["bands"] + S["projects"])
band_rows = NL.join(f'        <div class="bar"><span class="lbl">{millions(b["lo_m"])} to {millions(b["hi_m"])}</span><i style="--w:{float(b["rate"]) / band_max * 100:.0f}%"></i><span class="val">{money(b["rate"])}</span></div>' for b in S["bands"])
proj_bars = NL.join(f'        <div class="bar"><span class="lbl">{p["name"]}</span><i style="--w:{float(p["rate"]) / band_max * 100:.0f}%"></i><span class="val">{money(p["rate"])}</span></div>' for p in S["projects"])
proj_rows = NL.join(f'          <tr><td>{p["name"]}</td><td class="n">{money(p["rate"])} per hour</td></tr>' for p in S["projects"])

body += section("C", "The table", "s-table", f'''      <h2 id="table">Site allowance from {fig("site_allowance.applies_from", d_long(S["applies_from"]))}</h2>
      <p class="stamp">Applies from {fig("site_allowance.applies_from", d_long(S["applies_from"]))}</p>
      <p>The union's site allowance sheet for this period applies the {fig("site_allowance.cpi_pct", S["cpi_pct"])}% All Groups CPI (Melbourne) increase to both the rates and the project values. The previous sheet applies to hours worked up to {fig("site_allowance.day_before", day_before_long(S["applies_from"]))}.</p>
      <h3>Melbourne inner suburbs and shopping centres</h3>
      <div class="tbl"><table>
        <thead><tr><th>Project</th><th>Site allowance</th></tr></thead>
        <tbody>
          <tr><td>New projects, {millions(S["threshold_m"])} to {millions(S["inner_cap_m"])}</td><td class="n">{m_("site_allowance","inner_new")} per hour</td></tr>
          <tr><td>Renovations, restorations and refurbishments, {millions(S["threshold_m"])} to {millions(S["inner_cap_m"])}</td><td class="n">{m_("site_allowance","inner_reno")} per hour</td></tr>
          <tr><td>Projects over {millions(S["inner_cap_m"])}</td><td>Banded rates below</td></tr>
        </tbody>
      </table></div>
      <h3>New projects elsewhere, by project value</h3>
      <p>Per hour worked, stepping up with the head contract value. The bar is the rate relative to the highest figure on the sheet.</p>
      <div class="bars">
{band_rows}
      </div>
      <h3>Project-specific rates</h3>
      <div class="bars">
{proj_bars}
      </div>
      <p class="src">Source: CFMEU Victoria, <i>{S["source_title"]}</i> sheet applicable from {fig("site_allowance.applies_from", d_long(S["applies_from"]))}, <a href="{S["source_url"]}" rel="noopener">vic.cfmeu.org/wages</a>. The project value is the head contract value, which the head contractor states; ask for it in writing before the first pay run on a new job.</p>''')

body += section("D", "Fares", "s-fares", f'''      <h2 id="fares">Fares and travel</h2>
      <p class="stamp">{m_("wages","travel_daily")} per day from {fig("wages.benefits_from", d_long(W["benefits_from"]))}</p>
      <p>The daily fares and travel allowance is a flat amount for each day the worker attends work, paid once a day no matter how many sites they visit (cl 27.5). It is not paid on an RDO, a day of leave or a public holiday not worked, and it is not paid to a worker who has the use of a company vehicle.</p>
      <p>Two situations change the amount:</p>
      <ul>
        <li><b>Sites outside the radial area.</b> The daily allowance is written for sites inside a 50 km radial area. For a site outside it, the agreement adds travel time outside ordinary hours at the ordinary rate, to the next quarter hour with a minimum of half an hour per return journey, and a per-kilometre amount for a worker using their own vehicle (cl 27.8). The union's allowances sheet lists that own-vehicle figure at {m_("allowances","own_vehicle_outside_km")} per kilometre, correct at {fig("allowances.correct_at", d_long(A["correct_at"]))}.</li>
        <li><b>Transfer between sites during the day.</b> Time spent travelling between sites in working hours is paid, with a minimum of 30 minutes, and a worker asked to use their own car for the transfer is paid {m_("allowances","own_vehicle_transfer_km")} per kilometre (cl 27.12, cl 27.13; own-vehicle figure from the {fig("allowances.correct_at", d_long(A["correct_at"]))} sheet).</li>
      </ul>
      <p>Apprentices' fares differ by year of apprenticeship, and a non-apprentice attending a training day keeps the day's fares (cl 27.14).</p>
      <p class="src">Source: CFMEU Victoria, <i>{W["source_title"]}</i> (other benefits from {fig("wages.benefits_from", d_long(W["benefits_from"]))}) and <i>{A["source_title"]}</i>, <a href="{W["source_url"]}" rel="noopener">vic.cfmeu.org/wages</a>.</p>''')

body += section("E", "Extras", "s-extras", f'''      <h2 id="extras">Multi-storey, leading hand and the rest</h2>
      <p class="stamp">Correct at {fig("allowances.correct_at", d_long(A["correct_at"]))}</p>
      <p>The allowances sheet runs to two pages. These are the ones a formwork, structure or civil subcontractor's office meets most weeks.</p>
      <div class="tbl"><table>
        <thead><tr><th>Allowance</th><th>Figure</th><th>Basis</th></tr></thead>
        <tbody>
          <tr><td>Multi-storey, start to 15th floor</td><td class="n">{m_("allowances","multistorey_1_15")} per hour</td><td>Per hour worked</td></tr>
          <tr><td>Multi-storey, floors 16 to 30</td><td class="n">{m_("allowances","multistorey_16_30")} per hour</td><td>Per hour worked</td></tr>
          <tr><td>Multi-storey, floors 31 to 45</td><td class="n">{m_("allowances","multistorey_31_45")} per hour</td><td>Per hour worked</td></tr>
          <tr><td>Multi-storey, floors 46 to 60</td><td class="n">{m_("allowances","multistorey_46_60")} per hour</td><td>Per hour worked</td></tr>
          <tr><td>Multi-storey, floors 61 and above</td><td class="n">{m_("allowances","multistorey_61_plus")} per hour</td><td>Per hour worked</td></tr>
          <tr><td>Leading hand, in charge of one person</td><td class="n">{m_("allowances","leading_hand_1")} per hour</td><td>Per hour, all purpose</td></tr>
          <tr><td>Leading hand, 2 to 5 people</td><td class="n">{m_("allowances","leading_hand_2_5")} per hour</td><td>Per hour, all purpose</td></tr>
          <tr><td>Leading hand, 6 to 10 people</td><td class="n">{m_("allowances","leading_hand_6_10")} per hour</td><td>Per hour, all purpose</td></tr>
          <tr><td>Leading hand, 11 or more</td><td class="n">{m_("allowances","leading_hand_11_plus")} per hour</td><td>Per hour, all purpose</td></tr>
          <tr><td>Overtime meal allowance</td><td class="n">{m_("wages","ot_meal")}</td><td>When 1.5 hours or more of overtime is worked on an ordinary day</td></tr>
          <tr><td>Living away from home</td><td class="n">{m_("wages","laha_week")} per week, {m_("wages","laha_day")} per day</td><td>Distant work</td></tr>
          <tr><td>Additional overnight allowance</td><td class="n">{m_("wages","overnight")} per night</td><td>Each night away from home</td></tr>
          <tr><td>Wet work, dirty work, cold work below 0&deg;C</td><td class="n">{m_("allowances","wet_dirty_cold")} per hour</td><td>Per hour on that work</td></tr>
          <tr><td>Hot work, 46 to 54&deg;C / over 54&deg;C</td><td class="n">{m_("allowances","hot_46_54")} / {m_("allowances","hot_over_54")} per hour</td><td>Per hour on that work</td></tr>
          <tr><td>Confined space, cutting tiles, insulation, roof repairs</td><td class="n">{m_("allowances","confined_space")} per hour</td><td>Per hour on that work</td></tr>
          <tr><td>Explosive powered tool</td><td class="n">{m_("allowances","explosive_tool_day")} per day</td><td>Per day</td></tr>
          <tr><td>Demolition, directly performing / working alongside</td><td class="n">{m_("allowances","demolition_direct")} / {m_("allowances","demolition_alongside")} per hour</td><td>Per hour</td></tr>
        </tbody>
      </table></div>
      <p class="src">Source: CFMEU Victoria, <i>{A["source_title"]}</i> (Appendix M and the allowances clause) and the <i>{W["source_title"]}</i> sheet, <a href="{W["source_url"]}" rel="noopener">vic.cfmeu.org/wages</a>. Leading hand rates shown are for a CW3 tradesperson supervising trades; the sheet points to the union for other classifications. The full sheet also covers swing scaffold, towers, heavy blocks, toxic substances, service core, the Altona area and more.</p>''')

body += section("F", "Payslip", "s-payslip", f'''      <h2 id="payslip">How they should land on a payslip</h2>
      <p>Every allowance above is either <b>per hour worked</b>, <b>per day attended</b> or <b>per week</b>, and the pay run has to carry that basis through to the payslip in units MYOB can price. The errors are always in the basis, not the arithmetic.</p>
      <ol class="steps">
        <li><b>Site allowance on ordinary hours only.</b> It is paid on every hour worked at the site, overtime included. A 10-hour day on a {m_("site_allowance","inner_new")} site is 10 units, not 8.</li>
        <li><b>One site allowance for a two-site day.</b> Each site's rate applies to the hours worked there. Split the day.</li>
        <li><b>Fares paid twice.</b> A worker who moves between two sites gets one daily fares allowance plus paid transfer time, not two allowances.</li>
        <li><b>Fares on days not attended.</b> No fares on an RDO, a sick day or an unworked public holiday, and none for a worker with a company vehicle.</li>
        <li><b>Multi-storey by the building, not the floor.</b> The rate follows the floor the worker is on; a job that reaches level 16 changes rate for the hours above it.</li>
        <li><b>Rates typed in by hand.</b> Hold every allowance as a named MYOB payroll category with the current figure, and change the figure in one place at each increase. The timesheet should only carry units.</li>
      </ol>
      <p>This is the reason PayKicker never holds a dollar rate: it classifies each hour and each day into the right category, exports units, and MYOB applies the figure you loaded from the union sheet. When the sheet changes, one number changes.</p>''')

body += section("G", "Demo", "demo", DEMO.format(related='<a href="/guides/cfmeu-rdo-calendar-2026">RDO calendar 2026 and the 36-hour week</a> &middot; <a href="/guides/cfmeu-eba-jobs-victoria">CFMEU EBA jobs and the list of EBA companies</a> &middot; <a href="/eba-payroll-software">EBA payroll software</a> &middot; <a href="/guides/">All guides</a>'))

page(SA_PATH, SA_TITLE, SA_OG, SA_DESC, article_ld(SA_PATH, SA_OG, SA_DESC, PUBLISHED, AS_AT), body)

# ---------------------------------------------------------------- CFMEU EBA jobs + employer list

from decimal import Decimal

JOBS_PATH = "/guides/cfmeu-eba-jobs-victoria"
N_EMP = E["count"]
LIST_GEN = E["list_generated"]
YEAR = date.fromisoformat(AS_AT).year
TRAVEL_5 = money(str(Decimal(W["travel_daily"]) * 5))
JOBS_TITLE = f"CFMEU EBA Jobs in Victoria {YEAR}: How to Get One, and Every Company With an EBA | PayKicker"
JOBS_OG = f"CFMEU EBA jobs: how to get one, and the list of {N_EMP} Victorian companies with a CFMEU EBA"
JOBS_DESC = (f"What a CFMEU EBA job pays in {YEAR} (CW3 {money(W['cw3_hour'])} an hour on a 36-hour week, 26 RDOs, super and Incolink), the tickets you need, "
             f"where EBA jobs are advertised, and a list of {N_EMP} companies with a CFMEU Victorian construction EBA, from the Fair Work Commission's register.")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


JOBS_FAQ = [
    ("What is a CFMEU EBA job?",
     "A job with an employer whose enterprise agreement was made with the CFMEU's Victorian Construction and General Division and approved by the Fair Work Commission. Pay, hours, RDOs, allowances, super and redundancy come from that agreement rather than the award. Head contractors sign a builders' agreement; subcontractors sign the pattern agreement for their trade."),
    (f"How much does a CFMEU EBA job pay in {YEAR}?",
     f"On the union's wage sheet, from {d_long(W['rates_from'])}, a CW3 tradesperson is on {money(W['cw3_hour'])} an hour ({money(W['cw3_week'])} for the 36-hour week), a CW2 on {money(W['cw2_hour'])} and a CW1 labourer on {money(W['cw1_hour'])}. On top come super of {money(W['super_weekly'])} a week or {W['super_pct']}% (whichever is greater), {money(W['incolink_weekly'])} a week into Incolink, {money(W['travel_daily'])} a day fares and travel, and site allowance on larger projects."),
    ("Do I have to join the union to get an EBA job?",
     "No. Union membership is voluntary under the Fair Work Act: an employer cannot require it and cannot refuse to hire you for being a member. The agreement covers every employee in the classifications it names, member or not. Whether to join is your decision."),
    ("How do I check whether a company has a CFMEU EBA?",
     "Search the employer's name in the Fair Work Commission's agreements database. A CFMEU Victorian construction agreement carries the union's division in its title. The Commission also publishes a spreadsheet of every agreement it approves each year; the list on this page is built from those spreadsheets."),
    ("Do labour hire companies have CFMEU EBAs?",
     "Yes. Labour hire firms sign the same pattern agreement as other subcontractors and supply EBA sites at EBA rates. Their most recent agreements reached nominal expiry in May 2026; an agreement keeps operating after that date until it is replaced or terminated, so the list marks those firms rather than dropping them."),
]


def faq_ld(items):
    ents = ",\n".join('    { "@type": "Question", "name": ' + json.dumps(q) + ', "acceptedAnswer": { "@type": "Answer", "text": ' + json.dumps(a) + ' } }' for q, a in items)
    return '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [\n' + ents + '\n  ]\n}\n</script>'


def faq_html(items):
    return '      <div class="faq-col">' + NL + NL.join(f'        <details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + NL + '      </div>'


JOBS_TOC = [("B", "what", "What an EBA job is"), ("C", "pay", "What it pays"), ("D", "how", "How to get one"), ("E", "check", "Check a company"),
            ("F", "list", f"The list: {N_EMP} companies"), ("G", "faq", "Questions"), ("H", "demo", "For the companies on the list")]

body = head_section("EBA jobs", f"CFMEU EBA jobs: how to get one, and the list of Victorian companies with a CFMEU EBA",
    f"An EBA job in Victorian construction means working for a company whose enterprise agreement was made with the CFMEU: a 36-hour week, 26 RDOs, union-negotiated rates, super and redundancy paid on top, and a wage sheet that says what everyone on the crew gets. This guide covers what those jobs pay right now, the tickets and search terms that get you one, how to check any company, and a list of {N_EMP} Victorian companies with a CFMEU construction EBA, taken from the Fair Work Commission's register.",
    JOBS_TOC,
    f'  <p class="note">Written 25 September 2026. Pay figures checked {fig("as_at", d_long(AS_AT))}; the company list is built from the Fair Work Commission\'s lists of approved agreements, generated {d_long(LIST_GEN)}, and refreshes automatically when the Commission updates them.</p>{NL}'
    + tiles([(m_("wages", "cw3_hour"), " /hr", f"CW3 tradesperson on the union sheet from {d_short(W['rates_from'])}"), ("36", " hrs", "the week, with 26 paid RDOs a year on top"),
             (f"{N_EMP:,}", None, "Victorian companies with a CFMEU construction EBA on the Commission's lists"), (str(len(E["sectors"])), None, "trades on the list, from head contractors to wind turbine erection")]))

body += section("B", "EBA", "s-what", '''      <h2 id="what">What a CFMEU EBA job is</h2>
      <p>EBA stands for enterprise bargaining agreement. In Victorian commercial construction it nearly always means an agreement between an employer and the CFMEU's Victorian Construction and General Division, approved by the Fair Work Commission and running for about three years. An EBA job is a job with one of those employers. Your pay, hours, allowances, super, redundancy and rostered days off come from the agreement, which sits well above the Building and Construction General On-site Award.</p>
      <p>Two kinds of company sign one:</p>
      <ul>
        <li><b>Head contractors (builders)</b> sign a builders' agreement that covers their own workforce: labourers, hoist and crane crews, carpenters, cleaners, traffic and the site team on the tools.</li>
        <li><b>Subcontractors</b> sign the pattern agreement for their trade: formwork, steelfixing, concrete placement, scaffolding, cranes, earthmoving, cladding and so on. The trade agreements share one skeleton and one wage sheet, so a CW3 carpenter is on the same base rate whichever EBA company employs them.</li>
      </ul>
      <p>What every one of them carries:</p>
      <ul>
        <li>A <b>36-hour week</b> worked as five 8-hour days, with the extra 4 hours banked toward <b>26 paid RDOs a year</b>. The <a href="/guides/cfmeu-rdo-calendar-2026">RDO calendar guide</a> has the dates and the accrual rules.</li>
        <li><b>Rates by classification</b>: CW1 for labourers and concrete gangs, CW2 for scaffolders, steel fixers and concrete finishers, CW3 for carpenters, plasterers, bricklayers and other tradespeople, with higher classifications above.</li>
        <li><b>Super and Incolink</b> paid by the employer on top of wages: super at a flat weekly amount or the legislated percentage, whichever is greater, and a weekly redundancy contribution to Incolink, which also carries income protection and portable sick leave for the industry.</li>
        <li><b>Allowances</b>: a daily fares and travel amount, site allowance on every hour worked on a project over the value threshold, multi-storey, leading hand and the rest of the sheet. The <a href="/guides/cfmeu-site-allowance-fares-travel-2026">site allowance guide</a> has the figures.</li>
        <li><b>Portable long service leave</b> through LeavePlus, the Victorian construction scheme, which follows you from employer to employer.</li>
        <li><b>Weather rules</b>: the union's own FAQ says work stops and the crew leaves site when the temperature reaches 35&deg;C at the nearest weather station, and nobody works in the rain.</li>
      </ul>''')

body += section("C", "Pay", "s-pay", f'''      <h2 id="pay">What an EBA job pays, dated</h2>
      <p class="stamp">Rates from {fig("wages.rates_from", d_long(W["rates_from"]))}</p>
      <p>These are the figures on the CFMEU Victoria on-site wage sheet. They move at each wage increase, so the date is part of the number.</p>
      <div class="tbl"><table>
        <thead><tr><th>Item</th><th>Figure</th><th>From</th></tr></thead>
        <tbody>
          <tr><td>CW3 carpenter, tile-layer, plasterer, bricklayer (100%)</td><td class="n">{m_("wages","cw3_hour")} per hour, {m_("wages","cw3_week")} per 36-hour week</td><td class="n">{fig("wages.rates_from", d_short(W["rates_from"]))}</td></tr>
          <tr><td>CW2 scaffolder, steel fixer, concrete finisher (96%)</td><td class="n">{m_("wages","cw2_hour")} per hour, {m_("wages","cw2_week")} per week</td><td class="n">{fig("wages.rates_from", d_short(W["rates_from"]))}</td></tr>
          <tr><td>CW1 trades labourer, concrete gang (92.4%)</td><td class="n">{m_("wages","cw1_hour")} per hour, {m_("wages","cw1_week")} per week</td><td class="n">{fig("wages.rates_from", d_short(W["rates_from"]))}</td></tr>
          <tr><td>Superannuation (employer pays on top)</td><td class="n">{m_("wages","super_weekly")} per week or {fig("wages.super_pct", W["super_pct"])}% of ordinary time earnings, whichever is greater</td><td class="n">{fig("wages.benefits_from", d_short(W["benefits_from"]))}</td></tr>
          <tr><td>Incolink redundancy contribution (employer pays on top)</td><td class="n">{m_("wages","incolink_weekly")} per week</td><td class="n">{fig("wages.benefits_from", d_short(W["benefits_from"]))}</td></tr>
          <tr><td>Fares and travel allowance</td><td class="n">{m_("wages","travel_daily")} per day attended</td><td class="n">{fig("wages.benefits_from", d_short(W["benefits_from"]))}</td></tr>
          <tr><td>Site allowance, Melbourne inner suburbs, new project over {millions(S["threshold_m"])}</td><td class="n">{m_("site_allowance","inner_new")} per hour worked</td><td class="n">{fig("site_allowance.applies_from", d_short(S["applies_from"]))}</td></tr>
        </tbody>
      </table></div>
      <p>Put together for a CW3 tradesperson attending five days on a 36-hour week: {m_("wages","cw3_week")} in wages plus {TRAVEL_5} fares and travel, before any site allowance, overtime or other allowances, with {m_("wages","super_weekly")} super and {m_("wages","incolink_weekly")} Incolink paid by the employer on top. Overtime is paid at penalty rates, weekends and public holidays higher again, and an RDO is a paid day off.</p>
      <p class="src">Source: CFMEU Victoria, <i>{W["source_title"]}</i> (rates from {fig("wages.rates_from", d_long(W["rates_from"]))}; other benefits from {fig("wages.benefits_from", d_long(W["benefits_from"]))}) and the site allowance sheet applying from {fig("site_allowance.applies_from", d_long(S["applies_from"]))}, <a href="{W["source_url"]}" rel="noopener">vic.cfmeu.org/wages</a>. Weekly rates are the hourly rate times 36. Apprentice and other classification rates are on the same sheet.</p>''')

body += section("D", "Getting in", "s-how", f'''      <h2 id="how">How to get a CFMEU EBA job</h2>
      <ol class="steps">
        <li><b>Get the tickets first.</b> Nobody sets foot on a Victorian construction site without a White Card (general construction induction). After that it is trade by trade: a high-risk work licence for dogging, rigging, scaffolding, crane and hoist work or a forklift; an elevated work platform ticket; confined space, working at heights and asbestos awareness for civil and demolition crews; a first aid certificate helps everywhere. Companies on the list will not look at a CV without the ticket the job needs.</li>
        <li><b>Know your classification.</b> A labourer starts at CW1, a scaffolder or steel fixer is CW2, a qualified tradesperson CW3. The wage sheet lists the rest. It decides your rate on day one, so read the table above before the interview and ask which classification the role is.</li>
        <li><b>Search the right words.</b> On SEEK and Indeed, search "EBA" with your trade: "EBA labourer", "EBA carpenter", "EBA formwork", "EBA rates". Adverts that say EBA rates, CFMEU EBA, RDOs or Incolink are the ones you want; an advert that quotes an award rate is not an EBA job.</li>
        <li><b>Go direct to the companies on the list.</b> Most subcontractors hire through the office and word of mouth long before an advert goes up. Pick your trade in the list below, then the careers page, a phone call to the office, or a CV dropped at the yard. If you are already on a site, ask the leading hands which subbies are putting people on.</li>
        <li><b>Use labour hire with an EBA to get a start.</b> Labour hire companies with their own CFMEU agreement supply EBA sites at EBA rates, and they are the fastest way in for someone without contacts. A good run through labour hire is how many people end up on a subcontractor's books.</li>
        <li><b>Apprentices and trainees.</b> The agreement sets apprentice rates and fares by year of apprenticeship. Group training organisations place apprentices with EBA companies, and the head contractors' agreements usually carry apprentice and trainee targets on major projects.</li>
        <li><b>Turn up with what they want.</b> Commercial experience over domestic, references from a foreman who will pick up the phone, your own hand tools for a trade role, reliability. EBA companies pay well and are held to the agreement on every hour, so they hire people who make the crew's day run.</li>
        <li><b>Check your first payslip.</b> Rate against your classification, super at the greater of the weekly amount or the percentage, Incolink, fares on every day attended, RDO accrual shown. The <a href="/guides/cfmeu-rdo-calendar-2026">RDO guide</a> and the <a href="/guides/cfmeu-site-allowance-fares-travel-2026">allowances guide</a> set out what should be there. If something is missing, raise it with the office first; the union's wage sheets are the reference both sides use.</li>
      </ol>
      <div class="aside chalk">
        <p><b>On union membership.</b> It is voluntary. Under the Fair Work Act an employer cannot require you to join and cannot refuse you work for being a member, and the agreement covers every employee in its classifications either way. Whether to join is your decision, and this page takes no side on it.</p>
      </div>''')

body += section("E", "Check", "s-check", f'''      <h2 id="check">How to check whether a company has an EBA</h2>
      <ul>
        <li><b>Search the Fair Work Commission's agreements database.</b> Go to <a href="{E["search_url"]}" rel="noopener">fwc.gov.au, find an agreement</a> and search the employer's name. A CFMEU Victorian construction agreement is titled <i>"[Company] and the CFMEU (Victorian Construction and General Division) Subcontractors [Trade] Enterprise Agreement 2024&nbsp;-&nbsp;2027"</i>, or for head contractors just <i>"[Company] and the CFMEU (Victorian Construction and General Division) Enterprise Agreement 2024&nbsp;-&nbsp;2027"</i>.</li>
        <li><b>Use the Commission's yearly lists.</b> It publishes a spreadsheet of every agreement approved each year at <a href="{E["source_url"]}" rel="noopener">fwc.gov.au</a>, with the title, approval date and nominal expiry. The list below is built from those spreadsheets.</li>
        <li><b>Mind the nominal expiry.</b> The current pattern agreements nominally expire on 2 July 2027. An agreement keeps operating past that date until it is replaced or terminated, so a company on an older agreement can still be an EBA employer; the list flags any agreement past its nominal expiry rather than dropping it.</li>
        <li><b>Other unions, other lists.</b> Electricians (ETU), plumbers (PPTEU) and metal trades (AMWU) work the same sites under agreements with their own unions. Those are not CFMEU agreements and are not on this list. Nor are the CFMEU's agreements in other states.</li>
        <li><b>Ask on site.</b> The union's delegates and the site office know which companies on the job are on an agreement. The CFMEU Victoria office is on (03) 9341 3444.</li>
      </ul>''')

sector_links = " ".join(f'<a href="#emp-{slug(s)}">{s} ({len(v)})</a>' for s, v in E["sectors"].items())
n_old = sum(1 for v in E["sectors"].values() for r in v if r.get("nominal_expiry_passed"))
sec_html = []
for s, v in E["sectors"].items():
    rows = NL.join(
        f'          <li data-s="{s}"><span class="nm">{r["name"].replace("&", "&amp;")}</span>'
        + (f'<span class="dt old">nominal expiry {d_short(r["expiry"])}</span>' if r.get("nominal_expiry_passed") else f'<span class="dt">from {d_short(r["operative"])}</span>')
        + '</li>' for r in v)
    sec_html.append(f'      <div class="emp-sec" id="emp-{slug(s)}">{NL}        <h3>{s} <span class="n">({len(v)})</span></h3>{NL}        <ul class="emp">{NL}{rows}{NL}        </ul>{NL}      </div>')
list_inner = f'''      <h2 id="list">The list: {N_EMP} Victorian companies with a CFMEU EBA</h2>
      <p class="stamp">Commission lists generated {d_long(LIST_GEN)}</p>
      <p>Every company below is party to an enterprise agreement with the CFMEU (Victorian Construction and General Division) on the Fair Work Commission's lists of approved agreements, within or just past its nominal term, grouped by the trade named in the agreement's title. Names are as registered with the Commission, which is not always the trading name on the ute. The date is the day the agreement came into operation.</p>
      <form class="emp-filter" role="search">
        <label for="emp-q">Find a company or a trade</label>
        <input id="emp-q" type="search" autocomplete="off" placeholder="Type part of a name, or a trade such as formwork">
        <span class="cnt" id="emp-n" aria-live="polite">{N_EMP} companies</span>
      </form>
      <p class="emp-jump">{sector_links}</p>
{NL.join(sec_html)}
      <p class="src">Source: Fair Work Commission, <i>List of agreements</i> spreadsheets for {", ".join(str(f["year"]) for f in E["files"])} (<a href="{E["source_url"]}" rel="noopener">fwc.gov.au, find an agreement</a>), filtered to agreements whose title names the CFMEU's Victorian Construction and General Division and whose nominal expiry is no more than a year past. {n_old} of the {N_EMP} are past nominal expiry and marked in orange. Head contractors whose agreement title does not carry the union's name, and agreements approved after the Commission generated its list, are not captured. Companies that have changed name or closed since approval will still appear until the Commission's list changes.</p>'''
body += section("F", "The list", "s-list", list_inner)

body += section("G", "FAQ", "s-faq", f'''      <h2 id="faq">Questions people ask</h2>
{faq_html(JOBS_FAQ)}''')

body += section("H", "Employers", "demo", DEMO_JOBS.format(related='<a href="/guides/cfmeu-rdo-calendar-2026">RDO calendar 2026 and the 36-hour week</a> &middot; <a href="/guides/cfmeu-site-allowance-fares-travel-2026">Site allowance, fares and travel 2026</a> &middot; <a href="/eba-payroll-software">EBA payroll software</a> &middot; <a href="/guides/">All guides</a>'))

jobs_html_extra = '<script src="/js/employers.js" defer></script>'
page(JOBS_PATH, JOBS_TITLE, JOBS_OG, JOBS_DESC, article_ld(JOBS_PATH, JOBS_OG, JOBS_DESC, PUBLISHED, max(AS_AT, LIST_GEN)) + NL + faq_ld(JOBS_FAQ) + NL + jobs_html_extra, body)

# ---------------------------------------------------------------- Pay calculator

CALC_PATH = "/guides/cfmeu-eba-pay-calculator"
CALC_TITLE = f"CFMEU EBA Pay Calculator {YEAR}: Price a Week on the Tools | PayKicker"
CALC_OG = f"CFMEU EBA pay calculator {YEAR}: a week on the tools, priced by the agreement"
CALC_DESC = (f"Free CFMEU EBA pay calculator for Victorian construction. Enter the week's hours, site allowance and leading hand band and see ordinary pay on the 36-hour week, "
             f"double-time overtime, weekend and public holiday rates, fares, super and Incolink, from the union's {d_short(W['rates_from'])} sheet.")

# figures for the calculator script, generated so the page never holds a rate the data file does not
site_opts = [("0", "No site allowance (project under the threshold)"), (S["inner_new"], f"Melbourne inner suburbs, new project ({money(S['inner_new'])})"),
             (S["inner_reno"], f"Melbourne inner suburbs, renovation ({money(S['inner_reno'])})")]
site_opts += [(b["rate"], f"{millions(b['lo_m'])} to {millions(b['hi_m'])} ({money(b['rate'])})") for b in S["bands"]]
site_opts += [(p["rate"], f"{p['name']} ({money(p['rate'])})") for p in S["projects"]]
ms_opts = [("0", "Not a multi-storey job")] + [(A[k], f"{lbl} ({money(A[k])})") for k, lbl in (("multistorey_1_15", "Floors 1 to 15"), ("multistorey_16_30", "Floors 16 to 30"), ("multistorey_31_45", "Floors 31 to 45"), ("multistorey_46_60", "Floors 46 to 60"), ("multistorey_61_plus", "Floors 61 and above"))]
lh_opts = [("0", "Not a leading hand")] + [(A[k], f"{lbl} ({money(A[k])})") for k, lbl in (("leading_hand_1", "In charge of 1"), ("leading_hand_2_5", "In charge of 2 to 5"), ("leading_hand_6_10", "In charge of 6 to 10"), ("leading_hand_11_plus", "In charge of 11 or more"))]
calc_data = {"as_at": AS_AT, "rates_from": W["rates_from"], "rates": {"cw1": float(W["cw1_hour"]), "cw2": float(W["cw2_hour"]), "cw3": float(W["cw3_hour"])},
             "super_weekly": float(W["super_weekly"]), "super_pct": float(W["super_pct"]), "incolink": float(W["incolink_weekly"]), "travel": float(W["travel_daily"]), "ot_meal": float(W["ot_meal"])}
io.open(os.path.join(PUB, "js", "calc-data.js"), "w", encoding="utf-8", newline="\n").write(
    "/* Generated by scripts/cfmeu/build_guides.py from data/cfmeu-figures.json. Do not edit. */\nwindow.CFMEU_CALC = " + json.dumps(calc_data, indent=1) + ";\n")
print("wrote public/js/calc-data.js")


def opts(pairs, selected=None):
    return "".join(f'<option value="{v}"{" selected" if v == selected else ""}>{t}</option>' for v, t in pairs)


KINDS = [("ord", "Ordinary day"), ("rdo", "RDO taken"), ("rdoc", "RDO worked, crew consulted"), ("rdou", "RDO worked, not consulted"), ("ph", "Public holiday, not worked"), ("phw", "Public holiday worked"), ("absent", "Not attended")]
day_rows = NL.join(f'''          <div class="crow"><label for="h-{d}">{name}</label><select id="k-{d}" aria-label="{name} day type">{opts(KINDS, "ord")}</select><input id="h-{d}" type="number" inputmode="decimal" min="0" max="16" step="0.5" value="8" aria-label="{name} hours"></div>'''
                   for d, name in (("mon", "Monday"), ("tue", "Tuesday"), ("wed", "Wednesday"), ("thu", "Thursday"), ("fri", "Friday")))

CALC_FAQ = [
    ("Is this the official CFMEU pay calculator?",
     "No. It is an independent calculator built by PayKicker from the CFMEU Victoria wage sheets and the clauses of the 2024 to 2027 on-site construction agreements. The union's published sheets and the agreement itself are the source; if they disagree with this page, they win."),
    ("What does the calculator include?",
     f"Ordinary hours on the 36-hour week (8 a day paid as 7.2 with 0.8 banked toward RDOs), overtime at double time, Saturday and Sunday at double time with a four-hour minimum, public holidays and unconsulted worked RDOs at 250% with a four-hour minimum, site allowance and multi-storey per hour worked, the leading hand allowance as an all-purpose rate, fares and travel per day attended, the overtime meal allowance, super at the greater of {money(W['super_weekly'])} a week or {W['super_pct']}% of ordinary-time earnings, and the {money(W['incolink_weekly'])} Incolink contribution."),
    ("What does it leave out?",
     "Casual loadings, shiftwork, apprentice rates, distant work and living away from home, wet weather and inclement weather payments, the Christmas shutdown, annual and personal leave, redundancy and termination, and any company-specific arrangement. Hours are taken as worked inside the 6am to 6pm span; an early start or late finish outside it is overtime under the agreement and is not modelled here."),
    ("Where do the figures come from?",
     f"The CFMEU Victoria on-site wage sheet (rates from {d_long(W['rates_from'])}, other benefits from {d_long(W['benefits_from'])}), the on-site allowances sheet correct at {d_long(A['correct_at'])} and the site allowance sheet applying from {d_long(S['applies_from'])}. The figures on this page are checked against the union's sheets every week and change when they change."),
]

CALC_TOC = [("B", "week", "Your week"), ("C", "result", "What the week pays"), ("D", "rules", "The rules applied"), ("E", "faq", "Questions"), ("F", "demo", "Run it for the whole crew")]

body = head_section("Calculator", f"CFMEU EBA pay calculator {YEAR}: a week on the tools, priced by the agreement",
    f"Enter a week's hours, the site and the crew you lead, and this page prices it the way a CFMEU Victorian construction EBA does: 8 ordinary hours a day paid as 7.2 with 0.8 banked, every overtime hour at double time, weekends and holidays at their penalties, site allowance on every hour worked, fares on every day attended, and the super and Incolink the employer pays on top. Figures are the union's, dated {fig('as_at', d_long(AS_AT))}.",
    CALC_TOC,
    f'  <p class="note">Independent, not the union\'s. Rates from {fig("wages.rates_from", d_long(W["rates_from"]))}; allowances correct at {fig("allowances.correct_at", d_long(A["correct_at"]))}; site allowance from {fig("site_allowance.applies_from", d_long(S["applies_from"]))}. Full-time weekly hire, day work inside 6am to 6pm; casuals, shiftwork and apprentices are not modelled.</p>{NL}')

body += section("B", "Your week", "s-week", f'''      <h2 id="week">Your week</h2>
      <form class="calc chalk" id="calc" novalidate>
        <div class="cgrid">
          <div class="cfield"><label for="cls">Classification</label><select id="cls">{opts([("cw3", f"CW3 tradesperson ({money(W['cw3_hour'])})"), ("cw2", f"CW2 scaffolder, steel fixer, concrete finisher ({money(W['cw2_hour'])})"), ("cw1", f"CW1 labourer, concrete gang ({money(W['cw1_hour'])})"), ("custom", "Another rate (type it in)")], "cw3")}</select></div>
          <div class="cfield"><label for="rate">Hourly rate</label><input id="rate" type="number" inputmode="decimal" min="0" step="0.01" value="{W["cw3_hour"]}" disabled></div>
          <div class="cfield"><label for="site">Site allowance</label><select id="site">{opts(site_opts, "0")}</select></div>
          <div class="cfield"><label for="ms">Multi-storey</label><select id="ms">{opts(ms_opts, "0")}</select></div>
          <div class="cfield"><label for="lh">Leading hand</label><select id="lh">{opts(lh_opts, "0")}</select></div>
        </div>
        <div class="cdays">
          <div class="crow chead"><span>Day</span><span>What kind of day</span><span>Hours</span></div>
{day_rows}
          <div class="crow"><label for="h-sat">Saturday</label><span class="cnote">Double time, 4-hour minimum</span><input id="h-sat" type="number" inputmode="decimal" min="0" max="16" step="0.5" value="0" aria-label="Saturday hours"></div>
          <div class="crow"><label for="h-sun">Sunday</label><span class="cnote">Double time, 4-hour minimum</span><input id="h-sun" type="number" inputmode="decimal" min="0" max="16" step="0.5" value="0" aria-label="Sunday hours"></div>
        </div>
        <p class="cfoot"><button type="reset" class="outline" id="calc-reset">Start again</button><span>Hours are the hours on the tools, meal break excluded. Enter 0 for a day not attended, or pick "Not attended".</span></p>
      </form>''')

body += section("C", "The week", "s-result", f'''      <h2 id="result">What the week pays</h2>
      <div class="tiles" aria-live="polite">
        <div class="tile"><b id="t-gross">$0.00</b><span class="cap">gross wages and allowances for the week</span></div>
        <div class="tile"><b id="t-super">$0.00</b><span class="cap" id="t-super-how">super</span></div>
        <div class="tile"><b id="t-inco">$0.00</b><span class="cap">Incolink redundancy contribution, paid by the employer</span></div>
        <div class="tile"><b id="t-bank">+0.0 hrs</b><span class="cap" id="t-bank-how">banked toward the next RDO</span></div>
      </div>
      <div class="tbl"><table>
        <thead><tr><th>Line on the payslip</th><th>Units</th><th>Rate</th><th>Amount</th></tr></thead>
        <tbody id="calc-lines"></tbody>
        <tfoot><tr><th>Cost to the employer for the week, wages plus super and Incolink</th><th></th><th></th><th class="n" id="t-total">$0.00</th></tr></tfoot>
      </table></div>
      <p class="src">Ordinary hourly rate used, including any leading hand allowance: <span id="t-ordrate">$0.00</span>. Weekly figures assume a full-time weekly hire employee. Ordinary-time earnings for super are the ordinary hours and the site and multi-storey allowances on those hours; if your fund or agreement counts more, the super figure moves. Site allowance is the head contract band; ask the head contractor for the project value in writing before the first pay run.</p>''')

body += section("D", "Rules", "s-rules", '''      <h2 id="rules">The rules the calculator applies</h2>
      <ol class="steps">
        <li><b>The 36-hour week.</b> Ordinary hours are the first 8 worked between 6am and 6pm, Monday to Friday. Each 8-hour day pays 7.2 hours and banks 0.8 toward an RDO, so five days pay 36 (cl 36.1, 36.2, 38.1).</li>
        <li><b>Overtime is double time.</b> Every hour past 8 on a weekday is paid at 200% of the ordinary rate. There is no time-and-a-half step in this agreement (cl 39.3).</li>
        <li><b>Weekends.</b> Saturday and Sunday are double time with a minimum of four hours' pay for attending (cl 39.8).</li>
        <li><b>Public holidays and RDOs.</b> A holiday not worked is paid as an ordinary day. A holiday worked is 250% with a four-hour minimum (cl 39.9). An RDO taken is paid from the bank. An RDO worked with the crew consulted in writing is ordinary money and the bank is kept; without consultation it is 250% with the four-hour minimum (cl 38.8).</li>
        <li><b>Allowances.</b> Site allowance and multi-storey are per hour worked, overtime included (App C para 4; cl 27.3). The leading hand allowance is all-purpose, so it rides into overtime and penalties. Fares and travel is one amount per day attended, not on an RDO or a holiday not worked (cl 27.5). The meal allowance is paid when 1.5 hours or more of overtime follows the normal finish (cl 39.4).</li>
        <li><b>On top of wages.</b> Super at the greater of the weekly amount or the percentage of ordinary-time earnings, and the weekly Incolink contribution, both from the union's sheet.</li>
      </ol>
      <p>The <a href="/guides/cfmeu-rdo-calendar-2026">RDO guide</a> and the <a href="/guides/cfmeu-site-allowance-fares-travel-2026">allowances guide</a> set out each of these with the figures dated.</p>''')

body += section("E", "FAQ", "s-faq", f'''      <h2 id="faq">Questions</h2>
{faq_html(CALC_FAQ)}''')

body += section("F", "Demo", "demo", DEMO.format(related='<a href="/guides/cfmeu-rdo-calendar-2026">RDO calendar 2026 and the 36-hour week</a> &middot; <a href="/guides/cfmeu-site-allowance-fares-travel-2026">Site allowance, fares and travel 2026</a> &middot; <a href="/guides/cfmeu-eba-jobs-victoria">CFMEU EBA jobs and the list of EBA companies</a> &middot; <a href="/guides/">All guides</a>')
    .replace("<h2>See your own agreement running in it</h2>", "<h2>Run it for the whole crew, every week</h2>")
    .replace("PayKicker encodes the clauses above once and applies them to every timesheet,", "This page prices one worker's week from typed hours. PayKicker applies the same clauses to every timesheet the crew taps in on site,"))

calc_extra = '<script src="/js/calc-data.js" defer></script>' + NL + '<script src="/js/calc.js" defer></script>'
page(CALC_PATH, CALC_TITLE, CALC_OG, CALC_DESC, article_ld(CALC_PATH, CALC_OG, CALC_DESC, PUBLISHED, AS_AT) + NL + faq_ld(CALC_FAQ) + NL + calc_extra, body)

# ---------------------------------------------------------------- Index

IDX_PATH = "/guides/"
IDX_TITLE = "CFMEU EBA Guides for Subcontractors' Offices | PayKicker"
IDX_OG = "CFMEU EBA guides for the subcontractor's office"
IDX_DESC = "Plain-English guides to running payroll under a CFMEU Victorian construction EBA: the 36-hour week and RDO calendar, site allowance, fares and travel, with dated figures and clause references."
IDX_LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "CFMEU EBA guides for the subcontractor's office",
  "url": "https://paykicker.com.au/guides/",
  "description": "''' + IDX_DESC + '''",
  "inLanguage": "en-AU",
  "isPartOf": { "@id": "https://paykicker.com.au/#website" },
  "publisher": { "@id": "https://paykicker.com.au/#organization" },
  "hasPart": [
    { "@type": "Article", "headline": "''' + RDO_OG + '''", "url": "https://paykicker.com.au/guides/cfmeu-rdo-calendar-2026" },
    { "@type": "Article", "headline": "''' + SA_OG + '''", "url": "https://paykicker.com.au/guides/cfmeu-site-allowance-fares-travel-2026" },
    { "@type": "Article", "headline": "''' + JOBS_OG + '''", "url": "https://paykicker.com.au/guides/cfmeu-eba-jobs-victoria" },
    { "@type": "WebPage", "name": "''' + CALC_OG + '''", "url": "https://paykicker.com.au/guides/cfmeu-eba-pay-calculator" }
  ]
}
</script>'''

body = head_section("Guides", "CFMEU EBA guides for the subcontractor's office",
    "The agreement is 186 pages and the office needs about twelve of them every week. These guides take one clause cluster at a time, in plain English, with the union's current published figures and the date each one applies from. Written by people who run CFMEU EBA crews and the payroll behind them.",
    None,
    f'''  <div class="gcards">
    <a class="gcard chalk" href="/guides/cfmeu-rdo-calendar-2026">
      <div class="big">26<small>RDOs a year</small></div>
      <h2>{RDO_OG}</h2>
      <p>The {Y0} on-site RDO dates as month grids, how 0.8 of an hour a day becomes 26 days off, what a worked RDO pays with and without consultation, and the four ways payroll gets the bank wrong.</p>
      <p class="when">Figures dated {d_short(W["rates_from"])} and {d_short(W["benefits_from"])}. Checked {fig("as_at", d_long(AS_AT))}.</p>
      <span class="go">Read the guide <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></span>
    </a>
    <a class="gcard chalk" href="/guides/cfmeu-site-allowance-fares-travel-2026">
      <div class="big">{m_("site_allowance","inner_new")}<small>an hour, inner Melbourne site allowance</small></div>
      <h2>{SA_OG}</h2>
      <p>The site allowance bands from {fig("site_allowance.applies_from", d_long(S["applies_from"]))}, the {m_("wages","travel_daily")} daily fares allowance and its radial-area rules, multi-storey and leading hand rates, and how each one should land on a payslip.</p>
      <p class="when">Figures dated {d_short(A["correct_at"])} and {d_short(S["applies_from"])}. Checked {fig("as_at", d_long(AS_AT))}.</p>
      <span class="go">Read the guide <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></span>
    </a>
    <a class="gcard chalk" href="/guides/cfmeu-eba-jobs-victoria">
      <div class="big">{N_EMP:,}<small>companies with a CFMEU EBA</small></div>
      <h2>{JOBS_OG}</h2>
      <p>What an EBA job pays right now, the tickets and search terms that get you one, how to check any company on the Fair Work Commission's register, and the full list by trade. For workers looking for a start, and for the companies on the list.</p>
      <p class="when">Company list from the Commission's lists generated {d_short(LIST_GEN)}. Pay figures checked {fig("as_at", d_long(AS_AT))}.</p>
      <span class="go">Read the guide <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></span>
    </a>
    <a class="gcard chalk" href="/guides/cfmeu-eba-pay-calculator">
      <div class="big">{m_("wages","cw3_week")}<small>a 36-hour week at CW3, before allowances</small></div>
      <h2>{CALC_OG}</h2>
      <p>Type a week's hours, pick the site allowance and the leading hand band, and see the payslip lines: ordinary time, double-time overtime, weekend and holiday rates, fares, super and Incolink.</p>
      <p class="when">Rates from {d_short(W["rates_from"])}. Checked {fig("as_at", d_long(AS_AT))}.</p>
      <span class="go">Open the calculator <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><use href="#i-arrow"/></svg></span>
    </a>
  </div>
  <p class="note">More guides follow: overtime, weekends and inclement weather; public holidays, Cup Day and daily hire. Every figure on these pages carries its source and date, and a weekly job checks the union's published sheets and the Commission's lists; when a source changes, the page changes.</p>''')

body += section("B", "Demo", "demo", DEMO.format(related='<a href="/eba-payroll-software">EBA payroll software</a> &middot; <a href="/digital-dayworks-docket">Digital dayworks dockets</a>'))

page(IDX_PATH, IDX_TITLE, IDX_OG, IDX_DESC, IDX_LD, body)

# ---------------------------------------------------------------- landing page figures + sitemap

def replace_figs(path):
    """Refresh <span data-fig="..."> contents on a hand-written page."""
    p = os.path.join(PUB, path)
    s = io.open(p, "r", encoding="utf-8", newline="").read()
    values = {
        "wages.travel_daily": money(W["travel_daily"]),
        "wages.super_weekly": money(W["super_weekly"]),
        "wages.super_pct": W["super_pct"],
        "wages.benefits_from": d_long(W["benefits_from"]),
    }
    def sub(m):
        key = m.group(1)
        return f'<span data-fig="{key}">{values[key]}</span>' if key in values else m.group(0)
    s2 = re.sub(r'<span data-fig="([^"]+)">[^<]*</span>', sub, s)
    if s2 != s:
        io.open(p, "w", encoding="utf-8", newline="").write(s2)
        print("refreshed figures in", path)


replace_figs("eba-payroll-software.html")


def stamp_css():
    """Version the shared stylesheet link on every page so a CSS change reaches cached browsers (Cloudflare serves
    /css/setout.css with a one-day max-age and a week of stale-while-revalidate)."""
    import hashlib, glob
    v = hashlib.sha256(open(os.path.join(PUB, "css", "setout.css"), "rb").read()).hexdigest()[:8]
    for f in glob.glob(os.path.join(PUB, "**", "*.html"), recursive=True):
        h = io.open(f, "r", encoding="utf-8", newline="").read()
        h2 = re.sub(r'href="/css/setout\.css(\?v=[0-9a-f]+)?"', f'href="/css/setout.css?v={v}"', h)
        if h2 != h:
            io.open(f, "w", encoding="utf-8", newline="").write(h2)
            print("css version", v, "->", os.path.relpath(f, ROOT))


stamp_css()

sm = os.path.join(PUB, "sitemap.xml")
s = io.open(sm, "r", encoding="utf-8", newline="").read()
for u, when in (("/guides/", max(AS_AT, LIST_GEN)), ("/guides/cfmeu-rdo-calendar-2026", AS_AT), ("/guides/cfmeu-site-allowance-fares-travel-2026", AS_AT),
                ("/guides/cfmeu-eba-jobs-victoria", max(AS_AT, LIST_GEN)), ("/guides/cfmeu-eba-pay-calculator", AS_AT), ("/eba-payroll-software", AS_AT)):
    s = re.sub(r'(<loc>https://paykicker\.com\.au' + re.escape(u) + r'</loc>\s*<lastmod>)[0-9-]+(</lastmod>)', lambda m, when=when: m.group(1) + when + m.group(2), s)
io.open(sm, "w", encoding="utf-8", newline="").write(s)
print("sitemap lastmod ->", AS_AT)
print("done")
