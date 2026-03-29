"""Smoke test — verify each feed source can fetch items without errors.

Usage:
    python -m tests.smoke_test          # default 7-day window
    python -m tests.smoke_test --days 30
"""

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from sources.blogs import fetch_blogs
from sources.claude_blog import fetch_claude_blog
from sources.pg_essays import fetch_pg_essays
from sources.substack import fetch_substack
from sources.youtube import fetch_yt_videos
from sources.gh_trending import fetch_gh_trending


SOURCES = [
    ("Blogs", lambda days: fetch_blogs(days=days)),
    ("Claude Blog", lambda days: fetch_claude_blog(days=days)),
    ("Paul Graham", lambda days: fetch_pg_essays(days=days)),
    ("Substack", lambda days: fetch_substack(days=days)),
    ("YouTube", lambda days: fetch_yt_videos(days=days)),
    ("GitHub Trending", lambda _: fetch_gh_trending()),
]


def run(days):
    print(f"Fetching with {days}-day window...\n")
    passed = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=6) as pool:
        future_to_name = {
            pool.submit(fn, days): name for name, fn in SOURCES
        }
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                items = future.result()
                status = f"\u2713 {name}: {len(items)} items"
                print(status)
                for item in items:
                    title = item.get("title") or item.get("name", "?")
                    url = item.get("url") or ""
                    if "youtubeId" in item:
                        url = f"https://youtube.com/watch?v={item['youtubeId']}"
                    print(f"    {url}  {title}  [{name}]")
                passed += 1
            except Exception as e:
                print(f"\u2717 {name}: ERROR - {e}")
                failed += 1

    print(f"\n{'='*40}")
    print(f"Passed: {passed}  Failed: {failed}")
    return failed == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    ok = run(args.days)
    sys.exit(0 if ok else 1)
