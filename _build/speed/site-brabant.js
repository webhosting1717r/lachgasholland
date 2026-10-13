/* Lachgas Brabant: menu sluiten na navigatie en service worker registreren. */
(function () {
  "use strict";
  var S = window.__site = window.__site || {};
  S.init = function () {
    var m = document.querySelector("details.menu"); if (m) m.open = false;
  };
  if ("serviceWorker" in navigator && (location.protocol === "https:" || /^(localhost|127\.0\.0\.1)$/.test(location.hostname))) {
    window.addEventListener("load", function () { navigator.serviceWorker.register("/sw.js").catch(function () {}); });
  }
})();
