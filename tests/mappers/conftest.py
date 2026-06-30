import pytest
from datetime import datetime
from interpretation_models.models import InterpretationProcessingMetadata, SourceContext

# ---------------------------------------------------------------------------
# Shared metadata fixtures for mapper tests
# ---------------------------------------------------------------------------


@pytest.fixture
def source_context() -> SourceContext:
    return SourceContext(
        database="SOME_DB",
        project="SOME_PROJECT",
        timezone="Europe/Berlin",
    )


@pytest.fixture
def processing_metadata() -> InterpretationProcessingMetadata:
    return InterpretationProcessingMetadata(
        file_available=True,
        file_error_message=None,
        file_path="/path/to/file",
        create_date_utc=datetime(2025, 1, 1, 12, 0, 0),
        update_date_utc=datetime(2025, 7, 1, 12, 0, 0),
    )
