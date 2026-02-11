from datetime import datetime
from models.interpretation import Interpretation


class Surface(Interpretation):
    # Required geometry
    ncol: int
    nrow: int
    xori: float
    yori: float
    xinc: float
    yinc: float
    rotation: float
    # yflip: int  # handedness?

    # Surface properties
    geo_name: str | None = None
    geo_type: str | None = None
    z_unit: str | None = None
    z_non: float | None = None
    z_domain: str | None = None
    attribute_source: str | None = None
    interpreter_source: str | None = None
    remark_source: str | None = None
    business_project_source: str | None = None      # Petrel Studio
    data_status_source: str | None = None           # Petrel Studio
    confidence_factor_source: str | None = None     # Petrel Studio

    # SID
    file_availability: str

    # Redundant?
    ntotal: int | None = None
    nnan: int | None = None
    deleted: bool | None = None
    deleted_date: datetime | None = None