"""Fetch recent Spotify podcast episodes."""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests


def fetch_spotify_podcasts(shows_file=None, days=1):
    if shows_file is None:
        shows_file = Path(__file__).resolve().parents[2] / "spotify-shows.txt"

    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]

    # Get access token
    token_resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token_resp.raise_for_status()
    token = token_resp.json()["access_token"]

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Read show IDs
    shows = []
    with open(shows_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            _name, show_id = line.split(":", 1)
            shows.append((_name, show_id))

    episodes = []
    for name, show_id in shows:
        resp = requests.get(
            f"https://api.spotify.com/v1/shows/{show_id}/episodes",
            params={"limit": 10},
            headers={"Authorization": f"Bearer {token}"},
        )
        if not resp.ok:
            print(f"    [Spotify] {name}: HTTP {resp.status_code}", file=sys.stderr)
            continue
        show_eps = resp.json().get("items", [])
        if not show_eps:
            print(f"    [Spotify] {name}: no episodes returned", file=sys.stderr)
        matched = 0
        for ep in show_eps:
            if ep["release_date"] >= since:
                matched += 1
                episodes.append({
                    "title": ep["name"],
                    "spotifyEmbedUrl": f"https://open.spotify.com/embed/episode/{ep['id']}",
                })
        if show_eps and not matched:
            print(f"    [Spotify] {name}: {len(show_eps)} episodes but none since {since}", file=sys.stderr)

    return episodes
