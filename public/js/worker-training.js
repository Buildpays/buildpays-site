// Page script for paykicker-worker-training.html — was inline; moved so the CSP can drop 'unsafe-inline' (audit A24, 7 Sep 2026). Loaded with defer.
(function(){
  var scenes=[].slice.call(document.querySelectorAll('.scene'));
  var dotsEl=document.getElementById('dots'),pp=document.getElementById('pp');
  var i=0,timer=null,playing=true;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  scenes.forEach(function(s,k){
    var d=document.createElement('div');d.className='dot';d.innerHTML='<i></i>';
    d.addEventListener('click',function(){go(k);});dotsEl.appendChild(d);
  });
  var dots=[].slice.call(dotsEl.children);
  function show(k){
    scenes.forEach(function(s,x){s.classList.toggle('on',x===k);});
    dots.forEach(function(d,x){
      d.classList.toggle('done',x<k);
      d.classList.remove('live');d.firstChild.style.animation='none';
      if(x===k){void d.offsetWidth;d.firstChild.style.animation='';
        d.style.setProperty('--dur',(scenes[k].dataset.dur||7500)+'ms');d.classList.add('live');}
    });
  }
  function next(){go((i+1)%scenes.length);}
  function go(k){clearTimeout(timer);i=k;show(i);
    if(playing){timer=setTimeout(next,reduce?4500:(+scenes[i].dataset.dur||7500));}}
  pp.addEventListener('click',function(){
    playing=!playing;pp.textContent=playing?'⏸ Pause':'▶ Play';
    if(playing){timer=setTimeout(next,2500);}else{clearTimeout(timer);dots[i].classList.remove('live');}
  });
  document.getElementById('restart').addEventListener('click',function(){playing=true;pp.textContent='⏸ Pause';go(0);});
  go(0);
})();
