import datetime

from mappers.metadata_ow import convert_date_to_utc, localize_date, id_generate
from models.metadata import SourceContext, SourceMetadata
from models.enums import SourceSystem


def test_id_generate_with_native_id():
    context = SourceContext(database="MY_DB", project="MY_PROJECT")
    result = id_generate(context, "12345")
    assert result == "MY_DB:MY_PROJECT:12345"


def test_id_generate_with_empty_id():
    context = SourceContext(database="MY_DB", project="MY_PROJECT")
    result = id_generate(context, "")
    assert result == "MY_DB:MY_PROJECT:"


def test_convert_date_to_utc_normal_time():
    """CET (normal time): UTC+1, so UTC should be 1 hour less."""
    local_date = datetime.datetime(2025, 1, 15, 12, 0, 0)
    result = convert_date_to_utc(local_date, timezone="Europe/Oslo")
    assert result.hour == 11
    assert result.tzname() == "UTC"


def test_convert_date_to_utc_daylight_saving():
    """CEST (daylight saving): UTC+2, so UTC should be 2 hours less."""
    local_date = datetime.datetime(2025, 7, 15, 12, 0, 0)
    result = convert_date_to_utc(local_date, timezone="Europe/Oslo")
    assert result.hour == 10
    assert result.tzname() == "UTC"


def test_localize_date_daylight_saving():
    """CEST (daylight saving): naive datetime gets +02:00 offset."""
    naive_date = datetime.datetime(2026, 5, 18, 14, 21, 0)
    result = localize_date(naive_date, timezone="Europe/Oslo")
    assert result.utcoffset() == datetime.timedelta(hours=2)
    assert result.hour == 14
    assert result.minute == 21


def test_source_metadata_localized_dates_json():
    """SourceMetadata with localized create_date serializes with correct offsets."""
    naive_date = datetime.datetime(2026, 5, 18, 14, 21, 0)
    timezone = "Europe/Oslo"

    source_metadata = SourceMetadata(
        system=SourceSystem.OPENWORKS,
        database="TEST_DB",
        project="TEST_PROJECT",
        id="123",
        name="test_surface",
        create_user="user1",
        create_date=localize_date(naive_date, timezone),
        create_date_utc=convert_date_to_utc(naive_date, timezone),
    )

    data = source_metadata.model_dump(mode="json")

    assert data["create_date"] == "2026-05-18T14:21:00+02:00"
    assert data["create_date_utc"] == "2026-05-18T12:21:00Z"

