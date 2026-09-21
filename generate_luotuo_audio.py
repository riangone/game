#!/usr/bin/env python3
"""Generate real MP3 audio for the 《骆驼和羊》(luotuo-he-yang) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook pages for 《骆驼和羊》:
- st1.mp3 .. st15.mp3 (15 story sentences)
- zi1.mp3 .. zi15.mp3 (15 生字: 骆 驼 矮 件 比 俩 扒 肯 输 窄 跪 钻 找 评 短)
- ci1.mp3 .. ci14.mp3 (14 词语: 事情 证明 旁边 围墙 茂盛 枝叶 抬头 脖子 摇头 大模大样 进去 自己 长处 短处)
- sent1.mp3, sent2.mp3 (课后重点句子: 高比矮好 / 老牛评理名句)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "luotuo"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# 1. 课文逐句 (Story sentences)
STORY = [
    ("st1", "骆驼长得高，羊长得矮。"),
    ("st2", "骆驼说：“长得高好。”羊说：“不对，长得矮才好呢。”"),
    ("st3", "骆驼说：“我可以做一件事，证明高比矮好。”"),
    ("st4", "羊说：“我也可以做一件事，证明矮比高好。”"),
    ("st5", "他们俩走到一个园子旁边。"),
    ("st6", "园子四面有围墙，里面种了很多树，茂盛的枝叶伸出墙外来。"),
    ("st7", "骆驼一抬头就吃到了树叶。"),
    ("st8", "羊抬起前腿，扒在墙上，脖子伸得老长，还是吃不着。"),
    ("st9", "骆驼说：“你看，这可以证明了吧，高比矮好。”羊摇了摇头，不肯认输。"),
    ("st10", "他们俩又走了几步，看见围墙上有个又窄又矮的门。"),
    ("st11", "羊大模大样地走进去吃园子里的草。"),
    ("st12", "骆驼跪下前腿，低下头，往门里钻，怎么也钻不进去。"),
    ("st13", "羊说：“你看，这可以证明了吧，矮比高好。”骆驼摇了摇头，也不肯认输。"),
    ("st14", "他们俩找老牛评理。"),
    ("st15", "老牛说：“你们俩都只看到自己的长处，看不到自己的短处，这是不对的。”"),
]

# 2. 课后生字表 (15 Characters)
CHARACTERS = [
    ("zi1", "骆"),    # luò
    ("zi2", "驼"),    # tuó
    ("zi3", "矮"),    # ǎi
    ("zi4", "件"),    # jiàn
    ("zi5", "比"),    # bǐ
    ("zi6", "俩"),    # liǎ
    ("zi7", "扒"),    # bā
    ("zi8", "肯"),    # kěn
    ("zi9", "输"),    # shū
    ("zi10", "窄"),   # zhǎi
    ("zi11", "跪"),   # guì
    ("zi12", "钻"),   # zuān
    ("zi13", "找"),   # zhǎo
    ("zi14", "评"),   # píng
    ("zi15", "短"),   # duǎn
]

# 3. 课后词语表 (14 Words)
WORDS = [
    ("ci1", "事情"),      # shìqing
    ("ci2", "证明"),      # zhèngmíng
    ("ci3", "旁边"),      # pángbiān
    ("ci4", "围墙"),      # wéiqiáng
    ("ci5", "茂盛"),      # màoshèng
    ("ci6", "枝叶"),      # zhīyè
    ("ci7", "抬头"),      # táitóu
    ("ci8", "脖子"),      # bózi
    ("ci9", "摇头"),      # yáotóu
    ("ci10", "大模大样"),  # dàmú-dàyàng
    ("ci11", "进去"),      # jìnqù
    ("ci12", "自己"),      # zìjǐ
    ("ci13", "长处"),      # chángchù
    ("ci14", "短处"),      # duǎnchù
]

# 4. 课后重点句子 (Key Sentences)
KEY_SENTENCES = [
    ("sent1", "高比矮好。"),
    ("sent2", "你们俩都只看到自己的长处，看不到自己的短处，这是不对的。"),
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
    print("Done generating luotuo audio.")


if __name__ == "__main__":
    asyncio.run(main())
