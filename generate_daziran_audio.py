#!/usr/bin/env python3
"""Generate real MP3 audio for the 《大自然的语言》(daziran-yuyan) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《大自然的语言》(第11课):
- st1.mp3 .. st8.mp3 (8 story sentences)
- zi1.mp3 .. zi11.mp3 (11 生字: 言 丰 富 晴 蚂 蚁 搬 伞 察 懂 考)
- ci1.mp3 .. ci10.mp3 (10 词语: 大自然 语言 丰富 晴天 公园 搬家 多么 认真 观察 思考)
- sent1.mp3 (课本例句/课后重点句子: 只有认真学习、细心观察，你才能看得见、听得懂。)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "daziran"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "人有语言，大自然也有语言吗？"),
    ("st2", "有的，大自然的语言可丰富了。"),
    ("st3", "你看，白云飘在高高的蓝天上，明天一定是个晴天，你可以去公园游玩了。"),
    ("st4", "你看，地上的蚂蚁正在忙着搬家呢，天很快就要下雨了，你出门可要带上雨伞啊。"),
    ("st5", "你再看，河里的冰化了，地上的草绿了，树叶长出来了，这是春天来了。"),
    ("st6", "大自然的语言多么丰富、多么奇妙啊！"),
    ("st7", "只有认真学习、细心观察，你才能看得见、听得懂。"),
    ("st8", "让我们做个爱学习、爱思考的好学生吧。"),
]

# 2. 课后生字表 (11 Characters)
CHARACTERS = [
    ("zi1", "言"),   # yán
    ("zi2", "丰"),   # fēng
    ("zi3", "富"),   # fù
    ("zi4", "晴"),   # qíng
    ("zi5", "蚂"),   # mǎ
    ("zi6", "蚁"),   # yǐ
    ("zi7", "搬"),   # bān
    ("zi8", "伞"),   # sǎn
    ("zi9", "察"),   # chá
    ("zi10", "懂"),  # dǒng
    ("zi11", "考"),  # kǎo
]

# 3. 课后词语表 (10 Words)
WORDS = [
    ("ci1", "大自然"),  # dàzìrán
    ("ci2", "语言"),    # yǔyán
    ("ci3", "丰富"),    # fēngfù
    ("ci4", "晴天"),    # qíngtiān
    ("ci5", "公园"),    # gōngyuán
    ("ci6", "搬家"),    # bānjiā
    ("ci7", "多么"),    # duōme
    ("ci8", "认真"),    # rènzhēn
    ("ci9", "观察"),    # guānchá
    ("ci10", "思考"),   # sīkǎo
]

# 4. 课本例句 / 课后重点句子 (Key Sentence)
KEY_SENTENCES = [
    ("sent1", "只有认真学习、细心观察，你才能看得见、听得懂。"),
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
    print("Done generating daziran audio.")


if __name__ == "__main__":
    asyncio.run(main())
