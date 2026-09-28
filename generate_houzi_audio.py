#!/usr/bin/env python3
"""Generate real MP3 audio for the 《猴子捞月亮》(houzi-lao-yueliang) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《猴子捞月亮》(第6课):
- st1.mp3 .. st8.mp3 (8 story sentences)
- zi1.mp3 .. zi8.mp3 (8 生字: 猴 捞 晚 群 跟 啊 接 碰)
- ci1.mp3 .. ci7.mp3 (7 词语: 月亮 晚上 跟着 于是 下面 伸手 这时)
- sent1.mp3 (课本例句/课后重点句子: 月亮不是还在天上吗？)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "houzi"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "有一天晚上，一群猴子在湖边的树上玩儿。"),
    ("st2", "突然，一只小猴子喊起来：“不好啦，月亮掉到水里了！”"),
    ("st3", "大猴子一看，也叫了起来：“不好啦，月亮真的掉到水里了！”"),
    ("st4", "一群猴子看了后都跟着说：“是啊，月亮怎么掉到水里了？”"),
    ("st5", "大猴子说：“我们把月亮捞上来吧！”"),
    ("st6", "于是，猴子们爬到树上，一只拉着一只，一直接到水里。"),
    ("st7", "挂在最下面的小猴子伸手去捞月亮。他的手刚碰到水，月亮就不见了。"),
    ("st8", "猴子们觉得很奇怪。这时，大猴子抬头一看，突然叫了起来：“月亮不是还在天上吗？”"),
]

# 2. 课后生字表 (8 Characters)
CHARACTERS = [
    ("zi1", "猴"),   # hóu
    ("zi2", "捞"),   # lāo
    ("zi3", "晚"),   # wǎn
    ("zi4", "群"),   # qún
    ("zi5", "跟"),   # gēn
    ("zi6", "啊"),   # a
    ("zi7", "接"),   # jiē
    ("zi8", "碰"),   # pèng
]

# 3. 课后词语表 (7 Words)
WORDS = [
    ("ci1", "月亮"),    # yuèliang
    ("ci2", "晚上"),    # wǎnshang
    ("ci3", "跟着"),    # gēnzhe
    ("ci4", "于是"),    # yúshì
    ("ci5", "下面"),    # xiàmiàn
    ("ci6", "伸手"),    # shēnshǒu
    ("ci7", "这时"),    # zhèshí
]

# 4. 课本例句 / 课后重点句子 (Key Sentence)
KEY_SENTENCES = [
    ("sent1", "月亮不是还在天上吗？"),
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
    print("Done generating houzi audio.")


if __name__ == "__main__":
    asyncio.run(main())
