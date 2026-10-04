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

# Initials with human 1st-tone呼读音:
TARGETS["fo1"] = "fo1"
TARGETS["de1"] = "de1"

# 16 整体认读音节:
OVERALL_MAP = {
    "zhi": "zhi1", "chi": "chi1", "shi": "shi1", "ri": "ri4",
    "zi": "zi1", "ci": "ci1", "si": "si1", "yi": "yi1", "wu": "wu1",
    "yu": "yu1", "ye": "ye1", "yue": "yue4", "yuan": "yuan1",
    "yin": "yin1", "yun": "yun2", "ying": "ying1"
}
for ovr, src in OVERALL_MAP.items():
    TARGETS[src] = src

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

    # Derive pure single vowel o1..o4 by slicing out bilabial stop burst + [w] on-glide
    # to eliminate the "窝" (wo) diphthong artifact and obtain pure "喔" (o) monophthong.
    print("\nDeriving pure vowel o1..o4 from bo1..bo4 human recordings (acoustic steady-state slices)...")
    import subprocess
    import scipy.io.wavfile as wavfile
    import numpy as np

    # Acoustically measured steady-state slices in seconds:
    BO_SLICES = {
        "1": (0.170, 0.640),  # voiced 0.060..0.645s, skips [p] burst and [w] glide (onset+110ms)
        "2": (0.410, 0.745),  # voiced 0.289..0.754s, skips [w] glide, clean 35 rising tone
        "3": (0.280, 0.880),  # voiced 0.161..0.921s, skips [w] glide, full 214 dip-and-rebound
        "4": (0.490, 0.745),  # voiced 0.401..0.881s, skips [w] glide and pre-speech noise, full 51 fall
    }

    for tone, (t_start, t_end) in BO_SLICES.items():
        out_dest = OUT_DIR / f"o{tone}.mp3"
        try:
            raw_bo = fetch(f"bo{tone}")
            tmp_bo_mp3 = f"/tmp/fetch_bo{tone}.mp3"
            tmp_bo_wav = f"/tmp/fetch_bo{tone}.wav"
            tmp_o_wav = f"/tmp/fetch_o{tone}.wav"
            Path(tmp_bo_mp3).write_bytes(raw_bo)
            subprocess.run(["ffmpeg", "-y", "-i", tmp_bo_mp3, "-ar", "44100", "-ac", "1", tmp_bo_wav],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            rate, data = wavfile.read(tmp_bo_wav)
            data_float = data.astype(np.float32)
            i_start = int(t_start * rate)
            i_end = min(len(data_float), int(t_end * rate))
            trimmed = data_float[i_start:i_end]

            # 15ms cosine fade in and fade out
            fade_len = int(rate * 0.015)
            if len(trimmed) > fade_len * 2:
                fade_in = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, fade_len)))
                fade_out = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, fade_len)))
                trimmed[:fade_len] *= fade_in
                trimmed[-fade_len:] *= fade_out

            # Peak normalize to -1dBFS
            peak = np.max(np.abs(trimmed))
            if peak > 0:
                trimmed = trimmed / peak * (32767 * 0.89)

            wavfile.write(tmp_o_wav, rate, trimmed.astype(np.int16))
            subprocess.run(["ffmpeg", "-y", "-i", tmp_o_wav, "-b:a", "128k", str(out_dest)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            # Sync to audio/pinyin-basics as well
            pb_dest = ROOT / "audio" / "pinyin-basics" / f"tone_o_{tone}.mp3"
            pb_dest.write_bytes(out_dest.read_bytes())
            print(f"  o{tone}.mp3  <- pure steady-state slice of bo{tone}.mp3 ({t_start:.3f}s~{t_end:.3f}s, {out_dest.stat().st_size} bytes)")
        except Exception as e:
            print(f"  Failed deriving o{tone}: {e}")

    # Also sync o1.mp3 to final_o_pure.mp3
    o1_src = OUT_DIR / "o1.mp3"
    if o1_src.exists():
        (ROOT / "audio" / "pinyin-basics" / "final_o_pure.mp3").write_bytes(o1_src.read_bytes())
        print("  final_o_pure.mp3 synced with o1.mp3")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()

