#!/usr/bin/env python3
"""Wire up the Korean (ko-KR) UI/audio layer in a lesson HTML file, mirroring
the existing English/Japanese architecture exactly:
  - CSS: .sentence-ko / .full-sentence .sentence-ko / .cloze-ko
  - Story reader: storyKoRow + mini speak button + chipKo toggle
  - Full text reader: ko row in template + chipFullKo toggle
  - Cloze test: clozeKo text line
  - JS state: showKo / fullShowKo, toggleStoryKo / toggleFullKo
  - renderStory / renderFullText / renderCloze updated to populate ko
  - charMeaning / flashMeaning (and PROPER_NOUNS-based meaning renders)
    append meaningKo
  - playClip(): 'ko-KR' -> audio/<slug>_ko/
  - pickVoice()/speakText(): koVoice selection

Idempotent: each substitution only applies if the "before" pattern is still
present (so re-running on an already-patched file is a safe no-op) and it
prints a warning (not an error) if a pattern isn't found, so unusual lessons
can be hand-finished.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KO_COLOR = "#059669"


def sub1(text, pattern, repl, label, flags=re.DOTALL, required=True):
    new_text, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n == 0:
        print(f"  [WARN] pattern not found: {label}")
        return text
    return new_text


def patch(text, slug):
    if 'id="storyKoRow"' in text:
        print("  [SKIP] already patched (storyKoRow marker present)")
        return text
    # ---------- CSS ----------
    text = sub1(
        text,
        r'(\.sentence-jp\{[^}]*\})',
        r'\1\n  .sentence-ko{font-size:13px;color:' + KO_COLOR + r';text-align:center;}',
        "css .sentence-jp",
    )
    text = sub1(
        text,
        r'(\.full-sentence \.sentence-jp\{[^}]*\})',
        r'\1\n  .full-sentence .sentence-ko{font-size:12px;text-align:left;color:' + KO_COLOR + r';margin-top:2px;}',
        "css .full-sentence .sentence-jp",
    )
    text = sub1(
        text,
        r'(\.cloze-jp\{[^}]*\})',
        r'\1\n  .cloze-ko{font-size:12px;color:' + KO_COLOR + r';font-style:italic;text-align:center;}',
        "css .cloze-jp",
    )

    # ---------- HTML: story reader ----------
    text = sub1(
        text,
        r'(<div class="lang-line-row" id="storyJpRow"[^>]*>\s*'
        r'<div class="sentence-jp" id="storyJp"></div>\s*'
        r'<button class="mini-speak-btn" onclick="event\.stopPropagation\(\); playClip\(STORY\[storyIdx\]\.id, STORY\[storyIdx\]\.jp\|\|\'\', null, \'ja-JP\'\)" title="播放日文发音">🔊</button>\s*'
        r'</div>)',
        r"""\1
        <div class="lang-line-row" id="storyKoRow" style="display:flex;align-items:center;justify-content:center;gap:6px;">
          <div class="sentence-ko" id="storyKo"></div>
          <button class="mini-speak-btn" onclick="event.stopPropagation(); playClip(STORY[storyIdx].id, STORY[storyIdx].ko||'', null, 'ko-KR')" title="播放韩文发音">🔊</button>
        </div>""",
        "html storyJpRow block",
    )
    text = sub1(
        text,
        r'(<div class="chip active" id="chipJp" onclick="toggleStoryJp\(\)">日本語</div>)',
        r'\1\n        <div class="chip active" id="chipKo" onclick="toggleStoryKo()">한국어</div>',
        "html chipJp toggle row",
    )

    # ---------- HTML: full text reader chip row ----------
    text = sub1(
        text,
        r'(<div class="chip active" id="chipFullJp" onclick="toggleFullJp\(\)">日本語</div>)',
        r'\1\n        <div class="chip active" id="chipFullKo" onclick="toggleFullKo()">한국어</div>',
        "html chipFullJp toggle row",
    )

    # ---------- HTML: cloze ----------
    text = sub1(
        text,
        r'(<div class="cloze-jp" id="clozeJp"></div>)',
        r'\1\n          <div class="cloze-ko" id="clozeKo"></div>',
        "html clozeJp div",
    )

    # ---------- JS: state vars ----------
    text = sub1(
        text,
        r'let storyIdx = 0, showPy = true, showEn = true, showJp = true;',
        r"let storyIdx = 0, showPy = true, showEn = true, showJp = true, showKo = true;",
        "js story state vars",
    )
    text = sub1(
        text,
        r'let fullPlaying = false, fullPlayIdx = 0, fullShowPy = true, fullShowEn = true, fullShowJp = true;',
        r"let fullPlaying = false, fullPlayIdx = 0, fullShowPy = true, fullShowEn = true, fullShowJp = true, fullShowKo = true;",
        "js full state vars",
    )

    # ---------- JS: renderStory ----------
    text = sub1(
        text,
        r"(document\.getElementById\('storyJp'\)\.textContent = s\.jp \|\| '';)",
        r"\1\n  document.getElementById('storyKo').textContent = s.ko || '';",
        "js renderStory textContent ko",
    )
    text = sub1(
        text,
        r"(document\.getElementById\('storyJp'\)\.style\.display = showJp \? 'block' : 'none';)",
        r"\1\n  document.getElementById('storyKo').style.display = showKo ? 'block' : 'none';",
        "js renderStory display ko",
    )
    text = sub1(
        text,
        r"(const jpRow = document\.getElementById\('storyJpRow'\); if\(jpRow\) jpRow\.style\.display = \(showJp && s\.jp\) \? 'flex' : 'none';)",
        r"\1\n  const koRow = document.getElementById('storyKoRow'); if(koRow) koRow.style.display = (showKo && s.ko) ? 'flex' : 'none';",
        "js renderStory koRow display",
    )
    text = sub1(
        text,
        r"function toggleStoryJp\(\)\{ showJp = !showJp; document\.getElementById\('chipJp'\)\.classList\.toggle\('active', showJp\); renderStory\(\); \}",
        r"function toggleStoryJp(){ showJp = !showJp; document.getElementById('chipJp').classList.toggle('active', showJp); renderStory(); }\n"
        r"function toggleStoryKo(){ showKo = !showKo; document.getElementById('chipKo').classList.toggle('active', showKo); renderStory(); }",
        "js toggleStoryJp -> add toggleStoryKo",
    )

    # ---------- JS: renderFullText template ----------
    text = sub1(
        text,
        r'(<div style="display:\$\{\(fullShowJp && s\.jp\)\?\'flex\':\'none\'\};align-items:center;justify-content:center;gap:6px;">\s*'
        r'<div class="sentence-jp">\$\{s\.jp\|\|\'\'\}</div>\s*'
        r'<button class="mini-speak-btn" onclick="event\.stopPropagation\(\); playClip\(STORY\[\$\{idx\}\]\.id, STORY\[\$\{idx\}\]\.jp\|\|\'\', null, \'ja-JP\'\);" title="播放日文发音">🔊</button>\s*'
        r'</div>)',
        r"""\1
      <div style="display:${(fullShowKo && s.ko)?'flex':'none'};align-items:center;justify-content:center;gap:6px;">
        <div class="sentence-ko">${s.ko||''}</div>
        <button class="mini-speak-btn" onclick="event.stopPropagation(); playClip(STORY[${idx}].id, STORY[${idx}].ko||'', null, 'ko-KR');" title="播放韩文发音">🔊</button>
      </div>""",
        "js renderFullText template ko row",
    )
    text = sub1(
        text,
        r"function toggleFullJp\(\)\{ fullShowJp = !fullShowJp; document\.getElementById\('chipFullJp'\)\.classList\.toggle\('active', fullShowJp\); renderFullText\(\); \}",
        r"function toggleFullJp(){ fullShowJp = !fullShowJp; document.getElementById('chipFullJp').classList.toggle('active', fullShowJp); renderFullText(); }\n"
        r"function toggleFullKo(){ fullShowKo = !fullShowKo; document.getElementById('chipFullKo').classList.toggle('active', fullShowKo); renderFullText(); }",
        "js toggleFullJp -> add toggleFullKo",
    )

    # ---------- JS: cloze render ----------
    text = sub1(
        text,
        r"(document\.getElementById\('clozeJp'\)\.textContent = q\.jp \|\| '';)",
        r"\1\n  document.getElementById('clozeKo').textContent = q.ko || '';",
        "js renderCloze ko",
    )

    # ---------- JS: meaning concatenation (CHARACTERS) ----------
    text = sub1(
        text,
        r"(document\.getElementById\('charMeaning'\)\.textContent = c\.meaning \+ \(c\.meaningJp \? ' / ' \+ c\.meaningJp : ''\)) \+ ' · ' \+ c\.context;",
        r"\1 + (c.meaningKo ? ' / ' + c.meaningKo : '') + ' · ' + c.context;",
        "js charMeaning +meaningKo",
    )

    # ---------- JS: meaning concatenation (WORDS/VOCAB flashcards) ----------
    text = sub1(
        text,
        r"document\.getElementById\('flashMeaning'\)\.textContent = (\w+)\.meaning \+ \((\w+)\.meaningJp \? ' / ' \+ \2\.meaningJp : ''\);",
        r"document.getElementById('flashMeaning').textContent = \1.meaning + (\2.meaningJp ? ' / ' + \2.meaningJp : '') + (\2.meaningKo ? ' / ' + \2.meaningKo : '');",
        "js flashMeaning +meaningKo",
    )

    # ---------- JS: playClip dir mapping ----------
    text = sub1(
        text,
        r"const dir = lang === 'en-US' \? 'audio/" + slug + r"_en/' : \(lang === 'ja-JP' \? 'audio/" + slug + r"_ja/' : 'audio/" + slug + r"/'\);",
        r"const dir = lang === 'en-US' ? 'audio/" + slug + r"_en/' : (lang === 'ja-JP' ? 'audio/" + slug + r"_ja/' : (lang === 'ko-KR' ? 'audio/" + slug + r"_ko/' : 'audio/" + slug + r"/'));",
        "js playClip dir mapping",
    )

    # ---------- JS: pickVoice / speakText ----------
    text = sub1(
        text,
        r"let zhVoice = null, enVoice = null, jaVoice = null;",
        r"let zhVoice = null, enVoice = null, jaVoice = null, koVoice = null;",
        "js voice vars",
    )
    text = sub1(
        text,
        r"(jaVoice = voices\.find\(v=>/\^ja/i\.test\(v\.lang\|\|''\)\)\s*\|\| null;)",
        r"\1\n  koVoice = voices.find(v=>/^ko/i.test(v.lang||'')) || null;",
        "js pickVoice koVoice",
    )
    text = sub1(
        text,
        r"\(\(zhVoice && enVoice && jaVoice\) \|\| voicePolls > 8\)",
        r"((zhVoice && enVoice && jaVoice && koVoice) || voicePolls > 8)",
        "js voice poll condition",
    )
    text = sub1(
        text,
        r"let voice = /\^zh/i\.test\(lang\) \? zhVoice : /\^ja/i\.test\(lang\) \? jaVoice : /\^en/i\.test\(lang\) \? enVoice : null;",
        r"let voice = /^zh/i.test(lang) ? zhVoice : /^ja/i.test(lang) ? jaVoice : /^ko/i.test(lang) ? koVoice : /^en/i.test(lang) ? enVoice : null;",
        "js speakText voice select 1",
    )
    text = sub1(
        text,
        r"if\(!voice\)\{ pickVoice\(\); voice = /\^zh/i\.test\(lang\) \? zhVoice : /\^ja/i\.test\(lang\) \? jaVoice : /\^en/i\.test\(lang\) \? enVoice : null; \}",
        r"if(!voice){ pickVoice(); voice = /^zh/i.test(lang) ? zhVoice : /^ja/i.test(lang) ? jaVoice : /^ko/i.test(lang) ? koVoice : /^en/i.test(lang) ? enVoice : null; }",
        "js speakText voice select 2",
    )

    # ---------- Variant B fallbacks (yiheyuan / gugong / hanjia style) ----------
    text = sub1(
        text,
        r"let fullPy = true, fullEn = true, fullJp = true;",
        r"let fullPy = true, fullEn = true, fullJp = true, fullKo = true;",
        "js(B) full state vars",
        required=False,
    )
    text = sub1(
        text,
        r"document\.getElementById\('storyJp'\)\.textContent = showJp \? \(s\.jp \|\| ''\) : '';",
        r"document.getElementById('storyJp').textContent = showJp ? (s.jp || '') : '';\n"
        r"  document.getElementById('storyKo').textContent = showKo ? (s.ko || '') : '';",
        "js(B) renderStory textContent ko",
        required=False,
    )
    JP_TEMPLATE_LINE = (
        "(fullJp && s.jp ? '<div style=\"display:flex;align-items:center;justify-content:center;gap:6px;\">"
        "<div class=\"sentence-jp\">'+s.jp+'</div><button class=\"mini-speak-btn\" onclick=\"event.stopPropagation(); "
        "playClip(STORY['+i+'].id, STORY['+i+'].jp||\\'\\', null, \\'ja-JP\\');\" title=\"播放日文发音\">🔊</button></div>' : '') +"
    )
    KO_TEMPLATE_LINE = (
        "\n      (fullKo && s.ko ? '<div style=\"display:flex;align-items:center;justify-content:center;gap:6px;\">"
        "<div class=\"sentence-ko\">'+s.ko+'</div><button class=\"mini-speak-btn\" onclick=\"event.stopPropagation(); "
        "playClip(STORY['+i+'].id, STORY['+i+'].ko||\\'\\', null, \\'ko-KR\\');\" title=\"播放韩文发音\">🔊</button></div>' : '') +"
    )
    if JP_TEMPLATE_LINE in text and KO_TEMPLATE_LINE not in text:
        text = text.replace(JP_TEMPLATE_LINE, JP_TEMPLATE_LINE + KO_TEMPLATE_LINE, 1)
    elif KO_TEMPLATE_LINE not in text:
        print("  [WARN] pattern not found: js(B) renderFullText template ko row (plain)")
    text = sub1(
        text,
        r"function toggleFullJp\(\)\{ fullJp = !fullJp; document\.getElementById\('chipFullJp'\)\.classList\.toggle\('active', fullJp\); renderFullText\(\); \}",
        r"function toggleFullJp(){ fullJp = !fullJp; document.getElementById('chipFullJp').classList.toggle('active', fullJp); renderFullText(); }\n"
        r"function toggleFullKo(){ fullKo = !fullKo; document.getElementById('chipFullKo').classList.toggle('active', fullKo); renderFullText(); }",
        "js(B) toggleFullJp -> add toggleFullKo",
        required=False,
    )
    text = sub1(
        text,
        r"const AUDIO_DIR_JA = 'audio/" + slug + r"_ja/';",
        r"const AUDIO_DIR_JA = 'audio/" + slug + r"_ja/';\nconst AUDIO_DIR_KO = 'audio/" + slug + r"_ko/';",
        "js(B) AUDIO_DIR_KO const",
        required=False,
    )
    text = sub1(
        text,
        r"const dir = lang === 'en-US' \? AUDIO_DIR_EN : \(lang === 'ja-JP' \? AUDIO_DIR_JA : AUDIO_DIR\);",
        r"const dir = lang === 'en-US' ? AUDIO_DIR_EN : (lang === 'ja-JP' ? AUDIO_DIR_JA : (lang === 'ko-KR' ? AUDIO_DIR_KO : AUDIO_DIR));",
        "js(B) playClip dir mapping",
        required=False,
    )
    text = sub1(
        text,
        r"let jaVoice = null;",
        r"let jaVoice = null;\nlet koVoice = null;",
        "js(B) voice vars",
        required=False,
    )

    return text


def main():
    html_name = sys.argv[1]
    slug = sys.argv[2]
    path = ROOT / html_name
    text = path.read_text(encoding="utf-8")
    print(f"=== {html_name} (slug={slug}) ===")
    text = patch(text, slug)
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
