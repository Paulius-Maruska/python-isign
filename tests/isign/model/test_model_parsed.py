from datetime import datetime

from isign.model.parsed import Base64Str, DateTimeStr


def test_datetimestr_can_return_parsed_datetime_object() -> None:
    obj = DateTimeStr("2001-02-03T04:05:06+07:08")
    dt = obj.as_datetime()
    assert isinstance(dt, datetime)
    assert dt.year == 2001
    assert dt.month == 2
    assert dt.day == 3
    assert dt.hour == 4
    assert dt.minute == 5
    assert dt.second == 6
    assert dt.tzinfo is not None


def test_base64str_can_return_decoded_bytes() -> None:
    obj = Base64Str("Zm9v")
    b = obj.as_bytes()
    assert isinstance(b, bytes)
    assert b == b"foo"


def test_base64str_can_return_decoded_str() -> None:
    obj = Base64Str("YmFy")
    b = obj.as_str()
    assert isinstance(b, str)
    assert b == "bar"
