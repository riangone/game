#!/usr/bin/env python3
"""Generate real MP3 audio for the 《わたしの家族》(nihongo7) learning game.

Lesson 7 in the series, continuing from 《楽しい旅行》(nihongo6.html):
same character (ゆうき), same N5 difficulty, same edge-tts architecture.
Output folders:
- audio/nihongo7/       (Japanese: st1-8, zi1-12, ci1-12, pn1-7, sent1, cloze_1-12)
- audio/nihongo7_en/    (English story translations)
- audio/nihongo7_zh/    (Chinese story translations)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "nihongo7"
OUT_DIR_EN = ROOT / "audio" / "nihongo7_en"
OUT_DIR_ZH = ROOT / "audio" / "nihongo7_zh"
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
    ("st1", "ゆうきは、父と母と兄と妹の五人家族です。"),
    ("st2", "父は会社員で、毎朝電車で仕事に行きます。"),
    ("st3", "母は料理が上手で、毎日美味しいご飯を作ります。"),
    ("st4", "兄は高校生で、サッカーが大好きな男の子です。"),
    ("st5", "妹はまだ小さい女の子で、いつも元気に歌を歌います。"),
    ("st6", "家には、白くてかわいい犬も一匹います。"),
    ("st7", "日曜日は、家族みんなで公園へ散歩に行きます。"),
    ("st8", "優しい家族と一緒にいると、毎日がとても幸せです。"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "Yuki's family has five people: father, mother, older brother, younger sister, and Yuki."),
    ("st2", "My father is an office worker and goes to work by train every morning."),
    ("st3", "My mother is good at cooking and makes delicious meals every day."),
    ("st4", "My older brother is a high school student, a boy who loves soccer."),
    ("st5", "My younger sister is still a little girl and always sings cheerfully."),
    ("st6", "At home, we also have a cute white dog."),
    ("st7", "On Sundays, the whole family goes for a walk in the park."),
    ("st8", "Being together with my kind family makes every day very happy."),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "由纪家有五口人：爸爸、妈妈、哥哥、妹妹和由纪。"),
    ("st2", "爸爸是公司职员，每天早上坐电车去上班。"),
    ("st3", "妈妈很会做菜，每天都做好吃的饭菜。"),
    ("st4", "哥哥是高中生，是个超爱足球的男孩子。"),
    ("st5", "妹妹还是个小女孩，总是精神饱满地唱着歌。"),
    ("st6", "家里还有一只白白的、可爱的小狗。"),
    ("st7", "星期天，全家人一起去公园散步。"),
    ("st8", "和温柔的家人在一起，每一天都很幸福。"),
]

# 2. 课后生字表 (12 汉字)
CHARACTERS = [
    ("zi1", "父"),
    ("zi2", "母"),
    ("zi3", "兄"),
    ("zi4", "弟"),
    ("zi5", "妹"),
    ("zi6", "家"),
    ("zi7", "族"),
    ("zi8", "男"),
    ("zi9", "女"),
    ("zi10", "子"),
    ("zi11", "犬"),
    ("zi12", "仕"),
]

# 3. 课后单词表 (12 Words)
WORDS = [
    ("ci1", "家族"),
    ("ci2", "会社員"),
    ("ci3", "仕事"),
    ("ci4", "上手"),
    ("ci5", "高校生"),
    ("ci6", "男の子"),
    ("ci7", "女の子"),
    ("ci8", "歌"),
    ("ci9", "犬"),
    ("ci10", "日曜日"),
    ("ci11", "散歩"),
    ("ci12", "優しい"),
]

# 4. 课后「家族称呼」词表 (7 Family Terms)
PROPER_NOUNS = [
    ("pn1", "お父さん"),
    ("pn2", "お母さん"),
    ("pn3", "お兄さん"),
    ("pn4", "お姉さん"),
    ("pn5", "おじいさん"),
    ("pn6", "おばあさん"),
    ("pn7", "両親"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "優しい家族と一緒にいると、毎日がとても幸せです。"),
]

# 6. 选词填空原声句子 (12 Sentences)
CLOZE_ITEMS = [
    ("cloze_1", "ゆうきは、父と母と兄と妹の五人家族です。"),
    ("cloze_2", "父は会社員で、毎朝電車で仕事に行きます。"),
    ("cloze_3", "母は料理が上手で、毎日美味しいご飯を作ります。"),
    ("cloze_4", "兄は高校生で、サッカーが大好きな男の子です。"),
    ("cloze_5", "妹はまだ小さい女の子で、いつも元気に歌を歌います。"),
    ("cloze_6", "家には、白くてかわいい犬も一匹います。"),
    ("cloze_7", "日曜日は、家族みんなで公園へ散歩に行きます。"),
    ("cloze_8", "優しい家族と一緒にいると、毎日がとても幸せです。"),
    ("cloze_9", "わたしの弟は、小学生です。"),
    ("cloze_10", "田中さんのお母さんは、とても優しい人です。"),
    ("cloze_11", "おじいさんは毎朝公園を散歩します。"),
    ("cloze_12", "週末は両親と一緒に買い物に行きます。"),
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

    print("Done generating nihongo7 audio.")


if __name__ == "__main__":
    asyncio.run(main())
