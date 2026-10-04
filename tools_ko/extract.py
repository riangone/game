#!/usr/bin/env python3
"""Extract STORY / CHARACTERS / WORDS / CLOZE_QUESTIONS text needing Korean
translation from each lesson HTML file, dumped as JSON for review."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STR_RE = r'"(?:[^"\\]|\\.)*"'
OBJ_RE = re.compile(r'\{(?:[^{}])*\}', re.DOTALL)


def unesc(s):
    if s is None:
        return None
    s = s[1:-1]  # strip quotes
    return s.replace('\\"', '"').replace("\\n", " ")


def field(obj_text, name):
    m = re.search(name + r':\s*(' + STR_RE + r')', obj_text)
    return unesc(m.group(1)) if m else None


def grab_array_body(text, name):
    m = re.search(r'const ' + name + r'\s*=\s*\[(.*?)\n\];', text, re.DOTALL)
    return m.group(1) if m else None


def parse_array(text, name):
    body = grab_array_body(text, name)
    if body is None:
        return []
    out = []
    for om in OBJ_RE.finditer(body):
        ot = om.group(0)
        out.append({
            "id": field(ot, "id"),
            "zh": field(ot, "zh"),
            "en": field(ot, "en"),
            "jp": field(ot, "jp"),
            "meaning": field(ot, "meaning"),
            "meaningJp": field(ot, "meaningJp"),
        })
    return out


def main():
    fname = sys.argv[1]
    arrays = sys.argv[2].split(",") if len(sys.argv) > 2 else \
        ["STORY", "CLOZE_QUESTIONS", "CHARACTERS", "WORDS"]
    text = (ROOT / fname).read_text(encoding="utf-8")
    result = {name: parse_array(text, name) for name in arrays}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
