from datetime import datetime, timezone


def get_now_datetime() -> datetime:
    """
    Returns the current date and time in UTC.
    """
    return datetime.now(timezone.utc)
