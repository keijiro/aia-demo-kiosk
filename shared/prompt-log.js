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
// `data-prompts-dir` must contain an `index.json` listing the *.md filenames.
// Requires marked (shared/marked.min.js) to be loaded first. Styles: .prompt-md
// in kiosk.css.
(function () {
  var root = document.querySelector("#prompt-log");
  if (!root) return;

  var dir = root.dataset.promptsDir;
  var listEl = root.querySelector("#prompt-log-list");
  var contentEl = root.querySelector("#prompt-log-content");
  var scroller = contentEl.closest(".overflow-y-auto") || contentEl;

  var BTN_BASE =
    "w-full text-left flex items-center justify-between gap-sm p-md border-l-2 transition-all";
  var BTN_ACTIVE = " bg-surface-container-high text-primary border-primary";
  var BTN_IDLE = " hover:bg-surface-container text-on-surface-variant border-transparent";

  function parseName(file) {
    var base = file.replace(/\.md$/, "");
    var first = base.indexOf("-");
    var last = base.lastIndexOf("-");
    var dateRaw = base.slice(0, first); // e.g. 20260531
    var title = base.slice(first + 1, last).replace(/_/g, " ");
    var date = dateRaw.replace(/(\d{4})(\d{2})(\d{2})/, "$1-$2-$3");
    return { file: file, title: title, date: date, dateRaw: dateRaw };
  }

  // Hide the local filesystem Path and the Task ID from the metadata header.
  function stripMeta(md) {
    return md.replace(/^- \*\*(Path|Task ID):\*\*.*\n?/gm, "");
  }

  function render(md) {
    if (window.marked && typeof window.marked.parse === "function") {
      return window.marked.parse(md);
    }
    // Fallback: escaped preformatted text if marked is unavailable.
    var pre = document.createElement("pre");
    pre.textContent = md;
    return pre.outerHTML;
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
      .then(function (md) {
        contentEl.innerHTML = render(stripMeta(md));
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

  fetch(dir + "/index.json")
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(function (files) {
      var entries = files.map(parseName).sort(function (a, b) {
        return a.dateRaw.localeCompare(b.dateRaw); // oldest first
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
