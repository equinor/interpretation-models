import json
from pathlib import Path

import pytest
from dsis_model_sdk.models.common import SurfaceGrid

from models import InterpretationProcessingMetadata
from models import SourceContext


@pytest.fixture
def surfacegrid_payload() -> dict:
    file_path = (
        Path(__file__).resolve().parent / "data" / "surfacegrid_volve_public.json"
    )
    return json.loads(file_path.read_text(encoding="utf-8"))

@pytest.fixture
def surfacegrid_obj(surfacegrid_payload: dict) -> SurfaceGrid:
    return SurfaceGrid.model_validate(surfacegrid_payload)


@pytest.fixture
def processing_metadata() -> InterpretationProcessingMetadata:
    return InterpretationProcessingMetadata(
        id="11111111-1111-1111-1111-111111111111",
    )


@pytest.fixture
def source_context() -> SourceContext:
    return SourceContext(
        database="BG4FROST",
        project="VOLVE_PUBLIC",
        timezone="Europe/Berlin",
    )
