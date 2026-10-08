import json
import pytest
import pathlib

from interpretation_models.mappers import surfacegrid_from_ow
from interpretation_models.models import SurfaceGridRecord
from dsis_model_sdk.models.common import SurfaceGrid


@pytest.fixture
def surface_grid_record(source_context, processing_metadata) -> SurfaceGridRecord:
    record_path = (
        pathlib.Path("tests")
        / "mappers"
        / "openworks"
        / "data"
        / "surfacegrid_volve_public.json"
    )
    record = json.loads(record_path.read_text(encoding="utf-8"))
    surface_grid = SurfaceGrid.model_validate(record)
    return surfacegrid_from_ow(surface_grid, source_context, processing_metadata)
