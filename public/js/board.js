// The site's few behaviours: the product on/off switches, the nav (scroll state, one orange in view, the phone menu),
// the full-size view of every product window, and a once-only fade-up as sections and cards enter.
// Loaded in <head> without defer so the "js" and reveal classes are set before first paint; everything that touches the
// page waits for DOMContentLoaded. Vanilla, no dependencies (CSP: self only).
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var still = !window.matchMedia || window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canReveal = !still && 'IntersectionObserver' in window;
  if (canReveal) root.classList.add('rv-on');

  // A label can follow a product's on/off switch elsewhere on the page:
  // data-live-from="<id of the element carrying data-live>" with data-v-live (the live text) and data-cls-live (the
  // live status class, replacing its st-* class).
  function applySwitches() {
    document.querySelectorAll('[data-live-from]').forEach(function (el) {
      var src = document.getElementById(el.getAttribute('data-live-from'));
      if (!src || src.getAttribute('data-live') !== 'true') return;
      var v = el.getAttribute('data-v-live');
      if (v) el.textContent = v;
      var cls = el.getAttribute('data-cls-live');
      if (cls) el.className = el.className.replace(/\bst-\w+/g, '').trim() + ' ' + cls;
    });
  }

  // The bar turns translucent with a blur once the page has scrolled.
  function initNavScroll() {
    var nav = document.querySelector('.nav');
    if (!nav) return;
    var on = false;
    function check() {
      var s = (window.scrollY || window.pageYOffset) > 4;
      if (s !== on) { on = s; nav.classList.toggle('scrolled', s); }
    }
    check();
    window.addEventListener('scroll', check, { passive: true });
  }

  // One orange in view: while one of the page's own orange actions (outside the nav) is on screen, the nav's Book a demo
  // steps back to the secondary style (.nav.quiet); it comes back once none is in view.
  function initQuiet() {
    var nav = document.querySelector('.nav');
    if (!nav || !('IntersectionObserver' in window)) return;
    var gos = Array.prototype.slice.call(document.querySelectorAll('.btn.go')).filter(function (b) { return !nav.contains(b); });
    if (!gos.length) return;
    var seen = new Set(), bar = nav.offsetHeight || 64;
    gos.forEach(function (b) { var r = b.getBoundingClientRect(); if (r.height && r.bottom > bar && r.top < window.innerHeight) seen.add(b); });
    nav.classList.toggle('quiet', seen.size > 0);
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting && e.target.getClientRects().length) seen.add(e.target); else seen.delete(e.target); });
      nav.classList.toggle('quiet', seen.size > 0);
    }, { rootMargin: '-' + bar + 'px 0px 0px 0px', threshold: 0 });
    gos.forEach(function (b) { io.observe(b); });
  }

  // A once-only fade-up (12px, 450ms) on every section after the first and on every card, as it enters. What is already
  // on screen when the page opens shows at once; reduced motion (or no IntersectionObserver): nothing moves.
  function initReveal() {
    if (!canReveal) return;
    var main = document.querySelector('main');
    if (!main) return;
    var els = [];
    Array.prototype.slice.call(main.querySelectorAll('section, .paper-wrap')).forEach(function (s) {
      if (s.parentElement.closest('section')) return;          // sections inside a section move with it
      if (s.classList.contains('hero') || s.classList.contains('doc-hero')) return;
      var w = s.querySelector(':scope > .wrap') || (s.classList.contains('wrap') ? s : null);
      if (w) els.push(w);
    });
    main.querySelectorAll('.trio > li, .gcard').forEach(function (c) { els.push(c); });
    var h = window.innerHeight;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        e.target.classList.add('in');
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    els.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < h && r.bottom > 0) return;                    // on screen already: no fade
      if (el.parentElement.closest('.rv')) return;              // inside a section that fades already: it moves with it
      // Cards in one row arrive one after another.
      var p = el.parentElement, i = p && /\b(trio|gcards)\b/.test(p.className) ? Array.prototype.indexOf.call(p.children, el) : 0;
      if (i > 0) el.style.transitionDelay = Math.min(i, 3) * 80 + 'ms';
      el.classList.add('rv');
      io.observe(el);
    });
  }

  // Every product window (.win) opens its whole capture full size: click, tap, Enter or Space. A window that shows a part
  // of a screen (the homepage cards) names the whole capture in data-full (with data-full-w, its CSS width, and
  // data-full-alt), and that is what opens. The window becomes a button named by the capture it opens; a "View full
  // size" (or "View the whole screen") label sits on it (hover/focus) or under it (narrow screens).
  // The overlay holds the capture at its own CSS size (the files are 2x), never wider than 96vw on a wide screen and at
  // full size on a phone, scrolling as needed. Close, Esc or a click on the backdrop closes it; focus goes back.
  function initZoom() {
    var wins = Array.prototype.slice.call(document.querySelectorAll('.win'));
    if (!wins.length) return;
    var lb = null, img = null, cap = null, close = null, from = null;
    function build() {
      lb = document.createElement('div');
      lb.className = 'lb';
      lb.hidden = true;
      lb.setAttribute('role', 'dialog');
      lb.setAttribute('aria-modal', 'true');
      lb.setAttribute('aria-label', 'Screen at full size');
      lb.innerHTML = '<button class="lb-close" type="button"><svg class="ic" aria-hidden="true"><use href="#i-close"/></svg><span>Close</span></button><div class="lb-in"><img alt=""><p class="lb-cap"></p></div>';
      document.body.appendChild(lb);
      img = lb.querySelector('img'); cap = lb.querySelector('.lb-cap'); close = lb.querySelector('.lb-close');
      close.addEventListener('click', hide);
      lb.addEventListener('click', function (e) { if (e.target === lb || e.target === lb.firstChild.nextSibling || e.target === cap) hide(); });   // the backdrop, not the image
      lb.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { e.preventDefault(); hide(); }
        else if (e.key === 'Tab') { e.preventDefault(); close.focus(); }   // the one control in the dialog
      });
    }
    function show(win) {
      var src = win.querySelector('img');
      if (!src) return;
      if (!lb) build();
      from = win;
      var full = win.getAttribute('data-full');
      var w = Number(full ? win.getAttribute('data-full-w') : src.getAttribute('width')) || Math.round((src.naturalWidth || 1600) / 2);
      img.style.setProperty('--lw', w + 'px');
      img.src = full || src.currentSrc || src.src;
      img.alt = full ? (win.getAttribute('data-full-alt') || src.alt) : src.alt;
      cap.textContent = 'Example data.';
      lb.hidden = false;
      lb.scrollTop = 0; lb.scrollLeft = 0;
      root.classList.add('lb-open');
      close.focus();
    }
    function hide() {
      if (!lb || lb.hidden) return;
      lb.hidden = true;
      root.classList.remove('lb-open');
      if (from) from.focus();
    }
    wins.forEach(function (win) {
      var src = win.querySelector('img');
      if (!src) return;
      win.setAttribute('role', 'button');
      win.tabIndex = 0;
      win.setAttribute('aria-label', (win.getAttribute('data-full') ? 'View the whole screen: ' + (win.getAttribute('data-full-alt') || src.alt) : 'View full size: ' + src.alt));
      var box = document.createElement('div');
      box.className = 'win-box';
      win.parentNode.insertBefore(box, win);
      box.appendChild(win);
      var hint = document.createElement('span');
      hint.className = 'win-hint';
      hint.setAttribute('aria-hidden', 'true');
      hint.textContent = win.getAttribute('data-full') ? 'View the whole screen' : 'View full size';
      box.appendChild(hint);
      win.addEventListener('click', function () { show(win); });
      win.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') { e.preventDefault(); show(win); }
      });
    });
  }

  function initMenu() {
    var nav = document.querySelector('.nav');
    var btn = nav && nav.querySelector('.menu-btn');
    if (!btn) return;
    var label = btn.querySelector('span'), use = btn.querySelector('use');
    function set(open) {
      nav.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      label.textContent = open ? 'Close' : 'Menu';
      use.setAttribute('href', open ? '#i-close' : '#i-menu');
    }
    btn.addEventListener('click', function () { set(!nav.classList.contains('open')); });
    nav.querySelectorAll('.links a').forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { set(false); btn.focus(); }
    });
  }

  function init() {
    try { applySwitches(); } catch (e) { /* the labels stay as written */ }
    try { initNavScroll(); } catch (e) { /* the bar stays solid */ }
    try { initQuiet(); } catch (e) { /* the nav keeps its orange */ }
    try { initZoom(); } catch (e) { /* the windows stay as pictures */ }
    try { initReveal(); } catch (e) { root.classList.remove('rv-on'); }
    initMenu();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
