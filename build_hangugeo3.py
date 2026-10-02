#!/usr/bin/env python3
import json
import re

STORY_JS = """const STORY = [
  {id:"st1", zh:"주말에 친구와 함께 전통시장에 갑니다.", py:"Ju-mal-e chin-gu-wa ham-kke jeon-tong-si-jang-e gam-ni-da.", en:"On the weekend, I go to the traditional market with my friend.", jp:"周末和朋友一起去传统市场。"},
  {id:"st2", zh:"시장에는 맛있는 음식이 정말 많습니다.", py:"Si-jang-e-neun mas-it-neun eum-sig-i jeong-mal man-seum-ni-da.", en:"There is really a lot of delicious food in the market.", jp:"市场里美味的食物真的很多。"},
  {id:"st3", zh:"우리는 분식집에서 떡볶이와 김밥을 주문해요.", py:"U-ri-neun bun-sik-jip-e-seo tteok-bok-ki-wa gim-bab-eul ju-mun-hae-yo.", en:"We order tteokbokki and kimbap at the snack restaurant.", jp:"我们在小吃店点辣炒年糕和紫菜包饭。"},
  {id:"st4", zh:"매콤하고 달콤한 떡볶이가 아주 맛있어요.", py:"Mae-kom-ha-go dal-kom-han tteok-bok-ki-ga a-ju mas-it-eo-yo.", en:"The spicy and sweet tteokbokki is very delicious.", jp:"微辣带甜的炒年糕非常美味。"},
  {id:"st5", zh:"따뜻한 어묵 국물도 한 컵 마십니다.", py:"Tta-tteut-han eo-muk guk-mul-do han keop ma-sim-ni-da.", en:"I also drink a cup of warm fish cake broth.", jp:"温热的鱼饼汤也喝上一杯。"},
  {id:"st6", zh:"후식으로 달콤하고 바삭한 호떡을 사 먹어요.", py:"Hu-sig-eu-ro dal-kom-ha-go ba-sak-han ho-tteog-eul sa meog-eo-yo.", en:"For dessert, we buy and eat sweet, crispy hotteok.", jp:"作为甜点，买香甜酥脆的糖饼吃。"},
  {id:"st7", zh:"이모님, 정말 잘 먹었습니다! 인사해요.", py:"I-mo-nim, jeong-mal jal meog-eot-seum-ni-da! In-sa-hae-yo.", en:"Auntie, thank you for the wonderful meal! We greet politely.", jp:"阿姨，真的吃得很好！礼貌地道谢。"},
  {id:"st8", zh:"배도 부르고 기분도 참 행복합니다.", py:"Bae-do bu-reu-go gi-bun-do cham haeng-bok-ham-ni-da.", en:"My belly is full and I feel truly happy.", jp:"肚子吃得饱饱的，心情也特别幸福。"}
];"""

CHARACTERS_JS = """const CHARACTERS = [
  {id:"zi1", zh:"맛", py:"mat", hanja:"味/固有", cho:"ㅁ", jung:"ㅏ", jong:"ㅅ", words:"맛있다 (好吃), 맛집 (名吃店), 손맛 (厨艺/手艺)", meaning:"Taste / Flavor", context:"시장에는 맛있는 음식이 정말 많습니다"},
  {id:"zi2", zh:"음", py:"eum", hanja:"飮/音", cho:"ㅇ", jung:"ㅡ", jong:"ㅁ", words:"음식 (食物), 음료수 (饮料), 음악 (音乐)", meaning:"Food / Drink", context:"시장에는 맛있는 음식이 정말 많습니다"},
  {id:"zi3", zh:"식", py:"sik", hanja:"食/式", cho:"ㅅ", jung:"ㅣ", jong:"ㄱ", words:"음식 (饮食), 분식 (小吃), 식당 (餐馆)", meaning:"Food / Meal", context:"우리는 분식집에서 떡볶이와 김밥을 주문해요"},
  {id:"zi4", zh:"장", py:"jang", hanja:"場/市", cho:"ㅈ", jung:"ㅏ", jong:"ㅇ", words:"시장 (市场), 전통시장 (传统市场), 광장 (广场)", meaning:"Market / Place", context:"주말에 친구와 함께 전통시장에 갑니다"},
  {id:"zi5", zh:"떡", py:"tteok", hanja:"固有 (年糕)", cho:"ㄸ", jung:"ㅓ", jong:"ㄱ", words:"떡볶이 (炒年糕), 호떡 (糖饼), 꿀떡 (蜜年糕)", meaning:"Rice Cake", context:"우리는 분식집에서 떡볶이와 김밥을 주문해요"},
  {id:"zi6", zh:"김", py:"gim", hanja:"金/固有 (紫菜)", cho:"ㄱ", jung:"ㅣ", jong:"ㅁ", words:"김밥 (紫菜包饭), 김치 (泡菜), 조미김 (烤海苔)", meaning:"Seaweed / Laver", context:"우리는 분식집에서 떡볶이와 김밥을 주문해요"},
  {id:"zi7", zh:"주", py:"ju", hanja:"注/主/周", cho:"ㅈ", jung:"ㅜ", jong:null, words:"주문 (点餐), 주인 (主人), 주말 (周末)", meaning:"Order / Pour", context:"우리는 분식집에서 떡볶이와 김밥을 주문해요"},
  {id:"zi8", zh:"문", py:"mun", hanja:"文/問/門", cho:"ㅁ", jung:"ㅜ", jong:"ㄴ", words:"주문 (点餐/订购), 질문 (提问), 동대문 (东大门)", meaning:"Order / Gate", context:"우리는 분식집에서 떡볶이와 김밥을 주문해요"},
  {id:"zi9", zh:"물", py:"mul", hanja:"水/物", cho:"ㅁ", jung:"ㅜ", jong:"ㄹ", words:"국물 (汤汁), 생수 (矿泉水), 선물 (礼物)", meaning:"Water / Broth", context:"따뜻한 어묵 국물도 한 컵 마십니다"},
  {id:"zi10", zh:"복", py:"bok", hanja:"福/復", cho:"ㅂ", jung:"ㅗ", jong:"ㄱ", words:"행복 (幸福), 새해 복 (新年福气), 복주머니 (福袋)", meaning:"Blessing / Fortune", context:"배도 부르고 기분도 참 행복합니다"},
  {id:"zi11", zh:"행", py:"haeng", hanja:"幸/行", cho:"ㅎ", jung:"ㅐ", jong:"ㅇ", words:"행복 (幸福), 여행 (旅行), 은행 (银行)", meaning:"Happiness / Travel", context:"배도 부르고 기분도 참 행복합니다"},
  {id:"zi12", zh:"말", py:"mal", hanja:"末/固有 (语)", cho:"ㅁ", jung:"ㅏ", jong:"ㄹ", words:"주말 (周末), 한국말 (韩国话), 인사말 (问候语)", meaning:"Weekend / Word", context:"주말에 친구와 함께 전통시장에 갑니다"}
];"""

WORDS_JS = """const WORDS = [
  {id:"ci1", zh:"시장", py:"si-jang", meaning:"market / bazaar", meaningJp:"市场、集市", emoji:"🏬", context:"주말에 친구와 함께 전통시장에 갑니다", tag:"场所"},
  {id:"ci2", zh:"음식", py:"eum-sik", meaning:"food / cuisine", meaningJp:"食物、料理", emoji:"🍲", context:"시장에는 맛있는 음식이 정말 많습니다", tag:"饮食"},
  {id:"ci3", zh:"분식집", py:"bun-sik-jip", meaning:"snack restaurant", meaningJp:"小吃店、便餐店", emoji:"🏪", context:"우리는 분식집에서 떡볶이와 김밥을 주문해요", tag:"场所"},
  {id:"ci4", zh:"주문", py:"ju-mun", meaning:"order / ordering", meaningJp:"点单、点餐", emoji:"📋", context:"떡볶이와 김밥을 주문해요", tag:"动作"},
  {id:"ci5", zh:"국물", py:"guk-mul", meaning:"broth / soup", meaningJp:"汤水、汤汁", emoji:"🥣", context:"따뜻한 어묵 국물도 한 컵 마십니다", tag:"饮食"},
  {id:"ci6", zh:"후식", py:"hu-sik", meaning:"dessert", meaningJp:"甜点、饭后点心", emoji:"🍮", context:"후식으로 달콤하고 바삭한 호떡을 사 먹어요", tag:"饮食"},
  {id:"ci7", zh:"이모님", py:"i-mo-nim", meaning:"auntie (friendly restaurant call)", meaningJp:"阿姨、姨母(亲切称谓)", emoji:"👩", context:"이모님, 정말 잘 먹었습니다! 인사해요", tag:"称谓"},
  {id:"ci8", zh:"주말", py:"ju-mal", meaning:"weekend", meaningJp:"周末", emoji:"🗓️", context:"주말에 친구와 함께 전통시장에 갑니다", tag:"时间"},
  {id:"ci9", zh:"행복", py:"haeng-bok", meaning:"happiness", meaningJp:"幸福、快乐", emoji:"✨", context:"배도 부르고 기분도 참 행복합니다", tag:"情感"},
  {id:"ci10", zh:"맛있다", py:"mas-it-da", meaning:"delicious / tasty", meaningJp:"好吃、美味", emoji:"😋", context:"매콤하고 달콤한 떡볶이가 아주 맛있어요", tag:"形容"},
  {id:"ci11", zh:"맵다", py:"maep-da", meaning:"spicy / hot", meaningJp:"辣", emoji:"🌶️", context:"매콤한 떡볶이가 아주 맛있어요", tag:"形容"},
  {id:"ci12", zh:"달다", py:"dal-da", meaning:"sweet", meaningJp:"甜、香甜", emoji:"🍯", context:"달콤한 호떡을 사 먹어요", tag:"形容"}
];"""

PROPER_NOUNS_JS = """const PROPER_NOUNS = [
  {id:"pn1", zh:"떡볶이", py:"tteok-bok-ki", meaning:"spicy rice cake (tteokbokki)", meaningJp:"辣炒年糕", emoji:"🍢", context:"우리는 분식집에서 떡볶이와 김밥을 주문해요", tag:"美食"},
  {id:"pn2", zh:"김밥", py:"gim-bap", meaning:"seaweed rice roll (kimbap)", meaningJp:"紫菜包饭", emoji:"🍙", context:"우리는 분식집에서 떡볶이와 김밥을 주문해요", tag:"美食"},
  {id:"pn3", zh:"어묵", py:"eo-muk", meaning:"fish cake (odeng)", meaningJp:"鱼饼、鱼糕", emoji:"🍥", context:"따뜻한 어묵 국물도 한 컵 마십니다", tag:"美食"},
  {id:"pn4", zh:"호떡", py:"ho-tteok", meaning:"sweet filled pancake (hotteok)", meaningJp:"糖饼、香甜油饼", emoji:"🥞", context:"후식으로 달콤하고 바삭한 호떡을 사 먹어요", tag:"美食"},
  {id:"pn5", zh:"비빔밥", py:"bi-bim-bap", meaning:"mixed rice (bibimbap)", meaningJp:"韩式拌饭", emoji:"🥗", context:"한국의 대표적인 전통 건강식 비빔밥", tag:"美食"},
  {id:"pn6", zh:"라면", py:"ra-myeon", meaning:"ramen / instant noodles", meaningJp:"拉面、方便面", emoji:"🍜", context:"얼큰하고 쫄깃쫄깃한 라면 한 그릇", tag:"美食"},
  {id:"pn7", zh:"물냉면", py:"mul-naeng-myeon", meaning:"cold buckwheat noodles", meaningJp:"水冷面", emoji:"🧊", context:"살얼음 동동 시원한 물냉면", tag:"美食"}
];"""

SCRAMBLE_JS = """const SCRAMBLE_SENTENCES = [
  {
    id: "sent1",
    zh: "맛있는 음식을 친구와 함께 나누어 먹는 것은 큰 기쁨입니다.",
    tokens: ["맛있는 음식을", "친구와 함께", "나누어 먹는 것은", "큰 기쁨입니다."],
    isKey: true
  },
  {
    id: "st1",
    zh: "주말에 친구와 함께 전통시장에 갑니다.",
    tokens: ["주말에", "친구와 함께", "전통시장에", "갑니다."]
  },
  {
    id: "st3",
    zh: "우리는 분식집에서 떡볶이와 김밥을 주문해요.",
    tokens: ["우리는", "분식집에서", "떡볶이와 김밥을", "주문해요."]
  },
  {
    id: "st4",
    zh: "매콤하고 달콤한 떡볶이가 아주 맛있어요.",
    tokens: ["매콤하고 달콤한", "떡볶이가", "아주 맛있어요."]
  },
  {
    id: "st7",
    zh: "이모님, 정말 잘 먹었습니다! 인사해요.",
    tokens: ["이모님,", "정말 잘 먹었습니다!", "인사해요."]
  }
];"""

QUIZ_JS = """const QUIZ = [
  {q:"민우는 주말에 누구와 어디에 갑니까?", opts:["혼자 도서관 (独自去图书馆)", "친구와 전통시장 (和朋友去传统市场)", "동생과 수영장", "가족과 공항"], a:1},
  {q:"분식집에서 먼저 주문한 두 가지 음식은 무엇입니까?", opts:["피자와 콜라", "커피와 케이크", "떡볶이와 김밥 (辣炒年糕和紫菜包饭)", "삼계탕과 냉면"], a:2},
  {q:"떡볶이의 맛은 어떠했습니까?", opts:["매콤하고 달콤해요 (微辣带甜)", "너무 짜요 (太咸)", "쓰고 떫어요 (苦涩)", "아무 맛도 안 나요"], a:0},
  {q:"음식을 먹으며 함께 따뜻하게 마신 것은 무엇입니까?", opts:["시원한 콜라", "차가운 우유", "따뜻한 어묵 국물 (温热的鱼饼汤)", "녹차"], a:2},
  {q:"식사 후 달콤한 ‘후식’(디저트)으로 사 먹은 음식은?", opts:["아이스크림", "달콤하고 바삭한 호떡 (香甜酥脆的糖饼)", "초콜릿", "과일 주스"], a:1},
  {q:"식사를 마친 후 식당 이모님께 드린 한국어 감사의 인사는?", opts:["안녕하세요", "죄송합니다", "잘 먹었습니다! (多谢款待/吃得很好)", "안녕히 계세요"], a:2},
  {q:"글자 ‘떡’의 초성인 ‘ㄸ’은 한글에서 무엇이라고 부릅니까?", opts:["쌍자음 (双辅音)", "단모음 (单元音)", "받침 (终声收音)", "이중모음"], a:0},
  {q:"한국의 분식집이나 식당에서 친근하게 여주인님을 부르는 호칭은?", opts:["선생님 (老师)", "이모님 / 이모 (姨母/阿姨)", "대통령", "동생"], a:1},
];"""

CLOZE_JS = """const CLOZE_QUESTIONS = [
  {
    id: "kr3_c1",
    type: "text",
    before: "주말에 친구",
    answer: "와",
    after: " 함께 전통시장에 갑니다.",
    py: "Ju-mal-e chin-gu-wa ham-kke jeon-tong-si-jang-e gam-ni-da.",
    en: "On the weekend, I go to the traditional market with my friend.",
    jp: "周末和朋友一起去传统市场。",
    options: ["와", "과", "를", "에서"],
    hint: "语法助词 · 无收音名词后用伴随助词「와」(和...)",
    audioId: "st1"
  },
  {
    id: "kr3_c2",
    type: "text",
    before: "주말에 친구와 함께 전통시장",
    answer: "에",
    after: " 갑니다.",
    py: "Ju-mal-e chin-gu-wa ham-kke jeon-tong-si-jang-e gam-ni-da.",
    en: "On the weekend, I go to the traditional market with my friend.",
    jp: "周末和朋友一起去传统市场。",
    options: ["에", "에서", "을", "의"],
    hint: "语法助词 · 接在去向目的地名词后的方向助词「에」",
    audioId: "st1"
  },
  {
    id: "kr3_c3",
    type: "text",
    before: "",
    answer: "시장",
    after: "에는 맛있는 음식이 정말 많습니다.",
    py: "Si-jang-e-neun mas-it-neun eum-sig-i jeong-mal man-seum-ni-da.",
    en: "There is really a lot of delicious food in the market.",
    jp: "市场里美味的食物真的很多。",
    options: ["시장", "병원", "도서관", "운동장"],
    hint: "课文核心词 · 表示商品与美食交易的「市场」",
    audioId: "st2"
  },
  {
    id: "kr3_c4",
    type: "text",
    before: "시장에는 맛있는 음식",
    answer: "이",
    after: " 정말 많습니다.",
    py: "Si-jang-e-neun mas-it-neun eum-sig-i jeong-mal man-seum-ni-da.",
    en: "There is really a lot of delicious food in the market.",
    jp: "市场里美味的食物真的很多。",
    options: ["이", "가", "을", "를"],
    hint: "语法助词 · 有收音的名词后用主格助词「이」",
    audioId: "st2"
  },
  {
    id: "kr3_c5",
    type: "text",
    before: "우리는 분식집",
    answer: "에서",
    after: " 떡볶이와 김밥을 주문해요.",
    py: "U-ri-neun bun-sik-jip-e-seo tteok-bok-ki-wa gim-bab-eul ju-mun-hae-yo.",
    en: "We order tteokbokki and kimbap at the snack restaurant.",
    jp: "我们在小吃店点辣炒年糕和紫菜包饭。",
    options: ["에서", "에", "로", "과"],
    hint: "语法助词 · 表示动作进行场所的助词「에서」(在...)",
    audioId: "st3"
  },
  {
    id: "kr3_c6",
    type: "text",
    before: "우리는 분식집에서 떡볶이와 김밥",
    answer: "을",
    after: " 주문해요.",
    py: "U-ri-neun bun-sik-jip-e-seo tteok-bok-ki-wa gim-bab-eul ju-mun-hae-yo.",
    en: "We order tteokbokki and kimbap at the snack restaurant.",
    jp: "我们在小吃店点辣炒年糕和紫菜包饭。",
    options: ["을", "를", "이", "가"],
    hint: "语法助词 · 有收音的名词后用宾格助词「을」",
    audioId: "st3"
  },
  {
    id: "kr3_c7",
    type: "text",
    before: "매콤하",
    answer: "고",
    after: " 달콤한 떡볶이가 아주 맛있어요.",
    py: "Mae-kom-ha-go dal-kom-han tteok-bok-ki-ga a-ju mas-it-eo-yo.",
    en: "The spicy and sweet tteokbokki is very delicious.",
    jp: "微辣带甜的炒年糕非常美味。",
    options: ["고", "면", "지만", "며"],
    hint: "语法连接词尾 · 表示两个形容词并列并存的「-고」",
    audioId: "st4"
  },
  {
    id: "kr3_c8",
    type: "text",
    before: "따뜻한 ",
    answer: "어묵",
    after: " 국물도 한 컵 마십니다.",
    py: "Tta-tteut-han eo-muk guk-mul-do han keop ma-sim-ni-da.",
    en: "I also drink a cup of warm fish cake broth.",
    jp: "温热的鱼饼汤也喝上一杯。",
    options: ["어묵", "사탕", "수박", "초콜릿"],
    hint: "韩国特色传统小吃 · 串在竹签上的「鱼饼/鱼糕」",
    audioId: "st5"
  },
  {
    id: "kr3_c9",
    type: "text",
    before: "후식",
    answer: "으로",
    after: " 달콤하고 바삭한 호떡을 사 먹어요.",
    py: "Hu-sig-eu-ro dal-kom-ha-go ba-sak-han ho-tteog-eul sa meog-eo-yo.",
    en: "For dessert, we buy and eat sweet, crispy hotteok.",
    jp: "作为甜点，买香甜酥脆的糖饼吃。",
    options: ["으로", "에서", "와", "는"],
    hint: "语法助词 · 表示身份、用途或资格的助词「-(으)로」(作为...)",
    audioId: "st6"
  },
  {
    id: "kr3_c10",
    type: "text",
    before: "달콤하고 바삭한 호떡을 ",
    answer: "사 먹어요",
    after: ".",
    py: "Hu-sig-eu-ro dal-kom-ha-go ba-sak-han ho-tteog-eul sa meog-eo-yo.",
    en: "For dessert, we buy and eat sweet, crispy hotteok.",
    jp: "作为甜点，买香甜酥脆的糖饼吃。",
    options: ["사 먹어요", "버려요", "그려요", "던져요"],
    hint: "复合动词表达 · 表示「买来吃」日常表达",
    audioId: "st6"
  },
  {
    id: "kr3_c11",
    type: "text",
    before: "이모님, 정말 ",
    answer: "잘 먹었습니다",
    after: "! 인사해요.",
    py: "I-mo-nim, jeong-mal jal meog-eot-seum-ni-da! In-sa-hae-yo.",
    en: "Auntie, thank you for the wonderful meal! We greet politely.",
    jp: "阿姨，真的吃得很好！礼貌地道谢。",
    options: ["잘 먹었습니다", "안녕히 가세요", "처음 뵙겠습니다", "축하합니다"],
    hint: "韩国用餐经典礼仪 · 饭后向主人表达美味与感谢的常用语",
    audioId: "st7"
  },
  {
    id: "kr3_c12",
    type: "text",
    before: "배도 부르고 기분도 참 ",
    answer: "행복합니다",
    after: ".",
    py: "Bae-do bu-reu-go gi-bun-do cham haeng-bok-ham-ni-da.",
    en: "My belly is full and I feel truly happy.",
    jp: "肚子吃得饱饱的，心情也特别幸福。",
    options: ["행복합니다", "슬픕니다", "어렵습니다", "춥습니다"],
    hint: "情感形容词 · 表示「幸福、满心喜悦」的格式体敬语",
    audioId: "st8"
  }
];"""

with open('/home/ubuntu/ws/jump-jump-game/hangugeo2.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace title & header
c = c.replace('<title>나의 하루 - 韩国语课文识字闯关 (My Day in Korea)</title>', '<title>맛있는 한국 음식 - 韩国语课文识字闯关 (Delicious Korean Food)</title>')
c = c.replace('<h1 id="topTitle">나의 하루</h1>', '<h1 id="topTitle">맛있는 한국 음식</h1>')

# Replace home banner & svg
old_home_header = '''      <div class="palace-ico" aria-label="时钟与一日">
        <svg viewBox="0 0 64 64" width="60" height="60" xmlns="http://www.w3.org/2000/svg">
          <circle cx="32" cy="32" r="26" fill="#ffffff" stroke="#1d4ed8" stroke-width="3.5"/>
          <circle cx="32" cy="32" r="3" fill="#1d4ed8"/>
          <line x1="32" y1="32" x2="32" y2="14" stroke="#dc2626" stroke-width="3.5" stroke-linecap="round"/>
          <line x1="32" y1="32" x2="45" y2="39" stroke="#1d4ed8" stroke-width="3.5" stroke-linecap="round"/>
          <circle cx="32" cy="8" r="1.5" fill="#dc2626"/>
          <circle cx="56" cy="32" r="1.5" fill="#1d4ed8"/>
          <circle cx="32" cy="56" r="1.5" fill="#dc2626"/>
          <circle cx="8" cy="32" r="1.5" fill="#1d4ed8"/>
        </svg>
      </div>
      <div style="display:flex;gap:8px;margin-top:4px;">
        <a href="hangugeo.html" style="font-size:12px;font-weight:700;padding:4px 10px;border-radius:12px;background:#fff;border:1.5px solid #bfdbfe;color:#1d4ed8;text-decoration:none;">◀ 第1课: 나의 일주일</a>
        <span style="font-size:12px;font-weight:800;padding:4px 10px;border-radius:12px;background:#1d4ed8;color:#fff;">第2课: 나의 하루</span>
      </div>
      <h2 class="title">나의 하루 (My Day)</h2>
      <p class="sub">跟随原创韩语课文走进韩国学生的一天生活！学习常用时间表达、日常活动句型与12个核心音节字块。本课是《나의 일주일》的续篇。</p>'''

new_home_header = '''      <div class="palace-ico" aria-label="美味韩食与传统市场">
        <svg viewBox="0 0 64 64" width="60" height="60" xmlns="http://www.w3.org/2000/svg">
          <circle cx="32" cy="32" r="28" fill="#fff7ed" stroke="#ea580c" stroke-width="2.5"/>
          <path d="M14 28 Q32 20 50 28 L46 48 Q32 54 18 48 Z" fill="#c2410c"/>
          <path d="M16 29 Q32 24 48 29 Q32 34 16 29 Z" fill="#f97316"/>
          <path d="M26 20 Q24 14 26 10" stroke="#f97316" stroke-width="2" stroke-linecap="round" fill="none"/>
          <path d="M32 18 Q34 12 32 8" stroke="#ea580c" stroke-width="2.5" stroke-linecap="round" fill="none"/>
          <path d="M38 20 Q36 14 38 10" stroke="#f97316" stroke-width="2" stroke-linecap="round" fill="none"/>
          <circle cx="32" cy="31" r="3" fill="#fef08a"/>
        </svg>
      </div>
      <div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap;justify-content:center;">
        <a href="hangugeo.html" style="font-size:12px;font-weight:700;padding:4px 10px;border-radius:12px;background:#fff;border:1.5px solid #bfdbfe;color:#1d4ed8;text-decoration:none;">◀ 第1课: 나의 일주일</a>
        <a href="hangugeo2.html" style="font-size:12px;font-weight:700;padding:4px 10px;border-radius:12px;background:#fff;border:1.5px solid #bfdbfe;color:#1d4ed8;text-decoration:none;">◀ 第2课: 나의 하루</a>
        <span style="font-size:12px;font-weight:800;padding:4px 10px;border-radius:12px;background:#ea580c;color:#fff;">第3课: 맛있는 한국 음식</span>
      </div>
      <h2 class="title">맛있는 한국 음식 (Delicious Korean Food)</h2>
      <p class="sub">跟随敏宇走进热闹非凡的韩国传统市场！探索经典街头小吃、餐厅点餐交流、双辅音与12个核心音节字块。本课是《나의 하루》的精彩续篇。</p>'''

if old_home_header in c:
    c = c.replace(old_home_header, new_home_header)
else:
    print("Warning: old_home_header not matched exactly")

c = c.replace('<div class="desc">19个常用词与时间表达</div>', '<div class="desc">19个餐饮美食与日常词汇</div>')

# Replace Data Definitions
data_start_mark = "/* ---------------- DATA DEFINITIONS ---------------- */"
data_end_mark = "const ALL_VOCAB = [...WORDS, ...PROPER_NOUNS];"

# Let's locate the entire data block between data_start_mark and audio_dir
start_pos = c.find(data_start_mark)
if start_pos != -1:
    end_pos = c.find("/* ---------------- GLOBAL STATE ---------------- */", start_pos)
    if end_pos != -1:
        new_data_section = f"""{data_start_mark}
// 1. 课文《맛있는 한국 음식》(Delicious Korean Food · A1/TOPIK 1入门 · 续《나의 하루》)
{STORY_JS}

// 2. 课后核心音节字块 (12 Syllable Blocks)
{CHARACTERS_JS}

// 3. 课后核心生词 (12 Words)
{WORDS_JS}

// 4. 课后「韩国美食」词表 (7 Thematic Food Words)
{PROPER_NOUNS_JS}

const ALL_VOCAB = [...WORDS, ...PROPER_NOUNS];

// 5. 课后重点句子打散重组 (5 Sentences)
{SCRAMBLE_JS}

// 6. 故事与韩语常识问答 (8 Questions)
{QUIZ_JS}

// 7. 选词填空 (12 Questions: 课文句式 + 助词用法)
{CLOZE_JS}

"""
        c = c[:start_pos] + new_data_section + c[end_pos:]
        print("Successfully replaced data definitions!")
    else:
        print("Error: Could not find GLOBAL STATE marker")
else:
    print("Error: Could not find data definitions marker")

# Replace storage keys & audio directories
c = c.replace("hangugeo2_progress", "hangugeo3_progress")
c = c.replace("hangugeo2_srs", "hangugeo3_srs")
c = c.replace("'hangugeo2_'", "'hangugeo3_'")
c = c.replace('"hangugeo2_"', '"hangugeo3_"')
c = c.replace("hangugeo2_", "hangugeo3_")
c = c.replace("audio/hangugeo2/", "audio/hangugeo3/")
c = c.replace("audio/hangugeo2_en/", "audio/hangugeo3_en/")
c = c.replace("audio/hangugeo2_zh/", "audio/hangugeo3_zh/")

with open('/home/ubuntu/ws/jump-jump-game/hangugeo3.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Generated hangugeo3.html successfully! Size:", len(c))
