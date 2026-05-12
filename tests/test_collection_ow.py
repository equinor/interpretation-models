from dsis_model_sdk.models.native import ISetDataObject

from mappers.collection_ow import resolve_id


def test_resolve_id_map2d_extracts_grid_id_from_native_uid() -> None:
    data_object_json = {
        "interpretation_set_id": "200",
        "iset_folder_id": 201,
        "data_key": "CntrParmName=somename;gridId=1830;interpreter=INTERP;",
        "data_type": "Map2D",
        "data_object_id": 1357,
        "data_object_name": "some grid",
        "native_uid": '{"interpretation_set_id":200,"iset_folder_id":201,"data_key":"CntrParmName=somename;gridId=42;interpreter=INTERP;","data_type":"Map2D"}',
    }
    ow_data_object = ISetDataObject(**data_object_json)

    assert resolve_id(ow_data_object) == "42"


def test_resolve_id_map2d_without_grid_id_returns_empty_string() -> None:
    data_object_json = {
        "interpretation_set_id": "200",
        "iset_folder_id": 201,
        "data_key": "CntrParmName=somename;interpreter=INTERP;",
        "data_type": "Map2D",
        "data_object_id": 1357,
        "data_object_name": "some grid",
        "native_uid": '{"interpretation_set_id":200,"iset_folder_id":201,"data_key":"CntrParmName=somename;interpreter=INTERP;","data_type":"Map2D"}',
    }
    ow_data_object = ISetDataObject(**data_object_json)

    assert resolve_id(ow_data_object) == ""


def test_resolve_id_non_map2d_uses_data_object_id() -> None:
    data_object_json = {
        "interpretation_set_id": "200",
        "iset_folder_id": 201,
        "data_key": "attribute=Depth_structure;dataSource=INTERP;geoName=Some Fm. Top;geoType=SURFACE;mapDataSetName=someName;",
        "data_type": "RGrid",
        "data_object_id": 1357,
        "data_object_name": "some grid",
        "native_uid": '{"interpretation_set_id":200,"iset_folder_id":201,"data_key":"attribute=Depth_structure;dataSource=INTERP;geoName=Some Fm. Top;geoType=SURFACE;mapDataSetName=someName;","data_type":"Rgrid"}',
    }
    ow_data_object = ISetDataObject(**data_object_json)

    assert resolve_id(ow_data_object) == "1357"


def test_resolve_id_non_map2d_without_data_object_id_returns_empty_string() -> None:
    data_object_json = {
        "interpretation_set_id": "200",
        "iset_folder_id": 201,
        "data_key": "attribute=Depth_structure;dataSource=INTERP;geoName=Some Fm. Top;geoType=SURFACE;mapDataSetName=someName;",
        "data_type": "RGrid",
        "data_object_name": "some grid",
        "native_uid": '{"interpretation_set_id":200,"iset_folder_id":201,"data_key":"attribute=Depth_structure;dataSource=INTERP;geoName=Some Fm. Top;geoType=SURFACE;mapDataSetName=someName;","data_type":"Rgrid"}',
    }
    ow_data_object = ISetDataObject(**data_object_json)

    assert resolve_id(ow_data_object) == ""
