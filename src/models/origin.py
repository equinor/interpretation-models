from pydantic import BaseModel
from enum import Enum


class SourceSystem(str, Enum):
    OPENWORKS = "OpenWorks R5000"  # or 'OpenWorks'?
    PETREL = "Petrel Studio"


class Project(BaseModel):
    source_system: SourceSystem
    database: str
    name: str
    timezone: str
    last_pipeline_run_date: str | None = None


class Collection(BaseModel):
    id: str  # SID UUID
