from pydantic import BaseModel
from interpretation_models.models.enums import InterpretationDataType
from interpretation_models.models.interpretations.metadata import SourceMetadata, ProcessingMetadata, OWCollectionMetadata, OWCollectionItemMetadata


class CollectionItem(BaseModel):
    id:str
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
