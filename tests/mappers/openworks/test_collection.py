"""Contract tests for Collection and CollectionItem mapping and flattening.

Tests map_collection and map_collection_item with realistic OW inputs
including Map2D (with grid id resolution), RGrid, and a Map2D edge case
where gridId is missing. Flattened output is compared against hardcoded
expected dicts to guard the contract.
"""

import pytest

from interpretation_models.mappers import collection_from_ow, collection_item_from_ow
from interpretation_models.models import Collection, CollectionItem
from interpretation_models.models import SourceContext
from interpretation_models.tables import flatten_record, flatten_columns

from dsis_model_sdk.models.native import ISetDataObject
from interpretation_models.mappers.openworks.collection import _resolve_id

# ---------------------------------------------------------------------------
# Collection mapping
# ---------------------------------------------------------------------------

def test_collection_all_model_fields_present(ow_interpretation_set, source_context):
    coll = collection_from_ow(ow_interpretation_set, source_context)
    assert isinstance(coll, Collection)
    flat = flatten_record(coll)
    expected_keys = {col.name for col in flatten_columns(Collection)}
    assert set(flat.keys()) == expected_keys

def test_collection_flat_values(ow_interpretation_set, source_context):
    coll = collection_from_ow(ow_interpretation_set, source_context)
    flat = flatten_record(coll)

    expected = {
        "id": "SOME_DB:SOME_PROJECT:Collection:100",
        "source_system": "OpenWorks R5000",
        "source_database": "SOME_DB",
        "source_project": "SOME_PROJECT",
        "source_id": "100",
        "source_name": "Volve objects",
        "source_remark": "Test collection",
        "source_create_user": "USER1",
        "source_update_user": "USER2",
        "source_create_date_utc": "2020-03-15T09:30:00Z",
        "source_update_date_utc": "2021-06-20T12:00:00Z",
        'source_ow_data_source': "IHD",
        "source_ow_field_prospect_name": "Volve",
        "processing_create_date_utc": None,
        "processing_update_date_utc": None,
    }
    assert flat == expected


# ---------------------------------------------------------------------------
# ID resolution tests for CollectionItem
# ---------------------------------------------------------------------------

def test_resolve_id_default_uses_data_object_id(ow_isetdataobject_rgrid) -> None:
    assert _resolve_id(ow_isetdataobject_rgrid) == "42"


def test_resolve_id_map2d_extracts_grid_id_from_native_uid(ow_isetdataobject_map2d) -> None:
    assert _resolve_id(ow_isetdataobject_map2d) == "1357"


def test_resolve_id_map2d_without_grid_id_returns_empty_string(ow_isetdataobject_map2d_no_gridid) -> None:
    assert _resolve_id(ow_isetdataobject_map2d_no_gridid) == ""


# ---------------------------------------------------------------------------
# CollectionItem mapping
# ---------------------------------------------------------------------------


def test_collection_item_all_model_fields_present(ow_isetdataobject_map2d, source_context):
    ci = collection_item_from_ow(ow_isetdataobject_map2d, source_context)
    assert isinstance(ci, CollectionItem)
    flat = flatten_record(ci)
    expected_keys = {col.name for col in flatten_columns(CollectionItem)}
    assert set(flat.keys()) == expected_keys

def test_map2d_item_flat_values(ow_isetdataobject_map2d, source_context):
    ci = collection_item_from_ow(ow_isetdataobject_map2d, source_context)
    assert isinstance(ci, CollectionItem)
    flat = flatten_record(ci)

    expected = {
        "id": "SOME_DB:SOME_PROJECT:Collection:100:SurfaceGrid:1357",
        "collection_id": "SOME_DB:SOME_PROJECT:Collection:100",
        "object_id": "SOME_DB:SOME_PROJECT:SurfaceGrid:1357",
        "datatype": "SurfaceGrid",
        "source_system": "OpenWorks R5000",
        "source_database": "SOME_DB",
        "source_project": "SOME_PROJECT",
        "source_id": "42",
        "source_name": "Hugin Fm. Top depth",
        "source_remark": "Main horizon",
        "source_create_user": "USER1",
        "source_update_user": "USER2",
        "source_create_date_utc": "2020-03-15T09:30:00Z",
        "source_update_date_utc": "2021-06-20T12:00:00Z",
        "source_ow_data_type": "Map2D",
        "source_ow_data_key":"CntrParmName=contour;gridId=1357;interpreter=INTERP;",
        "source_ow_interpretation_set_id": '100',
        "source_ow_iset_folder_id": 201,
        "processing_create_date_utc": None,
        "processing_update_date_utc": None,
    }
    assert flat == expected

def test_rgrid_item_flat_values(ow_isetdataobject_rgrid, source_context):
    ci = collection_item_from_ow(ow_isetdataobject_rgrid, source_context)
    assert isinstance(ci, CollectionItem)
    flat = flatten_record(ci)

    expected = {
        "id": "SOME_DB:SOME_PROJECT:Collection:100:SurfaceGrid:42",
        "collection_id": "SOME_DB:SOME_PROJECT:Collection:100",
        "object_id": "SOME_DB:SOME_PROJECT:SurfaceGrid:42",
        "datatype": "SurfaceGrid",
        "source_system": "OpenWorks R5000",
        "source_database": "SOME_DB",
        "source_project": "SOME_PROJECT",
        "source_id": "42",
        "source_name": "Draupne Fm. depth",
        "source_remark": None,
        "source_create_user": "USER1",
        "source_update_user": "USER1",
        "source_create_date_utc": "2020-05-10T06:00:00Z",
        "source_update_date_utc": "2020-05-10T06:00:00Z",
        "source_ow_data_type": "Rgrid",
        "source_ow_data_key": "attribute=Depth;dataSource=IHD;geoName=Draupne Fm.;geoType=SURFACE;mapDataSetName=draupneDepth;",
        "source_ow_interpretation_set_id": '100',
        "source_ow_iset_folder_id": 201,
        "processing_create_date_utc": None,
        "processing_update_date_utc": None,
    }
    assert flat == expected
