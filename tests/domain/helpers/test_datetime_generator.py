from datetime import datetime, timezone

from app.domain.helpers.datetime_generator import get_now_datetime


def test_get_now_datetime_type_and_timezone():
    now = get_now_datetime()
    assert isinstance(now, datetime)
    assert now.tzinfo == timezone.utc


def test_get_now_datetime_value_close_to_real_time():
    now = get_now_datetime()
    real_now = datetime.now(timezone.utc)

    diff = abs((real_now - now).total_seconds())
    assert diff < 1
