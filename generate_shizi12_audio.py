#!/usr/bin/env python3
"""Generate neural-TTS MP3 audio for 《中文》第一册 第12课《新年到》(shizi-12.html).

Same pipeline as the Book 4 lessons (hanjia-jianwen etc.), using edge-tts:
- audio/shizi12/          title, st1-4, zi1-12, vc1-12, cloze_1-12   (zh-CN-XiaoxiaoNeural)
- audio/shizi12_en|ja|ko/ st1-4 translations (Jenny / Nanami / SunHi)
- audio/shizi12_clause/   st{n}_c{m} clause clips for the ClausePlayer
- data/shizi12_clauses.json + the "shizi12" entry in data/lesson-clauses-data.js

Keep the text in sync with STORY / CHARACTERS / VOCAB / CLOZE_QUESTIONS in shizi-12.html.
"""
import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent
SLUG = "shizi12"
ZH_VOICE, ZH_RATE = "zh-CN-XiaoxiaoNeural", "-12%"
CLAUSE_RATE = "-10%"  # same as generate_all_clause_audio.py
LANG_VOICES = {
    "en": ("en-US-JennyNeural", "-8%"),
    "ja": ("ja-JP-NanamiNeural", "-10%"),
    "ko": ("ko-KR-SunHiNeural", "-8%"),
}

# id, zh, py, en, ja, ko, clauses [(zh, py, en, ja, ko), ...]
STORY = [
    ("st1", "新年到，真热闹，", "Xīnnián dào, zhēn rènao,",
     "The New Year is here. How lively it is!", "新年が来た、とてもにぎやか、", "새해가 왔어요, 정말 북적북적해요,",
     [("新年到，", "Xīnnián dào,", "The New Year is here.", "新年が来た、", "새해가 왔어요,"),
      ("真热闹，", "zhēn rènao,", "How lively it is!", "とてもにぎやか、", "정말 북적북적해요,")]),
    ("st2", "穿新衣，戴新帽。", "Chuān xīn yī, dài xīn mào.",
     "We put on new clothes and new hats.", "新しい服を着て、新しい帽子をかぶります。", "새 옷을 입고, 새 모자를 써요.",
     [("穿新衣，", "Chuān xīn yī,", "We put on new clothes", "新しい服を着て、", "새 옷을 입고,"),
      ("戴新帽。", "dài xīn mào.", "and new hats.", "新しい帽子をかぶります。", "새 모자를 써요.")]),
    ("st3", "我祝大家身体好，", "Wǒ zhù dàjiā shēntǐ hǎo,",
     "I wish everyone good health,", "わたしはみんなの健康を祈り、", "나는 모두가 건강하기를 빌고,",
     [("我祝大家身体好，", "Wǒ zhù dàjiā shēntǐ hǎo,", "I wish everyone good health,", "わたしはみんなの健康を祈り、", "나는 모두가 건강하기를 빌고,")]),
    ("st4", "大家祝我学习好。", "Dàjiā zhù wǒ xuéxí hǎo.",
     "and everyone wishes me well in my studies.", "みんなはわたしが勉強をがんばれるよう祈ってくれます。", "모두는 내가 공부를 잘하기를 빌어 줘요.",
     [("大家祝我学习好。", "Dàjiā zhù wǒ xuéxí hǎo.", "and everyone wishes me well in my studies.", "みんなはわたしが勉強をがんばれるよう祈ってくれます。", "모두는 내가 공부를 잘하기를 빌어 줘요.")]),
]

TITLE = [("title", "新年到")]
CHARS = [(f"zi{i+1}", c) for i, c in enumerate("新到热闹穿衣戴帽祝身体习")]
VOCAB = [(f"vc{i+1}", w) for i, w in enumerate(
    ["新年", "热闹", "大家", "身体", "学习", "新衣", "新帽", "衣服", "帽子", "祝福", "春节", "拜年"])]
CLOZE = [(f"cloze_{i+1}", s) for i, s in enumerate([
    "新年到，真热闹，",
    "新年到，真热闹，",
    "穿新衣，戴新帽。",
    "穿新衣，戴新帽。",
    "我祝大家身体好，",
    "我祝大家身体好，",
    "大家祝我学习好。",
    "大家祝我学习好。",
    "天冷了，出门要戴上帽子。",
    "过新年，妈妈给我买了新衣服。",
    "多运动，身体才会好。",
    "春节到了，我祝爷爷奶奶新年快乐！",
])]


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                         capture_output=True, text=True, check=True)
    return round(float(out.stdout.strip()), 3)


async def main():
    sem = asyncio.Semaphore(4)
    jobs = []

    def job(path, text, voice, rate):
        async def run():
            path.parent.mkdir(parents=True, exist_ok=True)
            async with sem:
                await edge_tts.Communicate(text, voice, rate=rate).save(str(path))
            size = path.stat().st_size if path.exists() else 0
            print(("OK  " if size > 500 else "WARN") + f" {path.relative_to(ROOT)} ({text})")
        jobs.append(run())

    zh_dir = ROOT / "audio" / SLUG
    for fid, text in TITLE + [(s[0], s[1]) for s in STORY] + CHARS + VOCAB + CLOZE:
        job(zh_dir / f"{fid}.mp3", text, ZH_VOICE, ZH_RATE)
    for idx, lang in ((3, "en"), (4, "ja"), (5, "ko")):
        voice, rate = LANG_VOICES[lang]
        for s in STORY:
            job(ROOT / "audio" / f"{SLUG}_{lang}" / f"{s[0]}.mp3", s[idx], voice, rate)
    clause_dir = ROOT / "audio" / f"{SLUG}_clause"
    for s in STORY:
        for ci, c in enumerate(s[6]):
            job(clause_dir / f"{s[0]}_c{ci+1}.mp3", c[0], ZH_VOICE, CLAUSE_RATE)

    await asyncio.gather(*jobs)

    # Clause timeline metadata, same shape as generate_all_clause_audio.py (+ ko fields)
    g = 0.0
    sentences = []
    for si, (sid, zh, py, en, ja, ko, clauses) in enumerate(STORY):
        start, local, items = g, 0.0, []
        for ci, (czh, cpy, cen, cja, cko) in enumerate(clauses):
            cid = f"{sid}_c{ci+1}"
            d = duration(clause_dir / f"{cid}.mp3")
            items.append({"id": cid, "sentId": sid, "sentIndex": si, "clauseIndex": ci,
                          "zh": czh, "py": cpy, "en": cen, "jp": cja, "ko": cko,
                          "audioUrl": f"audio/{SLUG}_clause/{cid}.mp3", "duration": d,
                          "sentOffsetStart": round(local, 3), "sentOffsetEnd": round(local + d, 3),
                          "globalOffsetStart": round(g, 3), "globalOffsetEnd": round(g + d, 3)})
            local += d
            g += d
        sentences.append({"sentId": sid, "sentIndex": si, "sentZh": zh, "sentPy": py, "sentEn": en,
                          "sentJp": ja, "sentKo": ko, "clauses": items, "duration": round(local, 3),
                          "globalOffsetStart": round(start, 3), "globalOffsetEnd": round(g, 3),
                          "clauseCount": len(items)})
    meta = {"lesson": SLUG, "title": "新年到", "totalSentences": len(sentences),
            "totalClauses": sum(s["clauseCount"] for s in sentences),
            "totalDuration": round(g, 3), "sentences": sentences}
    (ROOT / "data" / f"{SLUG}_clauses.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    # Merge into the bundle that the pages load (window.ALL_LESSON_CLAUSES = {...};)
    bundle_path = ROOT / "data" / "lesson-clauses-data.js"
    prefix = "window.ALL_LESSON_CLAUSES = "
    raw = bundle_path.read_text(encoding="utf-8").strip()
    assert raw.startswith(prefix) and raw.endswith(";")
    bundle = json.loads(raw[len(prefix):-1])
    bundle[SLUG] = meta
    bundle_path.write_text(prefix + json.dumps(bundle, ensure_ascii=False, separators=(",", ":")) + ";",
                           encoding="utf-8")
    print(f"Clauses: {meta['totalClauses']}, {meta['totalDuration']}s -> {bundle_path.relative_to(ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
