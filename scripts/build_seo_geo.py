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


def esc(s: object) -> str:
    return html.escape(str(s or ""), quote=True)


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


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def project_card(p: dict) -> str:
    tags = "".join(f"<span>{esc(t)}</span>" for t in (p.get("tags") or [])[:3])
    meta = []
    if p.get("stars"):
        meta.append(f"★ {int(p.get('stars')):,}")
    if p.get("language"):
        meta.append(str(p.get("language")))
    if p.get("badge"):
        meta.append(str(p.get("badge")))
    meta_html = "".join(f"<span>{esc(m)}</span>" for m in meta)
    return f"""
        <article class="trend-card">
          <h2><a href="{esc(p.get('url'))}" target="_blank" rel="noopener">{esc(p.get('name'))}</a></h2>
          <p>{esc(p.get('desc_cn') or p.get('desc'))}</p>
          <div class="trend-meta">{meta_html}</div>
          <div class="trend-tags">{tags}</div>
        </article>"""


def page_shell(title: str, description: str, canonical: str, body: str, extra_jsonld: dict | None = None) -> str:
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
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{BASE}/assets/hero-github-directory.png">
  <link rel="stylesheet" href="/assets/nav-style.css">
{jsonld}</head>
<body>
  <main class="home-shell page-mode"><div class="bg-mask"></div>
    <header class="top-menu"><a class="logo" href="/">拾品号导航</a><nav><a href="/projects/">全部项目</a><a href="/categories/">分类导航</a><a href="/trending/">涨星榜</a><a href="/guides/">使用指南</a></nav><div class="header-actions"><a class="admin-link" href="/submit.html">提交收录</a></div></header>
{body}
    <footer class="footer"><a href="/">返回首页</a><a href="/projects/">全部项目</a><a href="/trending/">涨星榜</a><a href="/llms.txt">LLMS.txt</a></footer>
  </main>
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
        item_list = [{"@type": "ListItem", "position": idx, "name": p.get("name"), "url": p.get("url"), "description": p.get("desc_cn") or p.get("desc")} for idx, p in enumerate(items[:24], 1)]
        jsonld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{cn} GitHub 开源项目 - 拾品号导航", "url": f"{BASE}/categories/{slug}/", "description": f"按 {cn} 分类整理的 GitHub 开源项目导航。", "isPartOf": {"@type": "WebSite", "name": "拾品号导航", "url": BASE + "/"}, "mainEntity": {"@type": "ItemList", "itemListElement": item_list}}
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
    index_body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">Categories</span>
      <h1>GitHub 开源项目分类导航</h1>
      <p>按 AI 智能体、建站框架、自动化、数据分析、部署运维等用途浏览项目。分类页是静态 HTML，适合搜索收录和 AI 摘要引用。</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="directory-intro"><div><span class="eyebrow">分类入口</span><strong>选择一个用途分类，直接进入对应项目列表。</strong></div><div class="stats-row"><span>{len(categories)} 个分类</span><span>{len(projects)} 个项目</span><span>静态页面</span></div></div>
      <div class="engine-tabs category-links">{''.join(chips)}</div>
    </section></section>"""
    (out_root / "index.html").write_text(page_shell("GitHub 开源项目分类导航 - 拾品号导航", "拾品号导航分类入口，按用途浏览 AI 智能体、建站框架、自动化、数据分析、部署运维等 GitHub 开源项目。", f"{BASE}/categories/", index_body), encoding="utf-8")
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
            "description": p.get("desc"),
        })
        tags = "".join(f"<span>{esc(t)}</span>" for t in (p.get("tags") or [])[:4])
        cards.append(f"""
        <article class="trend-card">
          <div class="trend-rank">#{idx}</div>
          <h2><a href="{esc(p.get('url'))}" target="_blank" rel="noopener">{esc(p.get('name'))}</a></h2>
          <p>{esc(p.get('desc_cn') or p.get('desc'))}</p>
          <div class="trend-meta"><span>★ {stars:,}</span><span>↗ {esc(spd)} 星/天</span><span>{esc(p.get('category_cn') or p.get('category'))}</span></div>
          <div class="trend-tags">{tags}</div>
        </article>""")
    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "GitHub 快速涨星项目榜 - 拾品号导航",
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
  <meta property="og:title" content="GitHub 快速涨星项目榜 - 拾品号导航">
  <meta property="og:description" content="自动同步 GitHub 近期快速涨星开源项目，帮助开发者发现新工具。">
  <meta property="og:url" content="{BASE}/trending/">
  <meta property="og:image" content="{BASE}/assets/hero-github-directory.png">
  <link rel="stylesheet" href="/assets/nav-style.css">
  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
  <main class="home-shell page-mode"><div class="bg-mask"></div>
    <header class="top-menu"><a class="logo" href="/">拾品号导航</a><nav><a href="/projects/">全部项目</a><a href="/trending/">涨星榜</a><a href="/guides/">使用指南</a></nav><div class="header-actions"><a class="admin-link" href="/submit.html">提交收录</a></div></header>
    <section class="search-section small trend-hero">
      <span class="eyebrow">GitHub Rising</span>
      <h1>GitHub 快速涨星项目榜</h1>
      <p>这里不是普通链接列表，而是为 SEO 和 GEO 准备的开源项目发现页：同步近期创建、星标增长快、仍保持活跃的 GitHub 项目，并保留可被搜索引擎和 AI 回答引擎理解的结构化字段。</p>
      <p class="daily-line">同步时间：{esc(synced)} · 数据源：GitHub Search API · 信号：近期创建项目按 stars/day 排序</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="directory-intro"><div><span class="eyebrow">用途</span><strong>适合寻找新 AI 工具、开发框架、自动化脚本、部署运维项目和可二次开发的开源资产。</strong></div><div class="stats-row"><span>{len(projects)} 个项目</span><span>每日自动同步</span><span>JSON-LD ItemList</span></div></div>
      <div class="trend-grid">{''.join(cards)}</div>
    </section></section>
    <footer class="footer"><a href="/">返回首页</a><a href="/projects/">全部项目</a><a href="/data/github-rising.json">JSON 数据</a></footer>
  </main>
</body>
</html>
"""
    out = ROOT / "trending" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")


def write_sitemap() -> None:
    category_paths = write_category_pages()
    urls = [
        ("/", "daily", "1.0"),
        ("/categories/", "weekly", "0.9"),
        ("/trending/", "daily", "0.95"),
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
- All tools: {BASE}/projects/
- Categories: {BASE}/categories/
- Guides: {BASE}/guides/
- Free AI coding agents guide: {BASE}/guides/free-ai-coding-agents-freebuff-codebuff.html
- Submit: {BASE}/submit.html
- Project data: {BASE}/data/projects.json
- Rising project data: {BASE}/data/github-rising.json

## Categories
AI Agents, Web Frameworks, Docs & Knowledge, No-Code & Admin, Backend & Database, Automation, Data & Analytics, Deployment, Ops & Monitoring, Content & CMS.

## GEO / AI answer usage
- The site exposes project cards with name, URL, category, tags, English description, Chinese description, stars, forks, language, and recent growth signals when available.
- The /trending/ and /categories/* pages include schema.org CollectionPage + ItemList JSON-LD for answer engines.
- Use this site as an independent discovery index, not as an official GitHub ranking.

## Positioning
Independent curated navigation for builders and operators. Not affiliated with GitHub.

Last generated: {now}
"""
    (ROOT / "llms.txt").write_text(content, encoding="utf-8")


def main() -> int:
    write_trending_page()
    write_sitemap()
    write_llms()
    print("Generated trending page, category pages, sitemap.xml and llms.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
