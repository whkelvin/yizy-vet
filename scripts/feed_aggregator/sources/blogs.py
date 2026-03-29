"""Fetch recent posts from tech company blogs via RSS/Atom."""

import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser

FEEDS = [
    ("Anthropic News", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_anthropic_news.xml"),
    ("Anthropic Engineering", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_anthropic_engineering.xml"),
    ("Anthropic Research", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_anthropic_research.xml"),
    ("Anthropic Frontier Red Team", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_anthropic_red.xml"),
    ("Claude Code Changelog", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_anthropic_changelog_claude_code.xml"),
    ("Anthropic", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_anthropic.xml"),
    ("OpenAI Developer Blog", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_openai_developer.xml"),
    ("OpenAI Research", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_openai_research.xml"),
    ("Cursor", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_cursor.xml"),
    ("Google AI", "https://raw.githubusercontent.com/whkelvin/rss/main/feeds/feed_google_ai.xml"),
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
    status = getattr(feed, "status", None)
    if feed.bozo:
        print(f"    [Blogs] {name}: feed error - {feed.bozo_exception}", file=sys.stderr)
    if status and status != 200:
        print(f"    [Blogs] {name}: HTTP {status}", file=sys.stderr)
    if not feed.entries:
        print(f"    [Blogs] {name}: 0 entries in feed (status={status})", file=sys.stderr)
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
