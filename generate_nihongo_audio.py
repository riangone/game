#!/usr/bin/env python3
"""Generate real MP3 audio for the 《わたしの一週間》(nihongo) learning game.

Uses edge-tts (Microsoft neural voices, free, no API key), mirroring the exact
same architecture already used for the Chinese lesson games (generate_gugong_audio.py
+ generate_en_ja_story_audio.py), but with the language roles reversed: the main
narration is Japanese, with English + Chinese bonus tracks for the story only.

Generates:
- audio/nihongo/st1.mp3 .. st8.mp3       (8 story sentences, Japanese)
- audio/nihongo/zi1.mp3 .. zi12.mp3      (12 生字: 日月火水木金土学校友先生)
- audio/nihongo/ci1.mp3 .. ci12.mp3      (12 单词)
- audio/nihongo/pn1.mp3 .. pn7.mp3       (7 星期: 月火水木金土日曜日)
- audio/nihongo/sent1.mp3                (课后重点句子)
- audio/nihongo_en/st1.mp3 .. st8.mp3    (8 story sentences, English translation)
- audio/nihongo_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese bonus translation)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "nihongo"
OUT_DIR_EN = ROOT / "audio" / "nihongo_en"
OUT_DIR_ZH = ROOT / "audio" / "nihongo_zh"
for d in (OUT_DIR, OUT_DIR_EN, OUT_DIR_ZH):
    d.mkdir(parents=True, exist_ok=True)

JA_VOICE = "ja-JP-NanamiNeural"
EN_VOICE = "en-US-JennyNeural"
ZH_VOICE = "zh-CN-XiaoxiaoNeural"
JA_RATE = "-12%"  # slightly slower for language-learning clarity
EN_RATE = "-8%"
ZH_RATE = "-10%"

# 1. 课文逐句 (Story sentences, Japanese)
STORY = [
    ("st1", "わたしの名前はゆうきです。"),
    ("st2", "わたしは毎日学校へ行きます。"),
    ("st3", "月曜日と水曜日と金曜日は音楽の授業があります。"),
    ("st4", "火曜日と木曜日は学校で友達と日本語を勉強します。"),
    ("st5", "土曜日は家族と公園で遊びます。"),
    ("st6", "日曜日は家で本を読みます。"),
    ("st7", "わたしの先生はとても親切です。"),
    ("st8", "わたしは毎日とても元気です。"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "My name is Yuki."),
    ("st2", "I go to school every day."),
    ("st3", "On Mondays, Wednesdays, and Fridays, there is a music class."),
    ("st4", "On Tuesdays and Thursdays, I study Japanese with friends at school."),
    ("st5", "On Saturdays, I play in the park with my family."),
    ("st6", "On Sundays, I read a book at home."),
    ("st7", "My teacher is very kind."),
    ("st8", "I am very well and full of energy every day."),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "我的名字是由纪。"),
    ("st2", "我每天去学校。"),
    ("st3", "星期一、星期三和星期五有音乐课。"),
    ("st4", "星期二和星期四，我在学校和朋友一起学习日语。"),
    ("st5", "星期六我和家人在公园玩。"),
    ("st6", "星期天我在家看书。"),
    ("st7", "我的老师非常亲切。"),
    ("st8", "我每天都很有精神。"),
]

# 2. 课后生字表 (12 汉字)
CHARACTERS = [
    ("zi1", "日"), ("zi2", "月"), ("zi3", "火"), ("zi4", "水"),
    ("zi5", "木"), ("zi6", "金"), ("zi7", "土"), ("zi8", "学"),
    ("zi9", "校"), ("zi10", "友"), ("zi11", "先"), ("zi12", "生"),
]

# 3. 课后单词表 (12 Words)
WORDS = [
    ("ci1", "名前"), ("ci2", "毎日"), ("ci3", "学校"), ("ci4", "音楽"),
    ("ci5", "授業"), ("ci6", "友達"), ("ci7", "日本語"), ("ci8", "勉強"),
    ("ci9", "家族"), ("ci10", "公園"), ("ci11", "元気"), ("ci12", "親切"),
]

# 4. 课后「星期」词表 (7 Weekday Words)
PROPER_NOUNS = [
    ("pn1", "月曜日"), ("pn2", "火曜日"), ("pn3", "水曜日"), ("pn4", "木曜日"),
    ("pn5", "金曜日"), ("pn6", "土曜日"), ("pn7", "日曜日"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "日本語を勉強するのは、とても楽しいです。"),
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
