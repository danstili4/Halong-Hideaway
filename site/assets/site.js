(() => {
  /* ---------- light stops: one per time of day ---------- */
  // One family of colours. Every page runs like a day on the boat: morning sea,
  // turquoise lagoon, sunny afternoon, sunset, party pink, then evening.
  // Everything stays light, ending on a soft dusk, so the light never "jumps".
  // CTA colour is the same coral everywhere: the one thing that always pops.
  const INK = {ink:'#0F2E38', soft:'#3E5A61', acc:'#D9381B', accInk:'#FFFFFF'};
  const STOPS = {
    dawn:    {bg:'#D9ECEA', ...INK, sunA:.55, sunX:78, sunY:18},
    mist:    {bg:'#E2EEEB', ...INK, sunA:.45, sunX:24, sunY:30},
    midday:  {bg:'#A6DAD2', ...INK, sunA:.7,  sunX:74, sunY:14},
    golden:  {bg:'#FBDDA6', ...INK, sunA:.85, sunX:66, sunY:26},
    sunset:  {bg:'#F9C7AB', ...INK, sunA:.9,  sunX:80, sunY:52},
    night:   {bg:'#EFB8C2', ...INK, sunA:.5,  sunX:22, sunY:60},
    dusk:    {bg:'#DCC6E0', ...INK, sunA:.35, sunX:20, sunY:66},
    evening: {bg:'#C9B5DC', ...INK, sunA:.3, sunX:76, sunY:22},
  };
  const VAR = {top:'--sky-top',bot:'--sky-bot',accInk:'--acc-ink'};
  const root = document.documentElement.style;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const hex = h => [1,3,5].map(i => parseInt(h.slice(i,i+2),16)/255);
  const toLin = c => c <= .04045 ? c/12.92 : ((c+.055)/1.055) ** 2.4;
  const toSrgb = c => c <= .0031308 ? c*12.92 : 1.055 * c ** (1/2.4) - .055;
  function oklab(h){
    const [r,g,b] = hex(h).map(toLin);
    const l = Math.cbrt(.4122214708*r+.5363325363*g+.0514459929*b), m = Math.cbrt(.2119034982*r+.6806995451*g+.1073969566*b), s = Math.cbrt(.0883024619*r+.2817188376*g+.6299787005*b);
    return [.2104542553*l+.7936177850*m-.0040720468*s, 1.9779984951*l-2.4285922050*m+.4505937099*s, .0259040371*l+.7827717662*m-.8086757660*s];
  }
  function rgbOf([L,A,B]){
    const l = (L+.3963377774*A+.2158037573*B)**3, m = (L-.1055613458*A-.0638541728*B)**3, s = (L-.0894841775*A-1.2914855480*B)**3;
    return [4.0767416621*l-3.3077115913*m+.2309699292*s, -1.2684380046*l+2.6097574011*m-.3413193965*s, -.0041960863*l-.7034186147*m+1.7076147010*s]
      .map(c => Math.round(Math.max(0,Math.min(1,toSrgb(c)))*255));
  }
  const labCache = {};
  const lab = h => labCache[h] || (labCache[h] = oklab(h));
  const mixArr = (a,b,t) => { const x=lab(a), y=lab(b); return rgbOf(x.map((v,i)=>v+(y[i]-v)*t)); };
  const mix = (a,b,t) => `rgb(${mixArr(a,b,t).join(',')})`;
  const shade = (c,k) => { const x = lab(c); return `rgb(${rgbOf([x[0]*(1-k), x[1]*(1+k*.4), x[2]*(1+k*.4)]).join(',')})`; };
  const lerp = (a,b,t) => a+(b-a)*t;
  const smooth = t => t*t*(3-2*t);
  const clamp = t => Math.max(0,Math.min(1,t));

  const sections = [...document.querySelectorAll('[data-stop],[data-stops]')];
  const topbar = document.querySelector('.top');

  // Each section carries its own text colours, so words always match the
  // light they sit in.
  const stopsOf = s => (s.dataset.stops || s.dataset.stop).split(',').map(k => STOPS[k.trim()]);
  sections.forEach(s => {
    const S = stopsOf(s)[0];
    s.style.setProperty('--ink', S.ink); s.style.setProperty('--soft', S.soft);
    s.style.setProperty('--acc', S.acc); s.style.setProperty('--acc-ink', S.accInk);
    s.style.setProperty('--sky-bot', S.bg);
  });


  /* ---------- gallery reel: vertical scroll drives a horizontal film strip ---------- */
  const reels = [...document.querySelectorAll('.reel-sec')];
  const stackedMQ = matchMedia('(max-width: 900px), (prefers-reduced-motion: reduce)');
  function sizeReels(){
    reels.forEach(sec => {
      const pin = sec.querySelector('.reel-pin'), track = sec.querySelector('.reel-track');
      if (stackedMQ.matches) { sec.style.height = ''; track.style.transform = ''; sec._dist = 0; return; }
      const dist = Math.max(0, track.scrollWidth - pin.clientWidth);
      sec._dist = dist;
      sec.style.height = (dist + innerHeight) + 'px';
    });
  }
  function moveReels(){
    reels.forEach(sec => {
      if (!sec._dist) return;
      const top = sec.getBoundingClientRect().top + scrollY;
      const p = clamp((scrollY - top) / sec._dist);
      sec.querySelector('.reel-track').style.transform = `translate3d(${(-p * sec._dist).toFixed(1)}px,0,0)`;
      const bar = sec.querySelector('.reel-bar i'); if (bar) bar.style.transform = `scaleX(${p})`;
      const label = sec.querySelector('.reel-now');
      if (label) {
        const mid = innerWidth * .55; let cur = '';
        sec.querySelectorAll('[data-time]').forEach(el => { if (el.getBoundingClientRect().left < mid) cur = el.dataset.time; });
        if (label.textContent !== cur) label.textContent = cur;
      }
    });
  }
  const onMQ = (mq, fn) => mq.addEventListener ? mq.addEventListener('change', fn) : (mq.addListener && mq.addListener(fn));
  onMQ(stackedMQ, () => { layout(); paint(); moveReels(); });

  // The sky is one long gradient painted behind the whole page. Neighbouring
  // sections blend across their full height (centre to centre), sampled densely
  // with an eased curve in OKLab, so there is no visible seam anywhere. The only
  // tighter blend is into the dark footer, so text keeps its contrast.
  const strip = document.createElement('div');
  strip.className = 'sky-strip'; strip.setAttribute('aria-hidden','true');
  document.body.prepend(strip);
  let anchors = [];  // [y, stop]
  function layout(){
    anchors = [];
    sizeReels();
    const boxes = sections.map(s => { const r = s.getBoundingClientRect(), L = stopsOf(s); return {y0:r.top+scrollY, y1:r.bottom+scrollY, h:r.height, L, S:L[0], E:L[L.length-1]}; });
    boxes.forEach((b,i) => {
      const prev = boxes[i-1], next = boxes[i+1];
      const fIn  = prev && prev.E.ink !== b.S.ink ? .2 : .5;
      const fOut = next && next.S.ink !== b.E.ink ? .2 : .5;
      if (b.L.length > 1) {
        // a section that travels through several lights (the gallery reel)
        b.L.forEach((S,k) => anchors.push([b.y0 + (b.h * k) / (b.L.length - 1), S]));
        return;
      }
      if (!prev) anchors.push([b.y0, b.S]); else anchors.push([b.y0 + b.h*fIn, b.S]);
      if (!next) anchors.push([b.y1, b.S]); else anchors.push([b.y1 - b.h*fOut, b.S]);
    });
    if (!anchors.length) return;
    const H = anchors[anchors.length-1][0], stops = [];
    for (let y = 0; y <= H + 24; y += 24) stops.push(`${colourAt(y)} ${Math.round(y)}px`);
    strip.style.background = `linear-gradient(to bottom, ${stops.join(', ')})`;
  }
  function at(y){
    if (!anchors.length) return [STOPS.dawn, STOPS.dawn, 0];
    if (y <= anchors[0][0]) return [anchors[0][1], anchors[0][1], 0];
    for (let i = 0; i < anchors.length - 1; i++){
      const [ya,A] = anchors[i], [yb,B] = anchors[i+1];
      if (y <= yb) return [A, B, A === B ? 0 : smooth(clamp((y - ya) / Math.max(1, yb - ya)))];
    }
    const L = anchors[anchors.length-1][1]; return [L, L, 0];
  }
  const colourAt = y => { const [A,B,t] = at(y); return mix(A.bg, B.bg, t); };

  function paint(){
    if (!sections.length) return;
    // the islands, water and haze are tinted from the sky right behind them,
    // so they always belong to the scene instead of sitting on top of it
    const [A,B,t] = at(scrollY + innerHeight*.88), base = mix(A.bg, B.bg, t);
    const inkAt = t < .5 ? A.ink : B.ink, dark = inkAt !== INK.ink;
    root.setProperty('--haze', base);
      const baseHex = '#' + mixArr(A.bg,B.bg,t).map(v => v.toString(16).padStart(2,'0')).join('');
    root.setProperty('--r1', shade(baseHex, dark ? .06 : .07));
    root.setProperty('--r2', shade(baseHex, dark ? .12 : .13));
    root.setProperty('--r3', shade(baseHex, dark ? .2 : .2));
    root.setProperty('--water', mix(baseHex, '#3FA7A0', dark ? .15 : .28));
    const [C,D,u] = at(scrollY + innerHeight*.3);
    root.setProperty('--sun-x', lerp(C.sunX,D.sunX,u)+'%');
    root.setProperty('--sun-y', lerp(C.sunY,D.sunY,u)+'vh');
    root.setProperty('--sun-a', lerp(C.sunA,D.sunA,u));
    root.setProperty('--stars', (C.ink !== INK.ink ? 1-u : 0) + (D.ink !== INK.ink ? u : 0));
    // the nav takes the colours of whatever is under it
    if (topbar){
      const y = scrollY + 40, [N,M,v] = at(y), S = v < .5 ? N : M;
      topbar.style.setProperty('--nav-bg', colourAt(y));
      for (const [k,c] of [['--ink',S.ink],['--soft',S.soft],['--acc',S.acc],['--acc-ink',S.accInk]]) topbar.style.setProperty(k,c);
      topbar.style.color = S.ink;
    }
    if (!reduce) {
      const prog = scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight);
      root.setProperty('--ridge-shift', (-prog * innerWidth * .12).toFixed(1)+'px');
    }
  }
  const measure = () => { layout(); };
  let queued = false;
  addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; paint(); moveReels(); }); } }, {passive:true});
  addEventListener('resize', () => { layout(); paint(); });
  addEventListener('load', () => { layout(); paint(); });
  if ('ResizeObserver' in window) new ResizeObserver(() => { layout(); paint(); }).observe(document.body);

  /* ---------- karst silhouettes ---------- */
  function rng(seed){ return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function karst(seed, count, minH, maxH){
    const r = rng(seed), H = 300, towers = [];
    for (let n = 0; n < count; n++) towers.push({c: -80 + r()*1760, w: 25 + r()*85, h: minH + r()*(maxH-minH), p: 2.2 + r()*2.5, tilt: (r()-.5)*.5});
    const pts = [];
    let rough = 0;
    for (let x = -60; x <= 1660; x += 5){
      let y = 8 + r()*3;
      for (const t of towers){
        const dx = (x - t.c) / t.w + t.tilt * ((x - t.c) / t.w) ** 2 * .3;
        if (Math.abs(dx) < 1) y = Math.max(y, t.h * Math.pow(1 - Math.pow(Math.abs(dx), t.p), .45));
      }
      rough = rough * .6 + (r()-.5) * 6;
      pts.push(`${x} ${(H - Math.max(0, y + (y > 12 ? rough : 0))).toFixed(1)}`);
    }
    return `M-60 ${H} L${pts.join(' L')} L1660 ${H} Z`;
  }
  const world = document.querySelector('.world');
  if (world) {
    world.insertAdjacentHTML('beforeend', `
      <div class="stars"></div><div class="sun"></div>
      <div class="ridges">
        <svg class="l1" viewBox="0 0 1600 300" preserveAspectRatio="none"><path d="${karst(11,26,90,290)}"/></svg>
        <svg class="l2" viewBox="0 0 1600 300" preserveAspectRatio="none"><path d="${karst(29,18,70,280)}"/></svg>
        <svg class="l3" viewBox="0 0 1600 300" preserveAspectRatio="none"><path d="${karst(47,11,60,270)}"/></svg>
      </div><div class="haze"></div><div class="water"></div>`);
    const stars = world.querySelector('.stars'), sr = rng(7);
    for (let n = 0; n < 70; n++){
      const s = document.createElement('i');
      s.style.left = (sr()*100)+'%'; s.style.top = (sr()*100)+'%'; s.style.opacity = (.3 + sr()*.7).toFixed(2);
      if (sr() > .9) s.style.width = s.style.height = '2px';
      stars.appendChild(s);
    }
  }

  /* ---------- hamburger menu ---------- */
  const toggle = document.querySelector('.menu-toggle');
  if (toggle) {
    const setMenu = open => {
      topbar.classList.toggle('open', open);
      document.documentElement.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    toggle.addEventListener('click', e => { e.stopPropagation(); setMenu(!topbar.classList.contains('open')); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && topbar.classList.contains('open')) { setMenu(false); toggle.focus(); } });
    document.addEventListener('click', e => { if (topbar.classList.contains('open') && !topbar.contains(e.target)) setMenu(false); });
    topbar.querySelectorAll('nav a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    onMQ(matchMedia('(min-width: 1081px)'), e => { if (e.matches) setMenu(false); });
  }


  /* ---------- looping clips: download only when near the screen, play only while visible ---------- */
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  document.querySelectorAll('video.loop').forEach(v => {
    v.muted = true; // required for autoplay on phones
    if (reduce) { v.removeAttribute('autoplay'); v.preload = 'none'; return; }
    const play = () => {
      if (v.dataset.src && !v.src) { v.src = v.dataset.src; v.load(); }
      const p = v.play(); if (p) p.catch(() => {});
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => e.isIntersecting ? play() : (v.muted && v.pause()),
        {rootMargin: saveData ? '0px' : '300px 0px'}).observe(v);
    } else play();
  });

  /* ---------- muted YouTube preview inside the photo frame ---------- */
  // Plays the company's video silently on loop, cropped to fill the frame.
  // YouTube only allows this on a real web address (http/https), so a page
  // opened straight from the computer keeps the photo instead.
  const FILM_ID = 'XsAsDFy_2qI'; // swap for your own recap video's YouTube ID
  const watchUrl = `https://www.youtube.com/watch?v=${FILM_ID}`;
  document.querySelectorAll('[data-watch]').forEach(a => a.href = watchUrl);
  const canEmbed = location.protocol === 'http:' || location.protocol === 'https:';
  document.querySelectorAll('.has-preview').forEach(fig => {
    const box = fig.querySelector('.yt-preview');
    if (!box || !canEmbed || reduce || saveData || matchMedia('(max-width: 1024px), (pointer: coarse)').matches) return;
    const ifr = document.createElement('iframe');
    ifr.title = 'Halong Hideaway trip preview';
    ifr.tabIndex = -1;
    ifr.allow = 'autoplay; encrypted-media';
    ifr.referrerPolicy = 'strict-origin-when-cross-origin';
    ifr.src = `https://www.youtube-nocookie.com/embed/${FILM_ID}?autoplay=1&mute=1&loop=1&playlist=${FILM_ID}&controls=0&disablekb=1&fs=0&iv_load_policy=3&modestbranding=1&playsinline=1&rel=0`;
    // cover-crop a 16:9 video into whatever shape the frame is
    const fit = () => {
      const w = fig.clientWidth, h = fig.clientHeight, k = 1.12; // slight overscan hides YouTube's edges
      const vw = Math.max(w, h * 16/9) * k, vh = vw * 9/16;
      ifr.style.width = vw + 'px'; ifr.style.height = vh + 'px';
    };
    ifr.addEventListener('load', () => setTimeout(() => fig.classList.add('playing'), 900));
    box.appendChild(ifr); fit();
    addEventListener('resize', fit);
  });


  /* ---------- hero promo: a light silent preview; the full film loads only on tap ---------- */
  const promo = document.getElementById('promo'), soundBtn = document.querySelector('.play.sound');
  if (promo && soundBtn) {
    const label = soundBtn.querySelector('span');
    const previewSrc = promo.getAttribute('src'), fullSrc = promo.dataset.full;
    const toPreview = () => {
      promo.muted = true; promo.loop = true;
      if (!promo.src.endsWith(previewSrc)) { promo.src = previewSrc; }
      const p = promo.play(); if (p) p.catch(() => {});
      label.textContent = 'Watch with sound'; soundBtn.setAttribute('aria-pressed','false');
    };
    soundBtn.addEventListener('click', () => {
      if (!promo.muted) return toPreview();
      label.textContent = 'Loading…';
      promo.src = fullSrc; promo.loop = false; promo.muted = false;
      const p = promo.play(); if (p) p.catch(() => {});
      promo.addEventListener('playing', () => { label.textContent = 'Mute'; }, {once: true});
      soundBtn.setAttribute('aria-pressed','true');
    });
    promo.addEventListener('ended', () => { if (!promo.loop) toPreview(); });
  }

  /* ---------- scroll reveals (one IntersectionObserver for the whole page) ---------- */
  // Text fades up; photos and videos only slide (never hidden), so nothing can stay invisible.
  const revealAll = () => document.querySelectorAll('.rv, .rv-img').forEach(t => t.classList.add('in'));
  addEventListener('error', revealAll);
  if (!reduce && document.documentElement.classList.contains('js')) try {
    const TEXT = 'main section:not(.hero):not(.intro):not(.tour-head):not(.gal-head) :is(.line,.title,.says,.lede,.body,.facts,.note,.hook,.ticks,.price,.badge,.choose li,.moments li,.qa > div,.spec li,.others a,.interlude,.cols > div,.days li,.chapter h2,.tour-row .big,.tour-row h2,.tour-row .buy,.actions), footer .ask, footer > div';
    const IMGS = '.beat .shot, .split .shot, .chapter .shot, .sleep-pics .shot';
    document.querySelectorAll(TEXT).forEach(el => { if (!el.closest('.reel-track')) el.classList.add('rv'); });
    document.querySelectorAll(IMGS).forEach(el => el.classList.add('rv-img'));
    document.querySelectorAll('.moments, .choose, .qa, .spec, .others, .days, .cols').forEach(list => {
      [...list.children].forEach((c, i) => c.style.setProperty('--d', Math.min(i * 0.07, .42) + 's'));
    });
    const targets = document.querySelectorAll('.rv, .rv-img');
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), {rootMargin: '0px 0px -8% 0px', threshold: .01});
    targets.forEach(t => io.observe(t));
  } catch (err) { revealAll(); }

  /* ---------- the itinerary line draws with scroll ---------- */
  const routes = [...document.querySelectorAll('.route')];
  const drawRoutes = () => routes.forEach(r => {
    const b = r.getBoundingClientRect();
    const p = reduce ? 1 : clamp((innerHeight * .65 - b.top) / Math.max(1, b.height));
    r.style.setProperty('--route-p', p.toFixed(3));
  });
  if (routes.length) { addEventListener('scroll', () => requestAnimationFrame(drawRoutes), {passive:true}); addEventListener('resize', drawRoutes); drawRoutes(); }

  /* ---------- tours dropdown ---------- */
  document.querySelectorAll('.dd').forEach(dd => {
    const btn = dd.querySelector('button'), panel = dd.querySelector('.dd-panel');
    const set = open => { btn.setAttribute('aria-expanded', String(open)); panel.hidden = !open; };
    btn.addEventListener('click', e => { e.stopPropagation(); set(panel.hidden); });
    dd.addEventListener('keydown', e => { if (e.key === 'Escape') { set(false); btn.focus(); } });
    document.addEventListener('click', e => { if (!dd.contains(e.target)) set(false); });
    dd.addEventListener('focusout', e => { if (!dd.contains(e.relatedTarget)) set(false); });
  });

  /* ---------- sticky book button on tour pages ---------- */
  const bookbar = document.querySelector('.bookbar');
  if (bookbar) {
    const head = document.querySelector('.tour-head');
    const foot = document.querySelector('footer');
    const check = () => {
      const past = head.getBoundingClientRect().bottom < 0;
      const atEnd = foot.getBoundingClientRect().top < innerHeight * .6;
      bookbar.classList.toggle('show', past && !atEnd);
    };
    addEventListener('scroll', check, {passive:true}); check();
  }

  /* ---------- gallery viewer: swipe, arrows, keyboard, swipe down to close ---------- */
  const viewer = document.getElementById('viewer');
  if (viewer) {
    const vi = viewer.querySelector('img'), vc = viewer.querySelector('.v-cap'), vn = viewer.querySelector('.v-count');
    let items = [], idx = 0;
    const collect = () => items = [...document.querySelectorAll('.zoom')].filter(b => !b.classList.contains('missing'));
    const preload = i => { const it = items[(i + items.length) % items.length]; if (it) new Image().src = it.querySelector('img').src; };
    const show = i => {
      idx = (i + items.length) % items.length;
      const b = items[idx], img = b.querySelector('img');
      vi.src = img.currentSrc || img.src; vi.alt = img.alt;
      vc.textContent = b.closest('figure').querySelector('figcaption')?.textContent || '';
      vn.textContent = `${idx + 1} / ${items.length}`;
      preload(idx + 1); preload(idx - 1);
    };
    document.querySelectorAll('.zoom').forEach(b => b.addEventListener('click', () => {
      collect(); const i = items.indexOf(b); if (i < 0) return;
      show(i); viewer.showModal(); document.documentElement.classList.add('menu-open');
    }));
    viewer.addEventListener('close', () => document.documentElement.classList.remove('menu-open'));
    viewer.querySelector('.close').addEventListener('click', () => viewer.close());
    viewer.querySelector('.v-prev').addEventListener('click', () => show(idx - 1));
    viewer.querySelector('.v-next').addEventListener('click', () => show(idx + 1));
    viewer.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
      if (e.key === 'ArrowLeft')  { e.preventDefault(); show(idx - 1); }
    });
    // swipe left/right to move, drag down to close; the photo follows the finger
    let sx = 0, sy = 0, dragging = false;
    const stage = viewer.querySelector('.v-stage');
    stage.addEventListener('pointerdown', e => { if (e.pointerType === 'mouse') return; dragging = true; sx = e.clientX; sy = e.clientY; vi.style.transition = 'none'; });
    stage.addEventListener('pointermove', e => {
      if (!dragging) return;
      const dx = e.clientX - sx, dy = e.clientY - sy;
      vi.style.transform = Math.abs(dx) > Math.abs(dy) ? `translateX(${dx}px)` : `translateY(${Math.max(0,dy)}px) scale(${1 - Math.max(0,dy)/1600})`;
    });
    const end = e => {
      if (!dragging) return; dragging = false;
      const dx = e.clientX - sx, dy = e.clientY - sy;
      vi.style.transition = 'transform .25s ease'; vi.style.transform = '';
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(idx + (dx < 0 ? 1 : -1));
      else if (dy > 90) viewer.close();
    };
    stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
    viewer.addEventListener('click', e => { if (e.target === viewer || e.target === stage) viewer.close(); });
  }

  /* ---------- trip picker (prices) ---------- */
  const pick = document.querySelector('.pick');
  if (pick) {
    const fmt = n => n.toLocaleString('en-US') + '₫';
    const TRIPS = {
      2: {name:'Halong Hideaway, 2 days 1 night', price:3150000,
          blurb:'One night on the boat. You get the beach stop, the sunset party and the BBQ, then kayaking and a cooking demo before heading back.',
          book:'https://halonghideaway.com/booking-tour/1751',
          days:[['Day 1','Hanoi to Lan Ha Bay. Lunch on board, beach stop with boat jumping, banana tubing and volleyball, jacuzzis, sunset party, BBQ, party.'],
                ['Day 2','Guided kayaking, cooking demo, lunch on board, back at the hostel around 4:30pm.']],
          incl:['Bus and boat transfers from Hanoi','Your cabin on the Hideaway','Every meal on the itinerary','Tour guide','Kayaking, banana tubing and swimming','Entrance fees'],
          excl:'Not included: drinks, travel insurance and personal spending.'},
      3: {name:'Halong Hideaway, 3 days 2 nights', price:4900000,
          blurb:'The full trip. Two sunset parties, the Cat Ba cycle and jungle trek, a fish massage lunch, and kayaking on the last morning.',
          book:'https://halonghideaway.com/booking-tour/1741',
          days:[['Day 1','Hanoi to Lan Ha Bay. Beach stop, boat jumping, banana tubing, jacuzzis, sunset party, BBQ, party.'],
                ['Day 2','Cat Ba National Park: cycle through Viet Hai village, jungle trek, lunch with fish massage. Jacuzzi, sunset, BBQ, party.'],
                ['Day 3','Guided kayaking, lunch on board, back at the hostel around 4:30pm.']],
          incl:['Bus and boat transfers from Hanoi','Two nights in your cabin on the Hideaway','Every meal on the itinerary','Tour guide','Cycling, trekking, kayaking, tubing, swimming and beach volleyball','Entrance fees'],
          excl:'Not included: drinks, travel insurance and personal spending.'},
      6: {name:'Halong Bay and the Ha Giang Loop, 6 days 6 nights', price:{self:8800000, driver:9800000},
          blurb:'The full 3-day cruise, then a night bus north and three days on a motorbike around the Ha Giang loop, staying with local families.',
          book:'https://halonghideaway.com/booking-tour/1752',
          days:[['Day 1–3','The full Hideaway cruise. Back in Hanoi at 4:30pm, sleeper bus to Ha Giang at 7:30pm, free bed when you arrive.'],
                ['Day 4','Ha Giang to Du Gia, about 120km over Quan Ba pass and through Dong Van Geopark. Homestay with an ethnic minority family.'],
                ['Day 5','Du Gia to Dong Van through Meo Vac, a boat on the Nho Que river and Ma Pi Leng pass. Hot pot dinner if you want it.'],
                ['Day 6','Sa Phin palace and Yen Minh, back to Ha Giang City. Bus to Hanoi at 5pm, free hostel bed when you get in.']],
          incl:['The full 3-day Hideaway cruise','Sleeper buses to and from Ha Giang','Homestays on the loop','Every meal on the tour','Motorbike and fuel','Guide and entrance fees'],
          excl:'Not included: drinks, tips, travel insurance and personal spending.'},
    };
    const fromHash = { '#2':2, '#3':3, '#6':6 };
    let len = fromHash[location.hash] || 3, ride = 'self';
    const $ = id => document.getElementById(id);
    const render = () => {
      const t = TRIPS[len];
      $('t-name').textContent = t.name;
      $('t-blurb').textContent = t.blurb;
      $('t-book').href = t.book;
      $('t-price').textContent = fmt(typeof t.price === 'number' ? t.price : t.price[ride]);
      $('t-unit').textContent = len === 6 ? (ride === 'self' ? 'per person, riding yourself' : 'per person, with a driver') : 'per person';
      $('t-ride').hidden = len !== 6;
      const shot = $('t-shot'); if (shot) shot.hidden = len !== 6;
      $('t-days').innerHTML = t.days.map(([d,x]) => `<li><span>${d}</span><p style="margin:0">${x}</p></li>`).join('');
      $('t-incl').innerHTML = t.incl.map(i => `<li>${i}</li>`).join('');
      $('t-excl').textContent = t.excl;
      document.querySelectorAll('[data-len]').forEach(b => b.setAttribute('aria-checked', String(+b.dataset.len === len)));
      document.querySelectorAll('[data-ride]').forEach(b => b.setAttribute('aria-checked', String(b.dataset.ride === ride)));
    };
    document.querySelectorAll('[data-len]').forEach(b => b.addEventListener('click', () => {
      len = +b.dataset.len; history.replaceState(null,'','#'+len); render(); measure(); paint();
    }));
    document.querySelectorAll('[data-ride]').forEach(b => b.addEventListener('click', () => { ride = b.dataset.ride; render(); }));
    document.querySelectorAll('[role=radiogroup]').forEach(g => g.addEventListener('keydown', e => {
      if (!['ArrowLeft','ArrowRight'].includes(e.key)) return;
      const opts = [...g.querySelectorAll('[role=radio]')], i = opts.indexOf(document.activeElement);
      if (i < 0) return; e.preventDefault();
      const next = opts[(i + (e.key === 'ArrowRight' ? 1 : opts.length-1)) % opts.length]; next.focus(); next.click();
    }));
    render();
  }

  layout(); paint(); moveReels();
})();
