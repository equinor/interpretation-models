from pydantic import BaseModel
from models.extent import Extent
from models.metadata import SourceMetadata, ProcessingMetadata


class InterpretationRecord(BaseModel):
    source: SourceMetadata | None = None
    processing: ProcessingMetadata | None = None
    extent: Extent | None = None
    crs: str | None = None
    z_domain: str | None = None
    z_unit: str | None = None


class GridGeometry(BaseModel):
    ncol: int | None = None
    nrow: int | None = None
    xori: float | None = None
    yori: float | None = None
    xinc: float | None = None
    yinc: float | None = None
    rotation: float | None = None
    left_handed: bool | None = True  # yflip


class GriddedInterpretationRecord(InterpretationRecord):
    geometry: GridGeometry | None = None
    grid_null_value: float | None = None
    grid_ntotal: int | None = None
    grid_nnan: int | None = None


class VectorInterpretationRecord(InterpretationRecord):
    num_points: int | None = None
    num_properties: int | None = None


class SurfaceGridRecord(GriddedInterpretationRecord):
    parent_surface_id: str | None = None
