---
version: 1
slug: "public-index-html"
primary_target: "public/index.html"
related_targets: []
---

# Surface brief: homepage (public/index.html)

Scope: the homepage only, on branch `redesign-setout`. Visitor mode: Persuade.

Audience: the owner/director and the office/payroll manager of a Melbourne CFMEU-EBA subcontractor, both equally. Job: decide in one screen that PayKicker sets their agreement out once and every timesheet lands on it. Action: book a 30-minute demo bringing their EBA and a recent pay run (form `#demoForm`, phone 03 4061 6223). Proof on hand: the synthetic MYOB export sample (E0012, WGT01), the explainer iframe, the founder line "built by someone who runs CFMEU EBA crews" (no name). Constraints: keep every section, sentence of product copy, form field, hidden attribution field, script include, JSON-LD block, the explainer embed (portrait on phones), the independence and legal lines. Fonts only from Google Fonts (CSP). No invented figures, customers or photos.

Unresolved: founder name and trade (do not invent). Whether the set-out grid bubbles persist onto the landing pages (decided after TR picks a direction).

## Direction contract

THESIS: The rules are set out on the slab before the crew arrives. The homepage is a surveyor's set-out of PayKicker's week: string lines, grid bubbles, stencilled names, one spray mark for the action. It refuses the dark SaaS hero with a screenshot beside it and the three-card feature grid.

OWN-WORLD: Ground is raw concrete, a light warm grey slab (#d8d5ce with an inline-SVG grain and darker cured patches around #c6c3bb), never white, never cream, never dark. Ink is logo navy #12293f for all type and for the string lines (1px hairlines at about 55% navy, with a survey-nail dot at each end). Chalk white #f4f2ec is the only panel colour: a chalked rectangle drawn on the slab. Fluoro orange #ff5a1f is reserved by law for the primary action (an irregular spray-paint patch behind "Book a demo") and for the applied-rule marks in the demonstration; nothing else wears it, not headings, not icons, not links. Grid bubbles: navy hairline circles with a letter down the left edge (A, B, C…) and a number along the top (1, 2, 3…), as on a set-out drawing; every section is named by its bubble and its literal stencilled name (ROSTER, DOCKET, PAY RUN, RULES, SETUP, PRICE, DEMO, FAQ). Display face: Big Shoulders Stencil Display (Google Fonts) in caps, 700 to 800; body: Archivo 400/500 with tabular numerals; the MYOB file sample alone may use Courier Prime because it is a text file. Icons are authored single-stroke SVG in navy. Links are underlined with a string line. Inputs are chalk boxes with a navy hairline. Each section closes with the same string-line rule with two nails. One motion: on load and on scroll into view, a lit pulse travels the string line from the worker's tap to the pay line; reduced motion lights it instantly.

STORY: A subbie owner or payroll manager understands within seconds that PayKicker encodes a CFMEU EBA once and every one-tap timesheet comes out as the right MYOB pay line and a signed docket; believes it because the demonstration shows a real-shaped tap becoming real-shaped pay lines, and because the page speaks as a subbie; then books the demo with their own agreement.

FIRST VIEWPORT: Full-bleed slab. The nav is a thin title-block strip: logo left, section links, phone number, "Book a demo" orange patch, "Log in" outline. Below, the set-out grid: number bubbles 1 to 4 across the top edge, letter bubbles A to D down the left, string lines between. The headline "Run the site. Sign the docket. Nail the pay run." is stencilled in navy across columns 1 to 2, three lines, sized so the three lines fill rows A to B. The sub line sits at B1 in Archivo. "Book a demo" on its orange spray patch sits at C1 with the chalk note "No self-serve trial. If it fits, the pilot period is on us." beside it, and "See how it works" underlined below. Columns 3 to 4, rows A to C hold the demonstration: a chalk phone panel (Tue 07 Jul · 06:00 to 15:30 · WGT01 · one tap) at A3, a string line running from it across the grid to a chalk panel at B4 to C4 showing the MYOB export lines (the existing E0012 sample), with the overtime and site-allowance lines marked in orange as the applied rules. The phone line and fine print sit at D1. At 390px the number bubbles drop, the letter bubbles stay as a left rail, and the demonstration stacks under the action.

FORM: A surveyor's set-out on a raw slab, position 5 on the ordered grounded list (docket book, hoarding signage, shop-drawing sheet, 6am whiteboard, set-out marks, off-form concrete, footy scoreboard); seed key d4d011c9, assigned index 5. Raises: literal stencilled section names in grid bubbles (Industrial Quote Grammar); string lines as one SVG path set with a travelling pulse (Man-Machine); each engine rule as a full-width row, hours in, pay line out (Forge Scale Shower); orange reserved by law (Arcade Pixel Glow); identical crew chips as the roster row's ruler (VU Meter Bridge); one devoted column closed by the same rule, dated at the bottom (Fansite Shrine).

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
