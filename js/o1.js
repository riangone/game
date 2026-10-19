/* o1.js — 0101.click 本地进度（2026-10-20）
 * 只存在你的浏览器里：一个名为 o1 的 cookie，Domain=.0101.click，这样主页能读到各子域名上的进度。
 * 不发送到任何统计服务；服务器不读取它。
 *   l: {zh|ja|ko: [url, 标题, 时间戳]}  最近学的课
 *   d: [YYYYMMDD...]                    学习过的日子（在课文页停留满 60 秒算一天，保留 60 天）
 *   t: [[file, 标题]...]                 最近用过的工具（8 个）
 *   q: [YYYYMMDD...]                    完成每日数独的日子（保留 60 天）
 * 用法：<script src="js/o1.js" data-o1="lesson"></script>（课文页）
 *       data-o1="tool"（工具页，由 pwa-register.js 自动加载）
 */
(function () {
  'use strict';
  var NAME = 'o1';
  function today(off) {
    var d = new Date(Date.now() - (off || 0) * 86400000);
    return d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
  }
  function get() {
    var m = document.cookie.match(/(?:^|;\s*)o1=([^;]*)/);
    if (!m) return {};
    try { return JSON.parse(decodeURIComponent(m[1])) || {}; } catch (e) { return {}; }
  }
  function set(o) {
    var v = encodeURIComponent(JSON.stringify(o));
    var dom = /(^|\.)0101\.click$/.test(location.hostname) ? '; domain=.0101.click' : '';
    document.cookie = NAME + '=' + v + '; path=/; max-age=34560000; samesite=lax' + dom +
      (location.protocol === 'https:' ? '; secure' : '');
  }
  function addDay(key) {
    var o = get(), a = o[key] || [], t = today();
    if (a[a.length - 1] !== t) { a.push(t); o[key] = a.slice(-60); set(o); }
  }
  // 连续天数：从今天（或昨天，今天还没学时）往回数
  function streak(a) {
    a = a || [];
    if (!a.length) return 0;
    var set_ = {}, i, n = 0;
    for (i = 0; i < a.length; i++) set_[a[i]] = 1;
    var start = set_[today()] ? 0 : (set_[today(1)] ? 1 : -1);
    if (start < 0) return 0;
    while (set_[today(start + n)]) n++;
    return n;
  }
  function shortTitle() {
    var t = (document.title || '').split(/\s[-–|·]\s/)[0].trim();
    return t.length > 18 ? t.slice(0, 18) + '…' : t;
  }
  function langOf(path) {
    if (/\/(nihongo|kana|nhg-)/.test(path)) return 'ja';
    if (/\/(hangugeo|hangeul|korean|kr-)/.test(path)) return 'ko';
    return 'zh';
  }
  function lesson() {
    var o = get(), l = o.l || {}, path = location.pathname;
    l[langOf(path)] = [location.origin + path, shortTitle(), Date.now()];
    o.l = l; set(o);
    // 页面可见累计 60 秒才算「今天学过」
    var acc = 0, last = Date.now(), done = false;
    var timer = setInterval(function () {
      var now = Date.now();
      if (document.visibilityState === 'visible') acc += now - last;
      last = now;
      if (!done && acc >= 60000) { done = true; addDay('d'); clearInterval(timer); }
    }, 5000);
  }
  function tool() {
    var file = location.pathname.split('/').pop() || 'tools.html';
    if (file === 'tools.html' || file === 'index.html') return;
    var o = get(), a = (o.t || []).filter(function (x) { return x[0] !== file; });
    a.unshift([file, shortTitle()]);
    o.t = a.slice(0, 8); set(o);
  }
  window.O1 = { get: get, set: set, today: today, streak: streak, addDay: addDay, lesson: lesson, tool: tool };
  var me = document.currentScript, mode = me && me.getAttribute('data-o1');
  if (mode === 'lesson') lesson();
  else if (mode === 'tool') tool();
})();
