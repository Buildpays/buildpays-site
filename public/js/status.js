/* The status page checks from the VISITOR'S browser, deliberately.
   A status page that reports what our own server believes is a status page that can lie: the
   classic failure is a green page served from a cache while every customer sees an error. Checking
   from the reader's device answers the question they actually asked, which is "can I reach it".

   Two probes:
     · /functions/v1/health  — the real one. Unauthenticated by design, CORS-open, never cached, and
       it does a genuine round trip to Postgres plus a look at whether the scheduled jobs are current.
       Returns {status, checks:{database, scheduled}}.
     · the app origin — a no-cors HEAD. The response is opaque (we may not read it cross-origin), but
       a resolved promise proves the host answered and a rejection proves it did not. That is all a
       liveness check needs.
   Nothing here needs a key, so nothing here can leak one. */
(function () {
  var HEALTH = "https://oakqmoisxqzxosmhjfzz.supabase.co/functions/v1/health";
  var APP = "https://app.paykicker.com.au/";
  var TIMEOUT = 8000;

  var el = function (id) { return document.getElementById(id); };
  var pill = function (id, state, text) {
    var n = el(id); n.className = "pill " + state; n.textContent = text;
  };

  function withTimeout(p, ms) {
    return new Promise(function (resolve, reject) {
      var done = false;
      var t = setTimeout(function () { if (!done) { done = true; reject(new Error("timeout")); } }, ms);
      p.then(function (v) { if (!done) { done = true; clearTimeout(t); resolve(v); } },
             function (e) { if (!done) { done = true; clearTimeout(t); reject(e); } });
    });
  }

  function melbourne(d) {
    try {
      return new Intl.DateTimeFormat("en-AU", {
        timeZone: "Australia/Melbourne", day: "2-digit", month: "short",
        hour: "2-digit", minute: "2-digit", hour12: false
      }).format(d) + " Melbourne";
    } catch (e) { return d.toISOString().slice(0, 16).replace("T", " ") + " UTC"; }
  }

  function paint(app, db, cron) {
    pill("p-app", app ? "up" : "down", app ? "Operational" : "Unreachable");
    pill("p-db", db === "ok" ? "up" : db === "unknown" ? "warn" : "down",
         db === "ok" ? "Operational" : db === "unknown" ? "Unknown" : "Unavailable");
    pill("p-cron", cron === "ok" ? "up" : cron === "stale" ? "warn" : "warn",
         cron === "ok" ? "Running to schedule" : cron === "stale" ? "Behind schedule" : "Unknown");

    var banner = el("banner"), head = el("headline"), sub = el("subline");
    var worstDown = !app || db === "down";
    var degraded = cron === "stale" || db === "unknown";
    banner.className = "banner " + (worstDown ? "down" : degraded ? "warn" : "up");
    if (worstDown) {
      head.textContent = "We have a problem";
      sub.textContent = !app
        ? "This device cannot reach the app. If other sites load, it is us — please phone 03 4061 6223."
        : "The app is reachable but the database is not answering. We are almost certainly already on it.";
    } else if (degraded) {
      head.textContent = "Working, with something behind";
      sub.textContent = cron === "stale"
        ? "You can log in and work normally. A background job (alerts, reminders or backups) is running late."
        : "You can log in and work normally. One check could not be completed from this device.";
    } else {
      head.textContent = "All systems operational";
      sub.textContent = "The app, the database and the scheduled jobs all answered from this device.";
    }
    el("stamp").textContent = "Checked " + melbourne(new Date());
  }

  function run() {
    el("stamp").textContent = "Checking…";
    var appP = withTimeout(fetch(APP, { method: "HEAD", mode: "no-cors", cache: "no-store" }), TIMEOUT)
      .then(function () { return true; }, function () { return false; });
    var healthP = withTimeout(fetch(HEALTH, { cache: "no-store" }), TIMEOUT)
      .then(function (r) { return r.ok ? r.json() : { status: "error", checks: {} }; })
      .then(function (j) {
        var c = j && j.checks ? j.checks : {};
        return { db: c.database === "ok" ? "ok" : (j && j.status === "ok" ? "unknown" : "down"),
                 cron: c.scheduled || "unknown" };
      }, function () { return { db: "down", cron: "unknown" }; });

    Promise.all([appP, healthP]).then(function (r) { paint(r[0], r[1].db, r[1].cron); });
  }

  el("again").addEventListener("click", run);
  run();
  setInterval(run, 60000);
})();
