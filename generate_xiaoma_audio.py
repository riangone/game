#!/usr/bin/env python3
"""Generate real MP3 audio for the 《小马过河》(xiaoma-guohe) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《小马过河》(第5课):
- st1.mp3 .. st8.mp3 (8 story sentences)
- zi1.mp3 .. zi10.mp3 (10 生字: 喝 伯 深 浅 正 突 松 鼠 淹 定)
- ci1.mp3 .. ci7.mp3 (7 词语: 伯伯 突然 只好 那么 一定 最好 那样)
- sent1.mp3 (课后重点句子: 河水是深还是浅，最好你自己去试试。)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "xiaoma"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "小马要过河，看见一头老牛在喝水。"),
    ("st2", "小马问：“牛伯伯，我要过河，水深吗？”"),
    ("st3", "老牛说：“水很浅，你过得去。”"),
    ("st4", "小马听了老牛的话，正要过河，突然，一只小松鼠从树上跳下来，大声说：“小马，别过河！水深得很呢！你会淹死的！”"),
    ("st5", "听了小松鼠的话，小马不知道该怎么办，只好回家问妈妈。"),
    ("st6", "妈妈说：“孩子，老牛又高又大，他会觉得水很浅；松鼠那么小，他一定会说水很深。河水是深还是浅，最好你自己去试试。”"),
    ("st7", "小马听了妈妈的话，又跑到河边，小心地过了河。"),
    ("st8", "原来，河水既不像老牛说的那样浅，也不像松鼠说的那样深。"),
]

# 2. 课后生字表 (10 Characters)
CHARACTERS = [
    ("zi1", "喝"),   # hē
    ("zi2", "伯"),   # bó
    ("zi3", "深"),   # shēn
    ("zi4", "浅"),   # qiǎn
    ("zi5", "正"),   # zhèng
    ("zi6", "突"),   # tū
    ("zi7", "松"),   # sōng
    ("zi8", "鼠"),   # shǔ
    ("zi9", "淹"),   # yān
    ("zi10", "定"),  # dìng
]

# 3. 课后词语表 (7 Words)
WORDS = [
    ("ci1", "伯伯"),    # bóbo
    ("ci2", "突然"),    # tūrán
    ("ci3", "只好"),    # zhǐhǎo
    ("ci4", "那么"),    # nàme
    ("ci5", "一定"),    # yídìng
    ("ci6", "最好"),    # zuìhǎo
    ("ci7", "那样"),    # nàyàng
]

# 4. 课后重点句子 (Key Sentence)
KEY_SENTENCES = [
    ("sent1", "河水是深还是浅，最好你自己去试试。"),
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
    print("Done generating xiaoma audio.")


if __name__ == "__main__":
    asyncio.run(main())
