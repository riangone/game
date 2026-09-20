/**
 * voice-recorder.js
 * 纯前端高保真课文朗读录音与 IndexedDB 本地持久化留存组件
 * 支持：MediaRecorder 原生音频捕获、Blob 二进制存储、双轨试听、音频导出与离线秒开
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

class AppVoiceManager {
  constructor() {
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.currentId = null;
    this.startTime = 0;
    this.activePlayer = null;
    this.stream = null;
  }

  isRecording() {
    return this.mediaRecorder && this.mediaRecorder.state === 'recording';
  }

  async startRecord(id, onStart, onFinish, onError) {
    if (this.isRecording()) {
      await this.stopRecord();
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

      this.mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) this.audioChunks.push(e.data);
      };

      this.mediaRecorder.onstop = async () => {
        const blob = new Blob(this.audioChunks, { type: mimeType });
        const duration = Math.round((Date.now() - this.startTime) / 1000);
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
      console.error('Audio capture failed:', err);
      if (onError) onError(err);
      else alert('无法启动麦克风录音，请确认浏览器允许访问麦克风！\n' + err.message);
    }
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
        resolve();
      }
    });
  }

  async playRecord(id, onStart, onEnd) {
    const rec = await getVoiceBlob(id);
    if (!rec || !rec.blob) {
      alert('此句尚未录音，请先点击麦克风按钮录制！');
      return;
    }
    if (this.activePlayer) {
      this.activePlayer.pause();
      this.activePlayer = null;
    }
    const url = URL.createObjectURL(rec.blob);
    this.activePlayer = new Audio(url);
    this.activePlayer.onended = () => {
      URL.revokeObjectURL(url);
      this.activePlayer = null;
      if (onEnd) onEnd();
    };
    if (onStart) onStart();
    this.activePlayer.play();
  }

  async downloadRecord(id, filename) {
    const rec = await getVoiceBlob(id);
    if (!rec || !rec.blob) return;
    const url = URL.createObjectURL(rec.blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || `${id}.webm`;
    a.click();
    URL.revokeObjectURL(url);
  }
}

// Global voice manager instance
window.voiceManager = new AppVoiceManager();
