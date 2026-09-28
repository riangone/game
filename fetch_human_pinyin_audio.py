#!/usr/bin/env python3
"""Fetch real human-recorded pinyin syllable audio to replace the weakest
spot in the TTS pipeline: isolated single-syllable tone pronunciation
(especially tone 3, which neural TTS systematically under-articulates
because their training data is dominated by connected speech, where tone 3
is almost always the reduced "half third tone" 211, not the textbook 214
citation form).

Source: davinfifield/mp3-chinese-pinyin-sound (GitHub), Unlicense
(public domain) — verified 2026 via `git/trees` API (1632 real mp3 files)
and ffprobe on samples (128kbps/44.1kHz mono, ID3 date=2006, i.e. an old
real-voice recording set, predating any neural TTS). See README discussion
in project chat history for the rejected alternative
(zispace/hanyu-pinyin-audio — no LICENSE, self-describes source audio as
scraped from commercial teaching sites, "仅供参考" — not safe to redistribute).

This script pulls ONLY the ~28 files actually needed by pinyin-abc.html and
pinyin-basics.html's tone-family drills, not the full 1632-file repo, to
avoid bloating this project with unused assets.

Output: audio/human-pinyin/<canonical-syllable><tone>.mp3
  e.g. a1.mp3, e3.mp3, ma3.mp3, yi3.mp3, wu3.mp3, yu3.mp3, shu3.mp3

Both game pages resolve their own internal key naming (pinyin-abc.html
uses bare vowel letters i/u/ü as tone-family keys; pinyin-basics.html
uses tone_<base>_<n>) down to these same canonical syllable filenames at
playback time (see HUMAN_ALIAS in pinyin-abc.html and humanKeyFor() in
pinyin-basics.html), so there is exactly ONE copy of each audio file on
disk — no per-page duplication, no drift.

NOT fetched (and why):
- o1..o4: "o" alone is not a valid isolated Mandarin syllable (o only
  occurs after b/p/m/f as bo/po/mo/fo) — the source repo has no such
  files, correctly. These 4 keys stay on the existing TTS fallback.
- tone_ma_0 (吗, neutral tone): the source repo's ma5.mp3 (a plausible
  neutral-tone slot) was verified byte-IDENTICAL (md5) to its own ma1.mp3
  — i.e. not a real distinct recording, just a filler/duplicate. Silently
  using it would swap a bad TTS neutral tone for a wrong tone-1 recording,
  which is worse. Left on TTS fallback.

Usage: python3 fetch_human_pinyin_audio.py
"""
import hashlib
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "human-pinyin"

BASE_URL = "https://raw.githubusercontent.com/davinfifield/mp3-chinese-pinyin-sound/master/mp3/{}.mp3"

# canonical output filename -> source repo filename (usually identical;
# differs only for the bare-vowel families that this project maps onto
# their zero-initial syllable, e.g. game key "i3" -> canonical "yi3" ->
# source "yi3.mp3")
TARGETS = {}
for tone in "1234":
    TARGETS[f"a{tone}"] = f"a{tone}"
    TARGETS[f"e{tone}"] = f"e{tone}"
    TARGETS[f"ma{tone}"] = f"ma{tone}"
    TARGETS[f"yi{tone}"] = f"yi{tone}"
    TARGETS[f"wu{tone}"] = f"wu{tone}"
    TARGETS[f"yu{tone}"] = f"yu{tone}"
    TARGETS[f"shu{tone}"] = f"shu{tone}"

MIN_BYTES = 2000  # real clips observed 10KB-32KB; guard against HTML error pages / empty stubs


def fetch(name: str) -> bytes:
    url = BASE_URL.format(name)
    req = urllib.request.Request(url, headers={"User-Agent": "jump-jump-game-fetch-script"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok, failed = [], []
    seen_hashes = {}
    for out_name, src_name in sorted(TARGETS.items()):
        dest = OUT_DIR / f"{out_name}.mp3"
        try:
            data = fetch(src_name)
        except urllib.error.HTTPError as e:
            failed.append((out_name, f"HTTP {e.code}"))
            continue
        except Exception as e:  # noqa: BLE001
            failed.append((out_name, str(e)))
            continue
        if len(data) < MIN_BYTES:
            failed.append((out_name, f"too small ({len(data)} bytes)"))
            continue
        h = hashlib.md5(data).hexdigest()
        seen_hashes.setdefault(h, []).append(out_name)
        dest.write_bytes(data)
        ok.append((out_name, len(data)))
        print(f"  {out_name}.mp3  <- {src_name}.mp3  ({len(data)} bytes)")

    dupes = {h: names for h, names in seen_hashes.items() if len(names) > 1}
    print(f"\nDone: {len(ok)} fetched, {len(failed)} failed.")
    if failed:
        print("Failed:")
        for name, reason in failed:
            print(f"  {name}: {reason}")
    if dupes:
        print("WARNING: byte-identical files detected across different syllables "
              "(source repo may have duplicated content) — verify before trusting:")
        for h, names in dupes.items():
            print(f"  {names}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
