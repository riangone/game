// 由 build_en_lessons.py 从 data/en-lessons-data.json 生成，请勿手改。
// English Micro-Narrative Curriculum Data
window.EN_LESSONS_DATA = [
  {
    "id": "en1",
    "level": 1,
    "title": "Morning Coffee",
    "titleZh": "晨间咖啡点单",
    "situation": "在街角咖啡馆点一杯小杯冰拿铁，说明甜度，选择外带并询问等待时间。",
    "icon": "☕",
    "tags": [
      "日常生存",
      "高频点单",
      "连读突破"
    ],
    "chunks": [
      {
        "id": "en1_c1",
        "text": "Can I get a...",
        "meaning": "请给我来一份……（最自然的点单句式）",
        "phonetic": "/kən aɪ ˈɡet ə/",
        "usageTip": "比 I want... 更礼貌自然。Can I 和 get a 都要连读。",
        "warmupQuiz": {
          "prompt": "组装短语：“请给我来一份……”",
          "tokens": [
            "get a",
            "Can I",
            "please"
          ],
          "correct": [
            "Can I",
            "get a"
          ]
        }
      },
      {
        "id": "en1_c2",
        "text": "For here or to go?",
        "meaning": "在这儿吃喝还是带走？",
        "phonetic": "/fər hɪr ɔːr tə ɡoʊ/",
        "usageTip": "柜台点单必问句。英式英语常说 Eat in or take away?",
        "warmupQuiz": {
          "prompt": "组装短语：“堂食还是外带？”",
          "tokens": [
            "to go",
            "or",
            "For here"
          ],
          "correct": [
            "For here",
            "or",
            "to go"
          ]
        }
      },
      {
        "id": "en1_c3",
        "text": "How long is the wait?",
        "meaning": "要等多久？",
        "phonetic": "/haʊ lɔŋ ɪz ðə weɪt/",
        "usageTip": "wait 在这里是名词“等待时间”。餐厅、排队、取号都能用。",
        "warmupQuiz": {
          "prompt": "组装短语：“要等多久？”",
          "tokens": [
            "the wait",
            "How long",
            "is",
            "time"
          ],
          "correct": [
            "How long",
            "is",
            "the wait"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en1_d1",
        "speaker": "B",
        "speakerName": "Barista",
        "role": "咖啡师",
        "en": "Good morning! What can I get for you?",
        "zh": "早上好！想喝点什么？",
        "phoneticHtml": "Good morning! <span class='linking'>What‿can‿I</span> get for you?",
        "linkingNotes": [
          "What can I：t 失去爆破，can 和 I 连读成 /kə-naɪ/。"
        ]
      },
      {
        "id": "en1_d2",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Hi! Can I get a small iced latte, please?",
        "zh": "嗨！请给我一杯小杯冰拿铁。",
        "phoneticHtml": "Hi! <span class='linking'>Can‿I</span> <span class='linking'>get‿a</span> small iced latte, please?",
        "linkingNotes": [
          "get a 里的 t 弱化成闪音，听起来像 /ɡe-də/。"
        ]
      },
      {
        "id": "en1_d3",
        "speaker": "B",
        "speakerName": "Barista",
        "role": "咖啡师",
        "en": "Sure. Would you like it sweet?",
        "zh": "好的。要加甜吗？",
        "phoneticHtml": "Sure. <span class='linking'>Would‿you</span> <span class='linking'>like‿it</span> sweet?",
        "linkingNotes": [
          "Would you 同化为 /wʊ-dʒu/，like it 连读成 /laɪ-kɪt/。"
        ]
      },
      {
        "id": "en1_d4",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Just a little sweet, please.",
        "zh": "稍微甜一点就好。",
        "phoneticHtml": "<span class='linking'>Just‿a</span> little sweet, please.",
        "linkingNotes": [
          "Just a 连读成 /dʒʌs-tə/。"
        ]
      },
      {
        "id": "en1_d5",
        "speaker": "B",
        "speakerName": "Barista",
        "role": "咖啡师",
        "en": "For here or to go?",
        "zh": "在这儿喝还是带走？",
        "phoneticHtml": "For <span class='linking'>here‿or</span> <span class='reduction'>to</span> go?",
        "linkingNotes": [
          "here or 连读，to 弱读为 /tə/。"
        ]
      },
      {
        "id": "en1_d6",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "To go, please. How long is the wait?",
        "zh": "带走，谢谢。要等多久？",
        "phoneticHtml": "<span class='reduction'>To</span> go, please. How <span class='linking'>long‿is</span> the wait?",
        "linkingNotes": [
          "long is 连读成 /lɔŋ-ɪz/。"
        ]
      },
      {
        "id": "en1_d7",
        "speaker": "B",
        "speakerName": "Barista",
        "role": "咖啡师",
        "en": "About five minutes. Your order will be ready soon.",
        "zh": "大约五分钟。您点的很快就好。",
        "phoneticHtml": "About five minutes. <span class='linking'>Your‿order</span> will be ready soon.",
        "linkingNotes": [
          "Your order：r 和 o 连读成 /jʊ-rɔːr-dər/。"
        ]
      },
      {
        "id": "en1_d8",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Great, I can wait. Thank you!",
        "zh": "好的，我可以等。谢谢！",
        "phoneticHtml": "Great, I <span class='reduction'>can</span> wait. <span class='linking'>Thank‿you</span>!",
        "linkingNotes": [
          "can 在句中弱读为 /kən/；Thank you 连读成 /θæŋ-kju/。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (顾客)",
      "description": "扮演到店顾客 Alex，跟随咖啡师的问询完成自然点餐与定制要求。"
    },
    "vocabulary": [
      {
        "id": "en1_v1",
        "word": "order",
        "phonetic": "/ˈɔːrdər/",
        "pos": "n./v.",
        "meaning": "点的东西；点（餐）",
        "audio": "audio/en_vocab/en1_v1.mp3",
        "example": "About five minutes. Your order will be ready soon.",
        "exampleZh": "大约五分钟。您点的很快就好。",
        "forms": [
          "order"
        ]
      },
      {
        "id": "en1_v2",
        "word": "small",
        "phonetic": "/smɔːl/",
        "pos": "adj.",
        "meaning": "小的；小杯的",
        "audio": "audio/en_vocab/en1_v2.mp3",
        "example": "Hi! Can I get a small iced latte, please?",
        "exampleZh": "嗨！请给我一杯小杯冰拿铁。",
        "forms": [
          "small"
        ]
      },
      {
        "id": "en1_v3",
        "word": "sweet",
        "phonetic": "/swiːt/",
        "pos": "adj.",
        "meaning": "甜的",
        "audio": "audio/en_vocab/en1_v3.mp3",
        "example": "Sure. Would you like it sweet?",
        "exampleZh": "好的。要加甜吗？",
        "forms": [
          "sweet"
        ]
      },
      {
        "id": "en1_v4",
        "word": "ready",
        "phonetic": "/ˈredi/",
        "pos": "adj.",
        "meaning": "准备好的",
        "audio": "audio/en_vocab/en1_v4.mp3",
        "example": "About five minutes. Your order will be ready soon.",
        "exampleZh": "大约五分钟。您点的很快就好。",
        "forms": [
          "ready"
        ]
      },
      {
        "id": "en1_v5",
        "word": "minute",
        "phonetic": "/ˈmɪnɪt/",
        "pos": "n.",
        "meaning": "分钟",
        "audio": "audio/en_vocab/en1_v5.mp3",
        "example": "About five minutes. Your order will be ready soon.",
        "exampleZh": "大约五分钟。您点的很快就好。",
        "forms": [
          "minute",
          "minutes"
        ]
      },
      {
        "id": "en1_v6",
        "word": "wait",
        "phonetic": "/weɪt/",
        "pos": "v./n.",
        "meaning": "等待；等待时间",
        "audio": "audio/en_vocab/en1_v6.mp3",
        "example": "To go, please. How long is the wait?",
        "exampleZh": "带走，谢谢。要等多久？",
        "forms": [
          "wait"
        ]
      }
    ],
    "topicWords": [
      {
        "id": "en1_t1",
        "word": "latte",
        "phonetic": "/ˈlɑːteɪ/",
        "pos": "n.",
        "meaning": "拿铁咖啡",
        "audio": "audio/en_vocab/en1_t1.mp3",
        "example": "Hi! Can I get a small iced latte, please?",
        "exampleZh": "嗨！请给我一杯小杯冰拿铁。",
        "forms": [
          "latte"
        ]
      },
      {
        "id": "en1_t2",
        "word": "iced",
        "phonetic": "/aɪst/",
        "pos": "adj.",
        "meaning": "加冰的",
        "audio": "audio/en_vocab/en1_t2.mp3",
        "example": "Hi! Can I get a small iced latte, please?",
        "exampleZh": "嗨！请给我一杯小杯冰拿铁。",
        "forms": [
          "iced"
        ]
      }
    ],
    "properNouns": []
  },
  {
    "id": "en2",
    "level": 1,
    "title": "Lost in the Subway",
    "titleZh": "地铁站问路与换乘",
    "situation": "在地铁站问去中央公园坐哪条线、要不要换乘、远不远，以及下一班车什么时候来。",
    "icon": "🚇",
    "tags": [
      "公共出行",
      "方向问询",
      "辅元连读"
    ],
    "chunks": [
      {
        "id": "en2_c1",
        "text": "Which train goes to...",
        "meaning": "哪趟车去……？",
        "phonetic": "/wɪtʃ treɪn ɡoʊz tə/",
        "usageTip": "问路最实用的句式，后面接地名。goes to 连读，to 弱读。",
        "warmupQuiz": {
          "prompt": "组装短语：“哪趟车去……？”",
          "tokens": [
            "goes to",
            "Which train",
            "stop"
          ],
          "correct": [
            "Which train",
            "goes to"
          ]
        }
      },
      {
        "id": "en2_c2",
        "text": "Do I need to change trains?",
        "meaning": "我需要换乘吗？",
        "phonetic": "/du aɪ niːd tə tʃeɪndʒ treɪnz/",
        "usageTip": "change trains 是固定搭配，trains 要用复数。",
        "warmupQuiz": {
          "prompt": "组装短语：“我需要换乘吗？”",
          "tokens": [
            "change trains",
            "Do I",
            "need to",
            "far"
          ],
          "correct": [
            "Do I",
            "need to",
            "change trains"
          ]
        }
      },
      {
        "id": "en2_c3",
        "text": "When is the next train?",
        "meaning": "下一趟车什么时候来？",
        "phonetic": "/wen ɪz ðə nekst treɪn/",
        "usageTip": "next train 两个 t 相遇，第一个 t 失去爆破。",
        "warmupQuiz": {
          "prompt": "组装短语：“下一趟车什么时候来？”",
          "tokens": [
            "the next train",
            "When is",
            "line"
          ],
          "correct": [
            "When is",
            "the next train"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en2_d1",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "乘客 (你)",
        "en": "Excuse me, which train goes to Central Park?",
        "zh": "打扰一下，哪趟车去中央公园？",
        "phoneticHtml": "Excuse me, which train <span class='linking'>goes‿to</span> Central Park?",
        "linkingNotes": [
          "goes to 连读，to 弱读为 /tə/。"
        ]
      },
      {
        "id": "en2_d2",
        "speaker": "B",
        "speakerName": "Officer",
        "role": "站务员",
        "en": "Take the Blue Line. It stops at Central Park.",
        "zh": "坐蓝线，它在中央公园停。",
        "phoneticHtml": "Take the Blue Line. It <span class='linking'>stops‿at</span> Central Park.",
        "linkingNotes": [
          "stops at 连读成 /stɑp-sæt/。"
        ]
      },
      {
        "id": "en2_d3",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "乘客 (你)",
        "en": "Do I need to change trains?",
        "zh": "我需要换乘吗？",
        "phoneticHtml": "Do I <span class='linking'>need‿to</span> change trains?",
        "linkingNotes": [
          "need to：d 和 t 发音部位相同，只发一次，读成 /niː-tə/。"
        ]
      },
      {
        "id": "en2_d4",
        "speaker": "B",
        "speakerName": "Officer",
        "role": "站务员",
        "en": "No, you don't. It's five stops from here.",
        "zh": "不用。从这儿坐五站就到。",
        "phoneticHtml": "No, you don't. It's five stops from here.",
        "linkingNotes": [
          "don't 的 t 在句末常常只做口型，不完全爆破。"
        ]
      },
      {
        "id": "en2_d5",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "乘客 (你)",
        "en": "Is it far?",
        "zh": "远吗？",
        "phoneticHtml": "<span class='linking'>Is‿it</span> far?",
        "linkingNotes": [
          "Is it 连读成 /ɪ-zɪt/。"
        ]
      },
      {
        "id": "en2_d6",
        "speaker": "B",
        "speakerName": "Officer",
        "role": "站务员",
        "en": "Not really. About fifteen minutes.",
        "zh": "不太远，大概十五分钟。",
        "phoneticHtml": "Not really. About fifteen minutes.",
        "linkingNotes": [
          "Not really：t 失去爆破。"
        ]
      },
      {
        "id": "en2_d7",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "乘客 (你)",
        "en": "When is the next train?",
        "zh": "下一趟车什么时候来？",
        "phoneticHtml": "<span class='linking'>When‿is</span> the next train?",
        "linkingNotes": [
          "When is 连读成 /we-nɪz/；next train 的第一个 t 失去爆破。"
        ]
      },
      {
        "id": "en2_d8",
        "speaker": "B",
        "speakerName": "Officer",
        "role": "站务员",
        "en": "In two minutes. Please wait over here.",
        "zh": "两分钟后到。请在这边等。",
        "phoneticHtml": "In two minutes. Please <span class='linking'>wait‿over</span> here.",
        "linkingNotes": [
          "wait over 连读，t 弱化成闪音，像 /weɪ-doʊ-vər/。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (乘客)",
      "description": "扮演找不到站台的乘客，向工作人员核对列车方向与下车站点。"
    },
    "vocabulary": [
      {
        "id": "en2_v1",
        "word": "train",
        "phonetic": "/treɪn/",
        "pos": "n.",
        "meaning": "火车；地铁列车",
        "audio": "audio/en_vocab/en2_v1.mp3",
        "example": "Excuse me, which train goes to Central Park?",
        "exampleZh": "打扰一下，哪趟车去中央公园？",
        "forms": [
          "train",
          "trains"
        ]
      },
      {
        "id": "en2_v2",
        "word": "line",
        "phonetic": "/laɪn/",
        "pos": "n.",
        "meaning": "（地铁）线路；队伍",
        "audio": "audio/en_vocab/en2_v2.mp3",
        "example": "Take the Blue Line. It stops at Central Park.",
        "exampleZh": "坐蓝线，它在中央公园停。",
        "forms": [
          "line"
        ]
      },
      {
        "id": "en2_v3",
        "word": "stop",
        "phonetic": "/stɑːp/",
        "pos": "n./v.",
        "meaning": "车站；停下",
        "audio": "audio/en_vocab/en2_v3.mp3",
        "example": "Take the Blue Line. It stops at Central Park.",
        "exampleZh": "坐蓝线，它在中央公园停。",
        "forms": [
          "stop",
          "stops",
          "stopped"
        ]
      },
      {
        "id": "en2_v4",
        "word": "change",
        "phonetic": "/tʃeɪndʒ/",
        "pos": "v.",
        "meaning": "换；换乘",
        "audio": "audio/en_vocab/en2_v4.mp3",
        "example": "Do I need to change trains?",
        "exampleZh": "我需要换乘吗？",
        "forms": [
          "change"
        ]
      },
      {
        "id": "en2_v5",
        "word": "far",
        "phonetic": "/fɑːr/",
        "pos": "adj.",
        "meaning": "远的",
        "audio": "audio/en_vocab/en2_v5.mp3",
        "example": "Is it far?",
        "exampleZh": "远吗？",
        "forms": [
          "far"
        ]
      },
      {
        "id": "en2_v6",
        "word": "next",
        "phonetic": "/nekst/",
        "pos": "adj.",
        "meaning": "下一个的；旁边的",
        "audio": "audio/en_vocab/en2_v6.mp3",
        "example": "When is the next train?",
        "exampleZh": "下一趟车什么时候来？",
        "forms": [
          "next"
        ]
      }
    ],
    "topicWords": [],
    "properNouns": [
      "Central",
      "Park"
    ]
  },
  {
    "id": "en3",
    "level": 1,
    "title": "Late for Meeting",
    "titleZh": "会议迟到说明与致歉",
    "situation": "地铁临时停车，开会要迟到，打电话向主管说明情况，请大家先开始。",
    "icon": "⏰",
    "tags": [
      "职场日常",
      "轻微致歉",
      "地道表达"
    ],
    "chunks": [
      {
        "id": "en3_c1",
        "text": "I'm going to be late.",
        "meaning": "我要迟到了。",
        "phonetic": "/aɪm ˈɡʌnə bi leɪt/",
        "usageTip": "going to 口语常弱读成 gonna /ˈɡʌnə/。",
        "warmupQuiz": {
          "prompt": "组装短语：“我要迟到了。”",
          "tokens": [
            "be late",
            "I'm",
            "going to",
            "early"
          ],
          "correct": [
            "I'm",
            "going to",
            "be late"
          ]
        }
      },
      {
        "id": "en3_c2",
        "text": "No worries.",
        "meaning": "没关系 / 别担心。",
        "phonetic": "/noʊ ˈwɜːriz/",
        "usageTip": "比 It's OK 更轻松友好，美式、澳式口语都很常用。",
        "warmupQuiz": {
          "prompt": "组装短语：“没关系。”",
          "tokens": [
            "worries",
            "No",
            "problem"
          ],
          "correct": [
            "No",
            "worries"
          ]
        }
      },
      {
        "id": "en3_c3",
        "text": "Go ahead and start without me.",
        "meaning": "你们先开始吧，不用等我。",
        "phonetic": "/ɡoʊ əˈhed ən stɑːrt wɪˈðaʊt mi/",
        "usageTip": "go ahead 中间加一个轻微的 /w/ 过渡；and 弱读为 /ən/。",
        "warmupQuiz": {
          "prompt": "组装短语：“你们先开始吧，不用等我。”",
          "tokens": [
            "without me",
            "Go ahead",
            "and start",
            "wait"
          ],
          "correct": [
            "Go ahead",
            "and start",
            "without me"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en3_d1",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "员工 (你)",
        "en": "Hi Sarah, I'm sorry, but I'm going to be late.",
        "zh": "嗨 Sarah，抱歉，我要迟到了。",
        "phoneticHtml": "Hi Sarah, I'm sorry, but I'm <span class='linking'>going‿to</span> be late.",
        "linkingNotes": [
          "going to 口语常读成 gonna /ˈɡʌnə/。"
        ]
      },
      {
        "id": "en3_d2",
        "speaker": "B",
        "speakerName": "Sarah",
        "role": "主管",
        "en": "No worries. What happened?",
        "zh": "没关系。怎么了？",
        "phoneticHtml": "No worries. What happened?",
        "linkingNotes": [
          "What happened：What 的 t 失去爆破。"
        ]
      },
      {
        "id": "en3_d3",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "员工 (你)",
        "en": "My train stopped for ten minutes. There was a problem on the line.",
        "zh": "我坐的车停了十分钟，线路出了问题。",
        "phoneticHtml": "My train stopped for ten minutes. There <span class='linking'>was‿a</span> <span class='linking'>problem‿on</span> the line.",
        "linkingNotes": [
          "was a 连读成 /wə-zə/，problem on 连读成 /prɑbləm-ɑn/。"
        ]
      },
      {
        "id": "en3_d4",
        "speaker": "B",
        "speakerName": "Sarah",
        "role": "主管",
        "en": "Oh no. When can you get here?",
        "zh": "哎呀，你什么时候能到？",
        "phoneticHtml": "Oh no. When <span class='reduction'>can</span> you get here?",
        "linkingNotes": [
          "can 弱读为 /kən/；get here 的 t 失去爆破。"
        ]
      },
      {
        "id": "en3_d5",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "员工 (你)",
        "en": "The next stop is mine. I'll be there in twenty minutes.",
        "zh": "下一站就到了，我二十分钟后到。",
        "phoneticHtml": "The next <span class='linking'>stop‿is</span> mine. I'll be <span class='linking'>there‿in</span> twenty minutes.",
        "linkingNotes": [
          "stop is 连读成 /stɑ-pɪz/；there in 连读成 /ðe-rɪn/。"
        ]
      },
      {
        "id": "en3_d6",
        "speaker": "B",
        "speakerName": "Sarah",
        "role": "主管",
        "en": "OK. We're almost ready to start. Should we wait for you?",
        "zh": "好的，我们差不多要开始了。要等你吗？",
        "phoneticHtml": "OK. We're almost ready <span class='reduction'>to</span> start. Should we wait for you?",
        "linkingNotes": [
          "to 弱读为 /tə/；wait for 的 t 失去爆破。"
        ]
      },
      {
        "id": "en3_d7",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "员工 (你)",
        "en": "No, please go ahead and start without me.",
        "zh": "不用，请先开始吧，不用等我。",
        "phoneticHtml": "No, please <span class='linking'>go‿ahead‿and</span> start without me.",
        "linkingNotes": [
          "go ahead 中间带轻微 /w/ 过渡；and 弱读为 /ən/。"
        ]
      },
      {
        "id": "en3_d8",
        "speaker": "B",
        "speakerName": "Sarah",
        "role": "主管",
        "en": "Will do. Don't worry, and stay safe!",
        "zh": "好的。别担心，注意安全！",
        "phoneticHtml": "Will do. Don't worry, and stay safe!",
        "linkingNotes": [
          "Don't worry：t 失去爆破；and 弱读为 /ən/。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (员工)",
      "description": "地铁临时停车要迟到，打电话向主管说明情况，请大家先开始。"
    },
    "vocabulary": [
      {
        "id": "en3_v1",
        "word": "late",
        "phonetic": "/leɪt/",
        "pos": "adj.",
        "meaning": "迟到的；晚的",
        "audio": "audio/en_vocab/en3_v1.mp3",
        "example": "Hi Sarah, I'm sorry, but I'm going to be late.",
        "exampleZh": "嗨 Sarah，抱歉，我要迟到了。",
        "forms": [
          "late"
        ]
      },
      {
        "id": "en3_v2",
        "word": "worry",
        "phonetic": "/ˈwɜːri/",
        "pos": "v./n.",
        "meaning": "担心",
        "audio": "audio/en_vocab/en3_v2.mp3",
        "example": "No worries. What happened?",
        "exampleZh": "没关系。怎么了？",
        "forms": [
          "worry",
          "worries"
        ]
      },
      {
        "id": "en3_v3",
        "word": "start",
        "phonetic": "/stɑːrt/",
        "pos": "v.",
        "meaning": "开始",
        "audio": "audio/en_vocab/en3_v3.mp3",
        "example": "OK. We're almost ready to start. Should we wait for you?",
        "exampleZh": "好的，我们差不多要开始了。要等你吗？",
        "forms": [
          "start",
          "starts"
        ]
      },
      {
        "id": "en3_v4",
        "word": "safe",
        "phonetic": "/seɪf/",
        "pos": "adj.",
        "meaning": "安全的",
        "audio": "audio/en_vocab/en3_v4.mp3",
        "example": "Will do. Don't worry, and stay safe!",
        "exampleZh": "好的。别担心，注意安全！",
        "forms": [
          "safe"
        ]
      },
      {
        "id": "en3_v5",
        "word": "problem",
        "phonetic": "/ˈprɑːbləm/",
        "pos": "n.",
        "meaning": "问题；故障",
        "audio": "audio/en_vocab/en3_v5.mp3",
        "example": "My train stopped for ten minutes. There was a problem on the line.",
        "exampleZh": "我坐的车停了十分钟，线路出了问题。",
        "forms": [
          "problem"
        ]
      },
      {
        "id": "en3_v6",
        "word": "almost",
        "phonetic": "/ˈɔːlmoʊst/",
        "pos": "adv.",
        "meaning": "几乎，差不多",
        "audio": "audio/en_vocab/en3_v6.mp3",
        "example": "OK. We're almost ready to start. Should we wait for you?",
        "exampleZh": "好的，我们差不多要开始了。要等你吗？",
        "forms": [
          "almost"
        ]
      }
    ],
    "topicWords": [],
    "properNouns": []
  },
  {
    "id": "en4",
    "level": 1,
    "title": "Quick Lunch Order",
    "titleZh": "轻食快餐快捷点选",
    "situation": "午饭时间在快餐店点三明治和饮料，刷卡付款，临时把饮料换成茶。",
    "icon": "🥪",
    "tags": [
      "午餐就餐",
      "偏好选择",
      "辅元连读"
    ],
    "chunks": [
      {
        "id": "en4_c1",
        "text": "Next, please!",
        "meaning": "下一位！",
        "phonetic": "/nekst pliːz/",
        "usageTip": "排队点餐、办事窗口最常听到的一句话。next 的 t 在 please 前失去爆破。",
        "warmupQuiz": {
          "prompt": "组装短语：“下一位！”",
          "tokens": [
            "please",
            "Next",
            "wait"
          ],
          "correct": [
            "Next",
            "please"
          ]
        }
      },
      {
        "id": "en4_c2",
        "text": "How would you like to pay?",
        "meaning": "您想怎么付款？",
        "phonetic": "/haʊ wʊd ju laɪk tə peɪ/",
        "usageTip": "收银员必问句。回答 By card / In cash 即可。",
        "warmupQuiz": {
          "prompt": "组装短语：“您想怎么付款？”",
          "tokens": [
            "to pay",
            "How would",
            "you like",
            "order"
          ],
          "correct": [
            "How would",
            "you like",
            "to pay"
          ]
        }
      },
      {
        "id": "en4_c3",
        "text": "Can I change my drink?",
        "meaning": "我能换一下饮料吗？",
        "phonetic": "/kən aɪ tʃeɪndʒ maɪ drɪŋk/",
        "usageTip": "change A to B：把 A 换成 B。点完单想改主意时用。",
        "warmupQuiz": {
          "prompt": "组装短语：“我能换一下饮料吗？”",
          "tokens": [
            "my drink",
            "Can I",
            "change",
            "price"
          ],
          "correct": [
            "Can I",
            "change",
            "my drink"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en4_d1",
        "speaker": "B",
        "speakerName": "Clerk",
        "role": "店员",
        "en": "Next, please! What can I get you for lunch?",
        "zh": "下一位！午饭想吃点什么？",
        "phoneticHtml": "Next, please! <span class='linking'>What‿can‿I</span> get you for lunch?",
        "linkingNotes": [
          "What can I：t 失去爆破，can 和 I 连读。"
        ]
      },
      {
        "id": "en4_d2",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Hi. Can I order the chicken sandwich?",
        "zh": "你好，我点一份鸡肉三明治。",
        "phoneticHtml": "Hi. <span class='linking'>Can‿I‿order</span> the chicken sandwich?",
        "linkingNotes": [
          "I order 之间带轻微 /j/ 过渡：/kə-naɪ-jɔːr-dər/。"
        ]
      },
      {
        "id": "en4_d3",
        "speaker": "B",
        "speakerName": "Clerk",
        "role": "店员",
        "en": "Sure. Do you want a drink with that?",
        "zh": "好的。要配一杯饮料吗？",
        "phoneticHtml": "Sure. Do you <span class='linking'>want‿a</span> drink with that?",
        "linkingNotes": [
          "want a 口语中 t 常省略，读成 /wɑ-nə/。"
        ]
      },
      {
        "id": "en4_d4",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Yes, a small coffee, please. Not too sweet.",
        "zh": "要，一杯小杯咖啡，别太甜。",
        "phoneticHtml": "Yes, a small coffee, please. Not too sweet.",
        "linkingNotes": [
          "Not too：两个 t 相遇，第一个 t 失去爆破。"
        ]
      },
      {
        "id": "en4_d5",
        "speaker": "B",
        "speakerName": "Clerk",
        "role": "店员",
        "en": "That's nine dollars. How would you like to pay?",
        "zh": "一共九美元。您想怎么付款？",
        "phoneticHtml": "That's nine dollars. How <span class='linking'>would‿you</span> like <span class='reduction'>to</span> pay?",
        "linkingNotes": [
          "would you 同化为 /wʊ-dʒu/；to 弱读为 /tə/。"
        ]
      },
      {
        "id": "en4_d6",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "By card, please. Oh, wait. Can I change my drink to tea?",
        "zh": "刷卡，谢谢。哦，等一下，我能把饮料换成茶吗？",
        "phoneticHtml": "By card, please. Oh, wait. <span class='linking'>Can‿I</span> change my drink <span class='reduction'>to</span> tea?",
        "linkingNotes": [
          "Can I 连读；to 弱读为 /tə/。"
        ]
      },
      {
        "id": "en4_d7",
        "speaker": "B",
        "speakerName": "Clerk",
        "role": "店员",
        "en": "No problem. It's the same price. Your order will be ready in five minutes.",
        "zh": "没问题，价格一样。您的餐五分钟后就好。",
        "phoneticHtml": "No problem. It's the same price. <span class='linking'>Your‿order</span> will be <span class='linking'>ready‿in</span> five minutes.",
        "linkingNotes": [
          "Your order：r 和 o 连读；ready in 连读成 /re-di-jɪn/。"
        ]
      },
      {
        "id": "en4_d8",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Thanks! I'm so hungry, and I'm almost late for work.",
        "zh": "谢谢！我好饿，上班也快迟到了。",
        "phoneticHtml": "Thanks! I'm so hungry, and I'm almost late for work.",
        "linkingNotes": [
          "and 弱读为 /ən/；late for 的 t 失去爆破。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (顾客)",
      "description": "在快餐店点餐、配饮料、刷卡付款，并临时把饮料换成茶。"
    },
    "vocabulary": [
      {
        "id": "en4_v1",
        "word": "lunch",
        "phonetic": "/lʌntʃ/",
        "pos": "n.",
        "meaning": "午饭",
        "audio": "audio/en_vocab/en4_v1.mp3",
        "example": "Next, please! What can I get you for lunch?",
        "exampleZh": "下一位！午饭想吃点什么？",
        "forms": [
          "lunch"
        ]
      },
      {
        "id": "en4_v2",
        "word": "drink",
        "phonetic": "/drɪŋk/",
        "pos": "n.",
        "meaning": "饮料",
        "audio": "audio/en_vocab/en4_v2.mp3",
        "example": "Sure. Do you want a drink with that?",
        "exampleZh": "好的。要配一杯饮料吗？",
        "forms": [
          "drink"
        ]
      },
      {
        "id": "en4_v3",
        "word": "pay",
        "phonetic": "/peɪ/",
        "pos": "v.",
        "meaning": "付款",
        "audio": "audio/en_vocab/en4_v3.mp3",
        "example": "That's nine dollars. How would you like to pay?",
        "exampleZh": "一共九美元。您想怎么付款？",
        "forms": [
          "pay"
        ]
      },
      {
        "id": "en4_v4",
        "word": "card",
        "phonetic": "/kɑːrd/",
        "pos": "n.",
        "meaning": "卡；银行卡",
        "audio": "audio/en_vocab/en4_v4.mp3",
        "example": "By card, please. Oh, wait. Can I change my drink to tea?",
        "exampleZh": "刷卡，谢谢。哦，等一下，我能把饮料换成茶吗？",
        "forms": [
          "card"
        ]
      },
      {
        "id": "en4_v5",
        "word": "price",
        "phonetic": "/praɪs/",
        "pos": "n.",
        "meaning": "价格",
        "audio": "audio/en_vocab/en4_v5.mp3",
        "example": "No problem. It's the same price. Your order will be ready in five minutes.",
        "exampleZh": "没问题，价格一样。您的餐五分钟后就好。",
        "forms": [
          "price"
        ]
      },
      {
        "id": "en4_v6",
        "word": "hungry",
        "phonetic": "/ˈhʌŋɡri/",
        "pos": "adj.",
        "meaning": "饿的",
        "audio": "audio/en_vocab/en4_v6.mp3",
        "example": "Thanks! I'm so hungry, and I'm almost late for work.",
        "exampleZh": "谢谢！我好饿，上班也快迟到了。",
        "forms": [
          "hungry"
        ]
      }
    ],
    "topicWords": [
      {
        "id": "en4_t1",
        "word": "sandwich",
        "phonetic": "/ˈsænwɪtʃ/",
        "pos": "n.",
        "meaning": "三明治",
        "audio": "audio/en_vocab/en4_t1.mp3",
        "example": "Hi. Can I order the chicken sandwich?",
        "exampleZh": "你好，我点一份鸡肉三明治。",
        "forms": [
          "sandwich",
          "sandwiches"
        ]
      },
      {
        "id": "en4_t2",
        "word": "chicken",
        "phonetic": "/ˈtʃɪkɪn/",
        "pos": "n.",
        "meaning": "鸡肉",
        "audio": "audio/en_vocab/en4_t2.mp3",
        "example": "Hi. Can I order the chicken sandwich?",
        "exampleZh": "你好，我点一份鸡肉三明治。",
        "forms": [
          "chicken"
        ]
      }
    ],
    "properNouns": []
  },
  {
    "id": "en5",
    "level": 2,
    "title": "Supermarket Aisle",
    "titleZh": "超市货架导购与寻物",
    "situation": "在超市找鲜牛奶，问路线，确认面包打折，并了解付款方式。",
    "icon": "🛒",
    "tags": [
      "生活购物",
      "位置询问",
      "常用句型"
    ],
    "chunks": [
      {
        "id": "en5_c1",
        "text": "Where can I find...",
        "meaning": "在哪儿能找到……？",
        "phonetic": "/wer kən aɪ faɪnd/",
        "usageTip": "找东西万能句。can 弱读为 /kən/，can I 连读。",
        "warmupQuiz": {
          "prompt": "组装短语：“在哪儿能找到……？”",
          "tokens": [
            "find",
            "Where",
            "can I",
            "far"
          ],
          "correct": [
            "Where",
            "can I",
            "find"
          ]
        }
      },
      {
        "id": "en5_c2",
        "text": "Is it far from here?",
        "meaning": "离这儿远吗？",
        "phonetic": "/ɪz ɪt fɑːr frəm hɪr/",
        "usageTip": "Is it 连读成 /ɪ-zɪt/，from 弱读为 /frəm/。",
        "warmupQuiz": {
          "prompt": "组装短语：“离这儿远吗？”",
          "tokens": [
            "far",
            "Is it",
            "from here",
            "next"
          ],
          "correct": [
            "Is it",
            "far",
            "from here"
          ]
        }
      },
      {
        "id": "en5_c3",
        "text": "on sale",
        "meaning": "打折；在促销",
        "phonetic": "/ɑːn seɪl/",
        "usageTip": "on sale 是“打折”。for sale 是“出售中”，意思不同。",
        "warmupQuiz": {
          "prompt": "组装短语：“打折中”",
          "tokens": [
            "sale",
            "on",
            "for"
          ],
          "correct": [
            "on",
            "sale"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en5_d1",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Excuse me, where can I find fresh milk?",
        "zh": "打扰一下，在哪儿能找到鲜牛奶？",
        "phoneticHtml": "Excuse me, where <span class='linking'>can‿I</span> find fresh milk?",
        "linkingNotes": [
          "can I 连读成 /kə-naɪ/；find fresh 的 d 失去爆破。"
        ]
      },
      {
        "id": "en5_d2",
        "speaker": "B",
        "speakerName": "Staff",
        "role": "店员",
        "en": "It's at the back of the store, next to the eggs.",
        "zh": "在商店最里面，鸡蛋旁边。",
        "phoneticHtml": "<span class='linking'>It's‿at</span> the <span class='linking'>back‿of</span> the store, <span class='linking'>next‿to</span> the eggs.",
        "linkingNotes": [
          "It's at 连读；back of 连读成 /bæ-kəv/；next to 的 t 只发一次。"
        ]
      },
      {
        "id": "en5_d3",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Is it far from here?",
        "zh": "离这儿远吗？",
        "phoneticHtml": "<span class='linking'>Is‿it</span> far from here?",
        "linkingNotes": [
          "Is it 连读成 /ɪ-zɪt/；from 弱读为 /frəm/。"
        ]
      },
      {
        "id": "en5_d4",
        "speaker": "B",
        "speakerName": "Staff",
        "role": "店员",
        "en": "Not far. Go straight and turn left.",
        "zh": "不远。直走然后左转。",
        "phoneticHtml": "Not far. Go <span class='linking'>straight‿and</span> turn left.",
        "linkingNotes": [
          "straight and 连读，and 弱读为 /ən/。"
        ]
      },
      {
        "id": "en5_d5",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Thanks. Is the bread on sale today?",
        "zh": "谢谢。今天面包打折吗？",
        "phoneticHtml": "Thanks. Is the <span class='linking'>bread‿on</span> sale today?",
        "linkingNotes": [
          "bread on 连读成 /bre-dɑn/。"
        ]
      },
      {
        "id": "en5_d6",
        "speaker": "B",
        "speakerName": "Staff",
        "role": "店员",
        "en": "Yes, it's half price until tomorrow.",
        "zh": "是的，半价到明天为止。",
        "phoneticHtml": "Yes, it's half price until tomorrow.",
        "linkingNotes": [
          "half price 的 f 和 p 衔接紧凑，中间不停顿。"
        ]
      },
      {
        "id": "en5_d7",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Great. Can I pay by card at the front?",
        "zh": "太好了。可以在前面刷卡付款吗？",
        "phoneticHtml": "Great. <span class='linking'>Can‿I</span> pay by card at the front?",
        "linkingNotes": [
          "Can I 连读；card at 连读成 /kɑr-dæt/。"
        ]
      },
      {
        "id": "en5_d8",
        "speaker": "B",
        "speakerName": "Staff",
        "role": "店员",
        "en": "Sure. If the line is long, don't worry. Use the machine by the door.",
        "zh": "可以。如果排队很长，别担心，用门边的机器就行。",
        "phoneticHtml": "Sure. If the <span class='linking'>line‿is</span> long, don't worry. Use the machine by the door.",
        "linkingNotes": [
          "line is 连读成 /laɪ-nɪz/；don't worry 的 t 失去爆破。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (顾客)",
      "description": "向超市店员询问鲜牛奶的位置和路线，确认打折和付款方式。"
    },
    "vocabulary": [
      {
        "id": "en5_v1",
        "word": "find",
        "phonetic": "/faɪnd/",
        "pos": "v.",
        "meaning": "找到",
        "audio": "audio/en_vocab/en5_v1.mp3",
        "example": "Excuse me, where can I find fresh milk?",
        "exampleZh": "打扰一下，在哪儿能找到鲜牛奶？",
        "forms": [
          "find"
        ]
      },
      {
        "id": "en5_v2",
        "word": "fresh",
        "phonetic": "/freʃ/",
        "pos": "adj.",
        "meaning": "新鲜的",
        "audio": "audio/en_vocab/en5_v2.mp3",
        "example": "Excuse me, where can I find fresh milk?",
        "exampleZh": "打扰一下，在哪儿能找到鲜牛奶？",
        "forms": [
          "fresh"
        ]
      },
      {
        "id": "en5_v3",
        "word": "sale",
        "phonetic": "/seɪl/",
        "pos": "n.",
        "meaning": "促销；打折",
        "audio": "audio/en_vocab/en5_v3.mp3",
        "example": "Thanks. Is the bread on sale today?",
        "exampleZh": "谢谢。今天面包打折吗？",
        "forms": [
          "sale"
        ]
      },
      {
        "id": "en5_v4",
        "word": "turn",
        "phonetic": "/tɜːrn/",
        "pos": "v.",
        "meaning": "转弯",
        "audio": "audio/en_vocab/en5_v4.mp3",
        "example": "Not far. Go straight and turn left.",
        "exampleZh": "不远。直走然后左转。",
        "forms": [
          "turn"
        ]
      },
      {
        "id": "en5_v5",
        "word": "left",
        "phonetic": "/left/",
        "pos": "adv./adj.",
        "meaning": "向左；剩下的",
        "audio": "audio/en_vocab/en5_v5.mp3",
        "example": "Not far. Go straight and turn left.",
        "exampleZh": "不远。直走然后左转。",
        "forms": [
          "left"
        ]
      },
      {
        "id": "en5_v6",
        "word": "tomorrow",
        "phonetic": "/təˈmɑːroʊ/",
        "pos": "n./adv.",
        "meaning": "明天",
        "audio": "audio/en_vocab/en5_v6.mp3",
        "example": "Yes, it's half price until tomorrow.",
        "exampleZh": "是的，半价到明天为止。",
        "forms": [
          "tomorrow"
        ]
      }
    ],
    "topicWords": [],
    "properNouns": []
  },
  {
    "id": "en6",
    "level": 2,
    "title": "Weekend Catch-up",
    "titleZh": "周末邀约与看展协商",
    "situation": "约朋友周六去看新开的艺术展，商量先吃午饭、见面时间和地点。",
    "icon": "🎨",
    "tags": [
      "社交闲聊",
      "时间协商",
      "口语同化"
    ],
    "chunks": [
      {
        "id": "en6_c1",
        "text": "Are you free this weekend?",
        "meaning": "你这周末有空吗？",
        "phonetic": "/ɑːr ju friː ðɪs ˈwiːkend/",
        "usageTip": "约人最常用的开场白。free 在这里是“有空的”，不是“免费的”。",
        "warmupQuiz": {
          "prompt": "组装短语：“你这周末有空吗？”",
          "tokens": [
            "this weekend",
            "Are you",
            "free",
            "late"
          ],
          "correct": [
            "Are you",
            "free",
            "this weekend"
          ]
        }
      },
      {
        "id": "en6_c2",
        "text": "Sounds like a plan!",
        "meaning": "好主意，就这么定了！",
        "phonetic": "/saʊndz laɪk ə plæn/",
        "usageTip": "同意别人提议的地道说法，比 OK 更有热情。like a 连读。",
        "warmupQuiz": {
          "prompt": "组装短语：“就这么定了！”",
          "tokens": [
            "a plan",
            "Sounds",
            "like",
            "idea"
          ],
          "correct": [
            "Sounds",
            "like",
            "a plan"
          ]
        }
      },
      {
        "id": "en6_c3",
        "text": "Where should we meet?",
        "meaning": "我们在哪儿见面？",
        "phonetic": "/wer ʃʊd wi miːt/",
        "usageTip": "should 弱读为 /ʃəd/。也可以问 What time should we meet?",
        "warmupQuiz": {
          "prompt": "组装短语：“我们在哪儿见面？”",
          "tokens": [
            "we meet",
            "Where",
            "should",
            "start"
          ],
          "correct": [
            "Where",
            "should",
            "we meet"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en6_d1",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "Hey Emma, are you free this weekend?",
        "zh": "Emma，这周末有空吗？",
        "phoneticHtml": "Hey Emma, <span class='linking'>are‿you</span> free this weekend?",
        "linkingNotes": [
          "are you 连读成 /ɑr-ju/。"
        ]
      },
      {
        "id": "en6_d2",
        "speaker": "B",
        "speakerName": "Emma",
        "role": "朋友",
        "en": "I'm free on Saturday. What's the plan?",
        "zh": "我周六有空。有什么计划？",
        "phoneticHtml": "I'm <span class='linking'>free‿on</span> Saturday. What's the plan?",
        "linkingNotes": [
          "free on 之间带轻微 /j/ 过渡。"
        ]
      },
      {
        "id": "en6_d3",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "There's a new art show near the park. It starts at two.",
        "zh": "公园附近有个新的艺术展，两点开始。",
        "phoneticHtml": "<span class='linking'>There's‿a</span> new art show near the park. It <span class='linking'>starts‿at</span> two.",
        "linkingNotes": [
          "There's a 连读成 /ðer-zə/；starts at 连读。"
        ]
      },
      {
        "id": "en6_d4",
        "speaker": "B",
        "speakerName": "Emma",
        "role": "朋友",
        "en": "Sounds like a plan! Let's get lunch before it starts.",
        "zh": "好主意！开始前我们先吃午饭吧。",
        "phoneticHtml": "Sounds <span class='linking'>like‿a</span> plan! Let's get lunch <span class='linking'>before‿it</span> starts.",
        "linkingNotes": [
          "like a 连读成 /laɪ-kə/；before it 连读。"
        ]
      },
      {
        "id": "en6_d5",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "Good idea. I know a place with great sandwiches, and the price is good.",
        "zh": "好主意。我知道一家三明治很棒的店，价格也不贵。",
        "phoneticHtml": "Good idea. I <span class='linking'>know‿a</span> place with great sandwiches, and the <span class='linking'>price‿is</span> good.",
        "linkingNotes": [
          "know a 之间带轻微 /w/ 过渡；price is 连读。"
        ]
      },
      {
        "id": "en6_d6",
        "speaker": "B",
        "speakerName": "Emma",
        "role": "朋友",
        "en": "Perfect. Where should we meet?",
        "zh": "太好了。我们在哪儿见面？",
        "phoneticHtml": "Perfect. Where should we meet?",
        "linkingNotes": [
          "should 弱读为 /ʃəd/。"
        ]
      },
      {
        "id": "en6_d7",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "Let's meet at the train station at twelve. Don't be late!",
        "zh": "十二点在火车站见吧。别迟到！",
        "phoneticHtml": "Let's <span class='linking'>meet‿at</span> the train station at twelve. Don't be late!",
        "linkingNotes": [
          "meet at 连读，t 弱化成闪音：/miː-dæt/。"
        ]
      },
      {
        "id": "en6_d8",
        "speaker": "B",
        "speakerName": "Emma",
        "role": "朋友",
        "en": "No problem. Don't worry, I'll be there early. See you tomorrow!",
        "zh": "没问题。别担心，我会早点到。明天见！",
        "phoneticHtml": "No problem. Don't worry, I'll be there early. See you tomorrow!",
        "linkingNotes": [
          "Don't worry 的 t 失去爆破；there early 连读成 /ðe-rɜːrli/。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (你)",
      "description": "向好友发出看展邀约，商榷集合时间并达成共识。"
    },
    "vocabulary": [
      {
        "id": "en6_v1",
        "word": "free",
        "phonetic": "/friː/",
        "pos": "adj.",
        "meaning": "有空的；免费的",
        "audio": "audio/en_vocab/en6_v1.mp3",
        "example": "Hey Emma, are you free this weekend?",
        "exampleZh": "Emma，这周末有空吗？",
        "forms": [
          "free"
        ]
      },
      {
        "id": "en6_v2",
        "word": "weekend",
        "phonetic": "/ˈwiːkend/",
        "pos": "n.",
        "meaning": "周末",
        "audio": "audio/en_vocab/en6_v2.mp3",
        "example": "Hey Emma, are you free this weekend?",
        "exampleZh": "Emma，这周末有空吗？",
        "forms": [
          "weekend"
        ]
      },
      {
        "id": "en6_v3",
        "word": "plan",
        "phonetic": "/plæn/",
        "pos": "n.",
        "meaning": "计划",
        "audio": "audio/en_vocab/en6_v3.mp3",
        "example": "I'm free on Saturday. What's the plan?",
        "exampleZh": "我周六有空。有什么计划？",
        "forms": [
          "plan"
        ]
      },
      {
        "id": "en6_v4",
        "word": "meet",
        "phonetic": "/miːt/",
        "pos": "v.",
        "meaning": "见面",
        "audio": "audio/en_vocab/en6_v4.mp3",
        "example": "Perfect. Where should we meet?",
        "exampleZh": "太好了。我们在哪儿见面？",
        "forms": [
          "meet"
        ]
      },
      {
        "id": "en6_v5",
        "word": "early",
        "phonetic": "/ˈɜːrli/",
        "pos": "adj./adv.",
        "meaning": "早的；提早",
        "audio": "audio/en_vocab/en6_v5.mp3",
        "example": "No problem. Don't worry, I'll be there early. See you tomorrow!",
        "exampleZh": "没问题。别担心，我会早点到。明天见！",
        "forms": [
          "early"
        ]
      },
      {
        "id": "en6_v6",
        "word": "place",
        "phonetic": "/pleɪs/",
        "pos": "n.",
        "meaning": "地方；店",
        "audio": "audio/en_vocab/en6_v6.mp3",
        "example": "Good idea. I know a place with great sandwiches, and the price is good.",
        "exampleZh": "好主意。我知道一家三明治很棒的店，价格也不贵。",
        "forms": [
          "place"
        ]
      }
    ],
    "topicWords": [],
    "properNouns": [
      "Saturday"
    ]
  },
  {
    "id": "en7",
    "level": 2,
    "title": "Hotel Check-in",
    "titleZh": "酒店入住与前台咨询",
    "situation": "到酒店前台办理入住，拿房卡，问早餐、付款方式和能吃午饭的安静地方。",
    "icon": "🏨",
    "tags": [
      "海外差旅",
      "酒店沟通",
      "核心服务"
    ],
    "chunks": [
      {
        "id": "en7_c1",
        "text": "I'd like to check in.",
        "meaning": "我想办理入住。",
        "phonetic": "/aɪd laɪk tə tʃek ɪn/",
        "usageTip": "check in 连读成 /tʃe-kɪn/。退房是 check out。",
        "warmupQuiz": {
          "prompt": "组装短语：“我想办理入住。”",
          "tokens": [
            "check in",
            "I'd like",
            "to",
            "stay"
          ],
          "correct": [
            "I'd like",
            "to",
            "check in"
          ]
        }
      },
      {
        "id": "en7_c2",
        "text": "Is breakfast free?",
        "meaning": "早餐免费吗？",
        "phonetic": "/ɪz ˈbrekfəst friː/",
        "usageTip": "free 表示“免费的”。也可以问 Is breakfast included?",
        "warmupQuiz": {
          "prompt": "组装短语：“早餐免费吗？”",
          "tokens": [
            "free",
            "Is",
            "breakfast",
            "room"
          ],
          "correct": [
            "Is",
            "breakfast",
            "free"
          ]
        }
      },
      {
        "id": "en7_c3",
        "text": "Enjoy your stay!",
        "meaning": "祝您入住愉快！",
        "phonetic": "/ɪnˈdʒɔɪ jər steɪ/",
        "usageTip": "酒店前台的标准结束语。your 弱读为 /jər/。",
        "warmupQuiz": {
          "prompt": "组装短语：“祝您入住愉快！”",
          "tokens": [
            "your stay",
            "Enjoy",
            "room"
          ],
          "correct": [
            "Enjoy",
            "your stay"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en7_d1",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "住客 (你)",
        "en": "Good afternoon. I'd like to check in. My name is Alex Taylor.",
        "zh": "下午好，我想办理入住。我叫 Alex Taylor。",
        "phoneticHtml": "Good afternoon. I'd like <span class='reduction'>to</span> <span class='linking'>check‿in</span>. My <span class='linking'>name‿is</span> Alex Taylor.",
        "linkingNotes": [
          "check in 连读成 /tʃe-kɪn/；name is 连读成 /neɪ-mɪz/。"
        ]
      },
      {
        "id": "en7_d2",
        "speaker": "B",
        "speakerName": "Front Desk",
        "role": "前台",
        "en": "Welcome! You're a little early, but your room is ready.",
        "zh": "欢迎！您来得有点早，不过房间已经准备好了。",
        "phoneticHtml": "Welcome! <span class='linking'>You're‿a</span> little early, but your <span class='linking'>room‿is</span> ready.",
        "linkingNotes": [
          "You're a 连读；room is 连读成 /ruː-mɪz/。"
        ]
      },
      {
        "id": "en7_d3",
        "speaker": "B",
        "speakerName": "Front Desk",
        "role": "前台",
        "en": "Here is your key card. You're on the fifth floor.",
        "zh": "这是您的房卡。您在五楼。",
        "phoneticHtml": "<span class='linking'>Here‿is</span> your key card. <span class='linking'>You're‿on</span> the fifth floor.",
        "linkingNotes": [
          "Here is 连读成 /hɪ-rɪz/；You're on 连读。"
        ]
      },
      {
        "id": "en7_d4",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "住客 (你)",
        "en": "Thanks. Is breakfast free? And can I pay by card when I leave?",
        "zh": "谢谢。早餐免费吗？退房时可以刷卡付款吗？",
        "phoneticHtml": "Thanks. Is breakfast free? And <span class='reduction'>can</span> I pay by card when I leave?",
        "linkingNotes": [
          "breakfast 中 k 和 f 衔接紧凑；can 弱读为 /kən/。"
        ]
      },
      {
        "id": "en7_d5",
        "speaker": "B",
        "speakerName": "Front Desk",
        "role": "前台",
        "en": "Yes, breakfast is free. It starts at seven tomorrow. And yes, you can pay by card.",
        "zh": "是的，早餐免费，明天早上七点开始。可以刷卡付款。",
        "phoneticHtml": "Yes, <span class='linking'>breakfast‿is</span> free. It <span class='linking'>starts‿at</span> seven tomorrow. And yes, you <span class='reduction'>can</span> pay by card.",
        "linkingNotes": [
          "breakfast is 连读；starts at 连读成 /stɑr-tsæt/。"
        ]
      },
      {
        "id": "en7_d6",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "住客 (你)",
        "en": "Is there a quiet place to have lunch and meet a friend?",
        "zh": "有没有安静的地方可以吃午饭、见朋友？",
        "phoneticHtml": "Is <span class='linking'>there‿a</span> quiet place <span class='reduction'>to</span> have lunch and <span class='linking'>meet‿a</span> friend?",
        "linkingNotes": [
          "there a 连读；meet a 连读，t 弱化成闪音。"
        ]
      },
      {
        "id": "en7_d7",
        "speaker": "B",
        "speakerName": "Front Desk",
        "role": "前台",
        "en": "Yes, the cafe on the first floor. Turn left after the elevator, and you'll find it. Enjoy your stay!",
        "zh": "有，一楼的咖啡馆。出电梯左转就能找到。祝您入住愉快！",
        "phoneticHtml": "Yes, the <span class='linking'>cafe‿on</span> the first floor. Turn <span class='linking'>left‿after</span> the elevator, and you'll <span class='linking'>find‿it</span>. Enjoy your stay!",
        "linkingNotes": [
          "cafe on 之间带轻微 /j/ 过渡；left after 连读；find it 连读成 /faɪn-dɪt/。"
        ]
      },
      {
        "id": "en7_d8",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "住客 (你)",
        "en": "Perfect. Thank you so much!",
        "zh": "太好了，非常感谢！",
        "phoneticHtml": "Perfect. <span class='linking'>Thank‿you</span> so much!",
        "linkingNotes": [
          "Thank you 连读成 /θæŋ-kju/。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (住客)",
      "description": "在前台报出姓名办理入住，拿到房卡，问清早餐、付款方式和能见朋友的地方。"
    },
    "vocabulary": [
      {
        "id": "en7_v1",
        "word": "room",
        "phonetic": "/ruːm/",
        "pos": "n.",
        "meaning": "房间；空间",
        "audio": "audio/en_vocab/en7_v1.mp3",
        "example": "Welcome! You're a little early, but your room is ready.",
        "exampleZh": "欢迎！您来得有点早，不过房间已经准备好了。",
        "forms": [
          "room"
        ]
      },
      {
        "id": "en7_v2",
        "word": "key",
        "phonetic": "/kiː/",
        "pos": "n.",
        "meaning": "钥匙",
        "audio": "audio/en_vocab/en7_v2.mp3",
        "example": "Here is your key card. You're on the fifth floor.",
        "exampleZh": "这是您的房卡。您在五楼。",
        "forms": [
          "key",
          "keys"
        ]
      },
      {
        "id": "en7_v3",
        "word": "floor",
        "phonetic": "/flɔːr/",
        "pos": "n.",
        "meaning": "楼层；地面",
        "audio": "audio/en_vocab/en7_v3.mp3",
        "example": "Here is your key card. You're on the fifth floor.",
        "exampleZh": "这是您的房卡。您在五楼。",
        "forms": [
          "floor"
        ]
      },
      {
        "id": "en7_v4",
        "word": "breakfast",
        "phonetic": "/ˈbrekfəst/",
        "pos": "n.",
        "meaning": "早餐",
        "audio": "audio/en_vocab/en7_v4.mp3",
        "example": "Thanks. Is breakfast free? And can I pay by card when I leave?",
        "exampleZh": "谢谢。早餐免费吗？退房时可以刷卡付款吗？",
        "forms": [
          "breakfast"
        ]
      },
      {
        "id": "en7_v5",
        "word": "stay",
        "phonetic": "/steɪ/",
        "pos": "n./v.",
        "meaning": "停留，入住；保持",
        "audio": "audio/en_vocab/en7_v5.mp3",
        "example": "Yes, the cafe on the first floor. Turn left after the elevator, and you'll find it. Enjoy your stay!",
        "exampleZh": "有，一楼的咖啡馆。出电梯左转就能找到。祝您入住愉快！",
        "forms": [
          "stay"
        ]
      },
      {
        "id": "en7_v6",
        "word": "quiet",
        "phonetic": "/ˈkwaɪət/",
        "pos": "adj.",
        "meaning": "安静的",
        "audio": "audio/en_vocab/en7_v6.mp3",
        "example": "Is there a quiet place to have lunch and meet a friend?",
        "exampleZh": "有没有安静的地方可以吃午饭、见朋友？",
        "forms": [
          "quiet"
        ]
      }
    ],
    "topicWords": [],
    "properNouns": [
      "Taylor"
    ]
  },
  {
    "id": "en8",
    "level": 2,
    "title": "Returning an Item",
    "titleZh": "服装店尺码换退",
    "situation": "上周末买的外套小了一号，拿着小票去店里换大号，并要求先试穿。",
    "icon": "🧥",
    "tags": [
      "售后维权",
      "尺码沟通",
      "礼貌协商"
    ],
    "chunks": [
      {
        "id": "en8_c1",
        "text": "It doesn't fit.",
        "meaning": "不合身。",
        "phonetic": "/ɪt ˈdʌzənt fɪt/",
        "usageTip": "fit 指尺寸合不合身；suit 指款式、颜色适不适合。",
        "warmupQuiz": {
          "prompt": "组装短语：“不合身。”",
          "tokens": [
            "fit",
            "It",
            "doesn't",
            "size"
          ],
          "correct": [
            "It",
            "doesn't",
            "fit"
          ]
        }
      },
      {
        "id": "en8_c2",
        "text": "Can I change it for...",
        "meaning": "能把它换成……吗？",
        "phonetic": "/kən aɪ tʃeɪndʒ ɪt fər/",
        "usageTip": "change A for B：用 A 换 B。也可以说 exchange it for...",
        "warmupQuiz": {
          "prompt": "组装短语：“能把它换成……吗？”",
          "tokens": [
            "change it",
            "Can I",
            "for",
            "try"
          ],
          "correct": [
            "Can I",
            "change it",
            "for"
          ]
        }
      },
      {
        "id": "en8_c3",
        "text": "try it on",
        "meaning": "试穿一下",
        "phonetic": "/traɪ ɪt ɑːn/",
        "usageTip": "代词 it 必须放在 try 和 on 中间，不能说 try on it。三个词连读。",
        "warmupQuiz": {
          "prompt": "组装短语：“试穿一下”",
          "tokens": [
            "on",
            "try",
            "it",
            "fit"
          ],
          "correct": [
            "try",
            "it",
            "on"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en8_d1",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Hi. I bought this jacket last weekend, but it doesn't fit.",
        "zh": "你好，我上周末买了这件夹克，但是不合身。",
        "phoneticHtml": "Hi. I bought this jacket last weekend, <span class='linking'>but‿it</span> doesn't fit.",
        "linkingNotes": [
          "but it 连读，t 弱化成闪音：/bʌ-dɪt/。"
        ]
      },
      {
        "id": "en8_d2",
        "speaker": "B",
        "speakerName": "Staff",
        "role": "店员",
        "en": "I'm sorry to hear that. Is it too big or too small?",
        "zh": "很抱歉。是太大还是太小？",
        "phoneticHtml": "I'm sorry <span class='reduction'>to</span> hear that. <span class='linking'>Is‿it</span> too <span class='linking'>big‿or</span> too small?",
        "linkingNotes": [
          "Is it 连读；big or 连读成 /bɪ-ɡɔːr/。"
        ]
      },
      {
        "id": "en8_d3",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "It's too small. Can I change it for a bigger size?",
        "zh": "太小了。能换大一号吗？",
        "phoneticHtml": "It's too small. <span class='linking'>Can‿I</span> <span class='linking'>change‿it</span> <span class='linking'>for‿a</span> bigger size?",
        "linkingNotes": [
          "change it 连读成 /tʃeɪn-dʒɪt/；for a 连读成 /fə-rə/。"
        ]
      },
      {
        "id": "en8_d4",
        "speaker": "B",
        "speakerName": "Staff",
        "role": "店员",
        "en": "Sure. Do you have the receipt?",
        "zh": "可以。您带小票了吗？",
        "phoneticHtml": "Sure. Do you have the receipt?",
        "linkingNotes": [
          "receipt 的 p 不发音：/rɪˈsiːt/。"
        ]
      },
      {
        "id": "en8_d5",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Yes, here it is. I got it on sale.",
        "zh": "带了，在这儿。我是打折时买的。",
        "phoneticHtml": "Yes, <span class='linking'>here‿it‿is</span>. I <span class='linking'>got‿it‿on</span> sale.",
        "linkingNotes": [
          "here it is 连读成 /hɪ-rɪ-dɪz/；got it on 连读成 /ɡɑ-dɪ-dɑn/。"
        ]
      },
      {
        "id": "en8_d6",
        "speaker": "B",
        "speakerName": "Staff",
        "role": "店员",
        "en": "That's fine. Let me find a large for you. There's only one left.",
        "zh": "没关系。我帮您找一件大号的。只剩一件了。",
        "phoneticHtml": "That's fine. Let me <span class='linking'>find‿a</span> large for you. There's only one left.",
        "linkingNotes": [
          "find a 连读成 /faɪn-də/；only one 之间不停顿。"
        ]
      },
      {
        "id": "en8_d7",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "顾客 (你)",
        "en": "Thank you. Is there a place to try it on?",
        "zh": "谢谢。有地方可以试穿吗？",
        "phoneticHtml": "Thank you. Is <span class='linking'>there‿a</span> place <span class='reduction'>to</span> <span class='linking'>try‿it‿on</span>?",
        "linkingNotes": [
          "try it on 连读成 /traɪ-jɪ-dɑn/。"
        ]
      },
      {
        "id": "en8_d8",
        "speaker": "B",
        "speakerName": "Staff",
        "role": "店员",
        "en": "Of course. Turn left, and the first room is free. Take your time.",
        "zh": "当然。左转，第一间试衣间空着。您慢慢来。",
        "phoneticHtml": "Of course. Turn left, and the first <span class='linking'>room‿is</span> free. Take your time.",
        "linkingNotes": [
          "room is 连读；Take your 的 k 和 y 衔接紧凑。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (顾客)",
      "description": "向店员说明换大号外套的需求，出示小票并完成调换。"
    },
    "vocabulary": [
      {
        "id": "en8_v1",
        "word": "fit",
        "phonetic": "/fɪt/",
        "pos": "v.",
        "meaning": "（尺寸）合身",
        "audio": "audio/en_vocab/en8_v1.mp3",
        "example": "Hi. I bought this jacket last weekend, but it doesn't fit.",
        "exampleZh": "你好，我上周末买了这件夹克，但是不合身。",
        "forms": [
          "fit"
        ]
      },
      {
        "id": "en8_v2",
        "word": "size",
        "phonetic": "/saɪz/",
        "pos": "n.",
        "meaning": "尺码",
        "audio": "audio/en_vocab/en8_v2.mp3",
        "example": "It's too small. Can I change it for a bigger size?",
        "exampleZh": "太小了。能换大一号吗？",
        "forms": [
          "size"
        ]
      },
      {
        "id": "en8_v3",
        "word": "large",
        "phonetic": "/lɑːrdʒ/",
        "pos": "adj./n.",
        "meaning": "大的；大号",
        "audio": "audio/en_vocab/en8_v3.mp3",
        "example": "That's fine. Let me find a large for you. There's only one left.",
        "exampleZh": "没关系。我帮您找一件大号的。只剩一件了。",
        "forms": [
          "large"
        ]
      },
      {
        "id": "en8_v4",
        "word": "try",
        "phonetic": "/traɪ/",
        "pos": "v.",
        "meaning": "尝试；试穿",
        "audio": "audio/en_vocab/en8_v4.mp3",
        "example": "Thank you. Is there a place to try it on?",
        "exampleZh": "谢谢。有地方可以试穿吗？",
        "forms": [
          "try"
        ]
      },
      {
        "id": "en8_v5",
        "word": "last",
        "phonetic": "/læst/",
        "pos": "adj.",
        "meaning": "上一个的；最近的",
        "audio": "audio/en_vocab/en8_v5.mp3",
        "example": "Hi. I bought this jacket last weekend, but it doesn't fit.",
        "exampleZh": "你好，我上周末买了这件夹克，但是不合身。",
        "forms": [
          "last"
        ]
      },
      {
        "id": "en8_v6",
        "word": "only",
        "phonetic": "/ˈoʊnli/",
        "pos": "adv.",
        "meaning": "只，仅仅",
        "audio": "audio/en_vocab/en8_v6.mp3",
        "example": "That's fine. Let me find a large for you. There's only one left.",
        "exampleZh": "没关系。我帮您找一件大号的。只剩一件了。",
        "forms": [
          "only"
        ]
      }
    ],
    "topicWords": [
      {
        "id": "en8_t1",
        "word": "jacket",
        "phonetic": "/ˈdʒækɪt/",
        "pos": "n.",
        "meaning": "夹克，外套",
        "audio": "audio/en_vocab/en8_t1.mp3",
        "example": "Hi. I bought this jacket last weekend, but it doesn't fit.",
        "exampleZh": "你好，我上周末买了这件夹克，但是不合身。",
        "forms": [
          "jacket"
        ]
      },
      {
        "id": "en8_t2",
        "word": "receipt",
        "phonetic": "/rɪˈsiːt/",
        "pos": "n.",
        "meaning": "收据，小票",
        "audio": "audio/en_vocab/en8_t2.mp3",
        "example": "Sure. Do you have the receipt?",
        "exampleZh": "可以。您带小票了吗？",
        "forms": [
          "receipt"
        ]
      }
    ],
    "properNouns": []
  },
  {
    "id": "en9",
    "level": 3,
    "title": "Asking for a Hand",
    "titleZh": "即时求助与感激致谢",
    "situation": "搬一个很重的箱子到车上，请路人搭把手，途中休息一下，最后真诚道谢。",
    "icon": "🤝",
    "tags": [
      "即时求助",
      "礼貌委婉",
      "浊化同化"
    ],
    "chunks": [
      {
        "id": "en9_c1",
        "text": "Could you give me a hand?",
        "meaning": "能帮我一下吗？",
        "phonetic": "/kʊd ju ɡɪv mi ə hænd/",
        "usageTip": "give me a hand = help me，多指需要动手的帮忙。Could you 同化为 /kʊ-dʒu/。",
        "warmupQuiz": {
          "prompt": "组装短语：“能帮我一下吗？”",
          "tokens": [
            "a hand",
            "Could you",
            "give me",
            "mind"
          ],
          "correct": [
            "Could you",
            "give me",
            "a hand"
          ]
        }
      },
      {
        "id": "en9_c2",
        "text": "Do you mind if...",
        "meaning": "你介意……吗？",
        "phonetic": "/du ju maɪnd ɪf/",
        "usageTip": "注意回答：不介意要说 Not at all / No, go ahead，不是 Yes。",
        "warmupQuiz": {
          "prompt": "组装短语：“你介意……吗？”",
          "tokens": [
            "mind if",
            "Do you",
            "carry"
          ],
          "correct": [
            "Do you",
            "mind if"
          ]
        }
      },
      {
        "id": "en9_c3",
        "text": "I really appreciate it!",
        "meaning": "真的非常感谢！",
        "phonetic": "/aɪ ˈriːəli əˈpriːʃieɪt ɪt/",
        "usageTip": "比 Thank you 更郑重。appreciate it 连读，t 弱化成闪音。",
        "warmupQuiz": {
          "prompt": "组装短语：“真的非常感谢！”",
          "tokens": [
            "appreciate it",
            "I",
            "really",
            "careful"
          ],
          "correct": [
            "I",
            "really",
            "appreciate it"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en9_d1",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "Excuse me, could you give me a hand? This box is really heavy.",
        "zh": "打扰一下，能帮我一下吗？这个箱子很重。",
        "phoneticHtml": "Excuse me, <span class='linking'>could‿you</span> give <span class='linking'>me‿a</span> hand? This <span class='linking'>box‿is</span> really heavy.",
        "linkingNotes": [
          "could you 同化为 /kʊ-dʒu/；me a 连读；box is 连读成 /bɑk-sɪz/。"
        ]
      },
      {
        "id": "en9_d2",
        "speaker": "B",
        "speakerName": "Passerby",
        "role": "路人",
        "en": "Sure. Where do you need to carry it?",
        "zh": "当然。要搬到哪儿？",
        "phoneticHtml": "Sure. Where do you <span class='linking'>need‿to</span> <span class='linking'>carry‿it</span>?",
        "linkingNotes": [
          "need to 的 d 只做口型；carry it 连读成 /kæ-ri-jɪt/。"
        ]
      },
      {
        "id": "en9_d3",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "Just to my car over there. It's not far.",
        "zh": "就到那边我的车上。不远。",
        "phoneticHtml": "<span class='linking'>Just‿to</span> my car over there. It's not far.",
        "linkingNotes": [
          "Just to：t 只发一次；not far 的 t 失去爆破。"
        ]
      },
      {
        "id": "en9_d4",
        "speaker": "B",
        "speakerName": "Passerby",
        "role": "路人",
        "en": "OK, I'll take this side. Be careful, the floor is wet.",
        "zh": "好，我抬这边。小心，地面是湿的。",
        "phoneticHtml": "OK, I'll take this side. Be careful, the <span class='linking'>floor‿is</span> wet.",
        "linkingNotes": [
          "floor is 连读成 /flɔː-rɪz/。"
        ]
      },
      {
        "id": "en9_d5",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "Thanks. Do you mind if we stop for a second?",
        "zh": "谢谢。你介意我们停一下吗？",
        "phoneticHtml": "Thanks. Do you <span class='linking'>mind‿if</span> we stop <span class='linking'>for‿a</span> second?",
        "linkingNotes": [
          "mind if 连读成 /maɪn-dɪf/；for a 连读。"
        ]
      },
      {
        "id": "en9_d6",
        "speaker": "B",
        "speakerName": "Passerby",
        "role": "路人",
        "en": "Not at all. Do you have the key? I'll open the back.",
        "zh": "一点也不。你有钥匙吗？我来打开后备箱。",
        "phoneticHtml": "<span class='linking'>Not‿at‿all</span>. Do you have the key? I'll open the back.",
        "linkingNotes": [
          "Not at all 连读，t 弱化：/nɑ-də-dɔːl/。"
        ]
      },
      {
        "id": "en9_d7",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "Here it is. Good, there's room in the back. I really appreciate it!",
        "zh": "给你。太好了，后面放得下。真的非常感谢！",
        "phoneticHtml": "<span class='linking'>Here‿it‿is</span>. Good, there's <span class='linking'>room‿in</span> the back. I really <span class='linking'>appreciate‿it</span>!",
        "linkingNotes": [
          "room in 连读；appreciate it 连读，t 弱化成闪音。"
        ]
      },
      {
        "id": "en9_d8",
        "speaker": "B",
        "speakerName": "Passerby",
        "role": "路人",
        "en": "Glad to help. Nice to meet you, and have a good weekend!",
        "zh": "很高兴能帮上忙。认识你很高兴，周末愉快！",
        "phoneticHtml": "Glad <span class='reduction'>to</span> help. Nice <span class='reduction'>to</span> meet you, and <span class='linking'>have‿a</span> good weekend!",
        "linkingNotes": [
          "to 弱读为 /tə/；meet you 同化为 /miː-tʃu/；have a 连读。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (你)",
      "description": "搬重箱子时向路人求助，途中休息一下，最后真诚道谢。"
    },
    "vocabulary": [
      {
        "id": "en9_v1",
        "word": "heavy",
        "phonetic": "/ˈhevi/",
        "pos": "adj.",
        "meaning": "重的",
        "audio": "audio/en_vocab/en9_v1.mp3",
        "example": "Excuse me, could you give me a hand? This box is really heavy.",
        "exampleZh": "打扰一下，能帮我一下吗？这个箱子很重。",
        "forms": [
          "heavy"
        ]
      },
      {
        "id": "en9_v2",
        "word": "hand",
        "phonetic": "/hænd/",
        "pos": "n.",
        "meaning": "手；帮助",
        "audio": "audio/en_vocab/en9_v2.mp3",
        "example": "Excuse me, could you give me a hand? This box is really heavy.",
        "exampleZh": "打扰一下，能帮我一下吗？这个箱子很重。",
        "forms": [
          "hand"
        ]
      },
      {
        "id": "en9_v3",
        "word": "carry",
        "phonetic": "/ˈkæri/",
        "pos": "v.",
        "meaning": "搬，拿，携带",
        "audio": "audio/en_vocab/en9_v3.mp3",
        "example": "Sure. Where do you need to carry it?",
        "exampleZh": "当然。要搬到哪儿？",
        "forms": [
          "carry"
        ]
      },
      {
        "id": "en9_v4",
        "word": "careful",
        "phonetic": "/ˈkerfəl/",
        "pos": "adj.",
        "meaning": "小心的",
        "audio": "audio/en_vocab/en9_v4.mp3",
        "example": "OK, I'll take this side. Be careful, the floor is wet.",
        "exampleZh": "好，我抬这边。小心，地面是湿的。",
        "forms": [
          "careful"
        ]
      },
      {
        "id": "en9_v5",
        "word": "mind",
        "phonetic": "/maɪnd/",
        "pos": "v.",
        "meaning": "介意",
        "audio": "audio/en_vocab/en9_v5.mp3",
        "example": "Thanks. Do you mind if we stop for a second?",
        "exampleZh": "谢谢。你介意我们停一下吗？",
        "forms": [
          "mind"
        ]
      },
      {
        "id": "en9_v6",
        "word": "appreciate",
        "phonetic": "/əˈpriːʃieɪt/",
        "pos": "v.",
        "meaning": "感激",
        "audio": "audio/en_vocab/en9_v6.mp3",
        "example": "Here it is. Good, there's room in the back. I really appreciate it!",
        "exampleZh": "给你。太好了，后面放得下。真的非常感谢！",
        "forms": [
          "appreciate"
        ]
      }
    ],
    "topicWords": [],
    "properNouns": []
  },
  {
    "id": "en10",
    "level": 3,
    "title": "Weather Small Talk",
    "titleZh": "电梯天气与日常破冰",
    "situation": "在公司电梯里遇到同事，从多变的天气聊起，顺手把备用雨伞借给他。",
    "icon": "🌦️",
    "tags": [
      "职场破冰",
      "闲聊艺术",
      "自然语调"
    ],
    "chunks": [
      {
        "id": "en10_c1",
        "text": "It looks like rain.",
        "meaning": "看起来要下雨了。",
        "phonetic": "/ɪt lʊks laɪk reɪn/",
        "usageTip": "looks like + 名词：看起来像……。looks like 的 k 和 l 衔接紧凑。",
        "warmupQuiz": {
          "prompt": "组装短语：“看起来要下雨了。”",
          "tokens": [
            "rain",
            "It looks",
            "like",
            "warm"
          ],
          "correct": [
            "It looks",
            "like",
            "rain"
          ]
        }
      },
      {
        "id": "en10_c2",
        "text": "Did you bring...",
        "meaning": "你带……了吗？",
        "phonetic": "/dɪd ju brɪŋ/",
        "usageTip": "Did you 同化为 /dɪ-dʒu/，这是美式口语最常见的音变之一。",
        "warmupQuiz": {
          "prompt": "组装短语：“你带……了吗？”",
          "tokens": [
            "bring",
            "Did you",
            "forget"
          ],
          "correct": [
            "Did you",
            "bring"
          ]
        }
      },
      {
        "id": "en10_c3",
        "text": "Have a good one!",
        "meaning": "祝你愉快！（告别语）",
        "phonetic": "/hæv ə ɡʊd wʌn/",
        "usageTip": "万能告别语，一天中什么时候都能用。have a 连读成 /hæ-və/。",
        "warmupQuiz": {
          "prompt": "组装短语：“祝你愉快！”",
          "tokens": [
            "good one",
            "Have",
            "a",
            "day"
          ],
          "correct": [
            "Have",
            "a",
            "good one"
          ]
        }
      }
    ],
    "dialogue": [
      {
        "id": "en10_d1",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "Hi David. Strange weather today, right?",
        "zh": "嗨 David，今天天气好奇怪，对吧？",
        "phoneticHtml": "Hi David. Strange weather today, right?",
        "linkingNotes": [
          "Strange weather 中间不停顿；right 的 t 在句末轻读。"
        ]
      },
      {
        "id": "en10_d2",
        "speaker": "B",
        "speakerName": "David",
        "role": "同事",
        "en": "I know! It was warm this morning, and now it's cold.",
        "zh": "是啊！早上还挺暖和，现在就冷了。",
        "phoneticHtml": "I know! It was warm this morning, and <span class='linking'>now‿it's</span> cold.",
        "linkingNotes": [
          "now it's 之间带轻微 /w/ 过渡：/naʊ-wɪts/。"
        ]
      },
      {
        "id": "en10_d3",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "It looks like rain. Did you bring an umbrella?",
        "zh": "看起来要下雨了。你带伞了吗？",
        "phoneticHtml": "It looks like rain. <span class='linking'>Did‿you</span> <span class='linking'>bring‿an</span> umbrella?",
        "linkingNotes": [
          "Did you 同化为 /dɪ-dʒu/；bring an 连读成 /brɪŋ-ən/。"
        ]
      },
      {
        "id": "en10_d4",
        "speaker": "B",
        "speakerName": "David",
        "role": "同事",
        "en": "No, I forgot it at home, with my keys!",
        "zh": "没带，我把伞和钥匙都忘在家里了！",
        "phoneticHtml": "No, I <span class='linking'>forgot‿it‿at</span> home, with my keys!",
        "linkingNotes": [
          "forgot it at 连读，t 弱化成闪音：/fər-ɡɑ-dɪ-dæt/。"
        ]
      },
      {
        "id": "en10_d5",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "I always keep an extra one in my bag. You can take it.",
        "zh": "我包里一直放着一把备用的，你拿去用吧。",
        "phoneticHtml": "I always <span class='linking'>keep‿an</span> extra <span class='linking'>one‿in</span> my bag. You can <span class='linking'>take‿it</span>.",
        "linkingNotes": [
          "keep an 连读；one in 连读；take it 连读成 /teɪ-kɪt/。"
        ]
      },
      {
        "id": "en10_d6",
        "speaker": "B",
        "speakerName": "David",
        "role": "同事",
        "en": "Really? Thanks! I'll give it back tomorrow.",
        "zh": "真的吗？谢谢！我明天还给你。",
        "phoneticHtml": "Really? Thanks! I'll <span class='linking'>give‿it</span> back tomorrow.",
        "linkingNotes": [
          "give it 连读成 /ɡɪ-vɪt/。"
        ]
      },
      {
        "id": "en10_d7",
        "speaker": "A",
        "speakerName": "Alex",
        "role": "你",
        "en": "No problem. Oh, this is my floor. Be careful on the way home!",
        "zh": "不客气。哦，我到楼层了。回家路上小心！",
        "phoneticHtml": "No problem. Oh, <span class='linking'>this‿is</span> my floor. Be <span class='linking'>careful‿on</span> the way home!",
        "linkingNotes": [
          "this is 连读成 /ðɪ-sɪz/；careful on 连读。"
        ]
      },
      {
        "id": "en10_d8",
        "speaker": "B",
        "speakerName": "David",
        "role": "同事",
        "en": "You too. Stay warm and stay dry. Have a good one!",
        "zh": "你也是。注意保暖，别淋湿了。祝你愉快！",
        "phoneticHtml": "You too. Stay warm and stay dry. <span class='linking'>Have‿a</span> good one!",
        "linkingNotes": [
          "and 弱读为 /ən/；Have a 连读成 /hæ-və/。"
        ]
      }
    ],
    "rolePlay": {
      "userRole": "A",
      "targetRoleName": "Alex (你)",
      "description": "在电梯与同事就天气展开破冰闲聊，自然道别。"
    },
    "vocabulary": [
      {
        "id": "en10_v1",
        "word": "weather",
        "phonetic": "/ˈweðər/",
        "pos": "n.",
        "meaning": "天气",
        "audio": "audio/en_vocab/en10_v1.mp3",
        "example": "Hi David. Strange weather today, right?",
        "exampleZh": "嗨 David，今天天气好奇怪，对吧？",
        "forms": [
          "weather"
        ]
      },
      {
        "id": "en10_v2",
        "word": "warm",
        "phonetic": "/wɔːrm/",
        "pos": "adj.",
        "meaning": "温暖的",
        "audio": "audio/en_vocab/en10_v2.mp3",
        "example": "I know! It was warm this morning, and now it's cold.",
        "exampleZh": "是啊！早上还挺暖和，现在就冷了。",
        "forms": [
          "warm"
        ]
      },
      {
        "id": "en10_v3",
        "word": "cold",
        "phonetic": "/koʊld/",
        "pos": "adj.",
        "meaning": "冷的",
        "audio": "audio/en_vocab/en10_v3.mp3",
        "example": "I know! It was warm this morning, and now it's cold.",
        "exampleZh": "是啊！早上还挺暖和，现在就冷了。",
        "forms": [
          "cold"
        ]
      },
      {
        "id": "en10_v4",
        "word": "rain",
        "phonetic": "/reɪn/",
        "pos": "n./v.",
        "meaning": "雨；下雨",
        "audio": "audio/en_vocab/en10_v4.mp3",
        "example": "It looks like rain. Did you bring an umbrella?",
        "exampleZh": "看起来要下雨了。你带伞了吗？",
        "forms": [
          "rain"
        ]
      },
      {
        "id": "en10_v5",
        "word": "bring",
        "phonetic": "/brɪŋ/",
        "pos": "v.",
        "meaning": "带来，带上",
        "audio": "audio/en_vocab/en10_v5.mp3",
        "example": "It looks like rain. Did you bring an umbrella?",
        "exampleZh": "看起来要下雨了。你带伞了吗？",
        "forms": [
          "bring"
        ]
      },
      {
        "id": "en10_v6",
        "word": "forget",
        "phonetic": "/fərˈɡet/",
        "pos": "v.",
        "meaning": "忘记",
        "audio": "audio/en_vocab/en10_v6.mp3",
        "example": "No, I forgot it at home, with my keys!",
        "exampleZh": "没带，我把伞和钥匙都忘在家里了！",
        "forms": [
          "forget",
          "forgot"
        ]
      }
    ],
    "topicWords": [
      {
        "id": "en10_t1",
        "word": "umbrella",
        "phonetic": "/ʌmˈbrelə/",
        "pos": "n.",
        "meaning": "雨伞",
        "audio": "audio/en_vocab/en10_t1.mp3",
        "example": "It looks like rain. Did you bring an umbrella?",
        "exampleZh": "看起来要下雨了。你带伞了吗？",
        "forms": [
          "umbrella"
        ]
      }
    ],
    "properNouns": []
  }
];
