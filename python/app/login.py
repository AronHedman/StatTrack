from flask import Flask, redirect, request, session, jsonify

import db


def check_user(db_conn, username, password):
    cursor = db_conn.cursor(dictionary=True)

    query = "SELECT user_id, password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    results = cursor.fetchall()
    cursor.close()
