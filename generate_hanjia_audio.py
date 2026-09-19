#!/usr/bin/env python3
"""Generate real MP3 audio for the 《寒假见闻》(hanjia-jianwen) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key).
Generates audio files matching the exact textbook page for 《寒假见闻》:
- st1.mp3 .. st11.mp3 (11 story sentences)
- vc1.mp3 .. vc16.mp3 (16 vocabulary words)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "hanjia"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"  # slightly slower for language-learning clarity

# Keep IDs/text in sync with the STORY / VOCAB arrays in hanjia-jianwen.html
STORY = [
    ("st1", "今年寒假，我们全家回北京看望了爷爷奶奶。"),
    ("st2", "爷爷奶奶带着我们去了好多地方，天安门、故宫、长城……"),
    ("st3", "让我感觉最亲切的还是北京的胡同，因为那是爸爸小时候住过的地方。"),
    ("st4", "那天，爷爷带我去逛胡同。"),
    ("st5", "我们坐在人力车上，爷爷给我介绍，这是他们住过的四合院，那是爸爸小时候爬过的老槐树……"),
    ("st6", "蓝蓝的天、暖暖的阳光、弯弯曲曲的胡同，成为我难忘的老北京印象。"),
    ("st7", "北京既古老又现代。"),
    ("st8", "到处都有共享单车、共享汽车，交通非常方便。"),
    ("st9", "现在人们出门不用带现金，去哪儿都可以用手机付款。"),
    ("st10", "我最喜欢的是小区门口的自助图书馆，奶奶用手机扫一下，我就借到了想看的书！"),
    ("st11", "我喜欢北京，以后还会经常回来住住、看看。"),
]

VOCAB = [
    ("vc1", "寒假"),
    ("vc2", "爷爷奶奶"),
    ("vc3", "天安门"),
    ("vc4", "故宫"),
    ("vc5", "长城"),
    ("vc6", "胡同"),
    ("vc7", "人力车"),
    ("vc8", "四合院"),
    ("vc9", "老槐树"),
    ("vc10", "印象"),
    ("vc11", "共享单车"),
    ("vc12", "方便"),
    ("vc13", "现金"),
    ("vc14", "自助图书馆"),
    ("vc15", "古老"),
    ("vc16", "现代"),
]

ITEMS = STORY + VOCAB


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
