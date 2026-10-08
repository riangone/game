#!/usr/bin/env python3
"""Generate dedicated audio files for CLOZE questions and missing SCRAMBLE sentences across all 14 lessons.
Ensures 100% exact text-to-speech match for every cloze sentence.
"""
import asyncio
import os
import re
from pathlib import Path
import edge_tts

ROOT_DIR = Path(__file__).resolve().parent

LESSONS = [
    ('hanjia-jianwen.html', 'audio/hanjia', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('gugong.html', 'audio/gugong', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('yiheyuan.html', 'audio/yiheyuan', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('luotuo-he-yang.html', 'audio/luotuo', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('xiaoma-guohe.html', 'audio/xiaoma', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('houzi-lao-yueliang.html', 'audio/houzi', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('sima-guang.html', 'audio/sima', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('shu-xingxing.html', 'audio/xingxing', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('gushi-er-shou.html', 'audio/gushi', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('diqiu-qingjiegong.html', 'audio/diqiu', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('daziran-yuyan.html', 'audio/daziran', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('tanyue.html', 'audio/tanyue', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('nihongo0.html', 'audio/nihongo0', 'ja-JP-NanamiNeural', '-5%'),
    ('nihongo.html', 'audio/nihongo', 'ja-JP-NanamiNeural', '-10%'),
    ('nihongo2.html', 'audio/nihongo2', 'ja-JP-NanamiNeural', '-10%'),
    ('nihongo3.html', 'audio/nihongo3', 'ja-JP-NanamiNeural', '-5%'),
    ('nihongo4.html', 'audio/nihongo4', 'ja-JP-NanamiNeural', '-5%'),
    ('nihongo5.html', 'audio/nihongo5', 'ja-JP-NanamiNeural', '-5%'),
    ('nihongo6.html', 'audio/nihongo6', 'ja-JP-NanamiNeural', '-5%'),
]

MISSING_SCRAMBLE = [
    ('audio/xiaoma/st4b.mp3', '水深得很呢！你会淹死的！', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('audio/xiaoma/st6b.mp3', '老牛又高又大，他会觉得水很浅。', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('audio/houzi/st2b.mp3', '不好啦，月亮掉到水里了！', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('audio/houzi/st8a.mp3', '猴子们觉得很奇怪。', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('audio/tanyue/st3a.mp3', '美国宇航员第一次登上了月球。', 'zh-CN-XiaoxiaoNeural', '-12%'),
    ('audio/tanyue/st8a.mp3', '“嫦娥四号”实现了人类航天器首次在月球背面着陆。', 'zh-CN-XiaoxiaoNeural', '-12%'),
]

sem = asyncio.Semaphore(6)

async def generate_file(out_path, text, voice, rate):
    out_file = ROOT_DIR / out_path
    out_file.parent.mkdir(parents=True, exist_ok=True)
    if out_file.exists() and out_file.stat().st_size > 0:
        # Check if overwrite needed
        pass
    async with sem:
        for attempt in range(3):
            try:
                c = edge_tts.Communicate(text, voice, rate=rate)
                await c.save(str(out_file))
                if out_file.stat().st_size > 0:
                    return True
            except Exception as e:
                if attempt == 2:
                    print(f"Failed to generate {out_path}: {e}")
                await asyncio.sleep(1)
        return False

async def main():
    tasks = []
    
    # 1. Missing scramble
    for rel_path, text, voice, rate in MISSING_SCRAMBLE:
        tasks.append(generate_file(rel_path, text, voice, rate))
        
    # 2. Cloze files for all lessons
    for fn, out_dir, voice, rate in LESSONS:
        with open(ROOT_DIR / fn, 'r', encoding='utf-8') as f:
            c = f.read()
        m = re.search(r'const CLOZE_QUESTIONS = \[(.*?)\];', c, re.DOTALL)
        if not m:
            continue
        blocks = re.findall(r'\{[^{}]*id:[^{}]*\}', m.group(1), re.DOTALL)
        for idx, b in enumerate(blocks, 1):
            b_m = re.search(r'before:\s*[\"\']([^\"\']*)[\"\']', b)
            a_m = re.search(r'answer:\s*[\"\']([^\"\']*)[\"\']', b)
            af_m = re.search(r'after:\s*[\"\']([^\"\']*)[\"\']', b)
            if b_m and a_m and af_m:
                text = b_m.group(1) + a_m.group(1) + af_m.group(1)
                out_path = f"{out_dir}/cloze_{idx}.mp3"
                tasks.append(generate_file(out_path, text, voice, rate))
                
    print(f"Total audio tasks to generate: {len(tasks)}")
    results = await asyncio.gather(*tasks)
    success = sum(1 for r in results if r)
    print(f"Successfully generated {success} / {len(tasks)} audio files.")

if __name__ == '__main__':
    asyncio.run(main())
