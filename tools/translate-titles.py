#!/usr/bin/env python3
"""Translate the authored JA prompt-log titles to <lang> via LiteLLM.

Reads <project>/Prompts/titles.json ( { "<hash>": "日本語タイトル" } ) and writes
<project>/Prompts/titles.<lang>.json with the same hash keys and translated
values, in a single request.

Usage:  python3 tools/translate-titles.py <project> <en|ko> [--model NAME]
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _litellm import populate_anthropic_env_from_keychain

TARGET = {"en": "English", "ko": "Korean (자연스러운 한국어)"}

SYSTEM = """\
You translate short UI labels. Each value is a concise title (a few words) \
describing a game-development task, shown in a sidebar list. Translate every \
value into {target}, keeping it concise (no trailing period). Keep technical \
terms / product names (Unity, RPG, UI Toolkit, HUD, MPB, GLB, AudioManager, C#, \
SerializeField, BGM, TIPS, etc.) as-is. Return ONLY a JSON object with the SAME \
keys and translated string values — no commentary, no code fence.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("lang", choices=["en", "ko"])
    ap.add_argument("--model", default="claude-sonnet-4-6")
    args = ap.parse_args()

    src = os.path.join(args.project, "Prompts", "titles.json")
    titles = json.load(open(src, encoding="utf-8"))

    populate_anthropic_env_from_keychain()
    import anthropic
    client = anthropic.Anthropic()

    with client.messages.stream(
        model=args.model, max_tokens=8000,
        system=SYSTEM.format(target=TARGET[args.lang]),
        messages=[{"role": "user", "content": json.dumps(titles, ensure_ascii=False, indent=2)}],
    ) as stream:
        raw = "".join(t for t in stream.text_stream).strip()

    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    out = json.loads(raw)
    # keep only known keys, fall back to original where missing
    merged = {k: (out.get(k) if isinstance(out.get(k), str) else v) for k, v in titles.items()}

    dst = os.path.join(args.project, "Prompts", f"titles.{args.lang}.json")
    json.dump(merged, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {dst} ({len(merged)} titles)")


if __name__ == "__main__":
    main()
