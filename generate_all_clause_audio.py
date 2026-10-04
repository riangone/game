#!/usr/bin/env python3
"""Batch generate clause-level audio and timeline metadata for all Chinese textbook lessons.
"""
import asyncio
import json
import re
import subprocess
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-10%"

LESSONS = [
    {"html": "hanjia-jianwen.html", "slug": "hanjia", "title": "寒假见闻"},
    {"html": "gugong.html", "slug": "gugong", "title": "故宫"},
    {"html": "yiheyuan.html", "slug": "yiheyuan", "title": "颐和园"},
    {"html": "luotuo-he-yang.html", "slug": "luotuo", "title": "骆驼和羊"},
    {"html": "xiaoma-guohe.html", "slug": "xiaoma", "title": "小马过河"},
    {"html": "houzi-lao-yueliang.html", "slug": "houzi", "title": "猴子捞月亮"},
    {"html": "sima-guang.html", "slug": "sima", "title": "司马光"},
    {"html": "shu-xingxing.html", "slug": "xingxing", "title": "数星星的孩子"},
    {"html": "gushi-er-shou.html", "slug": "gushi", "title": "古诗二首"},
    {"html": "diqiu-qingjiegong.html", "slug": "diqiu", "title": "地球清洁工"},
    {"html": "daziran-yuyan.html", "slug": "daziran", "title": "大自然的语言"},
    {"html": "tanyue.html", "slug": "tanyue", "title": "探月"},
]

def split_clauses_zh(text):
    puncts = set('，、；：。！？,!?;:')
    parts = []
    cur = ''
    chars = list(text)
    n = len(chars)
    i = 0
    while i < n:
        ch = chars[i]
        cur += ch
        if ch in puncts:
            # Check trailing quotes
            if i + 1 < n and chars[i+1] in '”’"\'':
                cur += chars[i+1]
                i += 1
            parts.append(cur.strip())
            cur = ''
        i += 1
    if cur.strip():
        if parts:
            parts[-1] += cur.strip()
        else:
            parts.append(cur.strip())
    return [p for p in parts if p]

def split_clauses_by_punct(text):
    if not text:
        return []
    # Split by common western & chinese punctuation
    puncts = set('，、；：。！？,!?;:')
    parts = []
    cur = ''
    chars = list(text)
    n = len(chars)
    i = 0
    while i < n:
        ch = chars[i]
        cur += ch
        if ch in puncts:
            if i + 1 < n and chars[i+1] in '”’"\'':
                cur += chars[i+1]
                i += 1
            parts.append(cur.strip())
            cur = ''
        i += 1
    if cur.strip():
        if parts:
            parts[-1] += cur.strip()
        else:
            parts.append(cur.strip())
    return [p for p in parts if p]

def get_duration(file_path):
    try:
        res = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(file_path)],
            capture_output=True, text=True, check=True
        )
        return round(float(res.stdout.strip()), 3)
    except Exception as e:
        print(f"Error reading duration for {file_path}: {e}")
        return 2.0

def extract_story_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'const STORY = (\[[\s\S]*?\]);', content)
    if not m:
        return []
    raw_json = m.group(1)
    # Convert JS object syntax to valid JSON
    # Replace unquoted keys (id:, zh:, py:, en:, jp:) with quoted keys
    cleaned = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)\s*:', r'\1"\2":', raw_json)
    # Remove trailing commas before } or ]
    cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
    try:
        return json.loads(cleaned)
    except Exception as err:
        print(f"JSON load failed on {file_path}, fallback to eval-style parser: {err}")
        # Simple regex extraction of items
        items = []
        item_matches = re.finditer(r'\{[^{}]*id\s*:\s*["\']([^"\']+)["\'][^{}]*\}', raw_json)
        for im in item_matches:
            block = im.group(0)
            id_m = re.search(r'id\s*:\s*["\']([^"\']+)["\']', block)
            zh_m = re.search(r'zh\s*:\s*["\']([^"\']+)["\']', block)
            py_m = re.search(r'py\s*:\s*["\']([^"\']+)["\']', block)
            en_m = re.search(r'en\s*:\s*["\']([^"\']+)["\']', block)
            jp_m = re.search(r'jp\s*:\s*["\']([^"\']+)["\']', block)
            if id_m and zh_m:
                items.append({
                    "id": id_m.group(1),
                    "zh": zh_m.group(1),
                    "py": py_m.group(1) if py_m else "",
                    "en": en_m.group(1) if en_m else "",
                    "jp": jp_m.group(1) if jp_m else ""
                })
        return items

async def process_all_lessons():
    sem = asyncio.Semaphore(5)
    all_lessons_meta = {}

    for l_info in LESSONS:
        html_file = ROOT / l_info["html"]
        slug = l_info["slug"]
        title = l_info["title"]
        out_dir = ROOT / "audio" / f"{slug}_clause"
        out_dir.mkdir(parents=True, exist_ok=True)

        story_items = extract_story_from_html(html_file)
        print(f"\n==============================")
        print(f"Processing 《{title}》 ({slug}): {len(story_items)} sentences")

        # Step 1: parse clauses
        lesson_sentences = []
        generation_tasks = []

        for s_idx, item in enumerate(story_items):
            sent_id = item.get("id", f"st{s_idx+1}")
            zh_clauses = split_clauses_zh(item.get("zh", ""))
            py_clauses = split_clauses_by_punct(item.get("py", ""))
            en_clauses = split_clauses_by_punct(item.get("en", ""))
            jp_clauses = split_clauses_by_punct(item.get("jp", ""))

            c_count = len(zh_clauses)
            parsed_clauses = []

            for c_idx, zh_c in enumerate(zh_clauses):
                cid = f"{sent_id}_c{c_idx+1}"
                target_mp3 = out_dir / f"{cid}.mp3"
                
                # Match py, en, jp or fallback
                py_c = py_clauses[c_idx] if c_idx < len(py_clauses) else item.get("py", "")
                en_c = en_clauses[c_idx] if c_idx < len(en_clauses) else item.get("en", "")
                jp_c = jp_clauses[c_idx] if c_idx < len(jp_clauses) else item.get("jp", "")

                clause_entry = {
                    "id": cid,
                    "sentId": sent_id,
                    "sentIndex": s_idx,
                    "clauseIndex": c_idx,
                    "zh": zh_c,
                    "py": py_c,
                    "en": en_c,
                    "jp": jp_c,
                    "audioUrl": f"audio/{slug}_clause/{cid}.mp3"
                }
                parsed_clauses.append(clause_entry)

                async def gen(t_path=target_mp3, t_text=zh_c, cid_name=cid):
                    if t_path.exists() and t_path.stat().st_size > 800:
                        return
                    async with sem:
                        try:
                            comm = edge_tts.Communicate(t_text, VOICE, rate=RATE)
                            await comm.save(str(t_path))
                        except Exception as err:
                            print(f"Failed {slug}/{cid_name} ({t_text}): {err}")

                generation_tasks.append(gen())

            lesson_sentences.append({
                "sentId": sent_id,
                "sentIndex": s_idx,
                "sentZh": item.get("zh", ""),
                "sentPy": item.get("py", ""),
                "sentEn": item.get("en", ""),
                "sentJp": item.get("jp", ""),
                "clauses": parsed_clauses
            })

        # Run TTS generation
        print(f"Generating {len(generation_tasks)} audio clauses for {slug}...")
        await asyncio.gather(*generation_tasks)

        # Measure durations and compute offsets
        global_time = 0.0
        processed_sentences = []

        for sent in lesson_sentences:
            sent_duration = 0.0
            sent_start_global = global_time

            for c in sent["clauses"]:
                target_mp3 = out_dir / f"{c['id']}.mp3"
                dur = get_duration(target_mp3)
                c["duration"] = dur
                c["sentOffsetStart"] = round(sent_duration, 3)
                c["sentOffsetEnd"] = round(sent_duration + dur, 3)
                c["globalOffsetStart"] = round(global_time, 3)
                c["globalOffsetEnd"] = round(global_time + dur, 3)
                sent_duration += dur
                global_time += dur

            sent["duration"] = round(sent_duration, 3)
            sent["globalOffsetStart"] = round(sent_start_global, 3)
            sent["globalOffsetEnd"] = round(global_time, 3)
            sent["clauseCount"] = len(sent["clauses"])
            processed_sentences.append(sent)

        lesson_meta = {
            "lesson": slug,
            "title": title,
            "totalSentences": len(processed_sentences),
            "totalClauses": sum(s["clauseCount"] for s in processed_sentences),
            "totalDuration": round(global_time, 3),
            "sentences": processed_sentences
        }

        # Save individual lesson metadata
        single_meta_file = DATA_DIR / f"{slug}_clauses.json"
        with open(single_meta_file, "w", encoding="utf-8") as f:
            json.dump(lesson_meta, f, ensure_ascii=False, indent=2)

        print(f"✓ Saved {single_meta_file}: {lesson_meta['totalClauses']} clauses, {lesson_meta['totalDuration']}s duration.")
        all_lessons_meta[slug] = lesson_meta

    all_meta_file = DATA_DIR / "all_lesson_clauses.json"
    with open(all_meta_file, "w", encoding="utf-8") as f:
        json.dump(all_lessons_meta, f, ensure_ascii=False, indent=2)

    print(f"\n=======================================================")
    print(f"ALL DONE! Processed {len(all_lessons_meta)} lessons.")
    print(f"Master metadata saved to: {all_meta_file}")

if __name__ == "__main__":
    asyncio.run(process_all_lessons())
