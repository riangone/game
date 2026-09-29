#!/usr/bin/env python3
"""Upgrade all 14 lesson apps with:
1. "句子排序" -> "连词成句" across menu, title, results.
2. "对一对" -> "答案" with correct answer highlighted, waiting for audio end + 700ms before advance.
3. Wrong order in scramble: red shake + dual-tone gentle buzzer ("不，不" sound) + toast.
4. "选词填空" description -> "选择恰当的词语".
5. Dedicated cloze audio files matching text 100%, playing on correct and on "朗读句子".
6. Wrong choice in cloze: red shake + "不，不" buzzer, keeps question open and allows re-selection.
7. Previous / Next navigation ("上一句/下一句", "上一题/下一题") for both scramble and cloze.
"""
import os
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

COMMON_CSS = """
  .scramble-target.correct{border-color:#10b981!important;background:#f0fdf4!important;}
  .scramble-target.wrong{border-color:#ef4444!important;background:#fef2f2!important;animation:shake .35s ease-in-out;}
  .word-chip.in-target.correct{background:#10b981!important;color:#fff!important;border-color:#059669!important;}
  .cloze-opt-btn.wrong{background:var(--red-soft,#fee2e2)!important;border-color:var(--danger-red,#ef4444)!important;color:var(--danger-red,#dc2626)!important;opacity:0.65;cursor:not-allowed;}
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
        i += 1
    return None

def update_cloze_audio_ids(content):
    """Update audioId in CLOZE_QUESTIONS to cloze_1 .. cloze_12"""
    m = re.search(r'(const CLOZE_QUESTIONS = \[)(.*?)(\];)', content, re.DOTALL)
    if not m:
        return content
    header, body, footer = m.group(1), m.group(2), m.group(3)
    
    blocks = re.split(r'(\{[^{}]*id:[^{}]*\})', body)
    block_idx = 0
    new_parts = []
    for part in blocks:
        if part.startswith('{') and 'id:' in part:
            block_idx += 1
            new_id = f"cloze_{block_idx}"
            if re.search(r'audioId:\s*[\"\'][^\"\']*[\"\']', part):
                part = re.sub(r'audioId:\s*[\"\'][^\"\']*[\"\']', f'audioId: "{new_id}"', part)
            else:
                part = re.sub(r'\s*\}$', f',\n    audioId: "{new_id}"\n  }}', part)
        new_parts.append(part)
        
    return content[:m.start()] + header + "".join(new_parts) + footer + content[m.end():]

def patch_file(fn, is_early):
    # Read fresh backup if exists to ensure idempotency
    bak_path = ROOT / f"{fn}.bak_20260929"
    orig_path = ROOT / fn
    if bak_path.exists():
        with open(bak_path, 'r', encoding='utf-8') as bf:
            c = bf.read()
    else:
        with open(orig_path, 'r', encoding='utf-8') as f:
            c = f.read()
        with open(bak_path, 'w', encoding='utf-8') as bf:
            bf.write(c)

    # 1. 句子排序 -> 连词成句
    c = c.replace('<span class="name">句子排序</span>', '<span class="name">连词成句</span>')
    c = c.replace('<div class="name">句子排序</div>', '<div class="name">连词成句</div>')
    c = c.replace('<h2 class="title">🔤 句子排序</h2>', '<h2 class="title">🔤 连词成句</h2>')
    c = c.replace("showResult('🔤 句子排序全通关！'", "showResult('🔤 连词成句全通关！'")
    c = c.replace("scramble:'🔤 句子排序'", "scramble:'🔤 连词成句'")
    c = c.replace("scramble: '🔤 句子排序'", "scramble: '🔤 连词成句'")

    # 2. 选词填空描述 -> 选择恰当的词语
    c = re.sub(r'<span class="desc">语境填空[^\n<]*</span>', '<span class="desc">选择恰当的词语</span>', c)
    c = re.sub(r'<div class="desc">语境填空[^\n<]*</div>', '<div class="desc">选择恰当的词语</div>', c)

    # 3. Scramble buttons: 撤销 / 对一对 -> 上一句 / 撤销 / 答案 / 下一句
    new_scramble_nav = """<div class="scramble-nav-bar" style="display:flex;align-items:center;justify-content:center;gap:10px;margin:12px 0 6px;flex-wrap:wrap;">
        <button class="btn ghost small" onclick="scramblePrev()">⬅️ 上一句</button>
        <button class="btn ghost small" onclick="scrambleUndo()">撤销</button>
        <button class="btn gold small" id="scrambleCheckBtn" onclick="scrambleCheck()">答案</button>
        <button class="btn ghost small" onclick="scrambleNext()">下一句 ➡️</button>
      </div>"""
    c = re.sub(r'<div style="display:flex;gap:10px;">\s*<button class="btn ghost small" onclick="scrambleUndo\(\)">撤销</button>\s*<button class="btn [a-z]+ small" onclick="scrambleCheck\(\)">对一对</button>\s*</div>',
               new_scramble_nav, c)

    # 4. Cloze nav: 上一题 / 下一题 below .cloze-card
    if 'cloze-nav-bar' not in c:
        c = re.sub(r'(</div>\s*<div class="cloze-opts"[^>]*></div>\s*</div>\s*)(<button class="btn ghost")',
                   r"""\1<div class="cloze-nav-bar" style="display:flex;align-items:center;justify-content:center;gap:12px;margin:12px 0 6px;">
        <button class="btn ghost small" onclick="clozePrev()">⬅️ 上一题</button>
        <button class="btn ghost small" onclick="clozeNext()">下一题 ➡️</button>
      </div>\n      \2""", c)
        if 'cloze-nav-bar' not in c:
            # Fallback insertion
            c = re.sub(r'(<button class="btn ghost"[^>]*onclick="[^"]*goHome\(\)[^"]*">返回菜单</button>\s*</section>)',
                       r"""<div class="cloze-nav-bar" style="display:flex;align-items:center;justify-content:center;gap:12px;margin:12px 0 6px;">
        <button class="btn ghost small" onclick="clozePrev()">⬅️ 上一题</button>
        <button class="btn ghost small" onclick="clozeNext()">下一题 ➡️</button>
      </div>\n      \1""", c)

    # 5. CSS
    if '.scramble-target.correct' not in c:
        c = c.replace('</style>', COMMON_CSS + '\n</style>')

    # 6. Audio IDs in CLOZE_QUESTIONS
    c = update_cloze_audio_ids(c)

    # 7. Tone functions
    # Replace existing playSuccessTone if present, else prepend before scramble
    pst_bounds = find_function_bounds(c, 'function playSuccessTone(')
    if pst_bounds:
        c = c[:pst_bounds[0]] + TONE_FUNCTIONS.strip() + c[pst_bounds[1]:]
    else:
        # Insert before /* ---------------- SCRAMBLE or end of first script
        m_sc = re.search(r'/\* -+ SCRAMBLE', c)
        if m_sc:
            c = c[:m_sc.start()] + TONE_FUNCTIONS.strip() + '\n\n' + c[m_sc.start():]
        else:
            c = c.replace('</script>', TONE_FUNCTIONS.strip() + '\n</script>', 1)

    # 8. JS Functions replacement using exact bracket bounds
    if is_early:
        # Early Scramble
        early_scramble_replacement = """
let scrambleChecking = false;
function scramblePrev(){
  stopClip();
  if(!SCRAMBLE_SENTENCES || SCRAMBLE_SENTENCES.length === 0) return;
  if(scrambleState.idx > 0) scrambleState.idx--;
  else scrambleState.idx = SCRAMBLE_SENTENCES.length - 1;
  setupScrambleRound();
}
function scrambleNext(){
  stopClip();
  if(!SCRAMBLE_SENTENCES || SCRAMBLE_SENTENCES.length === 0) return;
  if(scrambleState.idx < SCRAMBLE_SENTENCES.length - 1) scrambleState.idx++;
  else scrambleState.idx = 0;
  setupScrambleRound();
}

function scrambleCheck(){
  if(scrambleChecking) return;
  const round = SCRAMBLE_SENTENCES[scrambleState.idx];
  const built = scrambleState.placed.map(p => (p.text !== undefined ? p.text : p.token)).join('');
  const target = document.getElementById('scrambleTarget');
  if(built === round.zh){
    scrambleChecking = true;
    if(target){
      target.classList.remove('wrong');
      target.classList.add('correct');
      target.querySelectorAll('.word-chip').forEach(c => c.classList.add('correct'));
    }
    playSuccessTone();
    toast('🎉 答对了！太棒了！');
    playClip(round.id, round.zh, () => {
      setTimeout(() => {
        scrambleChecking = false;
        if(target) target.classList.remove('correct');
        scrambleState.idx++;
        setupScrambleRound();
      }, 700);
    });
  } else {
    if(target){
      target.classList.remove('correct');
      target.classList.add('wrong');
      setTimeout(() => target.classList.remove('wrong'), 600);
    }
    playWrongTone();
    toast('排序还不太对哦，点击词块可以撤回调整！');
    recordMistake({
      id: round.id,
      type: 'sentence',
      zh: round.zh,
      py: round.py || '',
      meaning: '连词成句',
      audioId: round.id
    });
  }
}
""".strip()
        sc_b = find_function_bounds(c, 'function scrambleCheck(')
        if sc_b:
            c = c[:sc_b[0]] + early_scramble_replacement + c[sc_b[1]:]

        # Early Cloze speak & answer
        early_speak_replacement = """
function speakClozeSentence(){
  const q = clozeState.questions[clozeState.idx];
  if(!q) return;
  const text = q.before + q.answer + q.after;
  playClip(q.audioId || ('cloze_' + (clozeState.idx + 1)), text);
}
""".strip()
        sp_b = find_function_bounds(c, 'function speakClozeSentence(')
        if sp_b:
            c = c[:sp_b[0]] + early_speak_replacement + c[sp_b[1]:]

        early_answer_replacement = """
function clozePrev(){
  stopClip();
  if(!clozeState.questions || clozeState.questions.length === 0) return;
  if(clozeState.idx > 0) clozeState.idx--;
  else clozeState.idx = clozeState.questions.length - 1;
  renderClozeQuestion();
}
function clozeNext(){
  stopClip();
  if(!clozeState.questions || clozeState.questions.length === 0) return;
  if(clozeState.idx < clozeState.questions.length - 1) clozeState.idx++;
  else clozeState.idx = 0;
  renderClozeQuestion();
}

function answerCloze(selected, btn){
  if(clozeState.answered) return;
  const q = clozeState.questions[clozeState.idx];
  const isCorrect = selected === q.answer;
  const slot = document.getElementById('clozeSlot');

  if(isCorrect){
    clozeState.answered = true;
    btn.classList.remove('wrong');
    btn.classList.add('correct');
    slot.textContent = q.answer;
    slot.className = 'cloze-slot filled';
    clozeState.correct++;
    clozeState.streak++;
    if(clozeState.streak > clozeState.maxStreak){
      clozeState.maxStreak = clozeState.streak;
    }
    document.getElementById('clozeStreak').textContent = '🔥 连对 ' + clozeState.streak;
    toast('🎉 填入正确！语境完全吻合！');
    playSuccessTone();

    document.querySelectorAll('#clozeOpts .cloze-opt-btn').forEach(b => {
      b.style.pointerEvents = 'none';
    });

    const fullText = q.before + q.answer + q.after;
    playClip(q.audioId || ('cloze_' + (clozeState.idx + 1)), fullText, () => {
      setTimeout(() => {
        clozeState.idx++;
        renderClozeQuestion();
      }, 800);
    });
  } else {
    clozeState.streak = 0;
    document.getElementById('clozeStreak').textContent = '🔥 连对 ' + clozeState.streak;
    playWrongTone();

    btn.classList.add('wrong');
    btn.style.pointerEvents = 'none';

    slot.textContent = selected;
    slot.className = 'cloze-slot wrong';
    toast('选错了哦，再想一想，换个词试试！');

    setTimeout(() => {
      if(!clozeState.answered){
        slot.textContent = '____';
        slot.className = 'cloze-slot';
      }
    }, 800);

    recordMistake({
      id: 'cloze_' + q.id,
      type: 'cloze',
      zh: q.answer,
      py: q.answerPy || '',
      meaning: q.before + '【' + q.answer + '】' + q.after,
      audioId: q.audioId || null,
      clozeItem: q
    });
  }
}
""".strip()
        ac_b = find_function_bounds(c, 'function answerCloze(')
        if ac_b:
            c = c[:ac_b[0]] + early_answer_replacement + c[ac_b[1]:]

    else:
        # Late Scramble
        late_scramble_replacement = """
let scrambleChecking = false;
function scramblePrev(){
  stopClip();
  if(!SCRAMBLE_SENTENCES || SCRAMBLE_SENTENCES.length === 0) return;
  if(scrambleState.idx > 0) scrambleState.idx--;
  else scrambleState.idx = SCRAMBLE_SENTENCES.length - 1;
  loadScrambleSentence();
}
function scrambleNext(){
  stopClip();
  if(!SCRAMBLE_SENTENCES || SCRAMBLE_SENTENCES.length === 0) return;
  if(scrambleState.idx < SCRAMBLE_SENTENCES.length - 1) scrambleState.idx++;
  else scrambleState.idx = 0;
  loadScrambleSentence();
}

function scrambleCheck(){
  if(scrambleChecking) return;
  const s = SCRAMBLE_SENTENCES[scrambleState.idx];
  const built = scrambleState.placed.map(p => (p.token !== undefined ? p.token : p.text)).join('');
  const target = document.getElementById('scrambleTarget');
  if(built === s.zh){
    scrambleChecking = true;
    if(target){
      target.classList.remove('wrong');
      target.classList.add('correct');
      target.querySelectorAll('.word-chip').forEach(c => c.classList.add('correct'));
    }
    playSuccessTone();
    toast('🎉 答对了！太棒了！');
    playClip(s.id, s.zh, () => {
      setTimeout(() => {
        scrambleChecking = false;
        if(target) target.classList.remove('correct');
        scrambleState.idx++;
        if(scrambleState.idx < SCRAMBLE_SENTENCES.length){
          loadScrambleSentence();
        } else {
          progress.scramble = 3;
          saveProgress();
          showResult('🔤 连词成句全通关！', 3, 100, ['语感大师', '句意通达']);
        }
      }, 700);
    });
  } else {
    if(target){
      target.classList.remove('correct');
      target.classList.add('wrong');
      setTimeout(() => target.classList.remove('wrong'), 600);
    }
    playWrongTone();
    toast('排序还不太对哦，点击词块可以撤回调整！');
    recordMistake({
      id: 'scramble_' + s.id,
      type: 'sentence',
      zh: s.zh,
      py: '',
      meaning: '连词成句',
      audioId: s.id
    });
  }
}
""".strip()
        sc_b = find_function_bounds(c, 'function scrambleCheck(')
        if sc_b:
            c = c[:sc_b[0]] + late_scramble_replacement + c[sc_b[1]:]

        # Late Cloze
        late_speak_replacement = """
function speakClozeSentence(){
  const q = clozeList[clozeIdx];
  if(!q) return;
  const fullSentence = q.before + q.answer + q.after;
  playClip(q.audioId || ('cloze_' + (clozeIdx + 1)), fullSentence);
}
""".strip()
        sp_b = find_function_bounds(c, 'function speakClozeSentence(')
        if sp_b:
            c = c[:sp_b[0]] + late_speak_replacement + c[sp_b[1]:]

        late_answer_replacement = """
let clozePassed = false;
function clozePrev(){
  stopClip();
  if(!clozeList || clozeList.length === 0) return;
  if(clozeIdx > 0) clozeIdx--;
  else clozeIdx = clozeList.length - 1;
  loadClozeQuestion();
}
function clozeNext(){
  stopClip();
  if(!clozeList || clozeList.length === 0) return;
  if(clozeIdx < clozeList.length - 1) clozeIdx++;
  else clozeIdx = 0;
  loadClozeQuestion();
}

function answerCloze(choice, btn, q){
  if(clozePassed) return;
  const slot = document.getElementById('clozeSlot');
  const isRight = (choice === q.answer);

  if(isRight){
    clozePassed = true;
    slot.textContent = q.answer;
    slot.className = 'cloze-slot filled';
    btn.classList.remove('wrong');
    btn.classList.add('correct');
    clozeStreak++;
    updateClozeStreakUI();
    toast('🎉 太棒了！选词完全正确！');
    playSuccessTone();

    document.querySelectorAll('.cloze-opt-btn').forEach(b => {
      b.style.pointerEvents = 'none';
    });

    const fullSentence = q.before + q.answer + q.after;
    playClip(q.audioId || ('cloze_' + (clozeIdx + 1)), fullSentence, () => {
      setTimeout(() => {
        clozeIdx++;
        loadClozeQuestion();
      }, 800);
    });
  } else {
    clozeStreak = 0;
    updateClozeStreakUI();
    playWrongTone();

    slot.textContent = choice;
    slot.className = 'cloze-slot wrong';
    btn.classList.add('wrong');
    btn.style.pointerEvents = 'none';
    toast('选错了哦，再想一想，换个词试试！');

    setTimeout(() => {
      if(!clozePassed){
        slot.textContent = '____';
        slot.className = 'cloze-slot';
      }
    }, 800);

    recordMistake({
      id: q.id,
      type: 'word',
      zh: q.answer,
      py: q.answerPy || '',
      meaning: q.hint,
      audioId: q.audioId,
      extra: q.before + `【${q.answer}】` + q.after
    });
  }
}
""".strip()
        ac_b = find_function_bounds(c, 'function answerCloze(')
        if ac_b:
            c = c[:ac_b[0]] + late_answer_replacement + c[ac_b[1]:]

    # Reset in setup / load functions
    if is_early:
        c = re.sub(r'(function setupScrambleRound\(\)\s*\{)', r'\1\n  scrambleChecking = false;\n  const _tg = document.getElementById("scrambleTarget"); if(_tg) _tg.classList.remove("correct","wrong");', c)
    else:
        c = re.sub(r'(function loadScrambleSentence\(\)\s*\{)', r'\1\n  scrambleChecking = false;\n  const _tg = document.getElementById("scrambleTarget"); if(_tg) _tg.classList.remove("correct","wrong");', c)
        c = re.sub(r'(function loadClozeQuestion\(\)\s*\{)', r'\1\n  clozePassed = false;', c)

    # Validate JavaScript syntax with node
    scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', c, re.DOTALL)
    combined_js = "\n".join(scripts)
    
    tmp_js = Path('/tmp/check_syntax.js')
    tmp_js.write_text(combined_js, encoding='utf-8')
    proc = subprocess.run(['node', '--check', str(tmp_js)], capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"[{fn}] SYNTAX ERROR:\n{proc.stderr}")
        return False

    with open(orig_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"[{fn}] SUCCESS: Patched and syntax verified.")
    return True

def main():
    all_success = True
    print("--- Patching Early Files ---")
    for f in EARLY_FILES:
        res = patch_file(f, is_early=True)
        if not res: all_success = False

    print("\n--- Patching Late Files ---")
    for f in LATE_FILES:
        res = patch_file(f, is_early=False)
        if not res: all_success = False

    print("\nOverall Status:", "ALL PASSED" if all_success else "FAILED")

if __name__ == '__main__':
    main()
