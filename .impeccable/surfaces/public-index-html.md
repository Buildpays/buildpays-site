---
version: 1
slug: "public-index-html"
primary_target: "public/index.html"
related_targets: []
---

# Surface brief: homepage (public/index.html)

Scope: the homepage, on branch `redesign-yearend` — the first surface of a replacement visual world for the whole site
(then /construction, /ap-automation, /square, /integrations, /partners). Visitor mode: Persuade.

Audience: three, equally — the owner or office manager of a Melbourne construction subcontractor on a CFMEU agreement; the
owner of any Australian small business (a shop on Square, a trade, a cafe); the accountant or bookkeeper who looks after
them. Job: see in one screen that PayKicker reads what the business already produces (hours, supplier bills, Square sales,
bank lines) and writes it into Xero or MYOB coded — and which door is theirs. Action: Book a demo (form `#contact`, the
one orange action) or Start free trial (Invoices, outline). Proof: the pack itself — every figure carries a note naming the
product that wrote it and the artifact it came from, shown as an exhibit. Constraints: PRODUCT.md (no invented figures,
no customers or testimonials, independence line, legal footer, CSP, analytics wiring, logo locked); copy verified against
the app repo 12 Oct 2026 (see the plan file); "other apps", never Amaka; Yo More never named; example businesses are
Southline Formwork Pty Ltd (construction) and — new, TR to confirm — a fictional retail example for the Square lines.

Unresolved: the retail example business name; whether exhibits are captured from the real app (TR's choice: the real product
on screen) or drawn — the mock draws them in HTML with the app's real labels, the build captures them from the harness.

## Direction contract

THESIS: The books, set like the best firm's year-end pack — and PayKicker is the one who wrote them. The homepage is a
financial-statements pack prepared for an example business: statements, notes and exhibits, where every figure carries a
note naming the PayKicker product that wrote it into Xero or MYOB. It refuses the SaaS hero with a device-framed screenshot,
the three-card feature grid, and the cream-paper-and-italic-serif editorial look.

OWN-WORLD: Paper white ground (#ffffff) with one cool second surface (#f4f6f8) for exhibits and the footer; ink is logo navy
#12293f for figures, heads and rules of weight, a greyed navy (#5c6977) for notes and secondary text; hairlines #d7dce2;
the only accent is the logo's orange #f25c1f, spent on the primary action and the small "written by PayKicker" marks beside
figures. No gradients, no shadows, no rounded cards; exhibits sit in 1px hairline frames. Type: Schibsted Grotesk for
headlines, figures, column heads, labels and buttons (tight tracking at display size, tabular numerals — verify `tnum`,
else Public Sans for figures) and Source Serif 4 for narrative notes and body. Composition: a pack's page grid — a wide
left margin column carrying note markers and section numbers, statements as right-aligned figure columns on hairline
rules, section titles set like statement titles ("Statement of … for the week ended 7 July 2026"), a contents list, and
exhibits lettered A, B, C. Controls: solid navy or hairline-outlined rectangles, 0 radius; links underlined with a hairline.

STORY: An owner or accountant lands on a pack that looks like the one their firm sends at year-end, except the figures are
this week's and each one is footnoted "written by PayKicker from …". They believe it because the note points at the
artifact (a one-tap timesheet, a bill PDF, a Square day) shown beside it as an exhibit, in the real app. They find their
door in the contents (crews, any business, accountants) and book a demo or start the trial.

FIRST VIEWPORT: A hairline nav: logo left; EBA Construction · AP automation · Square sales · Integrations · Partners; Log in
outlined; Book a demo solid orange. Below, the pack cover as the thesis: small tracked caps "PAYKICKER · PREPARED FOR
SOUTHLINE FORMWORK PTY LTD · WEEK ENDED 7 JULY 2026", then the headline in Schibsted at display size: "Your books. Written by
the software." with the strap "Hours, supplier bills and Square sales read, coded and posted into Xero or MYOB — every
figure below carries the note that says so." Beneath it, inside the first viewport on desktop, the first statement:
"Statement of entries written" — four rows (Wages — EBA pay run W27 · Materials — Westgate Reo INV 44821 · Sales — 212
Square orders · Transfer to savings, paired) with right-aligned figures, each row ending in an orange note marker; the
contents list (1 Construction crews · 2 Any business · 3 Accountants & bookkeepers) on the right as the doors.

FORM: The year-end pack, position 1 on the grounded list (year-end pack, general ledger page, reconciliation screen, tax
invoice, bank statement, pay advice, Z report); seed key 937ee779, kind pick (the roll dealt 5, the bank statement, twice;
TR declined it and took the pick). Raises from the declined challengers: cover lines in tiers (the cover carries kicker,
headline, strap as three ranked tiers); caption boxes with their own physics (note markers behave one way everywhere:
superscript, orange, the note revealed in the margin once on scroll and left lit); unlit segments designed too (the
"opening soon" and "coming" rows are designed blanks, same columns, greyed figures); one-bit chrome discipline (exhibits in
one hairline weight, no device chrome); a single light source (one accent, one direction of emphasis); a wake that traces
motion (revealed notes stay revealed). Signature interaction: the notes — as a statement scrolls into view its figures
tabulate once and each marker lights, its note sliding into the margin; reduced motion shows everything at rest.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md rewritten
from the built world, and every shipping raster (the captured product screens) carrying its provenance and a synthetic-data
label.
