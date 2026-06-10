// Shared Unity WebGL embedder for the project detail pages.
//
// Drop a configured container anywhere on the page:
//   <div id="unity-container"
//        data-build-dir="DriftMayhem"      (folder holding Build/ and StreamingAssets/)
//        data-build-name="DriftMayhem"     (build file basename; defaults to build-dir)
//        data-product-name="Drift Mayhem"
//        data-product-version="0.1"
//        data-company-name="Keijiro">
//     <canvas id="unity-canvas" tabindex="-1"></canvas>
//     <div id="unity-loading-bar"><div id="unity-progress-bar-empty"><div id="unity-progress-bar-full"></div></div></div>
//     <div id="unity-warning"></div>
//   </div>
//
// Then load this file (after the page DOM). The matching styles live in kiosk.css.
(function () {
  var container = document.querySelector("#unity-container");
  if (!container) return;

  var canvas = container.querySelector("#unity-canvas");
  var loadingBar = container.querySelector("#unity-loading-bar");
  var progressFull = container.querySelector("#unity-progress-bar-full");

  var dir = container.dataset.buildDir;
  var name = container.dataset.buildName || dir;
  var buildUrl = dir + "/Build";

  function unityShowBanner(msg, type) {
    var warningBanner = container.querySelector("#unity-warning");
    function updateBannerVisibility() {
      warningBanner.style.display = warningBanner.children.length ? "block" : "none";
    }
    var div = document.createElement("div");
    div.innerHTML = msg;
    warningBanner.appendChild(div);
    if (type == "error") {
      div.style = "background: red; color: #fff; padding: 10px;";
    } else {
      if (type == "warning") div.style = "background: yellow; padding: 10px;";
      setTimeout(function () {
        warningBanner.removeChild(div);
        updateBannerVisibility();
      }, 5000);
    }
    updateBannerVisibility();
  }

  var config = {
    arguments: [],
    dataUrl: buildUrl + "/" + name + ".data.unityweb",
    frameworkUrl: buildUrl + "/" + name + ".framework.js.unityweb",
    codeUrl: buildUrl + "/" + name + ".wasm.unityweb",
    streamingAssetsUrl: dir + "/StreamingAssets",
    companyName: container.dataset.companyName || "",
    productName: container.dataset.productName || "",
    productVersion: container.dataset.productVersion || "",
    showBanner: unityShowBanner,
  };

  // Capture any AudioContext the engine creates so it can be resumed on the
  // first user interaction anywhere on the page (browser autoplay policy),
  // not only when the canvas itself is clicked.
  var audioContexts = [];
  var OrigAC = window.AudioContext || window.webkitAudioContext;
  if (OrigAC) {
    var WrappedAC = function () {
      var ctx = new OrigAC(...arguments);
      audioContexts.push(ctx);
      return ctx;
    };
    WrappedAC.prototype = OrigAC.prototype;
    window.AudioContext = WrappedAC;
    window.webkitAudioContext = WrappedAC;
  }
  function resumeAudio() {
    audioContexts.forEach(function (c) { if (c.state === "suspended") c.resume(); });
  }
  ["pointerdown", "keydown", "touchstart"].forEach(function (ev) {
    window.addEventListener(ev, resumeAudio, { passive: true });
  });

  loadingBar.style.display = "block";

  var loader = document.createElement("script");
  loader.src = buildUrl + "/" + name + ".loader.js";
  loader.onload = function () {
    createUnityInstance(canvas, config, function (progress) {
      progressFull.style.width = 100 * progress + "%";
    }).then(function (unityInstance) {
      window.unityInstance = unityInstance;
      loadingBar.style.display = "none";
    }).catch(function (message) {
      unityShowBanner(message, "error");
    });
  };
  document.body.appendChild(loader);
})();
