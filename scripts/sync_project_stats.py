#!/usr/bin/env python3
"""Refresh GitHub stars/forks/language and stars-per-day for every project card.

The navigation cards render `growth.stars_per_day` when present. This script
fills that field for all GitHub repositories in data/projects.json, not only the
fast-rising list.
"""
from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_PATH = ROOT / "data" / "projects.json"
BASE = "https://api.github.com"
REPO_RE = re.compile(r"github\.com/([^/]+)/([^/#?]+)")


def api(path: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "daohang-bot-cd-project-stats-sync",
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


def repo_path(url: str) -> str | None:
    match = REPO_RE.search(url or "")
    if not match:
        return None
    owner, repo = match.group(1), match.group(2).removesuffix(".git")
    return f"{owner}/{repo}"


def stars_per_day(stars: int, created_at: str, now: datetime) -> float:
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    age_days = max((now - created).total_seconds() / 86400, 1)
    return round(stars / age_days, 2)


def should_fetch(project: dict) -> bool:
    if os.environ.get("PROJECT_STATS_MISSING_ONLY") == "1":
        return not bool(project.get("growth", {}).get("stars_per_day"))
    return True


def apply_repo_stats(project: dict, repo: dict, now: datetime) -> None:
    stars = int(repo.get("stargazers_count") or 0)
    project["stars"] = stars
    project["forks"] = int(repo.get("forks_count") or 0)
    if repo.get("language"):
        project["language"] = repo.get("language")
    growth = dict(project.get("growth") or {})
    # Preserve rising rank for ranking labels, but refresh the actual metrics.
    growth.update({
        "stars_per_day": stars_per_day(stars, repo["created_at"], now),
        "created_at": repo["created_at"],
        "pushed_at": repo.get("pushed_at"),
        "synced_at": now.isoformat().replace("+00:00", "Z"),
    })
    project["growth"] = growth


def main() -> int:
    now = datetime.now(timezone.utc)
    projects = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))
    cache: dict[str, dict] = {}
    updated = skipped = failed = 0
    for project in projects:
        path = repo_path(project.get("url", ""))
        if not path:
            skipped += 1
            continue
        if not should_fetch(project):
            skipped += 1
            continue
        try:
            repo = cache.get(path)
            if repo is None:
                repo = api(f"/repos/{path}")
                cache[path] = repo
                # Be gentle in local unauthenticated runs; GitHub Actions uses a token.
                if not (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")):
                    time.sleep(0.15)
            apply_repo_stats(project, repo, now)
            updated += 1
        except Exception as exc:  # Keep the daily job useful even if one repo is removed.
            failed += 1
            print(f"WARN {path}: {exc}")
    PROJECTS_PATH.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated stats for {updated} projects; skipped {skipped}; failed {failed}.")
    if failed and updated == 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
