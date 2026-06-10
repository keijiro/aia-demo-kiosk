// Shared lightweight UI behaviors for all kiosk pages.
// Safe to include everywhere: each part no-ops when its targets are absent.
(function () {
  // Resume autoplaying preview videos when the page is restored from the
  // back/forward cache (bfcache); otherwise they stay paused after navigating
  // back. Also covers the normal initial load.
  window.addEventListener("pageshow", function () {
    document.querySelectorAll("video").forEach(function (v) {
      var p = v.play();
      if (p && typeof p.catch === "function") p.catch(function () {});
    });
  });

  // Smooth press-scale micro-interaction for buttons and links.
  document.querySelectorAll("button, a").forEach(function (el) {
    el.addEventListener("mousedown", function () { el.classList.add("scale-95"); });
    el.addEventListener("mouseup", function () { el.classList.remove("scale-95"); });
    el.addEventListener("mouseleave", function () { el.classList.remove("scale-95"); });
  });
})();
