#!/usr/bin/env python3
"""Normalize prompt-log .md files in a directory to the common kiosk format.

For each *.md whose header `- **Date:** ... UTC` line is in UTC, convert it to
the system local timezone (dropping the " UTC" suffix) and rename the file to
include the local time: `YYYYMMDD-HHMM-Title-hash.md` (the date part is taken
from the local datetime too, so it follows any midnight rollover). Files whose
Date line is already local (no " UTC") are left untouched.

Usage:  python3 tools/normalize-utc-dates.py <promptsDir>
"""
import sys, os, re, glob
from datetime import datetime, timezone

NAME_RE = re.compile(r'^(\d{8})(?:-(\d{4}))?-(.+)-([0-9a-fA-F]{6,})\.md$')
DATE_RE = re.compile(r'^(- \*\*Date:\*\* )(.+?)\s*$', re.M)


def main(dirpath):
    changed = 0
    for path in sorted(glob.glob(os.path.join(dirpath, "*.md"))):
        fn = os.path.basename(path)
        text = open(path, encoding="utf-8").read()
        m = DATE_RE.search(text)
        if not m or not m.group(2).endswith("UTC"):
            continue  # already local (or no Date) -> leave as-is

        raw = m.group(2).replace("UTC", "").strip()
        dt_utc = datetime.strptime(raw, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        loc = dt_utc.astimezone()

        new_text = DATE_RE.sub(lambda mm: mm.group(1) + loc.strftime("%Y-%m-%d %H:%M"), text, count=1)

        nm = NAME_RE.match(fn)
        if not nm:
            print(f"  WARN: unrecognized filename, skipping rename: {fn}")
            new_name = fn
        else:
            title, h = nm.group(3), nm.group(4)
            new_name = f"{loc.strftime('%Y%m%d-%H%M')}-{title}-{h}.md"

        new_path = os.path.join(dirpath, new_name)
        with open(new_path, "w", encoding="utf-8") as fp:
            fp.write(new_text)
        if new_name != fn:
            os.remove(path)
        print(f"  {fn}  ->  {new_name}")
        changed += 1
    print(f"normalized {changed} file(s) in {dirpath}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: normalize-utc-dates.py <promptsDir>")
        sys.exit(1)
    main(sys.argv[1])
