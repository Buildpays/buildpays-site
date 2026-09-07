// Page script for paykicker-explainer.html — was inline; moved so the CSP can drop 'unsafe-inline' (audit A24, 7 Sep 2026). Loaded with defer.
(function(){
  // skyline
  var sky=document.getElementById('sky');
  [[0,14,60],[13,9,90],[21,12,44],[32,8,74],[39,16,58],[54,10,96],[63,13,50],[75,11,70],[85,15,40]].forEach(function(b){
    var d=document.createElement('div');d.className='bld';
    d.style.left=b[0]+'%';d.style.width=b[1]+'%';d.style.height=b[2]+'px';sky.appendChild(d);
  });

  var scenes=[].slice.call(document.querySelectorAll('.scene'));
  var dotsEl=document.getElementById('dots');
  var pp=document.getElementById('pp');
  var stage=document.getElementById('stage');
  var i=0,timer=null,playing=true;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  scenes.forEach(function(s,k){
    var d=document.createElement('div');d.className='dot';d.innerHTML='<i></i>';
    d.addEventListener('click',function(){go(k);});
    dotsEl.appendChild(d);
  });
  var dots=[].slice.call(dotsEl.children);

  function show(k){
    scenes.forEach(function(s,x){
      s.classList.toggle('on',x===k);
      s.classList.toggle('bye',x===(k+scenes.length-1)%scenes.length && x!==k);
    });
    stage.classList.toggle('night',k===3); // 4:45pm dusk
    dots.forEach(function(d,x){
      d.classList.toggle('done',x<k);
      d.classList.remove('live');d.firstChild.style.animation='none';
      if(x===k){void d.offsetWidth;d.firstChild.style.animation='';
        d.style.setProperty('--dur',(scenes[k].dataset.dur||7000)+'ms');
        d.classList.add('live');}
    });
  }
  function next(){go((i+1)%scenes.length);}
  function go(k){
    clearTimeout(timer);i=k;show(i);
    if(playing){timer=setTimeout(next,reduce?4000:(+scenes[i].dataset.dur||7000));}
  }
  pp.addEventListener('click',function(){
    playing=!playing;
    pp.textContent=playing?'⏸ Pause':'▶ Play';
    if(playing){timer=setTimeout(next,2500);}else{clearTimeout(timer);dots[i].classList.remove('live');}
  });
  document.getElementById('restart').addEventListener('click',function(){playing=true;pp.textContent='⏸ Pause';go(0);});
  go(0);
})();
