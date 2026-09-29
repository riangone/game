#!/usr/bin/env python3
"""Apply Quiz improvements across all 15 lesson apps:
1. Wrong choice feedback:
   - Plays gentle dual-tone buzzer sound ("不，不" sound, 220Hz -> 160Hz via playWrongTone)
   - Visual symbol and feedback: red background/border, shake animation, appends " ❌", disabled (pointer-events: none, cursor: not-allowed)
   - Toast notification encouraging the user
   - Allows re-selection: DOES NOT advance, DOES NOT reveal the correct answer early, keeps remaining options open
   - Records mistake in SRS on first wrong attempt
2. Correct choice feedback:
   - Green highlight, appends " ✔️"
   - Plays cheerful success tone via playSuccessTone
   - Disables all options
   - Gentle pause (900ms) before advancing to next question or result screen
3. Previous / Next navigation:
   - Adds [⬅️ 上一题] [下一题 ➡️] navigation controls to repeat / review questions freely
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EARLY_FILES = [
    'hanjia-jianwen.html',
    'gugong.html',
    'yiheyuan.html',
    'nihongo.html',
    'nihongo2.html',
    'hangugeo.html',
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

QUIZ_NAV_HTML = """      <div style="display:flex;gap:10px;justify-content:center;margin:12px 0;width:100%;max-width:560px;">
        <button class="btn ghost small" onclick="quizPrev()">⬅️ 上一题</button>
        <button class="btn ghost small" onclick="quizNext()">下一题 ➡️</button>
      </div>
"""

CSS_ENHANCEMENT = """
  .opt-btn.correct{background:var(--green-soft,#d1fae5)!important;border-color:var(--green,#10b981)!important;color:var(--green-dark,#065f46)!important;}
  .opt-btn.wrong{background:var(--red-soft,#fee2e2)!important;border-color:var(--danger-red,#ef4444)!important;color:var(--danger-red,#dc2626)!important;animation:shake .35s ease-in-out;opacity:0.75;cursor:not-allowed;}
"""

TONE_FUNCTIONS = """
function playSuccessTone(){
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(523.25, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(659.25, ctx.currentTime + 0.1);
    osc.frequency.exponentialRampToValueAtTime(783.99, ctx.currentTime + 0.2);
    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.35);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.35);
  } catch(e){}
}

function playWrongTone(){
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const now = ctx.currentTime;
    [0, 0.12].forEach((delay) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(220, now + delay);
      osc.frequency.exponentialRampToValueAtTime(160, now + delay + 0.09);
      gain.gain.setValueAtTime(0.18, now + delay);
      gain.gain.exponentialRampToValueAtTime(0.01, now + delay + 0.09);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now + delay);
      osc.stop(now + delay + 0.09);
    });
  } catch(e){}
}
"""

def find_function_bounds(content, func_prefix):
    idx = content.find(func_prefix)
    if idx == -1:
        return None
    brace_open = content.find('{', idx)
    if brace_open == -1:
        return None
    depth = 0
    i = brace_open
    while i < len(content):
        ch = content[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return (idx, i + 1)
        elif ch == '/' and i + 1 < len(content) and content[i+1] == '/':
            nl = content.find('\n', i)
            if nl == -1: break
            i = nl
        i += 1
    return None

def update_early_file(file_path):
    content = file_path.read_text(encoding='utf-8')
    orig = content

    # 1. Ensure CSS
    if '.opt-btn.wrong{background:var(--red-soft,#fee2e2)!important;' not in content:
        style_end = content.find('</style>')
        if style_end != -1:
            content = content[:style_end] + CSS_ENHANCEMENT + content[style_end:]

    # 2. Ensure tones
    if 'playWrongTone' not in content:
        script_idx = content.find('<script>')
        if script_idx != -1:
            pos = script_idx + len('<script>\n')
            content = content[:pos] + TONE_FUNCTIONS + content[pos:]

    # 3. Add Quiz Prev/Next navigation HTML if not present
    if 'quizPrev()' not in content:
        sec_pattern = r'(<section[^>]*id=[\"\']screen-quiz[\"\'][\s\S]*?)(<button class=[\"\']btn ghost[^>]*onclick=[\"\']goHome\(\)[\"\']>返回菜单</button>)'
        m = re.search(sec_pattern, content)
        if m:
            content = content[:m.start(2)] + QUIZ_NAV_HTML + content[m.start(2):]

    # 4. Update renderQuiz to reset quizState.hasWrong
    b_render = find_function_bounds(content, 'function renderQuiz')
    if b_render:
        render_src = content[b_render[0]:b_render[1]]
        if 'quizState.hasWrong = false;' not in render_src:
            new_render_src = render_src.replace(
                'quizState.answered = false;',
                'quizState.answered = false;\n  quizState.hasWrong = false;'
            )
            content = content[:b_render[0]] + new_render_src + content[b_render[1]:]

    # 5. Update answerQuiz and add quizPrev / quizNext
    b_ans = find_function_bounds(content, 'function answerQuiz')
    if b_ans:
        ans_src = content[b_ans[0]:b_ans[1]]
        # Check score note in original render/result
        is_kr = 'hangugeo' in file_path.name
        
        new_ans_src = """function answerQuiz(i, el){
  if(quizState.answered) return;
  const item = QUIZ[quizState.idx];
  if(i === item.a){
    quizState.answered = true;
    el.classList.remove('wrong');
    el.classList.add('correct');
    if(!el.textContent.includes('✔️')){
      el.textContent += ' ✔️';
    }
    document.querySelectorAll('#quizOpts .opt-btn').forEach(b => {
      b.style.pointerEvents = 'none';
    });
    playSuccessTone();
    if(!quizState.hasWrong){
      quizState.correct++;
      toast('🌟 答对啦！太棒了！');
    } else {
      toast('🎉 太棒了，找到正确答案了！');
    }
    setTimeout(()=>{
      quizState.idx++;
      renderQuiz();
    }, 900);
  } else {
    if(!quizState.hasWrong){
      quizState.hasWrong = true;
      recordMistake({
        id: 'quiz_' + quizState.idx,
        type: 'quiz',
        zh: item.q,
        py: '',
        meaning: '正确答案: ' + item.opts[item.a],
        extra: '误选: ' + item.opts[i],
        quizItem: item
      });
    }
    playWrongTone();
    el.classList.add('wrong');
    if(!el.textContent.includes('❌')){
      el.textContent += ' ❌';
    }
    el.style.pointerEvents = 'none';
    toast('❌ 选错了哦，再想一想，换个答案试试！');
  }
}

function quizPrev(){
  if(quizState.idx > 0) quizState.idx--;
  else quizState.idx = QUIZ.length - 1;
  renderQuiz();
}

function quizNext(){
  if(quizState.idx < QUIZ.length - 1) quizState.idx++;
  else quizState.idx = 0;
  renderQuiz();
}"""
        content = content[:b_ans[0]] + new_ans_src + content[b_ans[1]:]

    if content != orig:
        file_path.write_text(content, encoding='utf-8')
        print(f"Updated early file: {file_path.name}")
    else:
        print(f"No change for early file: {file_path.name}")

def update_late_file(file_path):
    content = file_path.read_text(encoding='utf-8')
    orig = content

    # 1. Ensure CSS
    if '.opt-btn.wrong{background:var(--red-soft,#fee2e2)!important;' not in content:
        style_end = content.find('</style>')
        if style_end != -1:
            content = content[:style_end] + CSS_ENHANCEMENT + content[style_end:]

    # 2. Ensure tones
    if 'playWrongTone' not in content:
        script_idx = content.find('<script>')
        if script_idx != -1:
            pos = script_idx + len('<script>\n')
            content = content[:pos] + TONE_FUNCTIONS + content[pos:]

    # 3. Add Quiz Prev/Next navigation HTML if not present
    if 'quizPrev()' not in content:
        sec_pattern = r'(<section[^>]*id=[\"\']screen-quiz[\"\'][\s\S]*?)(<button class=[\"\']btn ghost[^>]*onclick=[\"\']goHome\(\)[\"\']>返回菜单</button>)'
        m = re.search(sec_pattern, content)
        if m:
            content = content[:m.start(2)] + QUIZ_NAV_HTML + content[m.start(2):]

    # 4. Update loadQuizQuestion to reset quizState.hasWrong
    b_load = find_function_bounds(content, 'function loadQuizQuestion')
    if b_load:
        load_src = content[b_load[0]:b_load[1]]
        if 'quizState.hasWrong = false;' not in load_src:
            new_load_src = load_src.replace(
                'quizState.answered = false;',
                'quizState.answered = false;\n  quizState.hasWrong = false;'
            )
            content = content[:b_load[0]] + new_load_src + content[b_load[1]:]

    # 5. Extract original showResult line from answerQuiz
    b_ans = find_function_bounds(content, 'function answerQuiz')
    if b_ans:
        ans_src = content[b_ans[0]:b_ans[1]]
        m_sr = re.search(r'showResult\([^\n]+\);', ans_src)
        if m_sr:
            sr_line = m_sr.group(0)
        else:
            sr_line = "showResult('❓ 问答完成！', stars, pct, ['问答小博士', pct === 100 ? '满分通关' : '博闻强识']);"

        new_ans_src = f"""function answerQuiz(choice, btn){{
  if(quizState.answered) return;
  const q = QUIZ[quizState.idx];
  const isRight = (choice === q.a);
  if(isRight){{
    quizState.answered = true;
    btn.classList.remove('wrong');
    btn.classList.add('correct');
    if(!btn.textContent.includes('✔️')){{
      btn.textContent += ' ✔️';
    }}
    document.querySelectorAll('#quizOpts .opt-btn').forEach(b => {{
      b.style.pointerEvents = 'none';
    }});
    playSuccessTone();
    if(!quizState.hasWrong){{
      quizState.correct++;
      toast('🌟 答对啦！太棒了！');
    }} else {{
      toast('🎉 太棒了，找到正确答案了！');
    }}
    setTimeout(()=>{{
      quizState.idx++;
      if(quizState.idx < QUIZ.length){{
        loadQuizQuestion();
      }} else {{
        const pct = Math.round((quizState.correct / QUIZ.length) * 100);
        const stars = pct >= 85 ? 3 : (pct >= 60 ? 2 : 1);
        progress.quiz = Math.max(progress.quiz || 0, stars);
        saveProgress();
        {sr_line}
      }}
    }}, 900);
  }} else {{
    if(!quizState.hasWrong){{
      quizState.hasWrong = true;
      recordMistake({{
        id: 'quiz_' + quizState.idx,
        type: 'quiz',
        zh: q.q,
        py: '',
        meaning: '正确答案: ' + q.opts[q.a],
        audioId: null
      }});
    }}
    playWrongTone();
    btn.classList.add('wrong');
    if(!btn.textContent.includes('❌')){{
      btn.textContent += ' ❌';
    }}
    btn.style.pointerEvents = 'none';
    toast('❌ 选错了哦，再想一想，换个答案试试！');
  }}
}}

function quizPrev(){{
  if(quizState.idx > 0) quizState.idx--;
  else quizState.idx = QUIZ.length - 1;
  loadQuizQuestion();
}}

function quizNext(){{
  if(quizState.idx < QUIZ.length - 1) quizState.idx++;
  else quizState.idx = 0;
  loadQuizQuestion();
}}"""
        content = content[:b_ans[0]] + new_ans_src + content[b_ans[1]:]

    if content != orig:
        file_path.write_text(content, encoding='utf-8')
        print(f"Updated late file: {file_path.name}")
    else:
        print(f"No change for late file: {file_path.name}")

def main():
    for f in EARLY_FILES:
        p = ROOT / f
        if p.exists():
            update_early_file(p)
    for f in LATE_FILES:
        p = ROOT / f
        if p.exists():
            update_late_file(p)

if __name__ == '__main__':
    main()
