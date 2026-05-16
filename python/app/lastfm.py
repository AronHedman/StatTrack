import os
import requests
import re
from dotenv import load_dotenv
from datetime import datetime, timezone

import helpers as h

load_dotenv()
API_KEY = os.getenv("LASTFM_API_KEY")


def verify_user(username):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getinfo",
        "user": username,
        "api_key": API_KEY,
        "format": "json",
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("user")
    except Exception:
        return None


def fetch_recent_tracks(username, limit, page):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getrecenttracks",
        "user": username,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit,
        "page": page,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("recenttracks", {}).get("track", [])
    except Exception as e:
        print(f"Fel vid Last.fm-anrop: {e}")
        return None


def clean_track_title(title):
    patterns = [
        r"\s*[\(\-\[].*?(?:remaster|remastered|remix|version|live|deluxe|anniversary|with|edit|bonus|radio|feat).*",
        r"\s*[\(\-\[].*?\d{4}.*?[\)\]]?",
    ]

    clean_title = title
    for pattern in patterns:
        clean_title = re.sub(pattern, "", clean_title, flags=re.IGNORECASE)

    return clean_title.strip()


def extract_images(track):
    images = {
        "small": None,
        "medium": None,
        "large": None,
        "extralarge": None,
    }

    track_images = track.get("image")

    if isinstance(track_images, list):
        for img in track_images:
            size = img.get("size")
            url = img.get("#text")
            if size in images and url:
                images[size] = url

    return images


def process_data(api_return):
    result = []

    for track in api_return:
        # Skip currently playing (no timestamp)
        if track.get("@attr", {}).get("nowplaying") == "true":
            continue

        artist = track.get("artist", {}).get("#text")
        title = track.get("name")

        if not artist or not title:
            continue

        dt = h.parse_uts(track)
        if not dt:
            continue

        images = extract_images(track)

        result.append(
            {
                "artist": artist,
                "title_cleaned": clean_track_title(title),
                "title_original": title,
                "date_time": dt,
                "small": images["small"],
                "medium": images["medium"],
                "large": images["large"],
                "extralarge": images["extralarge"],
            }
        )

    result.sort(key=lambda x: x["date_time"], reverse=True)

    return result
