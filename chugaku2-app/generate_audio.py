#!/usr/bin/env python3
"""Generate high-fidelity neural MP3 audio for chugaku2-app using Edge-TTS.

Voices:
- Japanese: ja-JP-NanamiNeural
- English: en-US-JennyNeural
"""
import asyncio
import json
import re
from pathlib import Path
import edge_tts

APP_ROOT = Path(__file__).resolve().parent
DATA_DIR = APP_ROOT / "data" / "grade2"
AUDIO_ROOT = APP_ROOT / "audio"
AUDIO_ROOT.mkdir(parents=True, exist_ok=True)

JA_VOICE = "ja-JP-NanamiNeural"
EN_VOICE = "en-US-JennyNeural"
JA_RATE = "+0%"
EN_RATE = "-4%"

def latex_to_speech_ja(text: str) -> str:
    t = text
    # Unwrap \text{...}
    t = re.sub(r'\\text\{([^{}]+)\}', r'\1', t)
    # Fractions \frac{A}{B} -> B分のA
    while r'\frac' in t:
        new_t = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'\2分の\1', t)
        if new_t == t:
            break
        t = new_t

    # Chemical reactions
    t = t.replace(r'\text{', '').replace('}', '')
    t = t.replace(r'\to', ' 矢印 ')
    t = t.replace(r'\equiv', ' 合同 ')
    t = t.replace(r'\times', ' かける ')
    t = t.replace(r'\triangle', '三角形')
    t = t.replace(r'\angle', '角')
    t = t.replace(r'\pm', 'プラスマイナス')
    for a, b in [(r'\leqq', ' 以下 '), (r'\geqq', ' 以上 '), (r'\leq', ' 以下 '), (r'\geq', ' 以上 '),
                 (r'\Omega', 'オーム'), (r'\cdot', ' かける '), (r'\div', ' わる '), (r'\,', ' '), (r'\ ', ' ')]:
        t = t.replace(a, b)
    t = t.replace(r'^\circ', '度').replace(r'\parallel', ' 平行 ').replace(r'\perp', ' 垂直 ')
    t = re.sub(r'\^2', 'の2乗', t)
    t = re.sub(r'_(\w)', r'\1', t)
    t = re.sub(r'\\[a-zA-Z]+', '', t)  # 残りのコマンドは除去
    t = re.sub(r'([a-zA-Z0-9])\s*>\s*([a-zA-Z0-9])', r'\1 大なり \2', t)
    t = re.sub(r'([a-zA-Z0-9])\s*<\s*([a-zA-Z0-9])', r'\1 小なり \2', t)
    t = t.replace('$', '')
    # Strip bullet circles like ①, ②
    # Clean whitespace
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def is_japanese(text: str) -> bool:
    return bool(re.search(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]', text))

async def synthesize(text: str, voice: str, rate: str, out_path: Path):
    if out_path.exists() and out_path.stat().st_size > 1000:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = edge_tts.Communicate(text, voice, rate=rate)
    await c.save(str(out_path))

async def main():
    json_files = sorted(DATA_DIR.glob("**/*.json"))
    tasks = []
    
    for jf in json_files:
        data = json.loads(jf.read_text(encoding="utf-8"))
        unit_id = data["unitId"]
        subject = data["subject"]
        unit_audio_dir = AUDIO_ROOT / unit_id
        unit_audio_dir.mkdir(parents=True, exist_ok=True)

        print(f"Processing unit: {unit_id} ({subject})")

        # 1. Story sentences
        for s in data.get("story", []):
            sid = s["id"]
            raw_text = s["text"]
            out_file = unit_audio_dir / f"{sid}.mp3"
            if subject == "english":
                voice = EN_VOICE
                rate = EN_RATE
                text = raw_text
            else:
                voice = JA_VOICE
                rate = JA_RATE
                text = latex_to_speech_ja(raw_text)

            print(f"  [STORY {sid}] {text[:40]}... -> {out_file.name}")
            tasks.append((text, voice, rate, out_file))

        # 2. Flashcards
        for fc in data.get("flashcards", []):
            fcid = fc["id"]
            raw_term = fc["term"]
            out_file = unit_audio_dir / f"{fcid}.mp3"
            if is_japanese(raw_term):
                voice = JA_VOICE
                rate = JA_RATE
                text = latex_to_speech_ja(raw_term)
            elif subject == "english":
                voice = EN_VOICE
                rate = EN_RATE
                text = raw_term
            else:
                voice = JA_VOICE
                rate = JA_RATE
                text = latex_to_speech_ja(raw_term)

            print(f"  [FC {fcid}] {text[:40]}... -> {out_file.name}")
            tasks.append((text, voice, rate, out_file))

    print(f"\nStarting generation of {len(tasks)} audio files with Edge-TTS...")
    # Run tasks with concurrency limit
    semaphore = asyncio.Semaphore(5)

    async def sem_task(t, v, r, p):
        async with semaphore:
            await synthesize(t, v, r, p)

    await asyncio.gather(*(sem_task(t, v, r, p) for t, v, r, p in tasks))
    print("Done! All audio files generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
