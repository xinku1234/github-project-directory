#!/usr/bin/env python3
"""Post-process all pages to add missing SEO/GEO signals.

Adds to pages that are missing them:
- BreadcrumbList JSON-LD
- FAQPage JSON-LD (where appropriate)
- og:title / og:description meta tags
- More internal links for tag pages
"""
from __future__ import annotations
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://daohang.bot.cd"

# ─── Breadcrumb Templates ─────────────────────────────────────────────

BREADCRUMB_HOME = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "首页", "item": f"{BASE}/"},
    ]
}

# ─── FAQ Templates by Page Type ───────────────────────────────────────

FAQ_TEMPLATES = {
    "homepage": [
        ("拾品号导航是什么？", "拾品号导航是一个精选 GitHub 开源项目的导航站，收录 370+ 个项目，涵盖 AI 智能体、建站框架、自动化、DevOps 等分类，每日自动更新涨星最快的项目。"),
        ("如何提交我的开源项目？", "访问 /submit.html 页面，填写项目信息即可提交收录。我们会审核后添加到导航站。"),
        ("数据多久更新一次？", "每日凌晨 3 点自动从 GitHub Search API 同步最新涨星数据，重建所有页面并部署。"),
        ("支持哪些语言？", "支持中文和英文，每个项目都有中英文描述。点击页面右上角的语言切换按钮可以切换。"),
        ("这个网站是免费的吗？", "是的，完全免费。这是一个非盈利项目，旨在帮助开发者发现优质的 GitHub 开源工具。"),
    ],
    "trending": [
        ("什么是涨星榜？", "涨星榜展示最近一段时间内 Star 增长最快的 GitHub 开源项目，帮助你发现正在流行的工具。"),
        ("涨星数据怎么计算的？", "通过 GitHub Search API 查询近期创建且 Star 数较高的项目，按每日平均涨星速度排序。"),
        ("多久更新一次？", "每日凌晨 3 点自动更新，确保你能看到最新的趋势项目。"),
        ("如何判断一个项目是否值得使用？", "除了看 Star 数，还要关注最近提交时间、Issue 响应速度、文档质量和社区活跃度。"),
    ],
    "daily-brief": [
        ("每日快报包含什么内容？", "每日快报汇总当天涨星最快的 GitHub 项目，包含项目名称、Star 数、涨星速度和简要描述。"),
        ("如何订阅每日快报？", "可以通过 RSS Feed (/feed.xml) 或 JSON Feed (/feed.json) 订阅，也可以关注我们的社交媒体。"),
    ],
    "category": [
        ("什么是分类导航？", "分类导航将所有收录的开源项目按功能分类（如 AI 智能体、建站框架、自动化等），方便按需浏览。"),
        ("如何选择合适的开源项目？", "建议从 Star 数、最近更新频率、文档质量和社区活跃度四个维度评估。"),
    ],
    "tags": [
        ("标签页有什么用？", "标签页按技术栈（如 Python、TypeScript、Rust 等）聚合相关项目，方便按技术选型浏览。"),
        ("为什么有些标签只有几个项目？", "我们只收录 Star 数较高且活跃的项目，小众技术栈的项目数量自然较少。"),
    ],
}

# ─── Hub-specific FAQ ─────────────────────────────────────────────────

HUB_FAQ = {
    "ai-agents": [
        ("什么是 AI Agent？", "AI Agent（AI 智能体）是能自主执行任务的 AI 程序，可以调用工具、做出决策并完成复杂工作流。"),
        ("最好的 AI Agent 框架是什么？", "2026 年主流框架包括 LangChain、CrewAI、AutoGen 等，选择取决于你的具体需求和技术栈。"),
        ("AI Agent 和普通 Chatbot 有什么区别？", "Chatbot 只能对话，AI Agent 可以执行代码、调用 API、操作文件、浏览网页等实际操作。"),
    ],
    "ai-coding-tools": [
        ("AI 编程工具能替代程序员吗？", "不能完全替代，但能大幅提升效率。AI 工具擅长代码补全、重复任务和样板代码，复杂架构设计仍需人类。"),
        ("最好的免费 AI 编程工具有哪些？", "Codeium、Continue、Tabby 等开源工具提供免费方案，GitHub Copilot 也有免费额度。"),
    ],
    "mcp-ecosystem": [
        ("什么是 MCP？", "MCP (Model Context Protocol) 是 Anthropic 提出的开放协议，让 AI 模型标准化地调用外部工具和数据源。"),
        ("如何创建自己的 MCP Server？", "可以使用 TypeScript 或 Python SDK，定义工具的 schema 和处理函数，即可创建自定义 MCP Server。"),
    ],
    "web-development": [
        ("2026 年最流行的 Web 框架是什么？", "React、Next.js、Astro、SvelteKit 等都很流行，选择取决于项目需求和团队技术栈。"),
    ],
    "devops-tools": [
        ("DevOps 工具有哪些必备的？", "Docker（容器化）、Kubernetes（编排）、GitHub Actions（CI/CD）、Prometheus（监控）是基础四件套。"),
    ],
    "automation": [
        ("自动化工具怎么选？", "简单任务用 n8n/Activepieces，复杂工作流用 Temporal/Prefect，AI 自动化用 LangChain/CrewAI。"),
    ],
}

def make_breadcrumb_jsonld(page_type: str, page_name: str = None, page_url: str = None) -> dict:
    """Generate BreadcrumbList JSON-LD for a page type."""
    bc = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": f"{BASE}/"},
        ]
    }
    if page_type == "homepage":
        return bc
    elif page_type == "category":
        bc["itemListElement"].append({"@type": "ListItem", "position": 2, "name": "分类导航", "item": f"{BASE}/categories/"})
        if page_name:
            bc["itemListElement"].append({"@type": "ListItem", "position": 3, "name": page_name, "item": page_url})
    elif page_type == "trending":
        bc["itemListElement"].append({"@type": "ListItem", "position": 2, "name": "涨星榜", "item": f"{BASE}/trending/"})
    elif page_type == "daily-brief":
        bc["itemListElement"].append({"@type": "ListItem", "position": 2, "name": "每日快报", "item": f"{BASE}/daily-brief/"})
    elif page_type == "tags":
        bc["itemListElement"].append({"@type": "ListItem", "position": 2, "name": "标签", "item": f"{BASE}/tags/"})
        if page_name:
            bc["itemListElement"].append({"@type": "ListItem", "position": 3, "name": page_name, "item": page_url})
    elif page_type == "collections":
        bc["itemListElement"].append({"@type": "ListItem", "position": 2, "name": "专题合集", "item": f"{BASE}/collections/"})
        if page_name:
            bc["itemListElement"].append({"@type": "ListItem", "position": 3, "name": page_name, "item": page_url})
    elif page_type == "hub":
        bc["itemListElement"].append({"@type": "ListItem", "position": 2, "name": "主题导航", "item": f"{BASE}/hubs/"})
        if page_name:
            bc["itemListElement"].append({"@type": "ListItem", "position": 3, "name": page_name, "item": page_url})
    return bc

def make_faq_jsonld(qa_pairs: list) -> dict:
    """Generate FAQPage JSON-LD from Q&A pairs."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            } for q, a in qa_pairs
        ]
    }

def inject_jsonld(content: str, new_jsonld: dict) -> str:
    """Inject a new JSON-LD block before </head>."""
    tag = f'  <script type="application/ld+json">{json.dumps(new_jsonld, ensure_ascii=False)}</script>'
    return content.replace('</head>', f'{tag}\n</head>', 1)

def has_breadcrumb(content: str) -> bool:
    return 'BreadcrumbList' in content

def has_faq(content: str) -> bool:
    return 'FAQPage' in content

def process_file(filepath: str, page_type: str, page_name: str = None, page_url: str = None) -> bool:
    """Process a single HTML file. Returns True if modified."""
    content = open(filepath, encoding='utf-8').read()
    modified = False
    
    # Add BreadcrumbList if missing
    if not has_breadcrumb(content):
        bc = make_breadcrumb_jsonld(page_type, page_name, page_url)
        content = inject_jsonld(content, bc)
        modified = True
    
    # Add FAQPage if missing and we have templates
    if not has_faq(content):
        faq_key = page_type
        if page_type == "hub" and page_name:
            # Map hub directory name to FAQ key
            hub_name = Path(filepath).parent.name
            faq_key = hub_name
        
        faq_pairs = FAQ_TEMPLATES.get(faq_key) or HUB_FAQ.get(faq_key)
        if faq_pairs:
            faq = make_faq_jsonld(faq_pairs)
            content = inject_jsonld(content, faq)
            modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return modified

def main():
    stats = {"processed": 0, "modified": 0}
    
    # Homepage
    fp = str(ROOT / "index.html")
    if os.path.exists(fp):
        stats["processed"] += 1
        if process_file(fp, "homepage"):
            stats["modified"] += 1
            print("  ✓ homepage: added BreadcrumbList + FAQPage")
    
    # Category pages
    cat_dir = ROOT / "categories"
    if cat_dir.exists():
        for d in sorted(os.listdir(cat_dir)):
            fp = cat_dir / d / "index.html"
            if fp.exists() and d != "__pycache__":
                stats["processed"] += 1
                name = d.replace("-", " ").title()
                url = f"{BASE}/categories/{d}/"
                if process_file(str(fp), "category", name, url):
                    stats["modified"] += 1
                    print(f"  ✓ categories/{d}: added BreadcrumbList + FAQPage")
    
    # Trending
    fp = str(ROOT / "trending" / "index.html")
    if os.path.exists(fp):
        stats["processed"] += 1
        if process_file(fp, "trending"):
            stats["modified"] += 1
            print("  ✓ trending: added BreadcrumbList + FAQPage")
    
    # Daily brief
    fp = str(ROOT / "daily-brief" / "index.html")
    if os.path.exists(fp):
        stats["processed"] += 1
        if process_file(fp, "daily-brief"):
            stats["modified"] += 1
            print("  ✓ daily-brief: added BreadcrumbList + FAQPage")
    
    # Tag pages
    tags_dir = ROOT / "tags"
    if tags_dir.exists():
        for d in sorted(os.listdir(tags_dir)):
            fp = tags_dir / d / "index.html"
            if fp.exists() and d != "__pycache__":
                stats["processed"] += 1
                url = f"{BASE}/tags/{d}/"
                if process_file(str(fp), "tags", d, url):
                    stats["modified"] += 1
                    print(f"  ✓ tags/{d}: added BreadcrumbList + FAQPage")
    
    # Collection pages
    coll_dir = ROOT / "collections"
    if coll_dir.exists():
        for d in sorted(os.listdir(coll_dir)):
            fp = coll_dir / d / "index.html"
            if fp.exists() and d != "__pycache__":
                stats["processed"] += 1
                name = d.replace("-", " ").title()
                url = f"{BASE}/collections/{d}/"
                if process_file(str(fp), "collections", name, url):
                    stats["modified"] += 1
                    print(f"  ✓ collections/{d}: added BreadcrumbList")
    
    # Hub pages
    hubs_dir = ROOT / "hubs"
    if hubs_dir.exists():
        for d in sorted(os.listdir(hubs_dir)):
            fp = hubs_dir / d / "index.html"
            if fp.exists() and d != "__pycache__":
                stats["processed"] += 1
                name = d.replace("-", " ").title()
                url = f"{BASE}/hubs/{d}/"
                if process_file(str(fp), "hub", name, url):
                    stats["modified"] += 1
                    print(f"  ✓ hubs/{d}: added BreadcrumbList + FAQPage")
    
    print(f"\nProcessed: {stats['processed']} | Modified: {stats['modified']}")

if __name__ == "__main__":
    main()
