"""Korean citation-form TTS helper (shared by generate_hangugeo*_audio.py / generate_hangeul_jamo_audio.py).

Problem: at the lesson rate (-5%) edge-tts squeezes an isolated syllable / jamo name into
~0.25-0.45s of voiced audio (e.g. "기역" 0.44s, "국" 0.24s), so 받침 and the second syllable get
swallowed. Measured: a carrier phrase ("X. X. X.") does NOT lengthen it; only a slower rate does
(-50%: "기역" 0.83s, "국" 0.45s). So: synthesize alone at CITATION_RATE, trim leading/trailing
silence, add a small pad on both sides.
"""
import asyncio
import subprocess
import tempfile
from pathlib import Path

import edge_tts

KO_VOICE = "ko-KR-SunHiNeural"
CITATION_RATE = "-10%"
_TRIM = ("silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.01,"
         "areverse,silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.01,"
         "areverse,adelay=15:all=1,apad=pad_dur=0.06,loudnorm=I=-16:TP=-1.5:LRA=7")


async def synth_citation(text, out_path, voice=KO_VOICE, rate=CITATION_RATE, retries=3):
    """Write a slow, clear citation-form clip of `text` (syllable / jamo name / short word)."""
    out_path = Path(out_path)
    last_err = None
    for _ in range(retries):
        try:
            with tempfile.TemporaryDirectory() as td:
                raw = Path(td) / "raw.mp3"
                wav = Path(td) / "trimmed.wav"
                await edge_tts.Communicate(text, voice, rate=rate).save(str(raw))
                # Step 1: trim silence into intermediate wav (avoids libmp3lame padding bug with areverse)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af", _TRIM,
                                "-ac", "1", "-ar", "24000", str(wav)], check=True)
                # Step 2: encode clean wav to mp3
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
                                "-b:a", "48k", str(out_path)], check=True)
                if out_path.stat().st_size < 800:
                    raise RuntimeError(f"output too small for {text!r}")
                return out_path
        except Exception as e:  # network hiccup -> retry
            last_err = e
            await asyncio.sleep(1)
    raise RuntimeError(f"synth_citation failed for {text!r}: {last_err}")


def voiced_duration(path, threshold="-40dB"):
    """Seconds of non-silent audio (for QA)."""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                          f"silencedetect=n={threshold}:d=0.08", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                  "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout)
    silent = sum(float(l.split("silence_duration:")[1]) for l in out.splitlines() if "silence_duration:" in l)
    return total - silent
