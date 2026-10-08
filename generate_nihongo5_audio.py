#!/usr/bin/env python3
"""Generate real MP3 audio for the 《おいしい日本料理》(nihongo5) learning game.

This is lesson 5 in the series, continuing directly from 《わたしの町》
(nihongo4.html / generate_nihongo4_audio.py): same character (ゆうき), same
N5 difficulty, same edge-tts architecture — output folders:
- audio/nihongo5/       (Japanese)
- audio/nihongo5_en/    (English translations)
- audio/nihongo5_zh/    (Chinese translations)

Generates:
- audio/nihongo5/st1.mp3 .. st8.mp3       (8 story sentences, Japanese)
- audio/nihongo5/zi1.mp3 .. zi12.mp3      (12 生字: 料理食水肉茶米牛味甘作体)
- audio/nihongo5/ci1.mp3 .. ci12.mp3      (12 单词: 料理/ご飯/味噌汁/卵焼き/魚/寿司/天ぷら/お弁当/お茶/食堂/美味しい/感謝)
- audio/nihongo5/pn1.mp3 .. pn7.mp3       (7 饮食表达词: いただきます/ごちそうさま/甘い/辛い/温かい/冷たい/好き)
- audio/nihongo5/sent1.mp3                (课后重点句子)
- audio/nihongo5/cloze_1.mp3 .. cloze_12.mp3 (12 选词填空原声句)
- audio/nihongo5_en/st1.mp3 .. st8.mp3    (8 story sentences, English)
- audio/nihongo5_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "nihongo5"
OUT_DIR_EN = ROOT / "audio" / "nihongo5_en"
OUT_DIR_ZH = ROOT / "audio" / "nihongo5_zh"
for d in (OUT_DIR, OUT_DIR_EN, OUT_DIR_ZH):
    d.mkdir(parents=True, exist_ok=True)

JA_VOICE = "ja-JP-NanamiNeural"
EN_VOICE = "en-US-JennyNeural"
ZH_VOICE = "zh-CN-XiaoxiaoNeural"
JA_RATE = "-5%"   # Natural rhythm and pitch
EN_RATE = "-8%"
ZH_RATE = "-10%"

# 1. 课文逐句 (Story sentences, Japanese)
STORY = [
    ("st1", "ゆうきは、美味しい日本料理が大好きです。"),
    ("st2", "朝は、温かいご飯と味噌汁を食べます。"),
    ("st3", "お昼には、甘い卵焼きと魚のお弁当を食べます。"),
    ("st4", "夜は、家族と一緒に寿司や天ぷらを作ります。"),
    ("st5", "食事の前に、「いただきます」と言います。"),
    ("st6", "食べた後には、「ごちそうさま」と感謝します。"),
    ("st7", "食堂で、冷たい水や温かいお茶を飲みます。"),
    ("st8", "日本の食べ物は、体に優しくてとても元気になります。"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "Yuki loves delicious Japanese food."),
    ("st2", "In the morning, I eat warm rice and miso soup."),
    ("st3", "For lunch, I eat a bento with sweet tamagoyaki and fish."),
    ("st4", "In the evening, I make sushi and tempura together with my family."),
    ("st5", "Before eating, we say 'Itadakimasu'."),
    ("st6", "After eating, we say 'Gochisousama' with gratitude."),
    ("st7", "In the cafeteria, we drink cold water or warm tea."),
    ("st8", "Japanese food is gentle on the body and brings lots of energy."),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "由纪非常喜欢美味的日本料理。"),
    ("st2", "早晨吃热腾腾的米饭和味增汤。"),
    ("st3", "中午吃带有甜味玉子烧和鱼的便当。"),
    ("st4", "晚上和家人一起做寿司和天妇罗。"),
    ("st5", "在开饭之前，说一句“我开动了”。"),
    ("st6", "吃完之后，说一句“承蒙款待”以表谢意。"),
    ("st7", "在食堂里，喝清凉的水或温热的绿茶。"),
    ("st8", "日本的美食温润养身，让人元气满满。"),
]

# 2. 课后生字表 (12 汉字)
CHARACTERS = [
    ("zi1", "料"), ("zi2", "理"), ("zi3", "食"), ("zi4", "水"),
    ("zi5", "肉"), ("zi6", "茶"), ("zi7", "米"), ("zi8", "牛"),
    ("zi9", "味"), ("zi10", "甘"), ("zi11", "作"), ("zi12", "体"),
]

# 3. 课后单词表 (12 Words)
WORDS = [
    ("ci1", "料理"), ("ci2", "ご飯"), ("ci3", "味噌汁"), ("ci4", "卵焼き"),
    ("ci5", "魚"), ("ci6", "寿司"), ("ci7", "天ぷら"), ("ci8", "お弁当"),
    ("ci9", "お茶"), ("ci10", "食堂"), ("ci11", "美味しい"), ("ci12", "感謝"),
]

# 4. 课后「饮食与味道」词表 (7 Dining Words)
PROPER_NOUNS = [
    ("pn1", "いただきます"), ("pn2", "ごちそうさま"), ("pn3", "甘い"), ("pn4", "辛い"),
    ("pn5", "温かい"), ("pn6", "冷たい"), ("pn7", "好き"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "日本の料理は、とても美味しくて体に優しいです。"),
]

# 6. 选词填空原声句子 (12 Sentences)
CLOZE_ITEMS = [
    ("cloze_1", "ゆうきは、美味しい日本料理が大好きです。"),
    ("cloze_2", "朝は、温かいご飯と味噌汁を食べます。"),
    ("cloze_3", "お昼には、甘い卵焼きと魚のお弁当を食べます。"),
    ("cloze_4", "夜は、家族と一緒に寿司や天ぷらを作ります。"),
    ("cloze_5", "食事の前に、「いただきます」と言います。"),
    ("cloze_6", "食べた後には、「ごちそうさま」と感謝します。"),
    ("cloze_7", "食堂で、冷たい水や温かいお茶を飲みます。"),
    ("cloze_8", "日本の食べ物は、体に優しくてとても元気になります。"),
    ("cloze_9", "この牛肉はとても美味しいです。"),
    ("cloze_10", "暑い日には、冷たいお茶を飲みましょう。"),
    ("cloze_11", "野菜と肉をたくさん買って、料理を作ります。"),
    ("cloze_12", "美味しい料理を食べて、みんなが笑顔になりました。"),
]

JA_ITEMS = STORY + CHARACTERS + WORDS + PROPER_NOUNS + KEY_SENTENCE + CLOZE_ITEMS


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
