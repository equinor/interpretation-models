from datetime import datetime
from pydantic import BaseModel

# this class is just here for development purposes, to compare the v2 and v3 models; can be removed later


class SurfaceGrid_SIDv2(BaseModel):
    ssdf_uuid: str | None = None

    # Source
    source: str | None = None
    source_database: str | None = None
    source_project: str | None = None
    source_grid_id: str | None = None

    # Surface properties
    surface_name: str | None = None
    geo_name: str | None = None
    geo_type: str | None = None
    z_unit: str | None = None
    z_non: float | None = None
    z_domain: str | None = None
    attribute_source: str | None = None
    interpreter_source: str | None = None
    create_user_source: str | None = None
    update_user_source: str | None = None
    remark_source: str | None = None
    business_project_source: str | None = None
    data_status_source: str | None = None
    confidence_factor_source: str | None = None

    # Coordinate systems
    object_coordinate_system_name_source: str | None = None  # OpenWorks R5000
    object_coordinate_system_unit_source: str | None = None  # OpenWorks R5000
    object_coordinate_system_id_source: str | None = None  # OpenWorks R5000
    projected_coordinate_system: str | None = None  # Petrel Studio
    projected_coordinate_unit: str | None = None  # Petrel Studio
    projected_coordinate_uuid: str | None = None  # Petrel Studio

    # Grid geometry and properties
    xinc: float | None = None
    yinc: float | None = None
    xori: float | None = None
    yori: float | None = None
    rotation: float | None = None
    yflip: int | None = None
    ncol: int | None = None
    nrow: int | None = None
    ntotal: int | None = None
    nnan: int | None = None

    # Timestamps
    create_date: datetime | None = None
    create_date_source: datetime | None = None
    create_date_source_utc: datetime | None = None
    update_date: datetime | None = None
    update_date_source: datetime | None = None
    update_date_source_utc: datetime | None = None

    # SMDA
    smda_project_uuid: str | None = None
    cs_smda_project_uuid: int | None = None

    # Bulk file and deletion status
    file_availability: str | None = None
    deleted: bool | None = None
    deleted_date: datetime | None = None
