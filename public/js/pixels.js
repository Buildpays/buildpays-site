/* ---------------------------------------------------------------------------
   Ad-platform pixels: Meta (Facebook/Instagram), LinkedIn Insight Tag, TikTok.

   Same rule as the Google Ads tag in gtag.js: INERT UNTIL CONFIGURED. Each
   block below runs only when its id is filled in. Empty id = no script loaded,
   no request made, no console error. Fill in one, two or all three.

   Why this exists: each platform bids toward the event you report back to it.
   With no pixel, an ad buys clicks. With the pixel + the Lead event that
   lead.js fires on a confirmed enquiry, the platform learns which people
   actually enquire and finds more of them. The pixel also builds the
   retargeting audience (everyone who visited, last 30/90 days).

   Where the ids come from (setup steps in C:\paykicker-sales\ads-setup.md):
     Meta      Events Manager -> Data sources -> your pixel -> Settings.
               A 15-16 digit number, e.g. "1234567890123456".
     LinkedIn  Campaign Manager -> Analyze -> Insight Tag -> "I will install
               the tag myself". The partner id is the number in
               _linkedin_partner_id = "1234567".
     TikTok    Ads Manager -> Tools -> Events -> Web events -> your pixel.
               A 20-char code, e.g. "CABCDEFG1234567890AB".

   The CSP in public/_headers already lists the three vendors' hosts, so
   nothing else has to change when the ids go in. Deploy, then confirm with
   Meta Pixel Helper / LinkedIn Insight Tag Checker / TikTok Pixel Helper.
--------------------------------------------------------------------------- */
window.PK_META_PIXEL_ID      = "";   // e.g. "1234567890123456"
window.PK_LINKEDIN_PARTNER_ID = "";   // e.g. "1234567"
window.PK_TIKTOK_PIXEL_ID    = "";   // e.g. "CABCDEFG1234567890AB"

(function (w, d) {
  function loadScript(src) {
    var s = d.createElement("script");
    s.async = true;
    s.src = src;
    var first = d.getElementsByTagName("script")[0];
    if (first && first.parentNode) first.parentNode.insertBefore(s, first);
    else d.head.appendChild(s);
  }

  /* ------------------------------------------------------------- Meta */
  if (w.PK_META_PIXEL_ID) {
    if (!w.fbq) {
      var n = w.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!w._fbq) w._fbq = n;
      n.push = n; n.loaded = true; n.version = "2.0"; n.queue = [];
      loadScript("https://connect.facebook.net/en_US/fbevents.js");
    }
    w.fbq("init", w.PK_META_PIXEL_ID);
    w.fbq("track", "PageView");
  }

  /* --------------------------------------------------------- LinkedIn */
  if (w.PK_LINKEDIN_PARTNER_ID) {
    w._linkedin_partner_id = w.PK_LINKEDIN_PARTNER_ID;
    w._linkedin_data_partner_ids = w._linkedin_data_partner_ids || [];
    w._linkedin_data_partner_ids.push(w.PK_LINKEDIN_PARTNER_ID);
    if (!w.lintrk) {
      w.lintrk = function (a, b) { w.lintrk.q.push([a, b]); };
      w.lintrk.q = [];
    }
    loadScript("https://snap.licdn.com/li.lms-analytics/insight.min.js");
  }

  /* ----------------------------------------------------------- TikTok */
  if (w.PK_TIKTOK_PIXEL_ID) {
    var t = "ttq";
    w.TiktokAnalyticsObject = t;
    var ttq = w[t] = w[t] || [];
    ttq.methods = ["page","track","identify","instances","debug","on","off","once",
                   "ready","alias","group","enableCookie","disableCookie",
                   "holdConsent","revokeConsent","grantConsent"];
    ttq.setAndDefer = function (obj, method) {
      obj[method] = function () {
        obj.push([method].concat(Array.prototype.slice.call(arguments, 0)));
      };
    };
    for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
    ttq.instance = function (id) {
      var e = ttq._i[id] || [];
      for (var j = 0; j < ttq.methods.length; j++) ttq.setAndDefer(e, ttq.methods[j]);
      return e;
    };
    ttq.load = function (id, opts) {
      var url = "https://analytics.tiktok.com/i18n/pixel/events.js";
      ttq._i = ttq._i || {}; ttq._i[id] = []; ttq._i[id]._u = url;
      ttq._t = ttq._t || {}; ttq._t[id] = +new Date();
      ttq._o = ttq._o || {}; ttq._o[id] = opts || {};
      loadScript(url + "?sdkid=" + id + "&lib=" + t);
    };
    ttq.load(w.PK_TIKTOK_PIXEL_ID);
    ttq.page();
  }
})(window, document);
