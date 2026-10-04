#!/usr/bin/env python3
"""Given an extracted JSON (from extract.py), produce a reduced translation
worklist: CLOZE_QUESTIONS entries whose `jp` text exactly matches a STORY
entry's `jp` text are auto-resolved (noted as alias), everything else needs
a fresh `ko` (sentence arrays) / `meaningKo` (meaning arrays) translation.
"""
import json
import sys

SENTENCE_ARRAYS = {"STORY", "CLOZE_QUESTIONS"}


def main():
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    story_by_jp = {}
    if "STORY" in data:
        for e in data["STORY"]:
            if e.get("jp"):
                story_by_jp.setdefault(e["jp"], e["id"])

    worklist = {}
    aliases = {}  # array -> {id: story_id}
    for arr, entries in data.items():
        is_sentence = arr in SENTENCE_ARRAYS
        items = []
        for e in entries:
            if arr == "CLOZE_QUESTIONS" and e.get("jp") in story_by_jp:
                aliases.setdefault(arr, {})[e["id"]] = story_by_jp[e["jp"]]
                continue
            text_field = "en" if is_sentence else "meaning"
            items.append({"id": e["id"], "zh": e.get("zh"), "text": e.get(text_field), "jp_or_meaningJp": e.get("jp") or e.get("meaningJp")})
        worklist[arr] = items

    print(json.dumps({"worklist": worklist, "aliases": aliases}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
