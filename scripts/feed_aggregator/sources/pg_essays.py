"""Fetch Paul Graham essays from RSS."""

import sys
from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser
import requests

FEED_URL = "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_paulgraham.xml"


def fetch_pg_essays(days=1):
    resp = requests.get(FEED_URL, timeout=15)
    if not resp.ok:
        print(f"    [PG essays] HTTP {resp.status_code}", file=sys.stderr)
        return []
    feed = feedparser.parse(resp.content)
    since = datetime.now(timezone.utc) - timedelta(days=days)

    if feed.bozo and not feed.entries:
        print(f"    [PG essays] feed parse error - {feed.bozo_exception}", file=sys.stderr)
    if not feed.entries:
        print(f"    [PG essays] 0 entries in feed", file=sys.stderr)

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
