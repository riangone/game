#!/usr/bin/env python3
"""
英文课文构建：data/en-lessons-data.json（唯一数据源）→ data/en-lessons-data.js

步骤:
  1. 为 vocabulary / topicWords 自动补全派生字段：
     - example / exampleZh：本课对话中第一句包含该词（含屈折形式）的句子
     - forms：该词在全部课文对话中出现过的表面形式（前端点查、高亮、挖空用）
  2. 运行 check_en_lessons.py 的全部规则，有错误则中止，不写产物
  3. 写回 JSON（派生字段）并生成 JS

流水线: 编辑 JSON → python3 build_en_lessons.py → python3 generate_en_lessons_audio.py
不要手改 data/en-lessons-data.js。
"""
import json
import sys

from check_en_lessons import DATA_FILE, ROOT, check, load_ranks, same_lexeme, tokens

JS_FILE = ROOT / "data" / "en-lessons-data.js"
JS_HEADER = (
    "// 由 build_en_lessons.py 从 data/en-lessons-data.json 生成，请勿手改。\n"
    "// English Micro-Narrative Curriculum Data\n"
)


def enrich(lessons):
    all_tokens = {tok for l in lessons for line in l["dialogue"] for tok in tokens(line["en"])}
    for lesson in lessons:
        for entry in lesson.get("vocabulary", []) + lesson.get("topicWords", []):
            word = entry["word"]
            line = next((d for d in lesson["dialogue"]
                         if any(same_lexeme(t, word) for t in tokens(d["en"]))), None)
            if line:
                entry["example"] = line["en"]
                entry["exampleZh"] = line["zh"]
            forms = {t.lower() for t in all_tokens if same_lexeme(t, word)}
            forms.add(word.lower())
            entry["forms"] = sorted(forms, key=lambda f: (len(f), f))


def main():
    lessons = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    enrich(lessons)
    errors, warnings, _ = check(lessons, load_ranks())
    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        for e in errors:
            print(f"ERROR {e}")
        print(f"\n构建中止：{len(errors)} 个错误（详见 python3 check_en_lessons.py --report）")
        sys.exit(1)
    body = json.dumps(lessons, ensure_ascii=False, indent=2)
    DATA_FILE.write_text(body + "\n", encoding="utf-8")
    JS_FILE.write_text(f"{JS_HEADER}window.EN_LESSONS_DATA = {body};\n", encoding="utf-8")
    print(f"OK  {len(lessons)} 课 → {JS_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
