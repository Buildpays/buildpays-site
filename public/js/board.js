// The board: split-flap rows on the homepage, plus the phone menu.
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

  function animateRow(row, cells) {
    row.classList.add('moving');
    var byCol = function (sel) {
      return cells.filter(function (c) { return c.el.parentNode.matches(sel); })[0];
    };
    var time = byCol('.c-time'), entry = byCol('.c-entry'), amt = byCol('.c-amt'),
        acct = byCol('.c-acct'), job = byCol('.c-job'), gst = byCol('.c-gst'), stat = byCol('.c-stat');
    var jobs = [];
    function chars(c, start, stagger, spin) {
      c.chars.forEach(function (ch, i) {
        if (ch.v === ' ' || !ch.f) return;
        jobs.push(wait(start + i * stagger).then(function () {
          return run(ch.f, churn(ch.v, spin + (i % 3)), 74);
        }));
      });
    }
    chars(time, 0, 34, 2);
    jobs.push(wait(110).then(function () { return run(entry.f, [entry.v], 210); }));
    chars(amt, 180, 30, 3);
    var reading = wait(240).then(function () {
      stat.el.classList.add('reading');
      return run(stat.f, [stat.via], 190);
    });
    [acct, job, gst].forEach(function (c, i) {
      jobs.push(wait(620 + i * 120).then(function () { return run(c.f, [c.v], 200); }));
    });
    return Promise.all(jobs.concat([reading])).then(function () { return wait(160); }).then(function () {
      return run(stat.f, [stat.v], 200, function () { stat.el.classList.remove('reading'); });
    }).then(function () {
      row.classList.remove('moving');
    });
  }

  function initBoard() {
    var board = document.getElementById('board');
    if (!board) return;
    var rows = Array.prototype.slice.call(board.querySelectorAll('.brow[data-row]'));
    var built = rows.map(buildRow);
    root.classList.remove('flip');
    if (!canAnimate) return;
    // One orchestrated run: rows start in sequence, overlap a little, settle, and stay.
    rows.forEach(function (row, i) {
      wait(320 + i * 640).then(function () { return animateRow(row, built[i]); });
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
    try { initBoard(); } catch (e) { root.classList.remove('flip'); }
    initMenu();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
