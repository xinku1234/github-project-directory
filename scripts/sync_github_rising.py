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
from zoneinfo import ZoneInfo
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_PATH = ROOT / "data" / "projects.json"
TRENDING_PATH = ROOT / "data" / "github-rising.json"
BASE = "https://api.github.com"
# Repos matching these never enter the public data (site or WeChat).
EXCLUDED_KEYWORDS = (
    "nsfw", "porn", "xxx", "hentai", "adult", "onlyfans", "lewd", "erotic",
    "crack", "keygen", "pirate", "nulled", "warez", "破解", "成人", "色情",
)

CN_TZ = ZoneInfo("Asia/Shanghai")


def local_token() -> str | None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    env_path = Path.home() / ".hermes" / ".env"
    if env_path.exists():
        for raw in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if line.startswith("GITHUB_TOKEN=") or line.startswith("GH_TOKEN="):
                candidate = line.split("=", 1)[1].strip().strip('"').strip("'")
                if candidate:
                    return candidate
    return None

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
    token = local_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(BASE + path, headers=headers)
    delays = [10, 20, 40]
    for attempt in range(len(delays) + 1):
        try:
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:500]
            if (500 <= e.code < 600 or e.code == 429) and attempt < len(delays):
                delay = delays[attempt]
                print(f"[WARN] GitHub API HTTP {e.code}, retrying in {delay}s (attempt {attempt + 1}/{len(delays)})...", file=sys.stderr)
                time.sleep(delay)
                continue
            raise RuntimeError(f"GitHub API HTTP {e.code}: {detail}") from e
        except (URLError, TimeoutError) as e:
            if attempt < len(delays):
                delay = delays[attempt]
                print(f"[WARN] GitHub API network error ({e}), retrying in {delay}s (attempt {attempt + 1}/{len(delays)})...", file=sys.stderr)
                time.sleep(delay)
                continue
            raise RuntimeError(f"GitHub API network error: {e}") from e
    raise RuntimeError(f"GitHub API request failed after retries: {path}")


def html_search_repo_names(since: str, min_stars: int, limit: int) -> list[str]:
    """Return public repository names from GitHub's HTML search page.

    GitHub's REST search endpoint has a separate, much smaller quota than the
    normal repository endpoint. When the shared server IP exhausts that search
    quota, the web search page remains usable; metadata is fetched separately
    through /repos/<owner>/<repo> so the normal schema and ranking stay intact.
    """
    query = quote(f"created:>={since} stars:>={min_stars} fork:false archived:false")
    url = "https://github.com/search?q=%s&type=repositories&s=stars&o=desc" % query
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; daohang-rising-sync/1.0)", "Accept": "text/html"})
    with urlopen(req, timeout=45) as resp:
        page = resp.read().decode("utf-8", "replace")
    names = []
    skip_prefixes = ('topics/', 'search/', 'login/', 'settings/')
    for name in re.findall(r'href="/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"', page):
        if name.lower().startswith(skip_prefixes):
            continue
        if name not in names:
            names.append(name)
        if len(names) >= limit:
            break
    if not names:
        raise RuntimeError("GitHub HTML search fallback returned no repository names")
    return names


def fetch_repos_from_html_search(since: str, min_stars: int, limit: int) -> list[dict]:
    repos = []
    for name in html_search_repo_names(since, min_stars, limit):
        try:
            repos.append(api("/repos/" + quote(name, safe="/")))
        except RuntimeError as exc:
            print("[WARN] metadata fetch failed for %s: %s" % (name, exc), file=sys.stderr)
    if not repos:
        raise RuntimeError("GitHub HTML search fallback found names but no repository metadata")
    return repos

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
    """Write a user-facing description focused on what the project does.

    Growth is still available in the meta row, but the paragraph should explain
    the repository's purpose instead of repeating that it is fast-rising.
    """
    lang = repo.get("language") or "开源"
    desc = clean_desc(repo.get("description"))
    category_cn = CAT_CN.get(category, category)
    if desc.startswith("Fast-rising open-source project"):
        return f"这是一个 {category_cn} 方向的 {lang} 开源项目，适合查看源码、功能定位和二次开发价值；原仓库暂未提供更详细的项目简介。"
    return f"这是一个 {category_cn} 方向的 {lang} 开源项目，主要用于：{desc}"

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
    since = (now.astimezone(CN_TZ) - timedelta(days=int(os.environ.get("RISING_WINDOW_DAYS", "45")))).date().isoformat()
    min_stars = int(os.environ.get("RISING_MIN_STARS", "50"))
    limit = int(os.environ.get("RISING_LIMIT", "100"))
    query = quote(f"created:>={since} stars:>={min_stars} fork:false archived:false")
    source = "GitHub Search API"
    try:
        data = api(f"/search/repositories?q={query}&sort=stars&order=desc&per_page=100")
        repos = data.get("items", [])
    except RuntimeError as exc:
        if "HTTP 403" not in str(exc) and "rate limit" not in str(exc).lower():
            raise
        print("[WARN] GitHub REST search rate-limited; using public HTML search fallback", file=sys.stderr)
        repos = fetch_repos_from_html_search(since, min_stars, min(limit, 100))
        source = "GitHub public HTML search fallback"
    ranked = []
    seen = set()
    for repo in repos:
        if repo.get("fork") or repo.get("archived") or repo["full_name"].lower() in seen:
            continue
        # Content red line: these never enter the public site data. Expanding the
        # rising pool surfaced an "nsfw-pose-skill" repo at rank 25.
        _blob = (repo["full_name"] + " " + (repo.get("description") or "")).lower()
        if any(k in _blob for k in EXCLUDED_KEYWORDS):
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
        "source": source,
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
