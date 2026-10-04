import asyncio
import edge_tts
import parselmouth
from parselmouth.praat import call
import numpy as np
from pathlib import Path
import subprocess

OUT_DIR = Path("audio/psola-experiment/native_finals_test")
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = Path("audio/tmp_test_finals")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def save_mp3(snd: parselmouth.Sound, out_path: Path):
    samples = snd.values[0].copy()
    sr = snd.sampling_frequency
    m = np.max(np.abs(samples))
    if m > 1e-4:
        samples *= (0.891 / m)
    fl = int(sr * 0.012)
    if len(samples) > fl * 2:
        fi = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, fl)))
        fo = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, fl)))
        samples[:fl] *= fi
        samples[-fl:] *= fo
    tmp_wav = out_path.parent / f"tmp_{out_path.stem}.wav"
    parselmouth.Sound(samples, sampling_frequency=sr).save(str(tmp_wav), "WAV")
    subprocess.run(["ffmpeg", "-y", "-i", str(tmp_wav), "-b:a", "128k", str(out_path)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp_wav.unlink(missing_ok=True)

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

async def synth(text, out_f):
    if not out_f.exists():
        c = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="-15%")
        await c.save(str(out_f))

# Define extraction recipes for all 24 finals:
# Type 1: Direct text (trimmed)
# Type 2: Cut consonant prefix (for o from mo, e from ge, ong from hong)
RECIPES = [
    ("final_a_pure", "ā", "direct"),
    ("final_o_pure", "摸", "cut_mo"),
    ("final_e_pure", "哥", "cut_ge"),
    ("final_i_pure", "衣", "direct"),
    ("final_u_pure", "屋", "direct"),
    ("final_v_pure", "淤", "direct"),
    ("final_ai_pure", "哀", "direct"),
    ("final_ei_pure", "ēi", "direct"),
    ("final_ui_pure", "威", "direct"),
    ("final_ao_pure", "凹", "direct"),
    ("final_ou_pure", "欧", "direct"),
    ("final_iu_pure", "忧", "direct"),
    ("final_ie_pure", "耶", "direct"),
    ("final_ve_pure", "约", "direct"),
    ("final_er_pure", "ēr", "direct"),
    ("final_an_pure", "安", "direct"),
    ("final_en_pure", "恩", "direct"),
    ("final_in_pure", "因", "direct"),
    ("final_un_pure", "温", "direct"),
    ("final_vn_pure", "晕", "direct"),
    ("final_ang_pure", "肮", "direct"),
    ("final_eng_pure", "鞥", "direct"),
    ("final_ing_pure", "英", "direct"),
    ("final_ong_pure", "轰", "cut_hong"),
]

async def prepare_raw():
    tasks = []
    for fname, text, rtype in RECIPES:
        tasks.append(synth(text, RAW_DIR / f"{fname}.mp3"))
    await asyncio.gather(*tasks)

def cut_vowel(snd_raw: parselmouth.Sound, skip_sec: float) -> parselmouth.Sound:
    dur = snd_raw.duration
    part = snd_raw.extract_part(from_time=skip_sec, to_time=dur)
    return trim_silence(part)

def process_all():
    print("Processing 24 finals using pure native neural voice (NO PSOLA)...")
    for fname, text, rtype in RECIPES:
        raw_f = RAW_DIR / f"{fname}.mp3"
        snd_raw = parselmouth.Sound(str(raw_f))
        
        if rtype == "direct":
            snd_out = trim_silence(snd_raw)
        elif rtype == "cut_mo":
            # Cut [m] nasal consonant (approx first 120ms of sound)
            # Find energy onset of vowel
            pitch = call(snd_raw, "To Pitch", 0.005, 80, 500)
            times = pitch.xs()
            f0 = pitch.selected_array['frequency']
            voiced = np.where(f0 > 0)[0]
            # In mo, [m] is voiced too, but vowel [o] has much higher amplitude (F1 > 500Hz)
            # Find where waveform amplitude jumps up significantly
            samples = snd_raw.values[0]
            sr = snd_raw.sampling_frequency
            # windowed RMS energy
            win_size = int(sr * 0.015)
            rms = np.array([np.sqrt(np.mean(samples[i:i+win_size]**2)) for i in range(0, len(samples)-win_size, win_size)])
            rms_times = np.arange(len(rms)) * (win_size / sr)
            max_rms = np.max(rms)
            vowel_start_idx = np.where(rms > max_rms * 0.45)[0][0]
            t_start = max(0, rms_times[vowel_start_idx] - 0.01)
            snd_out = cut_vowel(snd_raw, t_start)
            
        elif rtype == "cut_ge":
            # [g] is burst, unvoiced closure, then voice onset of [ɤ]
            pitch = call(snd_raw, "To Pitch", 0.005, 80, 500)
            times = pitch.xs()
            f0 = pitch.selected_array['frequency']
            voiced = np.where(f0 > 0)[0]
            v_start = times[voiced[0]]
            snd_out = cut_vowel(snd_raw, v_start)
            
        elif rtype == "cut_hong":
            # [h] is voiceless friction, voice onset is [ʊŋ]
            pitch = call(snd_raw, "To Pitch", 0.005, 80, 500)
            times = pitch.xs()
            f0 = pitch.selected_array['frequency']
            voiced = np.where(f0 > 0)[0]
            v_start = times[voiced[0]]
            snd_out = cut_vowel(snd_raw, v_start)
            
        out_f = OUT_DIR / f"{fname}.mp3"
        save_mp3(snd_out, out_f)
        
        # Analyze
        harm = call(snd_out, "To Harmonicity (cc)", 0.01, 80, 0.1, 4.5)
        hnr = call(harm, "Get mean", 0, 0)
        pitch = call(snd_out, "To Pitch", 0.005, 80, 500)
        f0 = pitch.selected_array['frequency']
        v = f0[f0 > 0]
        s_f0 = v[int(len(v)*0.1)] if len(v) > 0 else 0
        m_f0 = v[int(len(v)*0.5)] if len(v) > 0 else 0
        e_f0 = v[int(len(v)*0.9)] if len(v) > 0 else 0
        f0_std = np.std(v) if len(v) > 0 else 0
        
        print(f"{fname:16s} ({text:2s}): dur={snd_out.duration:.2f}s, midF0={m_f0:.1f}Hz, F0_std={f0_std:.1f}Hz, HNR={hnr:.1f}dB")

if __name__ == "__main__":
    asyncio.run(prepare_raw())
    process_all()
