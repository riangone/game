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
  <script src="js/consent-default.js"></script>
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
  <meta name="description" content="汇聚 LINE、Mercari、ZOZO、Pixiv、日本经济新闻 (Nikkei)、IIJ、富士通研究所、MIXI、GMO Pepabo 等 gihyo.jp 全部收录企业、NAVER、Kakao、Toss、Coupang、美团、有赞、云风、Draveness、EMQX、APISIX、Doris、CoolShell、Cloudflare、GitHub 等 73 家中日韩及全球顶尖科技企业技术博客。只收录各博客文章的标题、日期和原文链接，由本站服务器每 3 小时抓取官方 RSS 更新。">
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
    <!-- og+ld (#43) -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="0101.click 实用工具箱">
    <meta property="og:title" content="中日韩与全球企业技术博客雷达 · 工程前沿 RSS 聚合平台">
    <meta property="og:description" content="汇聚 LINE、Mercari、ZOZO、Pixiv、日本经济新闻 (Nikkei)、IIJ、富士通研究所、MIXI、GMO Pepabo 等 gihyo.jp 全部收录企业、NAVER、Kakao、Toss、Coupang、美团、有赞、云风、Draveness、EMQX、APISIX、Doris、CoolShell、Cloudflare、GitHub 等 73 家中日韩及全球顶尖科技企业技术博客。只收录各博客文章的标题、日期和原文链接，由本站服务器每 3 小时抓取官方 RSS 更新。">
    <meta property="og:url" content="https://tool.0101.click/tech-blogs.html">
    <meta property="og:image" content="https://tool.0101.click/assets/og/tech-blogs.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="企业技术博客雷达">
    <meta property="og:locale" content="zh_CN">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "WebApplication",
   "name": "企业技术博客雷达",
   "url": "https://tool.0101.click/tech-blogs.html",
   "description": "汇聚 LINE、Mercari、ZOZO、Pixiv、日本经济新闻 (Nikkei)、IIJ、富士通研究所、MIXI、GMO Pepabo 等 gihyo.jp 全部收录企业、NAVER、Kakao、Toss、Coupang、美团、有赞、云风、Draveness、EMQX、APISIX、Doris、CoolShell、Cloudflare、GitHub 等 73 家中日韩及全球顶尖科技企业技术博客。只收录各博客文章的标题、日期和原文链接，由本站服务器每 3 小时抓取官方 RSS 更新。",
   "applicationCategory": "ReferenceApplication",
   "operatingSystem": "Any",
   "browserRequirements": "Requires JavaScript",
   "inLanguage": "zh-CN",
   "image": "https://tool.0101.click/assets/og/tech-blogs.png"
  },
  {
   "@type": "BreadcrumbList",
   "itemListElement": [
    {
     "@type": "ListItem",
     "position": 1,
     "name": "工具箱",
     "item": "https://tool.0101.click/"
    },
    {
     "@type": "ListItem",
     "position": 2,
     "name": "企业技术博客雷达",
     "item": "https://tool.0101.click/tech-blogs.html"
    }
   ]
  }
 ]
}
    </script>
    <link rel="stylesheet" href="css/tools-header.css">
  <script src="js/pwa-register.js"></script>
</head>
<body>

  <!-- 顶部导航 -->
    <!-- 统一小工具顶部导航 -->
  <header class="app-header">
    <div class="header-left">
      <a href="tools.html" class="back-link" title="返回实用工具箱">
        <span class="back-icon">←</span>
        <span class="back-text">工具箱</span>
      </a>
      <div class="app-brand">
        <span class="brand-icon">📡</span>
        <span class="brand-title">企业技术博客雷达</span>
        <span class="badge-sub" style="font-size:11px;font-weight:600;padding:2px 7px;border-radius:9999px;background:var(--primary-subtle);color:var(--primary);border:1px solid var(--border-color);">73家名企</span>
      </div>
    </div>
    <div class="header-right">
      <a href="index.html" class="hall-btn" title="返回游戏大厅">
        <span class="hall-icon">🎮</span>
        <span class="hall-text">大厅</span>
      </a>
      <select class="tool-switch" onchange="if(this.value) location.href=this.value;" title="快速切换小工具">
        <option value="">🔀 快捷切换小工具...</option>
        <optgroup label="常用必备">
          <option value="calculator.html">🧮 表达式计算器</option>
          <option value="notepad.html">📝 极简便签</option>
          <option value="unit-converter.html">📐 全能单位换算器</option>
          <option value="currency.html">💱 全球实时汇率换算</option>
          <option value="weather.html">🌤️ 极简实时天气看板</option>
          <option value="qrcode.html">📱 二维码大师</option>
          <option value="pomodoro.html">🍅 极简番茄时钟</option>
          <option value="calendar.html">📅 万年历与节气</option>
        </optgroup>
        <optgroup label="文本与开发">
          <option value="markdown-editor.html">📑 Markdown 排版工坊</option>
          <option value="text-tools.html">🔤 文本综合工具箱</option>
          <option value="diff-tool.html">🪞 文本差异对比</option>
          <option value="json-csv-tool.html">🔄 JSON / CSV 互转工坊</option>
          <option value="hash-tool.html">#️⃣ 哈希校验工具</option>
          <option value="encrypt-tool.html">🛡️ 本地加解密工具</option>
          <option value="uuid-generator.html">🆔 唯一标识符生成器</option>
          <option value="cron-parser.html">⏰ Cron 表达式工坊</option>
          <option value="css-generator.html">🎨 现代 CSS 视觉工坊</option>
          <option value="github-card.html">🐙 GitHub 开发者名片工坊</option>
        </optgroup>
        <optgroup label="图形与多媒体">
          <option value="image-tool.html">🖼️ 本地图片工坊</option>
          <option value="image-grid-splitter.html">🧩 九宫格切图工坊</option>
          <option value="img-to-pdf.html">📄 图片转 PDF</option>
          <option value="drawing-board.html">🖌️ 简易画板</option>
          <option value="color-tool.html">🎨 颜色转换工具箱</option>
          <option value="favicon-generator.html">🌐 Favicon 图标生成器</option>
          <option value="ascii-art.html">🔤 字符画与 ASCII 艺术字</option>
          <option value="font-previewer.html">🔤 字体预览工坊</option>
          <option value="quote-card.html">🖋️ 一言·灵感排版工坊</option>
          <option value="metronome.html">⏱️ 电子节拍器与律动鼓机</option>
        </optgroup>
        <optgroup label="日常与生活">
          <option value="todolist.html">✅ 极简待办清单</option>
          <option value="expense-tracker.html">💰 极简记账本</option>
          <option value="habit-tracker.html">🔥 习惯打卡</option>
          <option value="countdown.html">⏳ 倒数日与纪念日</option>
          <option value="time-tool.html">🕐 世界时间工具箱</option>
          <option value="loan-calculator.html">🏦 贷款与房贷计算器</option>
          <option value="tip-calculator.html">🧾 账单 AA 分摊与小费</option>
          <option value="password.html">🔐 安全密码工坊</option>
          <option value="packing-list.html">🧳 旅行与出差行李清单</option>
          <option value="random-picker.html">🎯 随机抉择与抽奖转盘</option>
          <option value="bmi-tracker.html">⚖️ BMI 与健康指标追踪</option>
          <option value="water-reminder.html">💧 喝水打卡与健康提醒</option>
        </optgroup>
        <optgroup label="资讯与探索">
          <option value="country-explorer.html">🌍 世界地理大百科</option>
          <option value="global-news.html">🌍 全球新闻视角雷达</option>
          <option value="tech-blogs.html" selected>📡 企业技术博客雷达</option>
          <option value="network-info.html">🌐 网络信息查询探针</option>
          <option value="doh-lookup.html">🔍 浏览器原生 DNS 探针</option>
        </optgroup>
      </select>
      <button class="theme-btn" onclick="toggleTheme()" id="themeBtn" title="切换深色/浅色模式">🌓</button>
    </div>
  </header>

  <!-- 主体内容 -->
  <main class="container">

    <!-- Hero 介绍 -->
    <section class="hero-banner">
      <h2 class="hero-title">中日韩与全球知名科技企业 <span>技术博客与前沿雷达</span></h2>
      <p class="hero-desc">
        本站服务器每 3 小时抓取一次各博客的官方 RSS，只保存文章标题、日期和原文链接，点击后到原站阅读全文。追踪来自 NAVER、Kakao、Toss、Coupang、LINE/Yahoo、Mercari、ZOZO、Pixiv、日本经济新闻 (Nikkei)、IIJ、富士通研究所、MIXI、GMO Pepabo 等 gihyo.jp 全部收录企业、Cloudflare、GitHub、Netflix、美团、有赞、云风、Draveness、EMQX、APISIX、Doris、CoolShell 等 73 家顶尖团队的一线实战演进。
      </p>

      <!-- 架构特性徽章 -->
      <div class="feature-pills">
        <div class="feature-pill"><span class="icon">📦</span> 内置精选离线兜底 (0ms 秒开)</div>
        <div class="feature-pill"><span class="icon">⚡</span> 服务器每 3 小时抓取官方 RSS</div>
        <div class="feature-pill"><span class="icon">🔗</span> 只存标题 · 日期 · 原文链接</div>
        <div class="feature-pill"><span class="icon">🔒</span> 浏览器不连接第三方代理</div>
      </div>

      <!-- 架构设计折叠栏 -->
      <details class="arch-details">
        <summary class="arch-summary">
          <span>🏛️ 点击查看：系统架构演进路线与多级容灾设计规范</span>
        </summary>
        <div class="arch-content">
          <div class="arch-item">
            <strong>Level 0: DOM 内置种子打底</strong>
            页面打包时已预置完整博客元数据与最新文章精选。弱网或断网时也能正常浏览和跳转。
          </div>
          <div class="arch-item">
            <strong>Level 1: 服务器定时抓取的静态 JSON</strong>
            本站服务器用 <code>scripts/update_tech_blogs.py</code> 每 3 小时直接抓取各博客官方 RSS，只保存标题、日期和原文链接，生成 <code>data/tech-blogs.json</code> 静态分发。
          </div>
          <div class="arch-item">
            <strong>Level 2: 手动重新载入</strong>
            点「重新载入最新数据」只会重新读取本站的 <code>data/tech-blogs.json</code>，浏览器不直接访问 RSS 源，也不经过任何第三方代理。
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
        <button class="filter-tab active" data-cat="all" onclick="setCategory('all')">全部 (<span id="countAll">73</span>)</button>
        <button class="filter-tab" data-cat="japan" onclick="setCategory('japan')">🇯🇵 日本名企 (<span id="countJapan">41</span>)</button>
        <button class="filter-tab" data-cat="korea" onclick="setCategory('korea')">🇰🇷 韩国团队 (<span id="countKorea">7</span>)</button>
        <button class="filter-tab" data-cat="global" onclick="setCategory('global')">🌐 全球巨头 (<span id="countGlobal">7</span>)</button>
        <button class="filter-tab" data-cat="china" onclick="setCategory('china')">🇨🇳 国内团队 (<span id="countChina">18</span>)</button>
      </div>

      <div class="action-controls">
        <select class="select-sort" id="sortSelect" onchange="applySorting()">
          <option value="default">默认推荐顺序</option>
          <option value="newest">按文章最新发布时间</option>
        </select>

        <button class="btn-action-primary" id="syncAllBtn" onclick="syncAllLiveFeeds()">
          <span id="syncBtnIcon">🔄</span>
          <span id="syncBtnText">重新载入最新数据</span>
        </button>
      </div>
    </div>

    <!-- 实时拉取进度面板 -->
    <div class="progress-container" id="progressContainer">
      <div class="progress-header">
        <span id="progressStatusText">正在读取本站最新数据...</span>
        <span id="progressCountText">0 / 73</span>
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
          statusBadge = '<span class="status-badge live">🟢 已刷新</span>';
        } else if (blog._source === 'ci') {
          statusBadge = '<span class="status-badge ci">⚡ 服务器抓取</span>';
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
                <button class="btn-foot" onclick="refreshSingleBlog('${blog.id}')" title="重新读取本站最新数据">
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

    // 以服务器快照为准合并：已有博客更新元数据与文章，快照中新增的博客直接追加
    // （避免 BUILTIN_DATA 未重建时，新接入的博客在前端被静默丢弃）
    function mergeServerBlogs(remoteBlogs, source) {
      const localMap = new Map(currentBlogs.map(b => [b.id, b]));
      remoteBlogs.forEach(rBlog => {
        const hasArticles = rBlog.articles && rBlog.articles.length > 0;
        const local = localMap.get(rBlog.id);
        if (local) {
          ['name', 'category', 'url', 'feedUrl', 'icon', 'desc', 'tags'].forEach(k => {
            if (rBlog[k] !== undefined) local[k] = rBlog[k];
          });
          if (hasArticles) {
            local.articles = rBlog.articles;
            local._source = source;
          }
        } else {
          const nb = JSON.parse(JSON.stringify(rBlog));
          nb.articles = nb.articles || [];
          if (hasArticles) nb._source = source;
          currentBlogs.push(nb);
        }
      });
    }

    // 2. 检查本地静态预聚合 JSON (Level 1: 服务器定时抓取输出的 data/tech-blogs.json)
    async function tryLoadCIPrebuiltData() {
      try {
        const resp = await fetch('data/tech-blogs.json?_t=' + Date.now());
        if (resp.ok) {
          const remoteData = await resp.json();
          if (remoteData && remoteData.blogs && remoteData.blogs.length > 0) {
            mergeServerBlogs(remoteData.blogs, 'ci');
            console.log('⚡ 成功加载 CI 预聚合静态 JSON 数据');
            updateCategoryCounts();
            filterBlogs();
          }
        }
      } catch (e) {
        console.log('ℹ️ 未检测到外部 CI JSON 文件，保持 Level 0 内置精选数据。', e);
      }
    }

    // 3. 手动刷新：只重新读取本站服务器定时抓取生成的 data/tech-blogs.json
    //    （浏览器不直连 RSS 源，也不经过任何第三方代理；JSON 只含标题、日期和原文链接）
    let serverSnapshotPromise = null;
    function loadServerSnapshot() {
      if (!serverSnapshotPromise) {
        serverSnapshotPromise = fetch('data/tech-blogs.json?_t=' + Date.now())
          .then(resp => {
            if (!resp.ok) throw new Error('HTTP ' + resp.status);
            return resp.json();
          })
          .finally(() => setTimeout(() => { serverSnapshotPromise = null; }, 60000));
      }
      return serverSnapshotPromise;
    }

    // 单个 Feed：从服务器快照里取对应博客的文章
    async function fetchFeedWithFallback(feedUrl, blogId) {
      const data = await loadServerSnapshot();
      const blogs = data.blogs || [];
      const blog = blogs.find(b => blogId && b.id === blogId) || blogs.find(b => b.feedUrl === feedUrl);
      if (!blog || !blog.articles || blog.articles.length === 0) {
        throw new Error('No server snapshot for ' + feedUrl);
      }
      return { articles: blog.articles, fromCache: false };
    }

    // 单个博客独立刷新
    async function refreshSingleBlog(blogId) {
      const blog = currentBlogs.find(b => b.id === blogId);
      if (!blog) return;

      blog._loading = true;
      filterBlogs();
      showToast('🔄 正在读取 ' + blog.name + ' 最新文章...');

      try {
        const res = await fetchFeedWithFallback(blog.feedUrl, blog.id);
        if (res && res.articles && res.articles.length > 0) {
          blog.articles = res.articles;
          blog._source = 'live';
          showToast('✅ ' + blog.name + ' 最新文章已更新！');
        }
      } catch (e) {
        showToast('⚠️ 读取最新数据失败，已保留现有内容。');
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

      // 先把服务器快照里新增的博客并入列表（只请求一次快照）
      try {
        const snap = await loadServerSnapshot();
        if (snap && snap.blogs) mergeServerBlogs(snap.blogs, 'live');
      } catch (e) { /* 快照不可用时保留现有内容 */ }

      let completedCount = 0;
      const total = currentBlogs.length;

      // 并发池（数据都来自同一份服务器快照，实际只请求一次）
      const queue = [...currentBlogs];
      const concurrency = 3;

      async function worker() {
        while (queue.length > 0) {
          const blog = queue.shift();
          progressStatusText.textContent = '正在获取：' + blog.name + '...';
          blog._loading = true;

          try {
            const res = await fetchFeedWithFallback(blog.feedUrl, blog.id);
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
      document.getElementById('syncBtnText').textContent = '重新载入最新数据';
      progressStatusText.textContent = '🎉 已载入最新数据！';
      showToast('🎉 已载入 ' + total + ' 家博客的最新数据');

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
