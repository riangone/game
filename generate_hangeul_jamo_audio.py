#!/usr/bin/env python3
"""Generate jamo-name audio (ㄱ→기역, ㄴ→니은, ㅏ→아 ...) for every jamo in js/hangeul_stroke_data.js.

Output: audio/ko/<jamo>.mp3  (e.g. audio/ko/ㄱ.mp3 says "기역")
Shared by hangeul.html / korean.html / hangul.html (playHangeulSound) and
playJamoAudio() in js/hangeul_stroke_data.js (hangugeo*.html part cards + stroke modal).
The previous audio/ko/<jamo>.mp3 were ~0.3s of voiced audio — far too short for a 2-syllable name.
Uses tools_ko.ko_tts.synth_citation (slow citation rate) so the 2-syllable names are fully articulated.

  python3 generate_hangeul_jamo_audio.py           # only missing files
  python3 generate_hangeul_jamo_audio.py --force   # regenerate all
"""
import asyncio
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from tools_ko.ko_tts import synth_citation, voiced_duration  # noqa: E402

OUT_DIR = ROOT / "audio" / "ko"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# 复合收音 (겹받침) — not in HANGEUL_STROKE_META, but clickable in hangeul.html
EXTRA_NAMES = {
    "ㄳ": "기역시옷", "ㄵ": "니은지읒", "ㄶ": "니은히읗", "ㄺ": "리을기역", "ㄻ": "리을미음",
    "ㄼ": "리을비읍", "ㄽ": "리을시옷", "ㄾ": "리을티읕", "ㄿ": "리을피읖", "ㅀ": "리을히읗",
    "ㅄ": "비읍시옷",
}


def load_jamo_names():
    src = (ROOT / "js" / "hangeul_stroke_data.js").read_text(encoding="utf-8")
    m = re.search(r"const HANGEUL_STROKE_META = (\{.*?\n\});", src, re.S)
    meta = json.loads(m.group(1))
    names = {jamo: v["name"].split("/")[0].strip() for jamo, v in meta.items()}
    names.update(EXTRA_NAMES)
    names["ㄱ"] = "기윽"  # Explicitly pronounce 기윽 as requested by user
    return names


async def main(force):
    names = load_jamo_names()
    sem = asyncio.Semaphore(4)

    async def one(jamo, name):
        out = OUT_DIR / f"{jamo}.mp3"
        if out.exists() and out.stat().st_size > 800 and not force:
            return
        async with sem:
            await synth_citation(name, out)
        print(f"  {jamo} -> {name:5s} {out.name}  voiced={voiced_duration(out, '-45dB'):.2f}s")

    print(f"Synthesizing {len(names)} jamo names...")
    await asyncio.gather(*(one(j, n) for j, n in names.items()))
    print("done:", len(names), "jamo")


if __name__ == "__main__":
    asyncio.run(main("--force" in sys.argv))
