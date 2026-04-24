from models.metadata import SourceContext
from models.enums import SourceSystem, OWDataType, DataType
from models.metadata import SourceMetadata, ProcessingMetadata, OWCollectionMetadata, OWCollectionItemMetadata, InterpretationProcessingMetadata
from models.collection import Collection, CollectionItem
from mappers.metadata_ow import convert_date_to_utc, id_generate
from dsis_model_sdk.models.native import InterpretationSet, ISetDataObject


def map_collection(
    ow_iset: InterpretationSet,
    source_context: SourceContext,
    processing_metadata: InterpretationProcessingMetadata | None = None,
) -> Collection:
    """Map an OW InterpretationSet to a Collection.

    Args:
        ow_iset: DSIS CommonModel interpretation set object to convert
        source_context: SourceContext with database/project info
        processing_metadata: optional processing metadata (UUIDs, timestamps, etc.)

    Returns:
        Collection instance
    """
    if ow_iset.update_date is None:
        ow_iset.update_date = ow_iset.create_date
        ow_iset.update_user_id = ow_iset.create_user_id

    source_metadata = SourceMetadata(
        id=id_generate(source_context, ow_iset.interpretation_set_id),
        system=SourceSystem.OPENWORKS,
        database=source_context.database,
        project=source_context.project,
        name=ow_iset.interpret_set_name,
        remark=ow_iset.remark,

        create_user=ow_iset.create_user_id,
        update_user=ow_iset.update_user_id,
        create_date=ow_iset.create_date,
        create_date_utc=convert_date_to_utc(
            ow_iset.create_date, source_context.timezone
        ) if ow_iset.create_date is not None else None,
        update_date=ow_iset.update_date,
        update_date_utc=convert_date_to_utc(
            ow_iset.update_date, source_context.timezone
        ) if ow_iset.update_date is not None else None,
    )

    source_ow_metadata = OWCollectionMetadata(
        field_prospect_name=ow_iset.field_prospect_name,
    )

    return Collection(
        source=source_metadata,
        source_ow=source_ow_metadata,
        processing=processing_metadata
    )
