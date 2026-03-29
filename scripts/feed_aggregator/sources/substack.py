"""Fetch recent posts from Substack publications via RSS."""

import sys
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
    status = getattr(feed, "status", None)
    if feed.bozo:
        print(f"    [Substack] {handle}: feed error - {feed.bozo_exception}", file=sys.stderr)
    if status and status != 200:
        print(f"    [Substack] {handle}: HTTP {status}", file=sys.stderr)
    if not feed.entries:
        print(f"    [Substack] {handle}: 0 entries in feed (status={status})", file=sys.stderr)
    posts = []
    for e in feed.entries:
        pub = e.get("published_parsed") or e.get("updated_parsed")
        if not pub:
            continue
        pub_dt = datetime.fromtimestamp(mktime(pub), tz=timezone.utc)
        if pub_dt >= since:
            posts.append({"title": e.title, "url": e.link})
    if feed.entries and not posts:
        print(f"    [Substack] {handle}: {len(feed.entries)} entries but none since {since.isoformat()}", file=sys.stderr)
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
