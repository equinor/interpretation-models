import datetime

from mappers.openworks.metadata import convert_date_to_utc, localize_date, id_generate, map_ow_source_metadata
from models.metadata import SourceContext, SourceMetadata
from models.enums import SourceSystem
from dsis_model_sdk.models.native import InterpretationSet


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


def test_map_ow_source_metadata_update_date_falls_back_to_create_date():
    """When update_date is None, map_ow_source_metadata uses create_date as update_date and computes UTC.
    We test here with an ISet as an example, but the SourceMetadata behaviour is the same for all OW metadata mappers
    """
    create_date = datetime.datetime(2026, 5, 18, 14, 21, 0)
    timezone = "Europe/Oslo"

    ow_iset = InterpretationSet(
        interpretation_set_id="ISET1",
        interpret_set_name="Test ISet",
        data_source="OW",
        create_date=create_date,
        create_user_id="creator",
        update_date=None,
        update_user_id=None,
    )
    source_context = SourceContext(database="DB", project="PROJ", timezone=timezone)

    result = map_ow_source_metadata(ow_iset, source_context, id="uid1", name="Test ISet")

    assert result.update_user == "creator"
    assert result.update_date == result.create_date
    assert result.update_date_utc == result.create_date_utc

