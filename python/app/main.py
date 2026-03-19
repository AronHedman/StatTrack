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
    return g.db


@app.teardown_appcontext
def close_db(error):
    db_conn = g.pop("db", None)
    if db_conn is not None:
        db_conn.close()  # Returns connection to the pool


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or password:
        return jsonify({"error": "Username or password missing"}), 400

    # Kolla om användaren finns hos LastFM
    user_info = lastfm.verify_user(username)

    if user_info:
        if login.check_users(g.db, username, password):
            session["user"] = {"username": user_info["name"]}
            return jsonify({"success": True})
        else:
            return (
                jsonify(
                    {"success": False, "message": "Last.fm-användaren hittades inte"}
                ),
                404,
            )


@app.route("/signup", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or password:
        return jsonify({"error": "Username or password missing"}), 400

    # Kolla om användaren finns hos LastFM
    user_info = lastfm.verify_user(username)

    if user_info:
        if login.check_users(g.db, username, password):
            session["user"] = {"username": user_info["name"]}
            return jsonify({"success": True})
        else:
            return (
                jsonify(
                    {"success": False, "message": "Last.fm-användaren hittades inte"}
                ),
                404,
            )


@app.route("/callback")
def callback():

    return


@app.route("/stats")
def get_stats():
    # Hämta användarnamnet från sessionen som vi sparade i /login
    user = session.get("user")
    if not user:
        return jsonify({"error": "Inte inloggad"}), 401

    username = user["username"]
    tracks = lastfm.fetch_recent_tracks(username)

    if tracks is None:
        return jsonify({"error": "Kunde inte hämta data från Last.fm"}), 500

    tracks = lastfm.process_data(tracks)
    return jsonify(tracks)  # change to tracks


@app.route("/hello")
def hello():
    return jsonify({"message": "Hello from Python!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
