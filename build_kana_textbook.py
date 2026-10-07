# -*- coding: utf-8 -*-
"""
Generator for kana.html - The Official Japanese Kana Textbook (课文教材体系)
Pure textbook design: systematic curriculum, zero arcade gimmicks, zero locks.
"""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-Y1P7PMMM6V"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-Y1P7PMMM6V');
    </script>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>五十音与假名基础 - 日语课文教材 (Japanese Kana Textbook)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&family=Outfit:wght@500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  :root {
    --jp-red: #b91c1c;
    --jp-red-dark: #881337;
    --jp-red-soft: #fff1f2;
    --jp-navy: #1e3a8a;
    --jp-navy-soft: #eff6ff;
    --jp-gold: #d97706;
    --jp-gold-soft: #fef3c7;
    --jp-green: #059669;
    --jp-green-soft: #ecfdf5;
    --ink: #1e293b;
    --ink-sub: #475569;
    --muted: #64748b;
    --paper: #fcfbf7;
    --card: #ffffff;
    --border: #e2e8f0;
    --border-warm: #fed7aa;
    --radius-lg: 16px;
    --radius-md: 12px;
    --radius-sm: 8px;
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 6px 18px rgba(30, 41, 59, 0.08);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }

  html, body {
    width: 100%;
    min-height: 100%;
    background-color: var(--paper);
    color: var(--ink);
    font-family: "M PLUS Rounded 1c", system-ui, -apple-system, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }

  body {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 60px;
  }

  /* Sticky Textbook Header */
  .textbook-header {
    width: 100%;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(8px);
    border-bottom: 1.5px solid var(--border-warm);
    position: sticky;
    top: 0;
    z-index: 100;
    padding: 10px 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.03);
  }
  .header-inner {
    max-width: 960px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
  .back-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: #fff;
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--ink);
    text-decoration: none;
    font-size: 13px;
    font-weight: 700;
    transition: all .2s;
  }
  .back-btn:hover { background: var(--jp-red-soft); border-color: var(--jp-red); color: var(--jp-red); }
  .book-brand {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .book-badge {
    font-size: 10px;
    font-weight: 800;
    color: var(--jp-red);
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .book-title {
    font-size: 16px;
    font-weight: 900;
    color: var(--ink);
  }
  .header-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 700;
    color: var(--muted);
  }
  .progress-tag {
    background: var(--jp-gold-soft);
    color: var(--jp-gold);
    padding: 3px 8px;
    border-radius: 999px;
    border: 1px solid rgba(217, 119, 6, 0.2);
  }

  /* Textbook Major Tab Navigation */
  .textbook-tabs {
    width: 100%;
    max-width: 960px;
    margin: 16px auto 8px;
    padding: 0 16px;
    display: flex;
    gap: 8px;
    border-bottom: 2px solid var(--border);
    overflow-x: auto;
  }
  .tab-btn {
    padding: 8px 16px;
    border: none;
    background: none;
    font-size: 14px;
    font-weight: 800;
    color: var(--muted);
    cursor: pointer;
    position: relative;
    white-space: nowrap;
    transition: color .2s;
  }
  .tab-btn:hover { color: var(--jp-red); }
  .tab-btn.active {
    color: var(--jp-red);
  }
  .tab-btn.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--jp-red);
    border-radius: 3px 3px 0 0;
  }

  /* Main Textbook Container */
  main {
    width: 100%;
    max-width: 960px;
    padding: 12px 16px;
  }

  /* SECTION 1: UNIT SYLLABUS BAR */
  .unit-nav-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 10px 12px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
  }
  .unit-nav-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 12px;
    font-weight: 800;
    color: var(--ink-sub);
  }
  .unit-pills {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 4px;
    -webkit-overflow-scrolling: touch;
  }
  .unit-pill {
    flex-shrink: 0;
    padding: 6px 14px;
    border-radius: var(--radius-sm);
    border: 1.5px solid var(--border);
    background: var(--paper);
    color: var(--ink);
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all .15s ease;
  }
  .unit-pill:hover { border-color: var(--jp-red); color: var(--jp-red); }
  .unit-pill.active {
    background: var(--jp-red);
    color: #fff;
    border-color: var(--jp-red);
    box-shadow: 0 2px 6px rgba(185, 28, 28, 0.25);
  }
  .unit-pill.learned::after {
    content: '✓';
    font-size: 11px;
    color: var(--jp-green);
    background: #fff;
    border-radius: 50%;
    width: 14px;
    height: 14px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
  }
  .unit-pill.active.learned::after {
    color: var(--jp-red);
  }

  /* Unit Content Header */
  .unit-head-card {
    background: var(--card);
    border: 1.5px solid var(--border-warm);
    border-radius: var(--radius-lg);
    padding: 20px 24px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-sm);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
  }
  .unit-head-info {
    flex: 1;
    min-width: 260px;
  }
  .unit-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 800;
    background: var(--jp-red-soft);
    color: var(--jp-red);
    padding: 3px 10px;
    border-radius: 999px;
    margin-bottom: 6px;
  }
  .unit-title-row {
    display: flex;
    align-items: baseline;
    gap: 12px;
    flex-wrap: wrap;
  }
  .unit-title {
    font-size: 24px;
    font-weight: 900;
    color: var(--ink);
  }
  .unit-romaji {
    font-size: 15px;
    font-family: 'Outfit', sans-serif;
    color: var(--jp-navy);
    font-weight: 700;
  }
  .unit-desc {
    font-size: 13px;
    color: var(--ink-sub);
    margin-top: 6px;
    line-height: 1.5;
  }
  .unit-head-actions {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .read-row-btn {
    border: none;
    background: var(--jp-gold);
    color: #fff;
    padding: 8px 16px;
    border-radius: var(--radius-sm);
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 2px 6px rgba(217, 119, 6, 0.25);
    transition: transform .1s, background-color .2s;
  }
  .read-row-btn:hover { background: #b45309; }
  .read-row-btn:active { transform: translateY(1px); }

  .mark-read-toggle {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 700;
    color: var(--ink-sub);
    cursor: pointer;
    user-select: none;
    padding: 6px 10px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: var(--paper);
  }
  .mark-read-toggle input { cursor: pointer; }

  /* SECTION BLOCK */
  .section-block {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 22px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-sm);
  }
  .section-title-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    border-bottom: 1.5px solid var(--border);
    padding-bottom: 10px;
  }
  .section-title {
    font-size: 17px;
    font-weight: 900;
    color: var(--ink);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .section-title::before {
    content: '';
    width: 4px;
    height: 18px;
    background: var(--jp-red);
    border-radius: 2px;
  }
  .section-subtitle {
    font-size: 12px;
    color: var(--muted);
  }

  /* 1. KANA CARDS GRID */
  .kana-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px;
  }
  .kana-card {
    background: var(--paper);
    border: 1.5px solid var(--border-warm);
    border-radius: var(--radius-md);
    padding: 16px 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 6px;
    position: relative;
    cursor: pointer;
    transition: all .2s ease;
  }
  .kana-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--jp-red);
  }
  .kana-card:active { transform: translateY(0); }
  .kana-card.playing {
    border-color: var(--jp-red);
    background: var(--jp-red-soft);
    animation: kanaPulse 1s infinite alternate;
  }
  @keyframes kanaPulse {
    from { box-shadow: 0 0 0 2px rgba(185, 28, 28, 0.2); }
    to { box-shadow: 0 0 0 6px rgba(185, 28, 28, 0.4); }
  }
  .kana-main {
    font-size: 50px;
    font-weight: 900;
    color: var(--jp-red-dark);
    line-height: 1.1;
  }
  .kana-sub-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 800;
  }
  .kana-kata {
    color: var(--jp-gold);
    font-weight: 900;
    font-size: 18px;
  }
  .kana-romaji {
    font-family: 'Outfit', sans-serif;
    color: var(--jp-navy);
    font-weight: 800;
  }
  .kana-origin {
    font-size: 11px;
    font-weight: 700;
    color: var(--ink-sub);
    background: #fff;
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid var(--border);
  }
  .kana-hint {
    font-size: 11px;
    color: var(--muted);
    margin-top: 4px;
    line-height: 1.4;
  }
  .kana-play-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 50%;
    width: 26px;
    height: 26px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: var(--muted);
  }

  /* 2. TEXTBOOK VOCABULARY TABLE / CARDS */
  .vocab-intro-tip {
    font-size: 12px;
    color: var(--ink-sub);
    background: var(--jp-navy-soft);
    border-left: 3px solid var(--jp-navy);
    padding: 8px 12px;
    border-radius: 4px;
    margin-bottom: 14px;
  }
  .vocab-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 12px;
  }
  .vocab-card {
    background: var(--paper);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    transition: border-color .2s, box-shadow .2s;
  }
  .vocab-card:hover {
    border-color: var(--jp-gold);
    box-shadow: var(--shadow-sm);
  }
  .vocab-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .vocab-emoji {
    font-size: 30px;
    line-height: 1;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));
  }
  .vocab-text-box {
    display: flex;
    flex-direction: column;
  }
  .vocab-word {
    font-size: 20px;
    font-weight: 900;
    color: var(--ink);
    letter-spacing: 0.5px;
  }
  .vocab-romaji {
    font-size: 12px;
    font-family: 'Outfit', sans-serif;
    color: var(--jp-navy);
    font-weight: 700;
  }
  .vocab-meaning {
    font-size: 13px;
    color: var(--ink-sub);
    font-weight: 600;
  }
  .vocab-speak-btn {
    border: 1px solid var(--border);
    background: #fff;
    color: var(--jp-red);
    width: 38px;
    height: 38px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 15px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    transition: all .15s;
  }
  .vocab-speak-btn:hover { background: var(--jp-red-soft); border-color: var(--jp-red); transform: scale(1.05); }

  /* 3. SELF-ASSESSMENT EXERCISES (课后自测) */
  .exercise-subtabs {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }
  .subtab-btn {
    border: none;
    background: var(--paper);
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-size: 12px;
    font-weight: 800;
    color: var(--muted);
    cursor: pointer;
    transition: all .15s;
  }
  .subtab-btn.active {
    background: var(--jp-navy);
    color: #fff;
  }

  .exercise-pane { display: none; }
  .exercise-pane.active { display: block; }

  /* Exercise 1: Listening test */
  .listen-test-card {
    background: var(--paper);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
  }
  .listen-prompt {
    font-size: 14px;
    font-weight: 700;
    color: var(--ink-sub);
  }
  .listen-sound-btn {
    border: none;
    background: var(--jp-red);
    color: #fff;
    padding: 10px 22px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 800;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 3px 10px rgba(185, 28, 28, 0.25);
    transition: transform .1s;
  }
  .listen-sound-btn:active { transform: scale(0.97); }
  .listen-options {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
    max-width: 440px;
  }
  .listen-opt {
    flex: 1;
    min-width: 80px;
    padding: 14px 10px;
    background: #fff;
    border: 2px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: 26px;
    font-weight: 900;
    color: var(--ink);
    cursor: pointer;
    transition: all .15s;
  }
  .listen-opt:hover { border-color: var(--jp-navy); }
  .listen-opt.correct {
    border-color: var(--jp-green);
    background: var(--jp-green-soft);
    color: var(--jp-green);
  }
  .listen-opt.wrong {
    border-color: var(--jp-red);
    background: var(--jp-red-soft);
    color: var(--jp-red);
  }
  .listen-feedback {
    min-height: 24px;
    font-size: 13px;
    font-weight: 700;
  }

  /* Exercise 2: Spelling Builder */
  .spell-builder-card {
    background: var(--paper);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-md);
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
  }
  .spell-target-box {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .spell-slots {
    display: flex;
    gap: 10px;
    min-height: 52px;
    align-items: center;
    justify-content: center;
  }
  .spell-slot {
    width: 48px;
    height: 48px;
    border: 2px dashed var(--border);
    border-radius: 8px;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: 900;
    color: var(--jp-red);
    cursor: pointer;
  }
  .spell-slot.filled {
    border-style: solid;
    border-color: var(--jp-navy);
  }
  .spell-tiles {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    max-width: 400px;
  }
  .spell-tile {
    width: 42px;
    height: 42px;
    background: #fff;
    border: 2px solid var(--jp-gold);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 900;
    color: var(--ink);
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    transition: transform .1s;
  }
  .spell-tile:active { transform: translateY(2px); }
  .spell-tile.used {
    opacity: 0.3;
    pointer-events: none;
    border-color: var(--border);
  }
  .spell-actions {
    display: flex;
    gap: 10px;
    margin-top: 4px;
  }
  .btn-action {
    padding: 6px 14px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: #fff;
    font-size: 12px;
    font-weight: 700;
    color: var(--ink-sub);
    cursor: pointer;
  }
  .btn-action:hover { background: var(--paper); border-color: var(--muted); }

  /* Bottom Unit Pagination */
  .unit-pagination {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 20px;
  }
  .page-nav-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 18px;
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-md);
    color: var(--ink);
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
    text-decoration: none;
    transition: all .15s;
    box-shadow: var(--shadow-sm);
  }
  .page-nav-btn:hover { border-color: var(--jp-red); color: var(--jp-red); }

  /* OVERVIEW VIEW (全表) */
  .chart-section {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 22px;
    margin-bottom: 24px;
  }
  .chart-toggle-row {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
  }
  .chart-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 6px;
  }
  .chart-cell {
    background: var(--paper);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 6px;
    text-align: center;
    cursor: pointer;
    transition: all .15s;
  }
  .chart-cell:hover {
    border-color: var(--jp-red);
    background: var(--jp-red-soft);
    transform: translateY(-2px);
  }
  .chart-cell.empty {
    background: none;
    border: none;
    cursor: default;
  }
  .cell-kana { font-size: 24px; font-weight: 900; color: var(--jp-red-dark); line-height: 1.1; }
  .cell-sub { font-size: 11px; font-family: 'Outfit', sans-serif; color: var(--muted); font-weight: 700; }

  /* CONFUSABLE KANA (易混辨析) */
  .confusable-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
  }
  .confusable-card {
    background: var(--paper);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px;
  }
  .confusable-pair {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 12px;
  }
  .confusable-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  .confusable-char { font-size: 44px; font-weight: 900; color: var(--jp-red-dark); }
  .confusable-romaji { font-size: 13px; font-family: 'Outfit', sans-serif; color: var(--jp-navy); font-weight: 800; }
  .confusable-vs { font-size: 18px; font-weight: 900; color: var(--jp-gold); }
  .confusable-tip {
    font-size: 13px;
    color: var(--ink-sub);
    line-height: 1.5;
    background: #fff;
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
  }

  /* Toast */
  #textbookToast {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(30, 41, 59, 0.95);
    color: #fff;
    padding: 8px 18px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    pointer-events: none;
    z-index: 9999;
    opacity: 0;
    transition: opacity .2s;
  }

  @media (max-width: 600px) {
    .header-inner { flex-wrap: wrap; }
    .unit-head-card { flex-direction: column; align-items: flex-start; }
    .kana-main { font-size: 42px; }
  }
</style>
</head>
<body>

  <!-- Sticky Textbook Top Header -->
  <header class="textbook-header">
    <div class="header-inner">
      <a href="nhg-index.html" class="back-btn" title="返回课文目录">
        <span>📖</span>
        <span>课文目录</span>
      </a>
      <div class="book-brand">
        <span class="book-badge">Japanese Courseware · Foundation</span>
        <h1 class="book-title">《五十音与假名基础》</h1>
      </div>
      <div class="header-meta">
        <span class="progress-tag" id="statLearnedTag">已读 0 / 10 单元</span>
      </div>
    </div>
  </header>

  <!-- Textbook Major View Navigation Tabs -->
  <nav class="textbook-tabs">
    <button class="tab-btn active" id="tabMainUnits" onclick="switchMainView('units')">📚 十行系统精讲</button>
    <button class="tab-btn" id="tabIntro" onclick="switchMainView('intro')">📖 绪论：假名认知导学</button>
    <button class="tab-btn" id="tabChart" onclick="switchMainView('chart')">📊 五十音图全览</button>
    <button class="tab-btn" id="tabPairs" onclick="switchMainView('pairs')">🔍 易混假名辨析</button>
  </nav>

  <main id="mainContainer">
    <!-- View 1: 10 Units System (Default) -->
    <div id="viewUnits">
      <!-- Unit Syllabus Nav Pills -->
      <div class="unit-nav-wrap">
        <div class="unit-nav-header">
          <span>课文单元索引 (点击任意单元自由学习，无锁定)</span>
          <span style="color:var(--muted);font-weight:normal;">共 10 单元 · 46 清音 · 73 例词</span>
        </div>
        <div class="unit-pills" id="unitPillsContainer"></div>
      </div>

      <!-- Unit Detail Content -->
      <div id="unitContentWorkspace"></div>
    </div>

    <!-- View 2: Introduction -->
    <div id="viewIntro" style="display:none;">
      <div class="section-block">
        <div class="section-title-wrap">
          <h2 class="section-title">绪论：日语文字系统与五十音概论</h2>
          <span class="section-subtitle">入门认知指南</span>
        </div>
        <div style="font-size:14px;color:var(--ink-sub);line-height:1.8;display:flex;flex-direction:column;gap:14px;">
          <p>
            日语的现代书写体系由**平假名（ひらがな）**、**片假名（カタカナ）**和**汉字（漢字）**三者交融而成。初学者掌握五十音，即掌握了打开日语殿堂的第一把钥匙。
          </p>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:8px 0;">
            <div style="background:var(--paper);border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px;">
              <div style="font-weight:900;color:var(--jp-red);font-size:16px;">🌸 平假名 (ひらがな)</div>
              <div style="font-size:12px;color:var(--muted);margin-top:4px;">源自汉字草书。线条圆润流畅，用于书写日本固有词汇、动词活用词尾及语法助词（如：は、が、を）。</div>
            </div>
            <div style="background:var(--paper);border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px;">
              <div style="font-weight:900;color:var(--jp-navy);font-size:16px;">📐 片假名 (カタカナ)</div>
              <div style="font-size:12px;color:var(--muted);margin-top:4px;">源自汉字楷书的偏旁部首。笔画方正遒劲，主要用于外来语词汇（如：コーヒー/咖啡）、拟声拟态词及特别强调。</div>
            </div>
            <div style="background:var(--paper);border:1px solid var(--border);border-radius:var(--radius-sm);padding:14px;">
              <div style="font-weight:900;color:var(--jp-gold);font-size:16px;">🔤 罗马字 (Romaji)</div>
              <div style="font-size:12px;color:var(--muted);margin-top:4px;">拉丁字母注音，用于国际交流、招牌注音以及电脑和手机的日语键盘输入法（IME）。</div>
            </div>
          </div>
          <h3 style="font-size:16px;font-weight:900;color:var(--ink);margin-top:10px;">五十音图的矩阵构造（段与行）</h3>
          <p>
            五十音图并非杂乱无章的符号堆砌，而是一个严密的**二维发音矩阵**：
          </p>
          <ul style="padding-left:20px;line-height:1.7;">
            <li>**五段（母音）**：横向分为 <code>あ段 (a)</code>、<code>い段 (i)</code>、<code>う段 (u)</code>、<code>え段 (e)</code>、<code>お段 (o)</code>。母音是所有日语发音的底色。</li>
            <li>**十行（子音）**：纵向分为 <code>あ行</code>、<code>か行 (k)</code>、<code>さ行 (s)</code>、<code>た行 (t)</code>、<code>な行 (n)</code>、<code>は行 (h)</code>、<code>ま行 (m)</code>、<code>や行 (y)</code>、<code>ら行 (r)</code>、<code>わ行 (w)</code> 以及独立的拨音 <code>ん (n)</code>。</li>
          </ul>
          <div style="background:var(--jp-gold-soft);border:1px solid rgba(217,119,6,0.3);padding:12px 16px;border-radius:var(--radius-sm);margin-top:8px;">
            <strong>💡 教材推荐学法：受限拼读法</strong><br>
            不要枯燥地孤立死记字母。本教材每讲授一行，便提供完全由**已学假名**拼成的真实例词（如学完あ行即可拼出「あい/爱」、「いえ/家」；学到か行即可拼出「あか/红」、「あき/秋」）。在真实的音义绑定中，假名自然融会贯通。
          </div>
        </div>
      </div>
    </div>

    <!-- View 3: Complete Kana Chart -->
    <div id="viewChart" style="display:none;">
      <div class="chart-section">
        <div class="section-title-wrap">
          <h2 class="section-title">五十音图全息点读总表</h2>
          <span class="section-subtitle">点击任意假名即可聆听标准真人发音</span>
        </div>
        <div class="chart-toggle-row">
          <button class="btn-action active" id="btnChartHira" onclick="switchChartMode('hira')">平假名 (Hiragana)</button>
          <button class="btn-action" id="btnChartKata" onclick="switchChartMode('kata')">片假名 (Katakana)</button>
        </div>
        <div style="overflow-x:auto;">
          <table class="chart-table" id="chartTableMain"></table>
        </div>
      </div>
    </div>

    <!-- View 4: Confusable Minimal Pairs -->
    <div id="viewPairs" style="display:none;">
      <div class="section-block">
        <div class="section-title-wrap">
          <h2 class="section-title">易混假名专项辨析讲义</h2>
          <span class="section-subtitle">破解初学者形近、音近视觉盲区</span>
        </div>
        <div class="confusable-grid" id="confusableGridContainer"></div>
      </div>
    </div>
  </main>

  <div id="textbookToast"></div>

<script>
/* ==========================================================
   KANA TEXTBOOK DATA ARCHITECTURE (10 Units, 46 Kana, 73 Vocab)
   ========================================================== */
const KANA_UNITS = [
  {
    id: "unit_a",
    rowName: "あ行",
    unitNum: "第 1 单元",
    romaji: "a · i · u · e · o",
    title: "元音之源 · 纯净五母音",
    desc: "所有日语发音的基石母音。发音时嘴唇自然松弛，不夸张、不撅嘴，声调平稳自然。",
    kana: [
      {h:'あ', k:'ア', r:'a', origin:'安', hint:'安化为あ，大肚圆圆', note:'嘴张大如轻发“啊”，但比汉语口型微小'},
      {h:'い', k:'イ', r:'i', origin:'以', hint:'以字左半，两笔相依', note:'嘴角微向两侧咧，舌面自然上抬'},
      {h:'う', k:'ウ', r:'u', origin:'宇', hint:'宇冠弧线，短横轻勾', note:'★勿撅嘴！双唇扁平微拢，气流自然呼出'},
      {h:'え', k:'エ', r:'e', origin:'衣', hint:'衣字连笔，如元之姿', note:'口型介于i和a之间，舌前部稍抬起'},
      {h:'お', k:'オ', r:'o', origin:'於', hint:'於字左偏，十字加点', note:'嘴唇微圆但不突出，舌后部轻抬'}
    ],
    words: [
      {word:'あい', r:'ai', meaning:'爱 / 喜爱', emoji:'❤️'},
      {word:'あお', r:'ao', meaning:'蓝色', emoji:'🔷'},
      {word:'いえ', r:'ie', meaning:'家 / 房屋', emoji:'🏠'},
      {word:'うえ', r:'ue', meaning:'上面 / 向上', emoji:'⬆️'},
      {word:'いい', r:'ii', meaning:'好的 / 优秀的', emoji:'👍'},
      {word:'え', r:'e', meaning:'图画 / 绘画', emoji:'🎨'}
    ]
  },
  {
    id: "unit_ka",
    rowName: "か行",
    unitNum: "第 2 单元",
    romaji: "ka · ki · ku · ke · ko",
    title: "清脆送气 · k声带弹跳",
    desc: "舌根轻触软腭后迅速弹开送气，声调清澈欢快。与汉语k相似但送气较弱。",
    kana: [
      {h:'か', k:'カ', r:'ka', origin:'加', hint:'加字带力，右上一点', note:'舌根送气k配合元音a'},
      {h:'き', k:'キ', r:'ki', origin:'幾', hint:'几木成弦，两横贯穿', note:'k配合舌面上抬发i'},
      {h:'く', k:'ク', r:'ku', origin:'久', hint:'久之一角，如开口鸟', note:'双唇勿向前撅起'},
      {h:'け', k:'ケ', r:'ke', origin:'計', hint:'计字立人，右侧弯带', note:'清脆k配合元音e'},
      {h:'こ', k:'コ', r:'ko', origin:'己', hint:'己身微伏，上下两横', note:'双唇微呈小圆'}
    ],
    words: [
      {word:'あか', r:'aka', meaning:'红色', emoji:'🔴'},
      {word:'あき', r:'aki', meaning:'秋天', emoji:'🍁'},
      {word:'えき', r:'eki', meaning:'车站', emoji:'🚉'},
      {word:'いけ', r:'ike', meaning:'水池 / 池塘', emoji:'🏞️'},
      {word:'かお', r:'kao', meaning:'脸庞 / 容貌', emoji:'👤'},
      {word:'こえ', r:'koe', meaning:'声音 / 声响', emoji:'🗣️'},
      {word:'きく', r:'kiku', meaning:'听 / 菊花', emoji:'👂'},
      {word:'ここ', r:'koko', meaning:'这里', emoji:'📍'}
    ]
  },
  {
    id: "unit_sa",
    rowName: "さ行",
    unitNum: "第 3 单元",
    romaji: "sa · shi · su · se · so",
    title: "齿擦清响 · s春风拂叶",
    desc: "气流从齿缝掠出。特别注意“し”不是si，而是类似于xi/shi的清擦音。",
    kana: [
      {h:'さ', k:'サ', r:'sa', origin:'左', hint:'左之草书，弧光一掠', note:'齿缝轻擦送气'},
      {h:'し', k:'シ', r:'shi', origin:'之', hint:'之一落水，鱼钩微扬', note:'★非si！舌面隆起贴硬腭发[ɕi]，近汉语“西”'},
      {h:'す', k:'ス', r:'su', origin:'寸', hint:'寸带小圈，如卷小草', note:'嘴唇扁平不撅，微送摩擦气流'},
      {h:'せ', k:'セ', r:'se', origin:'世', hint:'世间连枝，右弯向外', note:'擦音s配合元音e'},
      {h:'そ', k:'ソ', r:'so', origin:'曽', hint:'曾之一笔，折角飞转', note:'微圆双唇，清脆短促'}
    ],
    words: [
      {word:'あさ', r:'asa', meaning:'早晨 / 清晨', emoji:'🌅'},
      {word:'かさ', r:'kasa', meaning:'雨伞', emoji:'☂️'},
      {word:'あし', r:'ashi', meaning:'脚 / 足部', emoji:'🦶'},
      {word:'すし', r:'sushi', meaning:'寿司', emoji:'🍣'},
      {word:'おかし', r:'okashi', meaning:'点心 / 零食', emoji:'🍘'},
      {word:'うそ', r:'uso', meaning:'谎言 / 玩笑', emoji:'🤭'},
      {word:'そこ', r:'soko', meaning:'那里', emoji:'👉'},
      {word:'いし', r:'ishi', meaning:'石头', emoji:'🪨'}
    ]
  },
  {
    id: "unit_ta",
    rowName: "た行",
    unitNum: "第 4 单元",
    romaji: "ta · chi · tsu · te · to",
    title: "齿龈弹击 · t的跳跃律动",
    desc: "舌尖轻碰上齿龈弹开。注意“ち”发chi(七)，“つ”发tsu(次)，切勿发成ti或tu。",
    kana: [
      {h:'た', k:'タ', r:'ta', origin:'太', hint:'太字连笔，十加小横', note:'舌尖抵上齿龈后弹开爆破'},
      {h:'ち', k:'チ', r:'chi', origin:'知', hint:'知草如5，圆弧外拓', note:'★非ti！塞擦音[tɕi]，近似汉语“七”'},
      {h:'つ', k:'ツ', r:'tsu', origin:'川', hint:'川水一波，浪花半弯', note:'★非tu！齿龈塞擦[tsɯ]，近似汉语“次”'},
      {h:'て', k:'テ', r:'te', origin:'天', hint:'天之一划，圆钩抱怀', note:'舌尖弹击上齿龈发te'},
      {h:'と', k:'ト', r:'to', origin:'止', hint:'止化为弧，一竖带兜', note:'双唇稍圆，送气短促'}
    ],
    words: [
      {word:'うた', r:'uta', meaning:'歌曲 / 唱歌', emoji:'🎵'},
      {word:'たこ', r:'tako', meaning:'章鱼 / 风筝', emoji:'🐙'},
      {word:'くち', r:'kuchi', meaning:'嘴巴 / 口部', emoji:'👄'},
      {word:'つくえ', r:'tsukue', meaning:'书桌 / 桌子', emoji:'🪑'},
      {word:'て', r:'te', meaning:'手', emoji:'✋'},
      {word:'とけい', r:'tokei', meaning:'时钟 / 手表', emoji:'⌚'},
      {word:'ちち', r:'chichi', meaning:'父亲 / 爸爸', emoji:'👨'},
      {word:'そと', r:'soto', meaning:'室外 / 外面', emoji:'🚪'}
    ]
  },
  {
    id: "unit_na",
    rowName: "な行",
    unitNum: "第 5 单元",
    romaji: "na · ni · nu · ne · no",
    title: "鼻腔柔共鸣 · n的温润音",
    desc: "舌尖贴紧上齿龈，气流从鼻腔流出形成温润柔和的共鸣。",
    kana: [
      {h:'な', k:'ナ', r:'na', origin:'奈', hint:'奈字右绕，小圈收尾', note:'鼻音n自然过渡到元音a'},
      {h:'に', k:'ニ', r:'ni', origin:'仁', hint:'仁立一边，右侧平列', note:'舌前部抬高贴硬腭'},
      {h:'ぬ', k:'ヌ', r:'nu', origin:'奴', hint:'奴身交错，尾端带环', note:'双唇微拢，鼻音轻柔'},
      {h:'ね', k:'ネ', r:'ne', origin:'祢', hint:'祢左垂竖，右挽小卷', note:'鼻音n与前元音e结合'},
      {h:'の', k:'ノ', r:'no', origin:'乃', hint:'乃如圆圈，一笔画就', note:'双唇微圆，平缓流出'}
    ],
    words: [
      {word:'いぬ', r:'inu', meaning:'小狗', emoji:'🐶'},
      {word:'ねこ', r:'neko', meaning:'小猫', emoji:'🐱'},
      {word:'なつ', r:'natsu', meaning:'夏天', emoji:'🌻'},
      {word:'さかな', r:'sakana', meaning:'鱼', emoji:'🐟'},
      {word:'きのこ', r:'kinoko', meaning:'蘑菇', emoji:'🍄'},
      {word:'なに', r:'nani', meaning:'什么', emoji:'❓'},
      {word:'にく', r:'niku', meaning:'肉 / 肉类', emoji:'🥩'}
    ]
  },
  {
    id: "unit_ha",
    rowName: "は行",
    unitNum: "第 6 单元",
    romaji: "ha · hi · fu · he · ho",
    title: "呼气如兰 · h的和雅之息",
    desc: "声门微启呼出气息。注意“ふ”绝不咬唇，而是双唇微拢自唇缝吹气。",
    kana: [
      {h:'は', k:'ハ', r:'ha', origin:'波', hint:'波之水旁，右有一圈', note:'声门微开呼气，平稳自然'},
      {h:'ひ', k:'ヒ', r:'hi', origin:'比', hint:'比做笑脸，两角上扬', note:'舌前部与硬腭摩擦送气'},
      {h:'ふ', k:'フ', r:'fu', origin:'不', hint:'不飞若星，中间一点', note:'★切勿咬唇！双唇微拢不触碰，自缝隙吹出[ɸɯ]'},
      {h:'へ', k:'ヘ', r:'he', origin:'部', hint:'部之房檐，一撇一捺', note:'平缓呼气配合元音e'},
      {h:'ほ', k:'ホ', r:'ho', origin:'保', hint:'保顶有帽，左竖右环', note:'微圆双唇，清澈呼气'}
    ],
    words: [
      {word:'はな', r:'hana', meaning:'花朵 / 鼻子', emoji:'🌸'},
      {word:'ひと', r:'hito', meaning:'人 / 人们', emoji:'🧑'},
      {word:'ほし', r:'hoshi', meaning:'星星', emoji:'⭐'},
      {word:'ふね', r:'fune', meaning:'轮船 / 小舟', emoji:'🚢'},
      {word:'ふく', r:'fuku', meaning:'衣服', emoji:'👕'},
      {word:'はは', r:'haha', meaning:'母亲 / 妈妈', emoji:'👩'},
      {word:'はし', r:'hashi', meaning:'筷子 / 桥', emoji:'🥢'}
    ]
  },
  {
    id: "unit_ma",
    rowName: "ま行",
    unitNum: "第 7 单元",
    romaji: "ma · mi · mu · me · mo",
    title: "双唇紧闭 · m的丰盈共振",
    desc: "双唇先闭合阻断气流，气流由鼻腔流出，随后双唇松开自然发音。",
    kana: [
      {h:'ま', k:'マ', r:'ma', origin:'末', hint:'末加两横，下画小圈', note:'闭唇鼻音瞬时开启配合a'},
      {h:'み', k:'ミ', r:'mi', origin:'美', hint:'美之一撇，斜横飞扬', note:'双唇鼻音配合高元音i'},
      {h:'む', k:'ム', r:'mu', origin:'武', hint:'武字右卷，头顶一点', note:'双唇微拢，鼻腔共振流出'},
      {h:'め', k:'メ', r:'me', origin:'女', hint:'女字交错，弧线平滑', note:'闭唇鼻音自然过渡到e'},
      {h:'も', k:'モ', r:'mo', origin:'毛', hint:'毛字三笔，横贯竖勾', note:'双唇微呈小圆，圆润饱满'}
    ],
    words: [
      {word:'あめ', r:'ame', meaning:'糖果 / 雨', emoji:'🍬'},
      {word:'みみ', r:'mimi', meaning:'耳朵', emoji:'👂'},
      {word:'め', r:'me', meaning:'眼睛', emoji:'👁️'},
      {word:'まち', r:'machi', meaning:'城镇 / 城市', emoji:'🏙️'},
      {word:'もも', r:'momo', meaning:'桃子', emoji:'🍑'},
      {word:'むし', r:'mushi', meaning:'昆虫', emoji:'🐛'},
      {word:'みち', r:'michi', meaning:'道路 / 街道', emoji:'🛣️'}
    ]
  },
  {
    id: "unit_ya",
    rowName: "や行",
    unitNum: "第 8 单元",
    romaji: "ya · (i) · yu · (e) · yo",
    title: "滑音流转 · y的半元音美感",
    desc: "舌面抬高，由高元音i快速滑向对应母音。现代日语中や行仅保留や、ゆ、よ三音。",
    kana: [
      {h:'や', k:'ヤ', r:'ya', origin:'也', hint:'也之一角，斜点相随', note:'由i快速滑向a'},
      {h:'ゆ', k:'ユ', r:'yu', origin:'由', hint:'由字曲折，竖线贯通', note:'由i快速滑向扁唇u'},
      {h:'よ', k:'ヨ', r:'yo', origin:'与', hint:'与上折转，下挽小环', note:'由i快速滑向圆唇o'}
    ],
    words: [
      {word:'やま', r:'yama', meaning:'大山', emoji:'⛰️'},
      {word:'ゆき', r:'yuki', meaning:'雪花 / 白雪', emoji:'❄️'},
      {word:'へや', r:'heya', meaning:'房间 / 屋子', emoji:'🛋️'},
      {word:'ゆめ', r:'yume', meaning:'梦想 / 梦境', emoji:'💭'},
      {word:'よむ', r:'yomu', meaning:'阅读 / 朗读', emoji:'📖'},
      {word:'おやつ', r:'oyatsu', meaning:'下午茶 / 零食点心', emoji:'🍰'}
    ]
  },
  {
    id: "unit_ra",
    rowName: "ら行",
    unitNum: "第 9 单元",
    romaji: "ra · ri · ru · re · ro",
    title: "舌尖轻弹 · r的飞扬闪音",
    desc: "★重点：绝非英语卷舌r！舌尖轻碰上齿龈一次即刻弹开，属于舌尖闪音（Flap）。",
    kana: [
      {h:'ら', k:'ラ', r:'ra', origin:'良', hint:'良之上点，下如小5', note:'舌尖快速轻弹齿龈发ra'},
      {h:'り', k:'リ', r:'ri', origin:'利', hint:'利刃两道，右竖带钩', note:'舌尖轻弹配合元音i'},
      {h:'る', k:'ル', r:'ru', origin:'留', hint:'留之回旋，尾端带圈', note:'舌尖轻弹配合扁唇u'},
      {h:'れ', k:'レ', r:'re', origin:'礼', hint:'礼之立身，右折展翅', note:'舌尖轻弹配合元音e'},
      {h:'ろ', k:'ロ', r:'ro', origin:'呂', hint:'吕如3字，尾无小圈', note:'舌尖轻弹配合圆唇o'}
    ],
    words: [
      {word:'そら', r:'sora', meaning:'天空', emoji:'⛅'},
      {word:'とり', r:'tori', meaning:'小鸟', emoji:'🐦'},
      {word:'さくら', r:'sakura', meaning:'樱花', emoji:'🌸'},
      {word:'しろ', r:'shiro', meaning:'白色 / 城堡', emoji:'⚪'},
      {word:'よる', r:'yoru', meaning:'夜晚', emoji:'🌙'},
      {word:'くるま', r:'kuruma', meaning:'汽车 / 车辆', emoji:'🚗'},
      {word:'はる', r:'haru', meaning:'春天', emoji:'🌱'}
    ]
  },
  {
    id: "unit_wa",
    rowName: "わ行・ん",
    unitNum: "第 10 单元",
    romaji: "wa · (i) · (u) · (e) · wo / n",
    title: "圆唇与鼻韵 · 假名星图终章",
    desc: "双唇收拢滑出wa；“を”现代发音同o，专作宾语助词；“ん”为独立占一拍的鼻音韵尾。",
    kana: [
      {h:'わ', k:'ワ', r:'wa', origin:'和', hint:'和之圆弧，背部圆润', note:'双唇拢圆后快速滑向a'},
      {h:'を', k:'ヲ', r:'wo', origin:'乎', hint:'乎之多折，宾语助词', note:'发音同o，专用于句中作宾格助词'},
      {h:'ん', k:'ン', r:'n', origin:'无', hint:'无之行草，如h飘逸', note:'★拨音：独立占一拍(mora)，发音随其后假名而变化'}
    ],
    words: [
      {word:'わたし', r:'watashi', meaning:'我', emoji:'🙋'},
      {word:'ほん', r:'hon', meaning:'书本', emoji:'📚'},
      {word:'にほん', r:'nihon', meaning:'日本', emoji:'🗾'},
      {word:'みかん', r:'mikan', meaning:'蜜柑 / 橘子', emoji:'🍊'},
      {word:'きりん', r:'kirin', meaning:'长颈鹿', emoji:'🦒'},
      {word:'わに', r:'wani', meaning:'鳄鱼', emoji:'🐊'},
      {word:'らいおん', r:'raion', meaning:'狮子', emoji:'🦁'},
      {word:'てんき', r:'tenki', meaning:'天气', emoji:'☀️'},
      {word:'かんたん', r:'kantan', meaning:'简单 / 容易', emoji:'✨'}
    ]
  }
];

const CONFUSABLE_PAIRS = [
  {
    pair: [
      {h:'あ', k:'ア', r:'a'},
      {h:'お', k:'オ', r:'o'}
    ],
    title: "平假名「あ」与「お」",
    analysis: "「あ」腹部浑圆饱满，源自草书“安”；「お」右侧带有一点飞扬小点，源自草书“於”。"
  },
  {
    pair: [
      {h:'さ', k:'サ', r:'sa'},
      {h:'き', k:'キ', r:'ki'}
    ],
    title: "平假名「さ」与「き」",
    analysis: "「さ」上方只有一横，源自“左”；「き」上方有两道平行横线，如木头琴弦，源自“幾”。"
  },
  {
    pair: [
      {h:'い', k:'イ', r:'i'},
      {h:'り', k:'リ', r:'ri'}
    ],
    title: "平假名「い」与「り」",
    analysis: "「い」左长右短，左撇带微勾；「り」左短右长，右笔垂竖带大弧钩。"
  },
  {
    pair: [
      {h:'は', k:'ハ', r:'ha'},
      {h:'ほ', k:'ホ', r:'ho'}
    ],
    title: "平假名「は」与「ほ」",
    analysis: "「は」右部横线出头无帽；「ほ」顶部横线戴有一顶盖帽（横线不出头）。"
  },
  {
    pair: [
      {h:'ぬ', k:'ヌ', r:'nu'},
      {h:'め', k:'メ', r:'me'}
    ],
    title: "平假名「ぬ」与「め」",
    analysis: "「ぬ」右侧末尾卷成一个小圆环（有尾巴）；「め」右侧舒展撇出，无小环圆卷（无尾巴）。"
  },
  {
    pair: [
      {h:'ね', k:'ネ', r:'ne'},
      {h:'れ', k:'レ', r:'re'}
    ],
    title: "平假名「ね」与「れ」",
    analysis: "「ね」末尾内卷成小环圆卷；「れ」末尾向右外侧高高翘起展翅。"
  },
  {
    pair: [
      {h:'シ', k:'し', r:'shi'},
      {h:'ツ', k:'つ', r:'tsu'}
    ],
    title: "片假名「シ」与「ツ」",
    analysis: "★世纪大坑：看笔顺方向！「シ」(shi) 两点由上至下微横，长划由左下向上提扫；「ツ」(tsu) 两点斜立并列，长划由右上向左下重划劈下。"
  },
  {
    pair: [
      {h:'ソ', k:'そ', r:'so'},
      {h:'ン', k:'ん', r:'n'}
    ],
    title: "片假名「ソ」与「ン」",
    analysis: "「ソ」(so) 上点竖立，长划自右上向左下撇；「ン」(n) 上点横卧，长划自左下向右上挑出。"
  }
];

const SEION_MATRIX = [
  ['あ','a','い','i','う','u','え','e','お','o'],
  ['か','ka','き','ki','く','ku','け','ke','こ','ko'],
  ['さ','sa','し','shi','す','su','せ','se','そ','so'],
  ['た','ta','ち','chi','つ','tsu','て','te','と','to'],
  ['な','na','に','ni','ぬ','nu','ね','ne','の','no'],
  ['は','ha','ひ','hi','ふ','fu','へ','he','ほ','ho'],
  ['ま','ma','み','mi','む','mu','め','me','も','mo'],
  ['や','ya','','','ゆ','yu','','','よ','yo'],
  ['ら','ra','り','ri','る','ru','れ','re','ろ','ro'],
  ['わ','wa','','','','','','','を','wo'],
  ['ん','n','','','','','','','','']
];
const KATA_MAP = {
  'あ':'ア','い':'イ','う':'ウ','え':'エ','お':'オ',
  'か':'カ','き':'キ','く':'ク','け':'ケ','こ':'コ',
  'さ':'サ','し':'シ','す':'ス','せ':'セ','そ':'ソ',
  'た':'タ','ち':'チ','つ':'ツ','て':'テ','と':'ト',
  'な':'ナ','に':'ニ','ぬ':'ヌ','ね':'ネ','の':'ノ',
  'は':'ハ','ひ':'ヒ','ふ':'フ','へ':'ヘ','ほ':'ホ',
  'ま':'マ','み':'ミ','む':'ム','め':'メ','も':'モ',
  'や':'ヤ','ゆ':'ユ','よ':'ヨ',
  'ら':'ラ','り':'リ','る':'ル','れ':'レ','ろ':'ロ',
  'わ':'ワ','を':'ヲ','ん':'ン'
};
const ROMAJI_AUDIO_MAP = {
  'あ':'a','い':'i','う':'u','え':'e','お':'o',
  'か':'ka','き':'ki','く':'ku','け':'ke','こ':'ko',
  'さ':'sa','し':'shi','す':'su','せ':'se','そ':'so',
  'た':'ta','ち':'chi','つ':'tsu','て':'te','と':'to',
  'な':'na','に':'ni','ぬ':'nu','ね':'ne','の':'no',
  'は':'ha','ひ':'hi','ふ':'fu','へ':'he','ほ':'ho',
  'ま':'ma','み':'mi','む':'mu','め':'me','も':'mo',
  'や':'ya','ゆ':'yu','よ':'yo',
  'ら':'ra','り':'ri','る':'ru','れ':'re','ろ':'ro',
  'わ':'wa','を':'wo','ん':'n'
};

/* ==========================================================
   APP CONTROLLER & STATE MANAGEMENT
   ========================================================== */
let currentUnitIdx = 0;
let currentExerciseTab = 'listen'; // 'listen' | 'spell'
let chartDisplayMode = 'hira'; // 'hira' | 'kata'
let learnedUnits = {};

function initApp() {
  loadLearnedUnits();
  renderUnitPills();
  renderCurrentUnit();
  renderChartTable();
  renderConfusablePairs();
  updateLearnedTag();
}

function loadLearnedUnits() {
  try {
    const s = localStorage.getItem('nhg_kana_learned_units');
    if (s) learnedUnits = JSON.parse(s);
  } catch(e) {}
}

function saveLearnedUnits() {
  try {
    localStorage.setItem('nhg_kana_learned_units', JSON.stringify(learnedUnits));
  } catch(e) {}
  updateLearnedTag();
  renderUnitPills();
}

function updateLearnedTag() {
  const count = Object.keys(learnedUnits).filter(k => learnedUnits[k]).length;
  const el = document.getElementById('statLearnedTag');
  if (el) el.textContent = `已读 ${count} / ${KANA_UNITS.length} 单元`;
}

function toggleUnitLearned(idx) {
  learnedUnits[idx] = !learnedUnits[idx];
  saveLearnedUnits();
  toast(learnedUnits[idx] ? `✅ 已标记【${KANA_UNITS[idx].rowName}】为已研读！` : `已取消标记`);
}

function switchMainView(view) {
  const tabs = ['units', 'intro', 'chart', 'pairs'];
  tabs.forEach(t => {
    const el = document.getElementById('view' + t.charAt(0).toUpperCase() + t.slice(1));
    const btn = document.getElementById('tab' + (t === 'units' ? 'MainUnits' : t.charAt(0).toUpperCase() + t.slice(1)));
    if (el) el.style.display = t === view ? 'block' : 'none';
    if (btn) btn.className = t === view ? 'tab-btn active' : 'tab-btn';
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ==========================================================
   UNIT RENDERING (TEXTBOOK COURSEWARE)
   ========================================================== */
function renderUnitPills() {
  const container = document.getElementById('unitPillsContainer');
  if (!container) return;
  container.innerHTML = '';

  KANA_UNITS.forEach((unit, idx) => {
    const pill = document.createElement('div');
    let cls = 'unit-pill';
    if (idx === currentUnitIdx) cls += ' active';
    if (learnedUnits[idx]) cls += ' learned';
    pill.className = cls;
    pill.innerHTML = `<span>${unit.rowName}</span>`;
    pill.onclick = () => selectUnit(idx);
    container.appendChild(pill);
  });
}

function selectUnit(idx) {
  currentUnitIdx = idx;
  renderUnitPills();
  renderCurrentUnit();
  window.scrollTo({ top: 120, behavior: 'smooth' });
}

function renderCurrentUnit() {
  const container = document.getElementById('unitContentWorkspace');
  if (!container) return;
  const unit = KANA_UNITS[currentUnitIdx];
  if (!unit) return;

  const isLearned = !!learnedUnits[currentUnitIdx];

  container.innerHTML = `
    <!-- Unit Header -->
    <div class="unit-head-card">
      <div class="unit-head-info">
        <span class="unit-tag">${unit.unitNum} · 核心课文</span>
        <div class="unit-title-row">
          <h2 class="unit-title">${unit.rowName}</h2>
          <span class="unit-romaji">${unit.romaji}</span>
        </div>
        <div class="unit-desc"><strong>${unit.title}</strong> —— ${unit.desc}</div>
      </div>
      <div class="unit-head-actions">
        <button class="read-row-btn" onclick="playCurrentRowSequentialAudio()" title="顺序朗读本单元全部假名">
          <span>🔊</span>
          <span>整行示范朗读</span>
        </button>
        <label class="mark-read-toggle">
          <input type="checkbox" ${isLearned ? 'checked' : ''} onchange="toggleUnitLearned(${currentUnitIdx})">
          <span>已研读</span>
        </label>
      </div>
    </div>

    <!-- Section 1: Kana Deep Study -->
    <div class="section-block">
      <div class="section-title-wrap">
        <h3 class="section-title">假名精讲与发音要领</h3>
        <span class="section-subtitle">点击卡片即可发音试听 · 汉字草书溯源</span>
      </div>
      <div class="kana-cards-grid">
        ${unit.kana.map(k => `
          <div class="kana-card" id="kcard_${k.r}" onclick="playKanaSound('${k.h}', '${k.r}')">
            <span class="kana-play-btn" title="点击发音">🔊</span>
            <div class="kana-main">${k.h}</div>
            <div class="kana-sub-row">
              <span class="kana-kata" title="对应片假名">${k.k}</span>
              <span class="kana-romaji">${k.r}</span>
            </div>
            <div class="kana-origin">源自汉字「${k.origin}」</div>
            <div class="kana-hint">${k.hint}</div>
            <div style="font-size:10px;color:var(--jp-navy);margin-top:2px;">${k.note}</div>
          </div>
        `).join('')}
      </div>
    </div>

    <!-- Section 2: Textbook Vocabulary (Restricted Phonics) -->
    <div class="section-block">
      <div class="section-title-wrap">
        <h3 class="section-title">教材受限词汇拼读 (${unit.words.length} 词)</h3>
        <span class="section-subtitle">严格仅由当前行及已学假名构成</span>
      </div>
      <div class="vocab-intro-tip">
        <strong>💡 教材拼读法则：</strong> 本单元生词全部由当前行假名与此前已学假名组合而成，无生词挫败感。请一边朗读一边记忆实际音义绑定。
      </div>
      <div class="vocab-grid">
        ${unit.words.map(w => `
          <div class="vocab-card">
            <div class="vocab-left">
              <span class="vocab-emoji">${w.emoji}</span>
              <div class="vocab-text-box">
                <span class="vocab-word">${w.word}</span>
                <span class="vocab-romaji">[ ${w.r} ]</span>
                <span class="vocab-meaning">${w.meaning}</span>
              </div>
            </div>
            <button class="vocab-speak-btn" onclick="playVocabSound('${w.word}', '${w.r}')" title="朗读单词">🔊</button>
          </div>
        `).join('')}
      </div>
    </div>

    <!-- Section 3: Self-Assessment Exercises -->
    <div class="section-block">
      <div class="section-title-wrap">
        <h3 class="section-title">课后巩固与自测练习</h3>
        <span class="section-subtitle">课后自我检测 · 自由练习解析</span>
      </div>

      <div class="exercise-subtabs">
        <button class="subtab-btn ${currentExerciseTab==='listen'?'active':''}" onclick="switchExerciseTab('listen')">1. 听音辨字自测</button>
        <button class="subtab-btn ${currentExerciseTab==='spell'?'active':''}" onclick="switchExerciseTab('spell')">2. 词汇拼装演练</button>
      </div>

      <div class="exercise-pane ${currentExerciseTab==='listen'?'active':''}" id="paneExerciseListen">
        <div id="listenTestContainer"></div>
      </div>
      <div class="exercise-pane ${currentExerciseTab==='spell'?'active':''}" id="paneExerciseSpell">
        <div id="spellTestContainer"></div>
      </div>
    </div>

    <!-- Section 4: Unit Pagination -->
    <div class="unit-pagination">
      ${currentUnitIdx > 0 ? `
        <button class="page-nav-btn" onclick="selectUnit(${currentUnitIdx - 1})">
          <span>⬅️</span>
          <span>上一单元 (${KANA_UNITS[currentUnitIdx - 1].rowName})</span>
        </button>
      ` : `<div></div>`}

      ${currentUnitIdx < KANA_UNITS.length - 1 ? `
        <button class="page-nav-btn" onclick="selectUnit(${currentUnitIdx + 1})">
          <span>下一单元 (${KANA_UNITS[currentUnitIdx + 1].rowName})</span>
          <span>➡️</span>
        </button>
      ` : `
        <button class="page-nav-btn" onclick="switchMainView('chart')">
          <span>查看五十音全图谱</span>
          <span>🌟</span>
        </button>
      `}
    </div>
  `;

  initUnitListeningTest();
  initUnitSpellingTest();
}

/* ==========================================================
   EXERCISE 1: LISTENING SELF-TEST
   ========================================================== */
let listenTargetKana = null;

function switchExerciseTab(tab) {
  currentExerciseTab = tab;
  document.querySelectorAll('.subtab-btn').forEach((b, idx) => {
    b.className = (idx === 0 && tab === 'listen') || (idx === 1 && tab === 'spell') ? 'subtab-btn active' : 'subtab-btn';
  });
  const pListen = document.getElementById('paneExerciseListen');
  const pSpell = document.getElementById('paneExerciseSpell');
  if (pListen) pListen.className = tab === 'listen' ? 'exercise-pane active' : 'exercise-pane';
  if (pSpell) pSpell.className = tab === 'spell' ? 'exercise-pane active' : 'exercise-pane';
}

function initUnitListeningTest() {
  const container = document.getElementById('listenTestContainer');
  if (!container) return;
  const unit = KANA_UNITS[currentUnitIdx];
  if (!unit || !unit.kana.length) return;

  listenTargetKana = unit.kana[Math.floor(Math.random() * unit.kana.length)];

  // Options pool
  let options = [listenTargetKana];
  let pool = unit.kana.filter(k => k.r !== listenTargetKana.r);
  pool.sort(() => Math.random() - 0.5);
  while (options.length < 4 && pool.length > 0) {
    options.push(pool.pop());
  }
  // Fill from earlier units if needed
  if (options.length < 4) {
    for (let u = 0; u <= currentUnitIdx; u++) {
      for (const k of KANA_UNITS[u].kana) {
        if (!options.find(o => o.r === k.r)) options.push(k);
        if (options.length >= 4) break;
      }
      if (options.length >= 4) break;
    }
  }
  options.sort(() => Math.random() - 0.5);

  container.innerHTML = `
    <div class="listen-test-card">
      <div class="listen-prompt">🎧 听录音选假名：点击按钮播放标准读音，选出正确的假名</div>
      <button class="listen-sound-btn" onclick="playTargetListenAudio()">
        <span>🔊</span>
        <span>播放考题发音</span>
      </button>
      <div class="listen-options">
        ${options.map(opt => `
          <button class="listen-opt" onclick="checkListenAnswer('${opt.r}', this)">
            ${opt.h} <span style="font-size:14px;color:var(--jp-gold);margin-left:2px;">${opt.k}</span>
          </button>
        `).join('')}
      </div>
      <div class="listen-feedback" id="listenFeedbackArea"></div>
      <div style="margin-top:6px;">
        <button class="btn-action" onclick="initUnitListeningTest()">🔄 换下一题</button>
      </div>
    </div>
  `;

  setTimeout(() => playTargetListenAudio(), 200);
}

function playTargetListenAudio() {
  if (listenTargetKana) {
    playKanaSound(listenTargetKana.h, listenTargetKana.r);
  }
}

function checkListenAnswer(selectedRomaji, btn) {
  const fb = document.getElementById('listenFeedbackArea');
  if (selectedRomaji === listenTargetKana.r) {
    btn.classList.add('correct');
    if (fb) fb.innerHTML = `<span style="color:var(--jp-green);">🎉 回答正确！「${listenTargetKana.h}」/「${listenTargetKana.k}」罗马音为 [${listenTargetKana.r}]，源自汉字「${listenTargetKana.origin}」。</span>`;
  } else {
    btn.classList.add('wrong');
    if (fb) fb.innerHTML = `<span style="color:var(--jp-red);">不正确哦，请再仔细听一次读音！</span>`;
    setTimeout(() => playTargetListenAudio(), 350);
  }
}

/* ==========================================================
   EXERCISE 2: RESTRICTED SPELLING BUILDER
   ========================================================== */
let spellWordIdx = 0;
let spellSlots = [];
let spellTiles = [];

function initUnitSpellingTest() {
  spellWordIdx = 0;
  renderSpellingWord();
}

function renderSpellingWord() {
  const container = document.getElementById('spellTestContainer');
  if (!container) return;
  const unit = KANA_UNITS[currentUnitIdx];
  const w = unit.words[spellWordIdx];
  if (!w) return;

  spellSlots = new Array(w.word.length).fill(null);

  // Tiles: word chars + 1 or 2 distractor chars from learned units
  let tiles = [];
  for (let i = 0; i < w.word.length; i++) {
    tiles.push({ id: 'w_' + i, char: w.word[i], used: false });
  }
  let learnedChars = [];
  for (let u = 0; u <= currentUnitIdx; u++) {
    KANA_UNITS[u].kana.forEach(k => {
      if (!w.word.includes(k.h) && !learnedChars.includes(k.h)) learnedChars.push(k.h);
    });
  }
  learnedChars.sort(() => Math.random() - 0.5);
  for (let d = 0; d < Math.min(2, learnedChars.length); d++) {
    tiles.push({ id: 'd_' + d, char: learnedChars[d], used: false });
  }
  tiles.sort(() => Math.random() - 0.5);
  spellTiles = tiles;

  container.innerHTML = `
    <div class="spell-builder-card">
      <div style="font-size:12px;font-weight:700;color:var(--muted);">例词拼读演练 ${spellWordIdx + 1} / ${unit.words.length}</div>
      <div class="spell-target-box">
        <span style="font-size:36px;">${w.emoji}</span>
        <div>
          <div style="font-size:16px;font-weight:900;color:var(--ink);">${w.meaning}</div>
          <div style="font-size:13px;font-family:'Outfit',sans-serif;color:var(--jp-navy);font-weight:700;">[ ${w.r} ]</div>
        </div>
        <button class="vocab-speak-btn" onclick="playVocabSound('${w.word}', '${w.r}')" title="播放读音">🔊</button>
      </div>

      <div class="spell-slots" id="spellSlotsWrap"></div>
      <div class="spell-tiles" id="spellTilesWrap"></div>

      <div id="spellFeedback" style="font-size:13px;font-weight:700;min-height:20px;">点击下方假名词块填入格子中</div>

      <div class="spell-actions">
        <button class="btn-action" onclick="resetSpelling()">🔄 重新排列</button>
        <button class="btn-action" onclick="revealSpellingAnswer()">💡 查看答案</button>
        <button class="btn-action" onclick="nextSpellingWord()">⏭️ 下一词</button>
      </div>
    </div>
  `;

  renderSpellSlotsAndTiles();
  setTimeout(() => playVocabSound(w.word, w.r), 200);
}

function renderSpellSlotsAndTiles() {
  const slotsWrap = document.getElementById('spellSlotsWrap');
  const tilesWrap = document.getElementById('spellTilesWrap');
  if (!slotsWrap || !tilesWrap) return;

  slotsWrap.innerHTML = '';
  spellSlots.forEach((slot, idx) => {
    const sEl = document.createElement('div');
    sEl.className = 'spell-slot' + (slot ? ' filled' : '');
    sEl.textContent = slot ? slot.char : '';
    sEl.title = slot ? '点击取下' : '待填槽位';
    sEl.onclick = () => removeSpellSlot(idx);
    slotsWrap.appendChild(sEl);
  });

  tilesWrap.innerHTML = '';
  spellTiles.forEach(tile => {
    const tEl = document.createElement('div');
    tEl.className = 'spell-tile' + (tile.used ? ' used' : '');
    tEl.textContent = tile.char;
    tEl.onclick = () => pickSpellTile(tile.id);
    tilesWrap.appendChild(tEl);
  });
}

function pickSpellTile(tileId) {
  const tile = spellTiles.find(t => t.id === tileId);
  if (!tile || tile.used) return;
  const emptyIdx = spellSlots.findIndex(s => s === null);
  if (emptyIdx === -1) return;

  tile.used = true;
  spellSlots[emptyIdx] = tile;
  renderSpellSlotsAndTiles();

  if (!spellSlots.includes(null)) {
    checkSpellingResult();
  }
}

function removeSpellSlot(slotIdx) {
  const slot = spellSlots[slotIdx];
  if (!slot) return;
  slot.used = false;
  spellSlots[slotIdx] = null;
  renderSpellSlotsAndTiles();
}

function resetSpelling() {
  spellSlots.forEach(s => { if (s) s.used = false; });
  spellSlots = spellSlots.map(() => null);
  renderSpellSlotsAndTiles();
}

function revealSpellingAnswer() {
  const unit = KANA_UNITS[currentUnitIdx];
  const w = unit.words[spellWordIdx];
  const fb = document.getElementById('spellFeedback');
  if (fb) fb.innerHTML = `<span style="color:var(--jp-navy);">答案为：<strong>${w.word}</strong> [${w.r}]</span>`;
}

function checkSpellingResult() {
  const unit = KANA_UNITS[currentUnitIdx];
  const w = unit.words[spellWordIdx];
  const assembled = spellSlots.map(s => s.char).join('');
  const fb = document.getElementById('spellFeedback');

  if (assembled === w.word) {
    if (fb) fb.innerHTML = `<span style="color:var(--jp-green);">🎉 拼读正确！${w.word} [${w.r}] = ${w.meaning}</span>`;
    playVocabSound(w.word, w.r);
  } else {
    if (fb) fb.innerHTML = `<span style="color:var(--jp-red);">顺序不对哦，点击已填入的格子即可取下重新排！</span>`;
  }
}

function nextSpellingWord() {
  const unit = KANA_UNITS[currentUnitIdx];
  spellWordIdx = (spellWordIdx + 1) % unit.words.length;
  renderSpellingWord();
}

/* ==========================================================
   AUDIO ENGINE (Native Audio with Web Speech API fallback)
   ========================================================== */
let audioCache = {};
let isSequentialPlaying = false;

function playAudioFile(url, fallbackText) {
  return new Promise((resolve) => {
    let a = audioCache[url];
    if (!a) {
      a = new Audio(url);
      audioCache[url] = a;
    }
    a.currentTime = 0;
    a.onended = () => resolve();
    a.onerror = () => {
      // Fallback to speech synthesis
      speakFallback(fallbackText, resolve);
    };
    a.play().catch(() => {
      speakFallback(fallbackText, resolve);
    });
  });
}

function speakFallback(text, doneCallback) {
  if ('speechSynthesis' in window && text) {
    try {
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'ja-JP';
      u.rate = 0.9;
      u.onend = () => { if (doneCallback) doneCallback(); };
      u.onerror = () => { if (doneCallback) doneCallback(); };
      window.speechSynthesis.speak(u);
      return;
    } catch(e) {}
  }
  if (doneCallback) doneCallback();
}

function playKanaSound(kanaChar, romaji) {
  const audioFile = `audio/nihongo0/kana_${romaji}.mp3`;
  const card = document.getElementById('kcard_' + romaji);
  if (card) {
    card.classList.add('playing');
    setTimeout(() => card.classList.remove('playing'), 900);
  }
  playAudioFile(audioFile, kanaChar);
}

function playVocabSound(word, romaji) {
  const audioFile = `audio/nihongo0/kw_${romaji}.mp3`;
  playAudioFile(audioFile, word);
}

async function playCurrentRowSequentialAudio() {
  if (isSequentialPlaying) return;
  isSequentialPlaying = true;
  const unit = KANA_UNITS[currentUnitIdx];
  toast(`🔊 正在连播【${unit.rowName}】全行发音...`);

  for (let i = 0; i < unit.kana.length; i++) {
    const k = unit.kana[i];
    const card = document.getElementById('kcard_' + k.r);
    if (card) card.classList.add('playing');
    await playAudioFile(`audio/nihongo0/kana_${k.r}.mp3`, k.h);
    await new Promise(r => setTimeout(r, 260));
    if (card) card.classList.remove('playing');
  }
  isSequentialPlaying = false;
}

/* ==========================================================
   VIEW 3: COMPLETE 50-SOUND CHART
   ========================================================== */
function switchChartMode(mode) {
  chartDisplayMode = mode;
  document.getElementById('btnChartHira').className = mode === 'hira' ? 'btn-action active' : 'btn-action';
  document.getElementById('btnChartKata').className = mode === 'kata' ? 'btn-action active' : 'btn-action';
  renderChartTable();
}

function renderChartTable() {
  const table = document.getElementById('chartTableMain');
  if (!table) return;
  table.innerHTML = '';

  SEION_MATRIX.forEach(row => {
    const tr = document.createElement('tr');
    for (let c = 0; c < 10; c += 2) {
      const hira = row[c];
      const romaji = row[c + 1];
      const td = document.createElement('td');
      if (!hira) {
        td.className = 'chart-cell empty';
      } else {
        td.className = 'chart-cell';
        const displayChar = chartDisplayMode === 'kata' ? (KATA_MAP[hira] || hira) : hira;
        td.innerHTML = `
          <div class="cell-kana">${displayChar}</div>
          <div class="cell-sub">${romaji}</div>
        `;
        td.onclick = () => {
          const rAudio = ROMAJI_AUDIO_MAP[hira] || romaji;
          playKanaSound(hira, rAudio);
        };
      }
      tr.appendChild(td);
    }
    table.appendChild(tr);
  });
}

/* ==========================================================
   VIEW 4: CONFUSABLE MINIMAL PAIRS
   ========================================================== */
function renderConfusablePairs() {
  const container = document.getElementById('confusableGridContainer');
  if (!container) return;
  container.innerHTML = '';

  CONFUSABLE_PAIRS.forEach(cp => {
    const card = document.createElement('div');
    card.className = 'confusable-card';
    card.innerHTML = `
      <div style="font-size:14px;font-weight:900;color:var(--ink);margin-bottom:10px;">${cp.title}</div>
      <div class="confusable-pair">
        <div class="confusable-item" onclick="playKanaSound('${cp.pair[0].h}', '${cp.pair[0].r}')" style="cursor:pointer;" title="点击发音">
          <span class="confusable-char">${cp.pair[0].h}</span>
          <span class="confusable-romaji">[ ${cp.pair[0].r} ] 🔊</span>
        </div>
        <div class="confusable-vs">VS</div>
        <div class="confusable-item" onclick="playKanaSound('${cp.pair[1].h}', '${cp.pair[1].r}')" style="cursor:pointer;" title="点击发音">
          <span class="confusable-char">${cp.pair[1].h}</span>
          <span class="confusable-romaji">[ ${cp.pair[1].r} ] 🔊</span>
        </div>
      </div>
      <div class="confusable-tip">${cp.analysis}</div>
    `;
    container.appendChild(card);
  });
}

/* Toast */
function toast(msg) {
  let el = document.getElementById('textbookToast');
  if (!el) return;
  el.textContent = msg;
  el.style.opacity = '1';
  clearTimeout(el._timer);
  el._timer = setTimeout(() => { el.style.opacity = '0'; }, 2200);
}

window.addEventListener('DOMContentLoaded', initApp);
</script>
</body>
</html>
"""

with open('/home/ubuntu/ws/jump-jump-game/kana.html', 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)

print("kana.html generated successfully. Size:", len(HTML_CONTENT), "bytes")
