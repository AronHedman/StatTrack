import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("LASTFM_API_KEY")

def fetch_recent_tracks(username, limit=100):
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