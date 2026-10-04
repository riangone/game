import asyncio
import edge_tts
import parselmouth
from parselmouth.praat import call
import numpy as np
from pathlib import Path
import subprocess

OUT_DIR = Path("audio/psola-experiment/native_finals_clean")
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = Path("audio/tmp_clean_build")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# 24 Finals Perfect Recipe Table:
# (final_name, carrier_text, mode, cut_source_desc)
# mode: 'direct' or 'cut_consonant'
FINAL_RECIPES = [
    ("final_a_pure",   "八", "cut", "从'八'(bā)切除声母b，保留纯正高亢[a]"),
    ("final_o_pure",   "波", "cut", "从'波'(bō)切除声母b，保留纯正后圆唇[o]"),
    ("final_e_pure",   "哥", "cut", "从'哥'(gē)切除声母g，保留纯正后半高[ɤ]"),
    ("final_i_pure",   "衣", "direct", "直取'衣'(yī)原生一声"),
    ("final_u_pure",   "猪", "cut", "从'猪'(zhū)切除声母zh，保留纯正圆唇[u]"),
    ("final_v_pure",   "居", "cut", "从'居'(jū)切除声母j，保留纯正舌面元音[y]"),
    ("final_ai_pure",  "猜", "cut", "从'猜'(cāi)切除声母c，保留纯正[ai]"),
    ("final_ei_pure",  "杯", "cut", "从'杯'(bēi)切除声母b，保留纯正[ei]"),
    ("final_ui_pure",  "威", "direct", "直取'威'(wēi)原生一声"),
    ("final_ao_pure",  "高", "cut", "从'高'(gāo)切除声母g，保留纯正[ao]"),
    ("final_ou_pure",  "偷", "cut", "从'偷'(tōu)切除声母t，保留纯正[ou]"),
    ("final_iu_pure",  "忧", "direct", "直取'忧'(yōu)原生一声"),
    ("final_ie_pure",  "耶", "direct", "直取'耶'(yē)原生一声"),
    ("final_ve_pure",  "约", "direct", "直取'约'(yuē)原生一声"),
    ("final_er_pure",  "ēr", "direct", "直取'ēr'原生一声"),
    ("final_an_pure",  "安", "direct", "直取'安'(ān)原生一声"),
    ("final_en_pure",  "分", "cut", "从'分'(fēn)切除声母f，保留纯正[ən]"),
    ("final_in_pure",  "因", "direct", "直取'因'(yīn)原生一声"),
    ("final_un_pure",  "温", "direct", "直取'温'(wēn)原生一声"),
    ("final_vn_pure",  "晕", "direct", "直取'晕'(yūn)原生一声"),
    ("final_ang_pure", "刚", "cut", "从'刚'(gāng)切除声母g，保留纯正[aŋ]"),
    ("final_eng_pure", "风", "cut", "从'风'(fēng)切除声母f，保留纯正[əŋ]"),
    ("final_ing_pure", "英", "direct", "直取'英'(yīng)原生一声"),
    ("final_ong_pure", "东", "cut", "从'东'(dōng)切除声母d，保留纯正[ʊŋ]"),
]

def trim_silence(snd: parselmouth.Sound, thresh_ratio=0.03, pad_ms=15) -> parselmouth.Sound:
    samples = snd.values[0]
    sr = snd.sampling_frequency
    thresh = np.max(np.abs(samples)) * thresh_ratio
    active = np.where(np.abs(samples) > thresh)[0]
    if len(active) == 0:
        return snd
    s_idx = max(0, active[0] - int(sr * pad_ms / 1000))
    e_idx = min(len(samples), active[-1] + int(sr * pad_ms / 1000))
    return parselmouth.Sound(samples[s_idx:e_idx], sampling_frequency=sr)

def save_mp3(snd: parselmouth.Sound, out_path: Path):
    samples = snd.values[0].copy()
    sr = snd.sampling_frequency
    m = np.max(np.abs(samples))
    if m > 1e-4:
        samples *= (0.891 / m)
    # Cosine fade-in (12ms) and fade-out (15ms)
    fl_in = int(sr * 0.012)
    fl_out = int(sr * 0.015)
    if len(samples) > (fl_in + fl_out):
        samples[:fl_in] *= 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, fl_in)))
        samples[-fl_out:] *= 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, fl_out)))
    tmp_wav = out_path.parent / f"tmp_{out_path.stem}.wav"
    parselmouth.Sound(samples, sampling_frequency=sr).save(str(tmp_wav), "WAV")
    subprocess.run(["ffmpeg", "-y", "-i", str(tmp_wav), "-b:a", "128k", str(out_path)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp_wav.unlink(missing_ok=True)

def cut_consonant(snd_raw: parselmouth.Sound) -> parselmouth.Sound:
    pitch = call(snd_raw, "To Pitch", 0.005, 80, 500)
    times = pitch.xs()
    f0 = pitch.selected_array['frequency']
    voiced = np.where(f0 > 0)[0]
    if len(voiced) == 0:
        return trim_silence(snd_raw)
    
    # Precise Voice Onset Time (VOT)
    # The first voiced frame marks the start of the vowel/rhyme
    v_start_t = times[voiced[0]]
    
    # Extract from v_start_t to end
    rhyme = snd_raw.extract_part(from_time=v_start_t, to_time=snd_raw.duration)
    return trim_silence(rhyme)

async def synth_all():
    tasks = []
    for fname, text, mode, desc in FINAL_RECIPES:
        raw_f = RAW_DIR / f"{fname}.mp3"
        if not raw_f.exists():
            c = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="-15%")
            tasks.append(c.save(str(raw_f)))
    if tasks:
        await asyncio.gather(*tasks)

def run():
    print("Step 1: Generating raw TTS...")
    asyncio.run(synth_all())
    
    print("\nStep 2: Performing precise acoustic consonant removal and native extraction...")
    results = []
    for fname, text, mode, desc in FINAL_RECIPES:
        raw_f = RAW_DIR / f"{fname}.mp3"
        snd_raw = parselmouth.Sound(str(raw_f))
        
        if mode == "cut":
            snd_clean = cut_consonant(snd_raw)
        else:
            snd_clean = trim_silence(snd_raw)
            
        out_f = OUT_DIR / f"{fname}.mp3"
        save_mp3(snd_clean, out_f)
        
        # Acoustic verification
        snd_ver = parselmouth.Sound(str(out_f))
        pitch = call(snd_ver, "To Pitch", 0.005, 80, 500)
        f0 = pitch.selected_array['frequency']
        v = f0[f0 > 0]
        harm = call(snd_ver, "To Harmonicity (cc)", 0.01, 80, 0.1, 4.5)
        hnr = call(harm, "Get mean", 0, 0)
        pp = call(snd_ver, "To PointProcess (periodic, cc)", 80, 500)
        jit = call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3) * 100
        
        mid_f0 = v[len(v)//2] if len(v) > 0 else 0
        f0_std = np.std(v) if len(v) > 0 else 0
        diff = (v[-1] - v[0]) if len(v) > 0 else 0
        
        results.append((fname, text, snd_ver.duration, mid_f0, f0_std, diff, hnr, jit, desc))
        
    print(f"\n{'韵母名称':16s} {'字源':4s} {'时长':6s} {'中段F0':8s} {'F0波动':8s} {'首尾差':8s} {'HNR':8s} {'Jitter':8s} {'声调评定'}")
    print("-" * 88)
    for fn, t, dur, mf0, std, diff, hnr, jit, desc in results:
        tone_eval = "55 高平调 ✓" if (285 <= mf0 <= 325 and std < 20) else "待检查"
        print(f"{fn:16s} {t:4s} {dur:5.2f}s {mf0:6.1f}Hz {std:6.1f}Hz {diff:+6.1f}Hz {hnr:6.1f}dB {jit:5.2f}%  {tone_eval}")

if __name__ == "__main__":
    run()
