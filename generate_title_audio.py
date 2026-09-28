#!/usr/bin/env python3
"""Generate `title.mp3` for every Chinese 课文 (lesson) app's audio folder.

These are used by the new "《课名》🔊" pronunciation button added to the
读课文 (Sentence by Sentence) screen in each app -- students can now hear
the lesson title itself read aloud, not just the story sentences.

Uses the exact same voice/rate as each lesson's own generate_*_audio.py
script (all currently share zh-CN-XiaoxiaoNeural / -12%), so the title
clip matches the rest of that lesson's narration.
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"

# (audio subfolder, title text)
LESSONS = [
    ("gugong", "故宫"),
    ("hanjia", "寒假见闻"),
    ("yiheyuan", "颐和园"),
    ("luotuo", "骆驼和羊"),
    ("xiaoma", "小马过河"),
    ("houzi", "猴子捞月亮"),
    ("sima", "司马光"),
    ("xingxing", "数星星的孩子"),
    ("gushi", "古诗二首"),
    ("diqiu", "地球清洁工"),
    ("daziran", "大自然的语言"),
    ("tanyue", "探月"),
]


async def main():
    sem = asyncio.Semaphore(4)

    async def generate_one(slug, text):
        out_dir = ROOT / "audio" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "title.mp3"
        try:
            async with sem:
                comm = edge_tts.Communicate(text, VOICE, rate=RATE)
                await comm.save(str(target))
            if target.exists() and target.stat().st_size > 500:
                print(f"OK  audio/{slug}/title.mp3  ({text})")
            else:
                print(f"WARN audio/{slug}/title.mp3 looks too small")
        except Exception as e:
            print(f"FAIL {slug}: {e}")

    await asyncio.gather(*(generate_one(slug, text) for slug, text in LESSONS))
    print("Done generating title audio.")


if __name__ == "__main__":
    asyncio.run(main())
