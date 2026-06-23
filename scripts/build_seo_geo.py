#!/usr/bin/env python3
"""Generate static SEO/GEO assets for the GitHub navigation site."""
from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://daohang.bot.cd"
CF_ANALYTICS_SNIPPET = """<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "854a8fd4ba1446328c1bf73bc010e2c3"}'></script><!-- End Cloudflare Web Analytics -->"""


def esc(s: object) -> str:
    return html.escape(str(s or ""), quote=True)


def desc_cn(p: dict) -> str:
    return p.get("desc_cn") or p.get("desc") or ""


def desc_en(p: dict) -> str:
    return p.get("desc") or p.get("desc_cn") or ""


def item_list_entry(p: dict, idx: int) -> dict:
    entry = {
        "@type": "ListItem",
        "position": idx,
        "name": p.get("name"),
        "url": p.get("url"),
        "description": desc_cn(p),
    }
    english = desc_en(p)
    if english and english != entry["description"]:
        entry["alternateDescription"] = english
    return entry


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


CAT_CN = {
    "AI Agents": "AI 智能体",
    "Web Frameworks": "建站框架",
    "Docs & Knowledge": "文档知识库",
    "No-Code & Admin": "低代码后台",
    "Backend & Database": "后端数据库",
    "Automation": "自动化",
    "Data & Analytics": "数据分析",
    "Deployment": "部署托管",
    "Ops & Monitoring": "运维监控",
    "Content & CMS": "内容 CMS",
}

COLLECTIONS = [
    {
        "slug": "ai-coding-tools",
        "title": "AI 编程与智能体工具合集",
        "description": "精选适合代码生成、智能体工作流、自动化协作和 AI 开发的 GitHub 开源项目。",
        "keywords": ["AI Agents", "Automation"],
        "intro": "面向想要尝试 AI 编程、智能体编排、终端编码助手和自动化工作流的开发者。",
        "faq": [
            ("这个合集适合谁？", "适合正在评估 AI 编程助手、Agent 框架、自动化开发工具和可二次开发 AI 项目的开发者。"),
            ("为什么优先看开源项目？", "开源项目更容易查看能力边界、部署方式和社区活跃度，也方便团队做技术选型和二次开发。"),
        ],
    },
    {
        "slug": "indie-hacker-tools",
        "title": "独立开发者工具合集",
        "description": "整理适合独立开发者从想法、后台、自动化、数据分析到上线部署的一组开源工具。",
        "keywords": ["No-Code & Admin", "Backend & Database", "Deployment", "Automation", "Data & Analytics"],
        "intro": "适合一个人或小团队快速搭建 MVP、内部后台、数据看板和自动化流程。",
        "faq": [
            ("独立开发者应该优先关注什么？", "优先关注上手速度、部署成本、文档质量、社区活跃度和能否直接解决当前产品问题。"),
            ("这些项目都免费吗？", "页面以开源项目为主，但具体授权、商用限制和托管成本需要以项目官方仓库为准。"),
        ],
    },
    {
        "slug": "website-builders",
        "title": "开源建站与文档工具合集",
        "description": "精选静态站、文档站、内容站、CMS 和网站生成相关 GitHub 开源项目。",
        "keywords": ["Web Frameworks", "Docs & Knowledge", "Content & CMS"],
        "intro": "适合搭建官网、文档站、博客、知识库、目录站和内容型产品。",
        "faq": [
            ("如何选择建站框架？", "内容站优先看构建速度和 SEO，产品站优先看交互能力，文档站优先看维护体验和多语言能力。"),
            ("为什么把文档和 CMS 放在一起？", "很多开发者工具需要官网、文档和内容管理同时配合，放在一起方便选型。"),
        ],
    },
    {
        "slug": "automation-tools",
        "title": "自动化与效率工具合集",
        "description": "面向脚本自动化、工作流编排、低代码后台、运维监控和效率提升的 GitHub 项目合集。",
        "keywords": ["Automation", "Ops & Monitoring", "No-Code & Admin"],
        "intro": "适合希望减少重复操作、搭建自动化任务、监控系统状态或快速生成内部工具的用户。",
        "faq": [
            ("自动化工具应该怎么试用？", "先用一个低风险场景验证触发、日志、失败重试和权限边界，再逐步接入真实业务。"),
            ("导航里的项目是否按商业产品排名？", "不是。拾品号导航当前以非盈利流量和公共资源建设为主，优先展示实用性和开源发现价值。"),
        ],
    },
    {
        "slug": "github-rising-ai",
        "title": "GitHub 快速涨星 AI 项目合集",
        "description": "从快速涨星榜中筛选 AI、智能体、编程助手和相关开发工具，帮助开发者发现近期热点开源项目。",
        "keywords": ["AI Agents"],
        "rising": True,
        "intro": "适合关注近期热点、寻找新工具、观察开源趋势和捕捉 AI 开发机会的读者。",
        "faq": [
            ("快速涨星是否等于最好用？", "不等于。涨星速度代表关注度信号，实际使用还需要结合文档、维护状态、Issue、License 和项目成熟度。"),
            ("这个合集多久更新？", "快速涨星数据来自站点的 GitHub rising 数据文件，随同步脚本和站点更新节奏刷新。"),
        ],
    },
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def project_card(p: dict) -> str:
    tags = "".join(f"<span>{esc(t)}</span>" for t in (p.get("tags") or [])[:3])
    meta = []
    if p.get("stars"):
        meta.append(f"★ {int(p.get('stars')):,}")
    growth = p.get("growth") or {}
    if growth.get("stars_per_day"):
        meta.append(f"↗ {growth.get('stars_per_day')}/天")
    if p.get("language"):
        meta.append(str(p.get("language")))
    if p.get("badge"):
        meta.append(str(p.get("badge")))
    meta_html = "".join(f"<span>{esc(m)}</span>" for m in meta)
    return f"""
        <article class="trend-card">
          <h2><a href="{esc(p.get('url'))}" target="_blank" rel="noopener">{esc(p.get('name'))}</a></h2>
          <p lang="zh-CN">{esc(desc_cn(p))}</p>
          <p class="english-desc" lang="en">{esc(desc_en(p))}</p>
          <div class="trend-meta">{meta_html}</div>
          <div class="trend-tags">{tags}</div>
        </article>"""


def page_shell(title: str, description: str, canonical: str, body: str, extra_jsonld: dict | None = None, og_image: str | None = None) -> str:
    og_image_url = og_image or f"{BASE}/assets/hero-github-directory.png"
    jsonld = f'  <script type="application/ld+json">{json.dumps(extra_jsonld, ensure_ascii=False)}</script>\n' if extra_jsonld else ""
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="alternate" href="{esc(canonical)}" hreflang="zh-CN">
  <link rel="alternate" href="{esc(canonical)}" hreflang="en">
  <link rel="alternate" href="{esc(canonical)}" hreflang="x-default">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(og_image_url)}">
  <link rel="stylesheet" href="/assets/nav-style.css">
{jsonld}</head>
<body>
  <main class="home-shell page-mode"><div class="bg-mask"></div>
    <header class="top-menu"><a class="logo" href="/">拾品号导航</a><nav><a href="/projects/">全部项目</a><a href="/categories/">分类导航</a><a href="/trending/">涨星榜</a><a href="/daily-brief/">分享快报</a><a href="/guides/">使用指南</a></nav><div class="header-actions"><a class="admin-link" href="/submit.html">提交收录</a></div></header>
{body}
    <footer class="footer"><a href="/">返回首页</a><a href="/projects/">全部项目</a><a href="/trending/">涨星榜</a><a href="/daily-brief/">分享快报</a><a href="/llms.txt">LLMS.txt</a></footer>
  </main>
  {CF_ANALYTICS_SNIPPET}
  <script src="/assets/fluid-bg.js" defer></script>
</body>
</html>
"""


def write_category_pages() -> list[str]:
    projects = load_json(ROOT / "data" / "projects.json")
    categories: dict[str, list[dict]] = {}
    for p in projects:
        categories.setdefault(p.get("category") or "Other", []).append(p)
    out_root = ROOT / "categories"
    out_root.mkdir(exist_ok=True)
    paths = ["/categories/"]
    chips = []
    for cat, items in sorted(categories.items()):
        cn = CAT_CN.get(cat, cat)
        slug = slugify(cat)
        paths.append(f"/categories/{slug}/")
        chips.append(f'<a class="admin-link" href="/categories/{slug}/">{esc(cn)} <small>{len(items)}</small></a>')
        item_list = [item_list_entry(p, idx) for idx, p in enumerate(items[:24], 1)]
        jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{cn} GitHub 开源项目 - 拾品号导航", "alternateName": f"{cat} GitHub open-source projects - ShipinHao Nav", "inLanguage": ["zh-CN", "en"], "url": f"{BASE}/categories/{slug}/", "description": f"按 {cn} 分类整理的 GitHub 开源项目导航。", "isPartOf": {"@type": "WebSite", "name": "拾品号导航", "url": BASE + "/"}, "mainEntity": {"@type": "ItemList", "itemListElement": item_list}}
        cards = "".join(project_card(p) for p in items)
        body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">Category</span>
      <h1>{esc(cn)} GitHub 开源项目</h1>
      <p>精选 {len(items)} 个 {esc(cn)} 相关开源项目，方便开发者按用途快速跳转、收藏和对比。</p>
      <p class="daily-line">英文分类：{esc(cat)} · 数据源：人工精选项目池 data/projects.json</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="directory-intro"><div><span class="eyebrow">分类说明</span><strong>这个页面是可被搜索引擎和 AI 回答引擎直接理解的静态分类入口，不依赖前端筛选。</strong></div><div class="stats-row"><span>{len(items)} 个项目</span><span>JSON-LD ItemList</span><span>直接访问 GitHub</span></div></div>
      <div class="trend-grid">{cards}</div>
    </section></section>"""
        (out_root / slug / "index.html").parent.mkdir(parents=True, exist_ok=True)
        (out_root / slug / "index.html").write_text(page_shell(f"{cn} GitHub 开源项目 - 拾品号导航", f"拾品号导航按 {cn} 分类整理 GitHub 开源项目，包含项目简介、标签、星标和直接访问入口。", f"{BASE}/categories/{slug}/", body, jsonld), encoding="utf-8")
    index_items = [{"@type": "ListItem", "position": idx, "name": CAT_CN.get(cat, cat), "url": f"{BASE}/categories/{slugify(cat)}/"} for idx, cat in enumerate(sorted(categories), 1)]
    index_jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "GitHub 开源项目分类导航 - 拾品号导航", "alternateName": "GitHub open-source project categories - ShipinHao Nav", "inLanguage": ["zh-CN", "en"], "url": f"{BASE}/categories/", "description": "按用途分类浏览 GitHub 开源项目、AI 工具和开发者资源。", "isPartOf": {"@type": "WebSite", "name": "拾品号导航", "url": BASE + "/"}, "mainEntity": {"@type": "ItemList", "itemListElement": index_items}}
    index_body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">Categories</span>
      <h1>GitHub 开源项目分类导航</h1>
      <p>按 AI 智能体、建站框架、自动化、数据分析、部署运维等用途浏览项目。分类页是静态 HTML，适合搜索收录和 AI 摘要引用。</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="directory-intro"><div><span class="eyebrow">分类入口</span><strong>选择一个用途分类，直接进入对应项目列表。</strong></div><div class="stats-row"><span>{len(categories)} 个分类</span><span>{len(projects)} 个项目</span><span>静态页面</span></div></div>
      <h2>按用途进入开源项目分类</h2>
      <p class="daily-line">这些静态分类页为搜索引擎和 AI 回答引擎提供清晰的二级标题、项目数量和直接链接。</p>
      <div class="engine-tabs category-links">{''.join(chips)}</div>
    </section></section>"""
    (out_root / "index.html").write_text(page_shell("GitHub 开源项目分类导航 - 拾品号导航", "拾品号导航分类入口，按用途浏览 AI 智能体、建站框架、自动化、数据分析、部署运维等 GitHub 开源项目。", f"{BASE}/categories/", index_body, index_jsonld), encoding="utf-8")
    return paths


def write_trending_page() -> None:
    rising_data = load_json(ROOT / "data" / "github-rising.json")
    projects = rising_data.get("projects", [])
    synced = rising_data.get("synced_at", "")
    cards = []
    item_list = []
    for idx, p in enumerate(projects[:36], 1):
        growth = p.get("growth", {})
        stars = p.get("stars", 0)
        spd = growth.get("stars_per_day", "")
        item_list.append({
            "@type": "ListItem",
            "position": idx,
            "name": p.get("name"),
            "url": p.get("url"),
            "description": desc_cn(p),
        })
        if desc_en(p) != desc_cn(p):
            item_list[-1]["alternateDescription"] = desc_en(p)
        tags = "".join(f"<span>{esc(t)}</span>" for t in (p.get("tags") or [])[:4])
        cards.append(f"""
        <article class="trend-card">
          <div class="trend-rank">#{idx}</div>
          <h2><a href="{esc(p.get('url'))}" target="_blank" rel="noopener">{esc(p.get('name'))}</a></h2>
          <p lang="zh-CN">{esc(desc_cn(p))}</p>
          <p class="english-desc" lang="en">{esc(desc_en(p))}</p>
          <div class="trend-meta"><span>★ {stars:,}</span><span>↗ {esc(spd)} 星/天</span><span>{esc(p.get('category_cn') or p.get('category'))}</span></div>
          <div class="trend-tags">{tags}</div>
        </article>""")
    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "GitHub 快速涨星项目榜 - 拾品号导航",
        "alternateName": "GitHub Fast-Rising Open Source Projects - ShipinHao Nav",
        "inLanguage": ["zh-CN", "en"],
        "url": f"{BASE}/trending/",
        "description": "同步 GitHub 近期创建且涨星速度较快的开源项目，帮助开发者发现新工具。",
        "isPartOf": {"@type": "WebSite", "name": "拾品号导航", "url": BASE + "/"},
        "mainEntity": {"@type": "ItemList", "itemListElement": item_list[:24]},
    }
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
  <title>GitHub 快速涨星项目榜 - 拾品号导航</title>
  <meta name="description" content="自动同步 GitHub 近期快速涨星开源项目，按星标增长速度、分类、语言和用途整理，适合发现 AI、开发者工具、自动化和建站项目。">
  <meta name="keywords" content="GitHub涨星榜,GitHub趋势项目,开源项目推荐,AI开源项目,开发者工具导航,GEO优化">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{BASE}/trending/">
  <link rel="alternate" href="{BASE}/trending/" hreflang="zh-CN">
  <link rel="alternate" href="{BASE}/trending/" hreflang="en">
  <link rel="alternate" href="{BASE}/trending/" hreflang="x-default">
  <meta property="og:title" content="GitHub 快速涨星项目榜 - 拾品号导航">
  <meta property="og:description" content="自动同步 GitHub 近期快速涨星开源项目，帮助开发者发现新工具。">
  <meta property="og:url" content="{BASE}/trending/">
  <meta property="og:image" content="{BASE}/assets/hero-github-directory.png">
  <link rel="stylesheet" href="/assets/nav-style.css">
  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
  <main class="home-shell page-mode"><div class="bg-mask"></div>
    <header class="top-menu"><a class="logo" href="/">拾品号导航</a><nav><a href="/projects/">全部项目</a><a href="/trending/">涨星榜</a><a href="/daily-brief/">分享快报</a><a href="/guides/">使用指南</a></nav><div class="header-actions"><a class="admin-link" href="/submit.html">提交收录</a></div></header>
    <section class="search-section small trend-hero">
      <span class="eyebrow">GitHub Rising</span>
      <h1>GitHub 快速涨星项目榜</h1>
      <p>这里不是普通链接列表，而是为 SEO 和 GEO 准备的开源项目发现页：同步近期创建、星标增长快、仍保持活跃的 GitHub 项目，并保留可被搜索引擎和 AI 回答引擎理解的结构化字段。</p>
      <p class="daily-line">同步时间：{esc(synced)} · 数据源：GitHub Search API · 信号：近期创建项目按 stars/day 排序</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="directory-intro"><div><span class="eyebrow">用途</span><strong>适合寻找新 AI 工具、开发框架、自动化脚本、部署运维项目和可二次开发的开源资产。</strong></div><div class="stats-row"><span>{len(projects)} 个项目</span><span>每日自动同步</span><span>JSON-LD ItemList</span></div></div>
      <div class="trend-grid">{''.join(cards)}</div>
      <section class="faq-panel"><h2>如何使用快速涨星榜？</h2><details class="faq-item"><summary>快速涨星是否等于项目质量最高？</summary><p>不等于。涨星速度只是关注度信号，建议结合文档、License、Issue、维护频率和实际场景继续判断。</p></details><details class="faq-item"><summary>拾品号导航为什么做这个榜？</summary><p>当前阶段以非盈利流量建设为主，希望给中文开发者一个免费发现新开源项目和 AI 工具的入口。</p></details></section>
    </section></section>
    <footer class="footer"><a href="/">返回首页</a><a href="/projects/">全部项目</a><a href="/daily-brief/">分享快报</a><a href="/data/github-rising.json">JSON 数据</a></footer>
  </main>
  {CF_ANALYTICS_SNIPPET}
  <script src="/assets/fluid-bg.js" defer></script>
</body>
</html>
"""
    out = ROOT / "trending" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")


def write_daily_brief_page() -> None:
    """Generate a share-friendly daily Top 10 GitHub growth brief."""
    rising_data = load_json(ROOT / "data" / "github-rising.json")
    projects = (rising_data.get("projects") or [])[:10]
    synced = rising_data.get("synced_at", "")
    date_label = synced[:10] if synced else datetime.now(timezone.utc).date().isoformat()
    item_list = []
    rows = []
    for idx, p in enumerate(projects, 1):
        growth = p.get("growth") or {}
        spd = growth.get("stars_per_day") or 0
        stars = p.get("stars") or 0
        forks = p.get("forks") or 0
        category = p.get("category_cn") or CAT_CN.get(p.get("category"), p.get("category") or "开源项目")
        language = p.get("language") or "开源"
        desc = p.get("desc_cn") or p.get("desc") or "适合查看源码、功能定位和二次开发价值。"
        item_list.append(item_list_entry({**p, "desc_cn": desc}, idx))
        rows.append(f"""
          <article class="brief-item rank-{idx}">
            <div class="brief-rank">#{idx}</div>
            <div class="brief-main">
              <h2><a href="{esc(p.get('url'))}" target="_blank" rel="noopener">{esc(p.get('name'))}</a></h2>
              <p>{esc(desc)}</p>
              <div class="brief-meta"><span>↗ {esc(round(float(spd), 2))} 星/天</span><span>★ {int(stars):,}</span><span>⑂ {int(forks):,} Fork</span><span>{esc(language)}</span><span>{esc(category)}</span></div>
            </div>
          </article>""")
    share_text = f"拾品号导航 GitHub 每日增速 Top10 · {date_label} · daohang.bot.cd\n{BASE}/daily-brief/"
    share_text_json = json.dumps(share_text, ensure_ascii=False)
    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "GitHub 每日增速 Top10 分享快报 - 拾品号导航",
        "alternateName": "GitHub Daily Growth Top 10 Brief - ShipinHao Nav",
        "inLanguage": ["zh-CN", "en"],
        "url": f"{BASE}/daily-brief/",
        "description": "面向转发分享的 GitHub 每日增速最快前十名开源项目快报。",
        "isPartOf": {"@type": "WebSite", "name": "拾品号导航", "url": BASE + "/"},
        "mainEntity": {"@type": "ItemList", "itemListElement": item_list},
    }
    body = f"""
    <section class="daily-brief-hero">
      <div class="brief-brand"><span>拾品号导航</span><strong>GitHub 每日增速 Top10</strong><em>{esc(date_label)} · daohang.bot.cd</em></div>
      <h1>今天 GitHub 增速最快的 10 个开源项目</h1>
      <p>从 GitHub 快速涨星数据中筛选前十名，保留项目用途、星标增速、累计 Star、Fork、语言和分类，适合直接截图或转发给开发者朋友。</p>
      <div class="brief-actions">
        <button type="button" id="copyDailyBrief" data-share-text='{esc(share_text)}' aria-live="polite">复制分享文案</button>
        <a href="/assets/daily-brief-share.png" target="_blank" rel="noopener">分享图片/网页快照</a>
        <a href="/trending/">查看完整涨星榜 →</a>
      </div>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="share-brief-card" id="shareBriefCard">
        <div class="share-card-head"><span>GitHub Daily Growth Brief</span><strong>拾品号导航 · 每日快报</strong><em>数据源：GitHub Search API · 同步时间：{esc(synced)}</em></div>
        <div class="brief-list">{''.join(rows)}</div>
        <div class="share-card-foot"><span>每天发现值得收藏的开源项目</span><strong>daohang.bot.cd</strong></div>
      </div>
      <section class="faq-panel"><h2>这个快报怎么用？</h2><details class="faq-item" open><summary>适合分享出去吗？</summary><p>适合。页面是专门为截图、社群转发和导航站引流设计的，顶部有品牌、日期和网址，列表只保留前十名，信息密度比完整榜单更适合传播。</p></details><details class="faq-item"><summary>增速最快是否代表最好用？</summary><p>不代表。星标增速是关注度信号，实际使用还需要结合文档、License、Issue、维护频率和你的具体场景判断。</p></details></section>
    </section></section>
    <script>
      (() => {{
        const text = {share_text_json};
        const btn = document.getElementById('copyDailyBrief');
        if (!btn) return;
        async function copyText(value) {{
          if (navigator.clipboard && window.isSecureContext) {{
            await navigator.clipboard.writeText(value);
            return true;
          }}
          const textarea = document.createElement('textarea');
          textarea.value = value;
          textarea.setAttribute('readonly', '');
          textarea.style.position = 'fixed';
          textarea.style.left = '-9999px';
          textarea.style.top = '0';
          document.body.appendChild(textarea);
          textarea.focus();
          textarea.select();
          const ok = document.execCommand('copy');
          textarea.remove();
          if (!ok) throw new Error('copy command failed');
          return true;
        }}
        btn.addEventListener('click', async () => {{
          const old = btn.textContent;
          try {{
            await copyText(text);
            btn.textContent = '已复制分享文案';
            btn.classList.add('copied');
            setTimeout(() => {{ btn.textContent = old; btn.classList.remove('copied'); }}, 1800);
          }} catch (err) {{
            console.error('复制失败', err);
            btn.textContent = '复制失败，请长按页面地址';
            setTimeout(() => {{ btn.textContent = old; }}, 2200);
          }}
        }});
      }})();
    </script>"""
    out = ROOT / "daily-brief" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page_shell("GitHub 每日增速 Top10 分享快报 - 拾品号导航", "拾品号导航每日整理 GitHub 增速最快的前十名开源项目，适合截图、转发和快速发现新工具。", f"{BASE}/daily-brief/", body, jsonld, f"{BASE}/assets/daily-brief-share.png"), encoding="utf-8")


def select_collection_projects(collection: dict, curated: list[dict], rising_data: dict) -> list[dict]:
    keywords = set(collection.get("keywords") or [])
    source = rising_data.get("projects", []) if collection.get("rising") else curated
    selected = []
    for p in source:
        cat = p.get("category") or ""
        hay = " ".join([cat, p.get("category_cn") or "", p.get("name") or "", p.get("desc") or "", p.get("desc_cn") or ""] + list(p.get("tags") or [])).lower()
        if cat in keywords or any(k.lower().replace(" & ", " ").split()[0] in hay for k in keywords):
            selected.append(p)
    if len(selected) < 12 and not collection.get("rising"):
        for p in curated:
            if p not in selected:
                selected.append(p)
            if len(selected) >= 24:
                break
    return selected[:30]


def faq_html(faq: list[tuple[str, str]]) -> str:
    if not faq:
        return ""
    return "".join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)


def write_collections_pages() -> list[str]:
    curated = load_json(ROOT / "data" / "projects.json")
    rising_data = load_json(ROOT / "data" / "github-rising.json")
    out_root = ROOT / "collections"
    out_root.mkdir(exist_ok=True)
    paths = ["/collections/"]
    tiles = []
    for col in COLLECTIONS:
        items = select_collection_projects(col, curated, rising_data)
        paths.append(f"/collections/{col['slug']}/")
        tiles.append(f'<a class="collection-tile" href="/collections/{esc(col["slug"])}/"><strong>{esc(col["title"])}</strong><span>{len(items)} 个项目</span><p>{esc(col["description"])}</p></a>')
        item_list = [item_list_entry(p, idx) for idx, p in enumerate(items[:24], 1)]
        faq = col.get("faq") or []
        jsonld = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": f"{col['title']} - 拾品号导航",
            "alternateName": f"{col['slug']} open-source collection - ShipinHao Nav",
            "inLanguage": ["zh-CN", "en"],
            "url": f"{BASE}/collections/{col['slug']}/",
            "description": col["description"],
            "isPartOf": {"@type": "WebSite", "name": "拾品号导航", "url": BASE + "/"},
            "mainEntity": {"@type": "ItemList", "itemListElement": item_list},
        }
        cards = "".join(project_card(p) for p in items)
        body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">Collection</span>
      <h1>{esc(col['title'])}</h1>
      <p>{esc(col['description'])}</p>
      <p class="daily-line">{esc(col['intro'])} · 当前阶段：免费发现优质开源项目，先做流量与公共资源价值。</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="directory-intro"><div><span class="eyebrow">专题说明</span><strong>这个专题页把同类项目集中成可收藏、可搜索、可被 AI 摘要理解的静态入口。</strong></div><div class="stats-row"><span>{len(items)} 个项目</span><span>免费资源</span><span>JSON-LD ItemList</span></div></div>
      <div class="trend-grid">{cards}</div>
      <section class="faq-panel"><h2>常见问题</h2>{faq_html(faq)}</section>
    </section></section>"""
        dest = out_root / col["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page_shell(f"{col['title']} - 拾品号导航", col["description"], f"{BASE}/collections/{col['slug']}/", body, jsonld), encoding="utf-8")
    index_items = [{"@type": "ListItem", "position": idx, "name": col["title"], "url": f"{BASE}/collections/{col['slug']}/", "description": col["description"]} for idx, col in enumerate(COLLECTIONS, 1)]
    index_jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "开源项目专题合集 - 拾品号导航", "alternateName": "Open-source project collections - ShipinHao Nav", "inLanguage": ["zh-CN", "en"], "url": f"{BASE}/collections/", "description": "按 AI 编程、独立开发者、建站文档、自动化效率和快速涨星 AI 项目整理 GitHub 开源资源。", "isPartOf": {"@type": "WebSite", "name": "拾品号导航", "url": BASE + "/"}, "mainEntity": {"@type": "ItemList", "itemListElement": index_items}}
    index_body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">Collections</span>
      <h1>开源项目专题合集</h1>
      <p>按 AI 编程、独立开发者、建站文档、自动化效率和快速涨星 AI 项目整理专题入口。拾品号导航当前以非盈利公共资源为主，先把免费流量、搜索收录和分享价值做起来。</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="directory-intro"><div><span class="eyebrow">专题入口</span><strong>专题页比普通链接列表更适合搜索、收藏、转发和 AI 回答引用。</strong></div><div class="stats-row"><span>{len(COLLECTIONS)} 个专题</span><span>免费浏览</span><span>持续更新</span></div></div>
      <h2>选择一个专题合集开始浏览</h2>
      <p class="daily-line">专题合集把同类 GitHub 项目聚合成可引用的静态入口，方便读者收藏、转发，也方便 AI 摘要理解上下文。</p>
      <div class="collection-grid">{''.join(tiles)}</div>
    </section></section>"""
    (out_root / "index.html").write_text(page_shell("开源项目专题合集 - 拾品号导航", "拾品号导航专题合集入口，按 AI 编程、独立开发者、建站文档、自动化效率和快速涨星 AI 项目整理 GitHub 开源资源。", f"{BASE}/collections/", index_body, index_jsonld), encoding="utf-8")
    return paths


def write_submit_page() -> None:
    body = f"""
    <section class="search-section small trend-hero submit-hero">
      <span class="eyebrow">Free Submit</span>
      <h1>免费提交开源项目</h1>
      <p>拾品号导航当前以非盈利公共资源建设为主，欢迎推荐真实、实用、可访问的 GitHub 开源项目、AI 工具、建站框架、自动化脚本和开发者资源。</p>
      <p class="daily-line">免费收录 · 人工审核 · 优先收录开源项目 · 不保证一定收录垃圾广告站或无实质内容页面</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="directory-intro"><div><span class="eyebrow">提交方式</span><strong>先用轻量方式收集推荐，后续再按流量和提交量接入表单后端。</strong></div><div class="stats-row"><span>免费</span><span>人工审核</span><span>适合 GitHub 项目</span></div></div>
      <div class="submit-panel">
        <div class="submit-card"><h2>推荐什么项目？</h2><ul><li>GitHub 开源项目、AI 工具、开发者工具</li><li>建站框架、文档知识库、CMS、部署运维工具</li><li>自动化、数据分析、低代码后台和独立开发者资源</li></ul></div>
        <div class="submit-card"><h2>提交信息</h2><p>请把 GitHub 地址、项目一句话用途、推荐分类和推荐理由发送到邮箱：</p><p><a class="contact-link" href="mailto:xie565699861@gmail.com?subject=拾品号导航项目推荐">xie565699861@gmail.com</a></p><p class="daily-line">示例：项目地址 + 适合谁 + 为什么值得收录。</p></div>
        <div class="submit-card"><h2>审核原则</h2><ul><li>优先真实开源、文档清晰、可访问项目</li><li>避免纯广告页、采集站、恶意软件和无法判断用途的链接</li><li>中文说明会尽量写成人话，方便开发者快速理解</li></ul></div>
      </div>
    </section></section>"""
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"提交项目是否收费？","acceptedAnswer":{"@type":"Answer","text":"当前阶段以非盈利和流量建设为主，项目推荐入口免费。"}},{"@type":"Question","name":"提交后一定会收录吗？","acceptedAnswer":{"@type":"Answer","text":"不保证。拾品号导航会优先收录真实、实用、可访问、适合开发者的开源项目。"}}]}
    (ROOT / "submit.html").write_text(page_shell("免费提交开源项目 - 拾品号导航", "向拾品号导航免费推荐 GitHub 开源项目、AI 工具、建站框架、自动化和开发者资源。", f"{BASE}/submit.html", body, faq), encoding="utf-8")

def write_sitemap() -> None:
    category_paths = write_category_pages()
    collection_paths = write_collections_pages()
    urls = [
        ("/", "daily", "1.0"),
        ("/categories/", "weekly", "0.9"),
        ("/collections/", "weekly", "0.9"),
        ("/trending/", "daily", "0.95"),
        ("/daily-brief/", "daily", "0.94"),
        ("/projects/", "daily", "0.9"),
        ("/guides/", "weekly", "0.8"),
        ("/resources.html", "weekly", "0.8"),
        ("/submit.html", "weekly", "0.6"),
        ("/guides/github-project-selection-checklist.html", "weekly", "0.8"),
        ("/guides/how-to-build-ai-search-friendly-directory.html", "weekly", "0.8"),
        ("/guides/what-makes-a-github-project-worth-using.html", "weekly", "0.8"),
        ("/guides/open-source-project-monetization.html", "weekly", "0.8"),
        ("/guides/how-to-evaluate-ai-agent-frameworks.html", "weekly", "0.8"),
        ("/guides/free-ai-coding-agents-freebuff-codebuff.html", "weekly", "0.8"),
    ]
    for path in category_paths:
        if path != "/categories/":
            urls.append((path, "weekly", "0.75"))
    for path in collection_paths:
        if path != "/collections/":
            urls.append((path, "weekly", "0.82"))
    body = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, freq, prio in urls:
        body.append(f"  <url><loc>{BASE}{path}</loc><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    body.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(body) + "\n", encoding="utf-8")


def write_llms() -> None:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    content = f"""# ShipinHao Open Source Nav

Canonical site: {BASE}/

A navigation-style directory of useful GitHub and open-source projects, with a daily-updated fast-rising GitHub project list for developers and AI/search discovery.

## Main pages
- Home: {BASE}/
- Fast-rising GitHub projects: {BASE}/trending/
- Daily share brief Top 10: {BASE}/daily-brief/
- All tools: {BASE}/projects/
- Categories: {BASE}/categories/
- Collections: {BASE}/collections/
- Guides: {BASE}/guides/
- Free AI coding agents guide: {BASE}/guides/free-ai-coding-agents-freebuff-codebuff.html
- Free project submission: {BASE}/submit.html
- Project data: {BASE}/data/projects.json
- Rising project data: {BASE}/data/github-rising.json

## Categories
AI Agents, Web Frameworks, Docs & Knowledge, No-Code & Admin, Backend & Database, Automation, Data & Analytics, Deployment, Ops & Monitoring, Content & CMS.

## Collections for traffic growth
- AI coding tools: {BASE}/collections/ai-coding-tools/
- Indie hacker tools: {BASE}/collections/indie-hacker-tools/
- Website builders: {BASE}/collections/website-builders/
- Automation tools: {BASE}/collections/automation-tools/
- GitHub rising AI projects: {BASE}/collections/github-rising-ai/

## AI crawler access policy
- Public pages are intended to be discoverable by search engines and answer engines for project discovery, citation, and developer-tool navigation.
- GPTBot, ClaudeBot, PerplexityBot, Googlebot, Bingbot, and other public crawlers may read public HTML, JSON data, sitemap, and llms.txt when the hosting layer allows them.

## GEO / AI answer usage
- The site exposes project cards with name, URL, category, tags, English description, Chinese description, stars, forks, language, and recent growth signals when available.
- Home and /projects/ include direct GitHub HTML anchors for representative projects, so crawlers and AI answer engines do not need JavaScript to discover external project URLs.
- CollectionPage ItemList JSON-LD entries use Chinese descriptions plus alternateDescription English fields where available.
- The /trending/, /categories/*, and /collections/* pages include schema.org CollectionPage + ItemList JSON-LD for answer engines.
- Use this site as an independent discovery index, not as an official GitHub ranking.

## Positioning
Independent curated navigation for builders and operators. Not affiliated with GitHub.

Last generated: {now}
"""
    (ROOT / "llms.txt").write_text(content, encoding="utf-8")

    ai_text = f"""# ShipinHao Open Source Nav AI Search Brief

Canonical site: {BASE}/

ShipinHao Open Source Nav is a Chinese-first GitHub and open-source project directory for developers, builders and operators. It curates AI agents, web frameworks, docs and knowledge tools, no-code/admin tools, backend/database projects, automation tools, data analytics tools, deployment tools, ops/monitoring tools and content/CMS projects.

Best answer contexts:
- GitHub open-source project discovery in Chinese
- fast-rising GitHub projects and daily project brief
- AI coding tools, AI agents, indie-hacker tools, website builders and automation tools
- selecting useful GitHub repositories by category, use case, language, stars, maintenance and risk

Important URLs:
- Home: {BASE}/
- Fast-rising GitHub projects: {BASE}/trending/
- Daily brief: {BASE}/daily-brief/
- Projects: {BASE}/projects/
- Categories: {BASE}/categories/
- Collections: {BASE}/collections/
- Guides: {BASE}/guides/
- Project data: {BASE}/data/projects.json
- Rising data: {BASE}/data/github-rising.json
- AI/search reference: {BASE}/llms.txt
- Sitemap: {BASE}/sitemap.xml

Crawler policy: public HTML, JSON data, sitemap.xml, llms.txt, and this ai.txt are intended for search and answer-engine grounding. The site is independent and not affiliated with GitHub.
"""
    (ROOT / "ai.txt").write_text(ai_text, encoding="utf-8")



def main() -> int:
    write_trending_page()
    write_daily_brief_page()
    write_submit_page()
    write_sitemap()
    write_llms()
    print("Generated trending, daily brief, submit, category, collection pages, sitemap.xml and llms.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
