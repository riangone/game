#!/usr/bin/env python3
import asyncio
import os
from pathlib import Path
import edge_tts

OUT_DIR = Path("/home/ubuntu/ws/jump-jump-game/audio/bistro")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ITEMS = [
    # UI & General
    ("welcome_zh", "zh-CN-XiaoxiaoNeural", "欢迎来到魔法点餐小餐厅！让我们一起听小动物点餐，做出美味佳肴吧！"),
    ("welcome_ja", "ja-JP-NanamiNeural", "魔法のレストランへようこそ！どうぶつのお客さんの注文を聞いて、おいしいごはんを作ろう！"),
    ("please_enjoy", "zh-CN-XiaoxiaoNeural", "请慢用！"),
    ("give_you", "zh-CN-XiaoxiaoNeural", "给你！"),
    ("order_ready", "zh-CN-XiaoxiaoNeural", "做好了！请慢用！"),
    ("chef_praise_zh", "zh-CN-XiaoxiaoNeural", "做得太棒了！客人非常满意！"),
    ("chef_praise_ja", "ja-JP-NanamiNeural", "すばらしい！お客さんも大満足だよ！"),
    ("step_num_zh", "zh-CN-XiaoxiaoNeural", "第一步：客人要几个？选出正确的数字拼音！"),
    ("step_num_ja", "ja-JP-NanamiNeural", "ステップ1：いくつほしいかな？数字のピンインを選ぼう！"),
    ("step_attr_zh", "zh-CN-XiaoxiaoNeural", "第二步：客人要什么颜色和口味？选出正确的特征拼音！"),
    ("step_attr_ja", "ja-JP-NanamiNeural", "ステップ2：どんな色や味かな？特徴のピンインを選ぼう！"),
    ("step_food_zh", "zh-CN-XiaoxiaoNeural", "第三步：客人要吃什么食物？选出正确的食物拼音！"),
    ("step_food_ja", "ja-JP-NanamiNeural", "ステップ3：何を食べるかな？料理のピンインを選ぼう！"),
    ("plate_serve_zh", "zh-CN-XiaoxiaoNeural", "美食制作完成！点击铃铛，端给小动物客人吧！"),
    ("plate_serve_ja", "ja-JP-NanamiNeural", "お料理が完成！ベルを押してお客さんにお届けしよう！"),

    # Numbers
    ("num_1", "zh-CN-XiaoxiaoNeural", "yī，一个"),
    ("num_2", "zh-CN-XiaoxiaoNeural", "liǎng，两个"),
    ("num_3", "zh-CN-XiaoxiaoNeural", "sān，三个"),
    ("num_4", "zh-CN-XiaoxiaoNeural", "sì，四个"),
    ("num_5", "zh-CN-XiaoxiaoNeural", "wǔ，五个"),
    ("py_yi", "zh-CN-XiaoxiaoNeural", "yī"),
    ("py_liang", "zh-CN-XiaoxiaoNeural", "liǎng"),
    ("py_san", "zh-CN-XiaoxiaoNeural", "sān"),
    ("py_si", "zh-CN-XiaoxiaoNeural", "sì"),
    ("py_wu", "zh-CN-XiaoxiaoNeural", "wǔ"),

    # Colors & Attributes
    ("attr_hong", "zh-CN-XiaoxiaoNeural", "hóng，红色的"),
    ("attr_huang", "zh-CN-XiaoxiaoNeural", "huáng，黄色的"),
    ("attr_lv", "zh-CN-XiaoxiaoNeural", "lǜ，绿色的"),
    ("attr_bai", "zh-CN-XiaoxiaoNeural", "bái，白色的"),
    ("attr_tian", "zh-CN-XiaoxiaoNeural", "tián，甜甜的"),
    ("attr_re", "zh-CN-XiaoxiaoNeural", "rè，热乎乎的"),
    ("attr_wen", "zh-CN-XiaoxiaoNeural", "wēn，温温的"),
    ("attr_xiang", "zh-CN-XiaoxiaoNeural", "xiāng，香喷喷的"),
    ("py_hong", "zh-CN-XiaoxiaoNeural", "hóng"),
    ("py_huang", "zh-CN-XiaoxiaoNeural", "huáng"),
    ("py_lv", "zh-CN-XiaoxiaoNeural", "lǜ"),
    ("py_bai", "zh-CN-XiaoxiaoNeural", "bái"),
    ("py_tian", "zh-CN-XiaoxiaoNeural", "tián"),
    ("py_re", "zh-CN-XiaoxiaoNeural", "rè"),
    ("py_wen", "zh-CN-XiaoxiaoNeural", "wēn"),
    ("py_xiang", "zh-CN-XiaoxiaoNeural", "xiāng"),

    # Foods
    ("food_pingguo", "zh-CN-XiaoxiaoNeural", "píngguǒ，苹果"),
    ("food_mianbao", "zh-CN-XiaoxiaoNeural", "miànbāo，面包"),
    ("food_niunai", "zh-CN-XiaoxiaoNeural", "niúnǎi，牛奶"),
    ("food_xigua", "zh-CN-XiaoxiaoNeural", "xīguā，西瓜"),
    ("food_xiangjiao", "zh-CN-XiaoxiaoNeural", "xiāngjiāo，香蕉"),
    ("food_mifan", "zh-CN-XiaoxiaoNeural", "mǐfàn，米饭"),
    ("food_cha", "zh-CN-XiaoxiaoNeural", "chá，茶"),
    ("food_caomei", "zh-CN-XiaoxiaoNeural", "cǎoméi，草莓"),
    ("food_dangao", "zh-CN-XiaoxiaoNeural", "dàngāo，蛋糕"),
    ("food_jiaozi", "zh-CN-XiaoxiaoNeural", "jiǎozi，饺子"),
    ("py_pingguo", "zh-CN-XiaoxiaoNeural", "píng guǒ"),
    ("py_mianbao", "zh-CN-XiaoxiaoNeural", "miàn bāo"),
    ("py_niunai", "zh-CN-XiaoxiaoNeural", "niú nǎi"),
    ("py_xigua", "zh-CN-XiaoxiaoNeural", "xī guā"),
    ("py_xiangjiao", "zh-CN-XiaoxiaoNeural", "xiāng jiāo"),
    ("py_mifan", "zh-CN-XiaoxiaoNeural", "mǐ fàn"),
    ("py_cha", "zh-CN-XiaoxiaoNeural", "chá"),
    ("py_caomei", "zh-CN-XiaoxiaoNeural", "cǎo méi"),
    ("py_dangao", "zh-CN-XiaoxiaoNeural", "dàn gāo"),
    ("py_jiaozi", "zh-CN-XiaoxiaoNeural", "jiǎo zi"),

    # Guest 1: 猫咪咪咪 (Cat Mimi)
    ("guest1_order", "zh-CN-XiaoyiNeural", "你好！我想吃两个红苹果！"),
    ("guest1_order_ja", "ja-JP-NanamiNeural", "こんにちは！赤いリンゴを2つ食べたいな！"),
    ("guest1_thanks", "zh-CN-XiaoyiNeural", "喵呜！红苹果又脆又甜，真好吃！谢谢你！"),
    ("guest1_hint", "zh-CN-XiaoyiNeural", "喵呜？这不是两个红苹果呢，我想吃两个红苹果哦！"),

    # Guest 2: 小熊波波 (Bear Bobo)
    ("guest2_order", "zh-CN-YunjianNeural", "你好！请给我一个甜面包！"),
    ("guest2_order_ja", "ja-JP-NanamiNeural", "こんにちは！甘いパンを1つください！"),
    ("guest2_thanks", "zh-CN-YunjianNeural", "哇吼！甜甜的面包太香了！非常感谢！"),
    ("guest2_hint", "zh-CN-YunjianNeural", "吼？这好像不是一个甜面包呢，我想吃一个甜面包！"),

    # Guest 3: 小兔米米 (Bunny Mimi)
    ("guest3_order", "zh-CN-XiaoxiaoNeural", "你好！我想吃三个红草莓！"),
    ("guest3_order_ja", "ja-JP-NanamiNeural", "こんにちは！赤いイチゴを3つ食べたいな！"),
    ("guest3_thanks", "zh-CN-XiaoxiaoNeural", "哇，草莓酸酸甜甜，太美味啦！谢谢小主厨！"),
    ("guest3_hint", "zh-CN-XiaoxiaoNeural", "咦？这不是三个红草莓呢，我想吃三个红草莓呀！"),

    # Guest 4: 小狗旺旺 (Puppy Wangwang)
    ("guest4_order", "zh-CN-YunxiNeural", "你好！我想吃一碗热米饭！"),
    ("guest4_order_ja", "ja-JP-NanamiNeural", "こんにちは！あつあつのご飯を1杯食べたいな！"),
    ("guest4_thanks", "zh-CN-YunxiNeural", "汪汪！热气腾腾的米饭真香！谢谢小老板！"),
    ("guest4_hint", "zh-CN-YunxiNeural", "汪？这不是一碗热米饭呢，我想吃一碗热米饭哦！"),

    # Guest 5: 熊猫盼盼 (Panda Panpan)
    ("guest5_order", "zh-CN-YunyangNeural", "你好！我想吃一个大西瓜！"),
    ("guest5_order_ja", "ja-JP-NanamiNeural", "こんにちは！大きなスイカを1つ食べたいな！"),
    ("guest5_thanks", "zh-CN-YunyangNeural", "咕咚！大西瓜好甜好凉快！太棒啦，谢谢！"),
    ("guest5_hint", "zh-CN-YunyangNeural", "嗯？这不是一个大西瓜呢，我想吃一个大西瓜哦！"),

    # Guest 6: 小猴皮皮 (Monkey Pipi)
    ("guest6_order", "zh-CN-YunxiNeural", "你好！我想吃四个黄香蕉！"),
    ("guest6_order_ja", "ja-JP-NanamiNeural", "こんにちは！黄色いバナナを4つ食べたいな！"),
    ("guest6_thanks", "zh-CN-YunxiNeural", "吱吱！四个香蕉太可口了！你真是天才主厨！"),
    ("guest6_hint", "zh-CN-YunxiNeural", "咦？这不是四个黄香蕉呢，我想吃四个黄香蕉！"),

    # Guest 7: 大象伯伯 (Elephant Uncle)
    ("guest7_order", "zh-CN-YunyangNeural", "你好！请给我两杯绿茶！"),
    ("guest7_order_ja", "ja-JP-NanamiNeural", "こんにちは！おいしい緑茶を2杯ください！"),
    ("guest7_thanks", "zh-CN-YunyangNeural", "温润清香，真是好茶！多谢小主厨！"),
    ("guest7_hint", "zh-CN-YunyangNeural", "呵呵，这好像不是两杯绿茶呢，请给我两杯绿茶吧！"),

    # Guest 8: 小鹿悠悠 (Deer Youyou)
    ("guest8_order", "zh-CN-XiaoxiaoNeural", "你好！请给我两杯温牛奶！"),
    ("guest8_order_ja", "ja-JP-NanamiNeural", "こんにちは！あたたかいミルクを2杯ください！"),
    ("guest8_thanks", "zh-CN-XiaoxiaoNeural", "好香好滑的温牛奶，肚子暖烘烘的！谢谢你！"),
    ("guest8_hint", "zh-CN-XiaoxiaoNeural", "咦？这不是两杯温牛奶呢，我想喝两杯温牛奶！"),

    # Guest 9: 小猪嘟嘟 (Piggy Dudu)
    ("guest9_order", "zh-CN-XiaoyiNeural", "你好！我想吃五个香水饺！"),
    ("guest9_order_ja", "ja-JP-NanamiNeural", "こんにちは！おいしい水餃子を5つ食べたいな！"),
    ("guest9_thanks", "zh-CN-XiaoyiNeural", "嗷呜一口！水饺馅料太足啦，超满足！谢谢！"),
    ("guest9_hint", "zh-CN-XiaoyiNeural", "哼哼？这不是五个香水饺呢，我想吃五个香水饺！"),

    # Guest 10: 企鹅波波 (Penguin Bobo)
    ("guest10_order", "zh-CN-XiaoxiaoNeural", "你好！我想吃一块甜蛋糕！"),
    ("guest10_order_ja", "ja-JP-NanamiNeural", "こんにちは！甘いケーキを1つ食べたいな！"),
    ("guest10_thanks", "zh-CN-XiaoxiaoNeural", "哇！草莓奶油甜蛋糕，幸福满满！谢谢！"),
    ("guest10_hint", "zh-CN-XiaoxiaoNeural", "扑棱扑棱~ 这不是甜蛋糕呢，我想吃一块甜蛋糕！"),
]

async def gen_file(name: str, voice: str, text: str):
    target = OUT_DIR / f"{name}.mp3"
    if target.exists() and target.stat().st_size > 500:
        return
    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(target))
            print(f"[OK] {name}.mp3 ({voice}) -> {text[:15]}...")
            return
        except Exception as e:
            print(f"[RETRY {attempt+1}] {name}: {e}")
            await asyncio.sleep(1)
    print(f"[FAIL] {name}")

async def main():
    sem = asyncio.Semaphore(5)
    async def worker(item):
        async with sem:
            await gen_file(*item)
    tasks = [worker(it) for it in ITEMS]
    await asyncio.gather(*tasks)
    print(f"Total files in {OUT_DIR}: {len(list(OUT_DIR.glob('*.mp3')))}")

if __name__ == "__main__":
    asyncio.run(main())
