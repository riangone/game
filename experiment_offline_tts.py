#!/usr/bin/env python3
"""Offline TTS (Sherpa-ONNX / MeloTTS) Benchmark Experiment.

Tests:
1. Running offline neural TTS inference via Sherpa-ONNX with MeloTTS-zh-en model on CPU.
2. Generating 4 tones for all 6 single vowels (a, o, e, i, u, v/ü) and syllable 'ma'.
3. Audio files are isolated under audio/psola-experiment/offline_melotts_*.mp3
   (Strict isolation: zero impact on production textbook audio).
4. Acoustic F0 trajectory sampling (10%, 30%, 50%, 70%, 90%) using Praat-Parselmouth.
5. Generating a 5-way interactive comparison HTML laboratory:
   - ① Human Benchmark (Baseline)
   - ② Raw Neural TTS (Edge-TTS default)
   - ③ Scheme 1: PSOLA Resynthesis (Acoustic Pitch Transplant)
   - ④ Scheme 2: SSML Parameterized Tuning
   - ⑤ Scheme 3 (New): Sherpa-ONNX MeloTTS (Offline Neural Model)
"""

import os
import sys
import subprocess
from pathlib import Path
import numpy as np
import parselmouth
from parselmouth.praat import call
import sherpa_onnx

ROOT = Path("/home/ubuntu/ws/jump-jump-game")
EXP_DIR = ROOT / "audio" / "psola-experiment"
EXP_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DIR = ROOT / "offline-tts-models" / "vits-melo-tts-zh_en"
HUMAN_DIR = ROOT / "audio" / "human-pinyin"

def trim_silence(snd: parselmouth.Sound, thresh_ratio=0.03, pad_ms=25) -> parselmouth.Sound:
    samples = snd.values[0]
    sr = snd.sampling_frequency
    thresh = np.max(np.abs(samples)) * thresh_ratio
    active = np.where(np.abs(samples) > thresh)[0]
    if len(active) == 0:
        return snd
    start_idx = max(0, active[0] - int(sr * pad_ms / 1000))
    end_idx = min(len(samples), active[-1] + int(sr * pad_ms / 1000))
    trimmed = samples[start_idx:end_idx]
    fade_len = int(sr * 0.010)
    if len(trimmed) > fade_len * 2:
        fade_in = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, fade_len)))
        fade_out = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, fade_len)))
        trimmed[:fade_len] *= fade_in
        trimmed[-fade_len:] *= fade_out
    return parselmouth.Sound(trimmed, sampling_frequency=sr)

def analyze_f0(snd_path: Path):
    if not snd_path.exists():
        return None
    try:
        snd = parselmouth.Sound(str(snd_path))
        snd = trim_silence(snd)
        pitch = call(snd, "To Pitch", 0.005, 80, 500)
        f0 = pitch.selected_array['frequency']
        valid_idx = np.where(f0 > 0)[0]
        if len(valid_idx) == 0:
            return {
                "dur": float(snd.duration),
                "voiced_dur": 0.0,
                "f0_10": 0.0, "f0_30": 0.0, "f0_50": 0.0, "f0_70": 0.0, "f0_90": 0.0,
                "min": 0.0, "max": 0.0, "mean": 0.0
            }
        f0_valid = f0[valid_idx]
        pcts = [0.1, 0.3, 0.5, 0.7, 0.9]
        traj = [float(f0_valid[int(p * (len(f0_valid) - 1))]) for p in pcts]
        return {
            "dur": float(snd.duration),
            "voiced_dur": float(len(valid_idx) * 0.005),
            "f0_10": round(traj[0], 1),
            "f0_30": round(traj[1], 1),
            "f0_50": round(traj[2], 1),
            "f0_70": round(traj[3], 1),
            "f0_90": round(traj[4], 1),
            "min": round(float(np.min(f0_valid)), 1),
            "max": round(float(np.max(f0_valid)), 1),
            "mean": round(float(np.mean(f0_valid)), 1),
        }
    except Exception as e:
        print(f"Error analyzing {snd_path.name}: {e}")
        return None

def init_melo_tts():
    vits_config = sherpa_onnx.OfflineTtsVitsModelConfig(
        model=str(MODEL_DIR / "model.onnx"),
        lexicon=str(MODEL_DIR / "lexicon.txt"),
        tokens=str(MODEL_DIR / "tokens.txt"),
        dict_dir=str(MODEL_DIR / "dict"),
        noise_scale=0.667,
        noise_scale_w=0.8,
        length_scale=1.1, # slightly slower for clearer tone contour
    )
    model_config = sherpa_onnx.OfflineTtsModelConfig(
        vits=vits_config,
        num_threads=2,
        debug=False,
        provider="cpu",
    )
    tts_config = sherpa_onnx.OfflineTtsConfig(
        model=model_config,
        rule_fsts=",".join([
            str(MODEL_DIR / "phone.fst"),
            str(MODEL_DIR / "date.fst"),
            str(MODEL_DIR / "number.fst"),
            str(MODEL_DIR / "new_heteronym.fst"),
        ]),
    )
    return sherpa_onnx.OfflineTts(tts_config)

TARGET_FAMILIES = [
    ("a",  "单韵母 a",  ["a1", "a2", "a3", "a4"],   "a"),
    ("o",  "单韵母 o",  ["o1", "o2", "o3", "o4"],   "o"),
    ("e",  "单韵母 e",  ["e1", "e2", "e3", "e4"],   "e"),
    ("i",  "单韵母 i",  ["i1", "i2", "i3", "i4"],   "yi"),
    ("u",  "单韵母 u",  ["u1", "u2", "u3", "u4"],   "wu"),
    ("v",  "单韵母 ü",  ["v1", "v2", "v3", "v4"],   "yu"),
    ("ma", "声韵组合 ma", ["ma1", "ma2", "ma3", "ma4"], "ma"),
]

def generate_melotts_audio(tts):
    print("\n[Step 1] Synthesizing 28 tone samples using Sherpa-ONNX MeloTTS...")
    import wave
    import tempfile

    for fam_key, fam_name, pinyin_tokens, ref_key in TARGET_FAMILIES:
        for tone_idx, token in enumerate(pinyin_tokens, 1):
            out_mp3 = EXP_DIR / f"offline_melotts_{fam_key}{tone_idx}.mp3"
            res = tts.generate(token, sid=0, speed=1.0)
            samples = np.array(res.samples, dtype=np.float32)
            sr = res.sample_rate

            # Normalize peak volume
            max_amp = np.max(np.abs(samples))
            if max_amp > 1e-4:
                samples = samples / max_amp * 0.9

            samples_int16 = (samples * 32767).astype(np.int16)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_f:
                tmp_wav_path = tmp_f.name

            try:
                with wave.open(tmp_wav_path, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(sr)
                    wf.writeframes(samples_int16.tobytes())
                cmd = ["ffmpeg", "-y", "-i", tmp_wav_path, "-b:a", "128k", str(out_mp3)]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            finally:
                if os.path.exists(tmp_wav_path):
                    os.unlink(tmp_wav_path)
            
            print(f"  -> Generated: {out_mp3.name} ({len(samples)/sr:.2f}s)")

def build_5way_data():
    print("\n[Step 2] Collecting acoustic data across all 5 schemes...")
    all_data = []

    for fam_key, fam_name, pinyin_tokens, ref_key in TARGET_FAMILIES:
        fam_items = []
        for tone in range(1, 5):
            # 1. Human Ref
            human_file = HUMAN_DIR / f"{ref_key}{tone}.mp3"
            # 2. Raw Edge-TTS
            raw_file = EXP_DIR / f"raw_tts_{fam_key}_{tone}.mp3"
            # 3. PSOLA Scheme 1
            psola_file = EXP_DIR / f"psola_{fam_key}{tone}.mp3"
            # 4. Scheme 2 SSML
            scheme2_file = EXP_DIR / f"scheme2_{fam_key}{tone}.mp3"
            # 5. Offline MeloTTS
            melotts_file = EXP_DIR / f"offline_melotts_{fam_key}{tone}.mp3"

            fam_items.append({
                "tone": tone,
                "token": pinyin_tokens[tone-1],
                "schemes": {
                    "human":   {"file": human_file.name,   "stats": analyze_f0(human_file)},
                    "raw":     {"file": raw_file.name,     "stats": analyze_f0(raw_file)},
                    "psola":   {"file": psola_file.name,   "stats": analyze_f0(psola_file)},
                    "ssml":    {"file": scheme2_file.name, "stats": analyze_f0(scheme2_file)},
                    "melotts": {"file": melotts_file.name, "stats": analyze_f0(melotts_file)},
                }
            })
        all_data.append({
            "key": fam_key,
            "name": fam_name,
            "ref_key": ref_key,
            "items": fam_items
        })
    return all_data

def generate_comparison_html(all_data):
    print("\n[Step 3] Generating 5-way laboratory comparison HTML...")
    out_html = EXP_DIR / "tone_offline_tts_comparison.html"

    tone_meta = {
        1: ("一声 高平 (55)", "badge-tone1", "ˉ"),
        2: ("二声 中升 (35)", "badge-tone2", "ˊ"),
        3: ("三声 降升 (214)", "badge-tone3", "ˇ"),
        4: ("四声 全降 (51)", "badge-tone4", "ˋ"),
    }

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>拼音声调生成技术方案全景评测实验室 (五方横向对比)</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", sans-serif; background: #f8fafc; color: #1e293b; padding: 24px; max-width: 1440px; margin: 0 auto; }
  h1 { color: #0f172a; margin-bottom: 6px; font-size: 26px; }
  .subtitle { color: #64748b; font-size: 15px; margin-top: 0; margin-bottom: 24px; }
  
  .architect-card { background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 20px 24px; margin-bottom: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); }
  .architect-card h2 { margin-top: 0; font-size: 18px; color: #0f172a; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; }
  
  .comparison-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-top: 14px; }
  .comp-box { background: #f8fafc; border-radius: 8px; padding: 14px; border: 1px solid #e2e8f0; font-size: 12px; }
  .comp-box h3 { margin: 0 0 8px 0; font-size: 13px; }
  .comp-box ul { margin: 0; padding-left: 16px; color: #475569; }
  .comp-box li { margin-bottom: 4px; }
  .badge-tag { display: inline-block; font-size: 10px; padding: 1px 6px; border-radius: 4px; font-weight: 600; margin-left: 4px; }

  .fam-section { background: white; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.04); margin-bottom: 24px; overflow: hidden; }
  .fam-title { background: #f1f5f9; padding: 12px 18px; font-size: 16px; font-weight: 600; color: #334155; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; }
  table { width: 100%; border-collapse: collapse; text-align: left; table-layout: fixed; }
  th, td { padding: 10px 12px; border-bottom: 1px solid #f1f5f9; font-size: 11px; vertical-align: middle; word-wrap: break-word; }
  th { background: #fafafa; font-weight: 600; color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; }
  
  .col-tone { width: 11%; }
  .col-scheme { width: 17.8%; }

  .badge { display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 12px; font-weight: 600; }
  .badge-tone1 { background: #e0f2fe; color: #0369a1; }
  .badge-tone2 { background: #dcfce7; color: #15803d; }
  .badge-tone3 { background: #fef3c7; color: #b45309; }
  .badge-tone4 { background: #fee2e2; color: #b91c1c; }
  
  audio { width: 100%; height: 28px; display: block; margin-bottom: 4px; }
  .tag { font-family: ui-monospace, SFMono-Regular, monospace; font-size: 10px; color: #64748b; }
  .highlight { color: #0284c7; font-weight: 600; }
  .f0-line { font-family: ui-monospace, monospace; font-size: 10px; color: #334155; margin-top: 2px; }
  .verdict-pass { color: #16a34a; font-weight: bold; }
  .verdict-warn { color: #d97706; font-weight: bold; }
  .verdict-fail { color: #dc2626; font-weight: bold; }
</style>
</head>
<body>

<h1>🎙️ 拼音四声调音方案全景横向评测实验室</h1>
<p class="subtitle">全面评测五种技术路线在小学语文拼音单音节四声（55 / 35 / 214 / 51）上的声学还原度与工程可用性</p>

<div class="architect-card">
  <h2>🏛️ 架构决策与五大方案对照总览 (Architect Assessment)</h2>
  <div class="comparison-grid">
    <div class="comp-box">
      <h3>① 原始真人录音 (基准)</h3>
      <span class="badge-tag" style="background:#e0e7ff; color:#3730a3;">教学黄金基准</span>
      <ul>
        <li><b>声学调值</b>：100% 严格吻合 55/35/214/51</li>
        <li><b>三声反弹</b>：深下探反弹，极具示范价值</li>
        <li><b>局限缺陷</b>：带历史底噪，部分单音节缺失需切片</li>
      </ul>
    </div>

    <div class="comp-box">
      <h3>② 原生 Edge-TTS</h3>
      <span class="badge-tag" style="background:#fee2e2; color:#991b1b;">语流先验偏离</span>
      <ul>
        <li><b>声学调值</b>：一声尾部下坠；四声常发成短促二声</li>
        <li><b>三声反弹</b>：0%（日常语流半三声 211 陷阱）</li>
        <li><b>音质底噪</b>：底噪为 0，音色清脆现代</li>
      </ul>
    </div>

    <div class="comp-box" style="border: 2px solid #0284c7; background: #f0f9ff;">
      <h3>③ 方案一 PSOLA 重合成</h3>
      <span class="badge-tag" style="background:#0284c7; color:#fff;">推荐落地方案</span>
      <ul>
        <li><b>声学调值</b>：将真人标准 55/35/214/51 注入现代音色</li>
        <li><b>三声反弹</b>：100% 达成完整教科书折返爬升</li>
        <li><b>优势</b>：兼备真人黄金调值与神经引擎 0 底噪</li>
      </ul>
    </div>

    <div class="comp-box">
      <h3>④ 方案二 SSML 调谐</h3>
      <span class="badge-tag" style="background:#fef3c7; color:#92400e;">协议与效果受限</span>
      <ul>
        <li><b>动态 contour</b>：免费网关协议层直接掐断 (1007)</li>
        <li><b>静态参数</b>：无法扭转神经模型底层音高下倾倾向</li>
        <li><b>三声反弹</b>：依然无法恢复 214 折返</li>
      </ul>
    </div>

    <div class="comp-box" style="border: 1px solid #10b981; background: #ecfdf5;">
      <h3>⑤ 方案三 MeloTTS (离线)</h3>
      <span class="badge-tag" style="background:#10b981; color:#fff;">全新离线神经探索</span>
      <ul>
        <li><b>推理架构</b>：Sherpa-ONNX 本地 CPU 推理，零外部 API 依赖</li>
        <li><b>单音节调值</b>：原生支持拼音标记 (a1~a4)，调型整体自然</li>
        <li><b>三声与一声</b>：请试听实测数据与音频对比</li>
      </ul>
    </div>
  </div>
</div>
"""

    def fmt_stats(st):
        if not st or st.get("dur", 0) == 0:
            return "<div class='f0-line'>（无有效数据）</div>"
        traj_str = f"{st['f0_10']} → {st['f0_50']} → {st['f0_90']} Hz"
        dur_str = f"时长: {st['dur']:.2f}s"
        return f"<div class='f0-line'><b>F0轨迹:</b> {traj_str}</div><div class='tag'>{dur_str} (有效: {st['voiced_dur']:.2f}s)</div>"

    for fam in all_data:
        html += f"""
<div class="fam-section">
  <div class="fam-title">
    <span>{fam['name']} (Family: {fam['key']})</span>
    <span style="font-size: 12px; color: #64748b; font-weight: normal;">五方同台横向视听</span>
  </div>
  <table>
    <thead>
      <tr>
        <th class="col-tone">声调</th>
        <th class="col-scheme">① 真人基准录音</th>
        <th class="col-scheme">② 原生 Edge-TTS</th>
        <th class="col-scheme">③ 方案一 PSOLA 重合成</th>
        <th class="col-scheme">④ 方案二 SSML 调谐</th>
        <th class="col-scheme">⑤ 方案三 MeloTTS 离线</th>
      </tr>
    </thead>
    <tbody>
"""
        for it in fam["items"]:
            t_num = it["tone"]
            t_label, badge_cls, mark = tone_meta[t_num]
            sch = it["schemes"]

            # Human
            h_audio = f"../human-pinyin/{sch['human']['file']}"
            h_stats = fmt_stats(sch['human']['stats'])

            # Raw
            raw_audio = f"{sch['raw']['file']}"
            raw_stats = fmt_stats(sch['raw']['stats'])

            # PSOLA
            psola_audio = f"{sch['psola']['file']}"
            psola_stats = fmt_stats(sch['psola']['stats'])

            # SSML
            ssml_audio = f"{sch['ssml']['file']}"
            ssml_stats = fmt_stats(sch['ssml']['stats'])

            # MeloTTS
            melo_audio = f"{sch['melotts']['file']}"
            melo_stats = fmt_stats(sch['melotts']['stats'])

            html += f"""
      <tr>
        <td>
          <span class="badge {badge_cls}">{t_label}</span>
          <div style="font-size: 13px; font-weight: bold; margin-top: 4px; color: #334155;">{it['token']}</div>
        </td>
        <td>
          <audio controls preload="none" src="{h_audio}"></audio>
          {h_stats}
        </td>
        <td>
          <audio controls preload="none" src="{raw_audio}"></audio>
          {raw_stats}
        </td>
        <td style="background: #f0f9ff;">
          <audio controls preload="none" src="{psola_audio}"></audio>
          {psola_stats}
        </td>
        <td>
          <audio controls preload="none" src="{ssml_audio}"></audio>
          {ssml_stats}
        </td>
        <td style="background: #ecfdf5;">
          <audio controls preload="none" src="{melo_audio}"></audio>
          {melo_stats}
        </td>
      </tr>
"""
        html += """
    </tbody>
  </table>
</div>
"""

    html += """
</body>
</html>
"""
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML comparison page created successfully: {out_html}")
    return out_html

def main():
    tts = init_melo_tts()
    generate_melotts_audio(tts)
    data = build_5way_data()
    out_html = generate_comparison_html(data)
    print("\nExperiment finished successfully!")

if __name__ == "__main__":
    main()
