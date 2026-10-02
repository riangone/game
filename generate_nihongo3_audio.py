#!/usr/bin/env python3
"""Generate real MP3 audio for the 《日本の四季》(nihongo3) learning game.

This is lesson 3 in the series, continuing directly from 《わたしの一日》
(nihongo2.html / generate_nihongo2_audio.py): same character (ゆうき), same
N5 difficulty, same edge-tts architecture — only the output folders and
lesson content change (the four seasons and nature in Japan).

Generates:
- audio/nihongo3/st1.mp3 .. st8.mp3       (8 story sentences, Japanese)
- audio/nihongo3/zi1.mp3 .. zi12.mp3      (12 生字: 春夏秋冬天雨雪花山川空白)
- audio/nihongo3/ci1.mp3 .. ci12.mp3      (12 单词)
- audio/nihongo3/pn1.mp3 .. pn7.mp3       (7 季节词: 春夏秋冬四季天气季节)
- audio/nihongo3/sent1.mp3                (课后重点句子)
- audio/nihongo3_en/st1.mp3 .. st8.mp3    (8 story sentences, English translation)
- audio/nihongo3_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese bonus translation)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "nihongo3"
OUT_DIR_EN = ROOT / "audio" / "nihongo3_en"
OUT_DIR_ZH = ROOT / "audio" / "nihongo3_zh"
for d in (OUT_DIR, OUT_DIR_EN, OUT_DIR_ZH):
    d.mkdir(parents=True, exist_ok=True)

JA_VOICE = "ja-JP-NanamiNeural"
EN_VOICE = "en-US-JennyNeural"
ZH_VOICE = "zh-CN-XiaoxiaoNeural"
JA_RATE = "-5%"   # Tuned for natural rhythm and clarity
EN_RATE = "-8%"
ZH_RATE = "-10%"

# 1. 课文逐句 (Story sentences, Japanese)
STORY = [
    ("st1", "ゆうきは、日本の美しい四季が大好きです。"),
    ("st2", "春になると、公園で桜の花がたくさん咲きます。"),
    ("st3", "夏休みには、青い空の下で、海や山へ行きます。"),
    ("st4", "秋は風が涼しく、山の木々が赤や黄色に変わります。"),
    ("st5", "冬の朝、静かな空から白い雪が降ります。"),
    ("st6", "川の近くを散歩して、澄んだ空気を吸います。"),
    ("st7", "一年中、旬の果物や美味しい季節の料理を食べます。"),
    ("st8", "季節が巡るたびに、毎日新しい発見があります。"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "Yuki loves Japan's beautiful four seasons."),
    ("st2", "When spring comes, lots of cherry blossoms bloom in the park."),
    ("st3", "During summer vacation, under the blue sky, I go to the sea and mountains."),
    ("st4", "In autumn, the wind is cool, and the trees on the mountains turn red and yellow."),
    ("st5", "On winter mornings, white snow falls quietly from the sky."),
    ("st6", "I take a walk near the river and breathe in the clear air."),
    ("st7", "Throughout the year, we eat seasonal fruits and delicious seasonal dishes."),
    ("st8", "Each time the seasons turn, there are new discoveries every day."),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "由纪非常喜欢日本美丽的四季。"),
    ("st2", "春天来临时，公园里盛开着许多樱花。"),
    ("st3", "暑假里，在蓝天之下，去大海和高山游玩。"),
    ("st4", "秋天微风凉爽，山上的树木染成了红黄相间的色彩。"),
    ("st5", "冬天的清晨，洁白的雪花从沉静的天空中静静飘落。"),
    ("st6", "漫步在小河边，呼吸着清澈清新的空气。"),
    ("st7", "一年四季，品尝着应季的水果和美味的时令料理。"),
    ("st8", "随着四季流转，每一天都有令人惊喜的新发现。"),
]

# 2. 课后生字表 (12 汉字)
CHARACTERS = [
    ("zi1", "春"), ("zi2", "夏"), ("zi3", "秋"), ("zi4", "冬"),
    ("zi5", "天"), ("zi6", "雨"), ("zi7", "雪"), ("zi8", "花"),
    ("zi9", "山"), ("zi10", "川"), ("zi11", "空"), ("zi12", "白"),
]

# 3. 课后单词表 (12 Words)
WORDS = [
    ("ci1", "桜"), ("ci2", "海"), ("ci3", "紅葉"), ("ci4", "料理"),
    ("ci5", "果物"), ("ci6", "散歩"), ("ci7", "景色"), ("ci8", "雲"),
    ("ci9", "綺麗"), ("ci10", "美しい"), ("ci11", "大好き"), ("ci12", "一年中"),
]

# 4. 课后「季节」词表 (7 Season Words)
PROPER_NOUNS = [
    ("pn1", "春"), ("pn2", "夏"), ("pn3", "秋"), ("pn4", "冬"),
    ("pn5", "四季"), ("pn6", "天気"), ("pn7", "季節"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "日本の四季は、色彩が豊かで、とても素晴らしいです。"),
]

JA_ITEMS = STORY + CHARACTERS + WORDS + PROPER_NOUNS + KEY_SENTENCE


async def synth(text, voice, rate, out_path):
    if out_path.exists() and out_path.stat().st_size > 500:
        print(f"SKIP {out_path.relative_to(ROOT)} (already exists)")
        return
    try:
        comm = edge_tts.Communicate(text, voice, rate=rate)
        await comm.save(str(out_path))
        if out_path.exists() and out_path.stat().st_size > 500:
            print(f"OK   {out_path.relative_to(ROOT)}  ({text})")
        else:
            print(f"WARN {out_path.relative_to(ROOT)} looks too small")
    except Exception as e:
        print(f"FAIL {out_path.relative_to(ROOT)}: {e}")


async def main():
    sem = asyncio.Semaphore(4)

    async def run(items, voice, rate, out_dir):
        async def one(fname, text):
            async with sem:
                await synth(text, voice, rate, out_dir / f"{fname}.mp3")
        await asyncio.gather(*(one(f, t) for f, t in items))

    print(f"Generating {len(JA_ITEMS)} Japanese audio files into {OUT_DIR} ...")
    await run(JA_ITEMS, JA_VOICE, JA_RATE, OUT_DIR)

    print(f"Generating {len(STORY_EN)} English story audio files into {OUT_DIR_EN} ...")
    await run(STORY_EN, EN_VOICE, EN_RATE, OUT_DIR_EN)

    print(f"Generating {len(STORY_ZH)} Chinese bonus story audio files into {OUT_DIR_ZH} ...")
    await run(STORY_ZH, ZH_VOICE, ZH_RATE, OUT_DIR_ZH)

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
