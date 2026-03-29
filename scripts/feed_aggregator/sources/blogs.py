"""Fetch recent posts from tech company blogs via RSS/Atom."""

import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from time import mktime

import feedparser
import requests

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FeedAggregator/1.0)",
    "Accept": "application/rss+xml, application/xml, text/xml",
}

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
    ("Netflix Eng", "https://netflixtechblog.com/feed/tagged/engineering"),
    ("Microsoft DevOps", "https://devblogs.microsoft.com/devops/feed/"),
    ("Vercel Eng", "https://vercel.com/atom"),
]


def _fetch_feed(name, url, since):
    """Fetch a single feed and return recent posts."""
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=15)
    except requests.RequestException as exc:
        print(f"    [Blogs] {name}: request failed - {exc}", file=sys.stderr)
        return []
    if not resp.ok:
        print(f"    [Blogs] {name}: HTTP {resp.status_code}", file=sys.stderr)
        return []
    feed = feedparser.parse(resp.content)
    if feed.bozo and not feed.entries:
        print(f"    [Blogs] {name}: feed parse error - {feed.bozo_exception}", file=sys.stderr)
    if not feed.entries:
        print(f"    [Blogs] {name}: 0 entries in feed", file=sys.stderr)
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
