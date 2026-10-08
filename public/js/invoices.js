// /invoices — the "how many invoices a month?" slider (TR, 9 Oct 2026). A file, not inline: the site's CSP allows no inline script.
// The bands are the public price list (GST-inclusive); PayKicker's own copy lives in the app (supabase/functions/_shared/invoiceTiers.js).
(function () {
  var BANDS = [
    { top: 20, name: "Lite", price: "$9.99" },
    { top: 100, name: "Starter", price: "$29.99" },
    { top: 400, name: "Business", price: "$69.99" },
    { top: 2000, name: "Pro", price: "$149" }
  ];
  var range = document.getElementById("inv-count");
  var out = document.getElementById("inv-est");
  var cards = document.querySelectorAll(".inv-band");
  if (!range || !out) return;
  function show() {
    var n = Number(range.value) || 0, hit = -1;
    for (var i = 0; i < BANDS.length; i++) { if (n <= BANDS[i].top) { hit = i; break; } }
    for (var j = 0; j < cards.length; j++) cards[j].classList.toggle("here", j === hit);
    var words = hit < 0 ? "Over 2,000 · talk to us" : BANDS[hit].name + " · " + BANDS[hit].price + " a month";
    out.innerHTML = "";
    out.appendChild(document.createTextNode(words));
    var small = document.createElement("small");
    small.textContent = n.toLocaleString("en-AU") + " invoice" + (n === 1 ? "" : "s") + (n >= 2500 ? "+" : "");
    out.appendChild(small);
  }
  range.addEventListener("input", show);
  show();
})();
