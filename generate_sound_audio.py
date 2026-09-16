#!/usr/bin/env python3
import asyncio
import os
from pathlib import Path
import edge_tts

OUT_DIR = Path("/home/ubuntu/ws/jump-jump-game/audio/sound")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ITEMS = [
    # UI Guides & Greetings
    ("welcome_zh", "zh-CN-XiaoxiaoNeural", "欢迎来到拼音单音王国！让我们从最基础的发音开始探险吧！"),
    ("welcome_ja", "ja-JP-NanamiNeural", "はじめてのピンイン単音王国へようこそ！基本の音からいっしょに遊ぼう！"),
    ("prompt_listen_zh", "zh-CN-XiaoxiaoNeural", "仔细听，是哪一个发音呢？"),
    ("prompt_listen_ja", "ja-JP-NanamiNeural", "よーく聴いて、どの音かあててみてね！"),
    ("feed_prompt_zh", "zh-CN-XiaoxiaoNeural", "小怪兽肚子饿啦，快喂它吃正确发音的食物吧！"),
    ("feed_prompt_ja", "ja-JP-NanamiNeural", "おなかがペコペコ！正しい音のおやつを食べさせてね！"),
    ("trace_prompt_zh", "zh-CN-XiaoxiaoNeural", "伸出小手指，跟着发光的小星星描一描吧！"),
    ("trace_prompt_ja", "ja-JP-NanamiNeural", "ゆびで光る星をなぞってみよう！"),

    # Praises & Cheers
    ("praise_1_zh", "zh-CN-XiaoxiaoNeural", "太棒啦！完全正确！"),
    ("praise_1_ja", "ja-JP-NanamiNeural", "すごい！大正解！"),
    ("praise_2_zh", "zh-CN-XiaoxiaoNeural", "哇！你真聪明！"),
    ("praise_2_ja", "ja-JP-NanamiNeural", "わぁ、とってもじょうず！"),
    ("praise_3_zh", "zh-CN-XiaoxiaoNeural", "太厉害了！发音真标准！"),
    ("praise_3_ja", "ja-JP-NanamiNeural", "かっこいい！きれいな発音！"),
    ("stage_clear_zh", "zh-CN-XiaoxiaoNeural", "太精彩啦！你集齐了这一关的所有发音精灵！"),
    ("stage_clear_ja", "ja-JP-NanamiNeural", "大成功！このステージのおとせいれいをぜんぶ集めたよ！"),

    # Simple Vowels (单韵母) Rhymes
    ("rhyme_a", "zh-CN-XiaoxiaoNeural", "张大嘴巴 a a a，红红苹果抱回家！"),
    ("rhyme_o", "zh-CN-XiaoxiaoNeural", "公鸡打鸣 o o o，清晨太阳升起来！"),
    ("rhyme_e", "zh-CN-XiaoxiaoNeural", "白鹅倒影 e e e，清清水中游得欢！"),
    ("rhyme_i", "zh-CN-XiaoxiaoNeural", "牙齿对齐 i i i，整整齐齐穿新衣！"),
    ("rhyme_u", "zh-CN-XiaoxiaoNeural", "嘴巴突出 u u u，乌龟背壳爬呀爬！"),
    ("rhyme_ü", "zh-CN-XiaoxiaoNeural", "小鱼吐泡 ü ü ü，吹着口哨真可爱！"),

    # Key Initials Rhymes
    ("rhyme_b", "zh-CN-XiaoxiaoNeural", "右下半圆 b b b，收音机里听广播！"),
    ("rhyme_p", "zh-CN-XiaoxiaoNeural", "右上半圆 p p p，拍起皮球跳呀跳！"),
    ("rhyme_m", "zh-CN-XiaoxiaoNeural", "两个门洞 m m m，小猫咪咪捉迷藏！"),
    ("rhyme_f", "zh-CN-XiaoxiaoNeural", "一根拐杖 f f f，老爷爷把大佛拜！"),
    ("rhyme_d", "zh-CN-XiaoxiaoNeural", "左下半圆 d d d，小马快跑敲小鼓！"),
    ("rhyme_t", "zh-CN-XiaoxiaoNeural", "一把雨伞 t t t，下雨下雪撑开伞！"),
    ("rhyme_n", "zh-CN-XiaoxiaoNeural", "一个门洞 n n n，小猪进门喝牛奶！"),
    ("rhyme_l", "zh-CN-XiaoxiaoNeural", "一根小棍 l l l，又脆又甜大鸭梨！"),

    # Retroflex Special Focus
    ("rhyme_zh", "zh-CN-XiaoxiaoNeural", "织毛衣 zh zh zh，卷起舌头真温暖！"),
    ("rhyme_ch", "zh-CN-XiaoxiaoNeural", "吃西瓜 ch ch ch，大口吃瓜甜滋滋！"),
    ("rhyme_sh", "zh-CN-XiaoxiaoNeural", "大狮子 sh sh sh，威风凛凛大声吼！"),
    ("rhyme_r", "zh-CN-XiaoxiaoNeural", "红日头 r r r，金色阳光洒大地！")
]

async def generate_item(key, voice, text):
    out_file = OUT_DIR / f"{key}.mp3"
    if out_file.exists() and out_file.stat().st_size > 1000:
        return
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(out_file))
        print(f"Generated {out_file.name}")
    except Exception as e:
        print(f"Failed {key}: {e}")

async def main():
    tasks = [generate_item(k, v, t) for k, v, t in ITEMS]
    await asyncio.gather(*tasks)
    print(f"Done generating sound audio assets in {OUT_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
