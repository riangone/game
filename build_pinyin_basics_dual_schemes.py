#!/usr/bin/env python3
"""Build Dual-Scheme Audio Assets for Pinyin Basics:
Scheme 1: A1 (原方案 A1 - 标准紧凑版)
Scheme 2: A1-M (方案 A1-M - 适度延长版 ⭐推荐教学首选)

Generates:
- audio/pinyin-basics-a1/   (193 files, crisp & compact)
- audio/pinyin-basics-a1m/  (193 files, +35% extended, relaxed & demonstrative)
"""

import sys
import subprocess
from pathlib import Path
import asyncio
import edge_tts
import numpy as np
import parselmouth
from parselmouth.praat import call

ROOT = Path("/home/ubuntu/ws/jump-jump-game")
SRC_DIR = ROOT / "audio" / "pinyin-basics"
EXP_DIR = ROOT / "audio" / "psola-experiment"
HUMAN_DIR = ROOT / "audio" / "human-pinyin"

DIR_A1 = ROOT / "audio" / "pinyin-basics-a1"
DIR_A1M = ROOT / "audio" / "pinyin-basics-a1m"
DIR_A1.mkdir(parents=True, exist_ok=True)
DIR_A1M.mkdir(parents=True, exist_ok=True)

def trim_silence(snd: parselmouth.Sound, thresh_ratio=0.025, pad_ms=20) -> parselmouth.Sound:
    samples = snd.values[0]
    sr = snd.sampling_frequency
    thresh = np.max(np.abs(samples)) * thresh_ratio
    active = np.where(np.abs(samples) > thresh)[0]
    if len(active) == 0:
        return snd
    s_idx = max(0, active[0] - int(sr * pad_ms / 1000))
    e_idx = min(len(samples), active[-1] + int(sr * pad_ms / 1000))
    trimmed = samples[s_idx:e_idx].copy()
    
    fade_len = int(sr * 0.012)
    if len(trimmed) > fade_len * 2:
        fade_in = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, fade_len)))
        fade_out = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, fade_len)))
        trimmed[:fade_len] *= fade_in
        trimmed[-fade_len:] *= fade_out
        
    return parselmouth.Sound(trimmed, sampling_frequency=sr)

def save_sound_mp3(snd: parselmouth.Sound, out_mp3: Path, normalize=True):
    sr = snd.sampling_frequency
    samples = snd.values[0].copy()
    if normalize:
        m = np.max(np.abs(samples))
        if m > 1e-4:
            samples *= (0.891 / m)  # -1 dBFS peak
            
    # Apply fade in / fade out
    fl = int(sr * 0.010)
    if len(samples) > fl * 2:
        fi = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, fl)))
        fo = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, fl)))
        samples[:fl] *= fi
        samples[-fl:] *= fo
        
    out_snd = parselmouth.Sound(samples, sampling_frequency=sr)
    tmp_wav = out_mp3.parent / f"tmp_{out_mp3.stem}.wav"
    out_snd.save(str(tmp_wav), "WAV")
    subprocess.run(["ffmpeg", "-y", "-i", str(tmp_wav), "-b:a", "128k", str(out_mp3)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp_wav.unlink(missing_ok=True)

def stretch_sound(snd: parselmouth.Sound, factor=1.35) -> parselmouth.Sound:
    return call(snd, "Lengthen (overlap-add)", 80, 500, factor)

def make_psola_from_ref(ref_mp3: Path, carrier_mp3: Path, dur_ratio=1.0):
    ref_snd = trim_silence(parselmouth.Sound(str(ref_mp3)))
    carrier_snd = trim_silence(parselmouth.Sound(str(carrier_mp3)))
    
    pitch = call(ref_snd, "To Pitch", 0.005, 80, 500)
    f0 = pitch.selected_array['frequency']
    times = pitch.xs()
    valid = np.where(f0 > 0)[0]
    if len(valid) == 0:
        raise ValueError(f"No voiced segment in {ref_mp3}")
    f0_v = f0[valid]
    times_v = times[valid]
    tau = (times_v - times_v[0]) / (times_v[-1] - times_v[0])
    
    target_dur = max(0.40, (times_v[-1] - times_v[0]) * dur_ratio)
    factor = target_dur / carrier_snd.duration
    stretched = call(carrier_snd, "Lengthen (overlap-add)", 80, 500, factor)
    manip = call(stretched, "To Manipulation", 0.005, 80, 500)
    pt = call("Create PitchTier", "pitch", 0, stretched.duration)
    for i in range(len(tau)):
        t_tar = 0.02 + tau[i] * (stretched.duration - 0.04)
        call(pt, "Add point", t_tar, float(f0_v[i]))
    call([pt, manip], "Replace pitch tier")
    return call(manip, "Get resynthesis (overlap-add)")

def build_all():
    print("=== Step 1: Processing o, e & u tones (A1 & A1-M) ===")
    for tone in [1, 2, 3, 4]:
        f_a1 = EXP_DIR / f"edge_pure_mo_o{tone}.mp3"
        f_a1m = EXP_DIR / f"edge_pure_mo_med_o{tone}.mp3"
        
        target_a1 = DIR_A1 / f"tone_o_{tone}.mp3"
        target_a1m = DIR_A1M / f"tone_o_{tone}.mp3"
        
        target_a1.write_bytes(f_a1.read_bytes())
        target_a1m.write_bytes(f_a1m.read_bytes())
        
        if tone == 1:
            (DIR_A1 / "final_o_pure.mp3").write_bytes(f_a1.read_bytes())
            (DIR_A1M / "final_o_pure.mp3").write_bytes(f_a1m.read_bytes())

    for tone in [1, 2, 3, 4]:
        f_a1 = EXP_DIR / f"e_detremor_opt1_a1_t{tone}.mp3"
        f_a1m = EXP_DIR / f"e_detremor_opt1_a1m_t{tone}.mp3"
        
        target_a1 = DIR_A1 / f"tone_e_{tone}.mp3"
        target_a1m = DIR_A1M / f"tone_e_{tone}.mp3"
        
        target_a1.write_bytes(f_a1.read_bytes())
        target_a1m.write_bytes(f_a1m.read_bytes())
        
        if tone == 1:
            (DIR_A1 / "final_e_pure.mp3").write_bytes(f_a1.read_bytes())
            (DIR_A1M / "final_e_pure.mp3").write_bytes(f_a1m.read_bytes())

    for tone in [1, 2, 3, 4]:
        f_a1 = EXP_DIR / f"u_detremor_opt1_a1_t{tone}.mp3"
        f_a1m = EXP_DIR / f"u_detremor_opt1_a1m_t{tone}.mp3"
        
        target_a1 = DIR_A1 / f"tone_u_{tone}.mp3"
        target_a1m = DIR_A1M / f"tone_u_{tone}.mp3"
        
        target_a1.write_bytes(f_a1.read_bytes())
        target_a1m.write_bytes(f_a1m.read_bytes())
        
        if tone == 1:
            (DIR_A1 / "final_u_pure.mp3").write_bytes(f_a1.read_bytes())
            (DIR_A1M / "final_u_pure.mp3").write_bytes(f_a1m.read_bytes())
            
    print("=== Step 2: Processing core tone families (a, i, v, ma, yi, wu, shu) ===")
    tone_map = {
        "a": ("a", 1.0),
        "i": ("i", 1.0),
        "v": ("v", 1.0),
        "ma": ("ma", 1.0),
        "yi": ("i", 1.0),
        "wu": ("u", 1.0),
    }
    
    for base, (src_base, _) in tone_map.items():
        for tone in [1, 2, 3, 4]:
            cand_psola = EXP_DIR / f"psola_{src_base}{tone}.mp3"
            if not cand_psola.exists() and src_base == "v":
                cand_psola = EXP_DIR / f"psola_yu{tone}.mp3"
                
            if cand_psola.exists():
                snd = trim_silence(parselmouth.Sound(str(cand_psola)))
                out_a1 = DIR_A1 / f"tone_{base}_{tone}.mp3"
                save_sound_mp3(snd, out_a1)
                
                # A1-M: stretch 1.35x
                snd_m = stretch_sound(snd, 1.35)
                out_a1m = DIR_A1M / f"tone_{base}_{tone}.mp3"
                save_sound_mp3(snd_m, out_a1m)
            else:
                print(f"Warning: Missing psola for {base}{tone}")

    # shu tones: Scheme 2 (全音节音段修正版: shu_opt1_a1_t{tone}.mp3 & shu_opt1_a1m_t{tone}.mp3)
    for tone in [1, 2, 3, 4]:
        f_a1 = EXP_DIR / f"shu_opt1_a1_t{tone}.mp3"
        f_a1m = EXP_DIR / f"shu_opt1_a1m_t{tone}.mp3"
        if f_a1.exists() and f_a1m.exists():
            (DIR_A1 / f"tone_shu_{tone}.mp3").write_bytes(f_a1.read_bytes())
            (DIR_A1M / f"tone_shu_{tone}.mp3").write_bytes(f_a1m.read_bytes())
        else:
            ref_f = HUMAN_DIR / f"shu{tone}.mp3"
            carrier_f = SRC_DIR / f"tone_shu_{tone}.mp3"
            snd_a1 = make_psola_from_ref(ref_f, carrier_f, dur_ratio=1.0)
            save_sound_mp3(snd_a1, DIR_A1 / f"tone_shu_{tone}.mp3")
            snd_a1m = make_psola_from_ref(ref_f, carrier_f, dur_ratio=1.35)
            save_sound_mp3(snd_a1m, DIR_A1M / f"tone_shu_{tone}.mp3")

    # ma0 (neutral tone)
    ma0_src = SRC_DIR / "tone_ma_0.mp3"
    if ma0_src.exists():
        snd_ma0 = trim_silence(parselmouth.Sound(str(ma0_src)))
        save_sound_mp3(snd_ma0, DIR_A1 / "tone_ma_0.mp3")
        snd_ma0_m = stretch_sound(snd_ma0, 1.25)
        save_sound_mp3(snd_ma0_m, DIR_A1M / "tone_ma_0.mp3")

    print("=== Step 2.5: Processing Pinyin Full Table (63 items, unified Tone 1 & pure neural pipeline) ===")
    from generate_full_table_unified import TABLE_SPECS, cut_consonant, cut_er
    full_table_keys = {f"{fname}.mp3" for fname, text, py, cat, mode in TABLE_SPECS}
    
    for fname, text, py, cat, mode in TABLE_SPECS:
        out_a1 = DIR_A1 / f"{fname}.mp3"
        out_a1m = DIR_A1M / f"{fname}.mp3"
        out_fb = SRC_DIR / f"{fname}.mp3"
        
        raw_f = ROOT / "audio" / "tmp_full_table_build" / f"{fname}.mp3"
        raw_f.parent.mkdir(parents=True, exist_ok=True)
        if not raw_f.exists():
            comm = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="-15%")
            asyncio.run(comm.save(str(raw_f)))
        snd_raw = parselmouth.Sound(str(raw_f))
        
        if mode == "cut":
            snd_a1 = cut_consonant(snd_raw)
        elif mode == "er_cut":
            snd_a1 = cut_er(snd_raw)
        else:
            snd_a1 = trim_silence(snd_raw)
            
        snd_a1m = stretch_sound(snd_a1, factor=1.35)
        
        save_sound_mp3(snd_a1, out_a1)
        save_sound_mp3(snd_a1m, out_a1m)
        out_fb.write_bytes(out_a1m.read_bytes())

    print("=== Step 3: Processing all other assets (chars, syls, chants, words) ===")
    all_src_files = list(SRC_DIR.glob("*.mp3"))
    print(f"Total source files to examine: {len(all_src_files)}")
    
    for src_file in all_src_files:
        fn = src_file.name
        
        # Already handled in Step 1, 2 & 2.5
        if fn.startswith("tone_") or fn in full_table_keys:
            continue
            
        target_a1 = DIR_A1 / fn
        target_a1m = DIR_A1M / fn
        
        # Chants (long poems / songs): preserve authentic singing/chanting tempo
        if fn.startswith("chant_"):
            target_a1.write_bytes(src_file.read_bytes())
            target_a1m.write_bytes(src_file.read_bytes())
            continue
            
        # Single sound items: trim trailing silence for A1, extend 1.35x for A1-M
        try:
            snd = parselmouth.Sound(str(src_file))
            snd_trimmed = trim_silence(snd)
            save_sound_mp3(snd_trimmed, target_a1)
            
            snd_extended = stretch_sound(snd_trimmed, factor=1.35)
            save_sound_mp3(snd_extended, target_a1m)
        except Exception as e:
            print(f"Fallback for {fn}: {e}")
            target_a1.write_bytes(src_file.read_bytes())
            target_a1m.write_bytes(src_file.read_bytes())

    # Sync optimized o, e, u, shu files to fallback SRC_DIR as well
    for tone in [1, 2, 3, 4]:
        (SRC_DIR / f"tone_u_{tone}.mp3").write_bytes((DIR_A1M / f"tone_u_{tone}.mp3").read_bytes())
        (SRC_DIR / f"tone_shu_{tone}.mp3").write_bytes((DIR_A1M / f"tone_shu_{tone}.mp3").read_bytes())
    (SRC_DIR / "final_u_pure.mp3").write_bytes((DIR_A1M / "final_u_pure.mp3").read_bytes())

    # Check totals
    cnt_a1 = len(list(DIR_A1.glob("*.mp3")))
    cnt_a1m = len(list(DIR_A1M.glob("*.mp3")))
    print(f"\nCompleted! Generated {cnt_a1} files in A1 and {cnt_a1m} files in A1-M.")

if __name__ == "__main__":
    build_all()
