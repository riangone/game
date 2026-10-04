#!/usr/bin/env python3
"""Generate real MP3 audio for the 《拼音基础乐园》(pinyin-basics.html) learning game.

NOTE: output directory is audio/pinyin-basics/ (with hyphen) — intentionally
distinct from audio/pinyinbasics/ (no hyphen), which is used by a different
sibling game (pinyin-abc.html) with its own filename scheme. Keeping separate
directories avoids two independently-generated asset sets clobbering each
other's same-named files.

Uses edge-tts (Microsoft neural voices, free, no API key).

Produces:
- init_<code>_demo.mp3   23 声母 demo syllables (b->"bo", zh->"zhi" etc, official textbook pairing)
- init_<code>_word.mp3   23 memory words, one per 声母
- final_<code>_pure.mp3  standalone zero-initial reading of 23/24 韵母 (ong has no zero-initial form)
- final_<code>_word.mp3  24 memory words, one per 韵母
- tone_<base>_<n>.mp3    4 tone-practice syllable families (ma/yi/wu/shu), n = 1/2/3/4/0(neutral)
- syl_<key>.mp3          24 拼读练习 target characters (声母+韵母+声调 combined)
"""
import asyncio
from pathlib import Path
import edge_tts

OUT_DIR = Path(__file__).resolve().parent / "audio" / "pinyin-basics"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-15%"  # slower, extra clarity for absolute beginners

# Isolated-syllable 3rd-tone (上声, 214 dip-then-rise) fix: measured via a
# custom autocorrelation F0 probe (analyze_pitch.py) that XiaoxiaoNeural's
# citation-form single-character rendering realizes 3rd tone with a real
# dip but a very weak/short compensatory rise (e.g. 马 fell 239->200Hz then
# only recovered to ~250Hz), which reads as "not standard" next to the
# textbook 214 contour taught in class. zh-CN-XiaoyiNeural measured a much
# fuller recovery on the same characters (e.g. 椅 fell 258->239Hz then rose
# back to ~327Hz, close to its own tone-1/2/4 register), so it is used for
# the four explicit tone-comparison families below (ma/yi/wu/shu), keeping
# each 4-5-tone family internally consistent in one voice rather than
# mixing voices mid-comparison.
TONE_VOICE = VOICE  # reverted: XiaoyiNeural fixed tone-3's rise but made ALL
# four tones sound mechanical/robotic per user listening test — the pitch-
# contour probe only measured F0 shape, not perceptual naturalness. Voice
# swap abandoned; back to a single consistent voice across the whole game.

# ---------------------------------------------------------------- 声母 23
# (code, demo-syllable text, memory word)
INITIALS = [
    ("b", "波", "爸爸"),
    ("p", "坡", "皮球"),
    ("m", "摸", "妈妈"),
    ("f", "fō", "飞机"),
    ("d", "dē", "蛋糕"),
    ("t", "特", "兔子"),
    ("n", "讷", "牛奶"),
    ("l", "了", "老虎"),
    ("g", "哥", "哥哥"),
    ("k", "科", "咖啡"),
    ("h", "喝", "河马"),
    ("j", "基", "鸡蛋"),
    ("q", "七", "铅笔"),
    ("x", "西", "西瓜"),
    ("zh", "知", "蜘蛛"),
    ("ch", "吃", "长城"),
    ("sh", "诗", "狮子"),
    ("r", "日", "人"),
    ("z", "资", "足球"),
    ("c", "疵", "草莓"),
    ("s", "思", "松鼠"),
    ("y", "衣", "月亮"),
    ("w", "屋", "乌龟"),
]

# ---------------------------------------------------------------- 韵母 24
# (code, zero-initial standalone reading or None, memory word)
FINALS = [
    ("a", "啊", "阿姨"),
    ("o", "哦", "菠萝"),
    ("e", "鹅", "鹅"),
    ("i", "衣", "一"),
    ("u", "屋", "五"),
    ("v", "淤", "鱼"),
    ("ai", "哀", "奶奶"),
    ("ei", "诶", "黑板"),
    ("ui", "威", "水"),
    ("ao", "熬", "猫"),
    ("ou", "欧", "猴子"),
    ("iu", "忧", "牛"),
    ("ie", "耶", "蝴蝶"),
    ("ve", "约", "雪"),
    ("er", "儿", "耳朵"),
    ("an", "安", "三"),
    ("en", "恩", "门"),
    ("in", "因", "心"),
    ("un", "温", "云"),
    ("vn", "晕", "裙子"),
    ("ang", "昂", "大象"),
    ("eng", "鞥", "风"),
    ("ing", "英", "星星"),
    ("ong", None, "熊"),
]

# ---------------------------------------------------------------- 声调练习 (单韵母与音节家族)
TONES = [
    ("a", [("1", "啊——"), ("2", "啊？"), ("3", "哑？"), ("4", "啊！")]),
    ("o", [("1", "喔——"), ("2", "喔？"), ("3", "哦……"), ("4", "哦！")]),
    ("e", [("1", "婀——"), ("2", "鹅"), ("3", "恶"), ("4", "饿")]),
    ("i", [("1", "一"), ("2", "姨"), ("3", "椅？"), ("4", "意")]),
    ("u", [("1", "乌"), ("2", "无"), ("3", "五？"), ("4", "雾")]),
    ("v", [("1", "淤"), ("2", "鱼"), ("3", "雨？"), ("4", "玉")]),
    ("ma", [("1", "妈"), ("2", "麻"), ("3", "马？"), ("4", "骂"), ("0", "吗")]),
    ("yi", [("1", "一"), ("2", "姨"), ("3", "椅？"), ("4", "意")]),
    ("wu", [("1", "乌"), ("2", "无"), ("3", "五？"), ("4", "雾")]),
    ("shu", [("1", "书"), ("2", "熟"), ("3", "鼠？"), ("4", "树")]),
]

# ---------------------------------------------------------------- 16 整体认读音节
OVERALL_SYLLABLES = [
    ("zhi", "知"), ("chi", "吃"), ("shi", "诗"), ("ri", "日"),
    ("zi", "资"), ("ci", "刺"), ("si", "思"), ("yi", "衣"),
    ("wu", "屋"), ("yu", "鱼"), ("ye", "耶"), ("yue", "月"),
    ("yuan", "圆"), ("yin", "因"), ("yun", "云"), ("ying", "英"),
]

# ---------------------------------------------------------------- 拼读练习 24
SPELL_ITEMS = [
    ("ba1", "八"), ("pa2", "爬"), ("ma1", "妈"), ("tu4", "兔"),
    ("ku3", "苦"), ("ge1", "歌"), ("he2", "河"), ("ji1", "鸡"),
    ("qi2", "骑"), ("xi1", "西"), ("zhi1", "知"), ("chi1", "吃"),
    ("shi4", "是"), ("ri4", "日"), ("zai4", "在"), ("cao3", "草"),
    ("san1", "三"), ("yang2", "羊"), ("wan2", "玩"), ("niu2", "牛"),
    ("lao3", "老"), ("fei1", "飞"), ("ping2", "瓶"), ("da4", "大"),
]

# ---------------------------------------------------------------- 拼音儿歌口诀
CHANTS = [
    ("chant_a", "张大嘴巴 ɑ ɑ ɑ，圆圆嘴巴 o o o，白鹅倒影 e e e，牙齿对齐 i i i，嘴巴突出 u u u，吹起口哨 ü ü ü。"),
    ("chant_b", "右下半圆 b b b，右上半圆 p p p，两个门洞 m m m，一根拐棍 f f f，左下半圆 d d d，伞柄朝下 t t t，一个门洞 n n n，一根小棍 l l l。"),
    ("chant_tone", "一声平平高又高，二声就像上山坡，三声下坡又上坡，四声就像下山坡。"),
    ("chant_mark", "有 a 不放过，没 a 找 o、e，i、u 并列标在后，单个韵母不用说。"),
    ("chant_jqx", "小 ü 见到 j q x，脱帽行礼笑嘻嘻，去掉两点还读 ü。"),
    ("chant_zh", "zh、ch、sh、r 舌尖翘，z、c、s 舌尖平。"),
]

# ---------------------------------------------------------------- 田字格描红标杆字
CHARS = [
    ("b", "八，拼音 bā"), ("p", "皮，拼音 pí"), ("m", "马，拼音 mǎ"), ("f", "飞，拼音 fēi"),
    ("d", "大，拼音 dà"), ("t", "土，拼音 tǔ"), ("a", "啊，拼音 à"), ("o", "哦，拼音 ó"),
    ("e", "鹅，拼音 é"), ("i", "衣，拼音 yī"), ("u", "乌，拼音 wū"), ("v", "鱼，拼音 yú")
]

ITEMS = []
for code, demo, word in INITIALS:
    ITEMS.append((f"init_{code}_demo", demo))
    ITEMS.append((f"init_{code}_word", word))
for code, pure, word in FINALS:
    if pure:
        ITEMS.append((f"final_{code}_pure", pure))
    ITEMS.append((f"final_{code}_word", word))
TONE_FAMILY_KEYS = set()
for base, entries in TONES:
    for n, char in entries:
        key = f"tone_{base}_{n}"
        ITEMS.append((key, char))
        TONE_FAMILY_KEYS.add(key)
for key, char in SPELL_ITEMS:
    ITEMS.append((f"syl_{key}", char))
for ovr, char in OVERALL_SYLLABLES:
    ITEMS.append((f"overall_{ovr}", char))
for cid, text in CHANTS:
    ITEMS.append((cid, text))
for letter, text in CHARS:
    ITEMS.append((f"char_{letter}", text))


async def main():
    print(f"Generating {len(ITEMS)} audio files into {OUT_DIR} ...")
    sem = asyncio.Semaphore(4)

    async def generate_one(fname, text):
        target = OUT_DIR / f"{fname}.mp3"
        # Protect human-derived audio assets from being clobbered by lower-quality TTS
        if fname.startswith("tone_o_") or fname == "final_o_pure":
            human_o = ROOT / "audio" / "human-pinyin" / (f"o{fname[-1]}.mp3" if fname.startswith("tone_o_") else "o1.mp3")
            if human_o.exists():
                target.write_bytes(human_o.read_bytes())
                print(f"SKIP (Preserved human-derived) {fname}.mp3")
                return
        voice = TONE_VOICE if fname in TONE_FAMILY_KEYS else VOICE
        try:
            async with sem:
                comm = edge_tts.Communicate(text, voice, rate=RATE)
                await comm.save(str(target))
            if target.exists() and target.stat().st_size > 300:
                print(f"OK  {fname}.mp3  ({text})")
            else:
                print(f"WARN {fname}.mp3 looks too small")
        except Exception as e:
            print(f"FAIL {fname}: {e}")

    await asyncio.gather(*(generate_one(f, t) for f, t in ITEMS))
    print("Done generating pinyin-basics audio.")


if __name__ == "__main__":
    asyncio.run(main())
