import pytest
from pydantic import ValidationError
from models.surface import Surface


def test_surface_grid_missing_required_field():
    with pytest.raises(ValidationError):
        Surface(
            id="11111111-1111-1111-1111-111111111111",
            crs="ST_ED50_UTM31N_P23031_T1133",
            rotation=0.0,
            # name omitted on purpose
        )
