/**
 * ClausePlayer - 课文三种朗读模式与高精度音频进度条通用组件
 * 
 * 模式 1: 🎵 原来整句播放 (Original Mode)
 *        - 100% 保留教材自然语流原声，无逗号切片停顿（零间隔）
 *        - 进度条平滑滑动显示真实进度，支持任意时间轴拖拽与标点吸附瞬移
 *        - 保留整句原版大字排版
 * 
 * 模式 2: 🔹 逗号分句细读 (Clause Mode)
 *        - 按标点意群切片为短句胶囊，突出微观精听精读
 *        - 配备单分句无限循环复读 (Loop 攻坚难句)
 *        - 聚焦卡片单独展示该分句之拼音、汉字、英文与日文释义
 * 
 * 模式 3: 🔸 整句连续听 (Sentence Mode)
 *        - 分句依次连贯朗读，分句间保留微小停顿 (200ms) 便于学生短时记忆跟读与模仿
 *        - 卡拉OK式短句胶囊随播放进度动态变黄同步高亮
 * 
 * 具备带吸附锚点的可定位音频进度条 (Interactive Scrub Bar with Clause Ticks)
 */

(function(window) {
  'use strict';

  const LESSON_KEY_MAP = {
    'hanjia-jianwen': 'hanjia',
    'gugong': 'gugong',
    'yiheyuan': 'yiheyuan',
    'luotuo-he-yang': 'luotuo',
    'xiaoma-guohe': 'xiaoma',
    'houzi-lao-yueliang': 'houzi',
    'sima-guang': 'sima',
    'shu-xingxing': 'xingxing',
    'gushi-er-shou': 'gushi',
    'diqiu-qingjiegong': 'diqiu',
    'daziran-yuyan': 'daziran',
    'tanyue': 'tanyue'
  };

  const ClausePlayer = {
    lessonKey: null,
    lessonData: null,
    currentSentIdx: 0,
    currentClauseIdx: 0,
    granularityMode: 'original', // 'original' | 'clause' | 'sentence'
    isPlaying: false,
    isLooping: false,
    playbackRate: 1.0,
    activeAudio: null,
    animFrameId: null,
    mounted: false,
    isDraggingScrub: false,

    /**
     * 自动初始化或指定 lessonKey / lessonSlug
     */
    init: function(options) {
      options = options || {};
      let key = options.lessonKey || options.lessonSlug;
      if (!key) {
        const path = window.location.pathname;
        for (const [slug, mappedKey] of Object.entries(LESSON_KEY_MAP)) {
          if (path.indexOf(slug) !== -1) {
            key = mappedKey;
            break;
          }
        }
      }
      this.lessonKey = key || 'xiaoma';

      // 提取课文分句元数据
      if (window.ALL_LESSON_CLAUSES && window.ALL_LESSON_CLAUSES[this.lessonKey]) {
        this.lessonData = window.ALL_LESSON_CLAUSES[this.lessonKey];
      } else {
        console.warn('[ClausePlayer] 未找到课文分句数据:', this.lessonKey);
        return;
      }

      // 读取持久化模式偏好，默认优先使用原来的整句模式
      try {
        const savedMode = localStorage.getItem('cp_playback_mode');
        if (savedMode === 'original' || savedMode === 'clause' || savedMode === 'sentence') {
          this.granularityMode = savedMode;
        } else {
          this.granularityMode = 'original';
        }
      } catch (e) {
        this.granularityMode = 'original';
      }

      this.precomputeTimings();
      this.mountUI();
      this.hookExistingStory();
      this.hookExistingFullText();
      console.log('[ClausePlayer] 已就绪 (3模式版), 课文:', this.lessonData.title, '当前模式:', this.granularityMode);
    },

    precomputeTimings: function() {
      if (!this.lessonData || !this.lessonData.sentences) return;
      let globalAcc = 0;
      this.lessonData.sentences.forEach(sent => {
        let sentAcc = 0;
        (sent.clauses || []).forEach(c => {
          c.duration = c.duration || 2.0;
          c.sentOffsetStart = sentAcc;
          c.sentOffsetEnd = sentAcc + c.duration;
          c.globalOffsetStart = globalAcc;
          c.globalOffsetEnd = globalAcc + c.duration;
          sentAcc += c.duration;
          globalAcc += c.duration;
        });
        sent.duration = sentAcc || 3.0;
      });
      this.lessonData.totalDuration = globalAcc;
    },

    /**
     * 将播放组件注入到 screen-story 中
     */
    mountUI: function() {
      const storyScreen = document.getElementById('screen-story');
      if (!storyScreen) return;

      const storyCard = storyScreen.querySelector('.story-card');
      if (!storyCard) return;

      // 避免重复挂载
      if (document.getElementById('clausePlayerRoot')) return;

      // 1. 三种模式选择器 (原来的整句播放 / 逗号分句细读 / 整句连续听)
      const modeBar = document.createElement('div');
      modeBar.className = 'clause-mode-selector';
      modeBar.id = 'clauseModeBar';
      modeBar.innerHTML = `
        <button class="clause-mode-btn ${this.granularityMode === 'original' ? 'active' : ''}" id="cpBtnModeOriginal" onclick="ClausePlayer.setMode('original')" title="原来整句播放：教材原声，自然连贯无切片停顿">
          <span>🎵 原来整句播放</span>
        </button>
        <button class="clause-mode-btn ${this.granularityMode === 'clause' ? 'active' : ''}" id="cpBtnModeClause" onclick="ClausePlayer.setMode('clause')" title="逗号分句细读：短句点击精读，单句无限循环">
          <span>🔹 逗号分句细读</span>
        </button>
        <button class="clause-mode-btn ${this.granularityMode === 'sentence' ? 'active' : ''}" id="cpBtnModeSentence" onclick="ClausePlayer.setMode('sentence')" title="整句连续听：分句带短暂间隔，便于跟读模仿">
          <span>🔸 整句连续听</span>
        </button>
      `;

      // 2. 分句气泡条与聚焦卡片与进度条容器
      const playerRoot = document.createElement('div');
      playerRoot.id = 'clausePlayerRoot';
      playerRoot.style.width = '100%';
      playerRoot.style.display = 'flex';
      playerRoot.style.flexDirection = 'column';
      playerRoot.style.gap = '8px';

      playerRoot.innerHTML = `
        <!-- 分句药丸列表 -->
        <div class="clause-pills-container" id="cpPillsContainer">
          <div class="clause-pills-hint" id="cpPillsHint">👇 点击下方任意短句可单独点读：</div>
          <div class="clause-pills-list" id="cpPillsList"></div>
        </div>

        <!-- 当前精读分句聚焦卡片 -->
        <div class="clause-focus-card" id="cpFocusCard" style="display:none;">
          <div class="clause-focus-tag">
            <span>🎯 当前精读小分句：</span>
            <span id="cpFocusNum">分句 1 / 1</span>
          </div>
          <div class="clause-focus-py" id="cpFocusPy"></div>
          <div class="clause-focus-zh" id="cpFocusZh"></div>
          <div class="clause-focus-trans" id="cpFocusTrans">
            <div class="clause-focus-en" id="cpFocusEn"></div>
            <div class="clause-focus-jp" id="cpFocusJp"></div>
          </div>
        </div>

        <!-- 音频进度条与控制器 -->
        <div class="clause-player-box" id="cpPlayerBox">
          <div class="clause-time-row">
            <span class="clause-status-txt" id="cpStatusTxt">就绪</span>
            <span class="clause-timer-display" id="cpTimerTxt">00:00 / 00:00</span>
          </div>

          <!-- 可拖拽/点击定位进度条与吸附锚点 -->
          <div class="clause-scrub-container" id="cpScrubContainer">
            <div class="clause-scrub-track" id="cpScrubTrack">
              <div class="clause-scrub-fill" id="cpScrubFill"></div>
              <div class="clause-scrub-thumb" id="cpScrubThumb"></div>
            </div>
          </div>

          <!-- 控制按钮栏 -->
          <div class="clause-ctrl-row">
            <div class="clause-ctrl-left">
              <button class="cp-icon-btn" id="cpPrevBtn" onclick="ClausePlayer.prev()" title="上一句 / 上一分句">⏮️</button>
              <button class="cp-icon-btn primary" id="cpPlayBtn" onclick="ClausePlayer.togglePlay()" title="播放 / 暂停">▶️</button>
              <button class="cp-icon-btn" id="cpNextBtn" onclick="ClausePlayer.next()" title="下一句 / 下一分句">⏭️</button>
            </div>
            <div class="clause-ctrl-right">
              <button class="cp-tag-btn" id="cpLoopBtn" onclick="ClausePlayer.toggleLoop()" title="单句循环跟读">🔁 循环当前句</button>
              <button class="cp-tag-btn" id="cpRateBtn" onclick="ClausePlayer.toggleRate()" title="切换语速">⚡ 1.0x</button>
            </div>
          </div>
        </div>
      `;

      // 插入模式切换器到卡片上方
      storyCard.parentNode.insertBefore(modeBar, storyCard);
      // 插入分句控制器到原整句显示卡片中
      storyCard.appendChild(playerRoot);

      this.initScrubEvents();
      this.updateVisibilityForMode();
      this.mounted = true;
    },

    /**
     * 进度条点击与拖拽手势
     */
    initScrubEvents: function() {
      const container = document.getElementById('cpScrubContainer');
      const track = document.getElementById('cpScrubTrack');
      if (!container || !track) return;

      const onSeek = (clientX) => {
        const rect = track.getBoundingClientRect();
        const ratio = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
        const sent = this.getCurrentSent();
        if (!sent) return;

        if (this.granularityMode === 'original') {
          const dur = (this.activeAudio && !isNaN(this.activeAudio.duration) && this.activeAudio.duration > 0)
            ? this.activeAudio.duration : (sent.duration || 5.0);
          const targetTime = ratio * dur;
          this.seekOriginalTo(targetTime);
          return;
        }

        // clause or sentence mode
        const targetTime = ratio * (sent.duration || 1.0);
        let matchedIdx = 0;
        const clauses = sent.clauses || [];
        for (let i = 0; i < clauses.length; i++) {
          if (targetTime >= clauses[i].sentOffsetStart && targetTime <= clauses[i].sentOffsetEnd) {
            matchedIdx = i;
            break;
          }
        }
        if (this.granularityMode === 'clause') {
          this.selectClause(matchedIdx, true);
        } else {
          this.playSentenceMode(matchedIdx);
        }
      };

      container.addEventListener('click', (e) => {
        if (e.target.closest('.clause-tick-mark')) return; // 由锚点自身处理
        onSeek(e.clientX);
      });

      // 触屏滑动支持
      let isTouching = false;
      container.addEventListener('touchstart', (e) => {
        isTouching = true;
        this.isDraggingScrub = true;
        if (e.touches && e.touches[0]) onSeek(e.touches[0].clientX);
      }, { passive: true });

      window.addEventListener('touchmove', (e) => {
        if (!isTouching) return;
        if (e.touches && e.touches[0]) onSeek(e.touches[0].clientX);
      }, { passive: true });

      window.addEventListener('touchend', () => {
        isTouching = false;
        this.isDraggingScrub = false;
      });
    },

    /**
     * 优雅劫持与联动原有的 story 流程
     */
    hookExistingStory: function() {
      const self = this;
      const originalRenderStory = window.renderStory;
      if (typeof originalRenderStory === 'function') {
        window.renderStory = function() {
          originalRenderStory.apply(this, arguments);
          const idx = typeof window.storyIdx === 'number' ? window.storyIdx : 0;
          self.onSentenceChange(idx);
        };
      }

      // 联动全局 stopClip，避免多音频冲突
      const originalStopClip = window.stopClip;
      if (typeof originalStopClip === 'function') {
        window.stopClip = function() {
          originalStopClip.apply(this, arguments);
          self.stopAudio();
        };
      }

      // 智能代理 playClip：在 screen-story 活跃且播放当前句子时，接入 ClausePlayer 的模式
      const originalPlayClip = window.playClip;
      if (typeof originalPlayClip === 'function') {
        window.playClip = function(id, fallbackText, onEnded, lang) {
          const storyScreen = document.getElementById('screen-story');
          const isStoryActive = storyScreen && storyScreen.classList.contains('active');
          const currentSent = self.getCurrentSent();
          const isCurrentSentAudio = currentSent && (currentSent.sentId === id || id === 'st' + (self.currentSentIdx + 1));

          if (isStoryActive && isCurrentSentAudio && (!lang || lang === 'zh-CN')) {
            if (self.granularityMode === 'original') {
              self.playOriginalSentence();
            } else if (self.granularityMode === 'clause') {
              self.playCurrentClause();
            } else {
              self.playSentenceMode(0);
            }
            return;
          }

          // 其他场景（生词、汉字、英文翻译、日文翻译等）保持原生播放
          self.stopAudio();
          return originalPlayClip.apply(this, arguments);
        };
      }

      // 如果页面打开就在 story 屏，立即同步一次
      const currentIdx = typeof window.storyIdx === 'number' ? window.storyIdx : 0;
      this.onSentenceChange(currentIdx);
    },

    hookExistingFullText: function() {
      const self = this;
      const originalRenderFull = window.renderFullText;
      if (typeof originalRenderFull === 'function') {
        window.renderFullText = function() {
          originalRenderFull.apply(this, arguments);
          self.enhanceFullTextList();
        };
      }
    },

    enhanceFullTextList: function() {
      if (!this.lessonData || !this.lessonData.sentences) return;
      const listEl = document.getElementById('fullTextList');
      if (!listEl) return;

      this.lessonData.sentences.forEach((sent, sIdx) => {
        const item = document.getElementById('full-sent-' + sIdx);
        if (!item) return;
        const zhEl = item.querySelector('.sentence-zh');
        if (!zhEl || zhEl.dataset.cpEnhanced) return;
        zhEl.dataset.cpEnhanced = 'true';

        let html = `${sIdx + 1}. `;
        (sent.clauses || []).forEach((c, cIdx) => {
          html += `<span class="full-clause-item" id="full-clause-${sIdx}-${cIdx}" title="点击精听该分句" onclick="event.stopPropagation(); ClausePlayer.playSingleClauseFromFull(${sIdx}, ${cIdx});">${c.zh}</span>`;
        });
        zhEl.innerHTML = html;
      });
    },

    playSingleClauseFromFull: function(sIdx, cIdx) {
      if (typeof window.stopFullPlay === 'function') window.stopFullPlay();
      this.currentSentIdx = sIdx;
      this.currentClauseIdx = cIdx;

      document.querySelectorAll('.full-clause-item').forEach(el => el.classList.remove('playing-clause'));
      const activeEl = document.getElementById(`full-clause-${sIdx}-${cIdx}`);
      if (activeEl) activeEl.classList.add('playing-clause');

      const sent = this.lessonData.sentences[sIdx];
      const clause = sent && sent.clauses ? sent.clauses[cIdx] : null;
      if (!clause) return;

      this.playAudioUrl(clause.audioUrl, clause.zh, () => {
        if (activeEl) activeEl.classList.remove('playing-clause');
      });
    },

    getCurrentSent: function() {
      if (!this.lessonData || !this.lessonData.sentences) return null;
      return this.lessonData.sentences[this.currentSentIdx] || null;
    },

    getCurrentClause: function() {
      const sent = this.getCurrentSent();
      if (!sent || !sent.clauses) return null;
      return sent.clauses[this.currentClauseIdx] || null;
    },

    onSentenceChange: function(sIdx) {
      this.stopAudio();
      this.currentSentIdx = sIdx;
      this.currentClauseIdx = 0;
      this.renderClauseView();
    },

    renderClauseView: function() {
      const sent = this.getCurrentSent();
      if (!sent) return;

      // 1. 渲染分句药丸胶囊
      const pillsList = document.getElementById('cpPillsList');
      if (pillsList) {
        pillsList.innerHTML = '';
        (sent.clauses || []).forEach((c, idx) => {
          const pill = document.createElement('div');
          pill.className = `clause-pill ${idx === this.currentClauseIdx ? 'active' : ''}`;
          pill.id = `cp-pill-${idx}`;
          pill.innerHTML = `
            <span>${c.zh}</span>
            <span class="pill-speaker-ico">🔊</span>
          `;
          pill.onclick = () => {
            if (this.granularityMode === 'original') {
              this.seekOriginalTo(c.sentOffsetStart);
            } else {
              this.selectClause(idx, true);
            }
          };
          pillsList.appendChild(pill);
        });
      }

      // 2. 渲染进度条上的分句吸附锚点 (Clause Markers)
      const track = document.getElementById('cpScrubTrack');
      if (track) {
        track.querySelectorAll('.clause-tick-mark').forEach(el => el.remove());
        (sent.clauses || []).forEach((c, idx) => {
          const marker = document.createElement('div');
          marker.className = 'clause-tick-mark';
          const percent = (c.sentOffsetStart / (sent.duration || 1)) * 100;
          marker.style.left = percent + '%';
          marker.title = `跳转到分句: ${c.zh} (${this.formatSec(c.sentOffsetStart)})`;
          marker.onclick = (e) => {
            e.stopPropagation();
            if (this.granularityMode === 'original') {
              this.seekOriginalTo(c.sentOffsetStart);
              this.updateStatusText(`跳转至原声分句：${c.zh}`);
            } else if (this.granularityMode === 'clause') {
              this.selectClause(idx, true);
            } else {
              this.playSentenceMode(idx);
            }
          };
          track.appendChild(marker);
        });
      }

      this.updateFocusCard();
      this.updateVisibilityForMode();
      this.updateScrubUI(0, sent.duration);
      this.updateStatusText('就绪');
    },

    updateFocusCard: function() {
      const sent = this.getCurrentSent();
      const clause = this.getCurrentClause();
      if (!sent || !clause) return;

      const numEl = document.getElementById('cpFocusNum');
      const pyEl = document.getElementById('cpFocusPy');
      const zhEl = document.getElementById('cpFocusZh');
      const enEl = document.getElementById('cpFocusEn');
      const jpEl = document.getElementById('cpFocusJp');

      if (numEl) numEl.textContent = `分句 ${this.currentClauseIdx + 1} / ${sent.clauses.length}`;
      if (pyEl) {
        pyEl.textContent = clause.py || '';
        pyEl.style.display = (window.showPy !== false) ? 'block' : 'none';
      }
      if (zhEl) zhEl.textContent = clause.zh || '';
      if (enEl) {
        enEl.textContent = clause.en || '';
        enEl.style.display = (window.showEn !== false && clause.en) ? 'block' : 'none';
      }
      if (jpEl) {
        jpEl.textContent = clause.jp || '';
        jpEl.style.display = (window.showJp !== false && clause.jp) ? 'block' : 'none';
      }
    },

    updateVisibilityForMode: function() {
      const storyScreen = document.getElementById('screen-story');
      const origZh = storyScreen ? storyScreen.querySelector('#storyZh') : null;
      const origPy = storyScreen ? storyScreen.querySelector('#storyPy') : null;
      const origEnRow = document.getElementById('storyEnRow');
      const origJpRow = document.getElementById('storyJpRow');
      const pillsContainer = document.getElementById('cpPillsContainer');
      const focusCard = document.getElementById('cpFocusCard');

      if (this.granularityMode === 'original') {
        // 原声整句模式：显示整句大字和译文，隐藏分句药丸和聚焦卡片
        if (origZh) origZh.style.display = 'block';
        if (origPy) origPy.style.display = (window.showPy !== false) ? 'block' : 'none';
        if (origEnRow) origEnRow.style.display = (window.showEn !== false) ? 'flex' : 'none';
        if (origJpRow) origJpRow.style.display = (window.showJp !== false) ? 'flex' : 'none';
        if (focusCard) focusCard.style.display = 'none';
        if (pillsContainer) pillsContainer.style.display = 'none';
      } else if (this.granularityMode === 'clause') {
        // 逗号分句细读模式：隐藏整句大字，展示分句胶囊和聚焦卡片
        if (origZh) origZh.style.display = 'none';
        if (origPy) origPy.style.display = 'none';
        if (origEnRow) origEnRow.style.display = 'none';
        if (origJpRow) origJpRow.style.display = 'none';
        if (focusCard) focusCard.style.display = 'flex';
        if (pillsContainer) pillsContainer.style.display = 'flex';
      } else {
        // 整句连续听模式：保留整句大字与分句胶囊，胶囊随音频同步高亮
        if (origZh) origZh.style.display = 'block';
        if (origPy) origPy.style.display = (window.showPy !== false) ? 'block' : 'none';
        if (origEnRow) origEnRow.style.display = (window.showEn !== false) ? 'flex' : 'none';
        if (origJpRow) origJpRow.style.display = (window.showJp !== false) ? 'flex' : 'none';
        if (focusCard) focusCard.style.display = 'none';
        if (pillsContainer) pillsContainer.style.display = 'flex';
      }
      this.updateLoopBtnUI();
    },

    updateHighlightUI: function() {
      const sent = this.getCurrentSent();
      if (!sent) return;
      (sent.clauses || []).forEach((c, idx) => {
        const pill = document.getElementById(`cp-pill-${idx}`);
        if (pill) pill.classList.toggle('active', idx === this.currentClauseIdx);
      });
    },

    selectClause: function(cIdx, triggerPlay) {
      this.currentClauseIdx = cIdx;
      this.updateHighlightUI();
      this.updateFocusCard();

      const sent = this.getCurrentSent();
      const clause = this.getCurrentClause();
      if (sent && clause) {
        this.updateScrubUI(clause.sentOffsetStart, sent.duration);
      }

      if (triggerPlay) {
        if (this.granularityMode === 'clause') {
          this.playCurrentClause();
        } else if (this.granularityMode === 'original') {
          this.seekOriginalTo(clause ? clause.sentOffsetStart : 0);
        } else {
          this.playSentenceMode(cIdx);
        }
      }
    },

    setMode: function(mode) {
      this.stopAudio();
      this.granularityMode = mode;
      try {
        localStorage.setItem('cp_playback_mode', mode);
      } catch (e) {}

      const btnOriginal = document.getElementById('cpBtnModeOriginal');
      const btnClause = document.getElementById('cpBtnModeClause');
      const btnSentence = document.getElementById('cpBtnModeSentence');
      if (btnOriginal) btnOriginal.classList.toggle('active', mode === 'original');
      if (btnClause) btnClause.classList.toggle('active', mode === 'clause');
      if (btnSentence) btnSentence.classList.toggle('active', mode === 'sentence');

      this.updateVisibilityForMode();
      this.updateFocusCard();

      if (mode === 'original') {
        this.updateStatusText('原来整句播放模式 (自然流畅)');
        this.playOriginalSentence();
      } else if (mode === 'clause') {
        this.updateStatusText('逗号分句细读模式');
        this.playCurrentClause();
      } else {
        this.updateStatusText('整句连续听模式 (分句停顿跟读)');
        this.playSentenceMode(0);
      }
    },

    togglePlay: function() {
      if (this.isPlaying) {
        this.stopAudio();
        this.updateStatusText('已暂停');
      } else {
        if (this.granularityMode === 'original') {
          this.playOriginalSentence();
        } else if (this.granularityMode === 'clause') {
          this.playCurrentClause();
        } else {
          this.playSentenceMode(this.currentClauseIdx);
        }
      }
    },

    /**
     * 模式 1：播放原版整句音频（无分句切片停顿）
     */
    playOriginalSentence: function(startTimeOffset) {
      this.stopAudio();
      this.isPlaying = true;
      this.updatePlayBtnUI();

      const sent = this.getCurrentSent();
      if (!sent) return;

      const sentId = sent.sentId || ('st' + (this.currentSentIdx + 1));
      const origAudioUrl = 'audio/' + this.lessonKey + '/' + sentId + '.mp3';
      const text = sent.sentZh || sent.zh || '';
      this.updateStatusText(`正在播放原整句：${text}`);

      const self = this;
      const audio = new Audio(origAudioUrl);
      this.activeAudio = audio;
      audio.playbackRate = this.playbackRate;

      let estDuration = sent.duration || 5.0;

      audio.onloadedmetadata = function() {
        if (audio.duration && !isNaN(audio.duration) && audio.duration > 0) {
          estDuration = audio.duration;
        }
        if (typeof startTimeOffset === 'number' && startTimeOffset > 0 && startTimeOffset < estDuration) {
          try { audio.currentTime = startTimeOffset; } catch(e) {}
        }
        self.updateScrubUI(audio.currentTime, estDuration);
      };

      function tickProgress() {
        if (!self.isPlaying || !self.activeAudio) return;
        const cur = self.activeAudio.currentTime || 0;
        const dur = (self.activeAudio.duration && !isNaN(self.activeAudio.duration) && self.activeAudio.duration > 0)
          ? self.activeAudio.duration : estDuration;
        self.updateScrubUI(cur, dur);

        // 联动分句索引
        const clauses = sent.clauses || [];
        for (let i = 0; i < clauses.length; i++) {
          if (cur >= clauses[i].sentOffsetStart && cur <= clauses[i].sentOffsetEnd) {
            if (self.currentClauseIdx !== i) {
              self.currentClauseIdx = i;
              self.updateHighlightUI();
            }
            break;
          }
        }
        self.animFrameId = requestAnimationFrame(tickProgress);
      }

      audio.onplay = function() {
        self.animFrameId = requestAnimationFrame(tickProgress);
      };

      let finished = false;
      const done = function() {
        if (finished) return;
        finished = true;
        self.stopAudio();
        if (self.isLooping && self.granularityMode === 'original') {
          setTimeout(function() {
            if (self.isLooping && self.granularityMode === 'original') {
              self.playOriginalSentence();
            }
          }, 400);
        } else {
          self.updateStatusText('原整句播放完毕 (可重听或点击下一句)');
        }
      };

      audio.onended = done;

      audio.onerror = function() {
        console.warn('[ClausePlayer] 原整句音频缺失，使用 TTS 兜底:', origAudioUrl);
        self.activeAudio = null;
        self.speakFallback(text, done);
      };

      audio.play().catch(function(err) {
        console.warn('[ClausePlayer] 播放失败，尝试降级:', err);
        self.activeAudio = null;
        self.speakFallback(text, done);
      });
    },

    seekOriginalTo: function(timeInSec) {
      const sent = this.getCurrentSent();
      if (!sent) return;
      const dur = (this.activeAudio && !isNaN(this.activeAudio.duration) && this.activeAudio.duration > 0)
        ? this.activeAudio.duration : (sent.duration || 5.0);
      const clampedTime = Math.max(0, Math.min(timeInSec, dur));

      if (this.activeAudio) {
        try { this.activeAudio.currentTime = clampedTime; } catch(e) {}
        this.updateScrubUI(clampedTime, dur);
        if (!this.isPlaying) {
          this.activeAudio.play().then(() => {
            this.isPlaying = true;
            this.updatePlayBtnUI();
          }).catch(() => {});
        }
      } else {
        this.playOriginalSentence(clampedTime);
      }
    },

    /**
     * 模式 2：播放当前选中的逗号分句
     */
    playCurrentClause: function() {
      const sent = this.getCurrentSent();
      const clause = this.getCurrentClause();
      if (!sent || !clause) return;

      this.updateStatusText(`正在朗读：${clause.zh}`);
      this.playClauseStep(clause, () => {
        if (this.isLooping && this.granularityMode === 'clause') {
          setTimeout(() => {
            if (this.isLooping && this.granularityMode === 'clause') {
              this.playCurrentClause();
            }
          }, 350);
        } else {
          this.updateStatusText('朗读完毕 (可重读或点下一句)');
        }
      });
    },

    /**
     * 模式 3：整句连续听 (分句停顿带跟读)
     */
    playSentenceMode: function(startCIdx) {
      const sent = this.getCurrentSent();
      if (!sent || !sent.clauses) return;
      let cIdx = typeof startCIdx === 'number' ? startCIdx : 0;
      if (cIdx >= sent.clauses.length) cIdx = 0;

      this.stopAudio();
      this.isPlaying = true;
      this.updatePlayBtnUI();

      const self = this;
      function step() {
        if (!self.isPlaying) return;
        if (cIdx >= sent.clauses.length) {
          self.stopAudio();
          if (self.isLooping && self.granularityMode === 'sentence') {
            setTimeout(() => {
              if (self.isLooping && self.granularityMode === 'sentence') {
                self.playSentenceMode(0);
              }
            }, 500);
          } else {
            self.updateStatusText('整句连续朗读完毕 🎉');
          }
          return;
        }
        self.selectClause(cIdx, false);
        const clause = sent.clauses[cIdx];
        self.updateStatusText(`正在连续朗读 (${cIdx + 1}/${sent.clauses.length})：${clause.zh}`);
        self.playClauseStep(clause, () => {
          cIdx++;
          setTimeout(step, 200);
        });
      }

      step();
    },

    playClauseStep: function(clause, onEnded) {
      this.stopAudio();
      this.isPlaying = true;
      this.updatePlayBtnUI();

      const sent = this.getCurrentSent();
      const startTime = Date.now();
      const durSec = (clause.duration || 2.0) / this.playbackRate;

      const self = this;
      function tickProgress() {
        if (!self.isPlaying) return;
        const elapsed = self.activeAudio ? self.activeAudio.currentTime : (Date.now() - startTime) / 1000;
        const ratioInClause = Math.min(elapsed / (clause.duration || 1), 1.0);
        const sentTime = clause.sentOffsetStart + (ratioInClause * clause.duration);

        self.updateScrubUI(sentTime, sent ? sent.duration : 1.0);

        if (elapsed < durSec + 0.1) {
          self.animFrameId = requestAnimationFrame(tickProgress);
        }
      }

      this.playAudioUrl(clause.audioUrl, clause.zh, () => {
        self.isPlaying = false;
        self.updatePlayBtnUI();
        if (onEnded) onEnded();
      }, () => {
        self.animFrameId = requestAnimationFrame(tickProgress);
      });
    },

    playAudioUrl: function(url, fallbackText, onEnded, onStarted) {
      if (this.activeAudio) {
        this.activeAudio.pause();
        this.activeAudio = null;
      }

      const audio = new Audio(url);
      this.activeAudio = audio;
      audio.playbackRate = this.playbackRate;

      let finished = false;
      const done = () => {
        if (finished) return;
        finished = true;
        this.activeAudio = null;
        if (onEnded) onEnded();
      };

      audio.onplay = () => {
        if (onStarted) onStarted();
      };

      audio.onended = done;

      audio.onerror = () => {
        console.warn('[ClausePlayer] 音频文件缺失，降级至 Web Speech:', url);
        this.activeAudio = null;
        this.speakFallback(fallbackText, done);
      };

      audio.play().catch(err => {
        console.warn('[ClausePlayer] 自动播放阻止或失败，降级:', err);
        this.activeAudio = null;
        this.speakFallback(fallbackText, done);
      });
    },

    speakFallback: function(text, onEnd) {
      if (!('speechSynthesis' in window)) {
        if (onEnd) onEnd();
        return;
      }
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'zh-CN';
      u.rate = this.playbackRate * 0.9;
      u.onend = () => { if (onEnd) onEnd(); };
      u.onerror = () => { if (onEnd) onEnd(); };
      window.speechSynthesis.speak(u);
    },

    stopAudio: function() {
      if (this.activeAudio) {
        this.activeAudio.pause();
        this.activeAudio.onended = null;
        this.activeAudio.onerror = null;
        this.activeAudio = null;
      }
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      if (this.animFrameId) {
        cancelAnimationFrame(this.animFrameId);
        this.animFrameId = null;
      }
      this.isPlaying = false;
      this.updatePlayBtnUI();
    },

    prev: function() {
      this.stopAudio();
      if (this.granularityMode === 'original') {
        if (typeof window.storyPrev === 'function') window.storyPrev();
      } else if (this.granularityMode === 'clause') {
        if (this.currentClauseIdx > 0) {
          this.selectClause(this.currentClauseIdx - 1, true);
        } else if (typeof window.storyPrev === 'function') {
          window.storyPrev();
        }
      } else {
        if (this.currentClauseIdx > 0) {
          this.playSentenceMode(this.currentClauseIdx - 1);
        } else if (typeof window.storyPrev === 'function') {
          window.storyPrev();
        }
      }
    },

    next: function() {
      this.stopAudio();
      const sent = this.getCurrentSent();
      if (this.granularityMode === 'original') {
        if (typeof window.storyNext === 'function') window.storyNext();
      } else if (this.granularityMode === 'clause') {
        if (sent && this.currentClauseIdx < sent.clauses.length - 1) {
          this.selectClause(this.currentClauseIdx + 1, true);
        } else if (typeof window.storyNext === 'function') {
          window.storyNext();
        }
      } else {
        if (sent && this.currentClauseIdx < sent.clauses.length - 1) {
          this.playSentenceMode(this.currentClauseIdx + 1);
        } else if (typeof window.storyNext === 'function') {
          window.storyNext();
        }
      }
    },

    prevClause: function() { this.prev(); },
    nextClause: function() { this.next(); },

    toggleLoop: function() {
      this.isLooping = !this.isLooping;
      this.updateLoopBtnUI();
    },

    updateLoopBtnUI: function() {
      const btn = document.getElementById('cpLoopBtn');
      if (!btn) return;
      btn.classList.toggle('active-loop', this.isLooping);
      if (this.granularityMode === 'original') {
        btn.textContent = this.isLooping ? '🔁 循环整句中' : '🔁 循环当前句';
      } else if (this.granularityMode === 'clause') {
        btn.textContent = this.isLooping ? '🔁 循环分句中' : '🔁 循环当前句';
      } else {
        btn.textContent = this.isLooping ? '🔁 循环连续听中' : '🔁 循环连续听';
      }
    },

    toggleRate: function() {
      if (this.playbackRate === 1.0) this.playbackRate = 0.8;
      else if (this.playbackRate === 0.8) this.playbackRate = 1.2;
      else this.playbackRate = 1.0;

      const btn = document.getElementById('cpRateBtn');
      if (btn) btn.textContent = `⚡ ${this.playbackRate}x`;
      if (this.activeAudio) this.activeAudio.playbackRate = this.playbackRate;
    },

    updatePlayBtnUI: function() {
      const btn = document.getElementById('cpPlayBtn');
      if (btn) btn.textContent = this.isPlaying ? '⏸️' : '▶️';
    },

    updateStatusText: function(txt) {
      const el = document.getElementById('cpStatusTxt');
      if (el) el.textContent = txt;
    },

    updateScrubUI: function(currentTime, duration) {
      duration = duration || 1;
      const percent = Math.min((currentTime / duration) * 100, 100);
      const fill = document.getElementById('cpScrubFill');
      const thumb = document.getElementById('cpScrubThumb');
      const timer = document.getElementById('cpTimerTxt');

      if (fill) fill.style.width = percent + '%';
      if (thumb) thumb.style.left = percent + '%';
      if (timer) timer.textContent = `${this.formatSec(currentTime)} / ${this.formatSec(duration)}`;
    },

    formatSec: function(s) {
      s = Math.max(0, s || 0);
      const mins = Math.floor(s / 60);
      const secs = (s % 60).toFixed(1);
      return `${mins < 10 ? '0' : ''}${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }
  };

  // 挂载到全局
  window.ClausePlayer = ClausePlayer;

  // DOM 准备好后自动加载
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ClausePlayer.init());
  } else {
    ClausePlayer.init();
  }

})(window);
