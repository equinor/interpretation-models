from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class SourceSystem(str, Enum):
    OPENWORKS = "OpenWorks R5000"
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
    system: SourceSystem | None = None
    database: str | None = None
    project: str | None = None
    id: str | None = None
    name: str | None = None
    remark: str | None = None
    create_user: str | None = None
    update_user: str | None = None
    create_date: datetime | None = None
    create_date_utc: datetime | None = None
    update_date: datetime | None = None
    update_date_utc: datetime | None = None
    ow: OWMetadata | None = None
    petrel: PetrelMetadata | None = None


class ProcessingMetadata(BaseModel):
    """
    Metadata related to the processing of the data, such as timestamps, UUIDs, etc.
    This is included only so these attributes can be included in the table schemas derived from the interpretation models,
    Callers can send the information to include directly in the output object without transformation.
    It is optional - if not storing intermediate processing information, this can be skipped.
    """
    id: str
    create_date: datetime | None = None
    update_date: datetime | None = None
    file_available: bool | None = None
    deleted: bool | None = None
    delete_date: datetime | None = None


class SourceContext(BaseModel):
    """
    Meant as input only so callers can represent project metadata which is not present in typed source objects.
    In the output models, the information derived from this is included as part of SourceMetadata.
    See docs/design_interpretations#source-context for more details.
    """
    database: str
    project: str
    timezone: str | None = None
    crs: str | None = None
