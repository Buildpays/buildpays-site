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
window.PK_ADS_ID = "AW-18538204607";   // PayKicker's own Google Ads account 306-175-8733 (27 Oct 2026; was the Yo More account)   // e.g. "AW-0000000000"

if (window.PK_ADS_ID) {
  gtag("config", window.PK_ADS_ID);
}

/* ---------------------------------------------------------------------------
   "Start free click" (TR, 26 Oct 2026: the Square-sync Google Ads campaign). Sign-ups happen on
   app.paykicker.com.au, where this site's tag does not run, so the click on a sign-up link IS the
   conversion the ads bid toward. Inert until PK_SIGNUP_LABEL holds the label of the "Start free click"
   conversion action (Google Ads -> Goals -> Conversions). GA4 also gets a sign_up_click event.
--------------------------------------------------------------------------- */
window.PK_SIGNUP_LABEL = "6qQOCPWXrqodEL-b2odF";   // "Start free click" (Google Ads, created 26 Oct 2026)

(function () {
  "use strict";
  function signupLink(el) {
    for (var a = el; a && a !== document; a = a.parentNode) {
      if (a.tagName === "A" && /^https:\/\/app\.paykicker\.com\.au\/(signup|partners)/.test(a.href || "")) return a;
    }
    return null;
  }
  document.addEventListener("click", function (e) {
    var a = signupLink(e.target);
    if (!a) return;
    var where = (a.href.match(/for=([a-z]+)/) || [])[1] || (a.href.indexOf("/partners") > 0 ? "partners" : "signup");
    try { gtag("event", "sign_up_click", { link_url: a.href, product: where, transport_type: "beacon" }); } catch (err) {}
    if (window.PK_ADS_ID && window.PK_SIGNUP_LABEL) {
      try { gtag("event", "conversion", { send_to: window.PK_ADS_ID + "/" + window.PK_SIGNUP_LABEL, transport_type: "beacon" }); } catch (err) {}
    }
  }, true);
})();
