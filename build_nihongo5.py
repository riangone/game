#!/usr/bin/env python3
"""Build nihongo5.html for Lesson 5: 《おいしい日本料理》(Delicious Japanese Food).
Based on the clean, battle-tested engine of nihongo4.html.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

with open(ROOT / 'nihongo4.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

# 1. Basic Title & Meta Replacements
out = tpl
out = out.replace(
    '<title>わたしの町 - 日语课文识字闯关 (My Town in Japan)</title>',
    '<title>おいしい日本料理 - 日语课文识字闯关 (Delicious Japanese Food)</title>'
)
out = out.replace(
    '<link rel="canonical" href="https://nhg.0101.click/nihongo4.html">',
    '<link rel="canonical" href="https://nhg.0101.click/nihongo5.html">'
)
out = out.replace(
    '<h1 id="headerTitle">わたしの町</h1>',
    '<h1 id="headerTitle">おいしい日本料理</h1>'
)
out = out.replace(
    '<h2 class="title">わたしの町 (My Town)</h2>\n      <p class="sub">跟随原创日语课文《わたしの町》漫步由纪生活的美丽城镇，学习日语空间方位、生活设施、汉字与高频词汇！本课是《日本の四季》的续篇。</p>',
    '<h2 class="title">おいしい日本料理 (Japanese Food)</h2>\n      <p class="sub">跟随原创日语课文《おいしい日本料理》品尝丰富地道的和风美食，学习一日三餐表达、日本餐桌礼仪、汉字与常用词汇！本课是《わたしの町》的续篇。</p>'
)
out = out.replace(
    '<h2 class="title">📖 わたしの町 (My Town)</h2>',
    '<h2 class="title">📖 おいしい日本料理 (Japanese Food)</h2>'
)
out = out.replace(
    '<h2 class="title">📜 わたしの町 · 全文</h2>',
    '<h2 class="title">📜 おいしい日本料理 · 全文</h2>'
)

# Flashcard proper filter name
out = out.replace(
    '<div class="chip" id="chipVocabProper" onclick="setVocabFilter(\'proper\')">时间 (7)</div>',
    '<div class="chip" id="chipVocabProper" onclick="setVocabFilter(\'proper\')">饮食 (7)</div>'
)
out = out.replace(
    '<div class="chip" id="chipMatchProper" onclick="setMatchMode(\'proper\')">⏰ 时间 (7)</div>',
    '<div class="chip" id="chipMatchProper" onclick="setMatchMode(\'proper\')">🍱 饮食 (7)</div>'
)

# Storage keys and paths
out = out.replace('nihongo4_progress', 'nihongo5_progress')
out = out.replace('nihongo4_srs', 'nihongo5_srs')
out = out.replace('nihongo4_', 'nihongo5_')
out = out.replace('audio/nihongo4/', 'audio/nihongo5/')
out = out.replace('audio/nihongo4_en/', 'audio/nihongo5_en/')
out = out.replace('audio/nihongo4_zh/', 'audio/nihongo5_zh/')
out = out.replace('わたしの町_第', 'おいしい日本料理_第')

# Theme color tweak (give it a rich, warm, appetizing palette)
out = out.replace(
    '--red:#c2410c; --red-dark:#9a3412; --red-soft:#ffedd5;\n    --imperial-red:#b91c1c; --imperial-gold:#d97706; --gold-soft:#fef3c7;\n    --green:#059669; --green-soft:#d1fae5;\n    --blue:#0284c7; --blue-soft:#e0f2fe;',
    '--red:#b91c1c; --red-dark:#881337; --red-soft:#ffe4e6;\n    --imperial-red:#991b1b; --imperial-gold:#d97706; --gold-soft:#fef3c7;\n    --green:#059669; --green-soft:#d1fae5;\n    --blue:#0284c7; --blue-soft:#e0f2fe;'
)
out = out.replace(
    'background:linear-gradient(160deg,#fff4e6,#ffedd5 60%,#fed7aa);',
    'background:linear-gradient(160deg,#fff7ed,#ffedd5 60%,#fecdd3);'
)
# Home palace icon
out = out.replace(
    '<div class="palace-ico">🏡</div>',
    '<div class="palace-ico">🍱</div>'
)

# Replace data section
DATA_SECTION = """// 1. 课文《おいしい日本料理》(原创日语课文 · N5 难度 · 续《わたしの町》)
const STORY = [
  {id:"st1", zh:"ゆうきは、美味しい日本料理が大好きです。", py:"ゆうきは、おいしい にほんりょうりが だいすきです。", en:"Yuki loves delicious Japanese food.", jp:"由纪非常喜欢美味的日本料理。"},
  {id:"st2", zh:"朝は、温かいご飯と味噌汁を食べます。", py:"あさは、あたたかい ごはんと みそしるを たべます。", en:"In the morning, I eat warm rice and miso soup.", jp:"早晨吃热腾腾的米饭和味增汤。"},
  {id:"st3", zh:"お昼には、甘い卵焼きと魚のお弁当を食べます。", py:"おひるには、あまい たまごやきと さかなの おべんとうを たべます。", en:"For lunch, I eat a bento with sweet tamagoyaki and fish.", jp:"中午吃带有甜味玉子烧和鱼的便当。"},
  {id:"st4", zh:"夜は、家族と一緒に寿司や天ぷらを作ります。", py:"よるは、かぞくと いっしょに すしや てんぷらを つくります。", en:"In the evening, I make sushi and tempura together with my family.", jp:"晚上和家人一起做寿司和天妇罗。"},
  {id:"st5", zh:"食事の前に、「いただきます」と言います。", py:"しょくじの まえに、「いただきます」と いいます。", en:"Before eating, we say 'Itadakimasu'.", jp:"在开饭之前，说一句“我开动了”。"},
  {id:"st6", zh:"食べた後には、「ごちそうさま」と感謝します。", py:"たべた あとには、「ごちそうさま」と かんしゃします。", en:"After eating, we say 'Gochisousama' with gratitude.", jp:"吃完之后，说一句“承蒙款待”以表谢意。"},
  {id:"st7", zh:"食堂で、冷たい水や温かいお茶を飲みます。", py:"しょくどうで、つめたい みずや あたたかい おちゃを のみます。", en:"In the cafeteria, we drink cold water or warm tea.", jp:"在食堂里，喝清凉的水或温热的绿茶。"},
  {id:"st8", zh:"日本の食べ物は、体に優しくてとても元気になります。", py:"にほんの たべものは、からだに やさしくて とても げんきに なります。", en:"Japanese food is gentle on the body and brings lots of energy.", jp:"日本的美食温润养身，让人元气满满。"}
];

// 2. 课后生字表 (12 汉字：仅收录与简体中文笔顺完全一致的字，用于田字格描红)
const CHARACTERS = [
  {id:"zi1", zh:"料", py:"りょう", radical:"斗部（とます）", radicalBadge:"斗 —— 料", words:"料理、料金", meaning:"ingredients / fee", meaningJp:"材料、费用、料理", context:"ゆうきは、美味しい日本料理が大好きです"},
  {id:"zi2", zh:"理", py:"り", radical:"王部・玉部（たまへん）", radicalBadge:"王 —— 理", words:"料理、理由", meaning:"reason / logic", meaningJp:"道理、整理、料理", context:"ゆうきは、美味しい日本料理が大好きです"},
  {id:"zi3", zh:"食", py:"しょく・た(べる)", radical:"食部（しょく）", radicalBadge:"食 —— 食", words:"食事、食べる", meaning:"eat / food", meaningJp:"进食、饭食、食物", context:"朝は、温かいご飯と味噌汁を食べます"},
  {id:"zi4", zh:"水", py:"みず・すい", radical:"水部（みず）", radicalBadge:null, words:"水、冷水", meaning:"water", meaningJp:"水、清水、凉水", context:"食堂で、冷たい水や温かいお茶を飲みます"},
  {id:"zi5", zh:"肉", py:"にく", radical:"肉部（にく）", radicalBadge:null, words:"肉、牛肉", meaning:"meat", meaningJp:"肉类、牛肉、鱼肉", context:"野菜と肉をたくさん買って、料理を作ります"},
  {id:"zi6", zh:"茶", py:"ちゃ・さ", radical:"艹部（くさかんむり）", radicalBadge:"艹 —— 茶", words:"お茶、茶道", meaning:"tea", meaningJp:"茶水、绿茶、茶道", context:"食堂で、冷たい水や温かいお茶を飲みます"},
  {id:"zi7", zh:"米", py:"こめ・まい", radical:"米部（こめ）", radicalBadge:null, words:"米、白米", meaning:"rice / grain", meaningJp:"大米、米谷", context:"朝は、温かいご飯と味噌汁を食べます"},
  {id:"zi8", zh:"牛", py:"うし・ぎゅう", radical:"牛部（うし）", radicalBadge:null, words:"牛、牛肉", meaning:"cow / cattle", meaningJp:"牛、牛肉、黄牛", context:"この牛肉はとても美味しいです"},
  {id:"zi9", zh:"味", py:"あじ・み", radical:"口部（くちへん）", radicalBadge:"口 —— 味", words:"味、意味", meaning:"taste / flavor", meaningJp:"味道、风味、滋味", context:"朝は、温かいご飯と味噌汁を食べます"},
  {id:"zi10", zh:"甘", py:"あま(い)・かん", radical:"甘部（かん）", radicalBadge:null, words:"甘い、甘味", meaning:"sweet", meaningJp:"甜味、甘甜", context:"お昼には、甘い卵焼きと魚のお弁当を食べます"},
  {id:"zi11", zh:"作", py:"つく(る)・さく", radical:"亻部（にんべん）", radicalBadge:"亻 —— 作", words:"作る、作文", meaning:"make / create", meaningJp:"制作、烹饪、创作", context:"夜は、家族と一緒に寿司や天ぷらを作ります"},
  {id:"zi12", zh:"体", py:"からだ・たい", radical:"亻部（にんべん）", radicalBadge:"亻 —— 体", words:"体、体力", meaning:"body", meaningJp:"身体、体魄", context:"日本の食べ物は、体に優しくてとても元気になります"}
];

// 3. 课后单词表 (12 Words)
const WORDS = [
  {id:"ci1", zh:"料理", py:"りょうり", meaning:"cuisine / cooking", meaningJp:"料理、菜肴", emoji:"🍱", context:"美味しい日本料理が大好きです", tag:"单词"},
  {id:"ci2", zh:"ご飯", py:"ごはん", meaning:"cooked rice / meal", meaningJp:"米饭、饭食", emoji:"🍚", context:"温かいご飯を食べます", tag:"单词"},
  {id:"ci3", zh:"味噌汁", py:"みそしる", meaning:"miso soup", meaningJp:"味增汤", emoji:"🥣", context:"ご飯と味噌汁を食べます", tag:"单词"},
  {id:"ci4", zh:"卵焼き", py:"たまごやき", meaning:"tamagoyaki (rolled omelet)", meaningJp:"玉子烧、煎蛋卷", emoji:"🍳", context:"甘い卵焼きを食べます", tag:"单词"},
  {id:"ci5", zh:"魚", py:"さかな", meaning:"fish", meaningJp:"鱼、鱼肉", emoji:"🐟", context:"魚のお弁当を食べます", tag:"单词"},
  {id:"ci6", zh:"寿司", py:"すし", meaning:"sushi", meaningJp:"寿司", emoji:"🍣", context:"寿司や天ぷらを作ります", tag:"单词"},
  {id:"ci7", zh:"天ぷら", py:"てんぷら", meaning:"tempura", meaningJp:"天妇罗", emoji:"🍤", context:"寿司や天ぷらを作ります", tag:"单词"},
  {id:"ci8", zh:"お弁当", py:"おべんとう", meaning:"boxed lunch / bento", meaningJp:"便当、盒饭", emoji:"🍱", context:"魚のお弁当を食べます", tag:"单词"},
  {id:"ci9", zh:"お茶", py:"おちゃ", meaning:"tea / green tea", meaningJp:"茶、绿茶", emoji:"🍵", context:"温かいお茶を飲みます", tag:"单词"},
  {id:"ci10", zh:"食堂", py:"しょくどう", meaning:"cafeteria / dining hall", meaningJp:"食堂、餐厅", emoji:"🥢", context:"食堂で、冷たい水を飲みます", tag:"单词"},
  {id:"ci11", zh:"美味しい", py:"おいしい", meaning:"delicious / tasty", meaningJp:"美味、好吃", emoji:"😋", context:"美味しい日本料理が大好きです", tag:"单词"},
  {id:"ci12", zh:"感謝", py:"かんしゃ", meaning:"gratitude / thanks", meaningJp:"感谢、感激", emoji:"🙏", context:"ごちそうさまと感謝します", tag:"单词"}
];

// 4. 课后「饮食与味道」词表 (7 Dining Words)
const PROPER_NOUNS = [
  {id:"pn1", zh:"いただきます", py:"いただきます", meaning:"Itadakimasu (Let's eat)", meaningJp:"我开动了（餐前礼仪）", emoji:"🙏", context:"食事の前に「いただきます」と言います", tag:"饮食"},
  {id:"pn2", zh:"ごちそうさま", py:"ごちそうさま", meaning:"Gochisousama (Thank you for the meal)", meaningJp:"多谢款待（餐后礼仪）", emoji:"🙇", context:"食べた後に「ごちそうさま」と感謝します", tag:"饮食"},
  {id:"pn3", zh:"甘い", py:"あまい", meaning:"sweet", meaningJp:"甜的", emoji:"🍬", context:"甘い卵焼きを食べます", tag:"饮食"},
  {id:"pn4", zh:"辛い", py:"からい", meaning:"spicy / pungent", meaningJp:"辣的、咸辣", emoji:"🌶️", context:"辛い料理も少し食べられます", tag:"饮食"},
  {id:"pn5", zh:"温かい", py:"あたたかい", meaning:"warm", meaningJp:"温热的、暖和的", emoji:"♨️", context:"温かいご飯とお茶をいただきます", tag:"饮食"},
  {id:"pn6", zh:"冷たい", py:"つめたい", meaning:"cold (to touch)", meaningJp:"冰凉的、冷的", emoji:"🧊", context:"冷たい水を飲みます", tag:"饮食"},
  {id:"pn7", zh:"好き", py:"すき", meaning:"like / fond of", meaningJp:"喜欢、喜爱", emoji:"❤️", context:"美味しい料理が大好きです", tag:"饮食"}
];

// 合并生词表 (19项)
const ALL_VOCAB = [...WORDS, ...PROPER_NOUNS];

// 5. 课后重点句子与排序 (5 Sentences)
const SCRAMBLE_SENTENCES = [
  {
    id: "sent1",
    zh: "日本の料理は、とても美味しくて体に優しいです。",
    tokens: ["日本の料理は、", "とても美味しくて", "体に", "優しいです。"],
    isKey: true
  },
  {
    id: "st2",
    zh: "朝は、温かいご飯と味噌汁を食べます。",
    tokens: ["朝は、", "温かいご飯と", "味噌汁を", "食べます。"]
  },
  {
    id: "st4",
    zh: "夜は、家族と一緒に寿司や天ぷらを作ります。",
    tokens: ["夜は、", "家族と一緒に", "寿司や天ぷらを", "作ります。"]
  },
  {
    id: "st5",
    zh: "食事の前に、「いただきます」と言います。",
    tokens: ["食事の前に、", "「いただきます」と", "言います。"]
  },
  {
    id: "st6",
    zh: "食べた後には、「ごちそうさま」と感謝します。",
    tokens: ["食べた後には、", "「ごちそうさま」と", "感謝します。"]
  }
];

// 6. 故事与字词问答 (8 Questions)
const QUIZ = [
  {q:"ゆうきが毎日大好きな料理は何ですか？", opts:["美味しい日本料理", "辛すぎる料理", "冷たいパン", "苦い薬"], a:0},
  {q:"朝ご飯に食べる組み合わせは何ですか？", opts:["温かいご飯と味噌汁", "アイスクリーム", "ハンバーガー", "お菓子"], a:0},
  {q:"生字「食」の部首は何ですか？", opts:["食部（しょく）", "木部（き）", "水部（みず）", "火部（ひ）"], a:0},
  {q:"お昼のお弁当に入っている甘い料理は何ですか？", opts:["卵焼き", "わさび", "唐辛子", "レモン"], a:0},
  {q:"食事の直前に言う日本の挨拶は何ですか？", opts:["いただきます", "ごちそうさま", "さようなら", "おはよう"], a:0},
  {q:"食べ終わった後に感謝を込めて言う言葉は何ですか？", opts:["ごちそうさま", "こんにちは", "おやすみ", "すみません"], a:0},
  {q:"生字「茶」の部首は何ですか？", opts:["艹部（くさかんむり）", "日部（ひ）", "口部（くち）", "心部（こころ）"], a:0},
  {q:"「温かい」の反対の意味を持つ言葉は何ですか？", opts:["冷たい", "甘い", "辛い", "美味しい"], a:0},
];

// 7. 选词填空 (12 Questions: 8 课文原句 + 4 微情境拓展)
const CLOZE_QUESTIONS = [
  {
    id: "nhg5_c1",
    type: "text",
    before: "ゆうきは、美味しい 日本",
    answer: "料理",
    after: "が 大好きです。",
    py: "ゆうきは、おいしい にほんりょうりが だいすきです。",
    en: "Yuki loves delicious Japanese food.",
    jp: "由纪非常喜欢美味的日本料理。",
    answerPy: "りょう り",
    options: ["料理", "旅行", "運動", "音楽"],
    hint: "课文原句 · 生词「料理」(cuisine)",
    audioId: "cloze_1"
  },
  {
    id: "nhg5_c2",
    type: "text",
    before: "朝は、温かい",
    answer: "ご飯",
    after: "と 味噌汁を 食べます。",
    py: "あさは、あたたかい ごはんと みそしるを たべます。",
    en: "In the morning, I eat warm rice and miso soup.",
    jp: "早晨吃热腾腾的米饭和味增汤。",
    answerPy: "ご はん",
    options: ["ご飯", "パン", "ケーキ", "果物"],
    hint: "课文原句 · 生词「ご飯」(cooked rice)",
    audioId: "cloze_2"
  },
  {
    id: "nhg5_c3",
    type: "text",
    before: "お昼には、",
    answer: "甘い",
    after: "卵焼きと 魚の お弁当を 食べます。",
    py: "おひるには、あまい たまごやきと さかなの おべんとうを たべます。",
    en: "For lunch, I eat a bento with sweet tamagoyaki and fish.",
    jp: "中午吃带有甜味玉子烧和鱼的便当。",
    answerPy: "あま い",
    options: ["甘い", "辛い", "苦い", "酸っぱい"],
    hint: "课文原句 · 味道「甘い」(sweet)",
    audioId: "cloze_3"
  },
  {
    id: "nhg5_c4",
    type: "text",
    before: "夜は、家族と 一緒に",
    answer: "寿司",
    after: "や 天ぷらを 作ります。",
    py: "よるは、かぞくと いっしょに すしや てんぷらを つくります。",
    en: "In the evening, I make sushi and tempura together with my family.",
    jp: "晚上和家人一起做寿司和天妇罗。",
    answerPy: "す し",
    options: ["寿司", "ラーメン", "カレー", "ピザ"],
    hint: "课文原句 · 名菜「寿司」(sushi)",
    audioId: "cloze_4"
  },
  {
    id: "nhg5_c5",
    type: "text",
    before: "食事の 前に、「",
    answer: "いただきます",
    after: "」と 言います。",
    py: "しょくじの まえに、「いただきます」と いいます。",
    en: "Before eating, we say 'Itadakimasu'.",
    jp: "在开饭之前，说一句“我开动了”。",
    answerPy: "いただきます",
    options: ["いただきます", "ごちそうさま", "ありがとう", "こんにちは"],
    hint: "课文原句 · 餐前礼仪「いただきます」",
    audioId: "cloze_5"
  },
  {
    id: "nhg5_c6",
    type: "text",
    before: "食べた 後には、「",
    answer: "ごちそうさま",
    after: "」と 感謝します。",
    py: "たべた あとには、「ごちそうさま」と かんしゃします。",
    en: "After eating, we say 'Gochisousama' with gratitude.",
    jp: "吃完之后，说一句“承蒙款待”以表谢意。",
    answerPy: "ごちそうさま",
    options: ["ごちそうさま", "いただきます", "さようなら", "おはよう"],
    hint: "课文原句 · 餐后礼仪「ごちそうさま」",
    audioId: "cloze_6"
  },
  {
    id: "nhg5_c7",
    type: "text",
    before: "食堂で、冷たい",
    answer: "水",
    after: "や 温かい お茶を 飲みます。",
    py: "しょくどうで、つめたい みずや あたたかい おちゃを のみます。",
    en: "In the cafeteria, we drink cold water or warm tea.",
    jp: "在食堂里，喝清凉的水或温热的绿茶。",
    answerPy: "みず",
    options: ["水", "湯", "酒", "薬"],
    hint: "课文原句 · 生字「水」(water)",
    audioId: "cloze_7"
  },
  {
    id: "nhg5_c8",
    type: "text",
    before: "日本の 食べ物は、体に 優しくて とても",
    answer: "元気",
    after: "に なります。",
    py: "にほんの たべものは、からだに やさしくて とても げんきに なります。",
    en: "Japanese food is gentle on the body and brings lots of energy.",
    jp: "日本的美食温润养身，让人元气满满。",
    answerPy: "げん き",
    options: ["元気", "天気", "病気", "気分"],
    hint: "课文原句 · 词汇「元気」(energetic)",
    audioId: "cloze_8"
  },
  {
    id: "nhg5_c9",
    type: "micro",
    before: "この 牛肉は とても",
    answer: "美味しい",
    after: "です。",
    py: "この ぎゅうにくは とても おいしいです。",
    en: "This beef is very delicious.",
    jp: "这份牛肉非常美味好吃。",
    answerPy: "おい しい",
    options: ["美味しい", "寒い", "古い", "新しい"],
    hint: "微情境拓展 · 味道评价「美味しい」(delicious)",
    audioId: "cloze_9"
  },
  {
    id: "nhg5_c10",
    type: "micro",
    before: "暑い 日には、冷たい",
    answer: "お茶",
    after: "を 飲みましょう。",
    py: "あつい ひには、つめたい おちゃを のみましょう。",
    en: "On a hot day, let's drink some cold green tea.",
    jp: "在炎热的日子里，喝点冰凉的绿茶吧。",
    answerPy: "お ちゃ",
    options: ["お茶", "ご飯", "魚", "肉"],
    hint: "微情境拓展 · 饮品搭配「お茶」(tea)",
    audioId: "cloze_10"
  },
  {
    id: "nhg5_c11",
    type: "micro",
    before: "野菜と",
    answer: "肉",
    after: "を たくさん 買って、料理を 作ります。",
    py: "やさいと にくを たくさん かって、りょうりを つくります。",
    en: "I buy plenty of vegetables and meat to cook a meal.",
    jp: "买了很多蔬菜和肉来做料理。",
    answerPy: "にく",
    options: ["肉", "木", "本", "車"],
    hint: "微情境拓展 · 食材生字「肉」(meat)",
    audioId: "cloze_11"
  },
  {
    id: "nhg5_c12",
    type: "micro",
    before: "美味しい 料理を 食べて、みんなが",
    answer: "笑顔",
    after: "に なりました。",
    py: "おいしい りょうりを たべて、みんなが えがおに なりました。",
    en: "Eating delicious food, everyone was filled with smiles.",
    jp: "吃到了美味的料理，大家都露出了灿烂的笑容。",
    answerPy: "え がお",
    options: ["笑顔", "声", "星", "道"],
    hint: "微情境拓展 · 情感表达「笑顔」(smile)",
    audioId: "cloze_12"
  }
];"""

# Replace the data block precisely
pattern = r'// 1\. 课文《わたしの町》.*?const CLOZE_QUESTIONS = \[.*?\];'
out = re.sub(pattern, DATA_SECTION, out, flags=re.DOTALL)

with open(ROOT / 'nihongo5.html', 'w', encoding='utf-8') as f:
    f.write(out)

print(f"Successfully generated nihongo5.html ({len(out)} bytes)")
