#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for global-news.html
Generates a standalone, beautiful Jamstack application with embedded Level 0 seed data.
"""

import os
import json

def generate_page():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "global-news.json")
    with open(data_path, "r", encoding="utf-8") as f:
        news_data = json.load(f)

    json_str = json.dumps(news_data, ensure_ascii=False, indent=2)

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-Y1P7PMMM6V"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-Y1P7PMMM6V');
  </script>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>中日韩美·全球新闻视角雷达 · 24家权威大报多重视角对比</title>
  <meta name="description" content="汇聚中日韩美 24 家权威主流通讯社与顶级大报（新华社、澎湃、NHK、日经、朝日、韩联社、朝鲜日报、纽约时报、华尔街日报、CNN等）。三重视图：四国多栏对照看板、全球即时时钟时间线、机构全景矩阵。">
  <meta name="theme-color" content="#0284c7">

  <style>
    :root {{
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

      --color-cn: #dc2626;
      --color-cn-subtle: #fee2e2;
      --color-cn-border: #fca5a5;

      --color-jp: #ea580c;
      --color-jp-subtle: #ffedd5;
      --color-jp-border: #fdba74;

      --color-kr: #2563eb;
      --color-kr-subtle: #dbeafe;
      --color-kr-border: #93c5fd;

      --color-us: #7c3aed;
      --color-us-subtle: #ede9fe;
      --color-us-border: #c4b5fd;

      --success: #10b981;
      --success-subtle: #d1fae5;
      --warning: #f59e0b;
      --warning-subtle: #fef3c7;

      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-pill: 9999px;

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
      --shadow-lg: 0 12px 24px -4px rgba(15, 23, 42, 0.08), 0 4px 12px -2px rgba(15, 23, 42, 0.04);
      --shadow-hover: 0 18px 28px -6px rgba(15, 23, 42, 0.12), 0 6px 12px -3px rgba(15, 23, 42, 0.06);

      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    }}

    [data-theme="dark"] {{
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

      --color-cn: #f87171;
      --color-cn-subtle: rgba(239, 68, 68, 0.2);
      --color-cn-border: #b91c1c;

      --color-jp: #fb923c;
      --color-jp-subtle: rgba(249, 115, 22, 0.2);
      --color-jp-border: #c2410c;

      --color-kr: #60a5fa;
      --color-kr-subtle: rgba(37, 99, 235, 0.2);
      --color-kr-border: #1d4ed8;

      --color-us: #a78bfa;
      --color-us-subtle: rgba(124, 58, 237, 0.2);
      --color-us-border: #6d28d9;

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
      --shadow-lg: 0 12px 24px -4px rgba(0, 0, 0, 0.6);
      --shadow-hover: 0 20px 30px -6px rgba(0, 0, 0, 0.7);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.25s ease, color 0.25s ease;
      line-height: 1.5;
    }}

    /* 顶部导航 */
    .app-header {{
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
    }}

    .brand-group {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: inherit;
    }}

    .brand-icon {{
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
    }}

    .brand-text h1 {{
      font-size: 18px;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .brand-text p {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 1px;
    }}

    .badge-sub {{
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: var(--radius-pill);
      background: var(--primary-subtle);
      color: var(--primary);
      border: 1px solid var(--primary-border);
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .btn-nav {{
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
    }}

    .btn-nav:hover {{
      background: var(--primary-subtle);
      border-color: var(--primary-border);
      color: var(--primary);
    }}

    .btn-icon-only {{
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
    }}

    .btn-icon-only:hover {{
      background: var(--primary-subtle);
      border-color: var(--primary-border);
    }}

    /* 容器 */
    .container {{
      max-width: 1480px;
      margin: 0 auto;
      padding: 24px 20px 60px;
      width: 100%;
      flex: 1;
    }}

    /* Hero Banner */
    .hero-banner {{
      background: linear-gradient(135deg, var(--bg-surface) 0%, var(--bg-subtle) 100%);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 28px 32px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
      position: relative;
      overflow: hidden;
    }}

    .hero-title {{
      font-size: 26px;
      font-weight: 900;
      color: var(--text-main);
      margin-bottom: 8px;
      letter-spacing: -0.02em;
      line-height: 1.3;
    }}

    .hero-title span {{
      background: linear-gradient(120deg, #dc2626, #ea580c, #2563eb, #7c3aed);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero-desc {{
      font-size: 14px;
      color: var(--text-muted);
      max-width: 860px;
      line-height: 1.6;
      margin-bottom: 18px;
    }}

    .feature-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 18px;
    }}

    .feature-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      font-size: 12px;
      font-weight: 600;
      border-radius: var(--radius-pill);
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-main);
    }}

    .feature-pill.cn {{ border-color: var(--color-cn-border); background: var(--color-cn-subtle); color: var(--color-cn); }}
    .feature-pill.jp {{ border-color: var(--color-jp-border); background: var(--color-jp-subtle); color: var(--color-jp); }}
    .feature-pill.kr {{ border-color: var(--color-kr-border); background: var(--color-kr-subtle); color: var(--color-kr); }}
    .feature-pill.us {{ border-color: var(--color-us-border); background: var(--color-us-subtle); color: var(--color-us); }}

    /* 状态与控制栏 */
    .status-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 18px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      font-size: 13px;
    }}

    .status-info {{
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: var(--radius-pill);
      font-size: 12px;
    }}

    .status-badge.seed {{ background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }}
    .status-badge.ci {{ background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }}
    .status-badge.live {{ background: #d1fae5; color: #047857; border: 1px solid #a7f3d0; }}

    .sync-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      background: var(--primary);
      color: #ffffff;
      border: none;
      border-radius: var(--radius-pill);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 2px 4px rgba(2, 132, 199, 0.25);
    }}

    .sync-btn:hover {{
      background: var(--primary-hover);
      transform: translateY(-1px);
    }}

    .sync-btn:disabled {{
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
    }}

    /* 控制面板 */
    .controls-panel {{
      margin: 20px 0;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .controls-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }}

    /* 视图切换 Tabs */
    .view-tabs {{
      display: flex;
      background: var(--bg-subtle);
      padding: 4px;
      border-radius: var(--radius-pill);
      border: 1px solid var(--border-color);
      gap: 4px;
    }}

    .view-tab {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 16px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      border: none;
      background: transparent;
      border-radius: var(--radius-pill);
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .view-tab.active {{
      background: var(--bg-surface);
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }}

    /* 搜索栏 */
    .search-box {{
      position: relative;
      flex: 1;
      max-width: 480px;
      min-width: 260px;
    }}

    .search-box input {{
      width: 100%;
      padding: 10px 38px 10px 38px;
      font-size: 14px;
      border-radius: var(--radius-pill);
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
      color: var(--text-main);
      outline: none;
      transition: all 0.2s ease;
    }}

    .search-box input:focus {{
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px var(--primary-subtle);
    }}

    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-light);
      font-size: 15px;
      pointer-events: none;
    }}

    .search-clear {{
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-light);
      cursor: pointer;
      font-size: 16px;
      display: none;
    }}

    .search-clear.visible {{
      display: block;
    }}

    /* 分类与国别过滤器 */
    .filters-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }}

    .filter-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 600;
      border-radius: var(--radius-pill);
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .filter-btn:hover {{
      border-color: var(--border-focus);
      color: var(--text-main);
    }}

    .filter-btn.active {{
      background: var(--primary);
      border-color: var(--primary);
      color: #ffffff;
    }}

    .filter-btn .count-badge {{
      padding: 1px 6px;
      border-radius: var(--radius-pill);
      background: rgba(0, 0, 0, 0.08);
      font-size: 10px;
    }}

    .filter-btn.active .count-badge {{
      background: rgba(255, 255, 255, 0.25);
    }}

    /* 同步进度条 */
    .progress-bar-container {{
      height: 4px;
      background: var(--bg-subtle);
      border-radius: 2px;
      overflow: hidden;
      margin-top: 10px;
      display: none;
    }}

    .progress-bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, #dc2626, #ea580c, #2563eb, #7c3aed);
      width: 0%;
      transition: width 0.3s ease;
    }}

    /* ========================================================
       视图 1: 四国多栏视角看板 (Perspective Columns Deck)
       ======================================================== */
    .perspective-deck {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      align-items: start;
    }}

    .deck-column {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .deck-column:hover {{
      box-shadow: var(--shadow-md);
    }}

    .column-header {{
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .column-header-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .column-title {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 16px;
      font-weight: 800;
    }}

    .column-count {{
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: var(--radius-pill);
    }}

    .deck-column.cn {{ border-top: 4px solid var(--color-cn); }}
    .deck-column.cn .column-count {{ background: var(--color-cn-subtle); color: var(--color-cn); }}
    .deck-column.jp {{ border-top: 4px solid var(--color-jp); }}
    .deck-column.jp .column-count {{ background: var(--color-jp-subtle); color: var(--color-jp); }}
    .deck-column.kr {{ border-top: 4px solid var(--color-kr); }}
    .deck-column.kr .column-count {{ background: var(--color-kr-subtle); color: var(--color-kr); }}
    .deck-column.us {{ border-top: 4px solid var(--color-us); }}
    .deck-column.us .column-count {{ background: var(--color-us-subtle); color: var(--color-us); }}

    .column-source-select {{
      width: 100%;
      padding: 6px 10px;
      font-size: 12px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
      background: var(--bg-subtle);
      color: var(--text-main);
      outline: none;
    }}

    .column-articles {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 14px;
      max-height: 800px;
      overflow-y: auto;
    }}

    /* 单条新闻项 (Card in column) */
    .news-item {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 12px 14px;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .news-item:hover {{
      border-color: var(--border-focus);
      transform: translateY(-2px);
      box-shadow: var(--shadow-sm);
    }}

    .news-meta {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      font-size: 11px;
    }}

    .news-source-tag {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-weight: 700;
      color: var(--text-muted);
    }}

    .news-time {{
      color: var(--text-light);
      white-space: nowrap;
    }}

    .news-title {{
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
      text-decoration: none;
      line-height: 1.45;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
      transition: color 0.15s ease;
    }}

    .news-title:hover {{
      color: var(--primary);
    }}

    .news-snippet {{
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.5;
      display: none;
      padding-top: 6px;
      border-top: 1px dashed var(--border-color);
    }}

    .news-snippet.open {{
      display: block;
    }}

    .news-actions {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 4px;
      padding-top: 6px;
      border-top: 1px solid var(--border-color);
      font-size: 11px;
    }}

    .news-action-btn {{
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 11px;
      padding: 2px 4px;
      border-radius: 4px;
      text-decoration: none;
      transition: color 0.15s ease;
    }}

    .news-action-btn:hover {{
      color: var(--primary);
      background: var(--primary-subtle);
    }}

    /* ========================================================
       视图 2: 全球即时时钟时间线 (Unified Timeline)
       ======================================================== */
    .timeline-container {{
      max-width: 960px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .timeline-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      gap: 16px;
      transition: all 0.2s ease;
      box-shadow: var(--shadow-sm);
    }}

    .timeline-card:hover {{
      border-color: var(--border-focus);
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }}

    .timeline-flag-box {{
      font-size: 28px;
      line-height: 1;
      display: flex;
      align-items: flex-start;
      padding-top: 2px;
    }}

    .timeline-content {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .timeline-meta {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 12px;
    }}

    .timeline-source {{
      font-weight: 700;
      color: var(--text-main);
    }}

    .timeline-title {{
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
      text-decoration: none;
      line-height: 1.4;
    }}

    .timeline-title:hover {{
      color: var(--primary);
    }}

    /* ========================================================
       视图 3: 机构全景矩阵 (Media Outlets Grid)
       ======================================================== */
    .media-matrix {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 18px;
    }}

    .media-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 18px 20px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: all 0.2s ease;
    }}

    .media-card:hover {{
      border-color: var(--border-focus);
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }}

    .media-card-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
    }}

    .media-info {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .media-icon {{
      font-size: 24px;
      width: 40px;
      height: 40px;
      border-radius: var(--radius-sm);
      background: var(--bg-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--border-color);
    }}

    .media-name {{
      font-size: 15px;
      font-weight: 800;
      color: var(--text-main);
    }}

    .media-desc {{
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    .media-articles-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      border-top: 1px solid var(--border-color);
      padding-top: 10px;
    }}

    .media-article-link {{
      font-size: 13px;
      color: var(--text-main);
      text-decoration: none;
      line-height: 1.4;
      display: flex;
      align-items: flex-start;
      gap: 6px;
      transition: color 0.15s ease;
    }}

    .media-article-link:hover {{
      color: var(--primary);
    }}

    .media-article-link::before {{
      content: "•";
      color: var(--primary);
      font-weight: bold;
    }}

    /* Toast */
    .toast {{
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
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 100;
      pointer-events: none;
    }}

    .toast.show {{
      transform: translateY(0);
      opacity: 1;
    }}

    /* Footer */
    .footer {{
      background: var(--bg-surface);
      border-top: 1px solid var(--border-color);
      padding: 24px;
      text-align: center;
      font-size: 13px;
      color: var(--text-muted);
      margin-top: auto;
    }}

    .footer-links {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 12px;
    }}

    .footer-links a {{
      color: var(--text-muted);
      text-decoration: none;
      transition: color 0.2s ease;
    }}

    .footer-links a:hover {{
      color: var(--primary);
    }}

    /* 响应式适配 */
    @media (max-width: 1200px) {{
      .perspective-deck {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    @media (max-width: 768px) {{
      .perspective-deck {{
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        padding-bottom: 14px;
      }}
      .deck-column {{
        min-width: 300px;
        flex: 0 0 85%;
        scroll-snap-align: center;
      }}
      .hero-title {{
        font-size: 20px;
      }}
      .hero-banner {{
        padding: 20px 18px;
      }}
    }}
  </style>
</head>
<body>

  <!-- 顶部导航 -->
  <header class="app-header">
    <a href="#" class="brand-group">
      <div class="brand-icon">🌍</div>
      <div class="brand-text">
        <h1>全球新闻视角雷达 <span class="badge-sub">中日韩美 · 24大报</span></h1>
        <p>Global News Perspectives Deck · 多重视角事实透镜</p>
      </div>
    </a>
    <div class="nav-actions">
      <a href="tools.html" class="btn-nav">🧰 返回工具箱</a>
      <a href="index.html" class="btn-nav">🎮 游戏大厅</a>
      <button class="btn-icon-only" onclick="toggleTheme()" title="切换明暗主题">🌓</button>
    </div>
  </header>

  <!-- 主体容器 -->
  <main class="container">

    <!-- 顶部 Banner -->
    <section class="hero-banner">
      <h2 class="hero-title">中日韩美 · <span>全球大报多重视角雷达</span></h2>
      <p class="hero-desc">
        同一时刻，世界如何被讲述？汇聚中、日、韩、美四方 24 家顶级通讯社与主流大报，打破单一语境的信息偏狭与推荐算法的信息茧房。
        采用三层容灾架构：内置种子离线秒开 + CI 静态预聚合快照 + 边缘代理实时同步。
      </p>

      <div class="feature-pills">
        <span class="feature-pill cn">🇨🇳 中国视角 (新华社 / 澎湃 / 界面 / FT中文 / 人民网)</span>
        <span class="feature-pill jp">🇯🇵 日本視点 (NHK 主要 / NHK 国际 / 日经 / 朝日 / Yahoo! Japan)</span>
        <span class="feature-pill kr">🇰🇷 한국 시선 (韩联社中文 / 韩联社韩语 / 朝鲜日报 / 东亚日报)</span>
        <span class="feature-pill us">🇺🇸 美欧全球 (纽约时报 / 华尔街日报 / CNN / NPR / BBC)</span>
      </div>

      <!-- 状态与同步条 -->
      <div class="status-bar">
        <div class="status-info">
          <span class="status-badge live" id="statusBadge">⚡ CI 预构建快照</span>
          <span id="statSummary">收录 24 家媒体 · 共 270+ 篇要闻</span>
          <span id="lastUpdated" style="color: var(--text-light);">更新于: 刚刚</span>
        </div>
        <button class="sync-btn" id="syncAllBtn" onclick="syncAllFeeds()">
          <span>🔄</span> 实时同步所有视角
        </button>
      </div>

      <div class="progress-bar-container" id="progressBar">
        <div class="progress-bar-fill" id="progressFill"></div>
      </div>
    </section>

    <!-- 控制面板 -->
    <div class="controls-panel">
      <div class="controls-row">
        <!-- 视图切换 -->
        <div class="view-tabs">
          <button class="view-tab active" id="tabColumns" onclick="switchView('columns')">🏛️ 四国多栏看板</button>
          <button class="view-tab" id="tabTimeline" onclick="switchView('timeline')">🌊 全球即时时钟</button>
          <button class="view-tab" id="tabMatrix" onclick="switchView('matrix')">📰 机构全景矩阵</button>
        </div>

        <!-- 搜索框 -->
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" placeholder="搜索全球新闻标题、机构或关键词... (按 / 聚焦)" oninput="handleSearch()">
          <button class="search-clear" id="searchClear" onclick="clearSearch()">✕</button>
        </div>
      </div>

      <!-- 分类与国别筛选 -->
      <div class="filters-bar">
        <button class="filter-btn active" data-filter="all" onclick="setCategoryFilter('all')">
          全部领域 <span class="count-badge" id="countAll">270</span>
        </button>
        <button class="filter-btn" data-filter="headline" onclick="setCategoryFilter('headline')">
          综合要闻
        </button>
        <button class="filter-btn" data-filter="international" onclick="setCategoryFilter('international')">
          国际时政
        </button>
        <button class="filter-btn" data-filter="economy" onclick="setCategoryFilter('economy')">
          财经商业
        </button>
      </div>
    </div>

    <!-- 视图 1: 四国多栏看板 (Perspective Columns) -->
    <section id="viewColumns" class="perspective-deck">
      <!-- 🇨🇳 中国 -->
      <div class="deck-column cn">
        <div class="column-header">
          <div class="column-header-top">
            <div class="column-title"><span>🇨🇳</span> 中国观察 (China)</div>
            <span class="column-count" id="countColCn">72篇</span>
          </div>
          <select class="column-source-select" onchange="filterColumnSource('cn', this.value)">
            <option value="all">全部中国信源 (6家)</option>
            <option value="xinhua_world">新华社 (国际频道)</option>
            <option value="thepaper">澎湃新闻 (时事要闻)</option>
            <option value="jiemian">界面新闻 (商业财经)</option>
            <option value="people_world">人民网 (国际视野)</option>
            <option value="ftchinese">FT中文网 (全球财经)</option>
            <option value="dw_zh">德国之声 (中文视点)</option>
          </select>
        </div>
        <div class="column-articles" id="colArticlesCn"></div>
      </div>

      <!-- 🇯🇵 日本 -->
      <div class="deck-column jp">
        <div class="column-header">
          <div class="column-header-top">
            <div class="column-title"><span>🇯🇵</span> 日本視点 (Japan)</div>
            <span class="column-count" id="countColJp">63篇</span>
          </div>
          <select class="column-source-select" onchange="filterColumnSource('jp', this.value)">
            <option value="all">全部日本信源 (6家)</option>
            <option value="nhk_top">NHK NEWS WEB (主要ニュース)</option>
            <option value="nhk_world">NHK NEWS (国際ニュース)</option>
            <option value="nikkei">日本経済新聞 (日経速報)</option>
            <option value="asahi">朝日新聞 (ニュース速報)</option>
            <option value="yahoo_jp">Yahoo! JAPAN (トピックス)</option>
            <option value="toyokeizai">東洋経済 (ビジネス速報)</option>
          </select>
        </div>
        <div class="column-articles" id="colArticlesJp"></div>
      </div>

      <!-- 🇰🇷 韩国 -->
      <div class="deck-column kr">
        <div class="column-header">
          <div class="column-header-top">
            <div class="column-title"><span>🇰🇷</span> 한국 시선 (Korea)</div>
            <span class="column-count" id="countColKr">72篇</span>
          </div>
          <select class="column-source-select" onchange="filterColumnSource('kr', this.value)">
            <option value="all">全部韩国信源 (6家)</option>
            <option value="yna_zh">韩联社 (中文网)</option>
            <option value="yna_kr">연합뉴스 (속보·헤드라인)</option>
            <option value="chosun">조선일보 (Chosun Ilbo)</option>
            <option value="donga">동아일보 (Dong-A Ilbo)</option>
            <option value="hani">한겨레 (Hankyoreh)</option>
            <option value="kbs_zh">KBS World (国际广播中文网)</option>
          </select>
        </div>
        <div class="column-articles" id="colArticlesKr"></div>
      </div>

      <!-- 🇺🇸 美欧全球 -->
      <div class="deck-column us">
        <div class="column-header">
          <div class="column-header-top">
            <div class="column-title"><span>🇺🇸</span> 美欧全球 (US & World)</div>
            <span class="column-count" id="countColUs">70篇</span>
          </div>
          <select class="column-source-select" onchange="filterColumnSource('us', this.value)">
            <option value="all">全部美欧信源 (6家)</option>
            <option value="nyt_top">The New York Times (Top Stories)</option>
            <option value="nyt_world">The New York Times (World News)</option>
            <option value="wsj_world">Wall Street Journal (World News)</option>
            <option value="cnn_top">CNN (Breaking & Top)</option>
            <option value="npr_news">NPR News (Public Radio)</option>
            <option value="bbc_world">BBC News (World Service)</option>
          </select>
        </div>
        <div class="column-articles" id="colArticlesUs"></div>
      </div>
    </section>

    <!-- 视图 2: 全球即时时钟时间线 (Unified Timeline) -->
    <section id="viewTimeline" class="timeline-container" style="display: none;"></section>

    <!-- 视图 3: 机构全景矩阵 (Media Outlets Grid) -->
    <section id="viewMatrix" class="media-matrix" style="display: none;"></section>

  </main>

  <!-- 底部说明与跨域导航 -->
  <footer class="footer">
    <div class="footer-links">
      <a href="index.html">🎮 游戏大厅 (game.0101.click)</a>
      <span>·</span>
      <a href="kids.html">🎈 奇趣益智乐园 (l.0101.click)</a>
      <span>·</span>
      <a href="languages.html">🌐 多语言课文乐园</a>
      <span>·</span>
      <a href="tech-blogs.html">📡 企业技术博客雷达</a>
      <span>·</span>
      <a href="tools.html">🧰 实用小工具集</a>
    </div>
    <p>中日韩美·全球新闻视角雷达 · 仅供公开学术研究与资讯对照 · 所有新闻知识产权归原媒体机构所有</p>
  </footer>

  <!-- 悬浮通知 Toast -->
  <div class="toast" id="toast">已复制到剪贴板</div>

  <script>
    // 1. Level 0 离线打底种子数据 (秒开 0ms / 离线兜底)
    const BUILTIN_NEWS_DATA = {json_str};

    // 运行时状态
    let currentData = JSON.parse(JSON.stringify(BUILTIN_NEWS_DATA));
    let activeView = 'columns'; // 'columns' | 'timeline' | 'matrix'
    let activeCategory = 'all';
    let searchQuery = '';
    let columnSourceFilters = {{ cn: 'all', jp: 'all', kr: 'all', us: 'all' }};
    let isSyncing = false;

    // 主题切换管理
    function initTheme() {{
      const savedTheme = localStorage.getItem('app_theme');
      if (savedTheme) {{
        document.documentElement.setAttribute('data-theme', savedTheme);
      }} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
        document.documentElement.setAttribute('data-theme', 'dark');
      }}
    }}

    function toggleTheme() {{
      const current = document.documentElement.getAttribute('data-theme');
      const target = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', target);
      localStorage.setItem('app_theme', target);
    }}

    initTheme();

    // 格式化相对时间
    function formatRelativeTime(isoStr) {{
      if (!isoStr) return '近期';
      const d = new Date(isoStr);
      if (isNaN(d.getTime())) return isoStr;
      const diffMs = Date.now() - d.getTime();
      const diffMin = Math.floor(diffMs / 60000);
      if (diffMin < 1) return '刚刚';
      if (diffMin < 60) return `${{diffMin}}分钟前`;
      const diffHours = Math.floor(diffMin / 60);
      if (diffHours < 24) return `${{diffHours}}小时前`;
      const diffDays = Math.floor(diffHours / 24);
      if (diffDays === 1) return '昨天';
      if (diffDays < 7) return `${{diffDays}}天前`;
      return isoStr.slice(0, 10);
    }}

    // 显示 Toast
    function showToast(msg) {{
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2200);
    }}

    // 切换视图
    function switchView(viewName) {{
      activeView = viewName;
      document.getElementById('tabColumns').classList.toggle('active', viewName === 'columns');
      document.getElementById('tabTimeline').classList.toggle('active', viewName === 'timeline');
      document.getElementById('tabMatrix').classList.toggle('active', viewName === 'matrix');

      document.getElementById('viewColumns').style.display = viewName === 'columns' ? 'grid' : 'none';
      document.getElementById('viewTimeline').style.display = viewName === 'timeline' ? 'flex' : 'none';
      document.getElementById('viewMatrix').style.display = viewName === 'matrix' ? 'grid' : 'none';

      renderActiveView();
    }}

    // 设置分类过滤
    function setCategoryFilter(cat) {{
      activeCategory = cat;
      document.querySelectorAll('.filter-btn').forEach(btn => {{
        btn.classList.toggle('active', btn.getAttribute('data-filter') === cat);
      }});
      renderActiveView();
    }}

    // 列单独源过滤
    function filterColumnSource(region, sourceId) {{
      columnSourceFilters[region] = sourceId;
      renderColumnsView();
    }}

    // 搜索输入
    function handleSearch() {{
      searchQuery = document.getElementById('searchInput').value.trim().toLowerCase();
      document.getElementById('searchClear').classList.toggle('visible', searchQuery.length > 0);
      renderActiveView();
    }}

    function clearSearch() {{
      document.getElementById('searchInput').value = '';
      searchQuery = '';
      document.getElementById('searchClear').classList.remove('visible');
      renderActiveView();
    }}

    // 快捷键监听
    window.addEventListener('keydown', (e) => {{
      if (e.key === '/' && document.activeElement !== document.getElementById('searchInput')) {{
        e.preventDefault();
        document.getElementById('searchInput').focus();
      }} else if (e.key === 'Escape' && document.activeElement === document.getElementById('searchInput')) {{
        clearSearch();
      }}
    }});

    // 判定文章是否满足当前过滤条件
    function matchArticle(art) {{
      if (activeCategory !== 'all' && art.category !== activeCategory) {{
        return false;
      }}
      if (searchQuery) {{
        const text = (art.title + ' ' + art.sourceName).toLowerCase();
        if (!text.includes(searchQuery)) return false;
      }}
      return true;
    }}

    // 生成单条新闻卡片 HTML
    function buildNewsItemHtml(art) {{
      const isForeign = art.language && art.language !== 'zh';
      const translateUrl = `https://translate.google.com/translate?sl=auto&tl=zh-CN&u=${{encodeURIComponent(art.link)}}`;
      const escapedTitle = art.title.replace(/"/g, '&quot;');

      return `
        <article class="news-item">
          <div class="news-meta">
            <span class="news-source-tag">${{art.regionFlag}} ${{art.sourceName}}</span>
            <span class="news-time" title="${{art.pubDateIso || ''}}">${{formatRelativeTime(art.pubDateIso)}}</span>
          </div>
          <a href="${{art.link}}" target="_blank" rel="noopener noreferrer" class="news-title">
            ${{art.title}}
          </a>
          <div class="news-actions">
            <div>
              ${{isForeign ? `<a href="${{translateUrl}}" target="_blank" rel="noopener noreferrer" class="news-action-btn" title="在 Google 翻译中打开全文">🌏 译文</a>` : ''}}
            </div>
            <div>
              <button class="news-action-btn" onclick="copyText('${{escapedTitle}} ${{art.link}}')">📋 复制</button>
              <a href="${{art.link}}" target="_blank" rel="noopener noreferrer" class="news-action-btn">原文 ↗</a>
            </div>
          </div>
        </article>
      `;
    }}

    function toggleSnippet(id) {{
      const el = document.getElementById(id);
      if (el) el.classList.toggle('open');
    }}

    function copyText(str) {{
      navigator.clipboard.writeText(str).then(() => {{
        showToast('已复制新闻标题与链接');
      }}).catch(() => {{
        showToast('复制失败，请手动选择复制');
      }});
    }}

    function copyRss(url) {{
      navigator.clipboard.writeText(url).then(() => {{
        showToast('已复制 RSS Feed 订阅地址');
      }}).catch(() => {{
        showToast('复制失败');
      }});
    }}

    // 渲染视图 1: 多栏视角看板
    function renderColumnsView() {{
      const regions = ['cn', 'jp', 'kr', 'us'];
      regions.forEach(reg => {{
        const container = document.getElementById(`colArticles${{reg.charAt(0).toUpperCase() + reg.slice(1)}}`);
        const countEl = document.getElementById(`countCol${{reg.charAt(0).toUpperCase() + reg.slice(1)}}`);
        if (!container) return;

        // 获取该区域的信源
        let sources = currentData.sources.filter(s => s.region === reg);
        if (columnSourceFilters[reg] !== 'all') {{
          sources = sources.filter(s => s.id === columnSourceFilters[reg]);
        }}

        // 收集符合过滤的所有文章
        let articles = [];
        sources.forEach(s => {{
          (s.articles || []).forEach(art => {{
            if (matchArticle(art)) articles.push(art);
          }});
        }});

        // 按时间排序
        articles.sort((a, b) => (b.pubDateIso || '').localeCompare(a.pubDateIso || ''));

        if (countEl) countEl.textContent = `${{articles.length}}篇`;

        if (articles.length === 0) {{
          container.innerHTML = '<div style="text-align: center; color: var(--text-light); padding: 24px 0; font-size: 13px;">暂无匹配要闻</div>';
        }} else {{
          container.innerHTML = articles.map(buildNewsItemHtml).join('');
        }}
      }});
    }}

    // 渲染视图 2: 全球即时时钟时间线
    function renderTimelineView() {{
      const container = document.getElementById('viewTimeline');
      if (!container) return;

      // 汇总所有文章
      let articles = [];
      currentData.sources.forEach(s => {{
        (s.articles || []).forEach(art => {{
          if (matchArticle(art)) articles.push(art);
        }});
      }});

      // 降序
      articles.sort((a, b) => (b.pubDateIso || '').localeCompare(a.pubDateIso || ''));

      if (articles.length === 0) {{
        container.innerHTML = '<div style="text-align: center; color: var(--text-light); padding: 40px 0; font-size: 14px;">没有找到匹配的新闻条目</div>';
        return;
      }}

      container.innerHTML = articles.slice(0, 100).map(art => {{
        const isForeign = art.language && art.language !== 'zh';
        const translateUrl = `https://translate.google.com/translate?sl=auto&tl=zh-CN&u=${{encodeURIComponent(art.link)}}`;
        const escapedTitle = art.title.replace(/"/g, '&quot;');

        return `
          <div class="timeline-card">
            <div class="timeline-flag-box">${{art.regionFlag}}</div>
            <div class="timeline-content">
              <div class="timeline-meta">
                <span class="timeline-source">${{art.sourceName}}</span>
                <span style="color: var(--text-light);">·</span>
                <span style="color: var(--text-light);">${{formatRelativeTime(art.pubDateIso)}}</span>
                <span class="badge-sub">${{art.categoryName || '要闻'}}</span>
              </div>
              <a href="${{art.link}}" target="_blank" rel="noopener noreferrer" class="timeline-title">
                ${{art.title}}
              </a>
              <div class="news-actions" style="margin-top: 8px;">
                <div>
                  ${{isForeign ? `<a href="${{translateUrl}}" target="_blank" rel="noopener noreferrer" class="news-action-btn">🌏 中文翻译</a>` : ''}}
                  <button class="news-action-btn" onclick="copyText('${{escapedTitle}} ${{art.link}}')">📋 复制</button>
                </div>
                <a href="${{art.link}}" target="_blank" rel="noopener noreferrer" class="news-action-btn">阅读原文 ↗</a>
              </div>
            </div>
          </div>
        `;
      }}).join('');
    }}

    // 渲染视图 3: 机构全景矩阵
    function renderMatrixView() {{
      const container = document.getElementById('viewMatrix');
      if (!container) return;

      let sources = currentData.sources;
      if (searchQuery) {{
        sources = sources.filter(s => (s.name + ' ' + s.desc).toLowerCase().includes(searchQuery));
      }}

      container.innerHTML = sources.map(s => {{
        const articles = (s.articles || []).slice(0, 4);
        return `
          <div class="media-card">
            <div class="media-card-top">
              <div class="media-info">
                <div class="media-icon">${{s.icon || '📰'}}</div>
                <div>
                  <div class="media-name">${{s.regionFlag}} ${{s.name}}</div>
                  <div style="font-size: 11px; color: var(--text-light);">${{s.regionName}} · ${{s.categoryName}}</div>
                </div>
              </div>
              <button class="news-action-btn" onclick="copyRss('${{s.feedUrl}}')" title="复制 RSS 源链接">📡 RSS</button>
            </div>
            <p class="media-desc">${{s.desc}}</p>
            <div class="media-articles-list">
              ${{articles.map(art => `
                <a href="${{art.link}}" target="_blank" rel="noopener noreferrer" class="media-article-link" title="${{art.title}}">
                  ${{art.title}}
                </a>
              `).join('')}}
              ${{articles.length === 0 ? '<div style="font-size: 12px; color: var(--text-light);">暂无可用要闻</div>' : ''}}
            </div>
          </div>
        `;
      }}).join('');
    }}

    // 统一渲染当前激活视图
    function renderActiveView() {{
      if (activeView === 'columns') renderColumnsView();
      else if (activeView === 'timeline') renderTimelineView();
      else if (activeView === 'matrix') renderMatrixView();
      updateStats();
    }}

    function updateStats() {{
      let total = 0;
      currentData.sources.forEach(s => total += (s.articles || []).length);
      const sumEl = document.getElementById('statSummary');
      if (sumEl) sumEl.textContent = `收录 ${{currentData.sources.length}} 家媒体 · 共 ${{total}} 篇要闻`;
      const allCountEl = document.getElementById('countAll');
      if (allCountEl) allCountEl.textContent = total;
    }}

    // 2. Level 1: 异步获取本地 CI 静态 JSON 快照 (data/global-news.json)
    async function loadCiStaticData() {{
      try {{
        const resp = await fetch('./data/global-news.json', {{ cache: 'no-cache' }});
        if (resp.ok) {{
          const remote = await resp.json();
          if (remote && remote.sources && remote.sources.length > 0) {{
            currentData = remote;
            document.getElementById('statusBadge').className = 'status-badge ci';
            document.getElementById('statusBadge').textContent = '⚡ CI 预构建快照';
            if (remote.updatedAt) {{
              document.getElementById('lastUpdated').textContent = `更新于: ${{formatRelativeTime(remote.updatedAt)}}`;
            }}
            renderActiveView();
            console.log('⚡ 成功加载 CI 静态快照 JSON');
          }}
        }}
      }} catch (e) {{
        console.log('ℹ️ 未检测到远程 CI JSON，使用 Level 0 离线打底种子');
      }}
    }}

    // 3. Level 2: 浏览器端多路代理并发实时同步
    const PROXY_CANDIDATES = [
      url => `https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}`
    ];

    async function fetchRssText(url) {{
      for (const getProxyUrl of PROXY_CANDIDATES) {{
        try {{
          const proxyUrl = getProxyUrl(url);
          const res = await fetch(proxyUrl, {{ signal: AbortSignal.timeout(6000) }});
          if (!res.ok) continue;
          if (proxyUrl.includes('allorigins.win')) {{
            const data = await res.json();
            if (data && data.contents) return data.contents;
          }} else {{
            const text = await res.text();
            if (text && text.includes('<')) return text;
          }}
        }} catch (e) {{}}
      }}
      return null;
    }}

    function parseXmlArticles(xmlText, src) {{
      const parser = new DOMParser();
      const doc = parser.parseFromString(xmlText, 'text/xml');
      const articles = [];
      const items = doc.querySelectorAll('item, entry');

      items.forEach((item, idx) => {{
        if (idx >= 12) return;
        const title = (item.querySelector('title')?.textContent || '').trim();
        let link = (item.querySelector('link')?.textContent || '').trim();
        if (!link) {{
          const linkEl = item.querySelector('link[href]');
          if (linkEl) link = linkEl.getAttribute('href');
        }}
        if (!link) {{
          const guid = item.querySelector('guid')?.textContent || '';
          if (guid.startsWith('http')) link = guid;
        }}
        if (!title || !link) return;

        let dateStr = item.querySelector('pubDate, date, updated, published')?.textContent || '';
        let pubDateIso = new Date().toISOString();
        if (dateStr) {{
          const d = new Date(dateStr);
          if (!isNaN(d.getTime())) pubDateIso = d.toISOString();
        }}


        articles.push({{
          title,
          link,
          pubDateIso,
          snippet: '',
          sourceId: src.id,
          sourceName: src.name,
          region: src.region,
          regionFlag: src.regionFlag,
          category: src.category,
          categoryName: src.categoryName,
          language: src.language
        }});
      }});
      return articles;
    }}

    async function syncAllFeeds() {{
      if (isSyncing) return;
      isSyncing = true;

      const btn = document.getElementById('syncAllBtn');
      const pBar = document.getElementById('progressBar');
      const pFill = document.getElementById('progressFill');

      btn.disabled = true;
      btn.innerHTML = '<span>⏳</span> 正在多路同步...';
      pBar.style.display = 'block';
      pFill.style.width = '0%';

      let completed = 0;
      const total = currentData.sources.length;

      for (const src of currentData.sources) {{
        try {{
          const xml = await fetchRssText(src.feedUrl);
          if (xml) {{
            const newArts = parseXmlArticles(xml, src);
            if (newArts.length > 0) {{
              src.articles = newArts;
            }}
          }}
        }} catch (e) {{}}

        completed++;
        pFill.style.width = `${{(completed / total) * 100}}%`;
      }}

      isSyncing = false;
      btn.disabled = false;
      btn.innerHTML = '<span>🔄</span> 实时同步所有视角';
      pBar.style.display = 'none';

      document.getElementById('statusBadge').className = 'status-badge live';
      document.getElementById('statusBadge').textContent = '🟢 边缘实时已同步';
      document.getElementById('lastUpdated').textContent = '更新于: 刚刚 (实时)';

      renderActiveView();
      showToast('🎉 全球 24 家大报新闻视角同步完成');
    }}

    // 初始化渲染
    renderActiveView();
    loadCiStaticData();
  </script>
</body>
</html>
'''

    out_file = os.path.join(os.path.dirname(__file__), "..", "global-news.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Successfully built {out_file} (Embedded {len(news_data['sources'])} sources, {news_data['totalArticles']} articles)")

if __name__ == "__main__":
    generate_page()
