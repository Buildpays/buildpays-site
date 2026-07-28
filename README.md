# buildpays-site
Marketing site for BuildPays (buildpays.com.au). Static HTML — no build step.

Everything served lives in `public/`.

- `index.html` — marketing site
- `buildpays-explainer.html` — animated "one week on site" (embedded via iframe on the homepage)
- `buildpays-worker-training.html` — worker training walkthrough (link from onboarding SMS); `noindex`
- `404.html` — not-found page; `noindex`
- `robots.txt` — allows search engines, blocks AI training crawlers, points at the sitemap
- `sitemap.xml` — indexable pages only. **Add new pages here when you add them.**
- `_headers` — security headers + CSP (Cloudflare Pages)

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

## Redirects — read before adding one
There is **no `_redirects` file**, and the bare-domain → www redirect this README used to claim
was never implemented there. Cloudflare Pages `_redirects` matches on **path only** — it cannot
match on hostname, so `/* https://www.buildpays.com.au/:splat 301` would also match requests
already on www and redirect them to themselves forever.

Host-level redirects (apex → www) must be a Cloudflare **Single Redirect** rule on the
`buildpays.com.au` zone, not a file in this repo.
