#!/usr/bin/env python3
"""Generate real MP3 audio for the 《わたしの一日》(nihongo2) learning game.

This is lesson 2 in the series, continuing directly from 《わたしの一週間》
(nihongo.html / generate_nihongo_audio.py): same character (ゆうき), same
N5 difficulty, same edge-tts architecture — only the output folders and
lesson content change (a school day, from waking up to going to sleep).

Generates:
- audio/nihongo2/st1.mp3 .. st8.mp3       (8 story sentences, Japanese)
- audio/nihongo2/zi1.mp3 .. zi12.mp3      (12 生字: 朝起洗半出会休教室夜九食)
- audio/nihongo2/ci1.mp3 .. ci12.mp3      (12 单词)
- audio/nihongo2/pn1.mp3 .. pn7.mp3       (7 时间词: 朝昼夜六時七時半九時半)
- audio/nihongo2/sent1.mp3                (课后重点句子)
- audio/nihongo2_en/st1.mp3 .. st8.mp3    (8 story sentences, English translation)
- audio/nihongo2_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese bonus translation)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "nihongo2"
OUT_DIR_EN = ROOT / "audio" / "nihongo2_en"
OUT_DIR_ZH = ROOT / "audio" / "nihongo2_zh"
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
    ("st1", "ゆうきは朝六時に起きます。"),
    ("st2", "顔を洗ってから、朝ごはんを食べます。"),
    ("st3", "七時半に家を出て、学校へ行きます。"),
    ("st4", "学校で先生や友達に会って、挨拶をします。"),
    ("st5", "昼休みに、教室でお弁当を食べます。"),
    ("st6", "授業が終わってから、図書館で本を読みます。"),
    ("st7", "家へ帰って、家族と晩ごはんを食べます。"),
    ("st8", "夜九時に寝ます。明日もがんばります。"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "Yuki wakes up at six in the morning."),
    ("st2", "After washing my face, I eat breakfast."),
    ("st3", "I leave home at seven thirty and go to school."),
    ("st4", "At school, I meet my teacher and friends and greet them."),
    ("st5", "During lunch break, I eat my bento in the classroom."),
    ("st6", "After classes end, I read books in the library."),
    ("st7", "I go home and eat dinner with my family."),
    ("st8", "I go to sleep at nine at night. I'll do my best tomorrow too."),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "由纪早上六点起床。"),
    ("st2", "洗脸之后，吃早饭。"),
    ("st3", "七点半出门，去学校。"),
    ("st4", "在学校遇见老师和朋友，互相打招呼。"),
    ("st5", "午休时间，在教室里吃便当。"),
    ("st6", "下课后，在图书馆看书。"),
    ("st7", "回家后，和家人一起吃晚饭。"),
    ("st8", "晚上九点睡觉。明天也要加油。"),
]

# 2. 课后生字表 (12 汉字)
CHARACTERS = [
    ("zi1", "朝"), ("zi2", "起"), ("zi3", "洗"), ("zi4", "半"),
    ("zi5", "出"), ("zi6", "会"), ("zi7", "休"), ("zi8", "教"),
    ("zi9", "室"), ("zi10", "夜"), ("zi11", "九"), ("zi12", "食"),
]

# 3. 课后单词表 (12 Words)
WORDS = [
    ("ci1", "顔"), ("ci2", "挨拶"), ("ci3", "昼休み"), ("ci4", "教室"),
    ("ci5", "弁当"), ("ci6", "図書館"), ("ci7", "友達"), ("ci8", "授業"),
    ("ci9", "家族"), ("ci10", "朝ごはん"), ("ci11", "晩ごはん"), ("ci12", "先生"),
]

# 4. 课后「时间」词表 (7 Time Words)
PROPER_NOUNS = [
    ("pn1", "朝"), ("pn2", "昼"), ("pn3", "夜"), ("pn4", "六時"),
    ("pn5", "七時半"), ("pn6", "九時"), ("pn7", "半"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "毎朝起きるのは、とても気持ちがいいです。"),
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
