import pytest
from dsis_model_sdk.models.common import SurfaceGrid
from pydantic import ValidationError


def test_surfacegrid_raw_json_fails_strict_validation(surfacegrid_payload: dict):
    with pytest.raises(ValidationError):
        SurfaceGrid.model_validate(surfacegrid_payload)


def test_surfacegrid_normalized_json_validates(
    surfacegrid_payload_normalized: dict,
):
    obj = SurfaceGrid.model_validate(surfacegrid_payload_normalized)
    assert isinstance(obj, SurfaceGrid)
