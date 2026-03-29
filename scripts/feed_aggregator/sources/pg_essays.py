"""Fetch Paul Graham essays from RSS."""

import sys
from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser

FEED_URL = "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_paulgraham.xml"


def fetch_pg_essays(days=1):
    feed = feedparser.parse(FEED_URL)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    status = getattr(feed, "status", None)
    if feed.bozo:
        print(f"    [PG essays] feed error - {feed.bozo_exception}", file=sys.stderr)
    if status and status != 200:
        print(f"    [PG essays] HTTP {status}", file=sys.stderr)
    if not feed.entries:
        print(f"    [PG essays] 0 entries in feed (status={status})", file=sys.stderr)

    essays = []
    for e in feed.entries:
        pub = e.get("published_parsed") or e.get("updated_parsed")
        if not pub:
            continue
        pub_dt = datetime.fromtimestamp(mktime(pub), tz=timezone.utc)
        if pub_dt >= since:
            essays.append({"title": e.title, "url": e.link})

    if feed.entries and not essays:
        print(f"    [PG essays] {len(feed.entries)} entries but none since {since.isoformat()}", file=sys.stderr)

    return essays
