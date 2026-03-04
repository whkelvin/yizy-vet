"""Fetch recent YouTube videos from subscribed channels."""

import re
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests


def _resolve_channel_id(handle):
    """Fetch a YouTube channel page and extract the channel ID."""
    resp = requests.get(f"https://www.youtube.com/@{handle}", headers={
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    })
    if not resp.ok:
        return None
    match = re.search(r'channel_id=([^"&]+)', resp.text)
    return match.group(1) if match else None


def _parse_feed(xml_text):
    """Parse a YouTube RSS feed and return list of (published, videoId, title)."""
    root = ET.fromstring(xml_text)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }
    entries = []
    for entry in root.findall("atom:entry", ns):
        vid = entry.findtext("yt:videoId", namespaces=ns)
        title = entry.findtext("atom:title", namespaces=ns)
        published = entry.findtext("atom:published", namespaces=ns)
        if vid and title and published:
            entries.append((published, vid, title))
    return entries


def _fetch_channel_videos(handle, since):
    """Fetch videos for a single channel handle, filtered by date."""
    cid = _resolve_channel_id(handle)
    if not cid:
        return []

    resp = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")
    if not resp.ok:
        return []

    videos = []
    for published, vid, title in _parse_feed(resp.text):
        pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
        if pub_dt >= since:
            videos.append({"title": title, "youtubeId": vid})
    return videos


def fetch_yt_videos(channels_file=None, days=1):
    if channels_file is None:
        channels_file = Path(__file__).resolve().parents[2] / "youtube-channels.txt"

    since = datetime.now(timezone.utc) - timedelta(days=days)

    handles = []
    with open(channels_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            handles.append(line.lstrip("@"))

    videos = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(_fetch_channel_videos, h, since) for h in handles]
        for f in futures:
            videos.extend(f.result())

    return videos
