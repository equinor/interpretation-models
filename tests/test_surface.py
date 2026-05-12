import pytest
from models.interpretation import SurfaceGridRecord


def test_surface_grid_record_accepts_no_required_fields():
    """SurfaceGridRecord can be created only id (all fields optional at record level)."""
    record = SurfaceGridRecord(id="id")
    assert record.source is None
    assert record.geometry is None
