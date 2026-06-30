import datetime

from interpretation_models.mappers.helpers import convert_date_to_utc
from interpretation_models.mappers.openworks import metadata
from interpretation_models.models import SourceContext, SourceMetadata
from interpretation_models.models import SourceSystem
from dsis_model_sdk.models.native import InterpretationSet


def test_source_metadata_utc_dates_json():
    """SourceMetadata serializes UTC create_date in Zulu format."""
    naive_date = datetime.datetime(2026, 5, 18, 14, 21, 0)
    timezone = "Europe/Oslo"

    source_metadata = SourceMetadata(
        system=SourceSystem.OPENWORKS,
        database="TEST_DB",
        project="TEST_PROJECT",
        id="123",
        name="test_surface",
        create_user="user1",
        create_date_utc=convert_date_to_utc(naive_date, timezone),
    )

    data = source_metadata.model_dump(mode="json")

    assert data["create_date_utc"] == "2026-05-18T12:21:00Z"


def test_map_ow_source_metadata_update_date_falls_back_to_create_date():
    """When update_date is None, source_metadata_from_ow uses create_date as update_date and computes UTC.
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

    result = metadata.source_metadata_from_ow(ow_iset, source_context, id="uid1", name="Test ISet")

    assert result.update_user == "creator"
    assert result.update_date_utc == result.create_date_utc

