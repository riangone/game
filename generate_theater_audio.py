#!/usr/bin/env python3
import asyncio
import os
from pathlib import Path
import edge_tts

OUT_DIR = Path("/home/ubuntu/ws/jump-jump-game/audio/theater")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ITEMS = [
    # General UI / Stage audio
    ("welcome_zh", "zh-CN-XiaoxiaoNeural", "欢迎来到神奇声调小剧场！让我们一起用声音演故事吧！"),
    ("welcome_ja", "ja-JP-NanamiNeural", "ふしぎなトーンシアターへようこそ！こえの抑揚でげきを演じよう！"),
    ("guide_trace_zh", "zh-CN-XiaoxiaoNeural", "根据剧情情绪，在屏幕上划出正确的声调吧！"),
    ("guide_trace_ja", "ja-JP-NanamiNeural", "きもちにあわせて、ゆびで声調のせんをなぞってみよう！"),
    ("praise_correct_zh", "zh-CN-XiaoxiaoNeural", "演得太精彩了！声调完全正确！"),
    ("praise_correct_ja", "ja-JP-NanamiNeural", "すごい！ぴったりの抑揚だよ！大成功！"),
    ("scene_clear_zh", "zh-CN-XiaoxiaoNeural", "本幕演出圆满成功！送你一枚金剧场奖章！"),
    ("scene_clear_ja", "ja-JP-NanamiNeural", "この幕は無事終幕！ゴールドシアターメダルをゲット！"),
    
    # Four Tone mnemonic rhymes
    ("rhyme_tone1", "zh-CN-XiaoxiaoNeural", "一声平平高又平，平静温柔好心情！"),
    ("rhyme_tone2", "zh-CN-XiaoxiaoNeural", "二声扬起往上爬，好奇疑问找找它！"),
    ("rhyme_tone3", "zh-CN-XiaoxiaoNeural", "三声拐弯下又上，思考点头荡秋千！"),
    ("rhyme_tone4", "zh-CN-XiaoxiaoNeural", "四声从天落下来，坚决有力真痛快！"),

    ("rhyme_short1", "zh-CN-XiaoxiaoNeural", "一声平！平稳平静。"),
    ("rhyme_short2", "zh-CN-XiaoxiaoNeural", "二声扬！好奇疑问。"),
    ("rhyme_short3", "zh-CN-XiaoxiaoNeural", "三声拐弯！思考起伏。"),
    ("rhyme_short4", "zh-CN-XiaoxiaoNeural", "四声下落！果断干脆。"),

    ("ja_tone1_desc", "ja-JP-NanamiNeural", "一声：まっすぐ平ら。おだやかで優しい声。"),
    ("ja_tone2_desc", "ja-JP-NanamiNeural", "二声：下から上へキュッ！疑問とびっくり！"),
    ("ja_tone3_desc", "ja-JP-NanamiNeural", "三声：谷を下りて上へ！じっくり考える声。"),
    ("ja_tone4_desc", "ja-JP-NanamiNeural", "四声：上から一気に下へ！元気でハッキリ！"),

    # Plays & Scenes Dialogue lines
    # Play 1: 小猫找妈妈 (Mimi's Cat Family)
    ("play1_intro", "zh-CN-XiaoxiaoNeural", "第一幕：小猫找妈妈。咪咪睡醒了，想找妈妈呢！"),
    ("p1_s1_prompt", "zh-CN-XiaoxiaoNeural", "咪咪揉揉眼睛，温柔地呼唤妈妈。该用平平的一声还是哪一个呢？"),
    ("p1_s1_voice", "zh-CN-XiaoxiaoNeural", "mā！妈妈！你在哪里呀？"),
    ("p1_s2_prompt", "zh-CN-XiaoxiaoNeural", "门后传来沙沙声，咪咪好奇地歪起小脑袋：咦？是谁呀？"),
    ("p1_s2_voice", "zh-CN-XiaoxiaoNeural", "má？是妈妈回来了吗？"),
    ("p1_s3_prompt", "zh-CN-XiaoxiaoNeural", "咪咪跳上摇摇木马，起起伏伏像骑小马一样等妈妈！"),
    ("p1_s3_voice", "zh-CN-XiaoxiaoNeural", "mǎ！摇摇小木马，晃悠悠！"),
    ("p1_s4_prompt", "zh-CN-XiaoxiaoNeural", "毛线球掉在地上，咪咪站得直直的，可不能淘气被批评哦！"),
    ("p1_s4_voice", "zh-CN-XiaoxiaoNeural", "mà！不淘气，做个乖宝宝！"),
    ("p1_outro", "zh-CN-XiaoxiaoNeural", "猫妈妈笑着抱起咪咪：咪咪真棒，四声都演得太准确啦！"),

    # Play 2: 小兔子奇妙信箱 (Bunny's Mysterious Mailbox)
    ("play2_intro", "zh-CN-XiaoxiaoNeural", "第二幕：小兔子的奇妙信箱。森林里送来了一个神奇包裹！"),
    ("p2_s1_prompt", "zh-CN-XiaoxiaoNeural", "波波在院子里看花，心情好舒畅呀！"),
    ("p2_s1_voice", "zh-CN-XiaoxiaoNeural", "huā！美丽的花儿开啦！"),
    ("p2_s2_prompt", "zh-CN-XiaoxiaoNeural", "咚咚咚！门外有人敲门，波波眨眨眼睛好奇地问：是谁呀？"),
    ("p2_s2_voice", "zh-CN-XiaoxiaoNeural", "shéi？是谁在敲门呢？"),
    ("p2_s3_prompt", "zh-CN-XiaoxiaoNeural", "波波抱着沉甸甸的包裹，好奇地琢磨：这里面是什么宝物呢？"),
    ("p2_s3_voice", "zh-CN-XiaoxiaoNeural", "bǎo！好珍贵的神秘大宝盒！"),
    ("p2_s4_prompt", "zh-CN-XiaoxiaoNeural", "拆开一瞧，是一辆酷炫小滑板车！快看呀！"),
    ("p2_s4_voice", "zh-CN-XiaoxiaoNeural", "kàn！大家快来看我的新滑板车！"),
    ("p2_outro", "zh-CN-XiaoxiaoNeural", "小兔子踩着滑板车欢呼，小信箱剧场完美谢幕！"),

    # Play 3: 小熊的大果园 (Baby Bear's Orchard)
    ("play3_intro", "zh-CN-XiaoxiaoNeural", "第三幕：小熊的大果园。秋天到啦，树上结满了香香的果子！"),
    ("p3_s1_prompt", "zh-CN-XiaoxiaoNeural", "小熊坐在树荫下，微风轻轻地吹拂着！"),
    ("p3_s1_voice", "zh-CN-XiaoxiaoNeural", "fēng！清凉的微风吹呀吹！"),
    ("p3_s2_prompt", "zh-CN-XiaoxiaoNeural", "头顶落下一个大果子，小熊揉揉鼻子：这是圆圆的桃子吗？"),
    ("p3_s2_voice", "zh-CN-XiaoxiaoNeural", "táo？是一颗香香的大甜桃吗？"),
    ("p3_s3_prompt", "zh-CN-XiaoxiaoNeural", "小熊咬了一口，满足地晃晃头：哇，味道真是太好啦！"),
    ("p3_s3_voice", "zh-CN-XiaoxiaoNeural", "hǎo！好甜好脆的味道！"),
    ("p3_s4_prompt", "zh-CN-XiaoxiaoNeural", "装满整整一大篮果子，果园丰收啦！送到家啦！"),
    ("p3_s4_voice", "zh-CN-XiaoxiaoNeural", "dào！果子全都送到家啦！"),
    ("p3_outro", "zh-CN-XiaoxiaoNeural", "小熊抱起大果篮开心地转圈圈，果园剧场掌声雷动！"),

    # Play 4: 小松鼠音乐会 (Squirrel's Forest Concert)
    ("play4_intro", "zh-CN-XiaoxiaoNeural", "第四幕：小松鼠的森林音乐会。大家一起奏响森林交响曲！"),
    ("p4_s1_prompt", "zh-CN-XiaoxiaoNeural", "小松鼠吹响竹笛，笛声悠扬平缓地飘向远方！"),
    ("p4_s1_voice", "zh-CN-XiaoxiaoNeural", "dī！悠扬的小笛声响起来！"),
    ("p4_s2_prompt", "zh-CN-XiaoxiaoNeural", "树枝上响起笃笃声，松鼠停下来听：咦？是谁在啼叫呢？"),
    ("p4_s2_voice", "zh-CN-XiaoxiaoNeural", "tí？是啄木鸟先生在啼鸣吗？"),
    ("p4_s3_prompt", "zh-CN-XiaoxiaoNeural", "大熊搬出了大木鼓，大家一起随着节拍点头思考！"),
    ("p4_s3_voice", "zh-CN-XiaoxiaoNeural", "gǔ！咚咚咚敲响大鼓！"),
    ("p4_s4_prompt", "zh-CN-XiaoxiaoNeural", "所有乐器齐奏，音乐太震撼啦，小动物们欢呼：太酷啦！"),
    ("p4_s4_voice", "zh-CN-XiaoxiaoNeural", "kù！这首交响乐太酷啦！"),
    ("p4_outro", "zh-CN-XiaoxiaoNeural", "全场观众挥舞荧光棒欢呼喝彩，音乐小剧场大获全胜！"),

    # Play 5: 小恐龙飞天记 (Little Dino's Flight)
    ("play5_intro", "zh-CN-XiaoxiaoNeural", "第五幕：小恐龙飞天记。雷雷想和天上的小鸟一样飞翔！"),
    ("p5_s1_prompt", "zh-CN-XiaoxiaoNeural", "雷雷抬头望向天空，彩云飘得好高好高！"),
    ("p5_s1_voice", "zh-CN-XiaoxiaoNeural", "gāo！蓝蓝的天空飞得高！"),
    ("p5_s2_prompt", "zh-CN-XiaoxiaoNeural", "雷雷系上小红披风，好奇地问自己：我真的能飞起来吗？"),
    ("p5_s2_voice", "zh-CN-XiaoxiaoNeural", "néng？我也能冲上云霄吗？"),
    ("p5_s3_prompt", "zh-CN-XiaoxiaoNeural", "踩上弹簧蘑菇腾空而起，雷雷晃动着尾巴保持平衡！"),
    ("p5_s3_voice", "zh-CN-XiaoxiaoNeural", "wěi！甩起大尾巴转个圈！"),
    ("p5_s4_prompt", "zh-CN-XiaoxiaoNeural", "火箭背包喷出彩虹光芒，一下子冲过了彩虹门：成功啦！"),
    ("p5_s4_voice", "zh-CN-XiaoxiaoNeural", "dào！顺利飞到彩虹终点啦！"),
    ("p5_outro", "zh-CN-XiaoxiaoNeural", "雷雷在空中做出了帅气特技，剧场落下漫天彩带！"),

    # Play 6: 萌宝礼貌交际屋 (Polite Friends Playhouse)
    ("play6_intro", "zh-CN-XiaoxiaoNeural", "第六幕：萌宝礼貌交际屋。在幼儿园里做个有礼貌的阳光宝贝！"),
    ("p6_s1_prompt", "zh-CN-XiaoxiaoNeural", "晨读时间到啦，小朋友们安静地坐在桌前认真听！"),
    ("p6_s1_voice", "zh-CN-XiaoxiaoNeural", "tīng！竖起小耳朵认真听！"),
    ("p6_s2_prompt", "zh-CN-XiaoxiaoNeural", "看到新来的小伙伴，小猫礼貌又好奇地上前问候：你在读什么呢？"),
    ("p6_s2_voice", "zh-CN-XiaoxiaoNeural", "shén？你在看什么有趣的画册呀？"),
    ("p6_s3_prompt", "zh-CN-XiaoxiaoNeural", "小伙伴互相谦让分享玩具，笑眯眯地点头问好：你好！"),
    ("p6_s3_voice", "zh-CN-XiaoxiaoNeural", "hǎo！你好呀，我们一起做好朋友！"),
    ("p6_s4_prompt", "zh-CN-XiaoxiaoNeural", "放学收到老师奖励的红花贴纸，大声说一声谢谢！"),
    ("p6_s4_voice", "zh-CN-XiaoxiaoNeural", "xiè！非常感谢老师和小伙伴！"),
    ("p6_outro", "zh-CN-XiaoxiaoNeural", "大家手拉着手唱歌跳舞，小剧场所有演员谢幕鞠躬！"),

    # (Note: Individual tone isolated vowels/syllables tone_a1~tone_ba4
    # are generated with 100% precision via generate_accurate_tones.py Praat PSOLA pipeline)
]

async def generate_one(sem, name, voice, text):
    async with sem:
        out_path = OUT_DIR / f"{name}.mp3"
        if out_path.exists() and out_path.stat().st_size > 500:
            return
        comm = edge_tts.Communicate(text=text, voice=voice)
        try:
            await comm.save(str(out_path))
            print(f"Generated {name}.mp3")
        except Exception as e:
            print(f"Failed {name}: {e}")

async def main():
    print(f"Generating {len(ITEMS)} theater audio files...")
    sem = asyncio.Semaphore(4)
    tasks = [generate_one(sem, name, voice, text) for name, voice, text in ITEMS]
    await asyncio.gather(*tasks)
    print("All theater audio generation completed!")

if __name__ == "__main__":
    asyncio.run(main())
