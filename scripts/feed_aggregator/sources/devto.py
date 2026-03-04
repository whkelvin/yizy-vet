"""Fetch top Dev.to articles from the past N days."""

import feedparser


def fetch_devto_top(top=1):
    feed = feedparser.parse(f"https://dev.to/feed?top={top}")
    return [{"title": e.title, "url": e.link} for e in feed.entries]
