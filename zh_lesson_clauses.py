#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clause-level (分句) data for the original Chinese situational lessons zh0–zh7.

Used by:
- build_chinese_lessons.py      → merges the Korean sentence translation (`ko`) into STORY
- generate_zh_clause_audio.py   → clause MP3s + Korean story MP3s + data/zh-lesson-clauses.js

Per lesson: one entry per STORY sentence (same order as LESSONS[*]["story"]):
    (sentence_ko, [(zh, py, en, jp, ko), ...])
The clause `zh` pieces must concatenate exactly to the sentence `zh` (checked by validate()).
Clause translations are hand-aligned so the ClausePlayer focus card shows a matching meaning.
"""

CLAUSES = {
    # ---------------- 第0课 拼音与日常问候 ----------------
    "zh0": [
        ("병음은 한자의 날개예요. 즐겁게 중국어를 배우기 시작해요.", [
            ("拼音是汉字的翅膀，", "Pīnyīn shì hànzì de chìbǎng,", "Pinyin is the wings of Chinese characters;", "ピンインは漢字の翼です。", "병음은 한자의 날개예요."),
            ("让我们开始快乐学中文。", "ràng wǒmen kāishǐ kuàilè xué zhōngwén.", "let's begin learning Chinese happily.", "楽しく中国語を学び始めましょう。", "즐겁게 중국어를 배우기 시작해요."),
        ]),
        ("아침에 만나면, 웃으며 \"좋은 아침\"이라고 말해요!", [
            ("早晨相遇，", "Zǎochén xiāngyù,", "Meeting in the morning,", "朝会ったら、", "아침에 만나면,"),
            ("微笑着说一声“早上好”！", "wēixiàozhe shuō yì shēng “Zǎoshang hǎo”!", "say “Good morning” with a bright smile!", "笑顔で「おはようございます」と言いましょう！", "웃으며 \"좋은 아침\"이라고 말해요!"),
        ]),
        ("친구를 만나면, 반갑게 \"안녕\"이라고 인사해요!", [
            ("朋友见面，", "Péngyou jiànmiàn,", "When meeting friends,", "友達に会ったら、", "친구를 만나면,"),
            ("热情地打招呼“你好”！", "rèqíng de dǎ zhāohu “Nǐ hǎo”!", "warmly greet them with “Hello”!", "元気に「こんにちは」と挨拶します！", "반갑게 \"안녕\"이라고 인사해요!"),
        ]),
        ("밤이 오면, 따뜻하게 \"좋은 저녁\"이라고 인사해요.", [
            ("夜幕降临，", "Yèmù jiànglín,", "When night falls,", "夜が来たら、", "밤이 오면,"),
            ("道一声温暖的“晚上好”。", "dào yì shēng wēnnuǎn de “Wǎnshang hǎo”.", "send a warm greeting: “Good evening”.", "温かく「こんばんは」と声をかけます。", "따뜻하게 \"좋은 저녁\"이라고 인사해요."),
        ]),
        ("도움을 받으면, 진심으로 \"고마워요\"라고 말해요.", [
            ("得到帮助，", "Dédào bāngzhù,", "When receiving help,", "助けてもらったら、", "도움을 받으면,"),
            ("真诚地说一声“谢谢”。", "zhēnchéng de shuō yì shēng “Xièxie”.", "sincerely say “Thank you”.", "心を込めて「ありがとう」と言います。", "진심으로 \"고마워요\"라고 말해요."),
        ]),
        ("예의 바르게 대답하며, 부드럽게 \"천만에요\"라고 말해요.", [
            ("礼貌回应，", "Lǐmào huíyìng,", "Politely respond", "礼儀正しく、", "예의 바르게 대답하며,"),
            ("温和地说“不客气”。", "wēnhé de shuō “Bú kèqi”.", "and gently say “You're welcome”.", "優しく「どういたしまして」と返します。", "부드럽게 \"천만에요\"라고 말해요."),
        ]),
        ("실수로 잘못했다면, 먼저 \"미안해요\"라고 말해요.", [
            ("如果不小心做错了，", "Rúguǒ bù xiǎoxīn zuòcuò le,", "If you accidentally make a mistake,", "うっかり間違えたら、", "실수로 잘못했다면,"),
            ("主动说“对不起”。", "zhǔdòng shuō “Duìbuqǐ”.", "take the initiative to say “Sorry”.", "自分から「ごめんなさい」と言います。", "먼저 \"미안해요\"라고 말해요."),
        ]),
        ("서로 이해하고 감싸 주며, 손을 흔들며 \"안녕히 가세요\"라고 말해요!", [
            ("互相理解与包容，", "Hùxiāng lǐjiě yǔ bāoróng,", "Understanding and forgiving each other,", "お互いに理解し合い、", "서로 이해하고 감싸 주며,"),
            ("挥挥手说“再见”！", "huīhui shǒu shuō “Zàijiàn”!", "wave and say “Goodbye”!", "手を振って「さようなら」と言いましょう！", "손을 흔들며 \"안녕히 가세요\"라고 말해요!"),
        ]),
    ],

    # ---------------- 第1课 我的一星期 ----------------
    "zh1": [
        ("월요일, 아침 해가 떠오르고, 우리는 책가방을 메고 신나게 학교에 가요.", [
            ("星期一，", "Xīngqīyī,", "On Monday,", "月曜日、", "월요일,"),
            ("朝阳升起，", "zhāoyáng shēngqǐ,", "the morning sun rises,", "朝の光が昇り、", "아침 해가 떠오르고,"),
            ("我们背上书包高高兴兴去学校。", "wǒmen bēishang shūbāo gāogāoxìngxìng qù xuéxiào.", "and we carry our schoolbags happily to school.", "私たちはランドセルを背負って元気に登校します。", "우리는 책가방을 메고 신나게 학교에 가요."),
        ]),
        ("화요일, 우리는 밝은 교실에서 열심히 수업을 듣고 중국어를 배워요.", [
            ("星期二，", "Xīngqī'èr,", "On Tuesday,", "火曜日、", "화요일,"),
            ("我们在明亮的教室里认真听讲、", "wǒmen zài míngliàng de jiàoshì lǐ rènzhēn tīngjiǎng,", "we listen attentively in the bright classroom", "私たちは明るい教室で真剣に先生の話を聞き、", "우리는 밝은 교실에서 열심히 수업을 듣고,"),
            ("学习中文。", "xuéxí zhōngwén.", "and study Chinese.", "中国語を学びます。", "중국어를 배워요."),
        ]),
        ("수요일, 수업이 끝나면 나는 친구들과 운동장에서 아름다운 음악을 들어요.", [
            ("星期三，", "Xīngqīsān,", "On Wednesday,", "水曜日、", "수요일,"),
            ("下课后我和同学们在操场上听优美的音乐。", "xiàkè hòu wǒ hé tóngxuémen zài cāochǎng shang tīng yōuměi de yīnyuè.", "after class my classmates and I listen to beautiful music on the playground.", "放課後にクラスメイトとグラウンドで美しい音楽を聴きます。", "수업이 끝나면 나는 친구들과 운동장에서 아름다운 음악을 들어요."),
        ]),
        ("목요일, 우리는 조용한 도서관에 들어가, 재미있게 책을 읽어요.", [
            ("星期四，", "Xīngqīsì,", "On Thursday,", "木曜日、", "목요일,"),
            ("我们走进安静的图书馆，", "wǒmen zǒujìn ānjìng de túshūguǎn,", "we walk into the quiet library", "私たちは静かな図書館に入り、", "우리는 조용한 도서관에 들어가,"),
            ("津津有味地看书。", "jīnjīnyǒuwèi de kàn shū.", "and read books with keen interest.", "夢中になって本を読みます。", "재미있게 책을 읽어요."),
        ]),
        ("금요일, 모두 함께 노래하고 춤추며, 즐겁게 주말을 맞이해요.", [
            ("星期五，", "Xīngqīwǔ,", "On Friday,", "金曜日、", "금요일,"),
            ("大家一起唱歌跳舞，", "dàjiā yìqǐ chàng gē tiào wǔ,", "everyone sings and dances together,", "みんなで歌って踊り、", "모두 함께 노래하고 춤추며,"),
            ("开开心心迎接周末。", "kāikāixīnxīn yíngjiē zhōumò.", "joyfully welcoming the weekend.", "楽しく週末を迎えます。", "즐겁게 주말을 맞이해요."),
        ]),
        ("토요일, 나는 엄마 아빠와 공원에 산책하러 가서, 활짝 핀 꽃을 봐요.", [
            ("星期六，", "Xīngqīliù,", "On Saturday,", "土曜日、", "토요일,"),
            ("我和爸爸妈妈去公园散步，", "wǒ hé bàba māma qù gōngyuán sànbù,", "my parents and I go for a walk in the park,", "私は両親と公園へ散歩に行き、", "나는 엄마 아빠와 공원에 산책하러 가서,"),
            ("看盛开的鲜花。", "kàn shèngkāi de xiānhuā.", "admiring the blooming flowers.", "満開の花を眺めます。", "활짝 핀 꽃을 봐요."),
        ]),
        ("일요일, 나는 따뜻한 집에서 그림 그리는 것을 좋아하고, 쉬는 날을 즐겨요.", [
            ("星期天，", "Xīngqītiān,", "On Sunday,", "日曜日、", "일요일,"),
            ("我喜欢坐在温暖的家里画画，", "wǒ xǐhuan zuò zài wēnnuǎn de jiā lǐ huàhuà,", "I like sitting in my warm home drawing pictures,", "私は温かい家で絵を描いて過ごし、", "나는 따뜻한 집에서 그림 그리는 것을 좋아하고,"),
            ("享受休息日。", "xiǎngshòu xiūxirì.", "enjoying the day of rest.", "休息日を楽しみます。", "쉬는 날을 즐겨요."),
        ]),
        ("알차고 즐거운 일주일, 하루하루 얻는 것이 가득해요!", [
            ("充实又快乐的一星期，", "Chōngshí yòu kuàilè de yì xīngqī,", "A full and happy week —", "充実して楽しい一週間、", "알차고 즐거운 일주일,"),
            ("每一天都有满满的收获！", "měi yì tiān dōu yǒu mǎnmǎn de shōuhuò!", "every single day brings plenty of gains!", "毎日たくさんの収穫があります！", "하루하루 얻는 것이 가득해요!"),
        ]),
    ],

    # ---------------- 第2课 我的一天 ----------------
    "zh2": [
        ("아침 7시, 자명종이 따르릉 울리고, 나는 제시간에 일어나요.", [
            ("早上七点，", "Zǎoshang qī diǎn,", "At seven in the morning,", "朝7時、", "아침 7시,"),
            ("闹钟叮咚响了，", "nàozhōng dīngdōng xiǎng le,", "the alarm clock rings,", "目覚まし時計が鳴り、", "자명종이 따르릉 울리고,"),
            ("我准时起床。", "wǒ zhǔnshí qǐchuáng.", "and I get up on time.", "時間通りに起きます。", "나는 제시간에 일어나요."),
        ]),
        ("세수하고 이를 닦은 뒤, 나는 가족과 함께 맛있는 아침을 먹어요.", [
            ("洗脸刷牙后，", "Xǐliǎn shuāyá hòu,", "After washing my face and brushing my teeth,", "洗顔と歯磨きをして、", "세수하고 이를 닦은 뒤,"),
            ("我和家人一起吃香喷喷的早餐。", "wǒ hé jiārén yìqǐ chī xiāngpēnpēn de zǎocān.", "I eat a delicious breakfast with my family.", "家族と一緒に美味しい朝ごはんを食べます。", "나는 가족과 함께 맛있는 아침을 먹어요."),
        ]),
        ("아침 8시, 나는 책가방을 메고 집을 나서, 학교를 향해 걸어가요.", [
            ("早上八点，", "Zǎoshang bā diǎn,", "At eight o'clock,", "朝8時、", "아침 8시,"),
            ("我背着书包走出家门，", "wǒ bēizhe shūbāo zǒuchū jiāmén,", "carrying my schoolbag, I step out the door", "カバンを背負って家を出て、", "나는 책가방을 메고 집을 나서,"),
            ("向着学校走去。", "xiàngzhe xuéxiào zǒuqù.", "and walk to school.", "学校に向かって歩きます。", "학교를 향해 걸어가요."),
        ]),
        ("낮 12시, 우리는 식당에서 점심을 먹어요. 갈비와 밥이 정말 맛있어요!", [
            ("中午十二点，", "Zhōngwǔ shí'èr diǎn,", "At twelve noon,", "お昼12時、", "낮 12시,"),
            ("我们在食堂吃午饭，", "wǒmen zài shítáng chī wǔfàn,", "we eat lunch in the cafeteria;", "食堂で昼ごはんを食べます。", "우리는 식당에서 점심을 먹어요."),
            ("排骨和米饭真香！", "páigǔ hé mǐfàn zhēn xiāng!", "the ribs and rice smell so good!", "おかずとご飯がとても美味しいです！", "갈비와 밥이 정말 맛있어요!"),
        ]),
        ("오후 4시, 하교 종이 울리고, 우리는 책을 챙겨 집에 갈 준비를 해요.", [
            ("下午四点，", "Xiàwǔ sì diǎn,", "At four in the afternoon,", "午後4時、", "오후 4시,"),
            ("放学铃声响起，", "fàngxué língshēng xiǎngqǐ,", "the school bell rings,", "下校のチャイムが鳴り、", "하교 종이 울리고,"),
            ("我们收拾好书本准备回家。", "wǒmen shōushi hǎo shūběn zhǔnbèi huíjiā.", "and we pack our books, ready to go home.", "本を片付けて帰宅の準備をします。", "우리는 책을 챙겨 집에 갈 준비를 해요."),
        ]),
        ("저녁 6시 반, 온 가족이 식탁에 둘러앉아 푸짐한 저녁을 먹어요.", [
            ("傍晚六点半，", "Bàngwǎn liù diǎn bàn,", "At half past six in the evening,", "夕方6時半、", "저녁 6시 반,"),
            ("全家人围坐在餐桌旁吃丰盛的晚饭。", "quán jiārén wéizuò zài cānzhuō páng chī fēngshèng de wǎnfàn.", "the whole family sits around the table eating a hearty dinner.", "家族全員で食卓を囲み、豪華な晩ごはんを食べます。", "온 가족이 식탁에 둘러앉아 푸짐한 저녁을 먹어요."),
        ]),
        ("저녁 8시, 나는 책상 앞에서 집중해서 숙제를 해요.", [
            ("晚上八点，", "Wǎnshang bā diǎn,", "At eight in the evening,", "夜8時、", "저녁 8시,"),
            ("我在书桌前专心致志地写作业。", "wǒ zài shūzhuō qián zhuānxīnzhìzhì de xiě zuòyè.", "I concentrate on my homework at my desk.", "机に向かって集中して宿題をします。", "나는 책상 앞에서 집중해서 숙제를 해요."),
        ]),
        ("밤 9시 반, 나는 엄마 아빠께 안녕히 주무시라고 인사하고, 편안하게 잠들어요.", [
            ("晚上九点半，", "Wǎnshang jiǔ diǎn bàn,", "At half past nine at night,", "夜9時半、", "밤 9시 반,"),
            ("我对爸爸妈妈道声晚安，", "wǒ duì bàba māma dào shēng wǎn'ān,", "I say good night to Mom and Dad", "両親に「おやすみなさい」と言って、", "나는 엄마 아빠께 안녕히 주무시라고 인사하고,"),
            ("安心睡觉。", "ānxīn shuìjiào.", "and fall asleep peacefully.", "安心して眠りにつきます。", "편안하게 잠들어요."),
        ]),
    ],

    # ---------------- 第3课 中国的四季 ----------------
    "zh3": [
        ("봄이 왔어요. 산들바람이 땅을 푸르게 물들이고, 복숭아꽃과 살구꽃이 살며시 피어나요.", [
            ("春天来了，", "Chūntiān lái le,", "Spring has arrived;", "春が来ました。", "봄이 왔어요."),
            ("微风吹绿了大地，", "wēifēng chuī lǜ le dàdì,", "a gentle breeze turns the earth green,", "そよ風が大地を緑に染め、", "산들바람이 땅을 푸르게 물들이고,"),
            ("桃花和杏花悄悄盛开。", "táohuā hé xìnghuā qiāoqiāo shèngkāi.", "and peach and apricot blossoms quietly bloom.", "桃と杏の花が静かに咲き誇ります。", "복숭아꽃과 살구꽃이 살며시 피어나요."),
        ]),
        ("봄비가 흙을 촉촉이 적시고, 아이들은 풀밭에서 즐겁게 연을 날려요.", [
            ("春雨滋润着泥土，", "Chūnyǔ zīrùn zhe nítǔ,", "Spring rain nourishes the soil;", "春の雨が土を潤し、", "봄비가 흙을 촉촉이 적시고,"),
            ("小朋友们在草地上快乐地放风筝。", "xiǎopéngyoumen zài cǎodì shang kuàilè de fàng fēngzheng.", "children happily fly kites on the grass.", "子どもたちが原っぱで楽しそうに凧揚げをします。", "아이들은 풀밭에서 즐겁게 연을 날려요."),
        ]),
        ("여름 햇살은 뜨겁고, 무성한 푸른 나무가 땅에 시원한 그늘을 드리워요.", [
            ("夏天阳光热烈，", "Xiàtiān yángguāng rèliè,", "The summer sun is blazing;", "夏の陽射しは眩しく、", "여름 햇살은 뜨겁고,"),
            ("茂密的绿树给大地送来一片片阴凉。", "màomì de lǜshù gěi dàdì sòng lái yí piànpiàn yīnliáng.", "thick green trees bring patches of shade to the earth.", "青々とした木陰が涼しさをもたらします。", "무성한 푸른 나무가 땅에 시원한 그늘을 드리워요."),
        ]),
        ("연못에는 분홍빛 연꽃이 우아하게 서 있고, 우리는 나무 그늘 아래에서 시원하고 달콤한 수박을 먹어요.", [
            ("池塘里粉红的荷花亭亭玉立，", "Chítáng lǐ fěnhóng de héhuā tíngtíngyùlì,", "In the pond, pink lotuses stand gracefully;", "池にはピンクの蓮の花が美しく咲き、", "연못에는 분홍빛 연꽃이 우아하게 서 있고,"),
            ("我们在树荫下吃冰甜的西瓜。", "wǒmen zài shùyīn xià chī bīngtián de xīguā.", "we eat cold, sweet watermelon in the shade.", "木陰で冷たいスイカを食べます。", "우리는 나무 그늘 아래에서 시원하고 달콤한 수박을 먹어요."),
        ]),
        ("가을이 오면, 선선한 가을바람이 불어오고, 황금빛 나뭇잎이 나비처럼 춤을 춰요.", [
            ("秋天到了，", "Qiūtiān dào le,", "Autumn arrives;", "秋が訪れ、", "가을이 오면,"),
            ("凉爽的秋风吹过，", "liángshuǎng de qiūfēng chuī guò,", "a cool autumn wind blows by,", "爽やかな秋風が吹き抜け、", "선선한 가을바람이 불어오고,"),
            ("金黄的树叶像蝴蝶般飞舞。", "jīnhuáng de shùyè xiàng húdié bān fēiwǔ.", "and golden leaves dance like butterflies.", "黄金色の落ち葉が蝶のように舞います。", "황금빛 나뭇잎이 나비처럼 춤을 춰요."),
        ]),
        ("가을은 수확의 황금 계절, 새빨간 사과가 가지마다 주렁주렁 열려요.", [
            ("秋天是收获的黄金季节，", "Qiūtiān shì shōuhuò de huángjīn jìjié,", "Autumn is the golden season of harvest;", "秋は実りの黄金の季節、", "가을은 수확의 황금 계절,"),
            ("红彤彤的苹果挂满了枝头。", "hóngtōngtōng de píngguǒ guàmǎn le zhītóu.", "bright red apples hang heavy on the branches.", "真っ赤なリンゴが枝いっぱいに実ります。", "새빨간 사과가 가지마다 주렁주렁 열려요."),
        ]),
        ("겨울에는 온 하늘에 눈이 날리고, 새하얀 눈송이가 온 세상을 은빛으로 물들여요.", [
            ("冬天漫天飞雪，", "Dōngtiān màntiān fēixuě,", "In winter, snow fills the sky;", "冬には雪が舞い散り、", "겨울에는 온 하늘에 눈이 날리고,"),
            ("洁白的雪花把天地染成了银白色。", "jiébái de xuěhuā bǎ tiāndì rǎnchéng le yínbáisè.", "pure white snowflakes paint the world silvery white.", "真っ白な雪が世界を銀世界へと染め上げます。", "새하얀 눈송이가 온 세상을 은빛으로 물들여요."),
        ]),
        ("모두 함께 눈사람을 만들고, 섣달그믐에는 빨간 등롱을 걸고, 온 가족이 모여 새해를 맞이해요!", [
            ("大家一起堆雪人，", "Dàjiā yìqǐ duī xuěrén,", "Everyone builds snowmen together;", "みんなで雪だるまを作り、", "모두 함께 눈사람을 만들고,"),
            ("大年三十挂红灯笼、", "dà nián sānshí guà hóng dēnglong,", "on New Year's Eve, red lanterns are hung,", "大晦日には赤い提灯を掲げ、", "섣달그믐에는 빨간 등롱을 걸고,"),
            ("全家团圆迎新年！", "quánjiā tuányuán yíng xīnnián!", "and the whole family gathers to welcome the New Year!", "家族そろって新年を迎えます！", "온 가족이 모여 새해를 맞이해요!"),
        ]),
    ],

    # ---------------- 第4课 我的社区与城市 ----------------
    "zh4": [
        ("나는 아름답고 편리한 동네에 살아요.", [
            ("我住在一个美丽又便利的社区里。", "Wǒ zhù zài yí gè měilì yòu biànlì de shèqū lǐ.", "I live in a beautiful and convenient community.", "私は美しく便利なコミュニティに住んでいます。", "나는 아름답고 편리한 동네에 살아요."),
        ]),
        ("지하철역 앞에는 큰 쇼핑몰과 은행이 있어요.", [
            ("地铁站的前面，", "Dìtiězhàn de qiánmiàn,", "In front of the subway station,", "地下鉄の駅の前には、", "지하철역 앞에는"),
            ("有大型商场和银行。", "yǒu dàxíng shāngchǎng hé yínháng.", "there are large shopping malls and banks.", "大きなショッピングモールや銀行があります。", "큰 쇼핑몰과 은행이 있어요."),
        ]),
        ("매일 아침, 나는 북적이는 거리를 지나 학교에 가요.", [
            ("每天早上，", "Měitiān zǎoshang,", "Every morning,", "毎朝、", "매일 아침,"),
            ("我穿过热闹的街道去上学。", "wǒ chuānguò rènao de jiēdào qù shàngxué.", "I walk through the lively streets to school.", "賑やかな通りを抜けて学校へ行きます。", "나는 북적이는 거리를 지나 학교에 가요."),
        ]),
        ("큰길 근처에는 오래된 서점과 작은 찻집이 있어요.", [
            ("马路附近，", "Mǎlù fùjìn,", "Near the road,", "大通りの近くに、", "큰길 근처에는"),
            ("有一家古老的书店和小茶馆。", "yǒu yì jiā gǔlǎo de shūdiàn hé xiǎo cháguǎn.", "there is an old bookstore and a small teahouse.", "古い本屋と小さな茶館があります。", "오래된 서점과 작은 찻집이 있어요."),
        ]),
        ("공원 안에는 푸르른 큰 나무와 예쁜 꽃들이 있어요.", [
            ("公园里面有绿绿的大树和漂亮的花朵。", "Gōngyuán lǐmiàn yǒu lǜlǜ de dàshù hé piàoliang de huāduǒ.", "Inside the park, there are lush green trees and pretty flowers.", "公園の中には、青々とした木や綺麗な花があります。", "공원 안에는 푸르른 큰 나무와 예쁜 꽃들이 있어요."),
        ]),
        ("집 밖으로 나가면, 언제나 친절하고 다정한 이웃을 만나요.", [
            ("走出家门外，", "Zǒuchū jiāmén wài,", "Stepping outside my home,", "家の外に出ると、", "집 밖으로 나가면,"),
            ("总能遇到热情友善的邻居。", "zǒng néng yùdào rèqíng yǒushàn de línjū.", "I always meet warm and friendly neighbors.", "いつも親切で友好的なご近所さんに会います。", "언제나 친절하고 다정한 이웃을 만나요."),
        ]),
        ("주민센터 오른쪽은 우체국이고, 왼쪽은 의원이에요.", [
            ("社区服务站的右边是邮局，", "Shèqū fúwùzhàn de yòubian shì yóujú,", "To the right of the community service center is the post office,", "コミュニティセンターの右に郵便局があり、", "주민센터 오른쪽은 우체국이고,"),
            ("左边是诊所。", "zuǒbian shì zhěnsuǒ.", "and to the left is the clinic.", "左にクリニックがあります。", "왼쪽은 의원이에요."),
        ]),
        ("웃음과 정이 가득한 이 새 도시가, 나는 정말 좋아요.", [
            ("这座充满欢笑和温情的新城市，", "Zhè zuò chōngmǎn huānxiào hé wēnqíng de xīn chéngshì,", "This new city, full of laughter and warmth —", "笑顔と温もりにあふれるこの新しい街が、", "웃음과 정이 가득한 이 새 도시가,"),
            ("我非常喜欢。", "wǒ fēicháng xǐhuan.", "I love it very much.", "大好きです。", "나는 정말 좋아요."),
        ]),
    ],

    # ---------------- 第5课 美味的中国菜 ----------------
    "zh5": [
        ("나는 풍성하고 맛있는 중국 요리를 정말 좋아해요.", [
            ("我非常喜欢丰富又美味的中国菜。", "Wǒ fēicháng xǐhuan fēngfù yòu měiwèi de zhōngguócài.", "I love rich and delicious Chinese food very much.", "私は豊かで美味しい中国料理が大好きです。", "나는 풍성하고 맛있는 중국 요리를 정말 좋아해요."),
        ]),
        ("이른 아침, 김이 모락모락 나는 바오쯔에 고소한 두유를 곁들여요.", [
            ("清晨，", "Qīngchén,", "In the early morning,", "清々しい朝、", "이른 아침,"),
            ("热气腾腾的包子配上香浓的豆浆。", "rèqì téngténg de bāozi pèishang xiāngnóng de dòujiāng.", "steaming hot buns come with rich soy milk.", "湯気の立つ包子（肉まん）に香ばしい豆乳を合わせます。", "김이 모락모락 나는 바오쯔에 고소한 두유를 곁들여요."),
        ]),
        ("정오, 갓 삶아 낸 수타면은 향긋하고 쫄깃하며 매끄러워요.", [
            ("正午，", "Zhèngwǔ,", "At noon,", "正午には、", "정오,"),
            ("刚出锅的手工面条香气扑鼻、", "gāng chūguō de shǒugōng miàntiáo xiāngqì pūbí,", "freshly cooked handmade noodles smell wonderful", "茹でたての手打ち麺が食欲をそそる香りを放ち、", "갓 삶아 낸 수타면은 향긋하고,"),
            ("劲道爽滑。", "jìndao shuǎnghuá.", "and are chewy and smooth.", "もっちりとのどごし豊かです。", "쫄깃하며 매끄러워요."),
        ]),
        ("해 질 녘 온 가족이 식탁에 둘러앉아, 직접 육즙 가득한 만두를 빚어요.", [
            ("傍晚全家围坐桌旁，", "Bàngwǎn quánjiā wéizuò zhuōpáng,", "In the evening, the whole family sits around the table", "夕暮れには家族みんなで食卓を囲み、", "해 질 녘 온 가족이 식탁에 둘러앉아,"),
            ("亲手包出鲜美多汁的饺子。", "qīnshǒu bāo chū xiānměi duōzhī de jiǎozi.", "and wraps fresh, juicy dumplings by hand.", "手作りでジューシーな餃子を包みます。", "직접 육즙 가득한 만두를 빚어요."),
        ]),
        ("식사 전에, 모두 서로 미소를 나누며, 예의 바르게 \"천천히 드세요\"라고 말해요.", [
            ("开饭前，", "Kāifàn qián,", "Before the meal,", "食事の前には、", "식사 전에,"),
            ("大家互致微笑，", "dàjiā hù zhì wēixiào,", "everyone exchanges smiles", "みんなで微笑みを交わし、", "모두 서로 미소를 나누며,"),
            ("礼貌地说一声“请慢用”。", "lǐmào de shuō yì shēng 'Qǐng mànyòng'.", "and politely says, 'Please enjoy your meal.'", "「どうぞごゆっくりお召し上がりください」と礼儀正しく挨拶します。", "예의 바르게 \"천천히 드세요\"라고 말해요."),
        ]),
        ("접시 위의 요리는 색, 향, 맛을 모두 갖추었고, 고기와 채소의 조화로 더욱 영양가 있고 건강해요.", [
            ("盘中的菜肴色香味俱全，", "Pán zhōng de càiyáo sè xiāng wèi jùquán,", "The dishes on the plate look, smell and taste wonderful;", "お皿の料理は彩り・香り・味の三拍子が揃い、", "접시 위의 요리는 색, 향, 맛을 모두 갖추었고,"),
            ("荤素搭配更显营养健康。", "hūn sù dāpèi gèng xiǎn yíngyǎng jiànkāng.", "a mix of meat and vegetables makes them healthy and nutritious.", "肉と野菜の調和が栄養と健康を引き立てます。", "고기와 채소의 조화로 더욱 영양가 있고 건강해요."),
        ]),
        ("식사 후 느긋하게 앉아, 달콤하고 향긋한 따뜻한 차 한 주전자를 천천히 음미해요.", [
            ("饭后闲坐，", "Fànhòu xiánzuò,", "Relaxing after the meal,", "食後はゆったりと寛ぎ、", "식사 후 느긋하게 앉아,"),
            ("细细品味一壶甘甜清香的热茶。", "xìxì pǐnwèi yì hú gāntián qīngxiāng de rèchá.", "we slowly savor a pot of sweet, fragrant hot tea.", "急須で淹れた甘く香り高い温かいお茶をじっくりと味わいます。", "달콤하고 향긋한 따뜻한 차 한 주전자를 천천히 음미해요."),
        ]),
        ("모락모락 피어나는 삶의 온기와 맛있는 요리는, 마음을 따뜻하게 하고, 끝없는 기쁨과 힘을 가져다줘요.", [
            ("缕缕烟火气与可口佳肴，", "Lǚlǚ yānhuǒqì yǔ kěkǒu jiāyáo,", "The warm smell of home cooking and tasty dishes", "立ちのぼる暮らしの温もりと美味しいごちそうは、", "모락모락 피어나는 삶의 온기와 맛있는 요리는,"),
            ("温暖了心灵，", "wēnnuǎn le xīnlíng,", "warm the heart", "心を温め、", "마음을 따뜻하게 하고,"),
            ("带来了无尽的欢愉与力量。", "dàilái le wújìn de huānyú yǔ lìliàng.", "and bring endless joy and strength.", "尽きることのない喜びと力を与えてくれます。", "끝없는 기쁨과 힘을 가져다줘요."),
        ]),
    ],

    # ---------------- 第6课 快乐的旅行 (新) ----------------
    "zh6": [
        ("여름 방학이 되어, 나는 엄마 아빠와 함께 항저우로 여행을 가요.", [
            ("放暑假了，", "Fàng shǔjià le,", "Summer vacation has begun,", "夏休みになり、", "여름 방학이 되어,"),
            ("我和爸爸妈妈一起去杭州旅行。", "wǒ hé bàba māma yìqǐ qù Hángzhōu lǚxíng.", "and I am going on a trip to Hangzhou with Mom and Dad.", "お父さんとお母さんと一緒に杭州へ旅行に行きます。", "나는 엄마 아빠와 함께 항저우로 여행을 가요."),
        ]),
        ("우리는 기차표를 들고 베이징남역에 들어가, 빠르고 편안한 고속철도에 올라탔어요.", [
            ("我们拿着车票走进北京南站，", "Wǒmen názhe chēpiào zǒujìn Běijīng Nánzhàn,", "Holding our tickets, we walk into Beijing South Station", "切符を持って北京南駅に入り、", "우리는 기차표를 들고 베이징남역에 들어가,"),
            ("坐上了又快又稳的高铁。", "zuòshang le yòu kuài yòu wěn de gāotiě.", "and board the fast, smooth high-speed train.", "速くて揺れの少ない高速鉄道に乗りました。", "빠르고 편안한 고속철도에 올라탔어요."),
        ]),
        ("차창 밖으로 푸른 산과 맑은 물이 휙휙 지나가는데, 한 폭의 그림처럼 아름다워요.", [
            ("车窗外，", "Chēchuāng wài,", "Outside the train window,", "車窓の外を、", "차창 밖으로"),
            ("青山绿水一闪而过，", "qīngshān lǜshuǐ yì shǎn ér guò,", "green hills and clear rivers flash past,", "緑の山と澄んだ川があっという間に過ぎていき、", "푸른 산과 맑은 물이 휙휙 지나가는데,"),
            ("美得像一幅画。", "měi de xiàng yì fú huà.", "as beautiful as a painting.", "まるで一枚の絵のように美しいです。", "한 폭의 그림처럼 아름다워요."),
        ]),
        ("항저우에 도착해서, 우리는 시후 호숫가를 산책하다가, 멀리 높은 레이펑탑을 보았어요.", [
            ("到了杭州，", "Dào le Hángzhōu,", "When we arrive in Hangzhou,", "杭州に着くと、", "항저우에 도착해서,"),
            ("我们在西湖边散步，", "wǒmen zài Xī Hú biān sànbù,", "we take a walk beside West Lake", "西湖のほとりを散歩し、", "우리는 시후 호숫가를 산책하다가,"),
            ("远远看见了高高的雷峰塔。", "yuǎnyuǎn kànjiàn le gāogāo de Léifēng Tǎ.", "and see the tall Leifeng Pagoda in the distance.", "遠くに高い雷峰塔が見えました。", "멀리 높은 레이펑탑을 보았어요."),
        ]),
        ("우리는 작은 배를 타고 호수를 돌며, 예쁜 사진을 많이 찍었어요.", [
            ("我们坐着小船游湖，", "Wǒmen zuòzhe xiǎochuán yóu hú,", "We ride a little boat around the lake", "小舟に乗って湖を巡り、", "우리는 작은 배를 타고 호수를 돌며,"),
            ("拍了很多漂亮的照片。", "pāi le hěn duō piàoliang de zhàopiàn.", "and take lots of lovely photos.", "きれいな写真をたくさん撮りました。", "예쁜 사진을 많이 찍었어요."),
        ]),
        ("점심에는 오래된 식당에 들어가, 맛있는 시후추위(새콤달콤한 생선 요리)를 맛보았어요.", [
            ("中午，", "Zhōngwǔ,", "At noon,", "お昼には、", "점심에는"),
            ("我们走进一家老饭馆，", "wǒmen zǒujìn yì jiā lǎo fànguǎn,", "we step into an old restaurant", "老舗のレストランに入り、", "오래된 식당에 들어가,"),
            ("尝了鲜美的西湖醋鱼。", "cháng le xiānměi de Xī Hú cùyú.", "and taste delicious West Lake fish in vinegar sauce.", "美味しい西湖醋魚（魚の甘酢あんかけ）を味わいました。", "맛있는 시후추위(새콤달콤한 생선 요리)를 맛보았어요."),
        ]),
        ("특산품 가게에서, 나는 친한 친구에게 줄 향긋한 룽징차 한 상자를 샀어요.", [
            ("在特产店里，", "Zài tèchǎndiàn lǐ,", "In a local specialty shop,", "名産品のお店で、", "특산품 가게에서,"),
            ("我给好朋友买了一盒清香的龙井茶。", "wǒ gěi hǎo péngyou mǎi le yì hé qīngxiāng de Lóngjǐng chá.", "I buy a box of fragrant Longjing tea for my good friend.", "仲良しの友達に香りのよい龍井茶を一箱買いました。", "나는 친한 친구에게 줄 향긋한 룽징차 한 상자를 샀어요."),
        ]),
        ("이번 여행은 정말 즐거웠고, 나에게 아름다운 추억을 남겨 주었어요.", [
            ("这次旅行真快乐，", "Zhè cì lǚxíng zhēn kuàilè,", "This trip was so much fun,", "今回の旅行はとても楽しく、", "이번 여행은 정말 즐거웠고,"),
            ("给我留下了美好的回忆。", "gěi wǒ liúxià le měihǎo de huíyì.", "and it left me with wonderful memories.", "すてきな思い出になりました。", "나에게 아름다운 추억을 남겨 주었어요."),
        ]),
    ],

    # ---------------- 第7课 我的家人 (新) ----------------
    "zh7": [
        ("우리 가족은 다섯 명이에요. 아빠, 엄마, 형, 여동생 그리고 나예요.", [
            ("我家有五口人：", "Wǒ jiā yǒu wǔ kǒu rén:", "There are five people in my family:", "わたしの家族は五人です。", "우리 가족은 다섯 명이에요."),
            ("爸爸、妈妈、哥哥、妹妹和我。", "bàba, māma, gēge, mèimei hé wǒ.", "Dad, Mom, my big brother, my little sister and me.", "お父さん、お母さん、お兄さん、妹、そしてわたしです。", "아빠, 엄마, 형, 여동생 그리고 나예요."),
        ]),
        ("아빠는 의사예요. 매일 아침 자전거를 타고 병원으로 출근해요.", [
            ("爸爸是一名医生，", "Bàba shì yì míng yīshēng,", "Dad is a doctor;", "お父さんはお医者さんで、", "아빠는 의사예요."),
            ("每天早上骑自行车去医院上班。", "měitiān zǎoshang qí zìxíngchē qù yīyuàn shàngbān.", "every morning he rides his bike to work at the hospital.", "毎朝自転車に乗って病院へ仕事に行きます。", "매일 아침 자전거를 타고 병원으로 출근해요."),
        ]),
        ("엄마가 만든 요리는 정말 맛있어요. 매일 우리에게 맛있는 밥을 해 주세요.", [
            ("妈妈做的菜特别好吃，", "Māma zuò de cài tèbié hǎochī,", "Mom's cooking is especially tasty;", "お母さんの料理はとても美味しくて、", "엄마가 만든 요리는 정말 맛있어요."),
            ("每天都给我们做香喷喷的饭菜。", "měitiān dōu gěi wǒmen zuò xiāngpēnpēn de fàncài.", "every day she cooks us delicious-smelling meals.", "毎日わたしたちにいい匂いのご飯を作ってくれます。", "매일 우리에게 맛있는 밥을 해 주세요."),
        ]),
        ("형은 중학생이에요. 친구들과 함께 축구하는 것을 가장 좋아해요.", [
            ("哥哥是中学生，", "Gēge shì zhōngxuéshēng,", "My big brother is a middle school student;", "お兄さんは中学生で、", "형은 중학생이에요."),
            ("他最喜欢和同学一起踢足球。", "tā zuì xǐhuan hé tóngxué yìqǐ tī zúqiú.", "he loves playing football with his classmates most of all.", "友達と一緒にサッカーをするのが一番好きです。", "친구들과 함께 축구하는 것을 가장 좋아해요."),
        ]),
        ("여동생은 아직 어려요. 언제나 신나게 노래하고 춤을 춰요.", [
            ("妹妹还很小，", "Mèimei hái hěn xiǎo,", "My little sister is still very young;", "妹はまだ小さくて、", "여동생은 아직 어려요."),
            ("总是开开心心地唱歌跳舞。", "zǒngshì kāikāixīnxīn de chàng gē tiào wǔ.", "she is always happily singing and dancing.", "いつも楽しそうに歌ったり踊ったりしています。", "언제나 신나게 노래하고 춤을 춰요."),
        ]),
        ("우리 집에는 하얀 아기 고양이도 한 마리 있는데, 정말 귀여워요.", [
            ("我家还有一只白白的小猫，", "Wǒ jiā hái yǒu yì zhī báibái de xiǎomāo,", "We also have a little white kitten at home,", "家には白い子猫も一匹いて、", "우리 집에는 하얀 아기 고양이도 한 마리 있는데,"),
            ("它可爱极了。", "tā kě'ài jí le.", "and it is super cute.", "とてもかわいいです。", "정말 귀여워요."),
        ]),
        ("일요일에는 온 가족이 함께 할아버지 할머니를 뵈러 가요.", [
            ("星期天，", "Xīngqītiān,", "On Sunday,", "日曜日には、", "일요일에는"),
            ("全家人一起去看望爷爷奶奶。", "quán jiā rén yìqǐ qù kànwàng yéye nǎinai.", "the whole family goes to visit Grandpa and Grandma.", "家族みんなでおじいちゃんとおばあちゃんに会いに行きます。", "온 가족이 함께 할아버지 할머니를 뵈러 가요."),
        ]),
        ("사랑하는 가족과 함께 있으면, 하루하루가 정말 행복해요.", [
            ("和亲爱的家人在一起，", "Hé qīn'ài de jiārén zài yìqǐ,", "Being together with my dear family,", "大好きな家族と一緒にいると、", "사랑하는 가족과 함께 있으면,"),
            ("每一天都很幸福。", "měi yì tiān dōu hěn xìngfú.", "every day is full of happiness.", "毎日がとても幸せです。", "하루하루가 정말 행복해요."),
        ]),
    ],
}


def validate(lessons):
    """Raise if a lesson's clauses don't line up with its STORY sentences."""
    for lesson in lessons:
        lid = lesson["id"]
        rows = CLAUSES.get(lid)
        if rows is None:
            raise KeyError(f"No clause data for {lid}")
        story = lesson["story"]
        if len(rows) != len(story):
            raise ValueError(f"{lid}: {len(rows)} clause rows vs {len(story)} sentences")
        for s, (ko, clauses) in zip(story, rows):
            joined = "".join(c[0] for c in clauses)
            if joined != s["zh"]:
                raise ValueError(f"{lid}/{s['id']}: clauses {joined!r} != sentence {s['zh']!r}")
            for c in clauses:
                if len(c) != 5 or not all(c):
                    raise ValueError(f"{lid}/{s['id']}: incomplete clause {c!r}")
