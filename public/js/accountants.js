// /accountants — the earnings calculator ("What would you earn?") and the two "Open a practice account" buttons, which
// carry the visit's utm_* on to the app (the page is reached from an email). A file, not inline: the site's CSP allows no
// inline script. Without script the page shows its worked examples instead and the buttons stay plain links.
(function () {
  // ---- THE RATES. They mirror the app: change them there first, then here.
  //   supabase/functions/_shared/partners.js REFERRAL: the client's first 3 charged bills are 50 % off; the partner earns
  //     15 % of the total (inc GST) of each of the client's first 12 charged bills, rounded half up per bill (shareCents).
  //   The price lists, EX GST as the app stores them, so a bill's +10 % GST (round(sub / 10), bill_raise_month) lands on
  //     the advertised price: _shared/invoiceTiers.js SELF_SERVE_TIERS (908 + 91 = $9.99, 2726 + 273 = $29.99,
  //     6363 + 636 = $69.99) and _shared/squareTiers.js SQUARE_TIERS (Sales sync up to 500 orders, 908 + 91 = $9.99).
  //   A month is ONE bill: its lines summed ex GST, the referral discount taken off that sum, then GST added (referralPlan).
  var REFERRAL = { discountPercent: 50, discountBills: 3, sharePercent: 15, shareBills: 12 };
  var PLAN_CENTS = { 'inv-999': 908, 'inv-2999': 2726, 'inv-6999': 6363 };   // Invoices bands, a month ex GST
  var SALES_SYNC_CENTS = 908;                                                // Sales sync up to 500 orders, a month ex GST
  var MAX_CLIENTS = 1000;

  // Integer cents throughout, every amount positive, so "round" is half up.
  function gst(sub) { return Math.floor((sub + 5) / 10); }                                       // round(sub / 10)
  function discount(sub) { return Math.floor((sub * REFERRAL.discountPercent + 50) / 100); }     // Math.round(sub × 50 %)
  function share(total) { return Math.floor((total * REFERRAL.sharePercent + 50) / 100); }       // shareCents(total)

  // One client's 12 bills: the first 3 after the discount, the rest at the full price; 15 % of each bill's total.
  function feeForClient(sub) {
    var cut = sub - discount(sub), fee = 0;
    for (var bill = 1; bill <= REFERRAL.shareBills; bill++) {
      var s = bill <= REFERRAL.discountBills ? cut : sub;
      fee += share(s + gst(s));
    }
    return fee;
  }

  function dollars(cents) { return '$' + Math.round(cents / 100).toLocaleString('en-AU'); }
  function exact(cents) { return '$' + (cents / 100).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }

  function initCalc() {
    var calc = document.getElementById('acc-calc');
    var n = document.getElementById('acc-n');
    var sales = document.getElementById('acc-sales');
    var out = document.getElementById('acc-total');
    var each = document.getElementById('acc-each');
    if (!calc || !n || !sales || !out || !each) return;

    function show() {
      var picked = calc.querySelector('input[name="acc-plan"]:checked');
      var sub = (picked ? PLAN_CENTS[picked.value] || 0 : 0) + (sales.checked ? SALES_SYNC_CENTS : 0);
      var count = Math.floor(Number(n.value));
      out.textContent = '';
      if (!(count >= 1) || !sub) {
        out.appendChild(document.createTextNode('Enter how many clients'));
        each.textContent = '';
        return;
      }
      count = Math.min(count, MAX_CLIENTS);
      var perClient = feeForClient(sub);
      out.appendChild(document.createTextNode('About ' + dollars(perClient * count) + ' '));
      var small = document.createElement('small');
      small.textContent = 'in their first year';
      out.appendChild(small);
      each.textContent = count === 1 ? exact(perClient) + ' from one client.'
        : exact(perClient) + ' a client × ' + count.toLocaleString('en-AU') + ' clients.';
    }

    calc.addEventListener('input', show);
    calc.addEventListener('change', show);
    calc.hidden = false;
    var ex = document.getElementById('acc-ex');
    if (ex) ex.hidden = true;
    show();
  }

  // The visit's utm_* ride on to the app's practice sign-up, so the app knows the email that brought the firm.
  function initUtm() {
    var q;
    try { q = new URLSearchParams(location.search); } catch (e) { return; }
    var have = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'].filter(function (k) { return q.get(k); });
    if (!have.length) return;
    Array.prototype.forEach.call(document.querySelectorAll('a[data-utm]'), function (a) {
      try {
        var u = new URL(a.href);
        have.forEach(function (k) { u.searchParams.set(k, q.get(k).slice(0, 100)); });
        a.href = u.toString();
      } catch (e) { /* the plain link stays */ }
    });
  }

  try { initCalc(); } catch (e) { /* the worked examples stay */ }
  try { initUtm(); } catch (e) { /* the buttons stay plain */ }
})();
