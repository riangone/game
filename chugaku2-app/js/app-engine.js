// app-engine.js - 中2 5教科 総合学習・復習・演習エンジン
class AppEngine {
  constructor() {
    this.units = [];
    this.currentSubject = 'all'; // all, math, english, science, society, japanese
    this.currentUnit = null;
    this.currentMode = null;
    this.currentScreen = 'screen-home';

    // 模式运行态
    this.modeState = {
      index: 0,
      total: 0,
      correctCount: 0,
      items: [],
      selectedMatchLeft: null,
      selectedMatchRight: null,
      matchedPairsCount: 0,
      scrambleUserOrder: [],
      scrambleTokensRemain: [],
      // 15分钟测试计时器
      testTimerId: null,
      testTimeRemain: 900 // 15分 = 900秒
    };

    this.init();
  }

  init() {
    this.loadData();
    this.bindGlobalEvents();
    this.updateHeaderStats();
    this.renderHome();
  }

  // 選択肢をシャッフル（正解位置の偏りを防ぐ）。answerIndex を付け替えたコピーを返す
  shuffleChoices(q) {
    const order = q.options.map((_, i) => i).sort(() => Math.random() - 0.5);
    const out = { ...q, options: order.map(i => q.options[i]) };
    if (typeof q.answerIndex === 'number') out.answerIndex = order.indexOf(q.answerIndex);
    return out;
  }

  loadData() {
    if (window.CHUGAKU_DATA && window.CHUGAKU_DATA.grade2 && window.CHUGAKU_DATA.grade2.units) {
      this.units = window.CHUGAKU_DATA.grade2.units;
    }
  }

  // KaTeX 数学・化学式レンダリング補助
  renderMath(text) {
    if (!text) return '';
    if (typeof katex === 'undefined') return text;

    // $$...$$ ブロック数式
    let result = text.replace(/\$\$([^$]+)\$\$/g, (match, expr) => {
      try {
        return katex.renderToString(expr.trim(), { displayMode: true, throwOnError: false });
      } catch (e) {
        return expr;
      }
    });

    // $...$ インライン数式
    result = result.replace(/\$([^$]+)\$/g, (match, expr) => {
      try {
        return katex.renderToString(expr.trim(), { displayMode: false, throwOnError: false });
      } catch (e) {
        return expr;
      }
    });

    return result;
  }

  bindGlobalEvents() {
    // 顶部返回按钮
    const btnNavBack = document.getElementById('btnNavBack');
    if (btnNavBack) {
      btnNavBack.addEventListener('click', () => this.handleBackNavigation());
    }

    // 科目选择 Tab
    document.querySelectorAll('.subject-tab').forEach(tab => {
      tab.addEventListener('click', (e) => {
        document.querySelectorAll('.subject-tab').forEach(t => t.classList.remove('active'));
        const target = e.currentTarget;
        target.classList.add('active');
        this.currentSubject = target.getAttribute('data-subject');
        this.renderUnitList();
      });
    });

    // 15分钟定期考冲刺小测入口
    const btnSprintTest = document.getElementById('btnStartSprintTest');
    if (btnSprintTest) {
      btnSprintTest.addEventListener('click', () => this.startSprintTest());
    }

    // 弱点克服 / 错题本入口
    const btnWeaknessReview = document.getElementById('btnOpenWeaknessReview');
    if (btnWeaknessReview) {
      btnWeaknessReview.addEventListener('click', () => this.openReviewScreen());
    }
  }

  updateHeaderStats() {
    const starEl = document.getElementById('headerStarCount');
    if (starEl && window.srsStorage) {
      starEl.textContent = window.srsStorage.getTotalStars();
    }
  }

  showToast(msg) {
    let t = document.getElementById('appToast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'appToast';
      t.className = 'toast-msg';
      document.body.appendChild(t);
    }
    t.innerHTML = msg;
    t.classList.add('show');
    clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => {
      t.classList.remove('show');
    }, 2200);
  }

  // 路由与画面切换
  switchScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    const target = document.getElementById(screenId);
    if (target) {
      target.classList.add('active');
      this.currentScreen = screenId;
      const main = document.querySelector('main.app-main');
      if (main) main.scrollTop = 0;
    }

    // 更新顶部返回按钮可见度
    const btnNavBack = document.getElementById('btnNavBack');
    if (btnNavBack) {
      btnNavBack.style.visibility = (screenId === 'screen-home') ? 'hidden' : 'visible';
    }
  }

  handleBackNavigation() {
    window.audioCtrl.stopSpeak();
    if (this.modeState.testTimerId) {
      clearInterval(this.modeState.testTimerId);
      this.modeState.testTimerId = null;
    }

    if (this.currentScreen === 'screen-home') {
      return;
    }
    if (this.currentScreen === 'screen-unit-detail') {
      this.switchScreen('screen-home');
      this.renderHome();
    } else {
      if (this.currentUnit) {
        this.switchScreen('screen-unit-detail');
        this.renderUnitDetail(this.currentUnit);
      } else {
        this.switchScreen('screen-home');
        this.renderHome();
      }
    }
  }

  // ================= 1. HOME SCREEN =================
  renderHome() {
    this.currentUnit = null;
    this.currentMode = null;
    this.updateHeaderStats();
    this.renderUnitList();

    // 更新 SRS 待复习计数 Badge
    const srsBadge = document.getElementById('homeSrsBadge');
    if (srsBadge && window.srsStorage) {
      const stats = window.srsStorage.getSrsStats();
      const errs = window.srsStorage.getWeaknesses();
      const count = stats.dueCount + errs.length;
      if (count > 0) {
        srsBadge.style.display = 'inline-block';
        srsBadge.textContent = count;
      } else {
        srsBadge.style.display = 'none';
      }
    }
  }

  renderUnitList() {
    const listEl = document.getElementById('homeUnitList');
    if (!listEl) return;

    let filtered = this.units;
    if (this.currentSubject !== 'all') {
      filtered = this.units.filter(u => u.subject === this.currentSubject);
    }

    if (filtered.length === 0) {
      listEl.innerHTML = `<div style="text-align:center;padding:30px;color:var(--ink-muted);">該当するユニットがありません</div>`;
      return;
    }

    const subjectMap = {
      math: { name: '数学', cls: 'math' },
      english: { name: '英語', cls: 'english' },
      science: { name: '理科', cls: 'science' },
      society: { name: '社会', cls: 'society' },
      japanese: { name: '国語', cls: 'japanese' }
    };

    listEl.innerHTML = filtered.map(u => {
      const s = subjectMap[u.subject] || { name: u.subject, cls: 'math' };
      const up = (window.srsStorage && window.srsStorage.state.unitProgress[u.unitId]) || { completedModes: [] };
      const modeCount = up.completedModes.length;

      return `
        <div class="unit-card" onclick="window.appEngine.openUnit('${u.unitId}')">
          <div class="unit-info">
            <div class="unit-tag-row">
              <span class="unit-badge ${s.cls}">${s.name}</span>
              <span class="unit-meta">中${u.grade} · 達成 ${modeCount}/6</span>
            </div>
            <div class="unit-title">${u.title}</div>
            <div class="unit-meta">${this.renderMath(u.description || '')}</div>
          </div>
          <button class="unit-action-btn">学習する ▶</button>
        </div>
      `;
    }).join('');
  }

  openUnit(unitId) {
    const u = this.units.find(x => x.unitId === unitId);
    if (!u) return;
    this.currentUnit = u;
    this.renderUnitDetail(u);
    this.switchScreen('screen-unit-detail');
  }

  // ================= 2. UNIT DETAIL SCREEN =================
  renderUnitDetail(u) {
    const titleEl = document.getElementById('unitDetailTitle');
    const descEl = document.getElementById('unitDetailDesc');
    const badgeEl = document.getElementById('unitDetailBadge');

    if (titleEl) titleEl.textContent = u.title;
    if (descEl) descEl.innerHTML = this.renderMath(u.description || '');

    const subjectMap = {
      math: { name: '数学', cls: 'math' },
      english: { name: '英語', cls: 'english' },
      science: { name: '理科', cls: 'science' },
      society: { name: '社会', cls: 'society' },
      japanese: { name: '国語', cls: 'japanese' }
    };
    const s = subjectMap[u.subject] || { name: u.subject, cls: 'math' };
    if (badgeEl) {
      badgeEl.className = 'unit-badge ' + s.cls;
      badgeEl.textContent = s.name;
    }

    const up = (window.srsStorage && window.srsStorage.state.unitProgress[u.unitId]) || { completedModes: [] };

    // 更新各个模式徽章
    const modes = ['story', 'flash', 'scramble', 'match', 'cloze', 'quiz'];
    modes.forEach(m => {
      const b = document.getElementById(`badge-mode-${m}`);
      if (b) {
        if (up.completedModes.includes(m)) {
          b.style.display = 'inline-block';
          b.textContent = '★ クリア';
          b.style.background = 'var(--success-light)';
          b.style.color = 'var(--success)';
        } else {
          b.style.display = 'none';
        }
      }
    });
  }

  startUnitMode(mode) {
    if (!this.currentUnit) return;
    this.currentMode = mode;

    switch (mode) {
      case 'story':
        this.initStoryMode();
        break;
      case 'flash':
        this.initFlashMode();
        break;
      case 'scramble':
        this.initScrambleMode();
        break;
      case 'match':
        this.initMatchMode();
        break;
      case 'cloze':
        this.initClozeMode();
        break;
      case 'quiz':
        this.initQuizMode();
        break;
    }
  }

  // ================= 3. STORY / READER MODE =================
  initStoryMode() {
    const list = this.currentUnit.story || [];
    if (list.length === 0) {
      this.showToast('このユニットには朗読文章がありません');
      return;
    }
    this.modeState.index = 0;
    this.modeState.items = list;
    this.renderStoryStep();
    this.switchScreen('screen-story');
  }

  renderStoryStep() {
    const item = this.modeState.items[this.modeState.index];
    const total = this.modeState.items.length;
    const pEl = document.getElementById('storyProgress');
    const textEl = document.getElementById('storyTextPrimary');
    const noteEl = document.getElementById('storyTextSecondary');

    if (pEl) pEl.textContent = `${this.modeState.index + 1} / ${total}`;
    if (textEl) textEl.innerHTML = this.renderMath(item.text);
    if (noteEl) noteEl.innerHTML = this.renderMath(item.note || '');

    // 自动朗读当前句子 (优先 Edge-TTS 高音质 MP3，无缝降级到浏览器 Natural 语音)
    const isJa = /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]/.test(item.text);
    const lang = (this.currentUnit && this.currentUnit.subject === 'english' && !isJa) ? 'en-US' : 'ja-JP';
    window.audioCtrl.playClip(this.currentUnit.unitId, item.id, item.text, lang);
  }

  storyPrev() {
    if (this.modeState.index > 0) {
      this.modeState.index--;
      this.renderStoryStep();
    }
  }

  storyNext() {
    if (this.modeState.index < this.modeState.items.length - 1) {
      this.modeState.index++;
      this.renderStoryStep();
    } else {
      // 完成
      this.completeMode('story', 1, 100);
    }
  }

  storyRepeatAudio() {
    const item = this.modeState.items[this.modeState.index];
    if (item) {
      const isJa = /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]/.test(item.text);
      const lang = (this.currentUnit && this.currentUnit.subject === 'english' && !isJa) ? 'en-US' : 'ja-JP';
      window.audioCtrl.playClip(this.currentUnit.unitId, item.id, item.text, lang);
    }
  }

  // ================= 4. FLASHCARD MODE =================
  initFlashMode() {
    const list = this.currentUnit.flashcards || [];
    if (list.length === 0) {
      this.showToast('このユニットには暗記カードがありません');
      return;
    }
    this.modeState.index = 0;
    this.modeState.items = [...list].sort(() => Math.random() - 0.5);
    this.modeState.correctCount = 0;
    this.renderFlashStep();
    this.switchScreen('screen-flash');
  }

  renderFlashStep() {
    const card = document.getElementById('flashCardElement');
    if (card) card.classList.remove('flipped');

    const item = this.modeState.items[this.modeState.index];
    const total = this.modeState.items.length;

    const pEl = document.getElementById('flashProgress');
    const termEl = document.getElementById('flashFrontTerm');
    const descEl = document.getElementById('flashBackDesc');
    const hintEl = document.getElementById('flashBackHint');

    if (pEl) pEl.textContent = `${this.modeState.index + 1} / ${total}`;
    if (termEl) termEl.innerHTML = this.renderMath(item.term);
    if (descEl) descEl.innerHTML = this.renderMath(item.desc);
    if (hintEl) hintEl.innerHTML = this.renderMath(item.hint || '');
  }

  flipFlashCard() {
    window.audioCtrl.playFlip();
    const card = document.getElementById('flashCardElement');
    if (card) card.classList.toggle('flipped');
  }

  flashAudio() {
    const item = this.modeState.items[this.modeState.index];
    if (item) {
      const isJa = /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]/.test(item.term);
      const lang = (isJa || !this.currentUnit || this.currentUnit.subject !== 'english') ? 'ja-JP' : 'en-US';
      window.audioCtrl.playClip(this.currentUnit.unitId, item.id, item.term, lang);
    }
  }

  handleFlashAction(remembered) {
    const item = this.modeState.items[this.modeState.index];
    item.subject = this.currentUnit.subject;
    window.srsStorage.recordSrsResult(item, remembered);

    if (remembered) {
      window.audioCtrl.playCorrect();
      this.modeState.correctCount++;
    } else {
      window.audioCtrl.playWrong();
    }

    if (this.modeState.index < this.modeState.items.length - 1) {
      this.modeState.index++;
      this.renderFlashStep();
    } else {
      const rate = Math.round((this.modeState.correctCount / this.modeState.items.length) * 100);
      const stars = (rate >= 80) ? 2 : 1;
      this.completeMode('flash', stars, rate);
    }
  }

  // ================= 5. SCRAMBLE / PROOF PUZZLE MODE =================
  initScrambleMode() {
    const list = this.currentUnit.scrambles || [];
    if (list.length === 0) {
      this.showToast('このユニットには並べ替え問題がありません');
      return;
    }
    this.modeState.index = 0;
    this.modeState.items = list;
    this.modeState.correctCount = 0;
    this.renderScrambleStep();
    this.switchScreen('screen-scramble');
  }

  renderScrambleStep() {
    const item = this.modeState.items[this.modeState.index];
    const total = this.modeState.items.length;
    const pEl = document.getElementById('scrambleProgress');
    const qEl = document.getElementById('scrambleQuestionText');
    const targetZone = document.getElementById('scrambleTargetZone');
    const sourceZone = document.getElementById('scrambleSourceZone');

    if (pEl) pEl.textContent = `${this.modeState.index + 1} / ${total}`;
    if (qEl) qEl.innerHTML = this.renderMath(item.question);

    const isProof = (item.type === 'proof');

    if (isProof) {
      targetZone.className = 'scramble-target-zone proof-mode';
      sourceZone.className = 'scramble-source-zone proof-mode';
      targetZone.innerHTML = '';

      // 将步骤打乱放入 sourceZone
      const steps = item.steps.map((text, idx) => ({ id: idx, text }));
      this.modeState.scrambleTokensRemain = [...steps].sort(() => Math.random() - 0.5);
      this.modeState.scrambleUserOrder = [];
      this.renderProofZones();
    } else {
      targetZone.className = 'scramble-target-zone';
      sourceZone.className = 'scramble-source-zone';
      targetZone.innerHTML = '';

      const tokens = item.tokens.map((text, idx) => ({ id: idx, text }));
      this.modeState.scrambleTokensRemain = [...tokens].sort(() => Math.random() - 0.5);
      this.modeState.scrambleUserOrder = [];
      this.renderTokenZones();
    }
  }

  renderProofZones() {
    const targetZone = document.getElementById('scrambleTargetZone');
    const sourceZone = document.getElementById('scrambleSourceZone');

    targetZone.innerHTML = this.modeState.scrambleUserOrder.map((step, idx) => `
      <div class="scramble-step-card" onclick="window.appEngine.removeProofStep(${idx})">
        <span style="font-weight:800;color:var(--primary);margin-right:6px;">#${idx + 1}</span>
        <span class="step-text">${this.renderMath(step.text)}</span>
        <span class="step-handle">✕</span>
      </div>
    `).join('') || '<div style="color:#94a3b8;font-size:13px;text-align:center;padding:16px;width:100%;">下から論理ステップをタップして順に並べてください</div>';

    sourceZone.innerHTML = this.modeState.scrambleTokensRemain.map((step, idx) => `
      <div class="scramble-step-card" onclick="window.appEngine.addProofStep(${idx})">
        <span class="step-text">${this.renderMath(step.text)}</span>
        <span class="step-handle" style="color:var(--primary);">+</span>
      </div>
    `).join('') || '<div style="color:#94a3b8;font-size:12px;text-align:center;padding:10px;width:100%;">すべてのステップを選択しました</div>';
  }

  addProofStep(sourceIdx) {
    window.audioCtrl.playFlip();
    const item = this.modeState.scrambleTokensRemain.splice(sourceIdx, 1)[0];
    this.modeState.scrambleUserOrder.push(item);
    this.renderProofZones();
  }

  removeProofStep(targetIdx) {
    window.audioCtrl.playFlip();
    const item = this.modeState.scrambleUserOrder.splice(targetIdx, 1)[0];
    this.modeState.scrambleTokensRemain.push(item);
    this.renderProofZones();
  }

  renderTokenZones() {
    const targetZone = document.getElementById('scrambleTargetZone');
    const sourceZone = document.getElementById('scrambleSourceZone');

    targetZone.innerHTML = this.modeState.scrambleUserOrder.map((token, idx) => `
      <span class="scramble-token" onclick="window.appEngine.removeScrambleToken(${idx})">
        ${this.renderMath(token.text)}
      </span>
    `).join('') || '<span style="color:#94a3b8;font-size:13px;padding:6px;">下のピースをタップして文を組み立ててください</span>';

    sourceZone.innerHTML = this.modeState.scrambleTokensRemain.map((token, idx) => `
      <span class="scramble-token" onclick="window.appEngine.addScrambleToken(${idx})">
        ${this.renderMath(token.text)}
      </span>
    `).join('');
  }

  addScrambleToken(idx) {
    window.audioCtrl.playFlip();
    const token = this.modeState.scrambleTokensRemain.splice(idx, 1)[0];
    this.modeState.scrambleUserOrder.push(token);
    this.renderTokenZones();
  }

  removeScrambleToken(idx) {
    window.audioCtrl.playFlip();
    const token = this.modeState.scrambleUserOrder.splice(idx, 1)[0];
    this.modeState.scrambleTokensRemain.push(token);
    this.renderTokenZones();
  }

  checkScramble() {
    const item = this.modeState.items[this.modeState.index];
    const isProof = (item.type === 'proof');

    let isCorrect = true;
    if (isProof) {
      if (this.modeState.scrambleUserOrder.length !== item.steps.length) {
        this.showToast('すべての手順を配置してください！');
        return;
      }
      for (let i = 0; i < item.steps.length; i++) {
        if (this.modeState.scrambleUserOrder[i].text !== (isProof ? item.steps[i] : item.tokens[i])) {
          isCorrect = false;
          break;
        }
      }
    } else {
      if (this.modeState.scrambleUserOrder.length !== item.tokens.length) {
        this.showToast('すべての単語ピースを配置してください！');
        return;
      }
      for (let i = 0; i < item.tokens.length; i++) {
        if (this.modeState.scrambleUserOrder[i].text !== (isProof ? item.steps[i] : item.tokens[i])) {
          isCorrect = false;
          break;
        }
      }
    }

    if (isCorrect) {
      window.audioCtrl.playCorrect();
      this.showToast('🎉 正解です！論理が完璧につながりました！');
      this.modeState.correctCount++;
    } else {
      window.audioCtrl.playWrong();
      this.showToast('❌ 順序が違います。もう一度見直してみましょう');
      window.srsStorage.recordWeakness({
        id: item.id,
        q: item.question,
        a: isProof ? item.steps.join(' → ') : item.tokens.join(' '),
        explanation: '順序並べ替え問題の復習',
        subject: this.currentUnit.subject
      });
    }

    setTimeout(() => {
      if (this.modeState.index < this.modeState.items.length - 1) {
        this.modeState.index++;
        this.renderScrambleStep();
      } else {
        const rate = Math.round((this.modeState.correctCount / this.modeState.items.length) * 100);
        this.completeMode('scramble', (rate >= 80) ? 2 : 1, rate);
      }
    }, 1200);
  }

  // ================= 6. MATCH PAIRS MODE =================
  initMatchMode() {
    const list = this.currentUnit.matches || [];
    if (list.length === 0) {
      this.showToast('このユニットには配対問題がありません');
      return;
    }
    this.modeState.items = list;
    this.modeState.selectedMatchLeft = null;
    this.modeState.selectedMatchRight = null;
    this.modeState.matchedPairsCount = 0;

    const leftCol = list.map((item, idx) => ({ id: idx, text: item.left })).sort(() => Math.random() - 0.5);
    const rightCol = list.map((item, idx) => ({ id: idx, text: item.right })).sort(() => Math.random() - 0.5);

    const leftContainer = document.getElementById('matchLeftCol');
    const rightContainer = document.getElementById('matchRightCol');

    leftContainer.innerHTML = leftCol.map(item => `
      <div class="match-item" id="match-l-${item.id}" data-id="${item.id}" onclick="window.appEngine.handleMatchClick('left', ${item.id})">
        ${this.renderMath(item.text)}
      </div>
    `).join('');

    rightContainer.innerHTML = rightCol.map(item => `
      <div class="match-item" id="match-r-${item.id}" data-id="${item.id}" onclick="window.appEngine.handleMatchClick('right', ${item.id})">
        ${this.renderMath(item.text)}
      </div>
    `).join('');

    this.switchScreen('screen-match');
  }

  handleMatchClick(side, id) {
    window.audioCtrl.playFlip();

    if (side === 'left') {
      document.querySelectorAll('#matchLeftCol .match-item').forEach(el => el.classList.remove('selected'));
      const el = document.getElementById(`match-l-${id}`);
      if (el && !el.classList.contains('matched')) {
        el.classList.add('selected');
        this.modeState.selectedMatchLeft = id;
      }
    } else {
      document.querySelectorAll('#matchRightCol .match-item').forEach(el => el.classList.remove('selected'));
      const el = document.getElementById(`match-r-${id}`);
      if (el && !el.classList.contains('matched')) {
        el.classList.add('selected');
        this.modeState.selectedMatchRight = id;
      }
    }

    if (this.modeState.selectedMatchLeft !== null && this.modeState.selectedMatchRight !== null) {
      const leftId = this.modeState.selectedMatchLeft;
      const rightId = this.modeState.selectedMatchRight;

      if (leftId === rightId) {
        window.audioCtrl.playCorrect();
        const lEl = document.getElementById(`match-l-${leftId}`);
        const rEl = document.getElementById(`match-r-${rightId}`);
        lEl.classList.remove('selected');
        rEl.classList.remove('selected');
        lEl.classList.add('matched');
        rEl.classList.add('matched');

        this.modeState.matchedPairsCount++;
        this.modeState.selectedMatchLeft = null;
        this.modeState.selectedMatchRight = null;

        if (this.modeState.matchedPairsCount === this.modeState.items.length) {
          setTimeout(() => {
            this.completeMode('match', 2, 100);
          }, 600);
        }
      } else {
        window.audioCtrl.playWrong();
        const lEl = document.getElementById(`match-l-${leftId}`);
        const rEl = document.getElementById(`match-r-${rightId}`);
        lEl.classList.add('error');
        rEl.classList.add('error');

        setTimeout(() => {
          lEl.classList.remove('error', 'selected');
          rEl.classList.remove('error', 'selected');
          this.modeState.selectedMatchLeft = null;
          this.modeState.selectedMatchRight = null;
        }, 500);
      }
    }
  }

  // ================= 7. CLOZE MODE =================
  initClozeMode() {
    const list = this.currentUnit.cloze || [];
    if (list.length === 0) {
      this.showToast('このユニットには穴埋め問題がありません');
      return;
    }
    this.modeState.index = 0;
    this.modeState.items = list.map(c => this.shuffleChoices(c));
    this.modeState.correctCount = 0;
    this.renderClozeStep();
    this.switchScreen('screen-cloze');
  }

  renderClozeStep() {
    const item = this.modeState.items[this.modeState.index];
    const total = this.modeState.items.length;
    const pEl = document.getElementById('clozeProgress');
    const qEl = document.getElementById('clozeQuestionText');
    const optsEl = document.getElementById('clozeOptionsContainer');
    const expEl = document.getElementById('clozeExplanationBox');

    if (pEl) pEl.textContent = `${this.modeState.index + 1} / ${total}`;
    if (qEl) qEl.innerHTML = this.renderMath(item.question);
    if (expEl) expEl.classList.remove('active');

    optsEl.innerHTML = item.options.map((opt, idx) => `
      <div class="quiz-option" id="cloze-opt-${idx}" onclick="window.appEngine.handleClozeAnswer(${idx})">
        <span style="font-weight:800;color:var(--primary);">${String.fromCharCode(65 + idx)}.</span>
        <span>${this.renderMath(opt)}</span>
      </div>
    `).join('');
  }

  handleClozeAnswer(optIdx) {
    const item = this.modeState.items[this.modeState.index];
    const selected = item.options[optIdx];
    const isCorrect = (selected === item.answer);
    const expEl = document.getElementById('clozeExplanationBox');

    document.querySelectorAll('#clozeOptionsContainer .quiz-option').forEach(el => el.style.pointerEvents = 'none');

    const optEl = document.getElementById(`cloze-opt-${optIdx}`);
    if (isCorrect) {
      window.audioCtrl.playCorrect();
      optEl.classList.add('correct');
      this.modeState.correctCount++;
    } else {
      window.audioCtrl.playWrong();
      optEl.classList.add('wrong');
      // 高亮正确选项
      const correctIdx = item.options.indexOf(item.answer);
      if (correctIdx >= 0) {
        document.getElementById(`cloze-opt-${correctIdx}`).classList.add('correct');
      }
      window.srsStorage.recordWeakness({
        id: item.id,
        q: item.question,
        a: item.answer,
        explanation: item.explanation,
        subject: this.currentUnit.subject
      });
    }

    if (expEl && item.explanation) {
      expEl.innerHTML = `<strong>解説:</strong> ` + this.renderMath(item.explanation);
      expEl.classList.add('active');
    }

    setTimeout(() => {
      if (this.modeState.index < this.modeState.items.length - 1) {
        this.modeState.index++;
        this.renderClozeStep();
      } else {
        const rate = Math.round((this.modeState.correctCount / this.modeState.items.length) * 100);
        this.completeMode('cloze', (rate >= 80) ? 2 : 1, rate);
      }
    }, 1600);
  }

  // ================= 8. QUIZ MODE =================
  initQuizMode() {
    const list = this.currentUnit.quizzes || [];
    if (list.length === 0) {
      this.showToast('このユニットにはクイズがありません');
      return;
    }
    this.modeState.index = 0;
    this.modeState.items = list.map(q => this.shuffleChoices(q));
    this.modeState.correctCount = 0;
    this.renderQuizStep();
    this.switchScreen('screen-quiz');
  }

  renderQuizStep() {
    const item = this.modeState.items[this.modeState.index];
    const total = this.modeState.items.length;
    const pEl = document.getElementById('quizProgress');
    const qEl = document.getElementById('quizQuestionText');
    const optsEl = document.getElementById('quizOptionsContainer');
    const expEl = document.getElementById('quizExplanationBox');

    if (pEl) pEl.textContent = `${this.modeState.index + 1} / ${total}`;
    if (qEl) qEl.innerHTML = this.renderMath(item.q);
    if (expEl) expEl.classList.remove('active');

    optsEl.innerHTML = item.options.map((opt, idx) => `
      <div class="quiz-option" id="quiz-opt-${idx}" onclick="window.appEngine.handleQuizAnswer(${idx})">
        <span style="font-weight:800;color:var(--primary);">${String.fromCharCode(65 + idx)}.</span>
        <span>${this.renderMath(opt)}</span>
      </div>
    `).join('');
  }

  handleQuizAnswer(optIdx) {
    const item = this.modeState.items[this.modeState.index];
    const isCorrect = (optIdx === item.answerIndex);
    const expEl = document.getElementById('quizExplanationBox');

    document.querySelectorAll('#quizOptionsContainer .quiz-option').forEach(el => el.style.pointerEvents = 'none');

    const optEl = document.getElementById(`quiz-opt-${optIdx}`);
    if (isCorrect) {
      window.audioCtrl.playCorrect();
      optEl.classList.add('correct');
      this.modeState.correctCount++;
    } else {
      window.audioCtrl.playWrong();
      optEl.classList.add('wrong');
      const correctEl = document.getElementById(`quiz-opt-${item.answerIndex}`);
      if (correctEl) correctEl.classList.add('correct');

      window.srsStorage.recordWeakness({
        id: item.id,
        q: item.q,
        a: item.options[item.answerIndex],
        explanation: item.explanation,
        subject: this.currentUnit.subject
      });
    }

    if (expEl && item.explanation) {
      expEl.innerHTML = `<strong>解説:</strong> ` + this.renderMath(item.explanation);
      expEl.classList.add('active');
    }

    setTimeout(() => {
      if (this.modeState.index < this.modeState.items.length - 1) {
        this.modeState.index++;
        this.renderQuizStep();
      } else {
        const rate = Math.round((this.modeState.correctCount / this.modeState.items.length) * 100);
        this.completeMode('quiz', (rate >= 80) ? 3 : 1, rate);
      }
    }, 1800);
  }

  // ================= 9. 15-MINUTE SPRINT TEST (小テスト) =================
  startSprintTest() {
    let pool = [];
    this.units.forEach(u => {
      if (u.quizzes) {
        u.quizzes.forEach(q => pool.push(this.shuffleChoices({ ...q, subject: u.subject, unitTitle: u.title })));
      }
    });

    if (pool.length === 0) {
      this.showToast('テスト用の問題プールが不足しています');
      return;
    }

    // 随机抽取 10 道题目
    this.modeState.items = pool.sort(() => Math.random() - 0.5).slice(0, 10);
    this.modeState.index = 0;
    this.modeState.correctCount = 0;
    this.modeState.testTimeRemain = 900; // 15分钟

    if (this.modeState.testTimerId) {
      clearInterval(this.modeState.testTimerId);
    }
    this.modeState.testTimerId = setInterval(() => {
      this.modeState.testTimeRemain--;
      this.updateTestTimerDisplay();
      if (this.modeState.testTimeRemain <= 0) {
        clearInterval(this.modeState.testTimerId);
        this.modeState.testTimerId = null;
        this.showToast('⏰ 制限時間終了です！');
        this.finishSprintTest();
      }
    }, 1000);

    this.renderTestStep();
    this.switchScreen('screen-test');
  }

  updateTestTimerDisplay() {
    const el = document.getElementById('testTimerDisplay');
    if (!el) return;
    const m = Math.floor(this.modeState.testTimeRemain / 60).toString().padStart(2, '0');
    const s = (this.modeState.testTimeRemain % 60).toString().padStart(2, '0');
    el.textContent = `⏱️ ${m}:${s}`;
  }

  renderTestStep() {
    const item = this.modeState.items[this.modeState.index];
    const total = this.modeState.items.length;
    const pEl = document.getElementById('testProgressDisplay');
    const qEl = document.getElementById('testQuestionText');
    const optsEl = document.getElementById('testOptionsContainer');

    if (pEl) pEl.textContent = `第 ${this.modeState.index + 1} 問 / 全 ${total} 問 (${item.unitTitle})`;
    if (qEl) qEl.innerHTML = this.renderMath(item.q);

    optsEl.innerHTML = item.options.map((opt, idx) => `
      <div class="quiz-option" id="test-opt-${idx}" onclick="window.appEngine.handleTestAnswer(${idx})">
        <span style="font-weight:800;color:var(--primary);">${String.fromCharCode(65 + idx)}.</span>
        <span>${this.renderMath(opt)}</span>
      </div>
    `).join('');
  }

  handleTestAnswer(optIdx) {
    const item = this.modeState.items[this.modeState.index];
    const isCorrect = (optIdx === item.answerIndex);

    if (isCorrect) {
      window.audioCtrl.playCorrect();
      this.modeState.correctCount++;
    } else {
      window.audioCtrl.playWrong();
      window.srsStorage.recordWeakness({
        id: item.id,
        q: item.q,
        a: item.options[item.answerIndex],
        explanation: item.explanation,
        subject: item.subject
      });
    }

    if (this.modeState.index < this.modeState.items.length - 1) {
      this.modeState.index++;
      this.renderTestStep();
    } else {
      this.finishSprintTest();
    }
  }

  finishSprintTest() {
    if (this.modeState.testTimerId) {
      clearInterval(this.modeState.testTimerId);
      this.modeState.testTimerId = null;
    }
    const rate = Math.round((this.modeState.correctCount / this.modeState.items.length) * 100);
    const stars = (rate >= 90) ? 3 : ((rate >= 60) ? 2 : 1);
    window.srsStorage.addStars(stars);
    this.showResultScreen('定期考査対策 15分小テスト', stars, rate, this.modeState.correctCount, this.modeState.items.length);
  }

  // ================= 10. REVIEW SCREEN (SRS & WEAKNESSES) =================
  openReviewScreen() {
    this.renderReviewScreen();
    this.switchScreen('screen-review');
  }

  renderReviewScreen() {
    const stats = window.srsStorage.getSrsStats();
    const weaknesses = window.srsStorage.getWeaknesses();

    const box1 = document.getElementById('srsBox1Count');
    const box2 = document.getElementById('srsBox2Count');
    const box3 = document.getElementById('srsBox3Count');
    const box4 = document.getElementById('srsBox4Count');

    if (box1) box1.textContent = stats.box1;
    if (box2) box2.textContent = stats.box2;
    if (box3) box3.textContent = stats.box3;
    if (box4) box4.textContent = stats.box4;

    const listEl = document.getElementById('weaknessItemList');
    if (!listEl) return;

    if (weaknesses.length === 0) {
      listEl.innerHTML = `<div style="text-align:center;padding:24px;color:var(--ink-muted);">現在、苦手ノートに登録された問題はありません！素晴らしい成果です 🎉</div>`;
      return;
    }

    listEl.innerHTML = weaknesses.map((w, idx) => `
      <div style="background:#fff;border:1.5px solid var(--border-color);border-radius:var(--radius-md);padding:12px;margin-bottom:8px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
          <span class="unit-badge ${w.subject}">${w.subject}</span>
          <button style="border:none;background:var(--success-light);color:var(--success);font-weight:800;font-size:11px;padding:3px 8px;border-radius:10px;cursor:pointer;" onclick="window.appEngine.resolveWeaknessItem('${w.id}')">克服済にする ✔</button>
        </div>
        <div style="font-weight:800;font-size:14px;margin-bottom:4px;">${this.renderMath(w.question)}</div>
        <div style="font-size:12px;color:var(--primary);font-weight:700;">正解: ${this.renderMath(w.answer)}</div>
        ${w.explanation ? `<div style="font-size:11px;color:var(--ink-muted);margin-top:4px;">${this.renderMath(w.explanation)}</div>` : ''}
      </div>
    `).join('');
  }

  resolveWeaknessItem(id) {
    window.audioCtrl.playStar();
    window.srsStorage.resolveWeakness(id);
    this.renderReviewScreen();
    this.showToast('🌟 苦手を克服しました！');
  }

  // ================= 11. COMPLETE & RESULT =================
  completeMode(modeKey, starsEarned, scorePercent) {
    if (this.currentUnit) {
      window.srsStorage.recordModeComplete(this.currentUnit.unitId, modeKey, starsEarned);
    }
    this.showResultScreen(this.currentUnit ? this.currentUnit.title : 'クリア', starsEarned, scorePercent);
  }

  showResultScreen(title, stars, scorePercent, correct = null, total = null) {
    window.audioCtrl.playFanfare();
    this.updateHeaderStats();

    const titleEl = document.getElementById('resultTitleText');
    const scoreEl = document.getElementById('resultScoreText');
    const starsEl = document.getElementById('resultStarsDisplay');
    const metaEl = document.getElementById('resultMetaText');

    if (titleEl) titleEl.textContent = title;
    if (scoreEl) scoreEl.textContent = `${scorePercent}%`;

    let starsStr = '';
    for (let i = 0; i < 3; i++) {
      starsStr += (i < stars) ? '⭐' : '☆';
    }
    if (starsEl) starsEl.textContent = starsStr;

    if (metaEl) {
      if (correct !== null && total !== null) {
        metaEl.textContent = `正答数: ${correct} / ${total} 問 (獲得スター: +${stars})`;
      } else {
        metaEl.textContent = `獲得スター: +${stars} ★`;
      }
    }

    this.switchScreen('screen-result');
  }

  backToCurrentUnit() {
    if (this.currentUnit) {
      this.switchScreen('screen-unit-detail');
      this.renderUnitDetail(this.currentUnit);
    } else {
      this.switchScreen('screen-home');
      this.renderHome();
    }
  }
}

window.AppEngine = AppEngine;

// 页面加载完成后实例化引擎
window.addEventListener('DOMContentLoaded', () => {
  window.appEngine = new AppEngine();
});
