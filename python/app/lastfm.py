import os
import requests
import json
import re
from dotenv import load_dotenv
import db

load_dotenv()
API_KEY = os.getenv("LASTFM_API_KEY")

def fetch_recent_tracks(username, limit=1):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getrecenttracks",
        "user": username,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
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
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("user")
    return None

def clean_track_title(title):
    patterns = [
        r"\s*[\(\-\[].*?(?:remaster|remix|version|live|deluxe|anniversary|digitally|edit|bonus|radio).*[\)\]]?",
        r"\s*[\(\-\[].*?\d{4}.*?[\)\]]?" # Catches years like (2004) or - 2012
    ]
    
    clean_title = title
    for pattern in patterns:
        # flags=re.IGNORECASE ensures "REMIX" and "remix" are both caught
        clean_title = re.sub(pattern, "", clean_title, flags=re.IGNORECASE)
    
    return clean_title.strip()

def process_data(api_return):
    array = []
    for track in api_return:
        if track["artist"]["#text"] != None:
            artist = track["artist"]["#text"]
        else:
            continue
        
        if track["name"] != None:
            title = track["name"]
        else:
            continue
        
        clean_title = clean_track_title(title)
        print(clean_title)

        array.append({"artist": artist, "song": clean_title})

    return array