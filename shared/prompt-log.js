// Shared "Prompt Log" controller for the project detail pages.
//
// Markup contract (see DriftMayhem.html):
//   <div id="prompt-log" data-prompts-dir="DriftMayhem/Prompts">
//     <aside id="prompt-log-list"></aside>            <- buttons injected here
//     <div class="... overflow-y-auto ...">
//       <div id="prompt-log-content" class="prompt-md"></div>
//     </div>
//   </div>
//
// `data-prompts-dir` must contain an `index.json` listing pre-rendered *.html
// fragments (produced by tools/render-prompts.js). View time is just fetch +
// innerHTML — no client-side markdown parsing. Styles: .prompt-md in kiosk.css.
(function () {
  var root = document.querySelector("#prompt-log");
  if (!root) return;

  var base = root.dataset.promptsDir;
  var lang = (function () {
    var l = new URLSearchParams(location.search).get("lang");
    return l === "ja" || l === "ko" || l === "en" ? l : "en";
  })();
  var dir = base + "/" + lang; // resolved/committed in loadIndex()
  var listEl = root.querySelector("#prompt-log-list");
  var contentEl = root.querySelector("#prompt-log-content");
  var scroller = contentEl.closest(".overflow-y-auto") || contentEl;

  var BTN_BASE =
    "w-full text-left flex items-center justify-between gap-sm p-md border-l-2 transition-all";
  var BTN_ACTIVE = " bg-surface-container-high text-primary border-primary";
  var BTN_IDLE = " hover:bg-surface-container text-on-surface-variant border-transparent";

  // Filenames are "YYYYMMDD-Title-hash" or "YYYYMMDD-HHMM-Title-hash"
  // (the optional HHMM time segment varies by project).
  function parseName(file) {
    var base = file.replace(/\.(html|md)$/, "");
    var m = base.match(/^(\d{8})(?:-(\d{4}))?-(.+)-[0-9a-f]{6,}$/);
    var dateRaw, time, titleRaw;
    if (m) {
      dateRaw = m[1]; time = m[2] || ""; titleRaw = m[3];
    } else {
      var first = base.indexOf("-"), last = base.lastIndexOf("-");
      dateRaw = base.slice(0, first); time = ""; titleRaw = base.slice(first + 1, last);
    }
    var date = dateRaw.replace(/(\d{4})(\d{2})(\d{2})/, "$1-$2-$3");
    if (time) date += " " + time.slice(0, 2) + ":" + time.slice(2);
    return { file: file, title: titleRaw.replace(/_/g, " "), date: date, sortKey: dateRaw + (time || "0000") };
  }

  function setActive(button) {
    listEl.querySelectorAll("button").forEach(function (b) {
      b.className = BTN_BASE + (b === button ? BTN_ACTIVE : BTN_IDLE);
      var chevron = b.querySelector(".chevron");
      if (chevron) chevron.style.visibility = b === button ? "visible" : "hidden";
    });
  }

  function select(entry, button) {
    setActive(button);
    contentEl.innerHTML = '<p class="text-outline">Loading…</p>';
    fetch(dir + "/" + entry.file)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.text();
      })
      .then(function (html) {
        contentEl.innerHTML = html;
        scroller.scrollTop = 0;
      })
      .catch(function (err) {
        contentEl.innerHTML =
          '<p class="text-error">Failed to load log: ' + err.message + "</p>";
      });
  }

  function buildButton(entry) {
    var btn = document.createElement("button");
    btn.className = BTN_BASE + BTN_IDLE;
    var label = document.createElement("span");
    label.className = "flex flex-col min-w-0";
    var title = document.createElement("span");
    title.className = "font-label-md truncate";
    title.textContent = entry.title;
    var date = document.createElement("span");
    date.className = "font-label-sm text-outline";
    date.textContent = entry.date;
    label.appendChild(title);
    label.appendChild(date);
    var chevron = document.createElement("span");
    chevron.className = "material-symbols-outlined text-sm chevron shrink-0";
    chevron.style.visibility = "hidden";
    chevron.textContent = "chevron_right";
    btn.appendChild(label);
    btn.appendChild(chevron);
    btn.addEventListener("click", function () { select(entry, btn); });
    return btn;
  }

  // Load the language index; fall back to ja if the chosen language isn't built.
  function loadIndex(d, isFallback) {
    return fetch(d + "/index.json").then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      dir = d; // commit the working dir that select() fetches from
      return r.json();
    }).catch(function (err) {
      if (!isFallback && d !== base + "/ja") {
        console.warn("prompt-log: '" + lang + "' unavailable, falling back to ja");
        return loadIndex(base + "/ja", true);
      }
      throw err;
    });
  }

  loadIndex(dir)
    .then(function (items) {
      // index.json entries may be plain filenames or { file, title } objects;
      // an explicit title (authored in titles.json) overrides the filename one.
      var entries = items.map(function (it) {
        var file = typeof it === "string" ? it : it.file;
        var meta = parseName(file);
        if (it && it.title) meta.title = it.title;
        return meta;
      }).sort(function (a, b) {
        return a.sortKey.localeCompare(b.sortKey); // oldest first
      });
      listEl.innerHTML = "";
      var firstButton = null;
      var firstEntry = null;
      entries.forEach(function (entry, i) {
        var btn = buildButton(entry);
        listEl.appendChild(btn);
        if (i === 0) { firstButton = btn; firstEntry = entry; }
      });
      if (firstEntry) select(firstEntry, firstButton);
    })
    .catch(function (err) {
      contentEl.innerHTML =
        '<p class="text-error">Failed to load prompt index: ' + err.message + "</p>";
    });
})();
