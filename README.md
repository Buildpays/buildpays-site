# paykicker-site
Marketing site for PayKicker (paykicker.com.au). Static HTML — no build step.

Everything served lives in `public/`.

- `index.html` — marketing site
- `css/setout.css` — the shared design system (tokens, nav, section grammar, buttons, forms, footer, breakpoints). Every page links it; page-only CSS stays inline. Rules and tokens are documented in `DESIGN.md` (built with the impeccable plugin, Sep 2026).
- `js/hero-pulse.js` — homepage hero: the orange pulse that walks the set-out grid from the timesheet tap to the MYOB file (desktop widths; phones use the CSS-only pulse).
- `eba-payroll-software.html` — landing page, EBA/CFMEU payroll keyword cluster
- `digital-dayworks-docket.html` — landing page, dayworks docket keyword cluster
- `guides/` — CFMEU EBA guides (`index.html` plus one page per topic: RDO calendar and the 36-hour week; site allowance, fares and travel). Every dollar figure carries its CFMEU sheet and effective date; re-check them at each wage increase (1 Feb, 1 Mar and 1 Oct sheets). Rendered by `scripts/cfmeu/build_guides.py` from `data/cfmeu-figures.json`, the single source of every figure. **Never edit a figure in the HTML**; change the JSON and re-run the script. `.github/workflows/cfmeu-figures.yml` runs `scripts/cfmeu/watch.py` weekly (and on 2 Feb, 2 Mar, 2 Oct): it hashes the union's sheets, and when one changes it extracts the new figures with Claude, checks them against sanity gates (every key present, within 0.5x to 1.5x of the previous figure, weekly = hourly x 36, dates never go backwards, 20 to 30 RDOs a year) and pushes to main. A failed gate opens a GitHub issue and publishes nothing. Needs the `ANTHROPIC_API_KEY` repo secret. The same workflow then runs `scripts/cfmeu/fwc_employers.py --publish`, which rebuilds `data/cfmeu-employers.json` from the Fair Work Commission's yearly `agreementsYYYY.xlsx` lists (every agreement whose title names the CFMEU Victorian Construction and General Division, within a year of nominal expiry, deduped per employer and trade) and republishes the `cfmeu-eba-jobs-victoria` guide when the list changes; gates: at least 300 employers, count within 0.7x-1.3x of the previous list. No LLM in that path. `public/js/employers.js` is the list filter (the page is complete without it).
- `paykicker-explainer.html` — animated "one week on site" (embedded via iframe on the homepage)
- `paykicker-worker-training.html` — worker training walkthrough (link from onboarding SMS); `noindex`
- `404.html` — not-found page; `noindex`, and deliberately **no** `rel=canonical` (a canonical on
  an error page is a soft-404 signal)
- `robots.txt` — allows search engines, blocks AI training crawlers, points at the sitemap
- `sitemap.xml` — indexable pages only. **Add new pages here when you add them.**
- `_headers` — security headers + CSP (Cloudflare Pages)
- `_redirects` — path-only redirects for URLs the PayKicker rename broke (see below)

## Landing pages — the rules they follow
Both keyword landing pages are built on the same shell as `privacy.html` / `terms.html` and reuse
the homepage `.btn` and `.docket` components rather than restyling. Two content rules matter:

- **Figures.** `eba-payroll-software.html` states exactly two dollar amounts — travel allowance
  and the superannuation floor — both stamped "as at 1 March 2026" and both framed as illustrating
  the shape of a calculation, not as a rate reference. Everything else points at
  `vic.cfmeu.org/wages`. **Do not add a rate, penalty step or allowance amount to these pages
  without a source.** They date, and a wrong one on a payroll vendor's site is worse than none.
- **Independence.** Both pages carry: *PayKicker is independent software and is not affiliated
  with or endorsed by the CFMEU or MYOB.* CFMEU is referred to descriptively only. Keep both.
- Example data uses **Southline Formwork Pty Ltd** and no other business.

## Deploy (Cloudflare Pages)
Framework preset: **None** · Build command: *(blank)* · Output directory: `public`
Pushing to `main` deploys production. Pushing any other branch gets a preview URL.

## Analytics and lead attribution
- GA4 tag `G-4DGX8VDBNH` is in the `<head>` of `index.html`.
- The enquiry form fires a `generate_lead` GA4 event **only on a confirmed successful send**.
- The form also posts hidden attribution fields (`lead_source`, `utm_*`, `gclid`, `referrer`,
  `landing_page`) to Web3Forms, so the enquiry email itself names the source. This keeps working
  when analytics is blocked.
- Anything added that loads an external script or calls an external API must be added to the
  CSP in `_headers`, or the browser will silently block it.

## Canonical hostname — changed at the PayKicker rebrand
BuildPays was canonical on **www**. PayKicker is canonical on the **apex**, `paykicker.com.au`.
Every `<link rel="canonical">`, Open Graph URL, JSON-LD `@id` and sitemap entry uses the apex.
`www.paykicker.com.au` should redirect to it.

## Redirects — read before adding one
`public/_redirects` exists and holds **path-only** redirects for the URLs the rename broke (the
explainer, the worker training page, and the old image filenames). Cloudflare Pages `_redirects`
matches on **path only** — it cannot match on hostname, so a blanket
`/* https://paykicker.com.au/:splat 301` would also match requests already on the apex and
redirect them to themselves forever. Do not add one.

Host-level redirects must be Cloudflare **Single Redirect** rules on the zone, not a file in
this repo. Two are wanted:
- `www.paykicker.com.au/*` → `https://paykicker.com.au/:splat` (301)
- `buildpays.com.au/*` and `www.buildpays.com.au/*` → `https://paykicker.com.au/:splat` (301)

**Neither is in place as at 18 Aug 2026.** `www.paykicker.com.au`, `buildpays.com.au` and
`www.buildpays.com.au` all return `200` and serve this site, so four hostnames serve identical
content. `rel=canonical` points Google at the apex, which limits the damage, but the old domain's
accumulated authority is not being passed to the new one because there is no 301 to pass it
through. This is the highest-value outstanding item and it cannot be fixed from this repo.
