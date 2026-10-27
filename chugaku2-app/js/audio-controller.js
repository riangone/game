// audio-controller.js - Web Audio 音效合成器 + Edge-TTS 神经网络原声 + Web Speech API 智能回退
class AudioController {
  constructor() {
    this.ctx = null;
    this.enabled = true;
    this.speechSynthesis = window.speechSynthesis || null;
    this.cachedVoices = [];
    this.currentClip = null;
    this.audioCache = {};

    if (this.speechSynthesis) {
      this.initVoices();
      if (this.speechSynthesis.onvoiceschanged !== undefined) {
        this.speechSynthesis.onvoiceschanged = () => this.initVoices();
      }
      // 部分浏览器（如 Chrome/Edge/Safari）首次 getVoices() 是异步的，定时轮询确保发音人列表就绪
      let attempts = 0;
      const pollTimer = setInterval(() => {
        this.initVoices();
        attempts++;
        if ((this.cachedVoices && this.cachedVoices.length > 0) || attempts > 20) {
          clearInterval(pollTimer);
        }
      }, 200);
    }
  }

  // 懒加载初始化 AudioContext（需要用户手势触发）
  getAudioContext() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
    return this.ctx;
  }

  initVoices() {
    if (!this.speechSynthesis) return;
    this.cachedVoices = this.speechSynthesis.getVoices();
  }

  // 正确音效 (上升双和弦)
  playCorrect() {
    if (!this.enabled) return;
    const ctx = this.getAudioContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc1 = ctx.createOscillator();
    const osc2 = ctx.createOscillator();
    const gain = ctx.createGain();

    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(523.25, now); // C5
    osc1.frequency.exponentialRampToValueAtTime(659.25, now + 0.12); // E5

    osc2.type = 'triangle';
    osc2.frequency.setValueAtTime(659.25, now); // E5
    osc2.frequency.exponentialRampToValueAtTime(783.99, now + 0.12); // G5

    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(ctx.destination);

    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + 0.35);
    osc2.stop(now + 0.35);
  }

  // 错误音效 (低音双沉降音)
  playWrong() {
    if (!this.enabled) return;
    const ctx = this.getAudioContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(220, now); // A3
    osc.frequency.linearRampToValueAtTime(146.83, now + 0.25); // D3

    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + 0.28);
  }

  // 点击/翻牌音效
  playFlip() {
    if (!this.enabled) return;
    const ctx = this.getAudioContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(800, now);
    osc.frequency.exponentialRampToValueAtTime(400, now + 0.05);

    gain.gain.setValueAtTime(0.12, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + 0.05);
  }

  // 过关/结算胜利音效 (三音阶欢庆)
  playFanfare() {
    if (!this.enabled) return;
    const ctx = this.getAudioContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
    notes.forEach((freq, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const startTime = now + i * 0.1;
      const duration = (i === notes.length - 1) ? 0.4 : 0.12;

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, startTime);

      gain.gain.setValueAtTime(0.18, startTime);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(startTime);
      osc.stop(startTime + duration);
    });
  }

  // 星星增加音效
  playStar() {
    if (!this.enabled) return;
    const ctx = this.getAudioContext();
    if (!ctx) return;

    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(987.77, now); // B5
    osc.frequency.exponentialRampToValueAtTime(1318.51, now + 0.15); // E6

    gain.gain.setValueAtTime(0.15, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + 0.2);
  }

  // 停止所有正在播放的音频与 TTS
  stopAll() {
    if (this.currentClip) {
      try {
        this.currentClip.pause();
        this.currentClip.currentTime = 0;
      } catch (e) {}
      this.currentClip = null;
    }
    if (this.speechSynthesis) {
      try {
        this.speechSynthesis.cancel();
      } catch (e) {}
    }
  }

  stopSpeak() {
    this.stopAll();
  }

  // 优先播放由 Edge-TTS 预生成的神经网络 MP3 原声音频，缺失时无缝降级到浏览器高质量语音合成
  playClip(unitId, itemId, fallbackText, lang = 'ja-JP', onEnd = null) {
    if (!this.enabled) return;
    this.stopAll();

    // 自动修正语言：如果文本包含日文字符，强制使用 ja-JP
    if (fallbackText && /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]/.test(fallbackText)) {
      lang = 'ja-JP';
    }

    if (!unitId || !itemId) {
      this.speak(fallbackText, lang, onEnd);
      return;
    }

    const key = `${unitId}/${itemId}`;
    // 兼容 /chugaku2-app/ 根路径与相对路径，确保在不同 URL 结构（末尾有无斜杠）下均能正确定位 MP3
    let basePath = 'audio/';
    if (typeof window !== 'undefined' && window.location) {
      if (window.location.protocol !== 'file:' && window.location.pathname.includes('chugaku2-app')) {
        basePath = '/chugaku2-app/audio/';
      }
    }
    const audioPath = `${basePath}${unitId}/${itemId}.mp3`;
    let a = this.audioCache[key];
    if (!a) {
      a = new Audio(audioPath);
      this.audioCache[key] = a;
    }
    a.currentTime = 0;

    let done = false;
    const finish = () => {
      if (done) return;
      done = true;
      if (this.currentClip === a) this.currentClip = null;
      if (onEnd) onEnd();
    };

    a.onended = finish;
    a.onerror = () => {
      if (done) return;
      done = true;
      if (this.currentClip === a) this.currentClip = null;
      // 降级使用 Edge/浏览器合成语音
      this.speak(fallbackText, lang, onEnd);
    };

    this.currentClip = a;
    const p = a.play();
    if (p && typeof p.catch === 'function') {
      p.catch(() => {
        if (done) return;
        done = true;
        if (this.currentClip === a) this.currentClip = null;
        this.speak(fallbackText, lang, onEnd);
      });
    }
  }

  cleanMathForSpeech(text, lang = 'ja-JP') {
    let t = text || '';
    t = t.replace(/\\text\{([^{}]+)\}/g, '$1');
    while (t.includes('\\frac')) {
      const next = t.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, lang === 'ja-JP' ? '$2分の$1' : '$1 over $2');
      if (next === t) break;
      t = next;
    }
    t = t.replace(/\\to/g, lang === 'ja-JP' ? ' 矢印 ' : ' to ');
    t = t.replace(/\\equiv/g, lang === 'ja-JP' ? ' 合同 ' : ' congruent ');
    t = t.replace(/\\times/g, lang === 'ja-JP' ? ' かける ' : ' times ');
    t = t.replace(/\\triangle/g, lang === 'ja-JP' ? '三角形' : 'triangle');
    t = t.replace(/\\angle/g, lang === 'ja-JP' ? '角' : 'angle');
    t = t.replace(/\\pm/g, lang === 'ja-JP' ? 'プラスマイナス' : 'plus minus');
    t = t.replace(/([a-zA-Z0-9])\s*>\s*([a-zA-Z0-9])/g, lang === 'ja-JP' ? '$1 大なり $2' : '$1 greater than $2');
    t = t.replace(/([a-zA-Z0-9])\s*<\s*([a-zA-Z0-9])/g, lang === 'ja-JP' ? '$1 小なり $2' : '$1 less than $2');
    t = t.replace(/\$/g, '');
    return t.replace(/\s+/g, ' ').trim();
  }

  getBestVoice(lang) {
    if (!this.cachedVoices || this.cachedVoices.length === 0) {
      if (this.speechSynthesis) this.cachedVoices = this.speechSynthesis.getVoices();
    }
    if (!this.cachedVoices || this.cachedVoices.length === 0) return null;

    const target = (lang || 'ja-JP').toLowerCase();
    const langPrefix = target.slice(0, 2);
    const langVoices = this.cachedVoices.filter(v => (v.lang || '').toLowerCase().replace('_', '-').startsWith(langPrefix));
    if (langVoices.length === 0) return null;

    // 优先选择 Microsoft Edge Online / Natural / Neural 语音，避免默认的粗糙机械音
    const naturalVoice = langVoices.find(v => {
      const name = (v.name || '').toLowerCase();
      return name.includes('natural') || name.includes('neural') || name.includes('online') ||
             name.includes('nanami') || name.includes('keita') || name.includes('jenny') || name.includes('guy');
    });
    if (naturalVoice) return naturalVoice;

    // 其次选择 Google 或高音质语音
    const googleVoice = langVoices.find(v => (v.name || '').toLowerCase().includes('google'));
    if (googleVoice) return googleVoice;

    // 排除明确标有 Desktop / SAPI 机械音的语音（如果有其他可选）
    const nonDesktop = langVoices.find(v => !(v.name || '').toLowerCase().includes('desktop'));
    return nonDesktop || langVoices[0];
  }

  // 语音合成朗读（回退通路）
  speak(text, lang = 'ja-JP', onEnd = null) {
    if (!this.speechSynthesis || !text) return;
    this.speechSynthesis.cancel();

    // 检查是否包含日语汉字/假名，若是则强制日语音频
    if (/[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]/.test(text)) {
      lang = 'ja-JP';
    }

    const cleanText = this.cleanMathForSpeech(text, lang);
    if (!cleanText) return;

    const utter = new SpeechSynthesisUtterance(cleanText);
    utter.lang = lang;
    utter.rate = (lang === 'en-US') ? 0.92 : 1.0;
    utter.pitch = 1.0;

    const bestVoice = this.getBestVoice(lang);
    if (bestVoice) {
      utter.voice = bestVoice;
    }

    if (onEnd) {
      utter.onend = onEnd;
      utter.onerror = onEnd;
    }

    this.speechSynthesis.speak(utter);
  }
}

window.audioCtrl = new AudioController();
