// Shopfront homepage: the fascia's phone-width menu. Loaded in <head> (no defer) so the
// .js class lands before first paint; the wiring waits for the DOM.
document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', function () {
  var fascia = document.querySelector('.fascia');
  var toggle = fascia && fascia.querySelector('.fascia__toggle');
  if (!toggle) return;
  var label = toggle.querySelector('.lbl');

  function set(open) {
    if (open) fascia.setAttribute('data-open', ''); else fascia.removeAttribute('data-open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (label) label.textContent = open ? 'Close' : 'Menu';
  }

  toggle.addEventListener('click', function () {
    set(!fascia.hasAttribute('data-open'));
  });

  fascia.querySelectorAll('.fascia__nav a').forEach(function (a) {
    a.addEventListener('click', function () { set(false); });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && fascia.hasAttribute('data-open')) { set(false); toggle.focus(); }
  });

  var wide = window.matchMedia('(min-width: 1180px)');
  var onWide = function (m) { if (m.matches) set(false); };
  if (wide.addEventListener) wide.addEventListener('change', onWide); else wide.addListener(onWide);
});
