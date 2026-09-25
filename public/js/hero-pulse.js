/* Hero pulse (desktop grid only): the worker's tap travels the set-out lines
   from the timesheet, left along the top of the "Roster the crew" cell to its
   right edge, down that edge, then right along its bottom line into the MYOB file. Phone widths keep
   the CSS-only vertical pulse. */
(function () {
  'use strict';
  var grid = document.querySelector('.setout');
  if (!grid || !('animate' in Element.prototype) || !CSS.supports('offset-path', 'path("M0 0")')) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var wide = window.matchMedia('(min-width: 861px)');
  var ph = grid.querySelector('.ph'), dot = grid.querySelector('.ph .dot');
  var tap = grid.querySelector('.phone .tap'), sb = grid.querySelector('.sb');
  var my = grid.querySelector('.my'), file = grid.querySelector('.file');
  var stub = my && my.querySelector('.stub2');
  if (!ph || !dot || !tap || !sb || !my || !file) return;
  var anim = null, timer = null;

  function layout() {
    var p = ph.getBoundingClientRect(), t = tap.getBoundingClientRect();
    var s = sb.getBoundingClientRect(), m = my.getBoundingClientRect(), f = file.getBoundingClientRect();
    // Coordinates relative to .ph (the dot's containing block).
    var x0 = t.left + t.width / 2 - p.left, y0 = t.bottom - p.top;
    var yTop = s.top - p.top;            // A/B grid line
    var xLeft = s.right - p.left;        // right edge of the "Roster the crew" cell
    var yBot = s.bottom - p.top;         // B/C grid line
    var xEnd = f.left - p.left;          // the file's left edge
    var d = 'M' + x0 + ' ' + y0 + ' V' + yTop + ' H' + xLeft + ' V' + yBot + ' H' + xEnd;
    if (stub) {
      stub.style.top = (s.bottom - m.top) + 'px';
      stub.style.width = (f.left - m.left) + 'px';
    }
    file.style.setProperty('--arrive', (s.bottom - f.top) + 'px');
    return { d: d, len: (y0 > yTop ? 0 : yTop - y0) + (x0 - xLeft) + (yBot - yTop) + (xEnd - xLeft) };
  }

  function run() {
    if (anim) { anim.cancel(); anim = null; }
    if (timer) { clearTimeout(timer); timer = null; }
    file.classList.remove('lit');
    if (!wide.matches) { dot.style.offsetPath = ''; dot.style.opacity = ''; return; }
    if (reduce.matches) { file.classList.add('lit'); return; }
    var g = layout();
    dot.style.offsetPath = 'path("' + g.d + '")';
    dot.style.offsetRotate = '0deg';
    dot.style.left = '0'; dot.style.top = '0'; dot.style.margin = '0';
    var dur = Math.max(6000, Math.min(12000, g.len * 12));
    anim = dot.animate(
      [{ offsetDistance: '0%', opacity: 0 }, { offsetDistance: '4%', opacity: 1 }, { offsetDistance: '96%', opacity: 1 }, { offsetDistance: '100%', opacity: 0 }],
      { duration: dur, delay: 400, easing: 'linear', fill: 'forwards' });
    timer = setTimeout(function () { file.classList.add('lit'); }, dur + 300);
  }

  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(run); } else { run(); }
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { if (wide.matches) { var g = layout(); dot.style.offsetPath = 'path("' + g.d + '")'; } }, 120); });
})();
