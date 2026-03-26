import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import time

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "statTrack")


def setup():
    retries = 15
    while retries > 0:
        try:
            pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="db_pool",
                pool_size=5,
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=DB_NAME,
            )
            print("DB Connected")
            return pool
        except Error as error:
            print("Pool conn failed: {error}")
            retries -= 1
            time.sleep(2)  # wait a few seconds to geiv the db time to start up
    raise Exception("Failed to connect to database after 30 seconds")


db_pool = setup()


def get_connection():
    conn = db_pool.get_connection()

    try:
        conn.ping(reconnect=True, attempts=3, delay=1)
    except Error:
        pass

    try:
        conn.database = DB_NAME
    except Error:
        cursor = conn.cursor()
        cursor.execute(f"USE {DB_NAME}")
        cursor.close()
    return conn


def fetch_user_id(conn, username):
    cursor = conn.cursor(dictionary=True)

    query = "SELECT user_id FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user_id = cursor.fetchone()["user_id"]

    cursor.close()

    return user_id


def fetch_last_synced(conn, user_id):
    cursor = conn.cursor(dictionary=True)

    query = "SELECT last_synced_datetime FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    last_synced_datetime = cursor.fetchone()["last_synced_datetime"]

    cursor.close()

    return last_synced_datetime


def fetch_artist_id(conn, artist):
    cursor = conn.cursor(dictionary=True)

    query = "SELECT artist_id FROM artists WHERE artist_name = %s"
    cursor.execute(query, (artist,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result["artist_id"]
    return None


def fetch_track_ids(conn, method, value):
    cursor = conn.cursor(dictionary=True)

    if method == "artist_id":
        query = "SELECT song_id FROM songs WHERE artist_id = %s"
        cursor.execute(query, (value,))
        result = cursor.fetchall()
        song_ids = [row["song_id"] for row in result]

    elif method == "title":
        query = "SELECT song_id FROM songs WHERE title = %s"
        cursor.execute(query, (value,))
        result = cursor.fetchall()
        song_ids = [row["song_id"] for row in result]

    cursor.close()
    return song_ids


def fetch_track_name(conn, id):
    cursor = conn.cursor(dictionary=True)

    query = "SELECT title FROM songs WHERE song_id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result["title"]
    return None


def new_last_synced(conn, user_id, new_time):
    cursor = conn.cursor(dictionary=True)

    query = "UPDATE users SET last_synced_datetime = %s WHERE user_id = %s"
    cursor.execute(query, (new_time, user_id))

    conn.commit()
    cursor.close()


def add_track(cursor, user_id, track):
    query = "INSERT IGNORE INTO artists (artist_name) VALUES (%s)"
    cursor.execute(query, (track["artist"],))

    query = "SELECT artist_id FROM artists WHERE artist_name = %s"
    cursor.execute(query, (track["artist"],))
    artist_id = cursor.fetchone()["artist_id"]

    query = "INSERT IGNORE INTO songs (artist_id, title) VALUES (%s, %s)"
    cursor.execute(query, (artist_id, track["title_cleaned"]))

    query = "SELECT song_id FROM songs WHERE title = %s AND artist_id = %s"
    cursor.execute(query, (track["title_cleaned"], artist_id))
    song_id = cursor.fetchone()["song_id"]

    query = "INSERT IGNORE INTO play_history (user_id, song_id, played_at_datetime) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE played_at_datetime = played_at_datetime"  # this 'on duplicate key update ... is not really doing anyhing except that if is a duplicate i will make cursor.rowcount == 2 instead of 1
    cursor.execute(query, (user_id, song_id, track["date_time"]))

    if cursor.rowcount == 1:
        query = "INSERT INTO user_song_stats (user_id, song_id, stream_count) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE stream_count = stream_count + 1"
        cursor.execute(query, (user_id, song_id))

        query = "INSERT INTO user_artist_stats (user_id, artist_id, stream_count) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE stream_count = stream_count + 1"
        cursor.execute(query, (user_id, artist_id))
