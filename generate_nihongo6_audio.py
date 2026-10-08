#!/usr/bin/env python3
"""Generate real MP3 audio for the 《楽しい旅行》(nihongo6) learning game.

This is lesson 6 in the series, continuing directly from 《おいしい日本料理》
(nihongo5.html / generate_nihongo5_audio.py): same character (ゆうき), same
N5 difficulty, same edge-tts architecture — output folders:
- audio/nihongo6/       (Japanese)
- audio/nihongo6_en/    (English translations)
- audio/nihongo6_zh/    (Chinese translations)

Generates:
- audio/nihongo6/st1.mp3 .. st8.mp3       (8 story sentences, Japanese)
- audio/nihongo6/zi1.mp3 .. zi12.mp3      (12 生字: 旅行車両見海買写真京都)
- audio/nihongo6/ci1.mp3 .. ci12.mp3      (12 单词: 旅行/新幹線/電車/東京/京都/富士山/写真/お寺/神社/お土産/海/思い出)
- audio/nihongo6/pn1.mp3 .. pn7.mp3       (7 交通旅行词: 新幹線/電車/バス/飛行機/切符/ホテル/楽しい)
- audio/nihongo6/sent1.mp3                (课后重点句子)
- audio/nihongo6/cloze_1.mp3 .. cloze_12.mp3 (12 选词填空原声句)
- audio/nihongo6_en/st1.mp3 .. st8.mp3    (8 story sentences, English)
- audio/nihongo6_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "nihongo6"
OUT_DIR_EN = ROOT / "audio" / "nihongo6_en"
OUT_DIR_ZH = ROOT / "audio" / "nihongo6_zh"
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
    ("st1", "ゆうきは、休日に友達と京都へ旅行に行きます。"),
    ("st2", "東京駅から、速い新幹線に乗ります。"),
    ("st3", "窓の外に、高くて美しい富士山が見えます。"),
    ("st4", "京都に着いて、古いお寺や神社を歩きます。"),
    ("st5", "静かな庭で、綺麗な写真をたくさん撮ります。"),
    ("st6", "お昼は、電車で海へ行って美味しい魚を食べます。"),
    ("st7", "お土産の店で、家族や友達にお菓子を買います。"),
    ("st8", "日本の旅は、とても楽しくて素晴らしい思い出になります。"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "On holidays, Yuki goes on a trip to Kyoto with friends."),
    ("st2", "From Tokyo Station, we take the fast Shinkansen bullet train."),
    ("st3", "Outside the window, we can see the tall and beautiful Mount Fuji."),
    ("st4", "Arriving in Kyoto, we walk around ancient temples and shrines."),
    ("st5", "In the quiet garden, we take lots of beautiful photos."),
    ("st6", "For lunch, we take a train to the sea and eat delicious fish."),
    ("st7", "At the souvenir shop, we buy sweets for family and friends."),
    ("st8", "Traveling in Japan is full of fun and becomes wonderful memories."),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "假期里，由纪和朋友一起去京都旅行。"),
    ("st2", "从东京站出发，坐上飞速的新干线。"),
    ("st3", "车窗外，能看见高大优美的富士山。"),
    ("st4", "到达京都后，我们在古老的寺庙和神社漫步。"),
    ("st5", "在恬静的日式庭院里，拍了许多漂亮的照片。"),
    ("st6", "中午坐电车去看海，还品尝了鲜美的海鱼。"),
    ("st7", "在特产店里，给家人和朋友挑选了点心伴手礼。"),
    ("st8", "日本的旅行非常快乐，留下了美好难忘的回忆。"),
]

# 2. 课后生字表 (12 汉字)
CHARACTERS = [
    ("zi1", "旅"), ("zi2", "行"), ("zi3", "来"), ("zi4", "車"),
    ("zi5", "電"), ("zi6", "見"), ("zi7", "海"), ("zi8", "買"),
    ("zi9", "写"), ("zi10", "真"), ("zi11", "京"), ("zi12", "都"),
]

# 3. 课后单词表 (12 Words)
WORDS = [
    ("ci1", "旅行"), ("ci2", "新幹線"), ("ci3", "電車"), ("ci4", "東京"),
    ("ci5", "京都"), ("ci6", "富士山"), ("ci7", "写真"), ("ci8", "お寺"),
    ("ci9", "神社"), ("ci10", "お土産"), ("ci11", "海"), ("ci12", "思い出"),
]

# 4. 课后「交通与旅行」词表 (7 Transportation Words)
PROPER_NOUNS = [
    ("pn1", "新幹線"), ("pn2", "電車"), ("pn3", "バス"), ("pn4", "飛行機"),
    ("pn5", "切符"), ("pn6", "ホテル"), ("pn7", "楽しい"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "日本の旅は、とても楽しくて素晴らしい思い出になります。"),
]

# 6. 选词填空原声句子 (12 Sentences)
CLOZE_ITEMS = [
    ("cloze_1", "ゆうきは、休日に友達と京都へ旅行に行きます。"),
    ("cloze_2", "東京駅から、速い新幹線に乗ります。"),
    ("cloze_3", "窓の外に、高くて美しい富士山が見えます。"),
    ("cloze_4", "京都に着いて、古いお寺や神社を歩きます。"),
    ("cloze_5", "静かな庭で、綺麗な写真をたくさん撮ります。"),
    ("cloze_6", "お昼は、電車で海へ行って美味しい魚を食べます。"),
    ("cloze_7", "お土産の店で、家族や友達にお菓子を買います。"),
    ("cloze_8", "日本の旅は、とても楽しくて素晴らしい思い出になります。"),
    ("cloze_9", "駅で電車の切符を買いました。"),
    ("cloze_10", "あしたは飛行機で遠くへ行きます。"),
    ("cloze_11", "今夜は綺麗なホテルに泊まります。"),
    ("cloze_12", "友だちと一緒に旅行して、とても楽しいです。"),
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

    print("Done generating nihongo6 audio.")


if __name__ == "__main__":
    asyncio.run(main())
