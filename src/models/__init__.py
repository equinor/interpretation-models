"""Interpretation models — semantic models for subsurface interpretation data.

Public API re-exports the interpretation record models and enums at the top level.
Source-specific models live in submodules (e.g. ``models.petrel``).
"""

from models.interpretations import (
    # Interpretation records
    InterpretationRecord,
    GridGeometry,
    GriddedInterpretationRecord,
    VectorInterpretationRecord,
    SurfaceGridRecord,
    # Collections
    Collection,
    CollectionItem,
    # Metadata
    ProcessingMetadata,
    InterpretationProcessingMetadata,
    SourceContext,
    SourceMetadata,
    OWMetadata,
    OWSurfaceGridMetadata,
    OWCollectionMetadata,
    OWCollectionItemMetadata,
    PetrelMetadata,
    # Geometry
    Extent,
    Point,
)

from models.enums import (
    SourceSystem,
    InterpretationDataType,
    UpdateType,
    OWDataType,
)

from models import petrel

__all__ = [
    # Interpretation records
    "InterpretationRecord",
    "GridGeometry",
    "GriddedInterpretationRecord",
    "VectorInterpretationRecord",
    "SurfaceGridRecord",
    # Collections
    "Collection",
    "CollectionItem",
    # Metadata
    "ProcessingMetadata",
    "InterpretationProcessingMetadata",
    "SourceContext",
    "SourceMetadata",
    "OWMetadata",
    "OWSurfaceGridMetadata",
    "OWCollectionMetadata",
    "OWCollectionItemMetadata",
    "PetrelMetadata",
    # Geometry
    "Extent",
    "Point",
    # Enums
    "SourceSystem",
    "InterpretationDataType",
    "UpdateType",
    "OWDataType",
    # Submodules
    "petrel",
]
