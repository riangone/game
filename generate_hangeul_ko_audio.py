#!/usr/bin/env python3
"""Generate audio/ko/<text>.mp3 for every Korean syllable/word clickable in hangeul.html.

hangeul.html's playHangeulSound()/playVocabSound() request audio/ko/<text>.mp3; that dir did not
exist, so everything fell back to browser speechSynthesis (unreliable for isolated syllables).
Single jamo (ㄱ, ㅏ ...) are NOT generated here — see generate_hangeul_jamo_audio.py.

Sources: all Hangul tokens in the data block (HANGEUL_UNITS .. STORAGE_KEY) + the 19x10 syllable matrix.
  python3 generate_hangeul_ko_audio.py [--force]
"""
import asyncio
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from tools_ko.ko_tts import synth_citation  # noqa: E402

OUT_DIR = ROOT / "audio" / "ko"
OUT_DIR.mkdir(parents=True, exist_ok=True)
JAMO = re.compile(r"[ㄱ-ㆎ]")


def collect():
    src = (ROOT / "hangeul.html").read_text(encoding="utf-8")
    data = src[src.index("const HANGEUL_UNITS"):src.index("const STORAGE_KEY")]
    items = {t for t in re.findall(r"[가-힣]+", data)}
    # All 19 choseong x 21 jungseong combinations (399 basic + compound syllables)
    for cho in range(19):
        for jung in range(21):
            items.add(chr(0xAC00 + (cho * 21 + jung) * 28))
    return sorted(t for t in items if not JAMO.search(t))


async def main(force):
    items = collect()
    sem = asyncio.Semaphore(5)
    made = 0

    async def one(t):
        nonlocal made
        out = OUT_DIR / f"{t}.mp3"
        if out.exists() and out.stat().st_size > 800 and not force:
            return
        async with sem:
            # Natural citation speech rate: -10% for clear, natural, distortion-free pronunciation
            await synth_citation(t, out, rate="-10%")
        made += 1

    print(f"{len(items)} items")
    await asyncio.gather(*(one(t) for t in items))
    print(f"generated {made}, total {len(list(OUT_DIR.glob('*.mp3')))}")


if __name__ == "__main__":
    asyncio.run(main("--force" in sys.argv))
