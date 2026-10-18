// /join: tick plans, see what the month costs, hand off to the app's sign-up.
// A file, not inline: the site's CSP allows no inline script.
//
// The app's /signup takes a comma list (for=invoices,square; via=xero|myob; ref=CODE) since app pass 857.
// MULTI false would send only the first ticked plan and say the rest is added after sign-up.
(function () {
  var MULTI = true;
  var SIGNUP = 'https://app.paykicker.com.au/signup';
  var ORDER = ['invoices', 'square'];
  var PLANS = {
    invoices: {
      name: 'Supplier invoices',
      cost: '$0 for 14 days or 8 invoices read, then $9.99 to $149 a month by how many you had',
      pitch: 'Supplier invoices: forward the bill, it lands coded. 14 days free.',
      href: '/ap-automation'
    },
    square: {
      name: 'Square sales sync',
      cost: '$0 up to 60 orders a month; $9.99 up to 500; $29.99 unlimited; any number of shops',
      pitch: 'Square sales sync: each shop’s day posted every night. Free up to 60 orders a month.',
      soon: 'Square sales sync opens soon.',
      href: '/integrations#square-myob'
    }
  };

  var box = document.getElementById('plans');
  if (!box) return;
  var lines = document.getElementById('t-lines');
  var total = document.getElementById('t-total');
  var suggest = document.getElementById('t-suggest');
  var note = document.getElementById('j-note');
  var go = { xero: document.getElementById('go-xero'), myob: document.getElementById('go-myob'), email: document.getElementById('go-email') };
  var q = new URLSearchParams(location.search);
  var ref = (q.get('ref') || '').slice(0, 40);

  // The Square row follows its switch: data-live="true" opens the tick.
  var sq = document.getElementById('j-square');
  var squareLive = sq && sq.getAttribute('data-live') === 'true';
  if (sq) {
    var sqIn = sq.querySelector('input');
    sqIn.disabled = !squareLive;
    sq.classList.toggle('off', !squareLive);
  }

  // ?for=square,invoices pre-ticks (only plans that are open).
  if (q.get('for')) {
    var want = q.get('for').toLowerCase().split(',');
    box.querySelectorAll('input[name=plan]').forEach(function (el) {
      if (!el.disabled) el.checked = want.indexOf(el.value) > -1;
    });
  }

  function ticked() {
    return ORDER.filter(function (k) {
      var el = box.querySelector('input[value="' + k + '"]');
      return el && el.checked && !el.disabled;
    });
  }

  function li(a, b) {
    var x = document.createElement('li');
    var s1 = document.createElement('span'); s1.textContent = a; x.appendChild(s1);
    if (b != null) { var s2 = document.createElement('span'); s2.textContent = b; x.appendChild(s2); }
    return x;
  }

  function url(sent, via) {
    var p = new URLSearchParams();
    p.set('for', sent.join(','));
    if (via) p.set('via', via);
    if (ref) p.set('ref', ref);
    return SIGNUP + '?' + p.toString().replace(/%2C/g, ',');
  }

  function show() {
    var on = ticked();
    lines.textContent = '';
    on.forEach(function (k) { lines.appendChild(li(PLANS[k].name, PLANS[k].cost)); });
    if (!on.length) {
      var e = li('Tick a plan to see what the month costs.');
      e.className = 't-empty';
      lines.appendChild(e);
    }
    total.hidden = !on.length;

    suggest.textContent = '';
    ORDER.forEach(function (k) {
      if (on.indexOf(k) > -1) return;
      var x = document.createElement('li');
      var p = PLANS[k];
      var a = document.createElement('a');
      a.href = p.href;
      if (k === 'square' && !squareLive) { x.appendChild(document.createTextNode(p.soon + ' ')); a.textContent = 'What it posts'; }
      else { x.appendChild(document.createTextNode(p.pitch + ' ')); a.textContent = 'More'; }
      x.appendChild(a);
      suggest.appendChild(x);
    });
    var crew = document.createElement('li');
    crew.appendChild(document.createTextNode('Run construction crews? '));
    var ca = document.createElement('a'); ca.href = '/construction'; ca.textContent = 'The crew system';
    crew.appendChild(ca);
    crew.appendChild(document.createTextNode(' is set up with you after a demo.'));
    suggest.appendChild(crew);

    var sent = MULTI ? on : on.slice(0, 1);
    Object.keys(go).forEach(function (via) {
      var a = go[via];
      if (!a) return;
      if (!on.length) { a.setAttribute('aria-disabled', 'true'); a.removeAttribute('href'); return; }
      a.removeAttribute('aria-disabled');
      a.href = url(sent, via === 'email' ? null : via);
    });
    note.textContent = !MULTI && on.length > 1
      ? PLANS[on[1]].name + ' is added after sign-up for now: you sign up with ' + PLANS[on[0]].name.toLowerCase() + ' first.'
      : '';
  }

  box.addEventListener('change', show);
  show();
})();
