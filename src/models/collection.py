from pydantic import BaseModel
from models.metadata import SourceMetadata, ProcessingMetadata, OWCollectionMetadata, OWCollectionItemMetadata


class CollectionItem(BaseModel):
    collection_id: str
    object_id: str
    datatype: str
    source: SourceMetadata | None = None
    processing: ProcessingMetadata | None = None
    source_ow: OWCollectionItemMetadata | None = None
    

class Collection(BaseModel):
    source: SourceMetadata | None = None
    processing: ProcessingMetadata | None = None
    source_ow: OWCollectionMetadata | None = None
