// Page script for paykicker-explainer.html — was inline; moved so the CSP can drop 'unsafe-inline' (audit A24, 7 Sep 2026). Loaded with defer.
//
// Capture mode. Add ?capture=1 to the URL and the page drops its player chrome,
// stops auto-advancing and stops every looping decoration, then exposes
// window.PKX so a screen recorder or a screenshot script can drive it frame by
// frame. That is how this one page becomes a video AND a LinkedIn PDF carousel
// without a second source of truth:
//
//   PKX.count            how many scenes there are
//   PKX.dur(k)           that scene's intended on-screen time, in ms
//   PKX.go(k)            show scene k and restart its entrance animations
//   PKX.settle()         jump every entrance animation to its finished state
//                        (use before a screenshot so nothing is half-flown-in)
//   PKX.index()          which scene is showing
//
// ?scene=N opens straight on scene N (0-based), with or without capture mode.
(function(){
  var params = new URLSearchParams(location.search);
  var capture = params.get('capture') === '1';

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
  var i=0,timer=null,playing=!capture;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if(capture) document.body.classList.add('capture');

  function dur(k){ return +scenes[k].dataset.dur || 7000; }

  scenes.forEach(function(s,k){
    var d=document.createElement('div');d.className='dot';d.innerHTML='<i></i>';
    d.addEventListener('click',function(){ playing=true; pp.textContent='⏸ Pause'; go(k); });
    dotsEl.appendChild(d);
  });
  var dots=[].slice.call(dotsEl.children);

  function show(k){
    scenes.forEach(function(s,x){
      s.classList.toggle('on',x===k);
      s.classList.toggle('bye',x===(k+scenes.length-1)%scenes.length && x!==k);
    });
    // Dusk follows the scene that declares it, so reordering scenes can't
    // desynchronise the sky from the clock in the corner.
    stage.classList.toggle('night', scenes[k].dataset.night === '1');
    dots.forEach(function(d,x){
      d.classList.toggle('done',x<k);
      d.classList.remove('live');d.firstChild.style.animation='none';
      if(x===k){void d.offsetWidth;d.firstChild.style.animation='';
        d.style.setProperty('--dur',dur(k)+'ms');
        d.classList.add('live');}
    });
  }
  function next(){go((i+1)%scenes.length);}
  function go(k){
    clearTimeout(timer);i=k;show(i);
    if(playing){timer=setTimeout(next,reduce?4000:dur(i));}
  }

  pp.addEventListener('click',function(){
    playing=!playing;
    pp.textContent=playing?'⏸ Pause':'▶ Play';
    if(playing){timer=setTimeout(next,2500);}else{clearTimeout(timer);dots[i].classList.remove('live');}
  });
  document.getElementById('restart').addEventListener('click',function(){playing=true;pp.textContent='⏸ Pause';go(0);});

  // Export hook — see the note at the top of this file.
  window.PKX = {
    count: scenes.length,
    dur: dur,
    index: function(){ return i; },
    go: function(k){ playing=false; clearTimeout(timer); go(k); return k; },
    settle: function(){
      var done=0;
      document.getAnimations().forEach(function(a){
        try{
          var t=a.effect && a.effect.getTiming ? a.effect.getTiming() : {};
          if(t.iterations===Infinity){ a.pause(); } else { a.finish(); done++; }
        }catch(e){}
      });
      return done;
    }
  };

  var start = parseInt(params.get('scene'), 10);
  go(Number.isFinite(start) && start>=0 && start<scenes.length ? start : 0);
})();
