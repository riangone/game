#!/usr/bin/env python3
"""Generate real MP3 audio for the 《わたしの町》(nihongo4) learning game.

This is lesson 4 in the series, continuing directly from 《日本の四季》
(nihongo3.html / generate_nihongo3_audio.py): same character (ゆうき), same
N5 difficulty, same edge-tts architecture — output folders:
- audio/nihongo4/       (Japanese)
- audio/nihongo4_en/    (English translations)
- audio/nihongo4_zh/    (Chinese translations)

Generates:
- audio/nihongo4/st1.mp3 .. st8.mp3       (8 story sentences, Japanese)
- audio/nihongo4/zi1.mp3 .. zi12.mp3      (12 生字: 町店前中外左右住近道古新)
- audio/nihongo4/ci1.mp3 .. ci12.mp3      (12 单词)
- audio/nihongo4/pn1.mp3 .. pn7.mp3       (7 方位空间词: 前/後ろ/中/外/左/右/近く)
- audio/nihongo4/sent1.mp3                (课后重点句子)
- audio/nihongo4_en/st1.mp3 .. st8.mp3    (8 story sentences, English)
- audio/nihongo4_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "nihongo4"
OUT_DIR_EN = ROOT / "audio" / "nihongo4_en"
OUT_DIR_ZH = ROOT / "audio" / "nihongo4_zh"
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
    ("st1", "ゆうきは、静かで便利な町に住んでいます。"),
    ("st2", "駅の前には、大きな店や銀行があります。"),
    ("st3", "毎日、賑やかな商店街を歩いて学校へ行きます。"),
    ("st4", "道の近くに、古い本屋と小さな喫茶店があります。"),
    ("st5", "公園の中には、緑の木や綺麗な花があります。"),
    ("st6", "家の外に出ると、親切な人たちに会います。"),
    ("st7", "交番の右に郵便局があり、左に病院があります。"),
    ("st8", "新しい出会いと笑顔が溢れるこの町が大好きです。"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "Yuki lives in a quiet and convenient town."),
    ("st2", "In front of the station, there are large shops and banks."),
    ("st3", "Every day, I walk through the bustling shopping street to go to school."),
    ("st4", "Near the street, there is an old bookstore and a small café."),
    ("st5", "Inside the park, there are green trees and beautiful flowers."),
    ("st6", "When I go outside my house, I meet kind people."),
    ("st7", "To the right of the police box is the post office, and to the left is the hospital."),
    ("st8", "I love this town, full of new encounters and smiles."),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "由纪住在一个安静而便利的小城镇。"),
    ("st2", "车站前面有大型商店和银行。"),
    ("st3", "每天穿过热闹的商店街步行去上学。"),
    ("st4", "街道附近有一家老书店和一家小咖啡馆。"),
    ("st5", "公园里有绿色的树木和美丽的花朵。"),
    ("st6", "走出家门，就会遇见亲切热情的邻里。"),
    ("st7", "岗亭右边是邮局，左边是医院。"),
    ("st8", "充满崭新相遇与灿烂欢笑的这个小镇，我非常喜欢。"),
]

# 2. 课后生字表 (12 汉字)
CHARACTERS = [
    ("zi1", "町"), ("zi2", "店"), ("zi3", "前"), ("zi4", "中"),
    ("zi5", "外"), ("zi6", "左"), ("zi7", "右"), ("zi8", "住"),
    ("zi9", "近"), ("zi10", "道"), ("zi11", "古"), ("zi12", "新"),
]

# 3. 课后单词表 (12 Words)
WORDS = [
    ("ci1", "駅"), ("ci2", "銀行"), ("ci3", "病院"), ("ci4", "郵便局"),
    ("ci5", "本屋"), ("ci6", "喫茶店"), ("ci7", "公園"), ("ci8", "交番"),
    ("ci9", "商店街"), ("ci10", "便利"), ("ci11", "賑やか"), ("ci12", "親切"),
]

# 4. 课后「方位与位置」词表 (7 Location Words)
PROPER_NOUNS = [
    ("pn1", "前"), ("pn2", "後ろ"), ("pn3", "中"), ("pn4", "外"),
    ("pn5", "左"), ("pn6", "右"), ("pn7", "近く"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "わたしの町は、静かで便利で、とても住みやすいです。"),
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
