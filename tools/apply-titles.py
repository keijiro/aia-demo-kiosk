#!/usr/bin/env python3
"""Apply authored titles to a rendered prompts directory (no re-render needed).

Reads <dir>/titles.json ( { "<hash>": "新しいタイトル", ... } ) and, for every
*.html in <dir>:
  - replaces the first <h1>…</h1> text with the mapped title (so the log body
    heading matches the sidebar), and
  - (re)writes <dir>/index.json as [ { "file": "...", "title": "..." }, ... ]
    sorted by filename, using the mapped title (falling back to the existing
    <h1> text, then a filename-derived title when no mapping exists).

Usage:  python3 tools/apply-titles.py <dir>
"""
import sys, os, re, json, glob

HASH_RE = re.compile(r'-([0-9a-fA-F]{6,})\.html$')
H1_RE = re.compile(r'(<h1[^>]*>)(.*?)(</h1>)', re.S)
NAME_RE = re.compile(r'^(\d{8})(?:-(\d{4}))?-(.+)-[0-9a-fA-F]{6,}\.html$')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def derived_title(fn):
    m = NAME_RE.match(fn)
    return m.group(3).replace("_", " ") if m else fn


def main(dirpath):
    tpath = os.path.join(dirpath, "titles.json")
    titles = json.load(open(tpath, encoding="utf-8")) if os.path.exists(tpath) else {}

    entries = []
    patched = 0
    for path in sorted(glob.glob(os.path.join(dirpath, "*.html"))):
        fn = os.path.basename(path)
        h = HASH_RE.search(fn)
        hash_id = h.group(1) if h else None
        html = open(path, encoding="utf-8").read()
        m = H1_RE.search(html)
        current_h1 = re.sub(r"<[^>]+>", "", m.group(2)).strip() if m else None

        title = titles.get(hash_id) if hash_id else None
        if title:
            if m:
                html = H1_RE.sub(lambda mm: mm.group(1) + esc(title) + mm.group(3), html, count=1)
                open(path, "w", encoding="utf-8").write(html)
                patched += 1
        final = title or current_h1 or derived_title(fn)
        entries.append({"file": fn, "title": final})

    entries.sort(key=lambda e: e["file"])
    json.dump(entries, open(os.path.join(dirpath, "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"{dirpath}: {len(entries)} entries, {patched} H1 patched, "
          f"{sum(1 for e in entries if titles.get(HASH_RE.search(e['file']).group(1) if HASH_RE.search(e['file']) else '')) } titled from titles.json")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: apply-titles.py <dir>")
        sys.exit(1)
    main(sys.argv[1])
