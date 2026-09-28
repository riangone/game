#!/usr/bin/env python3
"""Generate real MP3 audio for 《拼音启蒙 ABC》(pinyin-abc.html).

v2: parses INITIALS / FINALS / MA_FAMILY / REAL_SYLLABLES directly out of
pinyin-abc.html (single source of truth, same principle used for the en/ja
story audio generators) instead of maintaining a hand-typed duplicate word
list that can silently drift from what the game actually displays/plays.

Uses edge-tts (Microsoft neural voices, free, no API key).

Filename scheme (must match playClip() call sites in pinyin-abc.html exactly):
- <ltr>.mp3            23 声母 phoneme demo (b -> "波", p -> "坡" ...)
- <ltr>_word.mp3        23 声母 memory word audio (text = INITIALS[].word)
- <finalKey>.mp3        23 韵母 phoneme demo (zero-initial reading; 'ong' has none)
                        finalKey: 'ü'->'v', 'üe'->'ve', 'ün'->'vn', else = f itself
- <finalKey>_word.mp3   24 韵母 memory word audio (text = FINALS[].word)
- ma1..ma4.mp3          4 声调 "妈麻马骂" family (text = MA_FAMILY[].zh)
- <toneAscii><n>.mp3    24 tone-matrix / tone-quiz syllables, toneAscii in a/o/e/i/u/v,
                        n in 1..4 (text = the actual tone-marked vowel, e.g. "ā")
- <s>.mp3               REAL_SYLLABLES entries (text = the associated character, for
                        an unambiguous correct tone, not the toneless romanization)
"""
import asyncio
import re
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT / "pinyin-abc.html"
OUT_DIR = ROOT / "audio" / "pinyinbasics"
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
# back to ~327Hz, close to its own tone-1/2/4 register) so it is used for
# the two explicit tone-comparison families (ma1-4 and the a/o/e/i/u/v
# tone-matrix), keeping each 4-tone family internally consistent in one
# voice rather than mixing voices mid-comparison.
TONE_VOICE = VOICE  # reverted: XiaoyiNeural fixed tone-3's rise but made ALL
# four tones sound mechanical/robotic per user listening test — the pitch-
# contour probe only measured F0 shape, not perceptual naturalness. Voice
# swap abandoned; back to a single consistent voice across the whole game.

html = HTML_PATH.read_text(encoding="utf-8")


def extract_block(name):
    m = re.search(r"const %s = \[(.*?)\n\];" % re.escape(name), html, re.S)
    if not m:
        raise RuntimeError(f"could not find `const {name} = [...]` in {HTML_PATH.name}")
    return m.group(1)


initials = re.findall(r"ltr:'([^']+)'.*?word:'([^']+)'", extract_block("INITIALS"))
finals = re.findall(r"f:'([^']+)'.*?word:'([^']+)'", extract_block("FINALS"))
ma_family = re.findall(r"tone:(\d+),zh:'([^']+)'", extract_block("MA_FAMILY"))
real_syllables = re.findall(r"s:'([^']+)',ch:'([^']+)'", extract_block("REAL_SYLLABLES"))

assert len(initials) == 23, f"expected 23 INITIALS, parsed {len(initials)}"
assert len(finals) == 24, f"expected 24 FINALS, parsed {len(finals)}"
assert len(ma_family) == 4, f"expected 4 MA_FAMILY, parsed {len(ma_family)}"
assert len(real_syllables) >= 40, f"expected ~48 REAL_SYLLABLES, parsed {len(real_syllables)}"

# ---- fixed pinyin knowledge (not display data -> low drift risk, hardcoded) ----
INITIAL_DEMO = {
    "b": "波", "p": "坡", "m": "摸", "f": "佛", "d": "得", "t": "特", "n": "讷", "l": "了",
    "g": "哥", "k": "科", "h": "喝", "j": "基", "q": "七", "x": "西",
    "zh": "知", "ch": "吃", "sh": "诗", "r": "日", "z": "资", "c": "疵", "s": "思",
    "y": "衣", "w": "屋",
}
FINAL_DEMO = {
    "a": "啊", "o": "哦", "e": "鹅", "i": "衣", "u": "屋", "ü": "淤",
    "ai": "哀", "ei": "诶", "ui": "威", "ao": "熬", "ou": "欧", "iu": "忧",
    "ie": "耶", "üe": "约", "er": "儿", "an": "安", "en": "恩", "in": "因",
    "un": "温", "ün": "晕", "ang": "昂", "eng": "鞥", "ing": "英", "ong": None,
}
FINAL_ASCII = {"ü": "v", "üe": "ve", "ün": "vn"}
TONE_MAP = {
    "a": ["ā", "á", "ǎ", "à"], "o": ["ō", "ó", "ǒ", "ò"], "e": ["ē", "é", "ě", "è"],
    "i": ["ī", "í", "ǐ", "ì"], "u": ["ū", "ú", "ǔ", "ù"], "ü": ["ǖ", "ǘ", "ǚ", "ǜ"],
}
TONE_ASCII = {"a": "a", "o": "o", "e": "e", "i": "i", "u": "u", "ü": "v"}
# Scheme B: Contextual Prompting & Hanzi Anchors for accurate 4 tones
# 1声(高平55): 采用长音或高平汉字保持平稳，避免句尾降调下坠
# 2声(中升35): 采用纯正阳平汉字或疑问语境诱导自然爬升
# 3声(降升214): 采用拐弯语境「？」打破神经TTS孤立词默认半三声(211只降不升)缺陷，诱发饱满的先降后升
# 4声(全降51): 采用感叹或纯正去声汉字，干脆下坠
TONE_TEXT_OVERRIDE = {
    "a": ["啊——", "啊？", "哑？", "啊！"],
    "o": ["喔——", "喔？", "哦……", "哦！"],
    "e": ["婀——", "鹅", "恶", "饿"],
    "i": ["一", "姨", "椅？", "意"],
    "u": ["乌", "无", "五？", "雾"],
    "ü": ["迂", "鱼", "雨？", "玉"],
}
MA_PROMPT_OVERRIDE = {
    1: "妈",
    2: "麻",
    3: "马？",
    4: "骂",
}


def final_key(f):
    return FINAL_ASCII.get(f, f)


items = {}  # filename (no ext) -> spoken text

for ltr, word in initials:
    demo = INITIAL_DEMO.get(ltr)
    if demo:
        items[ltr] = demo
    items[f"{ltr}_word"] = word

for f, word in finals:
    demo = FINAL_DEMO.get(f)
    key = final_key(f)
    if demo:
        items[key] = demo
    items[f"{key}_word"] = word

for tone, zh in ma_family:
    items[f"ma{tone}"] = MA_PROMPT_OVERRIDE.get(int(tone), zh)

for vowel, marks in TONE_MAP.items():
    ascii_v = TONE_ASCII[vowel]
    overrides = TONE_TEXT_OVERRIDE.get(vowel)
    for i, mark in enumerate(marks, start=1):
        items[f"{ascii_v}{i}"] = overrides[i - 1] if overrides else mark

for s, ch in real_syllables:
    items[s] = ch

# keys that get TONE_VOICE instead of VOICE: the two explicit 4-tone
# comparison families (see TONE_VOICE comment above)
TONE_FAMILY_KEYS = {f"ma{n}" for n in range(1, 5)} | {
    f"{TONE_ASCII[v]}{i}" for v in TONE_MAP for i in range(1, 5)
}

print(f"Parsed from {HTML_PATH.name}: {len(initials)} initials, {len(finals)} finals, "
      f"{len(ma_family)} ma-family, {len(real_syllables)} real syllables")
print(f"-> {len(items)} audio files to generate into {OUT_DIR}")


async def main():
    sem = asyncio.Semaphore(4)

    async def generate_one(fname, text):
        target = OUT_DIR / f"{fname}.mp3"
        voice = TONE_VOICE if fname in TONE_FAMILY_KEYS else VOICE
        try:
            async with sem:
                comm = edge_tts.Communicate(text, voice, rate=RATE)
                await comm.save(str(target))
            if target.exists() and target.stat().st_size > 300:
                print(f"OK   {fname}.mp3  ({text})")
            else:
                print(f"WARN {fname}.mp3 looks too small ({text})")
        except Exception as e:
            print(f"FAIL {fname} ({text}): {e}")

    await asyncio.gather(*(generate_one(f, t) for f, t in items.items()))
    print("Done generating pinyinbasics audio.")


if __name__ == "__main__":
    asyncio.run(main())
