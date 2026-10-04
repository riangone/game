import asyncio
import edge_tts
import parselmouth
from parselmouth.praat import call
import numpy as np
from pathlib import Path

DIR = Path("audio/tmp_clean_build")

tests = [
    # Candidates for e:
    ("e_ge", "哥"),
    ("e_ke", "科"),
    ("e_he", "喝"),
    ("e_che", "车"),
    ("e_she", "赊"),
    
    # Candidates for in:
    ("in_yin", "因"),
    ("in_bin", "宾"),
    ("in_pin", "拼"),
    ("in_xin", "新"),
    ("in_jin", "金"),
    
    # Candidates for er:
    ("er_er1", "ēr"),
    ("er_ssml1", "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'><prosody pitch='+0Hz'>ēr</prosody></speak>"),
    ("er_erhuo", "儿"), # 2-tone
]

async def run():
    tasks = []
    for tag, text in tests:
        out_f = DIR / f"{tag}.mp3"
        if not out_f.exists():
            c = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="-15%")
            tasks.append(c.save(str(out_f)))
    if tasks:
        await asyncio.gather(*tasks)

    print("Analyzing candidates for e, in, er...")
    for tag, text in tests:
        out_f = DIR / f"{tag}.mp3"
        snd = parselmouth.Sound(str(out_f))
        pitch = call(snd, "To Pitch", 0.005, 80, 500)
        times = pitch.xs()
        f0 = pitch.selected_array['frequency']
        v = np.where(f0 > 0)[0]
        if len(v) > 0:
            # Cut consonant
            v_start = times[v[0]]
            part = snd.extract_part(v_start, snd.duration)
            p_part = call(part, "To Pitch", 0.005, 80, 500)
            f0_part = p_part.selected_array['frequency']
            vp = f0_part[f0_part > 0]
            if len(vp) > 0:
                mid_f0 = vp[len(vp)//2]
                f0_std = np.std(vp)
                diff = vp[-1] - vp[0]
                harm = call(part, "To Harmonicity (cc)", 0.01, 80, 0.1, 4.5)
                hnr = call(harm, "Get mean", 0, 0)
                print(f"{tag:12s} ({text[:6]:6s}): dur={part.duration:.2f}s, midF0={mid_f0:.1f}Hz, std={f0_std:.1f}Hz, diff={diff:+6.1f}Hz, HNR={hnr:.1f}dB")

asyncio.run(run())
