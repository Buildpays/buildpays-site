// The board: split-flap rows on any page (every element with data-flip), plus the phone menu.
// Loaded in <head> without defer so the "hold the lettering" class is set before first paint;
// everything that touches the page waits for DOMContentLoaded. Vanilla, no dependencies (CSP: self only).
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var still = !window.matchMedia || window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canAnimate = !still && typeof Element !== 'undefined' && 'animate' in Element.prototype;
  if (canAnimate) root.classList.add('flip');

  var DIGITS = '0123456789';
  var LETTERS = 'ABCDEFGHIJKLMNOPRSTUVWY';

  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  function leaf(cls) {
    var s = document.createElement('span');
    s.className = 'lf ' + cls;
    s.appendChild(document.createElement('b'));
    return s;
  }
  function put(lf, t) { lf.firstChild.textContent = t; }

  // One flap: two static halves (top shows the next value, bottom the current one)
  // and two moving leaves that carry the fall between them.
  function makeFlap(el, t) {
    var f = { el: el, top: leaf('top'), bot: leaf('bot'), ft: leaf('ft'), fb: leaf('fb'), cur: t };
    el.textContent = '';
    el.appendChild(f.top); el.appendChild(f.bot); el.appendChild(f.ft); el.appendChild(f.fb);
    put(f.top, t); put(f.bot, t);
    return f;
  }

  // Fall: the upper leaf drops away accelerating, the lower leaf lands and settles.
  function flipTo(f, t, dur, settle, onLand) {
    var from = f.cur;
    if (from === t) return Promise.resolve();
    put(f.top, t); put(f.ft, from); put(f.fb, t);
    f.ft.style.visibility = 'visible';
    var fall = f.ft.animate(
      [{ transform: 'rotateX(0deg)', filter: 'brightness(1)' }, { transform: 'rotateX(-90deg)', filter: 'brightness(.55)' }],
      { duration: dur * 0.42, easing: 'cubic-bezier(.5,0,.85,.4)', fill: 'forwards' }
    );
    return fall.finished.then(function () {
      f.ft.style.visibility = 'hidden';
      fall.cancel();
      if (onLand) onLand();
      f.fb.style.visibility = 'visible';
      var frames = settle
        ? [{ transform: 'rotateX(90deg)', filter: 'brightness(.6)' },
           { transform: 'rotateX(-9deg)', filter: 'brightness(1)', offset: 0.56 },
           { transform: 'rotateX(4deg)', offset: 0.78 },
           { transform: 'rotateX(-1.5deg)', offset: 0.9 },
           { transform: 'rotateX(0deg)' }]
        : [{ transform: 'rotateX(90deg)', filter: 'brightness(.6)' }, { transform: 'rotateX(0deg)', filter: 'brightness(1)' }];
      var land = f.fb.animate(frames, {
        duration: settle ? dur * 1.5 : dur * 0.58,
        easing: settle ? 'cubic-bezier(.25,.9,.3,1)' : 'cubic-bezier(.3,.6,.4,1)'
      });
      return land.finished;
    }).then(function () {
      put(f.bot, t);
      f.fb.style.visibility = 'hidden';
      f.cur = t;
    });
  }

  // Run a flap through a list of values; the last one lands with a settle.
  function run(f, seq, step, onFinal) {
    var p = Promise.resolve();
    seq.forEach(function (t, i) {
      var last = i === seq.length - 1;
      p = p.then(function () { return flipTo(f, t, last ? step * 1.1 : step, last, last ? onFinal : null); });
    });
    return p;
  }

  function churn(target, n) {
    var pool = DIGITS.indexOf(target) > -1 ? DIGITS : LETTERS.indexOf(target) > -1 ? LETTERS : '';
    var seq = [];
    if (pool) for (var i = 0; i < n; i++) seq.push(pool.charAt(Math.floor(Math.random() * pool.length)));
    seq.push(target);
    return seq;
  }

  function buildRow(row) {
    var cells = [];
    row.querySelectorAll('.fl').forEach(function (el) {
      var v = el.getAttribute('data-v');
      var cell = el.parentNode;
      var sr = document.createElement('span');
      sr.className = 'sr';
      sr.textContent = el.getAttribute('data-sr') || v.trim();
      cell.appendChild(sr);
      el.setAttribute('aria-hidden', 'true');
      if (el.classList.contains('chars')) {
        el.textContent = '';
        var chars = v.split('').map(function (c) {
          var s = document.createElement('span');
          var gap = c === ' ' && v.indexOf(' ') === 2;   // the space in "03 JUL" is a gap, not a blank flap
          s.className = 'cell' + (gap ? ' gap' : '') + (c === ',' || c === '.' ? ' pun' : '');
          el.appendChild(s);
          return { f: gap ? null : makeFlap(s, canAnimate ? ' ' : c), v: c };
        });
        cells.push({ kind: 'chars', el: el, chars: chars });
      } else {
        cells.push({ kind: 'word', el: el, f: makeFlap(el, canAnimate ? ' ' : v), v: v, via: el.getAttribute('data-via') });
      }
    });
    return cells;
  }

  // A row: every flap but the status starts at its own moment (the board's data-flip list, else
  // 120 ms apart, in reading order); the status shows its "via" word while the row works, then lands last.
  function animateRow(row, cells, at) {
    row.classList.add('moving');
    var jobs = [], stat = null, k = 0;
    cells.forEach(function (c) {
      if (c.via) { stat = c; return; }
      var start = at[k] != null ? at[k] : k * 120, spin = k === 0 ? 2 : 3;
      k++;
      if (c.kind === 'chars') {
        c.chars.forEach(function (ch, i) {
          if (ch.v === ' ' || !ch.f) return;
          jobs.push(wait(start + i * 32).then(function () { return run(ch.f, churn(ch.v, spin + (i % 3)), 74); }));
        });
      } else {
        jobs.push(wait(start).then(function () { return run(c.f, [c.v], 205); }));
      }
    });
    if (stat) {
      jobs.push(wait(240).then(function () {
        stat.el.classList.add('reading');
        return run(stat.f, [stat.via], 190);
      }));
    }
    return Promise.all(jobs).then(function () { return wait(160); }).then(function () {
      if (stat) return run(stat.f, [stat.v], 200, function () { stat.el.classList.remove('reading'); });
    }).then(function () {
      row.classList.remove('moving');
    });
  }

  // A flap can follow a product's on/off switch elsewhere on the page:
  // data-live-from="<id of the section carrying data-live>" with data-v-live / data-cls-live for the live state.
  function applySwitches(scope) {
    scope.querySelectorAll('.fl[data-live-from]').forEach(function (el) {
      var src = document.getElementById(el.getAttribute('data-live-from'));
      if (!src || src.getAttribute('data-live') !== 'true') return;
      var v = el.getAttribute('data-v-live');
      if (v) { el.setAttribute('data-v', v); el.textContent = v; }
      var cls = el.getAttribute('data-cls-live');
      if (cls) { el.className = el.className.replace(/\bst-\w+/g, '').trim() + ' ' + cls; }
    });
  }

  // Every board on the page that carries data-flip. A board in the first screen runs at once; one further
  // down waits until it is scrolled to, then runs once and stays.
  function initBoards() {
    applySwitches(document);
    var boards = Array.prototype.slice.call(document.querySelectorAll('[data-flip]')).filter(function (b) { return !b.closest('[hidden]'); });
    var plans = boards.map(function (board) {
      var rows = Array.prototype.slice.call(board.querySelectorAll('.brow[data-row]'));
      var at = (board.getAttribute('data-flip') || '').split(',').filter(Boolean).map(Number);
      var gap = Number(board.getAttribute('data-gap')) || 640;
      return { board: board, rows: rows, built: rows.map(buildRow), at: at, gap: gap };
    });
    root.classList.remove('flip');
    if (!canAnimate) return;
    function go(p) {
      if (p.done) return;
      p.done = true;
      p.rows.forEach(function (row, i) {
        wait(320 + i * p.gap).then(function () { return animateRow(row, p.built[i], p.at); });
      });
    }
    plans.forEach(function (p) {
      var r = p.board.getBoundingClientRect();
      if (!('IntersectionObserver' in window) || r.top < window.innerHeight) { go(p); return; }
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { io.disconnect(); go(p); } });
      }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
      io.observe(p.board);
    });
  }

  // One orange in view: while one of the page's own orange actions (outside the nav) is on screen, the nav's Book a demo
  // steps back to a hairline (.nav.quiet in board.css); it comes back once none is in view. Phone widths keep the nav's
  // actions inside the menu, so this only matters where the nav shows them.
  function initQuiet() {
    var nav = document.querySelector('.nav');
    if (!nav || !('IntersectionObserver' in window)) return;
    var gos = Array.prototype.slice.call(document.querySelectorAll('.btn.go')).filter(function (b) { return !nav.contains(b); });
    if (!gos.length) return;
    var seen = new Set();
    gos.forEach(function (b) { var r = b.getBoundingClientRect(); if (r.height && r.bottom > 68 && r.top < window.innerHeight) seen.add(b); });
    nav.classList.toggle('quiet', seen.size > 0);
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting && e.target.getClientRects().length) seen.add(e.target); else seen.delete(e.target); });
      nav.classList.toggle('quiet', seen.size > 0);
    }, { rootMargin: '-68px 0px 0px 0px', threshold: 0 });
    gos.forEach(function (b) { io.observe(b); });
  }

  // A figcaption's board row (.ex-row) lands its status word once, as a flap, when its exhibit comes into view:
  // READING, then the word. Reduced motion (or no Web Animations): the word as written.
  function initLand() {
    document.querySelectorAll('.ex-st').forEach(function (el) {
      var v = el.getAttribute('data-v'), via = el.getAttribute('data-via') || 'READING';
      var sr = document.createElement('span');
      sr.className = 'sr';
      sr.textContent = v;
      el.parentNode.insertBefore(sr, el.nextSibling);
      el.setAttribute('aria-hidden', 'true');
      if (!canAnimate || !('IntersectionObserver' in window)) return;
      // The flap's lettering sits in absolute leaves, so hold its width at the longer of the two words first.
      el.textContent = via.length > v.length ? via : v;
      el.style.width = Math.ceil(el.getBoundingClientRect().width) + 'px';
      var f = makeFlap(el, ' ');
      var fig = el.closest('figure') || el;
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (!e.isIntersecting) return;
          io.disconnect();
          wait(260).then(function () {
            el.classList.add('reading');
            return run(f, [via], 190);
          }).then(function () { return wait(520); }).then(function () {
            return run(f, [v], 200, function () { el.classList.remove('reading'); });
          });
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.35 });
      io.observe(fig);
    });
  }

  // Every product window (.win) opens its whole capture full size: click, tap, Enter or Space. The window becomes a
  // button named by its screenshot's alt; a "View full size" label sits on it (hover/focus) or under it (narrow screens).
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
      var w = Number(src.getAttribute('width')) || Math.round((src.naturalWidth || 1600) / 2);
      img.style.setProperty('--lw', w + 'px');
      img.src = src.currentSrc || src.src;
      img.alt = src.alt;
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
      win.setAttribute('aria-label', 'View full size: ' + src.alt);
      var box = document.createElement('div');
      box.className = 'win-box';
      win.parentNode.insertBefore(box, win);
      box.appendChild(win);
      var hint = document.createElement('span');
      hint.className = 'win-hint';
      hint.setAttribute('aria-hidden', 'true');
      hint.textContent = 'View full size';
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
    try { initQuiet(); } catch (e) { /* the nav keeps its orange */ }
    try { initZoom(); } catch (e) { /* the windows stay as pictures */ }
    try { initLand(); } catch (e) { /* the words stay as written */ }
    try { initBoards(); } catch (e) { root.classList.remove('flip'); }
    initMenu();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
