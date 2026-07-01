import logging
from typing import TypeAlias

from interpretation_models.mappers.helpers import convert_date_to_utc
from interpretation_models.models import SourceContext, SourceMetadata, InterpretationSourceMetadata
from interpretation_models.models import SourceSystem

from dsis_model_sdk.models.common import SurfaceGrid, SurfaceGridProperties
from dsis_model_sdk.models.native import InterpretationSet, ISetDataObject


OWSourceObject: TypeAlias = (
      InterpretationSet
    | ISetDataObject
    | SurfaceGrid
    | SurfaceGridProperties
)


def source_metadata_from_ow(
    ow_object: OWSourceObject,
    source_context: SourceContext,
    *,
    id: str | None = None,
    name: str | None = None,
) -> SourceMetadata:
    """Map common OW metadata fields to SourceMetadata.

    Handles update-date fallback to create-date and UTC conversion.
    The ``id`` and ``name`` parameters are caller-specific since each OW type derives them differently.
    update date and user fallback to create date and user if empty, as OW doesn't set them at object creation
    """
    logging.debug("Calling source_metadata_from_ow()")

    update_date = ow_object.update_date or ow_object.create_date
    update_user = ow_object.update_user_id or ow_object.create_user_id
    
    return SourceMetadata(
        system=SourceSystem.OPENWORKS,
        database=source_context.database,
        project=source_context.project,
        id=id,
        name=name,
        remark=ow_object.remark,
        create_user=ow_object.create_user_id,
        update_user=update_user,
        create_date_utc=convert_date_to_utc(
            ow_object.create_date, source_context.timezone
        ) if ow_object.create_date is not None else None,
        update_date_utc=convert_date_to_utc(
            update_date, source_context.timezone
        ) if update_date is not None else None,
    )

def interpretation_source_metadata_from_ow(
    ow_object: OWSourceObject,
    source_context: SourceContext,
    *,
    id: str | None = None,
    name: str | None = None,
    crs: str | None = None,
    z_domain: str | None = None,
    z_unit: str | None = None,
) -> InterpretationSourceMetadata:
    """Map common OW metadata fields to InterpretationSourceMetadata, including interpretation-specific fields."""

    logging.debug("Calling interpretation_source_metadata_from_ow()")

    base_metadata = source_metadata_from_ow(ow_object, source_context, id=id, name=name)
    return InterpretationSourceMetadata(
        **base_metadata.model_dump(),
        crs=crs,
        z_domain=z_domain,
        z_unit=z_unit,
    )