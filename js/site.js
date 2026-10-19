/* Lachgas Brabant: menu sluiten na navigatie en service worker registreren. */
(function () {
  "use strict";
  var S = window.__site = window.__site || {};
  // zachte reveal van kaarten en sectiekoppen onder de vouw; niets boven de vouw, geen layoutverschuiving, uit bij reduced motion.
  // Na het tonen gaan de hulpklassen weer weg, zodat hover-overgangen van de elementen zelf ongemoeid blijven.
  var RV = "main .grid > *, main .pf, main .sec-head, main .steps > div, main .usp > div, main .mb-12.text-center, main .mb-10.text-center", io, pending = [], tick = false;
  function show(el) {
    el.classList.add("in"); el.setAttribute("data-rv", "1");
    setTimeout(function () { el.classList.remove("rv", "in"); el.style.transitionDelay = ""; }, 1000);
  }
  function sweep() {
    tick = false;
    var vh = window.innerHeight, keep = [];
    for (var i = 0; i < pending.length; i++) {
      var el = pending[i]; if (el.classList.contains("in")) continue;
      var r = el.getBoundingClientRect();
      if (r.top < vh && r.bottom > 0) show(el); else keep.push(el);
    }
    pending = keep;
  }
  function onMove() { if (!tick && pending.length) { tick = true; requestAnimationFrame(sweep); } }
  function reveal() {
    if (!window.matchMedia || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (io) io.disconnect();
    io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { show(en.target); io.unobserve(en.target); } }); }, { rootMargin: "0px 0px -6% 0px", threshold: 0 }) : null;
    pending = [];
    var els = document.querySelectorAll(RV), vh = window.innerHeight, n = 0, last = null;
    for (var i = 0; i < els.length; i++) {
      var el = els[i]; if (el.hasAttribute("data-rv") || el.classList.contains("in")) continue;
      var r = el.getBoundingClientRect();
      if (!el.classList.contains("rv")) {
        if (r.top < vh || r.height === 0) continue;
        if (el.parentNode !== last) { last = el.parentNode; n = 0; }
        el.style.transitionDelay = (Math.min(n++, 3) * 70) + "ms";
        el.classList.add("rv");
      }
      pending.push(el); if (io) io.observe(el);
    }
    if (!io) sweep();
    // vangnet: wat na een tijdje nog verborgen is (buiten beeld), wordt stilletjes zichtbaar gemaakt
    setTimeout(function () { pending.forEach(show); pending = []; }, 8000);
  }
  window.addEventListener("scroll", onMove, { passive: true });
  window.addEventListener("resize", onMove, { passive: true });
  S.init = function () {
    var m = document.querySelector("details.menu"); if (m) m.open = false;
    reveal();
  };
  S.init();
  if ("serviceWorker" in navigator && (location.protocol === "https:" || /^(localhost|127\.0\.0\.1)$/.test(location.hostname))) {
    window.addEventListener("load", function () { navigator.serviceWorker.register("/sw.js").catch(function () {}); });
  }
})();
