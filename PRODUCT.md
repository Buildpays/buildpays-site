# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Confirmed 25 Sep 2026 (TR): the homepage must convince two people equally.

- **The owner or director** of a Melbourne construction subcontractor (formwork, structure, steelfixing, cranes, civil) whose workforce is on a CFMEU Victoria enterprise agreement, typically 20 to 200 people on the tools. They carry the back-pay, dispute and audit risk and decide to book the demo.
- **The office or payroll manager** who runs the weekly pay cycle out of MYOB and a spreadsheet, chases timesheets and dockets, and brings the tool to the boss.

Secondary, not a homepage audience: workers and leading hands use the phone app (roster SMS, one-tap timesheets, dockets); site supervisors and client reps countersign dockets.

## Product Purpose

PayKicker is a site-operations and EBA-payroll platform for Australian construction subcontractors. It rosters the crew each morning, gates rostering on inductions and tickets, collects one-tap timesheets, builds dayworks dockets from real hours (plus plant and materials by quantity) signed on site or by secure link, generates public-holiday and RDO pay lines automatically, and exports a MYOB-ready payroll file with EBA classifications and job codes applied. MYOB stays the system of record and holds the rates.

Success on the site is a booked demo: a subbie brings their enterprise agreement and a recent pay run to a 30-minute demo, then runs a free pilot alongside their current process until the MYOB file matches to the cent. There is deliberately no self-serve trial.

## Positioning

The mechanism a generic payroll or timesheet tool cannot truthfully copy: every clause of a CFMEU Victoria construction EBA (36-hour week and RDO accrual, flat double-time overtime, weekend minimums, per-project site allowance, daily fares and travel, casual loading, inclement weather, public holidays) is encoded once and applied to every timesheet, and the same hours flow into signed client dockets. Docket-to-pay, not docket-to-invoice.

Founder story, confirmed usable on the site (TR, 25 Sep 2026): PayKicker was built by someone who runs CFMEU EBA crews in Melbourne, not by a payroll company guessing at construction. **Open:** the founder's name and trade to print alongside the story are not yet confirmed; do not invent them.

## Operating Context

- Melbourne, Victoria. Pay cycle is weekly; the 6am site allocation board, SWMS and induction gates, the 36-hour week RDO calendar, and Cup Day are real rituals of the audience's week.
- Office tooling: MYOB AccountRight/Business payroll, Excel cost reports and dayworks valuations against a client rate schedule, the FWC-approved enterprise agreement PDF (about 186 pages), Incolink and CBUS obligations.
- Workers use a phone web app added to the home screen: no app store, no passwords.
- The site's only conversion path is the Web3Forms enquiry form (fires GA4 `generate_lead` on confirmed send, posts hidden attribution fields) plus a `mailto:` and the phone number 03 4061 6223.

## Capabilities and Constraints

Confirmed capabilities (from the shipped site copy, JSON-LD featureList and the app repo per the repo README rules): daily allocation board with SMS; induction and ticket enforcement before rostering; one-tap timesheets split across multi-site days; self-serve onboarding with tickets read from a photo; dayworks dockets with labour, plant and materials by quantity, e-signature on phone or secure link, signed copy emailed; named or anonymous crew dockets; automatic public holiday and RDO pay lines; payroll classification kept separate from client charge role with variations flagged; client-ready Excel cost reports; MYOB-ready export matched to payroll categories and job codes. Three modules: rostering and inductions, dockets and cost reports, EBA payroll (runs on top of rostering). Onboarding and tickets come with every plan.

Constraints future work must keep:

- **No invented figures.** The site states no pay rate, penalty step or allowance amount without a source; `eba-payroll-software.html` carries exactly two dated dollar amounts. Pricing is "contact us": per active employee for the full system, flat monthly fee per module, no lock-in.
- **Independence line** on every page that names an agreement or MYOB: PayKicker is independent software, not affiliated with or endorsed by the CFMEU or MYOB. CFMEU is referred to descriptively only.
- **Legal footer:** PAYKICKER PTY LTD, ABN 91 700 949 944; payroll software, not legal or IR advice; MYOB trademark notice.
- **Example data** uses Southline Formwork Pty Ltd and no other business.
- **Strict CSP** in `public/_headers` silently blocks any new external script, font host or API not listed there.
- Static HTML, no build step; everything served lives in `public/`; pushing `main` deploys production, any other branch gets a Cloudflare preview URL.
- Analytics and lead attribution wiring (GA4 tag, `js/gtag.js`, `js/lead.js`, `js/pixels.js`, hidden form fields) must survive any rewrite of the page.
- Terminology: subbie, crew, leading hand, docket, dayworks, RDO, EBA, SWMS, induction, ticket, allocation board, pay run, MYOB file.

## Brand Commitments

- Name: PayKicker (trading name of PAYKICKER PTY LTD). BuildPays is a legacy name that survives only in repo and Cloudflare project names.
- Locked (TR, 25 Sep 2026): the logo only, `public/paykicker-logo.svg` (navy square, orange bolt, PAY navy, KICKER orange; `#12293f` and `#f25c1f`) and its reversed, mono and icon variants. Site colours, typography and layout are open to change.
- Voice: plain, direct, trade-literate, Australian. Short sentences. No hype and no gamification. Speaks as a subbie to subbies.

## Evidence on Hand

- The animated explainer `public/paykicker-explainer.html` (sixty seconds, eight scenes, embedded on the homepage): a week on site from the 6am board to the MYOB file. It states "built by someone who runs CFMEU EBA crews, built in Melbourne, on site" without naming the person.
- A synthetic MYOB timesheet export sample (worker E0012, job WGT01) used as the hero demonstration. Labelled illustrative; not a customer's data.
- Landing pages with sourced explanations of the 36-hour week, RDO cycle, daily hire and the super floor (`eba-payroll-software.html`) and of docket-to-pay (`digital-dayworks-docket.html`).
- Worker training walkthrough `public/paykicker-worker-training.html` (noindex).
- Logo and icon assets, OG image `public/paykicker-og.png`.
- **Absent, do not fabricate:** customer names, testimonials, case studies, logos of clients, photos of real crews or sites, benchmarks, headcount served. Two TEST tenants exist in production; they are not customers.

## Product Principles

1. Prove the rules engine, never just claim it: show a real-shaped timesheet becoming a real-shaped pay line.
2. The whole week, one system: roster, docket and pay run are one flow, and the page should read that way.
3. A wrong figure on a payroll vendor's site is worse than none.
4. Built by a subbie, for subbies: the voice and the proof come from site, not from a software company.
5. One action: book the demo with your own agreement and a recent pay run.
