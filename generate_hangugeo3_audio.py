#!/usr/bin/env python3
"""Generate real MP3 audio for the 《맛있는 한국 음식》(hangugeo3) Korean learning game.

This is lesson 3 in the series, continuing directly from:
- Lesson 1: 《나의 일주일》(hangugeo.html / generate_hangugeo_audio.py)
- Lesson 2: 《나의 하루》(hangugeo2.html / generate_hangugeo2_audio.py)

Same character (민우), same TOPIK 1 / A1 difficulty, same edge-tts architecture:
- Korean main narration (ko-KR-SunHiNeural)
- English translation (en-US-JennyNeural)
- Chinese translation (zh-CN-XiaoxiaoNeural)

Generates:
- audio/hangugeo3/st1.mp3 .. st8.mp3       (8 story sentences, Korean)
- audio/hangugeo3/zi1.mp3 .. zi12.mp3      (12 核心音节字块: 맛음식장떡김주문물복행말)
- audio/hangugeo3/ci1.mp3 .. ci12.mp3      (12 核心单词: 시장, 음식, 분식집, 주문, ...)
- audio/hangugeo3/pn1.mp3 .. pn7.mp3       (7 韩国美食专词: 떡볶이, 김밥, 어묵, 호떡, 비빔밥, 라면, 물냉면)
- audio/hangugeo3/sent1.mp3                (课后重点句子)
- audio/hangugeo3_en/st1.mp3 .. st8.mp3    (8 story sentences, English translation)
- audio/hangugeo3_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese bonus translation)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "hangugeo3"
OUT_DIR_EN = ROOT / "audio" / "hangugeo3_en"
OUT_DIR_ZH = ROOT / "audio" / "hangugeo3_zh"
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
    ("st1", "주말에 친구와 함께 전통시장에 갑니다."),
    ("st2", "시장에는 맛있는 음식이 정말 많습니다."),
    ("st3", "우리는 분식집에서 떡볶이와 김밥을 주문해요."),
    ("st4", "매콤하고 달콤한 떡볶이가 아주 맛있어요."),
    ("st5", "따뜻한 어묵 국물도 한 컵 마십니다."),
    ("st6", "후식으로 달콤하고 바삭한 호떡을 사 먹어요."),
    ("st7", "이모님, 정말 잘 먹었습니다! 인사해요."),
    ("st8", "배도 부르고 기분도 참 행복합니다."),
]

# English translations of the same 8 sentences
STORY_EN = [
    ("st1", "On the weekend, I go to the traditional market with my friend."),
    ("st2", "There is really a lot of delicious food in the market."),
    ("st3", "We order tteokbokki and kimbap at the snack restaurant."),
    ("st4", "The spicy and sweet tteokbokki is very delicious."),
    ("st5", "I also drink a cup of warm fish cake broth."),
    ("st6", "For dessert, we buy and eat sweet, crispy hotteok."),
    ("st7", "Auntie, thank you for the wonderful meal! We greet politely."),
    ("st8", "My belly is full and I feel truly happy."),
]

# Chinese bonus translations of the same 8 sentences
STORY_ZH = [
    ("st1", "周末和朋友一起去传统市场。"),
    ("st2", "市场里美味的食物真的很多。"),
    ("st3", "我们在小吃店点辣炒年糕和紫菜包饭。"),
    ("st4", "微辣带甜的炒年糕非常美味。"),
    ("st5", "温热的鱼饼汤也喝上一杯。"),
    ("st6", "作为甜点，买香甜酥脆的糖饼吃。"),
    ("st7", "阿姨，真的吃得很好！礼貌地道谢。"),
    ("st8", "肚子吃得饱饱的，心情也特别幸福。"),
]

# 2. 课后核心音节字块 (12 Syllable Blocks)
CHARACTERS = [
    ("zi1", "맛"), ("zi2", "음"), ("zi3", "식"), ("zi4", "장"),
    ("zi5", "떡"), ("zi6", "김"), ("zi7", "주"), ("zi8", "문"),
    ("zi9", "물"), ("zi10", "복"), ("zi11", "행"), ("zi12", "말"),
]

# 3. 课后核心单词 (12 Words)
WORDS = [
    ("ci1", "시장"), ("ci2", "음식"), ("ci3", "분식집"), ("ci4", "주문"),
    ("ci5", "국물"), ("ci6", "후식"), ("ci7", "이모님"), ("ci8", "주말"),
    ("ci9", "행복"), ("ci10", "맛있다"), ("ci11", "맵다"), ("ci12", "달다"),
]

# 4. 课后「美食」专词 (7 Food Thematic Words)
PROPER_NOUNS = [
    ("pn1", "떡볶이"), ("pn2", "김밥"), ("pn3", "어묵"), ("pn4", "호떡"),
    ("pn5", "비빔밥"), ("pn6", "라면"), ("pn7", "물냉면"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "맛있는 음식을 친구와 함께 나누어 먹는 것은 큰 기쁨입니다."),
]

KO_ITEMS = STORY + CHARACTERS + WORDS + PROPER_NOUNS + KEY_SENTENCE


async def gen_item(name: str, text: str, voice: str, rate: str, out_dir: Path, sem: asyncio.Semaphore):
    out_file = out_dir / f"{name}.mp3"
    if out_file.exists() and out_file.stat().st_size > 500:
        return ("skip", name, text)
    async with sem:
        for attempt in range(4):
            try:
                communicate = edge_tts.Communicate(text, voice, rate=rate)
                await communicate.save(str(out_file))
                if out_file.exists() and out_file.stat().st_size > 500:
                    return ("ok", name, text)
            except Exception as e:
                if attempt == 3:
                    return ("err", name, f"{text} -> {e}")
                await asyncio.sleep(1.5 * (attempt + 1))
        return ("err", name, f"{text} -> failed after retries")


async def main():
    sem = asyncio.Semaphore(4)
    tasks = []

    # Korean items
    for name, text in KO_ITEMS:
        tasks.append(gen_item(name, text, KO_VOICE, KO_RATE, OUT_DIR, sem))

    # English translations
    for name, text in STORY_EN:
        tasks.append(gen_item(name, text, EN_VOICE, EN_RATE, OUT_DIR_EN, sem))

    # Chinese translations
    for name, text in STORY_ZH:
        tasks.append(gen_item(name, text, ZH_VOICE, ZH_RATE, OUT_DIR_ZH, sem))

    results = await asyncio.gather(*tasks)
    ok_count = sum(1 for r in results if r[0] == "ok")
    skip_count = sum(1 for r in results if r[0] == "skip")
    err_count = sum(1 for r in results if r[0] == "err")

    print(f"Done: {ok_count} created, {skip_count} cached, {err_count} errors (Total {len(tasks)})")
    for r in results:
        if r[0] == "err":
            print(f"  FAILED: {r[1]} - {r[2]}")


if __name__ == "__main__":
    asyncio.run(main())
