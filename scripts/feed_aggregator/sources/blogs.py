"""Fetch recent posts from tech company blogs via RSS/Atom."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser

FEEDS = [
    ("Cursor", "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_cursor.xml"),
    ("Google AI", "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_google_ai.xml"),
    ("Cloudflare Dev", "https://blog.cloudflare.com/tag/developers/rss/"),
    ("Stripe Dev", "https://stripe.dev/blog/feed.xml"),
    ("Atlassian Dev", "https://blog.developer.atlassian.com/feed"),
    ("Railway Eng", "https://blog.railway.com/s/engineering/feed"),
    ("Netflix Eng", "https://netflixtechblog.com/feed/tagged/engineering"),
    ("Microsoft Dev", "https://devblogs.microsoft.com/landing"),
    ("Vercel Eng", "https://vercel.com/atom"),
]


def _fetch_feed(name, url, since):
    """Fetch a single feed and return recent posts."""
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


def fetch_blogs(days=1):
    since = datetime.now(timezone.utc) - timedelta(days=days)

    all_posts = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(_fetch_feed, name, url, since) for name, url in FEEDS]
        for f in futures:
            all_posts.extend(f.result())

    return all_posts
