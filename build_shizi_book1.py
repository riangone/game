#!/usr/bin/env python3
"""Build 《中文》第一册 第1～10课 (shizi-1.html … shizi-10.html) in the Book 4 page format.

The page is rendered from shizi-12.html (itself built on hanjia-jianwen.html): only the
lesson-specific strings and the DATA block are swapped. Lesson content lives in
shizi_book1_data.py.

Usage:
  python3 build_shizi_book1.py            # all lessons 1-10: HTML + audio + clause data
  python3 build_shizi_book1.py 3 7        # only lessons 3 and 7
  python3 build_shizi_book1.py --html-only 3
  python3 build_shizi_book1.py --book2 1     # 第二册: zw-2-N.html from zhongwen_book2_data.py
  python3 build_shizi_book1.py --book2xin 1  # 第二册新版: zw-2x-N.html from zhongwen_book2_xin_data.py

Audio per lesson (edge-tts, same voices as Book 4 and lessons 11-12):
  audio/shiziN/          title, st*, zi*, vc1-12, cloze_1-12   (zh-CN-XiaoxiaoNeural)
  audio/shiziN_en|ja|ko/ st* translations (Jenny / Nanami / SunHi)
  audio/shiziN_clause/   st{n}_c{m} clause clips for the ClausePlayer
  data/shiziN_clauses.json + the "shiziN" entry in data/lesson-clauses-data.js
"""
import asyncio
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

if "--book2xin" in sys.argv:
    from zhongwen_book2_xin_data import LESSONS
elif "--book2" in sys.argv:
    from zhongwen_book2_data import LESSONS
else:
    from shizi_book1_data import LESSONS

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "shizi-12.html"
ZH_VOICE, ZH_RATE = "zh-CN-XiaoxiaoNeural", "-12%"
CLAUSE_RATE = "-10%"
LANG_VOICES = {"en": ("en-US-JennyNeural", "-8%"), "ja": ("ja-JP-NanamiNeural", "-10%"),
               "ko": ("ko-KR-SunHiNeural", "-8%")}

# Strings in shizi-12.html that are specific to lesson 12 (each must be present).
T_TITLE = "新年到"


def ids(n, L):
    """(page file stem, audio/clause slug, book label, TOC page) for a lesson."""
    if L.get("book") == "2x":
        return f"zw-2x-{n}", f"zw2x_{n}", "第二册（新版）", "zw-ty-2-xin.html"
    if L.get("book") == 2:
        return f"zw-2-{n}", f"zw2_{n}", "第二册", "zw-ty-2.html"
    return f"shizi-{n}", f"shizi{n}", "第一册", "zw-ty-1.html"


def js(v):
    return json.dumps(v, ensure_ascii=False)


def obj(d):
    return "{" + ", ".join(f"{k}:{js(v)}" for k, v in d.items()) + "}"


# ------------------------------------------------------------------ data normalisation
def normalise(n, L):
    story = [dict(id=f"st{i+1}", zh=s[0], py=s[1], en=s[2], jp=s[3], ko=s[4]) for i, s in enumerate(L["story"])]
    chars = [dict(id=f"zi{i+1}", zh=c[0], py=c[1], radical=c[2], words=c[3], meaning=c[4], meaningJp=c[5],
                  meaningKo=c[6], context=c[7]) for i, c in enumerate(L["chars"])]
    vocab = [dict(id=f"vc{i+1}", zh=v[0], py=v[1], meaning=v[2], meaningJp=v[3], meaningKo=v[4], emoji=v[5])
             for i, v in enumerate(L["vocab"])]
    quiz = [dict(q=q[0], opts=q[1], a=q[2]) for q in L["quiz"]]
    scramble = [dict(id=f"st{i}", zh=story[i-1]["zh"], tokens=toks) for i, toks in sorted(L["scramble"].items())]
    cloze = []
    for (si, before, ans, after, apy, opts, hint) in L["cloze_text"]:
        s = story[si-1]
        cloze.append(dict(type="text", before=before, answer=ans, after=after, py=s["py"], en=s["en"], jp=s["jp"],
                          ko=s["ko"], answerPy=apy, options=opts, hint="课文原句 · " + hint))
    for (before, ans, after, py, en, ja, ko, apy, opts, hint) in L["cloze_micro"]:
        cloze.append(dict(type="micro", before=before, answer=ans, after=after, py=py, en=en, jp=ja, ko=ko,
                          answerPy=apy, options=opts, hint="微情境拓展 · " + hint))
    for i, c in enumerate(cloze):
        c_id = {"id": f"s{n}_c{i+1}"}
        c_id.update(c)
        c_id["audioId"] = f"cloze_{i+1}"
        cloze[i] = c_id
    clauses = {}
    for i, s in enumerate(L["story"]):
        clauses[f"st{i+1}"] = L.get("clauses", {}).get(i + 1, [tuple(s)])
    return dict(story=story, chars=chars, vocab=vocab, quiz=quiz, scramble=scramble, cloze=cloze, clauses=clauses)


def validate(n, L, D):
    errs = []
    if len(D["vocab"]) != 12: errs.append(f"vocab count {len(D['vocab'])}")
    if len(D["cloze"]) != 12: errs.append(f"cloze count {len(D['cloze'])}")
    if len(D["quiz"]) != 7: errs.append(f"quiz count {len(D['quiz'])}")
    story_zh = [s["zh"] for s in D["story"]]
    for c in D["cloze"]:
        full = c["before"] + c["answer"] + c["after"]
        if c["type"] == "text" and full not in story_zh: errs.append(f"cloze text not in story: {full}")
        if c["answer"] not in c["options"]: errs.append(f"cloze answer not in options: {full}")
        if len(set(c["options"])) != 4: errs.append(f"cloze options not 4 unique: {c['options']}")
        if "'" in full: errs.append(f"apostrophe breaks inline JS: {full}")
    for q in D["quiz"]:
        if not (0 <= q["a"] < len(q["opts"])) or len(set(q["opts"])) != 4: errs.append(f"quiz bad: {q['q']}")
    for s in D["scramble"]:
        if "".join(s["tokens"]) != s["zh"]: errs.append(f"scramble tokens != sentence: {s['zh']}")
    for s in D["story"]:
        cl = "".join(c[0] for c in D["clauses"][s["id"]])
        if cl != s["zh"]: errs.append(f"clauses != sentence: {s['zh']}")
    for c in D["chars"]:
        if not (ROOT / "data" / "hanzi" / f"{c['zh']}.json").exists(): errs.append(f"missing stroke data {c['zh']}")
    if len({v["zh"] for v in D["vocab"]}) != 12: errs.append("duplicate vocab")
    for s in D["story"] + D["vocab"]:
        if "'" in s["zh"]: errs.append(f"apostrophe in zh: {s['zh']}")
    if errs:
        raise SystemExit(f"Lesson {n} data errors:\n  " + "\n  ".join(errs))


# ------------------------------------------------------------------ HTML
def sub_once(html, old, new, count=1):
    found = html.count(old)
    if found != count:
        raise SystemExit(f"template: expected {count}x {old!r}, found {found}")
    return html.replace(old, new)


def render(n, L, D):
    html = TEMPLATE.read_text(encoding="utf-8")
    title = L["title"]
    page, slug, book, toc = ids(n, L)
    k = len(D["chars"])
    page_title = ("" if book == "第一册" else f"{book} ") + f"第{n}课 {title} - {L['tag']} ({L['title_en']})"
    desc = f"《中文》小学版{book}第{n}课《{title}》：{L['desc']}，带拼音逐句朗读，学习{k}个生字笔顺、词语卡片并做听读练习。"

    html = re.sub(r"<title>.*?</title>", f"<title>{page_title}</title>", html, count=1)
    html = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, html, count=1)
    html = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + page_title, html, count=1)
    html = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + desc, html, count=1)
    html = sub_once(html, "shizi-12.html", f"{page}.html", 2)
    html = sub_once(html, 'href="zw-ty-1.html" class="nav-btn" title="第1册目录', f'href="{toc}" class="nav-btn" title="第{toc[6]}册目录')
    html = sub_once(html, "?v=shizi12", f"?v={slug}b4", 2)
    html = sub_once(html, '<h1 id="headerTitle">第12课 · 新年到</h1>', f'<h1 id="headerTitle">第{n}课 · {title}</h1>')
    html = sub_once(html, '<div class="lantern">🧧</div>', f'<div class="lantern">{L["emoji"]}</div>')
    html = sub_once(html, '<h2 class="title">12 新年到</h2>', f'<h2 class="title">{n} {title}</h2>')
    html = re.sub(r'(<p class="sub">)Spring Festival Is Coming · [^<]*', lambda m: m.group(1) + f"{L['title_en']} · {L['sub']}", html, count=1)
    html = sub_once(html, "12个生字 · 笔顺描红", f"{k}个生字 · 笔顺描红")
    html = sub_once(html, "翻卡认字 (12词)", f"翻卡认字 ({len(D['vocab'])}词)")
    html = sub_once(html, "📖 新年到</h2>", f"📖 {title}</h2>")
    html = sub_once(html, "playClip('title', '新年到', null, 'zh-CN')", f"playClip('title', '{title}', null, 'zh-CN')", 2)
    html = sub_once(html, "《新年到》</span>", f"《{title}》</span>")
    html = sub_once(html, ">xīn nián dào</span>", f">{L['title_py']}</span>")
    html = sub_once(html, "📜 新年到 · 全文", f"📜 {title} · 全文")
    html = sub_once(html, "'新年到_第'", f"'{title}_第'", 2)
    html = sub_once(html, "generate_shizi12_audio.py", "build_shizi_book1.py")
    if L.get("book") == "2x":
        # 新版第二册：读课文 / 朗读全文 的英日韩翻译默认关闭（拼音仍默认显示），点 chip 可打开。
        html = sub_once(html, "let storyIdx = 0, showPy = true, showEn = true, showJp = true, showKo = true;",
                        "let storyIdx = 0, showPy = true, showEn = false, showJp = false, showKo = false;")
        html = sub_once(html, "let fullPy = true, fullEn = true, fullJp = true, fullKo = true;",
                        "let fullPy = true, fullEn = false, fullJp = false, fullKo = false;")
        for chip in ("chipEn", "chipJp", "chipKo", "chipFullEn", "chipFullJp", "chipFullKo"):
            html = sub_once(html, f'<div class="chip active" id="{chip}"', f'<div class="chip" id="{chip}"')

    start = html.index("/* ---------------- DATA ---------------- */")
    end = html.index("/* ---------------- STATE ---------------- */")
    kind = "识字课：按课本生字分组排成课文行" if title.startswith("识字") else "逐字与教材一致"
    data = ["/* ---------------- DATA ---------------- */",
            "// Generated by build_shizi_book1.py from shizi_book1_data.py — edit the data file, not this block.",
            "const CHARACTERS = [", ",\n".join("  " + obj(c) for c in D["chars"]), "];", "",
            f"// 课文《{title}》（《中文》小学版{book}第{n}课，{kind}）",
            "const STORY = [", ",\n".join("  " + obj(s) for s in D["story"]), "];", "",
            f"// 生词卡片 ({len(D['vocab'])} words)",
            "const VOCAB = [", ",\n".join("  " + obj(v) for v in D["vocab"]), "];", "",
            "// 读解练习",
            "const QUIZ = [", ",\n".join("  " + obj(q) for q in D["quiz"]), "];", "",
            "// 连词成句",
            "const SCRAMBLE_SENTENCES = [", ",\n".join("  " + obj(s) for s in D["scramble"]), "];", "",
            "// 选词填空 (12 Questions: 8 课文原句 + 4 微情境拓展)",
            "const CLOZE_QUESTIONS = [", ",\n".join("  " + obj(c) for c in D["cloze"]), "];", "", ""]
    html = html[:start] + "\n".join(data) + html[end:]

    html = html.replace("shizi12", slug)
    for leftover in ("shizi12", "新年到", "xīn nián", "s12_c"):
        # Cloze ids are f"s{n}_c…", so for lesson 12 "s12_c" is legitimate, not a template leftover.
        if leftover == "s12_c" and n == 12:
            continue
        if leftover in html:
            raise SystemExit(f"lesson {n}: leftover {leftover!r} in rendered page")
    (ROOT / f"{page}.html").write_text(html, encoding="utf-8")
    print(f"HTML  {page}.html  ({k} chars, {len(D['story'])} lines)")


# ------------------------------------------------------------------ audio
def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                         capture_output=True, text=True, check=True)
    return round(float(out.stdout.strip()), 3)


async def build_audio(n, L, D):
    import edge_tts
    slug = ids(n, L)[1]
    for d in (slug, f"{slug}_en", f"{slug}_ja", f"{slug}_ko", f"{slug}_clause"):
        shutil.rmtree(ROOT / "audio" / d, ignore_errors=True)  # old pages' clips live in backup/
    sem = asyncio.Semaphore(4)
    jobs, failed = [], []
    tts = L.get("tts", {})

    def job(path, text, voice, rate):
        async def run():
            path.parent.mkdir(parents=True, exist_ok=True)
            for attempt in range(3):
                try:
                    async with sem:
                        await edge_tts.Communicate(text, voice, rate=rate).save(str(path))
                    if path.stat().st_size > 500:
                        return
                except Exception as e:  # noqa: BLE001 - retry any network error
                    err = e
                await asyncio.sleep(2 * (attempt + 1))
            failed.append(f"{path.relative_to(ROOT)} ({text})")
        jobs.append(run())

    zh_dir = ROOT / "audio" / slug
    items = [("title", L["title_tts"])] + [(s["id"], s["zh"]) for s in D["story"]]
    # tts may be keyed by card id (e.g. "zi8") when a character repeats with another reading
    items += [(c["id"], tts.get(c["id"], tts.get(c["zh"], c["zh"]))) for c in D["chars"]]
    items += [(v["id"], v["zh"]) for v in D["vocab"]]
    items += [(c["audioId"], c["before"] + c["answer"] + c["after"]) for c in D["cloze"]]
    for fid, text in items:
        job(zh_dir / f"{fid}.mp3", text, ZH_VOICE, ZH_RATE)
    for key, lang in (("en", "en"), ("jp", "ja"), ("ko", "ko")):
        voice, rate = LANG_VOICES[lang]
        for s in D["story"]:
            job(ROOT / "audio" / f"{slug}_{lang}" / f"{s['id']}.mp3", s[key], voice, rate)
    clause_dir = ROOT / "audio" / f"{slug}_clause"
    for s in D["story"]:
        for ci, c in enumerate(D["clauses"][s["id"]]):
            job(clause_dir / f"{s['id']}_c{ci+1}.mp3", c[0], ZH_VOICE, CLAUSE_RATE)
    total = len(jobs)
    await asyncio.gather(*jobs)
    if failed:
        raise SystemExit(f"lesson {n}: {len(failed)} audio files failed:\n  " + "\n  ".join(failed))
    print(f"AUDIO {slug}: {total} mp3")

    g, sentences = 0.0, []
    for si, s in enumerate(D["story"]):
        start, local, citems = g, 0.0, []
        for ci, (czh, cpy, cen, cja, cko) in enumerate(D["clauses"][s["id"]]):
            cid = f"{s['id']}_c{ci+1}"
            d = duration(clause_dir / f"{cid}.mp3")
            citems.append({"id": cid, "sentId": s["id"], "sentIndex": si, "clauseIndex": ci,
                           "zh": czh, "py": cpy, "en": cen, "jp": cja, "ko": cko,
                           "audioUrl": f"audio/{slug}_clause/{cid}.mp3", "duration": d,
                           "sentOffsetStart": round(local, 3), "sentOffsetEnd": round(local + d, 3),
                           "globalOffsetStart": round(g, 3), "globalOffsetEnd": round(g + d, 3)})
            local += d
            g += d
        sentences.append({"sentId": s["id"], "sentIndex": si, "sentZh": s["zh"], "sentPy": s["py"],
                          "sentEn": s["en"], "sentJp": s["jp"], "sentKo": s["ko"], "clauses": citems,
                          "duration": round(local, 3), "globalOffsetStart": round(start, 3),
                          "globalOffsetEnd": round(g, 3), "clauseCount": len(citems)})
    meta = {"lesson": slug, "title": L["title"], "totalSentences": len(sentences),
            "totalClauses": sum(s["clauseCount"] for s in sentences),
            "totalDuration": round(g, 3), "sentences": sentences}
    (ROOT / "data" / f"{slug}_clauses.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def merge_bundle(metas):
    bundle_path = ROOT / "data" / "lesson-clauses-data.js"
    prefix = "window.ALL_LESSON_CLAUSES = "
    raw = bundle_path.read_text(encoding="utf-8").strip()
    assert raw.startswith(prefix) and raw.endswith(";")
    bundle = json.loads(raw[len(prefix):-1])
    for m in metas:
        bundle[m["lesson"]] = m
    bundle_path.write_text(prefix + json.dumps(bundle, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")


def register_clause_player(ns):
    """ns: [(page, slug)]"""
    path = ROOT / "js" / "clause-player.js"
    src = path.read_text(encoding="utf-8")
    anchor = "    'shizi-11': 'shizi11',"
    assert anchor in src
    add = "".join(f"    '{page}': '{slug}',\n" for page, slug in ns if f"'{page}':" not in src)
    if add:
        src = src.replace(anchor, add + anchor)
        path.write_text(src, encoding="utf-8")


def main():
    args = sys.argv[1:]
    html_only = "--html-only" in args
    ns = [int(a) for a in args if a.isdigit()] or sorted(LESSONS)
    data = {}
    for n in ns:
        D = normalise(n, LESSONS[n])
        validate(n, LESSONS[n], D)
        data[n] = D
    for n in ns:
        render(n, LESSONS[n], data[n])
    if html_only:
        return
    metas = [asyncio.run(build_audio(n, LESSONS[n], data[n])) for n in ns]
    merge_bundle(metas)
    register_clause_player([ids(n, LESSONS[n])[:2] for n in ns])
    print("clause bundle + clause-player updated")


if __name__ == "__main__":
    main()
