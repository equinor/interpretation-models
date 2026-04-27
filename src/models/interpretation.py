from pydantic import BaseModel
from models.extent import Extent
from models.metadata import SourceMetadata, InterpretationProcessingMetadata, OWMetadata, OWSurfaceGridMetadata, PetrelMetadata


class InterpretationRecord(BaseModel):
    id: str
    source: SourceMetadata | None = None
    source_ow: OWMetadata | None = None
    source_petrel: PetrelMetadata | None = None
    processing: InterpretationProcessingMetadata | None = None
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
    """
    A surface defined in a regular 2D grid containing values for each of the points in the grid.
    The grid geometry is defined by the ``geometry`` parameters, which are sufficient to locate each point in space.
    SurfaceGrids are typically (but not necessarily) originated from a horizon, replacing its seismic bin grid by a
    locally defined grid (potentially after regridding)
    The values are stored separately as a flattened 2D array, the format of which is explained in
    http://github.com/equinor/interpretation-models/docs/bulk_data_models.md
    The values can represent a structural surface (depth or time) or a property defined on a surface
    (e.g. attribute, uncertainty, …).
    In the case the values represent a property, there's optionally included a parent structural surface that the
    property is defined on.
    """
    source_ow: OWSurfaceGridMetadata | None = None
    parent_surface_id: str | None = None
