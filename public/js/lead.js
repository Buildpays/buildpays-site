// Lead attribution + demo-form submit — was the inline <script> at the foot of index.html.
// Moved to a file so the CSP can drop 'unsafe-inline' for scripts (security audit A24, 7 Sep 2026).
// Loaded with defer, so the form and its hidden fields exist when this runs.
/* ---------------------------------------------------------------------------
   Lead attribution.
   Records how this visitor arrived (UTM tags, Google Ads click id, or referrer)
   and keeps it for the whole session, so an enquiry submitted after a bit of
   clicking around still reports the original source. The result is written into
   hidden form fields, so the enquiry EMAIL itself names the source — that works
   even when analytics is blocked. The same values are sent to GA4.
--------------------------------------------------------------------------- */
(function(){
  var KEY='bp_attribution';
  var SEARCH_ENGINES=/(^|\.)(google|bing|duckduckgo|yahoo|ecosia|brave)\./i;

  function readStored(){
    try { return JSON.parse(sessionStorage.getItem(KEY)||'null'); } catch(e){ return null; }
  }
  function store(v){
    try { sessionStorage.setItem(KEY, JSON.stringify(v)); } catch(e){}
  }

  function capture(){
    var q=new URLSearchParams(location.search);
    var attr={
      utm_source:  q.get('utm_source')  || '',
      utm_medium:  q.get('utm_medium')  || '',
      utm_campaign:q.get('utm_campaign')|| '',
      utm_term:    q.get('utm_term')    || '',
      utm_content: q.get('utm_content') || '',
      gclid:       q.get('gclid')       || '',
      referrer:    document.referrer    || '',
      landing_page: location.pathname + location.search,
      first_seen:  new Date().toISOString()
    };
    var prior=readStored();
    /* First touch wins, unless this hit carries campaign tags — a tagged link is
       a deliberate signal and should override an earlier untagged landing. */
    if(prior && !attr.utm_source && !attr.gclid) return prior;
    store(attr);
    return attr;
  }

  function describe(a){
    if(a.utm_source){
      var s=a.utm_source + (a.utm_medium ? ' / ' + a.utm_medium : '');
      return a.utm_campaign ? s + ' — ' + a.utm_campaign : s;
    }
    if(a.gclid) return 'google / cpc (Google Ads)';
    if(a.referrer){
      var host='';
      try { host=new URL(a.referrer).hostname; } catch(e){}
      if(!host) return 'direct / none';
      if(host===location.hostname) return 'direct / none';
      if(SEARCH_ENGINES.test(host)) return host + ' / organic search';
      return host + ' / referral';
    }
    return 'direct / none';
  }

  var attribution = capture();

  function fill(){
    var map={
      f_lead_source: describe(attribution),
      f_utm_source: attribution.utm_source,
      f_utm_medium: attribution.utm_medium,
      f_utm_campaign: attribution.utm_campaign,
      f_utm_term: attribution.utm_term,
      f_utm_content: attribution.utm_content,
      f_gclid: attribution.gclid,
      f_referrer: attribution.referrer,
      f_landing_page: attribution.landing_page,
      f_first_seen: attribution.first_seen
    };
    Object.keys(map).forEach(function(id){
      var el=document.getElementById(id);
      if(el) el.value=map[id];
    });
  }
  fill();

  /* ------------------------------------------------------------------ form */
  var f=document.getElementById('demoForm'), b=document.getElementById('demoBtn'), m=document.getElementById('demoMsg');
  if(!f) return;
  f.addEventListener('submit', function(e){
    e.preventDefault();
    fill(); /* refresh in case the visitor arrived via a tagged link mid-session */
    /* hCaptcha (Web3Forms' zero-config integration, security audit A24): the widget writes
       its token into a hidden h-captcha-response field inside the form; Web3Forms verifies it
       server-side. An empty token means the box was not ticked — say so instead of posting. */
    var cap=f.querySelector('[name="h-captcha-response"]');
    if(cap && !cap.value){ m.style.color='#c62828'; m.textContent='Please tick the "I am human" box first.'; return; }
    b.disabled=true; b.textContent='Sending…'; m.textContent=''; m.style.color='#5c7089';
    fetch('https://api.web3forms.com/submit',{
      method:'POST',
      headers:{'Content-Type':'application/json',Accept:'application/json'},
      body:JSON.stringify(Object.fromEntries(new FormData(f)))
    })
    .then(function(r){return r.json();})
    .then(function(d){
      if(d.success){
        /* GA4 conversion — fires only on a confirmed successful submission. */
        if(typeof gtag==='function'){
          gtag('event','generate_lead',{
            lead_source:  describe(attribution),
            source:       attribution.utm_source   || undefined,
            medium:       attribution.utm_medium   || undefined,
            campaign:     attribution.utm_campaign || undefined,
            landing_page: attribution.landing_page,
            currency:'AUD', value:1
          });
        }
        f.reset();
        b.style.display='none';
        m.style.color='#2e7d32';
        m.textContent="✓ Thanks — we'll be in touch within one business day.";
      } else { throw new Error(d.message||'failed'); }
    })
    .catch(function(){
      if(window.hcaptcha && typeof hcaptcha.reset==='function'){ try { hcaptcha.reset(); } catch(e){} }
      b.disabled=false; b.textContent='Book my demo';
      m.style.color='#c62828';
      m.innerHTML="Something went wrong. Email us directly at <a href='mailto:operations@paykicker.com.au' style='color:#f25c1f'>operations@paykicker.com.au</a>.";
    });
  });
})();
