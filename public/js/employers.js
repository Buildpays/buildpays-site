/* Employer list filter on /guides/cfmeu-eba-jobs-victoria. The page is complete
   without it: every company is in the HTML; this only hides rows that do not
   match what is typed. */
(function () {
  var q = document.getElementById('emp-q');
  if (!q) return;
  var items = [].slice.call(document.querySelectorAll('.emp li'));
  var secs = [].slice.call(document.querySelectorAll('.emp-sec'));
  var out = document.getElementById('emp-n');
  var jump = document.querySelector('.emp-jump');
  var total = items.length;
  function norm(s) { return (s || '').toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, ' ').trim(); }
  var keys = items.map(function (li) { return norm(li.getAttribute('data-s') + ' ' + li.textContent); });
  function run() {
    var v = norm(q.value);
    var n = 0;
    items.forEach(function (li, i) {
      var ok = !v || keys[i].indexOf(v) > -1;
      li.hidden = !ok;
      if (ok) n++;
    });
    secs.forEach(function (s) {
      var any = s.querySelector('.emp li:not([hidden])');
      s.hidden = !any;
      var c = s.querySelector('.n');
      if (c) c.textContent = '(' + s.querySelectorAll('.emp li:not([hidden])').length + ')';
    });
    if (jump) jump.hidden = !!v;
    if (out) out.textContent = v ? n + ' of ' + total + ' companies match' : total + ' companies';
  }
  q.addEventListener('input', run);
  if (q.form) q.form.addEventListener('submit', function (e) { e.preventDefault(); });
  run();
})();
