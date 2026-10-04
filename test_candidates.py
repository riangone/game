import asyncio
import edge_tts
import parselmouth
from parselmouth.praat import call
import numpy as np
from pathlib import Path

DIR = Path("audio/tmp_test_finals")

# Let's test candidate sources for the tricky finals:
# u, o, ai, ao, ou, ang, eng, a
cands = [
    # final_u:
    ("u_wu", "屋"),
    ("u_gu", "姑"),
    ("u_zhu", "猪"),
    ("u_chu", "初"),
    ("u_wuu", "wū"),
    
    # final_o:
    ("o_mo", "摸"),
    ("o_po", "坡"),
    ("o_bo", "波"),
    ("o_fo", "fō"),
    
    # final_a:
    ("a_a", "ā"),
    ("a_ba", "八"),
    ("a_da", "搭"),
    ("a_ka", "咖"),
    
    # final_ai:
    ("ai_ai", "哀"),
    ("ai_kai", "开"),
    ("ai_cai", "猜"),
    ("ai_tai", "胎"),
    
    # final_ao:
    ("ao_ao", "凹"),
    ("ao_bao", "包"),
    ("ao_gao", "高"),
    ("ao_cao", "操"),
    
    # final_ou:
    ("ou_ou", "欧"),
    ("ou_gou", "钩"),
    ("ou_zhou", "周"),
    ("ou_tou", "偷"),
    
    # final_v (ü):
    ("v_yu", "淤"),
    ("v_yuu", "yū"),
    ("v_ju", "居"),
    ("v_qu", "区"),
    ("v_xu", "需"),
    
    # final_ang:
    ("ang_ang", "肮"),
    ("ang_bang", "帮"),
    ("ang_gang", "刚"),
    ("ang_cang", "仓"),
    
    # final_eng:
    ("eng_eng", "鞥"),
    ("eng_beng", "崩"),
    ("eng_geng", "更"),
    ("eng_feng", "风"),
]

async def run():
    tasks = []
    for tag, text in cands:
        out_f = DIR / f"{tag}.mp3"
        if not out_f.exists():
            c = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="-15%")
            tasks.append(c.save(str(out_f)))
    if tasks:
        await asyncio.gather(*tasks)

    print("Analyzing candidate sources...")
    for tag, text in cands:
        out_f = DIR / f"{tag}.mp3"
        snd = parselmouth.Sound(str(out_f))
        pitch = call(snd, "To Pitch", 0.005, 80, 500)
        times = pitch.xs()
        f0 = pitch.selected_array['frequency']
        v = np.where(f0 > 0)[0]
        if len(v) > 0:
            v_times = times[v]
            v_f0 = f0[v]
            voiced_dur = v_times[-1] - v_times[0]
            mid_f0 = v_f0[len(v_f0)//2]
            f0_std = np.std(v_f0)
            diff = v_f0[-1] - v_f0[0]
            print(f"{tag:10s} ({text:2s}): voiced_dur={voiced_dur:.2f}s, midF0={mid_f0:.1f}Hz, F0_std={f0_std:.1f}Hz, diff={diff:+.1f}Hz")

asyncio.run(run())
