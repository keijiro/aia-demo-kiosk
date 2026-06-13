// Shared lightweight i18n for the kiosk.
//
// Language is chosen via ?lang=en|ja|ko (default en). This script:
//   - sets <html lang>,
//   - injects a fixed top-right EN · 日本語 · 한국어 switcher,
//   - localizes only elements tagged data-i18n (the game description paragraph),
//     swapping innerHTML to their data-ja / data-ko value for those languages.
// Everything else (genre, asset list, UI labels, titles) stays English.
// Prompt-log bodies are localized separately by shared/prompt-log.js.
(function () {
  var LANGS = [
    { code: "en", label: "EN" },
    { code: "ja", label: "日本語" },
    { code: "ko", label: "한국어" },
  ];

  var lang = (function () {
    var l = new URLSearchParams(location.search).get("lang");
    return l === "ja" || l === "ko" || l === "en" ? l : "en";
  })();
  window.KIOSK_LANG = lang;
  document.documentElement.lang = lang;

  // Localize tagged elements (description paragraph only).
  if (lang !== "en") {
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var v = el.dataset[lang];
      if (v) el.innerHTML = v;
    });
  }

  // Top-right language switcher.
  function langHref(code) {
    var u = new URL(location.href);
    u.searchParams.set("lang", code);
    return u.pathname + u.search;
  }
  var nav = document.createElement("nav");
  nav.id = "lang-switch";
  LANGS.forEach(function (l) {
    var a = document.createElement("a");
    a.href = langHref(l.code);
    a.textContent = l.label;
    if (l.code === lang) a.className = "active";
    nav.appendChild(a);
  });
  document.body.appendChild(nav);
})();
