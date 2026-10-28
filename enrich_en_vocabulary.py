#!/usr/bin/env python3
"""
Enrich English Micro-Narrative lessons (en1 ~ en10) with structured vocabulary layers.
Each lesson receives 6 high-frequency foundation words with:
  - id: {lesson_id}_v{1..6}
  - word: base word
  - phonetic: standard IPA
  - pos: part of speech (n., v., adj., adv., etc.)
  - meaning: concise Chinese meaning
  - example: in-lesson example sentence
  - exampleZh: translation of example
  - audio: audio/en_vocab/{id}.mp3
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_JSON = ROOT / "data" / "en-lessons-data.json"
DATA_JS = ROOT / "data" / "en-lessons-data.js"

LESSON_VOCABULARY = {
    "en1": [
        {
            "id": "en1_v1",
            "word": "latte",
            "phonetic": "/ˈlɑːteɪ/",
            "pos": "n.",
            "meaning": "拿铁咖啡",
            "example": "Can I get an iced oat latte, please?",
            "exampleZh": "请给我来一杯冰燕麦拿铁好吗？",
            "audio": "audio/en_vocab/en1_v1.mp3"
        },
        {
            "id": "en1_v2",
            "word": "iced",
            "phonetic": "/aɪst/",
            "pos": "adj.",
            "meaning": "加冰的，冰镇的",
            "example": "Can I get an iced oat latte, please?",
            "exampleZh": "请给我来一杯冰燕麦拿铁好吗？",
            "audio": "audio/en_vocab/en1_v2.mp3"
        },
        {
            "id": "en1_v3",
            "word": "oat",
            "phonetic": "/oʊt/",
            "pos": "n.",
            "meaning": "燕麦（常指燕麦奶）",
            "example": "Can I get an iced oat latte, please?",
            "exampleZh": "请给我来一杯冰燕麦拿铁好吗？",
            "audio": "audio/en_vocab/en1_v3.mp3"
        },
        {
            "id": "en1_v4",
            "word": "sweet",
            "phonetic": "/swiːt/",
            "pos": "adj.",
            "meaning": "甜的，有甜味的",
            "example": "Could you make it less sweet?",
            "exampleZh": "能帮我做半糖（少甜）吗？",
            "audio": "audio/en_vocab/en1_v4.mp3"
        },
        {
            "id": "en1_v5",
            "word": "counter",
            "phonetic": "/ˈkaʊntər/",
            "pos": "n.",
            "meaning": "柜台，出餐台",
            "example": "It will be ready at the counter in two minutes.",
            "exampleZh": "两分钟后在吧台出单取餐哦。",
            "audio": "audio/en_vocab/en1_v5.mp3"
        },
        {
            "id": "en1_v6",
            "word": "ready",
            "phonetic": "/ˈredi/",
            "pos": "adj.",
            "meaning": "准备好的，备齐的",
            "example": "It will be ready at the counter in two minutes.",
            "exampleZh": "两分钟后在吧台出单取餐哦。",
            "audio": "audio/en_vocab/en1_v6.mp3"
        }
    ],
    "en2": [
        {
            "id": "en2_v1",
            "word": "train",
            "phonetic": "/treɪn/",
            "pos": "n.",
            "meaning": "列车，地铁车次",
            "example": "Which train goes to Central Park?",
            "exampleZh": "哪趟车去中央公园？",
            "audio": "audio/en_vocab/en2_v1.mp3"
        },
        {
            "id": "en2_v2",
            "word": "platform",
            "phonetic": "/ˈplætfɔːrm/",
            "pos": "n.",
            "meaning": "月台，站台",
            "example": "It's on platform two.",
            "exampleZh": "在二号站台上车。",
            "audio": "audio/en_vocab/en2_v2.mp3"
        },
        {
            "id": "en2_v3",
            "word": "transfer",
            "phonetic": "/trænsˈfɜːr/",
            "pos": "v.",
            "meaning": "换乘，转车",
            "example": "Do I need to transfer along the way?",
            "exampleZh": "我中途需要换乘吗？",
            "audio": "audio/en_vocab/en2_v3.mp3"
        },
        {
            "id": "en2_v4",
            "word": "direct",
            "phonetic": "/daɪˈrekt/",
            "pos": "adj.",
            "meaning": "直达的，直接的",
            "example": "No, it's direct.",
            "exampleZh": "不用，这趟是直达的。",
            "audio": "audio/en_vocab/en2_v4.mp3"
        },
        {
            "id": "en2_v5",
            "word": "uptown",
            "phonetic": "/ˌʌpˈtaʊn/",
            "pos": "adv./adj.",
            "meaning": "往北区，上城方向",
            "example": "Take the Blue Line uptown.",
            "exampleZh": "乘坐蓝线上行方向。",
            "audio": "audio/en_vocab/en2_v5.mp3"
        },
        {
            "id": "en2_v6",
            "word": "street",
            "phonetic": "/striːt/",
            "pos": "n.",
            "meaning": "街，街道",
            "example": "Just make sure to get off at 72nd Street.",
            "exampleZh": "只要在第72街下车就行了。",
            "audio": "audio/en_vocab/en2_v6.mp3"
        }
    ],
    "en3": [
        {
            "id": "en3_v1",
            "word": "traffic",
            "phonetic": "/ˈtræfɪk/",
            "pos": "n.",
            "meaning": "交通，车流",
            "example": "Are you caught in traffic?",
            "exampleZh": "你路上堵车了吗？",
            "audio": "audio/en_vocab/en3_v1.mp3"
        },
        {
            "id": "en3_v2",
            "word": "stuck",
            "phonetic": "/stʌk/",
            "pos": "adj.",
            "meaning": "被卡住的，困住的",
            "example": "Yeah, my bus got stuck.",
            "exampleZh": "对啊，我坐的公交车被堵住了。",
            "audio": "audio/en_vocab/en3_v2.mp3"
        },
        {
            "id": "en3_v3",
            "word": "ahead",
            "phonetic": "/əˈhed/",
            "pos": "adv.",
            "meaning": "往前，先行，提前",
            "example": "Please go ahead without me.",
            "exampleZh": "你们先开吧，不用等我。",
            "audio": "audio/en_vocab/en3_v3.mp3"
        },
        {
            "id": "en3_v4",
            "word": "safe",
            "phonetic": "/seɪf/",
            "pos": "adj.",
            "meaning": "安全的，平安的",
            "example": "Take your time and stay safe!",
            "exampleZh": "慢慢来，路上注意安全！",
            "audio": "audio/en_vocab/en3_v4.mp3"
        },
        {
            "id": "en3_v5",
            "word": "late",
            "phonetic": "/leɪt/",
            "pos": "adj.",
            "meaning": "迟到的，晚的",
            "example": "I'm running a bit late.",
            "exampleZh": "我稍微有点赶不上时间了。",
            "audio": "audio/en_vocab/en3_v5.mp3"
        },
        {
            "id": "en3_v6",
            "word": "worries",
            "phonetic": "/ˈwɜːriz/",
            "pos": "n.",
            "meaning": "担忧，顾虑 (No worries 别客气/没关系)",
            "example": "No worries at all!",
            "exampleZh": "完全没关系！",
            "audio": "audio/en_vocab/en3_v6.mp3"
        }
    ],
    "en4": [
        {
            "id": "en4_v1",
            "word": "sandwich",
            "phonetic": "/ˈsænwɪtʃ/",
            "pos": "n.",
            "meaning": "三明治",
            "example": "I'll go with the turkey sandwich combo.",
            "exampleZh": "我要火鸡三明治套餐。",
            "audio": "audio/en_vocab/en4_v1.mp3"
        },
        {
            "id": "en4_v2",
            "word": "combo",
            "phonetic": "/ˈkɑːmboʊ/",
            "pos": "n.",
            "meaning": "套餐，组合餐",
            "example": "I'll go with the turkey sandwich combo.",
            "exampleZh": "我要火鸡三明治套餐。",
            "audio": "audio/en_vocab/en4_v2.mp3"
        },
        {
            "id": "en4_v3",
            "word": "chips",
            "phonetic": "/tʃɪps/",
            "pos": "n.",
            "meaning": "薯片，炸薯条",
            "example": "Chips or an apple on the side?",
            "exampleZh": "配菜要薯片还是苹果？",
            "audio": "audio/en_vocab/en4_v3.mp3"
        },
        {
            "id": "en4_v4",
            "word": "change",
            "phonetic": "/tʃeɪndʒ/",
            "pos": "n.",
            "meaning": "零钱，找零",
            "example": "Here is ten dollars, keep the change!",
            "exampleZh": "这是十美元，不用找零啦！",
            "audio": "audio/en_vocab/en4_v4.mp3"
        },
        {
            "id": "en4_v5",
            "word": "turkey",
            "phonetic": "/ˈtɜːrki/",
            "pos": "n.",
            "meaning": "火鸡肉",
            "example": "I'll go with the turkey sandwich combo.",
            "exampleZh": "我要火鸡三明治套餐。",
            "audio": "audio/en_vocab/en4_v5.mp3"
        },
        {
            "id": "en4_v6",
            "word": "pick",
            "phonetic": "/pɪk/",
            "pos": "n.",
            "meaning": "选择，挑选出的物品",
            "example": "Great pick!",
            "exampleZh": "选得好！/ 眼光不错！",
            "audio": "audio/en_vocab/en4_v6.mp3"
        }
    ],
    "en5": [
        {
            "id": "en5_v1",
            "word": "aisle",
            "phonetic": "/aɪl/",
            "pos": "n.",
            "meaning": "过道，货架走廊",
            "example": "It's in aisle four, right next to the vinegar.",
            "exampleZh": "在4号通道，就在醋的旁边。",
            "audio": "audio/en_vocab/en5_v1.mp3"
        },
        {
            "id": "en5_v2",
            "word": "organic",
            "phonetic": "/ɔːrˈɡænɪk/",
            "pos": "adj.",
            "meaning": "有机的，纯天然的",
            "example": "And are organic eggs in the back?",
            "exampleZh": "请问有机鸡蛋在后排吗？",
            "audio": "audio/en_vocab/en5_v2.mp3"
        },
        {
            "id": "en5_v3",
            "word": "stock",
            "phonetic": "/stɑːk/",
            "pos": "n.",
            "meaning": "存货，库存 (out of stock 缺货)",
            "example": "They are currently out of stock.",
            "exampleZh": "目前已经卖完了（缺货）。",
            "audio": "audio/en_vocab/en5_v3.mp3"
        },
        {
            "id": "en5_v4",
            "word": "batch",
            "phonetic": "/bætʃ/",
            "pos": "n.",
            "meaning": "一批，批次",
            "example": "A new batch arrives tomorrow.",
            "exampleZh": "明天会新到一批。",
            "audio": "audio/en_vocab/en5_v4.mp3"
        },
        {
            "id": "en5_v5",
            "word": "vinegar",
            "phonetic": "/ˈvɪnɪɡər/",
            "pos": "n.",
            "meaning": "食醋",
            "example": "Right next to the vinegar.",
            "exampleZh": "就在食醋的旁边。",
            "audio": "audio/en_vocab/en5_v5.mp3"
        },
        {
            "id": "en5_v6",
            "word": "arrive",
            "phonetic": "/əˈraɪv/",
            "pos": "v.",
            "meaning": "到达，到货",
            "example": "A new batch arrives tomorrow.",
            "exampleZh": "新的一批货明天送到。",
            "audio": "audio/en_vocab/en5_v6.mp3"
        }
    ],
    "en6": [
        {
            "id": "en6_v1",
            "word": "exhibition",
            "phonetic": "/ˌeksɪˈbɪʃn/",
            "pos": "n.",
            "meaning": "展览，展出",
            "example": "Are you up for that modern art exhibition this Saturday?",
            "exampleZh": "这周六有兴趣去看看那个现代艺术展吗？",
            "audio": "audio/en_vocab/en6_v1.mp3"
        },
        {
            "id": "en6_v2",
            "word": "modern",
            "phonetic": "/ˈmɑːdərn/",
            "pos": "adj.",
            "meaning": "现代的，摩登的",
            "example": "Are you up for that modern art exhibition this Saturday?",
            "exampleZh": "这周六有兴趣去看看那个现代艺术展吗？",
            "audio": "audio/en_vocab/en6_v2.mp3"
        },
        {
            "id": "en6_v3",
            "word": "gallery",
            "phonetic": "/ˈɡæləri/",
            "pos": "n.",
            "meaning": "画廊，艺术展馆",
            "example": "Let's meet in front of the gallery.",
            "exampleZh": "咱们在美术馆门口碰头吧。",
            "audio": "audio/en_vocab/en6_v3.mp3"
        },
        {
            "id": "en6_v4",
            "word": "grab",
            "phonetic": "/ɡræb/",
            "pos": "v.",
            "meaning": "抓取；(口语)顺便吃/买",
            "example": "We could grab lunch before that.",
            "exampleZh": "在那之前我们还可以顺便吃个午饭。",
            "audio": "audio/en_vocab/en6_v4.mp3"
        },
        {
            "id": "en6_v5",
            "word": "afternoon",
            "phonetic": "/ˌæftərˈnuːn/",
            "pos": "n.",
            "meaning": "下午",
            "example": "How about two in the afternoon?",
            "exampleZh": "下午两点怎么样？",
            "audio": "audio/en_vocab/en6_v5.mp3"
        },
        {
            "id": "en6_v6",
            "word": "plan",
            "phonetic": "/plæn/",
            "pos": "n.",
            "meaning": "计划 (Sounds like a plan 好主意/就这么定)",
            "example": "Sounds like a plan!",
            "exampleZh": "听起来是个好主意！",
            "audio": "audio/en_vocab/en6_v6.mp3"
        }
    ],
    "en7": [
        {
            "id": "en7_v1",
            "word": "keycard",
            "phonetic": "/ˈkiːkɑːrd/",
            "pos": "n.",
            "meaning": "房卡，感应钥匙卡",
            "example": "Here is your keycard for room 508.",
            "exampleZh": "这是您508号房间的房卡。",
            "audio": "audio/en_vocab/en7_v1.mp3"
        },
        {
            "id": "en7_v2",
            "word": "floor",
            "phonetic": "/flɔːr/",
            "pos": "n.",
            "meaning": "楼层",
            "example": "Room 508 on the top floor.",
            "exampleZh": "顶层的508号房。",
            "audio": "audio/en_vocab/en7_v2.mp3"
        },
        {
            "id": "en7_v3",
            "word": "breakfast",
            "phonetic": "/ˈbrekfəst/",
            "pos": "n.",
            "meaning": "早餐",
            "example": "What time is breakfast served tomorrow?",
            "exampleZh": "明天早餐几点供应？",
            "audio": "audio/en_vocab/en7_v3.mp3"
        },
        {
            "id": "en7_v4",
            "word": "served",
            "phonetic": "/sɜːrvd/",
            "pos": "v.",
            "meaning": "供应，提供（serve的过去分词）",
            "example": "From seven to ten on the second floor.",
            "exampleZh": "早上7点到10点在二楼供应。",
            "audio": "audio/en_vocab/en7_v4.mp3"
        },
        {
            "id": "en7_v5",
            "word": "welcome",
            "phonetic": "/ˈwelkəm/",
            "pos": "interj./v.",
            "meaning": "欢迎",
            "example": "Welcome! Here is your keycard.",
            "exampleZh": "欢迎光临！这是您的房卡。",
            "audio": "audio/en_vocab/en7_v5.mp3"
        },
        {
            "id": "en7_v6",
            "word": "enjoy",
            "phonetic": "/ɪnˈdʒɔɪ/",
            "pos": "v.",
            "meaning": "享受，祝...愉快",
            "example": "Enjoy your stay!",
            "exampleZh": "祝您入住愉快！",
            "audio": "audio/en_vocab/en7_v6.mp3"
        }
    ],
    "en8": [
        {
            "id": "en8_v1",
            "word": "exchange",
            "phonetic": "/ɪksˈtʃeɪndʒ/",
            "pos": "v./n.",
            "meaning": "调换，换货",
            "example": "I'm looking to exchange this jacket for a size up.",
            "exampleZh": "我想把这件夹克换大一个尺码。",
            "audio": "audio/en_vocab/en8_v1.mp3"
        },
        {
            "id": "en8_v2",
            "word": "jacket",
            "phonetic": "/ˈdʒækɪt/",
            "pos": "n.",
            "meaning": "夹克，外套",
            "example": "Exchange this jacket for a size up.",
            "exampleZh": "把这件夹克换大一个尺码。",
            "audio": "audio/en_vocab/en8_v2.mp3"
        },
        {
            "id": "en8_v3",
            "word": "receipt",
            "phonetic": "/rɪˈsiːt/",
            "pos": "n.",
            "meaning": "收据，购物小票",
            "example": "Do you happen to have the receipt with you?",
            "exampleZh": "请问您身上带了小票吗？",
            "audio": "audio/en_vocab/en8_v3.mp3"
        },
        {
            "id": "en8_v4",
            "word": "tight",
            "phonetic": "/taɪt/",
            "pos": "adj.",
            "meaning": "紧绷的，偏紧的",
            "example": "It's just a bit tight around the shoulders.",
            "exampleZh": "肩膀位置稍微有点紧。",
            "audio": "audio/en_vocab/en8_v4.mp3"
        },
        {
            "id": "en8_v5",
            "word": "shoulder",
            "phonetic": "/ˈʃoʊldər/",
            "pos": "n.",
            "meaning": "肩膀，肩部",
            "example": "A bit tight around the shoulders.",
            "exampleZh": "肩膀位置稍微有点紧。",
            "audio": "audio/en_vocab/en8_v5.mp3"
        },
        {
            "id": "en8_v6",
            "word": "medium",
            "phonetic": "/ˈmiːdiəm/",
            "pos": "n./adj.",
            "meaning": "中号，中码",
            "example": "Let me grab a medium from the back for you right now.",
            "exampleZh": "我现在去库房为您取一件中码。",
            "audio": "audio/en_vocab/en8_v6.mp3"
        }
    ],
    "en9": [
        {
            "id": "en9_v1",
            "word": "heavy",
            "phonetic": "/ˈhevi/",
            "pos": "adj.",
            "meaning": "沉重的，厚重的",
            "example": "Could you give me a hand with this heavy box?",
            "exampleZh": "能搭把手帮我抬一下这个沉箱子吗？",
            "audio": "audio/en_vocab/en9_v1.mp3"
        },
        {
            "id": "en9_v2",
            "word": "trunk",
            "phonetic": "/trʌŋk/",
            "pos": "n.",
            "meaning": "(汽车的) 后备箱",
            "example": "Just over by the trunk.",
            "exampleZh": "就在后备箱旁边就行。",
            "audio": "audio/en_vocab/en9_v2.mp3"
        },
        {
            "id": "en9_v3",
            "word": "appreciate",
            "phonetic": "/əˈpriːʃieɪt/",
            "pos": "v.",
            "meaning": "感激，感谢",
            "example": "I really appreciate it!",
            "exampleZh": "真的太感谢你了！",
            "audio": "audio/en_vocab/en9_v3.mp3"
        },
        {
            "id": "en9_v4",
            "word": "hand",
            "phonetic": "/hænd/",
            "pos": "n.",
            "meaning": "帮助，援手 (give a hand 帮把手)",
            "example": "Could you give me a hand with this heavy box?",
            "exampleZh": "能搭把手帮我抬一下这个沉箱子吗？",
            "audio": "audio/en_vocab/en9_v4.mp3"
        },
        {
            "id": "en9_v5",
            "word": "mind",
            "phonetic": "/maɪnd/",
            "pos": "v.",
            "meaning": "介意，在乎 (Do you mind... 介意...吗)",
            "example": "Do you mind if I grab this side?",
            "exampleZh": "你介意我抓这一侧吗？",
            "audio": "audio/en_vocab/en9_v5.mp3"
        },
        {
            "id": "en9_v6",
            "word": "glad",
            "phonetic": "/ɡlæd/",
            "pos": "adj.",
            "meaning": "乐意的，高兴的 (Glad to help 很高兴能帮上忙)",
            "example": "Glad to help. Have a good one!",
            "exampleZh": "乐意效劳，祝你有愉快的一天！",
            "audio": "audio/en_vocab/en9_v6.mp3"
        }
    ],
    "en10": [
        {
            "id": "en10_v1",
            "word": "weather",
            "phonetic": "/ˈweðər/",
            "pos": "n.",
            "meaning": "天气，气象",
            "example": "Crazy weather today, huh?",
            "exampleZh": "今天天气真怪，是吧？",
            "audio": "audio/en_vocab/en10_v1.mp3"
        },
        {
            "id": "en10_v2",
            "word": "umbrella",
            "phonetic": "/ʌmˈbrelə/",
            "pos": "n.",
            "meaning": "雨伞",
            "example": "Did you bring an umbrella?",
            "exampleZh": "你带伞了吗？",
            "audio": "audio/en_vocab/en10_v2.mp3"
        },
        {
            "id": "en10_v3",
            "word": "sunny",
            "phonetic": "/ˈsʌni/",
            "pos": "adj.",
            "meaning": "晴朗的，充满阳光的",
            "example": "It was completely sunny this morning.",
            "exampleZh": "今天早上还大晴天呢。",
            "audio": "audio/en_vocab/en10_v3.mp3"
        },
        {
            "id": "en10_v4",
            "word": "luckily",
            "phonetic": "/ˈlʌkɪli/",
            "pos": "adv.",
            "meaning": "幸运的是，万幸",
            "example": "Luckily, I keep one in my bag.",
            "exampleZh": "幸好我包里常备着一把。",
            "audio": "audio/en_vocab/en10_v4.mp3"
        },
        {
            "id": "en10_v5",
            "word": "completely",
            "phonetic": "/kəmˈpliːtli/",
            "pos": "adv.",
            "meaning": "完全地，彻底地",
            "example": "It was completely sunny this morning.",
            "exampleZh": "今天早上完全是个大晴天。",
            "audio": "audio/en_vocab/en10_v5.mp3"
        },
        {
            "id": "en10_v6",
            "word": "minute",
            "phonetic": "/ˈmɪnɪt/",
            "pos": "n.",
            "meaning": "分钟；片刻 (any minute now 随时都会)",
            "example": "Looks like rain any minute now.",
            "exampleZh": "看着随时都会下雨的样子。",
            "audio": "audio/en_vocab/en10_v6.mp3"
        }
    ]
}

def main():
    lessons = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    
    total_vocab = 0
    for lesson in lessons:
        lid = lesson["id"]
        vocab_items = LESSON_VOCABULARY.get(lid, [])
        lesson["vocabulary"] = vocab_items
        total_vocab += len(vocab_items)
        print(f"[{lid}] Added {len(vocab_items)} vocabulary words: {', '.join(v['word'] for v in vocab_items)}")

    # Write updated JSON
    DATA_JSON.write_text(json.dumps(lessons, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved {total_vocab} words across {len(lessons)} lessons to {DATA_JSON.name}")

    # Write updated JS
    js_content = f"// English Micro-Narrative Curriculum Data\n// 3-Tier Scaffolding Architecture + Lexical Vocabulary Support\nwindow.EN_LESSONS_DATA = {json.dumps(lessons, indent=2, ensure_ascii=False)};\n"
    DATA_JS.write_text(js_content, encoding="utf-8")
    print(f"Synchronized window.EN_LESSONS_DATA to {DATA_JS.name}")

if __name__ == "__main__":
    main()
