#!/usr/bin/env python3
"""Translate the Japanese conversation in prompt-log .md files via LiteLLM.

Kept verbatim (never sent): fenced code blocks and <details>...</details> blocks
(the assistant's 💭 思考 / 🔧 ツール sections, which are English). The remaining
Japanese prose is split into small fragments and each is translated with its own
plain-text request (no JSON — robust against control chars / extra output). Each
result is verified; fragments that still contain Japanese are retried. A fragment
that cannot be translated after all attempts keeps its original text (the run never
crashes) and is counted in the residual report. <summary> labels are localized via a
static map.

Usage:
  python3 tools/translate-logs.py <srcDir> <outDir> <en|ko> [--model NAME] [--workers N]
"""
import sys, os, glob, time, re, argparse
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _litellm import populate_anthropic_env_from_keychain

TARGET = {"en": "English", "ko": "Korean (자연스러운 한국어)"}
CHUNK_CHARS = 3000
MAX_TOKENS = 12000
ATTEMPTS = 4
# Detect untranslated Japanese by KANA only (hiragana/katakana). Kanji are excluded
# (they appear as Hanja in Korean output) and so is the middle dot ・ (U+30FB), which
# is widely used as a separator in the translated text itself — both are false positives.
# Any genuinely-untranslated Japanese sentence still contains other kana.
JP_RE = re.compile(r"[぀-ヺー-ヿ]")
SUMMARY_LABELS = {"en": {"思考": "Thinking", "ツール": "Tool"},
                  "ko": {"思考": "사고", "ツール": "도구"}}

SYSTEM = """\
You are a professional software-localization translator for a developer's chat with
an AI coding assistant. You receive ONE Markdown fragment. Translate it into {target}.

Rules:
1. Translate ALL Japanese natural-language text. The result must contain no
   untranslated Japanese sentences.
2. Leave text already in English (or any non-Japanese) unchanged.
3. Never alter inline `code`, file paths, identifiers, URLs, numbers, or metadata
   labels (**Date:**, **Project:**, **Messages:**) — reproduce them byte-for-byte.
4. Preserve Markdown markup exactly: headings (#), list markers, bold/italic,
   blockquotes, tables, and the turn headers "## 🧑 User" / "## 🤖 Assistant".
5. Output ONLY the translated fragment — no preamble, no commentary, no surrounding
   code fence, no quotes around it.
"""


def chunk_prose(text, budget):
    lines, chunks, cur, size = text.split("\n"), [], [], 0
    for ln in lines:
        cur.append(ln); size += len(ln) + 1
        if size >= budget and ln.strip() == "":
            chunks.append("\n".join(cur)); cur, size = [], 0
    if cur:
        chunks.append("\n".join(cur))
    return chunks


def build_units(md, budget):
    units, prose, buf, state, depth = [], [], [], "prose", 0

    def flush_prose():
        if prose:
            for ch in chunk_prose("\n".join(prose), budget):
                units.append([ch, bool(JP_RE.search(ch))])
            prose.clear()

    def flush_buf():
        if buf:
            units.append(["\n".join(buf), False]); buf.clear()

    for ln in md.split("\n"):
        s = ln.lstrip()
        if state == "prose":
            if s.startswith("```"):
                flush_prose(); buf.append(ln); state = "code"
            elif "<details>" in ln:
                flush_prose(); buf.append(ln)
                depth = ln.count("<details>") - ln.count("</details>")
                state = "details" if depth > 0 else "prose"
                if depth <= 0:
                    flush_buf()
            else:
                prose.append(ln)
        elif state == "code":
            buf.append(ln)
            if s.startswith("```"):
                flush_buf(); state = "prose"
        else:
            buf.append(ln)
            depth += ln.count("<details>") - ln.count("</details>")
            if depth <= 0:
                flush_buf(); state = "prose"
    flush_prose(); flush_buf()
    return units


PREAMBLE_RE = re.compile(r"^(here is|here's|here are|sure[,!]?|translated text:).*?(translat|fragment|markdown).*?:\s*$", re.I)


def _strip_fence(s):
    s = s.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[-1]
        if s.rstrip().endswith("```"):
            s = s.rsplit("```", 1)[0]
    # drop a leaked model preamble line like "Here is the translated Markdown fragment:"
    first, _, rest = s.partition("\n")
    if PREAMBLE_RE.match(first.strip()):
        s = rest.lstrip("\n")
    return s.strip()


def translate_fragment(client, text, lang, model):
    """Translate one fragment (plain text). Retry while Japanese remains; on
    persistent failure return the best result (never raise)."""
    system = SYSTEM.format(target=TARGET[lang])
    nfence = text.count("```")   # prose fragments carry no fences; never add/drop any
    best = text                  # safe fallback: original keeps structure intact
    have_struct_ok = False
    msg = text
    for attempt in range(ATTEMPTS):
        try:
            with client.messages.stream(
                model=model, max_tokens=MAX_TOKENS, system=system,
                messages=[{"role": "user", "content": msg}],
            ) as stream:
                out = _strip_fence("".join(stream.text_stream))
            struct_ok = out.count("```") == nfence
            if struct_ok:
                if len(JP_RE.findall(out)) < 4:
                    return out                     # perfect: translated + structure intact
                if not have_struct_ok:
                    best, have_struct_ok = out, True  # structurally ok, some kana left
            # echo and/or added fences — push harder next attempt
            msg = (f"Translate the following Markdown into {TARGET[lang]} COMPLETELY. "
                   f"Every Japanese sentence MUST become {TARGET[lang]}; do not copy Japanese "
                   f"verbatim. Do NOT add or remove ``` code fences or backticks. Keep code, "
                   f"paths and Markdown markup byte-for-byte.\n\n" + text)
        except Exception as e:  # noqa: BLE001 - transient API/stream errors
            print(f"    [retry] {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(2 ** attempt)
    return best


def cleanup_residual_lines(text, lang, client, model, pool):
    """Final safety net: re-translate any individual line that still holds Japanese
    (outside code/<details>, excluding the leading H1 which apply-titles replaces)."""
    lines = text.split("\n")
    incode, indet, targets = False, 0, []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("```"):
            incode = not incode; continue
        if incode:
            continue
        op, cl = ln.count("<details>"), ln.count("</details>")
        if indet > 0:
            indet += op - cl; continue
        if op > cl:
            indet += op - cl; continue
        if i == 0 and s.startswith("# "):
            continue
        if JP_RE.search(ln):
            targets.append(i)
    if targets:
        print(f"    cleanup: {len(targets)} residual line(s)", file=sys.stderr)
        fixed = list(pool.map(lambda i: translate_fragment(client, lines[i], lang, model), targets))
        for i, fx in zip(targets, fixed):
            lines[i] = fx.replace("\n", " ")
    return "\n".join(lines)


def ensure_blank_after_details(text):
    """Markdown HTML blocks (<details>...</details>) run until a blank line, so a
    heading/text right after </details> gets swallowed and rendered literally.
    Translation can strip those blank lines; re-insert them (outside code fences)."""
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


def localize_summaries(text, lang):
    labels = SUMMARY_LABELS[lang]
    def fix(m):
        line = m.group(0)
        for ja, tr in labels.items():
            line = line.replace(ja, tr)
        return line
    return re.sub(r"<summary>.*?</summary>", fix, text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("lang", choices=["en", "ko"])
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    populate_anthropic_env_from_keychain()
    import anthropic
    client = anthropic.Anthropic()
    pool = ThreadPoolExecutor(max_workers=args.workers)

    os.makedirs(args.out, exist_ok=True)
    files = sorted(glob.glob(os.path.join(args.src, "*.md")))
    print(f"translating {len(files)} files -> {args.lang} ({args.model}, {args.workers} workers)", file=sys.stderr)
    for i, path in enumerate(files, 1):
        fn = os.path.basename(path)
        outpath = os.path.join(args.out, fn)
        if os.path.exists(outpath):
            print(f"[{i}/{len(files)}] skip (exists) {fn}", file=sys.stderr)
            continue
        md = open(path, encoding="utf-8").read()
        units = build_units(md, CHUNK_CHARS)
        flagged = [j for j, u in enumerate(units) if u[1]]
        t0 = time.time()
        print(f"[{i}/{len(files)}] {fn} ({len(md)//1024} KB; {len(flagged)} fragment(s))", file=sys.stderr)

        out_units = [u[0] for u in units]
        translations = list(pool.map(
            lambda j: translate_fragment(client, units[j][0], args.lang, args.model), flagged))
        for j, tx in zip(flagged, translations):
            out_units[j] = tx

        out_text = cleanup_residual_lines("\n".join(out_units), args.lang, client, args.model, pool)
        out_text = ensure_blank_after_details(out_text)
        out_text = localize_summaries(out_text, args.lang)
        # residual report: count Japanese outside code/<details>, excluding the leading H1
        rl = out_text.split("\n"); incode = indet = residual = 0; incode = False
        for k, ln in enumerate(rl):
            s = ln.strip()
            if s.startswith("```"): incode = not incode; continue
            if incode: continue
            op, cl = ln.count("<details>"), ln.count("</details>")
            if indet > 0: indet += op - cl; continue
            if op > cl: indet += op - cl; continue
            if k == 0 and s.startswith("# "): continue
            residual += len(JP_RE.findall(ln))
        flag = "  *** RESIDUAL JP" if residual >= 4 else ""
        print(f"    -> done in {time.time()-t0:.0f}s (residual JP: {residual}){flag}", file=sys.stderr)

        tmp = outpath + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fp:
            fp.write(out_text)
        os.replace(tmp, outpath)
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
