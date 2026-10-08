#!/usr/bin/env python3
"""Build nihongo6.html for Lesson 6: 《楽しい旅行》(A Fun Trip in Japan).
Based on the clean, battle-tested engine of nihongo5.html.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

with open(ROOT / 'nihongo5.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

# 1. Basic Title & Meta Replacements
out = tpl
out = out.replace(
    '<title>おいしい日本料理 - 日语课文识字闯关 (Delicious Japanese Food)</title>',
    '<title>楽しい旅行 - 日语课文识字闯关 (A Fun Trip in Japan)</title>'
)
out = out.replace(
    '<link rel="canonical" href="https://nhg.0101.click/nihongo5.html">',
    '<link rel="canonical" href="https://nhg.0101.click/nihongo6.html">'
)
out = out.replace(
    '<h1 id="headerTitle">おいしい日本料理</h1>',
    '<h1 id="headerTitle">楽しい旅行</h1>'
)
out = out.replace(
    '<h2 class="title">おいしい日本料理 (Japanese Food)</h2>\n      <p class="sub">跟随原创日语课文《おいしい日本料理》品尝丰富地道的和风美食，学习一日三餐表达、日本餐桌礼仪、汉字与常用词汇！本课是《わたしの町》的续篇。</p>',
    '<h2 class="title">楽しい旅行 (A Fun Trip)</h2>\n      <p class="sub">跟随原创日语课文《楽しい旅行》乘坐新干线与电车开启关西之旅，学习交通工具表达、名胜见闻、汉字与高频词汇！本课是《おいしい日本料理》的续篇。</p>'
)
out = out.replace(
    '<h2 class="title">📖 おいしい日本料理 (Japanese Food)</h2>',
    '<h2 class="title">📖 楽しい旅行 (A Fun Trip)</h2>'
)
out = out.replace(
    '<h2 class="title">📜 おいしい日本料理 · 全文</h2>',
    '<h2 class="title">📜 楽しい旅行 · 全文</h2>'
)

# Flashcard proper filter name
out = out.replace(
    '<div class="chip" id="chipVocabProper" onclick="setVocabFilter(\'proper\')">饮食 (7)</div>',
    '<div class="chip" id="chipVocabProper" onclick="setVocabFilter(\'proper\')">交通 (7)</div>'
)
out = out.replace(
    '<div class="chip" id="chipMatchProper" onclick="setMatchMode(\'proper\')">🍱 饮食 (7)</div>',
    '<div class="chip" id="chipMatchProper" onclick="setMatchMode(\'proper\')">🚅 交通 (7)</div>'
)

# Storage keys and paths
out = out.replace('nihongo5_progress', 'nihongo6_progress')
out = out.replace('nihongo5_srs', 'nihongo6_srs')
out = out.replace('nihongo5_', 'nihongo6_')
out = out.replace('audio/nihongo5/', 'audio/nihongo6/')
out = out.replace('audio/nihongo5_en/', 'audio/nihongo6_en/')
out = out.replace('audio/nihongo5_zh/', 'audio/nihongo6_zh/')
out = out.replace('おいしい日本料理_第', '楽しい旅行_第')

# Theme color tweak (fresh travel azure & indigo palette)
out = out.replace(
    '--red:#b91c1c; --red-dark:#881337; --red-soft:#ffe4e6;\n    --imperial-red:#991b1b; --imperial-gold:#d97706; --gold-soft:#fef3c7;\n    --green:#059669; --green-soft:#d1fae5;\n    --blue:#0284c7; --blue-soft:#e0f2fe;',
    '--red:#0284c7; --red-dark:#0369a1; --red-soft:#e0f2fe;\n    --imperial-red:#0369a1; --imperial-gold:#d97706; --gold-soft:#fef3c7;\n    --green:#059669; --green-soft:#d1fae5;\n    --blue:#2563eb; --blue-soft:#dbeafe;'
)
out = out.replace(
    'background:linear-gradient(160deg,#fff7ed,#ffedd5 60%,#fecdd3);',
    'background:linear-gradient(160deg,#f0f9ff,#e0f2fe 60%,#ede9fe);'
)
out = out.replace(
    'border-bottom:2px solid #fbd38d;',
    'border-bottom:2px solid #93c5fd;'
)
out = out.replace(
    '<div class="palace-ico">🍱</div>',
    '<div class="palace-ico">🚅</div>'
)

# Replace data section
DATA_SECTION = """// 1. 课文《楽しい旅行》(原创日语课文 · N5 难度 · 续《おいしい日本料理》)
const STORY = [
  {id:"st1", zh:"ゆうきは、休日に友達と京都へ旅行に行きます。", py:"ゆうきは、きゅうじつに ともだちと きょうとへ りょこうに いきます。", en:"On holidays, Yuki goes on a trip to Kyoto with friends.", jp:"假期里，由纪和朋友一起去京都旅行。"},
  {id:"st2", zh:"東京駅から、速い新幹線に乗ります。", py:"とうきょうえきから、はやい しんかんせんに のります。", en:"From Tokyo Station, we take the fast Shinkansen bullet train.", jp:"从东京站出发，坐上飞速的新干线。"},
  {id:"st3", zh:"窓の外に、高くて美しい富士山が見えます。", py:"まどの そとに、たかくて うつくしい ふじさんが みえます。", en:"Outside the window, we can see the tall and beautiful Mount Fuji.", jp:"车窗外，能看见高大优美的富士山。"},
  {id:"st4", zh:"京都に着いて、古いお寺や神社を歩きます。", py:"きょうとに ついて、ふるい おてらや じんじゃを あるきます。", en:"Arriving in Kyoto, we walk around ancient temples and shrines.", jp:"到达京都后，我们在古老的寺庙和神社漫步。"},
  {id:"st5", zh:"静かな庭で、綺麗な写真をたくさん撮ります。", py:"しずかな にわで、きれいな しゃしんを たくさん とります。", en:"In the quiet garden, we take lots of beautiful photos.", jp:"在恬静的日式庭院里，拍了许多漂亮的照片。"},
  {id:"st6", zh:"お昼は、電車で海へ行って美味しい魚を食べます。", py:"おひるは、でんしゃで うみへ いって おいしい さかなを たべます。", en:"For lunch, we take a train to the sea and eat delicious fish.", jp:"中午坐电车去看海，还品尝了鲜美的海鱼。"},
  {id:"st7", zh:"お土産の店で、家族や友達にお菓子を買います。", py:"おみやげの みせで、かぞくや ともだちに おかしを かいます。", en:"At the souvenir shop, we buy sweets for family and friends.", jp:"在特产店里，给家人和朋友挑选了点心伴手礼。"},
  {id:"st8", zh:"日本の旅は、とても楽しくて素晴らしい思い出になります。", py:"にほんの たびは、とても たのしくて すばらしい おもいでに なります。", en:"Traveling in Japan is full of fun and becomes wonderful memories.", jp:"日本的旅行非常快乐，留下了美好难忘的回忆。"}
];

// 2. 课后生字表 (12 汉字)
const CHARACTERS = [
  {id:"zi1", zh:"旅", py:"たび・りょ", radical:"方部（ほう・かたへん）", radicalBadge:"方 —— 旅", words:"旅行、一人旅", meaning:"travel / trip", meaningJp:"旅行、旅途", context:"ゆうきは、休日に友達と京都へ旅行に行きます"},
  {id:"zi2", zh:"行", py:"い(く)・こう・ぎょう", radical:"行部（ぎょうがまえ）", radicalBadge:null, words:"行く、旅行", meaning:"go / conduct", meaningJp:"去、前往、实行", context:"ゆうきは、休日に友達と京都へ旅行に行きます"},
  {id:"zi3", zh:"来", py:"く(る)・らい", radical:"木部（き）", radicalBadge:null, words:"来る、来週", meaning:"come / next", meaningJp:"来、来到、下周", context:"日本の旅は、素晴らしい思い出になります"},
  {id:"zi4", zh:"車", py:"くるま・しゃ", radical:"車部（くるまへん）", radicalBadge:null, words:"電車、車", meaning:"car / train / vehicle", meaningJp:"车、车辆、电车", context:"東京駅から、速い新幹線に乗ります"},
  {id:"zi5", zh:"電", py:"でん", radical:"雨部（あめかんむり）", radicalBadge:"雨 —— 電", words:"電車、電気", meaning:"electricity", meaningJp:"电、电车、电灯", context:"東京駅から、速い新幹線に乗ります"},
  {id:"zi6", zh:"見", py:"み(る)・けん", radical:"見部（みる）", radicalBadge:null, words:"見る、見学", meaning:"see / look", meaningJp:"看、看见、见学", context:"窓の外に、高くて美しい富士山が見えます"},
  {id:"zi7", zh:"海", py:"うみ・かい", radical:"水部（さんずい）", radicalBadge:"氵 —— 海", words:"海、海外", meaning:"sea / ocean", meaningJp:"大海、海洋", context:"お昼は、電車で海へ行って美味しい魚を食べます"},
  {id:"zi8", zh:"買", py:"か(う)・ばい", radical:"貝部（かい）", radicalBadge:"罒/貝 —— 買", words:"買う、買い物", meaning:"buy / purchase", meaningJp:"买、购买、买东西", context:"お土産の店で、家族や友達にお菓子を買います"},
  {id:"zi9", zh:"写", py:"うつ(す)・しゃ", radical:"冖部（わかんむり）", radicalBadge:"冖 —— 写", words:"写真、写生", meaning:"copy / photograph", meaningJp:"抄写、摄影、拍照", context:"静かな庭で、綺麗な写真をたくさん撮ります"},
  {id:"zi10", zh:"真", py:"ま・しん", radical:"目部（め）", radicalBadge:"目 —— 真", words:"写真、真ん中", meaning:"truth / reality", meaningJp:"真实、正中、照片", context:"静かな庭で、綺麗な写真をたくさん撮ります"},
  {id:"zi11", zh:"京", py:"きょう・けい", radical:"亠部（なべぶた）", radicalBadge:"亠 —— 京", words:"京都、東京", meaning:"capital", meaningJp:"京城、首都、京都", context:"ゆうきは、休日に友達と京都へ旅行に行きます"},
  {id:"zi12", zh:"都", py:"みやこ・と・つ", radical:"阝部（おおざと）", radicalBadge:"阝 —— 都", words:"京都、都会", meaning:"metropolis / capital", meaningJp:"都市、京都", context:"ゆうきは、休日に友達と京都へ旅行に行きます"}
];

// 3. 课后单词表 (12 Words)
const WORDS = [
  {id:"ci1", zh:"旅行", py:"りょこう", meaning:"trip / travel", meaningJp:"旅行", emoji:"🧳", context:"京都へ旅行に行きます", tag:"单词"},
  {id:"ci2", zh:"新幹線", py:"しんかんせん", meaning:"bullet train / Shinkansen", meaningJp:"新干线", emoji:"🚄", context:"速い新幹線に乗ります", tag:"单词"},
  {id:"ci3", zh:"電車", py:"でんしゃ", meaning:"train / electric train", meaningJp:"电车", emoji:"🚃", context:"電車で海へ行きます", tag:"单词"},
  {id:"ci4", zh:"東京", py:"とうきょう", meaning:"Tokyo", meaningJp:"东京", emoji:"🗼", context:"東京駅から新幹線に乗ります", tag:"单词"},
  {id:"ci5", zh:"京都", py:"きょうと", meaning:"Kyoto", meaningJp:"京都", emoji:"⛩️", context:"友達と京都へ旅行に行きます", tag:"单词"},
  {id:"ci6", zh:"富士山", py:"ふじさん", meaning:"Mount Fuji", meaningJp:"富士山", emoji:"🗻", context:"高くて美しい富士山が見えます", tag:"单词"},
  {id:"ci7", zh:"写真", py:"しゃしん", meaning:"photograph / picture", meaningJp:"照片", emoji:"📷", context:"綺麗な写真をたくさん撮ります", tag:"单词"},
  {id:"ci8", zh:"お寺", py:"おてら", meaning:"Buddhist temple", meaningJp:"寺庙", emoji:"🏯", context:"古いお寺や神社を歩きます", tag:"单词"},
  {id:"ci9", zh:"神社", py:"じんじゃ", meaning:"Shinto shrine", meaningJp:"神社", emoji:"⛩️", context:"古いお寺や神社を歩きます", tag:"单词"},
  {id:"ci10", zh:"お土産", py:"おみやげ", meaning:"souvenir / gift", meaningJp:"特产、伴手礼", emoji:"🎁", context:"お土産の店でお菓子を買います", tag:"单词"},
  {id:"ci11", zh:"海", py:"うみ", meaning:"sea / ocean", meaningJp:"大海", emoji:"🌊", context:"電車で海へ行きます", tag:"单词"},
  {id:"ci12", zh:"思い出", py:"おもいで", meaning:"memories / recollection", meaningJp:"回忆、记忆", emoji:"✨", context:"素晴らしい思い出になります", tag:"单词"}
];

// 4. 课后「交通与旅行」词表 (7 Transportation Words)
const PROPER_NOUNS = [
  {id:"pn1", zh:"新幹線", py:"しんかんせん", meaning:"bullet train", meaningJp:"新干线（高速列车）", emoji:"🚄", context:"速い新幹線に乗ります", tag:"交通"},
  {id:"pn2", zh:"電車", py:"でんしゃ", meaning:"train", meaningJp:"电车（普通列车）", emoji:"🚃", context:"電車で海へ行きます", tag:"交通"},
  {id:"pn3", zh:"バス", py:"ばす", meaning:"bus", meaningJp:"巴士、公交车", emoji:"🚌", context:"市内をバスで巡ります", tag:"交通"},
  {id:"pn4", zh:"飛行機", py:"ひこうき", meaning:"airplane", meaningJp:"飞机", emoji:"✈️", context:"飛行機で遠くへ行きます", tag:"交通"},
  {id:"pn5", zh:"切符", py:"きっぷ", meaning:"ticket", meaningJp:"车票、乘车券", emoji:"🎫", context:"駅で電車の切符を買います", tag:"交通"},
  {id:"pn6", zh:"ホテル", py:"ほてる", meaning:"hotel", meaningJp:"酒店、宾馆", emoji:"🏨", context:"夜はホテルに泊まります", tag:"交通"},
  {id:"pn7", zh:"楽しい", py:"たのしい", meaning:"fun / enjoyable", meaningJp:"快乐的、有趣的", emoji:"😊", context:"日本の旅はとても楽しいです", tag:"交通"}
];

// 合并生词表 (19项)
const ALL_VOCAB = [...WORDS, ...PROPER_NOUNS];

// 5. 课后重点句子与排序 (5 Sentences)
const SCRAMBLE_SENTENCES = [
  {
    id: "sent1",
    zh: "日本の旅は、とても楽しくて素晴らしい思い出になります。",
    tokens: ["日本の旅は、", "とても楽しくて", "素晴らしい", "思い出になります。"],
    isKey: true
  },
  {
    id: "st2",
    zh: "東京駅から、速い新幹線に乗ります。",
    tokens: ["東京駅から、", "速い新幹線に", "乗ります。"]
  },
  {
    id: "st3",
    zh: "窓の外に、高くて美しい富士山が見えます。",
    tokens: ["窓の外に、", "高くて美しい", "富士山が", "見えます。"]
  },
  {
    id: "st5",
    zh: "静かな庭で、綺麗な写真をたくさん撮ります。",
    tokens: ["静かな庭で、", "綺麗な写真を", "たくさん", "撮ります。"]
  },
  {
    id: "st7",
    zh: "お土産の店で、家族や友達にお菓子を買います。",
    tokens: ["お土産の店で、", "家族や友達に", "お菓子を", "買います。"]
  }
];

// 6. 故事与字词问答 (8 Questions)
const QUIZ = [
  {q:"ゆうきは休日に誰と京都へ旅行に行きますか？", opts:["友達", "一人だけ", "先生", "知らない人"], a:0},
  {q:"東京駅から何に乗って京都へ向かいましたか？", opts:["速い新幹線", "自転車", "小舟", "トラクター"], a:0},
  {q:"生字「旅」の部首は何ですか？", opts:["方部（ほう・かたへん）", "木部（き）", "水部（みず）", "火部（ひ）"], a:0},
  {q:"新幹線の窓の外に見えた高くて美しい名山は何ですか？", opts:["富士山", "エベレスト", "高尾山", "アルプス"], a:0},
  {q:"京都の静かな庭で何を取りましたか？", opts:["綺麗な写真", "果物", "切符", "お弁当"], a:0},
  {q:"生字「電」の部首は何ですか？", opts:["雨部（あめかんむり）", "日部（ひ）", "口部（くち）", "心部（こころ）"], a:0},
  {q:"お土産の店で誰にお菓子を買いましたか？", opts:["家族や友達", "車掌さん", "駅員さん", "カラス"], a:0},
  {q:"「新幹線」の正しい読み方は何ですか？", opts:["しんかんせん", "でんしゃ", "ちかてつ", "ひこうき"], a:0}
];

// 7. 选词填空 (12 Questions: 8 课文原句 + 4 微情境拓展)
const CLOZE_QUESTIONS = [
  {
    id: "nhg6_c1",
    type: "text",
    before: "ゆうきは、休日に 友達と 京都へ",
    answer: "旅行",
    after: "に 行きます。",
    py: "ゆうきは、きゅうじつに ともだちと きょうとへ りょこうに いきます。",
    en: "On holidays, Yuki goes on a trip to Kyoto with friends.",
    jp: "假期里，由纪和朋友一起去京都旅行。",
    answerPy: "りょ こう",
    options: ["旅行", "授業", "掃除", "料理"],
    hint: "课文原句 · 假期出行「旅行」(travel)",
    audioId: "cloze_1"
  },
  {
    id: "nhg6_c2",
    type: "text",
    before: "東京駅から、速い",
    answer: "新幹線",
    after: "に 乗ります。",
    py: "とうきょうえきから、はやい しんかんせんに のります。",
    en: "From Tokyo Station, we take the fast Shinkansen bullet train.",
    jp: "从东京站出发，坐上飞速的新干线。",
    answerPy: "しん かん せん",
    options: ["新幹線", "自転車", "散歩", "階段"],
    hint: "课文原句 · 高铁出行「新幹線」(bullet train)",
    audioId: "cloze_2"
  },
  {
    id: "nhg6_c3",
    type: "text",
    before: "窓の 外に、高くて 美しい",
    answer: "富士山",
    after: "が 見えます。",
    py: "まどの そとに、たかくて うつくしい ふじさんが みえます。",
    en: "Outside the window, we can see the tall and beautiful Mount Fuji.",
    jp: "车窗外，能看见高大优美的富士山。",
    answerPy: "ふ じ さん",
    options: ["富士山", "東京塔", "学校", "食堂"],
    hint: "课文原句 · 著名名胜「富士山」(Mt. Fuji)",
    audioId: "cloze_3"
  },
  {
    id: "nhg6_c4",
    type: "text",
    before: "京都に 着いて、古い お寺や",
    answer: "神社",
    after: "を 歩きます。",
    py: "きょうとに ついて、ふるい おてらや じんじゃを あるきます。",
    en: "Arriving in Kyoto, we walk around ancient temples and shrines.",
    jp: "到达京都后，我们在古老的寺庙和神社漫步。",
    answerPy: "じん じゃ",
    options: ["神社", "教室", "病院", "郵便局"],
    hint: "课文原句 · 传统建筑「神社」(shrine)",
    audioId: "cloze_4"
  },
  {
    id: "nhg6_c5",
    type: "text",
    before: "静かな 庭で、綺麗な",
    answer: "写真",
    after: "を たくさん 撮ります。",
    py: "しずかな にわで、きれいな しゃしんを たくさん とります。",
    en: "In the quiet garden, we take lots of beautiful photos.",
    jp: "在恬静的日式庭院里，拍了许多漂亮的照片。",
    answerPy: "しゃ しん",
    options: ["写真", "本", "手紙", "絵"],
    hint: "课文原句 · 旅途记录「写真」(photo)",
    audioId: "cloze_5"
  },
  {
    id: "nhg6_c6",
    type: "text",
    before: "お昼は、電車で",
    answer: "海",
    after: "へ 行って 美味しい 魚を 食べます。",
    py: "おひるは、でんしゃで うみへ いって おいしい さかなを たべます。",
    en: "For lunch, we take a train to the sea and eat delicious fish.",
    jp: "中午坐电车去看海，还品尝了鲜美的海鱼。",
    answerPy: "うみ",
    options: ["海", "空", "山", "町"],
    hint: "课文原句 · 自然景观「海」(sea)",
    audioId: "cloze_6"
  },
  {
    id: "nhg6_c7",
    type: "text",
    before: "お土産の 店で、家族や 友達に お菓子を",
    answer: "買い",
    after: "ます。",
    py: "おみやげの みせで、かぞくや ともだちに おかしを かいます。",
    en: "At the souvenir shop, we buy sweets for family and friends.",
    jp: "在特产店里，给家人和朋友挑选了点心伴手礼。",
    answerPy: "か(い)",
    options: ["買い", "食べ", "行き", "飲み"],
    hint: "课文原句 · 购物动作「買い」(buy)",
    audioId: "cloze_7"
  },
  {
    id: "nhg6_c8",
    type: "text",
    before: "日本の 旅は、とても 楽しくて 素晴らしい",
    answer: "思い出",
    after: "に なります。",
    py: "にほんの たびは、とても たのしくて すばらしい おもいでに なります。",
    en: "Traveling in Japan is full of fun and becomes wonderful memories.",
    jp: "日本的旅行非常快乐，留下了美好难忘的回忆。",
    answerPy: "おも い で",
    options: ["思い出", "宿題", "試験", "約束"],
    hint: "课文原句 · 旅途体会「思い出」(memories)",
    audioId: "cloze_8"
  },
  {
    id: "nhg6_c9",
    type: "micro",
    before: "駅で 電車の",
    answer: "切符",
    after: "を 買いました。",
    py: "えきで でんしゃの きっぷを かいました。",
    en: "I bought a train ticket at the station.",
    jp: "在车站买了电车车票。",
    answerPy: "きっぷ",
    options: ["切符", "お茶", "水", "机"],
    hint: "微情境拓展 · 乘车购票「切符」(ticket)",
    audioId: "cloze_9"
  },
  {
    id: "nhg6_c10",
    type: "micro",
    before: "あしたは",
    answer: "飛行機",
    after: "で 遠くへ 行きます。",
    py: "あしたは ひこうきで とおくへ いきます。",
    en: "Tomorrow, I'll go far away by airplane.",
    jp: "明天要坐飞机去远方。",
    answerPy: "ひ こう き",
    options: ["飛行機", "公園", "椅子", "傘"],
    hint: "微情境拓展 · 交通工具「飛行機」(airplane)",
    audioId: "cloze_10"
  },
  {
    id: "nhg6_c11",
    type: "micro",
    before: "今夜は 綺麗な",
    answer: "ホテル",
    after: "に 泊まります。",
    py: "こんやは きれいな ほてるに とまります。",
    en: "Tonight we are staying at a nice hotel.",
    jp: "今晚住在漂亮的酒店里。",
    answerPy: "ほ てる",
    options: ["ホテル", "交番", "銀行", "駅"],
    hint: "微情境拓展 · 旅宿设施「ホテル」(hotel)",
    audioId: "cloze_11"
  },
  {
    id: "nhg6_c12",
    type: "micro",
    before: "友だちと 一緒に 旅行して、とても",
    answer: "楽しい",
    after: "です。",
    py: "ともだちと いっしょに りょこうして、とても たのしいです。",
    en: "Traveling together with friends is so much fun.",
    jp: "和朋友一起旅行，真是太快乐了。",
    answerPy: "たの しい",
    options: ["楽しい", "寒い", "辛い", "苦い"],
    hint: "微情境拓展 · 旅行感受「楽しい」(fun)",
    audioId: "cloze_12"
  }
];"""

# Replace the data block precisely
pattern = r'// 1\. 课文《おいしい日本料理》.*?const CLOZE_QUESTIONS = \[.*?\];'
out = re.sub(pattern, DATA_SECTION, out, flags=re.DOTALL)

with open(ROOT / 'nihongo6.html', 'w', encoding='utf-8') as f:
    f.write(out)

print(f"Successfully generated nihongo6.html ({len(out)} bytes)")
