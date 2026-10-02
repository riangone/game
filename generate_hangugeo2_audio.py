#!/usr/bin/env python3
"""Generate real MP3 audio for the 《나의 하루》(hangugeo2) Korean learning game.

This is lesson 2 in the series, continuing directly from 《나의 일주일》
(hangugeo.html / generate_hangugeo_audio.py): same character (민우), same
TOPIK 1 / A1 difficulty, same edge-tts architecture:
- Korean main narration (ko-KR-SunHiNeural)
- English translation (en-US-JennyNeural)
- Chinese translation (zh-CN-XiaoxiaoNeural)

Generates:
- audio/hangugeo2/st1.mp3 .. st8.mp3       (8 story sentences, Korean)
- audio/hangugeo2/zi1.mp3 .. zi12.mp3      (12 核心音节字块: 아침세수밥반인사점실관저)
- audio/hangugeo2/ci1.mp3 .. ci12.mp3      (12 核心单词: 세수, 인사, 점심, 교실, ...)
- audio/hangugeo2/pn1.mp3 .. pn7.mp3       (7 时间词: 아침, 점심, 저녁, 밤, 일곱 시, 여덟 시 반, 아홉 시)
- audio/hangugeo2/sent1.mp3                (课后重点句子)
- audio/hangugeo2_en/st1.mp3 .. st8.mp3    (8 story sentences, English translation)
- audio/hangugeo2_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese bonus translation)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "hangugeo2"
OUT_DIR_EN = ROOT / "audio" / "hangugeo2_en"
OUT_DIR_ZH = ROOT / "audio" / "hangugeo2_zh"
for d in (OUT_DIR, OUT_DIR_EN, OUT_DIR_ZH):
    d.mkdir(parents=True, exist_ok=True)

KO_VOICE = "ko-KR-SunHiNeural"
EN_VOICE = "en-US-JennyNeural"
ZH_VOICE = "zh-CN-XiaoxiaoNeural"
KO_RATE = "-5%"
EN_RATE = "-8%"
ZH_RATE = "-10%"

# 1. 课文逐句 (Story sentences, Korean)
STORY = [
    ("st1", "민우는 아침 일곱 시에 일어납니다."),
    ("st2", "세수를 하고 아침밥을 맛있게 먹어요."),
    ("st3", "여덟 시 반에 집을 나와서 학교에 갑니다."),
    ("st4", "학교에서 친구들과 인사하고 즐겁게 이야기해요."),
    ("st5", "점심시간에는 교실에서 친구와 도시락을 먹습니다."),
    ("st6", "방과 후에 도서관에서 재미있는 책을 읽어요."),
    ("st7", "저녁에 집에 돌아와 가족과 저녁밥을 먹습니다."),
    ("st8", "밤 아홉 시에 잠을 잡니다. 내일도 파이팅!"),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "Minwoo wakes up at seven in the morning."),
    ("st2", "After washing my face, I eat breakfast deliciously."),
    ("st3", "I leave home at eight thirty and go to school."),
    ("st4", "At school, I greet my friends and talk happily."),
    ("st5", "During lunchtime, I eat lunchbox with friends in the classroom."),
    ("st6", "After school, I read interesting books in the library."),
    ("st7", "In the evening, I return home and have dinner with my family."),
    ("st8", "I go to sleep at nine at night. Fighting tomorrow too!"),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "敏宇早上七点起床。"),
    ("st2", "洗脸之后，津津有味地吃早饭。"),
    ("st3", "八点半出门，去学校。"),
    ("st4", "在学校和朋友们打招呼，开心地聊天。"),
    ("st5", "午休时间，在教室里和朋友一起吃便当。"),
    ("st6", "放学后，在图书馆看有趣的书。"),
    ("st7", "晚上回到家，和家人一起吃晚饭。"),
    ("st8", "晚上九点睡觉。明天也要加油！"),
]

# 2. 课后核心音节字块 (12 Syllable Blocks)
CHARACTERS = [
    ("zi1", "아"), ("zi2", "침"), ("zi3", "세"), ("zi4", "수"),
    ("zi5", "밥"), ("zi6", "반"), ("zi7", "인"), ("zi8", "사"),
    ("zi9", "점"), ("zi10", "실"), ("zi11", "관"), ("zi12", "저"),
]

# 3. 课后核心单词 (12 Words)
WORDS = [
    ("ci1", "세수"), ("ci2", "인사"), ("ci3", "점심"), ("ci4", "교실"),
    ("ci5", "도시락"), ("ci6", "도서관"), ("ci7", "아침밥"), ("ci8", "저녁밥"),
    ("ci9", "방과 후"), ("ci10", "이야기"), ("ci11", "내일"), ("ci12", "파이팅"),
]

# 4. 课后「时间」词表 (7 Time Words)
PROPER_NOUNS = [
    ("pn1", "아침"), ("pn2", "점심"), ("pn3", "저녁"), ("pn4", "밤"),
    ("pn5", "일곱 시"), ("pn6", "여덟 시 반"), ("pn7", "아홉 시"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "매일 아침 일찍 일어나는 것은 상쾌해요."),
]

KO_ITEMS = STORY + CHARACTERS + WORDS + PROPER_NOUNS + KEY_SENTENCE


async def synth(text, voice, rate, out_path):
    if out_path.exists() and out_path.stat().st_size > 500:
        return
    try:
        comm = edge_tts.Communicate(text, voice, rate=rate)
        await comm.save(str(out_path))
    except Exception as e:
        print(f"FAIL {out_path.name}: {e}")


async def main():
    print(f"[1/3] Synthesizing {len(KO_ITEMS)} Korean clips with {KO_VOICE}...")
    sem = asyncio.Semaphore(5)

    async def run_ko(fn, txt):
        async with sem:
            await synth(txt, KO_VOICE, KO_RATE, OUT_DIR / f"{fn}.mp3")

    await asyncio.gather(*(run_ko(fn, txt) for fn, txt in KO_ITEMS))
    print(f"      -> Korean audio done. {len(list(OUT_DIR.glob('*.mp3')))} files.")

    print(f"[2/3] Synthesizing {len(STORY_EN)} English clips with {EN_VOICE}...")
    async def run_en(fn, txt):
        async with sem:
            await synth(txt, EN_VOICE, EN_RATE, OUT_DIR_EN / f"{fn}.mp3")

    await asyncio.gather(*(run_en(fn, txt) for fn, txt in STORY_EN))
    print(f"      -> English audio done. {len(list(OUT_DIR_EN.glob('*.mp3')))} files.")

    print(f"[3/3] Synthesizing {len(STORY_ZH)} Chinese clips with {ZH_VOICE}...")
    async def run_zh(fn, txt):
        async with sem:
            await synth(txt, ZH_VOICE, ZH_RATE, OUT_DIR_ZH / f"{fn}.mp3")

    await asyncio.gather(*(run_zh(fn, txt) for fn, txt in STORY_ZH))
    print(f"      -> Chinese audio done. {len(list(OUT_DIR_ZH.glob('*.mp3')))} files.")
    print("All audio generated successfully!")


if __name__ == "__main__":
    asyncio.run(main())
