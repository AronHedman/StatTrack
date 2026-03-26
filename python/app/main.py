# pyright: reportMissingImports=false

import os
from flask import Flask, redirect, request, session, jsonify, g
from flask_cors import CORS
import requests
import json

from werkzeug.security import generate_password_hash

import login
import lastfm
import db

app = Flask(__name__)
app.secret_key = "12345"  # måste fixa en secret generator...

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "http://localhost",
                "http://127.0.0.1",
                "http://127.0.0.1:5173",
            ]
        }
    },
    supports_credentials=True,
)


@app.before_request
def connect_db():
    if "db" not in g:
        g.db = db.get_connection()


@app.teardown_appcontext
def close_db(error):
    db_conn = g.pop("db", None)
    if db_conn is not None:
        db_conn.close()  # Returns connection to the pool


@app.route("/login", methods=["POST"])
def handle_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username or password missing"}), 400

    # Kolla om användaren finns hos LastFM
    user_info = lastfm.verify_user(username)

    if user_info:
        if login.verify_user(g.db, username, password):
            session["user"] = {"username": user_info["name"]}
            return jsonify({"success": True})
        else:
            return (
                jsonify(
                    {"success": False, "message": "Incorrect username or password"}
                ),
                409,
            )
    else:
        return jsonify({"Success": False, "message": "Couldn't fetch Last.FM user"})


@app.route("/signup", methods=["POST"])
def handle_signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username or password missing"}), 400

    # Kolla om användaren finns hos LastFM
    user_info = lastfm.verify_user(username)

    if user_info:
        if login.check_username(g.db, username):
            return (
                jsonify({"success": False, "message": "Username is already taken"}),
                409,
            )
        else:
            login.new_user(g.db, username, password)
            session["user"] = {"username": user_info["name"]}
            return jsonify({"success": True})

    else:
        return jsonify(
            {
                "Success": False,
                "message": "To use this program, please head to {https://www.last.fm/join} and create an account. Then sing in here with the same username",
            }
        )


@app.route("/callback")
def callback():

    return


@app.route("/fetch-recent")
def get_stats():
    user = session.get("user")
    if not user:
        return jsonify({"error": "Inte inloggad"}), 401

    username = user["username"]
    tracks = lastfm.fetch_recent_tracks(username, 50, 1)

    if tracks is None:
        return jsonify({"error": "Kunde inte hämta data från Last.fm"}), 500

    tracks = lastfm.process_data(tracks)
    return jsonify(tracks)


@app.route("/update-db")
def update_db():
    user = session.get("user")
    if not user:
        return jsonify({"error": "Inte inloggad"}), 401

    username = user["username"]
    user_id = db.fetch_user_id(g.db, username)

    last_synced_raw = db.fetch_last_synced(g.db, user_id)
    last_synced_datetime = last_synced_raw.isoformat() if last_synced_raw else None
    new_last_synced = False

    cursor = g.db.cursor(dictionary=True)
    page = 1
    try:
        while True:
            found_old_track = False
            raw_tracks = lastfm.fetch_recent_tracks(username, 50, page)

            if not raw_tracks:
                break

            tracks = lastfm.process_data(raw_tracks)

            if not tracks:
                break

            if page == 1:
                new_last_synced = tracks[0]["date_time"]

            for track in tracks:
                if last_synced_datetime and track["date_time"] == str(
                    last_synced_datetime
                ):
                    found_old_track = True
                    break

                db.add_track(cursor, user_id, track)

            g.db.commit()
            if found_old_track:
                break
            page += 1

        if new_last_synced:
            db.new_last_synced(g.db, user_id, new_last_synced)
    except Exception as e:
        g.db.rollback()  # to avoid committing a faulty dataset
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

    return jsonify(tracks)


@app.route("/fetch-tracks", methods=["GET"])
def fetch_tracks():
    artist = request.args.get("artist")

    if not artist:
        return jsonify([])

    # Update everything here to be able to handle more song data like album covers, artist name etc

    artist_id = db.fetch_artist_id(g.db, artist)

    if artist_id is None:
        return jsonify([])

    track_ids = db.fetch_track_ids(g.db, "artist_id", artist_id)

    track_names = []
    for id in track_ids:
        track_name = db.fetch_track_name(g.db, id)
        if track_name:
            track_names.append(track_name)

    return jsonify(track_names)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
