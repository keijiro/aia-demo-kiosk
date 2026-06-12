#!/usr/bin/env python3
"""Print a compact digest of each prompt log for authoring titles.

For every *.md in the given directory it prints the 8-hex task hash (from the
filename), the current H1 title, and the first few user turns (whitespace
collapsed and truncated). Read the digest, then write a titles.json mapping
"<hash>" -> "新しいタイトル" for apply-titles.py to consume.

Usage:  python3 tools/extract-prompts.py <dir> [num_user_turns] [truncate_chars]
"""
import sys, os, re, glob

HASH_RE = re.compile(r'-([0-9a-fA-F]{6,})\.md$')


def main(dirpath, n_turns=4, trunc=240):
    for path in sorted(glob.glob(os.path.join(dirpath, "*.md"))):
        fn = os.path.basename(path)
        h = HASH_RE.search(fn)
        hash_id = h.group(1) if h else "????????"
        text = open(path, encoding="utf-8").read()
        mt = re.search(r'^#\s+(.+)$', text, re.M)
        title = mt.group(1).strip() if mt else "(no title)"
        parts = re.split(r'^##\s+(🧑 User|🤖 Assistant)\s*$', text, flags=re.M)
        users = [parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)
                 if parts[i].startswith("🧑")]
        print("=" * 100)
        print(f"HASH : {hash_id}")
        print(f"FILE : {fn}")
        print(f"NOW  : {title}")
        print(f"USERTURNS: {len(users)}")
        for j, u in enumerate(users[:n_turns], 1):
            u = re.sub(r'\s+', ' ', u)
            print(f"  [U{j}] {u[:trunc]}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: extract-prompts.py <dir> [num_user_turns] [truncate_chars]")
        sys.exit(1)
    args = sys.argv[2:]
    main(sys.argv[1], int(args[0]) if len(args) > 0 else 4,
         int(args[1]) if len(args) > 1 else 240)
