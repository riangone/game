#!/usr/bin/env python3
"""Generate real MP3 audio for the 《地球清洁工》(diqiu-qingjiegong) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《地球清洁工》(第10课):
- st1.mp3 .. st8.mp3 (8 story sentences)
- zi1.mp3 .. zi14.mp3 (14 生字: 球 洁 牌 报 半 漂 剩 夫 鸦 泥 肥 料 环 境)
- ci1.mp3 .. ci14.mp3 (14 词语: 时间 动物 海鸥 生活 垃圾 食物 乌鸦 说话 苍蝇 地面 蚯蚓 经过 消化 了不起)
- sent1.mp3 (课本例句/课后重点句子: 这里被我打扫得干干净净。)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "diqiu"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "地球公公在一棵树上挂了一块牌子，牌子上写着“地球清洁工报名处”。"),
    ("st2", "不到半天时间，就来了许多报名的动物。"),
    ("st3", "海鸥说：“我是海面清洁工，我能把海面上漂着的死鱼，人们倒在海里的剩饭、剩菜什么的都吃掉，海面就干净了。”"),
    ("st4", "河里的清道夫鱼从水中伸出头来说：“我生活在淡水里，河里的水草、水虫和垃圾都是我的食物，河水被我打扫得干干净净。”"),
    ("st5", "穿着一身黑衣的乌鸦说话了：“我也会打扫。我可以吃掉苍蝇啊、小虫啊，还有落在地面上的各种东西，这样地面就会干净多了。”"),
    ("st6", "蚯蚓静静地从泥土里钻出头来，说：“我在地下吃的是垃圾，经过我的消化后，垃圾就变成了肥料。”"),
    ("st7", "地球公公听了，笑着说：“你们都是了不起的地球清洁工，"),
    ("st8", "大家一起努力，地球环境才能变得更好。谢谢你们！”"),
]

# 2. 课后生字表 (14 Characters)
CHARACTERS = [
    ("zi1", "球"),   # qiú
    ("zi2", "洁"),   # jié
    ("zi3", "牌"),   # pái
    ("zi4", "报"),   # bào
    ("zi5", "半"),   # bàn
    ("zi6", "漂"),   # piāo
    ("zi7", "剩"),   # shèng
    ("zi8", "夫"),   # fū
    ("zi9", "鸦"),   # yā
    ("zi10", "泥"),  # ní
    ("zi11", "肥"),  # féi
    ("zi12", "料"),  # liào
    ("zi13", "环"),  # huán
    ("zi14", "境"),  # jìng
]

# 3. 课后词语表 (14 Words)
WORDS = [
    ("ci1", "时间"),    # shíjiān
    ("ci2", "动物"),    # dòngwù
    ("ci3", "海鸥"),    # hǎi'ōu
    ("ci4", "生活"),    # shēnghuó
    ("ci5", "垃圾"),    # lājī
    ("ci6", "食物"),    # shíwù
    ("ci7", "乌鸦"),    # wūyā
    ("ci8", "说话"),    # shuōhuà
    ("ci9", "苍蝇"),    # cāngying
    ("ci10", "地面"),   # dìmiàn
    ("ci11", "蚯蚓"),   # qiūyǐn
    ("ci12", "经过"),   # jīngguò
    ("ci13", "消化"),   # xiāohuà
    ("ci14", "了不起"), # liǎobuqǐ
]

# 4. 课本例句 / 课后重点句子 (Key Sentence)
KEY_SENTENCES = [
    ("sent1", "这里被我打扫得干干净净。"),
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
    print("Done generating diqiu audio.")


if __name__ == "__main__":
    asyncio.run(main())
