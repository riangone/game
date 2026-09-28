#!/usr/bin/env python3
"""Generate real MP3 audio for the 《数星星的孩子》(shu-xingxing) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《数星星的孩子》(第8课):
- st1.mp3 .. st8.mp3 (8 story sentences)
- zi1.mp3 .. zi11.mp3 (11 生字: 数 靠 仰 颗 连 勺 斗 离 远 衡 努)
- ci1.mp3 .. ci9.mp3 (9 词语/专有名词: 星星 夜晚 天空 明亮 院子 努力 北斗星 北极星 张衡)
- sent1.mp3 (课本例句/课后重点句子: 那么多星星，你能数得清吗？)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "xingxing"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "夏天的夜晚，天空布满了明亮的星星。"),
    ("st2", "一个孩子坐在院子里，靠着奶奶，仰着头数天上的星星。"),
    ("st3", "他一颗一颗地数，数了很久，还是数不完。"),
    ("st4", "奶奶笑着说：“那么多星星，你能数得清吗？”"),
    ("st5", "孩子说：“看得见就能数得清。”"),
    ("st6", "爷爷过来了，说：“孩子，你看，那七颗星连起来像一把勺子，那是北斗星。离它不远的那颗星，叫北极星。”"),
    ("st7", "这个数星星的孩子叫张衡，是一千九百多年前的中国人。"),
    ("st8", "他努力学习，长大后成了著名的天文学家。"),
]

# 2. 课后生字表 (11 Characters)
CHARACTERS = [
    ("zi1", "数"),    # shǔ
    ("zi2", "靠"),    # kào
    ("zi3", "仰"),    # yǎng
    ("zi4", "颗"),    # kē
    ("zi5", "连"),    # lián
    ("zi6", "勺"),    # sháo
    ("zi7", "斗"),    # dǒu
    ("zi8", "离"),    # lí
    ("zi9", "远"),    # yuǎn
    ("zi10", "衡"),   # héng
    ("zi11", "努"),   # nǔ
]

# 3. 课后词语表 (6 Words + 3 专有名词)
WORDS = [
    ("ci1", "星星"),     # xīngxing
    ("ci2", "夜晚"),     # yèwǎn
    ("ci3", "天空"),     # tiānkōng
    ("ci4", "明亮"),     # míngliàng
    ("ci5", "院子"),     # yuànzi
    ("ci6", "努力"),     # nǔlì
    ("ci7", "北斗星"),   # Běidǒuxīng
    ("ci8", "北极星"),   # Běijíxīng
    ("ci9", "张衡"),     # Zhāng Héng
]

# 4. 课本例句 / 课后重点句子 (Key Sentence)
KEY_SENTENCES = [
    ("sent1", "那么多星星，你能数得清吗？"),
]

ITEMS = STORY + CHARACTERS + WORDS + KEY_SENTENCES


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
    print("Done generating shu-xingxing audio.")


if __name__ == "__main__":
    asyncio.run(main())
