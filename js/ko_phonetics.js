/**
 * KoPhonetics - Korean Pronunciation & Phonological Rules Engine
 *
 * Provides client-side and server-side Korean phonological analysis:
 * - Hangul decomposition & composition (초성, 중성, 종성)
 * - Phonological sound change rules (연음, 경음화, 비음화, 유음화, 격음화, 구개음화, ㅎ약화/탈락, ㄴ첨가, 음절끝소리규칙)
 * - Actual Korean phonetic reconstruction (표준 발음 표기, e.g. 한국어 -> [한구거], 학교 -> [학꾜], 독립 -> [동닙])
 * - Revised Romanization (국어의 로마자 표기법)
 * - Interactive HTML rendering with pronunciation tooltips & badges
 *
 * Inspired by & adapted from frankthinker/Korean-Pronunciation-Helper.
 */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.KoPhonetics = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ---------------- 1. HANGUL PRIMITIVES & DATA ---------------- */
  const S_BASE = 0xac00;
  const V_COUNT = 21;
  const T_COUNT = 28;
  const N_COUNT = V_COUNT * T_COUNT;

  const CHOSEONG = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
  ];

  const JUNGSEONG = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
    'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
  ];

  const JONGSEONG = [
    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
    'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
  ];

  const BASE_INITIAL_ROM = {
    'ㄱ': 'g', 'ㄲ': 'kk', 'ㄴ': 'n', 'ㄷ': 'd', 'ㄸ': 'tt', 'ㄹ': 'r', 'ㅁ': 'm',
    'ㅂ': 'b', 'ㅃ': 'pp', 'ㅅ': 's', 'ㅆ': 'ss', 'ㅇ': '', 'ㅈ': 'j', 'ㅉ': 'jj',
    'ㅊ': 'ch', 'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 'h'
  };

  const BASE_MEDIAL_ROM = {
    'ㅏ': 'a', 'ㅐ': 'ae', 'ㅑ': 'ya', 'ㅒ': 'yae', 'ㅓ': 'eo', 'ㅔ': 'e',
    'ㅕ': 'yeo', 'ㅖ': 'ye', 'ㅗ': 'o', 'ㅘ': 'wa', 'ㅙ': 'wae', 'ㅚ': 'oe',
    'ㅛ': 'yo', 'ㅜ': 'u', 'ㅝ': 'wo', 'ㅞ': 'we', 'ㅟ': 'wi', 'ㅠ': 'yu',
    'ㅡ': 'eu', 'ㅢ': 'ui', 'ㅣ': 'i'
  };

  const BASE_FINAL_ROM = {
    '': '', 'ㄱ': 'k', 'ㄲ': 'k', 'ㄳ': 'k', 'ㄴ': 'n', 'ㄵ': 'n', 'ㄶ': 'n',
    'ㄷ': 't', 'ㄹ': 'l', 'ㄺ': 'k', 'ㄻ': 'm', 'ㄼ': 'p', 'ㄽ': 'l', 'ㄾ': 'l',
    'ㄿ': 'p', 'ㅀ': 'l', 'ㅁ': 'm', 'ㅂ': 'p', 'ㅄ': 'p', 'ㅅ': 't', 'ㅆ': 't',
    'ㅇ': 'ng', 'ㅈ': 't', 'ㅊ': 't', 'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 't'
  };

  const FINAL_TO_INITIAL = {
    '': '', 'ㄱ': 'ㄱ', 'ㄲ': 'ㄲ', 'ㄳ': 'ㅅ', 'ㄴ': 'ㄴ', 'ㄵ': 'ㅈ', 'ㄶ': 'ㄴ',
    'ㄷ': 'ㄷ', 'ㄹ': 'ㄹ', 'ㄺ': 'ㄱ', 'ㄻ': 'ㅁ', 'ㄼ': 'ㅂ', 'ㄽ': 'ㅅ', 'ㄾ': 'ㅌ',
    'ㄿ': 'ㅍ', 'ㅀ': 'ㄹ', 'ㅁ': 'ㅁ', 'ㅂ': 'ㅂ', 'ㅄ': 'ㅅ', 'ㅅ': 'ㅅ', 'ㅆ': 'ㅆ',
    'ㅇ': 'ㅇ', 'ㅈ': 'ㅈ', 'ㅊ': 'ㅊ', 'ㅋ': 'ㅋ', 'ㅌ': 'ㅌ', 'ㅍ': 'ㅍ', 'ㅎ': 'ㅎ'
  };

  const BATCHIM_DECOMPOSITION = {
    'ㄳ': ['ㄱ', 'ㅅ'],
    'ㄵ': ['ㄴ', 'ㅈ'],
    'ㄶ': ['ㄴ', 'ㅎ'],
    'ㄺ': ['ㄹ', 'ㄱ'],
    'ㄻ': ['ㄹ', 'ㅁ'],
    'ㄼ': ['ㄹ', 'ㅂ'],
    'ㄽ': ['ㄹ', 'ㅅ'],
    'ㄾ': ['ㄹ', 'ㅌ'],
    'ㄿ': ['ㄹ', 'ㅍ'],
    'ㅀ': ['ㄹ', 'ㅎ'],
    'ㅄ': ['ㅂ', 'ㅅ']
  };

  // 7 standard representative codas (음절 끝소리 규칙 / 收音代表音)
  const NEUTRAL_FINAL_MAP = {
    'ㄲ': 'ㄱ', 'ㅋ': 'ㄱ', 'ㄳ': 'ㄱ', 'ㄺ': 'ㄱ',
    'ㄵ': 'ㄴ', 'ㄶ': 'ㄴ',
    'ㅅ': 'ㄷ', 'ㅆ': 'ㄷ', 'ㅈ': 'ㄷ', 'ㅊ': 'ㄷ', 'ㅌ': 'ㄷ', 'ㅎ': 'ㄷ',
    'ㄼ': 'ㄹ', 'ㄽ': 'ㄹ', 'ㄾ': 'ㄹ', 'ㅀ': 'ㄹ',
    'ㄻ': 'ㅁ',
    'ㅍ': 'ㅂ', 'ㅄ': 'ㅂ', 'ㄿ': 'ㅂ'
  };

  const TENSE_MAP = {
    'ㄱ': 'ㄲ', 'ㄷ': 'ㄸ', 'ㅂ': 'ㅃ', 'ㅅ': 'ㅆ', 'ㅈ': 'ㅉ'
  };

  const ASPIRATED_MAP = {
    'ㄱ': 'ㅋ', 'ㄷ': 'ㅌ', 'ㅂ': 'ㅍ', 'ㅈ': 'ㅊ'
  };

  const TH_FUSION_MAP = {
    'ㄷ': 'ㅌ', 'ㅅ': 'ㅌ', 'ㅆ': 'ㅌ', 'ㅈ': 'ㅊ', 'ㅊ': 'ㅊ', 'ㅌ': 'ㅌ'
  };

  const PALATAL_TRIGGERS = new Set(['ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ']);

  const TENSIFICATION_FINALS = new Set([
    'ㄱ', 'ㄲ', 'ㅋ', 'ㄳ', 'ㄺ',
    'ㄷ', 'ㅅ', 'ㅆ', 'ㅈ', 'ㅊ', 'ㅌ',
    'ㅂ', 'ㅄ', 'ㄼ', 'ㄾ', 'ㄿ', 'ㅀ',
    'ㅎ', 'ㄶ'
  ]);

  const H_WEAKENING_CONTEXT = new Set(['', 'ㄴ', 'ㄹ', 'ㅁ']);
  const N_INSERTION_FINALS = new Set(['ㄱ', 'ㄲ', 'ㅋ', 'ㄺ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄹ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅂ', 'ㅍ', 'ㅅ', 'ㅆ', 'ㅈ', 'ㅊ']);
  const N_INSERTION_VOWELS = new Set(['ㅣ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅖ', 'ㅒ']);
  const H_FINALS = new Set(['ㅎ', 'ㄶ', 'ㅀ']);
  const WORD_BOUNDARY_CHARS = new Set([' ', '\n', '\t', '.', ',', '!', '?', '"', '\'', ')', '(', ':', ';', '-', '—', '…']);
  const GLIDE_VOWELS = new Set(['ㅘ', 'ㅙ', 'ㅚ', 'ㅟ', 'ㅞ']);

  /* ---------------- 2. RULES & METADATA ---------------- */
  const RULE_COLORS = {
    liaison: '#ff8a65',       // 连音 (연음)
    assimilation: '#9575cd',  // 同化 (비음/유음화)
    tensification: '#ffb74d', // 紧音化 (경음화)
    aspiration: '#4fc3f7',    // 送气化 (격음화)
    palatalization: '#f06292',// 腭化 (구개음화)
    neutralization: '#aed581',// 收音中和/代表音 (음절말 자음화)
    contraction: '#ba68c8',   // 缩约 (축약)
    glide: '#4db6ac',         // 滑音 (반모음화)
    hWeakening: '#80cbc4',    // ㅎ弱化/消失
    nInsertion: '#f48fb1',    // ㄴ添加 (ㄴ첨가)
    base: '#90a4ae'
  };

  const RULE_REFERENCES = {
    liaison: { label: '连音 (연음)', nameKo: '연음' },
    assimilation: { label: '同化 (비음/유음화)', nameKo: '자음동화' },
    tensification: { label: '紧音化 (경음화)', nameKo: '경음화' },
    aspiration: { label: '送气化 (격음화)', nameKo: '격음화' },
    palatalization: { label: '腭化 (구개음화)', nameKo: '구개음화' },
    neutralization: { label: '收音代表音 (음절말 규칙)', nameKo: '음절 끝소리 규칙' },
    contraction: { label: '缩约 (축약)', nameKo: '축약' },
    glide: { label: '滑音 (반모음화)', nameKo: '반모음화' },
    hWeakening: { label: 'ㅎ弱化/消失', nameKo: 'ㅎ탈락' },
    nInsertion: { label: 'ㄴ添加 (ㄴ첨가)', nameKo: 'ㄴ첨가' },
    base: { label: '基础发音', nameKo: '기본 발음' }
  };

  const RULE_DESCRIPTIONS = {
    liaison: '前字终声（收音）移入后字以ㅇ起首的元音音节，形成连音朗读。',
    assimilation: '辅音受相邻鼻音(ㄴ, ㅁ)或流音(ㄹ)影响发生同化（鼻音化/流音化）。',
    tensification: '辅音受前字收音或语法规则影响变为紧音（ㄲ, ㄸ, ㅃ, ㅆ, ㅉ）。',
    aspiration: '平音(ㄱ, ㄷ, ㅂ, ㅈ)与ㅎ相遇合并为送气破裂音(ㅋ, ㅌ, ㅍ, ㅊ)。',
    palatalization: '收音ㄷ, ㅌ遇以ㅣ开头的元音时变为ㅈ, ㅊ。',
    neutralization: '收音在辅音前或词尾还原为7个标准代表音(ㄱ, ㄴ, ㄷ, ㄹ, ㅁ, ㅂ, ㅇ)。',
    contraction: '相邻两个元音或音素合并为一个缩约音。',
    glide: '滑音介音缓冲相邻元音发音。',
    hWeakening: 'ㅎ夹在元音或有声辅音之间时弱化或脱落。',
    nInsertion: '复合词在后词以ㅣ系元音开头时，前词收音激发出ㄴ插音。',
    base: '字块的标准拼写参考罗马音。'
  };

  const ASSIMILATION_RULES = {
    'ㄱㄴ': { final: 'ㅇ', initial: 'ㄴ' },
    'ㄱㄹ': { final: 'ㅇ', initial: 'ㄴ' },
    'ㄱㅁ': { final: 'ㅇ', initial: 'ㅁ' },
    'ㄴㄹ': { final: 'ㄹ', initial: 'ㄹ' },
    'ㄹㄴ': { final: 'ㄹ', initial: 'ㄹ' },
    'ㅂㅁ': { final: 'ㅁ', initial: 'ㅁ' },
    'ㅂㄴ': { final: 'ㅁ', initial: 'ㄴ' },
    'ㅂㄹ': { final: 'ㅁ', initial: 'ㄴ' },
    'ㅁㄹ': { final: 'ㅁ', initial: 'ㄴ' },
    'ㅁㄴ': { final: 'ㅁ', initial: 'ㄴ' },
    'ㅇㄹ': { final: 'ㅇ', initial: 'ㄴ' },
    'ㄷㄴ': { final: 'ㄴ', initial: 'ㄴ' },
    'ㄷㅁ': { final: 'ㄴ', initial: 'ㅁ' },
    'ㄷㄹ': { final: 'ㄴ', initial: 'ㄴ' },
    'ㅅㄴ': { final: 'ㄴ', initial: 'ㄴ' },
    'ㅆㄴ': { final: 'ㄴ', initial: 'ㄴ' },
    'ㅈㄴ': { final: 'ㄴ', initial: 'ㄴ' },
    'ㅊㄴ': { final: 'ㄴ', initial: 'ㄴ' },
    'ㅎㄴ': { final: 'ㄴ', initial: 'ㄴ' },
    'ㅅㅁ': { final: 'ㄴ', initial: 'ㅁ' },
    'ㅆㅁ': { final: 'ㄴ', initial: 'ㅁ' },
    'ㅈㅁ': { final: 'ㄴ', initial: 'ㅁ' },
    'ㅊㅁ': { final: 'ㄴ', initial: 'ㅁ' },
    'ㅎㅁ': { final: 'ㄴ', initial: 'ㅁ' }
  };

  /* ---------------- 3. LEXICON & GRAMMAR PATTERNS ---------------- */
  const PARTICLE_FORMS = new Set([
    '은', '는', '이', '가', '을', '를', '과', '와', '으로', '로',
    '에서', '에게', '께서', '까지', '부터', '만', '도', '이나', '나',
    '이라도', '라도', '조차', '뿐', '마저', '처럼', '처럼은', '처럼도', '에는', '에'
  ]);
  const PARTICLE_SUFFIXES = Array.from(PARTICLE_FORMS).sort((a, b) => b.length - a.length);

  const DEPENDENT_NOUNS = new Set([
    '것', '점', '분', '사람', '시간', '동안', '이상', '이후', '이전', '직후',
    '직전', '만큼', '만치', '뿐', '밖', '밖에', '바람', '차례', '차', '쯤',
    '정도', '결과', '덕분', '탓', '김', '김에', '대로', '데', '때', '때문',
    '측', '편', '쪽', '줄', '자리', '거리', '중', '사정', '사이', '와중', '양', '듯', '판'
  ]);

  const COUNTERS = new Set([
    '번', '회', '명', '분', '살', '마리', '마디', '개', '권', '장', '잔',
    '병', '대', '통', '가지', '줄', '송이', '시', '차', '켤레', '채', '필',
    '발', '척', '쪽', '단', '벌', '포기', '근', '모금', '모', '리터', '그램',
    '킬로', '팩', '상자', '세트', '모음', '입', '입자'
  ]);
  const COUNTER_SUFFIXES = ['살', '시', '개월', '주', '년', '차', '도', '층'];

  const COPULA_FORMS = new Set([
    '이다', '이에요', '이에', '이야', '이여', '이요', '이였습니다', '이었어요',
    '이었다', '입니다', '이라서', '이라도', '라면', '이라니', '이라며', '이지만',
    '이니까', '이니', '이네요', '이냐', '이냐고', '이라구', '이라고', '이라고요',
    '이라네', '이래요', '이랍니다'
  ]);
  const COPULA_REGEX = /^이(?:었|였|라|니|야|여|요|라[고니며]?|니까|니라|랍니다|래요|러니|라도|라면|라서|자|구|던)/;

  const LEXICAL_TENSE_PREFERRED = new Set([
    '사람', '정도', '시간', '조건', '성과', '성격', '사건', '관건', '효과',
    '교과', '상태', '결론', '결정', '감정', '분위기', '변화', '위기', '경험', '계획'
  ]);

  const FORCED_TENSIFICATION_PATTERNS = [
    { pattern: '절대', targets: [1], reason: 'ㄹ收音+ㄷ的汉字词' },
    { pattern: '달성', targets: [1], reason: 'ㄹ收音+ㅅ的汉字词' },
    { pattern: '발전', targets: [1], reason: 'ㄹ收音+ㅈ的汉字词' },
    { pattern: '인사과', targets: [2], reason: '合成词紧音化' },
    { pattern: '입장권', targets: [1], reason: '合成词紧音化' },
    { pattern: '대기권', targets: [2], reason: '合成词紧音化' },
    { pattern: '참정권', targets: [2], reason: '合成词紧音化' },
    { pattern: '당뇨병', targets: [2], reason: '合成词紧音化' },
    { pattern: '맥주병', targets: [2], reason: '合成词紧音化' },
    { pattern: '신뢰성', targets: [2], reason: '合成词紧音化' },
    { pattern: '로마자', targets: [2], reason: '合成词紧音化' },
    { pattern: '감사장', targets: [2], reason: '合成词紧音化' },
    { pattern: '문제점', targets: [2], reason: '合成词紧音化' },
    { pattern: '협심증', targets: [2], reason: '合成词紧音化' },
    { pattern: '성과', targets: [1], reason: '惯用汉字紧音化' },
    { pattern: '물가', targets: [1], reason: '惯用汉字紧音化' },
    { pattern: '사건', targets: [1], reason: '惯用汉字紧音化' },
    { pattern: '조건', targets: [1], reason: '惯用汉字紧音化' },
    { pattern: '인기', targets: [1], reason: '惯用汉字紧音化' },
    { pattern: '인건비', targets: [1], reason: '惯用汉字紧音化' },
    { pattern: '효과', targets: [1], reason: '规范允许的紧音' },
    { pattern: '교과', targets: [1], reason: '规范允许的紧音' },
    { pattern: '관건', targets: [1], reason: '规范允许的紧音' },
    { pattern: '넘겠다', targets: [1, 2], reason: 'ㄴ/ㅁ后接-겠다语尾' },
    { pattern: '젊지만', targets: [1], reason: 'ㄴ/ㅁ后接-지만语尾' },
    { pattern: '건널 다리', targets: [2], reason: '连体形-ㄹ后名词' },
    { pattern: '갈 사람', targets: [1], reason: '连体形-ㄹ后名词' },
    { pattern: '받을 자격', targets: [2], reason: '连体形-ㄹ后名词' },
    { pattern: '여덟 번', targets: [2], reason: '固有数词连用' },
    { pattern: '열 장', targets: [1], reason: '固有数词连用' },
    { pattern: '스물여덟 살', targets: [4], reason: '固有数词连用' },
    { pattern: '술집', targets: [1], reason: '固有合成词' },
    { pattern: '잠자리', targets: [1], reason: '固有合成词' }
  ];

  // Specific compound words where ㄴ-insertion applies
  const N_INSERTION_COMPOUNDS = new Set([
    '월요일', '일요일', '목요일', '금요일', '토요일', '꽃잎', '깻잎', '나뭇잎',
    '맨입', '솜이불', '알약', '물약', '눈요기', '남존여비', '신여성', '색연필', '식용유', '백분율'
  ]);

  const SUFFIX_TENSIFICATION_RULES = [
    { suffix: '다', precedingFinals: new Set(['ㄴ', 'ㅁ']), reason: '词干+基本形「-다」' },
    { suffix: '고', precedingFinals: new Set(['ㄴ', 'ㅁ']), reason: '连接语尾「-고」' },
    { suffix: '지만', precedingFinals: new Set(['ㄴ', 'ㅁ']), reason: '让步语尾「-지만」' },
    { suffix: '겠다', precedingFinals: new Set(['ㄴ', 'ㅁ']), reason: '意志/推量语尾「-겠다」' },
    { suffix: '소', precedingFinals: new Set(['ㄴ', 'ㅁ']), reason: '命令语尾「-소」' }
  ];

  /* ---------------- 4. CORE UTILITY FUNCTIONS ---------------- */
  function isHangul(char) {
    if (!char) return false;
    const code = char.charCodeAt(0);
    return code >= 0xac00 && code <= 0xd7a3;
  }

  function decompose(char) {
    if (!isHangul(char)) return null;
    const sIndex = char.charCodeAt(0) - S_BASE;
    const choIndex = Math.floor(sIndex / N_COUNT);
    const jungIndex = Math.floor((sIndex % N_COUNT) / T_COUNT);
    const jongIndex = sIndex % T_COUNT;
    return {
      initial: CHOSEONG[choIndex],
      medial: JUNGSEONG[jungIndex],
      final: JONGSEONG[jongIndex]
    };
  }

  function composeHangulSyllable(initial, medial, final) {
    const cIdx = CHOSEONG.indexOf(initial);
    const jIdx = JUNGSEONG.indexOf(medial);
    const fIdx = JONGSEONG.indexOf(final || '');
    if (cIdx === -1 || jIdx === -1 || fIdx === -1) return null;
    return String.fromCharCode(S_BASE + (cIdx * 21 + jIdx) * 28 + fIdx);
  }

  function cloneJamo(triple) {
    if (!triple) return null;
    return { ...triple };
  }

  function splitBatchim(finalJamo) {
    const parts = BATCHIM_DECOMPOSITION[finalJamo];
    if (!parts) return { base: finalJamo, release: '' };
    return { base: parts[0], release: parts[1] };
  }

  function romanizeInitial(jamo) {
    return BASE_INITIAL_ROM[jamo] ?? '';
  }

  function romanizeMedial(jamo) {
    return BASE_MEDIAL_ROM[jamo] ?? '';
  }

  function romanizeFinal(jamo) {
    return BASE_FINAL_ROM[jamo] ?? '';
  }

  function composeRomanization(jamoTriple) {
    if (!jamoTriple) return '';
    const { initial, medial, final } = jamoTriple;
    return [romanizeInitial(initial), romanizeMedial(medial), romanizeFinal(final)].join('');
  }

  function buildNote(rule, extra = {}) {
    const meta = RULE_REFERENCES[rule] ?? {};
    return {
      rule,
      label: meta.label ?? '音变',
      nameKo: meta.nameKo ?? '',
      description: RULE_DESCRIPTIONS[rule] ?? '',
      targets: ['current', 'next'],
      ...extra
    };
  }

  function tokenizeSentence(sentence) {
    const tokens = [];
    let buffer = '';
    let type = null;

    const flush = () => {
      if (!buffer) return;
      tokens.push({ text: buffer, type });
      buffer = '';
      type = null;
    };

    for (const char of sentence) {
      const isKor = isHangul(char);
      const nextType = isKor ? 'hangul' : 'other';
      if (type === null) {
        type = nextType;
        buffer = char;
        continue;
      }
      if (nextType === type) {
        buffer += char;
      } else {
        flush();
        type = nextType;
        buffer = char;
      }
    }
    flush();
    return tokens;
  }

  function classifyWord(rawWord) {
    if (!rawWord || !/[가-힣]/.test(rawWord)) {
      return { role: 'content', tags: new Set(), blockNInsertion: false, prefersTense: false };
    }
    const normalized = rawWord.replace(/[^가-힣]/g, '');
    const meta = { role: 'content', tags: new Set(), blockNInsertion: false, prefersTense: false };
    if (!normalized) return meta;

    if (COPULA_FORMS.has(normalized) || COPULA_REGEX.test(normalized)) {
      meta.role = 'copula';
      meta.tags.add('copula');
      meta.blockNInsertion = true;
      return meta;
    }
    if (PARTICLE_FORMS.has(normalized)) {
      meta.role = 'particle';
      meta.tags.add('particle');
      meta.blockNInsertion = true;
      return meta;
    }
    for (const suffix of PARTICLE_SUFFIXES) {
      if (normalized.endsWith(suffix) && normalized.length > suffix.length) {
        meta.tags.add('hasParticle');
        break;
      }
    }
    if (DEPENDENT_NOUNS.has(normalized)) {
      meta.role = 'dependentNoun';
      meta.tags.add('dependentNoun');
      meta.prefersTense = true;
      return meta;
    }
    if (COUNTERS.has(normalized) || COUNTER_SUFFIXES.some(s => normalized.endsWith(s))) {
      meta.role = 'counter';
      meta.tags.add('counter');
      meta.prefersTense = true;
      return meta;
    }
    if (LEXICAL_TENSE_PREFERRED.has(normalized)) {
      meta.prefersTense = true;
    }
    return meta;
  }

  /* ---------------- 5. PHONOLOGICAL TRANSFORMATION RULES ---------------- */

  // 5.1 缩约 (Contraction)
  function applyContraction(current, next) {
    if (!current || !next) return null;
    if (current.final === 'ㅎ' && next.initial === 'ㅇ' && next.medial === 'ㅕ') {
      return {
        apply: true,
        current: { ...current, final: '' },
        next: { ...next, medial: 'ㅕ' },
        note: buildNote('contraction', { label: 'ㅎ+여 缩约', before: 'ㅎ+ㅕ', after: 'ㅕ' })
      };
    }
    if (current.final === 'ㅂ' && next.initial === 'ㅇ' && next.medial === 'ㅗ') {
      return {
        apply: true,
        current: { ...current, final: '' },
        next: { ...next, medial: 'ㅘ' },
        note: buildNote('contraction', { label: 'ㅂ+ㅗ → ㅘ', before: 'ㅂ+ㅗ', after: 'ㅘ' })
      };
    }
    return null;
  }

  // 5.2 腭化 (Palatalization) - e.g. 같이 -> [가치], 굳이 -> [구지]
  function applyPalatalization(current, next, context = {}) {
    if (!context.sameWord) return null;
    if (!current?.final || !next?.initial) return null;
    if (next.initial !== 'ㅇ' || !PALATAL_TRIGGERS.has(next.medial)) return null;
    const palatalMap = { 'ㄷ': 'ㅈ', 'ㅌ': 'ㅊ', 'ㄸ': 'ㅉ' };
    const changed = palatalMap[current.final];
    if (changed) {
      return {
        apply: true,
        current: { ...current, final: '' },
        next: { ...next, initial: changed },
        note: buildNote('palatalization', {
          label: '腭化 (구개음화)',
          before: `${current.final} + ${next.medial}`,
          after: `${changed}${next.medial}`,
          targets: ['current', 'next']
        })
      };
    }
    return null;
  }

  // 5.3 送气化 (Aspiration) - e.g. 축하 -> [추카], 좋다 -> [조타], 입학 -> [이팍]
  function applyAspiration(current, next, context = {}) {
    if (!context.sameWord) return null;
    if (!current || !next) return null;
    // Case A: current has ㅎ / ㄶ / ㅀ and next starts with ㄱ/ㄷ/ㅂ/ㅈ
    if (ASPIRATED_MAP[next.initial]) {
      if (current.final === 'ㅎ') {
        return {
          apply: true,
          current: { ...current, final: '' },
          next: { ...next, initial: ASPIRATED_MAP[next.initial] },
          note: buildNote('aspiration', {
            label: 'ㅎ触发送气 (격음화)',
            before: `ㅎ + ${next.initial}`,
            after: ASPIRATED_MAP[next.initial],
            targets: ['current', 'next']
          })
        };
      }
      if (current.final) {
        const { base, release } = splitBatchim(current.final);
        if (release === 'ㅎ') {
          return {
            apply: true,
            current: { ...current, final: base },
            next: { ...next, initial: ASPIRATED_MAP[next.initial] },
            note: buildNote('aspiration', {
              label: 'ㅎ触发送气 (격음화)',
              before: `${current.final} + ${next.initial}`,
              after: `${base}${ASPIRATED_MAP[next.initial]}`,
              targets: ['current', 'next']
            })
          };
        }
      }
    }
    // Case B: current ends with ㄱ/ㄷ/ㅂ/ㅈ and next starts with ㅎ -> next becomes ㅋ/ㅌ/ㅍ/ㅊ
    if (next.initial === 'ㅎ' && current.final && ASPIRATED_MAP[current.final]) {
      const aspirated = ASPIRATED_MAP[current.final];
      return {
        apply: true,
        current: { ...current, final: '' },
        next: { ...next, initial: aspirated },
        note: buildNote('aspiration', {
          label: '收音激发送气 (격음화)',
          before: `${current.final} + ㅎ`,
          after: aspirated,
          targets: ['current', 'next']
        })
      };
    }
    return null;
  }

  // 5.4 收音+ㅎ合并 (TH Fusion) - e.g. 옷+한 -> 옫+한 -> 옫+탄
  function applyTHFusion(current, next, context = {}) {
    if (!context.sameWord) return null;
    if (!current?.final || next?.initial !== 'ㅎ') return null;
    const fused = TH_FUSION_MAP[current.final];
    if (!fused) return null;
    return {
      apply: true,
      current: { ...current, final: '' },
      next: { ...next, initial: fused },
      note: buildNote('aspiration', {
        label: '收音+ㅎ送气 (격음화)',
        before: `${current.final} + ㅎ`,
        after: fused,
        targets: ['current', 'next']
      })
    };
  }

  // 5.5 ㅎ弱化/脱落 (H-Weakening / Deletion) - e.g. 좋아 -> [조아], 놓아 -> [노아]
  function applyHWeakening(current, next, context = {}) {
    if (!context.sameWord) return null;
    if (!current || !next) return null;
    if (current.final === 'ㅎ' && (!next.initial || next.initial === 'ㅇ')) {
      return {
        apply: true,
        current: { ...current, final: '' },
        next: { ...next, initial: next.initial || 'ㅇ' },
        note: buildNote('hWeakening', {
          label: 'ㅎ脱落 (ㅎ탈락)',
          before: 'ㅎ + ㅇ',
          after: 'ㅇ',
          targets: ['current']
        })
      };
    }
    return null;
  }

  // 5.6 ㄴ添加 (N-Insertion) - only for known compounds (e.g. 월요일, 일요일, 꽃잎)
  function applyNInsertion(current, next, context = {}) {
    if (context?.blockNInsertion) return null;
    if (!current || !next) return null;
    if (next.initial !== 'ㅇ' || !N_INSERTION_VOWELS.has(next.medial)) return null;
    const prevFinal = current.final ?? '';
    if (!prevFinal || !N_INSERTION_FINALS.has(prevFinal)) return null;

    if (!context.isCompound) return null;

    return {
      apply: true,
      current: { ...current },
      next: { ...next, initial: 'ㄴ' },
      note: buildNote('nInsertion', {
        label: 'ㄴ添加 (ㄴ첨가)',
        before: 'Ø',
        after: 'ㄴ',
        targets: ['next']
      })
    };
  }

  // 5.7 连音 (Liaison / 연음) - e.g. 한국어 -> [한구거], 책을 -> [채글], 읽어요 -> [일거요]
  function applyLiaison(current, next, context = {}) {
    if (!context.sameWord) return null;
    if (!current?.final || !next) return null;
    if (current.final === 'ㅇ') return null; // ㅇ is nasal ng, never releases to onset
    const nextInitial = next.initial ?? '';
    if (nextInitial && nextInitial !== 'ㅇ') return null;

    // Handle double batchim (겹받침)
    if (BATCHIM_DECOMPOSITION[current.final]) {
      const [stay, release] = BATCHIM_DECOMPOSITION[current.final];
      const releasedOnset = (release === 'ㅅ') ? 'ㅆ' : (FINAL_TO_INITIAL[release] || release);
      return {
        apply: true,
        current: { ...current, final: stay },
        next: { ...next, initial: releasedOnset },
        note: buildNote('liaison', {
          label: '双收音连音 (연음)',
          before: `${current.final} + ㅇ`,
          after: `${stay} + ${releasedOnset}`,
          targets: ['current', 'next']
        })
      };
    }

    // Single batchim
    const released = FINAL_TO_INITIAL[current.final];
    if (!released) return null;
    return {
      apply: true,
      current: { ...current, final: '' },
      next: { ...next, initial: released },
      note: buildNote('liaison', {
        label: '连音释放 (연음)',
        before: `${current.final} + ㅇ`,
        after: released,
        targets: ['current', 'next']
      })
    };
  }

  // 5.8 辅音同化 (Assimilation / 비음화·유음화) - e.g. 갑니다 -> [감니다], 독립 -> [동닙]
  function applyAssimilation(current, next, context = {}) {
    if (!context.sameWord) return null;
    if (!current?.final || !next?.initial) return null;
    let baseFinal = current.final;
    if (BATCHIM_DECOMPOSITION[baseFinal]) {
      baseFinal = NEUTRAL_FINAL_MAP[baseFinal] || baseFinal;
    }
    // Neutralized equivalence for assimilation matching
    let lookupFinal = baseFinal;
    if (['ㅅ', 'ㅆ', 'ㅈ', 'ㅊ', 'ㅌ', 'ㅎ'].includes(baseFinal)) lookupFinal = 'ㄷ';
    if (['ㅋ', 'ㄲ', 'ㄳ', 'ㄺ'].includes(baseFinal)) lookupFinal = 'ㄱ';
    if (['ㅍ', 'ㄼ', 'ㄿ', 'ㅄ'].includes(baseFinal)) lookupFinal = 'ㅂ';

    const pair = lookupFinal + next.initial;
    const result = ASSIMILATION_RULES[pair];
    if (!result) return null;

    const currentChanged = current.final !== result.final;
    const nextChanged = next.initial !== result.initial;
    if (!currentChanged && !nextChanged) return null;

    const targets = [];
    if (currentChanged) targets.push('current');
    if (nextChanged) targets.push('next');

    return {
      apply: true,
      current: { ...current, final: result.final },
      next: { ...next, initial: result.initial },
      note: buildNote('assimilation', {
        label: '同化 (비음/유음화)',
        before: `${current.final} + ${next.initial}`,
        after: `${result.final} + ${result.initial}`,
        targets
      })
    };
  }

  // 5.9 紧音化 (Tensification / 경음화) - e.g. 학교 -> [학꾜], 식당 -> [식땅], 있습니다 -> [읻씀니다]
  function applyTensification(current, next, context = {}) {
    if (!next?.initial) return null;
    const tensified = TENSE_MAP[next.initial];
    if (!tensified || tensified === next.initial) return null;

    const reasonDescription = context.tensificationReason;

    if (context.forceTense) {
      return {
        apply: true,
        current: { ...current },
        next: { ...next, initial: tensified },
        note: buildNote('tensification', {
          label: '紧音化 (경음화)',
          before: next.initial,
          after: tensified,
          targets: ['next'],
          description: reasonDescription || RULE_DESCRIPTIONS.tensification
        })
      };
    }

    if (!context.sameWord) return null;
    if (!current?.final) return null;
    if (H_FINALS.has(current.final) && next.initial !== 'ㅅ') return null;

    let baseFinal = current.final;
    if (BATCHIM_DECOMPOSITION[baseFinal]) {
      baseFinal = NEUTRAL_FINAL_MAP[baseFinal] || baseFinal;
    }
    if (!TENSIFICATION_FINALS.has(current.final) && !TENSIFICATION_FINALS.has(baseFinal)) return null;

    return {
      apply: true,
      current: { ...current },
      next: { ...next, initial: tensified },
      note: buildNote('tensification', {
        label: '紧音化 (경음화)',
        before: next.initial,
        after: tensified,
        targets: ['next'],
        description: reasonDescription || `受前字收音 ${current.final} 影响发生紧音化`
      })
    };
  }

  // 5.10 滑音 (Glide)
  function applyGlide(current, next) {
    if (!current || !next) return null;
    if (current.final) return null;
    if (next.initial && next.initial !== 'ㅇ') return null;
    if (!GLIDE_VOWELS.has(next.medial)) return null;
    return {
      apply: true,
      current: { ...current },
      next: { ...next },
      note: buildNote('glide', {
        label: '滑音 (반모음화)',
        before: 'w + 元音',
        after: '滑音融合',
        targets: ['next']
      })
    };
  }

  // 5.11 收音中和/代表音化 (Neutralization)
  function applyNeutralization(jamo) {
    if (!jamo?.final) return jamo;
    const neutral = NEUTRAL_FINAL_MAP[jamo.final];
    if (neutral) {
      return { ...jamo, final: neutral };
    }
    return jamo;
  }

  const RULE_PIPELINE = [
    applyContraction,
    applyPalatalization, // Palatalization before liaison/aspiration (같이 -> 가치)
    applyAspiration,     // Aspiration before liaison (축하 -> 추카)
    applyTHFusion,
    applyHWeakening,
    applyNInsertion,
    applyLiaison,
    applyAssimilation,
    applyTensification,
    applyGlide
  ];

  function resolveRules(current, next, context = {}) {
    const state = { current: cloneJamo(current), next: cloneJamo(next), notes: [] };
    RULE_PIPELINE.forEach(fn => {
      const outcome = fn(state.current, state.next, context);
      if (outcome?.apply) {
        state.current = outcome.current;
        state.next = outcome.next;
        state.notes.push(outcome.note);
      }
    });
    return state;
  }

  function distributeNotes(notes = []) {
    const currentNotes = [];
    const nextNotes = [];
    notes.forEach(note => {
      const targets = note.targets ?? ['current'];
      if (targets.includes('current')) currentNotes.push(note);
      if (targets.includes('next')) nextNotes.push(note);
    });
    return { currentNotes, nextNotes };
  }

  /* ---------------- 6. MAIN ENGINE ANALYZER ---------------- */

  function analyzeSentence(sentence = '') {
    if (!sentence || typeof sentence !== 'string') {
      return { original: '', pronounced: '', cleanPronounced: '', bracketPronounced: '', romanization: '', hasChange: false, segments: [], rules: [] };
    }

    const tokens = tokenizeSentence(sentence);
    const wordContexts = tokens.map(t => t.type === 'hangul' ? classifyWord(t.text) : null);
    const sequence = [];
    let hangulCharCount = 0;

    tokens.forEach((token, tokenIdx) => {
      if (token.type !== 'hangul') {
        sequence.push({ type: 'other', text: token.text, tokenIdx });
      } else {
        Array.from(token.text).forEach((char, syllableIdx) => {
          const decomposed = decompose(char);
          sequence.push({
            type: 'syllable',
            char,
            tokenIdx,
            syllableIdx,
            globalIndex: hangulCharCount++,
            unit: {
              char,
              baseJamo: cloneJamo(decomposed),
              workJamo: cloneJamo(decomposed),
              pendingNotes: []
            }
          });
        });
      }
    });

    // Pre-calculate forced tensification targets
    const forcedTenseMap = new Map();
    FORCED_TENSIFICATION_PATTERNS.forEach(({ pattern, targets, reason }) => {
      let start = sentence.indexOf(pattern);
      while (start !== -1) {
        let globalIdx = 0;
        for (let i = 0; i < sentence.length; i++) {
          if (i === start) break;
          if (isHangul(sentence[i])) globalIdx++;
        }
        targets.forEach(tIdx => {
          forcedTenseMap.set(globalIdx + tIdx, reason);
        });
        start = sentence.indexOf(pattern, start + 1);
      }
    });

    const segments = [];
    const triggeredRules = new Map();

    const findNextSyllable = (startIdx) => {
      let hasSoftBoundary = false;
      let hasHardBoundary = false;
      for (let idx = startIdx; idx < sequence.length; idx++) {
        const item = sequence[idx];
        if (item.type === 'syllable') {
          return { item, index: idx, boundary: { hasSoftBoundary, hasHardBoundary } };
        }
        if (item.type === 'other') {
          if ([' ', '\t'].includes(item.text)) {
            hasSoftBoundary = true;
          } else {
            hasHardBoundary = true;
          }
        }
      }
      return { item: null, index: null, boundary: { hasSoftBoundary, hasHardBoundary } };
    };

    for (let idx = 0; idx < sequence.length; idx++) {
      const item = sequence[idx];
      if (item.type === 'other') {
        segments.push({ type: 'other', text: item.text, original: item.text, pronounced: item.text, hasChange: false });
        continue;
      }

      const unit = item.unit;
      if (!unit.baseJamo) {
        segments.push({ type: 'other', text: item.char, original: item.char, pronounced: item.char, hasChange: false });
        continue;
      }

      const baseJamo = cloneJamo(unit.baseJamo);
      let updated = cloneJamo(unit.workJamo);
      let notes = unit.pendingNotes ? [...unit.pendingNotes] : [];

      const { item: nextItem, boundary } = findNextSyllable(idx + 1);
      const nextUnit = nextItem ? nextItem.unit : null;

      if (nextUnit && nextUnit.workJamo) {
        const nextWorkJamo = cloneJamo(nextUnit.workJamo);
        const forcedReason = forcedTenseMap.get(nextItem.globalIndex);
        const currentToken = tokens[item.tokenIdx];
        const nextToken = tokens[nextItem.tokenIdx];

        // Check if token is in compound word list (e.g. 월요일, 일요일)
        const isCompound = N_INSERTION_COMPOUNDS.has(currentToken?.text || '');

        const pairContext = {
          sameWord: item.tokenIdx === nextItem.tokenIdx,
          betweenWords: item.tokenIdx !== nextItem.tokenIdx,
          boundary,
          wordBefore: wordContexts[item.tokenIdx],
          wordAfter: wordContexts[nextItem.tokenIdx],
          blockNInsertion: Boolean(wordContexts[nextItem.tokenIdx]?.blockNInsertion || (item.tokenIdx === nextItem.tokenIdx && !isCompound)),
          isCompound,
          forceTense: Boolean(forcedReason),
          tensificationReason: forcedReason || null
        };

        const resolution = resolveRules(updated, nextWorkJamo, pairContext);
        updated = resolution.current;
        nextUnit.workJamo = resolution.next;
        const { currentNotes, nextNotes } = distributeNotes(resolution.notes);
        notes = [...notes, ...currentNotes];
        if (nextNotes.length) {
          nextUnit.pendingNotes = [...(nextUnit.pendingNotes ?? []), ...nextNotes];
        }
      }

      // Final step for syllable: apply batchim neutralization (음절 끝소리 규칙)
      // If coda is unreleased and not followed by a vowel, normalize to 7 representative sounds
      const isLastBeforePause = !nextUnit || boundary?.hasHardBoundary;
      const isBeforeConsonant = nextUnit && nextUnit.workJamo && nextUnit.workJamo.initial !== 'ㅇ';
      if (isLastBeforePause || isBeforeConsonant) {
        const neutral = applyNeutralization(updated);
        if (neutral.final !== updated.final) {
          notes.push(buildNote('neutralization', {
            label: '收音代表音 (음절말 규칙)',
            before: updated.final,
            after: neutral.final,
            targets: ['current']
          }));
          updated = neutral;
        }
      }

      unit.workJamo = updated;

      // Recompose pronounced Hangul character
      const pronouncedChar = composeHangulSyllable(updated.initial, updated.medial, updated.final) || item.char;
      const baseRoman = composeRomanization(baseJamo);
      const finalRoman = composeRomanization(updated);
      const hasChange = (pronouncedChar !== item.char) || (notes.some(n => n.rule !== 'base'));

      notes.forEach(n => {
        if (n.rule && n.rule !== 'base') {
          if (!triggeredRules.has(n.rule)) {
            triggeredRules.set(n.rule, { ...n, count: 0 });
          }
          triggeredRules.get(n.rule).count++;
        }
      });

      segments.push({
        type: 'syllable',
        char: item.char,
        original: item.char,
        pronounced: pronouncedChar,
        baseJamo,
        finalJamo: updated,
        baseRoman,
        finalRoman,
        hasChange,
        notes
      });
    }

    const cleanPronounced = segments.map(s => s.pronounced || s.text || '').join('');
    const originalText = segments.map(s => s.original || s.text || '').join('');
    const fullRoman = segments.map(s => s.finalRoman || s.text || '').join('');
    const hasChange = segments.some(s => s.hasChange);
    const bracketPronounced = hasChange ? `[${cleanPronounced}]` : cleanPronounced;

    return {
      original: originalText,
      cleanPronounced,
      bracketPronounced,
      romanization: fullRoman,
      hasChange,
      segments,
      rules: Array.from(triggeredRules.values())
    };
  }

  /* ---------------- 7. HTML RENDERING & INTERACTIVE UI ---------------- */

  function renderAnnotatedHtml(sentence, options = {}) {
    const analysis = analyzeSentence(sentence);
    const mode = options.mode || 'badge'; // 'badge' | 'ruby' | 'inline'

    let html = '';
    analysis.segments.forEach(seg => {
      if (seg.type !== 'syllable') {
        html += seg.text.replace(/\n/g, '<br/>');
        return;
      }

      if (!seg.hasChange) {
        html += `<span class="ko-char">${seg.char}</span>`;
        return;
      }

      const activeNotes = (seg.notes || []).filter(n => n.rule !== 'base');
      const ruleLabel = activeNotes.map(n => n.label).join(', ') || '音变';
      const ruleDesc = activeNotes.map(n => n.description || n.label).join('； ') || '此处发音发生音变';
      const primaryRule = activeNotes[0]?.rule || 'tensification';
      const ruleColor = RULE_COLORS[primaryRule] || '#3b82f6';

      if (mode === 'ruby') {
        html += `<ruby class="ko-ruby" data-orig="${seg.char}" data-pron="${seg.pronounced}" data-rule="${ruleLabel}" data-desc="${ruleDesc}" style="--rule-color:${ruleColor};" onclick="KoPhonetics.showTooltip(this, event)" title="【${seg.char}】读作 [${seg.pronounced}] (${ruleLabel})">${seg.char}<rt>[${seg.pronounced}]</rt></ruby>`;
      } else {
        html += `<span class="ko-annotated-char" data-orig="${seg.char}" data-pron="${seg.pronounced}" data-rule="${ruleLabel}" data-desc="${ruleDesc}" data-roman="${seg.finalRoman}" style="--rule-color:${ruleColor};" onclick="KoPhonetics.showTooltip(this, event)" title="【${seg.char}】读作 [${seg.pronounced}] · ${ruleLabel}">` +
          `<span class="ko-char-orig">${seg.char}</span>` +
          `<span class="ko-char-badge" style="background:${ruleColor}20;color:${ruleColor};border-color:${ruleColor}40;">${seg.pronounced}</span>` +
          `</span>`;
      }
    });

    return html;
  }

  function renderWordPronunciation(word = '') {
    const res = analyzeSentence(word);
    if (!res.hasChange) return '';
    return `<span class="ko-word-pron-badge" title="标准发音">[발음: <strong>${res.cleanPronounced}</strong>]</span>`;
  }

  /* ---------------- 8. TOOLTIP POPUP CONTROLLER ---------------- */
  let _activePopover = null;

  function showTooltip(targetEl, event) {
    if (event) event.stopPropagation();
    closeTooltip();

    const orig = targetEl.getAttribute('data-orig') || '';
    const pron = targetEl.getAttribute('data-pron') || '';
    const rule = targetEl.getAttribute('data-rule') || '音变说明';
    const desc = targetEl.getAttribute('data-desc') || '';
    const roman = targetEl.getAttribute('data-roman') || '';

    const popover = document.createElement('div');
    popover.className = 'ko-phonetic-popover';
    popover.innerHTML = `
      <div class="ko-popover-header">
        <span class="ko-popover-rule">${rule}</span>
        <button type="button" class="ko-popover-close" onclick="KoPhonetics.closeTooltip()">&times;</button>
      </div>
      <div class="ko-popover-body">
        <div class="ko-popover-pron">
          <span class="orig">${orig}</span>
          <span class="arrow">➔</span>
          <strong class="pron">[${pron}]</strong>
          ${roman ? `<span class="roman">(${roman})</span>` : ''}
        </div>
        <p class="ko-popover-desc">${desc}</p>
      </div>
    `;

    document.body.appendChild(popover);
    _activePopover = popover;

    // Position popover
    const rect = targetEl.getBoundingClientRect();
    const popWidth = Math.min(280, window.innerWidth - 20);
    popover.style.width = popWidth + 'px';
    let top = rect.bottom + window.scrollY + 6;
    let left = rect.left + window.scrollX - (popWidth / 2) + (rect.width / 2);

    if (left < 10) left = 10;
    if (left + popWidth > window.innerWidth - 10) left = window.innerWidth - popWidth - 10;
    if (top + 160 > window.innerHeight + window.scrollY) {
      top = rect.top + window.scrollY - 130;
    }

    popover.style.top = top + 'px';
    popover.style.left = left + 'px';
  }

  function closeTooltip() {
    if (_activePopover && _activePopover.parentNode) {
      _activePopover.parentNode.removeChild(_activePopover);
    }
    _activePopover = null;
  }

  if (typeof document !== 'undefined') {
    document.addEventListener('click', (e) => {
      if (_activePopover && !e.target.closest('.ko-phonetic-popover')) {
        closeTooltip();
      }
    });

    // Auto-inject minimal CSS
    if (!document.getElementById('ko-phonetics-style')) {
      const st = document.createElement('style');
      st.id = 'ko-phonetics-style';
      st.textContent = `
        .ko-annotated-char {
          position: relative;
          display: inline-flex;
          flex-direction: column;
          align-items: center;
          cursor: pointer;
          margin: 0 1px;
          vertical-align: bottom;
          border-bottom: 2px solid var(--rule-color, #3b82f6);
        }
        .ko-char-orig {
          font-weight: 700;
        }
        .ko-char-badge {
          font-size: 10px;
          line-height: 12px;
          font-weight: 800;
          padding: 1px 3px;
          border-radius: 4px;
          border: 1px solid currentColor;
          margin-top: 1px;
          white-space: nowrap;
        }
        .ko-word-pron-badge {
          display: inline-block;
          font-size: 12px;
          color: #2563eb;
          background: #eff6ff;
          border: 1px solid #bfdbfe;
          border-radius: 6px;
          padding: 1px 6px;
          margin-left: 6px;
          vertical-align: middle;
        }
        .ko-phonetic-popover {
          position: absolute;
          z-index: 99999;
          background: #ffffff;
          color: #1e293b;
          border: 1.5px solid #bfdbfe;
          border-radius: 12px;
          box-shadow: 0 10px 25px -5px rgba(0,0,0,0.15), 0 8px 10px -6px rgba(0,0,0,0.1);
          padding: 10px 12px;
          box-sizing: border-box;
          animation: koPopIn 0.15s ease-out;
        }
        @keyframes koPopIn {
          from { opacity: 0; transform: translateY(-4px) scale(0.97); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .ko-popover-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 6px;
          border-bottom: 1px dashed #e2e8f0;
          padding-bottom: 4px;
        }
        .ko-popover-rule {
          font-size: 12px;
          font-weight: 800;
          color: #2563eb;
        }
        .ko-popover-close {
          background: transparent;
          border: none;
          font-size: 16px;
          color: #94a3b8;
          cursor: pointer;
          line-height: 1;
        }
        .ko-popover-pron {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 15px;
          margin-bottom: 6px;
        }
        .ko-popover-pron .orig { font-weight: 600; color: #475569; text-decoration: line-through; }
        .ko-popover-pron .arrow { color: #94a3b8; font-size: 12px; }
        .ko-popover-pron .pron { color: #dc2626; font-size: 17px; }
        .ko-popover-pron .roman { color: #64748b; font-size: 12px; }
        .ko-popover-desc {
          font-size: 12px;
          line-height: 1.45;
          color: #334155;
          margin: 0;
        }
      `;
      (document.head || document.documentElement).appendChild(st);
    }
  }

  /* ---------------- 9. PUBLIC API EXPORTS ---------------- */
  return {
    isHangul,
    decompose,
    compose: composeHangulSyllable,
    composeHangulSyllable,
    tokenize: tokenizeSentence,
    classifyWord,
    analyze: analyzeSentence,
    romanize: analyzeSentence,
    renderAnnotatedHtml,
    renderWordPronunciation,
    showTooltip,
    closeTooltip,
    RULE_COLORS,
    RULE_REFERENCES,
    RULE_DESCRIPTIONS,
    CHOSEONG,
    JUNGSEONG,
    JONGSEONG
  };
}));
