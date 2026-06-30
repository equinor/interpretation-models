import datetime

from interpretation_models.mappers.helpers import convert_date_to_utc, id_generate, localize_date


def test_convert_date_to_utc_normal_time():
    """CET (normal time): UTC+1, so UTC should be 1 hour less."""
    local_date = datetime.datetime(2025, 1, 15, 12, 0, 0)
    result = convert_date_to_utc(local_date, timezone="Europe/Oslo")
    assert result.hour == 11
    assert result.tzname() == "UTC"
    assert result.utcoffset() == datetime.timedelta(hours=0)


def test_convert_date_to_utc_daylight_saving():
    """CEST (daylight saving): UTC+2, so UTC should be 2 hours less."""
    local_date = datetime.datetime(2025, 7, 15, 12, 0, 0)
    result = convert_date_to_utc(local_date, timezone="Europe/Oslo")
    assert result.hour == 10
    assert result.tzname() == "UTC"
    assert result.utcoffset() == datetime.timedelta(hours=0)


def test_localize_date_normal_time():
    """CET (normal time): naive datetime gets +01:00 offset."""
    naive_date = datetime.datetime(2025, 1, 15, 12, 0, 0)
    result = localize_date(naive_date, timezone="Europe/Oslo")
    assert result.utcoffset() == datetime.timedelta(hours=1)
    assert result.hour == 12
    assert result.minute == 0


def test_localize_date_daylight_saving():
    """CEST (daylight saving): naive datetime gets +02:00 offset."""
    naive_date = datetime.datetime(2025, 7, 15, 12, 0, 0)
    result = localize_date(naive_date, timezone="Europe/Oslo")
    assert result.utcoffset() == datetime.timedelta(hours=2)
    assert result.hour == 12
    assert result.minute == 0


def test_id_generate_with_native_id(source_context):
    result = id_generate(source_context, "12345")
    assert result == "SOME_DB:SOME_PROJECT:12345"


def test_id_generate_with_empty_id(source_context):
    result = id_generate(source_context, "")
    assert result == "SOME_DB:SOME_PROJECT:"

def test_id_generate_with_combined_id(source_context):
    result = id_generate(source_context, "something:other_thing:12345")
    assert result == "SOME_DB:SOME_PROJECT:something:other_thing:12345"
