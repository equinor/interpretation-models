from pydantic import BaseModel
from models.enums import InterpretationDataType
from models.metadata import SourceMetadata, ProcessingMetadata, OWCollectionMetadata, OWCollectionItemMetadata


class CollectionItem(BaseModel):
    collection_id: str
    object_id: str
    datatype: InterpretationDataType
    source: SourceMetadata | None = None
    source_ow: OWCollectionItemMetadata | None = None
    processing: ProcessingMetadata | None = None


class Collection(BaseModel):
    id: str
    source: SourceMetadata | None = None
    source_ow: OWCollectionMetadata | None = None
    processing: ProcessingMetadata | None = None
