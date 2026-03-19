# pyright: reportMissingImports=false

import os
from flask import Flask, redirect, request, session, jsonify
from flask_cors import CORS    
import requests
import json

import lastfm
import db

app = Flask(__name__)
app.secret_key = "12345" #måste fixa en secret generator...

CORS(app, resources={r"/*": {"origins": [
            "http://localhost:5173", 
            "http://localhost", 
            "http://127.0.0.1", 
            "http://127.0.0.1:5173"]
            }}, supports_credentials=True)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    
    if not username:
        return jsonify({"error": "Användarnamn saknas"}), 400

    # Kolla om användaren finns
    user_info = lastfm.verify_user(username)
    
    if user_info:
        # Spara i Flask-sessionen
        session["user"] = {
            "username": user_info["name"],
            "image": user_info["image"][-1]["#text"] if user_info["image"] else None
        }
        #db.getDb() #maybe here? await user before establishing db connection here?
        return jsonify({"success": True, "user": session["user"]})
    
    return jsonify({"success": False, "message": "Last.fm-användaren hittades inte"}), 404


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
    
    tracks2 = lastfm.process_data(tracks)
    print(tracks2)
    return jsonify([tracks, tracks2]) #change to tracks

@app.route("/hello")
def hello():
    return jsonify({"message": "Hello from Python!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)