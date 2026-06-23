#!/usr/bin/env python3
"""Generate individual project detail pages for long-tail SEO.

Each project gets a page at /projects/<slug>/ with:
- Full description (zh + en)
- JSON-LD (SoftwareApplication + BreadcrumbList + FAQPage)
- Internal links to related projects and category
- Direct GitHub link
- Meta tags targeting "[project name] GitHub" queries
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://daohang.bot.cd"
PROJECTS_PATH = ROOT / "data" / "projects.json"

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

def esc(s: object) -> str:
    return html.escape(str(s or ""), quote=True)

def slugify(name: str) -> str:
    """Convert repo name to URL slug: owner/repo -> owner-repo"""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def desc_cn(p: dict) -> str:
    return p.get("desc_cn") or p.get("desc") or ""

def desc_en(p: dict) -> str:
    return p.get("desc") or p.get("desc_cn") or ""

def page_shell(title: str, description: str, canonical: str, body: str,
               extra_jsonld: list[dict] | None = None, og_image: str | None = None) -> str:
    og = og_image or f"{BASE}/assets/hero-github-directory.png"
    jsonld_blocks = ""
    if extra_jsonld:
        for ld in extra_jsonld:
            jsonld_blocks += f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
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
  <meta property="og:image" content="{esc(og)}">
  <link rel="stylesheet" href="/assets/nav-style.css">
{jsonld_blocks}</head>
<body>
  <main class="home-shell page-mode"><div class="bg-mask"></div>
    <header class="top-menu"><a class="logo" href="/">拾品号导航</a><nav><a href="/projects/">全部项目</a><a href="/categories/">分类导航</a><a href="/trending/">涨星榜</a><a href="/daily-brief/">分享快报</a><a href="/guides/">使用指南</a></nav><div class="header-actions"><a class="admin-link" href="/submit.html">提交收录</a></div></header>
{body}
    <footer class="footer"><a href="/">返回首页</a><a href="/projects/">全部项目</a><a href="/trending/">涨星榜</a><a href="/daily-brief/">分享快报</a><a href="/llms.txt">LLMS.txt</a></footer>
  </main>
  <script src="/assets/fluid-bg.js" defer></script>
</body>
</html>
"""

def build_related(projects: list[dict], current: dict, limit: int = 8) -> list[dict]:
    cat = current.get("category", "")
    tags = set(t.lower() for t in (current.get("tags") or []))
    scored = []
    for p in projects:
        if p.get("url") == current.get("url"):
            continue
        score = 0
        if p.get("category") == cat:
            score += 3
        ptags = set(t.lower() for t in (p.get("tags") or []))
        score += len(tags & ptags)
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda x: (-x[0], -(x[1].get("stars") or 0)))
    return [p for _, p in scored[:limit]]

def build_project_page(p: dict, projects: list[dict]) -> str:
    name = p.get("name", "Unknown")
    slug = slugify(name)
    canonical = f"{BASE}/projects/{slug}/"
    cat = p.get("category", "")
    cat_cn = CAT_CN.get(cat, cat)
    cn = desc_cn(p)
    en = desc_en(p)
    stars = p.get("stars") or 0
    forks = p.get("forks") or 0
    lang = p.get("language") or ""
    growth = p.get("growth") or {}
    spd = growth.get("stars_per_day") or 0
    tags = p.get("tags") or []

    # JSON-LD: BreadcrumbList
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "全部项目", "item": BASE + "/projects/"},
            {"@type": "ListItem", "position": 3, "name": cat_cn, "item": f"{BASE}/categories/{re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-')}/"},
            {"@type": "ListItem", "position": 4, "name": name},
        ]
    }

    # JSON-LD: SoftwareApplication
    software = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "url": p.get("url"),
        "description": cn,
        "alternateName": en if en != cn else None,
        "applicationCategory": cat_cn,
        "operatingSystem": "Cross-platform",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "aggregateRating": None,
    }
    if stars > 100:
        software["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": min(5, round(3 + stars / 10000, 1)),
            "bestRating": 5,
            "ratingCount": stars,
        }

    # JSON-LD: FAQPage
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"{name} 是什么？",
                "acceptedAnswer": {"@type": "Answer", "text": cn}
            },
            {
                "@type": "Question",
                "name": f"{name} 是开源的吗？",
                "acceptedAnswer": {"@type": "Answer", "text": f"是的，{name} 是一个托管在 GitHub 上的开源项目，目前有 {stars:,} 个 Star。"}
            },
            {
                "@type": "Question",
                "name": f"{name} 适合什么场景？",
                "acceptedAnswer": {"@type": "Answer", "text": f"{name} 属于 {cat_cn} 方向，{cn[:100]}… 适合需要相关能力的开发者和团队评估使用。"}
            },
        ]
    }

    # Related projects
    related = build_related(projects, p)
    related_cards = ""
    if related:
        items = ""
        for idx, r in enumerate(related, 1):
            rslug = slugify(r["name"])
            rdesc = desc_cn(r)[:60]
            items += f'<article class="trend-card"><h3><a href="/projects/{esc(rslug)}/">{esc(r["name"])}</a></h3><p>{esc(rdesc)}</p><div class="trend-meta"><span>★ {(r.get("stars") or 0):,}</span></div></article>\n'
        related_cards = f"""
      <section class="related-projects">
        <h2>相关项目推荐</h2>
        <div class="trend-grid">{items}</div>
      </section>"""

    # Tags HTML
    tags_html = "".join(f'<span class="tag-chip">{esc(t)}</span>' for t in tags[:6])

    body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">{esc(cat_cn)}</span>
      <h1>{esc(name)}</h1>
      <p>{esc(cn)}</p>
      <p class="daily-line">GitHub 开源项目 · {esc(cat_cn)} · {esc(lang)}</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <nav class="breadcrumb-nav" aria-label="面包屑导航">
        <a href="/">首页</a> &gt; <a href="/projects/">全部项目</a> &gt; <a href="/categories/{esc(re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-'))}/">{esc(cat_cn)}</a> &gt; <span>{esc(name)}</span>
      </nav>

      <div class="project-detail">
        <div class="detail-hero">
          <div class="detail-stats">
            <div class="stat-box"><strong>{stars:,}</strong><small>GitHub Stars</small></div>
            <div class="stat-box"><strong>{forks:,}</strong><small>Forks</small></div>
            {"<div class=\"stat-box\"><strong>" + f"{spd:.1f}" + "</strong><small>Stars/天</small></div>" if spd > 0 else ""}
            <div class="stat-box"><strong>{esc(lang)}</strong><small>主要语言</small></div>
          </div>
          <a class="github-link" href="{esc(p.get('url'))}" target="_blank" rel="noopener noreferrer">在 GitHub 上查看 →</a>
        </div>

        <div class="detail-section">
          <h2>项目简介</h2>
          <p lang="zh-CN">{esc(cn)}</p>
          {"<p lang=\"en\" class=\"english-desc\">" + esc(en) + "</p>" if en and en != cn else ""}
        </div>

        <div class="detail-section">
          <h2>项目信息</h2>
          <table class="info-table">
            <tr><td>项目名称</td><td>{esc(name)}</td></tr>
            <tr><td>分类</td><td><a href="/categories/{esc(re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-'))}/">{esc(cat_cn)}</a></td></tr>
            <tr><td>主要语言</td><td>{esc(lang)}</td></tr>
            <tr><td>Star 数</td><td>{stars:,}</td></tr>
            <tr><td>Fork 数</td><td>{forks:,}</td></tr>
            {"<tr><td>涨星速度</td><td>" + f"{spd:.2f}" + " Stars/天</td></tr>" if spd > 0 else ""}
            <tr><td>GitHub 地址</td><td><a href="{esc(p.get('url'))}" target="_blank" rel="noopener">{esc(p.get('url'))}</a></td></tr>
          </table>
        </div>

        {"<div class=\"detail-section\"><h2>项目标签</h2><div class=\"tags-wrap\">" + tags_html + "</div></div>" if tags else ""}

        <section class="faq-panel">
          <h2>常见问题</h2>
          <details class="faq-item" open><summary>{esc(name)} 是什么？</summary><p>{esc(cn)}</p></details>
          <details class="faq-item"><summary>{esc(name)} 是开源免费的吗？</summary><p>是的，{esc(name)} 是一个托管在 GitHub 上的开源项目，目前有 {stars:,} 个 Star，{forks:,} 个 Fork。具体 License 以 GitHub 仓库为准。</p></details>
          <details class="faq-item"><summary>{esc(name)} 适合什么场景？</summary><p>{esc(name)} 属于 {esc(cat_cn)} 方向，{esc(cn[:120])}。适合需要相关能力的开发者和团队评估使用。</p></details>
        </section>

        {related_cards}
      </div>
    </section></section>
    """
    return page_shell(
        f"{name} - {cat_cn} GitHub 开源项目 - 拾品号导航",
        f"{cn[:120]}。查看 {name} 的 GitHub Star、Fork、语言、标签和相关项目推荐。",
        canonical,
        body,
        [breadcrumbs, software, faq],
    )

def build_projects_index(projects: list[dict]) -> str:
    """Rebuild /projects/index.html with links to individual detail pages."""
    cards = []
    for p in projects:
        slug = slugify(p["name"])
        cn = desc_cn(p)[:80]
        stars = p.get("stars") or 0
        lang = p.get("language") or ""
        cat_cn = CAT_CN.get(p.get("category", ""), p.get("category", ""))
        growth = p.get("growth") or {}
        spd = growth.get("stars_per_day") or 0
        tags = "".join(f'<span>{esc(t)}</span>' for t in (p.get("tags") or [])[:3])
        cards.append(f"""
        <article class="trend-card">
          <h2><a href="/projects/{esc(slug)}/">{esc(p['name'])}</a></h2>
          <p lang="zh-CN">{esc(cn)}</p>
          <div class="trend-meta"><span>★ {stars:,}</span>{"<span>↗ " + f"{spd:.1f}" + "/天</span>" if spd > 0 else ""}<span>{esc(lang)}</span><span>{esc(cat_cn)}</span></div>
          <div class="trend-tags">{tags}</div>
        </article>""")

    item_list = []
    for idx, p in enumerate(projects[:50], 1):
        item_list.append({
            "@type": "ListItem",
            "position": idx,
            "name": p["name"],
            "url": f"{BASE}/projects/{slugify(p['name'])}/",
            "description": desc_cn(p),
        })

    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "全部 GitHub 开源项目 - 拾品号导航",
        "alternateName": "All GitHub Open Source Projects - ShipinHao Nav",
        "inLanguage": ["zh-CN", "en"],
        "url": f"{BASE}/projects/",
        "description": "拾品号导航收录的全部 GitHub 开源项目，支持搜索、分类浏览和项目详情查看。",
        "isPartOf": {"@type": "WebSite", "name": "拾品号导航", "url": BASE + "/"},
        "mainEntity": {"@type": "ItemList", "itemListElement": item_list},
    }

    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "全部项目"},
        ]
    }

    body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">All Projects</span>
      <h1>全部 GitHub 开源项目</h1>
      <p>拾品号导航收录的 {len(projects)} 个 GitHub 开源项目，每个项目都有独立详情页、结构化数据和直接链接。</p>
      <p class="daily-line">支持搜索 · 分类浏览 · 项目详情 · 直接跳转 GitHub</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="directory-intro"><div><span class="eyebrow">项目列表</span><strong>点击项目名称查看详细信息、Star 数据、标签和相关推荐。</strong></div><div class="stats-row"><span>{len(projects)} 个项目</span><span>独立详情页</span><span>JSON-LD</span></div></div>
      <div class="trend-grid">{''.join(cards)}</div>
    </section></section>"""

    return page_shell(
        f"全部 {len(projects)} 个 GitHub 开源项目 - 拾品号导航",
        f"拾品号导航收录的全部 GitHub 开源项目，覆盖 AI 智能体、建站框架、自动化、数据分析、部署运维等 {len(projects)} 个项目。",
        f"{BASE}/projects/",
        body,
        [breadcrumbs, jsonld],
    )

def main():
    projects = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))
    out_root = ROOT / "projects"
    out_root.mkdir(exist_ok=True)

    count = 0
    for p in projects:
        slug = slugify(p["name"])
        page_dir = out_root / slug
        page_dir.mkdir(parents=True, exist_ok=True)
        page_html = build_project_page(p, projects)
        (page_dir / "index.html").write_text(page_html, encoding="utf-8")
        count += 1

    # Rebuild /projects/index.html with links to detail pages
    index_html = build_projects_index(projects)
    (out_root / "index.html").write_text(index_html, encoding="utf-8")

    print(f"Generated {count} project detail pages + index at /projects/")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
