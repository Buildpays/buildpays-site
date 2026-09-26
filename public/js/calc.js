/* CFMEU EBA pay calculator (/guides/cfmeu-eba-pay-calculator). Figures come from
   /js/calc-data.js, generated from data/cfmeu-figures.json; the rules are the ones the
   guides quote: 8 ordinary hours a day paid as 7.2 with 0.8 banked (36-hour week), every
   overtime hour at double time, weekends double time with a 4-hour minimum, public
   holidays and unconsulted RDOs at 250% with a 4-hour minimum, site allowance and
   multi-storey per hour worked, leading hand all-purpose, fares per day attended. */
(function () {
  var D = window.CFMEU_CALC;
  var form = document.getElementById('calc');
  if (!D || !form) return;
  function $(id) { return document.getElementById(id); }
  function num(v) { v = parseFloat(v); return isFinite(v) ? v : 0; }
  function money(n) { return (n < 0 ? '-' : '') + '$' + Math.abs(n).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  var DAYS = ['mon', 'tue', 'wed', 'thu', 'fri'];

  function calc() {
    var cls = $('cls').value;
    var rateInput = $('rate');
    var rate = cls === 'custom' ? num(rateInput.value) : D.rates[cls];
    rateInput.disabled = cls !== 'custom';
    if (cls !== 'custom') rateInput.value = rate.toFixed(2);
    var lh = num($('lh').value), ms = num($('ms').value), site = num($('site').value);
    var base = rate + lh;  // leading hand is an all-purpose allowance: it rides into overtime and penalties

    var ordPaid = 0, ordWorked = 0, otH = 0, weH = 0, penH = 0, rdoH = 0, phH = 0, bank = 0, fares = 0, siteH = 0, ordSiteH = 0, meals = 0, drawn = 0, any = false;
    DAYS.forEach(function (d) {
      var kind = $('k-' + d).value, h = clamp(num($('h-' + d).value), 0, 16);
      if (kind === 'absent') return;
      any = true;
      if (kind === 'rdo') { rdoH += 8; drawn += 8; return; }          // paid from the bank; no fares, no accrual
      if (kind === 'ph') { phH += 7.2; bank += 0.8; return; }          // unworked holiday: ordinary pay, still accrues
      if (h <= 0) return;
      fares++; siteH += h;
      if (kind === 'ord' || kind === 'rdoc') {                          // ordinary day, or a consulted worked RDO
        var o = Math.min(h, 8), ot = h - o;
        ordWorked += o; ordPaid += o * 0.9; bank += o * 0.1; otH += ot; ordSiteH += o;
        if (ot >= 1.5) meals++;
      } else {                                                          // holiday worked, or an RDO worked without consultation
        penH += Math.max(h, 4); bank += 0.8;
      }
    });
    ['sat', 'sun'].forEach(function (d) {
      var h = clamp(num($('h-' + d).value), 0, 16);
      if (h > 0) { any = true; weH += Math.max(h, 4); fares++; siteH += h; }
    });

    var lines = [];
    function line(label, units, unit, r, amount) {
      if (units > 0) lines.push([label, units.toFixed(units % 1 ? 1 : 0) + ' ' + (units === 1 && unit !== 'hrs' ? unit.replace(/s$/, '') : unit), money(r), money(amount)]);
      return amount;
    }
    var gross = 0;
    gross += line('Ordinary hours (8 a day, 7.2 paid, 0.8 banked)', ordPaid, 'hrs', base, ordPaid * base);
    gross += line('RDO taken, paid from the bank', rdoH, 'hrs', base, rdoH * base);
    gross += line('Public holiday not worked', phH, 'hrs', base, phH * base);
    gross += line('Overtime, double time', otH, 'hrs', base * 2, otH * base * 2);
    gross += line('Saturday / Sunday, double time, 4-hour minimum', weH, 'hrs', base * 2, weH * base * 2);
    gross += line('Public holiday or unconsulted RDO worked, 250%, 4-hour minimum', penH, 'hrs', base * 2.5, penH * base * 2.5);
    gross += line('Site allowance, per hour worked', site ? siteH : 0, 'hrs', site, siteH * site);
    gross += line('Multi-storey allowance, per hour worked', ms ? siteH : 0, 'hrs', ms, siteH * ms);
    gross += line('Fares and travel, per day attended', fares, 'days', D.travel, fares * D.travel);
    gross += line('Overtime meal allowance (1.5 hrs or more after finish)', meals, 'meals', D.ot_meal, meals * D.ot_meal);

    var ote = (ordPaid + rdoH + phH) * base + ordSiteH * (site + ms);   // ordinary-time earnings: ordinary hours and the allowances on them
    var sup = any ? Math.max(D.super_weekly, ote * D.super_pct / 100) : 0;
    var inco = any ? D.incolink : 0;

    var tb = $('calc-lines');
    tb.innerHTML = lines.map(function (l) { return '<tr><td>' + l[0] + '</td><td class="n">' + l[1] + '</td><td class="n">' + l[2] + '</td><td class="n">' + l[3] + '</td></tr>'; }).join('') ||
      '<tr><td colspan="4">No hours entered.</td></tr>';
    $('t-gross').textContent = money(gross);
    $('t-super').textContent = money(sup);
    $('t-super-how').textContent = sup > 0 && sup > D.super_weekly + 0.005 ? D.super_pct + '% of ordinary-time earnings (' + money(ote) + ')' : 'the ' + money(D.super_weekly) + ' weekly floor (greater than ' + D.super_pct + '% of ' + money(ote) + ')';
    $('t-inco').textContent = money(inco);
    $('t-bank').textContent = (bank - drawn >= 0 ? '+' : '') + (bank - drawn).toFixed(1) + ' hrs';
    $('t-bank-how').textContent = drawn ? bank.toFixed(1) + ' banked, ' + drawn.toFixed(1) + ' drawn for the RDO' : bank.toFixed(1) + ' banked toward the next RDO';
    $('t-total').textContent = money(gross + sup + inco);
    $('t-ordrate').textContent = money(base);
  }

  form.addEventListener('input', calc);
  form.addEventListener('change', calc);
  form.addEventListener('submit', function (e) { e.preventDefault(); calc(); });
  var reset = $('calc-reset');
  if (reset) reset.addEventListener('click', function () { setTimeout(calc, 0); });
  calc();
})();
