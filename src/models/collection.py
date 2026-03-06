from pydantic import BaseModel


class Collection(BaseModel):
    id: str  # SID UUID
