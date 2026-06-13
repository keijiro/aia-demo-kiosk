# AIA Demo Kiosk

A **static, local kiosk web app** that showcases three Unity WebGL game prototypes
(Drift Mayhem, Dungeon Match Heroes, Mirror Mage) together with the **AI-assistant
chat logs** that produced them. It runs fully client-side and supports three UI
languages (English / Japanese / Korean).

This README documents the things that are **not obvious from the code alone** —
the architecture decisions, the offline build/translation pipeline, and the
gotchas — so work can be resumed in a fresh session.

---

## Running it

Serve the repo root over HTTP (it **cannot** run from `file://` — the Unity builds
and `fetch()`-ed prompt logs need a real origin):

```sh
python3 -m http.server 8000
# open http://localhost:8000/
```

Network is needed at **runtime** only for Tailwind (Play CDN) and Google Fonts.
The Unity builds, prompt logs, and `marked` are all local.

> Unity build caveat: the `.unityweb` files are Brotli/gzip-compressed. Over a
> plain static server they arrive without `Content-Encoding` headers, so the build
> loads only because it was published with **Decompression Fallback** enabled. If a
> rebuilt game fails to load, check that build setting — it's not an embed bug.

---

## Page structure

These HTML pages were originally generated from **Stitch** designs (the "Unity AI
Design System") and then localized into this static site. They are hand-maintained
now; Stitch is not in the runtime loop.

- `index.html` — the **Gallery**. Three game cards (local preview videos in
  `Videos/Project{1,2,3}.mp4`) linking to the detail pages.
- `DriftMayhem.html`, `DungeonMatchHeroes.html`, `MirrorMage.html` — **Project
  Detail** pages. Each one embeds the playable build and the Prompt Log panel.
- `<Game>/` — per-game assets:
  - `Build/` — the Unity WebGL output (`<Game>.{loader.js,data,framework.js,wasm}.unityweb`).
  - `Prompts/` — the prompt logs (see below).
  - Stock Unity `index.html` / `TemplateData/` were **deleted on purpose** (we embed
    the build directly; they're unused).

All pages share the assets in `shared/`. The detail pages are near-identical; only
the hero title/description, the `#unity-container` data-attributes, and the
`#prompt-log` `data-prompts-dir` differ.

---

## `shared/` — runtime assets (loaded by the browser)

| File | Purpose |
|---|---|
| `tailwind-config.js` | Tailwind **Play CDN** theme (design tokens). Loaded right after the CDN `<script>`. |
| `kiosk.css` | Design tokens + component CSS (scrollbars, `ghost-border`, the Unity panel, the `.prompt-md` prose styles, the language switcher). |
| `unity-embed.js` | Embeds the Unity build **directly** (no iframe). Reads `#unity-container` `data-*`. Shows a **"Click to Play"** overlay and defers all loading until clicked; unlocks audio on first interaction. |
| `prompt-log.js` | Builds the Prompt Log sidebar from `index.json` and renders the selected pre-rendered HTML on demand. Language-aware (per-language subdir, falls back to `ja`). |
| `i18n.js` | Reads `?lang=en|ja|ko` (default `en`), sets `<html lang>`, injects the top-right flag switcher, localizes the **description paragraph only**, and propagates `?lang` onto in-site links. |
| `ui.js` | Small shared behaviors: resume autoplay videos after bfcache restore; button press-scale. |

### Unity embed contract (`unity-embed.js`)
```html
<div id="unity-container"
     data-build-dir="DriftMayhem" data-build-name="DriftMayhem"
     data-product-name="Drift Mayhem" data-product-version="0.1" data-company-name="Keijiro">
  <canvas id="unity-canvas" ...></canvas>
  <div id="unity-loading-bar">…</div>
  <div id="unity-warning"></div>
</div>
```
Build URLs are derived as `${dir}/Build/${name}.{loader.js,...}`. The canvas fills
the 1280×720 panel. If a rebuild changes file names / `productVersion`, update these
data-attributes (no JS change needed).

---

## Prompt logs

The logs are AI-assistant chat exports (Japanese conversation, with English
"thinking"/"tool" blocks). **Sources live outside this repo** at
`~/Documents/<Game>/Extras/*.md` and are copied/processed in, never edited in place.

### Layout
```
<Game>/Prompts/
  titles.json          # authored Japanese titles, keyed by the 8-hex task hash (source of truth)
  titles.en.json       # machine-translated titles (generated)
  titles.ko.json       # machine-translated titles (generated)
  ja/  *.html  index.json
  en/  *.html  index.json
  ko/  *.html  index.json
```
- Logs are **pre-rendered to HTML** (not parsed in the browser) and fetched **on
  demand** per selection — total content is ~tens of MB, so never inline them.
- `index.json` is an array of `{ "file": "...html", "title": "..." }`. The sidebar
  shows `title`; the date/time shown is parsed from the **filename**.
- Filenames are `YYYYMMDD-HHMM-Title-hash.html` (sorted oldest-first). DriftMayhem's
  sources originally lacked the time and were in UTC; `normalize-utc-dates.py`
  converts them to JST and adds `HHMM` so all three projects match.
- Titles are **curated** (they summarize the *actual work*, not the first prompt).
  Authored in Japanese in `titles.json`; en/ko are translations of those.

### What gets translated (by design)
- **Translate:** only the Japanese **conversation prose**.
- **Keep verbatim:** fenced code blocks **and** `<details>…</details>` blocks (the
  `💭 思考` / `🔧 ツール` thinking/tool sections — already English). Only their
  `<summary>` labels are localized (思考→Thinking/사고, ツール→Tool/도구).
- Result: JA = the source as-is; EN/KO = Japanese parts translated, everything else
  preserved byte-for-byte.

---

## `tools/` — build/offline pipeline (NOT shipped to the browser)

Run from the repo root. Rendering uses **JavaScriptCore via `osascript`** (no Node
in this environment); `marked` is vendored at `tools/marked.min.js`.

| Tool | Role |
|---|---|
| `extract-prompts.py <dir> [n] [trunc]` | Print a digest (hash + current title + first N user turns) of each `*.md`, for authoring `titles.json`. |
| `normalize-utc-dates.py <dir>` | Convert ` … UTC` header dates to local (JST) and rename files to include `HHMM`. Only DriftMayhem needs it. |
| `translate-logs.py <srcDir> <outDir> <en|ko> [--model] [--workers]` | Translate Japanese conversation → en/ko (code & `<details>` kept verbatim). Uses LiteLLM. |
| `translate-titles.py <Game> <en|ko> [--model]` | Translate `titles.json` values → `Prompts/titles.<lang>.json`. |
| `render-prompts.js <dir>` | (osascript) Render every `*.md` in `<dir>` to `*.html` + write `index.json`. Strips the `Path` / `Task ID` metadata lines. |
| `apply-titles.py <dir> [titles.json]` | Patch each HTML `<h1>` and (re)write `index.json` as `{file,title}` from a titles map. |
| `fix-detail-blanks.py <dir>` | Insert a blank line after `</details>` when missing (see gotcha below). Now also baked into `translate-logs.py`. |
| `_litellm.py` | Helper: populate `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN` from the macOS Keychain. |

### LiteLLM / translation prerequisites
- Translation calls go to Unity's internal LiteLLM (`https://uai-litellm.internal.unity.com`)
  via the `anthropic` SDK. **You must be on the Unity corporate VPN** or you get a
  403 from the gateway.
- Auth comes from macOS **Keychain** items `LITELLM_BASE_URL` / `LITELLM_AUTH_TOKEN`
  (mapped to `ANTHROPIC_*` by `_litellm.py`). No keys are stored in the repo.
- Default model `claude-sonnet-4-6`; a few stubborn files were redone with
  `--model claude-opus-4-7`.

### `work/` — scratch build area
`work/<Game>/{src,en,ko}/` holds the intermediate `.md`. It is **regenerable** and
not needed at runtime (safe to delete / gitignore). `src/` = normalized Japanese
source; `en/`,`ko/` = translated `.md` before rendering.

---

## Regenerating logs (canonical flow)

For a game `G` (e.g. `DriftMayhem`):

```sh
# 0) source -> work/G/src
rm -rf work/G/src && mkdir -p work/G/src
cp ~/Documents/G/Extras/*.md work/G/src/
python3 tools/normalize-utc-dates.py work/G/src        # DriftMayhem only

# 1) Japanese (no translation): render src as-is
osascript -l JavaScript tools/render-prompts.js work/G/src
mkdir -p G/Prompts/ja && cp work/G/src/*.html work/G/src/index.json G/Prompts/ja/
python3 tools/apply-titles.py G/Prompts/ja G/Prompts/titles.json

# 2) English / Korean  (needs VPN + Keychain)
for L in en ko; do
  python3 tools/translate-logs.py work/G/src work/G/$L $L            # slow; chunked API calls
  osascript -l JavaScript tools/render-prompts.js work/G/$L
  mkdir -p G/Prompts/$L && cp work/G/$L/*.html work/G/$L/index.json G/Prompts/$L/
  python3 tools/translate-titles.py G $L
  python3 tools/apply-titles.py G/Prompts/$L G/Prompts/titles.$L.json
done
```

Authoring titles: run `extract-prompts.py` on the source dir, read the digests, and
hand-write `G/Prompts/titles.json` as `{ "<hash>": "日本語タイトル" }`.

### Verifying a regeneration
For each output `.md`, confirm vs. its `src` counterpart:
- code-fence count (```` ``` ````) matches (no structure corruption),
- `<details>` count matches,
- no residual **kana** outside code/`<details>` (excluding the H1, which
  `apply-titles` overwrites). Kanji/Hanja and `・` are **not** counted as residual.

---

## i18n details

- `?lang=en|ja|ko`, default `en`. Switcher is top-right (flag emojis 🇺🇸/🇯🇵/🇰🇷,
  always full color; selection shown by background).
- **Only the game description paragraph** is localized statically (via
  `data-i18n` + `data-ja` / `data-ko` attributes on that `<p>`). Genre lines, the
  "AI Generated Assets" list, UI labels, and page `<title>` stay English by design.
- Game titles (`<h1>`/`<h2>`) carry `lang="en"` so the browser keeps the Latin serif
  (EB Garamond) and does **not** substitute a CJK font under `?lang=ja|ko`.
- Language **persists across navigation** because `i18n.js` appends the current
  `?lang` to same-origin links (gallery cards, "Learn More", back link). It does
  **not** persist for a fresh direct visit with no `?lang` (no storage) — that was
  the chosen scope ("approach A"); switch to `localStorage` if sticky-across-restart
  is wanted.

---

## Gotchas / non-obvious decisions

- **Serve over HTTP**, never `file://` (Unity loader + `fetch`).
- **Markdown + `<details>`:** an HTML block runs until a blank line, so a heading
  placed directly after `</details>` (no blank line) is swallowed and rendered
  literally (e.g. `## 🧑 User` shown verbatim). Translation stripped those blanks;
  `fix-detail-blanks.py` / `ensure_blank_after_details()` re-insert them.
- **Residual-Japanese detection is kana-only** (`[぀-ヺー-ヿ]`). Kanji are excluded
  because they appear legitimately as Hanja in Korean; the middle dot `・` (U+30FB)
  is excluded because it's a common separator in the translated text. Some residual
  Japanese is **correct** (quoted in-game strings, terms under discussion,
  before→after code-comment diffs).
- **Translation is per-fragment plain text** (not a JSON batch): batching caused
  `JSONDecodeError`s and a single bad item could abort a whole run. The translator
  also guards the **code-fence count** (a fragment that adds/removes ``` is rejected
  → falls back to the original to protect structure) and strips leaked model
  preambles ("Here is the translated …:").
- **zsh does not word-split** unquoted parameters — `set -- $pair` will not split
  `"A B"` into two args. Bit us once; prefer explicit args in shell loops here.
- **No Node**: rendering runs `marked` under `osascript -l JavaScript`. Keep
  `tools/marked.min.js` in sync if you bump marked.
- **`.DS_Store`** is gitignored; the external `Extras/` dirs also contain `.DS_Store`
  / `.claude` which the `cp *.md` steps ignore.
