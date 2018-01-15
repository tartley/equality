"""
Unit tests for equality.
"""
from datetime import datetime, timedelta, tzinfo

import pendulum
import pytest

from ..equality import AnyInt, AnyTimestamp

def test_any_int_eq():
    assert AnyInt() == 0
    assert AnyInt() == 1
    assert AnyInt() == -42
    assert AnyInt() == int(1E15)

def test_any_int_not_eq():
    assert not(AnyInt() == 0.0)

def test_any_int_not_ne():
    assert not (AnyInt() != 0)
    assert not (AnyInt() != 1)
    assert not (AnyInt() != -42)
    assert not (AnyInt() != int(1E15))

def test_any_int_ne():
    assert AnyInt() != 0.0

def test_any_int_repr():
    assert repr(AnyInt()) == '<AnyInt>'


T0 = datetime(2017, 12, 31, 17, 59, 0)
MINUS_6 = "2017-12-31T23:58:54-06:00"
MINUS_5 = "2017-12-31T23:58:55-06:00"
T0_STR  = "2017-12-31T23:59:00-06:00"
PLUS_5  = "2017-12-31T23:59:05-06:00"
PLUS_6  = "2017-12-31T23:59:06-06:00"

ZERO = timedelta(0)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return ZERO

def test_any_timestamp_constructor_refuses_timezone():
    with pytest.raises(AssertionError) as exc_info:
        AnyTimestamp(datetime.now(UTC()))
    assert str(exc_info.value) == "Constructor doesn't support timezones"

def test_any_timestamp_eq():
    assert AnyTimestamp(T0, seconds=5) != MINUS_6
    assert AnyTimestamp(T0, seconds=5) == MINUS_5
    assert AnyTimestamp(T0, seconds=5) == PLUS_5
    assert AnyTimestamp(T0, seconds=5) != PLUS_6

def test_any_timestamp_ne():
    assert not (AnyTimestamp(T0, seconds=5) == MINUS_6)
    assert not (AnyTimestamp(T0, seconds=5) != MINUS_5)
    assert not (AnyTimestamp(T0, seconds=5) != PLUS_5)
    assert not (AnyTimestamp(T0, seconds=5) == PLUS_6)

def test_any_timestamp_repr():
    stamp = pendulum.create(2017, 12, 31, 23, 59, 58, tz=-4)
    assert repr(AnyTimestamp(stamp, seconds=123)) == \
        u'<AnyTimestamp 2017-12-31T23:59:58-04:00 +/- 123 secs>', 'x'

def test_parse_timestamp():
    stamp = AnyTimestamp(T0)
    assert stamp.parse_timestamp(PLUS_5) == datetime(2017, 12, 31, 23, 59, 5)

def test_parse_tz_offset():
    stamp = AnyTimestamp(T0)
    assert stamp.parse_tz_offset(PLUS_5) == -6

