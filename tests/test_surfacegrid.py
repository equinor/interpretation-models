import pytest
from pydantic import ValidationError
from models.surfacegrid import SurfaceGrid


def test_surface_grid_missing_required_field():
    with pytest.raises(ValidationError):
        SurfaceGrid(
            id="sg-missing-name",
            crs_identifier="EPSG:4326",
            rotation=0.0,
            # name omitted on purpose
        )
