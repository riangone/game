/**
 * voice-recorder.js
 * 纯前端高保真课文朗读录音与 IndexedDB 本地持久化留存组件
 * 
 * 核心特性：
 * 1. 原生 MediaRecorder 音频捕获管线，支持多种主流音频容器 (webm / mp4 / ogg)
 * 2. Web Audio API AnalyserNode 实时音量分析与声波频率频谱采样
 * 3. IndexedDB (ChineseLearningVoiceDB) 异步二进制持久化存储，离线可用、永不丢失
 * 4. 实时声波涟漪 (Dynamic Soundwave) 与计时器
 * 5. 全文连贯配音 (Sequential Dubbing Playback) 引擎
 * 6. 一键导出/下载本地音频文件
 * 7. 声音勋章与录音完成度统计感知
 */

const VOICE_DB_NAME = 'ChineseLearningVoiceDB';
const VOICE_STORE_NAME = 'recordings';
let _voiceDB = null;

function openVoiceDB() {
  return new Promise((resolve) => {
    if (!window.indexedDB) {
      console.warn('IndexedDB not supported in this browser.');
      resolve(null);
      return;
    }
    if (_voiceDB) {
      resolve(_voiceDB);
      return;
    }
    const req = indexedDB.open(VOICE_DB_NAME, 1);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(VOICE_STORE_NAME)) {
        db.createObjectStore(VOICE_STORE_NAME, { keyPath: 'id' });
      }
    };
    req.onsuccess = () => {
      _voiceDB = req.result;
      resolve(_voiceDB);
    };
    req.onerror = () => {
      console.error('Failed to open Voice IndexedDB:', req.error);
      resolve(null);
    };
  });
}

async function saveVoiceBlob(id, blob, duration) {
  const db = await openVoiceDB();
  if (!db) return;
  return new Promise((resolve, reject) => {
    const tx = db.transaction(VOICE_STORE_NAME, 'readwrite');
    const store = tx.objectStore(VOICE_STORE_NAME);
    store.put({ id, blob, duration, timestamp: Date.now() });
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function getVoiceBlob(id) {
  const db = await openVoiceDB();
  if (!db) return null;
  return new Promise((resolve) => {
    const tx = db.transaction(VOICE_STORE_NAME, 'readonly');
    const store = tx.objectStore(VOICE_STORE_NAME);
    const req = store.get(id);
    req.onsuccess = () => resolve(req.result || null);
    req.onerror = () => resolve(null);
  });
}

async function deleteVoiceBlob(id) {
  const db = await openVoiceDB();
  if (!db) return;
  return new Promise((resolve, reject) => {
    const tx = db.transaction(VOICE_STORE_NAME, 'readwrite');
    const store = tx.objectStore(VOICE_STORE_NAME);
    store.delete(id);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function getAllVoiceKeys() {
  const db = await openVoiceDB();
  if (!db) return [];
  return new Promise((resolve) => {
    const tx = db.transaction(VOICE_STORE_NAME, 'readonly');
    const store = tx.objectStore(VOICE_STORE_NAME);
    const req = store.getAllKeys();
    req.onsuccess = () => resolve(req.result || []);
    req.onerror = () => resolve([]);
  });
}

async function getVoiceStats(prefix, totalCount) {
  const keys = await getAllVoiceKeys();
  const matched = keys.filter(k => typeof k === 'string' && k.startsWith(prefix));
  return {
    recorded: matched.length,
    total: totalCount,
    percent: totalCount > 0 ? Math.round((matched.length / totalCount) * 100) : 0,
    isComplete: totalCount > 0 && matched.length >= totalCount,
    keys: matched
  };
}

class AppVoiceManager {
  constructor() {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.currentId = null;
    this.startTime = 0;
    this.activePlayer = null;
    this.stream = null;
    this.audioContext = null;
    this.analyser = null;
    this.animFrameId = null;
    this.timerInterval = null;
    this.currentLevel = 0;
    this.isSequentialPlaying = false;
    this.sequentialCancel = false;
    this.onVolumeChange = null;
    this.onTimerTick = null;
  }

  isRecording() {
    return !!(this.mediaRecorder && this.mediaRecorder.state === 'recording');
  }

  async startRecord(id, arg2, arg3, arg4) {
    if (this.isRecording()) {
      await this.stopRecord();
    }

    let onStart, onFinish, onError, onVolume, onTimer;
    if (typeof arg2 === 'object' && arg2 !== null) {
      onStart = arg2.onStart;
      onFinish = arg2.onFinish;
      onError = arg2.onError;
      onVolume = arg2.onVolume;
      onTimer = arg2.onTimer;
    } else {
      onStart = arg2;
      onFinish = arg3;
      onError = arg4;
    }

    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      let mimeType = 'audio/webm';
      if (!MediaRecorder.isTypeSupported('audio/webm')) {
        if (MediaRecorder.isTypeSupported('audio/mp4')) mimeType = 'audio/mp4';
        else if (MediaRecorder.isTypeSupported('audio/ogg')) mimeType = 'audio/ogg';
      }
      this.mediaRecorder = new MediaRecorder(this.stream, { mimeType });
      this.audioChunks = [];
      this.currentId = id;
      this.startTime = Date.now();

      // Web Audio API AnalyserNode 初始化
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) {
          this.audioContext = new AudioCtx();
          if (this.audioContext.state === 'suspended') {
            await this.audioContext.resume();
          }
          const source = this.audioContext.createMediaStreamSource(this.stream);
          this.analyser = this.audioContext.createAnalyser();
          this.analyser.fftSize = 64;
          this.analyser.smoothingTimeConstant = 0.6;
          source.connect(this.analyser);

          const freqBins = new Uint8Array(this.analyser.frequencyBinCount);
          const updateAudioMeter = () => {
            if (!this.isRecording()) return;
            this.analyser.getByteFrequencyData(freqBins);
            let sum = 0;
            for (let i = 0; i < freqBins.length; i++) sum += freqBins[i];
            const avg = sum / freqBins.length;
            const level = Math.min(1, avg / 120);
            this.currentLevel = level;
            if (onVolume) onVolume(level, freqBins);
            if (this.onVolumeChange) this.onVolumeChange(level, freqBins);
            this.animFrameId = requestAnimationFrame(updateAudioMeter);
          };
          this.animFrameId = requestAnimationFrame(updateAudioMeter);
        }
      } catch (audioCtxErr) {
        console.warn('AudioContext / AnalyserNode init skipped:', audioCtxErr);
      }

      // 计时器
      this.timerInterval = setInterval(() => {
        const elapsedSec = Math.round((Date.now() - this.startTime) / 1000);
        const mins = String(Math.floor(elapsedSec / 60)).padStart(2, '0');
        const secs = String(elapsedSec % 60).padStart(2, '0');
        const formatted = `${mins}:${secs}`;
        if (onTimer) onTimer(formatted, elapsedSec);
        if (this.onTimerTick) this.onTimerTick(formatted, elapsedSec);
      }, 300);

      this.mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) this.audioChunks.push(e.data);
      };

      this.mediaRecorder.onstop = async () => {
        this.cleanupAudioContext();
        const blob = new Blob(this.audioChunks, { type: mimeType });
        const duration = Math.max(1, Math.round((Date.now() - this.startTime) / 1000));
        await saveVoiceBlob(id, blob, duration);
        if (this.stream) {
          this.stream.getTracks().forEach(t => t.stop());
          this.stream = null;
        }
        this.mediaRecorder = null;
        this.currentId = null;
        if (onFinish) onFinish(blob, duration);
      };

      this.mediaRecorder.start(200);
      if (onStart) onStart();
    } catch (err) {
      this.cleanupAudioContext();
      console.error('Audio capture failed:', err);
      if (onError) onError(err);
      else alert('无法启动麦克风录音，请确认浏览器允许访问麦克风！\n' + err.message);
    }
  }

  cleanupAudioContext() {
    if (this.animFrameId) {
      cancelAnimationFrame(this.animFrameId);
      this.animFrameId = null;
    }
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
    if (this.audioContext) {
      try { this.audioContext.close(); } catch(e){}
      this.audioContext = null;
      this.analyser = null;
    }
    this.currentLevel = 0;
  }

  stopRecord() {
    return new Promise((resolve) => {
      if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
        const origOnStop = this.mediaRecorder.onstop;
        this.mediaRecorder.onstop = async (e) => {
          if (origOnStop) await origOnStop(e);
          resolve();
        };
        this.mediaRecorder.stop();
      } else {
        this.cleanupAudioContext();
        resolve();
      }
    });
  }

  async playRecord(id, onStart, onEnd) {
    const rec = await getVoiceBlob(id);
    if (!rec || !rec.blob) {
      if (onEnd) onEnd();
      return null;
    }
    this.stopPlay();
    const url = URL.createObjectURL(rec.blob);
    const audio = new Audio(url);
    this.activePlayer = audio;
    let finished = false;
    const finish = () => {
      if (finished) return;
      finished = true;
      URL.revokeObjectURL(url);
      if (this.activePlayer === audio) this.activePlayer = null;
      if (onEnd) onEnd();
    };
    audio.onended = finish;
    audio.onerror = finish;
    if (onStart) onStart();
    await audio.play();
    return audio;
  }

  stopPlay() {
    if (this.activePlayer) {
      try {
        this.activePlayer.pause();
        this.activePlayer.currentTime = 0;
      } catch(e){}
      this.activePlayer = null;
    }
  }

  async downloadRecord(id, filename) {
    const rec = await getVoiceBlob(id);
    if (!rec || !rec.blob) return;
    const url = URL.createObjectURL(rec.blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || `${id}.webm`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  /**
   * 全文连贯配音播放引擎
   * @param {Array} items 课文句子列表 [{ voiceId, fallbackId, text }]
   * @param {Object} options 回调配置
   */
  async playSequential(items, options = {}) {
    this.stopSequential();
    this.isSequentialPlaying = true;
    this.sequentialCancel = false;

    for (let i = 0; i < items.length; i++) {
      if (this.sequentialCancel) break;
      const item = items[i];
      const vId = typeof item === 'object' ? item.voiceId : item;
      const rec = await getVoiceBlob(vId);
      const hasMyVoice = !!(rec && rec.blob);

      if (options.onStepStart) {
        options.onStepStart(i, item, hasMyVoice);
      }

      await new Promise((resolve) => {
        if (this.sequentialCancel) { resolve(); return; }
        if (hasMyVoice) {
          this.playRecord(vId, null, () => resolve());
        } else if (typeof options.fallbackPlay === 'function') {
          options.fallbackPlay(i, item, () => resolve());
        } else {
          setTimeout(resolve, 1200);
        }
      });

      if (options.onStepEnd) {
        options.onStepEnd(i, item);
      }
      if (!this.sequentialCancel && i < items.length - 1) {
        await new Promise(r => setTimeout(r, 350));
      }
    }

    const wasCancelled = this.sequentialCancel;
    this.isSequentialPlaying = false;
    this.sequentialCancel = false;
    if (!wasCancelled && options.onFinish) {
      options.onFinish();
    }
  }

  stopSequential() {
    if (this.isSequentialPlaying) {
      this.sequentialCancel = true;
      this.isSequentialPlaying = false;
      this.stopPlay();
    }
  }
}

// Global voice manager instance
window.voiceManager = new AppVoiceManager();
