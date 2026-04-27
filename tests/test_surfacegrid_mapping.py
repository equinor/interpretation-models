"""Contract tests for SurfaceGrid mapping and flattening.

Ensures map_surfacegrid produces a SurfaceGridRecord with the expected
structure and values, and that flatten_record produces a dict whose keys
and values match the record.
"""


import pytest
from models.interpretation import SurfaceGridRecord
from mappers.surfacegrid_ow import map_surfacegrid
from tables import flatten_record


@pytest.fixture
def surface_record(surfacegrid_obj, source_context, processing_metadata) -> SurfaceGridRecord:
    return map_surfacegrid(surfacegrid_obj, source_context, processing_metadata)


class TestMapSurfacegridContract:
    """Verify key properties of the mapped SurfaceGridRecord."""

    def test_returns_surfacegrid_record(self, surface_record):
        assert isinstance(surface_record, SurfaceGridRecord)

    def test_source_metadata_populated(self, surface_record, surfacegrid_obj, source_context):
        src = surface_record.source
        assert src is not None
        assert src.database == source_context.database
        assert src.project == source_context.project
        assert src.id == surfacegrid_obj.native_uid
        assert src.name == surfacegrid_obj.map_data_set_name
    

    def test_geometry_populated(self, surface_record, surfacegrid_obj):
        geom = surface_record.geometry
        assert geom is not None
        assert geom.ncol == surfacegrid_obj.num_cols
        assert geom.nrow == surfacegrid_obj.num_rows
        assert geom.xori == surfacegrid_obj.rotation_origin_x
        assert geom.yori == surfacegrid_obj.rotation_origin_y
        assert geom.xinc == surfacegrid_obj.grid_interval_x
        assert geom.yinc == surfacegrid_obj.grid_interval_y


class TestFlattenSurfaceGridRecord:
    """Verify flattening produces a complete, value-accurate dict."""

    @pytest.fixture
    def flat(self, surface_record) -> dict:
        return flatten_record(surface_record)

    def test_all_model_fields_present(self, flat):
        """Every column from the model should appear as a key in the flattened dict."""
        from tables import flatten_columns

        expected_keys = {col.name for col in flatten_columns(SurfaceGridRecord)}
        actual_keys = set(flat.keys())
        assert expected_keys == actual_keys

    def test_flat_values_match_record(self, flat):
        """All flattened values must match the expected contract."""
        expected = {
            "id": "BG4FROST:VOLVE_PUBLIC:2636",
            "source_system": "OpenWorks R5000",
            "source_database": "BG4FROST",
            "source_project": "VOLVE_PUBLIC",
            "source_id": "2636",
            "source_name": "ihdTHugin13flt3",
            "source_remark": None,
            "source_create_user": "IHD",
            "source_update_user": "IHD",
            "source_create_date": "2013-11-15T08:20:49",
            "source_create_date_utc": "2013-11-15T07:20:49Z",
            "source_update_date": "2013-11-15T08:20:49",
            "source_update_date_utc": "2013-11-15T07:20:49Z",
            "source_ow_geo_name": "UNKNOWN",
            "source_ow_geo_type": "SURFACE",
            "source_ow_attribute": "DEPTH",
            "source_petrel_business_project": None,
            "source_petrel_data_status": None,
            "source_petrel_confidence_factor": None,
            "processing_create_date": None,
            "processing_update_date": None,
            "processing_file_available": None,
            "processing_file_error_message": None,
            "processing_file_path": None,
            "extent_points": None,
            "crs": "ST_ED50_UTM31N_P23031_T1133",
            "z_domain": "TVDSS",
            "z_unit": "meters",
            "geometry_ncol": 879,
            "geometry_nrow": 629,
            "geometry_xori": 429588.0,
            "geometry_yori": 6475211.0,
            "geometry_xinc": 12.0,
            "geometry_yinc": 12.0,
            "geometry_rotation": 0.0,
            "geometry_left_handed": True,
            "grid_null_value": None,
            "grid_ntotal": None,
            "grid_nnan": None,
            "parent_surface_id": None,
        }
        assert flat == expected

    def test_flat_values_are_json_serializable(self, flat):
        """All values should be JSON-compatible primitives (no Pydantic objects)."""
        import json
        json.dumps(flat, default=str)  # should not raise
