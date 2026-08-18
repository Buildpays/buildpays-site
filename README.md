# paykicker-site
Marketing site for PayKicker (paykicker.com.au). Static HTML — no build step.

Everything served lives in `public/`.

- `index.html` — marketing site
- `eba-payroll-software.html` — landing page, EBA/CFMEU payroll keyword cluster
- `digital-dayworks-docket.html` — landing page, dayworks docket keyword cluster
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
