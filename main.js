(function () {
  var root = document.documentElement;
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- chainsaw intro (home only; <html class="intro"> is set in <head>) ---------- */
  var intro = document.getElementById('intro');
  function ready() { root.classList.add('ready'); }
  if (intro && root.classList.contains('intro')) {
    var saw = intro.querySelector('.saw');
    var done = false;
    var finish = function () {
      if (done) return; done = true;
      root.classList.add('opening');
      ready();
      setTimeout(function () { root.classList.remove('intro', 'cutting', 'opening'); intro.remove(); }, 1000);
    };
    // Sawdust: spawn chips at the saw's tip while it travels.
    var spawn = setInterval(function () {
      var r = saw.getBoundingClientRect();
      if (r.left > innerWidth) return;
      for (var i = 0; i < 4; i++) {
        var c = document.createElement('i');
        c.className = 'chip';
        c.style.left = (r.left + r.width * 0.72) + 'px';
        c.style.top = (innerHeight / 2) + 'px';
        c.style.setProperty('--dx', (-40 - Math.random() * 140) + 'px');
        c.style.setProperty('--dy', ((Math.random() - 0.5) * 220) + 'px');
        c.style.setProperty('--r', (Math.random() * 720) + 'deg');
        intro.appendChild(c);
        setTimeout(c.remove.bind(c), 900);
      }
    }, 40);
    requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add('cutting'); }); });
    setTimeout(function () { clearInterval(spawn); finish(); }, 1300);
    intro.addEventListener('click', function () { clearInterval(spawn); finish(); });
    try { sessionStorage.setItem('introSeen', '1'); } catch (e) {}
  } else {
    requestAnimationFrame(ready);
  }

  /* ---------- header: solid after scrolling past the top ---------- */
  var header = document.querySelector('header');
  var onScroll = function () { header.classList.toggle('solid', scrollY > 40); };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- mobile drawer ---------- */
  var drawer = document.getElementById('drawer');
  document.querySelectorAll('[data-drawer]').forEach(function (b) {
    b.addEventListener('click', function () { drawer.classList.toggle('open'); });
  });
  drawer.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { drawer.classList.remove('open'); });
  });

  /* ---------- reveal on scroll ---------- */
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- count-up stats ---------- */
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var end = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
    var run = function () {
      var t0 = performance.now();
      (function step(t) {
        var p = Math.min(1, (t - t0) / 1400), v = end * (1 - Math.pow(1 - p, 3));
        el.textContent = v.toFixed(dec);
        if (p < 1) requestAnimationFrame(step);
      })(t0);
    };
    if (reduced || !('IntersectionObserver' in window)) return;
    el.textContent = (0).toFixed(dec);
    var o = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { run(); o.disconnect(); } });
    o.observe(el);
  });

  /* ---------- reviews carousel: autoplay + arrows + dots ---------- */
  document.querySelectorAll('.carousel').forEach(function (car) {
    var track = car.querySelector('.track'), slides = track.children;
    var dots = car.querySelector('.dots'), bar = car.querySelector('.progress span');
    var DELAY = 5500, timer, paused = false;
    var perView = function () { return Math.max(1, Math.round(track.clientWidth / slides[0].offsetWidth)); };
    var pages = function () { return slides.length - perView() + 1; };
    var current = function () {
      var x = track.scrollLeft, best = 0;
      for (var i = 0; i < slides.length; i++) if (Math.abs(slides[i].offsetLeft - track.offsetLeft - x) < Math.abs(slides[best].offsetLeft - track.offsetLeft - x)) best = i;
      return best;
    };
    var go = function (i) {
      var n = pages(); i = (i + n) % n;
      track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: reduced ? 'auto' : 'smooth' });
    };
    var buildDots = function () {
      dots.innerHTML = '';
      for (var i = 0; i < pages(); i++) {
        var b = document.createElement('button');
        b.setAttribute('aria-label', 'Go to review ' + (i + 1));
        b.addEventListener('click', go.bind(null, i));
        dots.appendChild(b);
      }
      mark();
    };
    var mark = function () {
      var c = Math.min(current(), dots.children.length - 1);
      [].forEach.call(dots.children, function (d, i) { d.classList.toggle('on', i === c); });
    };
    var restart = function () {
      clearTimeout(timer);
      if (bar) { bar.classList.remove('run'); void bar.offsetWidth; }
      if (paused || reduced) return;
      if (bar) { bar.style.setProperty('--dur', DELAY + 'ms'); bar.classList.add('run'); }
      timer = setTimeout(function () { go(current() + 1); restart(); }, DELAY);
    };
    car.querySelector('.prev').addEventListener('click', function () { go(current() - 1); restart(); });
    car.querySelector('.next').addEventListener('click', function () { go(current() + 1); restart(); });
    var st;
    track.addEventListener('scroll', function () { clearTimeout(st); st = setTimeout(mark, 80); }, { passive: true });
    ['mouseenter', 'focusin', 'touchstart'].forEach(function (ev) { car.addEventListener(ev, function () { paused = true; restart(); }, { passive: true }); });
    ['mouseleave', 'focusout', 'touchend'].forEach(function (ev) { car.addEventListener(ev, function () { paused = false; restart(); }, { passive: true }); });
    addEventListener('resize', buildDots);
    buildDots(); restart();
  });

  /* ---------- WhatsApp bubble: show tip once after a few seconds ---------- */
  var wa = document.querySelector('.wa');
  if (wa) {
    setTimeout(function () { wa.classList.add('tip'); }, 4500);
    setTimeout(function () { wa.classList.remove('tip'); }, 11000);
  }

  /* ---------- estimate form -> prefilled email ---------- */
  var form = document.getElementById('estimate-form');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = new FormData(form);
    var body = 'Name: ' + f.get('name') + '\nPhone: ' + f.get('phone') + '\nAddress/City: ' + f.get('address') +
      '\nType of work: ' + f.get('work') + '\n\nMessage:\n' + f.get('message');
    location.href = 'mailto:sandpointe5tar@gmail.com?subject=' +
      encodeURIComponent('Free estimate request - ' + f.get('work')) + '&body=' + encodeURIComponent(body);
  });

  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();
})();
