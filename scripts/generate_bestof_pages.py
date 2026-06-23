#!/usr/bin/env python3
"""Generate 'Best X' landing pages targeting high-volume search queries.

Each page loads projects from data/projects.json, filters by relevant
category/tags, renders project cards, and adds FAQPage + BreadcrumbList
+ Article JSON-LD structured data.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://daohang.bot.cd"


def esc(s):
    return html.escape(str(s or ""), quote=True)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def load_projects():
    with open(ROOT / "data" / "projects.json", encoding="utf-8") as f:
        return json.load(f)


def filter_projects(projects, *, categories=None, tags_any=None, limit=30):
    """Filter projects by category or tags, sorted by stars desc."""
    cats = set(categories or [])
    tags = set(tags_any or [])
    matched = []
    for p in projects:
        if cats and p.get("category", "") in cats:
            matched.append(p)
            continue
        if tags and tags & set(p.get("tags", [])):
            matched.append(p)
            continue
    matched.sort(key=lambda x: x.get("stars", 0), reverse=True)
    return matched[:limit]


# ── Page definitions ─────────────────────────────────────────────────

PAGES = [
    {
        "filename": "best-github-projects-2026",
        "title": "2026年最值得关注的GitHub开源项目 - 拾品号导航",
        "h1": "2026年最值得关注的GitHub开源项目",
        "meta_desc": "精选2026年GitHub上最热门的开源项目，涵盖AI Agent、Web框架、DevOps、数据分析等领域，附Star数和详细介绍。",
        "keywords": "GitHub开源项目,2026开源项目,GitHub热门项目,开源推荐,涨星项目",
        "filter": {"categories": ["AI Agents", "Automation", "Web Frameworks", "Ops & Monitoring", "Backend & Database", "Data & Analytics", "Docs & Knowledge", "Deployment", "No-Code & Admin", "Content & CMS"], "limit": 25},
        "intro": "<p>GitHub是全球最大的开源社区，每天都有大量优秀的项目涌现。本文精选了2026年最值得关注的GitHub开源项目，涵盖AI智能体、自动化、Web开发、数据工具等多个领域，帮助开发者快速发现高质量开源项目。</p>",
        "section_title": "精选开源项目推荐",
        "faq": [
            ("如何判断一个GitHub项目是否值得关注？", "主要看Star增长趋势、维护活跃度（最近commit时间）、文档质量和社区讨论度。Star数量是参考指标之一，但更重要的是项目是否在持续更新。"),
            ("GitHub上Star数最多的项目有哪些？", "知名的高Star项目包括Linux内核、Vue.js、React、TensorFlow等。2026年AI相关项目的Star增长最为迅猛。"),
            ("在哪里发现GitHub上的新项目？", "可以通过GitHub Trending、拾品号导航的涨星榜、Hacker News、Reddit等平台发现新项目。拾品号导航每天自动同步涨星数据。"),
        ],
    },
    {
        "filename": "best-developer-tools-2026",
        "title": "2026年最佳开发者工具推荐 - 拾品号导航",
        "h1": "2026年最佳开发者工具推荐",
        "meta_desc": "整理2026年最值得使用的开发者工具，覆盖AI编程助手、代码编辑器、终端工具、API开发、调试测试等场景。",
        "keywords": "开发者工具,2026开发工具,AI编程助手,代码编辑器,开发效率,开源工具",
        "filter": {"categories": ["AI Agents"], "tags_any": ["coding-agent", "ai-coding", "cli", "sandbox", "sandboxing"], "limit": 20},
        "intro": "<p>2026年的开发者工具正在经历AI驱动的变革。从AI编程助手到智能调试工具，新一代开发工具正在大幅提升开发效率。本文整理了最值得尝试的开发者工具。</p>",
        "section_title": "推荐开发者工具",
        "faq": [
            ("AI编程助手真的能提高效率吗？", "是的。AI编程助手在代码补全、代码生成、bug修复等重复性工作上能显著提升效率。但对于复杂的架构设计和业务逻辑，仍需开发者自身判断。"),
            ("免费的开发者工具有哪些？", "很多优秀的开发者工具都有免费版本或开源方案，如VS Code、GitHub Copilot Free、Aider、Continue等。"),
            ("如何选择适合自己的开发工具？", "根据你的技术栈、工作流偏好（终端vs IDE）、团队规模和预算来选择。建议先试用免费版本再做决定。"),
        ],
    },
    {
        "filename": "best-automation-tools-2026",
        "title": "2026年最佳自动化工具 - 拾品号导航",
        "h1": "2026年最佳自动化工具",
        "meta_desc": "精选2026年最佳自动化工具，涵盖浏览器自动化、RPA、工作流编排、AI Agent自动化等场景，提升工作效率。",
        "keywords": "自动化工具,RPA,浏览器自动化,工作流自动化,AI自动化,2026工具推荐",
        "filter": {"categories": ["Automation"], "tags_any": ["automation", "workflow", "browser-agent", "browser-use", "computer-use"], "limit": 20},
        "intro": "<p>自动化工具正在从简单的规则脚本进化为AI驱动的智能自动化。2026年，AI Agent让自动化工具能够理解自然语言指令、处理异常情况，甚至自主学习新流程。本文推荐最值得关注的自动化工具。</p>",
        "section_title": "推荐自动化工具",
        "faq": [
            ("自动化工具和AI Agent有什么区别？", "传统自动化工具基于固定规则执行任务，AI Agent具有理解、推理和自主决策能力。2026年的趋势是两者融合，用AI驱动自动化。"),
            ("浏览器自动化工具有哪些？", "主流的浏览器自动化工具包括Playwright、Puppeteer、Selenium。2026年新出现了许多AI驱动的浏览器Agent工具。"),
            ("自动化工具适合哪些场景？", "数据采集、表单填写、测试自动化、报表生成、工作流审批、客服自动回复等重复性任务都适合使用自动化工具。"),
        ],
    },
    {
        "filename": "best-web-frameworks-2026",
        "title": "2026年最佳Web开发框架 - 拾品号导航",
        "h1": "2026年最佳Web开发框架",
        "meta_desc": "对比2026年主流Web开发框架，包括Next.js、Astro、FastAPI、Nest.js等，帮你选择最适合的技术栈。",
        "keywords": "Web开发框架,2026前端框架,Next.js,Astro,后端框架,全栈框架",
        "filter": {"categories": ["Web Frameworks"], "tags_any": ["framework", "web-framework", "frontend", "backend"], "limit": 15},
        "intro": "<p>选择合适的Web开发框架是项目成功的关键。2026年，Web框架生态持续进化，前端框架更注重性能和开发体验，后端框架则更关注AI集成和类型安全。本文对比最流行的Web开发框架。</p>",
        "section_title": "推荐Web开发框架",
        "faq": [
            ("2026年最流行的前端框架是什么？", "React仍然占据最大份额，但Astro、Next.js、SvelteKit等框架增长迅速。选择取决于项目需求和团队技术栈。"),
            ("全栈框架和纯前端/后端框架怎么选？", "全栈框架（如Next.js）适合快速开发和小团队；大型项目可能需要前后端分离，分别选择最适合的框架。"),
            ("Web框架的学习成本高吗？", "不同框架差异较大。FastAPI上手简单，Nest.js需要一定的设计模式基础，Next.js的App Router概念需要时间理解。"),
        ],
    },
    {
        "filename": "best-data-tools-2026",
        "title": "2026年最佳数据分析工具 - 拾品号导航",
        "h1": "2026年最佳数据分析工具",
        "meta_desc": "整理2026年最值得使用的数据分析工具，涵盖数据可视化、BI平台、数据处理、机器学习等场景。",
        "keywords": "数据分析工具,数据可视化,BI工具,2026数据工具,开源数据分析",
        "filter": {"categories": ["Data & Analytics"], "tags_any": ["data", "analytics", "visualization", "dashboard", "research-agent", "deep-research"], "limit": 15},
        "intro": "<p>数据分析是现代企业决策的核心能力。2026年，AI正在让数据分析变得更加民主化，自然语言查询、自动报告生成、智能异常检测等功能让非技术人员也能进行复杂的数据分析。本文推荐最实用的数据分析工具。</p>",
        "section_title": "推荐数据分析工具",
        "faq": [
            ("没有编程基础能做数据分析吗？", "2026年的AI数据分析工具已经大幅降低了门槛。许多工具支持自然语言查询，可以自动生成SQL和图表。"),
            ("开源数据分析工具有哪些？", "Jupyter、Grafana、Metabase、Apache Superset等都是优秀的开源数据分析工具。"),
            ("企业级BI工具有什么推荐？", "对于企业级需求，可以考虑Metabase、Apache Superset（开源），或者Superset（商业）。选择时需考虑数据源支持、安全性和协作功能。"),
        ],
    },
    {
        "filename": "best-devops-tools-list",
        "title": "DevOps工具大全：从入门到精通 - 拾品号导航",
        "h1": "DevOps工具大全：从入门到精通",
        "meta_desc": "完整的DevOps工具清单，覆盖CI/CD、容器化、监控、日志管理、基础设施即代码等环节，适合新手和资深运维。",
        "keywords": "DevOps工具,CI/CD工具,Docker,Kubernetes,监控工具,运维工具,基础设施即代码",
        "filter": {"categories": ["Ops & Monitoring", "Deployment"], "tags_any": ["devops", "monitoring", "deployment", "observability", "infrastructure"], "limit": 15},
        "intro": "<p>DevOps是现代软件开发的核心实践，合适的工具链可以让开发和运维效率大幅提升。本文整理了从代码提交到生产部署的完整DevOps工具清单。</p>",
        "section_title": "DevOps工具推荐",
        "faq": [
            ("入门DevOps需要掌握哪些工具？", "建议从Git、Docker、CI/CD（GitHub Actions）开始，然后逐步学习Kubernetes、Terraform和监控工具。"),
            ("小型团队需要完整的DevOps工具链吗？", "不需要。小型团队可以用GitHub Actions + Docker + 云平台覆盖大部分需求，保持简单。"),
            ("DevOps和SRE有什么区别？", "DevOps是一种文化和实践，强调开发和运维的协作。SRE是Google提出的工程实践，更侧重系统可靠性和自动化。"),
        ],
    },
    {
        "filename": "best-free-developer-resources",
        "title": "免费开发者资源大全 - 拾品号导航",
        "h1": "免费开发者资源大全",
        "meta_desc": "整理2026年开发者可以免费使用的工具和资源，覆盖代码编辑、AI助手、学习平台、部署托管、设计素材等。",
        "keywords": "免费开发者资源,免费编程工具,开源资源,免费API,开发者福利",
        "filter": {"categories": ["AI Agents", "Web Frameworks", "Docs & Knowledge"], "tags_any": ["open-source", "cli", "framework", "rag", "knowledge-base"], "limit": 20},
        "intro": "<p>优秀的开发者懂得利用免费资源提升效率。2026年，大量高质量的开发工具和平台都提供免费版本。本文整理了最实用的免费开发者资源。</p>",
        "section_title": "免费开发者资源",
        "faq": [
            ("免费工具的质量靠谱吗？", "很多免费工具的质量非常高，尤其是开源项目。VS Code、GitHub Copilot Free、Cloudflare Pages等都被广泛使用。"),
            ("免费资源有什么使用限制？", "通常限制在使用次数、功能范围、存储空间等方面。对于个人学习和小项目完全够用。"),
            ("如何获取免费的云服务器？", "Oracle Cloud提供永久免费实例，AWS/GCP/Azure有12个月的免费套餐，GitHub Student Developer Pack对学生免费。"),
        ],
    },
    {
        "filename": "best-ai-agent-tools",
        "title": "AI Agent工具大全 - 拾品号导航",
        "h1": "AI Agent工具大全",
        "meta_desc": "全面整理2026年最热门的AI Agent工具和框架，涵盖编程Agent、浏览器Agent、多Agent协作、Agent开发框架等。",
        "keywords": "AI Agent工具,智能体框架,AI Agent开发,多Agent,Agent编排,2026 AI工具",
        "filter": {"categories": ["AI Agents"], "tags_any": ["agents", "agent-framework", "multi-agent", "agent-orchestration", "ai-agent"], "limit": 25},
        "intro": "<p>AI Agent（智能体）是2026年AI领域最热门的方向。从编程Agent到浏览器Agent，从单Agent到多Agent协作，开源社区涌现了大量优秀的Agent工具。本文全面整理AI Agent工具生态。</p>",
        "section_title": "AI Agent工具推荐",
        "faq": [
            ("AI Agent和普通的聊天机器人有什么区别？", "聊天机器人只能根据输入生成回复，而AI Agent能够自主规划任务、调用工具、执行操作并根据结果调整行为。Agent具有目标导向和环境感知能力。"),
            ("构建AI Agent需要什么技术基础？", "需要Python/TypeScript编程基础、对LLM API的了解、以及对Agent架构（工具调用、记忆、规划）的基本认知。"),
            ("哪个Agent框架最适合初学者？", "CrewAI上手最简单，API设计直观。如果需要更多控制，可以逐步迁移到LangGraph。"),
        ],
    },
    {
        "filename": "best-mcp-servers",
        "title": "最佳MCP Server推荐 - 拾品号导航",
        "h1": "最佳MCP Server推荐",
        "meta_desc": "精选最实用的MCP Server开源项目，涵盖开发框架、数据库连接、文件操作、API集成等场景。",
        "keywords": "MCP Server,Model Context Protocol,MCP框架,MCP工具,AI工具调用,MCP开发",
        "filter": {"categories": ["AI Agents"], "tags_any": ["mcp", "mcp-server"], "limit": 20},
        "intro": "<p>MCP（Model Context Protocol）是连接AI模型与外部工具的标准协议。2026年，MCP生态快速成长，涌现出大量优秀的MCP Server项目。本文推荐最值得关注的MCP Server。</p>",
        "section_title": "推荐MCP Server",
        "faq": [
            ("MCP Server有什么用？", "MCP Server让AI模型能够调用外部工具和数据源，如文件操作、数据库查询、API调用等，极大扩展了AI的能力边界。"),
            ("MCP Server用什么语言开发？", "官方SDK支持TypeScript和Python，社区有Rust、Go等实现。选择你最熟悉的语言即可。"),
            ("哪些AI应用支持MCP？", "Claude Desktop、Cursor、Windsurf、Cline等主流AI编程工具都已支持MCP协议。"),
        ],
    },
    {
        "filename": "best-open-source-admin-panels",
        "title": "最佳开源后台管理面板 - 拾品号导航",
        "h1": "最佳开源后台管理面板",
        "meta_desc": "对比2026年最流行的开源后台管理面板和低代码平台，帮你快速搭建企业管理系统。",
        "keywords": "开源后台管理,Admin Panel,低代码平台,后台管理系统,开源CMS,内部工具",
        "filter": {"categories": ["No-Code & Admin", "Content & CMS", "Backend & Database"], "tags_any": ["admin", "cms", "low-code", "dashboard", "internal-tools"], "limit": 15},
        "intro": "<p>开源后台管理面板可以大幅缩短企业内部管理系统的开发时间。2026年，低代码和AI辅助让后台管理系统的搭建更加高效。本文对比最流行的开源后台管理方案。</p>",
        "section_title": "推荐后台管理面板",
        "faq": [
            ("开源后台管理面板和自研系统怎么选？", "如果需求标准化（用户管理、权限控制、数据展示），用开源方案可以节省大量时间。如果需求高度定制化，可以基于开源方案二次开发。"),
            ("低代码平台适合什么场景？", "适合内部工具、数据管理、简单审批流程等标准化场景。复杂的业务逻辑和高性能要求的场景仍建议传统开发。"),
            ("后台管理面板的安全性怎么保障？", "选择有活跃维护的项目，定期更新依赖，配置HTTPS和访问控制，避免在公网暴露管理后台。"),
        ],
    },
]


def build_project_cards(projects):
    cards = []
    for i, p in enumerate(projects, 1):
        name = p.get("name", "")
        slug = slugify(name)
        desc = p.get("desc_cn") or p.get("desc", "")
        stars = p.get("stars", 0)
        lang = p.get("language", "")
        category = p.get("category_cn") or p.get("category", "")
        growth = p.get("growth", {})
        spd = growth.get("stars_per_day", 0)
        tags = p.get("tags", [])[:4]

        badge_html = ""
        if p.get("badge"):
            badge_html = f'<span class="card-badge">{esc(p["badge"])}</span>'

        stars_fmt = f"{stars:,}" if stars else "—"
        growth_text = f"📈 +{spd:.1f}/天" if spd else ""

        tag_spans = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags)

        cards.append(f"""      <article class="trend-card">
        <div class="card-head"><span class="rank">#{i}</span>{badge_html}</div>
        <h3><a href="/projects/{esc(slug)}/">{esc(name)}</a></h3>
        <p class="card-desc">{esc(desc)}</p>
        <div class="card-meta">
          <span class="stars">⭐ {stars_fmt}</span>
          <span class="lang">{esc(lang)}</span>
          <span class="category">{esc(category)}</span>
          {f'<span class="growth">{growth_text}</span>' if growth_text else ''}
        </div>
        <div class="card-tags">{tag_spans}</div>
      </article>""")
    return "\n".join(cards)


def build_page(page_def, projects):
    filtered = filter_projects(projects, **page_def["filter"])
    if not filtered:
        # fallback: use top projects by stars
        filtered = sorted(projects, key=lambda x: x.get("stars", 0), reverse=True)[:page_def["filter"].get("limit", 15)]

    canonical = f"{BASE}/guides/{page_def['filename']}.html"

    cards_html = build_project_cards(filtered)

    faq_html = ""
    if page_def.get("faq"):
        items = "".join(
            f'<details class="faq-item" open><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
            for q, a in page_def["faq"]
        )
        faq_html = f'<section class="faq-panel"><h2>常见问题</h2>{items}</section>'

    body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">Best Of</span>
      <h1>{esc(page_def['h1'])}</h1>
      <p class="daily-line">拾品号导航精选 · 帮你快速找到最优质的开源工具</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <nav class="breadcrumb-nav" aria-label="面包屑导航">
        <a href="/">首页</a> &gt; <a href="/guides/">使用指南</a> &gt; <span>{esc(page_def['h1'])}</span>
      </nav>
      <article class="guide-article">
        {page_def['intro']}
        <h2>{esc(page_def['section_title'])}</h2>
        <div class="trend-grid">
{cards_html}
        </div>
      </article>
      {faq_html}
      <div class="guide-links">
        <h2>相关资源</h2>
        <ul>
          <li><a href="/trending/">GitHub 涨星榜</a> - 发现最新热门项目</li>
          <li><a href="/collections/">专题合集</a> - 按主题浏览项目</li>
          <li><a href="/categories/">分类导航</a> - 按用途查找工具</li>
          <li><a href="/projects/">全部项目</a> - 浏览所有收录项目</li>
        </ul>
      </div>
    </section></section>"""

    # JSON-LD: BreadcrumbList
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "使用指南", "item": BASE + "/guides/"},
            {"@type": "ListItem", "position": 3, "name": page_def["h1"]},
        ],
    }

    # JSON-LD: FAQPage
    faq_entities = []
    for q, a in page_def.get("faq", []):
        faq_entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities,
    }

    # JSON-LD: Article
    article_jsonld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": page_def["h1"],
        "description": page_def["meta_desc"],
        "url": canonical,
        "publisher": {"@type": "Organization", "name": "拾品号导航", "url": BASE},
        "mainEntityOfPage": canonical,
    }

    return page_shell(
        page_def["title"],
        page_def["meta_desc"],
        canonical,
        body,
        [breadcrumbs, article_jsonld, faq_jsonld],
        page_def.get("keywords", ""),
    )


def page_shell(title, description, canonical, body, extra_jsonld=None, keywords=""):
    og = f"{BASE}/assets/hero-github-directory.png"
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
  <meta name="keywords" content="{esc(keywords)}">
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
    <footer class="footer"><a href="/">返回首页</a><a href="/projects/">全部项目</a><a href="/trending/">涨星榜</a><a href="/guides/">使用指南</a><a href="/llms.txt">LLMS.txt</a></footer>
  </main>
  <script src="/assets/fluid-bg.js" defer></script>
</body>
</html>
"""


def main():
    projects = load_projects()
    print(f"Loaded {len(projects)} projects")

    guides_root = ROOT / "guides"
    guides_root.mkdir(exist_ok=True)

    for page_def in PAGES:
        html_content = build_page(page_def, projects)
        out_path = guides_root / f"{page_def['filename']}.html"
        out_path.write_text(html_content, encoding="utf-8")
        print(f"  Generated: /guides/{page_def['filename']}.html")

    print(f"\nGenerated {len(PAGES)} best-of pages")


if __name__ == "__main__":
    main()
