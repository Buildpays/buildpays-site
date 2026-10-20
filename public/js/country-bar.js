// The country bar: a slim, dismissable line above the nav for visitors Cloudflare places outside Australia, pointing
// at that country's page. Never a redirect. Stamped onto every page with the footer (scripts/shell/footer.html);
// it skips the country's own page. Styles: .cbar in css/board.css. CSP: self only, no inline script.
//
// Where the visitor is: Cloudflare's /cdn-cgi/trace on this origin ("loc=NZ"). Any error or no loc line: nothing.
// ?geo=NZ in the URL wins over the trace (for testing from Australia); ?geo=AU forces it off.
// Dismiss is remembered in localStorage for 30 days per country.
(function () {
  // One line per country. A new country is one entry here plus its page.
  var BARS = {
    NZ: { href: "/nz/", text: "In New Zealand? See NZ pricing and what works there.", cta: "New Zealand page" }
  };
  var DAYS = 30;
  var KEY = "pk-cbar-";

  var path = location.pathname;

  function onOwnPage(bar) {
    var h = bar.href;
    return path === h || path === h.replace(/\/$/, "") || path.indexOf(h) === 0;
  }

  function dismissed(code) {
    try {
      var t = Number(localStorage.getItem(KEY + code));
      return t > 0 && Date.now() - t < DAYS * 864e5;
    } catch (e) { return false; }
  }

  function remember(code) {
    try { localStorage.setItem(KEY + code, String(Date.now())); } catch (e) {}
  }

  function svg(id, cls) {
    var ns = "http://www.w3.org/2000/svg";
    var s = document.createElementNS(ns, "svg");
    s.setAttribute("class", cls);
    s.setAttribute("aria-hidden", "true");
    s.setAttribute("focusable", "false");
    var u = document.createElementNS(ns, "use");
    u.setAttribute("href", "#" + id);
    s.appendChild(u);
    return s;
  }

  function show(code) {
    var bar = BARS[code];
    if (!bar || onOwnPage(bar) || dismissed(code) || document.querySelector(".cbar")) return;

    var box = document.createElement("aside");
    box.className = "cbar";
    box.setAttribute("aria-label", "Your country");
    var inner = document.createElement("div");
    inner.className = "wrap cbar-in";

    var p = document.createElement("p");
    p.className = "cbar-t";
    p.appendChild(document.createTextNode(bar.text + " "));
    var a = document.createElement("a");
    a.className = "cbar-a";
    a.href = bar.href;
    a.appendChild(document.createTextNode(bar.cta));
    a.appendChild(svg("i-arrow", "ic"));
    a.addEventListener("click", function () {
      if (typeof gtag === "function") gtag("event", "country_bar_click", { country: code });
    });
    p.appendChild(a);

    var x = document.createElement("button");
    x.type = "button";
    x.className = "cbar-x";
    x.setAttribute("aria-label", "Dismiss");
    x.appendChild(svg("i-close", "ic"));
    x.addEventListener("click", function () {
      remember(code);
      box.parentNode.removeChild(box);
      var brand = document.querySelector(".nav .brand");
      if (brand) brand.focus();
    });

    inner.appendChild(p);
    inner.appendChild(x);
    box.appendChild(inner);

    var nav = document.querySelector("header.nav");
    if (nav && nav.parentNode) nav.parentNode.insertBefore(box, nav);
    else document.body.insertBefore(box, document.body.firstChild);
  }

  var forced = null;
  try { forced = new URLSearchParams(location.search).get("geo"); } catch (e) {}
  if (forced) { show(forced.toUpperCase()); return; }

  // Nothing to fetch if no country could show here.
  var any = false;
  for (var c in BARS) if (!onOwnPage(BARS[c]) && !dismissed(c)) any = true;
  if (!any || !window.fetch) return;

  fetch("/cdn-cgi/trace", { credentials: "omit", cache: "no-store" })
    .then(function (r) { return r.ok ? r.text() : ""; })
    .then(function (t) {
      var m = /^loc=([A-Z]{2})\s*$/m.exec(t || "");
      if (m) show(m[1]);
    })
    .catch(function () {});
})();
