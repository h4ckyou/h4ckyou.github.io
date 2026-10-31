---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,500;0,700;0,800;1,400&display=swap">

<style>
/* ===== h4cky0u // about ============================================= */
.apro{
  --ax:#0ca678; --ax-2:#0a8f6a;
  --glow:rgba(12,166,120,.20);
  --glow-s:rgba(12,166,120,.40);
  --mono:"JetBrains Mono",ui-monospace,"SFMono-Regular","Cascadia Code",Menlo,Consolas,monospace;
  --panel:var(--card-bg,#fff);
  --edge:var(--card-border-color,#ececec);
  --ink:var(--text-color,#34343c);
  --dim:var(--text-muted-color,#8a8a8a);
  --head:var(--heading-color,#2a2a2a);
  --soft:rgba(128,128,128,.06);
  --soft-2:rgba(128,128,128,.11);
  font-family:var(--mono);
  margin:.3rem 0 1.4rem;
}
@media (prefers-color-scheme:dark){
  .apro{--ax:#2ee6a6;--ax-2:#17c78b;--glow:rgba(46,230,166,.15);--glow-s:rgba(46,230,166,.45);}
}
html[data-mode="dark"] .apro{--ax:#2ee6a6;--ax-2:#17c78b;--glow:rgba(46,230,166,.15);--glow-s:rgba(46,230,166,.45);}
html[data-mode="light"] .apro{--ax:#0ca678;--ax-2:#0a8f6a;--glow:rgba(12,166,120,.20);--glow-s:rgba(12,166,120,.40);}
.apro *{box-sizing:border-box;}

/* ---- panel ---- */
.apro .win{
  position:relative;border:1px solid var(--edge);border-radius:14px;
  background:var(--panel);overflow:hidden;margin-bottom:1.15rem;
  box-shadow:0 1px 2px rgba(0,0,0,.04),0 24px 48px -34px var(--glow);
}
.apro .win::before{content:"";position:absolute;inset:0 0 auto 0;height:2px;
  background:linear-gradient(90deg,transparent,var(--ax),transparent);opacity:.65;}
/* HUD corner ticks */
.apro .win::after{content:"";position:absolute;top:10px;right:12px;width:14px;height:14px;
  border-top:1.5px solid var(--ax);border-right:1.5px solid var(--ax);opacity:.35;
  pointer-events:none;transition:opacity .25s;}
.apro .win:hover::after{opacity:.85;}
.apro .bar{
  display:flex;align-items:center;gap:.5rem;padding:.6rem .9rem;
  border-bottom:1px solid var(--edge);
  background:linear-gradient(180deg,var(--soft-2),var(--soft));
  -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);
}
.apro .dot{width:11px;height:11px;border-radius:50%;flex:none;box-shadow:0 0 6px rgba(0,0,0,.15) inset;}
.apro .d1{background:#ff5f57;} .apro .d2{background:#febc2e;} .apro .d3{background:#28c840;}
.apro .bar .tt{margin-left:.45rem;font-size:.76rem;color:var(--dim);letter-spacing:.03em;}
.apro .bar .tt b{color:var(--ax);font-weight:600;}
.apro .body{padding:1.15rem 1.2rem;}

/* ---- hero ---- */
.apro .hero .body{
  display:grid;grid-template-columns:auto 1fr;gap:1.4rem;align-items:center;
  background:
    radial-gradient(760px 220px at 8% -30%,var(--glow),transparent 72%),
    linear-gradient(rgba(128,128,128,.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(128,128,128,.04) 1px,transparent 1px);
  background-size:auto,28px 28px,28px 28px;
}
.apro .idcol{display:flex;flex-direction:column;align-items:center;gap:.55rem;min-width:132px;}
.apro .ava{
  width:118px;height:118px;border-radius:50%;padding:3px;flex:none;
  background:conic-gradient(from 0deg,var(--ax),transparent 38%,var(--ax) 72%,transparent 96%,var(--ax));
  animation:apro-spin 7s linear infinite;
  filter:drop-shadow(0 0 16px var(--glow));
}
.apro .ava i{
  display:block;width:100%;height:100%;border-radius:50%;
  background-size:cover;background-position:center;background-color:var(--panel);
  box-shadow:0 0 0 3px var(--panel) inset;
}
@keyframes apro-spin{to{transform:rotate(360deg)}}
.apro .handle{font-weight:800;color:var(--head);font-size:.98rem;letter-spacing:.01em;}
.apro .loc{font-size:.72rem;color:var(--dim);display:flex;align-items:center;gap:.4rem;}
.apro .loc .live{width:7px;height:7px;border-radius:50%;background:var(--ax);
  box-shadow:0 0 0 0 var(--ax);animation:apro-pulse 1.9s infinite;}
@keyframes apro-pulse{0%{box-shadow:0 0 0 0 var(--glow-s)}70%{box-shadow:0 0 0 7px transparent}100%{box-shadow:0 0 0 0 transparent}}

.apro .term{min-height:150px;}
.apro .ln{margin:.1rem 0;line-height:1.75;font-size:.95rem;color:var(--ink);white-space:pre-wrap;word-break:break-word;}
.apro .pr::before{content:"\279C  ";color:var(--ax);font-weight:700;}
.apro .path{color:#6ea8fe;}
.apro .cmd{color:var(--head);font-weight:600;}
.apro .ok{color:var(--ax);font-weight:500;}
.apro .name{color:var(--ax);font-weight:800;font-size:1.7rem;letter-spacing:.005em;margin:.15rem 0 .05rem;
  text-shadow:0 0 18px var(--glow);}
.apro .tagline{color:var(--dim);font-size:.9rem;}
.apro .cur{display:inline-block;width:.6ch;height:1.05em;vertical-align:-.16em;margin-left:2px;
  background:var(--ax);animation:apro-blink .95s step-end infinite;box-shadow:0 0 8px var(--glow-s);}
@keyframes apro-blink{50%{opacity:0}}

.apro .chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1rem;}
.apro .chip{display:inline-flex;align-items:center;gap:.45rem;padding:.32rem .72rem;border-radius:999px;
  font-size:.79rem;border:1px solid var(--edge);background:var(--soft);color:var(--ink);transition:border-color .2s;}
.apro .chip:hover{border-color:var(--ax);}
.apro .chip i{color:var(--ax);}

/* ---- section label ---- */
.apro .sec{display:flex;align-items:center;gap:.55rem;margin:0 0 .95rem;font-size:.74rem;
  letter-spacing:.18em;text-transform:uppercase;color:var(--dim);}
.apro .sec i{color:var(--ax);}
.apro .sec::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,var(--edge),transparent);}

/* ---- stats ---- */
.apro .grid{display:grid;gap:.75rem;grid-template-columns:repeat(3,1fr);}
.apro .stat{position:relative;border:1px solid var(--edge);border-radius:11px;padding:.95rem .7rem;
  text-align:center;background:var(--soft);overflow:hidden;transition:transform .2s,border-color .2s,box-shadow .2s;}
.apro .stat:hover{transform:translateY(-4px);border-color:var(--ax);box-shadow:0 14px 30px -20px var(--glow-s);}
.apro .stat .n{font-size:1.75rem;font-weight:800;color:var(--ax);line-height:1;letter-spacing:-.02em;
  text-shadow:0 0 16px var(--glow);}
.apro .stat .l{margin-top:.45rem;font-size:.68rem;color:var(--dim);letter-spacing:.09em;}

/* ---- skills ---- */
.apro .skills{display:grid;gap:.75rem;grid-template-columns:repeat(3,1fr);}
.apro .sk{display:flex;gap:.8rem;align-items:center;border:1px solid var(--edge);border-radius:11px;
  padding:.8rem .85rem;background:var(--soft);transition:border-color .2s,transform .2s,box-shadow .2s;}
.apro .sk:hover{border-color:var(--ax);transform:translateY(-3px);box-shadow:0 14px 30px -22px var(--glow-s);}
.apro .sk .ic{width:42px;height:42px;border-radius:11px;flex:none;display:grid;place-items:center;
  color:var(--ax);font-size:1.1rem;border:1px solid var(--edge);
  background:linear-gradient(135deg,var(--glow),transparent);}
.apro .sk b{display:block;color:var(--head);font-size:.92rem;}
.apro .sk span{font-size:.73rem;color:var(--dim);}

/* ---- certs ---- */
.apro .certs{display:flex;flex-wrap:wrap;gap:.6rem;}
.apro .cert{display:inline-flex;align-items:center;gap:.4rem;padding:.42rem .9rem;border-radius:9px;
  font-weight:700;font-size:.82rem;letter-spacing:.05em;color:var(--ax);border:1px solid var(--ax);
  background:var(--glow);transition:transform .2s,box-shadow .2s;}
.apro .cert::before{content:"\2713";font-weight:800;font-size:.82rem;line-height:1;opacity:.9;}
.apro .cert:hover{transform:translateY(-3px);box-shadow:0 0 20px -2px var(--glow-s);}

/* ---- bio ---- */
.apro .bio{border-left:2px solid var(--ax);padding:.1rem 0 .1rem 1rem;color:var(--ink);
  line-height:1.8;font-size:.94rem;}
.apro .bio p{margin:.15rem 0 .75rem;}
.apro .bio p:last-child{margin-bottom:0;}
.apro .bio del{opacity:.5;}
.apro .bio b{color:var(--ax);}

/* ---- code ---- */
.apro pre.code{margin:0;padding:1.05rem 1.2rem;background:transparent;overflow-x:auto;
  font-family:var(--mono);font-size:.86rem;line-height:1.75;color:var(--ink);}
.apro .code .cm{color:var(--dim);font-style:italic;}
.apro .code .kw{color:#c678dd;} .apro .code .fn{color:#61afef;} .apro .code .ax{color:var(--ax);font-weight:700;}
.apro .runbar{display:flex;align-items:center;gap:.5rem;padding:.55rem 1.2rem;border-top:1px solid var(--edge);
  font-size:.73rem;color:var(--dim);background:var(--soft);}
.apro .runbar .live{width:7px;height:7px;border-radius:50%;background:var(--ax);animation:apro-pulse 1.9s infinite;}

/* ---- links ---- */
.apro .links{display:flex;flex-wrap:wrap;gap:.65rem;}
.apro .lk{display:inline-flex;align-items:center;gap:.55rem;text-decoration:none!important;
  padding:.6rem 1rem;border-radius:10px;font-size:.86rem;font-weight:600;border:1px solid var(--edge);
  color:var(--ink)!important;background:var(--soft);
  transition:border-color .2s,color .2s,transform .2s,box-shadow .2s;}
.apro .lk i{font-size:1rem;color:var(--ax);transition:transform .2s;}
.apro .lk:hover{border-color:var(--ax);color:var(--ax)!important;transform:translateY(-3px);
  box-shadow:0 14px 30px -20px var(--glow-s);}
.apro .lk:hover i{transform:scale(1.15);}

/* ---- reveal ---- */
.apro .reveal{opacity:0;transform:translateY(16px);}
.apro .reveal.in{opacity:1;transform:none;transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1);}

@media (prefers-reduced-motion:reduce){
  .apro .ava{animation:none;} .apro .cur{animation:none;}
  .apro .reveal{opacity:1;transform:none;}
}
@media (max-width:768px){
  .apro .hero .body{grid-template-columns:1fr;text-align:center;}
  .apro .idcol{margin:0 auto;}
  .apro .chips{justify-content:center;}
  .apro .grid{grid-template-columns:repeat(2,1fr);}
  .apro .skills{grid-template-columns:1fr;}
  .apro .name{font-size:1.45rem;}
}
</style>

<div class="apro" markdown="0">

  <div class="win hero">
    <div class="bar">
      <span class="dot d1"></span><span class="dot d2"></span><span class="dot d3"></span>
      <span class="tt"><b>mark</b>@h4cky0u: ~</span>
    </div>
    <div class="body">
      <div class="idcol">
        <span class="ava"><i style="background-image:url('https://avatars.githubusercontent.com/u/127159644')"></i></span>
        <span class="handle">@h4cky0u</span>
        <span class="loc"><span class="live"></span> root@offsec</span>
      </div>
      <div class="term" data-term>
        <div class="ln"><span class="pr"></span><span class="path">~</span> <span class="cmd">ssh mark@h4ckyou.github.io</span></div>
        <div class="ln ok">[ok] secure channel established</div>
        <div class="ln"><span class="pr"></span><span class="path">~</span> <span class="cmd">whoami</span></div>
        <div class="ln name">Mark Uchechukwu</div>
        <div class="ln tagline">Offensive Security · CTF Player · Binary Exploitation</div>
        <div class="chips">
          <span class="chip"><i class="fas fa-graduation-cap"></i> Computer Science Student</span>
          <span class="chip"><i class="fab fa-discord"></i> @h4cky0u</span>
          <span class="chip"><i class="fas fa-bug"></i> wannabe hacker in progress</span>
        </div>
      </div>
    </div>
  </div>

  <div class="win reveal">
    <div class="bar">
      <span class="dot d1"></span><span class="dot d2"></span><span class="dot d3"></span>
      <span class="tt">~/stats</span>
    </div>
    <div class="body">
      <div class="grid">
        <div class="stat"><div class="n" data-count="4" data-pad="2">00</div><div class="l">CERTIFICATIONS</div></div>
        <div class="stat"><div class="n">24/7</div><div class="l">UPTIME · PWNING</div></div>
        <div class="stat"><div class="n">0x00</div><div class="l">GRASS TOUCHED</div></div>
      </div>
    </div>
  </div>

  <div class="win reveal">
    <div class="bar">
      <span class="dot d1"></span><span class="dot d2"></span><span class="dot d3"></span>
      <span class="tt">~/skills --list</span>
    </div>
    <div class="body">
      <div class="sec"><i class="fas fa-terminal"></i> core skills</div>
      <div class="skills">
        <div class="sk"><span class="ic"><i class="fas fa-crosshairs"></i></span><div><b>Pwn</b><span>binary exploitation</span></div></div>
        <div class="sk"><span class="ic"><i class="fas fa-microchip"></i></span><div><b>Reverse Engineering</b><span>take it apart</span></div></div>
        <div class="sk"><span class="ic"><i class="fas fa-shield-halved"></i></span><div><b>Offensive Security</b><span>break &amp; report</span></div></div>
      </div>
      <div class="sec" style="margin-top:1.25rem"><i class="fas fa-certificate"></i> certifications</div>
      <div class="certs">
        <span class="cert">CPTS</span><span class="cert">OSCP</span><span class="cert">CRTA</span><span class="cert">CPENT</span>
      </div>
    </div>
  </div>

  <div class="win reveal">
    <div class="bar">
      <span class="dot d1"></span><span class="dot d2"></span><span class="dot d3"></span>
      <span class="tt">~/cat about.md</span>
    </div>
    <div class="body">
      <div class="bio">
        <p>I enjoy <b>breaking things</b> and understanding how they work &mdash; wannabe hacker in progress.</p>
        <p>When I'm not <del>pwning</del>, I'm probably watching anime.</p>
        <p>When I'm not watching anime, I'm probably not touching grass &#128517;</p>
      </div>
    </div>
  </div>

  <div class="win reveal">
    <div class="bar">
      <span class="dot d1"></span><span class="dot d2"></span><span class="dot d3"></span>
      <span class="tt">~/life.c</span>
    </div>
<pre class="code"><span class="kw">void</span> <span class="fn">Eat</span>(<span class="kw">void</span>);
<span class="kw">void</span> <span class="fn">Sleep</span>(<span class="kw">void</span>);
<span class="kw">void</span> <span class="fn">Pwn</span>(<span class="kw">void</span>);
<span class="kw">void</span> <span class="fn">Repeat</span>(<span class="kw">void</span>);

<span class="kw">int</span> <span class="fn">main</span>(<span class="kw">void</span>) {
    <span class="kw">for</span> (;;) {        <span class="cm">// the only loop that never segfaults</span>
        <span class="fn">Eat</span>();
        <span class="fn">Sleep</span>();
        <span class="ax">Pwn</span>();
        <span class="fn">Repeat</span>();
    }
}</pre>
    <div class="runbar"><span class="live"></span> process running &middot; pid 1337 &middot; press ^C to touch grass</div>
  </div>

  <div class="win reveal">
    <div class="bar">
      <span class="dot d1"></span><span class="dot d2"></span><span class="dot d3"></span>
      <span class="tt">~/connect</span>
    </div>
    <div class="body">
      <div class="sec"><i class="fas fa-satellite-dish"></i> find me</div>
      <div class="links">
        <a class="lk" href="https://github.com/h4ckyou" target="_blank" rel="noopener"><i class="fab fa-github"></i> github</a>
        <a class="lk" href="https://twitter.com/markuche1337" target="_blank" rel="noopener"><i class="fab fa-x-twitter"></i> twitter</a>
        <span class="lk" style="cursor:default"><i class="fab fa-discord"></i> @h4cky0u</span>
      </div>
    </div>
  </div>

</div>

<script>
(function(){
  var root=document.querySelector('.apro'); if(!root) return;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* reveal on scroll */
  var rev=root.querySelectorAll('.reveal');
  if(reduce||!('IntersectionObserver'in window)){rev.forEach(function(el){el.classList.add('in');});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12});
    rev.forEach(function(el){io.observe(el);});}

  /* count-up */
  function pad(v,p){v=String(v);while(p&&v.length<p)v='0'+v;return v;}
  root.querySelectorAll('[data-count]').forEach(function(el){
    var target=parseInt(el.getAttribute('data-count'),10)||0,p=parseInt(el.getAttribute('data-pad')||'0',10);
    if(reduce){el.textContent=pad(target,p);return;}
    var dur=1200,start=null;
    function step(ts){if(!start)start=ts;var k=Math.min((ts-start)/dur,1);
      var v=Math.round(target*(0.5-Math.cos(k*Math.PI)/2));el.textContent=pad(v,p);
      if(k<1)requestAnimationFrame(step);}
    setTimeout(function(){requestAnimationFrame(step);},500);
  });

  /* terminal typing */
  var term=root.querySelector('[data-term]'); if(!term) return;
  var chips=term.querySelector('.chips');
  if(reduce){ return; } /* keep static content */
  var steps=[
    {prompt:1,type:1,text:'ssh mark@h4ckyou.github.io',speed:34,after:230},
    {cls:'ok',text:'[ok] secure channel established',before:200,after:200},
    {prompt:1,type:1,text:'whoami',speed:60,after:250},
    {cls:'name',type:1,text:'Mark Uchechukwu',speed:72,after:160},
    {cls:'tagline',text:'Offensive Security · CTF Player · Binary Exploitation',before:100,after:120}
  ];
  /* clear static lines but keep chips */
  Array.prototype.slice.call(term.children).forEach(function(c){if(c!==chips)term.removeChild(c);});
  if(chips)chips.style.opacity='0';
  var cur=document.createElement('span');cur.className='cur';
  var i=0;
  function mkPrompt(el){var p=document.createElement('span');p.className='pr';el.appendChild(p);
    var path=document.createElement('span');path.className='path';path.textContent='~';el.appendChild(path);
    el.appendChild(document.createTextNode(' '));}
  function next(){
    if(i>=steps.length){ if(chips){chips.style.transition='opacity .5s';chips.style.opacity='1';}
      var last=term.querySelectorAll('.ln');(last[last.length-1]||term).appendChild(cur);return; }
    var s=steps[i++];var el=document.createElement('div');el.className='ln '+(s.cls||'');
    if(cur.parentNode)cur.parentNode.removeChild(cur);
    if(s.prompt)mkPrompt(el);
    var txt=document.createElement('span');if(s.prompt)txt.className='cmd';el.appendChild(txt);
    el.appendChild(cur);
    (function place(){ term.insertBefore(el, chips||null); })();
    if(s.type){var j=0;setTimeout(function tick(){txt.textContent=s.text.slice(0,j++);
      if(j<=s.text.length)setTimeout(tick,s.speed||45);else setTimeout(next,s.after||220);},s.before||0);}
    else{setTimeout(function(){txt.textContent=s.text;setTimeout(next,s.after||180);},s.before||120);}
  }
  next();
})();
</script>
