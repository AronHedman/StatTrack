import os
from flask import Flask, redirect, request, session, jsonify, g
from flask_cors import CORS
from datetime import timedelta, datetime
import requests
import json
import traceback

from werkzeug.security import generate_password_hash
from werkzeug.exceptions import HTTPException

import login
import lastfm
import db
import ranking
import helpers as h

'''
command to dump the database:

docker exec -i mariadb mariadb-dump -u root -p12345 --routines --events --triggers stattrack > ./db_init/schema.sql
'''


app = Flask(__name__)
app.secret_key = os.environ.get(
    "APP_SECRET", "dev-secret-key-change-me"
)  # change to ("SECRET_KEY", os.urandom(32)) when actually implemenmts a env var for SECRET_KEY

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # True in production (HTTPS)
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
)

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


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception("Unhandled error")
    if isinstance(e, HTTPException):
        return jsonify(error=str(e.description)), e.code
    return jsonify(success=False, message=str(e)), 500


@app.route("/me", methods=["GET"])  # returns user information on the current user
def me():
    user = session.get("user")
    if not user:
        return jsonify({"authenticated": False}), 401

    return jsonify({"authenticated": True, "user": user})

def get_current_user():
    user = session.get("user")
    if not user:
        return None, None
    return user["user_id"], user["username"]


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
            session.permanent = True
            user_id=db.fetch_user_id(g.db, username)
            session["user"] = {"username": user_info["name"], "user_id": user_id}
            return jsonify({"success": True})
        else:
            return (
                jsonify(
                    {"success": False, "message": "Incorrect username or password"}
                ),
                409,
            )
    else:
        return jsonify({"success": False, "message": "Couldn't fetch Last.FM user"})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})


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
            session.permanent = True
            user_id=db.fetch_user_id(g.db, username)
            session["user"] = {"username": user_info["name"], "user_id": user_id}
            return jsonify({"success": True})

    else:
        return jsonify(
            {
                "success": False,
                "message": "To use this program, please head to {https://www.last.fm/join} and create an account. Then sing in here with the same username",
            }
        )


@app.route("/callback")
def callback():

    return


@app.route("/fetch-recent")
def get_stats():
    user_id, username = get_current_user()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    tracks = lastfm.fetch_recent_tracks(username, 50, 1)

    if tracks is None:
        return jsonify({"error": "Kunde inte hämta data från Last.fm"}), 500

    tracks = lastfm.process_data(tracks)
    return jsonify(tracks)


@app.route("/update-db")
def update_db():
    user_id, username = get_current_user()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    last_synced_datetime = h.ensure_utc(db.fetch_last_synced(g.db, user_id))

    cursor = g.db.cursor(dictionary=True)
    page = 1
    new_last_synced = None

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
                track_dt = h.ensure_utc(track["date_time"])

                if last_synced_datetime and track_dt <= last_synced_datetime:
                    found_old_track = True
                    break

                track_to_store = dict(track)
                track_to_store["date_time"] = h.to_db_utc(track_dt)
                db.add_track(cursor, user_id, track_to_store)

            g.db.commit()

            if found_old_track:
                break

            page += 1

        if new_last_synced:
            db.new_last_synced(g.db, user_id, h.to_db_utc(new_last_synced))

    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

    return jsonify(tracks)


@app.route("/fetch/tracks", methods=["GET"])
def fetch_tracks():
    artist = request.args.get("artist")
    artist_id = request.args.get("artist_id")
    title = request.args.get("title")
    song_id = request.args.get("song_id")

    if not artist and not title and not artist_id and not song_id:
        return jsonify([])

    cursor = g.db.cursor(dictionary=True)

    try:
        query = """
            SELECT
                s.song_id,
                s.title,
                s.artist_id,
                a.artist_name,
                s.extralarge,
                s.large,
                s.medium,
                s.small
            FROM songs s
            JOIN artists a ON s.artist_id = a.artist_id
        """

        conditions = []  #adds WHERE conditions
        params = [] #adds params %s for each condition

        if artist:
            conditions.append("(a.artist_name = %s OR a.artist_name LIKE %s)")
            params.extend([artist, f"%{artist}%"])

        if artist_id:
            conditions.append("s.artist_id = %s")
            params.append(artist_id)

        if title:
            conditions.append("(s.title = %s OR s.title LIKE %s)")
            params.extend([title, f"%{title}%"])

        if song_id:
            conditions.append("s.song_id = %s")
            params.append(song_id)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)  # add WHERE and then joins the conditions with AND as the separator

        query += " ORDER BY s.title ASC, LENGTH(s.title) ASC LIMIT 100"

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        return jsonify(results)

    finally:
        cursor.close()
   


@app.route("/fetch/artists", methods=["GET"])
def fetch_artists():
    artist = request.args.get("artist")

    if not artist:
        return jsonify([])

    artists = db.fetch_artist(g.db, artist)

    if artists is None:
        return jsonify([])

    return jsonify(artists)


@app.route("/fetchtop/artists")
def fetchtop_artists():
    user_id, username = get_current_user()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    cursor = g.db.cursor(dictionary=True)

    try:
        query = """
        SELECT uas.artist_id, uas.stream_count, a.artist_name
        FROM user_artist_stats uas
        JOIN artists a ON a.artist_id = uas.artist_id
        WHERE user_id = %s
        ORDER BY stream_count DESC LIMIT 5
        """
        cursor.execute(query, (user_id,))

        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        g.db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 

@app.route("/fetchtop/songs")
def fetchtop_songs():
    user_id, username = get_current_user()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    
    artist_id = request.args.get("artist_id")

    cursor = g.db.cursor(dictionary=True)

    if not artist_id:
        try:
            query = """
                SELECT uss.song_id, uss.stream_count, s.title, s.artist_id, a.artist_name, s.extralarge 
                FROM user_song_stats uss
                JOIN songs s ON s.song_id = uss.song_id
                JOIN artists a ON a.artist_id = s.artist_id
                WHERE user_id = %s 
                ORDER BY stream_count DESC LIMIT 5
            """
            cursor.execute(query, (user_id,))

            results = cursor.fetchall()
            return jsonify(results)
        except Exception as e:
            g.db.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
    else:
        try:
            query = """
                SELECT uss.song_id, uss.stream_count, s.title, s.artist_id, a.artist_name, s.extralarge 
                FROM user_song_stats uss
                JOIN songs s ON s.song_id = uss.song_id
                JOIN artists a ON a.artist_id = s.artist_id
                WHERE user_id = %s and s.artist_id = %s
                ORDER BY stream_count DESC LIMIT 5
            """
            cursor.execute(query, (user_id, artist_id))

            results = cursor.fetchall()
            return jsonify(results)
        except Exception as e:
            g.db.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()



@app.route("/ranking/user", methods=["POST"])
def save_ranking():
    user_id, username = get_current_user()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    artist_id = data.get("artist_id")
    rankings = data.get("rankings")

    # rankings should look like: [{"song_id": 15, "rank": 1}, {"song_id": 42, "rank": 2}, ...]

    if not artist_id or not isinstance(rankings, list):
        return (
            jsonify({"error": "Missing artist_id or wrong ranking format"}),
            400,
        )
    
    try:
        ranking.save_user_ranking(g.db, user_id, artist_id, rankings)
        return jsonify({"success": True, "message": "Ranking saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ranking/user", methods=["GET"])
def get_user_ranking():
    user_id, username = get_current_user()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    artist_id = request.args.get("artist_id")
    if not artist_id:
        return jsonify({"error": "Missing artist_id parameter"}), 400

    try:
        rankings = ranking.fetch_user_ranking(g.db, user_id, artist_id)

        return jsonify(rankings)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ranking/global", methods=["GET"])
def get_global_ranking():
    artist_id = request.args.get("artist_id")

    if not artist_id:
        return jsonify({"error": "Missing artist_id parameter"}), 400

    try:
        results = ranking.fetch_global_ranking(g.db, artist_id)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
