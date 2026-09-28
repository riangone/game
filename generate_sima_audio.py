#!/usr/bin/env python3
"""Generate real MP3 audio for the 《司马光》(sima-guang) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《司马光》(第7课):
- st1.mp3 .. st8.mp3 (8 story sentences)
- zi1.mp3 .. zi13.mp3 (13 生字: 司 聪 扑 缸 装 吓 哭 慌 法 块 使 劲 砸)
- ci1.mp3 .. ci10.mp3 (10 词语/专有名词: 司马光 聪明 花园 扑通 小心 只有 惊慌 办法 石头 使劲)
- sent1.mp3 (课本例句/课后重点句子: 水缸破了，水流了出来。)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "sima"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "中国古代有一个聪明的孩子，叫司马光。"),
    ("st2", "一天，他和小朋友们在花园里玩儿，有的做游戏，有的爬树。"),
    ("st3", "突然，大家听到“扑通”一声。"),
    ("st4", "原来，树下有一个大水缸，有个小朋友不小心从树上掉到水缸里了。"),
    ("st5", "水缸又大又深，里面装满了水，别的小朋友都吓哭了，不知道怎么办，只有司马光不惊慌。"),
    ("st6", "他很快想出了一个办法，找来一块大石头，使劲向水缸砸去。"),
    ("st7", "水缸破了，水流了出来，那个小朋友得救了。"),
    ("st8", "大家都说：“司马光真聪明！”"),
]

# 2. 课后生字表 (13 Characters)
CHARACTERS = [
    ("zi1", "司"),    # sī
    ("zi2", "聪"),    # cōng
    ("zi3", "扑"),    # pū
    ("zi4", "缸"),    # gāng
    ("zi5", "装"),    # zhuāng
    ("zi6", "吓"),    # xià
    ("zi7", "哭"),    # kū
    ("zi8", "慌"),    # huāng
    ("zi9", "法"),    # fǎ
    ("zi10", "块"),   # kuài
    ("zi11", "使"),   # shǐ
    ("zi12", "劲"),   # jìn
    ("zi13", "砸"),   # zá
]

# 3. 课后词语表 (9 Words + 1 专有名词)
WORDS = [
    ("ci1", "司马光"),   # Sīmǎ Guāng
    ("ci2", "聪明"),     # cōngming
    ("ci3", "花园"),     # huāyuán
    ("ci4", "扑通"),     # pūtōng
    ("ci5", "小心"),     # xiǎoxīn
    ("ci6", "只有"),     # zhǐyǒu
    ("ci7", "惊慌"),     # jīnghuāng
    ("ci8", "办法"),     # bànfǎ
    ("ci9", "石头"),     # shítou
    ("ci10", "使劲"),    # shǐjìn
]

# 4. 课本例句 / 课后重点句子 (Key Sentence)
KEY_SENTENCES = [
    ("sent1", "水缸破了，水流了出来。"),
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
    print("Done generating sima-guang audio.")


if __name__ == "__main__":
    asyncio.run(main())
