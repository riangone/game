#!/usr/bin/env python3
"""Generate real neural-TTS MP3 audio for the English and Japanese story
translations across all four story-reading games, mirroring the exact same
architecture already used for Chinese narration (edge-tts, Microsoft neural
voices, free, no API key, pre-generated and cached as static MP3 files).

For each game, this script:
  1. Parses the `const STORY = [ ... ];` array directly out of the .html file
     with a regex (so it can never drift from the live game data).
  2. Generates one MP3 per sentence for the English (`en`) field into
     audio/<game>_en/<id>.mp3
  3. Generates one MP3 per sentence for the Japanese (`jp`) field into
     audio/<game>_ja/<id>.mp3

Games covered:
  gugong.html            -> audio/gugong_en/  audio/gugong_ja/
  yiheyuan.html          -> audio/yiheyuan_en/ audio/yiheyuan_ja/
  hanjia-jianwen.html    -> audio/hanjia_en/   audio/hanjia_ja/
  luotuo-he-yang.html    -> audio/luotuo_en/   audio/luotuo_ja/
"""
import asyncio
import re
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent

EN_VOICE = "en-US-JennyNeural"
JA_VOICE = "ja-JP-NanamiNeural"
EN_RATE = "-8%"
JA_RATE = "-10%"

GAMES = [
    ("gugong.html", "gugong"),
    ("yiheyuan.html", "yiheyuan"),
    ("hanjia-jianwen.html", "hanjia"),
    ("luotuo-he-yang.html", "luotuo"),
]

# Matches one STORY entry object and captures id, en, jp (jp optional/absent-safe)
ENTRY_RE = re.compile(
    r'\{id:"(?P<id>[^"]+)".*?en:"(?P<en>(?:[^"\\]|\\.)*)"'
    r'(?:,\s*jp:"(?P<jp>(?:[^"\\]|\\.)*)")?\s*\}',
    re.DOTALL,
)


def unescape(s):
    if s is None:
        return ""
    return s.replace('\\"', '"').replace("\\'", "'").replace("\\n", " ")


def extract_story(html_path):
    text = html_path.read_text(encoding="utf-8")
    m = re.search(r"const STORY\s*=\s*\[(.*?)\n\];", text, re.DOTALL)
    if not m:
        raise RuntimeError(f"Could not locate STORY array in {html_path}")
    body = m.group(1)
    entries = []
    for em in ENTRY_RE.finditer(body):
        entries.append(
            {
                "id": em.group("id"),
                "en": unescape(em.group("en")),
                "jp": unescape(em.group("jp")),
            }
        )
    return entries


async def synth(text, voice, rate, out_path):
    if not text.strip():
        return
    if out_path.exists() and out_path.stat().st_size > 0:
        return
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(out_path))
    print(f"  OK  {out_path.relative_to(ROOT)}")


async def process_game(html_name, audio_slug):
    html_path = ROOT / html_name
    entries = extract_story(html_path)
    en_dir = ROOT / "audio" / f"{audio_slug}_en"
    ja_dir = ROOT / "audio" / f"{audio_slug}_ja"
    en_dir.mkdir(parents=True, exist_ok=True)
    ja_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== {html_name}: {len(entries)} sentences ===")
    for e in entries:
        await synth(e["en"], EN_VOICE, EN_RATE, en_dir / f"{e['id']}.mp3")
        if e["jp"]:
            await synth(e["jp"], JA_VOICE, JA_RATE, ja_dir / f"{e['id']}.mp3")
        else:
            print(f"  SKIP {e['id']} (no jp text)")


async def main():
    for html_name, audio_slug in GAMES:
        await process_game(html_name, audio_slug)


if __name__ == "__main__":
    asyncio.run(main())
