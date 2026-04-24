import pytest
from models.interpretation import SurfaceGridRecord


def test_surface_grid_record_accepts_no_required_fields():
    """SurfaceGridRecord can be created with no arguments (all fields optional at record level)."""
    record = SurfaceGridRecord()
    assert record.source is None
    assert record.geometry is None
