#!/usr/bin/env python3
"""Generate social media share text for the daily GitHub rising brief.

Outputs share-ready text for Twitter/X, WeChat, and general use.
Can be called by cron or manually before social posting.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://daohang.bot.cd"

def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def main():
    rising = json.loads((ROOT / "data" / "github-rising.json").read_text(encoding="utf-8"))
    projects = rising.get("projects", [])[:10]
    date = rising.get("synced_at", "")[:10] or datetime.now(timezone.utc).date().isoformat()
    
    # Twitter/X thread format
    twitter_lines = [f"🔥 GitHub 开源项目增速 Top10 · {date}\n"]
    for i, p in enumerate(projects, 1):
        name = p.get("name", "")
        stars = p.get("stars", 0)
        growth = p.get("growth") or {}
        spd = growth.get("stars_per_day", 0)
        cat = p.get("category_cn") or p.get("category") or ""
        desc = (p.get("desc_cn") or p.get("desc") or "")[:60]
        url = p.get("url", "")
        twitter_lines.append(f"#{i} {name}\n★{stars:,} ↗{spd:.1f}/天 · {cat}\n{desc}\n{url}\n")
    
    twitter_lines.append(f"完整榜单: {BASE}/daily-brief/\n收录 200+ 项目: {BASE}/projects/")
    
    twitter_text = "\n".join(twitter_lines)
    
    # WeChat format (shorter, more visual)
    wechat_lines = [f"📊 GitHub 每日增速 Top10\n{date} · 拾品号导航\n"]
    for i, p in enumerate(projects[:5], 1):
        name = p.get("name", "")
        stars = p.get("stars", 0)
        growth = p.get("growth") or {}
        spd = growth.get("stars_per_day", 0)
        wechat_lines.append(f"{i}. {name} ★{stars:,} ↗{spd:.1f}/天")
    wechat_lines.append(f"\n👉 完整榜单: {BASE}/daily-brief/")
    wechat_lines.append(f"🔍 200+ 开源项目: {BASE}/")
    
    wechat_text = "\n".join(wechat_lines)
    
    # General share text
    general_text = f"GitHub 涨星最快的 10 个开源项目 ({date})\n{BASE}/daily-brief/\n\n"
    for i, p in enumerate(projects[:5], 1):
        general_text += f"{i}. {p.get('name', '')} (★{p.get('stars', 0):,})\n"
    general_text += f"\n更多项目: {BASE}/"
    
    # Output
    output_dir = ROOT / "data"
    
    (output_dir / "share_twitter.txt").write_text(twitter_text, encoding="utf-8")
    (output_dir / "share_wechat.txt").write_text(wechat_text, encoding="utf-8")
    (output_dir / "share_general.txt").write_text(general_text, encoding="utf-8")
    
    print(f"=== Share text generated for {date} ===")
    print(f"Twitter/X ({len(twitter_text)} chars):")
    print(twitter_text[:500])
    print(f"\nWeChat ({len(wechat_text)} chars):")
    print(wechat_text)
    print(f"\nGeneral ({len(general_text)} chars):")
    print(general_text)

if __name__ == "__main__":
    main()
