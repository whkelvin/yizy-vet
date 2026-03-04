"""Fetch GitHub trending repos (daily)."""

import re
import requests


def fetch_gh_trending():
    resp = requests.get(
        "https://github.com/trending",
        params={"since": "daily", "spoken_language_code": "en"},
        headers={"Accept": "text/html"},
    )
    resp.raise_for_status()

    articles = re.split(r'<article class="Box-row">', resp.text)[1:]

    repos = []
    for art in articles:
        link = re.search(r'<h2[^>]*>.*?href="(/[^/]+/[^"]+)"', art, re.DOTALL)
        if not link:
            continue

        path = link.group(1).strip()
        name = path.lstrip("/")
        url = "https://github.com" + path

        stars_match = re.search(r'([\d,]+)\s+stars today', art)
        stars = int(stars_match.group(1).replace(",", "")) if stars_match else 0

        repos.append({"name": name, "url": url, "starsThisWeek": stars})

    return repos
