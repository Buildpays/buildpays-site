// GA4 bootstrap — was an inline <script> on every page. Moved to a file so the site's
// Content-Security-Policy can drop 'unsafe-inline' for scripts (security audit A24, 7 Sep 2026).
// The async gtag.js tag stays in each page's <head>; it drains this queue whenever it loads.
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag("js", new Date());
gtag("config", "G-4DGX8VDBNH");

/* ---------------------------------------------------------------------------
   Google Ads conversion tracking.

   PAID ADS DO NOT WORK WITHOUT THIS. GA4 measures what happened; the Ads tag is
   what lets Google bid toward enquiries instead of toward clicks. Until the two
   constants below are filled in, every ad dollar buys traffic with no feedback.

   To turn it on (both values come from the Google Ads account, once it exists):
     1. Google Ads -> Goals -> Conversions -> New conversion action -> Website.
     2. Name it "Demo enquiry". Category: Submit lead form. Value: leave blank
        (a lead is not a sale yet). Count: One.
     3. It gives you a tag id "AW-0000000000" and a label "AbC-D_efGhIjKlMnOp".
     4. Put the tag id in ADS_ID here, and the label in ADS_LEAD_LABEL in lead.js.
     5. Deploy, then use the Google Tag Assistant to confirm it fires on submit.

   Leave them empty and nothing happens: no extra network call, no console error.
   The CSP already allows googletagmanager.com, so no header change is needed.
--------------------------------------------------------------------------- */
window.PK_ADS_ID = "AW-17839145831";   // e.g. "AW-0000000000"

if (window.PK_ADS_ID) {
  gtag("config", window.PK_ADS_ID);
}
