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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Stencil+Display:wght@700;800&family=Archivo:wght@400;500;600&family=Courier+Prime:wght@400;700&display=swap">
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
  @media(max-width:640px){{.tbl td.n{{white-space:normal}} .tbl th,.tbl td{{font-size:14px;padding-right:0}}}}
</style>
</head>
<body>
'''


def section(letter, name, sid, inner):
    return (f'<section class="sheet prose" id="{sid}">{NL}  <div class="wrap">{NL}'
            f'    <div class="mark"><span class="bub" aria-hidden="true">{letter}</span><span class="name">{name}</span><span class="string" aria-hidden="true"></span></div>{NL}'
            f'    <div class="body">{NL}{inner}{NL}      <div class="rule" aria-hidden="true"></div>{NL}    </div>{NL}  </div>{NL}</section>{NL}{NL}')


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

TAIL = NL + "</main>" + NL + NL + FOOT + NL + NL + "</body>" + NL + "</html>" + NL


def page(path, title, ogtitle, desc, jsonld, body):
    html = HEAD.format(title=title, ogtitle=ogtitle, desc=desc, path=path, jsonld=jsonld) + NL + SVG + NL + NL + NAV + NL + NL + "<main>" + NL + body + TAIL
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
    f'  <p class="note">Written 25 September 2026, figures checked {fig("as_at", d_long(AS_AT))}, for the 2024&ndash;2027 agreements. Clause numbers are the formwork subcontractors\' agreement; the crane, steelfixing and other trade agreements share the same skeleton with their own numbering.</p>{NL}')

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
      <div class="cal">
{rows}
      </div>
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
      <ol>
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

body += section("H", "Demo", "demo", DEMO.format(related='<a href="/guides/cfmeu-site-allowance-fares-travel-2026">Site allowance, fares and travel 2026</a> &middot; <a href="/eba-payroll-software">EBA payroll software</a> &middot; <a href="/guides/">All guides</a>'))

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
    f'  <p class="note">Written 25 September 2026, figures checked {fig("as_at", d_long(AS_AT))}, for the 2024&ndash;2027 agreements. Figures are the CFMEU Victoria sheets\' and are dated; clause numbers are the formwork subcontractors\' agreement.</p>{NL}')

body += section("B", "Site allowance", "s-site", f'''      <h2 id="site">What site allowance is, and when it applies</h2>
      <p>Site allowance is an hourly amount paid for every hour worked on a qualifying project, ordinary and overtime alike (Appendix C, para 4). It compensates for the conditions of a large site, so it is set by the project, not the worker: everyone on the job gets the same figure, and a worker on two sites in one day earns each site's allowance on the hours worked there.</p>
      <ul>
        <li><b>The threshold.</b> Site allowance applies to projects at or above the indexed value threshold, which is {fig("site_allowance.threshold_m", millions(S["threshold_m"]))} on the table that applies from {fig("site_allowance.applies_from", d_long(S["applies_from"]))}. Below that, the Award's special rates apply instead (Appendix C, paras 2 and 3).</li>
        <li><b>New work or renovation.</b> New projects and renovation, restoration or refurbishment projects carry different rates. Where a job mixes the two, the new-projects rate applies when the value of the new work is more than 33% of the total project value.</li>
        <li><b>Where the site is.</b> Melbourne inner suburbs and shopping centres have one flat rate for projects up to {fig("site_allowance.inner_cap_m", millions(S["inner_cap_m"]))}; elsewhere the rate steps up through value bands.</li>
        <li><b>Indexation.</b> Both the rates and the value bands move with Melbourne CPI each year, so the band a project sits in can change mid-job.</li>
      </ul>''')

band_rows = NL.join(f'          <tr><td>{millions(b["lo_m"])} to {millions(b["hi_m"])}</td><td class="n">{money(b["rate"])} per hour</td></tr>' for b in S["bands"])
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
      <div class="tbl"><table>
        <thead><tr><th>Project value</th><th>Site allowance</th></tr></thead>
        <tbody>
{band_rows}
        </tbody>
      </table></div>
      <h3>Project-specific rates</h3>
      <div class="tbl"><table>
        <thead><tr><th>Project</th><th>Site allowance</th></tr></thead>
        <tbody>
{proj_rows}
        </tbody>
      </table></div>
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
      <ol>
        <li><b>Site allowance on ordinary hours only.</b> It is paid on every hour worked at the site, overtime included. A 10-hour day on a {m_("site_allowance","inner_new")} site is 10 units, not 8.</li>
        <li><b>One site allowance for a two-site day.</b> Each site's rate applies to the hours worked there. Split the day.</li>
        <li><b>Fares paid twice.</b> A worker who moves between two sites gets one daily fares allowance plus paid transfer time, not two allowances.</li>
        <li><b>Fares on days not attended.</b> No fares on an RDO, a sick day or an unworked public holiday, and none for a worker with a company vehicle.</li>
        <li><b>Multi-storey by the building, not the floor.</b> The rate follows the floor the worker is on; a job that reaches level 16 changes rate for the hours above it.</li>
        <li><b>Rates typed in by hand.</b> Hold every allowance as a named MYOB payroll category with the current figure, and change the figure in one place at each increase. The timesheet should only carry units.</li>
      </ol>
      <p>This is the reason PayKicker never holds a dollar rate: it classifies each hour and each day into the right category, exports units, and MYOB applies the figure you loaded from the union sheet. When the sheet changes, one number changes.</p>''')

body += section("G", "Demo", "demo", DEMO.format(related='<a href="/guides/cfmeu-rdo-calendar-2026">RDO calendar 2026 and the 36-hour week</a> &middot; <a href="/eba-payroll-software">EBA payroll software</a> &middot; <a href="/guides/">All guides</a>'))

page(SA_PATH, SA_TITLE, SA_OG, SA_DESC, article_ld(SA_PATH, SA_OG, SA_DESC, PUBLISHED, AS_AT), body)

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
    { "@type": "Article", "headline": "''' + SA_OG + '''", "url": "https://paykicker.com.au/guides/cfmeu-site-allowance-fares-travel-2026" }
  ]
}
</script>'''

body = head_section("Guides", "CFMEU EBA guides for the subcontractor's office",
    "The agreement is 186 pages and the office needs about twelve of them every week. These guides take one clause cluster at a time, in plain English, with the union's current published figures and the date each one applies from. Written by people who run CFMEU EBA crews and the payroll behind them.",
    None,
    f'''  <ul class="guide-list">
    <li>
      <h2><a href="/guides/cfmeu-rdo-calendar-2026">{RDO_OG}</a></h2>
      <p>The {Y0} on-site RDO dates, how 0.8 of an hour a day becomes 26 days off, what a worked RDO pays with and without consultation, and the four ways payroll gets the bank wrong.</p>
      <p class="when">Figures dated {d_short(W["rates_from"])} and {d_short(W["benefits_from"])}. Checked {fig("as_at", d_long(AS_AT))}.</p>
    </li>
    <li>
      <h2><a href="/guides/cfmeu-site-allowance-fares-travel-2026">{SA_OG}</a></h2>
      <p>The site allowance table from {fig("site_allowance.applies_from", d_long(S["applies_from"]))}, the {m_("wages","travel_daily")} daily fares allowance and its radial-area rules, multi-storey and leading hand rates, and how each one should land on a payslip.</p>
      <p class="when">Figures dated {d_short(A["correct_at"])} and {d_short(S["applies_from"])}. Checked {fig("as_at", d_long(AS_AT))}.</p>
    </li>
  </ul>
  <p class="note">More guides follow: overtime, weekends and inclement weather; public holidays, Cup Day and daily hire. Every figure on these pages carries its source and date, and a weekly job checks the union's published sheets; when a sheet changes, the page changes.</p>''')

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

sm = os.path.join(PUB, "sitemap.xml")
s = io.open(sm, "r", encoding="utf-8", newline="").read()
for u in ("/guides/", "/guides/cfmeu-rdo-calendar-2026", "/guides/cfmeu-site-allowance-fares-travel-2026", "/eba-payroll-software"):
    s = re.sub(r'(<loc>https://paykicker\.com\.au' + re.escape(u) + r'</loc>\s*<lastmod>)[0-9-]+(</lastmod>)', lambda m: m.group(1) + AS_AT + m.group(2), s)
io.open(sm, "w", encoding="utf-8", newline="").write(s)
print("sitemap lastmod ->", AS_AT)
print("done")
