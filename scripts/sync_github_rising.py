#!/usr/bin/env python3
"""Sync fast-rising GitHub repositories into the static directory data.

Signal used: repositories created recently, not forks/archives, sorted by stars,
then ranked by stars per day. This is a practical public-API proxy for "rising
fast" that works in GitHub Actions without scraping trending pages.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_PATH = ROOT / "data" / "projects.json"
TRENDING_PATH = ROOT / "data" / "github-rising.json"
BASE = "https://api.github.com"

CATEGORY_RULES = [
    ("AI Agents", ["ai", "agent", "llm", "rag", "chatbot", "openai", "mcp", "model", "ollama", "transformer"]),
    ("Web Frameworks", ["web", "react", "nextjs", "vue", "svelte", "astro", "frontend", "ui", "tailwind"]),
    ("Docs & Knowledge", ["docs", "documentation", "knowledge", "wiki", "note", "search"]),
    ("No-Code & Admin", ["admin", "dashboard", "nocode", "low-code", "cms", "builder"]),
    ("Backend & Database", ["backend", "api", "database", "db", "postgres", "server", "cache", "queue"]),
    ("Automation", ["automation", "workflow", "bot", "cli", "scraper", "crawler", "task"]),
    ("Data & Analytics", ["data", "analytics", "etl", "visualization", "chart", "bi", "notebook"]),
    ("Deployment", ["deploy", "cloud", "serverless", "docker", "kubernetes", "infra", "hosting"]),
    ("Ops & Monitoring", ["monitoring", "observability", "logs", "metrics", "security", "devops"]),
    ("Content & CMS", ["content", "blog", "cms", "markdown", "newsletter"]),
]
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

def api(path: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "daohang-bot-cd-rising-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(BASE + path, headers=headers)
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")[:500]
        raise RuntimeError(f"GitHub API HTTP {e.code}: {detail}") from e
    except URLError as e:
        raise RuntimeError(f"GitHub API network error: {e}") from e

def clean_desc(text: str | None) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    if not text:
        return "Fast-rising open-source project discovered from recent GitHub activity."
    return text[:180].rstrip(" .") + ("." if len(text) <= 180 else "…")

def classify(repo: dict) -> str:
    hay = " ".join([
        repo.get("name") or "",
        repo.get("description") or "",
        repo.get("language") or "",
        " ".join(repo.get("topics") or []),
    ]).lower()
    scores = []
    for category, words in CATEGORY_RULES:
        score = sum(1 for word in words if word in hay)
        if score:
            scores.append((score, category))
    if scores:
        return sorted(scores, reverse=True)[0][1]
    return "Automation"

def zh_desc(repo: dict, category: str, stars_per_day: float) -> str:
    lang = repo.get("language") or "开源"
    desc = clean_desc(repo.get("description"))
    return f"近期 GitHub 涨星较快的 {lang} 项目，约 {stars_per_day:.1f} 星/天。简介：{desc}"

def icon(name: str) -> str:
    letters = re.findall(r"[A-Za-z0-9]", name.upper())
    return "".join(letters[:2]) or "GH"

def project_from_repo(repo: dict, rank: int, now: datetime) -> dict:
    created = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
    age_days = max((now - created).total_seconds() / 86400, 1)
    stars = int(repo.get("stargazers_count") or 0)
    forks = int(repo.get("forks_count") or 0)
    spd = stars / age_days
    category = classify(repo)
    tags = []
    if repo.get("language"):
        tags.append(str(repo["language"]).lower())
    tags.extend((repo.get("topics") or [])[:3])
    tags.append("rising")
    return {
        "name": repo["full_name"],
        "category": category,
        "url": repo["html_url"],
        "desc": clean_desc(repo.get("description")),
        "tags": list(dict.fromkeys(tags))[:5],
        "badge": f"Rising #{rank}",
        "featured": rank <= 12,
        "category_cn": CAT_CN.get(category, category),
        "icon": icon(repo.get("name") or repo["full_name"]),
        "desc_cn": zh_desc(repo, category, spd),
        "stars": stars,
        "forks": forks,
        "language": repo.get("language"),
        "growth": {
            "rank": rank,
            "stars_per_day": round(spd, 2),
            "created_at": repo["created_at"],
            "pushed_at": repo.get("pushed_at"),
            "synced_at": now.isoformat().replace("+00:00", "Z"),
        },
    }

def main() -> int:
    now = datetime.now(timezone.utc)
    since = (now - timedelta(days=int(os.environ.get("RISING_WINDOW_DAYS", "45")))).date().isoformat()
    min_stars = int(os.environ.get("RISING_MIN_STARS", "50"))
    limit = int(os.environ.get("RISING_LIMIT", "36"))
    query = quote(f"created:>={since} stars:>={min_stars} fork:false archived:false")
    data = api(f"/search/repositories?q={query}&sort=stars&order=desc&per_page=100")
    repos = data.get("items", [])
    ranked = []
    seen = set()
    for repo in repos:
        if repo.get("fork") or repo.get("archived") or repo["full_name"].lower() in seen:
            continue
        created = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
        age_days = max((now - created).total_seconds() / 86400, 1)
        stars = int(repo.get("stargazers_count") or 0)
        score = stars / age_days
        if stars < min_stars:
            continue
        seen.add(repo["full_name"].lower())
        ranked.append((score, stars, repo))
    ranked.sort(key=lambda x: (x[0], x[1]), reverse=True)
    rising = [project_from_repo(repo, i + 1, now) for i, (_, _, repo) in enumerate(ranked[:limit])]

    existing = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))
    existing_non_rising = [p for p in existing if "rising" not in [str(t).lower() for t in p.get("tags", [])] and not str(p.get("badge", "")).startswith("Rising #")]
    merged = existing_non_rising + rising
    PROJECTS_PATH.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    TRENDING_PATH.write_text(json.dumps({
        "source": "GitHub Search API",
        "signal": f"created:>={since} stars:>={min_stars} fork:false archived:false sorted by stars_per_day",
        "synced_at": now.isoformat().replace("+00:00", "Z"),
        "count": len(rising),
        "projects": rising,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Synced {len(rising)} rising repos since {since}; total projects: {len(merged)}")
    for p in rising[:10]:
        print(f"#{p['growth']['rank']:02d} {p['name']} ★{p['stars']} {p['growth']['stars_per_day']}/day")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
