"""Fetch recent Claude blog posts from RSS."""

import sys
from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser
import requests

FEED_URL = "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_claude.xml"


def fetch_claude_blog(days=1):
    resp = requests.get(FEED_URL, timeout=15)
    if not resp.ok:
        print(f"    [Claude blog] HTTP {resp.status_code}", file=sys.stderr)
        return []
    feed = feedparser.parse(resp.content)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    if feed.bozo and not feed.entries:
        print(f"    [Claude blog] feed parse error - {feed.bozo_exception}", file=sys.stderr)
    if not feed.entries:
        print(f"    [Claude blog] 0 entries in feed", file=sys.stderr)

    posts = []
    for e in feed.entries:
        if hasattr(e, "published_parsed") and e.published_parsed:
            pub_dt = datetime.fromtimestamp(mktime(e.published_parsed), tz=timezone.utc)
            if pub_dt >= since:
                posts.append({"title": e.title, "url": e.link})

    if feed.entries and not posts:
        print(f"    [Claude blog] {len(feed.entries)} entries but none since {since.isoformat()}", file=sys.stderr)

    return posts
