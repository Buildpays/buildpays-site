---
name: PayKicker site
description: A quiet dark workroom where the real product screens are the brightest thing on the page and one orange button says what to do next.
colors:
  ground: "#0b0f14"
  surface: "#131922"
  raised: "#1a2230"
  field: "#0b0f14"
  ink: "#f3f5f7"
  ink-secondary: "#9aa6b2"
  border: "rgba(255,255,255,.10)"
  border-control: "rgba(255,255,255,.22)"
  border-hover: "rgba(255,255,255,.4)"
  orange: "#f25c1f"
  orange-deep: "#e04f14"
  on-orange: "#0b1826"
  screen-edge: "#f4f6fa"
  placeholder: "#87929e"
  green: "#7fd6a3"
  green-tint: "rgba(127,214,163,.12)"
  amber: "#f0b541"
  amber-tint: "rgba(240,181,65,.12)"
  grey: "#9aa6b2"
  grey-tint: "rgba(154,166,178,.12)"
  red: "#f2a191"
  red-tint: "rgba(242,161,145,.12)"
  money-wash: "rgba(240,181,65,.18)"
typography:
  display:
    fontFamily: "Geist, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "clamp(2.5rem, 4.4vw, 4.9rem)"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  page-title:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "clamp(2.5rem, 3.9vw, 3.5rem)"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "clamp(2rem, 3.2vw, 3rem)"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  lede:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "1.1875em"
    fontWeight: 400
    lineHeight: 1.5
  small:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "normal"
  figure:
    fontFamily: "Geist, system-ui, sans-serif"
    fontSize: "clamp(1.6rem, 2.2vw, 2rem)"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.02em"
    fontFeature: "\"tnum\" 1"
rounded:
  mark: "0.25rem"
  control: "0.5rem"
  surface: "0.75rem"
  phone: "1.375rem"
  pill: "999px"
spacing:
  gutter: "clamp(1rem, 4vw, 2.5rem)"
  section: "clamp(4rem, 7.8vw, 7rem)"
  column: "clamp(1200px, 1200px + (100vw - 1440px) * .86, 1880px)"
  column-text: "clamp(1120px, 72vw, 1500px)"
  nav: "4rem"
components:
  button-primary:
    backgroundColor: "{colors.orange}"
    textColor: "{colors.on-orange}"
    rounded: "{rounded.control}"
    padding: "0 1.125rem"
    height: "2.75rem"
  button-primary-hover:
    backgroundColor: "{colors.orange-deep}"
    textColor: "{colors.on-orange}"
  button-primary-hero:
    backgroundColor: "{colors.orange}"
    textColor: "{colors.on-orange}"
    rounded: "{rounded.control}"
    padding: "0 1.5rem"
    height: "3.25rem"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0 1.125rem"
    height: "2.75rem"
  button-secondary-hover:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.orange}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.surface}"
  price-strip:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.surface}"
    padding: "1.25rem 1.5rem"
  input:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0.625rem 0.75rem"
    height: "2.75rem"
  pill-live:
    backgroundColor: "{colors.green-tint}"
    textColor: "{colors.green}"
    rounded: "{rounded.pill}"
    padding: "0.1875rem 0.625rem"
  pill-soon:
    backgroundColor: "{colors.amber-tint}"
    textColor: "{colors.amber}"
    rounded: "{rounded.pill}"
    padding: "0.1875rem 0.625rem"
  pill-coming:
    backgroundColor: "{colors.grey-tint}"
    textColor: "{colors.grey}"
    rounded: "{rounded.pill}"
    padding: "0.1875rem 0.625rem"
  nav:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    height: "4rem"
---

# Design System: PayKicker site

Recorded from the built site (branch `redesign-premium`, finish pass, 13 October 2026). The source of truth is
`public/css/board.css` (one shared stylesheet; the old name is kept so every page, guide and compare page picks it up),
`public/js/board.js` (the behaviours) and the shell templates in `scripts/shell/` (nav and footer, stamped into every
page by `scripts/shell.py`). This file replaces the Set-Out Marks system (stencils on a slab), which no page uses any more.

## Overview

**Creative North Star: "The Dark Workroom"**

The site is a dark, quiet room with the lights on the work. The ground is a near-black blue (#0b0f14); everything the
visitor reads sits on it in one typeface, Geist, at one weight family; the brightest things on any page are the real app
screens, white captures held in dark rounded frames. Colour is almost absent: one orange for the one action that
matters in the view, and three soft tints that say whether a product is live, opening soon or coming. Depth comes from
borders and tone steps, not from shadows or glows.

The system is borrowed in spirit from the premium product sites the owner pointed at (Notion, Linear, the Google Store)
and kept plain for a trade audience: short sentences, prices stated up front, nothing that moves unless it is arriving.
The site is **dark only**. There is no light theme and no theme switch; the logo is always the reversed one.

Above 1440px the page does not stretch a phone layout: the root font-size grows (16px at 1440, about 18px at 1920, 20px
at 2560), every component is sized in rem, and the content column grows with the screen, so a big monitor sees the same
page in the same proportions, larger.

**Key Characteristics:**
- One typeface (Geist 400/500/600/700), headlines at 600 with tight tracking (-0.02em), no uppercase labels.
- One ground, two surface steps (#131922, #1a2230), hairline borders at 10% white.
- One orange (#f25c1f) per view, on the primary action only; hover turns secondary controls and links orange.
- Real product screens, whole, never cropped, never upscaled past their own pixels, framed at a 12px radius.
- One band per page: the surface tone held by a hairline above and below.
- A once-only 12px fade-up as sections arrive; nothing moves with reduced motion.

## Colors

A near-monochrome dark palette: blue-black grounds, cool off-white ink, one hot orange and three status tints.

### Primary
- **Kicker Orange** (#f25c1f): the primary action only (Book a demo, Start free trial, Join, Become a partner), with
  dark lettering on it (#0b1826, 5.4:1). Darkens to #e04f14 on hover. Also the hover and keyboard-focus colour of every
  secondary control and text link (see Components). It is the logo's orange.

### Neutral
- **Workroom Ground** (#0b0f14): the page, the nav at rest, inputs' fields. `color-scheme: dark`; `theme-color` meta
  and the web manifest carry the same value.
- **Surface** (#131922): cards, panels, the comparison tables' header row, secondary buttons, the one band per page.
- **Raised Surface** (#1a2230): a strip inside a card (the window strip over a screen, the card's title bar), the price
  strip, the footer, the eyebrow pill.
- **Ink** (#f3f5f7): headings, body copy in panels, values (17.6:1 on the ground).
- **Secondary Ink** (#9aa6b2): ledes, notes, captions, table headers, footer headings (7.8:1 on the ground, 6.4:1 on
  the raised surface).
- **Hairline** (rgba(255,255,255,.10)): every divider, card edge, table row rule.
- **Control Edge** (rgba(255,255,255,.22)), **Control Edge Hover** (rgba(255,255,255,.4)): inputs and secondary buttons,
  a step firmer than a divider so a control reads as a control.
- **Screen Edge** (#f4f6fa): the app's own page colour, the ground behind a capture inside its frame, so a capture that
  does not fill its frame sits on its own colour, never on black.
- **Placeholder** (#87929e, 6.1:1).

### Status tints
- **Live** (#7fd6a3 on rgba(127,214,163,.12)), **Opening soon** (#f0b541 on rgba(240,181,65,.12)), **Coming**
  (#9aa6b2 on rgba(154,166,178,.12)), **Down** (#f2a191 on rgba(242,161,145,.12)): status pills only, and the green
  ticks in price strips and comparison tables. Each is at least 5.8:1 on its own tint.
- **Money Wash** (rgba(240,181,65,.18)): the faint amber mark under one money fact per paragraph (`mark.hi`).

### Named Rules
**The One Orange Rule.** One orange button per view. While a page's own orange action is on screen, the nav's Book a
demo steps back to the secondary style (board.js adds `.nav.quiet`); it returns when none is in view.

**The No Glow Rule.** No gradients, glows, blur halos or coloured shadows anywhere. Borders and tone steps carry depth.

## Typography

**Display Font:** Geist (Google Fonts, 400/500/600/700, `display=swap`), with system-ui, -apple-system, Segoe UI, Roboto
**Body Font:** Geist
**Label Font:** Geist

**Character:** One neo-grotesque face for everything, set tight and large for headlines and open for reading, with
tabular figures wherever money or hours line up.

### Hierarchy
- **Display** (600, clamp(2.5rem, 4.4vw, 4.9rem), 1.05, -0.02em): the homepage headline only; two lines at 1440 and up.
- **Page title** (600, clamp(2.5rem, 3.9vw, 3.5rem), 1.05): product page heroes (words left, screen right). Reading
  pages use clamp(2.25rem, 4vw, 3.5rem) at 1.08, max 24ch.
- **Headline** (600, clamp(2rem, 3.2vw, 3rem), 1.05): section heads, max 22ch.
- **Title** (600, 1.25rem, 1.25, -0.01em): card names, plan names, step titles (1.125rem in cards).
- **Body** (400, 1rem, 1.6; 1.0625rem at 1440 and up): reading text, max 60 to 68ch.
- **Lede** (400, 1.1875em, 1.5, secondary ink): the hero strap and section ledes, max 48 to 60ch.
- **Small** (400, 0.875 to 0.9375rem): notes, captions, fine print. Never under 14px at phone width.
- **Label** (500, 0.8125rem, sentence case): status pills, window strips, footer headings; raised to 14px at 640px and
  below.
- **Figure** (600, clamp(1.6rem, 2.2vw, 2rem), -0.02em, tabular): prices in price strips, plan prices, guide tiles.

### Named Rules
**The No Caps Rule.** No tracked uppercase labels anywhere; labels are sentence case at weight 500.

**The Ruler Figures Rule.** Money, hours and counts use tabular figures (`font-variant-numeric: tabular-nums`) so
columns line up.

## Layout

- **Column:** 1200px up to a 1440 viewport, then it grows with the screen: clamp(1200px, 1200px + (100vw - 1440px) x
  0.86, 1880px), about 1613px at 1920 and 1880px at 2560. Text-heavy pages (guides, compare, legal) use clamp(1120px,
  72vw, 1500px) and a reading column of 46rem.
- **Gutter:** clamp(1rem, 4vw, 2.5rem); 16px at phone width.
- **Root size:** clamp(100%, 100% + (100vw - 1440px) x 0.004, 125%). Every size is written in rem or against
  `--vw` (1vw up to 1440, then tied to the root), so the whole page scales in one proportion above 1440.
- **Rhythm:** one section space, clamp(4rem, 7.8vw, 7rem) (112px desktop, 64px phone). Plain sections are spaced by
  margins (two in a row collapse to one space); a band holds the same space inside, top and bottom.
- **Homepage:** centred hero (eyebrow, headline, strap, two buttons, the trial line), then the three product cards in
  one row directly under it (their top inside the first screen at 1440x900), then the screen slideshow, then the
  sections.
- **Product pages:** words left, framed screen right (45:55); the price strip under the buttons. Gate sections pair
  copy (38%) with a screen (62%), alternating sides.
- **Breakpoints:** the nav collapses to a menu under 1200px; two-column compositions stack at 1000px (product heroes,
  duos, cards), 900px (heads, forms, FAQ) and 820px; card grids go to one column at 1000px; small-text floor at 640px.
- **No horizontal scroll** at any width from 390 to 2560.

## Elevation & Depth

Flat by tone. Surfaces step up from the ground (#0b0f14) to the surface (#131922) to the raised strip (#1a2230), each
edged by a hairline. Shadows exist only as a faint inner top highlight; nothing casts a coloured or blurred shadow.

### Shadow Vocabulary
- **Surface highlight** (`box-shadow: inset 0 1px 0 rgba(255,255,255,.04)`): cards, panels, framed screens, tables.
- **Menu panel** (`box-shadow: 0 24px 40px -24px rgba(0,0,0,.6)`): the phone menu's slide-down panel only.

### Named Rules
**The Borders Do The Work Rule.** Depth is a tone step plus a 1px hairline. A hover lifts a card 2px and firms its edge
to the control edge; it never adds a shadow.

## Shapes

Gently rounded and consistent: 12px (0.75rem) for every card, panel, framed screen, table and price strip; 8px (0.5rem)
for buttons and inputs; 4px (0.25rem) for the money wash and focus outlines; fully round for status pills, the slideshow arrows and the dots; 22px for a phone capture.
A frame clips its contents (`overflow: hidden`), so a capture's own square corners never show.

## Components

### Buttons
- **Shape:** 8px radius; 44px tall (2.75rem), 52px in a hero (`.big`); weight 600, 15px.
- **Primary:** Kicker Orange with dark lettering; darkens on hover, presses 1px down.
- **Secondary (hairline):** surface ground, ink lettering, control-edge border; on hover and keyboard focus the border
  and lettering turn orange, the ground stays (150ms).
- **Ink:** an ink fill for two equal choices side by side (join: Continue with Xero / MYOB), so the orange stays single.

### Status pills
- **Style:** fully round, tinted ground, a 6px dot in the text colour, 13px weight 500, sentence case.
- **States:** Live (green), Opening soon (amber), Coming (grey), Down (red). A product's pill can follow its on/off
  switch elsewhere on the page (`data-live`, `data-live-from`).

### Cards / Containers
- **Corner Style:** 12px.
- **Background:** surface (#131922); a raised strip for a card's window bar.
- **Shadow Strategy:** the surface highlight only (see Elevation & Depth).
- **Border:** hairline; the control edge on hover.
- **Internal Padding:** 1rem 1.25rem for heads and feet; 1.5rem for steps and tiles.
- **Product card:** name and status pill, a window strip naming the screen, the snip (4:3, filling the card but never
  past the file's own pixels, centred on the screen-edge colour if the card is wider), one line, an arrow link.

### Framed screens
- **Frame:** 12px, hairline, a dark surface frame; a 38px window strip (three dots, the screen's name, "Example data")
  above the capture; the capture whole beneath it on the screen-edge colour.
- **Height rule:** at 1001px and up a framed screen beside copy fits the window height under the nav, so it is always
  seen whole: its width follows from its aspect (`--ar` on the figure) and the height left, never wider than its column.
- **Native-pixel cap:** a capture never scales past its own CSS pixels (the files are 2x); a frame wider than that
  centres the capture on the screen-edge colour.
- **Provenance:** every capture in `public/screens/` has a `.json` sidecar (source harness URL, app commit, viewport,
  clip, captured time, what it shows, the synthetic data note). No capture ships without one.

### Slideshow (homepage "See it work")
Three whole screens, one at a time, each framed with its strip and one sentence under it (max 70ch, centred). All slides
share the tallest capture's aspect; the others sit whole inside it. 44px round previous/next buttons over the frame's
edges at 1001px and up, under it with the dots between at 1000px and below; 8px dots (current = ink). Swipe (40px),
arrow keys when focused, a 250ms crossfade (none with reduced motion), no autoplay; hidden slides are `aria-hidden` and
`inert`. The frame fits the window height at desktop.

### Lightbox
Every framed screen is a button: click, tap, Enter or Space opens the whole capture at its own CSS size (never wider
than 96vw; full size and scrollable on a phone) over a near-opaque ground, with one Close control. Esc or a click on the
backdrop closes it and focus returns. A "View full size" chip shows on hover/focus, or as a line under the screen on
touch and narrow screens.

### Price strip
A raised-surface panel: a large figure (From $9.99 a month) with its qualifier under it, then up to three short facts
with green ticks. Sits under the buttons in a product hero.

### Comparison table ("PayKicker vs other apps")
A 12px-framed table, the PayKicker column on the raised surface and headed with the reversed mark, the other headed
"Other apps"; green ticks, "Not stated" in secondary ink; a dated source note under it. Folds to stacked rows at 700px.

### Inputs / Fields
- **Style:** ground-coloured field, control-edge border, 8px radius, 44px tall, light lettering.
- **Focus:** the border turns ink and a 3px ring (rgba(255,255,255,.16)) appears; no glow.
- **Error:** the red tint's text colour on the border (`:user-invalid`). Form messages use the green and red tokens.
- **Choice tiles:** checkbox and radio picks are bordered tiles; hover turns the edge orange, checked is an ink edge
  on the raised surface.

### Navigation
- **Style:** 64px, the ground at rest; after 4px of scroll it turns translucent with a backdrop blur and a hairline
  under it. Reversed logo, 200px (240px at 1920), links 15px weight 500, the phone number, Log in (secondary) and Book a
  demo (orange, quiet while the page's own orange is in view).
- **Current page:** a 2px ink underline under the link (`aria-current="page"`, stamped by the shell).
- **Hover:** links turn orange.
- **Mobile (under 1200px):** logo, a call button and Menu; the links drop down as a full-width panel (200ms fade and
  8px slide, none with reduced motion), each a 44px row with a hairline, the two buttons side by side under them.

### FAQ and folds
A plain accordion: a hairline between questions, the question at weight 500, a plus that turns 45 degrees when open;
the question turns orange on hover. "What your file needs" tables fold the same way.

### Footer
The raised surface with a hairline above: four link columns, then the legal row (reversed logo, PAYKICKER PTY LTD and
ABN, the not-legal-advice line and the trademark notices).

### Motion
A once-only fade-up (opacity 0 to 1, 12px rise, 450ms ease-out) on each section after the first and on cards as they
enter (IntersectionObserver; cards in a row 80ms apart). What is on screen at load shows at once. Hover transitions are
150ms. With `prefers-reduced-motion: reduce` nothing moves: no fade, no lift, no crossfade, no smooth scroll.

## Do's and Don'ts

### Do:
- **Do** keep the site dark only: #0b0f14 ground, the reversed logo, `theme-color` #0b0f14.
- **Do** put exactly one orange button in any view, and let hover turn secondary controls and links orange.
- **Do** show the real app's screens whole, from the harness with synthetic data, each with its `.json` provenance
  sidecar; the example business is Southline Formwork Pty Ltd and no other.
- **Do** size components in rem so the page grows with the root font-size above 1440.
- **Do** state prices with their source and GST basis (inc GST), and highlight at most one money fact per paragraph.
- **Do** keep text at 14px or more at phone width and secondary text at 4.5:1 or better.

### Don't:
- **Don't** add a light theme, a theme switch or a second stylesheet; tokens live on `:root` in board.css.
- **Don't** crop a screen, upscale it past its own pixels, or put a glow, gradient or blur halo behind it.
- **Don't** add testimonials, customer logos, client names, invented figures or photos of real crews or sites.
- **Don't** name a competitor in a comparison table or in public copy outside the dated /compare pages: it is "other
  apps".
- **Don't** use uppercase tracked labels, a second typeface or a colour outside the tokens above.
- **Don't** load a script, font or API from a host the CSP in `public/_headers` does not list (self-hosted scripts,
  Google Fonts only).

Not canonized: the homepage hero's eyebrow pill ("Built in Melbourne · Xero and MYOB") was an owner request for that one
hero and is not a pattern for other surfaces. The legacy stand-alone pages (the explainer and the worker training
walkthrough) keep their own older styles and are outside this system.
