from pydantic import BaseModel


class Project(BaseModel):
    name: str
    database: str | None = None
    smda_uuid: str | None = None
    timezone: str | None = None
