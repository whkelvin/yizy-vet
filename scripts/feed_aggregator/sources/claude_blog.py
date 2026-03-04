"""Fetch recent Claude blog posts from RSS."""

from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser


def fetch_claude_blog(days=1):
    feed = feedparser.parse("https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_claude.xml")
    since = datetime.now(timezone.utc) - timedelta(days=days)

    posts = []
    for e in feed.entries:
        if hasattr(e, "published_parsed") and e.published_parsed:
            pub_dt = datetime.fromtimestamp(mktime(e.published_parsed), tz=timezone.utc)
            if pub_dt >= since:
                posts.append({"title": e.title, "url": e.link})

    return posts
