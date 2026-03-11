"""Aggregate 1 day of feed sources and POST to the vet ingest endpoint."""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import requests

# from sources.hn import fetch_top_hn
from sources.gh_trending import fetch_gh_trending
from sources.pg_essays import fetch_pg_essays
from sources.claude_blog import fetch_claude_blog
from sources.blogs import fetch_blogs
from sources.spotify import fetch_spotify_podcasts
from sources.youtube import fetch_yt_videos
from sources.substack import fetch_substack


DAYS = int(os.environ.get("FEED_DAYS", "1"))


def _fetch_spotify_safe():
    try:
        return fetch_spotify_podcasts(days=DAYS)
    except KeyError:
        print("WARNING: SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET not set, skipping podcasts", file=sys.stderr)
        return []


SOURCES = {
    "articles": [
        # ("HN", lambda: fetch_top_hn(days=DAYS)),
        ("PG essays", lambda: fetch_pg_essays(days=DAYS)),
        ("Claude blog", lambda: fetch_claude_blog(days=DAYS)),
        ("Tech blogs", lambda: fetch_blogs(days=DAYS)),
        ("Substack", lambda: fetch_substack(days=DAYS)),
    ],
    "repos": [
        ("GitHub trending", fetch_gh_trending),
    ],
    "videos": [
        ("YouTube", lambda: fetch_yt_videos(days=DAYS)),
    ],
    "podcasts": [
        ("Spotify", _fetch_spotify_safe),
    ],
}


def main():
    ingest_url = os.environ.get("INGEST_URL")
    if not ingest_url:
        print("ERROR: INGEST_URL environment variable is required", file=sys.stderr)
        sys.exit(1)

    results = {"articles": [], "repos": [], "videos": [], "podcasts": []}

    # Flatten all sources into (category, name, fn) tuples
    tasks = []
    for category, sources in SOURCES.items():
        for name, fn in sources:
            tasks.append((category, name, fn))

    with ThreadPoolExecutor(max_workers=10) as pool:
        future_to_task = {}
        for category, name, fn in tasks:
            future_to_task[pool.submit(fn)] = (category, name)

        for future in as_completed(future_to_task):
            category, name = future_to_task[future]
            try:
                items = future.result()
                results[category].extend(items)
                print(f"  {name}: {len(items)} items", file=sys.stderr)
            except Exception as e:
                print(f"  {name}: ERROR - {e}", file=sys.stderr)

    draft = {
        "date": date.today().isoformat(),
        "articles": results["articles"],
        "repos": results["repos"],
        "videos": results["videos"],
        "podcasts": results["podcasts"],
    }

    total = sum(len(v) for v in results.values())
    print(f"\nTotal items: {total}", file=sys.stderr)

    # POST to ingest endpoint
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("API_KEY")
    if api_key:
        headers["X-API-Key"] = api_key

    resp = requests.post(
        ingest_url,
        json=draft,
        headers=headers,
    )
    print(f"POST {ingest_url} -> {resp.status_code}", file=sys.stderr)

    if resp.ok:
        print(f"Response: {resp.json()}", file=sys.stderr)
    else:
        print(f"Error response: {resp.text}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
