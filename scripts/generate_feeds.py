#!/usr/bin/env python3
"""Generate RSS feed for the navigation site.

RSS feed helps with:
- Content syndication
- RSS reader discovery
- Fresh content signals for search engines
- Automated social media posting
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring, indent

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://daohang.bot.cd"

def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def main():
    projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    rising = json.loads((ROOT / "data" / "github-rising.json").read_text(encoding="utf-8"))
    
    now = datetime.now(timezone.utc)
    now_str = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    # Build RSS feed
    rss = Element("rss", version="2.0")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")
    channel = SubElement(rss, "channel")
    
    SubElement(channel, "title").text = "拾品号导航 - GitHub 开源项目发现"
    SubElement(channel, "link").text = BASE + "/"
    SubElement(channel, "description").text = "精选 GitHub 开源项目、AI 工具、开发者资源和快速涨星项目榜。每日更新。"
    SubElement(channel, "language").text = "zh-CN"
    SubElement(channel, "lastBuildDate").text = now_str
    SubElement(channel, "ttl").text = "60"
    
    atom_link = SubElement(channel, "link")
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")
    atom_link.set("href", f"{BASE}/feed.xml")
    
    # Add rising projects as feed items
    rising_projects = rising.get("projects", [])[:10]
    for p in rising_projects:
        item = SubElement(channel, "item")
        name = p.get("name", "")
        slug = slugify(name)
        desc_cn = p.get("desc_cn") or p.get("desc") or ""
        growth = p.get("growth") or {}
        spd = growth.get("stars_per_day", 0)
        stars = p.get("stars", 0)
        cat_cn = p.get("category_cn") or p.get("category") or ""
        
        SubElement(item, "title").text = f"🔥 {name} - {cat_cn} (★{stars:,} ↗{spd:.1f}/天)"
        SubElement(item, "link").text = f"{BASE}/projects/{slug}/"
        SubElement(item, "description").text = f"{desc_cn} | GitHub: {p.get('url', '')} | Stars: {stars:,} | 增速: {spd:.2f}/天"
        SubElement(item, "guid").text = f"{BASE}/projects/{slug}/"
        SubElement(item, "pubDate").text = now_str
        SubElement(item, "category").text = cat_cn
    
    # Add latest daily brief
    item = SubElement(channel, "item")
    SubElement(item, "title").text = f"📊 GitHub 每日增速 Top10 · {now.strftime('%Y-%m-%d')}"
    SubElement(item, "link").text = f"{BASE}/daily-brief/"
    top3 = ", ".join(p.get("name", "") for p in rising_projects[:3])
    SubElement(item, "description").text = f"今日增速前三: {top3}。查看完整榜单和项目详情。"
    SubElement(item, "guid").text = f"{BASE}/daily-brief/"
    SubElement(item, "pubDate").text = now_str
    
    # Write RSS
    indent(rss, space="  ")
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(rss, encoding="unicode", xml_declaration=False)
    (ROOT / "feed.xml").write_text(xml_content, encoding="utf-8")
    print(f"RSS feed generated: {len(rising_projects)} rising items + daily brief")
    
    # Also generate a JSON Feed (for modern readers)
    json_feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "拾品号导航 - GitHub 开源项目发现",
        "home_page_url": BASE + "/",
        "feed_url": f"{BASE}/feed.json",
        "description": "精选 GitHub 开源项目、AI 工具、开发者资源和快速涨星项目榜。",
        "language": "zh-CN",
        "items": [],
    }
    
    for p in rising_projects:
        name = p.get("name", "")
        slug = slugify(name)
        desc_cn = p.get("desc_cn") or p.get("desc") or ""
        growth = p.get("growth") or {}
        spd = growth.get("stars_per_day", 0)
        stars = p.get("stars", 0)
        cat_cn = p.get("category_cn") or p.get("category") or ""
        
        json_feed["items"].append({
            "id": f"{BASE}/projects/{slug}/",
            "url": f"{BASE}/projects/{slug}/",
            "title": f"🔥 {name} - {cat_cn} (★{stars:,} ↗{spd:.1f}/天)",
            "content_text": f"{desc_cn}\n\nGitHub: {p.get('url', '')}\nStars: {stars:,} | 增速: {spd:.2f}/天",
            "tags": [cat_cn, "开源项目", "GitHub"],
        })
    
    (ROOT / "feed.json").write_text(json.dumps(json_feed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON Feed generated: {len(json_feed['items'])} items")

if __name__ == "__main__":
    main()
