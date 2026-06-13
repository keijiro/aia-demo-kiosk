#!/usr/bin/env python3
"""Ensure a blank line follows every </details> (outside code fences).

Markdown treats <details>...</details> as an HTML block that continues until a
blank line, so a heading or text placed directly after </details> (no blank line)
is swallowed into the HTML block and rendered literally (e.g. "## 🧑 User" shown
verbatim). Translation stripped those blank lines; this restores them.

Usage:  python3 tools/fix-detail-blanks.py <dir-with-*.md>
"""
import sys, os, glob


def fix(text):
    lines = text.split("\n")
    out, incode = [], False
    for i, ln in enumerate(lines):
        out.append(ln)
        s = ln.strip()
        if s.startswith("```"):
            incode = not incode
            continue
        if not incode and s.endswith("</details>"):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt.strip() != "":
                out.append("")
    return "\n".join(out)


def main(dirpath):
    changed = 0
    for p in sorted(glob.glob(os.path.join(dirpath, "*.md"))):
        t = open(p, encoding="utf-8").read()
        nt = fix(t)
        if nt != t:
            open(p, "w", encoding="utf-8").write(nt)
            changed += 1
    print(f"{dirpath}: fixed {changed} file(s)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: fix-detail-blanks.py <dir>")
        sys.exit(1)
    main(sys.argv[1])
