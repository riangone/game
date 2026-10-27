// srs-storage.js - 间隔复习 (Leitner 4-box) 与本地存储状态管理
class SrsStorage {
  constructor() {
    this.STORAGE_KEY = 'chugaku2_learning_state_v1';
    this.state = this.loadState();
  }

  loadState() {
    try {
      const raw = localStorage.getItem(this.STORAGE_KEY);
      if (raw) {
        return JSON.parse(raw);
      }
    } catch (e) {
      console.warn('Failed to parse local storage state:', e);
    }

    return {
      totalStars: 0,
      xp: 0,
      unitProgress: {}, // unitId -> { completedModes: [], starsEarned: 0 }
      srsItems: {},     // itemId -> { box: 1..4, lastReviewed: timestamp, nextReview: timestamp, streak: 0, misses: 0, term, desc, subject }
      weaknesses: []    // [{ id, question, answer, explanation, subject, unitId, type, timestamp }]
    };
  }

  save() {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.state));
    } catch (e) {
      console.error('Failed to save state to localStorage:', e);
    }
  }

  getTotalStars() {
    return this.state.totalStars || 0;
  }

  addStars(count = 1) {
    this.state.totalStars = (this.state.totalStars || 0) + count;
    this.state.xp = (this.state.xp || 0) + count * 15;
    this.save();
    return this.state.totalStars;
  }

  // 记录模式通关与单元评星
  recordModeComplete(unitId, modeKey, stars = 1) {
    if (!this.state.unitProgress[unitId]) {
      this.state.unitProgress[unitId] = { completedModes: [], starsEarned: 0 };
    }
    const up = this.state.unitProgress[unitId];
    if (!up.completedModes.includes(modeKey)) {
      up.completedModes.push(modeKey);
      this.addStars(stars);
    }
    this.save();
  }

  // Leitner 间隔记忆处理
  // Box 1: 1天 | Box 2: 3天 | Box 3: 7天 | Box 4: 14天+ (Mastered)
  recordSrsResult(item, isSuccess) {
    const id = item.id || (item.term ? item.term : (item.q ? item.q.slice(0, 20) : 'item_' + Date.now()));
    const now = Date.now();
    const intervals = [
      1 * 24 * 60 * 60 * 1000,  // Box 1 -> 1 day
      3 * 24 * 60 * 60 * 1000,  // Box 2 -> 3 days
      7 * 24 * 60 * 60 * 1000,  // Box 3 -> 7 days
      14 * 24 * 60 * 60 * 1000  // Box 4 -> 14 days
    ];

    if (!this.state.srsItems[id]) {
      this.state.srsItems[id] = {
        box: 1,
        lastReviewed: now,
        nextReview: now + intervals[0],
        streak: 0,
        misses: 0,
        term: item.term || item.q,
        desc: item.desc || item.a,
        subject: item.subject || 'general'
      };
    }

    const cur = this.state.srsItems[id];
    cur.lastReviewed = now;

    if (isSuccess) {
      cur.streak = (cur.streak || 0) + 1;
      cur.box = Math.min(4, (cur.box || 1) + 1);
    } else {
      cur.streak = 0;
      cur.misses = (cur.misses || 0) + 1;
      cur.box = 1; // 错误降回 Box 1
      this.recordWeakness(item);
    }

    cur.nextReview = now + intervals[cur.box - 1];
    this.save();
    return cur;
  }

  // 记录弱点/错题
  recordWeakness(item) {
    const id = item.id || (item.term || item.q || 'err_' + Date.now());
    // 查重：避免重复添加过多同题
    const exists = this.state.weaknesses.find(w => w.id === id);
    if (!exists) {
      this.state.weaknesses.unshift({
        id: id,
        question: item.q || item.term || item.question || '',
        answer: item.a || item.desc || item.answer || '',
        explanation: item.explanation || item.hint || '',
        subject: item.subject || 'general',
        timestamp: Date.now()
      });
      // 最多保留 100 条错题
      if (this.state.weaknesses.length > 100) {
        this.state.weaknesses.pop();
      }
      this.save();
    }
  }

  // 移除错题 (复习达标后)
  resolveWeakness(id) {
    this.state.weaknesses = this.state.weaknesses.filter(w => w.id !== id);
    this.save();
  }

  // 获取各 Box 统计与待复习列表
  getSrsStats() {
    const now = Date.now();
    const stats = { box1: 0, box2: 0, box3: 0, box4: 0, dueCount: 0, dueItems: [] };

    for (const id in this.state.srsItems) {
      const item = this.state.srsItems[id];
      const box = item.box || 1;
      if (stats['box' + box] !== undefined) {
        stats['box' + box]++;
      }
      if (item.nextReview <= now) {
        stats.dueCount++;
        stats.dueItems.push(item);
      }
    }

    return stats;
  }

  getWeaknesses() {
    return this.state.weaknesses || [];
  }
}

window.srsStorage = new SrsStorage();
