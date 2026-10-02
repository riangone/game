#!/usr/bin/env python3
"""apply_quiz_answer_fix.py
Architectural solution for Reading Comprehension (读解练习) quiz answers:
1. Static Data Balancing:
   - In the 16 lesson files, questions had their correct answers fixed to index 0 (a: 0).
   - Permute options in QUIZ arrays so correct answers are balanced evenly across positions 0, 1, 2, 3.
   - Preserve exact correct answer string via assertion: new_opts[new_a] === old_opts[old_a].
2. Runtime Dynamic Randomization (Per-Session Shuffle):
   - In renderQuiz() (early files) and loadQuizQuestion() (late files), options are dynamically shuffled
     using Fisher-Yates shuffle.
   - Per-session quizState.orderMap caches the permutation per question so previous/next navigation
     (quizPrev / quizNext) stays consistent during the round.
   - Re-entering the quiz (goQuiz / initQuiz) resets orderMap so each session has fresh permutations,
     preventing rote memorization of button locations.
   - Clicking a button passes the original option index to answerQuiz(i, el), ensuring full backward compatibility
     with SRS mistake recording and correctness evaluation without modifying answerQuiz internals.
"""

import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EARLY_FILES = [
    'hanjia-jianwen.html',
    'gugong.html',
    'yiheyuan.html',
    'nihongo.html',
    'nihongo2.html',
    'hangugeo.html',
    'hangugeo2.html',
]

LATE_FILES = [
    'luotuo-he-yang.html',
    'xiaoma-guohe.html',
    'houzi-lao-yueliang.html',
    'sima-guang.html',
    'shu-xingxing.html',
    'gushi-er-shou.html',
    'diqiu-qingjiegong.html',
    'daziran-yuyan.html',
    'tanyue.html',
]

TARGET_PATTERN_8 = [1, 2, 0, 3, 2, 1, 3, 0]
TARGET_PATTERN_7 = [1, 2, 0, 3, 2, 1, 0]

def update_static_quiz_data(content, file_name):
    m = re.search(r'(const QUIZ\s*=\s*\[)([\s\S]*?)(\];)', content)
    if not m:
        raise ValueError(f"Could not find const QUIZ in {file_name}")

    header, body, footer = m.group(1), m.group(2), m.group(3)
    raw_lines = [l for l in body.splitlines() if l.strip()]
    pat = TARGET_PATTERN_7 if len(raw_lines) == 7 else TARGET_PATTERN_8

    new_lines = []
    for idx, l in enumerate(raw_lines):
        m_item = re.match(r'\s*\{\s*q\s*:\s*\"(.*?)\"\s*,\s*opts\s*:\s*\[(.*?)\]\s*,\s*a\s*:\s*(\d+)\s*\},?', l)
        if not m_item:
            raise ValueError(f"Failed to match quiz item in {file_name}: {l}")

        q = m_item.group(1)
        opts_raw = m_item.group(2)
        orig_a = int(m_item.group(3))
        opts = [o.strip(' \t\n\r\"\'') for o in re.split(r'\",\s*\"|\',\'', opts_raw)]
        assert len(opts) == 4, f"Unexpected opts length in {file_name}: {opts}"

        target_a = pat[idx % len(pat)]
        correct_ans = opts[orig_a]
        distractors = [opt for i, opt in enumerate(opts) if i != orig_a]

        new_opts = [None] * len(opts)
        new_opts[target_a] = correct_ans
        d_idx = 0
        for i in range(len(opts)):
            if i != target_a:
                new_opts[i] = distractors[d_idx]
                d_idx += 1

        assert new_opts[target_a] == correct_ans, f"Verification failed for {file_name} Q{idx}"
        opts_json = json.dumps(new_opts, ensure_ascii=False)
        new_lines.append(f'  {{q:"{q}", opts:{opts_json}, a:{target_a}}},')

    new_body = "\n" + "\n".join(new_lines) + "\n"
    new_quiz_block = header + new_body + footer
    return content[:m.start(0)] + new_quiz_block + content[m.end(0):]

def update_early_file(file_path):
    content = file_path.read_text(encoding='utf-8')
    orig = content

    # 1. Update static QUIZ data
    content = update_static_quiz_data(content, file_path.name)

    # 2. Reset orderMap in goQuiz()
    # Find goQuiz and ensure quizState.orderMap = {};
    if 'quizState.orderMap = {};' not in content:
        content = re.sub(
            r'(function goQuiz\(\)\s*\{[\s\S]*?quizState\.correct\s*=\s*0;)',
            r'\1 quizState.orderMap = {};',
            content,
            count=1
        )

    # 3. Update renderQuiz() to dynamically shuffle options per-session
    old_render_opts = """  const optsEl = document.getElementById('quizOpts');
  optsEl.innerHTML = '';
  item.opts.forEach((opt, i)=>{
    const b = document.createElement('div');
    b.className = 'opt-btn';
    b.textContent = opt;
    b.onclick = ()=>answerQuiz(i, b);
    optsEl.appendChild(b);
  });"""

    new_render_opts = """  const optsEl = document.getElementById('quizOpts');
  optsEl.innerHTML = '';
  if(!quizState.orderMap) quizState.orderMap = {};
  if(!quizState.orderMap[quizState.idx]){
    const indices = item.opts.map((_, i) => i);
    for(let i = indices.length - 1; i > 0; i--){
      const j = Math.floor(Math.random() * (i + 1));
      [indices[i], indices[j]] = [indices[j], indices[i]];
    }
    quizState.orderMap[quizState.idx] = indices;
  }
  quizState.orderMap[quizState.idx].forEach(i => {
    const opt = item.opts[i];
    const b = document.createElement('div');
    b.className = 'opt-btn';
    b.textContent = opt;
    b.onclick = () => answerQuiz(i, b);
    optsEl.appendChild(b);
  });"""

    if old_render_opts in content:
        content = content.replace(old_render_opts, new_render_opts, 1)
    else:
        # Check if already updated or slight whitespace differences
        if 'if(!quizState.orderMap) quizState.orderMap = {};' not in content:
            print(f"Warning: old_render_opts not found verbatim in {file_path.name}")

    if content != orig:
        file_path.write_text(content, encoding='utf-8')
        print(f"Successfully updated early file: {file_path.name}")
    else:
        print(f"No changes made to {file_path.name}")

def update_late_file(file_path):
    content = file_path.read_text(encoding='utf-8')
    orig = content

    # 1. Update static QUIZ data
    content = update_static_quiz_data(content, file_path.name)

    # 2. Reset orderMap in initQuiz()
    if 'quizState.orderMap = {};' not in content:
        content = re.sub(
            r'(function initQuiz\(\)\s*\{[\s\S]*?quizState\.correct\s*=\s*0;)',
            r'\1\n  quizState.orderMap = {};',
            content,
            count=1
        )

    # 3. Update loadQuizQuestion() to dynamically shuffle options per-session
    old_load_opts = """  const opts = document.getElementById('quizOpts');
  opts.innerHTML = '';
  q.opts.forEach((opt, i)=>{
    const b = document.createElement('button');
    b.className = 'opt-btn';
    b.textContent = opt;
    b.onclick = () => answerQuiz(i, b);
    opts.appendChild(b);
  });"""

    new_load_opts = """  const opts = document.getElementById('quizOpts');
  opts.innerHTML = '';
  if(!quizState.orderMap) quizState.orderMap = {};
  if(!quizState.orderMap[quizState.idx]){
    const indices = q.opts.map((_, i) => i);
    for(let i = indices.length - 1; i > 0; i--){
      const j = Math.floor(Math.random() * (i + 1));
      [indices[i], indices[j]] = [indices[j], indices[i]];
    }
    quizState.orderMap[quizState.idx] = indices;
  }
  quizState.orderMap[quizState.idx].forEach(i => {
    const opt = q.opts[i];
    const b = document.createElement('button');
    b.className = 'opt-btn';
    b.textContent = opt;
    b.onclick = () => answerQuiz(i, b);
    opts.appendChild(b);
  });"""

    if old_load_opts in content:
        content = content.replace(old_load_opts, new_load_opts, 1)
    else:
        if 'if(!quizState.orderMap) quizState.orderMap = {};' not in content:
            print(f"Warning: old_load_opts not found verbatim in {file_path.name}")

    if content != orig:
        file_path.write_text(content, encoding='utf-8')
        print(f"Successfully updated late file: {file_path.name}")
    else:
        print(f"No changes made to {file_path.name}")

def main():
    for f in EARLY_FILES:
        p = ROOT / f
        if p.exists():
            update_early_file(p)
        else:
            print(f"File not found: {f}")

    for f in LATE_FILES:
        p = ROOT / f
        if p.exists():
            update_late_file(p)
        else:
            print(f"File not found: {f}")

if __name__ == '__main__':
    main()
