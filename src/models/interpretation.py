from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from models.extent import Extent
from models.collection import Collection
from models.project import Project


class SourceSystem(str, Enum):
    OPENWORKS = "OpenWorks"  # or 'OpenWorks R5000'?
    PETREL = "Petrel Studio"


class OWMetadata(BaseModel):
    geo_name: str | None = None
    geo_type: str | None = None
    attribute: str | None = None


class PetrelMetadata(BaseModel):
    business_project: str | None = None
    data_status: str | None = None
    confidence_factor: str | None = None


class SourceMetadata(BaseModel):
    system: SourceSystem
    # database: str | None = None
    # project: str | None = None
    native_uid: str | None = None
    name: str
    crs_identifier: str
    z_domain: str | None = None
    z_unit: str | None = None
    create_user: str | None = None
    update_user: str | None = None
    remark: str | None = None
    create_date: datetime | None = None
    create_date_utc: datetime | None = None
    update_date: datetime | None = None
    update_date_utc: datetime | None = None
    ow: OWMetadata | None = None
    petrel: PetrelMetadata | None = None


class PipelineMetadata(BaseModel):
    id: str  # SID UUID
    database: str | None = None
    project: Project | None = None
    project_smda_uuid: str | None = None  # from Project table?
    create_date: datetime | None = None
    update_date: datetime | None = None
    file_availability: str | None = None
    deleted: bool | None = None
    deleted_date: datetime | None = None


class Interpretation(BaseModel):
    source: SourceMetadata | None = None
    pipeline: PipelineMetadata | None = None
    extent: Extent | None = None
    collection: list[Collection]
