#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tech Blogs Aggregator & Normalizer
Fetches RSS/Atom feeds from top corporate engineering blogs in East Asia (Japan, Korea, China) & Global Giants,
cleanses metadata, and exports unified static JSON for frontend consumption & CI/CD deployment.
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
import xml.etree.ElementTree as ET

# Configuration of tracked corporate tech blogs
BLOG_CONFIGS = [
    # ==========================================
    # Japan (aligned with gihyo.jp techblog index)
    # ==========================================
    {
        "id": "lycorp",
        "name": "LY Corporation (LINE / Yahoo!)",
        "category": "japan",
        "url": "https://techblog.lycorp.co.jp/ja",
        "feedUrl": "https://techblog.lycorp.co.jp/ja/feed/index.xml",
        "icon": "💬",
        "desc": "LINE 与 Yahoo! JAPAN 合并后的技术团队，聚焦海量高并发分布式通信、AI Agent 与云原生架构。",
        "tags": ["高并发", "AI Agent", "微服务", "消息系统"]
    },
    {
        "id": "mercari",
        "name": "Mercari Engineering (メルカリ)",
        "category": "japan",
        "url": "https://engineering.mercari.com/blog/",
        "feedUrl": "https://engineering.mercari.com/blog/feed.xml",
        "icon": "🛍️",
        "desc": "日本知名二手交易平台，深入分享 Go 微服务治理、Kubernetes 生态、分布式事务与推荐系统。",
        "tags": ["Go", "Kubernetes", "分布式事务", "搜索推荐"]
    },
    {
        "id": "cyberagent",
        "name": "CyberAgent Developers",
        "category": "japan",
        "url": "https://developers.cyberagent.co.jp/blog/",
        "feedUrl": "https://developers.cyberagent.co.jp/blog/feed/",
        "icon": "🕊️",
        "desc": "日本互联网与数字媒体巨头，涵盖 ABEMA 大规模低延迟流媒体、广告引擎与私有 LLM 基础设施。",
        "tags": ["ABEMA", "音视频", "广告引擎", "LLM"]
    },
    {
        "id": "hatena",
        "name": "Hatena Developer Blog (はてな)",
        "category": "japan",
        "url": "https://developer.hatenastaff.com/",
        "feedUrl": "https://developer.hatenastaff.com/feed",
        "icon": "🔖",
        "desc": "日本老牌网络社交与书签服务商，深耕大规模 Web 架构长期演进、SRE 运维实践与开发者工程文化。",
        "tags": ["SRE", "Web架构", "Perl/Go", "开源文化"]
    },
    {
        "id": "cookpad",
        "name": "Cookpad TechLife (クックパッド)",
        "category": "japan",
        "url": "https://techlife.cookpad.com/",
        "feedUrl": "https://techlife.cookpad.com/feed",
        "icon": "🍳",
        "desc": "全球领先食谱社区平台，长期致力于大型单体架构现代化、移动端工程化与敏捷研发协作。",
        "tags": ["Rails", "移动端", "架构演进", "敏捷开发"]
    },
    {
        "id": "dena",
        "name": "DeNA Engineer Blog",
        "category": "japan",
        "url": "https://engineer.dena.com/",
        "feedUrl": "https://engineer.dena.com/index.xml",
        "icon": "🎮",
        "desc": "日本综合互联网与游戏巨头，专注移动游戏引擎底层优化、自动驾驶前沿研发与云原生架构。",
        "tags": ["游戏引擎", "AI研发", "移动架构", "云原生"]
    },
    {
        "id": "zozo",
        "name": "ZOZO Tech Blog",
        "category": "japan",
        "url": "https://techblog.zozo.com/",
        "feedUrl": "https://techblog.zozo.com/feed",
        "icon": "👗",
        "desc": "日本最大潮流时尚电商技术团队，分享个性化多模态推荐、GraphQL 微服务重构与云原生海量吞吐架构。",
        "tags": ["推荐系统", "GraphQL", "视觉AI", "云原生"]
    },
    {
        "id": "pixiv",
        "name": "inside pixiv (ピクシブ)",
        "category": "japan",
        "url": "https://inside.pixiv.blog/",
        "feedUrl": "https://inside.pixiv.blog/feed",
        "icon": "🎨",
        "desc": "全球知名 ACG 创作社区，深入分享海量图像视频处理、分布式存储、高性能搜索与创作者生态。",
        "tags": ["海量媒体", "图像处理", "搜索架构", "Go/PHP"]
    },
    {
        "id": "cybozu",
        "name": "Cybozu Inside Out (サイボウズ)",
        "category": "japan",
        "url": "https://blog.cybozu.io/",
        "feedUrl": "https://blog.cybozu.io/feed",
        "icon": "🏢",
        "desc": "日本协同办公软件巨头（kintone 开发商），专注自建 Kubernetes 私有云、SRE 混沌工程与现代前端。",
        "tags": ["kintone", "私有云", "SRE", "Kubernetes"]
    },
    {
        "id": "freee",
        "name": "freee Developers Hub",
        "category": "japan",
        "url": "https://developers.freee.co.jp/",
        "feedUrl": "https://developers.freee.co.jp/feed",
        "icon": "💼",
        "desc": "日本第一大云财务与 ERP SaaS 平台，分享大型单体解耦、细粒度多租户权限系统与基础设施自动化。",
        "tags": ["ERP/SaaS", "单体拆分", "安全架构", "Ruby/Go"]
    },
    {
        "id": "layerx",
        "name": "LayerX Tech Blog",
        "category": "japan",
        "url": "https://tech.layerx.co.jp/",
        "feedUrl": "https://tech.layerx.co.jp/feed",
        "icon": "⚡",
        "desc": "日本企业级 Fintech 与 LLM AI Agent 领跑独角兽，专注知识图谱、企业自动化工作流与前沿区块链落地。",
        "tags": ["LLM Agent", "知识图谱", "Fintech", "区块链"]
    },
    {
        "id": "kakehashi",
        "name": "Kakehashi Tech Blog (カケハシ)",
        "category": "japan",
        "url": "https://kakehashi-dev.hatenablog.com/",
        "feedUrl": "https://kakehashi-dev.hatenablog.com/feed",
        "icon": "💊",
        "desc": "日本医药健康 DX 领域高增长独角兽，深入实践领域驱动设计（DDD）、AWS Serverless 与可进化架构。",
        "tags": ["DDD", "Serverless", "医疗DX", "TypeScript"]
    },
    {
        "id": "paypay",
        "name": "PayPay Inside-Out",
        "category": "japan",
        "url": "https://blog.paypay.ne.jp/",
        "feedUrl": "https://blog.paypay.ne.jp/feed/",
        "icon": "💳",
        "desc": "日本第一大移动支付平台，剖析千万人级金融高频交易处理、微服务容灾演练与全球化工程协作。",
        "tags": ["移动支付", "金融高并发", "微服务", "测试自动化"]
    },
    {
        "id": "classmethod",
        "name": "DevelopersIO (Classmethod)",
        "category": "japan",
        "url": "https://dev.classmethod.jp/",
        "feedUrl": "https://dev.classmethod.jp/feed/",
        "icon": "🛠️",
        "desc": "日本顶级云计算技术博客社区，日更分享 AWS 深度架构实践、CI/CD 自动化与生成式 AI 落地实战。",
        "tags": ["AWS", "云计算", "DevOps", "AI实操"]
    },
    {
        "id": "smarthr",
        "name": "SmartHR Tech Blog",
        "category": "japan",
        "url": "https://tech.smarthr.jp/",
        "feedUrl": "https://tech.smarthr.jp/feed",
        "icon": "🤝",
        "desc": "日本顶尖劳务 HR SaaS 独角兽，分享多租户微服务架构、TypeScript 前端体系与可访问性设计。",
        "tags": ["SaaS架构", "TypeScript", "多租户", "Accessibility"]
    },
    {
        "id": "sansan",
        "name": "Sansan Builders Box",
        "category": "japan",
        "url": "https://buildersbox.corp-sansan.com/",
        "feedUrl": "https://buildersbox.corp-sansan.com/feed",
        "icon": "📇",
        "desc": "商务名片管理与企业关系网络 SaaS 先驱，深耕高精度 OCR 图像识别、知识图谱与海量数据建模。",
        "tags": ["OCR技术", "知识图谱", "企业级SaaS", "数据建模"]
    },
    {
        "id": "nikkei",
        "name": "NIKKEI TECH BLOG (日本経済新聞社)",
        "category": "japan",
        "url": "https://hack.nikkei.com/blog/",
        "feedUrl": "https://hack.nikkei.com/rss.xml",
        "icon": "📰",
        "desc": "日本经济新闻社官方技术博客，分享日经电子版高并发微服务、数据与AI中台、媒体DX转型及全球化工程实践。",
        "tags": ["日经电子版", "媒体DX", "AI与数据", "云原生架构"]
    },


    # ==========================================
    # Korea (Top Tech Unicorns & Tech Giants)
    # ==========================================
    {
        "id": "naver_d2",
        "name": "NAVER D2",
        "category": "korea",
        "url": "https://d2.naver.com/home",
        "feedUrl": "https://d2.naver.com/d2.atom",
        "icon": "🟢",
        "desc": "韩国最大互联网与搜索门户 NAVER 开发者平台，硬核分享超大规模分布式架构、自研 HyperCLOVA LLM 与搜索底层。",
        "tags": ["搜索引擎", "HyperCLOVA", "分布式系统", "基础软件"]
    },
    {
        "id": "kakao",
        "name": "Kakao Tech (카카오)",
        "category": "korea",
        "url": "https://tech.kakao.com/",
        "feedUrl": "https://tech.kakao.com/feed/",
        "icon": "🟡",
        "desc": "韩国国民移动通讯巨头 Kakao 官方工程团队，探讨海量即时通信、移动端跨端框架、AI Agent 架构与大数据平台。",
        "tags": ["即时通讯", "AI Agent", "移动工程", "大数据"]
    },
    {
        "id": "toss",
        "name": "Toss Tech (Viva Republica)",
        "category": "korea",
        "url": "https://toss.tech/",
        "feedUrl": "https://toss.tech/rss.xml",
        "icon": "💙",
        "desc": "韩国现象级金融科技与移动银行超级独角兽，业界公认的顶尖全栈 TypeScript 实践、Serverless 与极致交互体验。",
        "tags": ["Fintech", "TypeScript", "Serverless", "前端工程"]
    },
    {
        "id": "daangn",
        "name": "Karrot Engineering (당근)",
        "category": "korea",
        "url": "https://medium.com/daangn",
        "feedUrl": "https://medium.com/feed/daangn",
        "icon": "🥕",
        "desc": "韩国超高活跃度二手交易与本地生活社区独角兽，分享海量实时地理空间索引、微服务事件流与高可用推送系统。",
        "tags": ["地理空间", "微服务", "高并发", "社区生态"]
    },
    {
        "id": "coupang",
        "name": "Coupang Engineering (쿠팡)",
        "category": "korea",
        "url": "https://medium.com/coupang-engineering",
        "feedUrl": "https://medium.com/feed/coupang-engineering",
        "icon": "🚀",
        "desc": "韩国最大综合电商巨头（美股上市），深入解析百亿级商品流调度、智能仓储物流与海量推荐机器学习。",
        "tags": ["智能物流", "电商中台", "推荐算法", "机器学习"]
    },
    {
        "id": "nhncloud",
        "name": "NHN Cloud Meetup",
        "category": "korea",
        "url": "https://meetup.nhncloud.com/",
        "feedUrl": "https://meetup.nhncloud.com/rss",
        "icon": "☁️",
        "desc": "韩国老牌综合 IT 与云计算巨头 NHN，深度分享企业级公有云与私有云基础设施、DevOps 与安全网络实践。",
        "tags": ["云计算", "Kubernetes", "DevOps", "网络安全"]
    },
    {
        "id": "lineplus",
        "name": "LINE Plus Engineering (KR)",
        "category": "korea",
        "url": "https://engineering.linecorp.com/ko",
        "feedUrl": "https://engineering.linecorp.com/ko/feed/",
        "icon": "📱",
        "desc": "LINE 韩国研发中心核心技术博客，深入探讨全球数十亿消息吞吐系统、数据库运维与跨端通信底层。",
        "tags": ["消息系统", "全球化", "跨端通信", "数据库"]
    },

    # ==========================================
    # China Tech Teams & Open Source
    # ==========================================
    {
        "id": "meituan",
        "name": "美团技术团队 (Meituan Tech)",
        "category": "china",
        "url": "https://tech.meituan.com/",
        "feedUrl": "https://tech.meituan.com/feed/",
        "icon": "🚴",
        "desc": "国内生活服务科技领军团队，深入分享高并发分布式交易引擎、大模型在多业务落地实践与前端架构体系。",
        "tags": ["调度引擎", "大模型落地", "高并发", "前端工程"]
    },
    {
        "id": "youzan",
        "name": "有赞技术团队 (Youzan Tech)",
        "category": "china",
        "url": "https://tech.youzan.com/",
        "feedUrl": "https://tech.youzan.com/rss/",
        "icon": "🛒",
        "desc": "国内电商零售 SaaS 标杆技术团队，长期深耕分布式微服务治理、高性能缓存架构与知识库检索工程化。",
        "tags": ["零售SaaS", "微服务", "高并发", "缓存架构"]
    },
    {
        "id": "pingcap",
        "name": "PingCAP Tech Blog (TiDB)",
        "category": "china",
        "url": "https://pingcap.com/blog/",
        "feedUrl": "https://pingcap.com/blog/feed/",
        "icon": "🐬",
        "desc": "全球开源分布式关系型数据库 TiDB 研发团队，硬核分享 Raft 强一致性、HTAP 分布式执行引擎与存储架构。",
        "tags": ["TiDB", "分布式数据库", "Raft", "HTAP"]
    },
    {
        "id": "tw93",
        "name": "潮流周刊 (Tw93 / 阿里前端专家)",
        "category": "china",
        "url": "https://weekly.tw93.fun/",
        "feedUrl": "https://weekly.tw93.fun/rss.xml",
        "icon": "✨",
        "desc": "阿里巴巴前端技术专家 Tw93 主理的高影响力每周技术与产品雷达，精选现代前端工程、极客工具与前沿科技趋势。",
        "tags": ["科技周刊", "前端工程", "极客工具", "独立开发"]
    },
    {
        "id": "segmentfault",
        "name": "SegmentFault 思否技术头条",
        "category": "china",
        "url": "https://segmentfault.com/",
        "feedUrl": "https://segmentfault.com/feeds",
        "icon": "💡",
        "desc": "国内领先的专业开发者技术交流社区，涵盖全栈开发、开源生态、云原生与一线技术团队实践深度文章。",
        "tags": ["开源生态", "全栈开发", "架构设计", "开发者社区"]
    },
    {
        "id": "deepin",
        "name": "深度开源社区 (Deepin Linux)",
        "category": "china",
        "url": "https://www.deepin.org/zh/",
        "feedUrl": "https://www.deepin.org/zh/feed/",
        "icon": "🐧",
        "desc": "中国知名开源桌面操作系统与统信软件核心研发团队，深入分享 Linux 内核适配、桌面环境组件与系统级调优。",
        "tags": ["Linux内核", "操作系统", "开源生态", "桌面环境"]
    },
    {
        "id": "hellogithub",
        "name": "HelloGitHub 开源社区",
        "category": "china",
        "url": "https://hellogithub.com/",
        "feedUrl": "https://hellogithub.com/rss",
        "icon": "🌟",
        "desc": "优质开源项目月度技术雷达，涵盖 Python、Go、Rust、前端等多领域硬核开源项目深度解读与应用。",
        "tags": ["开源项目", "技术雷达", "开发者生态", "极客工具"]
    },
    {
        "id": "ruanyifeng",
        "name": "阮一峰的网络日志",
        "category": "china",
        "url": "https://www.ruanyifeng.com/blog/",
        "feedUrl": "https://www.ruanyifeng.com/blog/atom.xml",
        "icon": "📖",
        "desc": "国内最具影响力的技术博客之一，以清晰优雅的文笔解读 Web 技术标准、计算机基础原理与科技前沿思考。",
        "tags": ["科技周刊", "Web标准", "计算机通识", "前端开发"]
    },
    {
        "id": "codingnow",
        "name": "云风的 BLOG (Codingnow)",
        "category": "china",
        "url": "https://blog.codingnow.com/",
        "feedUrl": "https://blog.codingnow.com/atom.xml",
        "icon": "🎮",
        "desc": "原网易核心架构师、skynet 开源框架作者，长期分享硬核 C/Lua 系统底层设计、高并发 Actor 模式与游戏引擎实践。",
        "tags": ["C/Lua", "游戏引擎", "skynet", "底层并发"]
    },
    {
        "id": "draveness",
        "name": "面向信仰编程 (Draveness)",
        "category": "china",
        "url": "https://draveness.me/",
        "feedUrl": "https://draveness.me/feed.xml",
        "icon": "🕊️",
        "desc": "《Go语言设计与实现》作者 Draveness，深入浅出解构 Go 运行时机制、Kubernetes 调度、分布式系统与架构演进。",
        "tags": ["Go内核", "K8s", "分布式系统", "系统设计"]
    },
    {
        "id": "emqx",
        "name": "EMQ 技术博客 (EMQX)",
        "category": "china",
        "url": "https://www.emqx.com/zh/blog",
        "feedUrl": "https://www.emqx.com/rss.xml",
        "icon": "⚡",
        "desc": "全球领先的开源物联网 MQTT 消息服务器与流处理基础设施团队，专注海量高并发 Actor 分布式架构与边缘计算。",
        "tags": ["MQTT", "物联网", "Erlang/Elixir", "流处理"]
    },
    {
        "id": "oceanbase",
        "name": "OceanBase 技术博客",
        "category": "china",
        "url": "https://open.oceanbase.com/blog",
        "feedUrl": "https://open.oceanbase.com/blog",
        "icon": "🌊",
        "desc": "金融级原生分布式关系型数据库团队，硬核剖析 Paxos 一致性协议、LSM-Tree 高性能存储引擎与 HTAP 架构。",
        "tags": ["分布式数据库", "Paxos", "HTAP", "存储引擎"]
    },
    {
        "id": "solidot",
        "name": "Solidot (奇客资讯)",
        "category": "china",
        "url": "https://www.solidot.org/",
        "feedUrl": "https://www.solidot.org/index.rss",
        "icon": "📰",
        "desc": "中文互联网老牌开源与极客前沿资讯窗口，专注 Linux 内核动态、网络安全、开源生态演进与科技硬核讨论。",
        "tags": ["开源生态", "网络安全", "Linux", "极客资讯"]
    },
    {
        "id": "coolshell",
        "name": "酷 壳 – CoolShell",
        "category": "china",
        "url": "https://coolshell.cn/",
        "feedUrl": "https://coolshell.cn/feed",
        "icon": "🐚",
        "desc": "陈皓（左耳朵耗子）经典技术博客，沉淀海量高可用分布式架构模式、系统性能调优秘籍与严谨工程师文化。",
        "tags": ["系统架构", "性能调优", "分布式", "工程哲学"]
    },
    {
        "id": "jiqizhixin",
        "name": "机器之心 (Synced)",
        "category": "china",
        "url": "https://www.jiqizhixin.com/",
        "feedUrl": "https://www.jiqizhixin.com/",
        "icon": "🤖",
        "desc": "前沿人工智能科技媒体与产业智库，深度追踪大模型前沿架构（LLM/Transformer）、多模态与 AI Infra 算力集群演进。",
        "tags": ["大模型", "Transformer", "AI Infra", "多模态"]
    },
    {
        "id": "apisix",
        "name": "Apache APISIX 博客",
        "category": "china",
        "url": "https://apisix.apache.org/zh/blog/",
        "feedUrl": "https://apisix.apache.org/zh/blog/atom.xml",
        "icon": "🚀",
        "desc": "Apache 顶尖开源动态云原生微服务与 API 网关团队，专注海量请求动态路由、OpenResty/Wasm 插件与流量治理。",
        "tags": ["API网关", "云原生", "微服务治理", "OpenResty"]
    },
    {
        "id": "zilliz",
        "name": "Zilliz / Milvus 技术博客",
        "category": "china",
        "url": "https://zilliz.com.cn/blog",
        "feedUrl": "https://zilliz.com.cn/blog",
        "icon": "📐",
        "desc": "全球知名开源向量数据库 Milvus 研发团队，聚焦 AI 时代非结构化数据检索、多模态 Embedding 与 RAG 检索增强架构。",
        "tags": ["向量数据库", "Milvus", "RAG检索", "AI Infra"]
    },
    {
        "id": "doris",
        "name": "Apache Doris 技术博客",
        "category": "china",
        "url": "https://doris.apache.org/zh-CN/blog/",
        "feedUrl": "https://doris.apache.org/zh-CN/blog/atom.xml",
        "icon": "📊",
        "desc": "高性能实时分析型数据库 (OLAP) 核心团队，硬核分享向量化执行引擎、分布式查询优化器与大规模湖仓一体架构。",
        "tags": ["实时数仓", "OLAP", "向量化引擎", "湖仓一体"]
    },
    {
        "id": "tonybai",
        "name": "Tony Bai (白明)",
        "category": "china",
        "url": "https://tonybai.com/",
        "feedUrl": "https://tonybai.com/feed/",
        "icon": "🐿️",
        "desc": "国内知名资深 Go 语言专家与技术布道师，持续深耕 Go 运行时剖析、编译优化、云原生架构演进与现代编程范式。",
        "tags": ["Go语言", "云原生", "代码重构", "微服务架构"]
    },
    {
        "id": "halfrost",
        "name": "Halfrost (冰霜之地)",
        "category": "china",
        "url": "https://halfrost.com/",
        "feedUrl": "https://halfrost.com/rss/",
        "icon": "❄️",
        "desc": "专注于底层网络通信协议（深入剖析 HTTP/3、QUIC、TCP/IP 与 TLS）、高并发服务端架构与分布式算法体系。",
        "tags": ["网络协议", "HTTP/3 & QUIC", "Go算法", "网络调优"]
    },
    {
        "id": "zhangxinxu",
        "name": "张鑫旭 (鑫空间-鑫生活)",
        "category": "china",
        "url": "https://www.zhangxinxu.com/wordpress/",
        "feedUrl": "https://www.zhangxinxu.com/wordpress/feed/",
        "icon": "🎨",
        "desc": "知名 Web 前端技术专家，十余年专注现代 CSS 标准规范演进、SVG/Canvas 图形渲染与极致无障碍交互工程。",
        "tags": ["CSS3/CSS4", "Web标准", "SVG图形", "前端工程"]
    },
    {
        "id": "ctriptech",
        "name": "携程技术团队 (Ctrip Tech)",
        "category": "china",
        "url": "https://ctriptech.github.io/",
        "feedUrl": "https://ctriptech.github.io/",
        "icon": "🐬",
        "desc": "全球领先在线旅游巨头技术中台，深入分享千万级高并发票务交易、Apollo 动态配置中心演进与单元化异地多活灾备。",
        "tags": ["高并发交易", "Apollo", "异地多活", "服务治理"]
    },
    {
        "id": "xiaolincoding",
        "name": "小林coding",
        "category": "china",
        "url": "https://xiaolincoding.com/",
        "feedUrl": "https://xiaolincoding.com/",
        "icon": "📘",
        "desc": "《图解网络》《图解系统》作者，系统化图解计算机网络底层、Linux 内核调度与 MySQL/Redis 高性能存储中间件。",
        "tags": ["图解网络", "Linux内核", "MySQL", "Redis"]
    },

    # ==========================================
    # Global Tech Giants
    # ==========================================
    {
        "id": "cloudflare",
        "name": "Cloudflare Blog",
        "category": "global",
        "url": "https://blog.cloudflare.com/",
        "feedUrl": "https://blog.cloudflare.com/rss/",
        "icon": "☁️",
        "desc": "全球边缘网络与网络安全巨擘，深度长文剖析 Linux 内核优化、BGP 路由、Zero Trust 与 Rust 边缘计算。",
        "tags": ["边缘计算", "网络协议", "Rust", "网络安全"]
    },
    {
        "id": "github",
        "name": "GitHub Engineering",
        "category": "global",
        "url": "https://github.blog/category/engineering/",
        "feedUrl": "https://github.blog/category/engineering/feed/",
        "icon": "🐙",
        "desc": "全球最大开源平台工程博客，揭秘 Git 底层引擎优化、超大规模 MySQL 高可用架构与 Copilot 基础设施。",
        "tags": ["Git架构", "MySQL容灾", "DevOps", "AI工具链"]
    },
    {
        "id": "netflix",
        "name": "Netflix TechBlog",
        "category": "global",
        "url": "https://netflixtechblog.com/",
        "feedUrl": "https://netflixtechblog.com/feed",
        "icon": "🎬",
        "desc": "微服务与混沌工程理念开创者，分享 PB 级分布式流式计算、视频感知编码与个性化推荐算法演进。",
        "tags": ["混沌工程", "流式计算", "微服务", "推荐系统"]
    },
    {
        "id": "meta",
        "name": "Meta Engineering (Facebook)",
        "category": "global",
        "url": "https://engineering.fb.com/",
        "feedUrl": "https://engineering.fb.com/feed/",
        "icon": "🌐",
        "desc": "Meta 核心工程博客，涵盖 PyTorch 深度学习框架内核演进、全球超算集群拓扑与 React 底层机制。",
        "tags": ["PyTorch", "AI集群", "React内核", "分布式系统"]
    },
    {
        "id": "googleai",
        "name": "Google AI Research Blog",
        "category": "global",
        "url": "https://blog.google/technology/ai/",
        "feedUrl": "https://blog.google/technology/ai/rss/",
        "icon": "🧠",
        "desc": "谷歌人工智能前沿研究发布窗口，实时同步 Gemini 系列大模型、多模态前沿进展与负责任 AI 实践。",
        "tags": ["Gemini", "多模态", "深度学习", "前沿算法"]
    },
    {
        "id": "aws",
        "name": "AWS Architecture Blog",
        "category": "global",
        "url": "https://aws.amazon.com/blogs/architecture/",
        "feedUrl": "https://aws.amazon.com/blogs/architecture/feed/",
        "icon": "📐",
        "desc": "亚马逊 AWS 官方架构师团队，剖析 Well-Architected 架构框架、无服务器 Serverless 与跨可用区容灾设想。",
        "tags": ["Well-Architected", "Serverless", "容灾架构", "云原生"]
    },
    {
        "id": "vercel",
        "name": "Vercel Blog",
        "category": "global",
        "url": "https://vercel.com/blog",
        "feedUrl": "https://vercel.com/atom",
        "icon": "▲",
        "desc": "现代前端部署与云平台领航者，Next.js、Turborepo 以及全栈 Serverless/Edge 运行时演进一手技术解读。",
        "tags": ["Next.js", "Serverless", "前端工程化", "Edge"]
    }
]

def clean_text(text: str) -> str:
    """Strip tags and unescape html entities."""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return " ".join(text.split())

def parse_date(date_str: str, link: str = "") -> str:
    """Normalize various date formats into YYYY-MM-DD."""
    if not date_str:
        m = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', link)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    date_str = date_str.strip()

    # ISO formats like 2026-09-30T14:54:45Z
    if len(date_str) >= 10 and date_str[4] == '-' and date_str[7] == '-':
        return date_str[:10]

    # RFC 2822: Wed, 30 Sep 2026 02:00:00 GMT
    months = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    m = re.search(r'(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})', date_str)
    if m:
        day = int(m.group(1))
        mon = months.get(m.group(2), '01')
        year = m.group(3)
        return f"{year}-{mon}-{day:02d}"

    m = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', link)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]
_ua_idx = 0

def fetch_feed(url: str, timeout: int = 15) -> bytes:
    """Fetch raw XML content with robust headers and SSL handling."""
    global _ua_idx
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    ua = USER_AGENTS[_ua_idx % len(USER_AGENTS)]
    _ua_idx += 1

    headers = {
        "User-Agent": ua,
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.8"
    }

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.read()

def parse_feed_content(content: bytes, blog_id: str, limit: int = 5):
    """Parse RSS 2.0 or Atom XML with resilient fallback for malformed feeds."""
    articles = []
    root = None

    try:
        root = ET.fromstring(content)
    except Exception:
        pass

    if root is None:
        try:
            # Fallback: sanitize invalid chars & fix naked ampersands
            text = content.decode('utf-8', errors='ignore')
            text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
            text = re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[a-fA-F0-9]+);)', '&amp;', text)
            root = ET.fromstring(text.encode('utf-8'))
        except Exception as e:
            pass

    if root is not None:
        # Check if Atom feed
        is_atom = root.tag.endswith('feed') or '{http://www.w3.org/2005/Atom}' in root.tag

        if is_atom:
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            if not entries:
                entries = [el for el in root if el.tag.endswith('entry')]

            for entry in entries[:limit]:
                title_el = entry.find('{http://www.w3.org/2005/Atom}title')
                if title_el is None:
                    title_el = next((c for c in entry if c.tag.endswith('title')), None)
                title = clean_text(title_el.text if title_el is not None else "无标题")

                link = ""
                for l in entry.findall('{http://www.w3.org/2005/Atom}link') or [c for c in entry if c.tag.endswith('link')]:
                    rel = l.attrib.get('rel', 'alternate')
                    if rel in ('alternate', '') and 'href' in l.attrib:
                        link = l.attrib['href'].strip()
                        break
                if not link and entry.find('link') is not None:
                    link = (entry.find('link').text or "").strip()

                date_el = entry.find('{http://www.w3.org/2005/Atom}published')
                if date_el is None:
                    date_el = entry.find('{http://www.w3.org/2005/Atom}updated')
                if date_el is None:
                    date_el = next((c for c in entry if c.tag.endswith(('published', 'updated', 'date'))), None)
                raw_date = date_el.text if date_el is not None and date_el.text else ""
                pub_date = parse_date(raw_date, link)

                summary_el = entry.find('{http://www.w3.org/2005/Atom}summary')
                if summary_el is None:
                    summary_el = entry.find('{http://www.w3.org/2005/Atom}content')
                summary = clean_text(summary_el.text if summary_el is not None else "")
                if len(summary) > 120:
                    summary = summary[:120] + "..."

                if title and link:
                    articles.append({
                        "title": title,
                        "link": link,
                        "pubDate": pub_date,
                        "summary": summary
                    })
        else:
            # RSS 2.0 or RSS 1.0 (RDF)
            items = root.findall('.//item')
            for item in items[:limit]:
                title_el = item.find('title')
                title = clean_text(title_el.text if title_el is not None else "无标题")

                link_el = item.find('link')
                link = (link_el.text or "").strip() if link_el is not None else ""
                if not link:
                    guid_el = item.find('guid')
                    if guid_el is not None and guid_el.text and guid_el.text.startswith('http'):
                        link = guid_el.text.strip()

                date_el = item.find('pubDate')
                if date_el is None:
                    date_el = next((c for c in item if c.tag.endswith('date')), None)
                raw_date = date_el.text if date_el is not None and date_el.text else ""
                pub_date = parse_date(raw_date, link)

                desc_el = item.find('description')
                desc = clean_text(desc_el.text if desc_el is not None else "")
                if len(desc) > 120:
                    desc = desc[:120] + "..."

                if title and link:
                    articles.append({
                        "title": title,
                        "link": link,
                        "pubDate": pub_date,
                        "summary": desc
                    })

    # Regex emergency fallback if XML parser failed
    if not articles:
        try:
            text = content.decode('utf-8', errors='ignore')
            # Extract item/entry blocks
            item_blocks = re.findall(r'<(?:item|entry)[\s>](.*?)</(?:item|entry)>', text, re.DOTALL | re.IGNORECASE)
            for block in item_blocks[:limit]:
                t_match = re.search(r'<title[^>]*>(.*?)</title>', block, re.DOTALL | re.IGNORECASE)
                l_match = re.search(r'<link[^>]*href=["\']([^"\']+)["\']|<link[^>]*>(.*?)</link>|<guid[^>]*>(https?://.*?)</guid>', block, re.DOTALL | re.IGNORECASE)
                d_match = re.search(r'<(?:pubDate|published|updated|dc:date)[^>]*>(.*?)</(?:pubDate|published|updated|dc:date)>', block, re.DOTALL | re.IGNORECASE)

                t = clean_text(t_match.group(1)) if t_match else ""
                l = ""
                if l_match:
                    l = (l_match.group(1) or l_match.group(2) or l_match.group(3) or "").strip()
                d = clean_text(d_match.group(1)) if d_match else ""
                p_date = parse_date(d, l)

                if t and l:
                    articles.append({
                        "title": t,
                        "link": l,
                        "pubDate": p_date,
                        "summary": ""
                    })
        except Exception:
            pass

    return articles

def run_aggregation(output_path: str = "data/tech-blogs.json"):
    """Main aggregation pipeline."""
    print("🚀 Starting Tech Blogs Aggregation...")

    existing_blogs_map = {}
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
                for b in old_data.get('blogs', []):
                    existing_blogs_map[b['id']] = b.get('articles', [])
            print(f"📦 Loaded existing fallback cache for {len(existing_blogs_map)} blogs.")
        except Exception as e:
            print(f"⚠️ Could not load existing cache: {e}")

    aggregated_blogs = []
    total_articles_count = 0

    for blog in BLOG_CONFIGS:
        b_id = blog['id']
        b_name = blog['name']
        feed_url = blog['feedUrl']
        print(f"📡 Fetching: {b_name} ({feed_url})...", end=" ", flush=True)

        articles = []
        try:
            raw_xml = fetch_feed(feed_url, timeout=12)
            articles = parse_feed_content(raw_xml, b_id, limit=5)
            print(f"✅ OK ({len(articles)} items)")
        except urllib.error.HTTPError as he:
            if he.code == 429:
                print("⏳ Rate limited (429), waiting 2.5s and retrying...", end=" ", flush=True)
                time.sleep(2.5)
                try:
                    raw_xml = fetch_feed(feed_url, timeout=12)
                    articles = parse_feed_content(raw_xml, b_id, limit=5)
                    print(f"✅ OK on retry ({len(articles)} items)")
                except Exception as e2:
                    print(f"❌ Failed after retry: {e2}")
            else:
                print(f"❌ Failed: {he}")
        except Exception as e:
            print(f"❌ Failed: {e}")

        # Fallback to cached articles if fetch failed or empty
        if not articles and b_id in existing_blogs_map and existing_blogs_map[b_id]:
            articles = existing_blogs_map[b_id]
            print(f"   ↳ Fallback to {len(articles)} cached items")

        time.sleep(0.8)  # Polite delay between requests

        total_articles_count += len(articles)

        aggregated_blogs.append({
            "id": blog["id"],
            "name": blog["name"],
            "category": blog["category"],
            "url": blog["url"],
            "feedUrl": blog["feedUrl"],
            "icon": blog["icon"],
            "desc": blog["desc"],
            "tags": blog["tags"],
            "articles": articles
        })

    result_data = {
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "totalBlogs": len(aggregated_blogs),
        "totalArticles": total_articles_count,
        "categories": [
            {"id": "all", "name": "全部博客"},
            {"id": "japan", "name": "日本名企 (gihyo.jp 体系)"},
            {"id": "korea", "name": "韩国名企 (NAVER / Kakao / Toss)"},
            {"id": "china", "name": "国内名企前沿"},
            {"id": "global", "name": "全球科技巨头"}
        ],
        "blogs": aggregated_blogs
    }

    # Ensure output dir exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Aggregation completed! Output written to {output_path}")
    print(f"📊 Summary: {len(aggregated_blogs)} blogs, {total_articles_count} total articles.")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "data/tech-blogs.json"
    run_aggregation(out_file)
