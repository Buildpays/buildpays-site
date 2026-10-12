// The statements tabulate once. When a statement ([data-tabulate]) scrolls into view, each row's
// figures settle digit by digit, left to right (about 600 ms, exponential ease-out), then the row's
// note marker lights and its note slides into the margin. Everything stays lit afterwards.
// Reduced motion, or no IntersectionObserver: nothing runs and the page is already at rest.
(function () {
  var stmts = document.querySelectorAll('[data-tabulate]');
  if (!stmts.length) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window) || !window.requestAnimationFrame) return;

  var DUR = 600, STAGGER = 150;
  function easeOutExpo(t) { return t >= 1 ? 1 : 1 - Math.pow(2, -10 * t); }

  function tabulate(el, delay, done) {
    var final = el.textContent;
    var slots = [];
    for (var i = 0; i < final.length; i++) if (/\d/.test(final[i])) slots.push(i);
    var start = null;
    function frame(now) {
      if (start === null) start = now + delay;
      var t = Math.max(0, (now - start) / DUR);
      var locked = Math.floor(easeOutExpo(Math.min(t, 1)) * slots.length);
      if (t >= 1) { el.textContent = final; if (done) done(); return; }
      var out = final.split('');
      for (var k = locked; k < slots.length; k++) out[slots[k]] = String((Math.random() * 10) | 0);
      el.textContent = out.join('');
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function run(stmt) {
    var rows = stmt.querySelectorAll('[data-row]');
    Array.prototype.forEach.call(rows, function (row, i) {
      var figs = row.querySelectorAll('[data-fig]');
      var pending = figs.length;
      var light = function () { row.classList.add('is-lit'); };
      if (!pending) { setTimeout(light, i * STAGGER); return; }
      Array.prototype.forEach.call(figs, function (f) {
        tabulate(f, i * STAGGER, function () { if (--pending === 0) light(); });
      });
    });
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      run(e.target);
    });
  }, { threshold: 0.3 });

  Array.prototype.forEach.call(stmts, function (s) {
    s.classList.add('is-armed');
    io.observe(s);
  });
})();
