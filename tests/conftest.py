import json
from pathlib import Path

import pytest
from dsis_model_sdk.models.common import SurfaceGrid
from mappers.surface_helpers import normalize_surfacegrid_payload

from models.interpretation import PipelineMetadata
from models.origin import Database, Project


@pytest.fixture
def surfacegrid_payload() -> dict:
    file_path = (
        Path(__file__).resolve().parent / "data" / "surfacegrid_volve_public.json"
    )
    return json.loads(file_path.read_text(encoding="utf-8"))


@pytest.fixture
def surfacegrid_payload_normalized(surfacegrid_payload: dict) -> dict:
    return normalize_surfacegrid_payload(surfacegrid_payload)


@pytest.fixture
def surfacegrid_obj(surfacegrid_payload_normalized: dict) -> SurfaceGrid:
    return SurfaceGrid.model_validate(surfacegrid_payload_normalized)


@pytest.fixture
def pipeline_metadata() -> PipelineMetadata:
    return PipelineMetadata(
        id="11111111-1111-1111-1111-111111111111",
        project=Project(
            name="VOLVE_PUBLIC",
        ),
        database=Database(name="BG4FROST", timezone="Europe/Berlin"),
    )