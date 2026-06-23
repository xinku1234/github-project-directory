#!/usr/bin/env python3
"""Generate comparison and alternative pages targeting high-volume search queries.

These pages directly match search intent like "X alternatives", "X vs Y",
"best X for Y" — the queries developers actually type into Google.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://daohang.bot.cd"

COMPARISON_PAGES = [
    {
        "slug": "cursor-vs-windsurf-vs-claude-code",
        "title": "Cursor vs Windsurf vs Claude Code：2026 年 AI 编程工具终极对比 - 拾品号导航",
        "h1": "Cursor vs Windsurf vs Claude Code：2026 年 AI 编程工具终极对比",
        "meta_desc": "深度对比 Cursor、Windsurf 和 Claude Code 三款顶级 AI 编程工具的架构、功能、价格和适用场景，帮你选到最适合的 AI 编码助手。",
        "keywords": "Cursor vs Windsurf,Claude Code对比,AI编程工具对比,Cursor怎么样,Windsurf好用吗",
        "content": """
<p>Cursor、Windsurf 和 Claude Code 是 2026 年最受关注的三款 AI 编程工具。它们各有特色，适合不同类型的开发者。本文从多个维度深度对比，帮你做出选择。</p>

<h2>核心差异一览</h2>
<table>
<tr><th>维度</th><th>Cursor</th><th>Windsurf</th><th>Claude Code</th></tr>
<tr><td>类型</td><td>IDE（基于 VS Code）</td><td>IDE（基于 VS Code）</td><td>终端 CLI 工具</td></tr>
<tr><td>核心模型</td><td>多模型可选</td><td>多模型可选</td><td>Claude 系列</td></tr>
<tr><td>Agent 模式</td><td>✅ 完整</td><td>✅ Cascade</td><td>✅ 原生</td></tr>
<tr><td>多文件编辑</td><td>✅ 强大</td><td>✅ 支持</td><td>✅ 强大</td></tr>
<tr><td>终端集成</td><td>✅ 内置</td><td>✅ 内置</td><td>✅ 原生终端</td></tr>
<tr><td>价格</td><td>$20/月 Pro</td><td>$15/月 Pro</td><td>按 API 用量</td></tr>
<tr><td>适合人群</td><td>全栈开发者</td><td>注重流畅体验</td><td>终端党/高级用户</td></tr>
</table>

<h2>Cursor 详细分析</h2>
<p>Cursor 是基于 VS Code 的 AI-first 编辑器，由 Anysphere 开发。它的核心优势在于：</p>
<ul>
<li><strong>多模型支持：</strong>可以在 GPT-4o、Claude、Gemini 等模型之间切换</li>
<li><strong>代码库理解：</strong>能理解整个项目的上下文，不只是当前文件</li>
<li><strong>Agent 模式：</strong>可以自主执行多步骤任务，包括运行命令、搜索文件</li>
<li><strong>Tab 补全：</strong>最智能的代码补全体验之一</li>
</ul>
<p>适合需要丰富 IDE 功能、喜欢图形界面、团队协作的开发者。</p>

<h2>Windsurf 详细分析</h2>
<p>Windsurf（原 Codeium）强调流式编辑体验和 Cascade 多步骤工作流：</p>
<ul>
<li><strong>Cascade：</strong>AI 自动规划和执行多步骤操作，流畅度极高</li>
<li><strong>上下文感知：</strong>自动理解项目结构和依赖关系</li>
<li><strong>价格优势：</strong>$15/月的 Pro 计划比 Cursor 便宜</li>
<li><strong>快速迭代：</strong>功能更新频繁，社区活跃</li>
</ul>
<p>适合预算敏感、喜欢流畅编辑体验、不需要太多高级定制的开发者。</p>

<h2>Claude Code 详细分析</h2>
<p>Claude Code 是 Anthropic 推出的终端编程助手，与其他两款有本质不同：</p>
<ul>
<li><strong>终端原生：</strong>直接在命令行运行，不需要 GUI</li>
<li><strong>全栈能力：</strong>可以读写文件、运行命令、管理 Git、执行测试</li>
<li><strong>深度理解：</strong>能理解整个代码库的架构和依赖</li>
<li><strong>透明操作：</strong>所有操作都在终端可见，方便审计</li>
</ul>
<p>适合喜欢终端工作流、需要深度代码理解、高级开发者和 DevOps 工程师。</p>

<h2>如何选择？</h2>
<ul>
<li><strong>选 Cursor：</strong>如果你习惯 VS Code，需要丰富的 IDE 功能，团队环境</li>
<li><strong>选 Windsurf：</strong>如果预算有限，喜欢流畅的编辑体验，不需要太多定制</li>
<li><strong>选 Claude Code：</strong>如果你是终端用户，需要深度代码理解，高级开发者</li>
<li><strong>组合使用：</strong>很多开发者同时使用 IDE 和 CLI 工具，各取所长</li>
</ul>
""",
        "faq": [
            ("Cursor 和 Windsurf 哪个更好？", "没有绝对的好坏。Cursor 功能更全面、生态更成熟，Windsurf 价格更低、编辑体验更流畅。建议两者都试用免费版，选适合自己工作流的。"),
            ("Claude Code 比 IDE 工具好在哪？", "Claude Code 的优势在于终端原生、操作透明、深度代码理解。它不会隐藏操作细节，所有文件读写和命令执行都在终端可见，适合需要精确控制的高级用户。"),
            ("这些工具可以免费使用吗？", "Cursor 和 Windsurf 都有免费版（功能和次数有限）。Claude Code 需要 Anthropic API Key，按使用量付费。"),
        ],
    },
    {
        "slug": "cursor-alternatives",
        "title": "2026 年 Cursor 最佳替代品：10 款 AI 编程工具推荐 - 拾品号导航",
        "h1": "2026 年 Cursor 最佳替代品：10 款 AI 编程工具推荐",
        "meta_desc": "如果你不想用 Cursor 或需要更多选择，这 10 款 AI 编程工具是 2026 年最好的替代方案，涵盖免费和开源选项。",
        "keywords": "Cursor替代品,Cursor alternatives,AI编程工具,AI代码编辑器,Cursor免费替代,开源编程助手",
        "content": """
<p>Cursor 是目前最受欢迎的 AI 编程工具之一，但并非唯一选择。无论你是因为价格、隐私、平台限制还是个人偏好，都有很多优秀的替代方案。本文推荐 10 款 2026 年最值得关注的 Cursor 替代品。</p>

<h2>1. Windsurf</h2>
<p>最直接的 Cursor 竞品，同样基于 VS Code，但价格更低（$15/月 vs $20/月）。Cascade 工作流是其亮点，编辑体验流畅。适合预算敏感的开发者。</p>

<h2>2. Claude Code</h2>
<p>Anthropic 的终端编程助手，不需要 GUI，直接在命令行工作。适合终端用户和需要深度代码理解的高级开发者。</p>

<h2>3. GitHub Copilot</h2>
<p>GitHub 官方的 AI 编程助手，直接集成在 VS Code 和 JetBrains 中。有免费额度，适合已在 GitHub 生态中的开发者。</p>

<h2>4. Aider</h2>
<p>开源的终端编程助手，支持多种 LLM（GPT-4o、Claude、本地模型）。完全免费，需要自带 API Key。<a href="/projects/paul-gauthier-aider/">查看项目 →</a></p>

<h2>5. Continue</h2>
<p>开源的 VS Code AI 扩展，支持多模型和自定义配置。适合不想被锁定在某个 AI 服务商的开发者。</p>

<h2>6. Cline</h2>
<p>VS Code 扩展形式的 AI 编程助手，支持 Claude、GPT 等模型，有 Agent 模式。开源且活跃。</p>

<h2>7. OpenHands</h2>
<p>开源的 AI 软件开发 Agent，可以自主编写代码、运行测试、修复 Bug。适合需要全自动化开发流程的场景。</p>

<h2>8. Zed</h2>
<p>高性能的代码编辑器，内置 AI 功能。用 Rust 编写，速度极快。适合追求编辑器性能的开发者。</p>

<h2>9. JetBrains AI</h2>
<p>JetBrains IDE 的原生 AI 功能，深度集成在 IntelliJ、PyCharm 等工具中。适合 JetBrains 用户。</p>

<h2>10. Tabnine</h2>
<p>老牌 AI 代码补全工具，支持本地模型部署，注重代码隐私。适合企业用户和对隐私有要求的团队。</p>

<h2>选择建议</h2>
<p>没有「最好」的工具，只有「最适合」你的工具。建议：</p>
<ul>
<li>先试用 2-3 款的免费版</li>
<li>在真实项目中测试一周</li>
<li>关注：代码质量、响应速度、上下文理解、隐私政策</li>
</ul>
""",
        "faq": [
            ("有没有完全免费的 Cursor 替代品？", "有。Aider、Continue、Cline 都是免费开源的，需要自带 API Key。GitHub Copilot 也有免费额度。"),
            ("开源的 AI 编程工具好用吗？", "2026 年的开源工具已经非常成熟。Aider 和 Continue 在社区评价很高，功能不输商业产品。"),
            ("企业用哪个更安全？", "Tabnine 支持本地部署，代码不出企业网络。Cursor 和 Windsurf 也有企业版，提供隐私保护和审计功能。"),
        ],
    },
    {
        "slug": "best-ai-tools-for-programming",
        "title": "2026 年最好的 AI 编程工具完整指南 - 拾品号导航",
        "h1": "2026 年最好的 AI 编程工具完整指南",
        "meta_desc": "从代码补全到全栈开发，覆盖 2026 年最实用的 AI 编程工具，包括 Cursor、Claude Code、Copilot、Aider 等，按使用场景推荐。",
        "keywords": "最好的AI编程工具,AI编程工具推荐,AI写代码工具,2026编程工具,AI代码生成器",
        "content": """
<p>AI 编程工具已经从「可选的效率提升」变成了「必备的开发工具」。2026 年，几乎每个主流编辑器和 IDE 都内置了 AI 功能。本文按使用场景推荐最实用的 AI 编程工具。</p>

<h2>按场景推荐</h2>

<h3>日常编码（代码补全 + 聊天）</h3>
<ul>
<li><strong>首选：</strong>Cursor 或 Windsurf — 最完整的 AI IDE 体验</li>
<li><strong>免费：</strong>GitHub Copilot Free — 每月 2000 次补全</li>
<li><strong>开源：</strong>Continue — VS Code 扩展，支持多模型</li>
</ul>

<h3>终端编程（命令行工作流）</h3>
<ul>
<li><strong>首选：</strong>Claude Code — 最强大的终端 AI 助手</li>
<li><strong>开源：</strong>Aider — 支持多种 LLM，完全免费</li>
<li><strong>轻量：</strong>MiniCode — 类似 Claude Code 的轻量替代</li>
</ul>

<h3>全栈开发（前后端 + 部署）</h3>
<ul>
<li><strong>首选：</strong>Cursor Agent 模式 — 能处理完整的开发流程</li>
<li><strong>替代：</strong>Windsurf Cascade — 流畅的多步骤工作流</li>
</ul>

<h3>代码审查和重构</h3>
<ul>
<li><strong>首选：</strong>Claude Code — 深度代码理解能力最强</li>
<li><strong>替代：</strong>Cursor — 支持 @codebase 全项目理解</li>
</ul>

<h3>学习和探索代码库</h3>
<ul>
<li><strong>首选：</strong>Cursor — 代码库问答功能直观</li>
<li><strong>替代：</strong>GitHub Copilot Chat — 直接在 GitHub 上提问</li>
</ul>

<h3>自动化和脚本</h3>
<ul>
<li><strong>首选：</strong>Claude Code — 能直接执行 shell 命令</li>
<li><strong>替代：</strong>Aider — 终端原生，适合脚本化</li>
</ul>

<h2>免费 vs 付费</h2>
<table>
<tr><th>工具</th><th>免费额度</th><th>付费价格</th></tr>
<tr><td>GitHub Copilot</td><td>2000 次补全/月</td><td>$10/月</td></tr>
<tr><td>Cursor</td><td>基础功能免费</td><td>$20/月 Pro</td></tr>
<tr><td>Windsurf</td><td>基础功能免费</td><td>$15/月 Pro</td></tr>
<tr><td>Claude Code</td><td>无（按 API 用量）</td><td>约 $5-20/月</td></tr>
<tr><td>Aider</td><td>完全免费</td><td>自带 API Key</td></tr>
<tr><td>Continue</td><td>完全免费</td><td>自带 API Key</td></tr>
</table>

<h2>2026 年趋势</h2>
<p>AI 编程工具正在从「代码补全」进化为「编程智能体」。新一代工具不仅能写代码，还能理解需求、规划任务、执行测试和部署应用。MCP（Model Context Protocol）等标准的出现也让工具之间的互操作性更强。</p>
""",
        "faq": [
            ("AI 编程工具会取代程序员吗？", "不会。AI 工具是效率倍增器，帮助开发者减少重复工作。需要创造力、架构设计和业务理解的工作仍然需要人类。"),
            ("初学者应该用 AI 编程工具吗？", "可以，但要注意不要过度依赖。AI 工具可以帮助理解代码和学习新概念，但初学者应该先理解基础原理。"),
            ("哪个 AI 编程工具最值得付费？", "如果你每天写代码，Cursor 或 Windsurf 的 Pro 计划是最值得的投资。$15-20/月可以显著提升开发效率。"),
        ],
    },
    {
        "slug": "langchain-alternatives",
        "title": "LangChain 替代品：2026 年最佳 AI 框架对比 - 拾品号导航",
        "h1": "LangChain 替代品：2026 年最佳 AI 框架对比",
        "meta_desc": "LangChain 太重了？对比 LlamaIndex、Haystack、DSPy、Agno 等轻量级 AI 框架，找到最适合你项目的替代方案。",
        "keywords": "LangChain替代品,LangChain alternatives,AI框架对比,LlamaIndex,DSPy,轻量AI框架",
        "content": """
<p>LangChain 是最流行的 AI 应用框架，但也因为抽象层过多、学习曲线陡峭而受到批评。如果你觉得 LangChain 太重或不适合你的项目，有很多优秀的替代方案。</p>

<h2>为什么要找 LangChain 替代品？</h2>
<ul>
<li><strong>抽象过度：</strong>LangChain 的抽象层可能让简单任务变得复杂</li>
<li><strong>学习成本高：</strong>API 变化频繁，文档有时跟不上</li>
<li><strong>性能开销：</strong>多层抽象带来额外的性能开销</li>
<li><strong>依赖锁定：</strong>深度使用后难以迁移到其他框架</li>
</ul>

<h2>替代方案对比</h2>

<h3>LlamaIndex</h3>
<p>专注于数据连接和检索增强生成（RAG）。如果你的主要需求是让 LLM 理解你的数据，LlamaIndex 比 LangChain 更专注、更高效。</p>

<h3>Haystack</h3>
<p>deepset 推出的端到端 NLP 框架，专注于搜索和问答管道。架构清晰、文档完善、适合生产环境。</p>

<h3>DSPy</h3>
<p>斯坦福推出的声明式 LM 编程框架。不写 prompt，写「签名」和「模块」，让框架自动优化。适合研究和需要可复现性的场景。</p>

<h3>Agno</h3>
<p>轻量级 AI Agent 框架，API 简洁，上手快。适合不需要复杂编排、希望快速验证想法的开发者。</p>

<h3>直接使用 SDK</h3>
<p>对于简单场景，直接使用 OpenAI SDK 或 Anthropic SDK 可能比任何框架都简单。不要为了用框架而用框架。</p>

<h2>选择建议</h2>
<ul>
<li><strong>RAG 场景：</strong>LlamaIndex</li>
<li><strong>搜索/问答：</strong>Haystack</li>
<li><strong>研究/可复现：</strong>DSPy</li>
<li><strong>快速原型：</strong>Agno 或直接用 SDK</li>
<li><strong>复杂编排：</strong>LangGraph（LangChain 的图式子项目）</li>
</ul>
""",
        "faq": [
            ("LangChain 还值得学吗？", "值得。LangChain 生态最大、社区最活跃、工作机会最多。但了解替代方案也很重要，不同项目可能需要不同的工具。"),
            ("哪个框架最适合生产环境？", "Haystack 和 LangGraph 都有良好的生产实践。选择取决于你的具体需求和团队技术栈。"),
            ("直接用 OpenAI API 不行吗？", "完全可以。对于简单场景，直接用 API 比用框架更简单、更可控。框架的价值在于复杂场景下的抽象和复用。"),
        ],
    },
    {
        "slug": "self-hosted-notion-alternatives",
        "title": "自部署 Notion 替代品：2026 年开源笔记和知识库工具 - 拾品号导航",
        "h1": "自部署 Notion 替代品：2026 年开源笔记和知识库工具",
        "meta_desc": "不想把笔记存在别人的服务器上？这些开源工具可以自部署，功能不输 Notion，数据完全在你手里。",
        "keywords": "Notion替代品,自部署笔记,开源知识库,Affine,Outline,Obsidian,自部署CMS",
        "content": """
<p>Notion 很好用，但数据存在别人的服务器上。如果你在意数据隐私、想要更多定制能力、或者不想被 SaaS 订阅绑定，自部署的开源替代品是更好的选择。</p>

<h2>最佳开源替代品</h2>

<h3>Affine</h3>
<p>最接近 Notion 体验的开源替代品。支持文档、白板和数据库，界面美观，功能丰富。可以自部署也可以用他们的云服务。</p>

<h3>Outline</h3>
<p>团队知识库工具，Markdown 原生，搜索功能强大。界面简洁现代，适合团队文档和 Wiki。自部署简单（Docker 一键部署）。</p>

<h3>AppFlowy</h3>
<p>用 Rust 和 Flutter 构建的开源 Notion 替代。性能优秀，支持离线使用。适合个人和小团队。</p>

<h3>SiYuan (思源笔记)</h3>
<p>国产开源笔记工具，支持块级引用、双向链接、所见即所得编辑。数据存储在本地，支持端到端加密同步。</p>

<h3>HedgeDoc</h3>
<p>实时协作的 Markdown 编辑器，适合团队协作写文档。自部署简单，支持实时多人编辑。</p>

<h3>Wiki.js</h3>
<p>功能丰富的 Wiki 引擎，支持多种编辑器（Markdown、所见即所得）、多语言、权限管理。适合构建企业知识库。</p>

<h2>对比表</h2>
<table>
<tr><th>工具</th><th>Notion 相似度</th><th>自部署难度</th><th>特色功能</th></tr>
<tr><td>Affine</td><td>⭐⭐⭐⭐⭐</td><td>中等</td><td>白板 + 数据库</td></tr>
<tr><td>Outline</td><td>⭐⭐⭐⭐</td><td>简单</td><td>团队 Wiki</td></tr>
<tr><td>AppFlowy</td><td>⭐⭐⭐⭐</td><td>简单</td><td>离线优先</td></tr>
<tr><td>思源笔记</td><td>⭐⭐⭐</td><td>简单</td><td>块级引用</td></tr>
<tr><td>HedgeDoc</td><td>⭐⭐</td><td>简单</td><td>实时协作</td></tr>
<tr><td>Wiki.js</td><td>⭐⭐⭐</td><td>中等</td><td>企业 Wiki</td></tr>
</table>

<h2>如何选择？</h2>
<ul>
<li><strong>想要最像 Notion：</strong>Affine</li>
<li><strong>团队知识库：</strong>Outline 或 Wiki.js</li>
<li><strong>个人笔记：</strong>思源笔记或 AppFlowy</li>
<li><strong>实时协作：</strong>HedgeDoc</li>
</ul>
""",
        "faq": [
            ("自部署笔记工具需要什么服务器？", "一台最低配置的 VPS（1核1G）就够运行大部分笔记工具。如果用户多或数据量大，建议 2核4G。"),
            ("数据迁移方便吗？", "大部分工具支持 Markdown 导入导出。从 Notion 迁出可以用 Notion 的导出功能，然后导入到新工具。"),
            ("自部署的数据安全如何保障？", "定期备份是最重要的。建议使用 Docker volumes 存储数据，配合自动备份脚本。HTTPS 和强密码也是必须的。"),
        ],
    },
    {
        "slug": "open-source-chatgpt-alternatives",
        "title": "开源 ChatGPT 替代品：本地运行的大模型对话工具 - 拾品号导航",
        "h1": "开源 ChatGPT 替代品：本地运行的大模型对话工具",
        "meta_desc": "想在本地运行 AI 对话模型？Ollama、LM Studio、GPT4All 等开源工具让你在自己的电脑上跑大模型，无需联网。",
        "keywords": "开源ChatGPT,本地大模型,Ollama,LM Studio,GPT4All,本地AI,离线AI",
        "content": """
<p>不想把对话数据发到云端？想在没有网络的情况下使用 AI？这些开源工具让你在自己的电脑上运行大语言模型，完全离线、完全隐私。</p>

<h2>最佳本地 AI 工具</h2>

<h3>Ollama</h3>
<p>最简单的本地大模型运行工具。一行命令安装，一行命令运行模型。支持 Llama、Mistral、Qwen、Gemma 等主流模型。macOS、Linux、Windows 都支持。</p>

<h3>LM Studio</h3>
<p>图形界面的本地模型运行工具，支持搜索和下载 HuggingFace 上的模型。界面友好，适合不想用命令行的用户。</p>

<h3>GPT4All</h3>
<p>Nomic AI 推出的本地 AI 助手，支持多种开源模型。安装简单，有图形界面，支持文档问答。</p>

<h3>Open WebUI</h3>
<p>Ollama 的最佳前端界面，支持多模型切换、对话历史、文档上传、RAG。自部署后就是一个完整的 ChatGPT 替代品。</p>

<h3>KoboldCpp</h3>
<p>专注于角色扮演和创意写作的本地 AI 工具。支持 GGUF 格式模型，有图形界面和 API。</p>

<h2>硬件要求</h2>
<table>
<tr><th>模型大小</th><th>最低显存</th><th>推荐显存</th><th>可运行模型</th></tr>
<tr><td>7B</td><td>4GB</td><td>8GB</td><td>Llama 3 7B, Qwen 7B</td></tr>
<tr><td>13B</td><td>8GB</td><td>12GB</td><td>Llama 3 13B</td></tr>
<tr><td>70B</td><td>32GB</td><td>48GB</td><td>Llama 3 70B (量化)</td></tr>
</table>
<p>没有显卡也可以用 CPU 运行，只是速度较慢。Apple Silicon Mac 的统一内存架构非常适合运行大模型。</p>

<h2>推荐模型</h2>
<ul>
<li><strong>通用对话：</strong>Llama 3 8B、Qwen 2.5 7B</li>
<li><strong>编程辅助：</strong>DeepSeek Coder、CodeLlama</li>
<li><strong>中文优化：</strong>Qwen 2.5、Yi、ChatGLM</li>
<li><strong>轻量运行：</strong>Phi-3 Mini、Gemma 2B</li>
</ul>
""",
        "faq": [
            ("本地 AI 比 ChatGPT 好用吗？", "对于隐私敏感场景和离线需求，本地 AI 是唯一选择。但在绝对能力上，GPT-4o 等顶级云端模型仍然领先。本地模型适合日常对话、编程辅助、文档总结等常见任务。"),
            ("没有显卡能跑本地模型吗？", "可以。7B 参数的模型在 16GB 内存的 CPU 上就能运行，只是速度较慢（约 5-10 tokens/秒）。Apple Silicon Mac 的体验最好。"),
            ("本地模型的数据安全吗？", "是的。所有数据都在本地处理，不发送到任何服务器。这是本地 AI 最大的优势。"),
        ],
    },
]

def esc(s):
    return html.escape(str(s or ""), quote=True)

def page_shell(title, description, canonical, body, keywords="", extra_jsonld=None):
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
    count = 0

    for page in COMPARISON_PAGES:
        slug = page["slug"]
        canonical = f"{BASE}/guides/{slug}"
        # BreadcrumbList
        breadcrumbs = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "首页", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "使用指南", "item": BASE + "/guides/"},
                {"@type": "ListItem", "position": 3, "name": page["h1"]},
            ]
        }
        # FAQPage
        faq_entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page.get("faq", [])]
        faq_jsonld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities}
        # Article
        article_jsonld = {"@context": "https://schema.org", "@type": "Article", "headline": page["h1"], "description": page["meta_desc"], "url": canonical, "publisher": {"@type": "Organization", "name": "拾品号导航", "url": BASE}}

        # FAQ HTML
        faq_html = ""
        if page.get("faq"):
            items = "".join(f'<details class="faq-item" open><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in page["faq"])
            faq_html = f'<section class="faq-panel"><h2>常见问题</h2>{items}</section>'

        body = f"""
    <section class="search-section small trend-hero">
      <span class="eyebrow">对比评测</span>
      <h1>{esc(page["h1"])}</h1>
      <p class="daily-line">拾品号导航 · 深度对比评测 · 帮你选到最适合的工具</p>
    </section>
    <section class="content-wrap single"><section class="main-content">
      <nav class="breadcrumb-nav" aria-label="面包屑导航">
        <a href="/">首页</a> &gt; <a href="/guides/">使用指南</a> &gt; <span>{esc(page["h1"])}</span>
      </nav>
      <article class="guide-article">
        {page["content"]}
      </article>
      {faq_html}
      <div class="guide-links">
        <h2>相关资源</h2>
        <ul>
          <li><a href="/trending/">GitHub 涨星榜</a> - 发现最新热门项目</li>
          <li><a href="/collections/">专题合集</a> - 按主题浏览项目</li>
          <li><a href="/guides/">更多指南</a> - 开发者使用指南</li>
        </ul>
      </div>
    </section></section>"""

        out_path = guides_root / f"{slug}.html"
        out_path.write_text(page_shell(page["title"], page["meta_desc"], canonical, body, page.get("keywords", ""), [breadcrumbs, article_jsonld, faq_jsonld]), encoding="utf-8")
        count += 1
        print(f"  Generated: /guides/{slug}")

    print(f"\nGenerated {count} comparison/alternative pages")
    return count

if __name__ == "__main__":
    main()
