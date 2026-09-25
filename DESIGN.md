---
name: PayKicker site
description: A surveyor's set-out on a raw concrete slab; string lines, grid bubbles, stencilled names, one spray mark for the action.
colors:
  slab: "#d8d5ce"
  cured: "#c6c3bb"
  navy: "#12293f"
  ink2: "#3f4f5f"
  chalk: "#f4f2ec"
  orange: "#ff5a1f"
  string: "rgba(18,41,63,.55)"
  string-soft: "rgba(18,41,63,.3)"
typography:
  display:
    fontFamily: "Big Shoulders Stencil Display, Big Shoulders Stencil Text, Impact, sans-serif"
    fontSize: "clamp(48px, 6.9vw, 110px)"
    fontWeight: 800
    lineHeight: 0.92
    letterSpacing: "0.002em"
  page-title:
    fontFamily: "Big Shoulders Stencil Display, Big Shoulders Stencil Text, Impact, sans-serif"
    fontSize: "clamp(40px, 5.4vw, 80px)"
    fontWeight: 800
    lineHeight: 0.92
    letterSpacing: "0.002em"
  headline:
    fontFamily: "Big Shoulders Stencil Display, Big Shoulders Stencil Text, Impact, sans-serif"
    fontSize: "clamp(34px, 4.2vw, 62px)"
    fontWeight: 700
    lineHeight: 0.95
    letterSpacing: "0.005em"
  title:
    fontFamily: "Big Shoulders Stencil Display, Big Shoulders Stencil Text, Impact, sans-serif"
    fontSize: "24px"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "0.005em"
  stencil-name:
    fontFamily: "Big Shoulders Stencil Display, Big Shoulders Stencil Text, Impact, sans-serif"
    fontSize: "18px"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "0.12em"
  label:
    fontFamily: "Big Shoulders Stencil Display, Big Shoulders Stencil Text, Impact, sans-serif"
    fontSize: "15px"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "0.1em"
  action:
    fontFamily: "Big Shoulders Stencil Display, Big Shoulders Stencil Text, Impact, sans-serif"
    fontSize: "20px"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "0.05em"
  lede:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  body:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
  note:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  file:
    fontFamily: "Courier Prime, Courier New, monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: "normal"
rounded:
  hairline: "2px"
  panel: "3px"
  tap: "6px"
  phone: "14px"
  bubble: "50%"
spacing:
  nail: "7px"
  rail: "44px"
  rail-phone: "36px"
  gutter: "24px"
  gutter-phone: "16px"
  nav-height: "62px"
  nav-height-phone: "56px"
  sheet-top: "44px"
  sheet-top-phone: "30px"
  body-top: "22px"
  rule-gap: "24px"
  mark-gap: "14px"
  panel-pad: "26px"
  panel-pad-phone: "18px"
  field-gap: "16px 14px"
components:
  button-spray:
    backgroundColor: "{colors.orange}"
    textColor: "{colors.navy}"
    typography: "{typography.action}"
    padding: "12px 26px"
  button-spray-nav:
    backgroundColor: "{colors.orange}"
    textColor: "{colors.navy}"
    padding: "9px 18px"
  button-spray-form:
    backgroundColor: "{colors.orange}"
    textColor: "{colors.navy}"
    padding: "14px 20px"
    width: "100%"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.navy}"
    rounded: "{rounded.hairline}"
    padding: "10px 20px"
  button-outline-hover:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.chalk}"
  chalk-panel:
    backgroundColor: "{colors.chalk}"
    textColor: "{colors.navy}"
    rounded: "{rounded.panel}"
  input:
    backgroundColor: "{colors.chalk}"
    textColor: "{colors.navy}"
    rounded: "{rounded.hairline}"
    padding: "11px 12px"
  bubble:
    backgroundColor: "transparent"
    textColor: "{colors.navy}"
    rounded: "{rounded.bubble}"
    size: "30px"
  nav-link:
    textColor: "{colors.navy}"
    padding: "6px 0"
  status-pill:
    backgroundColor: "transparent"
    textColor: "{colors.ink2}"
    rounded: "{rounded.hairline}"
    padding: "5px 12px"
  tap-button:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.chalk}"
    rounded: "{rounded.tap}"
    height: "42px"
---

# Design System: PayKicker site

Recorded from the built code on branch `redesign-setout` (25 Sep 2026). Ground truth is `public/css/setout.css` (the shared system) plus each page's inline `<style>` block. Where this file and the CSS disagree, the CSS is right and this file is stale.

## Overview

**Creative North Star: "Set-Out Marks"**

The rules are set out on the slab before the crew arrives. Every page is a surveyor's set-out drawing on raw concrete: a light warm grey slab with a grain and darker cured patches, string lines stretched between survey nails, grid bubbles lettered down the left and numbered across the top, section names stencilled in caps, and a single fluoro spray mark where the one action is. Type is all logo navy. Chalk white is the only panel, a chalked rectangle drawn on the slab for anything that has to read as a thing (a phone, a MYOB file, a form, a table of modules). Nothing floats, nothing casts a shadow, nothing is white and nothing is dark: the slab is the page.

The world refuses the dark SaaS hero with a screenshot beside it and the three-card feature grid. Density is drawing-sheet density: generous slab between marks, but every mark is exact. Icons are authored single-stroke SVG in navy at one stroke weight. Links are underlined with a string line. The one motion is a lit pulse that travels the string from the worker's tap to the pay line, then the applied-rule marks fill in orange. The proof is the demonstration itself: a real-shaped one-tap timesheet becomes real-shaped MYOB pay lines.

**Key Characteristics:**
- Raw slab ground (`#d8d5ce` + inline-SVG grain + cured radial patches); never white, cream or dark.
- One ink: logo navy for all type, hairlines, nails, icons and bubbles.
- One panel colour: chalk `#f4f2ec` on a hairline, radius 3px.
- Fluoro orange only behind the primary action and on applied-rule marks (spray-edged via SVG filter).
- Big Shoulders Stencil Display in caps for every heading, name, label and button; Archivo for reading; Courier Prime only for file-shaped content.
- Every section (a "sheet") opens with a lettered bubble and a stencilled name on a string, and closes with the same 1px rule ending in two 7px nails.
- Flat: no box-shadows, no gradients except the slab's cured patches.

## Colors

A slab, an ink, a chalk, and one can of spray paint.

### Primary
- **Fluoro Orange** (`{colors.orange}`, `--orange`): the spray mark. It sits behind "Book a demo" (`.spray::before`), behind the applied-rule rows of the MYOB file and docket (`.row.hot::before`), the legend swatch, the training page's applied-rule stamp, and the pulse dot. It is never a text colour, never a heading, icon or link colour. On the status page it also colours the warn/down state (`.banner.warn`, `.pill.warn`, `.pill.down`); see the Spray Law below.

### Neutral
- **Slab** (`{colors.slab}`, `--slab`): the page background and the nav strip; also the fill of the station number bubbles and the training page's SMS bubble and clock tiles.
- **Cured** (`{colors.cured}`, `--cured`): the darker cured patches painted on the slab (as `rgba(198,195,187,.9)` / `rgba(192,189,181,.9)` radial gradients on `body`) and the solid ground of the footer title block.
- **Logo Navy** (`{colors.navy}`, `--navy`): all type by default, all hairline borders on interactive things (bubbles, outline button, inputs on focus), the nails, the icons, the selection background, the focus ring, the scrollbar thumb, and the fill of the tap button and hovered outline button (with chalk text).
- **Ink 2** (`{colors.ink2}`, `--ink2`): secondary text tinted from navy (5.7:1 on the slab): notes, fine print, FAQ answers, feature descriptions, the phone panel's keys, list markers, placeholders, disabled spray text.
- **Chalk** (`{colors.chalk}`, `--chalk`): the one panel colour (`.chalk`), input backgrounds, text on navy fills, the selection text colour, the pulse dot's ring.
- **String** (`{colors.string}`, `--string`): the string lines. 1px hairlines at 55% navy: section rules, grid cell borders, chalk panel borders, input borders at rest, nav bottom border, footer column dividers, table row dividers, link underlines.
- **String Soft** (`{colors.string-soft}`, `--string-soft`): 30% navy for hairlines inside a panel or list where a full string would be too loud: FAQ rows, file header/footer rules, module and price dividers, TOC rows, table body rows, phone key/value divider.

One literal colour sits outside the tokens: the explainer iframe well `.how-embed{background:#0f2438}` (index.html), a near-navy behind the embedded video while it loads. It is a one-off, not a token. The logo asset carries its own orange (`#f25c1f` in `paykicker-logo.svg`), which is locked by PRODUCT.md and is not the spray orange.

### Named Rules
**The Spray Law.** Orange is reserved for the primary action ("Book a demo" / "Book my demo" / the 404's "Back to the site office") and for marks that show a rule being applied (the `hot` file rows, the legend swatch, the training stamp, the pulse). Nothing else wears it: not headings, not icons, not links, not hover states. The status page is the one built exception: orange signals a degraded or down service. Nothing new may take a fourth use.

**The One Ink Rule.** Type is navy or ink2. There is no third text colour and no coloured text; emphasis is weight (`600` in Archivo, `700`/`800` in the stencil face), never hue.

**The One Panel Rule.** Anything that must read as an object on the slab is a `.chalk` panel: chalk fill, 1px string border, 3px radius. There is no second surface colour, no card tint, no dark panel.

## Typography

**Display Font:** Big Shoulders Stencil Display (with Big Shoulders Stencil Text, Impact, sans-serif), weights 700 and 800, always uppercase.
**Body Font:** Archivo (with system-ui, sans-serif), weights 400, 500, 600, tabular numerals on by default (`font-variant-numeric: tabular-nums` on `body`).
**File Font:** Courier Prime (with Courier New, monospace), weights 400 and 700, used only for content that is literally a text file: the MYOB export panel on the homepage and the example docket on the dayworks page.

All three come from one Google Fonts stylesheet link (the CSP allows only `fonts.googleapis.com` and `fonts.gstatic.com`): `Big+Shoulders+Stencil+Display:wght@700;800`, `Archivo:wght@400;500;600`, `Courier+Prime:wght@400;700`.

**Character:** the stencil is a site stencil: caps, tight leading (0.92 to 1.05), almost no tracking on the big sizes and wide tracking (0.1em to 0.12em) on the small names and labels, so a 15px label and a 110px headline are unmistakably the same hand. Archivo is plain and legible; its only job is to be read.

### Hierarchy
- **Display** (`{typography.display}`): the homepage `h1` (`.hd h1`), three lines each on its own `span`, `text-wrap: initial`. Steps to `clamp(38px,10.4vw,60px)` at ≤860 and `clamp(36px,10.2vw,48px)` at ≤640. The 404 uses the same treatment at `clamp(40px,6.4vw,96px)`.
- **Page title** (`{typography.page-title}`): `h1` inside `.page-head` on reading pages, max 20ch, margin-bottom 22px; `clamp(36px,9.6vw,56px)` at ≤860.
- **Headline** (`{typography.headline}`): every `h2`, max 22ch, `text-wrap: balance`, margin-bottom 20px. Inside `.prose` it is `clamp(30px,3.6vw,50px)` max 24ch; inside `.lawtext` it is `clamp(26px,3vw,36px)` max 30ch with a string line above and a nail at its left. Phone: `clamp(30px,8.6vw,40px)`.
- **Title** (`{typography.title}`): `h3` at 24px. Variants as built: features schedule 21px, stations 26px, footer column heads 16px with 0.12em tracking, `.lawtext h3` 21px.
- **Stencil name** (`{typography.stencil-name}`): the section name beside its bubble (`.mark .name`), 18px, 800, 0.12em, uppercase, `white-space: nowrap`; 15px at ≤640. Same voice at 16px for the TOC heading and footer heads.
- **Label** (`{typography.label}`): stencil small caps at 12px to 16px with 0.08em to 0.12em tracking, usually in ink2: bubble letters (16px), feature tags (`.stag` 15px), phone keys (14px), table heads (15px, 0.1em), status pills (14px, 0.08em), ruler labels (12px), crew chip tags (11.5px on the training page).
- **Action** (`{typography.action}`): button text. Spray 20px 0.05em (nav 17px, form 21px, phone 14px, ≤400 13px); outline 18px 0.05em (login 15px); nav phone number 19px 0.04em; the hero call-us number 22px 0.03em.
- **Lede** (`{typography.lede}`): `.lede`, 19px, max 64ch; 16.5px at ≤640. The hero sub line is 20px/1.45 max 46ch (17px at ≤860).
- **Body** (`{typography.body}`): 17px/1.55 on `body`, paragraphs max 68ch; 16px at ≤640. Reading pages use 15px to 15.5px for lists, tables, FAQ answers and feature copy.
- **Note** (`{typography.note}`): 15px in ink2 (`.note`, `.talk`, `.related`); fine print 14px to 12.5px (`.fine`, `.legal`, `.indep` 14.5px).
- **File** (`{typography.file}`): Courier Prime 12px/1.45 in the MYOB panel (`.file`), header and amounts at 700; 11px at ≤1000 and 11.5px at ≤640. The docket page's `.docket` runs the same voice at 13px (12px at ≤640).

### Named Rules
**The Stencil Rule.** The stencil face is always uppercase and always 700 or 800. It never sets running text, never drops below 11.5px, and never appears in mixed case.

**The File Voice Rule.** Courier Prime appears only where the content is a text file (the MYOB export, the docket). It is not a code font, a caption font or a label font.

**The Tabular Rule.** Numerals are tabular everywhere (`body`), so times, units and dollar amounts line up in the file, the phone panel and the tables without any extra class.

## Layout

**Wrap.** One container, `.wrap`: max-width 1360px (`--wrap`), centred, side gutter 24px (`{spacing.gutter}`), 16px at ≤640 (`{spacing.gutter-phone}`).

**Rail.** Every sheet body is a two-column grid: `var(--rail) minmax(0,1fr)`. The rail is 44px (`--rail`) and holds the letter bubble's column; it narrows to 36px at ≤860. Content sits in column 2; the closing `.rule` spans both columns and starts 3px left of the rail so its first nail sits on the rail's line.

**Sheet rhythm.** A `.sheet` has 44px top padding (30px at ≤860); its `.mark` row (bubble, name, string) is 30px tall with a 14px gap; the `.body` has 22px top / 16px bottom padding (16px / 8px at ≤860); the closing `.rule` sits 24px below the last content (20px at ≤860; 36px inside `.prose`). Reading pages add 36px under the page-head body and use 14px between paragraphs, 9px between list items, 30px above an `h3` and 10px below it.

**Hero set-out grid (index.html, `.setout`).** Desktop columns `var(--rail) 1fr .9fr .7fr 1.45fr`; rows `38px auto auto auto auto`; areas:

```
"cn n1 n2 n3 n4"     number bubbles 1-4 (38px rail row)
"ra hd hd hd ph"     A: headline across 1-3, phone panel at 4
"rb sb sb b3 my"     B: sub line across 1-2, empty 3, MYOB file at 4
"rc ct ct c3 my"     C: action across 1-2, empty 3, file continues
"rd ft ft d3 d4"     D: phone line and fine print across 1-2, empty 3-4
```

Cells carry a 1px string on top and left, a 7px nail at the top-left corner (`.cell::before`), and `.last` cells add the top-right nail; the grid has a string on its right edge. Cell padding is 18px 24px. The string from the tap runs vertically: 28px down out of the phone cell (`.ph::after`), a 22px stub into the file cell (`.my .stub`), and a nail on the file panel's top edge (`.file::before`). Note: the direction contract drew the demonstration across the grid from A3 to B4-C4; the build stacks it in column 4 (phone at A4, file at B4-C4) and the headline spans columns 1-3. The build is the record.

At ≤860 the grid collapses to `var(--rail) minmax(0,1fr)` with areas, top to bottom: `ra hd`, `rb sb`, `rc ct`, `rc ph`, `rc ln`, `rc my`, `rd ft`. The number bubbles and the empty cells (`cn n1-n4 b3 c3 d3 d4`) are hidden; the letter bubbles stay as the left rail with C spanning the action, phone, connector and file; the connector cell `.ln` (hidden on desktop) becomes a 34px vertical string; cell padding 18px 16px.

**Homepage sheets.** Modules: one chalk panel divided in four by soft strings (2 columns at ≤1000, 1 at ≤640). Features: a schedule, one full-width row per item on `150px | 1.1fr | 1.6fr` (tag, title, copy; the crew "ruler" of 34x22px chips under the copy), 2 columns at ≤1000, 1 at ≤860. The week: the explainer in a 16:9 frame max 960px, portrait 9:16 max 420px at ≤640. Rules: an auto-fit list min 220px, soft-string rows with a nail per row. Setup: three stations on one horizontal string (numbered 30px bubbles filled slab), vertical at ≤860 with 46px left indent. Price: one chalk panel in two halves `1.15fr | .85fr`, stacked at ≤1000. Demo: the form panel max 600px, two field columns (one at ≤640). FAQ: one column max 760px.

**Footer.** Cured ground, 1px navy top border; three columns `1.5fr 1fr 1fr` divided by strings with 20px 22px padding; one column at ≤860 with strings between rows. Legal line 12.5px ink2 under a string.

**Breakpoints (shared, `setout.css`):**
- **≤1000px** nav section links hidden; homepage: file panel 11px, modules 2-up, schedule 2 columns, price stacked.
- **≤860px** rail 36px; sheet padding 30/16/8; footer single column; hero stacks as above; stations vertical; schedule single column; `page-head h1`, `prose h2`, `lawtext h2` step down; TOC one column; table heads wrap.
- **≤640px** body 16px; gutter 16px; nav 56px tall, logo 24px, phone number text hidden (icon stays), spray 14px / login 13px; `h2 clamp(30px,8.6vw,40px)`; lede 16.5px; mark name 15px; form padding 18px 14px and one field column; FAQ summary 19px; hCaptcha scaled .86. Homepage: hero h1 `clamp(36px,10.2vw,48px)`, embed portrait, rules list one column, modules one column, price numbers 30px / 25px, file rows become a two-column grid.
- **≤400px** logo 21px; phone link hidden entirely; spray 13px 7px 9px; login 12px 6px 7px.

**Reading pages.** `.page-head` (first sheet with the `h1`, lede, optional `.toc`), then one `.sheet.prose` per `h2`, each with its bubble (B, C, D...) and the same closing rule; `.indep` independence line and `.cta-act` spray at the end. Legal pages use one `.sheet.prose.lawtext` in which each `h2` is a numbered heading pinned to its own string line with a nail (`.lawtext h2::before`). `scroll-margin-top` is 124px on `.prose` headings (100px at ≤860) and 96px on `.lawtext h2` to clear the sticky nav.

**Operate page (status.html).** A `.banner` chalk strip with a 14px state dot and a 30px stencil headline, a `.checked` line with the timestamp and an outline "Check again", then a `.chalk.rows` panel of service rows each ending in a `.pill`.

**Empty grid (404.html).** A three-column set-out `var(--rail) 1.4fr 1fr .8fr`, rows `38px auto auto auto`, bubbles 1-3 and A-C, min cell height 96px; the empty A3 cell is stencilled "not on this drawing" in 13px ink2. Collapses to rail + one column at ≤860.

**Stage (paykicker-worker-training.html).** `.stage` fills `calc(100dvh - 62px)` (56px nav at ≤640), min 560px; seven absolutely positioned `.scene`s cross-fade; each scene has a small mark (26px bubble, 14px name in ink2, no string), a centred `h2 clamp(28px,7vw,44px)`, a chalk phone `min(320px, 88vw)`, and a bottom `.bar` of seven progress segments (6px, chalk with navy fill) with two outline controls.

## Elevation & Depth

Flat. There are no box-shadows anywhere in the shared system or the homepage. Depth is conveyed by material and line: the slab's grain and cured patches make the ground read as concrete, and anything that is an object is a chalk panel on a string hairline. Layering is `z-index` only (sticky nav at 40, the training bar at 5, nails at 3, the pulse at 2). The sticky nav has no shadow; it is separated from the page by its 1px string bottom border.

The single exception in the codebase is on the training page: the arriving hand icon carries `filter: drop-shadow(0 3px 4px rgba(18,41,63,.35))` so it reads as hovering over the phone before it taps. It is a one-off on an animated prop, not a system value.

Focus is a ring, not a glow: `2px solid navy, offset 3px`; form fields swap to `border-color: navy` plus `box-shadow: 0 0 0 1px navy` (a 2px hairline, no blur).

### Named Rules
**The Flat Slab Rule.** Nothing casts a shadow on the slab. An object is a chalk panel; a boundary is a string; a point is a nail.

## Shapes

Set-out geometry: straight strings and round nails. Corners are barely eased so the panels read as chalked rectangles, not cards.

- **Hairline radius** (`{rounded.hairline}`, 2px): outline buttons, inputs, selects, textareas, status pills, training tags.
- **Panel radius** (`{rounded.panel}`, 3px): every `.chalk` panel, the explainer frame, the crew ruler chips, the file panel.
- **Tap radius** (`{rounded.tap}`, 6px): the navy "Submit" button inside the phone panel and the training page's big button.
- **Phone radius** (`{rounded.phone}`, 14px): the chalk phone panel (232px max on the homepage, 320px on the training page).
- **Bubble** (`{rounded.bubble}`, 50%): grid bubbles (30px), TOC bubbles (24px), training scene and golden-rule bubbles (26px), station numbers (30px), nails (7px), the pulse dot (11px), state dots (14px banner, 8px pill).
- **Spray patch:** no radius; an irregular blob `border-radius: 46% 54% 41% 59% / 58% 44% 56% 42%` rotated -1.2deg with the `#spray` SVG filter (turbulence 0.045/0.09, displacement 16, plus a speck layer). Applied-rule marks use `38% 62% 45% 55% / 60% 40% 60% 40%` with `#spray-fine` (turbulence 0.12/0.22, displacement 6) at 45% opacity; the legend swatch is 22x11px with `40% 60% 50% 50% / 60% 40% 60% 40%`.
- **Strings and nails:** every string is 1px. A closing `.rule` has a 7px navy nail at each end (`top:-3px`, `left/right:-3px`); the mark's string has one nail at its right end; grid cells have a nail at the top-left (`-4px`) and `.last` cells at the top-right; `.lawtext h2` has one at its left; the file panel has one on its top edge at centre. Lists (rules, price) use the same 7px nail as their bullet.
- **Grain:** the slab's texture is an inline-SVG `feTurbulence` (fractalNoise, baseFrequency .85, 3 octaves) coloured to navy at 16% alpha, tiled at 280px, over three cured radial gradients (`52% 38% at 18% 22%`, `44% 30% at 82% 60%`, `36% 26% at 45% 92%`) sized 1600x1100, 1400x1300 and 1800x900.
- **Icons:** `.ic` is a 1em square, `stroke: currentColor`, `stroke-width: 1.6`, round caps and joins, no fill; 24px viewBox symbols (`i-phone`, `i-tap`, `i-board`, `i-docket`, `i-ticket`, `i-export`, `i-arrow`, `i-ext`, `i-tick`, `i-crew`) in the page's `.svg-defs` block. Larger uses drop the stroke to 1.5 (module titles at 26px, chips at 13px); tick marks go to 2 or 2.2.

## Components

Everything below is defined in `public/css/setout.css` unless a page is named.

### Nav strip (`.nav`)
A thin title block. Sticky, slab ground, 1px string bottom border, 62px tall (56px at ≤640). Left: the logo at 30px high (24px at ≤640, 21px at ≤400). Right, after a flex spacer: section links (`.nl`, Archivo 15px 500, no underline at rest, a 1px navy underline that scales in from the left on hover over .3s; hidden at ≤1000), the phone number (`.nphone`, stencil 19px with the phone icon; number text hidden at ≤640, whole link hidden at ≤400), the spray "Book a demo" (17px, 9px 18px), and the outline "Log in" (15px, 8px 14px).

### Section mark (`.mark`)
Opens every sheet. A 30px navy hairline circle (`.bub`) with the section letter in stencil 800 16px, then the stencilled name (18px 800 0.12em uppercase, nowrap), then a 1px string filling the rest of the row with a 7px nail at its far end. The letters run A onward on each page (the homepage hero owns A-D and the sheets continue E, F, G, H, J, K, L, M, N: no I). The mark is `aria-hidden` on the bubble and string; the name is the visible heading device, not an eyebrow: it is the section's literal name.

### Closing rule (`.rule`)
A 1px string at 55% navy spanning the sheet from the rail, with a 7px navy nail at each end. Sits 24px under the content (20px phone, 36px in prose). Always the last child of `.body`.

### Spray button (`.spray`)
The one primary action. Stencil 800 20px 0.05em uppercase in navy, padding 12px 26px, no border, transparent element; the orange lives on `::before` (inset 2px, the irregular blob radius, `filter: url(#spray)`, rotated -1.2deg). Hover: the patch rotates to .6deg and scales 1.04 over .35s on `--ease`. Disabled: text ink2, patch at 55% opacity. Variants: nav 17px 9px 18px; form full-width 21px 14px 20px; ≤640 nav 14px 8px 11px; ≤400 13px 7px 9px. Requires the `#spray` filter in the page's SVG defs.

### Outline button (`.outline`)
The secondary action. Stencil 800 18px 0.05em uppercase navy, 1px navy border, 2px radius, padding 10px 20px, transparent. Hover: fills navy with chalk text over .2s. Variants: `.login` 15px 8px 14px; status "Check again" 14px 6px 12px; training bar 13px 7px 10px; price panel "Contact us" wraps and centres at ≤640.

### Chalk panel (`.chalk`)
Chalk fill, 1px string border, 3px radius, navy text. Padding is set per use: form 26px 26px 22px (18px 14px 16px phone); aside 18px 22px; status contact 20px 22px; phone 16px; modules 22px per cell; price 34px 36px per half. Internal dividers are `--string-soft`.

### File panel (`.chalk.file`, index.html; `.chalk.docket`, digital-dayworks-docket.html)
The text-file voice. Courier Prime 12px/1.45 (docket 13px), padding 16px 14px 12px, a nail on the top edge at centre. `.dhead` is a space-between header at 700 with 0.04em tracking over a soft string; `.row`s are space-between with the amount at 700 and nowrap; `.row.hot` carries the orange applied-rule mark on `::before` (inset -1px -4px, `#spray-fine`, opacity .45 after the pulse); `.dfoot` and `.legend` are 12px ink2 under a soft string, the legend leading with the 22x11px spray swatch. At ≤640 rows become a two-column grid.

### Phone panel (`.chalk.phone`)
A 232px-max chalk rectangle with 14px radius and 16px padding: a stencil key ("Timesheet", 14px ink2 0.1em), a 30px stencil value ("Tue 07 Jul"), a key/value grid over a soft string (keys stencil 14px ink2, values Archivo 17px 500 right-aligned tabular), a 12px ink2 caption, and the navy tap button (42px, 6px radius, stencil 15px 0.08em, chalk text, hand icon 18px). The training page's phone is 320px with the same construction.

### Inputs (`.form`)
Labels Archivo 13.5px 600 above the field; fields are chalk boxes: 1px string border, 2px radius, 11px 12px padding, 16px Archivo 400, navy caret, ink2 placeholder at full opacity. Focus: `outline: 0`, border navy, `box-shadow: 0 0 0 1px navy` (transition .2s). Textarea min 88px, vertical resize. Two-column field grid `16px 14px` gap, `.full` spans both; single column at ≤640. The submit is a full-width spray; the status message is 14px 600 centred; the fine print 12.5px ink2 centred.

### FAQ list (`.faq-col`)
One column max 760px under a string. Each `details` is a soft-string row; the `summary` is stencil 800 24px (19px at ≤640) with a 14px plus sign drawn from two navy 1.5px gradients that rotates 45deg when open (.3s). Answers are 15.5px ink2, max 62ch, with `b` in navy 600.

### Footer (`.foot`)
Cured ground, 1px navy top border, 14px/1.55. Three columns divided by strings: a stencil 16px 0.12em `h3` per column; the first holds the description (max 44ch) and the "Log in" arrow link; the others hold `.links` rows: inline links separated by a middle dot with 8px margins, wrapping. The `.legal` line sits under a string at 12.5px ink2 with the entity in navy 600.

### Reading-page TOC (`.toc`) and aside (`.aside`)
TOC: "On this page" in stencil 16px 0.12em, then a two-column list (one at ≤860) of soft-string rows, each led by a 24px hairline bubble showing its target sheet's letter (`data-b`), links underlined in string-soft. `.toc.num` swaps the bubbles for right-aligned counters in ink2. Aside: a chalk panel 18px 22px, max 72ch, 22px above, for a worked example or a caveat. Tables (`.tbl`) are string-soft rows with stencil 15px 0.1em heads over a navy 1px line, max 900px, horizontally scrollable.

### Status pills and banner (status.html)
`.pill`: stencil 800 14px 0.08em uppercase, 5px 12px, 1px string border, 2px radius, ink2 text, an 8px dot before the text. States: `.up` navy border, navy text, navy dot; `.warn` orange border and dot, navy text; `.down` orange fill, navy text, navy dot. `.banner`: chalk strip with a 14px dot (string fill at rest, navy when up, orange when warn/down; `.down` thickens the border to 2px orange) and a 30px stencil headline.

### Empty grid (404.html)
The hero set-out with nothing marked on it: bubbles 1-3 and A-C, the two-line stencil headline, one paragraph, the spray action and a stencil 15px 0.12em ink2 sign-off; empty cells stay empty except A3's "not on this drawing" in 13px stencil 700 ink2.

### Training stage (paykicker-worker-training.html)
Seven `.scene`s cross-fading (.45s opacity + 4% translate on `--ease`); props rise or slam in on a page-local spring `cubic-bezier(.34,1.56,.64,1)`; the applied-rule stamp is a spray patch at 85% opacity that lands rotated -5deg; the progress bar is seven 6px chalk segments that fill navy over each scene's `--dur`. Reduced motion collapses every animation and transition to .01s.

## Do's and Don'ts

### Do:
- **Do** start every new section as a `.sheet`: `.mark` (bubble letter, stencilled name, string) then `.body` then `.rule`, and let the rail carry the letter.
- **Do** put the one action on the slab as a `.spray` and every secondary action as an `.outline`; one spray per viewport.
- **Do** use `.chalk` for anything that must read as an object, and `--string-soft` for the dividers inside it.
- **Do** author icons as 24px single-stroke SVG symbols in the page's `.svg-defs` block, `stroke-width` 1.6 (1.5 at 26px, 2 to 2.2 for ticks), navy via `currentColor`.
- **Do** keep hairlines at 1px and nails at 7px; when a string ends, it ends in a nail.
- **Do** load fonts only through the single Google Fonts stylesheet link (Big Shoulders Stencil Display 700/800, Archivo 400/500/600, Courier Prime 400/700); the CSP allows no other font host.
- **Do** keep the reduced-motion branch honest: pulse hidden, marks at rest opacity .45, transitions off, `scroll-behavior: auto`.
- **Do** keep the copy rules from PRODUCT.md: no pay rate, penalty or allowance figure without a source; the independence line on every page naming an agreement or MYOB; the legal footer; Southline Formwork Pty Ltd as the only example business; trade terminology (subbie, crew, docket, dayworks, RDO, EBA, SWMS, allocation board, pay run, MYOB file).
- **Do** verify every page at 390px: number bubbles off, letter rail on, demonstration stacked under the action.

### Don't:
- **Don't** put orange on a heading, icon, link, border, hover or background. The Spray Law is the world's one hard prohibition.
- **Don't** add a second panel colour, a white surface, a cream tint or a dark section.
- **Don't** add a box-shadow, gradient fill or blur. The slab is flat; the training page's one drop-shadow on an animated prop is not a licence.
- **Don't** set the stencil face in mixed case, below 700, or as running text; don't use Courier Prime outside file-shaped content.
- **Don't** add eyebrow or kicker labels above headings. The stencilled section name is the section's literal name in its bubble; no "FEATURES" tag above an `h2` that says something else.
- **Don't** use emoji or glyph-font icons anywhere.
- **Don't** invent a fifth spray variant or a new bubble size; reuse 30 / 26 / 24px.
- **Don't** raise `--string` or `--string-soft` opacity to make a line "read"; the hairline is the design.

## How to add a page

1. Copy the `<head>` of `status.html`: the three Google Fonts lines (preconnect x2 + the one `css2` stylesheet) and `<link rel="stylesheet" href="/css/setout.css">`. Add a page-local `<style>` only for components that exist on no other page; shared grammar belongs in `setout.css`.
2. Paste the `.svg-defs` block from any page as the first child of `<body>`: it carries the `#spray` and `#spray-fine` filters (the spray button and applied-rule marks render as plain rectangles without them) and the ten icon symbols. Add new icons there as 24px `<symbol>`s with the same stroke language.
3. Paste the `<nav class="nav">` block (logo, spacer, five `.nl` links, `.nphone`, `.spray` "Book a demo", `.outline.login`). On non-homepage pages the links point at `/#features` etc.
4. Open with `<section class="sheet prose page-head" id="top">`: `.wrap` > `.mark` (bubble "A", the page's name, string) > `.body` (h1, `.lede`, optional `.toc`, `.rule`).
5. Add one `<section class="sheet prose">` per `h2`, lettering the bubbles B, C, D... (skip I), each ending in `<div class="rule" aria-hidden="true"></div>`. Use `.chalk.aside` for worked examples, `.tbl` for tables, `.indep` for the independence line, and `.cta-act` with a single `.spray` for the page's action.
6. Paste the `<footer class="foot">` block and keep the `.legal` paragraph verbatim.
7. Add the page to `sitemap.xml` (unless `noindex`), set the apex canonical, and check the page at 390px and 1360px before pushing.

## Decisions kept on the user's word (25 Sep 2026)

The finish review flagged these against the direction contract; TR reviewed the built homepage on his phone and kept them, so they are system decisions, not defects:

- **Modules row (`#pillars`) stays a four-cell chalk table** of icon, stencil heading and text. It is the one card grid on the site; do not copy the pattern to new sections.
- **Headline scale** stays `clamp(48px,6.9vw,110px)`. At the ~900 CSS px viewport TR reviews on, the three lines already fill their cell; larger wraps to four lines.
- **Rendered ground** is accepted as it renders (grain over `--slab` nets around #c8c8c4 on screen). Do not lift `--slab` without a new sign-off.
- **Hero layout** is the user-directed variant: headline across columns 1 to 3, timesheet at A4, MYOB file at B4 to C4, the pulse dropping vertically between them.

## The guides' handbook voice (TR, 25 Sep 2026)

TR reviewed the three `/guides/` pages and said they read "very mono, same fonts, boring". Reading pages under `<main class="guide">` therefore carry a second voice, scoped to that class in `setout.css`:

- **Reading face:** Zilla Slab 400/500/600 (+400 italic) for running text, the lede and list items on guides only; Archivo stays for notes, tables, labels, the TOC and the company list. Added to the guides' Google Fonts link, nowhere else.
- **Figure tiles (`.tiles` / `.tile`):** four navy-filled tiles under the lede with a stencil figure and an Archivo caption, each with a chalk string and nail. This is the one navy surface on the site; it is a stencilled sign, not a section, and does not license dark sections elsewhere.
- **Numbered steps (`ol.steps`):** two-digit stencil numerals in a left gutter with a string line, the bold lead on its own line.
- **Bars (`.bars`):** site allowance bands as navy bars proportional to the highest rate, stencil value at the right.
- **Month grids (`.months` / `.days`):** the RDO year as twelve Monday-first grids: RDOs filled navy, public holidays ringed, close-down shaded cured, lockdown weekends underlined.
- **Index cards (`.gcards` / `.gcard`):** the guides index is a row of chalk cards led by one stencil figure each.

The Spray Law is unchanged: no orange on any of it.
