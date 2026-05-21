import json
from datetime import datetime
from pathlib import Path

import pytest
from dsis_model_sdk.models.common import SurfaceGrid
from dsis_model_sdk.models.native import InterpretationSet, ISetDataObject


# ---------------------------------------------------------------------------
# OW SurfaceGrid fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def surfacegrid_payload() -> dict:
    file_path = (
        Path(__file__).resolve().parent / "data" / "surfacegrid_volve_public.json"
    )
    return json.loads(file_path.read_text(encoding="utf-8"))


@pytest.fixture
def surfacegrid_obj(surfacegrid_payload: dict) -> SurfaceGrid:
    return SurfaceGrid.model_validate(surfacegrid_payload)


# ---------------------------------------------------------------------------
# OW ISet / ISetDataObject fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def ow_interpretation_set() -> InterpretationSet:
    return InterpretationSet(
        interpretation_set_id="100",
        interpret_set_name="Volve objects",
        data_source="IHD",
        field_prospect_name="Volve",
        remark="Test collection",
        create_user_id="USER1",
        create_date=datetime(2020, 3, 15, 10, 30, 0),
        update_user_id="USER2",
        update_date=datetime(2021, 6, 20, 14, 0, 0),
    )


@pytest.fixture
def ow_isetdataobject_rgrid() -> ISetDataObject:
    """RGrid item — object_id used directly."""
    return ISetDataObject(
        interpretation_set_id="100",
        iset_folder_id=201,
        data_key="attribute=Depth;dataSource=IHD;geoName=Draupne Fm.;geoType=SURFACE;mapDataSetName=draupneDepth;",
        data_type="Rgrid",
        data_object_id=42,
        data_object_name="Draupne Fm. depth",
        create_user_id="USER1",
        create_date=datetime(2020, 5, 10, 8, 0, 0),
        native_uid=json.dumps({
            "interpretation_set_id": 100,
            "iset_folder_id": 201,
            "data_key": "attribute=Depth;dataSource=IHD;geoName=Draupne Fm.;geoType=SURFACE;mapDataSetName=draupneDepth;",
            "data_type": "Rgrid",
        }),
    )


@pytest.fixture
def ow_isetdataobject_map2d() -> ISetDataObject:
    """Map2D item — gridId should be 1357 extracted from native_uid (not 42 which is the container id)"""
    return ISetDataObject(
        interpretation_set_id="100",
        iset_folder_id=201,
        data_key="CntrParmName=contour;gridId=1357;interpreter=INTERP;",
        data_type="Map2D",
        data_object_id=42,
        data_object_name="Hugin Fm. Top depth",
        remark="Main horizon",
        create_user_id="USER1",
        create_date=datetime(2020, 3, 15, 10, 30, 0),
        update_user_id="USER2",
        update_date=datetime(2021, 6, 20, 14, 0, 0),
        native_uid=json.dumps({
            "interpretation_set_id": 100,
            "iset_folder_id": 201,
            "data_key": "CntrParmName=contour;gridId=1357;interpreter=INTERP;",
            "data_type": "Map2D",
        }),
    )


@pytest.fixture
def ow_isetdataobject_map2d_no_gridid() -> ISetDataObject:
    """Map2D item without gridId in native_uid — edge case."""
    return ISetDataObject(
        interpretation_set_id="100",
        iset_folder_id=203,
        data_key="CntrParmName=contour;interpreter=IHD;",
        data_type="Map2D",
        data_object_id=42,
        data_object_name="Broken Map2D",
        native_uid=json.dumps({
            "interpretation_set_id": 100,
            "iset_folder_id": 203,
            "data_key": "CntrParmName=contour;interpreter=IHD;",
            "data_type": "Map2D",
        }),
    )
