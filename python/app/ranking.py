def save_user_ranking(conn, user_id, artist_id, rankings):
    # rankings expects a list of dicts: [{"song_id": 123, "rank": 1}, ...]
    cursor = conn.cursor()
    try:
        # Wipe user's previous ranking for artist
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


def fetch_user_ranking(conn, user_id, artist_id):
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            r.song_id,
            r.rank,
            s.title,
            s.artist_id,
            a.artist_name,
            s.extralarge,
            s.large,
            s.medium,
            s.small
        FROM user_artist_rankings r
        JOIN songs s ON s.song_id = r.song_id
        JOIN artists a ON a.artist_id = s.artist_id
        WHERE r.user_id = %s
          AND r.artist_id = %s
        ORDER BY r.rank ASC
    """

    cursor.execute(query, (user_id, artist_id))
    results = cursor.fetchall()
    cursor.close()

    return results


def fetch_global_ranking(conn, artist_id):
    cursor = conn.cursor(dictionary=True)
    # Fetch top 10 from computed view

    query = "SELECT song_id, title, quality_score FROM global_artist_rankings WHERE artist_id = %s LIMIT 10"
    cursor.execute(query, (artist_id,))
    results = cursor.fetchall()
    cursor.close()
    return results
