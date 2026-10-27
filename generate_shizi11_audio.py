#!/usr/bin/env python3
"""Generate neural-TTS MP3 audio for 《中文》第一册 第11课《认方向》(shizi-11.html).

Same pipeline as the Book 4 lessons (hanjia-jianwen etc.), using edge-tts:
- audio/shizi11/          title, st1-4, zi1-10, vc1-12, cloze_1-12   (zh-CN-XiaoxiaoNeural)
- audio/shizi11_en|ja|ko/ st1-4 translations (Jenny / Nanami / SunHi)
- audio/shizi11_clause/   st{n}_c{m} clause clips for the ClausePlayer
- data/shizi11_clauses.json + the "shizi11" entry in data/lesson-clauses-data.js

Keep the text in sync with STORY / CHARACTERS / VOCAB / CLOZE_QUESTIONS in shizi-11.html.
"""
import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent
SLUG = "shizi11"
ZH_VOICE, ZH_RATE = "zh-CN-XiaoxiaoNeural", "-12%"
CLAUSE_RATE = "-10%"  # same as generate_all_clause_audio.py
LANG_VOICES = {
    "en": ("en-US-JennyNeural", "-8%"),
    "ja": ("ja-JP-NanamiNeural", "-10%"),
    "ko": ("ko-KR-SunHiNeural", "-8%"),
}

# id, zh, py, en, ja, ko, clauses [(zh, py, en, ja, ko), ...]
STORY = [
    ("st1", "早上起来，面向太阳。", "Zǎoshang qǐlai, miànxiàng tàiyáng.",
     "Getting up in the morning, I face the sun.", "朝起きて、太陽のほうを向きます。", "아침에 일어나서, 해를 바라봐요.",
     [("早上起来，", "Zǎoshang qǐlai,", "Getting up in the morning,", "朝起きて、", "아침에 일어나서,"),
      ("面向太阳。", "miànxiàng tàiyáng.", "I face the sun.", "太陽のほうを向きます。", "해를 바라봐요.")]),
    ("st2", "前面是东，后面是西。", "Qiánmiàn shì dōng, hòumiàn shì xī.",
     "In front is east, behind is west.", "前は東、後ろは西です。", "앞쪽은 동쪽, 뒤쪽은 서쪽이에요.",
     [("前面是东，", "Qiánmiàn shì dōng,", "In front is east,", "前は東、", "앞쪽은 동쪽,"),
      ("后面是西。", "hòumiàn shì xī.", "behind is west.", "後ろは西です。", "뒤쪽은 서쪽이에요.")]),
    ("st3", "左面是北，右面是南。", "Zuǒmiàn shì běi, yòumiàn shì nán.",
     "On the left is north, on the right is south.", "左は北、右は南です。", "왼쪽은 북쪽, 오른쪽은 남쪽이에요.",
     [("左面是北，", "Zuǒmiàn shì běi,", "On the left is north,", "左は北、", "왼쪽은 북쪽,"),
      ("右面是南。", "yòumiàn shì nán.", "on the right is south.", "右は南です。", "오른쪽은 남쪽이에요.")]),
    ("st4", "东南西北，四个方向。", "Dōng nán xī běi, sì ge fāngxiàng.",
     "East, south, west and north: the four directions.", "東・南・西・北、四つの方角です。", "동남서북, 네 가지 방향이에요.",
     [("东南西北，", "Dōng nán xī běi,", "East, south, west and north:", "東・南・西・北、", "동남서북,"),
      ("四个方向。", "sì ge fāngxiàng.", "the four directions.", "四つの方角です。", "네 가지 방향이에요.")]),
]

TITLE = [("title", "认方向")]
CHARS = [(f"zi{i+1}", c) for i, c in enumerate("认方向面太阳东西北南")]
VOCAB = [(f"vc{i+1}", w) for i, w in enumerate(
    ["方向", "早上", "太阳", "前面", "后面", "左面", "右面", "起来", "面向", "东南西北", "认识", "东方"])]
CLOZE = [(f"cloze_{i+1}", s) for i, s in enumerate([
    "早上起来，面向太阳。",
    "早上起来，面向太阳。",
    "前面是东，后面是西。",
    "前面是东，后面是西。",
    "左面是北，右面是南。",
    "左面是北，右面是南。",
    "东南西北，四个方向。",
    "东南西北，四个方向。",
    "太阳从东方升起，从西方落下。",
    "我家门口的大树在左面，小花园在右面。",
    "早上七点，我背着书包去学校。",
    "在外面找不到路的时候，可以看太阳认方向。",
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
    meta = {"lesson": SLUG, "title": "认方向", "totalSentences": len(sentences),
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
