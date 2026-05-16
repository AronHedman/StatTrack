from datetime import datetime, timezone

def ensure_utc(dt):
    if dt is None:
        return None

    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc)

def to_db_utc(dt):
    dt = ensure_utc(dt)
    if dt is None:
        return None
    return dt.replace(tzinfo=None)


def parse_uts(track):
    """
    Convert Last.fm UTS → UTC datetime
    """
    uts = track.get("date", {}).get("uts")

    if not uts:
        return None

    try:
        return datetime.fromtimestamp(int(uts), tz=timezone.utc)
    except Exception:
        return None