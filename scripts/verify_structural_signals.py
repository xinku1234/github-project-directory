#!/usr/bin/env python3
"""Local checks for Aion-style structural signals on ShipinHao Nav."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    html = read("index.html")
    robots = read("robots.txt")
    llms = read("llms.txt")
    css = read("assets/nav-style.css")

    title_match = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
    assert_true(title_match is not None, "homepage missing title tag")
    assert_true(desc_match is not None, "homepage missing meta description")
    title = title_match.group(1)
    desc = desc_match.group(1)
    h1_count = len(re.findall(r"<h1\b", html, flags=re.I))
    h2_count = len(re.findall(r"<h2\b", html, flags=re.I))
    jsonld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S)

    assert_true(20 <= len(title) <= 60, f"title length should be Aion-friendly, got {len(title)}: {title}")
    assert_true(60 <= len(desc) <= 180, f"meta description should be concise, got {len(desc)}")
    assert_true(h1_count == 1, f"homepage should have one H1, got {h1_count}")
    assert_true(h2_count >= 3, f"homepage should expose section H2 headings, got {h2_count}")
    assert_true(len(jsonld_blocks) >= 2, f"homepage should have JSON-LD blocks, got {len(jsonld_blocks)}")
    for block in jsonld_blocks:
        json.loads(block)

    for crawler in ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot"]:
        assert_true(f"User-agent: {crawler}\nAllow: /" in robots, f"robots.txt missing {crawler} allow rule")
    assert_true("LLMs: https://daohang.bot.cd/llms.txt" in robots or "Allow: /llms.txt" in robots, "robots should expose llms.txt")
    assert_true("AI crawler access policy" in llms, "llms.txt should document AI crawler policy")
    assert_true(".directory-intro h2" in css and ".category-title h2" in css, "CSS should style new H2 headings")

    print("STRUCTURAL_SIGNAL_CHECK_OK")
    print({"title_len": len(title), "meta_len": len(desc), "h1": h1_count, "h2": h2_count, "jsonld": len(jsonld_blocks)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
