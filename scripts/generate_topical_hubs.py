#!/usr/bin/env python3
"""Generate topical authority hub pages for SEO.

Each hub page aggregates projects, guides, and collections around a specific
topic with proper SEO signals:
- H1 with keyword
- Project cards from data/projects.json filtered by topic
- Links to related guides
- FAQ section with FAQPage JSON-LD
- BreadcrumbList JSON-LD
- ItemList JSON-LD for projects
- Internal links to categories and collections
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://daohang.bot.cd"

# ---------------------------------------------------------------------------
# Hub definitions
# ---------------------------------------------------------------------------

HUBS = [
    {
        "slug": "ai-agents",
        "title": "AI Agent 开源项目大全 - 2026 年最佳智能体工具推荐 - 拾品号导航",
        "h1": "AI Agent 开源项目大全：2026 年最佳智能体工具推荐",
        "meta_desc": "精选 2026 年最值得关注的 AI Agent（智能体）开源项目，涵盖 Agent 框架、多智能体编排、浏览器智能体、代码智能体等方向，帮助开发者快速选型。",
        "keywords": "AI Agent,智能体,Agent框架,多智能体,开源Agent,LangGraph,CrewAI,Agent编排,2026",
        "eyebrow": "Hub · AI Agents",
        "intro": "AI Agent（智能体）是 2026 年 AI 应用的核心趋势。本页汇聚拾品号导航收录的所有 Agent 相关开源项目、使用指南和专题合集，方便开发者按需选型。",
        "filter": {
            "categories": ["AI Agents"],
            "tags_any": [
                "agent", "agent-framework", "agent-orchestration", "multi-agent",
                "agentic", "agent-builder", "agent-deploy", "agent-memory",
                "agent-runtime", "agent-safety", "agent-security", "agent-workflow",
                "agent-os", "agent-governance", "agent-skill", "agent-skills",
            ],
        },
        "related_guides": [
            ("best-open-source-ai-agent-frameworks", "开源 AI Agent 框架对比"),
            ("ai-agent-use-cases", "AI Agent 实际应用场景"),
        ],
        "related_collections": [
            ("ai-coding-tools", "AI 编程与智能体工具合集"),
            ("github-rising-ai", "GitHub Rising AI"),
        ],
        "related_categories": [
            ("ai-agents", "AI 智能体"),
            ("automation", "自动化"),
        ],
        "faq": [
            ("什么是 AI Agent？", "AI Agent（智能体）是能够自主规划任务、调用工具、执行操作并根据结果调整行为的 AI 系统。与传统聊天机器人不同，Agent 具有目标导向和环境感知能力，可以完成多步骤复杂任务。"),
            ("2026 年最流行的 AI Agent 框架有哪些？", "2026 年主流的 AI Agent 框架包括 LangGraph（LangChain 生态）、CrewAI（多 Agent 协作）、AutoGen（微软）、Mastra（TypeScript）、Pydantic AI 等。选择取决于你的技术栈和场景需求。"),
            ("AI Agent 和普通聊天机器人有什么区别？", "聊天机器人只能根据输入生成回复，而 AI Agent 能够自主规划任务、调用工具、执行操作并根据结果调整行为。Agent 具有目标导向、工具调用和环境感知能力。"),
            ("个人开发者如何开始构建 AI Agent？", "建议从编程 Agent 开始体验（如 Claude Code），然后选择一个轻量级框架（如 CrewAI 或 Pydantic AI）搭建自己的 Agent。MCP 协议可以帮你快速接入外部工具。"),
        ],
    },
    {
        "slug": "ai-coding-tools",
        "title": "AI 编程工具大全 - 2026 年代码助手与智能体推荐 - 拾品号导航",
        "h1": "AI 编程工具大全：2026 年代码助手与智能体推荐",
        "meta_desc": "精选 2026 年最好的 AI 编程工具和代码助手，涵盖 IDE 集成、终端编程、代码生成、代码审查等方向，包括 Cursor、Claude Code、Windsurf 等热门工具。",
        "keywords": "AI编程工具,代码助手,Cursor,Claude Code,Windsurf,Copilot,AI代码生成,编程智能体,2026",
        "eyebrow": "Hub · AI Coding",
        "intro": "AI 编程工具正在改变开发者的工作方式。本页汇聚拾品号导航收录的所有 AI 编程相关项目、使用指南和专题合集，帮助你找到最适合的 AI 编码助手。",
        "filter": {
            "categories": [],
            "tags_any": [
                "ai-coding", "coding", "coding-agent", "coding-agents",
                "coding-workflow", "code-generation", "code-review",
                "code-intelligence",
            ],
            "name_keywords": [
                "code", "coding", "copilot", "cursor", "windsurf", "aider",
                "openhands", "continue",
            ],
        },
        "related_guides": [
            ("best-ai-coding-agents-2026", "2026 年最好用的 AI 编程助手推荐"),
            ("cursor-vs-windsurf-vs-claude-code", "Cursor vs Windsurf vs Claude Code 对比"),
            ("cursor-alternatives", "Cursor 替代品推荐"),
        ],
        "related_collections": [
            ("ai-coding-tools", "AI 编程与智能体工具合集"),
        ],
        "related_categories": [
            ("ai-agents", "AI 智能体"),
        ],
        "faq": [
            ("AI 编程工具能完全替代程序员吗？", "不能。AI 编程工具是提升效率的助手，帮助开发者减少重复性工作，专注于架构设计、业务逻辑和创新。需要人类判断力的领域仍然是不可替代的。"),
            ("2026 年最好的 AI 编程工具有哪些？", "Cursor、Claude Code、Windsurf 和 GitHub Copilot 是 2026 年最受欢迎的 AI 编程工具。Cursor 适合 IDE 用户，Claude Code 适合终端用户，Windsurf 价格最低，Copilot 与 GitHub 生态集成最深。"),
            ("免费的 AI 编程工具有哪些？", "GitHub Copilot 有免费额度，Cursor 和 Windsurf 有免费版（功能有限），开源方案如 Aider 和 OpenHands 完全免费但需自备 API Key。"),
            ("AI 编程工具生成的代码质量如何？", "对于常见 CRUD 操作、模板代码和简单功能，AI 生成的代码质量通常不错。复杂业务逻辑仍需人工审查。建议将 AI 输出作为起点，而非最终代码。"),
        ],
    },
    {
        "slug": "mcp-ecosystem",
        "title": "MCP 生态全景 - Model Context Protocol 工具与框架 - 拾品号导航",
        "h1": "MCP 生态全景：Model Context Protocol 工具与框架",
        "meta_desc": "全面梳理 MCP（Model Context Protocol）生态系统，收录 MCP Server、MCP 框架、MCP 工具链等开源项目，帮助开发者理解和参与 MCP 生态。",
        "keywords": "MCP,Model Context Protocol,MCP Server,MCP框架,MCP工具,AI工具调用,Agent工具链",
        "eyebrow": "Hub · MCP Ecosystem",
        "intro": "MCP（Model Context Protocol）是 Anthropic 提出的开放标准，用于规范 AI 模型与外部工具、数据源之间的通信。本页汇聚 MCP 生态相关项目、指南和资源。",
        "filter": {
            "categories": [],
            "tags_any": ["mcp", "mcp-server"],
            "name_keywords": ["mcp"],
        },
        "related_guides": [
            ("mcp-server-guide", "什么是 MCP Server？一文搞懂 Model Context Protocol"),
        ],
        "related_collections": [
            ("ai-coding-tools", "AI 编程与智能体工具合集"),
            ("github-rising-ai", "GitHub Rising AI"),
        ],
        "related_categories": [
            ("ai-agents", "AI 智能体"),
        ],
        "faq": [
            ("什么是 MCP（Model Context Protocol）？", "MCP 是 Anthropic 提出的开放标准协议，定义了 AI 模型与外部工具、数据源之间的通信规范。类似于 USB 协议让不同设备即插即用，MCP 让 AI 应用可以无缝连接各种工具和服务。"),
            ("MCP 和 Function Calling 有什么区别？", "Function Calling 是 OpenAI 等厂商的专有实现，MCP 是开放标准。MCP 支持工具发现、资源描述、多传输方式（stdio / HTTP SSE），比 Function Calling 更通用、更标准化。"),
            ("MCP Server 可以用什么语言开发？", "官方 SDK 支持 TypeScript 和 Python，社区有 Rust、Go、Java 等实现。只要遵循 MCP 协议规范，任何语言都可以开发 MCP Server。"),
            ("哪些 AI 应用支持 MCP？", "Claude Desktop、Cursor、Windsurf、Cline、Continue 等主流 AI 编程工具都已支持 MCP 协议。支持 MCP 的应用生态正在快速扩大。"),
        ],
    },
    {
        "slug": "web-development",
        "title": "Web 开发工具大全 - 2026 年前端与全栈开源项目 - 拾品号导航",
        "h1": "Web 开发工具大全：2026 年前端与全栈开源项目",
        "meta_desc": "精选 2026 年 Web 开发相关的开源项目和工具，涵盖前端框架、Web 自动化、浏览器工具、网站构建器、CMS 等方向。",
        "keywords": "Web开发,前端框架,全栈开发,Web自动化,浏览器工具,网站构建器,开源CMS,2026",
        "eyebrow": "Hub · Web Dev",
        "intro": "Web 开发是开源生态最活跃的领域之一。本页汇聚拾品号导航收录的 Web 开发相关项目、指南和专题合集，覆盖前端、全栈和 Web 自动化方向。",
        "filter": {
            "categories": ["Web Frameworks", "Content & CMS", "No-Code & Admin"],
            "tags_any": [
                "web", "web-agent", "web-browsing", "web-dashboard",
                "web-research", "web-scraper", "web-scraping", "web-tasks",
                "web-testing", "web-ui", "web-use", "browser", "browser-agent",
                "browser-agents", "browser-api", "browser-automation",
                "browser-infra", "browser-use", "frontend", "website-builder",
                "cms",
            ],
        },
        "related_guides": [
            ("how-to-build-static-site-with-ai", "用 AI 工具快速搭建静态网站"),
            ("browser-automation-tools-comparison", "浏览器自动化工具对比"),
        ],
        "related_collections": [
            ("website-builders", "网站构建器合集"),
            ("ai-coding-tools", "AI 编程与智能体工具合集"),
        ],
        "related_categories": [
            ("web-frameworks", "Web 框架"),
            ("content-cms", "内容管理 / CMS"),
            ("no-code-admin", "无代码 / 后台管理"),
        ],
        "faq": [
            ("2026 年最流行的 Web 前端框架是什么？", "React 仍然是最流行的前端框架，Next.js 是 React 生态的全栈解决方案。Vue 和 Nuxt.js 在国内也很流行。新兴框架如 Astro 适合内容站，SvelteKit 以轻量著称。"),
            ("AI 如何改变 Web 开发？", "AI 编程助手可以加速前端开发、自动生成组件代码、辅助 UI 设计。浏览器自动化 Agent 可以自动执行 E2E 测试、数据采集和网页任务。"),
            ("如何选择 Web 框架？", "内容站选 Astro，全栈应用选 Next.js 或 Nuxt.js，轻量交互选 SvelteKit。如果需要 CMS 能力，可以结合 Strapi 或 Payload CMS 等无头 CMS。"),
        ],
    },
    {
        "slug": "devops-tools",
        "title": "DevOps 工具大全 - 2026 年运维与部署开源项目 - 拾品号导航",
        "h1": "DevOps 工具大全：2026 年运维与部署开源项目",
        "meta_desc": "精选 2026 年 DevOps 和运维相关的开源工具，涵盖 CI/CD、容器化、监控、日志管理、部署、数据库和基础设施管理等方向。",
        "keywords": "DevOps工具,CI/CD,容器,Docker,Kubernetes,监控,部署,运维,日志管理,2026",
        "eyebrow": "Hub · DevOps",
        "intro": "DevOps 工具链是现代软件开发的基础设施。本页汇聚拾品号导航收录的 DevOps 相关项目和指南，覆盖从代码到部署的完整工具链。",
        "filter": {
            "categories": ["Deployment", "Ops & Monitoring", "Backend & Database"],
            "tags_any": [
                "deploy", "docker", "monitoring", "observability",
                "infrastructure", "ci-cd", "database", "serverless",
                "deployment", "devops", "kubernetes", "container",
            ],
        },
        "related_guides": [
            ("devops-tools-2026", "2026 年 DevOps 工具链推荐"),
            ("best-self-hosted-tools-2026", "最佳自部署开源工具推荐"),
        ],
        "related_collections": [],
        "related_categories": [
            ("deployment", "部署"),
            ("ops-monitoring", "运维监控"),
            ("backend-database", "后端 / 数据库"),
            ("automation", "自动化"),
        ],
        "faq": [
            ("小型团队需要完整的 DevOps 工具链吗？", "不需要。小型团队可以用 GitHub Actions + Docker + Vercel/Cloudflare Pages 覆盖大部分需求，保持简单。随着团队规模增长再逐步引入更多工具。"),
            ("2026 年最值得关注的 DevOps 趋势是什么？", "AI 驱动的运维（AIOps）正在兴起，包括智能告警、自动故障排查和自动生成运维脚本。GitOps、平台工程（Platform Engineering）和开发者体验（DX）也是热门趋势。"),
            ("自部署和云服务怎么选？", "如果你对数据隐私有严格要求或需要深度定制，选自部署。如果追求便捷和弹性扩展，选云服务。很多团队采用混合方案：核心系统自部署，辅助工具用云服务。"),
        ],
    },
    {
        "slug": "automation",
        "title": "自动化工具大全 - 2026 年工作流与 RPA 开源项目 - 拾品号导航",
        "h1": "自动化工具大全：2026 年工作流与 RPA 开源项目",
        "meta_desc": "精选 2026 年自动化相关开源项目和工具，涵盖工作流自动化、浏览器自动化、桌面自动化、RPA 和 AI 自动化等方向。",
        "keywords": "自动化工具,工作流自动化,RPA,浏览器自动化,桌面自动化,开源自动化,AI自动化,2026",
        "eyebrow": "Hub · Automation",
        "intro": "自动化工具可以将重复性任务交给机器执行，提升效率和一致性。本页汇聚拾品号导航收录的自动化相关项目和指南。",
        "filter": {
            "categories": ["Automation"],
            "tags_any": [
                "automation", "browser-automation", "desktop-automation",
                "workflow", "workflows", "agentic-workflow", "agent-workflow",
                "rpa", "scraping", "web-scraping", "web-scraper",
            ],
        },
        "related_guides": [
            ("browser-automation-tools-comparison", "浏览器自动化工具对比"),
            ("ai-agent-use-cases", "AI Agent 实际应用场景"),
        ],
        "related_collections": [
            ("automation-tools", "自动化工具合集"),
        ],
        "related_categories": [
            ("automation", "自动化"),
            ("ai-agents", "AI 智能体"),
        ],
        "faq": [
            ("工作流自动化和 RPA 有什么区别？", "工作流自动化侧重于将业务流程编排成可自动执行的工作流（如 n8n、Zapier）。RPA（机器人流程自动化）侧重于模拟人类在 GUI 上的操作（如点击、输入）。2026 年两者的边界正在模糊，AI Agent 也可以执行 GUI 自动化任务。"),
            ("开源自动化工具有哪些推荐？", "n8n 是最流行的开源工作流自动化工具，支持 400+ 集成。Playwright 是浏览器自动化的首选。Browser Use 和 Steel Browser 专注于 AI Agent 浏览器操作。Make（原 Integromat）和 Zapier 是商业替代。"),
            ("自动化工具需要编程基础吗？", "不一定。n8n、Zapier、Make 等工具提供可视化拖拽界面，无需编程。但如果需要复杂的定制逻辑，Python 或 JavaScript 基础会有很大帮助。"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def load_projects():
    data_path = ROOT / "data" / "projects.json"
    with open(data_path, encoding="utf-8") as f:
        return json.load(f)


def match_project(project: dict, filter_cfg: dict) -> bool:
    """Check if a project matches the hub filter criteria."""
    cat = project.get("category", "")
    tags = [t.lower() for t in project.get("tags", [])]
    name = project.get("name", "").lower()

    # Category match
    if filter_cfg.get("categories"):
        if cat in filter_cfg["categories"]:
            return True

    # Tag match (any)
    if filter_cfg.get("tags_any"):
        filter_tags = [t.lower() for t in filter_cfg["tags_any"]]
        if any(t in filter_tags for t in tags):
            return True

    # Name keyword match
    if filter_cfg.get("name_keywords"):
        keywords = [k.lower() for k in filter_cfg["name_keywords"]]
        if any(kw in name for kw in keywords):
            return True

    return False


def project_card(project: dict) -> str:
    """Render a single project card matching the existing site style."""
    name = esc(project.get("name", ""))
    url = esc(project.get("url", ""))
    desc_cn = esc(project.get("desc_cn", ""))
    desc_en = esc(project.get("desc", ""))
    stars = project.get("stars", 0)
    growth = project.get("growth", {})
    spd = growth.get("stars_per_day", 0)
    language = esc(project.get("language", ""))
    badge = esc(project.get("badge", ""))
    tags = project.get("tags", [])

    stars_str = f"{stars:,}" if isinstance(stars, int) else str(stars)
    spd_str = f"{spd:.2f}" if spd else "0"

    tags_html = "".join(f"<span>{esc(t)}</span>" for t in tags[:4])

    return f"""        <article class="trend-card">
          <h2><a href="{url}" target="_blank" rel="noopener">{name}</a></h2>
          <p lang="zh-CN">{desc_cn}</p>
          <p class="english-desc" lang="en">{desc_en}</p>
          <div class="trend-meta"><span>★ {stars_str}</span><span>↗ {spd_str}/天</span><span>{language}</span><span>{badge}</span></div>
          <div class="trend-tags">{tags_html}</div>
        </article>"""


def build_faq_html(faq_list: list) -> str:
    if not faq_list:
        return ""
    items = "".join(
        f'<details class="faq-item" open><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for q, a in faq_list
    )
    return f'<section class="faq-panel"><h2>常见问题</h2>{items}</section>'


def build_related_links_html(hub: dict) -> str:
    """Build the internal links section."""
    sections = []

    # Related guides
    guides = hub.get("related_guides", [])
    if guides:
        items = "".join(
            f'<li><a href="/guides/{slug}.html">{esc(title)}</a></li>'
            for slug, title in guides
        )
        sections.append(f"<h3>相关指南</h3><ul>{items}</ul>")

    # Related collections
    collections = hub.get("related_collections", [])
    if collections:
        items = "".join(
            f'<li><a href="/collections/{slug}/">{esc(title)}</a></li>'
            for slug, title in collections
        )
        sections.append(f"<h3>专题合集</h3><ul>{items}</ul>")

    # Related categories
    categories = hub.get("related_categories", [])
    if categories:
        items = "".join(
            f'<li><a href="/categories/{slug}/">{esc(title)}</a></li>'
            for slug, title in categories
        )
        sections.append(f"<h3>分类导航</h3><ul>{items}</ul>")

    # Standard links
    standard = """
      <h3>更多资源</h3>
      <ul>
        <li><a href="/trending/">GitHub 涨星榜</a> - 发现最新热门项目</li>
        <li><a href="/projects/">全部项目</a> - 浏览所有收录项目</li>
        <li><a href="/guides/">使用指南</a> - 开发者实用指南</li>
        <li><a href="/daily-brief/">分享快报</a> - 每日开源动态</li>
      </ul>"""

    inner = "\n".join(sections) + standard
    return f'<div class="guide-links"><h2>相关资源</h2>{inner}</div>'


def page_shell(title: str, description: str, canonical: str, body: str,
               extra_jsonld: list | None = None, keywords: str = "") -> str:
    og = f"{BASE}/assets/hero-github-directory.png"
    jsonld_blocks = ""
    if extra_jsonld:
        for ld in extra_jsonld:
            jsonld_blocks += (
                f'  <script type="application/ld+json">'
                f'{json.dumps(ld, ensure_ascii=False)}</script>\n'
            )
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


# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

def main():
    projects = load_projects()
    hubs_root = ROOT / "hubs"
    hubs_root.mkdir(exist_ok=True)

    for hub in HUBS:
        slug = hub["slug"]
        canonical = f"{BASE}/hubs/{slug}/"
        hub_dir = hubs_root / slug
        hub_dir.mkdir(exist_ok=True)

        # Filter matching projects
        matched = [p for p in projects if match_project(p, hub["filter"])]
        # Sort by stars descending
        matched.sort(key=lambda p: p.get("stars", 0), reverse=True)
        count = len(matched)

        # Build project cards
        cards_html = "\n".join(project_card(p) for p in matched)

        # Build FAQ
        faq_html = build_faq_html(hub.get("faq", []))

        # Build related links
        related_html = build_related_links_html(hub)

        # Build BreadcrumbList JSON-LD
        breadcrumbs = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "首页", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "专题 Hub", "item": BASE + "/hubs/"},
                {"@type": "ListItem", "position": 3, "name": hub["h1"]},
            ],
        }

        # Build FAQPage JSON-LD
        faq_entities = []
        for q, a in hub.get("faq", []):
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

        # Build ItemList JSON-LD for projects
        item_list_elements = []
        for idx, p in enumerate(matched, 1):
            item_list_elements.append({
                "@type": "ListItem",
                "position": idx,
                "name": p.get("name", ""),
                "url": p.get("url", ""),
                "description": p.get("desc_cn", "") or p.get("desc", ""),
            })
        itemlist_jsonld = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": hub["h1"],
            "url": canonical,
            "description": hub["meta_desc"],
            "isPartOf": {"@type": "WebSite", "name": "拾品号导航", "url": BASE},
            "mainEntity": {
                "@type": "ItemList",
                "itemListElement": item_list_elements,
            },
        }

        # Compose page body
        body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">{esc(hub['eyebrow'])}</span>
      <h1>{esc(hub['h1'])}</h1>
      <p>{esc(hub['intro'])}</p>
      <p class="daily-line">收录 {count} 个项目 · 数据来自 data/projects.json · 持续更新</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <nav class="breadcrumb-nav" aria-label="面包屑导航">
        <a href="/">首页</a> &gt; <a href="/hubs/">专题 Hub</a> &gt; <span>{esc(hub['h1'])}</span>
      </nav>
      <div class="directory-intro"><div><span class="eyebrow">Hub 说明</span><strong>{esc(hub['meta_desc'])}</strong></div><div class="stats-row"><span>{count} 个项目</span><span>JSON-LD ItemList</span><span>直接访问 GitHub</span></div></div>
      <div class="trend-grid">
{cards_html}
      </div>
      {faq_html}
      {related_html}
    </section></section>"""

        out_path = hub_dir / "index.html"
        out_path.write_text(
            page_shell(
                hub["title"],
                hub["meta_desc"],
                canonical,
                body,
                [breadcrumbs, itemlist_jsonld, faq_jsonld],
                hub.get("keywords", ""),
            ),
            encoding="utf-8",
        )
        print(f"  Generated: /hubs/{slug}/index.html ({count} projects)")

    # Generate hubs index page
    cards = ""
    for hub in HUBS:
        slug = hub["slug"]
        cards += (
            f'<article class="trend-card">'
            f'<h2><a href="/hubs/{slug}/">{esc(hub["h1"])}</a></h2>'
            f'<p>{esc(hub["meta_desc"])}</p>'
            f'</article>\n'
        )

    index_body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">Hubs</span>
      <h1>专题权威 Hub 导航</h1>
      <p>按主题聚合开源项目、使用指南和专题合集，帮助开发者快速找到特定领域的最佳工具和资源。</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="trend-grid">
{cards}
      </div>
    </section></section>"""

    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "专题 Hub"},
        ],
    }
    index_path = hubs_root / "index.html"
    index_path.write_text(
        page_shell(
            "专题权威 Hub 导航 - 拾品号导航",
            "按主题聚合开源项目、使用指南和专题合集，帮助开发者快速找到特定领域的最佳工具和资源。",
            f"{BASE}/hubs/",
            index_body,
            [breadcrumbs],
            "开源项目Hub,AI工具导航,开发者资源,专题合集",
        ),
        encoding="utf-8",
    )
    print(f"  Generated: /hubs/index.html")
    print("Done!")


if __name__ == "__main__":
    main()
