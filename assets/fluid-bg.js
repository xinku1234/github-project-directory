(() => {
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
  if (reduce || coarse || window.innerWidth < 641) return;
  const host = document.querySelector('.home-shell') || document.body;
  document.documentElement.classList.add('fluid-bg-active');
  const canvas = document.createElement('canvas');
  canvas.className = 'fluid-color-canvas';
  canvas.setAttribute('aria-hidden', 'true');
  host.insertBefore(canvas, host.firstChild);
  const ctx = canvas.getContext('2d', { alpha: true });
  let w = 0, h = 0, dpr = 1;
  let mx = innerWidth * 0.5, my = innerHeight * 0.32;
  let lastX = mx, lastY = my;
  let hue = 205;
  let dragging = false;
  const drops = [];
  const maxDrops = 90;

  function resize(){
    dpr = Math.min(window.devicePixelRatio || 1, 1.75);
    w = canvas.width = Math.floor(innerWidth * dpr);
    h = canvas.height = Math.floor(innerHeight * dpr);
    canvas.style.width = innerWidth + 'px';
    canvas.style.height = innerHeight + 'px';
    ctx.setTransform(dpr,0,0,dpr,0,0);
    ctx.clearRect(0,0,innerWidth,innerHeight);
  }
  function pushDrop(x,y,force=1){
    const dx = x - lastX, dy = y - lastY;
    const speed = Math.min(1.8, Math.hypot(dx,dy)/42 + force);
    hue = (hue + 16 + speed * 12) % 360;
    const count = dragging ? 3 : 1;
    for(let i=0;i<count;i++){
      const spread = dragging ? 34 : 16;
      drops.push({
        x: x + (Math.random()-.5)*spread,
        y: y + (Math.random()-.5)*spread,
        vx: dx * .018 + (Math.random()-.5)*.45,
        vy: dy * .018 + (Math.random()-.5)*.45,
        r: (dragging ? 34 : 22) + Math.random()*34 + speed*16,
        life: 1,
        hue: (hue + Math.random()*56 - 28 + (dragging ? 70 : 0)) % 360,
        sat: 78 + Math.random()*18,
        light: 52 + Math.random()*12
      });
    }
    while(drops.length > maxDrops) drops.shift();
    lastX = x; lastY = y;
  }
  function pointer(e){
    mx = e.clientX; my = e.clientY;
    document.documentElement.style.setProperty('--mx', mx + 'px');
    document.documentElement.style.setProperty('--my', my + 'px');
    pushDrop(mx,my, dragging ? 1.2 : .45);
  }
  addEventListener('resize', resize, { passive:true });
  addEventListener('pointerdown', e => { dragging = true; pointer(e); }, { passive:true });
  addEventListener('pointerup', () => { dragging = false; }, { passive:true });
  addEventListener('pointercancel', () => { dragging = false; }, { passive:true });
  addEventListener('pointermove', pointer, { passive:true });

  function seed(){
    for(let i=0;i<9;i++) pushDrop(innerWidth*(.15+Math.random()*.7), innerHeight*(.14+Math.random()*.45), .2);
  }
  function frame(){
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(3,7,17,0.082)';
    ctx.fillRect(0,0,innerWidth,innerHeight);
    ctx.globalCompositeOperation = 'lighter';
    for(const p of drops){
      p.x += p.vx; p.y += p.vy; p.vx *= .986; p.vy *= .986; p.r *= 1.012; p.life *= .973;
      const a = Math.max(0, p.life) * .22;
      const g = ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r);
      g.addColorStop(0, `hsla(${p.hue},${p.sat}%,${p.light+14}%,${a*.95})`);
      g.addColorStop(.28, `hsla(${(p.hue+38)%360},${p.sat}%,${p.light}%,${a*.55})`);
      g.addColorStop(.68, `hsla(${(p.hue+105)%360},${p.sat-8}%,${p.light-8}%,${a*.22})`);
      g.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill();
    }
    for(let i=drops.length-1;i>=0;i--) if(drops[i].life < .045) drops.splice(i,1);
    if(Math.random() < .035) pushDrop(mx + (Math.random()-.5)*260, my + (Math.random()-.5)*160, .12);
    requestAnimationFrame(frame);
  }
  resize(); seed(); frame();
})();
