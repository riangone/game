#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate high-quality neural-TTS MP3 audio for the Chinese situational lesson series:
zh0 (拼音与日常问候), zh1 (我的一星期), zh2 (我的一天), zh3 (中国的四季).

Uses edge-tts (Microsoft Azure neural voices, free, pre-cached static files):
- Chinese (Mandarin): zh-CN-XiaoxiaoNeural, rate -10%
- English (US): en-US-JennyNeural, rate -8%
- Japanese: ja-JP-NanamiNeural, rate -10%

Output directories:
- audio/zh0/, audio/zh1/, audio/zh2/, audio/zh3/
- audio/zh0_en/, audio/zh1_en/, audio/zh2_en/, audio/zh3_en/
- audio/zh0_ja/, audio/zh1_ja/, audio/zh2_ja/, audio/zh3_ja/
"""

import asyncio
from pathlib import Path
import edge_tts
from build_chinese_lessons import LESSONS

ROOT_DIR = Path(__file__).resolve().parent

ZH_VOICE = "zh-CN-XiaoxiaoNeural"
ZH_RATE = "-10%"
EN_VOICE = "en-US-JennyNeural"
EN_RATE = "-8%"
JA_VOICE = "ja-JP-NanamiNeural"
JA_RATE = "-10%"

sem = asyncio.Semaphore(8)

async def generate_speech_file(out_file: Path, text: str, voice: str, rate: str):
    if out_file.exists() and out_file.stat().st_size > 0:
        return
    out_file.parent.mkdir(parents=True, exist_ok=True)
    async with sem:
        for attempt in range(3):
            try:
                comm = edge_tts.Communicate(text, voice, rate=rate)
                await comm.save(str(out_file))
                break
            except Exception as e:
                if attempt == 2:
                    print(f"[FAIL] {out_file}: {e}")
                else:
                    await asyncio.sleep(0.5 * (attempt + 1))

async def main():
    tasks = []
    
    # 1. Pinyin sample audio into audio/zh/
    missing_samples = [
        ("tí", "提"),
        ("nǐ", "你"),
        ("hǎo", "好"),
        ("xiè", "谢"),
        ("dōng", "东"),
        ("rén", "人"),
        ("hóng", "红"),
    ]
    zh_dir = ROOT_DIR / "audio" / "zh"
    for py, char in missing_samples:
        tasks.append(generate_speech_file(zh_dir / f"{py}.mp3", char, ZH_VOICE, ZH_RATE))

    # 2. Per-lesson audio files
    for lesson in LESSONS:
        prefix = lesson["id"]
        dir_zh = ROOT_DIR / "audio" / prefix
        dir_en = ROOT_DIR / "audio" / f"{prefix}_en"
        dir_ja = ROOT_DIR / "audio" / f"{prefix}_ja"

        # Story (zh, en, ja)
        for s in lesson["story"]:
            s_id = s["id"]
            tasks.append(generate_speech_file(dir_zh / f"{s_id}.mp3", s["zh"], ZH_VOICE, ZH_RATE))
            tasks.append(generate_speech_file(dir_en / f"{s_id}.mp3", s["en"], EN_VOICE, EN_RATE))
            if "jp" in s and s["jp"]:
                tasks.append(generate_speech_file(dir_ja / f"{s_id}.mp3", s["jp"], JA_VOICE, JA_RATE))

        # Characters (zi1..zi12)
        for c in lesson["characters"]:
            tasks.append(generate_speech_file(dir_zh / f"{c['id']}.mp3", c["zh"], ZH_VOICE, ZH_RATE))

        # Words (ci1..ci12)
        for w in lesson["words"]:
            tasks.append(generate_speech_file(dir_zh / f"{w['id']}.mp3", w["zh"], ZH_VOICE, ZH_RATE))

        # Proper Nouns (pn1..pn7)
        for p in lesson["proper_nouns"]:
            tasks.append(generate_speech_file(dir_zh / f"{p['id']}.mp3", p["zh"], ZH_VOICE, ZH_RATE))

        # Scramble key sentences (sent1)
        for sc in lesson["scramble_sentences"]:
            if sc.get("id") == "sent1":
                tasks.append(generate_speech_file(dir_zh / "sent1.mp3", sc["zh"], ZH_VOICE, ZH_RATE))

        # Cloze full sentences (cloze_1..cloze_8)
        for cl in lesson["cloze"]:
            audio_id = cl.get("audioId")
            full_text = cl["before"] + cl["answer"] + cl["after"]
            if audio_id:
                tasks.append(generate_speech_file(dir_zh / f"{audio_id}.mp3", full_text, ZH_VOICE, ZH_RATE))

    print(f"Total audio tasks to process: {len(tasks)}")
    await asyncio.gather(*tasks)
    print("All audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
