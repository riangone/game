#!/usr/bin/env python3
"""Scheme 1 Experiment: PSOLA Resynthesis of 4-Tone Pinyin Guided by Human F0 Contours.

This script tests:
1. Extracting F0 pitch trajectories & timing from human recordings (audio/human-pinyin/)
2. Using neural Edge-TTS audio as clean, modern acoustic carriers
3. Applying Praat-Parselmouth PSOLA manipulation (time alignment + pitch-tier transplant)
4. Measuring F0 before and after, assessing acoustic fidelity to standard tone values (55, 35, 214, 51)
5. Exporting audio samples for auditory inspection and creating an HTML comparison player.
"""

import sys
import subprocess
from pathlib import Path
import numpy as np
import parselmouth
from parselmouth.praat import call

ROOT = Path(__file__).resolve().parent
HUMAN_DIR = ROOT / "audio" / "human-pinyin"
TTS_DIR = ROOT / "audio" / "pinyin-basics"
OUT_DIR = ROOT / "audio" / "psola-experiment"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def trim_audio_silence(snd: parselmouth.Sound, thresh_ratio=0.03, pad_ms=25) -> parselmouth.Sound:
    """Trim leading and trailing silence while preserving speech onsets/offsets."""
    samples = snd.values[0]
    sr = snd.sampling_frequency
    thresh = np.max(np.abs(samples)) * thresh_ratio
    active = np.where(np.abs(samples) > thresh)[0]
    if len(active) == 0:
        return snd
    start_idx = max(0, active[0] - int(sr * pad_ms / 1000))
    end_idx = min(len(samples), active[-1] + int(sr * pad_ms / 1000))
    trimmed = samples[start_idx:end_idx]
    # gentle 10ms cosine fade
    fade_len = int(sr * 0.010)
    if len(trimmed) > fade_len * 2:
        fade_in = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, fade_len)))
        fade_out = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, fade_len)))
        trimmed[:fade_len] *= fade_in
        trimmed[-fade_len:] *= fade_out
    return parselmouth.Sound(trimmed, sampling_frequency=sr)

def analyze_f0(snd: parselmouth.Sound, min_f=80, max_f=500):
    """Extract F0 statistics and trajectory samples at 5 time points (10%, 30%, 50%, 70%, 90%)."""
    pitch = call(snd, "To Pitch", 0.005, min_f, max_f)
    f0 = pitch.selected_array['frequency']
    times = pitch.xs()
    valid_idx = np.where(f0 > 0)[0]
    if len(valid_idx) == 0:
        return {"dur": snd.duration, "voiced_dur": 0, "min": 0, "max": 0, "mean": 0, "trajectory": []}
    f0_valid = f0[valid_idx]
    times_valid = times[valid_idx]
    pcts = [0.1, 0.3, 0.5, 0.7, 0.9]
    traj = [float(f0_valid[int(p * (len(f0_valid) - 1))]) for p in pcts]
    return {
        "dur": float(snd.duration),
        "voiced_dur": float(times_valid[-1] - times_valid[0]),
        "min": float(np.min(f0_valid)),
        "max": float(np.max(f0_valid)),
        "mean": float(np.mean(f0_valid)),
        "trajectory": traj,
        "times": times_valid,
        "f0": f0_valid
    }

def psola_resynthesize(ref_mp3: Path, carrier_mp3: Path, out_mp3: Path, target_dur_ratio=1.0):
    """Resynthesize carrier with reference pitch contour via Praat PSOLA."""
    # 1. Load and trim
    ref_snd = trim_audio_silence(parselmouth.Sound(str(ref_mp3)))
    carrier_snd = trim_audio_silence(parselmouth.Sound(str(carrier_mp3)))

    # 2. Extract reference F0
    ref_stats = analyze_f0(ref_snd)
    if ref_stats["voiced_dur"] == 0:
        raise ValueError(f"No voiced segment found in reference: {ref_mp3}")
    
    t_v = ref_stats["times"]
    f0_v = ref_stats["f0"]
    t_start, t_end = t_v[0], t_v[-1]
    tau = (t_v - t_start) / (t_end - t_start)

    # 3. Target duration: reference voiced duration + 60ms padding
    target_dur = max(0.40, ref_stats["voiced_dur"] * target_dur_ratio)
    
    # 4. Lengthen carrier to target duration
    factor = target_dur / carrier_snd.duration
    carrier_stretched = call(carrier_snd, "Lengthen (overlap-add)", 80, 500, factor)

    # 5. Build new PitchTier on stretched carrier timeline
    manipulation = call(carrier_stretched, "To Manipulation", 0.005, 80, 500)
    pt = call("Create PitchTier", "pitch", 0, carrier_stretched.duration)
    
    # Map normalized time to carrier active duration
    for i in range(len(tau)):
        # align tau[0] slightly after onset (e.g. 20ms) and tau[-1] slightly before offset
        t_target = 0.02 + tau[i] * (carrier_stretched.duration - 0.04)
        target_f0 = float(f0_v[i])
        call(pt, "Add point", t_target, target_f0)

    # Inject pitch tier and resynthesize
    call([pt, manipulation], "Replace pitch tier")
    resynth_snd = call(manipulation, "Get resynthesis (overlap-add)")

    # 6. Normalize peak volume to -1 dBFS
    max_amp = np.max(np.abs(resynth_snd.values[0]))
    if max_amp > 1e-4:
        norm_factor = 0.89 / max_amp  # ~ -1dB
        resynth_snd.values[0] *= norm_factor

    # 7. Save to temp wav and encode to MP3
    tmp_wav = OUT_DIR / (out_mp3.stem + ".wav")
    resynth_snd.save(str(tmp_wav), "WAV")
    subprocess.run(["ffmpeg", "-y", "-i", str(tmp_wav), "-b:a", "128k", str(out_mp3)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp_wav.unlink(missing_ok=True)

    out_stats = analyze_f0(resynth_snd)
    return {
        "ref": ref_stats,
        "out": out_stats
    }

def main():
    test_cases = [
        # (base, tone, ref_file, carrier_file)
        ("a", 1, HUMAN_DIR / "a1.mp3", TTS_DIR / "tone_a_1.mp3"),
        ("a", 2, HUMAN_DIR / "a2.mp3", TTS_DIR / "tone_a_1.mp3"), # use clear tone-1 carrier
        ("a", 3, HUMAN_DIR / "a3.mp3", TTS_DIR / "tone_a_1.mp3"),
        ("a", 4, HUMAN_DIR / "a4.mp3", TTS_DIR / "tone_a_1.mp3"),
        ("ma", 1, HUMAN_DIR / "ma1.mp3", TTS_DIR / "tone_ma_1.mp3"),
        ("ma", 2, HUMAN_DIR / "ma2.mp3", TTS_DIR / "tone_ma_1.mp3"),
        ("ma", 3, HUMAN_DIR / "ma3.mp3", TTS_DIR / "tone_ma_1.mp3"),
        ("ma", 4, HUMAN_DIR / "ma4.mp3", TTS_DIR / "tone_ma_1.mp3"),
        ("o", 1, HUMAN_DIR / "o1.mp3", TTS_DIR / "tone_o_1.mp3"),
        ("o", 2, HUMAN_DIR / "o2.mp3", TTS_DIR / "tone_o_1.mp3"),
        ("o", 3, HUMAN_DIR / "o3.mp3", TTS_DIR / "tone_o_1.mp3"),
        ("o", 4, HUMAN_DIR / "o4.mp3", TTS_DIR / "tone_o_1.mp3"),
    ]

    results = []
    print(f"{'Item':8s} | {'Duration':10s} | {'Ref Trajectory (Hz)':35s} | {'Resynth Trajectory (Hz)':35s} | Status")
    print("-" * 105)

    for base, tone, ref_f, carrier_f in test_cases:
        item_name = f"{base}{tone}"
        out_f = OUT_DIR / f"psola_{item_name}.mp3"
        try:
            res = psola_resynthesize(ref_f, carrier_f, out_f)
            ref_traj = " ".join([f"{x:5.1f}" for x in res["ref"]["trajectory"]])
            out_traj = " ".join([f"{x:5.1f}" for x in res["out"]["trajectory"]])
            dur_str = f"{res['out']['dur']:.2f}s"
            print(f"{item_name:8s} | {dur_str:10s} | {ref_traj:35s} | {out_traj:35s} | OK")
            results.append((base, tone, ref_f, carrier_f, out_f, res))
        except Exception as e:
            print(f"{item_name:8s} | FAILED: {e}")

    # Build comparison HTML player
    html_lines = [
        "<!DOCTYPE html>",
        "<html lang='zh-CN'>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "<title>方案一 (PSOLA声调重合成) 效果试听对比实验室</title>",
        "<style>",
        "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #1e293b; padding: 24px; max-width: 1000px; margin: 0 auto; }",
        "h1 { color: #0f172a; margin-bottom: 8px; }",
        "p.subtitle { color: #64748b; margin-top: 0; margin-bottom: 24px; font-size: 15px; }",
        ".card { background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); padding: 20px; margin-bottom: 24px; }",
        "table { width: 100%; border-collapse: collapse; margin-top: 12px; }",
        "th, td { padding: 12px 14px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 14px; }",
        "th { background: #f1f5f9; font-weight: 600; color: #475569; }",
        ".badge { display: inline-block; padding: 2px 8px; border-radius: 9999px; font-size: 12px; font-weight: 600; }",
        ".badge-tone1 { background: #e0f2fe; color: #0369a1; }",
        ".badge-tone2 { background: #dcfce7; color: #15803d; }",
        ".badge-tone3 { background: #fef3c7; color: #b45309; }",
        ".badge-tone4 { background: #fee2e2; color: #b91c1c; }",
        "audio { height: 32px; width: 190px; vertical-align: middle; }",
        ".f0-tag { font-family: monospace; font-size: 12px; color: #475569; background: #f8fafc; padding: 2px 6px; border-radius: 4px; display: block; margin-top: 4px; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>方案一：基于真人F0音高轮廓的声学重合成 (PSOLA) 效果对比</h1>",
        "<p class='subtitle'>将真人发音的经典声调走势（55高平、35中升、214降升、51全降）提取为精确音高层，强制调制到 Edge-TTS 纯净神经音色载体上。</p>",
        "<div class='card'>",
        "<table>",
        "<thead><tr><th>音节/声调</th><th>调型规范</th><th>① 原始真人录音 (基准)</th><th>② 原始 Edge-TTS (无调制)</th><th>③ 方案一 PSOLA 重合成 (测试效果)</th></tr></thead>",
        "<tbody>"
    ]

    tone_names = {
        1: ("一声高平 (55)", "badge-tone1"),
        2: ("二声中升 (35)", "badge-tone2"),
        3: ("三声降升 (214)", "badge-tone3"),
        4: ("四声全降 (51)", "badge-tone4"),
    }

    for base, tone, ref_f, carrier_f, out_f, res in results:
        t_desc, badge_cls = tone_names[tone]
        raw_tts_f = TTS_DIR / f"tone_{base}_{tone}.mp3"
        ref_rel = f"../human-pinyin/{ref_f.name}"
        raw_tts_rel = f"../pinyin-basics/tone_{base}_{tone}.mp3"
        psola_rel = f"./psola_{base}{tone}.mp3"

        ref_f0_str = f"F0: {res['ref']['min']:.0f} ~ {res['ref']['max']:.0f} Hz ({res['ref']['dur']:.2f}s)"
        out_f0_str = f"F0: {res['out']['min']:.0f} ~ {res['out']['max']:.0f} Hz ({res['out']['dur']:.2f}s)"

        html_lines.append(f"<tr>")
        html_lines.append(f"<td><strong>{base}{tone}</strong> <span class='badge {badge_cls}'>{tone}声</span></td>")
        html_lines.append(f"<td>{t_desc}</td>")
        html_lines.append(f"<td><audio controls src='{ref_rel}'></audio><span class='f0-tag'>{ref_f0_str}</span></td>")
        html_lines.append(f"<td><audio controls src='{raw_tts_rel}'></audio><span class='f0-tag'>原生 TTS</span></td>")
        html_lines.append(f"<td><audio controls src='{psola_rel}'></audio><span class='f0-tag' style='color:#0369a1;font-weight:600;'>PSOLA重合成: {out_f0_str}</span></td>")
        html_lines.append(f"</tr>")

    html_lines.extend([
        "</tbody></table>",
        "</div>",
        "</body></html>"
    ])

    html_path = OUT_DIR / "tone_psola_comparison.html"
    html_path.write_text("\n".join(html_lines), encoding="utf-8")
    print(f"\nCreated comparison report & player: {html_path}")

if __name__ == "__main__":
    main()
