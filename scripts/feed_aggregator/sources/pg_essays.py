"""Fetch Paul Graham essays from RSS."""

from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser


def fetch_pg_essays(days=1):
    feed = feedparser.parse("https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_paulgraham.xml")
    since = datetime.now(timezone.utc) - timedelta(days=days)

    essays = []
    for e in feed.entries:
        pub = e.get("published_parsed") or e.get("updated_parsed")
        if not pub:
            continue
        pub_dt = datetime.fromtimestamp(mktime(pub), tz=timezone.utc)
        if pub_dt >= since:
            essays.append({"title": e.title, "url": e.link})

    return essays
