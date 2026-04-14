def save_user_ranking(conn, user_id, artist_id, rankings):
    # rankings expects a list of dicts: [{"song_id": 123, "rank": 1}, ...]
    cursor = conn.cursor()
    try:
        # Wipe the user's previous ranking for this artist
        query = "DELETE FROM user_artist_rankings WHERE user_id = %s AND artist_id = %s"
        cursor.execute(query, (user_id, artist_id))

        # Insert new Top 10 (or fewer)
        query = "INSERT INTO user_artist_rankings (user_id, artist_id, song_id, rank) VALUES (%s, %s, %s, %s)"
        for item in rankings:
            cursor.execute(query, (user_id, artist_id, item["song_id"], item["rank"]))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def get_global_ranking(conn, artist_id):
    cursor = conn.cursor(dictionary=True)
    # Fetch top 10 from our computed view

    query = "SELECT song_id, title, quality_score FROM global_artist_rankings WHERE artist_id = %s LIMIT 10"
    cursor.execute(query, (artist_id,))
    results = cursor.fetchall()
    cursor.close()
    return results
