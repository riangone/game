#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_chinese_lessons.py
Architect build script for the brand new Chinese Situational Lesson series:
- zh0.html (Level 0: 汉语拼音与日常问候)
- zh1.html (Level 1: 我的一星期)
- zh2.html (Level 2: 我的一天)
- zh3.html (Level 3: 中国的四季)
- zh-index.html (Course Catalog & Portal)
"""

import os
import re
import json

BASE_DIR = '/home/ubuntu/ws/jump-jump-game'

# ----------------- LESSON DATA DEFINITIONS -----------------

LESSONS = [
    {
        "id": "zh0",
        "lesson_num": "0",
        "title": "拼音与日常问候 - 汉语课文识字闯关 (Pinyin & Greetings)",
        "canonical": "https://zw.0101.click/zh0.html",
        "header_title": "拼音与日常问候",
        "title_en": "Pinyin &amp; Greetings",
        "sub_desc": "跟随原创启蒙课文初识汉语拼音（声母、韵母与四声调），掌握高频日常礼貌问候与12个基础象形汉字！本课是全新原创汉语课程体系的入门序章（第0课）。",
        "story_title": "📖 拼音与日常问候 (Pinyin &amp; Greetings)",
        "full_title": "📜 汉语拼音与问候 · 全文",
        "palace_svg": """<svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="28" fill="#fff" stroke="#b91c1c" stroke-width="3"/>
          <circle cx="32" cy="32" r="23" fill="#fff7ed" stroke="#fbd38d" stroke-width="1.5"/>
          <text x="32" y="44" font-family="'M PLUS Rounded 1c', sans-serif" font-size="30" font-weight="900" fill="#b91c1c" text-anchor="middle">拼</text>
        </svg>""",
        "proper_label": "口语",
        "has_pinyin_chart": True,
        "story": [
            {"id":"st1", "zh":"拼音是汉字的翅膀，让我们开始快乐学中文。", "py":"Pīnyīn shì hànzì de chìbǎng, ràng wǒmen kāishǐ kuàilè xué zhōngwén.", "en":"Pinyin is the wings of Chinese characters; let's begin learning Chinese happily.", "jp":"ピンインは漢字の翼です。楽しく中国語を学び始めましょう。"},
            {"id":"st2", "zh":"早晨相遇，微笑着说一声“早上好”！", "py":"Zǎochén xiāngyù, wēixiàozhe shuō yì shēng “Zǎoshang hǎo”!", "en":"Meeting in the morning, say “Good morning” with a bright smile!", "jp":"朝会ったら、笑顔で「おはようございます」と言いましょう！"},
            {"id":"st3", "zh":"朋友见面，热情地打招呼“你好”！", "py":"Péngyou jiànmiàn, rèqíng de dǎ zhāohu “Nǐ hǎo”!", "en":"When meeting friends, warmly greet them with “Hello”!", "jp":"友達に会ったら、元気に「こんにちは」と挨拶します！"},
            {"id":"st4", "zh":"夜幕降临，道一声温暖的“晚上好”。", "py":"Yèmù jiànglín, dào yì shēng wēnnuǎn de “Wǎnshang hǎo”.", "en":"When night falls, send a warm greeting: “Good evening”.", "jp":"夜が来たら、温かく「こんばんは」と声をかけます。"},
            {"id":"st5", "zh":"得到帮助，真诚地说一声“谢谢”。", "py":"Dédào bāngzhù, zhēnchéng de shuō yì shēng “Xièxie”.", "en":"When receiving help, sincerely say “Thank you”.", "jp":"助けてもらったら、心を込めて「ありがとう」と言います。"},
            {"id":"st6", "zh":"礼貌回应，温和地说“不客气”。", "py":"Lǐmào huíyìng, wēnhé de shuō “Bú kèqi”.", "en":"Politely respond and gently say “You're welcome”.", "jp":"礼儀正しく、優しく「どういたしまして」と返します。"},
            {"id":"st7", "zh":"如果不小心做错了，主动说“对不起”。", "py":"Rúguǒ bù xiǎoxīn zuòcuò le, zhǔdòng shuō “Duìbuqǐ”.", "en":"If accidentally making a mistake, take the initiative to say “Sorry”.", "jp":"うっかり間違えたら、自分から「ごめんなさい」と言います。"},
            {"id":"st8", "zh":"互相理解与包容，挥挥手说“再见”！", "py":"Hùxiāng lǐjiě yǔ bāoróng, huīhui shǒu shuō “Zàijiàn”!", "en":"Understanding and forgiving each other, wave hands and say “Goodbye”!", "jp":"お互いに理解し合い、手を振って「さようなら」と言いましょう！"}
        ],
        "characters": [
            {"id":"zi1", "zh":"一", "py":"yī", "radical":"一部（自体即部首）", "radicalBadge":None, "words":"一个、第一、一起", "meaning":"one", "meaningJp":"ひとつ", "context":"早晨相遇，微笑着说一声“早上好”"},
            {"id":"zi2", "zh":"二", "py":"èr", "radical":"二部（自体即部首）", "radicalBadge":None, "words":"二月、十二、二人", "meaning":"two", "meaningJp":"ふたつ", "context":"基础数字象形汉字"},
            {"id":"zi3", "zh":"三", "py":"sān", "radical":"一部（一字旁）", "radicalBadge":None, "words":"三天、三个、三月", "meaning":"three", "meaningJp":"みっつ", "context":"基础数字象形汉字"},
            {"id":"zi4", "zh":"四", "py":"sì", "radical":"囗部（大口框）", "radicalBadge":"囗 —— 四", "words":"四个、四季、四周", "meaning":"four", "meaningJp":"よっつ", "context":"四声调与基础数字"},
            {"id":"zi5", "zh":"五", "py":"wǔ", "radical":"二部（二字头）", "radicalBadge":None, "words":"五个、五年、五月", "meaning":"five", "meaningJp":"いつつ", "context":"基础数字象形汉字"},
            {"id":"zi6", "zh":"人", "py":"rén", "radical":"人部（自体即部首）", "radicalBadge":None, "words":"人们、大家、大人", "meaning":"person / people", "meaningJp":"ひと", "context":"早晨相遇，微笑着向大家问好"},
            {"id":"zi7", "zh":"口", "py":"kǒu", "radical":"口部（自体即部首）", "radicalBadge":None, "words":"开口、门口、口水", "meaning":"mouth / opening", "meaningJp":"くち", "context":"微笑着开口打招呼"},
            {"id":"zi8", "zh":"手", "py":"shǒu", "radical":"手部（自体即部首）", "radicalBadge":None, "words":"双手、挥手、小手", "meaning":"hand", "meaningJp":"て", "context":"挥挥手说一声再见"},
            {"id":"zi9", "zh":"日", "py":"rì", "radical":"日部（自体即部首）", "radicalBadge":None, "words":"日子、日出、今日", "meaning":"sun / day", "meaningJp":"ひ / にち", "context":"象形文字：太阳与日子"},
            {"id":"zi10", "zh":"月", "py":"yuè", "radical":"月部（自体即部首）", "radicalBadge":None, "words":"月亮、月光、岁月", "meaning":"moon / month", "meaningJp":"つき / がつ", "context":"夜幕降临，月亮升起"},
            {"id":"zi11", "zh":"大", "py":"dà", "radical":"大部（自体即部首）", "radicalBadge":None, "words":"大家、大声、大地", "meaning":"big / great", "meaningJp":"おおきい", "context":"向大家问好，大声读拼音"},
            {"id":"zi12", "zh":"小", "py":"xiǎo", "radical":"小部（自体即部首）", "radicalBadge":None, "words":"小朋友、小心、小学", "meaning":"small / little", "meaningJp":"ちいさい", "context":"如果不小心做错了"}
        ],
        "words": [
            {"id":"ci1", "zh":"你好", "py":"nǐhǎo", "meaning":"hello", "meaningJp":"こんにちは", "emoji":"👋", "context":"朋友见面，热情地打招呼“你好”！", "tag":"寒暄"},
            {"id":"ci2", "zh":"早上好", "py":"zǎoshang hǎo", "meaning":"good morning", "meaningJp":"おはようございます", "emoji":"🌅", "context":"早晨相遇，微笑着说一声“早上好”！", "tag":"寒暄"},
            {"id":"ci3", "zh":"晚上好", "py":"wǎnshang hǎo", "meaning":"good evening", "meaningJp":"こんばんは", "emoji":"🌙", "context":"夜幕降临，道一声温暖的“晚上好”。", "tag":"寒暄"},
            {"id":"ci4", "zh":"谢谢", "py":"xièxie", "meaning":"thank you", "meaningJp":"ありがとう", "emoji":"🙏", "context":"得到帮助，真诚地说一声“谢谢”。", "tag":"礼貌"},
            {"id":"ci5", "zh":"不客气", "py":"bú kèqi", "meaning":"you're welcome", "meaningJp":"どういたしまして", "emoji":"😊", "context":"礼貌回应，温和地说“不客气”。", "tag":"礼貌"},
            {"id":"ci6", "zh":"对不起", "py":"duìbuqǐ", "meaning":"sorry", "meaningJp":"ごめんなさい", "emoji":"🙇", "context":"如果不小心做错了，主动说“对不起”。", "tag":"礼貌"},
            {"id":"ci7", "zh":"没关系", "py":"méi guānxi", "meaning":"it's okay / never mind", "meaningJp":"大丈夫です", "emoji":"👌", "context":"没关系，我们一起玩吧！", "tag":"礼貌"},
            {"id":"ci8", "zh":"再见", "py":"zàijiàn", "meaning":"goodbye", "meaningJp":"さようなら", "emoji":"🛫", "context":"互相理解与包容，挥挥手说“再见”！", "tag":"寒暄"},
            {"id":"ci9", "zh":"拼音", "py":"pīnyīn", "meaning":"Pinyin", "meaningJp":"ピンイン", "emoji":"🔤", "context":"拼音是汉字的翅膀，让我们开始快乐学中文。", "tag":"语言"},
            {"id":"ci10", "zh":"汉字", "py":"hànzì", "meaning":"Chinese character", "meaningJp":"漢字", "emoji":"🇨🇳", "context":"拼音是汉字的翅膀，帮助我们识字。", "tag":"语言"},
            {"id":"ci11", "zh":"中文", "py":"zhōngwén", "meaning":"Chinese language", "meaningJp":"中国語", "emoji":"📚", "context":"让我们开始快乐学中文。", "tag":"语言"},
            {"id":"ci12", "zh":"朋友", "py":"péngyou", "meaning":"friend", "meaningJp":"友達", "emoji":"🤝", "context":"朋友见面，热情地打招呼“你好”！", "tag":"日常"}
        ],
        "proper_nouns": [
            {"id":"pn1", "zh":"请", "py":"qǐng", "meaning":"please", "meaningJp":"どうぞ / お願いします", "emoji":"👉", "context":"请进，请坐！", "tag":"口语"},
            {"id":"pn2", "zh":"是的", "py":"shìde", "meaning":"yes", "meaningJp":"はい、そうです", "emoji":"✅", "context":"是的，我是学生。", "tag":"口语"},
            {"id":"pn3", "zh":"不是", "py":"búshì", "meaning":"no / not", "meaningJp":"いいえ、違います", "emoji":"❌", "context":"这不是我的书包。", "tag":"口语"},
            {"id":"pn4", "zh":"好的", "py":"hǎode", "meaning":"okay / all right", "meaningJp":"わかりました", "emoji":"👍", "context":"好的，我们一起做作业。", "tag":"口语"},
            {"id":"pn5", "zh":"欢迎", "py":"huānyíng", "meaning":"welcome", "meaningJp":"ようこそ", "emoji":"🎉", "context":"欢迎大家来学中文！", "tag":"口语"},
            {"id":"pn6", "zh":"明天见", "py":"míngtiān jiàn", "meaning":"see you tomorrow", "meaningJp":"また明日", "emoji":"👋", "context":"放学了，我们明天见！", "tag":"口语"},
            {"id":"pn7", "zh":"加油", "py":"jiāyóu", "meaning":"keep it up / cheer on", "meaningJp":"がんばって", "emoji":"💪", "context":"大家一起努力，加油！", "tag":"口语"}
        ],
        "scramble_sentences": [
            {
                "id": "sent1",
                "zh": "微笑着说一声早上好！",
                "tokens": ["微笑着", "说一声", "早上好！"],
                "isKey": True
            },
            {
                "id": "st1",
                "zh": "拼音是汉字的翅膀，让我们开始快乐学中文。",
                "tokens": ["拼音是", "汉字的翅膀，", "让我们开始", "快乐学中文。"]
            },
            {
                "id": "st3",
                "zh": "朋友见面，热情地打招呼你好！",
                "tokens": ["朋友见面，", "热情地", "打招呼", "你好！"]
            },
            {
                "id": "st5",
                "zh": "得到帮助，真诚地说一声谢谢。",
                "tokens": ["得到帮助，", "真诚地", "说一声", "谢谢。"]
            },
            {
                "id": "st8",
                "zh": "互相理解与包容，挥挥手说再见！",
                "tokens": ["互相理解", "与包容，", "挥挥手", "说再见！"]
            }
        ],
        "quiz": [
            {"q":"早上和老师、同学相遇时，最常用的问候语是什么？", "opts":["晚上好", "早上好", "对不起", "再见"], "a":1},
            {"q":"别人向你提供了热心帮助，应该礼貌地说什么？", "opts":["不客气", "没关系", "谢谢", "好的"], "a":2},
            {"q":"当别人向你真诚道谢（说“谢谢”）时，你应该怎样回应？", "opts":["对不起", "不客气", "再见", "是的"], "a":1},
            {"q":"如果不小心踩到了别人的脚，应该主动说什么？", "opts":["对不起", "你好", "谢谢", "加油"], "a":0},
            {"q":"汉字“口”的部首是什么？", "opts":["口部（自体即部首）", "日部", "目部", "人部"], "a":0},
            {"q":"基础象形字“日”最初来源于古代人对什么的描画？", "opts":["月亮", "太阳", "山川", "河流"], "a":1},
            {"q":"汉语拼音里的声调一共有几个基本声调？", "opts":["两个", "三个", "四个", "五个"], "a":2},
            {"q":"放学与朋友道别时，通常会说什么？", "opts":["你好", "欢迎", "再见", "不客气"], "a":2}
        ],
        "cloze": [
            {
                "id": "zh_c1",
                "type": "text",
                "before": "朋友见面，热情地打招呼“",
                "answer": "你好",
                "after": "”！",
                "py": "Péngyou jiànmiàn, rèqíng de dǎ zhāohu “Nǐ hǎo”!",
                "en": "When meeting friends, warmly greet them with “Hello”!",
                "jp": "友達に会ったら「こんにちは」と挨拶します！",
                "answerPy": "nǐ hǎo",
                "options": ["你好", "晚上好", "再见", "谢谢"],
                "hint": "课文原句 · 朋友相遇常用问候",
                "audioId": "cloze_1"
            },
            {
                "id": "zh_c2",
                "type": "text",
                "before": "早晨相遇，微笑着说一声“",
                "answer": "早上好",
                "after": "”！",
                "py": "Zǎochén xiāngyù, wēixiàozhe shuō yì shēng “Zǎoshang hǎo”!",
                "en": "Meeting in the morning, say “Good morning” with a smile!",
                "jp": "朝会ったら「おはよう」と言います！",
                "answerPy": "zǎo shang hǎo",
                "options": ["早上好", "对不起", "没关系", "欢迎"],
                "hint": "课文原句 · 清晨问候",
                "audioId": "cloze_2"
            },
            {
                "id": "zh_c3",
                "type": "text",
                "before": "得到帮助，真诚地说一声“",
                "answer": "谢谢",
                "after": "”。",
                "py": "Dédào bāngzhù, zhēnchéng de shuō yì shēng “Xièxie”.",
                "en": "When receiving help, sincerely say “Thank you”.",
                "jp": "助けてもらったら「ありがとう」と言います。",
                "answerPy": "xiè xie",
                "options": ["谢谢", "不客气", "早上好", "加油"],
                "hint": "课文原句 · 表达感谢",
                "audioId": "cloze_3"
            },
            {
                "id": "zh_c4",
                "type": "text",
                "before": "如果不小心做错了，主动说“",
                "answer": "对不起",
                "after": "”。",
                "py": "Rúguǒ bù xiǎoxīn zuòcuò le, zhǔdòng shuō “Duìbuqǐ”.",
                "en": "If accidentally making a mistake, take the initiative to say “Sorry”.",
                "jp": "間違えたら「ごめんなさい」と言います。",
                "answerPy": "duì bu qǐ",
                "options": ["对不起", "你好", "再见", "好的"],
                "hint": "课文原句 · 主动道歉",
                "audioId": "cloze_4"
            },
            {
                "id": "zh_c5",
                "type": "text",
                "before": "礼貌回应，温和地说“",
                "answer": "不客气",
                "after": "”。",
                "py": "Lǐmào huíyìng, wēnhé de shuō “Bú kèqi”.",
                "en": "Politely respond and gently say “You're welcome”.",
                "jp": "優しく「どういたしまして」と返します。",
                "answerPy": "bú kè qi",
                "options": ["不客气", "对不起", "你好", "明天见"],
                "hint": "课文原句 · 礼貌回应致谢",
                "audioId": "cloze_5"
            },
            {
                "id": "zh_c6",
                "type": "text",
                "before": "夜幕降临，道一声温暖的“",
                "answer": "晚上好",
                "after": "”。",
                "py": "Yèmù jiànglín, dào yì shēng wēnnuǎn de “Wǎnshang hǎo”.",
                "en": "When night falls, send a warm greeting: “Good evening”.",
                "jp": "夜が来たら「こんばんは」と声をかけます。",
                "answerPy": "wǎn shang hǎo",
                "options": ["晚上好", "早上好", "对不起", "谢谢"],
                "hint": "课文原句 · 夜晚问候",
                "audioId": "cloze_6"
            },
            {
                "id": "zh_c7",
                "type": "text",
                "before": "互相理解与包容，挥挥手说“",
                "answer": "再见",
                "after": "”！",
                "py": "Hùxiāng lǐjiě yǔ bāoróng, huīhui shǒu shuō “Zàijiàn”!",
                "en": "Understanding each other, wave hands and say “Goodbye”!",
                "jp": "手を振って「さようなら」と言いましょう！",
                "answerPy": "zài jiàn",
                "options": ["再见", "你好", "加油", "是的"],
                "hint": "课文原句 · 道别用语",
                "audioId": "cloze_7"
            },
            {
                "id": "zh_c8",
                "type": "text",
                "before": "拼音是汉字的翅膀，让我们开始快乐学",
                "answer": "中文",
                "after": "。",
                "py": "Pīnyīn shì hànzì de chìbǎng, ràng wǒmen kāishǐ kuàilè xué zhōngwén.",
                "en": "Pinyin is the wings of Chinese characters; let's begin learning Chinese happily.",
                "jp": "楽しく中国語を学び始めましょう。",
                "answerPy": "zhōng wén",
                "options": ["中文", "数字", "画画", "跳舞"],
                "hint": "课文原句 · 学习语言",
                "audioId": "cloze_8"
            }
        ]
    },
    {
        "id": "zh1",
        "lesson_num": "1",
        "title": "我的一星期 - 汉语课文识字闯关 (My Week)",
        "canonical": "https://zw.0101.click/zh1.html",
        "header_title": "我的一星期",
        "title_en": "My Week in Chinese",
        "sub_desc": "跟随原创情境课文《我的一星期》走进校园与家庭生活，掌握一周七天时间表达、学校爱好动词与12个核心汉字！本课是全新原创汉语课程第1课。",
        "story_title": "📖 我的一星期 (My Week)",
        "full_title": "📜 我的一星期 · 全文",
        "palace_svg": """<svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="28" fill="#fff" stroke="#b91c1c" stroke-width="3"/>
          <path d="M16 22 L48 22 L48 48 L16 48 Z" fill="#fff7ed" stroke="#b91c1c" stroke-width="2"/>
          <line x1="16" y1="30" x2="48" y2="30" stroke="#b91c1c" stroke-width="2"/>
          <line x1="26" y1="18" x2="26" y2="24" stroke="#b91c1c" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="38" y1="18" x2="38" y2="24" stroke="#b91c1c" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="24" cy="38" r="2.5" fill="#d97706"/>
          <circle cx="32" cy="38" r="2.5" fill="#d97706"/>
          <circle cx="40" cy="38" r="2.5" fill="#d97706"/>
        </svg>""",
        "proper_label": "时间",
        "has_pinyin_chart": False,
        "story": [
            {"id":"st1", "zh":"星期一，朝阳升起，我们背上书包高高兴兴去学校。", "py":"Xīngqīyī, zhāoyáng shēngqǐ, wǒmen bēishang shūbāo gāogāoxìngxìng qù xuéxiào.", "en":"On Monday, morning sun rises, we carry our schoolbags happily to school.", "jp":"月曜日、朝の光が昇り、私たちはランドセルを背負って元気に登校します。"},
            {"id":"st2", "zh":"星期二，我们在明亮的教室里认真听讲、学习中文。", "py":"Xīngqī'èr, wǒmen zài míngliàng de jiàoshì lǐ rènzhēn tīngjiǎng, xuéxí zhōngwén.", "en":"On Tuesday, we listen attentively and study Chinese in the bright classroom.", "jp":"火曜日、私たちは明るい教室で真剣に先生の話を聞き、中国語を学びます。"},
            {"id":"st3", "zh":"星期三，下课后我和同学们在操场上听优美的音乐。", "py":"Xīngqīsān, xiàkè hòu wǒ hé tóngxuémen zài cāochǎng shang tīng yōuměi de yīnyuè.", "en":"On Wednesday, after class my classmates and I listen to beautiful music on the playground.", "jp":"水曜日、放課後にクラスメイトとグラウンドで美しい音楽を聴きます。"},
            {"id":"st4", "zh":"星期四，我们走进安静的图书馆，津津有味地看书。", "py":"Xīngqīsì, wǒmen zǒujìn ānjìng de túshūguǎn, jīnjīnyǒuwèi de kàn shū.", "en":"On Thursday, we walk into the quiet library and read books with keen interest.", "jp":"木曜日、私たちは静かな図書館に入り、夢中になって本を読みます。"},
            {"id":"st5", "zh":"星期五，大家一起唱歌跳舞，开开心心迎接周末。", "py":"Xīngqīwǔ, dàjiā yìqǐ chàng gē tiào wǔ, kāikāixīnxīn yíngjiē zhōumò.", "en":"On Friday, everyone sings and dances together, joyfully welcoming the weekend.", "jp":"金曜日、みんなで歌って踊り、楽しく週末を迎えます。"},
            {"id":"st6", "zh":"星期六，我和爸爸妈妈去公园散步，看盛开的鲜花。", "py":"Xīngqīliù, wǒ hé bàba māma qù gōngyuán sànbù, kàn shèngkāi de xiānhuā.", "en":"On Saturday, my parents and I go strolling in the park, admiring blooming flowers.", "jp":"土曜日、私は両親と公園へ散歩に行き、満開の花を眺めます。"},
            {"id":"st7", "zh":"星期天，我喜欢坐在温暖的家里画画，享受休息日。", "py":"Xīngqītiān, wǒ xǐhuan zuò zài wēnnuǎn de jiā lǐ huàhuà, xiǎngshòu xiūxirì.", "en":"On Sunday, I like sitting in my warm home drawing pictures, enjoying the day of rest.", "jp":"日曜日、私は温かい家で絵を描いて過ごし、休息日を楽しみます。"},
            {"id":"st8", "zh":"充实又快乐的一星期，每一天都有满满的收获！", "py":"Chōngshí yòu kuàilè de yì xīngqī, měi yì tiān dōu yǒu mǎnmǎn de shōuhuò!", "en":"A fulfilling and happy week, every single day brings abundant gains!", "jp":"充実して楽しい一週間、毎日たくさんの収穫があります！"}
        ],
        "characters": [
            {"id":"zi1", "zh":"天", "py":"tiān", "radical":"一部（一字头）", "radicalBadge":"一 —— 天", "words":"天气、今天、明天", "meaning":"sky / day", "meaningJp":"そら / ひ", "context":"充实的一星期，每一天都有收获"},
            {"id":"zi2", "zh":"学", "py":"xué", "radical":"子部（子字底）", "radicalBadge":"子 —— 学", "words":"学习、学校、学生", "meaning":"study / learn", "meaningJp":"まなぶ", "context":"我们在明亮的教室里学习中文"},
            {"id":"zi3", "zh":"校", "py":"xiào", "radical":"木部（木字旁）", "radicalBadge":"木 —— 校", "words":"学校、校园、校长", "meaning":"school", "meaningJp":"がっこう", "context":"背上书包高高兴兴去学校"},
            {"id":"zi4", "zh":"同", "py":"tóng", "radical":"口部（同字框）", "radicalBadge":"口 —— 同", "words":"同学、同伴、共同", "meaning":"same / together", "meaningJp":"おなじ", "context":"下课后我和同学们一起玩耍"},
            {"id":"zi5", "zh":"友", "py":"yǒu", "radical":"又部（又字底）", "radicalBadge":"又 —— 友", "words":"朋友、友好、好友", "meaning":"friend", "meaningJp":"ともだち", "context":"我和好朋友一起听音乐"},
            {"id":"zi6", "zh":"看", "py":"kàn", "radical":"目部（目字底）", "radicalBadge":"目 —— 看", "words":"看书、看见、看望", "meaning":"look / see / read", "meaningJp":"みる / よむ", "context":"走进安静的图书馆看书"},
            {"id":"zi7", "zh":"书", "py":"shū", "radical":"乛部（横折钩）", "radicalBadge":None, "words":"书本、书包、读书", "meaning":"book", "meaningJp":"ほん", "context":"我们背上书包去学校"},
            {"id":"zi8", "zh":"听", "py":"tīng", "radical":"口部（口字旁）", "radicalBadge":"口 —— 听", "words":"听话、听见、收听", "meaning":"listen / hear", "meaningJp":"きく", "context":"认真听讲，听优美的音乐"},
            {"id":"zi9", "zh":"音", "py":"yīn", "radical":"音部（自体即部首）", "radicalBadge":None, "words":"音乐、声音、拼音", "meaning":"sound / music", "meaningJp":"おと", "context":"在操场上听优美的音乐"},
            {"id":"zi10", "zh":"乐", "py":"yuè / lè", "radical":"丿部（撇字头）", "radicalBadge":None, "words":"音乐、快乐、乐趣", "meaning":"music / joy", "meaningJp":"おんがく / たのしい", "context":"充实又快乐的一星期"},
            {"id":"zi11", "zh":"爱", "py":"ài", "radical":"爫部（爪字头）", "radicalBadge":"爫 —— 爱", "words":"爱心、可爱、喜爱", "meaning":"love / like", "meaningJp":"あいする", "context":"我爱我的学校和温暖的家"},
            {"id":"zi12", "zh":"家", "py":"jiā", "radical":"宀部（宝盖头）", "radicalBadge":"宀 —— 家", "words":"大家、家庭、家门", "meaning":"home / family", "meaningJp":"いえ", "context":"我喜欢坐在温暖的家里画画"}
        ],
        "words": [
            {"id":"ci1", "zh":"学校", "py":"xuéxiào", "meaning":"school", "meaningJp":"学校", "emoji":"🏫", "context":"高高兴兴去学校。", "tag":"场所"},
            {"id":"ci2", "zh":"同学", "py":"tóngxué", "meaning":"classmate", "meaningJp":"クラスメイト", "emoji":"👧", "context":"我和同学们在操场上听音乐。", "tag":"人物"},
            {"id":"ci3", "zh":"看书", "py":"kànshū", "meaning":"read books", "meaningJp":"本を読む", "emoji":"📖", "context":"我们在图书馆里津津有味地看书。", "tag":"动作"},
            {"id":"ci4", "zh":"音乐", "py":"yīnyuè", "meaning":"music", "meaningJp":"音楽", "emoji":"🎵", "context":"听优美的音乐。", "tag":"艺术"},
            {"id":"ci5", "zh":"公园", "py":"gōngyuán", "meaning":"park", "meaningJp":"公園", "emoji":"🌳", "context":"我和爸爸妈妈去公园散步。", "tag":"场所"},
            {"id":"ci6", "zh":"家里", "py":"jiālǐ", "meaning":"at home", "meaningJp":"家で", "emoji":"🏠", "context":"我喜欢坐在温暖的家里画画。", "tag":"场所"},
            {"id":"ci7", "zh":"快乐", "py":"kuàilè", "meaning":"happy / joyful", "meaningJp":"楽しい", "emoji":"😄", "context":"充实又快乐的一星期。", "tag":"情感"},
            {"id":"ci8", "zh":"星期", "py":"xīngqī", "meaning":"week", "meaningJp":"週 / 曜日", "emoji":"📅", "context":"每一天都是新的一天。", "tag":"时间"},
            {"id":"ci9", "zh":"书包", "py":"shūbāo", "meaning":"schoolbag", "meaningJp":"ランドセル / 鞄", "emoji":"🎒", "context":"我们背上书包去学校。", "tag":"物品"},
            {"id":"ci10", "zh":"教室", "py":"jiàoshì", "meaning":"classroom", "meaningJp":"教室", "emoji":"🚪", "context":"我们在明亮的教室里认真学习中文。", "tag":"场所"},
            {"id":"ci11", "zh":"喜欢", "py":"xǐhuan", "meaning":"like / enjoy", "meaningJp":"好き", "emoji":"❤️", "context":"我喜欢在家里画画享受休息日。", "tag":"情感"},
            {"id":"ci12", "zh":"周末", "py":"zhōumò", "meaning":"weekend", "meaningJp":"週末", "emoji":"🏖️", "context":"开开心心迎接周末。", "tag":"时间"}
        ],
        "proper_nouns": [
            {"id":"pn1", "zh":"星期一", "py":"xīngqīyī", "meaning":"Monday", "meaningJp":"月曜日", "emoji":"1️⃣", "context":"星期一去学校。", "tag":"星期"},
            {"id":"pn2", "zh":"星期二", "py":"xīngqī'èr", "meaning":"Tuesday", "meaningJp":"火曜日", "emoji":"2️⃣", "context":"星期二学中文。", "tag":"星期"},
            {"id":"pn3", "zh":"星期三", "py":"xīngqīsān", "meaning":"Wednesday", "meaningJp":"水曜日", "emoji":"3️⃣", "context":"星期三听音乐。", "tag":"星期"},
            {"id":"pn4", "zh":"星期四", "py":"xīngqīsì", "meaning":"Thursday", "meaningJp":"木曜日", "emoji":"4️⃣", "context":"星期四看书。", "tag":"星期"},
            {"id":"pn5", "zh":"星期五", "py":"xīngqīwǔ", "meaning":"Friday", "meaningJp":"金曜日", "emoji":"5️⃣", "context":"星期五唱歌跳舞。", "tag":"星期"},
            {"id":"pn6", "zh":"星期六", "py":"xīngqīliù", "meaning":"Saturday", "meaningJp":"土曜日", "emoji":"6️⃣", "context":"星期六去公园。", "tag":"星期"},
            {"id":"pn7", "zh":"星期天", "py":"xīngqītiān", "meaning":"Sunday", "meaningJp":"日曜日", "emoji":"7️⃣", "context":"星期天在家画画。", "tag":"星期"}
        ],
        "scramble_sentences": [
            {
                "id": "sent1",
                "zh": "我们背上书包高高兴兴去学校。",
                "tokens": ["我们背上", "书包", "高高兴兴", "去学校。"],
                "isKey": True
            },
            {
                "id": "st2",
                "zh": "我们在明亮的教室里认真听讲、学习中文。",
                "tokens": ["我们在明亮的", "教室里", "认真听讲、", "学习中文。"]
            },
            {
                "id": "st4",
                "zh": "我们走进安静的图书馆，津津有味地看书。",
                "tokens": ["我们走进", "安静的图书馆，", "津津有味地", "看书。"]
            },
            {
                "id": "st6",
                "zh": "我和爸爸妈妈去公园散步，看盛开的鲜花。",
                "tokens": ["我和爸爸妈妈", "去公园散步，", "看盛开的", "鲜花。"]
            },
            {
                "id": "st7",
                "zh": "我喜欢坐在温暖的家里画画，享受休息日。",
                "tokens": ["我喜欢坐在", "温暖的家里画画，", "享受", "休息日。"]
            }
        ],
        "quiz": [
            {"q":"星期一早上，我们带什么去学校？", "opts":["画笔", "书包", "雨伞", "足球"], "a":1},
            {"q":"星期二，我们在教室里认真学习什么？", "opts":["画画", "游泳", "中文", "做饭"], "a":2},
            {"q":"星期四，大家在哪里津津有味地看书？", "opts":["公园", "操场", "图书馆", "食堂"], "a":2},
            {"q":"汉字“学”的下半部分部首是什么？", "opts":["子部", "木部", "口部", "日部"], "a":0},
            {"q":"汉字“校”的部首“木字旁”通常与什么有关？", "opts":["金属", "水流", "树木木材", "火焰"], "a":2},
            {"q":"星期六，主人公和谁一起去公园散步？", "opts":["老师", "爸爸妈妈", "独自一人", "邻居"], "a":1},
            {"q":"星期天，主人公最喜欢在家里做什么？", "opts":["跑步", "画画", "跳舞", "弹琴"], "a":1},
            {"q":"多音字“乐”在“音乐”中读作什么？", "opts":["lè", "yuè", "luò", "yào"], "a":1}
        ],
        "cloze": [
            {
                "id": "zh_c1",
                "type": "text",
                "before": "星期一，朝阳升起，我们背上书包高高兴兴去",
                "answer": "学校",
                "after": "。",
                "py": "Xīngqīyī, zhāoyáng shēngqǐ, wǒmen bēishang shūbāo gāogāoxìngxìng qù xuéxiào.",
                "en": "On Monday, morning sun rises, we carry our schoolbags happily to school.",
                "jp": "月曜日、私たちはランドセルを背負って元気に登校します。",
                "answerPy": "xué xiào",
                "options": ["学校", "公园", "家里", "超市"],
                "hint": "课文原句 · 星期一上学目的地",
                "audioId": "cloze_1"
            },
            {
                "id": "zh_c2",
                "type": "text",
                "before": "我们在明亮的教室里认真听讲、学习",
                "answer": "中文",
                "after": "。",
                "py": "Wǒmen zài míngliàng de jiàoshì lǐ rènzhēn tīngjiǎng, xuéxí zhōngwén.",
                "en": "We listen attentively and study Chinese in the bright classroom.",
                "jp": "教室で真剣に中国語を学びます。",
                "answerPy": "zhōng wén",
                "options": ["中文", "数学", "科学", "历史"],
                "hint": "课文原句 · 学习的科目",
                "audioId": "cloze_2"
            },
            {
                "id": "zh_c3",
                "type": "text",
                "before": "下课后我和同学们在操场上听优美的",
                "answer": "音乐",
                "after": "。",
                "py": "Xiàkè hòu wǒ hé tóngxuémen zài cāochǎng shang tīng yōuměi de yīnyuè.",
                "en": "After class my classmates and I listen to beautiful music.",
                "jp": "放課後にグラウンドで美しい音楽を聴きます。",
                "answerPy": "yīn yuè",
                "options": ["音乐", "故事", "掌声", "风声"],
                "hint": "课文原句 · 操场上的美好旋律",
                "audioId": "cloze_3"
            },
            {
                "id": "zh_c4",
                "type": "text",
                "before": "我们走进安静的图书馆，津津有味地",
                "answer": "看书",
                "after": "。",
                "py": "Wǒmen zǒujìn ānjìng de túshūguǎn, jīnjīnyǒuwèi de kàn shū.",
                "en": "We walk into the quiet library and read books.",
                "jp": "静かな図書館に入り、夢中になって本を読みます。",
                "answerPy": "kàn shū",
                "options": ["看书", "唱歌", "睡觉", "跑步"],
                "hint": "课文原句 · 图书馆里的活动",
                "audioId": "cloze_4"
            },
            {
                "id": "zh_c5",
                "type": "text",
                "before": "星期五，大家一起唱歌跳舞，开开心心迎接",
                "answer": "周末",
                "after": "。",
                "py": "Xīngqīwǔ, dàjiā yìqǐ chàng gē tiào wǔ, kāikāixīnxīn yíngjiē zhōumò.",
                "en": "On Friday, everyone sings and dances together, welcoming the weekend.",
                "jp": "みんなで歌って踊り、楽しく週末を迎えます。",
                "answerPy": "zhōu mò",
                "options": ["周末", "星期一", "假期", "考试"],
                "hint": "课文原句 · 迎接周六和周日",
                "audioId": "cloze_5"
            },
            {
                "id": "zh_c6",
                "type": "text",
                "before": "我和爸爸妈妈去",
                "answer": "公园",
                "after": "散步，看盛开的鲜花。",
                "py": "Wǒ hé bàba māma qù gōngyuán sànbù, kàn shèngkāi de xiānhuā.",
                "en": "My parents and I go strolling in the park.",
                "jp": "両親と公園へ散歩に行きます。",
                "answerPy": "gōng yuán",
                "options": ["公园", "学校", "教室", "医院"],
                "hint": "课文原句 · 散步的好去处",
                "audioId": "cloze_6"
            },
            {
                "id": "zh_c7",
                "type": "text",
                "before": "我喜欢坐在温暖的",
                "answer": "家里",
                "after": "画画，享受休息日。",
                "py": "Wǒ xǐhuan zuò zài wēnnuǎn de jiā lǐ huàhuà, xiǎngshòu xiūxirì.",
                "en": "I like sitting in my warm home drawing pictures.",
                "jp": "温かい家で絵を描いて過ごします。",
                "answerPy": "jiā lǐ",
                "options": ["家里", "操场", "车站", "教室"],
                "hint": "课文原句 · 舒适温馨的所在",
                "audioId": "cloze_7"
            },
            {
                "id": "zh_c8",
                "type": "text",
                "before": "充实又",
                "answer": "快乐",
                "after": "的一星期，每一天都有满满的收获！",
                "py": "Chōngshí yòu kuàilè de yì xīngqī, měi yì tiān dōu yǒu mǎnmǎn de shōuhuò!",
                "en": "A fulfilling and happy week, every single day brings abundant gains!",
                "jp": "充実して楽しい一週間、毎日収穫があります！",
                "answerPy": "kuài lè",
                "options": ["快乐", "难过", "疲倦", "漫长"],
                "hint": "课文原句 · 描写美好的心情",
                "audioId": "cloze_8"
            }
        ]
    },
    {
        "id": "zh2",
        "lesson_num": "2",
        "title": "我的一天 - 汉语课文识字闯关 (My Day)",
        "canonical": "https://zw.0101.click/zh2.html",
        "header_title": "我的一天",
        "title_en": "My Day in Chinese",
        "sub_desc": "跟随原创情境课文《我的一天》体验一日作息生活，掌握时刻钟点、三餐起居、日常动作与12个核心汉字！本课是《我的一星期》的续篇（第2课）。",
        "story_title": "📖 我的一天 (My Day)",
        "full_title": "📜 我的一天 · 全文",
        "palace_svg": """<svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="26" fill="#fff" stroke="#b91c1c" stroke-width="4"/>
          <circle cx="32" cy="32" r="2.6" fill="#b91c1c"/>
          <line x1="32" y1="32" x2="32" y2="15" stroke="#b91c1c" stroke-width="3.4" stroke-linecap="round"/>
          <line x1="32" y1="32" x2="44" y2="39" stroke="#b91c1c" stroke-width="3.4" stroke-linecap="round"/>
        </svg>""",
        "proper_label": "时间",
        "has_pinyin_chart": False,
        "story": [
            {"id":"st1", "zh":"早上七点，闹钟叮咚响了，我准时起床。", "py":"Zǎoshang qī diǎn, nàozhōng dīngdōng xiǎng le, wǒ zhǔnshí qǐchuáng.", "en":"At 7 o'clock in the morning, the alarm rings, I get up on time.", "jp":"朝7時、目覚まし時計が鳴り、時間通りに起きます。"},
            {"id":"st2", "zh":"洗脸刷牙后，我和家人一起吃香喷喷的早餐。", "py":"Xǐliǎn shuāyá hòu, wǒ hé jiārén yìqǐ chī xiāngpēnpēn de zǎocān.", "en":"After washing face and brushing teeth, I eat delicious breakfast with family.", "jp":"洗顔と歯磨きをして、家族と一緒に美味しい朝ごはんを食べます。"},
            {"id":"st3", "zh":"早上八点，我背着书包走出家门，向着学校走去。", "py":"Zǎoshang bā diǎn, wǒ bēizhe shūbāo zǒuchū jiāmén, xiàngzhe xuéxiào zǒuqù.", "en":"At 8 o'clock, carrying my schoolbag, I step out the door and walk to school.", "jp":"朝8時、カバンを背負って家を出て、学校に向かって歩きます。"},
            {"id":"st4", "zh":"中午十二点，我们在食堂吃午饭，排骨和米饭真香！", "py":"Zhōngwǔ shí'èr diǎn, wǒmen zài shítáng chī wǔfàn, páigǔ hé mǐfàn zhēn xiāng!", "en":"At 12 o'clock noon, we eat lunch in the cafeteria; ribs and rice are delicious!", "jp":"お昼12時、食堂で昼ごはんを食べます。おかずとご飯がとても美味しいです！"},
            {"id":"st5", "zh":"下午四点，放学铃声响起，我们收拾好书本准备回家。", "py":"Xiàwǔ sì diǎn, fàngxué língshēng xiǎngqǐ, wǒmen shōushi hǎo shūběn zhǔnbèi huíjiā.", "en":"At 4 o'clock in the afternoon, the bell rings, we pack our books ready to go home.", "jp":"午後4時、下校のチャイムが鳴り、本を片付けて帰宅の準備をします。"},
            {"id":"st6", "zh":"傍晚六点半，全家人围坐在餐桌旁吃丰盛的晚饭。", "py":"Bàngwǎn liù diǎn bàn, quán jiārén wéizuò zài cānzhuō páng chī fēngshèng de wǎnfàn.", "en":"At 6:30 in the evening, the whole family sits around the table eating a hearty dinner.", "jp":"夕方6時半、家族全員で食卓を囲み、豪華な晩ごはんを食べます。"},
            {"id":"st7", "zh":"晚上八点，我在书桌前专心致志地写作业。", "py":"Wǎnshang bā diǎn, wǒ zài shūzhuō qián zhuānxīnzhìzhì de xiě zuòyè.", "en":"At 8 o'clock in the evening, I focus intently on my homework at the desk.", "jp":"夜8時、机に向かって集中して宿題をします。"},
            {"id":"st8", "zh":"晚上九点半，我对爸爸妈妈道声晚安，安心睡觉。", "py":"Wǎnshang jiǔ diǎn bàn, wǒ duì bàba māma dào shēng wǎn'ān, ānxīn shuìjiào.", "en":"At 9:30, I say good night to Mom and Dad, and fall asleep peacefully.", "jp":"夜9時半、両親に「おやすみなさい」と言って、安心して眠りにつきます。"}
        ],
        "characters": [
            {"id":"zi1", "zh":"早", "py":"zǎo", "radical":"日部（日字头）", "radicalBadge":"日 —— 早", "words":"早上、早饭、太早", "meaning":"early / morning", "meaningJp":"あさ / はやい", "context":"早上七点，闹钟响了"},
            {"id":"zi2", "zh":"午", "py":"wǔ", "radical":"十部（十字底）", "radicalBadge":None, "words":"中午、上午、下午", "meaning":"noon", "meaningJp":"ひる / ごご", "context":"中午十二点，我们在食堂吃午饭"},
            {"id":"zi3", "zh":"晚", "py":"wǎn", "radical":"日部（日字旁）", "radicalBadge":"日 —— 晚", "words":"晚上、晚饭、晚安", "meaning":"evening / late", "meaningJp":"よる / ばん", "context":"晚上八点，认真写作业"},
            {"id":"zi4", "zh":"点", "py":"diǎn", "radical":"灬部（四点底）", "radicalBadge":"灬 —— 点", "words":"点心、几点、钟点", "meaning":"o'clock / dot", "meaningJp":"じ / てん", "context":"早上七点起床，中午十二点吃午饭"},
            {"id":"zi5", "zh":"分", "py":"fēn", "radical":"刀部（八字头/刀字底）", "radicalBadge":"刀 —— 分", "words":"分钟、分别、十分", "meaning":"minute / divide", "meaningJp":"ふん / わける", "context":"时间钟点：分与秒"},
            {"id":"zi6", "zh":"起", "py":"qǐ", "radical":"走部（走字底）", "radicalBadge":"走 —— 起", "words":"起床、起来、起立", "meaning":"get up / rise", "meaningJp":"おきる", "context":"闹钟响了，我准时起床"},
            {"id":"zi7", "zh":"床", "py":"chuáng", "radical":"广部（广字旁）", "radicalBadge":"广 —— 床", "words":"木床、起床、床头", "meaning":"bed", "meaningJp":"ベッド / ゆか", "context":"准时从床上起床"},
            {"id":"zi8", "zh":"吃", "py":"chī", "radical":"口部（口字旁）", "radicalBadge":"口 —— 吃", "words":"吃饭、好吃、吃饱", "meaning":"eat", "meaningJp":"たべる", "context":"吃香喷喷的早餐和午饭"},
            {"id":"zi9", "zh":"饭", "py":"fàn", "radical":"饣部（饣字旁）", "radicalBadge":"饣 —— 饭", "words":"白饭、米饭、饭菜", "meaning":"meal / cooked rice", "meaningJp":"ごはん", "context":"全家人围坐在一起吃晚饭"},
            {"id":"zi10", "zh":"睡", "py":"shuì", "radical":"目部（目字旁）", "radicalBadge":"目 —— 睡", "words":"睡觉、午睡、熟睡", "meaning":"sleep", "meaningJp":"ねむる", "context":"安心闭上眼睛睡觉"},
            {"id":"zi11", "zh":"觉", "py":"jiào / jué", "radical":"见部（见字底）", "radicalBadge":"见 —— 觉", "words":"睡觉、感觉、午觉", "meaning":"sleep / feel", "meaningJp":"ねむり / かんじる", "context":"好好睡觉，迎接明天"},
            {"id":"zi12", "zh":"走", "py":"zǒu", "radical":"走部（自体即部首）", "radicalBadge":None, "words":"走路、走开、行走", "meaning":"walk / leave", "meaningJp":"あるく", "context":"走出家门，向着学校走去"}
        ],
        "words": [
            {"id":"ci1", "zh":"起床", "py":"qǐchuáng", "meaning":"get out of bed", "meaningJp":"起きる", "emoji":"⏰", "context":"我准时起床。", "tag":"作息"},
            {"id":"ci2", "zh":"早餐", "py":"zǎocān", "meaning":"breakfast", "meaningJp":"朝食", "emoji":"🥪", "context":"我和家人一起吃香喷喷的早餐。", "tag":"饮食"},
            {"id":"ci3", "zh":"午饭", "py":"wǔfàn", "meaning":"lunch", "meaningJp":"昼食", "emoji":"🍱", "context":"我们在食堂吃午饭。", "tag":"饮食"},
            {"id":"ci4", "zh":"晚饭", "py":"wǎnfàn", "meaning":"dinner", "meaningJp":"晩ご飯", "emoji":"🍲", "context":"全家人围坐在餐桌旁吃晚饭。", "tag":"饮食"},
            {"id":"ci5", "zh":"睡觉", "py":"shuìjiào", "meaning":"go to sleep", "meaningJp":"眠る", "emoji":"🛏️", "context":"安心进入梦乡睡觉。", "tag":"作息"},
            {"id":"ci6", "zh":"时间", "py":"shíjiān", "meaning":"time", "meaningJp":"時間", "emoji":"⏱️", "context":"珍惜时间，作息规律。", "tag":"时间"},
            {"id":"ci7", "zh":"作业", "py":"zuòyè", "meaning":"homework", "meaningJp":"宿題", "emoji":"📝", "context":"我在书桌前专心写作业。", "tag":"学习"},
            {"id":"ci8", "zh":"回家", "py":"huíjiā", "meaning":"return home", "meaningJp":"家に帰る", "emoji":"🚶", "context":"收拾好书本准备回家。", "tag":"动作"},
            {"id":"ci9", "zh":"洗脸", "py":"xǐliǎn", "meaning":"wash face", "meaningJp":"顔を洗う", "emoji":"🧼", "context":"洗脸刷牙后吃早饭。", "tag":"生活"},
            {"id":"ci10", "zh":"准备", "py":"zhǔnbèi", "meaning":"prepare / ready", "meaningJp":"準備する", "emoji":"🎒", "context":"收拾好书本准备回家。", "tag":"动作"},
            {"id":"ci11", "zh":"晚安", "py":"wǎn'ān", "meaning":"good night", "meaningJp":"おやすみなさい", "emoji":"🌙", "context":"对爸爸妈妈道声晚安。", "tag":"礼貌"},
            {"id":"ci12", "zh":"整点", "py":"zhěngdiǎn", "meaning":"on the hour", "meaningJp":"正時", "emoji":"🕛", "context":"早上八点整出发。", "tag":"时间"}
        ],
        "proper_nouns": [
            {"id":"pn1", "zh":"早上好", "py":"zǎoshang hǎo", "meaning":"good morning", "meaningJp":"おはよう", "emoji":"🌅", "context":"早上七点向家人问好。", "tag":"日常"},
            {"id":"pn2", "zh":"中午好", "py":"zhōngwǔ hǎo", "meaning":"good afternoon", "meaningJp":"こんにちは", "emoji":"☀️", "context":"中午十二点问候同学。", "tag":"日常"},
            {"id":"pn3", "zh":"下午好", "py":"xiàwǔ hǎo", "meaning":"good afternoon", "meaningJp":"こんにちは", "emoji":"🌤️", "context":"下午四点放学问候老师。", "tag":"日常"},
            {"id":"pn4", "zh":"晚上好", "py":"wǎnshang hǎo", "meaning":"good evening", "meaningJp":"こんばんは", "emoji":"🌆", "context":"傍晚六点吃晚餐。", "tag":"日常"},
            {"id":"pn5", "zh":"几点了", "py":"jǐ diǎn le", "meaning":"what time is it", "meaningJp":"いま何時ですか", "emoji":"⌚", "context":"看手表确认几点了。", "tag":"常用"},
            {"id":"pn6", "zh":"吃饭了", "py":"chī fàn le", "meaning":"meal is ready", "meaningJp":"ごはんですよ", "emoji":"🍚", "context":"妈妈叫我们吃饭了！", "tag":"日常"},
            {"id":"pn7", "zh":"晚安", "py":"wǎn'ān", "meaning":"good night", "meaningJp":"おやすみなさい", "emoji":"💤", "context":"安心睡觉说晚安。", "tag":"日常"}
        ],
        "scramble_sentences": [
            {
                "id": "sent1",
                "zh": "早上七点，闹钟叮咚响了，我准时起床。",
                "tokens": ["早上七点，", "闹钟叮咚响了，", "我准时", "起床。"],
                "isKey": True
            },
            {
                "id": "st2",
                "zh": "洗脸刷牙后，我和家人一起吃香喷喷的早餐。",
                "tokens": ["洗脸刷牙后，", "我和家人一起", "吃香喷喷的", "早餐。"]
            },
            {
                "id": "st4",
                "zh": "中午十二点，我们在食堂吃午饭，排骨和米饭真香！",
                "tokens": ["中午十二点，", "我们在食堂吃午饭，", "排骨和米饭", "真香！"]
            },
            {
                "id": "st6",
                "zh": "傍晚六点半，全家人围坐在餐桌旁吃丰盛的晚饭。",
                "tokens": ["傍晚六点半，", "全家人围坐在", "餐桌旁吃", "丰盛的晚饭。"]
            },
            {
                "id": "st8",
                "zh": "晚上九点半，我对爸爸妈妈道声晚安，安心睡觉。",
                "tokens": ["晚上九点半，", "我对爸爸妈妈", "道声晚安，", "安心睡觉。"]
            }
        ],
        "quiz": [
            {"q":"早上闹钟响后，主人公在几点准时起床？", "opts":["六点", "七点", "八点", "九点"], "a":1},
            {"q":"吃早餐之前，必须做哪两件事养成良好卫生习惯？", "opts":["看电视和玩游戏", "洗脸和刷牙", "画画和跳绳", "打扫操场"], "a":1},
            {"q":"中午十二点，大家在哪里吃午饭？", "opts":["操场", "教室", "食堂", "公园"], "a":2},
            {"q":"汉字“点”下方的部首“灬”（四点底）在古代通常代表什么？", "opts":["雨水", "火焰", "土壤", "竹子"], "a":1},
            {"q":"下午放学铃声响起的时间通常是几点？", "opts":["两点", "三点", "四点", "七点"], "a":2},
            {"q":"晚上八点，主人公在书桌前专心做什么？", "opts":["吃零食", "写作业", "睡觉", "洗澡"], "a":1},
            {"q":"汉字“睡”的部首是“目字旁”，说明它与人体的什么器官相关？", "opts":["耳朵", "眼睛", "鼻子", "嘴巴"], "a":1},
            {"q":"睡觉前向爸爸妈妈道别时，通常会说什么？", "opts":["早上好", "晚安", "再见", "加油"], "a":1}
        ],
        "cloze": [
            {
                "id": "zh_c1",
                "type": "text",
                "before": "早上七点，闹钟叮咚响了，我准时",
                "answer": "起床",
                "after": "。",
                "py": "Zǎoshang qī diǎn, nàozhōng dīngdōng xiǎng le, wǒ zhǔnshí qǐchuáng.",
                "en": "At 7 o'clock in the morning, the alarm rings, I get up on time.",
                "jp": "朝7時、目覚まし時計が鳴り、時間通りに起きます。",
                "answerPy": "qǐ chuáng",
                "options": ["起床", "睡觉", "洗澡", "看书"],
                "hint": "课文原句 · 早晨离开床铺",
                "audioId": "cloze_1"
            },
            {
                "id": "zh_c2",
                "type": "text",
                "before": "洗脸刷牙后，我和家人一起吃香喷喷的",
                "answer": "早餐",
                "after": "。",
                "py": "Xǐliǎn shuāyá hòu, wǒ hé jiārén yìqǐ chī xiāngpēnpēn de zǎocān.",
                "en": "After washing face, I eat delicious breakfast with family.",
                "jp": "家族と一緒に美味しい朝ごはんを食べます。",
                "answerPy": "zǎo cān",
                "options": ["早餐", "午饭", "晚饭", "夜宵"],
                "hint": "课文原句 · 早晨的第一餐",
                "audioId": "cloze_2"
            },
            {
                "id": "zh_c3",
                "type": "text",
                "before": "早上八点，我背着书包走出家门，向着",
                "answer": "学校",
                "after": "走去。",
                "py": "Zǎoshang bā diǎn, wǒ bēizhe shūbāo zǒuchū jiāmén, xiàngzhe xuéxiào zǒuqù.",
                "en": "At 8 o'clock, carrying my schoolbag, I step out and walk to school.",
                "jp": "カバンを背負って学校に向かって歩きます。",
                "answerPy": "xué xiào",
                "options": ["学校", "公园", "超市", "操场"],
                "hint": "课文原句 · 早晨前行的方向",
                "audioId": "cloze_3"
            },
            {
                "id": "zh_c4",
                "type": "text",
                "before": "中午十二点，我们在食堂吃",
                "answer": "午饭",
                "after": "，排骨和米饭真香！",
                "py": "Zhōngwǔ shí'èr diǎn, wǒmen zài shítáng chī wǔfàn, páigǔ hé mǐfàn zhēn xiāng!",
                "en": "At 12 noon, we eat lunch in the cafeteria.",
                "jp": "お昼12時、食堂で昼ごはんを食べます。",
                "answerPy": "wǔ fàn",
                "options": ["午饭", "早餐", "苹果", "点心"],
                "hint": "课文原句 · 中午的饭菜",
                "audioId": "cloze_4"
            },
            {
                "id": "zh_c5",
                "type": "text",
                "before": "下午四点，放学铃声响起，我们收拾好书本准备",
                "answer": "回家",
                "after": "。",
                "py": "Xiàwǔ sì diǎn, fàngxué língshēng xiǎngqǐ, wǒmen shōushi hǎo shūběn zhǔnbèi huíjiā.",
                "en": "At 4 o'clock, the bell rings, we pack books ready to go home.",
                "jp": "本を片付けて帰宅の準備をします。",
                "answerPy": "huí jiā",
                "options": ["回家", "上课", "跑步", "睡觉"],
                "hint": "课文原句 · 放学后的行程",
                "audioId": "cloze_5"
            },
            {
                "id": "zh_c6",
                "type": "text",
                "before": "傍晚六点半，全家人围坐在餐桌旁吃丰盛的",
                "answer": "晚饭",
                "after": "。",
                "py": "Bàngwǎn liù diǎn bàn, quán jiārén wéizuò zài cānzhuō páng chī fēngshèng de wǎnfàn.",
                "en": "At 6:30, the whole family sits around eating dinner.",
                "jp": "家族全員で食卓を囲み、晩ごはんを食べます。",
                "answerPy": "wǎn fàn",
                "options": ["晚饭", "午饭", "早餐", "零食"],
                "hint": "课文原句 · 傍晚全家人的聚餐",
                "audioId": "cloze_6"
            },
            {
                "id": "zh_c7",
                "type": "text",
                "before": "晚上八点，我在书桌前专心致志地写",
                "answer": "作业",
                "after": "。",
                "py": "Wǎnshang bā diǎn, wǒ zài shūzhuō qián zhuānxīnzhìzhì de xiě zuòyè.",
                "en": "At 8 o'clock, I focus on my homework at the desk.",
                "jp": "机に向かって集中して宿題をします。",
                "answerPy": "zuò yè",
                "options": ["作业", "信件", "画图", "歌词"],
                "hint": "课文原句 · 课后复习与任务",
                "audioId": "cloze_7"
            },
            {
                "id": "zh_c8",
                "type": "text",
                "before": "晚上九点半，我对爸爸妈妈道声晚安，安心",
                "answer": "睡觉",
                "after": "。",
                "py": "Wǎnshang jiǔ diǎn bàn, wǒ duì bàba māma dào shēng wǎn'ān, ānxīn shuìjiào.",
                "en": "At 9:30, I say good night and fall asleep peacefully.",
                "jp": "安心して眠りにつきます。",
                "answerPy": "shuì jiào",
                "options": ["睡觉", "起床", "看电视", "唱歌"],
                "hint": "课文原句 · 结束充实的一天",
                "audioId": "cloze_8"
            }
        ]
    },
    {
        "id": "zh3",
        "lesson_num": "3",
        "title": "中国的四季 - 汉语课文识字闯关 (Four Seasons)",
        "canonical": "https://zw.0101.click/zh3.html",
        "header_title": "中国的四季",
        "title_en": "Four Seasons in Chinese",
        "sub_desc": "跟随原创自然景致课文《中国的四季》感受春夏秋冬自然之美，学习节气气候、风物诗篇与12个核心汉字！本课是《我的一天》的续篇（第3课）。",
        "story_title": "📖 中国的四季 (Four Seasons)",
        "full_title": "📜 中国的四季 · 全文",
        "palace_svg": """<svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="28" fill="#fff" stroke="#b91c1c" stroke-width="3"/>
          <circle cx="32" cy="20" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="43" cy="28" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="39" cy="42" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="25" cy="42" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="21" cy="28" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="32" cy="32" r="5" fill="#fef08a"/>
        </svg>""",
        "proper_label": "时令",
        "has_pinyin_chart": False,
        "story": [
            {"id":"st1", "zh":"春天来了，微风吹绿了大地，桃花和杏花悄悄盛开。", "py":"Chūntiān lái le, wēifēng chuī lǜ le dàdì, táohuā hé xìnghuā qiāoqiāo shèngkāi.", "en":"Spring has arrived; gentle breeze greens the earth, peach and apricot blossoms quietly bloom.", "jp":"春が来ました。そよ風が大地を緑に染め、桃と杏の花が静かに咲き誇ります。"},
            {"id":"st2", "zh":"春雨滋润着泥土，小朋友们在草地上快乐地放风筝。", "py":"Chūnyǔ zīrùn zhe nítǔ, xiǎopéngyoumen zài cǎodì shang kuàilè de fàng fēngzheng.", "en":"Spring rain nourishes the soil; children happily fly kites on the grassland.", "jp":"春の雨が土を潤し、子どもたちが原っぱで楽しそうに凧揚げをします。"},
            {"id":"st3", "zh":"夏天阳光热烈，茂密的绿树给大地送来一片片阴凉。", "py":"Xiàtiān yángguāng rèliè, màomì de lǜshù gěi dàdì sòng lái yí piànpiàn yīnliáng.", "en":"Summer sun is blazing, dense green trees bring patches of shade to the earth.", "jp":"夏の陽射しは眩しく、青々とした木陰が涼しさをもたらします。"},
            {"id":"st4", "zh":"池塘里粉红的荷花亭亭玉立，我们在树荫下吃冰甜的西瓜。", "py":"Chítáng lǐ fěnhóng de héhuā tíngtíngyùlì, wǒmen zài shùyīn xià chī bīngtián de xīguā.", "en":"In the pond, pink lotuses stand gracefully; we eat chilled sweet watermelon under tree shades.", "jp":"池にはピンクの蓮の花が美しく咲き、木陰で冷たいスイカを食べます。"},
            {"id":"st5", "zh":"秋天到了，凉爽的秋风吹过，金黄的树叶像蝴蝶般飞舞。", "py":"Qiūtiān dào le, liángshuǎng de qiūfēng chuī guò, jīnhuáng de shùyè xiàng húdié bān fēiwǔ.", "en":"Autumn arrives; cool breeze sweeps through, golden leaves dancing like butterflies.", "jp":"秋が訪れ、爽やかな秋風が吹き抜け、黄金色の落ち葉が蝶のように舞います。"},
            {"id":"st6", "zh":"秋天是收获的黄金季节，红彤彤的苹果挂满了枝头。", "py":"Qiūtiān shì shōuhuò de huángjīn jìjié, hóngtōngtōng de píngguǒ guàmǎn le zhītóu.", "en":"Autumn is the golden season of harvest; bright red apples hang heavy on the branches.", "jp":"秋は実りの黄金の季節、真っ赤なリンゴが枝いっぱいに実ります。"},
            {"id":"st7", "zh":"冬天漫天飞雪，洁白的雪花把天地染成了银白色。", "py":"Dōngtiān màntiān fēixuě, jiébái de xuěhuā bǎ tiāndì rǎnchéng le yínbáisè.", "en":"In winter snow fills the sky; pure white snowflakes dye the world in silvery white.", "jp":"冬には雪が舞い散り、真っ白な雪が世界を銀世界へと染め上げます。"},
            {"id":"st8", "zh":"大家一起堆雪人，大年三十挂红灯笼、全家团圆迎新年！", "py":"Dàjiā yìqǐ duī xuěrén, dà nián sānshí guà hóng dēnglong, quánjiā tuányuán yíng xīnnián!", "en":"Everyone makes snowmen together; on New Year's Eve, red lanterns are hung, celebrating family reunion!", "jp":"みんなで雪だるまを作り、大晦日には赤い提灯を掲げて新年を迎えます！"}
        ],
        "characters": [
            {"id":"zi1", "zh":"春", "py":"chūn", "radical":"日部（日字底）", "radicalBadge":"日 —— 春", "words":"春天、春风、立春", "meaning":"spring", "meaningJp":"はる", "context":"春天来了，微风吹绿了大地"},
            {"id":"zi2", "zh":"夏", "py":"xià", "radical":"夂部（折文底）", "radicalBadge":None, "words":"夏天、夏季、初夏", "meaning":"summer", "meaningJp":"なつ", "context":"夏天阳光热烈，茂密的绿树"},
            {"id":"zi3", "zh":"秋", "py":"qiū", "radical":"禾部（禾木旁）", "radicalBadge":"禾 —— 秋", "words":"秋天、秋风、中秋", "meaning":"autumn / fall", "meaningJp":"あき", "context":"秋天到了，凉爽的秋风吹过"},
            {"id":"zi4", "zh":"冬", "py":"dōng", "radical":"夂部（折文头/两点底）", "radicalBadge":None, "words":"冬天、冬季、立冬", "meaning":"winter", "meaningJp":"ふゆ", "context":"冬天漫天飞雪，天地洁白"},
            {"id":"zi5", "zh":"风", "py":"fēng", "radical":"风部（风字框）", "radicalBadge":"风 —— 风", "words":"春风、大风、风雨", "meaning":"wind", "meaningJp":"かぜ", "context":"微风吹绿大地，放风筝"},
            {"id":"zi6", "zh":"雨", "py":"yǔ", "radical":"雨部（自体即部首）", "radicalBadge":None, "words":"春雨、下雨、雨水", "meaning":"rain", "meaningJp":"あめ", "context":"春雨滋润着泥土"},
            {"id":"zi7", "zh":"雪", "py":"xuě", "radical":"雨部（雨字头）", "radicalBadge":"雨 —— 雪", "words":"白雪、雪花、大雪", "meaning":"snow", "meaningJp":"ゆき", "context":"漫天飞雪，洁白的雪花"},
            {"id":"zi8", "zh":"花", "py":"huā", "radical":"艹部（草字头）", "radicalBadge":"艹 —— 花", "words":"鲜花、开花、红花", "meaning":"flower / blossom", "meaningJp":"はな", "context":"桃花和杏花悄悄盛开"},
            {"id":"zi9", "zh":"树", "py":"shù", "radical":"木部（木字旁）", "radicalBadge":"木 —— 树", "words":"大树、树叶、绿树", "meaning":"tree", "meaningJp":"き", "context":"茂密的绿树带来阴凉"},
            {"id":"zi10", "zh":"热", "py":"rè", "radical":"灬部（四点底）", "radicalBadge":"灬 —— 热", "words":"天热、热烈、热水", "meaning":"hot / warm", "meaningJp":"あつい", "context":"夏天的阳光灿烂热烈"},
            {"id":"zi11", "zh":"冷", "py":"lěng", "radical":"冫部（两点水）", "radicalBadge":"冫 —— 冷", "words":"天冷、冷风、寒冷", "meaning":"cold", "meaningJp":"つめたい / さむい", "context":"冬天的风儿好冷啊"},
            {"id":"zi12", "zh":"美", "py":"měi", "radical":"羊部（羊字头/大字底）", "radicalBadge":"羊 —— 美", "words":"美丽、美好、优美", "meaning":"beautiful", "meaningJp":"うつくしい", "context":"四季的风光真美丽"}
        ],
        "words": [
            {"id":"ci1", "zh":"春天", "py":"chūntiān", "meaning":"spring", "meaningJp":"春", "emoji":"🌸", "context":"春天来了，微风吹绿大地。", "tag":"季节"},
            {"id":"ci2", "zh":"夏天", "py":"xiàtiān", "meaning":"summer", "meaningJp":"夏", "emoji":"☀️", "context":"夏天阳光热烈。", "tag":"季节"},
            {"id":"ci3", "zh":"秋天", "py":"qiūtiān", "meaning":"autumn", "meaningJp":"秋", "emoji":"🍁", "context":"秋天到了，凉爽的秋风吹过。", "tag":"季节"},
            {"id":"ci4", "zh":"冬天", "py":"dōngtiān", "meaning":"winter", "meaningJp":"冬", "emoji":"❄️", "context":"冬天漫天飞雪。", "tag":"季节"},
            {"id":"ci5", "zh":"温暖", "py":"wēnnuǎn", "meaning":"warm", "meaningJp":"暖かい", "emoji":"🧣", "context":"春天的大地格外温暖。", "tag":"气候"},
            {"id":"ci6", "zh":"盛开", "py":"shèngkāi", "meaning":"in full bloom", "meaningJp":"咲き誇る", "emoji":"🌺", "context":"桃花和杏花盛开。", "tag":"自然"},
            {"id":"ci7", "zh":"凉爽", "py":"liángshuǎng", "meaning":"cool and refreshing", "meaningJp":"涼しい", "emoji":"🍂", "context":"凉爽的秋风送来惬意。", "tag":"气候"},
            {"id":"ci8", "zh":"收获", "py":"shōuhuò", "meaning":"harvest", "meaningJp":"収穫", "emoji":"🍎", "context":"秋天是收获的黄金季节。", "tag":"风物"},
            {"id":"ci9", "zh":"轻盈", "py":"qīngyíng", "meaning":"light and graceful", "meaningJp":"軽やか", "emoji":"🦋", "context":"树叶像蝴蝶般轻盈飞舞。", "tag":"状态"},
            {"id":"ci10", "zh":"新年", "py":"xīnnián", "meaning":"New Year", "meaningJp":"新年", "emoji":"🧧", "context":"挂红灯笼迎新年。", "tag":"节日"},
            {"id":"ci11", "zh":"阳光", "py":"yángguāng", "meaning":"sunshine", "meaningJp":"陽光", "emoji":"🌞", "context":"夏天阳光热烈灿烂。", "tag":"自然"},
            {"id":"ci12", "zh":"美丽", "py":"měilì", "meaning":"beautiful", "meaningJp":"美しい", "emoji":"✨", "context":"大自然的风景真美丽。", "tag":"美景"}
        ],
        "proper_nouns": [
            {"id":"pn1", "zh":"春天好", "py":"chūntiān hǎo", "meaning":"spring is nice", "meaningJp":"春がいい", "emoji":"🌱", "context":"鸟语花香春天好。", "tag":"四季"},
            {"id":"pn2", "zh":"天气好", "py":"tiānqì hǎo", "meaning":"good weather", "meaningJp":"天気がいい", "emoji":"🌤️", "context":"今天阳光明媚天气好。", "tag":"天气"},
            {"id":"pn3", "zh":"下雨了", "py":"xià yǔ le", "meaning":"it's raining", "meaningJp":"雨が降っている", "emoji":"🌧️", "context":"春雨绵绵下雨了。", "tag":"天气"},
            {"id":"pn4", "zh":"下雪了", "py":"xià xuě le", "meaning":"it's snowing", "meaningJp":"雪が降っている", "emoji":"🌨️", "context":"大地银装素裹下雪了。", "tag":"天气"},
            {"id":"pn5", "zh":"好热啊", "py":"hǎo rè a", "meaning":"so hot", "meaningJp":"とても暑い", "emoji":"🔥", "context":"烈日当空好热啊。", "tag":"感受"},
            {"id":"pn6", "zh":"好冷啊", "py":"hǎo lěng a", "meaning":"so cold", "meaningJp":"とても寒い", "emoji":"🥶", "context":"北风呼啸好冷啊。", "tag":"感受"},
            {"id":"pn7", "zh":"新年好", "py":"xīnnián hǎo", "meaning":"Happy New Year", "meaningJp":"あけましておめでとう", "emoji":"🎊", "context":"大年三十贺新年好！", "tag":"节日"}
        ],
        "scramble_sentences": [
            {
                "id": "sent1",
                "zh": "春天来了，微风吹绿了大地，桃花和杏花悄悄盛开。",
                "tokens": ["春天来了，", "微风吹绿了大地，", "桃花和杏花", "悄悄盛开。"],
                "isKey": True
            },
            {
                "id": "st2",
                "zh": "春雨滋润着泥土，小朋友们在草地上快乐地放风筝。",
                "tokens": ["春雨滋润着泥土，", "小朋友们在草地上", "快乐地", "放风筝。"]
            },
            {
                "id": "st4",
                "zh": "池塘里粉红的荷花亭亭玉立，我们在树荫下吃冰甜的西瓜。",
                "tokens": ["池塘里粉红的荷花", "亭亭玉立，", "我们在树荫下", "吃冰甜的西瓜。"]
            },
            {
                "id": "st6",
                "zh": "秋天是收获的黄金季节，红彤彤的苹果挂满了枝头。",
                "tokens": ["秋天是收获的", "黄金季节，", "红彤彤的苹果", "挂满了枝头。"]
            },
            {
                "id": "st8",
                "zh": "大家一起堆雪人，大年三十挂红灯笼、全家团圆迎新年！",
                "tokens": ["大家一起堆雪人，", "大年三十挂红灯笼、", "全家团圆", "迎新年！"]
            }
        ],
        "quiz": [
            {"q":"春天来到时，哪两种美丽的花朵悄悄盛开了？", "opts":["菊花和梅花", "桃花和杏花", "荷花和睡莲", "桂花和牡丹"], "a":1},
            {"q":"夏天在池塘里亭亭玉立开放的花是什么？", "opts":["荷花", "梅花", "迎春花", "菊花"], "a":0},
            {"q":"秋天是丰收的季节，课文中果园里挂满枝头的红彤彤的水果是什么？", "opts":["西瓜", "苹果", "草莓", "香蕉"], "a":1},
            {"q":"汉字“雪”上方的部首“雨字头”与什么自然现象密切相关？", "opts":["气象与降水", "山川与岩石", "泥土与农田", "草木与森林"], "a":0},
            {"q":"秋天凉爽的秋风吹过，金黄的树叶像什么一样在空中翩翩起舞？", "opts":["小鸟", "蝴蝶", "雪花", "小船"], "a":1},
            {"q":"冬天下大雪的时候，小朋友们最喜欢在雪地里玩什么游戏？", "opts":["游泳", "堆雪人", "放风筝", "摘苹果"], "a":1},
            {"q":"大年三十的除夕夜，家家户户会挂起什么迎新年？", "opts":["红灯笼", "彩带", "气球", "风铃"], "a":0},
            {"q":"汉字“冷”左边的两点水“冫”通常表示什么含义？", "opts":["冰冻与寒冷", "奔腾的江河", "燃烧的烈火", "晴朗的天空"], "a":0}
        ],
        "cloze": [
            {
                "id": "zh_c1",
                "type": "text",
                "before": "微风吹绿了大地，桃花和杏花悄悄",
                "answer": "盛开",
                "after": "。",
                "py": "Wēifēng chuī lǜ le dàdì, táohuā hé xìnghuā qiāoqiāo shèngkāi.",
                "en": "Gentle breeze greens the earth, blossoms bloom quietly.",
                "jp": "桃と杏の花が静かに咲き誇ります。",
                "answerPy": "shèng kāi",
                "options": ["盛开", "落下", "发芽", "生长"],
                "hint": "课文原句 · 花朵绽放的美景",
                "audioId": "cloze_1"
            },
            {
                "id": "zh_c2",
                "type": "text",
                "before": "春雨滋润着泥土，小朋友们在草地上快乐地放",
                "answer": "风筝",
                "after": "。",
                "py": "Chūnyǔ zīrùn zhe nítǔ, xiǎopéngyoumen zài cǎodì shang kuàilè de fàng fēngzheng.",
                "en": "Children happily fly kites on the grassland.",
                "jp": "子どもたちが原っぱで凧揚げをします。",
                "answerPy": "fēng zheng",
                "options": ["风筝", "气球", "小船", "陀螺"],
                "hint": "课文原句 · 春天草地上的传统游戏",
                "audioId": "cloze_2"
            },
            {
                "id": "zh_c3",
                "type": "text",
                "before": "夏天阳光热烈，茂密的绿树给大地送来一片片",
                "answer": "阴凉",
                "after": "。",
                "py": "Xiàtiān yángguāng rèliè, màomì de lǜshù gěi dàdì sòng lái yí piànpiàn yīnliáng.",
                "en": "Summer sun is blazing, green trees bring shade.",
                "jp": "青々とした木陰が涼しさをもたらします。",
                "answerPy": "yīn liáng",
                "options": ["阴凉", "温暖", "积雪", "落叶"],
                "hint": "课文原句 · 绿树带来的凉意",
                "audioId": "cloze_3"
            },
            {
                "id": "zh_c4",
                "type": "text",
                "before": "池塘里粉红的",
                "answer": "荷花",
                "after": "亭亭玉立，我们在树荫下吃冰甜的西瓜。",
                "py": "Chítáng lǐ fěnhóng de héhuā tíngtíngyùlì, wǒmen zài shùyīn xià chī bīngtián de xīguā.",
                "en": "In the pond, pink lotuses stand gracefully.",
                "jp": "池にはピンクの蓮の花が美しく咲きます。",
                "answerPy": "hé huā",
                "options": ["荷花", "桃花", "菊花", "梅花"],
                "hint": "课文原句 · 夏天池塘中的代表名花",
                "audioId": "cloze_4"
            },
            {
                "id": "zh_c5",
                "type": "text",
                "before": "秋天到了，凉爽的秋风吹过，金黄的树叶像",
                "answer": "蝴蝶",
                "after": "般飞舞。",
                "py": "Qiūtiān dào le, liángshuǎng de qiūfēng chuī guò, jīnhuáng de shùyè xiàng húdié bān fēiwǔ.",
                "en": "Cool breeze sweeps through, golden leaves dancing like butterflies.",
                "jp": "黄金色の落ち葉が蝶のように舞います。",
                "answerPy": "hú dié",
                "options": ["蝴蝶", "小鸟", "青蛙", "雪花"],
                "hint": "课文原句 · 树叶飘落的优美比喻",
                "audioId": "cloze_5"
            },
            {
                "id": "zh_c6",
                "type": "text",
                "before": "秋天是收获的黄金季节，红彤彤的",
                "answer": "苹果",
                "after": "挂满了枝头。",
                "py": "Qiūtiān shì shōuhuò de huángjīn jìjié, hóngtōngtōng de píngguǒ guàmǎn le zhītóu.",
                "en": "Autumn is harvest season; apples hang heavy on branches.",
                "jp": "真っ赤なリンゴが枝いっぱいに実ります。",
                "answerPy": "píng guǒ",
                "options": ["苹果", "西瓜", "雪梨", "葡萄"],
                "hint": "课文原句 · 果园里的丰收果实",
                "audioId": "cloze_6"
            },
            {
                "id": "zh_c7",
                "type": "text",
                "before": "冬天漫天飞雪，洁白的",
                "answer": "雪花",
                "after": "把天地染成了银白色。",
                "py": "Dōngtiān màntiān fēixuě, jiébái de xuěhuā bǎ tiāndì rǎnchéng le yínbáisè.",
                "en": "In winter snow fills the sky; white snowflakes dye the world silvery.",
                "jp": "真っ白な雪が世界を銀世界へと染め上げます。",
                "answerPy": "xuě huā",
                "options": ["雪花", "落叶", "鲜花", "露水"],
                "hint": "课文原句 · 冬天的白雪景致",
                "audioId": "cloze_7"
            },
            {
                "id": "zh_c8",
                "type": "text",
                "before": "大年三十挂红灯笼、全家团圆迎",
                "answer": "新年",
                "after": "！",
                "py": "Dà nián sānshí guà hóng dēnglong, quánjiā tuányuán yíng xīnnián!",
                "en": "Red lanterns are hung, celebrating family reunion for New Year!",
                "jp": "赤い提灯を掲げて新年を迎えます！",
                "answerPy": "xīn nián",
                "options": ["新年", "春天", "朋友", "客人"],
                "hint": "课文原句 · 辞旧迎新的传统佳节",
                "audioId": "cloze_8"
            }
        ]
    }
]

# ----------------- PINYIN CHART INJECTION FOR ZH0 -----------------

PINYIN_CHART_HTML = """
    <!-- PINYIN CHART (汉语拼音速查速听盘) -->
    <section class="screen" id="screen-pinyin-chart">
      <h2 class="title">🔤 汉语拼音速查速听盘</h2>
      <p class="sub">点击任意声母、单韵母、复韵母或四声调，即可聆听纯正普通话发音！</p>
      
      <div style="display:flex;gap:8px;justify-content:center;margin-bottom:12px;flex-wrap:wrap;">
        <button class="btn small gold" id="btnPyShengmu" onclick="switchPyMode('shengmu')">声母表 (23个)</button>
        <button class="btn small ghost" id="btnPyYunmu" onclick="switchPyMode('yunmu')">韵母表 (24个)</button>
        <button class="btn small ghost" id="btnPyShengdiao" onclick="switchPyMode('shengdiao')">四声调发音盘</button>
      </div>

      <div class="kana-grid-container" id="pinyinGridContainer" style="width:100%;max-width:540px;background:#fff;border:2px solid #fbd38d;border-radius:var(--radius-lg);padding:14px;box-shadow:var(--shadow-card);">
        <!-- dynamically rendered by renderPinyinGrid() -->
      </div>

      <div style="margin-top:14px;display:flex;gap:12px;">
        <button class="btn ghost small" onclick="goHome()">返回主菜单</button>
        <button class="btn gold small" onclick="goStory()">进入课文朗读 📖</button>
      </div>
    </section>
"""

PINYIN_JS_LOGIC = """
/* ---------------- PINYIN SANDBOX DATA & LOGIC (ZH0 ONLY) ---------------- */
const PY_SHENGMU = [
  {label: "双唇音", items: ["b", "p", "m", "f"]},
  {label: "舌尖中音", items: ["d", "t", "n", "l"]},
  {label: "舌根音", items: ["g", "k", "h"]},
  {label: "舌面音", items: ["j", "q", "x"]},
  {label: "翘舌音", items: ["zh", "ch", "sh", "r"]},
  {label: "平舌音", items: ["z", "c", "s"]},
  {label: "半元音/零声母", items: ["y", "w"]}
];

const PY_YUNMU = [
  {label: "单韵母", items: ["a", "o", "e", "i", "u", "ü"]},
  {label: "复韵母", items: ["ai", "ei", "ui", "ao", "ou", "iu", "ie", "üe", "er"]},
  {label: "前鼻韵母", items: ["an", "en", "in", "un", "ün"]},
  {label: "后鼻韵母", items: ["ang", "eng", "ing", "ong"]}
];

const PY_TONES = [
  {name: "一声 (阴平 高平)", symbol: "— 55", samples: [
    {py: "mā", zh: "妈 (妈妈)"}, {py: "bā", zh: "八 (八个)"}, {py: "tā", zh: "他 (他们)"}, {py: "dōng", zh: "东 (东方)"}
  ]},
  {name: "二声 (阳平 中升)", symbol: "／ 35", samples: [
    {py: "má", zh: "麻 (亚麻)"}, {py: "bá", zh: "拔 (拔草)"}, {py: "rén", zh: "人 (人们)"}, {py: "hóng", zh: "红 (红色)"}
  ]},
  {name: "三声 (上声 降升)", symbol: "∨ 214", samples: [
    {py: "mǎ", zh: "马 (小马)"}, {py: "bǎ", zh: "把 (火把)"}, {py: "nǐ", zh: "你 (你好)"}, {py: "hǎo", zh: "好 (早上好)"}
  ]},
  {name: "四声 (去声 全降)", symbol: "＼ 51", samples: [
    {py: "mà", zh: "骂 (责备)"}, {py: "bà", zh: "爸 (爸爸)"}, {py: "dà", zh: "大 (大家)"}, {py: "xiè", zh: "谢 (谢谢)"}
  ]}
];

let pyCurrentMode = 'shengmu';

function switchPyMode(mode) {
  pyCurrentMode = mode;
  const b1 = document.getElementById('btnPyShengmu');
  const b2 = document.getElementById('btnPyYunmu');
  const b3 = document.getElementById('btnPyShengdiao');
  if(b1) b1.className = mode === 'shengmu' ? 'btn small gold' : 'btn small ghost';
  if(b2) b2.className = mode === 'yunmu' ? 'btn small gold' : 'btn small ghost';
  if(b3) b3.className = mode === 'shengdiao' ? 'btn small gold' : 'btn small ghost';
  renderPinyinGrid();
}

function playPinyinSound(text, title) {
  const clean = text.trim();
  const audioUrl = '/audio/zh/' + encodeURIComponent(clean) + '.mp3';
  const a = new Audio(audioUrl);
  let played = false;
  const p = a.play();
  if (p && typeof p.catch === 'function') {
    p.catch(() => {
      if (!played) { played = true; speak(text, null, 'zh-CN'); }
    });
  }
  a.onerror = () => {
    if (!played) { played = true; speak(text, null, 'zh-CN'); }
  };
  toast('🔊 拼音发音: ' + (title || text));
}

function renderPinyinGrid() {
  const container = document.getElementById('pinyinGridContainer');
  if (!container) return;
  
  if (pyCurrentMode === 'shengdiao') {
    let html = '<div style="display:flex;flex-direction:column;gap:12px;">';
    PY_TONES.forEach(tone => {
      html += `<div style="background:#fffaf0;border:1.5px solid #fbd38d;border-radius:12px;padding:10px 12px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
          <span style="font-weight:800;color:var(--imperial-red);font-size:14px;">${tone.name}</span>
          <span style="font-size:12px;color:var(--imperial-gold);font-weight:700;">${tone.symbol}</span>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(100px, 1fr));gap:8px;">`;
      tone.samples.forEach(s => {
        html += `<div onclick="playPinyinSound('${s.py}', '${s.py} ${s.zh}')" style="background:#fff;border:1px solid #fed7aa;border-radius:8px;padding:8px 6px;text-align:center;cursor:pointer;box-shadow:0 2px 4px rgba(0,0,0,0.05);transition:transform .1s;" onmousedown="this.style.transform='scale(0.96)'" onmouseup="this.style.transform='none'">
          <div style="font-size:18px;font-weight:800;color:var(--blue);">${s.py}</div>
          <div style="font-size:12px;color:var(--muted);">${s.zh}</div>
        </div>`;
      });
      html += `</div></div>`;
    });
    html += '</div>';
    container.innerHTML = html;
    return;
  }

  const list = pyCurrentMode === 'shengmu' ? PY_SHENGMU : PY_YUNMU;
  let html = '<div style="display:flex;flex-direction:column;gap:10px;">';
  list.forEach(group => {
    html += `<div style="background:#fffaf0;border:1.5px solid #fbd38d;border-radius:12px;padding:8px 10px;">
      <div style="font-size:12px;font-weight:700;color:var(--muted);margin-bottom:6px;">${group.label}</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fill, minmax(56px, 1fr));gap:6px;">`;
    group.items.forEach(item => {
      html += `<div onclick="playPinyinSound('${item}', '${item}')" style="background:#fff;border:1px solid #fed7aa;border-radius:8px;padding:10px 4px;text-align:center;cursor:pointer;font-size:18px;font-weight:900;color:var(--imperial-red);box-shadow:0 2px 4px rgba(0,0,0,0.05);transition:transform .1s;" onmousedown="this.style.transform='scale(0.95)'" onmouseup="this.style.transform='none'">
        ${item}
      </div>`;
    });
    html += `</div></div>`;
  });
  html += '</div>';
  container.innerHTML = html;
}

function goPinyinChart() {
  showScreen('screen-pinyin-chart');
  renderPinyinGrid();
}
"""

def generate_lesson_html(lesson):
    """Generate self-contained lesson HTML file from template base."""
    with open(os.path.join(BASE_DIR, 'nihongo0.html'), 'r', encoding='utf-8') as f:
        src = f.read()

    # 1. Update Title and Canonical
    src = re.sub(r'<title>.*?</title>', f'<title>{lesson["title"]}</title>', src)
    src = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="{lesson["canonical"]}">', src)
    src = src.replace('<h1 id="headerTitle">五十音とあいさつ</h1>', f'<h1 id="headerTitle">{lesson["header_title"]}</h1>')

    # Menu section headers & SVGs
    src = re.sub(r'<div class="palace-ico".*?</div>', f'<div class="palace-ico" aria-label="课文图标" onclick="goStory()" style="cursor:pointer;" title="点击开始学习《{lesson["header_title"]}》">\n        {lesson["palace_svg"]}\n      </div>', src, flags=re.DOTALL)
    src = re.sub(r'<h2 class="title"[^>]*>五十音とあいさつ[^<]*</h2>', f'<h2 class="title" onclick="goStory()" style="cursor:pointer;" title="点击开始学习《{lesson["header_title"]}》">{lesson["header_title"]} ({lesson["title_en"]})</h2>', src)
    src = re.sub(r'<p class="sub">跟随由纪初识日语五十音.*?</p>', f'<p class="sub">{lesson["sub_desc"]}</p>', src, flags=re.DOTALL)

    # Readers section headers
    src = src.replace('<h2 class="title">📖 五十音とあいさつ (Hiragana &amp; Greetings)</h2>', f'<h2 class="title">{lesson["story_title"]}</h2>')
    src = src.replace('<h2 class="title">📜 五十音とあいさつ · 全文</h2>', f'<h2 class="title">{lesson["full_title"]}</h2>')

    # Top nav link to go back to zh-index.html
    src = src.replace('href="nhg-index.html"', 'href="zh-index.html"')

    # Chinese localization: replace legacy Japanese UI text
    src = src.replace('带假名朗读 · 点击单句发音', '带拼音朗读 · 点击单句发音')
    src = src.replace('19个假名与常用寒暄词', '19个生词与常用表达')
    src = src.replace('假名配对', '拼音配对')
    src = src.replace('汉字连假名 · 多分类挑战', '汉字连拼音 · 多分类挑战')
    src = src.replace('点击卡片翻面看假名读音和意思，再点喇叭听发音。', '点击卡片翻面看拼音读音和释义，再点喇叭听发音。')
    src = src.replace('<div class="chip active" id="chipPy" onclick="toggleStoryPy()">假名</div>', '<div class="chip active" id="chipPy" onclick="toggleStoryPy()">拼音</div>')
    src = src.replace('<div class="chip active" id="chipFullPy" onclick="toggleFullPy()">假名</div>', '<div class="chip active" id="chipFullPy" onclick="toggleFullPy()">拼音</div>')
    src = src.replace('<div class="chip active" id="chipJp" onclick="toggleStoryJp()">中文</div>', '<div class="chip active" id="chipJp" onclick="toggleStoryJp()">日文</div>')
    src = src.replace('<div class="chip active" id="chipFullJp" onclick="toggleFullJp()">中文</div>', '<div class="chip active" id="chipFullJp" onclick="toggleFullJp()">日文</div>')
    src = src.replace("match:'🧩 假名配对'", "match:'🧩 拼音配对'")
    src = src.replace('<h2 class="title">🧩 假名配对</h2>', '<h2 class="title">🧩 拼音配对</h2>')
    src = src.replace('<h2 class="title">✍️ 课后汉字 (Kanji)</h2>', '<h2 class="title">✍️ 认生字 (Characters)</h2>')
    src = src.replace('田字格标准习字 · 笔顺动态演示与指尖描红临摹（仅收录与简体中文笔顺一致的汉字）。', '田字格标准汉字习字 · 动态笔顺演示与指尖描红临摹。')
    proper_lbl = lesson.get("proper_label", "口语")
    src = src.replace('>时间 (7)</div>', f'>{proper_lbl} (7)</div>')
    src = src.replace('>⏰ 时间 (7)</div>', f'>⏰ {proper_lbl} (7)</div>')

    # Menu banner replacement
    if lesson["has_pinyin_chart"]:
        pinyin_banner = """<div style="background:linear-gradient(135deg,#fee2e2,#fef3c7);border:2px solid #f87171;border-radius:var(--radius-lg);padding:14px 16px;margin:10px 0 16px;text-align:center;box-shadow:0 4px 14px rgba(220,38,38,0.12);width:100%;max-width:520px;">
        <div style="font-size:16px;font-weight:900;color:#991b1b;">🔤 零基础拼音速听速查盘</div>
        <div style="font-size:12px;color:#78716c;margin:6px 0 10px;line-height:1.5;">23个声母 · 24个单复韵母 · 四声调标准发音 · 点击即听</div>
        <button onclick="goPinyinChart()" style="display:inline-flex;align-items:center;gap:6px;padding:8px 22px;background:#b91c1c;color:#fff;border:none;border-radius:999px;font-size:13px;font-weight:900;cursor:pointer;box-shadow:0 3px 8px rgba(185,28,28,0.25);"><span>🎧</span><span>进入拼音点读盘</span></button>
      </div>"""
        src = re.sub(r'<div style="background:linear-gradient\(135deg,#fee2e2,#fef3c7\);.*?</div>\s*<div class="menu-grid">', pinyin_banner + '\n      <div class="menu-grid">', src, flags=re.DOTALL)
    else:
        series_banner = """<div style="background:linear-gradient(135deg,#fff7ed,#fef3c7);border:2px solid #fbd38d;border-radius:var(--radius-lg);padding:12px 14px;margin:8px 0 14px;text-align:center;box-shadow:0 4px 14px rgba(217,119,6,0.1);width:100%;max-width:520px;">
        <div style="font-size:14px;font-weight:800;color:#c2410c;">📚 全新原创汉语情境课文系列</div>
        <div style="font-size:12px;color:#78716c;margin:4px 0 8px;">100% 原创零版权风险 · 阶梯识字闯关 · 象形字书写笔顺</div>
        <a href="zh-index.html" style="display:inline-flex;align-items:center;gap:6px;padding:6px 18px;background:#c2410c;color:#fff;border-radius:999px;font-size:12px;font-weight:800;text-decoration:none;"><span>📖</span><span>查看全部课程一览</span></a>
      </div>"""
        src = re.sub(r'<div style="background:linear-gradient\(135deg,#fee2e2,#fef3c7\);.*?</div>\s*<div class="menu-grid">', series_banner + '\n      <div class="menu-grid">', src, flags=re.DOTALL)

    # 2. Storage key & voice prefix isolation
    prefix = lesson["id"]
    src = src.replace("'nihongo0_progress'", f"'{prefix}_progress'")
    src = src.replace("'nihongo_progress'", f"'{prefix}_progress'")
    src = src.replace("'nihongo0_srs'", f"'{prefix}_srs'")
    src = src.replace("'nihongo_srs'", f"'{prefix}_srs'")
    src = src.replace("'nihongo0_'", f"'{prefix}_'")
    src = src.replace("'nihongo_'", f"'{prefix}_'")
    src = src.replace("'nihongo_' + s.id", f"'{prefix}_' + s.id")
    src = src.replace("'nihongo_' + sent.id", f"'{prefix}_' + sent.id")
    src = src.replace("'nihongo0_' + s.id", f"'{prefix}_' + s.id")
    src = src.replace("'nihongo0_' + sent.id", f"'{prefix}_' + sent.id")
    src = src.replace('五十音とあいさつ_第', f'{lesson["header_title"]}_第')

    # Audio dirs isolation (use absolute paths to prevent any path resolution issues)
    src = src.replace("const AUDIO_DIR = 'audio/nihongo0/';", f"const AUDIO_DIR = '/audio/{prefix}/';")
    src = src.replace("const AUDIO_DIR_EN = 'audio/nihongo0_en/';", f"const AUDIO_DIR_EN = '/audio/{prefix}_en/';")
    src = src.replace("const AUDIO_DIR_ZH = 'audio/nihongo0_zh/';", f"const AUDIO_DIR_JA = '/audio/{prefix}_ja/';")
    src = src.replace(
        "const dir = lang === 'en-US' ? AUDIO_DIR_EN : (lang === 'zh-CN' ? AUDIO_DIR_ZH : AUDIO_DIR);",
        "const dir = lang === 'en-US' ? AUDIO_DIR_EN : (lang === 'ja-JP' ? AUDIO_DIR_JA : AUDIO_DIR);"
    )

    # 3. Audio & Voice defaults -> Mandarin Chinese (zh-CN)
    src = src.replace("lang = lang || 'ja-JP';", "lang = lang || 'zh-CN';")
    src = src.replace("playClip(STORY[storyIdx].id, STORY[storyIdx].jp||'', null, 'zh-CN')\" title=\"播放中文发音\"", "playClip(STORY[storyIdx].id, STORY[storyIdx].jp||'', null, 'ja-JP')\" title=\"播放日文发音\"")
    src = src.replace("title=\"播放中文发音\">🔊</button>", "title=\"播放日文发音\">🔊</button>")
    src = src.replace(", null, \\'zh-CN\\');", ", null, \\'ja-JP\\');")

    # 4. Handle Pinyin Chart vs Kana Chart in HTML screens & menus
    if lesson["has_pinyin_chart"]:
        # Replace screen-kana-chart with screen-pinyin-chart
        src = re.sub(
            r'<!-- KANA CHART \(五十音図\) -->\s*<section class="screen" id="screen-kana-chart">.*?</section>',
            PINYIN_CHART_HTML.strip(),
            src,
            flags=re.DOTALL
        )
        src = src.replace('🌸 五十音図', '🔤 汉语拼音盘')
        src = src.replace('五十音図 · 假名速查速听', '拼音速查 · 声母韵母声调')
        src = src.replace('五十音图速查', '拼音点读速查')
        src = src.replace('清音46音 · 平假名/片假名点读发音', '23声母 · 24韵母 · 四声调点读发音')
        src = src.replace('goKanaChart()', 'goPinyinChart()')
    else:
        # Remove kana chart screen cleanly in zh1, zh2, zh3
        src = re.sub(
            r'<!-- KANA CHART \(五十音図\) -->\s*<section class="screen" id="screen-kana-chart">.*?</section>\s*',
            '',
            src,
            flags=re.DOTALL
        )
        # Remove kana chart menu card cleanly without leaving orphaned </div> !
        src = re.sub(
            r'<div class="menu-card full" onclick="goKanaChart\(\)"[^>]*>.*?(?=<div class="menu-card|\n\s*</div>\s*</section>)',
            '',
            src,
            flags=re.DOTALL
        )

    # 5. Replace Data Block
    p_data = src.find('/* ---------------- DATA ---------------- */')
    p_state = src.find('/* ---------------- STATE ---------------- */')
    if p_data == -1 or p_state == -1:
        raise RuntimeError("DATA or STATE marker not found in template")

    new_data_code = f"""/* ---------------- DATA ---------------- */
// 1. 课文《{lesson["header_title"]}》(全新原创汉语情境课文)
const STORY = {json.dumps(lesson["story"], ensure_ascii=False, indent=2)};

// 2. 课后生字表 (12 核心汉字，田字格笔顺与部首全具备)
const CHARACTERS = {json.dumps(lesson["characters"], ensure_ascii=False, indent=2)};

// 3. 课后词语表 (12 原创课文生词)
const WORDS = {json.dumps(lesson["words"], ensure_ascii=False, indent=2)};

// 4. 课后常用口语表达 (7 项常用表达)
const PROPER_NOUNS = {json.dumps(lesson["proper_nouns"], ensure_ascii=False, indent=2)};

// 合并生词表 (19项)
const ALL_VOCAB = [...WORDS, ...PROPER_NOUNS];

// 5. 课后重点句子与排序 (5 Sentences)
const SCRAMBLE_SENTENCES = {json.dumps(lesson["scramble_sentences"], ensure_ascii=False, indent=2)};

// 6. 故事与字词问答 (8 Questions)
const QUIZ = {json.dumps(lesson["quiz"], ensure_ascii=False, indent=2)};

// 7. 选词填空 (8 课文原句填空)
const CLOZE_QUESTIONS = {json.dumps(lesson["cloze"], ensure_ascii=False, indent=2)};
"""

    src = src[:p_data] + new_data_code + "\n" + src[p_state:]

    # 6. Pinyin chart JS logic injection or kana cleanup
    # Replace legacy Kana Chart block cleanly up to INIT
    if lesson["has_pinyin_chart"]:
        src = re.sub(
            r'/\* ---------------- KANA CHART \(五十音図\) ---------------- \*/.*?(?=/\* ---------------- INIT ---------------- \*/)',
            PINYIN_JS_LOGIC.strip() + '\n\n',
            src,
            flags=re.DOTALL
        )
    else:
        src = re.sub(
            r'/\* ---------------- KANA CHART \(五十音図\) ---------------- \*/.*?(?=/\* ---------------- INIT ---------------- \*/)',
            '',
            src,
            flags=re.DOTALL
        )

    # 7. Update Footer
    src = src.replace('<footer>nhg.0101.click</footer>', '<footer>zw.0101.click · 原创汉语课程体系</footer>')

    target_path = os.path.join(BASE_DIR, f'{lesson["id"]}.html')
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(src)
    print(f"Generated {target_path} ({len(src)} bytes)")

# ----------------- ZH-INDEX GENERATION -----------------

def generate_zh_index():
    """Generate modern, responsive zh-index.html catalog portal."""
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-Y1P7PMMM6V"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});
      gtag('config', 'G-Y1P7PMMM6V');
    </script>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>汉语情境课文与识字闯关 - 课程一览</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&family=M+PLUS+Rounded+1c:wght@600;700;800;900&display=swap" rel="stylesheet">
<style>
  :root{
    --red:#c2410c; --imperial-red:#b91c1c; --imperial-gold:#d97706; --gold-soft:#fef3c7;
    --ink:#1c1917; --muted:#78716c;
    --card:#fffbf0;
    --radius-xl:28px; --radius-lg:20px;
    --shadow-card:0 14px 30px rgba(120,50,20,0.14);
    --shadow-pop:0 6px 0 rgba(0,0,0,0.14);
  }
  *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;}
  html,body{width:100%;min-height:100%;background:linear-gradient(160deg,#fff4e6,#ffedd5 60%,#fed7aa);
    font-family:"M PLUS Rounded 1c","ZCOOL KuaiLe","PingFang SC",system-ui,sans-serif;color:var(--ink);}
  body{display:flex;flex-direction:column;align-items:center;padding:32px 16px 48px;min-height:100vh;}
  header{text-align:center;margin-bottom:26px;}
  header .ico{font-size:46px;filter:drop-shadow(0 6px 8px rgba(0,0,0,0.15));}
  h1{font-size:24px;font-weight:900;color:var(--imperial-red);margin-top:8px;}
  p.sub{font-size:13px;color:var(--muted);margin-top:6px;max-width:500px;line-height:1.6;}

  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;width:100%;max-width:580px;margin-top:8px;}
  @media (max-width:480px){.grid{grid-template-columns:1fr;}}

  a.card{background:var(--card);border:2px solid #fbd38d;border-radius:var(--radius-lg);padding:20px 14px;text-align:center;
    box-shadow:var(--shadow-card);text-decoration:none;color:var(--ink);display:flex;flex-direction:column;align-items:center;gap:8px;
    transition:transform .08s, box-shadow .08s;cursor:pointer;position:relative;touch-action:manipulation;-webkit-tap-highlight-color:rgba(185,28,28,0.1);}
  a.card:hover{transform:translateY(-2px);box-shadow:0 18px 34px rgba(120,50,20,0.16);border-color:#f97316;}
  a.card:active{transform:scale(0.97);background:#fef3c7;}
  a.card .level-tag{position:absolute;top:10px;right:10px;font-size:10px;font-weight:800;background:#d97706;color:#fff;padding:2px 8px;border-radius:10px;}
  a.card .ico{font-size:38px;}
  a.card .name{font-size:17px;font-weight:800;color:var(--imperial-red);}
  a.card .name-en{font-size:11px;color:var(--muted);}
  a.card .desc{font-size:12px;color:var(--muted);margin-top:2px;line-height:1.5;}

  .nav-pills{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:28px;max-width:600px;}
  .pill-link{font-size:12px;font-weight:700;padding:6px 12px;border-radius:14px;background:#fff;border:1.5px solid #cbd5e1;color:var(--ink);text-decoration:none;transition:background .15s;touch-action:manipulation;}
  .pill-link:hover{background:#f1f5f9;}

  footer{margin-top:36px;font-size:11px;color:var(--muted);text-align:center;}
</style>
<link rel="canonical" href="https://zw.0101.click/zh-index.html">
</head>
<body>
  <header>
    <div class="ico">🇨🇳</div>
    <h1>全新汉语情境课文系列</h1>
    <p class="sub">100% 原创零版权风险情境语篇 · 阶梯式汉语识字与拼音闯关 · 象形字书写笔顺 · 对标日常实际交际。</p>
  </header>

  <div class="series-nav" style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:20px;max-width:580px;width:100%;">
    <a style="font-size:13px;font-weight:800;padding:8px 16px;border-radius:16px;background:#fff;border:2px solid #fbd38d;color:var(--ink);text-decoration:none;display:inline-flex;align-items:center;gap:6px;box-shadow:0 4px 10px rgba(0,0,0,0.06);transition:transform .1s;" href="https://zw.0101.click/zw-index.html">
      <span>📖</span>
      <span>统编教材 · 课文总览 (zw-index)</span>
    </a>
    <a style="font-size:13px;font-weight:800;padding:8px 16px;border-radius:16px;background:#fff7ed;border:2px solid #f97316;color:#c2410c;text-decoration:none;display:inline-flex;align-items:center;gap:6px;box-shadow:0 4px 10px rgba(194,65,12,0.1);transition:transform .1s;" href="https://zw.0101.click/zw-ty-4.html">
      <span>📚</span>
      <span>统编教材 · 第4册专页 (zw-ty-4)</span>
    </a>
  </div>

  <div class="grid">
    <a class="card" href="/zh0.html" role="link" aria-label="入门序章 拼音与日常问候">
      <span class="level-tag">入门序章</span>
      <div class="ico">
        <svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="28" fill="#fff" stroke="#b91c1c" stroke-width="3"/>
          <circle cx="32" cy="32" r="23" fill="#fff7ed" stroke="#fbd38d" stroke-width="1.5"/>
          <text x="32" y="44" font-family="'M PLUS Rounded 1c', sans-serif" font-size="30" font-weight="900" fill="#b91c1c" text-anchor="middle">拼</text>
        </svg>
      </div>
      <div class="name">拼音与日常问候</div>
      <div class="name-en">Level 0 · Pinyin &amp; Basic Greetings</div>
      <div class="desc">拼音启蒙 · 声母韵母四声调速听盘 · 基础寒暄礼貌用语 · 12个象形高频字</div>
    </a>

    <a class="card" href="/zh1.html" role="link" aria-label="第1课 我的一星期">
      <span class="level-tag">第 1 课</span>
      <div class="ico">
        <svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="28" fill="#fff" stroke="#b91c1c" stroke-width="3"/>
          <path d="M16 22 L48 22 L48 48 L16 48 Z" fill="#fff7ed" stroke="#b91c1c" stroke-width="2"/>
          <line x1="16" y1="30" x2="48" y2="30" stroke="#b91c1c" stroke-width="2"/>
          <line x1="26" y1="18" x2="26" y2="24" stroke="#b91c1c" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="38" y1="18" x2="38" y2="24" stroke="#b91c1c" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="24" cy="38" r="2.5" fill="#d97706"/>
          <circle cx="32" cy="38" r="2.5" fill="#d97706"/>
          <circle cx="40" cy="38" r="2.5" fill="#d97706"/>
        </svg>
      </div>
      <div class="name">我的一星期</div>
      <div class="name-en">Level 1 · My Week in Chinese</div>
      <div class="desc">一周生活流 · 校园与朋友 · 句型训练 · 核心字词识字闯关</div>
    </a>

    <a class="card" href="/zh2.html" role="link" aria-label="第2课 我的一天">
      <span class="level-tag">第 2 课</span>
      <div class="ico">
        <svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="26" fill="#fff" stroke="#b91c1c" stroke-width="4"/>
          <circle cx="32" cy="32" r="2.6" fill="#b91c1c"/>
          <line x1="32" y1="32" x2="32" y2="15" stroke="#b91c1c" stroke-width="3.4" stroke-linecap="round"/>
          <line x1="32" y1="32" x2="44" y2="39" stroke="#b91c1c" stroke-width="3.4" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="name">我的一天</div>
      <div class="name-en">Level 2 · My Day in Chinese</div>
      <div class="desc">24小时时刻表达 · 一日三餐与作息动作 · 汉字笔顺临摹与配对游戏</div>
    </a>

    <a class="card" href="/zh3.html" role="link" aria-label="第3课 中国的四季">
      <span class="level-tag">第 3 课</span>
      <div class="ico">
        <svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="28" fill="#fff" stroke="#b91c1c" stroke-width="3"/>
          <circle cx="32" cy="20" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="43" cy="28" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="39" cy="42" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="25" cy="42" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="21" cy="28" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="32" cy="32" r="5" fill="#fef08a"/>
        </svg>
      </div>
      <div class="name">中国的四季</div>
      <div class="name-en">Level 3 · Four Seasons in China</div>
      <div class="desc">春夏秋冬自然景物 · 节气气候与传统节日 · 进阶汉字与沉浸朗读</div>
    </a>
  </div>

  <div class="nav-pills">
    <a class="pill-link" href="https://zw.0101.click/zw-index.html">📖 统编课文总览 (zw)</a>
    <a class="pill-link" href="https://zw.0101.click/zw-ty-4.html">📚 统编第4册 (zw-ty-4)</a>
    <a class="pill-link" href="https://l.0101.click">🏠 游乐场首页</a>
    <a class="pill-link" href="https://l.0101.click/languages.html">🌐 多语言大厅</a>
    <a class="pill-link" href="https://nhg.0101.click">🎌 日语课文一览</a>
    <a class="pill-link" href="https://hge.0101.click">🇰🇷 韩语课文一览</a>
  </div>

  <footer>zw.0101.click · 原创汉语情境课程系列</footer>

  <div class="site-legal-0101" style="clear:both;width:100%;box-sizing:border-box;padding:16px 12px 20px;text-align:center;font:12px/1.7 system-ui,sans-serif;color:#64748b;opacity:.9"><a href="https://0101.click/privacy.html" style="color:inherit;text-decoration:underline;opacity:.85">隐私政策 / プライバシー</a> · <a href="https://0101.click/about.html" style="color:inherit;text-decoration:underline;opacity:.85">关于 / 運営者情報</a> · <a href="https://0101.click/contact.html" style="color:inherit;text-decoration:underline;opacity:.85">联系 / お問い合わせ</a> · <a href="https://0101.click/" style="color:inherit;text-decoration:underline;opacity:.85">0101.click</a></div>

  <script>
    // 移动端/触屏/各浏览器点击导航增强与兜底
    document.querySelectorAll('a.card').forEach(function(card) {
      card.addEventListener('click', function(e) {
        if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) {
          return;
        }
        var targetUrl = this.getAttribute('href');
        if (targetUrl) {
          window.location.href = targetUrl;
        }
      });
    });
  </script>
</body>
</html>
"""
    target = os.path.join(BASE_DIR, 'zh-index.html')
    with open(target, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated {target} ({len(html)} bytes)")

# ----------------- MAIN PIPELINE -----------------

def main():
    print("=== Building New Chinese Lessons Series ===")
    for lesson in LESSONS:
        generate_lesson_html(lesson)
    generate_zh_index()
    print("=== All 5 files generated successfully! ===")

if __name__ == '__main__':
    main()
