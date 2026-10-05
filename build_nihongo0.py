#!/usr/bin/env python3
"""Build nihongo0.html from nihongo3.html with full fidelity, isolated storage,
new kana/greeting content, and an embedded interactive 50-sound chart (五十音図).
"""
import re

with open('nihongo3.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Title and header replacements
html = html.replace(
    '<title>日本の四季 - 日语课文识字闯关 (Four Seasons in Japan)</title>',
    '<title>五十音とあいさつ - 日语课文识字闯关 (Hiragana & Greetings)</title>'
)
html = html.replace(
    '<h1 id="headerTitle">日本の四季</h1>',
    '<h1 id="headerTitle">五十音とあいさつ</h1>'
)
html = html.replace(
    '<h2 class="title">日本の四季 (Four Seasons)</h2>',
    '<h2 class="title">五十音とあいさつ (Hiragana &amp; Greetings)</h2>'
)
html = html.replace(
    '<p class="sub">跟随原创日语课文《日本の四季》感受日本春夏秋冬的自然之美，学习日语汉字、单词与季节表达！本课是《わたしの一日》的续篇。</p>',
    '<p class="sub">跟随由纪初识日语五十音（あいうえお）、掌握高频日常问候（おはよう、こんにちは、こんばんは、ありがとう）与假名基础知识！本课是日语课文识字闯关系列的入门序章（第0课）。</p>'
)
html = html.replace(
    '<h2 class="title">📖 日本の四季 (Four Seasons)</h2>',
    '<h2 class="title">📖 五十音とあいさつ (Hiragana &amp; Greetings)</h2>'
)
html = html.replace(
    '<h2 class="title">📜 日本の四季 · 全文</h2>',
    '<h2 class="title">📜 五十音とあいさつ · 全文</h2>'
)

# Replace SVG icon on menu screen with Japanese Hiragana / Torii / Cherry Blossom theme
old_svg_block = """      <div class="palace-ico">
        <svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="28" fill="#fff" stroke="#b91c1c" stroke-width="3"/>
          <circle cx="32" cy="20" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="43" cy="28" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="39" cy="42" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="25" cy="42" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="21" cy="28" r="7.5" fill="#f43f5e" opacity="0.9"/>
          <circle cx="32" cy="32" r="5" fill="#fef08a"/>
        </svg>
      </div>"""

new_svg_block = """      <div class="palace-ico">
        <svg viewBox="0 0 64 64" width="1em" height="1em" xmlns="http://www.w3.org/2000/svg" style="vertical-align:-0.08em">
          <circle cx="32" cy="32" r="28" fill="#fff" stroke="#b91c1c" stroke-width="3"/>
          <!-- stylized 'あ' emblem -->
          <circle cx="32" cy="32" r="23" fill="#fff7ed" stroke="#fbd38d" stroke-width="1.5"/>
          <text x="32" y="44" font-family="'M PLUS Rounded 1c', sans-serif" font-size="34" font-weight="900" fill="#b91c1c" text-anchor="middle">あ</text>
        </svg>
      </div>"""

html = html.replace(old_svg_block, new_svg_block)

# 2. Add 50-sound chart menu card & chart screen
chart_menu_card = """        <div class="menu-card full" onclick="goKanaChart()" style="border-color:#ec4899;background:linear-gradient(135deg,#fff0f5,#fce7f3);">
          <div class="ico">🌸</div>
          <div class="name">五十音图速查</div>
          <div class="desc">清音46音 · 平假名/片假名点读发音</div>
          <div class="badge" style="background:#db2777;">基础必备</div>
        </div>
"""

# Insert chart menu card before '认汉字'
html = html.replace(
    '        <div class="menu-card" onclick="goChars()">\n          <div class="ico">✍️</div>\n          <div class="name">认汉字</div>',
    chart_menu_card + '        <div class="menu-card" onclick="goChars()">\n          <div class="ico">✍️</div>\n          <div class="name">认汉字</div>'
)

# Description replacements on menu cards
html = html.replace('<div class="desc">19个单词与时间表达</div>', '<div class="desc">19个假名与常用寒暄词</div>')

# 3. Add Kana Chart Screen HTML before </main>
chart_screen_html = """    <!-- KANA CHART (五十音図) -->
    <section class="screen" id="screen-kana-chart">
      <h2 class="title">🌸 五十音図速查速听</h2>
      <p class="sub">点击任意假名即可朗读标准发音，支持平假名与片假名对照学习！</p>
      
      <div style="display:flex;gap:10px;justify-content:center;margin-bottom:8px;">
        <button class="btn small gold" id="btnKanaHira" onclick="switchKanaMode('hira')">平假名 (Hiragana)</button>
        <button class="btn small ghost" id="btnKanaKata" onclick="switchKanaMode('kata')">片假名 (Katakana)</button>
      </div>

      <div class="kana-grid-container" id="kanaGridContainer" style="width:100%;max-width:540px;background:#fff;border:2px solid #fbd38d;border-radius:var(--radius-lg);padding:14px;box-shadow:var(--shadow-card);">
        <!-- populated dynamically by renderKanaGrid() -->
      </div>

      <div style="margin-top:12px;display:flex;gap:12px;">
        <button class="btn ghost small" onclick="goHome()">返回主菜单</button>
        <button class="btn gold small" onclick="goStory()">进入课文朗读 📖</button>
      </div>
    </section>
"""

html = html.replace('  </main>', chart_screen_html + '  </main>')

# Add CSS for kana-grid
kana_css = """
  /* kana chart styles */
  .kana-table { width: 100%; border-collapse: separate; border-spacing: 5px; table-layout: fixed; }
  .kana-cell {
    background: #fffdfa; border: 1.5px solid #fed7aa; border-radius: 10px;
    padding: 8px 4px; text-align: center; cursor: pointer; transition: all .15s;
    user-select: none;
  }
  .kana-cell:hover, .kana-cell:active {
    background: #fee2e2; border-color: #f87171; transform: scale(1.05);
  }
  .kana-cell.empty { background: transparent; border-color: transparent; cursor: default; }
  .kana-main { font-size: 20px; font-weight: 800; color: #b91c1c; line-height: 1.1; }
  .kana-sub { font-size: 11px; font-weight: 700; color: #0284c7; margin-top: 2px; }
  .kana-row-label { font-size: 11px; font-weight: 800; color: #78716c; vertical-align: middle; text-align: center; }
"""
html = html.replace('</style>', kana_css + '\n</style>')

# 4. Storage keys and audio directories
html = html.replace('nihongo3_progress', 'nihongo0_progress')
html = html.replace('nihongo3_srs', 'nihongo0_srs')
html = html.replace('audio/nihongo3/', 'audio/nihongo0/')
html = html.replace('audio/nihongo3_en/', 'audio/nihongo0_en/')
html = html.replace('audio/nihongo3_zh/', 'audio/nihongo0_zh/')
html = html.replace('nihongo3_', 'nihongo0_')
html = html.replace('日本の四季_第', '五十音とあいさつ_第')

# 5. Replace data block
DATA_BLOCK = """// 1. 课文《五十音とあいさつ》(原创日语课文 · 假名与日常寒暄入门篇 · 序章)
const STORY = [
  {id:"st1", zh:"あいうえお、日本語をはじめましょう。", py:"あいうえお、にほんごを はじめましょう。", en:"A-I-U-E-O, let's begin learning Japanese!", jp:"あいうえお，让我们开始快乐地学日语吧。"},
  {id:"st2", zh:"朝は「おはよう」と元気にあいさつします。", py:"あさは 「おはよう」と げんきに あいさつします。", en:"In the morning, we greet cheerfully with 'Ohayou'.", jp:"清晨时分，精神饱满地向大家问候“早上好”。"},
  {id:"st3", zh:"昼は「こんにちは」と笑顔で言います。", py:"ひるは 「こんにちは」と えがおで いいます。", en:"In the daytime, we say 'Konnichiwa' with a bright smile.", jp:"白天相遇，面带微笑亲切地说“你好”。"},
  {id:"st4", zh:"夜は「こんばんは」とあいさつします。", py:"よるは 「こんばんは」と あいさつします。", en:"In the evening, we greet warmly with 'Konbanwa'.", jp:"夜幕降临，道一声温和的“晚上好”。"},
  {id:"st5", zh:"感謝の気持ちで「ありがとう」と伝えます。", py:"かんしゃの きもちで 「ありがとう」と つたえます。", en:"With a thankful heart, we express our gratitude with 'Arigatou'.", jp:"怀着由衷的感激，真诚地表达“谢谢”。"},
  {id:"st6", zh:"かきくけこ、ひらがなを声に出して読みます。", py:"かきくけこ、ひらがなを こえに だして よみます。", en:"Ka-Ki-Ku-Ke-Ko, we read hiragana aloud with clear voices.", jp:"かきくけこ，大声朗读清脆优美的平假名。"},
  {id:"st7", zh:"ひらがなとカタカナは、日本語のたいせつな基本です。", py:"ひらがなと カタカナは、にほんごの たいせつな きほんです。", en:"Hiragana and Katakana are the essential foundations of Japanese.", jp:"平假名与片假名，是开启日语世界的关键基石。"},
  {id:"st8", zh:"さあ、みんなで楽しく五十音を学びましょう！", py:"さあ、みんなで たのしく ごじゅうおんを まなびましょう！", en:"Come on, let's enjoy learning the fifty sounds together!", jp:"来吧，让我们一起轻松愉快地学习五十音！"}
];

// 2. 课后生字表 (12 汉字：日语文字与基础高频汉字，田字格笔顺与部首全具备)
const CHARACTERS = [
  {id:"zi1", zh:"日", py:"ひ・にち・じつ", radical:"日部（自体が部首）", radicalBadge:null, words:"日本語、今日、毎日", meaning:"sun / day", meaningJp:"太阳、日子", context:"あいうえお、日本語をはじめましょう"},
  {id:"zi2", zh:"本", py:"ほん・もと", radical:"木部（木字旁）", radicalBadge:"木 —— 本", words:"日本語、基本、本", meaning:"book / origin", meaningJp:"书、根基", context:"あいうえお、日本語をはじめましょう"},
  {id:"zi3", zh:"語", py:"ご・かた(る)", radical:"言部（言字旁）", radicalBadge:"言 —— 語", words:"日本語、言葉、単語", meaning:"language / word", meaningJp:"语言、说话", context:"あいうえお、日本語をはじめましょう"},
  {id:"zi4", zh:"字", py:"じ・あざ", radical:"子部（宀部/子字底）", radicalBadge:"宀 —— 字", words:"漢字、文字、習字", meaning:"character / letter", meaningJp:"汉字、字", context:"ひらがなとカタカナは日本語の文字です"},
  {id:"zi5", zh:"文", py:"ぶん・もん・ふみ", radical:"文部（自体が部首）", radicalBadge:null, words:"文章、作文、例文", meaning:"sentence / text", meaningJp:"句子、文章", context:"ひらがなで文を作ります"},
  {id:"zi6", zh:"音", py:"おと・おん・いん", radical:"音部（自体が部首）", radicalBadge:null, words:"五十音、音楽、発音", meaning:"sound / pronunciation", meaningJp:"声音、发音", context:"さあ、みんなで楽しく五十音を学びましょう！"},
  {id:"zi7", zh:"声", py:"こえ・せい・しょう", radical:"士部（声）", radicalBadge:null, words:"大声、声色、歌声", meaning:"voice", meaningJp:"声音、嗓音", context:"かきくけこ、ひらがなを声に出して読みます"},
  {id:"zi8", zh:"名", py:"な・めい・みょう", radical:"口部（口字底）", radicalBadge:"夕 —— 名", words:"名前、平仮名、有名", meaning:"name", meaningJp:"名字、名称", context:"ひらがなの「名」は名前の字です"},
  {id:"zi9", zh:"言", py:"い(う)・げん・ごん", radical:"言部（自体が部首）", radicalBadge:null, words:"言う、言葉、発言", meaning:"say / word", meaningJp:"说、语言", context:"昼は「こんにちは」と笑顔で言います"},
  {id:"zi10", zh:"心", py:"こころ・しん", radical:"心部（自体が部首）", radicalBadge:null, words:"気持ち、安心、真心", meaning:"heart / mind", meaningJp:"心、心情", context:"感謝の気持ちで「ありがとう」と伝えます"},
  {id:"zi11", zh:"口", py:"くち・こう・く", radical:"口部（自体が部首）", radicalBadge:null, words:"出口、入口、口調", meaning:"mouth", meaningJp:"嘴巴、出入口", context:"口を大きく開けて発音します"},
  {id:"zi12", zh:"人", py:"ひと・じん・にん", radical:"人部（自体が部首）", radicalBadge:null, words:"日本人、先生、友人", meaning:"person / people", meaningJp:"人、大家", context:"たくさんの人とあいさつを交わします"}
];

// 3. 课后单词表 (12 Words - 原创课文生词)
const WORDS = [
  {id:"ci1", zh:"ひらがな", py:"ひらがな", meaning:"hiragana", meaningJp:"平假名", emoji:"🇯🇵", context:"かきくけこ、ひらがなを声に出して読みます", tag:"假名"},
  {id:"ci2", zh:"カタカナ", py:"かたかな", meaning:"katakana", meaningJp:"片假名", emoji:"🔤", context:"ひらがなとカタカナは、日本語のたいせつな基本です", tag:"假名"},
  {id:"ci3", zh:"あいさつ", py:"あいさつ", meaning:"greeting", meaningJp:"打招呼、寒暄", emoji:"🙇", context:"朝は「おはよう」と元気にあいさつします", tag:"寒暄"},
  {id:"ci4", zh:"おはよう", py:"おはよう", meaning:"good morning", meaningJp:"早上好", emoji:"🌅", context:"朝は「おはよう」と元気にあいさつします", tag:"寒暄"},
  {id:"ci5", zh:"こんにちは", py:"こんにちは", meaning:"hello / good day", meaningJp:"你好（白天）", emoji:"☀️", context:"昼は「こんにちは」と笑顔で言います", tag:"寒暄"},
  {id:"ci6", zh:"こんばんは", py:"こんばんは", meaning:"good evening", meaningJp:"晚上好", emoji:"🌙", context:"夜は「こんばんは」とあいさつします", tag:"寒暄"},
  {id:"ci7", zh:"ありがとう", py:"ありがとう", meaning:"thank you", meaningJp:"谢谢", emoji:"🙏", context:"感謝の気持ちで「ありがとう」と伝えます", tag:"寒暄"},
  {id:"ci8", zh:"はじめまして", py:"はじめまして", meaning:"nice to meet you", meaningJp:"初次见面", emoji:"🤝", context:"初めて会った人には「はじめまして」と言います", tag:"寒暄"},
  {id:"ci9", zh:"さようなら", py:"さようなら", meaning:"goodbye", meaningJp:"再见", emoji:"👋", context:"別れるときは笑顔で「さようなら」と言います", tag:"寒暄"},
  {id:"ci10", zh:"五十音", py:"ごじゅうおん", meaning:"fifty sounds", meaningJp:"五十音", emoji:"🎶", context:"さあ、みんなで楽しく五十音を学びましょう！", tag:"假名"},
  {id:"ci11", zh:"声", py:"こえ", meaning:"voice", meaningJp:"声音", emoji:"🗣️", context:"かきくけこ、ひらがなを声に出して読みます", tag:"单词"},
  {id:"ci12", zh:"笑顔", py:"えがお", meaning:"smiling face", meaningJp:"笑容、笑脸", emoji:"😊", context:"昼は「こんにちは」と笑顔で言います", tag:"单词"}
];

// 4. 课后「常用寒暄」词表 (7 Greeting Words - 常用口语高频表达)
const PROPER_NOUNS = [
  {id:"pn1", zh:"はい", py:"はい", meaning:"yes / okay", meaningJp:"是的、好的", emoji:"✅", context:"名前を呼ばれたら「はい」と返事します", tag:"日常"},
  {id:"pn2", zh:"いいえ", py:"いいえ", meaning:"no / not at all", meaningJp:"不、不是", emoji:"❌", context:"違っているときは「いいえ」と答えます", tag:"日常"},
  {id:"pn3", zh:"すみません", py:"すみません", meaning:"excuse me / sorry", meaningJp:"不好意思、对不起", emoji:"🙇‍♂️", context:"声をかけるときは「すみません」と言います", tag:"日常"},
  {id:"pn4", zh:"どうぞ", py:"どうぞ", meaning:"please / here you are", meaningJp:"请、给您", emoji:"👉", context:"物を渡すときは「どうぞ」と言います", tag:"日常"},
  {id:"pn5", zh:"どうも", py:"どうも", meaning:"thanks / hello", meaningJp:"多谢、你好", emoji:"✨", context:"軽く感謝を伝えるときは「どうも」と言います", tag:"日常"},
  {id:"pn6", zh:"よろしく", py:"よろしく", meaning:"pleased to meet you", meaningJp:"请多关照", emoji:"🤝", context:"これから仲良くしたいときは「よろしく」と言います", tag:"日常"},
  {id:"pn7", zh:"じゃあね", py:"じゃあね", meaning:"see you later", meaningJp:"回头见、拜拜", emoji:"👋", context:"友達と別れるときは「じゃあね」と言います", tag:"日常"}
];

// 合并生词表 (19项)
const ALL_VOCAB = [...WORDS, ...PROPER_NOUNS];

// 5. 课后重点句子与排序 (5 Sentences)
const SCRAMBLE_SENTENCES = [
  {
    id: "sent1",
    zh: "笑顔であいさつするのは、とても大切です。",
    tokens: ["笑顔で", "あいさつするのは、", "とても", "大切です。"],
    isKey: true
  },
  {
    id: "st1",
    zh: "あいうえお、日本語をはじめましょう。",
    tokens: ["あいうえお、", "日本語を", "はじめましょう。"]
  },
  {
    id: "st2",
    zh: "朝は「おはよう」と元気にあいさつします。",
    tokens: ["朝は", "「おはよう」と", "元気に", "あいさつします。"]
  },
  {
    id: "st3",
    zh: "昼は「こんにちは」と笑顔で言います。",
    tokens: ["昼は", "「こんにちは」と", "笑顔で", "言います。"]
  },
  {
    id: "st5",
    zh: "感謝の気持ちで「ありがとう」と伝えます。",
    tokens: ["感謝の", "気持ちで", "「ありがとう」と", "伝えます。"]
  }
];

// 6. 故事与字词问答 (8 Questions)
const QUIZ = [
  {q:"朝、誰かに会ったときにするあいさつは何ですか？", opts:["こんにちは", "こんばんは", "おはよう", "さようなら"], a:2},
  {q:"昼、友達や先生に会ったときのあいさつは何ですか？", opts:["おはよう", "こんにちは", "おやすみ", "ありがとう"], a:1},
  {q:"夜、人に会ったときのあいさつは何ですか？", opts:["こんばんは", "さようなら", "おはよう", "こんにちは"], a:0},
  {q:"親切にしてもらったとき、感謝を伝える言葉は何ですか？", opts:["すみません", "ありがとう", "どういたしまして", "はい"], a:1},
  {q:"日本語の母音（あいうえお）は全部でいくつありますか？", opts:["3つ", "4つ", "5つ", "6つ"], a:2},
  {q:"初めて会った人に自己紹介するとき、最初に言う言葉は何ですか？", opts:["さようなら", "はじめまして", "いただきます", "ごちそうさま"], a:1},
  {q:"生字「語」の部首は何ですか？", opts:["言部（言）", "口部（口）", "五部（五）", "心部（心）"], a:0},
  {q:"生字「音」の部首は何ですか？", opts:["日部（日）", "立部（立）", "音部（自体が部首）", "口部（口）"], a:2},
];

// 7. 选词填空 (12 Questions: 8 课文原句 + 4 微情境拓展)
const CLOZE_QUESTIONS = [
  {
    id: "nhg0_c1",
    type: "text",
    before: "あいうえお、",
    answer: "日本語",
    after: "をはじめましょう。",
    py: "あいうえお、にほんごを はじめましょう。",
    en: "A-I-U-E-O, let's begin learning Japanese!",
    jp: "あいうえお，让我们开始快乐地学日语吧。",
    answerPy: "に ほん ご",
    options: ["日本語", "英語", "音楽", "学校"],
    hint: "课文原句 · 我们开始学习的语言是？",
    audioId: "cloze_1"
  },
  {
    id: "nhg0_c2",
    type: "text",
    before: "朝は「",
    answer: "おはよう",
    after: "」と元気にあいさつします。",
    py: "あさは 「おはよう」と げんきに あいさつします。",
    en: "In the morning, we greet cheerfully with 'Ohayou'.",
    jp: "清晨时分，精神饱满地向大家问候“早上好”。",
    answerPy: "おはよう",
    options: ["おはよう", "こんにちは", "こんばんは", "おやすみ"],
    hint: "课文原句 · 早晨的问候语",
    audioId: "cloze_2"
  },
  {
    id: "nhg0_c3",
    type: "text",
    before: "昼は「",
    answer: "こんにちは",
    after: "」と笑顔で言います。",
    py: "ひるは 「こんにちは」と えがおで いいます。",
    en: "In the daytime, we say 'Konnichiwa' with a bright smile.",
    jp: "白天相遇，面带微笑亲切地说“你好”。",
    answerPy: "こんにちは",
    options: ["さようなら", "こんばんは", "こんにちは", "おはよう"],
    hint: "课文原句 · 白天见面的问候",
    audioId: "cloze_3"
  },
  {
    id: "nhg0_c4",
    type: "text",
    before: "夜は「",
    answer: "こんばんは",
    after: "」とあいさつします。",
    py: "よるは 「こんばんは」と あいさつします。",
    en: "In the evening, we greet warmly with 'Konbanwa'.",
    jp: "夜幕降临，道一声温和的“晚上好”。",
    answerPy: "こんばんは",
    options: ["こんばんは", "こんにちは", "いただきます", "おはよう"],
    hint: "课文原句 · 夜晚的问候语",
    audioId: "cloze_4"
  },
  {
    id: "nhg0_c5",
    type: "text",
    before: "感謝の気持ちで「",
    answer: "ありがとう",
    after: "」と伝えます。",
    py: "かんしゃの きもちで 「ありがとう」と つたえます。",
    en: "With a thankful heart, we express our gratitude with 'Arigatou'.",
    jp: "怀着由衷的感激，真诚地表达“谢谢”。",
    answerPy: "ありがとう",
    options: ["すみません", "どうも", "ありがとう", "いいえ"],
    hint: "课文原句 · 表达感谢的经典词语",
    audioId: "cloze_5"
  },
  {
    id: "nhg0_c6",
    type: "text",
    before: "かきくけこ、ひらがなを",
    answer: "声",
    after: "に出して読みます。",
    py: "かきくけこ、ひらがなを こえに だして よみます。",
    en: "Ka-Ki-Ku-Ke-Ko, we read hiragana aloud with clear voices.",
    jp: "かきくけこ，大声朗读清脆优美的平假名。",
    answerPy: "こえ",
    options: ["声", "手", "心", "歌"],
    hint: "课文原句 · 朗读时发出的声音（声に出す）",
    audioId: "cloze_6"
  },
  {
    id: "nhg0_c7",
    type: "text",
    before: "ひらがなとカタカナは、日本語のたいせつな",
    answer: "基本",
    after: "です。",
    py: "ひらがなと カタカナは、にほんごの たいせつな きほんです。",
    en: "Hiragana and Katakana are the essential foundations of Japanese.",
    jp: "平假名与片假名，是开启日语世界的关键基石。",
    answerPy: "き ほん",
    options: ["基本", "秘密", "文法", "時間"],
    hint: "课文原句 · 平假名与片假名是重要的基础（基本）",
    audioId: "cloze_7"
  },
  {
    id: "nhg0_c8",
    type: "text",
    before: "さあ、みんなで楽しく",
    answer: "五十音",
    after: "を学びましょう！",
    py: "さあ、みんなで たのしく ごじゅうおんを まなびましょう！",
    en: "Come on, let's enjoy learning the fifty sounds together!",
    jp: "来吧，让我们一起轻松愉快地学习五十音！",
    answerPy: "ご じゅう おん",
    options: ["五十音", "漢字", "数字", "四季"],
    hint: "课文原句 · 大家一起快乐学习的五十音",
    audioId: "cloze_8"
  },
  {
    id: "nhg0_c9",
    type: "micro",
    before: "名前を聞かれたら、元気に「",
    answer: "はい",
    after: "」と返事をします。",
    py: "なまえを きかれたら、げんきに 「はい」と へんじを します。",
    en: "When your name is called, answer cheerfully with 'Hai'.",
    jp: "被叫到名字时，精神饱满地答应“到/是的”。",
    answerPy: "はい",
    options: ["はい", "いいえ", "じゃあね", "どうぞ"],
    hint: "微情境拓展 · 答应与应答（はい）",
    audioId: "cloze_9"
  },
  {
    id: "nhg0_c10",
    type: "micro",
    before: "人に何かを渡すときは、「",
    answer: "どうぞ",
    after: "」と言います。",
    py: "ひとに なにかを わたすときは、「どうぞ」と いいます。",
    en: "When handing something to someone, say 'Douzo'.",
    jp: "递给别人东西时，客气地说“请/给您”。",
    answerPy: "どうぞ",
    options: ["どうぞ", "どうも", "いいえ", "すみません"],
    hint: "微情境拓展 · 礼貌客气（どうぞ）",
    audioId: "cloze_10"
  },
  {
    id: "nhg0_c11",
    type: "micro",
    before: "別れるときは、笑顔で「",
    answer: "さようなら",
    after: "」と言いましょう。",
    py: "わかれるときは、えがおで 「さようなら」と いいましょう。",
    en: "When parting, let's say 'Sayounara' with a smile.",
    jp: "分别告别时，微笑着说“再见”。",
    answerPy: "さようなら",
    options: ["さようなら", "はじめまして", "おはよう", "ありがとう"],
    hint: "微情境拓展 · 告别问候（さようなら）",
    audioId: "cloze_11"
  },
  {
    id: "nhg0_c12",
    type: "micro",
    before: "初めて会った人には、「",
    answer: "はじめまして",
    after: "」と自己紹介します。",
    py: "はじめて あった ひとには、「はじめまして」と じこしょうかい します。",
    en: "To someone you meet for the first time, introduce yourself with 'Hajimemashite'.",
    jp: "初次见面的人，先说“初次见面”再作自我介绍。",
    answerPy: "はじめまして",
    options: ["はじめまして", "さようなら", "こんばんは", "おやすみ"],
    hint: "微情境拓展 · 初次相识（はじめまして）",
    audioId: "cloze_12"
  }
];"""

# Replace data section
# Find from '// 1. 课文《日本の四季》' to '// 7. 选词填空'
pattern = re.compile(r'// 1\. 课文《日本の四季》.*?const CLOZE_QUESTIONS = \[.*?\];', re.DOTALL)
if pattern.search(html):
    html = pattern.sub(DATA_BLOCK, html)
    print("Replaced DATA_BLOCK successfully.")
else:
    print("WARNING: Could not find DATA_BLOCK match!")

# 6. Add JavaScript functions for Kana Chart
KANA_JS = """
/* ---------------- KANA CHART (五十音図) ---------------- */
let kanaCurrentMode = 'hira'; // 'hira' or 'kata'
const KANA_ROWS = [
  { name: 'あ行', romaji: 'a', items: [
    {h:'あ', k:'ア', r:'a'}, {h:'い', k:'イ', r:'i'}, {h:'う', k:'ウ', r:'u'}, {h:'え', k:'エ', r:'e'}, {h:'お', k:'オ', r:'o'}
  ]},
  { name: 'か行', romaji: 'k', items: [
    {h:'か', k:'カ', r:'ka'}, {h:'き', k:'キ', r:'ki'}, {h:'く', k:'ク', r:'ku'}, {h:'け', k:'ケ', r:'ke'}, {h:'こ', k:'コ', r:'ko'}
  ]},
  { name: 'さ行', romaji: 's', items: [
    {h:'さ', k:'サ', r:'sa'}, {h:'し', k:'シ', r:'shi'}, {h:'す', k:'ス', r:'su'}, {h:'せ', k:'セ', r:'se'}, {h:'そ', k:'ソ', r:'so'}
  ]},
  { name: 'た行', romaji: 't', items: [
    {h:'た', k:'タ', r:'ta'}, {h:'ち', k:'チ', r:'chi'}, {h:'つ', k:'ツ', r:'tsu'}, {h:'て', k:'テ', r:'te'}, {h:'と', k:'ト', r:'to'}
  ]},
  { name: 'な行', romaji: 'n', items: [
    {h:'な', k:'ナ', r:'na'}, {h:'に', k:'ニ', r:'ni'}, {h:'ぬ', k:'ヌ', r:'nu'}, {h:'ね', k:'ネ', r:'ne'}, {h:'の', k:'ノ', r:'no'}
  ]},
  { name: 'は行', romaji: 'h', items: [
    {h:'は', k:'ハ', r:'ha'}, {h:'ひ', k:'ヒ', r:'hi'}, {h:'ふ', k:'フ', r:'fu'}, {h:'へ', k:'ヘ', r:'he'}, {h:'ほ', k:'ホ', r:'ho'}
  ]},
  { name: 'ま行', romaji: 'm', items: [
    {h:'ま', k:'マ', r:'ma'}, {h:'み', k:'ミ', r:'mi'}, {h:'む', k:'ム', r:'mu'}, {h:'め', k:'メ', r:'me'}, {h:'も', k:'モ', r:'mo'}
  ]},
  { name: 'や行', romaji: 'y', items: [
    {h:'や', k:'ヤ', r:'ya'}, null, {h:'ゆ', k:'ユ', r:'yu'}, null, {h:'よ', k:'ヨ', r:'yo'}
  ]},
  { name: 'ら行', romaji: 'r', items: [
    {h:'ら', k:'ラ', r:'ra'}, {h:'り', k:'リ', r:'ri'}, {h:'る', k:'ル', r:'ru'}, {h:'れ', k:'レ', r:'re'}, {h:'ろ', k:'ロ', r:'ro'}
  ]},
  { name: 'わ行', romaji: 'w', items: [
    {h:'わ', k:'ワ', r:'wa'}, null, null, null, {h:'を', k:'ヲ', r:'wo'}
  ]},
  { name: 'ん', romaji: 'n', items: [
    {h:'ん', k:'ン', r:'n'}, null, null, null, null
  ]}
];

function goKanaChart() {
  showScreen('screen-kana-chart');
  renderKanaGrid();
}
window.switchScreen = showScreen;
window.goMenu = goHome;

function switchKanaMode(mode) {
  kanaCurrentMode = mode;
  const btnHira = document.getElementById('btnKanaHira');
  const btnKata = document.getElementById('btnKanaKata');
  if(btnHira) btnHira.className = mode === 'hira' ? 'btn small gold' : 'btn small ghost';
  if(btnKata) btnKata.className = mode === 'kata' ? 'btn small gold' : 'btn small ghost';
  renderKanaGrid();
}

function playKanaSound(romaji, kanaChar) {
  if (romaji) {
    playClip('kana_' + romaji, kanaChar, null, 'ja-JP');
    toast('🔊 ' + kanaChar + ' [' + romaji + ']');
    return;
  }
  speak(kanaChar, null, 'ja-JP');
  toast('🔊 ' + kanaChar);
}

function renderKanaGrid() {
  const container = document.getElementById('kanaGridContainer');
  if (!container) return;
  
  let html = '<table class="kana-table">';
  html += '<thead><tr><th style="width:40px;"></th><th>段 a</th><th>段 i</th><th>段 u</th><th>段 e</th><th>段 o</th></tr></thead>';
  html += '<tbody>';
  
  KANA_ROWS.forEach(row => {
    html += '<tr>';
    html += `<td class="kana-row-label">${row.name}</td>`;
    row.items.forEach(it => {
      if (!it) {
        html += '<td class="kana-cell empty"></td>';
      } else {
        const char = kanaCurrentMode === 'hira' ? it.h : it.k;
        const sub = it.r;
        html += `<td class="kana-cell" onclick="playKanaSound('${it.r}', '${char}')" title="点击朗读: ${char} (${sub})">
          <div class="kana-main">${char}</div>
          <div class="kana-sub">${sub}</div>
        </td>`;
      }
    });
    html += '</tr>';
  });
  
  html += '</tbody></table>';
  container.innerHTML = html;
}
"""

html = html.replace('/* ---------------- INIT ---------------- */', KANA_JS + '\n/* ---------------- INIT ---------------- */')

with open('nihongo0.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("nihongo0.html built successfully.")
