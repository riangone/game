#!/usr/bin/env python3
"""Generate real MP3 audio for the 《探月》(tanyue) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《探月》(第12课):
- st1.mp3 .. st8.mp3 (8 story sentences)
- zi1.mp3 .. zi15.mp3 (15 生字: 探 员 次 类 实 梦 船 达 植 音 式 程 器 背 陆)
- ci1.mp3 .. ci16.mp3 (16 词语/专有名词: 以前 明白 宇航员 人类 梦想 到达 荒凉 植物
  安全 正式 开展 实现 美国 阿波罗号 嫦娥探月工程 嫦娥四号)
- sent1.mp3 (课本例句/课后重点句子: 他们坐"阿波罗号"飞船离开了地球。)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "tanyue"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "月亮上有什么呢？"),
    ("st2", "人们很早很早以前就想看个明白。"),
    ("st3", "一九六九年七月二十一日，美国宇航员第一次登上了月球，在月球上留下了人类第一个脚印，实现了人类登月的梦想。"),
    ("st4", "七月十六日，他们坐“阿波罗号”飞船离开了地球，飞了三天多才到达月球。"),
    ("st5", "宇航员发现月球是一个荒凉的世界，到处都是石头和泥土，没有水，没有动物和植物，听不到一点儿声音。"),
    ("st6", "七月二十四日，他们带着月球上的泥土和石块，安全回到了地球。"),
    ("st7", "二〇〇四年，中国正式开展嫦娥探月工程。"),
    ("st8", "二〇一九年一月三日，“嫦娥四号”实现了人类航天器首次在月球背面着陆。"),
]

# 2. 课后生字表 (15 Characters)
CHARACTERS = [
    ("zi1", "探"),    # tàn
    ("zi2", "员"),    # yuán
    ("zi3", "次"),    # cì
    ("zi4", "类"),    # lèi
    ("zi5", "实"),    # shí
    ("zi6", "梦"),    # mèng
    ("zi7", "船"),    # chuán
    ("zi8", "达"),    # dá
    ("zi9", "植"),    # zhí
    ("zi10", "音"),   # yīn
    ("zi11", "式"),   # shì
    ("zi12", "程"),   # chéng
    ("zi13", "器"),   # qì
    ("zi14", "背"),   # bèi
    ("zi15", "陆"),   # lù
]

# 3. 课后词语表 (12 Words + 4 专有名词)
WORDS = [
    ("ci1", "以前"),         # yǐqián
    ("ci2", "明白"),         # míngbai
    ("ci3", "宇航员"),       # yǔhángyuán
    ("ci4", "人类"),         # rénlèi
    ("ci5", "梦想"),         # mèngxiǎng
    ("ci6", "到达"),         # dàodá
    ("ci7", "荒凉"),         # huāngliáng
    ("ci8", "植物"),         # zhíwù
    ("ci9", "安全"),         # ānquán
    ("ci10", "正式"),        # zhèngshì
    ("ci11", "开展"),        # kāizhǎn
    ("ci12", "实现"),        # shíxiàn
    ("ci13", "美国"),        # Měiguó
    ("ci14", "阿波罗号"),    # Ābōluóhào
    ("ci15", "嫦娥探月工程"), # Cháng'é tànyuè gōngchéng
    ("ci16", "嫦娥四号"),    # Cháng'é sìhào
]

# 4. 课本例句 / 课后重点句子 (Key Sentence)
KEY_SENTENCES = [
    ("sent1", "他们坐“阿波罗号”飞船离开了地球。"),
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
    print("Done generating tanyue audio.")


if __name__ == "__main__":
    asyncio.run(main())
