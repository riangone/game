/*
 * 本周挑战（Weekly Challenge）
 * - 按 ISO 周（周一开始）轮换挑战游戏和目标分，所有访客看到的题目相同。
 * - 成绩只保存在本机 localStorage，不上传、不做线上排行榜。
 * 用法：游戏结束时调用 WeeklyChallenge.record('<游戏 id>', score)。
 */
(function (global) {
  'use strict';

  // 轮换顺序：每周换一款游戏；同一款游戏每轮换一次，目标分依次提高。
  var GAMES = [
    { id: 'jj9',          file: 'jj9.html',          icon: '🦘', targets: [30, 50, 80],
      zh: '跳跳方块', ja: 'ジャンプ＆ジャンプ', unitZh: '分', unitJa: '点' },
    { id: 'snake',        file: 'snake.html',        icon: '🐍', targets: [200, 400, 600],
      zh: '霓虹贪吃蛇', ja: 'ネオンスネーク', unitZh: '分', unitJa: '点' },
    { id: 'stacktower',   file: 'stacktower.html',   icon: '🏢', targets: [20, 35, 50],
      zh: '层叠高塔', ja: 'スタックタワー', unitZh: '分', unitJa: '点' },
    { id: 'towerdefense', file: 'towerdefense.html', icon: '🏰', targets: [800, 1500, 2500],
      zh: '元素塔防', ja: 'エレメンタルTD', unitZh: '分（单关）', unitJa: '点（1ステージ）' }
  ];

  var PREFIX = 'wc_best_';

  // ISO 8601 周：返回 { year, week, monday(Date, 本地时间) }
  function isoWeek(d) {
    var date = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    var day = (date.getDay() + 6) % 7; // 周一 = 0
    var monday = new Date(date); monday.setDate(date.getDate() - day);
    var thursday = new Date(monday); thursday.setDate(monday.getDate() + 3);
    var year = thursday.getFullYear();
    var jan4 = new Date(year, 0, 4);
    var jan4Monday = new Date(jan4); jan4Monday.setDate(jan4.getDate() - (jan4.getDay() + 6) % 7);
    var week = 1 + Math.round((monday - jan4Monday) / 604800000);
    return { year: year, week: week, monday: monday };
  }

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function current(now) {
    var w = isoWeek(now || new Date());
    // 以 2024-01-01（周一）为起点的周序号，保证跨年连续轮换
    var epoch = new Date(2024, 0, 1);
    var n = Math.round((w.monday - epoch) / 604800000);
    var g = GAMES[((n % GAMES.length) + GAMES.length) % GAMES.length];
    var round = Math.floor(n / GAMES.length);
    var target = g.targets[((round % g.targets.length) + g.targets.length) % g.targets.length];
    var sunday = new Date(w.monday); sunday.setDate(w.monday.getDate() + 6);
    return {
      key: w.year + '-W' + pad(w.week),
      year: w.year, week: w.week,
      start: w.monday, end: sunday,
      game: g, target: target
    };
  }

  function storageKey(c, gameId) { return PREFIX + c.key + '_' + gameId; }

  function getBest(c) {
    c = c || current();
    try { return parseInt(localStorage.getItem(storageKey(c, c.game.id)) || '0', 10) || 0; }
    catch (e) { return 0; }
  }

  // 只有本周挑战的那款游戏会记分；返回 { best, isNew, done } 或 null
  function record(gameId, score) {
    var c = current();
    if (gameId !== c.game.id) return null;
    score = parseInt(score, 10) || 0;
    var best = getBest(c);
    var isNew = score > best;
    if (isNew) {
      try {
        localStorage.setItem(storageKey(c, gameId), String(score));
        cleanup(c);
      } catch (e) {}
      best = score;
    }
    return { best: best, isNew: isNew, done: best >= c.target, target: c.target };
  }

  // 清掉 8 周以前的旧记录，避免 localStorage 越积越多
  function cleanup(c) {
    var keep = {};
    var d = new Date(c.start);
    for (var i = 0; i < 8; i++) {
      var w = isoWeek(d);
      keep[w.year + '-W' + pad(w.week)] = true;
      d.setDate(d.getDate() - 7);
    }
    for (var j = localStorage.length - 1; j >= 0; j--) {
      var k = localStorage.key(j);
      if (k && k.indexOf(PREFIX) === 0 && !keep[k.slice(PREFIX.length, PREFIX.length + 8)]) {
        localStorage.removeItem(k);
      }
    }
  }

  global.WeeklyChallenge = { current: current, getBest: getBest, record: record, isoWeek: isoWeek, GAMES: GAMES };
})(window);
