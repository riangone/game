#!/usr/bin/env python3
"""Generate real MP3 audio for the 《나의 일주일》(hangugeo) Korean learning game.

Uses edge-tts (Microsoft neural voices, free, no API key), mirroring the exact
same architecture as generate_nihongo_audio.py:
- Korean main narration (ko-KR-SunHiNeural)
- English translation (en-US-JennyNeural)
- Chinese translation (zh-CN-XiaoxiaoNeural)

Generates:
- audio/hangugeo/st1.mp3 .. st8.mp3       (8 story sentences, Korean)
- audio/hangugeo/zi1.mp3 .. zi12.mp3      (12 核心音节字块: 한국어학교친구일월화수생)
- audio/hangugeo/ci1.mp3 .. ci12.mp3      (12 核心单词: 이름, 매일, 학교, ...)
- audio/hangugeo/pn1.mp3 .. pn7.mp3       (7 星期: 월화수목금토일요일)
- audio/hangugeo/sent1.mp3                (课后重点句子)
- audio/hangugeo_en/st1.mp3 .. st8.mp3    (8 story sentences, English translation)
- audio/hangugeo_zh/st1.mp3 .. st8.mp3    (8 story sentences, Chinese bonus translation)
"""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "hangugeo"
OUT_DIR_EN = ROOT / "audio" / "hangugeo_en"
OUT_DIR_ZH = ROOT / "audio" / "hangugeo_zh"
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
    ("st1", "안녕하세요! 제 이름은 민우입니다."),
    ("st2", "저는 매일 학교에 갑니다."),
    ("st3", "월요일과 수요일과 금요일에는 한국어 수업이 있습니다."),
    ("st4", "화요일과 목요일에는 학교에서 친구와 함께 공부합니다."),
    ("st5", "토요일에는 가족과 공원에서 놀아요."),
    ("st6", "일요일에는 집에서 책을 읽어요."),
    ("st7", "우리 선생님은 아주 친절합니다."),
    ("st8", "저는 매일매일 아주 건강하고 행복합니다."),
]

# English translations
STORY_EN = [
    ("st1", "Hello! My name is Minwoo."),
    ("st2", "I go to school every day."),
    ("st3", "On Mondays, Wednesdays, and Fridays, there is a Korean class."),
    ("st4", "On Tuesdays and Thursdays, I study together with friends at school."),
    ("st5", "On Saturdays, I play in the park with my family."),
    ("st6", "On Sundays, I read books at home."),
    ("st7", "Our teacher is very kind."),
    ("st8", "I am very healthy and happy every single day."),
]

# Chinese translations
STORY_ZH = [
    ("st1", "你好！我的名字是敏宇。"),
    ("st2", "我每天去学校。"),
    ("st3", "星期一、星期三和星期五有韩国语课。"),
    ("st4", "星期二和星期四，在学校和朋友一起学习。"),
    ("st5", "星期六我和家人在公园玩耍。"),
    ("st6", "星期天我在家里看书。"),
    ("st7", "我们的老师非常亲切。"),
    ("st8", "我每一天都很健康快乐。"),
]

# 2. 课后核心音节字块 (12 Syllables)
CHARACTERS = [
    ("zi1", "한"), ("zi2", "국"), ("zi3", "어"), ("zi4", "학"),
    ("zi5", "교"), ("zi6", "친"), ("zi7", "구"), ("zi8", "일"),
    ("zi9", "월"), ("zi10", "화"), ("zi11", "수"), ("zi12", "생"),
]

# 3. 课后核心词汇 (12 Words)
WORDS = [
    ("ci1", "이름"), ("ci2", "매일"), ("ci3", "학교"), ("ci4", "한국어"),
    ("ci5", "수업"), ("ci6", "친구"), ("ci7", "공부"), ("ci8", "가족"),
    ("ci9", "공원"), ("ci10", "선생님"), ("ci11", "친절"), ("ci12", "건강"),
]

# 4. 课后「星期」词汇 (7 Weekday Words)
PROPER_NOUNS = [
    ("pn1", "월요일"), ("pn2", "화요일"), ("pn3", "수요일"), ("pn4", "목요일"),
    ("pn5", "금요일"), ("pn6", "토요일"), ("pn7", "일요일"),
]

# 5. 课后重点句子 (Key Sentence)
KEY_SENTENCE = [
    ("sent1", "한국어를 공부하는 것은 정말 재미있어요."),
]

KO_ITEMS = STORY + CHARACTERS + WORDS + PROPER_NOUNS + KEY_SENTENCE


async def synth(text, voice, rate, out_path):
    if out_path.exists() and out_path.stat().st_size > 500:
        return
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(str(out_path))


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
