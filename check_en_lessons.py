#!/usr/bin/env python3
"""
英文课文词汇规则校验（复现率 + 词频）。

用法:
  python3 check_en_lessons.py            # 校验，不达标时退出码为 1
  python3 check_en_lessons.py --report   # 额外打印每课词汇明细

规则（数值在下方 RULES 中集中配置）:
  R1 词频档位：基石词（vocabulary）必须落在本课 level 对应的词频档位内。
  R2 超纲词：对话 / 语块中超出档位的词，必须是本课或之前课的基石词、
     本课 topicWords（情境专有词，需在课内注释），或 properNouns。
  R3 情境词上限：每课 topicWords 不超过 MAX_TOPIC_WORDS 个。
  R4 跨课复现：第 i 课的 6 个基石词里，至少 MIN_RECUR_WORDS 个要在
     之后 RECUR_WINDOW 课的对话里合计出现 ≥ MIN_RECUR_HITS 次。
     后续课不足 RECUR_WINDOW 课时只提示（pending），不判失败。
  R5 自身出现：每个基石词必须出现在本课对话中。

词频数据：data/wordlists/wordfreq-en-top10000.txt（wordfreq 3.1.1，CC BY-SA 4.0），
另有 data/wordlists/en-core-everyday.txt 补充被网络语料低估的 A1 日常词。
一个词的词频名次取其各种屈折形式（复数/过去式/进行时等）还原后名次的最小值。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "en-lessons-data.json"
RANK_FILE = ROOT / "data" / "wordlists" / "wordfreq-en-top10000.txt"
CORE_FILE = ROOT / "data" / "wordlists" / "en-core-everyday.txt"

RULES = {
    # level -> 允许的最大词频名次（wordfreq 名次；其列表含人名和网络用语，
    # 前 1500 名大致相当于 NGSL 前 1000 词族）
    "BAND": {1: 1500, 2: 2500, 3: 3500},
    "VOCAB_PER_LESSON": 6,
    "MAX_TOPIC_WORDS": 3,
    "RECUR_WINDOW": 3,
    "MIN_RECUR_WORDS": 4,
    "MIN_RECUR_HITS": 2,
}

CONTRACTION_SUFFIXES = ("n't", "'s", "'m", "'re", "'ll", "'d", "'ve")
IRREGULAR_NEG = {"won't": "will", "can't": "can", "shan't": "shall"}
# 常用不规则变化（屈折形式 -> 原形），用于词频还原和复现计数
IRREGULAR = {
    "forgot": "forget", "forgotten": "forget", "bought": "buy", "found": "find",
    "got": "get", "gotten": "get", "took": "take", "taken": "take", "went": "go",
    "gone": "go", "came": "come", "left": "leave", "brought": "bring",
    "kept": "keep", "met": "meet", "paid": "pay", "said": "say", "told": "tell",
    "made": "make", "thought": "think", "ate": "eat", "eaten": "eat",
    "drank": "drink", "saw": "see", "seen": "see", "gave": "give", "given": "give",
    "knew": "know", "known": "know", "felt": "feel", "began": "begin",
    "begun": "begin", "wore": "wear", "worn": "wear", "carried": "carry",
    "better": "good", "best": "good", "bigger": "big", "biggest": "big",
    "larger": "large", "largest": "large", "children": "child", "people": "person",
}


def load_ranks():
    ranks = {}
    n = 0
    for line in RANK_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        n += 1
        ranks.setdefault(line.strip(), n)
    # 日常核心词：视同 L1 档位以内（取 min，不会抬高已有名次）
    core_rank = RULES["BAND"][1]
    for line in CORE_FILE.read_text(encoding="utf-8").splitlines():
        w = line.strip()
        if w and not w.startswith("#"):
            ranks[w] = min(ranks.get(w, core_rank), core_rank)
    return ranks


def candidates(word):
    """词本身 + 规则屈折还原后的候选原形。"""
    w = word.lower()
    out = {w}
    if w in IRREGULAR_NEG:
        out.add(IRREGULAR_NEG[w])
    if w in IRREGULAR:
        out.add(IRREGULAR[w])
    for suf in CONTRACTION_SUFFIXES:
        if w.endswith(suf) and len(w) > len(suf):
            out.add(w[: -len(suf)])
    base = set(out)
    for b in base:
        if b.endswith("ies") and len(b) > 4:
            out.add(b[:-3] + "y")
        if b.endswith("ied") and len(b) > 4:
            out.add(b[:-3] + "y")
        if b.endswith("es") and len(b) > 3:
            out.add(b[:-2])
        if b.endswith("s") and not b.endswith("ss") and len(b) > 3:
            out.add(b[:-1])
        if b.endswith("ed") and len(b) > 3:
            out.add(b[:-2])
            out.add(b[:-1])
            if len(b) > 4 and b[-3] == b[-4]:
                out.add(b[:-3])
        if b.endswith("ing") and len(b) > 4:
            out.add(b[:-3])
            out.add(b[:-3] + "e")
            if len(b) > 5 and b[-4] == b[-5]:
                out.add(b[:-4])
        if b.endswith("ly") and len(b) > 4:
            out.add(b[:-2])
            if b.endswith("ily"):
                out.add(b[:-3] + "y")
    return out


def rank_of(word, ranks):
    best = None
    for c in candidates(word):
        r = ranks.get(c)
        if r is not None and (best is None or r < best):
            best = r
    return best


def same_lexeme(token, headword):
    """token 是否为 headword 的屈折形式。"""
    h = headword.lower()
    return h in candidates(token)


TOKEN_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


ORDINAL_RE = re.compile(r"\d+(?:st|nd|rd|th)\b")


def tokens(text):
    text = ORDINAL_RE.sub(" ", text.replace("’", "'"))
    return TOKEN_RE.findall(text)


def count_hits(headword, texts):
    return sum(1 for t in texts for tok in tokens(t) if same_lexeme(tok, headword))


def lesson_texts(lesson):
    return [line["en"] for line in lesson.get("dialogue", [])]


def check(lessons, ranks, report=False):
    errors, warnings, lines = [], [], []
    known_vocab = set()  # 之前各课的基石词
    known_topic = set()  # 之前各课的情境词

    for idx, lesson in enumerate(lessons):
        lid = lesson["id"]
        level = lesson.get("level", 1)
        band = RULES["BAND"][level]
        vocab = [v["word"].lower() for v in lesson.get("vocabulary", [])]
        topic = [t["word"].lower() for t in lesson.get("topicWords", [])]
        proper = {p.lower() for p in lesson.get("properNouns", [])}
        for line in lesson.get("dialogue", []):
            proper.update(tok.lower() for tok in tokens(line.get("speakerName", "")))
        texts = lesson_texts(lesson)

        # R1 / R5
        if len(vocab) != RULES["VOCAB_PER_LESSON"]:
            errors.append(f"{lid}: 基石词应为 {RULES['VOCAB_PER_LESSON']} 个，实际 {len(vocab)} 个")
        for w in vocab:
            r = rank_of(w, ranks)
            if r is None or r > band:
                errors.append(f"{lid}: 基石词 '{w}' 词频名次 {r or '>10000'} 超出 L{level} 档位 {band}")
            if count_hits(w, texts) == 0:
                errors.append(f"{lid}: 基石词 '{w}' 没有出现在本课对话中")
            if w in known_vocab:
                errors.append(f"{lid}: 基石词 '{w}' 在之前的课里已经教过")

        # R3
        if len(topic) > RULES["MAX_TOPIC_WORDS"]:
            errors.append(f"{lid}: 情境词 {len(topic)} 个，超过上限 {RULES['MAX_TOPIC_WORDS']}")

        # R2
        allowed = set(vocab) | known_vocab | set(topic) | known_topic | proper
        scan = texts + [c["text"] for c in lesson.get("chunks", [])]
        off = {}
        all_tokens = set()
        for t in scan:
            for tok in tokens(t):
                low = tok.lower()
                all_tokens.add(low)
                r = rank_of(low, ranks)
                if r is not None and r <= band:
                    continue
                if any(same_lexeme(low, a) for a in allowed) or low in proper:
                    continue
                off[low] = r
        for w, r in sorted(off.items()):
            errors.append(f"{lid}: 超纲词 '{w}'（名次 {r or '>10000'}，L{level} 档位 {band}），"
                          f"请替换，或列入 topicWords/properNouns")
        unused_topic = [t for t in topic if count_hits(t, texts) == 0]
        for t in unused_topic:
            warnings.append(f"{lid}: 情境词 '{t}' 未在对话中出现")

        # R4
        window = lessons[idx + 1: idx + 1 + RULES["RECUR_WINDOW"]]
        future = [t for l in window for t in lesson_texts(l)]
        hits = {w: count_hits(w, future) for w in vocab}
        ok = [w for w, h in hits.items() if h >= RULES["MIN_RECUR_HITS"]]
        need = RULES["MIN_RECUR_WORDS"]
        detail = ", ".join(f"{w}×{h}" for w, h in hits.items())
        if len(window) < RULES["RECUR_WINDOW"]:
            if len(ok) < need:
                warnings.append(f"{lid}: 复现待后续课补足（{len(ok)}/{need} 达标；{detail}）")
        elif len(ok) < need:
            errors.append(f"{lid}: 复现不足，只有 {len(ok)}/{need} 个基石词在之后 "
                          f"{RULES['RECUR_WINDOW']} 课出现 ≥{RULES['MIN_RECUR_HITS']} 次（{detail}）")

        if report:
            words = len([t for x in texts for t in tokens(x)])
            lines.append(f"{lid} L{level} 对话 {len(texts)} 句 / {words} 词 / {len(all_tokens)} 个不同词")
            lines.append(f"    基石词: " + ", ".join(f"{w}(#{rank_of(w, ranks)})" for w in vocab))
            lines.append(f"    情境词: {', '.join(topic) or '-'}")
            lines.append(f"    后续复现: {detail}")

        known_vocab |= set(vocab)
        known_topic |= set(topic)

    return errors, warnings, lines


def main():
    report = "--report" in sys.argv
    lessons = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    ranks = load_ranks()
    errors, warnings, lines = check(lessons, ranks, report)
    for l in lines:
        print(l)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    all_text = [t for l in lessons for t in lesson_texts(l)]
    distinct = {tok.lower() for t in all_text for tok in tokens(t)}
    print(f"\n{len(lessons)} 课，对话共 {len(all_text)} 句，{len(distinct)} 个不同词；"
          f"{len(errors)} 个错误，{len(warnings)} 个提示")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
