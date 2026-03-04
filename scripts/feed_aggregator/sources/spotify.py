"""Fetch recent Spotify podcast episodes."""

import os
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
            shows.append(show_id)

    episodes = []
    for show_id in shows:
        resp = requests.get(
            f"https://api.spotify.com/v1/shows/{show_id}/episodes",
            params={"limit": 10},
            headers={"Authorization": f"Bearer {token}"},
        )
        resp.raise_for_status()
        for ep in resp.json().get("items", []):
            if ep["release_date"] >= since:
                episodes.append({
                    "title": ep["name"],
                    "spotifyEmbedUrl": f"https://open.spotify.com/embed/episode/{ep['id']}",
                })

    return episodes
