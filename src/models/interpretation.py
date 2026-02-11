from pydantic import BaseModel
from datetime import datetime
from models.extent import Extent


class Interpretation(BaseModel):
    id: str                 # SID UUID
    source: str
    name: str
    crs_identifier: str     # from Project table?
    extent: Extent | None = None
    collection: list[int | None]    # list of IDs or names?
    create_user_source: str | None = None
    update_user_source: str | None = None

    # Origin
    source_database: str | None = None
    source_project: str | None = None
    source_project_smda_uuid: str | None = None     # from Project table?

    # Timestamps
    create_date: datetime | None = None
    create_date_source: datetime | None = None
    create_date_source_utc: datetime | None = None
    update_date: datetime | None = None
    update_date_source: datetime | None = None
    update_date_source_utc: datetime | None = None