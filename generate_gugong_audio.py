#!/usr/bin/env python3
"""Generate real MP3 audio for the 《故宫》(gugong) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook page for 《故宫》:
- st1.mp3 .. st8.mp3 (8 story sentences)
- zi1.mp3 .. zi12.mp3 (12 生字: 朝 清 皇 位 帝 居 殿 间 筑 藏 内 外)
- ci1.mp3 .. ci12.mp3 (12 词语: 这里 居住 世界 艺术 代表 珍贵 展览 吸引 游客 参观 著名 机会)
- pn1.mp3 .. pn6.mp3 (6 专有名词: 明朝 清朝 紫禁城 太和殿 中和殿 保和殿)
- sent1.mp3 (课后重点句子: 以后有机会我还要来故宫逛逛。)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "gugong"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "今天妈妈带我去游故宫。"),
    ("st2", "故宫是中国明朝和清朝的皇宫，又叫紫禁城，一共有二十四位皇帝在这里居住过。"),
    ("st3", "故宫已经有六百多年的历史了，是中国最大的古代宫殿，也是世界上最大的古代宫殿。"),
    ("st4", "我们以天安门为起点，一路向北，从午门进入故宫。"),
    ("st5", "故宫一共有九千多间房屋，都是用木头建造的，是中国古代建筑艺术的代表。"),
    ("st6", "故宫里收藏了许多珍贵的历史文物，有许多展览，吸引了许多国内外的游客前去参观。"),
    ("st7", "故宫真的很大，今天我们只参观了它最著名的三座大殿：太和殿、中和殿和保和殿。"),
    ("st8", "我对妈妈说，以后有机会我还要来故宫逛逛。"),
]

# 2. 课后生字表 (12 Characters)
CHARACTERS = [
    ("zi1", "朝"),    # cháo
    ("zi2", "清"),    # qīng
    ("zi3", "皇"),    # huáng
    ("zi4", "位"),    # wèi
    ("zi5", "帝"),    # dì
    ("zi6", "居"),    # jū
    ("zi7", "殿"),    # diàn
    ("zi8", "间"),    # jiān
    ("zi9", "筑"),    # zhù
    ("zi10", "藏"),   # cáng
    ("zi11", "内"),   # nèi
    ("zi12", "外"),   # wài
]

# 3. 课后词语表 (12 Words)
WORDS = [
    ("ci1", "这里"),   # zhèlǐ
    ("ci2", "居住"),   # jūzhù
    ("ci3", "世界"),   # shìjiè
    ("ci4", "艺术"),   # yìshù
    ("ci5", "代表"),   # dàibiǎo
    ("ci6", "珍贵"),   # zhēnguì
    ("ci7", "展览"),   # zhǎnlǎn
    ("ci8", "吸引"),   # xīyǐn
    ("ci9", "游客"),   # yóukè
    ("ci10", "参观"),  # cānguān
    ("ci11", "著名"),  # zhùmíng
    ("ci12", "机会"),  # jīhuì
]

# 4. 课后专有名词表 (6 Proper Nouns)
PROPER_NOUNS = [
    ("pn1", "明朝"),     # Míngcháo
    ("pn2", "清朝"),     # Qīngcháo
    ("pn3", "紫禁城"),   # Zǐjìnchéng
    ("pn4", "太和殿"),   # Tàihé Diàn
    ("pn5", "中和殿"),   # Zhōnghé Diàn
    ("pn6", "保和殿"),   # Bǎohé Diàn
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "以后有机会我还要来故宫逛逛。"),
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
