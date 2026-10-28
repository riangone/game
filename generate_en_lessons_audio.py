#!/usr/bin/env python3
"""
Generate neural-TTS MP3 audio for English Micro-Narrative lessons.
Uses Microsoft Neural voices via edge-tts:
  - Female voice: en-US-JennyNeural
  - Male voice: en-US-GuyNeural
Generates:
  1. Chunk audio: audio/en_chunks/{chunk_id}.mp3
  2. Dialogue sentence audio: audio/en_dialogues/{dialogue_id}.mp3
"""
import asyncio
import json
import re
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "en-lessons-data.json"
CHUNKS_DIR = ROOT / "audio" / "en_chunks"
DIALOGUES_DIR = ROOT / "audio" / "en_dialogues"
VOCAB_DIR = ROOT / "audio" / "en_vocab"

CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
DIALOGUES_DIR.mkdir(parents=True, exist_ok=True)
VOCAB_DIR.mkdir(parents=True, exist_ok=True)

VOICE_FEMALE = "en-US-JennyNeural"
VOICE_MALE = "en-US-GuyNeural"
RATE_NORMAL = "+0%"
RATE_SLOW = "-12%"

def load_lessons():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

async def synthesize(text: str, voice: str, rate: str, out_path: Path):
    if not text.strip():
        return
    if out_path.exists() and out_path.stat().st_size > 0:
        return
    communicator = edge_tts.Communicate(text, voice, rate=rate)
    await communicator.save(str(out_path))
    print(f"  [OK] {out_path.name}: {text}")

async def main(max_lessons=None):
    lessons = load_lessons()
    if max_lessons:
        lessons = lessons[:max_lessons]
    
    print(f"Generating neural TTS for {len(lessons)} English lessons...")
    
    for lesson in lessons:
        lid = lesson["id"]
        print(f"\nProcessing {lid}: {lesson['title']} ({lesson['titleZh']})")
        
        # 1. Synthesize chunks
        for chunk in lesson.get("chunks", []):
            cid = chunk["id"]
            clean_text = chunk["text"].replace("...", "")
            out_file = CHUNKS_DIR / f"{cid}.mp3"
            await synthesize(clean_text, VOICE_FEMALE, RATE_NORMAL, out_file)

        # 2. Synthesize vocabulary
        for vocab in lesson.get("vocabulary", []):
            vid = vocab["id"]
            out_file = VOCAB_DIR / f"{vid}.mp3"
            await synthesize(vocab["word"], VOICE_FEMALE, RATE_NORMAL, out_file)
            
        # 3. Synthesize dialogues
        for diag in lesson.get("dialogue", []):
            did = diag["id"]
            # Speaker A uses Guy/Jenny, Speaker B uses alternating voice
            voice = VOICE_MALE if diag.get("speaker") == "A" else VOICE_FEMALE
            out_file = DIALOGUES_DIR / f"{did}.mp3"
            await synthesize(diag["en"], voice, RATE_NORMAL, out_file)

    print("\nAudio generation complete!")

if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    asyncio.run(main(limit))
