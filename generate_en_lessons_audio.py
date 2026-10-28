#!/usr/bin/env python3
"""
Generate neural-TTS MP3 audio for English Micro-Narrative lessons (edge-tts).
  - Female voice: en-US-JennyNeural (chunks, vocabulary, speaker B)
  - Male voice:   en-US-GuyNeural   (speaker A)
Outputs:
  audio/en_chunks/{chunk_id}.mp3
  audio/en_dialogues/{dialogue_id}.mp3
  audio/en_vocab/{vocab_id|topic_id}.mp3

audio/en_audio_manifest.json 记录每个文件对应的 (文本, 声音, 语速) 指纹：
文本改动后会自动重新生成；不再被任何课文引用的旧文件会被删除。
用法: python3 generate_en_lessons_audio.py [--force]
"""
import asyncio
import hashlib
import json
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "en-lessons-data.json"
AUDIO = ROOT / "audio"
DIRS = {"chunk": AUDIO / "en_chunks", "dialogue": AUDIO / "en_dialogues", "vocab": AUDIO / "en_vocab"}
MANIFEST = AUDIO / "en_audio_manifest.json"

VOICE_FEMALE = "en-US-JennyNeural"
VOICE_MALE = "en-US-GuyNeural"
RATE_NORMAL = "+0%"


def jobs(lessons):
    for lesson in lessons:
        for c in lesson.get("chunks", []):
            yield DIRS["chunk"] / f"{c['id']}.mp3", c["text"].replace("...", ""), VOICE_FEMALE
        for v in lesson.get("vocabulary", []) + lesson.get("topicWords", []):
            yield DIRS["vocab"] / f"{v['id']}.mp3", v["word"], VOICE_FEMALE
        for d in lesson.get("dialogue", []):
            voice = VOICE_MALE if d.get("speaker") == "A" else VOICE_FEMALE
            yield DIRS["dialogue"] / f"{d['id']}.mp3", d["en"], voice


def fingerprint(text, voice):
    return hashlib.sha1(f"{text}|{voice}|{RATE_NORMAL}".encode()).hexdigest()[:16]


async def main(force=False):
    lessons = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for d in DIRS.values():
        d.mkdir(parents=True, exist_ok=True)

    wanted, made = {}, 0
    for path, text, voice in jobs(lessons):
        key = str(path.relative_to(ROOT))
        fp = fingerprint(text, voice)
        wanted[key] = fp
        if not force and path.exists() and path.stat().st_size > 0 and manifest.get(key) == fp:
            continue
        await edge_tts.Communicate(text, voice, rate=RATE_NORMAL).save(str(path))
        made += 1
        print(f"  [TTS] {key}: {text}")

    removed = 0
    for d in DIRS.values():
        for f in d.glob("*.mp3"):
            if str(f.relative_to(ROOT)) not in wanted:
                f.unlink()
                removed += 1
                print(f"  [DEL] {f.relative_to(ROOT)}")

    MANIFEST.write_text(json.dumps(dict(sorted(wanted.items())), indent=1) + "\n")
    print(f"\n生成 {made} 个，删除 {removed} 个，共 {len(wanted)} 个音频")


if __name__ == "__main__":
    asyncio.run(main(force="--force" in sys.argv))
