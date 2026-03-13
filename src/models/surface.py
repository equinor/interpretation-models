from pydantic import BaseModel
from models.interpretation import Interpretation


class GridGeometry(BaseModel):
    ncol: int | None = None
    nrow: int | None = None
    xori: float | None = None
    yori: float | None = None
    xinc: float | None = None
    yinc: float | None = None
    rotation: float | None = None
    left_handed: bool | None = True  # yflip


class Surface(Interpretation):
    geometry: GridGeometry | None = None
    parent_surface_id: str | None = (
        None  # for SurfaceGridProperties objects? source or SID id?
    )

    # Redundant?
    z_non: float | None = None
    ntotal: int | None = None
    nnan: int | None = None
