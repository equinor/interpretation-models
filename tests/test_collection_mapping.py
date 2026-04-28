"""Contract tests for Collection and CollectionItem mapping and flattening.

Tests map_collection and map_collection_item with realistic OW inputs
including Map2D (with grid id resolution), RGrid, and a Map2D edge case
where gridId is missing. Flattened output is compared against hardcoded
expected dicts to guard the contract.
"""

import json
from datetime import datetime

import pytest
from dsis_model_sdk.models.native import InterpretationSet, ISetDataObject

from mappers.collection_ow import map_collection, map_collection_item
from models.collection import Collection, CollectionItem
from models.metadata import SourceContext
from tables import flatten_record, flatten_columns


@pytest.fixture
def collection_source_context() -> SourceContext:
    return SourceContext(
        database="BG4FROST",
        project="VOLVE_PUBLIC",
        timezone="Europe/Berlin",
    )


@pytest.fixture
def ow_interpretation_set() -> InterpretationSet:
    return InterpretationSet(
        interpretation_set_id="100",
        interpret_set_name="Volve Horizons",
        data_source="IHD",
        field_prospect_name="VOLVE",
        remark="Test collection",
        create_user_id="USER1",
        create_date=datetime(2020, 3, 15, 10, 30, 0),
        update_user_id="USER2",
        update_date=datetime(2021, 6, 20, 14, 0, 0),
    )


@pytest.fixture
def ow_item_map2d() -> ISetDataObject:
    """Map2D item — gridId extracted from native_uid."""
    return ISetDataObject(
        interpretation_set_id="100",
        iset_folder_id=201,
        data_key="CntrParmName=contour;gridId=1830;interpreter=INTERP;",
        data_type="Map2D",
        data_object_id=5001,
        data_object_name="Hugin Fm. Top depth",
        remark="Main horizon",
        create_user_id="USER1",
        create_date=datetime(2020, 3, 15, 10, 30, 0),
        update_user_id="USER2",
        update_date=datetime(2021, 6, 20, 14, 0, 0),
        native_uid=json.dumps({
            "interpretation_set_id": 100,
            "iset_folder_id": 201,
            "data_key": "CntrParmName=contour;gridId=1830;interpreter=INTERP;",
            "data_type": "Map2D",
        }),
    )


@pytest.fixture
def ow_item_rgrid() -> ISetDataObject:
    """RGrid item — object_id used directly."""
    return ISetDataObject(
        interpretation_set_id="100",
        iset_folder_id=202,
        data_key="attribute=Depth;dataSource=IHD;geoName=Draupne Fm.;geoType=SURFACE;mapDataSetName=draupneDepth;",
        data_type="Rgrid",
        data_object_id=2636,
        data_object_name="Draupne Fm. depth",
        create_user_id="USER1",
        create_date=datetime(2020, 5, 10, 8, 0, 0),
        native_uid=json.dumps({
            "interpretation_set_id": 100,
            "iset_folder_id": 202,
            "data_key": "attribute=Depth;dataSource=IHD;geoName=Draupne Fm.;geoType=SURFACE;mapDataSetName=draupneDepth;",
            "data_type": "Rgrid",
        }),
    )


@pytest.fixture
def ow_item_map2d_no_gridid() -> ISetDataObject:
    """Map2D item without gridId in native_uid — edge case."""
    return ISetDataObject(
        interpretation_set_id="100",
        iset_folder_id=203,
        data_key="CntrParmName=contour;interpreter=IHD;",
        data_type="Map2D",
        data_object_id=5002,
        data_object_name="Broken Map2D",
        native_uid=json.dumps({
            "interpretation_set_id": 100,
            "iset_folder_id": 203,
            "data_key": "CntrParmName=contour;interpreter=IHD;",
            "data_type": "Map2D",
        }),
    )


# ---------------------------------------------------------------------------
# Collection mapping
# ---------------------------------------------------------------------------


class TestMapCollectionContract:
    def test_returns_collection(self, ow_interpretation_set, collection_source_context):
        coll = map_collection(ow_interpretation_set, collection_source_context)
        assert isinstance(coll, Collection)

    def test_collection_flat_values(self, ow_interpretation_set, collection_source_context):
        coll = map_collection(ow_interpretation_set, collection_source_context)
        flat = flatten_record(coll)

        expected = {
            "id": "BG4FROST:VOLVE_PUBLIC:100",
            "source_system": "OpenWorks R5000",
            "source_database": "BG4FROST",
            "source_project": "VOLVE_PUBLIC",
            "source_id": "BG4FROST:VOLVE_PUBLIC:100",
            "source_name": "Volve Horizons",
            "source_remark": "Test collection",
            "source_create_user": "USER1",
            "source_update_user": "USER2",
            "source_create_date": "2020-03-15T10:30:00",
            "source_create_date_utc": "2020-03-15T09:30:00Z",
            "source_update_date": "2021-06-20T14:00:00",
            "source_update_date_utc": "2021-06-20T12:00:00Z",
            "source_ow_field_prospect_name": "VOLVE",
            "processing_create_date": None,
            "processing_update_date": None,
        }
        assert flat == expected

    def test_collection_all_model_fields_present(self, ow_interpretation_set, collection_source_context):
        coll = map_collection(ow_interpretation_set, collection_source_context)
        flat = flatten_record(coll)
        expected_keys = {col.name for col in flatten_columns(Collection)}
        assert set(flat.keys()) == expected_keys


# ---------------------------------------------------------------------------
# CollectionItem mapping
# ---------------------------------------------------------------------------


class TestMapCollectionItemContract:
    """Test Map2D, RGrid, and edge-case items."""

    def test_map2d_item_flat_values(self, ow_item_map2d, collection_source_context):
        ci = map_collection_item(ow_item_map2d, collection_source_context)
        assert isinstance(ci, CollectionItem)
        flat = flatten_record(ci)

        expected = {
            "collection_id": "BG4FROST:VOLVE_PUBLIC:100",
            "object_id": "BG4FROST:VOLVE_PUBLIC:1830",
            "datatype": "SurfaceGrid",
            "source_system": "OpenWorks R5000",
            "source_database": "BG4FROST",
            "source_project": "VOLVE_PUBLIC",
            "source_id": "5001",
            "source_name": "Hugin Fm. Top depth",
            "source_remark": "Main horizon",
            "source_create_user": "USER1",
            "source_update_user": "USER2",
            "source_create_date": "2020-03-15T10:30:00",
            "source_create_date_utc": "2020-03-15T09:30:00Z",
            "source_update_date": "2021-06-20T14:00:00",
            "source_update_date_utc": "2021-06-20T12:00:00Z",
            "source_ow_data_type": "Map2D",
            "source_ow_data_object_name": "Hugin Fm. Top depth",
            "source_ow_data_object_id": "5001",
            "source_ow_native_uid": json.dumps({
                "interpretation_set_id": 100,
                "iset_folder_id": 201,
                "data_key": "CntrParmName=contour;gridId=1830;interpreter=INTERP;",
                "data_type": "Map2D",
            }),
            "processing_create_date": None,
            "processing_update_date": None,
        }
        assert flat == expected

    def test_map2d_resolves_grid_id_from_native_uid(self, ow_item_map2d, collection_source_context):
        """Map2D object_id should use the gridId from native_uid, not data_object_id."""
        ci = map_collection_item(ow_item_map2d, collection_source_context)
        assert ci.object_id == "BG4FROST:VOLVE_PUBLIC:1830"

    def test_rgrid_item_flat_values(self, ow_item_rgrid, collection_source_context):
        ci = map_collection_item(ow_item_rgrid, collection_source_context)
        assert isinstance(ci, CollectionItem)
        flat = flatten_record(ci)

        expected = {
            "collection_id": "BG4FROST:VOLVE_PUBLIC:100",
            "object_id": "BG4FROST:VOLVE_PUBLIC:2636",
            "datatype": "SurfaceGrid",
            "source_system": "OpenWorks R5000",
            "source_database": "BG4FROST",
            "source_project": "VOLVE_PUBLIC",
            "source_id": "2636",
            "source_name": "Draupne Fm. depth",
            "source_remark": None,
            "source_create_user": "USER1",
            "source_update_user": "USER1",
            "source_create_date": "2020-05-10T08:00:00",
            "source_create_date_utc": "2020-05-10T06:00:00Z",
            "source_update_date": "2020-05-10T08:00:00",
            "source_update_date_utc": "2020-05-10T06:00:00Z",
            "source_ow_data_type": "Rgrid",
            "source_ow_data_object_name": "Draupne Fm. depth",
            "source_ow_data_object_id": "2636",
            "source_ow_native_uid": json.dumps({
                "interpretation_set_id": 100,
                "iset_folder_id": 202,
                "data_key": "attribute=Depth;dataSource=IHD;geoName=Draupne Fm.;geoType=SURFACE;mapDataSetName=draupneDepth;",
                "data_type": "Rgrid",
            }),
            "processing_create_date": None,
            "processing_update_date": None,
        }
        assert flat == expected

    def test_rgrid_uses_data_object_id(self, ow_item_rgrid, collection_source_context):
        """RGrid object_id should use data_object_id directly."""
        ci = map_collection_item(ow_item_rgrid, collection_source_context)
        assert ci.object_id == "BG4FROST:VOLVE_PUBLIC:2636"

    def test_map2d_no_gridid_edge_case(self, ow_item_map2d_no_gridid, collection_source_context):
        """Map2D without gridId in native_uid — object_id resolves to empty id."""
        ci = map_collection_item(ow_item_map2d_no_gridid, collection_source_context)
        flat = flatten_record(ci)

        expected = {
            "collection_id": "BG4FROST:VOLVE_PUBLIC:100",
            "object_id": "BG4FROST:VOLVE_PUBLIC:",
            "datatype": "SurfaceGrid",
            "source_system": "OpenWorks R5000",
            "source_database": "BG4FROST",
            "source_project": "VOLVE_PUBLIC",
            "source_id": "5002",
            "source_name": "Broken Map2D",
            "source_remark": None,
            "source_create_user": None,
            "source_update_user": None,
            "source_create_date": None,
            "source_create_date_utc": None,
            "source_update_date": None,
            "source_update_date_utc": None,
            "source_ow_data_type": "Map2D",
            "source_ow_data_object_name": "Broken Map2D",
            "source_ow_data_object_id": "5002",
            "source_ow_native_uid": json.dumps({
                "interpretation_set_id": 100,
                "iset_folder_id": 203,
                "data_key": "CntrParmName=contour;interpreter=IHD;",
                "data_type": "Map2D",
            }),
            "processing_create_date": None,
            "processing_update_date": None,
        }
        assert flat == expected

    def test_collection_item_all_model_fields_present(self, ow_item_map2d, collection_source_context):
        ci = map_collection_item(ow_item_map2d, collection_source_context)
        flat = flatten_record(ci)
        expected_keys = {col.name for col in flatten_columns(CollectionItem)}
        assert set(flat.keys()) == expected_keys
