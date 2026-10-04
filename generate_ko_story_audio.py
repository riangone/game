#!/usr/bin/env python3
"""Generate real neural-TTS MP3 audio for the Korean story translations
across all lesson-reading games, mirroring the exact same architecture
already used for English/Japanese narration (edge-tts, Microsoft neural
voices, free, no API key, pre-generated and cached as static MP3 files).

For each game, this script:
  1. Parses the `const STORY = [ ... ];` array directly out of the .html file
     with a regex (so it can never drift from the live game data).
  2. Generates one MP3 per sentence for the Korean (`ko`) field into
     audio/<game>_ko/<id>.mp3

Only processes games whose STORY array already has a `ko` field (added by
tools_ko/inject.py) — others are skipped with a notice.
"""
import asyncio
import re
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent

KO_VOICE = "ko-KR-SunHiNeural"
KO_RATE = "-8%"

GAMES = [
    ("gugong.html", "gugong"),
    ("yiheyuan.html", "yiheyuan"),
    ("hanjia-jianwen.html", "hanjia"),
    ("luotuo-he-yang.html", "luotuo"),
    ("xiaoma-guohe.html", "xiaoma"),
    ("houzi-lao-yueliang.html", "houzi"),
    ("sima-guang.html", "sima"),
    ("shu-xingxing.html", "xingxing"),
    ("gushi-er-shou.html", "gushi"),
    ("diqiu-qingjiegong.html", "diqiu"),
    ("daziran-yuyan.html", "daziran"),
    ("tanyue.html", "tanyue"),
]

ENTRY_RE = re.compile(
    r'\{id:"(?P<id>[^"]+)".*?(?:ko:"(?P<ko>(?:[^"\\]|\\.)*)")?\s*\}',
    re.DOTALL,
)
# More robust: find id and ko independently within each object span.
OBJ_RE = re.compile(r'\{(?:[^{}])*\}', re.DOTALL)
ID_RE = re.compile(r'id:\s*"(?P<id>[^"]+)"')
KO_RE = re.compile(r'ko:\s*"(?P<ko>(?:[^"\\]|\\.)*)"')


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
    for om in OBJ_RE.finditer(body):
        ot = om.group(0)
        id_m = ID_RE.search(ot)
        ko_m = KO_RE.search(ot)
        if not id_m:
            continue
        entries.append({
            "id": id_m.group("id"),
            "ko": unescape(ko_m.group("ko")) if ko_m else "",
        })
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
    ko_dir = ROOT / "audio" / f"{audio_slug}_ko"
    ko_dir.mkdir(parents=True, exist_ok=True)

    has_ko = any(e["ko"] for e in entries)
    if not has_ko:
        print(f"\n=== {html_name}: no `ko` field yet, skipping ===")
        return

    print(f"\n=== {html_name}: {len(entries)} sentences ===")
    for e in entries:
        if e["ko"]:
            await synth(e["ko"], KO_VOICE, KO_RATE, ko_dir / f"{e['id']}.mp3")
        else:
            print(f"  SKIP {e['id']} (no ko text)")


async def main():
    for html_name, audio_slug in GAMES:
        await process_game(html_name, audio_slug)


if __name__ == "__main__":
    asyncio.run(main())
