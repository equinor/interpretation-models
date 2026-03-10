from pydantic import BaseModel
from enum import Enum


class SourceSystem(str, Enum):
    OPENWORKS = "OpenWorks R5000"  # or 'OpenWorks'?
    PETREL = "Petrel Studio"


class Database(BaseModel):
    name: str
    timezone: str


class Project(BaseModel):
    name: str
    database: Database | None = None
    smda_uuid: str | None = None
    last_pipeline_run_date: str | None = None


class Collection(BaseModel):
    id: str  # SID UUID