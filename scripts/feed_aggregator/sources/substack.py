"""Fetch recent posts from Substack publications via RSS."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import mktime

import feedparser

HANDLES_FILE = Path(__file__).resolve().parent.parent.parent / "substack-handles.txt"


def _fetch_feed(handle, since):
    """Fetch a single Substack feed and return recent posts."""
    url = f"https://{handle}.substack.com/feed"
    feed = feedparser.parse(url)
    posts = []
    for e in feed.entries:
        pub = e.get("published_parsed") or e.get("updated_parsed")
        if not pub:
            continue
        pub_dt = datetime.fromtimestamp(mktime(pub), tz=timezone.utc)
        if pub_dt >= since:
            posts.append({"title": e.title, "url": e.link})
    return posts


def fetch_substack(days=1):
    handles = []
    with open(HANDLES_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                handles.append(line)

    if not handles:
        return []

    since = datetime.now(timezone.utc) - timedelta(days=days)

    all_posts = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(_fetch_feed, handle, since) for handle in handles]
        for f in futures:
            all_posts.extend(f.result())

    return all_posts
