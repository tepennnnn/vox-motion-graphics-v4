/* MOTION GRAPHICS V3 — device runtime. Every device is a set of GSAP tweens on ONE paused timeline, at absolute
   seconds, so any frame renders on its own. Word times come from window.V3_WORDS (forced-aligned narration). */
window.V3 = (function () {
  const K = {};
  let tl, W = [];
  K.init = (timeline, words) => { tl = timeline; W = words || []; return K; };
  K.t = (i, d = 0) => W[i].start + d;            // word onset
  K.e = (i, d = 0) => W[i].end + d;              // word end
  const q = (s) => (typeof s === 'string' ? document.querySelectorAll(s) : s);

  // A word or element arriving: blur -> sharp, 0.16 s (REF-C/REF-A captions; motion.md "per word blur 6-10px")
  K.in = (sel, t, o = {}) => tl.fromTo(q(sel),
    { opacity: 0, filter: `blur(${o.blur ?? 10}px)`, x: o.x || 0, y: o.y || 0, scale: o.scale ?? 1, rotation: o.rot || 0 },
    { opacity: o.op ?? 1, filter: 'blur(0px)', x: 0, y: 0, scale: 1, rotation: 0, duration: o.dur ?? 0.16, ease: o.ease || 'power2.out', stagger: o.stagger || 0 }, t);
  K.out = (sel, t, o = {}) => {
    const a = { opacity: o.from ?? 1, filter: 'blur(0px)' }, b = { opacity: 0, filter: `blur(${o.blur ?? 8}px)`, duration: o.dur ?? 0.14, ease: o.ease || 'power2.in', stagger: o.stagger || 0, immediateRender: false };
    if (o.x !== undefined) { a.x = 0; b.x = o.x; } if (o.y !== undefined) { a.y = 0; b.y = o.y; } if (o.scale !== undefined) { a.scale = 1; b.scale = o.scale; }
    return tl.fromTo(q(sel), a, b, t);
  };
  // every [data-w] inside a scene lands on its spoken word (data-d shifts, data-mode picks the entrance)
  K.words = (root) => {
    Array.from(document.querySelectorAll(root)).flatMap((r) => Array.from(r.querySelectorAll('[data-w]'))).forEach((el) => {
      const i = +el.dataset.w, d = +(el.dataset.d || 0) - 0.04, m = el.dataset.mode || 'blur';
      const t = W[i].start + d;
      if (m === 'blur') K.in(el, t, { blur: 10 });
      else if (m === 'rise') K.in(el, t, { blur: 6, y: 40, dur: 0.22, ease: 'expo.out' });
      else if (m === 'slideR') K.in(el, t, { blur: 14, x: 260, dur: 0.32, ease: 'expo.out' });
      else if (m === 'slideL') K.in(el, t, { blur: 14, x: -260, dur: 0.32, ease: 'expo.out' });
      else if (m === 'pop') K.in(el, t, { blur: 4, scale: 1.35, dur: 0.2, ease: 'back.out(2)' });
      else if (m === 'grey') tl.fromTo(el, { opacity: 0.0, color: '#B9B7B1' }, { opacity: 1, color: el.dataset.to || '#1C1B1E', duration: 0.12, ease: 'none' }, t);
      else if (m === 'type') K.type(el, t, +(el.dataset.cps || 22));
      else if (m === 'letters') K.letters(el, t);
      else if (m === 'scramble') K.scramble(el, t);
      else if (m === 'cut') tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t);
    });
  };
  // typewriter with a cursor (REF-B "but he said")
  K.type = (el, t, cps = 22) => {
    const ch = el.querySelectorAll('.c');
    ch.forEach((c, k) => tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t + k / cps));
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t);
  };
  // letters bounce in one by one (REF-B "he failed")
  K.letters = (el, t) => {
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t);
    tl.fromTo(el.querySelectorAll('.c'), { opacity: 0, y: 40, filter: 'blur(4px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.24, ease: 'back.out(2.2)', stagger: 0.035 }, t);
  };
  // letters assemble in a shuffled order (REF-C "Categories")
  K.scramble = (el, t) => {
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t);
    const cs = [...el.querySelectorAll('.c')];
    cs.forEach((c, k) => { const o = ((k * 7) % cs.length) / cs.length; tl.fromTo(c, { opacity: 0, filter: 'blur(6px)' }, { opacity: 1, filter: 'blur(0px)', duration: 0.12 }, t + o * 0.45); });
  };
  // camera: push / drift on a wrapper (never on the timed clip)
  K.cam = (sel, t0, t1, from, to, ease = 'none', first = true) => tl.fromTo(q(sel), from, { ...to, duration: t1 - t0, ease, immediateRender: first }, t0);
  // odometer: each .col is a strip of glyphs; roll to its last glyph with motion blur (REF-C 1920 -> 1970)
  K.odo = (sel, t, dur = 0.7, o = {}) => {
    q(sel).forEach((od) => {
      const cols = [...od.querySelectorAll('.col')];
      cols.forEach((c, k) => {
        const n = c.children.length; if (n < 2) return;
        const h = +od.dataset.h || parseFloat(getComputedStyle(od).fontSize);
        const dd = dur * (o.stagger === false ? 1 : (0.55 + 0.45 * (k + 1) / cols.length));
        tl.fromTo(c, { y: 0 }, { y: -h * (n - 1), duration: dd, ease: o.ease || 'power3.inOut' }, t);
        tl.fromTo(c, { filter: 'blur(0px)' }, { filter: 'blur(5px)', duration: dd * 0.35, ease: 'power1.in', yoyo: true, repeat: 1 }, t + dd * 0.15);
      });
    });
  };
  // highlighter sweep, left -> right (REF-C)
  K.hl = (sel, t, dur = 0.35) => tl.fromTo(q(sel), { scaleX: 0, opacity: 1 }, { scaleX: 1, duration: dur, ease: 'power2.inOut', stagger: 0.12 }, t);
  // pen stroke drawing on (REF-B arrows/circles; REF-C Venn circles). paths need pathLength="1"
  K.draw = (sel, t, dur = 0.45, ease = 'power2.inOut') => tl.fromTo(q(sel), { strokeDasharray: 1, strokeDashoffset: 1, opacity: 1 }, { strokeDashoffset: 0, duration: dur, ease }, t);
  // bar -> card mask reveal (REF-A): a thin bar grows to the card
  K.barCard = (sel, t, o = {}) => (K.show(sel, t), tl.fromTo(q(sel), { clipPath: `inset(48% ${o.side ?? 0}% 48% ${o.side ?? 0}%)` }, { clipPath: 'inset(0% 0% 0% 0%)', duration: o.dur ?? 0.45, ease: 'expo.inOut' }, t));
  // sliver -> card (REF-B): opens from a thin vertical sliver
  K.sliver = (sel, t, dur = 0.4) => (K.show(sel, t), tl.fromTo(q(sel), { clipPath: 'inset(0% 47% 0% 47%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: dur, ease: 'expo.inOut' }, t));
  // a cutout rising out of a card's bottom edge (REF-B) / dropping in from the top (REF-A)
  K.show = (sel, t) => { gsap.set(q(sel), { opacity: 0 }); tl.set(q(sel), { opacity: 0 }, 0); tl.set(q(sel), { opacity: 1 }, t); };
  K.rise = (sel, t, dist = 520, dur = 0.55) => { K.show(sel, t); return tl.fromTo(q(sel), { y: dist }, { y: 0, duration: dur, ease: 'expo.out' }, t); };
  K.drop = (sel, t, dist = -900, dur = 0.5) => { K.show(sel, t); return tl.fromTo(q(sel), { y: dist }, { y: 0, duration: dur, ease: 'back.out(1.15)' }, t); };
  K.slide = (sel, t, dx = 700, dur = 0.5, ease = 'expo.out') => { K.show(sel, t); return tl.fromTo(q(sel), { x: dx }, { x: 0, duration: dur, ease }, t); };
  // RGB split arrival for a hero word (REF-A "NOBODY")
  K.rgb = (sel, t, dx = 300, dur = 0.4) => tl.fromTo(q(sel),
    { x: dx, opacity: 0, textShadow: '-26px 0 rgba(255,40,70,.85), 26px 0 rgba(0,210,255,.85)' },
    { x: 0, opacity: 1, textShadow: '0px 0 rgba(255,40,70,0), 0px 0 rgba(0,210,255,0)', duration: dur, ease: 'expo.out' }, t);
  // slice glitch: clones (class .slice) jump sideways for 2 frames (REF-A f17-18)
  K.slices = (sel, t, frames = 2) => {
    q(sel).forEach((s, k) => {
      const dx = (k % 2 ? -1 : 1) * (40 + 30 * k);
      tl.set(s, { opacity: 1, x: dx }, t); tl.set(s, { opacity: 0, x: 0 }, t + frames / 30);
    });
  };
  // full-frame white flash with an anamorphic streak (REF-A open, f1-5)
  K.flash = (flashSel, streakSel, t) => {
    tl.fromTo(streakSel, { opacity: 0, scaleX: 0.1, scaleY: 1 }, { opacity: 1, scaleX: 1.2, scaleY: 3, duration: 0.07, ease: 'power2.out' }, t);
    tl.to(streakSel, { opacity: 0, scaleY: 1, duration: 0.1 }, t + 0.1);
    tl.fromTo(flashSel, { opacity: 0 }, { opacity: 1, duration: 0.033 }, t + 0.033);
    tl.to(flashSel, { opacity: 0, duration: 0.16, ease: 'power2.out' }, t + 0.07);
  };
  K.bloom = (flashSel, t, up = 0.25, down = 0.3) => {        // highlights blow out to white (REF-A f517-525)
    tl.fromTo(flashSel, { opacity: 0 }, { opacity: 1, duration: up, ease: 'power2.in' }, t);
    tl.to(flashSel, { opacity: 0, duration: down, ease: 'power2.out' }, t + up);
  };
  // zoom-blur exit / entry (REF-A f45-46, REF-B f26-27)
  K.zoomOut = (sel, t, dur = 0.2, s0 = 1) => tl.fromTo(q(sel), { scale: s0, filter: 'blur(0px)', opacity: 1 }, { scale: s0 * 1.45, filter: 'blur(16px)', opacity: 0.0, duration: dur, ease: 'power3.in', immediateRender: false }, t);
  K.zoomIn = (sel, t, dur = 0.28) => tl.fromTo(q(sel), { scale: 1.25, filter: 'blur(16px)' }, { scale: 1, filter: 'blur(0px)', duration: dur, ease: 'expo.out' }, t);
  K.blurIn = (sel, t, dur = 0.3, b = 18) => tl.fromTo(q(sel), { filter: `blur(${b}px)`, opacity: 0 }, { filter: 'blur(0px)', opacity: 1, duration: dur, ease: 'power2.out' }, t);
  K.blurOut = (sel, t, dur = 0.25, b = 18) => tl.fromTo(q(sel), { filter: 'blur(0px)', opacity: 1 }, { filter: `blur(${b}px)`, opacity: 0, duration: dur, ease: 'power2.in', immediateRender: false }, t);
  // whip: horizontal smear out / in (motion.md "Whip")
  K.whipOut = (sel, t, dx = -900, dur = 0.16) => tl.fromTo(q(sel), { x: 0, filter: 'blur(0px)' }, { x: dx, filter: 'blur(22px)', duration: dur, ease: 'power3.in', immediateRender: false }, t);
  K.whipIn = (sel, t, dx = 900, dur = 0.24) => tl.fromTo(q(sel), { x: dx, filter: 'blur(22px)' }, { x: 0, filter: 'blur(0px)', duration: dur, ease: 'expo.out' }, t);
  // circle iris portal (REF-A f358-370): a dot grows past the frame
  K.iris = (sel, t, dur = 0.5, cx = '50%', cy = '50%') => tl.fromTo(q(sel), { clipPath: `circle(0% at ${cx} ${cy})` }, { clipPath: `circle(150% at ${cx} ${cy})`, duration: dur, ease: 'power3.in' }, t);
  // light-leak burn (REF-C f201-215, f331-337)
  K.leak = (sel, t, dur = 0.45) => {
    tl.fromTo(q(sel), { opacity: 0, x: -300, scale: 1 }, { opacity: 1, x: 0, scale: 1.15, duration: dur * 0.45, ease: 'power2.in' }, t);
    tl.to(q(sel), { opacity: 0, x: 260, duration: dur * 0.55, ease: 'power2.out' }, t + dur * 0.45);
  };
  // cinematic letterbox (REF-A f159-171)
  K.letterbox = (top, bot, t, h = 230, dur = 0.35) => {
    tl.fromTo(top, { height: 0 }, { height: h, duration: dur, ease: 'expo.out' }, t);
    tl.fromTo(bot, { height: 0 }, { height: h, duration: dur, ease: 'expo.out' }, t);
  };
  // echo rings pulsing off a shape on a stressed word (REF-C f571-620)
  K.pulse = (sel, t) => { tl.set(q(sel), { opacity: 0 }, 0); return tl.fromTo(q(sel), { scale: 1, opacity: 0.8 }, { scale: 1.32, opacity: 0, duration: 0.7, ease: 'power2.out', immediateRender: false }, t); };
  // specular sheen across a disc/logo (REF-C Al Ries circle)
  K.sheen = (sel, t, dur = 0.9) => tl.fromTo(q(sel), { xPercent: -160 }, { xPercent: 160, duration: dur, ease: 'power2.inOut' }, t);

  // ---------------- V3.1 additions (REF-D) ----------------
  // an object flies in (spinning, blurred) and parks; then keeps turning slowly until `until` (REF-D cheese/money)
  K.fly = (sel, t, o = {}) => {
    K.show(sel, t);
    tl.fromTo(q(sel), { x: o.x ?? 0, y: o.y ?? 900, rotation: o.rot ?? 220, scale: o.s0 ?? 0.5, filter: 'blur(14px)' },
      { x: 0, y: 0, rotation: o.r1 ?? 0, scale: 1, filter: 'blur(0px)', duration: o.dur ?? 0.55, ease: o.ease || 'expo.out', stagger: o.stagger || 0 }, t);
    if (o.until) tl.fromTo(q(sel), { rotation: o.r1 ?? 0 }, { rotation: (o.r1 ?? 0) + (o.spin ?? 25) * (o.until - t - (o.dur ?? 0.55)), duration: o.until - t - (o.dur ?? 0.55), ease: 'none', immediateRender: false }, t + (o.dur ?? 0.55));
  };
  // ribbon: a thick round-capped stroke whose visible segment slides along its path (head in, hold, tail out) with its
  // word riding the middle of the segment. path has pathLength="1000"; seg = visible length in those units (REF-D 12.6-15.2 s)
  K.ribbon = (pathSel, tpSel, t, o = {}) => {
    const seg = o.seg ?? 620, tin = o.tin ?? 0.42, hold = o.hold ?? 1.0, tout = o.tout ?? 0.38;
    const p = q(pathSel), tp = q(tpSel);
    tl.set(p, { strokeDasharray: `${seg} 3000`, strokeDashoffset: seg, opacity: 1 }, 0);
    tl.set(tp, { attr: { startOffset: `${(-seg / 2) / 10}%` } }, 0);
    tl.fromTo(p, { strokeDashoffset: seg }, { strokeDashoffset: -(o.park ?? 180), duration: tin, ease: 'power3.out', immediateRender: false }, t);
    tl.fromTo(tp, { attr: { startOffset: `${(-seg / 2) / 10}%` } }, { attr: { startOffset: `${(seg / 2 + (o.park ?? 180)) / 10}%` }, duration: tin, ease: 'power3.out', immediateRender: false }, t);
    tl.fromTo(p, { strokeDashoffset: -(o.park ?? 180) }, { strokeDashoffset: -(o.park ?? 180) - (o.drift ?? 60), duration: hold, ease: 'none', immediateRender: false }, t + tin);
    tl.fromTo(tp, { attr: { startOffset: `${(seg / 2 + (o.park ?? 180)) / 10}%` } }, { attr: { startOffset: `${(seg / 2 + (o.park ?? 180) + (o.drift ?? 60)) / 10}%` }, duration: hold, ease: 'none', immediateRender: false }, t + tin);
    tl.fromTo(p, { strokeDashoffset: -(o.park ?? 180) - (o.drift ?? 60) }, { strokeDashoffset: -1100, duration: tout, ease: 'power3.in', immediateRender: false }, t + tin + hold);
    tl.fromTo(tp, { attr: { startOffset: `${(seg / 2 + (o.park ?? 180) + (o.drift ?? 60)) / 10}%` } }, { attr: { startOffset: `${(1100 + seg / 2) / 10}%` }, duration: tout, ease: 'power3.in', immediateRender: false }, t + tin + hold);
  };
  // walking: a vertical bob at step rate while the figure recedes (scale down, up the frame)
  K.walk = (sel, t0, t1, o = {}) => {
    const steps = Math.max(2, Math.round((t1 - t0) * (o.rate ?? 3.2)));
    tl.fromTo(q(sel), { y: 0 }, { y: -(o.bob ?? 14), duration: (t1 - t0) / steps / 2, ease: 'sine.inOut', yoyo: true, repeat: steps * 2 - 1, immediateRender: false }, t0);
  };
  // snap zoom: fast punch into a point of a wrapper (REF-D laptop 23.0 s), motion blur peaking mid-move
  K.snap = (sel, t, s0, s1, o = {}) => {
    tl.fromTo(q(sel), { scale: s0, x: o.x0 ?? 0, y: o.y0 ?? 0 }, { scale: s1, x: o.x1 ?? 0, y: o.y1 ?? 0, duration: o.dur ?? 0.32, ease: o.ease || 'expo.inOut', immediateRender: false }, t);
    tl.fromTo(q(sel), { filter: 'blur(0px)' }, { filter: `blur(${o.blur ?? 10}px)`, duration: (o.dur ?? 0.32) / 2, ease: 'power2.in', yoyo: true, repeat: 1, immediateRender: false }, t);
  };
  // ink blots that bleed over the frame then clear (REF-D 4.8 s); circles inside an SVG with a goo filter
  K.blots = (sel, t, dur = 0.5) => {
    const cs = [...q(sel)];
    cs.forEach((c, k) => {
      tl.set(c, { attr: { r: 0 } }, 0);
      tl.fromTo(c, { attr: { r: 0 } }, { attr: { r: +c.dataset.r }, duration: dur * 0.55, ease: 'power2.in', immediateRender: false }, t + k * 0.03);
      tl.fromTo(c, { attr: { r: +c.dataset.r } }, { attr: { r: 0 }, duration: dur * 0.45, ease: 'power2.out', immediateRender: false }, t + dur * 0.55 + 0.05 + k * 0.02);
    });
  };
  // extruded word slam: big scale -> 1 with a small overshoot (REF-D headline words)
  K.slam = (sel, t, o = {}) => { K.show(sel, t); return tl.fromTo(q(sel), { scale: o.s0 ?? 1.7, filter: 'blur(10px)' }, { scale: 1, filter: 'blur(0px)', duration: o.dur ?? 0.28, ease: 'back.out(2.2)', stagger: o.stagger || 0 }, t); };
  // letters fly in from scattered positions and assemble (REF-D "COSTCO GIVES AWAY" 0.2-0.6 s)
  K.assemble = (sel, t, o = {}) => {
    const cs = [...q(sel)]; K.show(cs, t);
    cs.forEach((c, k) => {
      const a = (k * 137.5) * Math.PI / 180, r = (o.r ?? 420) * (0.6 + ((k * 7) % 5) / 10);
      tl.fromTo(c, { x: Math.cos(a) * r, y: Math.sin(a) * r, rotation: ((k * 53) % 90) - 45, scale: 0.3, filter: 'blur(8px)' },
        { x: 0, y: 0, rotation: 0, scale: 1, filter: 'blur(0px)', duration: o.dur ?? 0.45, ease: 'expo.out' }, t + k * (o.stagger ?? 0.025));
    });
  };
  K.set = (sel, vars, t) => tl.set(q(sel), vars, t);
  K.to = (sel, vars, t) => tl.to(q(sel), vars, t);
  K.fromTo = (sel, a, b, t) => tl.fromTo(q(sel), a, b, t);
  return K;
})();
