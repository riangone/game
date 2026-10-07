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

# 1. 课文逐句 (Story sentences, Japanese - 以假名为主的初阶入门课文)
STORY = [
    ("st1", "あいうえお、はじめまして。"),
    ("st2", "あさは 「おはよう」 と げんきに あいさつします。"),
    ("st3", "ひるは 「こんにちは」 と えがおで いいます。"),
    ("st4", "よるは 「こんばんは」 と あいさつします。"),
    ("st5", "こころを こめて 「ありがとう」 と つたえます。"),
    ("st6", "かきくけこ、さしすせそ、こえに だして よみます。"),
    ("st7", "ひらがなと カタカナ、たのしく おぼえましょう。"),
    ("st8", "さあ、みんなで ごじゅうおんを まなびましょう！"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "A-I-U-E-O, nice to meet you!"),
    ("st2", "In the morning, we greet cheerfully with 'Ohayou'."),
    ("st3", "In the daytime, we say 'Konnichiwa' with a bright smile."),
    ("st4", "In the evening, we greet warmly with 'Konbanwa'."),
    ("st5", "From the bottom of our hearts, we say 'Thank you'."),
    ("st6", "Ka-Ki-Ku-Ke-Ko, Sa-Shi-Su-Se-So, we read aloud with clear voices."),
    ("st7", "Let's enjoy learning hiragana and katakana together!"),
    ("st8", "Come on, let's learn the fifty sounds together!"),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "あいうえお，初次见面！"),
    ("st2", "清晨时分，精神饱满地问候“早上好”。"),
    ("st3", "白天相遇，面带微笑亲切地说“你好”。"),
    ("st4", "夜幕降临，道一声温和的“晚上好”。"),
    ("st5", "怀着由衷的心意，真诚地说一声“谢谢”。"),
    ("st6", "かきくけこ、さしすせそ，大声朗读清脆的假名。"),
    ("st7", "平假名与片假名，轻松愉快地记在心里吧。"),
    ("st8", "来吧，让我们一起快乐地学习五十音！"),
]

# 2. 课后核心假名字表 (12 核心假名：5母音 + 高频清音/拨音)
CHARACTERS = [
    ("zi1", "あ"), ("zi2", "い"), ("zi3", "う"), ("zi4", "え"),
    ("zi5", "お"), ("zi6", "か"), ("zi7", "さ"), ("zi8", "た"),
    ("zi9", "な"), ("zi10", "は"), ("zi11", "ま"), ("zi12", "ん"),
]

# 3. 课后单词表 (12 Words - 全假名化，便于假名初学者认读)
WORDS = [
    ("ci1", "ひらがな"), ("ci2", "カタカナ"), ("ci3", "ごじゅうおん"), ("ci4", "あいさつ"),
    ("ci5", "おはよう"), ("ci6", "こんにちは"), ("ci7", "こんばんは"), ("ci8", "ありがとう"),
    ("ci9", "はじめまして"), ("ci10", "さようなら"), ("ci11", "こえ"), ("ci12", "えがお"),
]

# 4. 课后「常用寒暄」词表 (7 Greeting Words - 纯假名高频表达)
PROPER_NOUNS = [
    ("pn1", "はい"), ("pn2", "いいえ"), ("pn3", "すみません"), ("pn4", "どうぞ"),
    ("pn5", "どうも"), ("pn6", "よろしく"), ("pn7", "じゃあね"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "えがおで あいさつするのは、とても たいせつです。"),
]

# 6. 选词填空完整朗读句子 (12 Cloze Sentences - 纯假名语境)
CLOZE_ITEMS = [
    ("cloze_1", "あいうえお、はじめまして。"),
    ("cloze_2", "あさは 「おはよう」 と げんきに あいさつします。"),
    ("cloze_3", "ひるは 「こんにちは」 と えがおで いいます。"),
    ("cloze_4", "よるは 「こんばんは」 と あいさつします。"),
    ("cloze_5", "こころを こめて 「ありがとう」 と つたえます。"),
    ("cloze_6", "かきくけこ、さしすせそ、こえに だして よみます。"),
    ("cloze_7", "ひらがなと カタカナ、たのしく おぼえましょう。"),
    ("cloze_8", "さあ、みんなで ごじゅうおんを まなびましょう！"),
    ("cloze_9", "なまえを よばれたら、げんきに 「はい」 と 返事をします。"),
    ("cloze_10", "ひとに ものを わたすときは、「どうぞ」 と 言います。"),
    ("cloze_11", "ともだちと わかれるときは、「じゃあね」 と 言いましょう。"),
    ("cloze_12", "ひとに こえを かけるときは、「すみません」 と 言います。"),
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
