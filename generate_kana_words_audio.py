#!/usr/bin/env python3
"""Generate audio for the Row-by-Row Restricted Phonics (受限拼读) system in nihongo0."""
import asyncio
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "nihongo0"
OUT_DIR.mkdir(parents=True, exist_ok=True)

JA_VOICE = "ja-JP-NanamiNeural"
JA_RATE = "-5%"

# 10 Rows of Restricted Phonics Words
WORDS_DATA = [
    # Row 1: あ行 (a, i, u, e, o)
    ("kw_ai", "あい"),
    ("kw_ao", "あお"),
    ("kw_ie", "いえ"),
    ("kw_ue", "うえ"),
    ("kw_ii", "いい"),
    ("kw_e", "え"),

    # Row 2: か行 (ka, ki, ku, ke, ko)
    ("kw_aka", "あか"),
    ("kw_aki", "あき"),
    ("kw_eki", "えき"),
    ("kw_ike", "いけ"),
    ("kw_kao", "かお"),
    ("kw_koe", "こえ"),
    ("kw_kiku", "きく"),
    ("kw_koko", "ここ"),

    # Row 3: さ行 (sa, shi, su, se, so)
    ("kw_asa", "あさ"),
    ("kw_kasa", "かさ"),
    ("kw_ashi", "あし"),
    ("kw_sushi", "すし"),
    ("kw_okashi", "おかし"),
    ("kw_uso", "うそ"),
    ("kw_soko", "そこ"),
    ("kw_ishi", "いし"),

    # Row 4: た行 (ta, chi, tsu, te, to)
    ("kw_uta", "うた"),
    ("kw_tako", "たこ"),
    ("kw_kuchi", "くち"),
    ("kw_tsukue", "つくえ"),
    ("kw_te", "て"),
    ("kw_tokei", "とけい"),
    ("kw_chichi", "ちち"),
    ("kw_soto", "そと"),

    # Row 5: な行 (na, ni, nu, ne, no)
    ("kw_inu", "いぬ"),
    ("kw_neko", "ねこ"),
    ("kw_natsu", "なつ"),
    ("kw_sakana", "さかな"),
    ("kw_kinoko", "きのこ"),
    ("kw_nani", "なに"),
    ("kw_niku", "にく"),

    # Row 6: は行 (ha, hi, fu, he, ho)
    ("kw_hana", "はな"),
    ("kw_hito", "ひと"),
    ("kw_hoshi", "ほし"),
    ("kw_fune", "ふね"),
    ("kw_fuku", "ふく"),
    ("kw_haha", "はは"),
    ("kw_hashi", "はし"),

    # Row 7: ま行 (ma, mi, mu, me, mo)
    ("kw_ame", "あめ"),
    ("kw_mimi", "みみ"),
    ("kw_me", "め"),
    ("kw_machi", "まち"),
    ("kw_momo", "もも"),
    ("kw_mushi", "むし"),
    ("kw_michi", "みち"),

    # Row 8: や行 (ya, yu, yo)
    ("kw_yama", "やま"),
    ("kw_yuki", "ゆき"),
    ("kw_heya", "へや"),
    ("kw_yume", "ゆめ"),
    ("kw_yomu", "よむ"),
    ("kw_oyatsu", "おやつ"),

    # Row 9: ら行 (ra, ri, ru, re, ro)
    ("kw_sora", "そら"),
    ("kw_tori", "とり"),
    ("kw_sakura", "さくら"),
    ("kw_shiro", "しろ"),
    ("kw_yoru", "よる"),
    ("kw_kuruma", "くるま"),
    ("kw_haru", "はる"),

    # Row 10: わ行・ん (wa, wo, n)
    ("kw_watashi", "わたし"),
    ("kw_hon", "ほん"),
    ("kw_nihon", "にほん"),
    ("kw_mikan", "みかん"),
    ("kw_kirin", "きりん"),
    ("kw_wani", "わに"),
    ("kw_raion", "らいおん"),
    ("kw_tenki", "てんき"),
    ("kw_kantan", "かんたん"),
]

async def synth(text, voice, rate, out_path):
    if out_path.exists() and out_path.stat().st_size > 500:
        print(f"SKIP {out_path.name}")
        return
    try:
        comm = edge_tts.Communicate(text, voice, rate=rate)
        await comm.save(str(out_path))
        print(f"OK   {out_path.name} ({text})")
    except Exception as e:
        print(f"FAIL {out_path.name}: {e}")

async def main():
    sem = asyncio.Semaphore(4)
    async def one(fname, text):
        async with sem:
            await synth(text, JA_VOICE, JA_RATE, OUT_DIR / f"{fname}.mp3")
    print(f"Synthesizing {len(WORDS_DATA)} restricted phonics words...")
    await asyncio.gather(*(one(f, t) for f, t in WORDS_DATA))
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
