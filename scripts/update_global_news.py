#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global News Perspectives Deck - Aggregator & Normalizer
Fetches, sanitizes, and aggregates RSS/RDF/Atom feeds from authoritative news organizations
across China (CN), Japan (JP), South Korea (KR), and United States (US).
Outputs unified static JSON (data/global-news.json) for 0ms Jamstack rendering and CI workflows.
"""

import sys
import os
import json
import re
import html
import time
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# 24 Selected Leading News Outlets across CN, JP, KR, and US
NEWS_SOURCES = [
    # ==========================================
    # 🇨🇳 中国视角 (China Perspectives)
    # ==========================================
    {
        "id": "xinhua_world",
        "name": "新华社 (国际频道)",
        "region": "cn",
        "regionName": "中国",
        "regionFlag": "🇨🇳",
        "category": "international",
        "categoryName": "国际时政",
        "url": "http://www.xinhuanet.com/world/",
        "feedUrl": "http://www.xinhuanet.com/world/news_world.xml",
        "icon": "🌐",
        "language": "zh",
        "desc": "国家通讯社核心外宣窗口，展现官方视野下的全球地缘政治与多边外交动态。"
    },
    {
        "id": "thepaper",
        "name": "澎湃新闻 (时事要闻)",
        "region": "cn",
        "regionName": "中国",
        "regionFlag": "🇨🇳",
        "category": "headline",
        "categoryName": "国内要闻",
        "url": "https://www.thepaper.cn/",
        "feedUrl": "https://feedx.net/rss/thepaper.xml",
        "icon": "📰",
        "language": "zh",
        "desc": "专注时政与思想的新媒体先锋，提供敏锐的社会事件调查与深度特稿。"
    },
    {
        "id": "jiemian",
        "name": "界面新闻 (商业财经)",
        "region": "cn",
        "regionName": "中国",
        "regionFlag": "🇨🇳",
        "category": "economy",
        "categoryName": "财经商业",
        "url": "https://www.jiemian.com/",
        "feedUrl": "https://feedx.net/rss/jiemian.xml",
        "icon": "📈",
        "language": "zh",
        "desc": "面向独立思考者的商业财经媒体，聚焦产业变革、资本市场与宏观经济指标。"
    },
    {
        "id": "people_world",
        "name": "人民网 (国际视野)",
        "region": "cn",
        "regionName": "中国",
        "regionFlag": "🇨🇳",
        "category": "international",
        "categoryName": "国际时政",
        "url": "http://world.people.com.cn/",
        "feedUrl": "http://www.people.com.cn/rss/world.xml",
        "icon": "🇨🇳",
        "language": "zh",
        "desc": "国家重点主流新闻网站，权威发布重大国际时事、双边关系与全球宏观议题。"
    },
    {
        "id": "ftchinese",
        "name": "FT中文网 (全球财经)",
        "region": "cn",
        "regionName": "中国",
        "regionFlag": "🇨🇳",
        "category": "economy",
        "categoryName": "财经商业",
        "url": "https://www.ftchinese.com/",
        "feedUrl": "https://www.ftchinese.com/rss/news",
        "icon": "📊",
        "language": "zh",
        "desc": "英国《金融时报》集团旗下的中文商业平台，提供西方观察家对大中华经济的独到审视。"
    },
    {
        "id": "dw_zh",
        "name": "德国之声 (中文视点)",
        "region": "cn",
        "regionName": "中国",
        "regionFlag": "🇨🇳",
        "category": "international",
        "categoryName": "国际时政",
        "url": "https://www.dw.com/zh",
        "feedUrl": "https://rss.dw.com/rdf/rss-chi-all",
        "icon": "🌍",
        "language": "zh",
        "desc": "德国国家公营国际传播机构，呈现欧洲视角下的中欧关系与全球战略格局。"
    },

    # ==========================================
    # 🇯🇵 日本视角 (Japan Perspectives)
    # ==========================================
    {
        "id": "nhk_top",
        "name": "NHK NEWS WEB (主要ニュース)",
        "region": "jp",
        "regionName": "日本",
        "regionFlag": "🇯🇵",
        "category": "headline",
        "categoryName": "综合要闻",
        "url": "https://www3.nhk.or.jp/news/",
        "feedUrl": "https://www.nhk.or.jp/rss/news/cat0.xml",
        "icon": "🔴",
        "language": "ja",
        "desc": "日本公共广播总社核心频道，客观严谨，为日本国民最重要的灾情与时政信息基石。"
    },
    {
        "id": "nhk_world",
        "name": "NHK NEWS (国際ニュース)",
        "region": "jp",
        "regionName": "日本",
        "regionFlag": "🇯🇵",
        "category": "international",
        "categoryName": "国际时政",
        "url": "https://www3.nhk.or.jp/news/cat06.html",
        "feedUrl": "https://www.nhk.or.jp/rss/news/cat6.xml",
        "icon": "🌏",
        "language": "ja",
        "desc": "NHK 国际观察板块，全面追踪东亚安全局势、美日同盟与全球热点事态发展。"
    },
    {
        "id": "nikkei",
        "name": "日本経済新聞 (日経速報)",
        "region": "jp",
        "regionName": "日本",
        "regionFlag": "🇯🇵",
        "category": "economy",
        "categoryName": "财经商业",
        "url": "https://www.nikkei.com/",
        "feedUrl": "https://assets.wor.jp/rss/rdf/nikkei/news.rdf",
        "icon": "💼",
        "language": "ja",
        "desc": "日本政界与金融界最具权威的财经日报，主导日经指数分析、半导体产业链与跨国并购动向。"
    },
    {
        "id": "asahi",
        "name": "朝日新聞 (ニュース速報)",
        "region": "jp",
        "regionName": "日本",
        "regionFlag": "🇯🇵",
        "category": "headline",
        "categoryName": "综合要闻",
        "url": "https://www.asahi.com/",
        "feedUrl": "http://rss.asahi.com/rss/asahi/newsheadlines.rdf",
        "icon": "🗞️",
        "language": "ja",
        "desc": "日本全国性三大报纸之一，注重深度调查报道与文化思潮，持审慎多元立场。"
    },
    {
        "id": "yahoo_jp",
        "name": "Yahoo! JAPAN (トピックス)",
        "region": "jp",
        "regionName": "日本",
        "regionFlag": "🇯🇵",
        "category": "headline",
        "categoryName": "综合要闻",
        "url": "https://news.yahoo.co.jp/",
        "feedUrl": "https://news.yahoo.co.jp/rss/topics/top-picks.xml",
        "icon": "🇯🇵",
        "language": "ja",
        "desc": "日本月活最高的门户资讯中心，实时反映日本大众国民此刻最聚焦的社会痛点与议题。"
    },
    {
        "id": "toyokeizai",
        "name": "東洋経済 (ビジネス速報)",
        "region": "jp",
        "regionName": "日本",
        "regionFlag": "🇯🇵",
        "category": "economy",
        "categoryName": "财经商业",
        "url": "https://toyokeizai.net/",
        "feedUrl": "https://toyokeizai.net/list/feed/rss",
        "icon": "🏭",
        "language": "ja",
        "desc": "逾百年历史的日本经济周刊数字版，擅长长篇拆解丰田、索尼、任天堂等巨头产业战略。"
    },

    # ==========================================
    # 🇰🇷 韩国视角 (Korea Perspectives)
    # ==========================================
    {
        "id": "yna_zh",
        "name": "韩联社 (中文网)",
        "region": "kr",
        "regionName": "韩国",
        "regionFlag": "🇰🇷",
        "category": "headline",
        "categoryName": "综合要闻",
        "url": "https://cn.yna.co.kr/",
        "feedUrl": "https://cn.yna.co.kr/RSS/news.xml",
        "icon": "🇰🇷",
        "language": "zh",
        "desc": "韩国国家通讯社面向华语圈的官方旗舰窗口，第一手传递青瓦台/龙山总统府政策与半岛局势。"
    },
    {
        "id": "yna_kr",
        "name": "연합뉴스 (속보·헤드라인)",
        "region": "kr",
        "regionName": "韩国",
        "regionFlag": "🇰🇷",
        "category": "headline",
        "categoryName": "综合要闻",
        "url": "https://www.yna.co.kr/",
        "feedUrl": "https://www.yna.co.kr/rss/news.xml",
        "icon": "⚡",
        "language": "ko",
        "desc": "韩联社韩国本土实时原版快讯，全天候 24 小时高频刷新韩国全境政治、经济与突发事态。"
    },
    {
        "id": "chosun",
        "name": "조선일보 (Chosun Ilbo)",
        "region": "kr",
        "regionName": "韩国",
        "regionFlag": "🇰🇷",
        "category": "headline",
        "categoryName": "综合要闻",
        "url": "https://www.chosun.com/",
        "feedUrl": "https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml",
        "icon": "🏛️",
        "language": "ko",
        "desc": "韩国历史最悠久、发行量最大的主流保守派大报，在政商军界拥有深远号召力与决策影响力。"
    },
    {
        "id": "donga",
        "name": "동아일보 (Dong-A Ilbo)",
        "region": "kr",
        "regionName": "韩国",
        "regionFlag": "🇰🇷",
        "category": "headline",
        "categoryName": "综合要闻",
        "url": "https://www.donga.com/",
        "feedUrl": "https://rss.donga.com/total.xml",
        "icon": "📜",
        "language": "ko",
        "desc": "创刊于 1920 年的韩国三大主流全国性报刊之一，深耕东亚外交互动、大企业财阀动向与法制社会。"
    },
    {
        "id": "hani",
        "name": "한겨레 (Hankyoreh)",
        "region": "kr",
        "regionName": "韩国",
        "regionFlag": "🇰🇷",
        "category": "international",
        "categoryName": "深度特稿",
        "url": "https://www.hani.co.kr/",
        "feedUrl": "https://www.hani.co.kr/rss/",
        "icon": "🕊️",
        "language": "ko",
        "desc": "韩国由民众募资创办的著名进步派独立报纸，长于人权保障、财阀垄断监督与劳动民生议题。"
    },
    {
        "id": "kbs_zh",
        "name": "KBS World (国际广播中文网)",
        "region": "kr",
        "regionName": "韩国",
        "regionFlag": "🇰🇷",
        "category": "international",
        "categoryName": "国际时政",
        "url": "https://world.kbs.co.kr/chinese/",
        "feedUrl": "https://world.kbs.co.kr/rss/rss_news.htm?lang=c",
        "icon": "📻",
        "language": "zh",
        "desc": "韩国公营电视台 KBS 的海外国际传播部门，权威发布半岛安全声明、经济往来与文化交流要闻。"
    },

    # ==========================================
    # 🇺🇸 美国与全球参照 (US & Global Perspectives)
    # ==========================================
    {
        "id": "nyt_top",
        "name": "The New York Times (Top Stories)",
        "region": "us",
        "regionName": "美国",
        "regionFlag": "🇺🇸",
        "category": "headline",
        "categoryName": "综合要闻",
        "url": "https://www.nytimes.com/",
        "feedUrl": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "icon": "🗽",
        "language": "en",
        "desc": "全球影响力最大的一流百年综合报纸，深刻主导西方社会关于华盛顿政治与世界事务的公共议程。"
    },
    {
        "id": "nyt_world",
        "name": "The New York Times (World News)",
        "region": "us",
        "regionName": "美国",
        "regionFlag": "🇺🇸",
        "category": "international",
        "categoryName": "国际时政",
        "url": "https://www.nytimes.com/section/world",
        "feedUrl": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "icon": "🌐",
        "language": "en",
        "desc": "纽约时报遍布全球的海外特派记者网络，提供具备宏大叙事深度的地缘格局第一线纪实。"
    },
    {
        "id": "wsj_world",
        "name": "Wall Street Journal (World News)",
        "region": "us",
        "regionName": "美国",
        "regionFlag": "🇺🇸",
        "category": "economy",
        "categoryName": "财经商业",
        "url": "https://www.wsj.com/news/world",
        "feedUrl": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
        "icon": "🏛️",
        "language": "en",
        "desc": "道琼斯旗下世界最顶尖金融财经日报，全球政商精英判断贸易壁垒、央行货币政策与供应链重组的关键读物。"
    },
    {
        "id": "cnn_top",
        "name": "CNN International (Breaking News)",
        "region": "us",
        "regionName": "美国",
        "regionFlag": "🇺🇸",
        "category": "headline",
        "categoryName": "综合要闻",
        "url": "https://edition.cnn.com/",
        "feedUrl": "http://rss.cnn.com/rss/edition.rss",
        "icon": "🔴",
        "language": "en",
        "desc": "开创 24 小时滚动电视新闻模式的全球新闻网，对国际突发危机与大选具有极快的情报响应能力。"
    },
    {
        "id": "npr_news",
        "name": "NPR News (National Public Radio)",
        "region": "us",
        "regionName": "美国",
        "regionFlag": "🇺🇸",
        "category": "headline",
        "categoryName": "深度特稿",
        "url": "https://www.npr.org/",
        "feedUrl": "https://feeds.npr.org/1001/rss.xml",
        "icon": "🎙️",
        "language": "en",
        "desc": "美国公立非营利广播机构，以非党派客观调查、人文深度叙事与公共科学报道享有极高声誉。"
    },
    {
        "id": "bbc_world",
        "name": "BBC News (World Service)",
        "region": "us",
        "regionName": "美国/全球",
        "regionFlag": "🌐",
        "category": "international",
        "categoryName": "国际时政",
        "url": "https://www.bbc.com/news/world",
        "feedUrl": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "icon": "👑",
        "language": "en",
        "desc": "全球公认的跨国公立新闻标杆，作为对比参照系，呈现英语世界经典、稳健的全球事实核查与报道。"
    }
]

def clean_html(raw_html: str) -> str:
    """Strip HTML tags and unescape character entities."""
    if not raw_html:
        return ""
    # Remove script and style tags
    cleaned = re.sub(r'<(script|style).*?</\1>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    # Remove CDATA wrapper
    cleaned = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', cleaned, flags=re.DOTALL)
    # Remove HTML tags
    cleaned = re.sub(r'<[^<]+?>', '', cleaned)
    # Unescape HTML entities twice
    cleaned = html.unescape(cleaned)
    cleaned = html.unescape(cleaned)
    # Collapse multiple whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def parse_iso_date(raw_date: str) -> tuple[str, str]:
    """Parse various date formats into display date (YYYY-MM-DD) and ISO UTC string."""
    if not raw_date:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%d"), now.isoformat()
    raw_date = raw_date.strip()
    
    # Try email/RFC 822 format (e.g., Tue, 06 Oct 2026 08:30:00 GMT)
    try:
        dt = parsedate_to_datetime(raw_date)
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.strftime("%Y-%m-%d"), dt_utc.isoformat()
    except Exception:
        pass
        
    # Try ISO 8601 (e.g. 2026-10-06T08:30:00+09:00, 2026-10-06T08:30:00Z)
    try:
        clean = raw_date.replace('Z', '+00:00')
        dt = datetime.fromisoformat(clean)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.strftime("%Y-%m-%d"), dt_utc.isoformat()
    except Exception:
        pass

    # Regex search YYYY-MM-DD
    m = re.search(r'(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})', raw_date)
    if m:
        try:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            dt = datetime(y, mo, d, 0, 0, 0, tzinfo=timezone.utc)
            return dt.strftime("%Y-%m-%d"), dt.isoformat()
        except Exception:
            pass

    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d"), now.isoformat()

def extract_tag(xml_snippet: str, tag_name: str) -> str:
    """Extract content of an XML tag, handling CDATA."""
    pattern = rf'<{tag_name}(?:\s[^>]*)?>(.*?)</{tag_name}>'
    m = re.search(pattern, xml_snippet, re.DOTALL | re.IGNORECASE)
    if m:
        val = m.group(1).strip()
        # strip CDATA
        cdata_m = re.search(r'<!\[CDATA\[(.*?)\]\]>', val, re.DOTALL)
        if cdata_m:
            return cdata_m.group(1).strip()
        return val
    return ""

def extract_link(xml_snippet: str) -> str:
    """Extract URL link from item or entry."""
    # First check <link>...</link>
    link = extract_tag(xml_snippet, 'link')
    if link and link.startswith('http'):
        return link
        
    # Check <link href="..." /> (Atom)
    m = re.search(r'<link(?:\s[^>]*?)?\shref=["\']([^"\']+)["\']', xml_snippet, re.IGNORECASE)
    if m:
        return m.group(1).strip()
        
    # Check <guid> or <id>
    guid = extract_tag(xml_snippet, 'guid')
    if guid and guid.startswith('http'):
        return guid
        
    atom_id = extract_tag(xml_snippet, 'id')
    if atom_id and atom_id.startswith('http'):
        return atom_id
        
    return link

def fetch_and_parse_feed(cfg: dict, max_items: int = 12) -> list[dict]:
    """Fetch feed using standard urllib and parse articles."""
    feed_url = cfg["feedUrl"]
    req = urllib.request.Request(
        feed_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,ko;q=0.5"
        }
    )
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        raw_bytes = resp.read()
        try:
            raw_content = raw_bytes.decode(charset, errors="replace")
        except Exception:
            raw_content = raw_bytes.decode("utf-8", errors="replace")

    # Match items (RSS 2.0 / RDF) or entries (Atom)
    items = re.findall(r'<item[\s>].*?</item>', raw_content, re.DOTALL | re.IGNORECASE)
    is_atom = False
    if not items:
        items = re.findall(r'<entry[\s>].*?</entry>', raw_content, re.DOTALL | re.IGNORECASE)
        is_atom = True

    articles = []
    seen_titles = set()

    for item_xml in items:
        if len(articles) >= max_items:
            break
            
        title_raw = extract_tag(item_xml, 'title')
        title = clean_html(title_raw)
        
        # Clean specific artifacts in title
        title = re.sub(r'^\s*\[.*?\]\s*', '', title)  # remove leading tags
        if not title or title in seen_titles:
            continue
            
        link = extract_link(item_xml)
        if not link:
            continue
            
        # Extract date
        date_raw = ""
        for tag in ['pubDate', 'dc:date', 'published', 'updated', 'date']:
            date_raw = extract_tag(item_xml, tag)
            if date_raw:
                break
        pub_display, pub_iso = parse_iso_date(date_raw)
        
        # Extract snippet / description
        snippet_raw = ""
        for tag in ['description', 'summary', 'content']:
            snippet_raw = extract_tag(item_xml, tag)
            if snippet_raw:
                break
        snippet = clean_html(snippet_raw)
        if snippet:
            # Truncate clean snippet to reasonable length
            snippet = snippet[:180] + ('...' if len(snippet) > 180 else '')

        seen_titles.add(title)
        articles.append({
            "title": title,
            "link": link,
            "pubDate": pub_display,
            "pubDateIso": pub_iso,
            "snippet": snippet,
            "sourceId": cfg["id"],
            "sourceName": cfg["name"],
            "region": cfg["region"],
            "regionFlag": cfg["regionFlag"],
            "category": cfg["category"],
            "categoryName": cfg["categoryName"],
            "language": cfg["language"]
        })

    return articles

def aggregate_news():
    print(f"🚀 Starting Global News Perspectives Aggregation ({len(NEWS_SOURCES)} outlets)...")
    start_time = time.time()
    
    output_sources = []
    all_articles = []
    success_count = 0
    fail_count = 0

    for i, cfg in enumerate(NEWS_SOURCES, 1):
        print(f"[{i:02d}/{len(NEWS_SOURCES)}] Fetching {cfg['regionFlag']} {cfg['name']}...", end=" ", flush=True)
        try:
            articles = fetch_and_parse_feed(cfg)
            source_data = dict(cfg)
            source_data["articles"] = articles
            source_data["lastArticleCount"] = len(articles)
            source_data["status"] = "ok"
            output_sources.append(source_data)
            all_articles.extend(articles)
            success_count += 1
            print(f"✅ OK ({len(articles)} articles)")
        except Exception as e:
            print(f"❌ Error: {e}")
            fail_count += 1
            fallback_source = dict(cfg)
            fallback_source["articles"] = []
            fallback_source["lastArticleCount"] = 0
            fallback_source["status"] = "failed"
            fallback_source["error"] = str(e)
            output_sources.append(fallback_source)

    # Sort all articles by pubDateIso descending for the unified timeline
    all_articles.sort(key=lambda x: x.get("pubDateIso", ""), reverse=True)

    # Deduplicate timeline by title similarity or exact match
    timeline_articles = []
    seen_timeline_titles = set()
    for art in all_articles:
        norm_title = re.sub(r'[\W_]+', '', art["title"].lower())
        if norm_title not in seen_timeline_titles:
            seen_timeline_titles.add(norm_title)
            timeline_articles.append(art)

    now_utc = datetime.now(timezone.utc).isoformat()
    aggregated_data = {
        "updatedAt": now_utc,
        "totalSources": len(NEWS_SOURCES),
        "successfulSources": success_count,
        "totalArticles": len(all_articles),
        "timelineArticlesCount": len(timeline_articles),
        "regions": [
            {"id": "cn", "name": "中国视角", "flag": "🇨🇳", "count": sum(len(s.get("articles", [])) for s in output_sources if s.get("region") == "cn")},
            {"id": "jp", "name": "日本視点", "flag": "🇯🇵", "count": sum(len(s.get("articles", [])) for s in output_sources if s.get("region") == "jp")},
            {"id": "kr", "name": "한국 시선", "flag": "🇰🇷", "count": sum(len(s.get("articles", [])) for s in output_sources if s.get("region") == "kr")},
            {"id": "us", "name": "美欧全球", "flag": "🇺🇸", "count": sum(len(s.get("articles", [])) for s in output_sources if s.get("region") == "us")},
        ],
        "categories": [
            {"id": "all", "name": "全部视角"},
            {"id": "headline", "name": "综合要闻"},
            {"id": "international", "name": "国际时政"},
            {"id": "economy", "name": "财经商业"}
        ],
        "sources": output_sources,
        "timelineArticles": timeline_articles[:120]  # Top 120 realtime timeline items
    }

    # Determine output file path
    target_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "data", "global-news.json"
    )
    target_path = os.path.abspath(target_path)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(aggregated_data, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - start_time
    print(f"\n🎉 Done in {elapsed:.2f}s! Successfully aggregated {len(all_articles)} articles ({len(timeline_articles)} timeline items).")
    print(f"📁 Output saved to: {target_path}")

if __name__ == "__main__":
    aggregate_news()
