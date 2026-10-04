#!/usr/bin/env python3
"""Inject Korean (ko / meaningKo) fields into a lesson HTML file's
STORY / CHARACTERS / WORDS / CLOZE_QUESTIONS data arrays, keyed by each
entry's existing `id`. Translations come from a sibling JSON file
tools_ko/translations/<slug>.json with shape:
  {"STORY": {"st1": "...", ...}, "CLOZE_QUESTIONS": {...},
   "CHARACTERS": {...}, "WORDS": {...}}
For STORY/CLOZE_QUESTIONS the value is the `ko` sentence (inserted after
`jp:"..."` or after `en:"..."` if jp absent).
For CHARACTERS/WORDS the value is the `meaningKo` gloss (inserted after
`meaningJp:"..."` or after `meaning:"..."` if meaningJp absent).
Entries with no matching translation are left untouched (reported).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STR_RE = r'"(?:[^"\\]|\\.)*"'
OBJ_RE = re.compile(r'\{(?:[^{}])*\}', re.DOTALL)


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


def process_array(text, array_name, trans_map, sentence_mode):
    body_m = re.search(r'(const ' + array_name + r'\s*=\s*\[)(.*?)(\n\];)', text, re.DOTALL)
    if body_m is None:
        return text, []
    prefix, body, suffix = body_m.group(1), body_m.group(2), body_m.group(3)
    missing = []

    def repl_obj(om):
        ot = om.group(0)
        id_m = re.search(r'id:\s*(' + STR_RE + r')', ot)
        if not id_m:
            return ot
        oid = id_m.group(1)[1:-1]
        if oid not in trans_map:
            missing.append(oid)
            return ot
        ko_text = esc(trans_map[oid])
        if sentence_mode:
            # insert after jp:"..."; else after en:"..."
            jp_m = re.search(r'jp:\s*(' + STR_RE + r')', ot)
            if jp_m:
                insert_at = jp_m.end()
            else:
                en_m = re.search(r'en:\s*(' + STR_RE + r')', ot)
                if not en_m:
                    return ot
                insert_at = en_m.end()
            return ot[:insert_at] + f', ko:"{ko_text}"' + ot[insert_at:]
        else:
            mjp_m = re.search(r'meaningJp:\s*(' + STR_RE + r')', ot)
            if mjp_m:
                insert_at = mjp_m.end()
            else:
                mm = re.search(r'meaning:\s*(' + STR_RE + r')', ot)
                if not mm:
                    return ot
                insert_at = mm.end()
            return ot[:insert_at] + f', meaningKo:"{ko_text}"' + ot[insert_at:]

    new_body = OBJ_RE.sub(repl_obj, body)
    new_text = text[:body_m.start()] + prefix + new_body + suffix + text[body_m.end():]
    return new_text, missing


SENTENCE_ARRAYS = {"STORY", "CLOZE_QUESTIONS"}


def main():
    html_name = sys.argv[1]
    trans_path = ROOT / "tools_ko" / "translations" / (Path(html_name).stem + ".json")
    translations = json.loads(trans_path.read_text(encoding="utf-8"))
    html_path = ROOT / html_name
    text = html_path.read_text(encoding="utf-8")

    all_missing = {}
    for arr in translations.keys():
        mode = arr in SENTENCE_ARRAYS
        text, missing = process_array(text, arr, translations[arr], mode)
        if missing:
            all_missing[arr] = missing

    html_path.write_text(text, encoding="utf-8")
    if all_missing:
        print(f"[{html_name}] MISSING translations:", json.dumps(all_missing, ensure_ascii=False))
    else:
        print(f"[{html_name}] OK, all ids translated")


if __name__ == "__main__":
    main()
