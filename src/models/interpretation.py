from pydantic import BaseModel

class Interpretation(BaseModel):
    id: str
    name: str
    crs_identifier: str
