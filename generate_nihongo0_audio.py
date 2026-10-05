#!/usr/bin/env python3
"""Generate real MP3 audio for the 《五十音とあいさつ》(nihongo0) learning game.

This is the foundational Level 0 (Kana & Greetings) course in the Japanese series,
providing a smooth runway before 《わたしの一週間》(nihongo.html).
Features Yuki (ゆうき) introducing the 50 sounds (あいうえお), essential daily
greetings (おはよう, こんにちは, こんばんは, ありがとう), and kana concepts.

Generates:
- audio/nihongo0/st1.mp3 .. st8.mp3       (8 story sentences, Japanese)
- audio/nihongo0/zi1.mp3 .. zi12.mp3      (12 生字: 日本語字文音声名言心口人)
- audio/nihongo0/ci1.mp3 .. ci12.mp3      (12 单词: ひらがな/カタカナ/あいさつ/おはよう/こんにちは/こんばんは/ありがとう/はじめまして/さようなら/五十音/声/笑顔)
- audio/nihongo0/pn1.mp3 .. pn7.mp3       (7 寒暄常用词: はい/いいえ/すみません/どうぞ/どうも/よろしく/じゃあね)
- audio/nihongo0/sent1.mp3                (课后重点句子)
- audio/nihongo0/cloze_1.mp3 .. 12.mp3    (12 选词填空完整句)
- audio/nihongo0_en/st1.mp3 .. st8.mp3    (8 story sentences, English translation)
- audio/nihongo0_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese bonus translation)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "nihongo0"
OUT_DIR_EN = ROOT / "audio" / "nihongo0_en"
OUT_DIR_ZH = ROOT / "audio" / "nihongo0_zh"
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
    ("st1", "あいうえお、日本語をはじめましょう。"),
    ("st2", "朝は「おはよう」と元気にあいさつします。"),
    ("st3", "昼は「こんにちは」と笑顔で言います。"),
    ("st4", "夜は「こんばんは」とあいさつします。"),
    ("st5", "感謝の気持ちで「ありがとう」と伝えます。"),
    ("st6", "かきくけこ、ひらがなを声に出して読みます。"),
    ("st7", "ひらがなとカタカナは、日本語のたいせつな基本です。"),
    ("st8", "さあ、みんなで楽しく五十音を学びましょう！"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "A-I-U-E-O, let's begin learning Japanese!"),
    ("st2", "In the morning, we greet cheerfully with 'Ohayou'."),
    ("st3", "In the daytime, we say 'Konnichiwa' with a bright smile."),
    ("st4", "In the evening, we greet warmly with 'Konbanwa'."),
    ("st5", "With a thankful heart, we express our gratitude with 'Arigatou'."),
    ("st6", "Ka-Ki-Ku-Ke-Ko, we read hiragana aloud with clear voices."),
    ("st7", "Hiragana and Katakana are the essential foundations of Japanese."),
    ("st8", "Come on, let's enjoy learning the fifty sounds together!"),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "あいうえお，让我们开始快乐地学日语吧。"),
    ("st2", "清晨时分，精神饱满地向大家问候“早上好”。"),
    ("st3", "白天相遇，面带微笑亲切地说“你好”。"),
    ("st4", "夜幕降临，道一声温和的“晚上好”。"),
    ("st5", "怀着由衷的感激，真诚地表达“谢谢”。"),
    ("st6", "かきくけこ，大声朗读清脆优美的平假名。"),
    ("st7", "平假名与片假名，是开启日语世界的关键基石。"),
    ("st8", "来吧，让我们一起轻松愉快地学习五十音！"),
]

# 2. 课后生字表 (12 汉字)
CHARACTERS = [
    ("zi1", "日"), ("zi2", "本"), ("zi3", "語"), ("zi4", "字"),
    ("zi5", "文"), ("zi6", "音"), ("zi7", "声"), ("zi8", "名"),
    ("zi9", "言"), ("zi10", "心"), ("zi11", "口"), ("zi12", "人"),
]

# 3. 课后单词表 (12 Words)
WORDS = [
    ("ci1", "ひらがな"), ("ci2", "カタカナ"), ("ci3", "あいさつ"), ("ci4", "おはよう"),
    ("ci5", "こんにちは"), ("ci6", "こんばんは"), ("ci7", "ありがとう"), ("ci8", "はじめまして"),
    ("ci9", "さようなら"), ("ci10", "五十音"), ("ci11", "声"), ("ci12", "笑顔"),
]

# 4. 课后「常用寒暄」词表 (7 Greeting Words)
PROPER_NOUNS = [
    ("pn1", "はい"), ("pn2", "いいえ"), ("pn3", "すみません"), ("pn4", "どうぞ"),
    ("pn5", "どうも"), ("pn6", "よろしく"), ("pn7", "じゃあね"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "笑顔であいさつするのは、とても大切です。"),
]

# 6. 选词填空完整朗读句子 (12 Cloze Sentences)
CLOZE_ITEMS = [
    ("cloze_1", "あいうえお、日本語をはじめましょう。"),
    ("cloze_2", "朝は「おはよう」と元気にあいさつします。"),
    ("cloze_3", "昼は「こんにちは」と笑顔で言います。"),
    ("cloze_4", "夜は「こんばんは」とあいさつします。"),
    ("cloze_5", "感謝の気持ちで「ありがとう」と伝えます。"),
    ("cloze_6", "かきくけこ、ひらがなを声に出して読みます。"),
    ("cloze_7", "ひらがなとカタカナは、日本語のたいせつな基本です。"),
    ("cloze_8", "さあ、みんなで楽しく五十音を学びましょう！"),
    ("cloze_9", "名前を聞かれたら、元気に「はい」と返事をします。"),
    ("cloze_10", "人に何かを渡すときは、「どうぞ」と言います。"),
    ("cloze_11", "別れるときは、笑顔で「さようなら」と言いましょう。"),
    ("cloze_12", "初めて会った人には、「はじめまして」と自己紹介します。"),
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

    print("Done generating nihongo0 audio.")


if __name__ == "__main__":
    asyncio.run(main())
