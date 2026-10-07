#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build tech-blogs.html with embedded fallback JSON seed, dynamic multi-proxy RSS fetcher,
and full UI consistent with tools.html design system.
"""

import json
import os

with open('data/tech-blogs.json', 'r', encoding='utf-8') as f:
    blogs_data = json.load(f)

json_seed = json.dumps(blogs_data, ensure_ascii=False, indent=2)

html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Y1P7PMMM6V"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
  gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});
    gtag('config', 'G-Y1P7PMMM6V');
  </script>
  <script>
    (function(){var sent=false;function u(e){var t=e.target;if(sent||!t||!t.closest||!t.closest('button,input,select,textarea,canvas,[role=button]')||t.closest('footer,nav'))return;sent=true;gtag('event','tool_use',{tool:'tech-blogs',action:'use'});}
    document.addEventListener('click',u,true);document.addEventListener('change',u,true);})();
  </script>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>中日韩与全球企业技术博客雷达 · 工程前沿 RSS 聚合平台</title>
  <meta name="description" content="汇聚 LINE、Mercari、ZOZO、Pixiv、日本经济新闻 (Nikkei)、NAVER、Kakao、Toss、Coupang、美团、有赞、云风、Draveness、EMQX、APISIX、Doris、CoolShell、Cloudflare、GitHub 等 54 家中日韩及全球顶尖科技企业技术博客。采用三层容灾架构：内置精选离线兜底 + 浏览器实时代理抓取 + GitHub Actions CI 静态预聚合。">
  <meta name="theme-color" content="#0284c7">

  <style>
    :root {
      --bg-base: #f8fafc;
      --bg-surface: #ffffff;
      --bg-subtle: #f1f5f9;
      --border-color: #e2e8f0;
      --border-focus: #0284c7;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --text-light: #94a3b8;

      --primary: #0284c7;
      --primary-hover: #0369a1;
      --primary-subtle: #e0f2fe;
      --primary-border: #bae6fd;

      --success: #10b981;
      --success-subtle: #d1fae5;
      --warning: #f59e0b;
      --warning-subtle: #fef3c7;
      --purple: #8b5cf6;
      --purple-subtle: #ede9fe;
      --rose: #f43f5e;
      --rose-subtle: #ffe4e6;

      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-pill: 9999px;

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
      --shadow-lg: 0 12px 24px -4px rgba(15, 23, 42, 0.08), 0 4px 12px -2px rgba(15, 23, 42, 0.04);
      --shadow-hover: 0 20px 30px -6px rgba(15, 23, 42, 0.12), 0 8px 16px -4px rgba(15, 23, 42, 0.06);

      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    }

    [data-theme="dark"] {
      --bg-base: #090d16;
      --bg-surface: #111827;
      --bg-subtle: #1f2937;
      --border-color: #374151;
      --border-focus: #38bdf8;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
      --text-light: #6b7280;

      --primary: #38bdf8;
      --primary-hover: #0ea5e9;
      --primary-subtle: rgba(56, 189, 248, 0.15);
      --primary-border: #0369a1;

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
      --shadow-lg: 0 12px 24px -4px rgba(0, 0, 0, 0.6);
      --shadow-hover: 0 20px 30px -6px rgba(0, 0, 0, 0.7);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.25s ease, color 0.25s ease;
      line-height: 1.5;
    }

    /* 顶部导航 */
    .app-header {
      background-color: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 50;
      backdrop-filter: blur(8px);
      transition: background-color 0.25s ease, border-color 0.25s ease;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: inherit;
    }

    .brand-icon {
      font-size: 26px;
      line-height: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 42px;
      height: 42px;
      border-radius: var(--radius-md);
      background: var(--primary-subtle);
      border: 1px solid var(--primary-border);
    }

    .brand-text h1 {
      font-size: 18px;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .brand-text p {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 1px;
    }

    .badge-sub {
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: var(--radius-pill);
      background: var(--primary-subtle);
      color: var(--primary);
      border: 1px solid var(--primary-border);
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .btn-nav {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-pill);
      text-decoration: none;
      transition: all 0.2s ease;
      cursor: pointer;
    }

    .btn-nav:hover {
      background: var(--primary-subtle);
      border-color: var(--primary-border);
      color: var(--primary);
    }

    .btn-icon-only {
      width: 36px;
      height: 36px;
      border-radius: var(--radius-pill);
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn-icon-only:hover {
      background: var(--primary-subtle);
      border-color: var(--primary-border);
    }

    /* 容器 */
    .container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 28px 24px 60px;
      width: 100%;
      flex: 1;
    }

    /* Hero Banner */
    .hero-banner {
      background: linear-gradient(135deg, var(--bg-surface) 0%, var(--bg-subtle) 100%);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 32px 36px;
      margin-bottom: 28px;
      box-shadow: var(--shadow-sm);
      position: relative;
      overflow: hidden;
    }

    .hero-title {
      font-size: 28px;
      font-weight: 900;
      color: var(--text-main);
      margin-bottom: 10px;
      letter-spacing: -0.02em;
      line-height: 1.3;
    }

    .hero-title span {
      background: linear-gradient(120deg, #0284c7, #8b5cf6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-desc {
      font-size: 14px;
      color: var(--text-muted);
      max-width: 820px;
      line-height: 1.7;
      margin-bottom: 20px;
    }

    .feature-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .feature-pill {
      font-size: 12px;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: var(--radius-pill);
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: var(--shadow-sm);
    }

    .feature-pill .icon {
      font-size: 14px;
    }

    /* 架构折叠卡片 */
    .arch-details {
      margin-top: 18px;
      border: 1px dashed var(--primary-border);
      border-radius: var(--radius-md);
      background: var(--primary-subtle);
      padding: 12px 18px;
      font-size: 13px;
      color: var(--text-main);
    }

    .arch-summary {
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--primary);
    }

    .arch-content {
      margin-top: 10px;
      line-height: 1.6;
      color: var(--text-muted);
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
    }

    .arch-item {
      background: var(--bg-surface);
      padding: 10px 14px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
    }

    .arch-item strong {
      color: var(--text-main);
      display: block;
      margin-bottom: 3px;
    }

    /* 工具栏 */
    .toolbar-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      margin-bottom: 22px;
    }

    .search-box {
      flex: 1;
      min-width: 280px;
      position: relative;
    }

    .search-input {
      width: 100%;
      height: 44px;
      padding: 0 16px 0 42px;
      border-radius: var(--radius-pill);
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
      color: var(--text-main);
      font-size: 14px;
      outline: none;
      transition: all 0.2s ease;
      box-shadow: var(--shadow-sm);
    }

    .search-input:focus {
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }

    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 16px;
      color: var(--text-light);
      pointer-events: none;
    }

    .filter-tabs {
      display: flex;
      gap: 6px;
      background: var(--bg-subtle);
      padding: 4px;
      border-radius: var(--radius-pill);
      border: 1px solid var(--border-color);
    }

    .filter-tab {
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 600;
      border-radius: var(--radius-pill);
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .filter-tab.active {
      background: var(--bg-surface);
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }

    .action-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-action-primary {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 9px 18px;
      font-size: 13px;
      font-weight: 700;
      color: #ffffff;
      background: var(--primary);
      border: none;
      border-radius: var(--radius-pill);
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: var(--shadow-sm);
    }

    .btn-action-primary:hover {
      background: var(--primary-hover);
      transform: translateY(-1px);
    }

    .btn-action-primary:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
    }

    .select-sort {
      height: 40px;
      padding: 0 12px;
      border-radius: var(--radius-pill);
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
      color: var(--text-main);
      font-size: 13px;
      font-weight: 600;
      outline: none;
      cursor: pointer;
    }

    /* 实时进度条 */
    .progress-container {
      background: var(--bg-surface);
      border: 1px solid var(--primary-border);
      border-radius: var(--radius-md);
      padding: 12px 18px;
      margin-bottom: 22px;
      box-shadow: var(--shadow-sm);
      display: none;
      animation: fadeIn 0.3s ease;
    }

    .progress-header {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 8px;
    }

    .progress-bar-bg {
      height: 8px;
      border-radius: var(--radius-pill);
      background: var(--bg-subtle);
      overflow: hidden;
    }

    .progress-bar-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #0284c7, #10b981);
      transition: width 0.3s ease;
    }

    /* 博客卡片网格 */
    .blogs-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 20px;
    }

    .blog-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 22px;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }

    .blog-card:hover {
      box-shadow: var(--shadow-hover);
      border-color: var(--primary-border);
      transform: translateY(-3px);
    }

    .card-head {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      margin-bottom: 12px;
    }

    .blog-icon {
      font-size: 28px;
      width: 48px;
      height: 48px;
      border-radius: var(--radius-md);
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .blog-title-area {
      flex: 1;
      min-width: 0;
    }

    .blog-name-link {
      font-size: 17px;
      font-weight: 800;
      color: var(--text-main);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .blog-name-link:hover {
      color: var(--primary);
    }

    .blog-meta-tags {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 4px;
      flex-wrap: wrap;
    }

    .cat-badge {
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: var(--radius-pill);
      background: var(--bg-subtle);
      color: var(--text-muted);
      border: 1px solid var(--border-color);
    }

    .cat-badge.japan {
      background: rgba(239, 68, 68, 0.08);
      color: #ef4444;
      border-color: rgba(239, 68, 68, 0.2);
    }

    .cat-badge.korea {
      background: rgba(139, 92, 246, 0.08);
      color: #8b5cf6;
      border-color: rgba(139, 92, 246, 0.2);
    }

    .cat-badge.global {
      background: rgba(14, 165, 233, 0.08);
      color: #0ea5e9;
      border-color: rgba(14, 165, 233, 0.2);
    }

    .cat-badge.china {
      background: rgba(245, 158, 11, 0.08);
      color: #d97706;
      border-color: rgba(245, 158, 11, 0.2);
    }

    .status-badge {
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: var(--radius-pill);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .status-badge.static {
      background: var(--bg-subtle);
      color: var(--text-muted);
      border: 1px solid var(--border-color);
    }

    .status-badge.ci {
      background: var(--purple-subtle);
      color: var(--purple);
      border: 1px solid rgba(139, 92, 246, 0.3);
    }

    .status-badge.live {
      background: var(--success-subtle);
      color: var(--success);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .status-badge.loading {
      background: var(--warning-subtle);
      color: var(--warning);
      border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .blog-desc {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 12px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .tech-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-bottom: 16px;
    }

    .tech-tag {
      font-size: 11px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: var(--radius-pill);
      background: var(--bg-subtle);
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid var(--border-color);
    }

    .tech-tag:hover {
      background: var(--primary-subtle);
      color: var(--primary);
      border-color: var(--primary-border);
    }

    /* 文章列表区域 */
    .articles-container {
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 10px 12px;
      margin-bottom: 16px;
      flex: 1;
    }

    .articles-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--border-color);
    }

    .articles-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .article-count {
      font-size: 11px;
      color: var(--text-light);
    }

    .article-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 9px;
    }

    .article-item {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .article-meta {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .article-date {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-light);
      font-variant-numeric: tabular-nums;
    }

    .article-link {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-main);
      text-decoration: none;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      transition: color 0.15s ease;
    }

    .article-link:hover {
      color: var(--primary);
      text-decoration: underline;
    }

    .article-link::after {
      content: " ↗";
      font-size: 11px;
      color: var(--text-light);
    }

    /* 卡片底栏操作 */
    .card-foot {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-top: auto;
      padding-top: 10px;
      border-top: 1px solid var(--border-color);
    }

    .foot-btn-group {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .btn-foot {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 5px 10px;
      font-size: 12px;
      font-weight: 600;
      border-radius: var(--radius-pill);
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
      color: var(--text-muted);
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s ease;
    }

    .btn-foot:hover {
      background: var(--primary-subtle);
      color: var(--primary);
      border-color: var(--primary-border);
    }

    /* 悬浮 Toast */
    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--text-main);
      color: var(--bg-surface);
      padding: 10px 18px;
      border-radius: var(--radius-pill);
      font-size: 13px;
      font-weight: 600;
      box-shadow: var(--shadow-lg);
      z-index: 100;
      opacity: 0;
      transform: translateY(20px);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
    }

    .toast.show {
      opacity: 1;
      transform: translateY(0);
    }

    /* 空状态 */
    .empty-state {
      text-align: center;
      padding: 60px 20px;
      grid-column: 1 / -1;
      color: var(--text-muted);
    }

    .empty-state h3 {
      font-size: 18px;
      color: var(--text-main);
      margin-bottom: 8px;
    }

    /* 页脚 */
    .footer {
      border-top: 1px solid var(--border-color);
      background: var(--bg-surface);
      padding: 24px 20px;
      text-align: center;
      font-size: 13px;
      color: var(--text-muted);
      margin-top: auto;
    }

    .footer-links {
      display: flex;
      justify-content: center;
      gap: 16px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }

    .footer-links a {
      color: var(--primary);
      text-decoration: none;
      font-weight: 600;
    }

    .footer-links a:hover {
      text-decoration: underline;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 640px) {
      .hero-title {
        font-size: 24px;
      }
      .app-header {
        padding: 10px 16px;
      }
      .container {
        padding: 18px 14px 40px;
      }
      .blogs-grid {
        grid-template-columns: 1fr;
      }
      .toolbar-bar {
        flex-direction: column;
        align-items: stretch;
      }
      .filter-tabs {
        overflow-x: auto;
      }
    }
  </style>
    <link rel="canonical" href="https://tool.0101.click/tech-blogs.html">
</head>
<body>

  <!-- 顶部导航 -->
  <header class="app-header">
    <a href="tech-blogs.html" class="brand-group">
      <div class="brand-icon">📡</div>
      <div class="brand-text">
        <h1>全球企业技术博客雷达 <span class="badge-sub">54 家中日韩名企 · RSS 聚合</span></h1>
        <p>对齐 gihyo.jp 体系 · 实时工程实战追踪</p>
      </div>
    </a>

    <div class="nav-actions">
      <a href="tools.html" class="btn-nav" title="返回实用工具箱">
        <span>🛠️</span>
        <span>工具矩阵</span>
      </a>
      <a href="index.html" class="btn-nav" title="返回游戏大厅">
        <span>🎮</span>
        <span>游戏大厅</span>
      </a>
      <button class="btn-icon-only" id="themeToggleBtn" onclick="toggleTheme()" title="切换明暗主题">
        🌓
      </button>
    </div>
  </header>

  <!-- 主体内容 -->
  <main class="container">

    <!-- Hero 介绍 -->
    <section class="hero-banner">
      <h2 class="hero-title">中日韩与全球知名科技企业 <span>技术博客与前沿雷达</span></h2>
      <p class="hero-desc">
        秉持“静态底座打底、边缘代理实时更新、CI/CD 定时归集”的高可用架构设计。实时追踪来自 NAVER、Kakao、Toss、Coupang、LINE/Yahoo、Mercari、ZOZO、Pixiv、日本经济新闻 (Nikkei)、Cloudflare、GitHub、Netflix、美团、有赞、云风、Draveness、EMQX、APISIX、Doris、CoolShell 等 54 家顶尖团队的一线实战演进。
      </p>

      <!-- 架构特性徽章 -->
      <div class="feature-pills">
        <div class="feature-pill"><span class="icon">📦</span> 内置精选离线兜底 (0ms 秒开)</div>
        <div class="feature-pill"><span class="icon">⚡</span> CI 静态预聚合 (GitHub Actions 定时同步)</div>
        <div class="feature-pill"><span class="icon">🌐</span> 浏览器端边缘代理实时获取 (CORS 容灾)</div>
        <div class="feature-pill"><span class="icon">🔒</span> 零后端常驻依赖与用户隐私隔离</div>
      </div>

      <!-- 架构设计折叠栏 -->
      <details class="arch-details">
        <summary class="arch-summary">
          <span>🏛️ 点击查看：系统架构演进路线与多级容灾设计规范</span>
        </summary>
        <div class="arch-content">
          <div class="arch-item">
            <strong>Level 0: DOM 内置种子打底</strong>
            页面打包时已预置完整博客元数据与最新文章精选。弱网、断网或代理失效时 100% 正常阅读与跳转导航。
          </div>
          <div class="arch-item">
            <strong>Level 1: CI/CD 预聚合静态 JSON</strong>
            通过 <code>scripts/update_tech_blogs.py</code> 定时由 GitHub Actions 在无 CORS 限制环境下抓取，生成 <code>data/tech-blogs.json</code> 静态分发。
          </div>
          <div class="arch-item">
            <strong>Level 2: 运行时多路代理动态拉取</strong>
            客户端支持通过 AllOrigins / CorsProxy 实时拉取最新 3~5 篇动态，DOMParser 本地解析并进行 LocalStorage 缓存。
          </div>
        </div>
      </details>
    </section>

    <!-- 搜索与筛选控制栏 -->
    <div class="toolbar-bar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="输入关键字搜索（如：LINE、Mercari、Go、Kubernetes、AI Agent、Rust、微服务...）" oninput="filterBlogs()">
      </div>

      <div class="filter-tabs">
        <button class="filter-tab active" data-cat="all" onclick="setCategory('all')">全部 (<span id="countAll">54</span>)</button>
        <button class="filter-tab" data-cat="japan" onclick="setCategory('japan')">🇯🇵 日本名企 (<span id="countJapan">17</span>)</button>
        <button class="filter-tab" data-cat="korea" onclick="setCategory('korea')">🇰🇷 韩国团队 (<span id="countKorea">7</span>)</button>
        <button class="filter-tab" data-cat="global" onclick="setCategory('global')">🌐 全球巨头 (<span id="countGlobal">7</span>)</button>
        <button class="filter-tab" data-cat="china" onclick="setCategory('china')">🇨🇳 国内团队 (<span id="countChina">23</span>)</button>
      </div>

      <div class="action-controls">
        <select class="select-sort" id="sortSelect" onchange="applySorting()">
          <option value="default">默认推荐顺序</option>
          <option value="newest">按文章最新发布时间</option>
        </select>

        <button class="btn-action-primary" id="syncAllBtn" onclick="syncAllLiveFeeds()">
          <span id="syncBtnIcon">🔄</span>
          <span id="syncBtnText">一键实时同步动态</span>
        </button>
      </div>
    </div>

    <!-- 实时拉取进度面板 -->
    <div class="progress-container" id="progressContainer">
      <div class="progress-header">
        <span id="progressStatusText">正在通过代理异步获取最新 Feed...</span>
        <span id="progressCountText">0 / 54</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" id="progressBarFill"></div>
      </div>
    </div>

    <!-- 博客卡片网格 -->
    <div class="blogs-grid" id="blogsGrid">
      <!-- 动态注入 / 静态初始渲染卡片 -->
    </div>

  </main>

  <!-- 底部说明与链接 -->
  <footer class="footer">
    <div class="footer-links">
      <a href="tools.html">🛠️ 实用工具箱 (tool.0101.click)</a>
      <span>·</span>
      <a href="index.html">🎮 游戏大厅 (game.0101.click)</a>
      <span>·</span>
      <a href="kids.html">🎈 奇趣益智乐园</a>
      <span>·</span>
      <a href="global-news.html">🌍 全球新闻视角雷达</a>
      <span>·</span>
      <a href="https://0101.click">🏠 0101.click 门户</a>
    </div>
    <p>© 2026 全球企业技术博客雷达 · 遵循纯前端自包含架构 · 灵感源自 gihyo.jp 博客聚合生态</p>
  </footer>

  <!-- 悬浮通知 Toast -->
  <div class="toast" id="toast">已复制到剪贴板</div>

  <script>
    // 1. 内置静态精选数据打底 (Level 0: 保证完全无网络/接口异常也能秒开展示全部导航与文章)
    const BUILTIN_DATA = ''' + json_seed + ''';

    // 状态管理
    let currentBlogs = JSON.parse(JSON.stringify(BUILTIN_DATA.blogs));
    let activeCategory = 'all';
    let isSyncingAll = false;

    // 主题切换管理
    function initTheme() {
      const savedTheme = localStorage.getItem('app_theme');
      if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
      } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
      }
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme');
      const target = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', target);
      localStorage.setItem('app_theme', target);
    }

    initTheme();

    function updateCategoryCounts() {
      const allCount = currentBlogs.length;
      const japanCount = currentBlogs.filter(b => b.category === 'japan').length;
      const koreaCount = currentBlogs.filter(b => b.category === 'korea').length;
      const chinaCount = currentBlogs.filter(b => b.category === 'china').length;
      const globalCount = currentBlogs.filter(b => b.category === 'global').length;

      const elAll = document.getElementById('countAll'); if (elAll) elAll.textContent = allCount;
      const elJp = document.getElementById('countJapan'); if (elJp) elJp.textContent = japanCount;
      const elKr = document.getElementById('countKorea'); if (elKr) elKr.textContent = koreaCount;
      const elCn = document.getElementById('countChina'); if (elCn) elCn.textContent = chinaCount;
      const elGl = document.getElementById('countGlobal'); if (elGl) elGl.textContent = globalCount;
    }

    // 格式化日期显示
    function formatDisplayDate(dateStr) {
      if (!dateStr) return '近期';
      const d = new Date(dateStr);
      if (isNaN(d.getTime())) return dateStr;
      
      const now = new Date();
      const diffMs = now - d;
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

      if (diffDays === 0) return '今天';
      if (diffDays === 1) return '昨天';
      if (diffDays > 1 && diffDays < 30) return diffDays + '天前';
      
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return year + '-' + month + '-' + day;
    }

    // 渲染卡片
    function renderBlogs(blogsList) {
      const grid = document.getElementById('blogsGrid');
      if (!blogsList || blogsList.length === 0) {
        grid.innerHTML = `
          <div class="empty-state">
            <h3>🔍 没有找到匹配的技术博客</h3>
            <p>可尝试精简关键字或切换到“全部”分类。</p>
          </div>
        `;
        return;
      }

      grid.innerHTML = blogsList.map(blog => {
        const catMap = {
          japan: { label: '🇯🇵 日本名企', cls: 'japan' },
          korea: { label: '🇰🇷 韩国团队', cls: 'korea' },
          china: { label: '🇨🇳 国内前沿', cls: 'china' },
          global: { label: '🌐 全球巨头', cls: 'global' }
        };
        const catInfo = catMap[blog.category] || { label: '科技团队', cls: '' };

        // 状态徽章判定
        let statusBadge = '<span class="status-badge static">📦 内置精选</span>';
        if (blog._source === 'live') {
          statusBadge = '<span class="status-badge live">🟢 实时更新</span>';
        } else if (blog._source === 'ci') {
          statusBadge = '<span class="status-badge ci">⚡ CI 预构建</span>';
        } else if (blog._loading) {
          statusBadge = '<span class="status-badge loading">⏳ 同步中...</span>';
        }

        // 标签渲染
        const tagsHtml = (blog.tags || []).map(t => 
          `<span class="tech-tag" onclick="selectTag('${t}')">${t}</span>`
        ).join('');

        // 文章列表渲染 (展示前 3~5 篇)
        const articles = (blog.articles || []).slice(0, 5);
        let articlesHtml = '';
        if (articles.length === 0) {
          articlesHtml = '<li class="article-item" style="color:var(--text-light);font-size:12px;">暂无抓取文章，可点击下方刷新重试</li>';
        } else {
          articlesHtml = articles.map(art => `
            <li class="article-item">
              <div class="article-meta">
                <span class="article-date">${formatDisplayDate(art.pubDate)}</span>
              </div>
              <a href="${art.link}" class="article-link" target="_blank" rel="noopener noreferrer" title="${art.title}">
                ${art.title}
              </a>
            </li>
          `).join('');
        }

        return `
          <div class="blog-card" id="card-${blog.id}" data-id="${blog.id}">
            <div class="card-head">
              <div class="blog-icon">${blog.icon || '💻'}</div>
              <div class="blog-title-area">
                <a href="${blog.url}" target="_blank" rel="noopener noreferrer" class="blog-name-link" title="前往 ${blog.name} 官网">
                  ${blog.name}
                </a>
                <div class="blog-meta-tags">
                  <span class="cat-badge ${catInfo.cls}">${catInfo.label}</span>
                  ${statusBadge}
                </div>
              </div>
            </div>

            <p class="blog-desc">${blog.desc || '知名工程技术团队官方博客。'}</p>

            <div class="tech-tags">${tagsHtml}</div>

            <div class="articles-container">
              <div class="articles-header">
                <span class="articles-title">📰 最新动态文章</span>
                <span class="article-count">${articles.length} 篇</span>
              </div>
              <ul class="article-list">
                ${articlesHtml}
              </ul>
            </div>

            <div class="card-foot">
              <a href="${blog.url}" target="_blank" rel="noopener noreferrer" class="btn-foot">
                <span>🔗 官网</span>
              </a>
              <div class="foot-btn-group">
                <button class="btn-foot" onclick="copyRss('${blog.feedUrl}')" title="复制 RSS 订阅地址">
                  <span>📋 复制 RSS</span>
                </button>
                <button class="btn-foot" onclick="refreshSingleBlog('${blog.id}')" title="通过代理单项重新拉取">
                  <span>🔄 刷新</span>
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    // 分类筛选
    function setCategory(cat) {
      activeCategory = cat;
      document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.classList.toggle('active', tab.getAttribute('data-cat') === cat);
      });
      filterBlogs();
    }

    // 标签快速检索
    function selectTag(tag) {
      document.getElementById('searchInput').value = tag;
      filterBlogs();
    }

    // 关键字搜索过滤
    function filterBlogs() {
      const query = (document.getElementById('searchInput').value || '').trim().toLowerCase();

      let filtered = currentBlogs.filter(blog => {
        const matchCat = (activeCategory === 'all') || (blog.category === activeCategory);
        if (!matchCat) return false;

        if (!query) return true;

        const inName = blog.name.toLowerCase().includes(query);
        const inDesc = (blog.desc || '').toLowerCase().includes(query);
        const inTags = (blog.tags || []).some(t => t.toLowerCase().includes(query));
        const inArticles = (blog.articles || []).some(a => (a.title || '').toLowerCase().includes(query));

        return inName || inDesc || inTags || inArticles;
      });

      // 排序处理
      const sortMode = document.getElementById('sortSelect').value;
      if (sortMode === 'newest') {
        filtered.sort((a, b) => {
          const dateA = a.articles && a.articles[0] ? new Date(a.articles[0].pubDate).getTime() : 0;
          const dateB = b.articles && b.articles[0] ? new Date(b.articles[0].pubDate).getTime() : 0;
          return dateB - dateA;
        });
      }

      renderBlogs(filtered);
    }

    function applySorting() {
      filterBlogs();
    }

    // 复制 RSS
    function copyRss(url) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(() => {
          showToast('✅ RSS 订阅源已复制到剪贴板！');
        }).catch(() => {
          fallbackCopy(url);
        });
      } else {
        fallbackCopy(url);
      }
    }

    function fallbackCopy(url) {
      const input = document.createElement('input');
      input.value = url;
      document.body.appendChild(input);
      input.select();
      document.execCommand('copy');
      document.body.removeChild(input);
      showToast('✅ RSS 订阅源已复制到剪贴板！');
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => {
        toast.classList.remove('show');
      }, 2400);
    }

    // 2. 检查本地静态预聚合 JSON (Level 1: CI/CD 输出的 data/tech-blogs.json)
    async function tryLoadCIPrebuiltData() {
      try {
        const resp = await fetch('data/tech-blogs.json?_t=' + Date.now());
        if (resp.ok) {
          const remoteData = await resp.json();
          if (remoteData && remoteData.blogs && remoteData.blogs.length > 0) {
            // 合并并更新数据
            const remoteMap = new Map(remoteData.blogs.map(b => [b.id, b]));
            currentBlogs.forEach(blog => {
              if (remoteMap.has(blog.id)) {
                const rBlog = remoteMap.get(blog.id);
                if (rBlog.articles && rBlog.articles.length > 0) {
                  blog.articles = rBlog.articles;
                  blog._source = 'ci';
                }
              }
            });
            console.log('⚡ 成功加载 CI 预聚合静态 JSON 数据');
            updateCategoryCounts();
            filterBlogs();
          }
        }
      } catch (e) {
        console.log('ℹ️ 未检测到外部 CI JSON 文件，保持 Level 0 内置精选数据。', e);
      }
    }

    // 3. 运行时多代理异步抓取引擎 (Level 2: 浏览器直连或多代理容灾)
    // 代理候选池
    const PROXY_CANDIDATES = [
      url => `https://api.allorigins.win/get?url=${encodeURIComponent(url)}`,
      url => `https://corsproxy.io/?url=${encodeURIComponent(url)}`,
      url => `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(url)}`
    ];

    // RSS / Atom XML 浏览器端解析函数
    function parseRssXml(xmlText) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(xmlText, 'text/xml');
      const articles = [];

      // 判断是 Atom 还是 RSS 2.0
      const entries = doc.querySelectorAll('entry');
      if (entries.length > 0) {
        // Atom
        entries.forEach(entry => {
          if (articles.length >= 5) return;
          const title = (entry.querySelector('title')?.textContent || '').trim();
          let link = '';
          const linkEl = entry.querySelector('link[rel="alternate"]') || entry.querySelector('link');
          if (linkEl) {
            link = linkEl.getAttribute('href') || linkEl.textContent;
          }
          const dateEl = entry.querySelector('published') || entry.querySelector('updated');
          const dateStr = dateEl ? dateEl.textContent : '';
          let pubDate = '';
          if (dateStr) {
            pubDate = dateStr.slice(0, 10);
          }

          if (title && link) {
            articles.push({ title, link, pubDate });
          }
        });
      } else {
        // RSS 2.0
        const items = doc.querySelectorAll('item');
        items.forEach(item => {
          if (articles.length >= 5) return;
          const title = (item.querySelector('title')?.textContent || '').trim();
          let link = (item.querySelector('link')?.textContent || '').trim();
          if (!link) {
            const guid = item.querySelector('guid')?.textContent || '';
            if (guid.startsWith('http')) link = guid;
          }
          const pubDateEl = item.querySelector('pubDate');
          let pubDate = '';
          if (pubDateEl && pubDateEl.textContent) {
            const d = new Date(pubDateEl.textContent);
            if (!isNaN(d.getTime())) {
              pubDate = d.toISOString().slice(0, 10);
            }
          }

          if (title && link) {
            articles.push({ title, link, pubDate });
          }
        });
      }

      return articles;
    }

    // 单个 Feed 抓取 (依次尝试代理)
    async function fetchFeedWithFallback(feedUrl) {
      // 检查 LocalStorage 缓存 (1小时内有效)
      const cacheKey = 'tb_feed_' + btoa(feedUrl).slice(0, 32);
      const cached = localStorage.getItem(cacheKey);
      if (cached) {
        try {
          const parsed = JSON.parse(cached);
          if (Date.now() - parsed.ts < 3600 * 1000 && parsed.articles && parsed.articles.length > 0) {
            return { articles: parsed.articles, fromCache: true };
          }
        } catch (e) {}
      }

      for (let i = 0; i < PROXY_CANDIDATES.length; i++) {
        const proxyGen = PROXY_CANDIDATES[i];
        const reqUrl = proxyGen(feedUrl);
        try {
          const controller = new AbortController();
          const timer = setTimeout(() => controller.abort(), 9000);
          const resp = await fetch(reqUrl, { signal: controller.signal });
          clearTimeout(timer);

          if (!resp.ok) continue;

          // 若是 rss2json，返回的是结构化 JSON
          if (reqUrl.includes('rss2json')) {
            const data = await resp.json();
            if (data && data.items && data.items.length > 0) {
              const articles = data.items.slice(0, 5).map(it => ({
                title: it.title,
                link: it.link,
                pubDate: (it.pubDate || '').slice(0, 10)
              }));
              localStorage.setItem(cacheKey, JSON.stringify({ ts: Date.now(), articles }));
              return { articles, fromCache: false };
            }
          } else if (reqUrl.includes('allorigins')) {
            const data = await resp.json();
            if (data && data.contents) {
              const articles = parseRssXml(data.contents);
              if (articles.length > 0) {
                localStorage.setItem(cacheKey, JSON.stringify({ ts: Date.now(), articles }));
                return { articles, fromCache: false };
              }
            }
          } else {
            // 直接 text
            const text = await resp.text();
            const articles = parseRssXml(text);
            if (articles.length > 0) {
              localStorage.setItem(cacheKey, JSON.stringify({ ts: Date.now(), articles }));
              return { articles, fromCache: false };
            }
          }
        } catch (err) {
          // 尝试下一代理
          continue;
        }
      }

      throw new Error('All proxies failed for ' + feedUrl);
    }

    // 单个博客独立刷新
    async function refreshSingleBlog(blogId) {
      const blog = currentBlogs.find(b => b.id === blogId);
      if (!blog) return;

      blog._loading = true;
      filterBlogs();
      showToast('🔄 正在拉取 ' + blog.name + ' 最新文章...');

      try {
        const res = await fetchFeedWithFallback(blog.feedUrl);
        if (res && res.articles && res.articles.length > 0) {
          blog.articles = res.articles;
          blog._source = 'live';
          showToast('✅ ' + blog.name + ' 最新文章已更新！');
        }
      } catch (e) {
        showToast('⚠️ 实时拉取超时，已保留静态精选数据。');
      } finally {
        blog._loading = false;
        filterBlogs();
      }
    }

    // 一键并发受控同步所有博客
    async function syncAllLiveFeeds() {
      if (isSyncingAll) return;
      isSyncingAll = true;

      const syncBtn = document.getElementById('syncAllBtn');
      const progressContainer = document.getElementById('progressContainer');
      const progressBarFill = document.getElementById('progressBarFill');
      const progressStatusText = document.getElementById('progressStatusText');
      const progressCountText = document.getElementById('progressCountText');

      syncBtn.disabled = true;
      document.getElementById('syncBtnText').textContent = '同步中...';
      progressContainer.style.display = 'block';

      let completedCount = 0;
      const total = currentBlogs.length;

      // 并发池控制（限制最大 3 个请求同时跑，避免请求风暴与限流）
      const queue = [...currentBlogs];
      const concurrency = 3;

      async function worker() {
        while (queue.length > 0) {
          const blog = queue.shift();
          progressStatusText.textContent = '正在获取：' + blog.name + '...';
          blog._loading = true;

          try {
            const res = await fetchFeedWithFallback(blog.feedUrl);
            if (res && res.articles && res.articles.length > 0) {
              blog.articles = res.articles;
              blog._source = 'live';
            }
          } catch (e) {
            // 保留原有数据
          } finally {
            blog._loading = false;
            completedCount++;
            const pct = Math.round((completedCount / total) * 100);
            progressBarFill.style.width = pct + '%';
            progressCountText.textContent = completedCount + ' / ' + total;
            updateCategoryCounts();
            filterBlogs();
          }
        }
      }

      const workers = Array(concurrency).fill(null).map(() => worker());
      await Promise.all(workers);

      isSyncingAll = false;
      syncBtn.disabled = false;
      document.getElementById('syncBtnText').textContent = '一键实时同步动态';
      progressStatusText.textContent = '🎉 全量博客动态同步完成！';
      showToast('🎉 全部 ' + total + ' 家博客动态已完成同步！');

      setTimeout(() => {
        progressContainer.style.display = 'none';
        progressBarFill.style.width = '0%';
      }, 3500);
    }

    // 页面加载启动序列
    document.addEventListener('DOMContentLoaded', () => {
      // Step 1: 毫秒级直接渲染 Level 0 内置精选打底数据 (零白屏、零加载等待)
      updateCategoryCounts();
      renderBlogs(currentBlogs);

      // Step 2: 异步尝试拉取 Level 1 CI 预构建 JSON
      tryLoadCIPrebuiltData();
    });
  </script>

<div class="site-legal-0101" style="clear:both;width:100%;box-sizing:border-box;padding:16px 12px 20px;text-align:center;font:12px/1.7 system-ui,sans-serif;color:#64748b;opacity:.9"><a href="https://0101.click/privacy.html" style="color:inherit;text-decoration:underline;opacity:.85">隐私政策 / プライバシー</a> · <a href="https://0101.click/about.html" style="color:inherit;text-decoration:underline;opacity:.85">关于 / 運営者情報</a> · <a href="https://0101.click/contact.html" style="color:inherit;text-decoration:underline;opacity:.85">联系 / お問い合わせ</a> · <a href="https://0101.click/" style="color:inherit;text-decoration:underline;opacity:.85">0101.click</a></div>
</body>
</html>
'''

with open('tech-blogs.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✅ tech-blogs.html generated successfully!")
