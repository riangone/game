#!/usr/bin/env python3
"""Generate real MP3 audio for the 《颐和园》(yiheyuan) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《颐和园》:
- st1.mp3 .. st12.mp3 (12 story sentences)
- zi1.mp3 .. zi18.mp3 (18 生字: 颐 园 久 站 底 岛 桥 洞 孔 柱 狮 分 廊 眼 万 寿 脚 收)
- ci1.mp3 .. ci6.mp3 (6 词语: 中心 美丽 生动 十分 栏杆 景色)
- pn1.mp3 .. pn4.mp3 (4 专有名词: 颐和园 昆明湖 十七孔桥 万寿山)
- sent1.mp3 (课后重点句子: 今年寒假，我终于来到了向往已久的颐和园。)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "yiheyuan"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "今年寒假，我终于来到了向往已久的颐和园。"),
    ("st2", "走进颐和园的东门，就能见到昆明湖。"),
    ("st3", "站在湖边，能看到湖底的水草，有时还能看见小鱼呢。"),
    ("st4", "湖中心有个美丽的小岛。"),
    ("st5", "从湖边到湖中心的小岛，要走过一座长长的石桥。"),
    ("st6", "这座桥有十七个桥洞，叫十七孔桥。"),
    ("st7", "桥两边的石柱上有许多小石狮子。"),
    ("st8", "它们都很生动，十分可爱。"),
    ("st9", "走在著名的长廊上，绿色的柱子，红色的栏杆，一眼望不到头。"),
    ("st10", "走完长廊，就来到了万寿山脚下。"),
    ("st11", "登上万寿山，颐和园的景色尽收眼底。"),
    ("st12", "颐和园到处都有美丽的景色，让人十分难忘。"),
]

# 2. 课后生字表 (18 Characters)
CHARACTERS = [
    ("zi1", "颐"),    # yí
    ("zi2", "园"),    # yuán
    ("zi3", "久"),    # jiǔ
    ("zi4", "站"),    # zhàn
    ("zi5", "底"),    # dǐ
    ("zi6", "岛"),    # dǎo
    ("zi7", "桥"),    # qiáo
    ("zi8", "洞"),    # dòng
    ("zi9", "孔"),    # kǒng
    ("zi10", "柱"),   # zhù
    ("zi11", "狮"),   # shī
    ("zi12", "分"),   # fēn
    ("zi13", "廊"),   # láng
    ("zi14", "眼"),   # yǎn
    ("zi15", "万"),   # wàn
    ("zi16", "寿"),   # shòu
    ("zi17", "脚"),   # jiǎo
    ("zi18", "收"),   # shōu
]

# 3. 课后词语表 (6 Words)
WORDS = [
    ("ci1", "中心"),   # zhōngxīn
    ("ci2", "美丽"),   # měilì
    ("ci3", "生动"),   # shēngdòng
    ("ci4", "十分"),   # shífēn
    ("ci5", "栏杆"),   # lángān
    ("ci6", "景色"),   # jǐngsè
]

# 4. 课后专有名词表 (4 Proper Nouns)
PROPER_NOUNS = [
    ("pn1", "颐和园"),   # Yíhé Yuán
    ("pn2", "昆明湖"),   # Kūnmíng Hú
    ("pn3", "十七孔桥"), # Shíqī-kǒng Qiáo
    ("pn4", "万寿山"),   # Wànshòu Shān
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "今年寒假，我终于来到了向往已久的颐和园。"),
]

ITEMS = STORY + CHARACTERS + WORDS + PROPER_NOUNS + KEY_SENTENCE


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
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
