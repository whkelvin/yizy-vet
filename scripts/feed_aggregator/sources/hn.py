"""Fetch top Hacker News stories from the past N days."""

import time
import requests


def fetch_top_hn(days=1, limit=10):
    since = int(time.time()) - days * 86400
    resp = requests.get(
        "https://hn.algolia.com/api/v1/search",
        params={
            "tags": "story",
            "numericFilters": f"created_at_i>{since}",
            "hitsPerPage": limit,
        },
    )
    resp.raise_for_status()
    hits = sorted(resp.json()["hits"], key=lambda h: h.get("points", 0), reverse=True)[:limit]

    results = []
    for h in hits:
        url = h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}"
        results.append({"title": h["title"], "url": url})
    return results
