#!/usr/bin/env python3
"""
Generate 100% acoustically accurate Mandarin Chinese Pinyin tones
using Microsoft Edge-TTS + Praat-Parselmouth (PSOLA acoustic pitch tier sculpting).

This eliminates:
1. Sentence-final intonation drop (which caused Tone 1 to fall like Tone 4)
2. Homograph character collapse (e.g. ō/ó/ǒ/ò all mapping to 喔)
3. Raw pinyin hallucination in TTS
4. Tone sandhi ambiguity in isolated syllables
"""

import asyncio
import os
import sys
import subprocess
from pathlib import Path
import numpy as np
import parselmouth
from parselmouth.praat import call
import edge_tts

ZH_DIR = Path("/home/ubuntu/ws/jump-jump-game/audio/zh")
THEATER_DIR = Path("/home/ubuntu/ws/jump-jump-game/audio/theater")
TEMP_DIR = Path("/tmp/tone_pipeline")

ZH_DIR.mkdir(parents=True, exist_ok=True)
THEATER_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"

# Base phonemes to synthesize with Xiaoxiao
BASE_PHONEMES = {
    'a': '阿',
    'o': '喔',
    'e': '婀',
    'i': '衣',
    'u': '乌',
    'ü': '迂',
    'ba': '八',
    'ma': '妈',
    'da': '搭'
}

# 5-Degree Scale (五度值) F0 parameters for XiaoxiaoNeural female voice (average F0 ~260Hz):
# Tone 1 (55): 310 Hz -> 310 Hz (high flat)
# Tone 2 (35): 220 Hz -> 320 Hz (rising)
# Tone 3 (214): 230 Hz -> 170 Hz (at 45%) -> 260 Hz (dipping)
# Tone 4 (51): 335 Hz -> 185 Hz (falling)
TONE_CURVES = {
    1: [(0.0, 310.0), (1.0, 310.0)],
    2: [(0.0, 220.0), (1.0, 320.0)],
    3: [(0.0, 240.0), (0.45, 170.0), (1.0, 250.0)],
    4: [(0.0, 335.0), (1.0, 185.0)]
}

VOWEL_TONE_NAMES = {
    'a': {1: 'ā', 2: 'á', 3: 'ǎ', 4: 'à'},
    'o': {1: 'ō', 2: 'ó', 3: 'ǒ', 4: 'ò'},
    'e': {1: 'ē', 2: 'é', 3: 'ě', 4: 'è'},
    'i': {1: 'ī', 2: 'í', 3: 'ǐ', 4: 'ì'},
    'u': {1: 'ū', 2: 'ú', 3: 'ǔ', 4: 'ù'},
    'ü': {1: 'ǖ', 2: 'ǘ', 3: 'ǚ', 4: 'ǜ'},
    'ba': {1: 'bā', 2: 'bá', 3: 'bǎ', 4: 'bà'},
    'ma': {1: 'mā', 2: 'má', 3: 'mǎ', 4: 'mà'},
    'da': {1: 'dā', 2: 'dá', 3: 'dǎ', 4: 'dà'},
}

THEATER_PREFIX = {
    'a': 'tone_a',
    'o': 'tone_o',
    'e': 'tone_e',
    'i': 'tone_i',
    'u': 'tone_u',
    'ü': 'tone_v',
    'ba': 'tone_ba',
    'ma': 'tone_ma',
}

async def fetch_base_audio(key, text):
    raw_mp3 = TEMP_DIR / f"base_{key}.mp3"
    raw_wav = TEMP_DIR / f"base_{key}.wav"
    c = edge_tts.Communicate(text, VOICE)
    await c.save(str(raw_mp3))
    subprocess.run(["ffmpeg", "-y", "-i", str(raw_mp3), "-ar", "16000", "-ac", "1", str(raw_wav)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return raw_wav

def sculpt_tone(input_wav, output_mp3, tone_num):
    orig_sound = parselmouth.Sound(str(input_wav))
    orig_pitch = orig_sound.to_pitch()
    
    # Detect voiced frames precisely
    n_frames = orig_pitch.get_number_of_frames()
    voiced_times = [
        orig_pitch.get_time_from_frame_number(i) 
        for i in range(1, n_frames + 1) 
        if not np.isnan(orig_pitch.get_value_in_frame(i))
    ]
    
    if not voiced_times:
        sound = orig_sound
    else:
        t_start = max(0.0, voiced_times[0])
        t_end = min(orig_sound.get_total_duration(), voiced_times[-1])
        sound = call(orig_sound, "Extract part", t_start, t_end, "rectangular", 1, "no")
        
    duration = sound.get_total_duration()
    manipulation = call(sound, "To Manipulation", 0.01, 75.0, 500.0)
    pitch_tier = call(manipulation, "Extract pitch tier")
    call(pitch_tier, "Remove points between", 0.0, duration)
    
    curve = TONE_CURVES[tone_num]
    for frac, f0 in curve:
        t_point = frac * duration
        call(pitch_tier, "Add point", t_point, f0)
        
    call([manipulation, pitch_tier], "Replace pitch tier")
    resynthesized = call(manipulation, "Get resynthesis (overlap-add)")
    
    tmp_wav = TEMP_DIR / "tmp_sculpt.wav"
    resynthesized.save(str(tmp_wav), "WAV")
    
    # Convert to MP3 with gentle 10ms fades
    total_dur = resynthesized.get_total_duration()
    subprocess.run([
        "ffmpeg", "-y", "-i", str(tmp_wav), 
        "-af", f"afade=t=in:ss=0:d=0.01,afade=t=out:st={max(0.0, total_dur - 0.02)}:d=0.02",
        "-b:a", "64k", str(output_mp3)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

async def main():
    print("=== Generating 100% Accurate Mandarin Pinyin Tones ===")
    
    for key, text in BASE_PHONEMES.items():
        print(f"\nProcessing base phoneme '{key}' ({text})...")
        base_wav = await fetch_base_audio(key, text)
        
        for tone in [1, 2, 3, 4]:
            pinyin_sym = VOWEL_TONE_NAMES[key][tone]
            
            # 1. Output to audio/zh/ (e.g. audio/zh/ā.mp3)
            zh_mp3 = ZH_DIR / f"{pinyin_sym}.mp3"
            sculpt_tone(base_wav, zh_mp3, tone)
            
            # 2. Output to audio/theater/ if in theater map
            if key in THEATER_PREFIX:
                theater_name = f"{THEATER_PREFIX[key]}{tone}.mp3"
                theater_mp3 = THEATER_DIR / theater_name
                sculpt_tone(base_wav, theater_mp3, tone)
                
            print(f"  ✓ Tone {tone}: {pinyin_sym} -> {zh_mp3.name}")

    # Also handle single-sound finals that were incorrect in ZH_FINALS
    # e: 婀 (1st tone, not 鹅 2nd tone)
    # ai: 哀 (1st tone, not 爱 4th tone)
    # ao: 熬 (1st tone, not 奥 4th tone)
    # eng: 亨 (1st tone, not 哼 hēng/hng)
    # üe: 约 (1st tone)
    print("\nFixing baseline 1st-tone finals in audio/zh/...")
    fixed_finals = {
        'e': '婀',
        'ai': '哀',
        'ao': '熬',
        'eng': '亨',
        'üe': '约',
    }
    for k, text in fixed_finals.items():
        out_mp3 = ZH_DIR / f"{k}.mp3"
        c = edge_tts.Communicate(text, VOICE)
        await c.save(str(out_mp3))
        print(f"  ✓ Final '{k}': synthesized via '{text}' -> {out_mp3.name}")

    print("\nAll accurate tone files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
