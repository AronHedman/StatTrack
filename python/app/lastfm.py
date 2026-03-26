import os
import requests
import json
import re
from dotenv import load_dotenv
from datetime import datetime
import db

load_dotenv()
API_KEY = os.getenv("LASTFM_API_KEY")


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


def verify_user(username):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getinfo",
        "user": username,
        "api_key": os.getenv("LASTFM_API_KEY"),
        "format": "json",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("user")
    return None


def clean_track_title(title):
    patterns = [  # regex
        r"\s*[\(\-\[].*?(?:remaster|remastered|remix|version|live|deluxe|anniversary|with|edit|bonus|radio|feat).*",
        r"\s*[\(\-\[].*?\d{4}.*?[\)\]]?",  # Catches years like (2004) or - 2012
    ]

    clean_title = title
    for pattern in patterns:
        # flags=re.IGNORECASE ensures "REMIX" and "remix" are both caught
        clean_title = re.sub(pattern, "", clean_title, flags=re.IGNORECASE)

    return clean_title.strip()


def format_time(time):
    # 18 Mar 2026, 14:35
    try:
        dt = datetime.strptime(time, "%d %b %Y, %H:%M")

        # ISO 8601 string (2026-03-18T14:35:00)
        return dt.isoformat()
    except ValueError:

        return None


def process_data(api_return):
    array = []
    for track in api_return:
        if track.get("@attr") and track.get("@attr").get("nowplaying") == "true":
            continue

        if track.get("artist") and track.get("artist").get("#text") != None:
            artist = track.get("artist").get("#text")
        else:
            continue

        if track.get("name") != None:
            title = track.get("name")
        else:
            continue

        if track.get("date") and track.get("date").get("#text") != None:
            date_time = track.get("date").get("#text")
        else:
            continue

        clean_title = clean_track_title(title)

        timestamp = format_time(date_time)

        if timestamp == None:
            continue

        array.append(
            {
                "artist": artist,
                "title_cleaned": clean_title,
                "title_original": title,
                "date_time": timestamp,
            }
        )

    return array
