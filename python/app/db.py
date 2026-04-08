import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import time
import sys

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "statTrack")


def setup():
    retries = 15
    while retries > 0:
        try:
            pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="db_pool",
                pool_size=10,
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=DB_NAME,
            )
            print("DB Connected")
            return pool
        except Error as error:
            print(f"Pool conn failed: {error}")
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
    exact_result = cursor.fetchone()

    if exact_result:
        cursor.close()
        return [exact_result["artist_id"]]

    query_partial = "SELECT artist_id FROM artists WHERE artist_name LIKE %s"
    cursor.execute(query_partial, (f"%{artist}%",))
    results = cursor.fetchall()
    cursor.close()

    return [row["artist_id"] for row in results]


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
    try:
        query = "INSERT IGNORE INTO artists (artist_name) VALUES (%s)"
        cursor.execute(query, (track["artist"],))

        query = "SELECT artist_id FROM artists WHERE artist_name = %s"
        cursor.execute(query, (track["artist"],))

        artist = cursor.fetchone()
        if not artist:
            return

        artist_id = artist["artist_id"]

        query = "INSERT IGNORE INTO songs (artist_id, title) VALUES (%s, %s)"
        cursor.execute(query, (artist_id, track["title_cleaned"]))

        query = "SELECT song_id FROM songs WHERE title = %s AND artist_id = %s"
        cursor.execute(query, (track["title_cleaned"], artist_id))

        song = cursor.fetchone()
        if not song:
            return

        song_id = song["song_id"]

        query = "INSERT IGNORE INTO play_history (user_id, song_id, played_at_datetime) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE played_at_datetime = played_at_datetime"  # this 'on duplicate key update ... is not really doing anyhing except that if is a duplicate i will make cursor.rowcount == 2 instead of 1
        cursor.execute(query, (user_id, song_id, track["date_time"]))

        # some coding wizardry to make sure that the duplicates are detected...
        if cursor.rowcount == 1:
            query = "INSERT INTO user_song_stats (user_id, song_id, stream_count) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE stream_count = stream_count + 1"
            cursor.execute(query, (user_id, song_id))

            query = "INSERT INTO user_artist_stats (user_id, artist_id, stream_count) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE stream_count = stream_count + 1"
            cursor.execute(query, (user_id, artist_id))

        valid_cols = {"extralarge", "large", "medium", "small"}
        for size, url in track.get("images", {}).items():
            if size in valid_cols and url:
                query = f"UPDATE songs SET {size} = %s WHERE song_id = %s"
                cursor.execute(query, (url, song_id))

    except Exception as e:
        print(f"CRITICAL ERROR in add_track: {str(e)}", file=sys.stderr)
        raise e  # Re-raise so Flask shows the error if debug is on
