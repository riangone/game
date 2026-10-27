#!/usr/bin/env python3
"""data/grade2/**/*.json から registry.js と units-manifest.json を再生成する。

ユニット JSON が唯一の正。編集後は:  python3 build_registry.py && python3 generate_audio.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "grade2"
SUBJECTS = {  # 表示順・メタ情報
    "japanese": ("国語", "#ef4444"),
    "math": ("数学", "#3b82f6"),
    "english": ("英語", "#10b981"),
    "science": ("理科", "#8b5cf6"),
    "society": ("社会", "#f59e0b"),
}
REQUIRED = ["unitId", "subject", "title", "grade", "story", "flashcards", "scrambles", "matches", "cloze", "quizzes"]


def validate(u, path):
    for k in REQUIRED:
        assert k in u, f"{path}: missing {k}"
    assert u["subject"] in SUBJECTS, f"{path}: bad subject"
    for q in u["quizzes"]:
        assert 0 <= q["answerIndex"] < len(q["options"]), f"{path}: {q['id']} answerIndex"
        assert len(set(q["options"])) == len(q["options"]), f"{path}: {q['id']} duplicate options"
    for c in u["cloze"]:
        assert c["answer"] in c["options"], f"{path}: {c['id']} answer not in options"
    for s in u["scrambles"]:
        assert s.get("steps") or s.get("tokens"), f"{path}: {s['id']} empty"
    for side in ("left", "right"):
        vals = [m[side] for m in u["matches"]]
        assert len(vals) == len(set(vals)), f"{path}: duplicate match {side}"
    ids = [x["id"] for x in u["story"] + u["flashcards"]]
    assert len(ids) == len(set(ids)), f"{path}: duplicate story/flashcard ids"


def main():
    units, seen = [], set()
    for p in sorted(DATA.glob("*/*.json")):
        u = json.loads(p.read_text(encoding="utf-8"))
        validate(u, p)
        assert u["unitId"] not in seen, f"duplicate unitId {u['unitId']}"
        seen.add(u["unitId"])
        units.append((u, p))
    subj_order = list(SUBJECTS)
    units.sort(key=lambda t: (subj_order.index(t[0]["subject"]), t[0].get("order", 99), t[0]["unitId"]))

    js = ("// registry.js - 自動生成 (build_registry.py)。直接編集せず data/grade2/**/*.json を編集すること\n"
          "window.CHUGAKU_DATA = window.CHUGAKU_DATA || {};\n"
          "window.CHUGAKU_DATA.grade2 = {\n  units: "
          + json.dumps([u for u, _ in units], ensure_ascii=False, indent=2) + "\n};\n")
    (DATA / "registry.js").write_text(js, encoding="utf-8")

    manifest = [{
        "id": u["unitId"], "subject": u["subject"], "subjectName": SUBJECTS[u["subject"]][0],
        "title": u["title"], "order": u.get("order"), "color": SUBJECTS[u["subject"]][1],
        "file": str(p.relative_to(ROOT)),
    } for u, p in units]
    (ROOT / "data" / "units-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for u, _ in units:
        n = lambda k: len(u[k])
        print(f"{u['subject']:9} {u.get('order','-'):>2} {u['unitId']:26} st{n('story')} fc{n('flashcards')} sc{n('scrambles')} m{n('matches')} cl{n('cloze')} qz{n('quizzes')}")
    print(f"{len(units)} units")


if __name__ == "__main__":
    main()
