from flask import Flask, redirect, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import db


def check_username(db_conn, username):
    cursor = db_conn.cursor(dictionary=True)

    query = "SELECT user_id FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    results = cursor.fetchone()
    cursor.close()

    if results:
        return True
    else:
        return False


def verify_user(db_conn, username, password):
    cursor = db_conn.cursor(dictionary=True)
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()  # Depends on username being unique?
    cursor.close()

    if result:
        return check_password_hash(
            result["password"], password
        )  # chack password or return false
    return False


def new_user(db_conn, username, password):
    cursor = db_conn.cursor(dictionary=True)

    hashed_password = generate_password_hash(password)

    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed_password))

    db_conn.commit()

    cursor.close()

    return
