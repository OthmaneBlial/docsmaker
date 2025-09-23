(function(){
  var body=document.body, btn=document.querySelector('.menu-btn'), ov=document.querySelector('.overlay');
  btn&&btn.addEventListener('click',function(){ body.classList.toggle('open'); });
  ov&&ov.addEventListener('click',function(){ body.classList.remove('open'); });
  function setTheme(m){ var d=document.documentElement; if(m==='dark') d.classList.add('dark'); else d.classList.remove('dark'); localStorage.setItem('theme',m);}
  var saved=localStorage.getItem('theme'); if(saved){ setTheme(saved); }
  document.getElementById('themeBtn').addEventListener('click',function(){ setTheme(document.documentElement.classList.contains('dark')?'light':'dark'); });
  Array.prototype.forEach.call(document.querySelectorAll('pre'), function(pre){
    var b=document.createElement('button'); b.className='copy-btn'; b.textContent='Copy';
    b.addEventListener('click', function(){
      var code=pre.querySelector('code'); if(!code) return;
      var r=document.createRange(); r.selectNodeContents(code); var s=window.getSelection(); s.removeAllRanges(); s.addRange(r);
      try{ document.execCommand('copy'); b.textContent='Copied'; setTimeout(function(){b.textContent='Copy';},1200);}catch(e){}
      s.removeAllRanges();
    });
    var wrap=document.createElement('div'); wrap.className='code-wrap'; pre.parentNode.insertBefore(wrap, pre); wrap.appendChild(pre); wrap.appendChild(b);
  });
  if(window.Prism) Prism.highlightAll();
})();