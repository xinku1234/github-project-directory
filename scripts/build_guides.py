#!/usr/bin/env python3
"""Generate SEO-optimized guide articles targeting high-volume search queries.

Each guide targets a specific search intent with:
- H1 targeting the main keyword
- FAQ structured data
- Breadcrumb navigation
- Internal links to projects, categories, and collections
- Answer-ready content for GEO/AI engines
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://daohang.bot.cd"

GUIDES = [
    {
        "slug": "best-ai-coding-agents-2026",
        "title": "2026 年最好用的 AI 编程助手推荐 - 拾品号导航",
        "h1": "2026 年最好用的 AI 编程助手推荐",
        "meta_desc": "精选 2026 年最值得关注的 AI 编程助手和代码生成工具，包括 Claude Code、Cursor、Windsurf 等开源和商业方案，帮助开发者提升编码效率。",
        "keywords": "AI编程助手,AI代码生成,Claude Code,Cursor,Windsurf,Copilot,开源编程工具",
        "content": """<p>AI 编程助手正在改变开发者的工作方式。从自动补全到完整的代码生成，这些工具可以显著提升开发效率。本文整理了 2026 年最值得关注的 AI 编程助手，涵盖开源和商业方案。</p>
<h2>什么是 AI 编程助手？</h2>
<p>AI 编程助手是利用大语言模型（LLM）帮助开发者编写、调试和优化代码的工具。它们通常支持代码补全、代码生成、代码审查、错误修复等功能。2026 年的 AI 编程助手已经从简单的代码补全进化到能够理解整个代码库上下文、执行多步骤任务的智能体（Agent）。</p>
<h2>2026 年推荐的 AI 编程助手</h2>
<h3>1. Claude Code</h3>
<p>Anthropic 推出的终端编程助手，直接在命令行中运行，能够理解项目全貌、执行复杂重构、运行测试和管理 Git 工作流。适合喜欢终端工作流的开发者。</p>
<h3>2. Cursor</h3>
<p>基于 VS Code 的 AI-first 编辑器，支持多模型切换、代码库问答、内联编辑和 Agent 模式。适合希望在 IDE 中获得完整 AI 体验的开发者。</p>
<h3>3. GitHub Copilot</h3>
<p>GitHub 官方的 AI 编程助手，深度集成在 VS Code 和 JetBrains 中，支持代码补全、聊天和 Agent 模式。适合已在 GitHub 生态中的团队。</p>
<h3>4. Windsurf (Codeium)</h3>
<p>Codeium 推出的 AI 编辑器，强调流式编辑体验和上下文理解能力，支持 Cascade 多步骤工作流。</p>
<h3>5. 开源替代方案</h3>
<p>如果你更倾向开源方案，可以关注：<a href="/projects/agent0ai-agent-zero/">Agent Zero</a>、<a href="/projects/openhands/">OpenHands</a>、<a href="/projects/aider/">Aider</a> 等项目。这些工具在 GitHub 上活跃维护，适合自部署和定制。</p>
<h2>如何选择 AI 编程助手？</h2>
<ul>
<li><strong>工作流偏好：</strong>终端用户推荐 Claude Code 或 Aider，IDE 用户推荐 Cursor 或 Windsurf</li>
<li><strong>隐私要求：</strong>对代码隐私有要求的团队可以选开源方案自部署</li>
<li><strong>预算：</strong>GitHub Copilot 和 Cursor 有免费额度，开源方案完全免费</li>
<li><strong>团队规模：</strong>大团队需要考虑企业级功能、权限管理和审计日志</li>
</ul>
<h2>AI 编程助手的发展趋势</h2>
<p>2026 年的 AI 编程助手正在从「代码补全」进化为「编程智能体」。新一代工具不仅能写代码，还能理解需求、规划任务、执行测试和部署应用。MCP（Model Context Protocol）等标准的出现也让 AI 工具能够调用外部服务和工具链。</p>""",
        "faq": [
            ("AI 编程助手会取代程序员吗？", "不会。AI 编程助手是提升效率的工具，帮助开发者减少重复性工作，专注于架构设计、业务逻辑和创新。需要人类判断力的领域仍然是不可替代的。"),
            ("AI 编程助手生成的代码质量如何？", "取决于任务复杂度和模型能力。对于常见的 CRUD 操作、模板代码和简单功能，质量通常不错。复杂业务逻辑仍需人工审查和调整。"),
            ("免费的 AI 编程工具有哪些？", "GitHub Copilot 有免费额度，Cursor 有免费版，开源方案如 Aider、OpenHands 完全免费但需要自己部署模型。"),
        ],
    },
    {
        "slug": "best-open-source-ai-agent-frameworks",
        "title": "开源 AI Agent 框架对比：2026 年最值得尝试的项目 - 拾品号导航",
        "h1": "开源 AI Agent 框架对比：2026 年最值得尝试的项目",
        "meta_desc": "对比 LangGraph、CrewAI、AutoGen、Agno 等主流开源 AI Agent 框架，从架构、易用性、扩展性和社区活跃度帮你选择最适合的方案。",
        "keywords": "AI Agent框架,LangGraph,CrewAI,AutoGen,开源智能体,多Agent,Agent编排",
        "content": """<p>AI Agent（智能体）是 2026 年 AI 应用的核心趋势之一。开源社区涌现了大量 Agent 框架，帮助开发者构建能够自主决策、调用工具、完成复杂任务的 AI 系统。本文对比主流开源 Agent 框架，帮你快速选型。</p>
<h2>什么是 AI Agent 框架？</h2>
<p>AI Agent 框架提供了一套基础设施，让开发者可以定义 Agent 的行为、工具调用、记忆管理和多 Agent 协作。一个好的框架应该支持：工具注册与调用、状态管理、错误恢复、可观测性和多模型支持。</p>
<h2>主流框架对比</h2>
<h3>LangGraph (LangChain)</h3>
<p>LangChain 团队推出的图式 Agent 框架，用有状态图建模多步骤 LLM 应用。优势是生态成熟、文档完善、支持复杂工作流。适合需要精细控制 Agent 行为的场景。</p>
<h3>CrewAI</h3>
<p>专注于多 Agent 协作的框架，提供角色定义、任务分配和团队协作的抽象。上手简单，适合快速搭建多 Agent 原型。</p>
<h3>AutoGen (Microsoft)</h3>
<p>微软开源的多 Agent 对话框架，支持 Agent 之间的自动对话和代码执行。适合研究性质的多 Agent 实验。</p>
<h3>Agno</h3>
<p>轻量级 Agent 框架，强调简洁 API 和快速开发。适合不需要复杂编排、希望快速验证想法的开发者。</p>
<h2>选择建议</h2>
<ul>
<li><strong>生产环境：</strong>优先考虑 LangGraph，生态成熟、可观测性好</li>
<li><strong>多 Agent 协作：</strong>CrewAI 或 AutoGen</li>
<li><strong>快速原型：</strong>Agno 或直接用 OpenAI/Anthropic SDK</li>
<li><strong>研究实验：</strong>AutoGen 或自定义框架</li>
</ul>""",
        "faq": [
            ("AI Agent 和普通的聊天机器人有什么区别？", "聊天机器人只能根据输入生成回复，而 AI Agent 能够自主规划任务、调用工具、执行操作并根据结果调整行为。Agent 具有目标导向和环境感知能力。"),
            ("构建 AI Agent 需要什么技术基础？", "需要 Python/TypeScript 编程基础、对 LLM API 的了解、以及对 Agent 架构（工具调用、记忆、规划）的基本认知。"),
            ("哪个 Agent 框架最适合初学者？", "CrewAI 上手最简单，API 设计直观。如果需要更多控制，可以逐步迁移到 LangGraph。"),
        ],
    },
    {
        "slug": "github-stars-guide",
        "title": "GitHub Star 是什么意思？如何找到快速涨星的项目？ - 拾品号导航",
        "h1": "GitHub Star 是什么意思？如何找到快速涨星的项目？",
        "meta_desc": "解释 GitHub Star 的含义、价值和局限性，以及如何利用涨星数据发现值得关注的新开源项目和 AI 工具。",
        "keywords": "GitHub Star,涨星,开源项目推荐,GitHub趋势,AI开源项目,开发者工具",
        "content": """<p>GitHub Star 是 GitHub 平台上的收藏功能，用户可以给自己觉得有价值的仓库点 Star。Star 数量常被用作衡量项目受欢迎程度的指标，但它真的代表项目质量吗？</p>
<h2>GitHub Star 的含义</h2>
<p>Star 本质上是一个「收藏夹」功能，类似于浏览器书签。用户点 Star 的原因多种多样：觉得项目有用、想以后再看、支持开发者、跟风收藏等。因此 Star 数更多反映的是「关注度」而非「质量」。</p>
<h2>快速涨星意味着什么？</h2>
<p>一个项目在短时间内获得大量 Star（即「涨星」），通常意味着：</p>
<ul>
<li>项目出现在了 Hacker News、Reddit、Twitter 等平台的热门推荐</li>
<li>项目解决了开发者的真实痛点</li>
<li>项目来自知名公司或开发者</li>
<li>项目具有创新性或话题性</li>
</ul>
<h2>如何找到快速涨星的项目？</h2>
<p>拾品号导航的 <a href="/trending/">GitHub 涨星榜</a> 每天自动同步 GitHub 上近期创建且涨星速度最快的项目。数据来自 GitHub Search API，按 Stars/天 排序，帮助你发现最新的开源热点。</p>
<h2>Star 数高 ≠ 项目好用</h2>
<p>判断一个开源项目是否值得使用，还需要看：</p>
<ul>
<li><strong>维护状态：</strong>最近是否有 commit、Issue 响应速度</li>
<li><strong>文档质量：</strong>README 是否清晰、是否有使用指南</li>
<li><strong>社区活跃度：</strong>Contributor 数量、Discussions 活跃度</li>
<li><strong>License：</strong>是否允许你的使用场景</li>
<li><strong>依赖风险：</strong>是否依赖其他不稳定的项目</li>
</ul>""",
        "faq": [
            ("GitHub Star 对项目有什么实际价值？", "Star 数影响项目在 GitHub 搜索结果中的排名、吸引贡献者和投资者的注意力、以及在社交媒体上的传播力。对于维护者来说，Star 是一种社区认可。"),
            ("如何区分真实涨星和刷 Star？", "真实涨星通常伴随 Issue 增长、PR 提交和社区讨论。如果一个项目 Star 很多但没有社区活动，可能存在刷 Star 的情况。"),
            ("拾品号导航的涨星数据多久更新一次？", "涨星数据通过 GitHub Search API 每日自动同步，按近 45 天内创建的项目按 Stars/天 排序。"),
        ],
    },
    {
        "slug": "how-to-build-static-site-with-ai",
        "title": "用 AI 工具快速搭建静态网站：2026 年完整指南 - 拾品号导航",
        "h1": "用 AI 工具快速搭建静态网站：2026 年完整指南",
        "meta_desc": "从零开始用 AI 编程助手和开源框架搭建静态网站的完整流程，覆盖 Astro、Hugo、Next.js 等方案，以及 Cloudflare Pages 部署。",
        "keywords": "静态网站,AI建站,Astro,Hugo,Next.js,Cloudflare Pages,开源建站",
        "content": """<p>2026 年，借助 AI 编程助手和现代静态网站生成器，从零搭建一个专业网站的时间已经从几天缩短到几小时。本文介绍如何用 AI 工具快速搭建和部署静态网站。</p>
<h2>为什么选择静态网站？</h2>
<p>静态网站具有速度快、安全性高、部署简单、成本低的优势。对于博客、文档站、产品官网、导航站等场景，静态网站是最佳选择。配合 CDN（如 Cloudflare Pages），可以实现全球毫秒级访问。</p>
<h2>推荐的静态网站框架</h2>
<h3>Astro</h3>
<p>2026 年最流行的静态网站框架之一，支持按需加载、零 JavaScript 默认输出、多 UI 框架混用。适合内容站、博客和文档站。</p>
<h3>Hugo</h3>
<p>Go 语言编写的静态网站生成器，构建速度极快（毫秒级），适合大型网站和频繁更新的内容站。</p>
<h3>Next.js (Static Export)</h3>
<p>React 生态的全栈框架，支持静态导出模式。适合需要丰富交互的网站。</p>
<h2>用 AI 辅助建站的流程</h2>
<ol>
<li><strong>确定需求：</strong>明确网站类型、页面结构和核心功能</li>
<li><strong>选择框架：</strong>内容站选 Astro，速度优先选 Hugo，交互丰富选 Next.js</li>
<li><strong>AI 生成代码：</strong>用 Claude Code 或 Cursor 生成初始项目结构和页面模板</li>
<li><strong>内容填充：</strong>用 AI 辅助撰写文案、生成图片描述</li>
<li><strong>SEO 优化：</strong>添加 meta 标签、sitemap、结构化数据</li>
<li><strong>部署：</strong>推送到 GitHub，连接 Cloudflare Pages 自动部署</li>
</ol>
<h2>部署到 Cloudflare Pages</h2>
<p>Cloudflare Pages 提供免费的静态网站托管，支持自动构建、预览部署和自定义域名。只需将 GitHub 仓库连接到 Cloudflare Pages，即可实现推送即部署。</p>""",
        "faq": [
            ("静态网站适合什么场景？", "博客、文档站、产品官网、导航站、作品集、营销落地页等以内容展示为主的场景。不适合需要频繁用户交互和实时数据的应用。"),
            ("AI 生成的网站代码可以直接用吗？", "可以作为起点，但建议人工审查代码质量、SEO 设置和安全性。AI 生成的代码通常需要根据实际需求调整。"),
            ("Cloudflare Pages 免费吗？", "是的，Cloudflare Pages 的免费计划支持每月 500 次构建、无限站点和无限带宽，对于个人项目完全够用。"),
        ],
    },
    {
        "slug": "mcp-server-guide",
        "title": "什么是 MCP Server？一文搞懂 Model Context Protocol - 拾品号导航",
        "h1": "什么是 MCP Server？一文搞懂 Model Context Protocol",
        "meta_desc": "解释 MCP（Model Context Protocol）的概念、工作原理和使用场景，推荐热门的 MCP Server 开源项目和开发框架。",
        "keywords": "MCP Server,Model Context Protocol,MCP框架,AI工具调用,Agent工具,MCP开发",
        "content": """<p>MCP（Model Context Protocol）是 Anthropic 提出的开放标准，用于规范 AI 模型与外部工具、数据源之间的通信协议。2026 年，MCP 已经成为 AI Agent 生态的重要基础设施。</p>
<h2>MCP 是什么？</h2>
<p>MCP 定义了一套标准协议，让 AI 模型可以发现、调用和管理外部工具。类似于 USB 协议让不同设备可以即插即用，MCP 让 AI 应用可以无缝连接各种工具和服务。</p>
<h2>MCP 的核心概念</h2>
<ul>
<li><strong>MCP Server：</strong>提供工具（Tools）、资源（Resources）和提示（Prompts）的服务端</li>
<li><strong>MCP Client：</strong>连接 MCP Server 并调用工具的客户端（通常是 AI 应用）</li>
<li><strong>Tools：</strong>AI 可以调用的函数，如搜索、计算、文件操作</li>
<li><strong>Resources：</strong>AI 可以读取的数据源，如数据库、API</li>
</ul>
<h2>热门 MCP Server 项目</h2>
<p>拾品号导航收录了多个 MCP 相关项目：</p>
<ul>
<li><a href="/projects/cyanheads-mcp-ts-core/">mcp-ts-core</a> - TypeScript MCP Server 框架</li>
<li><a href="/projects/hyper-mcp-rs-hyper-mcp/">hyper-mcp</a> - Rust 高性能 MCP Server</li>
<li><a href="/projects/samanhappy-mcphub/">MCPHub</a> - 统一管理多个 MCP Server</li>
<li><a href="/projects/MCPJam-inspector/">MCP Inspector</a> - MCP Server 测试和调试工具</li>
</ul>
<h2>如何开发自己的 MCP Server？</h2>
<p>开发 MCP Server 的主要步骤：</p>
<ol>
<li>选择 SDK（TypeScript、Python 或 Rust）</li>
<li>定义工具的输入输出 schema</li>
<li>实现工具的具体逻辑</li>
<li>配置传输方式（stdio 或 HTTP/SSE）</li>
<li>在 AI 客户端中注册和测试</li>
</ol>""",
        "faq": [
            ("MCP 和 Function Calling 有什么区别？", "Function Calling 是 OpenAI 等厂商的专有实现，MCP 是开放标准。MCP 支持工具发现、资源管理和多传输方式，比 Function Calling 更通用。"),
            ("MCP Server 可以用什么语言开发？", "官方 SDK 支持 TypeScript 和 Python，社区有 Rust、Go 等实现。只要遵循 MCP 协议规范，任何语言都可以。"),
            ("哪些 AI 应用支持 MCP？", "Claude Desktop、Cursor、Windsurf、Cline 等主流 AI 编程工具都已支持 MCP。"),
        ],
    },
    {
        "slug": "github-project-evaluation-checklist",
        "title": "评估 GitHub 开源项目的完整清单：避免踩坑指南 - 拾品号导航",
        "h1": "评估 GitHub 开源项目的完整清单：避免踩坑指南",
        "meta_desc": "从 Star 质量、维护状态、文档、License、安全性、社区活跃度等维度，教你系统评估一个 GitHub 开源项目是否值得使用。",
        "keywords": "开源项目评估,GitHub项目选择,开源选型,开发者工具评估,开源License",
        "content": """<p>面对一个新开源项目，你是否只看 Star 数就决定使用？这样做风险很大。本文提供一个系统化的评估清单，帮助你判断一个 GitHub 项目是否真正值得依赖。</p>
<h2>评估维度清单</h2>
<h3>1. 维护状态</h3>
<ul>
<li>最近一次 commit 是什么时候？超过 3 个月没有更新要警惕</li>
<li>Open Issue 的数量和响应速度</li>
<li>是否有定期的版本发布</li>
</ul>
<h3>2. 社区活跃度</h3>
<ul>
<li>Contributor 数量（1 人的项目风险较高）</li>
<li>Discussions 或社区讨论是否活跃</li>
<li>是否有企业用户或知名公司在使用</li>
</ul>
<h3>3. 文档质量</h3>
<ul>
<li>README 是否清晰描述了项目用途和安装方式</li>
<li>是否有详细的使用文档或 API 文档</li>
<li>是否有示例代码或教程</li>
</ul>
<h3>4. License 和法律风险</h3>
<ul>
<li>是否明确标注了 License</li>
<li>License 是否允许你的使用场景（商用、修改、分发）</li>
<li>是否包含特殊的专利条款</li>
</ul>
<h3>5. 安全性</h3>
<ul>
<li>依赖的第三方库是否安全</li>
<li>是否有已知的安全漏洞（CVE）</li>
<li>代码中是否有可疑的网络请求或数据收集</li>
</ul>
<h3>6. 技术质量</h3>
<ul>
<li>代码风格是否一致</li>
<li>是否有测试覆盖</li>
<li>CI/CD 是否正常运行</li>
</ul>""",
        "faq": [
            ("Star 数多少才算靠谱？", "没有绝对标准。100+ Star 的项目通常有一定社区基础，1000+ Star 的项目通常更成熟。但更重要的是 Star 的增长趋势和社区活跃度。"),
            ("一个人维护的项目能用吗？", "可以用，但要做好风险评估。如果项目代码质量好、文档完善、你的使用场景不复杂，一个人维护的项目也是可以依赖的。但对于核心业务依赖，建议选择有多个维护者的项目。"),
            ("如何快速判断一个项目是否还在维护？", "看最近一次 commit 时间、最近一次 release 时间、Issue 响应速度。GitHub 仓库页面右侧会显示这些信息。"),
        ],
    },
    {
        "slug": "browser-automation-tools-comparison",
        "title": "浏览器自动化工具对比：Playwright vs Puppeteer vs Selenium - 拾品号导航",
        "h1": "浏览器自动化工具对比：Playwright vs Puppeteer vs Selenium",
        "meta_desc": "对比 2026 年主流浏览器自动化工具 Playwright、Puppeteer 和 Selenium 的性能、功能、易用性和适用场景。",
        "keywords": "浏览器自动化,Playwright,Puppeteer,Selenium,Web自动化,E2E测试,爬虫",
        "content": """<p>浏览器自动化是 Web 开发、测试和数据采集的重要技术。2026 年主流的浏览器自动化工具包括 Playwright、Puppeteer 和 Selenium。本文从多个维度对比这三款工具。</p>
<h2>工具概览</h2>
<h3>Playwright (Microsoft)</h3>
<p>微软推出的现代浏览器自动化框架，支持 Chromium、Firefox 和 WebKit。API 设计优秀，支持自动等待、网络拦截和多浏览器并行。2026 年已成为最受欢迎的选择。</p>
<h3>Puppeteer (Google)</h3>
<p>Google 维护的 Node.js 库，主要用于控制 Chrome/Chromium。轻量、快速，适合 Chrome 专属的自动化场景。</p>
<h3>Selenium</h3>
<p>老牌浏览器自动化工具，支持多语言（Java、Python、C#、Ruby）。生态最成熟，但 API 设计较旧，配置复杂。</p>
<h2>对比总结</h2>
<table>
<tr><th>维度</th><th>Playwright</th><th>Puppeteer</th><th>Selenium</th></tr>
<tr><td>浏览器支持</td><td>Chromium, Firefox, WebKit</td><td>Chrome/Chromium</td><td>所有主流浏览器</td></tr>
<tr><td>语言支持</td><td>JS/TS, Python, Java, C#</td><td>JS/TS</td><td>Java, Python, C#, Ruby, JS</td></tr>
<tr><td>自动等待</td><td>✅ 内置</td><td>❌ 需手动</td><td>❌ 需手动</td></tr>
<tr><td>网络拦截</td><td>✅ 强大</td><td>✅ 支持</td><td>⚠️ 有限</td></tr>
<tr><td>性能</td><td>优秀</td><td>优秀</td><td>一般</td></tr>
<tr><td>学习曲线</td><td>低</td><td>低</td><td>中</td></tr>
</table>
<h2>选择建议</h2>
<ul>
<li><strong>新项目：</strong>优先选 Playwright，功能最全面</li>
<li><strong>Chrome 专属：</strong>Puppeteer 更轻量</li>
<li><strong>已有 Selenium 项目：</strong>继续用 Selenium，无需迁移</li>
<li><strong>AI Agent 场景：</strong>Playwright 或专门的浏览器 Agent 框架</li>
</ul>""",
        "faq": [
            ("Playwright 能替代 Selenium 吗？", "对于新项目完全可以。Playwright 的 API 更现代、性能更好、支持自动等待。但如果已有大量 Selenium 测试代码，迁移成本需要评估。"),
            ("浏览器自动化可以用来做什么？", "E2E 测试、Web 爬虫、自动化表单填写、截图生成、性能监控、AI Agent 的浏览器操作等。"),
            ("哪个工具最适合 AI Agent？", "Playwright 是目前 AI Agent 浏览器自动化的首选，因为它的 API 设计更适合程序化控制，且支持多浏览器。"),
        ],
    },
    {
        "slug": "free-ai-tools-for-developers",
        "title": "开发者免费 AI 工具大全：2026 年实用清单 - 拾品号导航",
        "h1": "开发者免费 AI 工具大全：2026 年实用清单",
        "meta_desc": "整理 2026 年开发者可以免费使用的 AI 工具，覆盖代码生成、文档写作、设计、数据分析、部署等场景。",
        "keywords": "免费AI工具,开发者工具,AI代码生成,AI写作,免费开发者资源,AI工具推荐",
        "content": """<p>AI 工具正在降低软件开发的门槛。2026 年，开发者可以免费使用大量高质量的 AI 工具来提升效率。本文整理了最实用的免费 AI 工具清单。</p>
<h2>代码生成与编程</h2>
<ul>
<li><strong>GitHub Copilot Free：</strong>每月 2000 次代码补全和 50 次聊天</li>
<li><strong>Cursor Free：</strong>基础 AI 编辑功能免费</li>
<li><strong>Aider：</strong>开源终端编程助手，需要自带 API Key</li>
<li><strong>Continue：</strong>开源 VS Code AI 扩展</li>
</ul>
<h2>文档与写作</h2>
<ul>
<li><strong>ChatGPT Free：</strong>基础对话和写作辅助</li>
<li><strong>Claude Free：</strong>长文本理解和写作</li>
<li><strong>Notion AI：</strong>Notion 内置的 AI 写作助手（有限免费额度）</li>
</ul>
<h2>设计与图片</h2>
<ul>
<li><strong>Figma：</strong>免费的设计工具，AI 功能有限免费</li>
<li><strong>Canva：</strong>免费的在线设计工具，支持 AI 生成图片</li>
<li><strong>Stable Diffusion：</strong>开源图片生成模型，可本地运行</li>
</ul>
<h2>数据分析</h2>
<ul>
<li><strong>Jupyter Notebook：</strong>免费的交互式编程环境</li>
<li><strong>Google Colab：</strong>免费的云端 Jupyter 环境，支持 GPU</li>
<li><strong>Observable：</strong>免费的数据可视化笔记本</li>
</ul>
<h2>部署与运维</h2>
<ul>
<li><strong>Cloudflare Pages：</strong>免费静态网站托管</li>
<li><strong>Vercel：</strong>免费的前端部署平台</li>
<li><strong>Railway：</strong>有免费额度的全栈部署平台</li>
</ul>""",
        "faq": [
            ("免费 AI 工具有什么限制？", "通常限制在使用次数、模型能力、并发数和功能范围。对于个人学习和小项目完全够用。"),
            ("AI 生成的代码有版权问题吗？", "这是一个法律灰色地带。不同 AI 工具的 Terms of Service 对生成内容的版权归属有不同规定。建议在商业项目中谨慎使用。"),
            ("如何选择适合自己的 AI 工具？", "先明确自己的需求场景（写代码、写文档、设计等），然后试用几款免费工具，选择最符合自己工作流的。"),
        ],
    },
    {
        "slug": "best-self-hosted-tools-2026",
        "title": "2026 年最佳自部署开源工具推荐 - 拾品号导航",
        "h1": "2026 年最佳自部署开源工具推荐",
        "meta_desc": "推荐适合自部署的开源工具，覆盖文件管理、笔记、项目管理、监控、CMS 等场景，帮你摆脱 SaaS 依赖。",
        "keywords": "自部署,Self-hosted,开源工具,Docker部署,私有化部署,数据自主",
        "content": """<p>自部署（Self-hosted）开源工具让你完全掌控自己的数据和服务。2026 年，Docker 和一键部署脚本让自部署变得前所未有的简单。本文推荐最值得自部署的开源工具。</p>
<h2>为什么要自部署？</h2>
<ul>
<li><strong>数据隐私：</strong>数据完全在自己控制之下</li>
<li><strong>成本控制：</strong>避免 SaaS 的订阅费用</li>
<li><strong>定制能力：</strong>可以根据需求修改代码</li>
<li><strong>无供应商锁定：</strong>不依赖第三方服务的可用性</li>
</ul>
<h2>推荐的自部署工具</h2>
<h3>文件管理</h3>
<ul>
<li><strong>Nextcloud：</strong>功能最全的自部署云盘，支持文件同步、日历、联系人</li>
<li><strong>Filebrowser：</strong>轻量级文件管理界面</li>
</ul>
<h3>笔记和知识库</h3>
<ul>
<li><strong>Affine：</strong>开源的 Notion 替代，支持文档、白板和数据库</li>
<li><strong>Outline：</strong>团队知识库工具，Markdown 原生</li>
</ul>
<h3>项目管理</h3>
<ul>
<li><strong>Plane：</strong>开源的 Jira/Linear 替代</li>
<li><strong>Appsmith：</strong>低代码内部工具构建平台</li>
</ul>
<h3>监控</h3>
<ul>
<li><strong>Uptime Kuma：</strong>简洁美观的网站监控工具</li>
<li><strong>Grafana：</strong>数据可视化和监控仪表板</li>
</ul>
<h3>CMS</h3>
<ul>
<li><strong>Strapi：</strong>最流行的开源无头 CMS</li>
<li><strong>ApostropheCMS：</strong>基于 Node.js 的 CMS</li>
</ul>""",
        "faq": [
            ("自部署需要什么技术基础？", "需要基本的 Linux 命令行操作、Docker 基础知识和网络配置概念。大部分工具都提供 Docker Compose 一键部署。"),
            ("自部署的服务器成本多少？", "一台最低配置的 VPS（1核1G）每月约 5 美元，可以运行多个轻量工具。如果需要更多资源，可以按需升级。"),
            ("自部署的数据安全如何保障？", "定期备份、使用 HTTPS、保持系统更新、限制访问权限是基本的安全措施。建议使用 Cloudflare Tunnel 等工具安全暴露服务。"),
        ],
    },
    {
        "slug": "ai-agent-use-cases",
        "title": "AI Agent 能做什么？10 个实际应用场景 - 拾品号导航",
        "h1": "AI Agent 能做什么？10 个实际应用场景",
        "meta_desc": "展示 AI Agent 在编程、客服、数据分析、自动化运维、内容创作等领域的实际应用案例，帮你理解 Agent 的真实价值。",
        "keywords": "AI Agent应用,智能体场景,AI自动化,Agent用例,AI编程助手,AI客服",
        "content": """<p>AI Agent（智能体）不只是聊天机器人的升级版。2026 年，Agent 已经在多个领域展现出真正的实用价值。本文列举 10 个 AI Agent 的实际应用场景。</p>
<h2>1. 编程 Agent</h2>
<p>自动编写代码、运行测试、修复 bug、执行重构。代表工具：<a href="/projects/anthropics-claude-code/">Claude Code</a>、Cursor Agent。这是目前最成熟的 Agent 应用场景。</p>
<h2>2. 客服 Agent</h2>
<p>理解用户问题、查询知识库、执行操作（退款、改地址等）、自动升级到人工。比传统聊天机器人更智能，能处理复杂多轮对话。</p>
<h2>3. 数据分析 Agent</h2>
<p>接收自然语言查询，自动生成 SQL、执行分析、生成图表和报告。让非技术人员也能进行复杂的数据分析。</p>
<h2>4. 运维 Agent</h2>
<p>监控系统状态、自动处理告警、执行故障排查、生成运维报告。减少 on-call 工程师的负担。</p>
<h2>5. 内容创作 Agent</h2>
<p>根据主题自动撰写文章、生成社交媒体内容、翻译和本地化。支持品牌调性和风格指南。</p>
<h2>6. 浏览器自动化 Agent</h2>
<p>模拟人类操作浏览器，完成表单填写、数据采集、网站测试等任务。结合 <a href="/projects/steel-dev-steel-browser/">Steel Browser</a> 等工具实现可控的浏览器环境。</p>
<h2>7. 研究 Agent</h2>
<p>自动搜索信息、阅读论文、整理摘要、生成研究报告。适合学术研究和市场调研。</p>
<h2>8. 交易和金融 Agent</h2>
<p>监控市场数据、执行交易策略、管理投资组合。需要严格的风控和合规机制。</p>
<h2>9. 教育 Agent</h2>
<p>个性化教学、自适应练习、作业批改、学习路径规划。让每个学生都有专属的 AI 导师。</p>
<h2>10. 多 Agent 协作</h2>
<p>多个 Agent 分工协作，完成更复杂的任务。例如一个 Agent 负责研究，一个负责编码，一个负责测试。这是 Agent 技术的前沿方向。</p>""",
        "faq": [
            ("AI Agent 和 RPA 有什么区别？", "RPA（机器人流程自动化）是基于固定规则的自动化，只能执行预定义的操作。AI Agent 具有理解和推理能力，可以处理未预见的情况。"),
            ("AI Agent 安全吗？", "安全是 Agent 部署的核心挑战。需要设置权限边界、审批流程、日志审计和人工监督机制。不要让 Agent 在没有约束的情况下执行高风险操作。"),
            ("个人开发者如何开始使用 AI Agent？", "从编程 Agent 开始（如 Claude Code），体验 Agent 在实际开发中的价值。然后逐步探索其他场景。"),
        ],
    },
    {
        "slug": "how-to-contribute-to-open-source",
        "title": "如何参与开源项目？新手完整指南 - 拾品号导航",
        "h1": "如何参与开源项目？新手完整指南",
        "meta_desc": "从选择项目、阅读代码、提交 Issue、发送 PR 到成为 Contributor 的完整流程，帮助开源新手迈出第一步。",
        "keywords": "开源贡献,参与开源,GitHub PR,开源新手,Contributor,开源社区",
        "content": """<p>参与开源项目是提升技术能力、建立个人品牌和结识优秀开发者的最佳方式之一。但很多新手不知道如何开始。本文提供一个完整的入门指南。</p>
<h2>为什么要参与开源？</h2>
<ul>
<li><strong>提升技术：</strong>阅读优秀项目的源码是最好的学习方式</li>
<li><strong>建立履历：</strong>GitHub 贡献记录是技术能力的有力证明</li>
<li><strong>结识人脉：</strong>与全球优秀开发者协作</li>
<li><strong>回馈社区：</strong>使用了那么多开源工具，贡献一份力量</li>
</ul>
<h2>如何找到适合贡献的项目？</h2>
<ol>
<li>从你日常使用的工具开始</li>
<li>在 GitHub 搜索 <code>good first issue</code> 标签</li>
<li>浏览 <a href="/trending/">拾品号涨星榜</a> 找到感兴趣的项目</li>
<li>关注项目的 CONTRIBUTING.md 文件</li>
</ol>
<h2>贡献的类型</h2>
<p>代码贡献不是唯一方式：</p>
<ul>
<li><strong>文档改进：</strong>修正错别字、补充说明、翻译文档</li>
<li><strong>Bug 报告：</strong>提交详细的 Issue 复现步骤</li>
<li><strong>功能建议：</strong>提出有建设性的 Feature Request</li>
<li><strong>代码审查：</strong>Review 其他人的 PR</li>
<li><strong>社区支持：</strong>回答新手问题</li>
</ul>
<h2>提交 PR 的流程</h2>
<ol>
<li>Fork 项目仓库</li>
<li>创建新分支（不要在 main 上直接改）</li>
<li>做出修改并写清楚 commit message</li>
<li>推送到你的 Fork</li>
<li>创建 Pull Request，描述你做了什么和为什么</li>
<li>等待 Review 并根据反馈修改</li>
</ol>""",
        "faq": [
            ("不会写代码也能参与开源吗？", "完全可以。文档翻译、Bug 报告、设计建议、社区支持等都是有价值的贡献方式。"),
            ("PR 被拒绝了怎么办？", "这是正常现象。阅读维护者的反馈，理解拒绝的原因，改进后重新提交。不要把拒绝当作人身攻击。"),
            ("如何选择第一个贡献的项目？", "选择你日常使用且感兴趣的项目，从简单的 Issue（如 good first issue）开始。不要一开始就挑太难的任务。"),
        ],
    },
    {
        "slug": "devops-tools-2026",
        "title": "2026 年 DevOps 工具链推荐：从代码到部署 - 拾品号导航",
        "h1": "2026 年 DevOps 工具链推荐：从代码到部署",
        "meta_desc": "整理 2026 年最值得使用的 DevOps 工具，覆盖版本控制、CI/CD、容器化、监控、日志管理等环节。",
        "keywords": "DevOps工具,CI/CD,Docker,Kubernetes,监控,日志管理,部署工具",
        "content": """<p>DevOps 工具链是现代软件开发的基础设施。2026 年，AI 正在改变 DevOps 的工作方式，但基础工具仍然不可或缺。本文整理从代码到部署的完整工具链推荐。</p>
<h2>版本控制与协作</h2>
<ul>
<li><strong>GitHub：</strong>最流行的代码托管平台，CI/CD（GitHub Actions）、项目管理一体化</li>
<li><strong>GitLab：</strong>功能最全的 DevOps 平台，支持自部署</li>
</ul>
<h2>CI/CD</h2>
<ul>
<li><strong>GitHub Actions：</strong>与 GitHub 深度集成，YAML 配置简单</li>
<li><strong>Dagger：</strong>用代码定义 CI/CD 流程，可移植性强</li>
<li><strong>Woodpecker CI：</strong>轻量级的开源 CI/CD 引擎</li>
</ul>
<h2>容器与编排</h2>
<ul>
<li><strong>Docker：</strong>容器化标准，几乎所有项目都在用</li>
<li><strong>Kubernetes：</strong>容器编排标准，适合大规模部署</li>
<li><strong>Docker Compose：</strong>单机多容器编排，适合开发和小规模部署</li>
</ul>
<h2>监控与可观测性</h2>
<ul>
<li><strong>Grafana：</strong>数据可视化和监控仪表板</li>
<li><strong>Prometheus：</strong>指标收集和告警</li>
<li><strong>Uptime Kuma：</strong>简洁的网站监控</li>
<li><strong>Sentry：</strong>错误追踪和性能监控</li>
</ul>
<h2>日志管理</h2>
<ul>
<li><strong>Loki：</strong>Grafana 生态的日志聚合系统</li>
<li><strong>Vector：</strong>高性能的日志收集和转发</li>
</ul>
<h2>基础设施即代码</h2>
<ul>
<li><strong>Terraform：</strong>多云基础设施管理标准</li>
<li><strong>Pulumi：</strong>用编程语言定义基础设施</li>
<li><strong>Ansible：</strong>配置管理和自动化</li>
</ul>""",
        "faq": [
            ("小型团队需要完整的 DevOps 工具链吗？", "不需要。小型团队可以用 GitHub Actions + Docker + Vercel/Cloudflare Pages 覆盖大部分需求，保持简单。"),
            ("DevOps 和 SRE 有什么区别？", "DevOps 是一种文化和实践，强调开发和运维的协作。SRE（Site Reliability Engineering）是 Google 提出的实践方法，更侧重于系统可靠性和自动化。"),
            ("AI 如何改变 DevOps？", "AI 正在帮助自动化故障排查、智能告警、自动生成运维脚本和优化资源分配。但基础的 DevOps 实践仍然是必要的。"),
        ],
    },
]

def esc(s):
    return html.escape(str(s or ""), quote=True)

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
    guides_root = ROOT / "guides"
    guides_root.mkdir(exist_ok=True)

    all_slugs = []

    for guide in GUIDES:
        slug = guide["slug"]
        canonical = f"{BASE}/guides/{slug}.html"
        all_slugs.append((slug, guide["title"], guide["meta_desc"]))

        # BreadcrumbList
        breadcrumbs = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "首页", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "使用指南", "item": BASE + "/guides/"},
                {"@type": "ListItem", "position": 3, "name": guide["h1"]},
            ]
        }

        # FAQPage
        faq_entities = []
        for q, a in guide.get("faq", []):
            faq_entities.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            })
        faq_jsonld = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities,
        }

        # Article JSON-LD
        article_jsonld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": guide["h1"],
            "description": guide["meta_desc"],
            "url": canonical,
            "publisher": {"@type": "Organization", "name": "拾品号导航", "url": BASE},
            "mainEntityOfPage": canonical,
        }

        # FAQ HTML
        faq_html = ""
        if guide.get("faq"):
            items = "".join(f'<details class="faq-item" open><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in guide["faq"])
            faq_html = f'<section class="faq-panel"><h2>常见问题</h2>{items}</section>'

        body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">Guide</span>
      <h1>{esc(guide["h1"])}</h1>
      <p class="daily-line">拾品号导航使用指南 · 覆盖开源项目选型、AI 工具使用和开发者资源</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <nav class="breadcrumb-nav" aria-label="面包屑导航">
        <a href="/">首页</a> &gt; <a href="/guides/">使用指南</a> &gt; <span>{esc(guide["h1"])}</span>
      </nav>
      <article class="guide-article">
        {guide["content"]}
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

        out_path = guides_root / f"{slug}.html"
        out_path.write_text(page_shell(guide["title"], guide["meta_desc"], canonical, body, [breadcrumbs, article_jsonld, faq_jsonld], guide.get("keywords", "")), encoding="utf-8")
        print(f"  Generated: /guides/{slug}.html")

    # Update guides index
    links = "".join(f'<article class="trend-card"><h2><a href="/guides/{s}.html">{esc(t)}</a></h2><p>{esc(d)}</p></article>' for s, t, d in all_slugs)

    # Also keep existing guides
    existing = [
        ("github-project-selection-checklist", "GitHub 项目选择清单"),
        ("how-to-build-ai-search-friendly-directory", "如何构建 AI 搜索友好的目录"),
        ("what-makes-a-github-project-worth-using", "什么样的 GitHub 项目值得使用"),
        ("open-source-project-monetization", "开源项目商业化"),
        ("how-to-evaluate-ai-agent-frameworks", "如何评估 AI Agent 框架"),
        ("free-ai-coding-agents-freebuff-codebuff", "免费 AI 编程助手"),
    ]
    for es, et in existing:
        links += f'<article class="trend-card"><h2><a href="/guides/{es}.html">{esc(et)}</a></h2></article>'

    index_body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">Guides</span>
      <h1>开发者使用指南</h1>
      <p>拾品号导航整理的开发者指南，覆盖 AI 工具选型、开源项目评估、建站部署和 DevOps 实践。</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <div class="trend-grid">{links}</div>
    </section></section>"""

    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "使用指南"},
        ]
    }
    (guides_root / "index.html").write_text(page_shell(
        "开发者使用指南 - 拾品号导航",
        "拾品号导航整理的开发者指南，覆盖 AI 工具选型、开源项目评估、建站部署和 DevOps 实践。",
        f"{BASE}/guides/",
        index_body,
        [breadcrumbs],
    ), encoding="utf-8")

    print(f"\nGenerated {len(GUIDES)} guide articles + updated index")

if __name__ == "__main__":
    main()
