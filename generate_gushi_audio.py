#!/usr/bin/env python3
"""Generate real MP3 audio for the 《古诗二首》(gushi-er-shou) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《古诗二首》(第9课):
《春晓》(唐)孟浩然 + 《悯农》(唐)李绅
- st1.mp3 .. st6.mp3 (6 story entries: 2 poem titles/bylines + 4 verse lines)
- zi1.mp3 .. zi13.mp3 (13 生字: 晓 孟 浩 眠 啼 悯 农 绅 锄 粒 皆 辛 苦)
- ci1.mp3 .. ci9.mp3 (9 词语/专有名词: 孟浩然 李绅 不觉 处处 风雨 多少 日当午 盘中餐 辛苦)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "gushi"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story entries: poem titles/bylines + verse lines)
STORY = [
    ("st1", "春晓 （唐）孟浩然"),
    ("st2", "春眠不觉晓，处处闻啼鸟。"),
    ("st3", "夜来风雨声，花落知多少。"),
    ("st4", "悯农 （唐）李绅"),
    ("st5", "锄禾日当午，汗滴禾下土。"),
    ("st6", "谁知盘中餐，粒粒皆辛苦。"),
]

# 2. 课后生字表 (13 Characters)
CHARACTERS = [
    ("zi1", "晓"),   # xiǎo
    ("zi2", "孟"),   # mèng
    ("zi3", "浩"),   # hào
    ("zi4", "眠"),   # mián
    ("zi5", "啼"),   # tí
    ("zi6", "悯"),   # mǐn
    ("zi7", "农"),   # nóng
    ("zi8", "绅"),   # shēn
    ("zi9", "锄"),   # chú
    ("zi10", "粒"),  # lì
    ("zi11", "皆"),  # jiē
    ("zi12", "辛"),  # xīn
    ("zi13", "苦"),  # kǔ
]

# 3. 课后词语表 (7 Words + 2 专有名词)
WORDS = [
    ("ci1", "孟浩然"),   # Mèng Hàorán
    ("ci2", "李绅"),     # Lǐ Shēn
    ("ci3", "不觉"),     # bùjué
    ("ci4", "处处"),     # chùchù
    ("ci5", "风雨"),     # fēngyǔ
    ("ci6", "多少"),     # duōshǎo
    ("ci7", "日当午"),   # rì dāng wǔ
    ("ci8", "盘中餐"),   # pánzhōngcān
    ("ci9", "辛苦"),     # xīnkǔ
]

ITEMS = STORY + CHARACTERS + WORDS


async def main():
    print(f"Generating {len(ITEMS)} audio files into {OUT_DIR} ...")
    sem = asyncio.Semaphore(4)

    async def generate_one(fname, text):
        target = OUT_DIR / f"{fname}.mp3"
        try:
            async with sem:
                comm = edge_tts.Communicate(text, VOICE, rate=RATE)
                await comm.save(str(target))
            if target.exists() and target.stat().st_size > 500:
                print(f"OK  {fname}.mp3  ({text})")
            else:
                print(f"WARN {fname}.mp3 looks too small")
        except Exception as e:
            print(f"FAIL {fname}: {e}")

    await asyncio.gather(*(generate_one(f, t) for f, t in ITEMS))
    print("Done generating gushi-er-shou audio.")


if __name__ == "__main__":
    asyncio.run(main())
