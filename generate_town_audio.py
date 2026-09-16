#!/usr/bin/env python3
import asyncio
import os
from pathlib import Path
import edge_tts

OUT_DIR = Path("/home/ubuntu/ws/jump-jump-game/audio/town")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ITEMS = [
    # NPC Requests
    ("bear_req", "zh-CN-YunjianNeural", "肚子好饿呀，我想吃面包！"),
    ("bear_thanks", "zh-CN-YunjianNeural", "哇，太香了！谢谢你！"),
    ("bunny_req", "zh-CN-XiaoxiaoNeural", "你好呀！我想吃红苹果！"),
    ("bunny_thanks", "zh-CN-XiaoxiaoNeural", "咔嚓咔嚓，苹果真甜！谢谢你！"),
    ("cat_req", "zh-CN-XiaoyiNeural", "喵呜~ 我想喝甜甜的牛奶！"),
    ("cat_thanks", "zh-CN-XiaoyiNeural", "咕咚咕咚，真好喝！谢谢你！"),
    ("puppy_req", "zh-CN-YunxiNeural", "汪汪！我要上学啦，想要新书包！"),
    ("puppy_thanks", "zh-CN-YunxiNeural", "哇，新书包真好看！谢谢你！"),
    ("panda_req", "zh-CN-YunyangNeural", "天气好热呀，我想吃大西瓜！"),
    ("panda_thanks", "zh-CN-YunyangNeural", "真甜真凉快！谢谢你！"),
    ("bird_req", "zh-CN-XiaoxiaoNeural", "啾啾！去野餐啦，我想要一个水杯！"),
    ("bird_thanks", "zh-CN-XiaoxiaoNeural", "喝到水啦，真开心！谢谢你！"),
    ("elephant_req", "zh-CN-YunyangNeural", "散步走累了，我想喝一杯热茶！"),
    ("elephant_thanks", "zh-CN-YunyangNeural", "好香的茶，非常感谢你！"),

    # Player Child Dialogue
    ("give_miànbāo", "zh-CN-XiaoxiaoNeural", "给你面包！"),
    ("give_píngguǒ", "zh-CN-XiaoxiaoNeural", "给你苹果！"),
    ("give_niúnǎi", "zh-CN-XiaoxiaoNeural", "给你牛奶！"),
    ("give_shūbāo", "zh-CN-XiaoxiaoNeural", "给你书包！"),
    ("give_xīguā", "zh-CN-XiaoxiaoNeural", "给你西瓜！"),
    ("give_shuǐbēi", "zh-CN-XiaoxiaoNeural", "给你水杯！"),
    ("give_chá", "zh-CN-XiaoxiaoNeural", "请喝茶！"),
    ("youre_welcome", "zh-CN-XiaoxiaoNeural", "不客气！"),
    ("hello", "zh-CN-XiaoxiaoNeural", "你好！"),
    ("goodbye", "zh-CN-XiaoxiaoNeural", "再见！"),

    # Pinyin Blending audio (m - iàn -> miàn, 面!)
    ("m_ian_blend", "zh-CN-XiaoxiaoNeural", "摸，面，miàn，面包的面！"),
    ("b_ao_blend", "zh-CN-XiaoxiaoNeural", "玻，包，bāo，面包的包！"),
    ("p_ing_blend", "zh-CN-XiaoxiaoNeural", "坡，平，píng，苹果的苹！"),
    ("g_uo_blend", "zh-CN-XiaoxiaoNeural", "哥，果，guǒ，苹果的果！"),
    ("n_iu_blend", "zh-CN-XiaoxiaoNeural", "讷，牛，niú，小牛的牛！"),
    ("n_ai_blend", "zh-CN-XiaoxiaoNeural", "讷，奶，nǎi，牛奶的奶！"),
    ("sh_u_blend", "zh-CN-XiaoxiaoNeural", "狮，书，shū，书包的书！"),
    ("x_i_blend", "zh-CN-XiaoxiaoNeural", "西，西，xī，西瓜的西！"),
    ("g_ua_blend", "zh-CN-XiaoxiaoNeural", "哥，瓜，guā，西瓜的瓜！"),
    ("sh_ui_blend", "zh-CN-XiaoxiaoNeural", "狮，水，shuǐ，水杯的水！"),
    ("b_ei_blend", "zh-CN-XiaoxiaoNeural", "玻，杯，bēi，水杯的杯！"),
    ("ch_a_blend", "zh-CN-XiaoxiaoNeural", "吃，茶，chá，茶叶的茶！"),

    # Words
    ("miànbāo", "zh-CN-XiaoxiaoNeural", "面包"),
    ("píngguǒ", "zh-CN-XiaoxiaoNeural", "苹果"),
    ("niúnǎi", "zh-CN-XiaoxiaoNeural", "牛奶"),
    ("shūbāo", "zh-CN-XiaoxiaoNeural", "书包"),
    ("xīguā", "zh-CN-XiaoxiaoNeural", "西瓜"),
    ("shuǐbēi", "zh-CN-XiaoxiaoNeural", "水杯"),
    ("chá", "zh-CN-XiaoxiaoNeural", "茶"),

    # Pinyin Single Letters / Syllables
    ("sym_m", "zh-CN-XiaoxiaoNeural", "摸"),
    ("sym_ian4", "zh-CN-XiaoxiaoNeural", "面"),
    ("sym_b", "zh-CN-XiaoxiaoNeural", "玻"),
    ("sym_ao1", "zh-CN-XiaoxiaoNeural", "包"),
    ("sym_p", "zh-CN-XiaoxiaoNeural", "坡"),
    ("sym_ing2", "zh-CN-XiaoxiaoNeural", "平"),
    ("sym_g", "zh-CN-XiaoxiaoNeural", "哥"),
    ("sym_uo3", "zh-CN-XiaoxiaoNeural", "果"),
    ("sym_n", "zh-CN-XiaoxiaoNeural", "讷"),
    ("sym_iu2", "zh-CN-XiaoxiaoNeural", "牛"),
    ("sym_ai3", "zh-CN-XiaoxiaoNeural", "奶"),
    ("sym_sh", "zh-CN-XiaoxiaoNeural", "狮"),
    ("sym_u1", "zh-CN-XiaoxiaoNeural", "书"),
    ("sym_x", "zh-CN-XiaoxiaoNeural", "西"),
    ("sym_i1", "zh-CN-XiaoxiaoNeural", "衣"),
    ("sym_ua1", "zh-CN-XiaoxiaoNeural", "瓜"),
    ("sym_ui3", "zh-CN-XiaoxiaoNeural", "水"),
    ("sym_ei1", "zh-CN-XiaoxiaoNeural", "杯"),
    ("sym_ch", "zh-CN-XiaoxiaoNeural", "吃"),
    ("sym_a2", "zh-CN-XiaoxiaoNeural", "茶"),

    # Guidance / Praises
    ("guide_place", "zh-CN-XiaoxiaoNeural", "把拼音积木放进拼读盒吧！"),
    ("guide_deliver", "zh-CN-XiaoxiaoNeural", "拼成功啦！把物品送给好朋友吧！"),
    ("praise_great", "zh-CN-XiaoxiaoNeural", "太棒了，回答完全正确！"),
    ("praise_super", "zh-CN-XiaoxiaoNeural", "哇，你真是个拼音小天才！"),
    ("quest_complete", "zh-CN-XiaoxiaoNeural", "小镇居民非常感谢你，获得一枚友谊徽章！"),

    # Japanese Bilingual Lines
    ("ja_welcome", "ja-JP-NanamiNeural", "ピンインタウンへようこそ！どうぶつのおともだちをたすけてあげよう！"),
    ("ja_guide_place", "ja-JP-NanamiNeural", "せいも と いんも を えらんで ガッチャンコしよう！"),
    ("ja_guide_deliver", "ja-JP-NanamiNeural", "かんせい！おともだちにとどけてあげよう！"),
    ("ja_praise", "ja-JP-NanamiNeural", "すごい！せいかいだよ！")
]

async def main():
    print(f"Generating {len(ITEMS)} audio files...")
    sem = asyncio.Semaphore(4)

    async def generate_one(fname, voice, text):
        target = OUT_DIR / f"{fname}.mp3"
        if target.exists() and target.stat().st_size > 1000:
            return
        async with sem:
            try:
                comm = edge_tts.Communicate(text, voice)
                await comm.save(str(target))
                print(f"Generated: {fname}.mp3 ({text})")
            except Exception as e:
                print(f"Failed {fname}: {e}")

    tasks = [generate_one(f, v, t) for f, v, t in ITEMS]
    await asyncio.gather(*tasks)
    print("Done generating town audio!")

if __name__ == "__main__":
    asyncio.run(main())
