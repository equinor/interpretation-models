import datetime
from typing import TypeAlias

from models.metadata import SourceContext, SourceMetadata
from models.enums import SourceSystem
import pytz

from dsis_model_sdk.models.common import SurfaceGrid, SurfaceGridProperties
from dsis_model_sdk.models.native import InterpretationSet, ISetDataObject


OWSourceObject: TypeAlias = (
      InterpretationSet
    | ISetDataObject
    | SurfaceGrid
    | SurfaceGridProperties
)

def _id_generate(
    context: SourceContext, native_id: str
) -> str:
    return f"{context.database}:{context.project}:{native_id}"


def _localize_date(
    date: datetime.datetime, timezone: str | None = None
) -> datetime.datetime:
    """Attach the given timezone to a naive datetime (or convert an aware one)."""
    if timezone is None:
        return date
    local_tz = pytz.timezone(timezone)
    return local_tz.localize(date) if date.tzinfo is None else date.astimezone(local_tz)


def _convert_date_to_utc(
    date: datetime.datetime, timezone: str | None = None
) -> datetime.datetime:
    if timezone is None:
        return date
    local_dt = _localize_date(date, timezone)
    return local_dt.astimezone(pytz.utc)


def source_metadata_from_ow(
    ow_object: OWSourceObject,
    source_context: SourceContext,
    *,
    id: str | None = None,
    name: str | None = None,
) -> SourceMetadata:
    """Map common OW metadata fields to SourceMetadata.

    Handles update-date fallback to create-date and date localization/UTC conversion.
    The ``id`` and ``name`` parameters are caller-specific since each OW type derives them differently.
    update date and user fallback to create date and user if empty, as OW doesn't set them at object creation
    """
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
        create_date=_localize_date(ow_object.create_date, source_context.timezone)
        if ow_object.create_date is not None else None,
        create_date_utc=_convert_date_to_utc(
            ow_object.create_date, source_context.timezone
        ) if ow_object.create_date is not None else None,
        update_date=_localize_date(update_date, source_context.timezone)
        if update_date is not None else None,
        update_date_utc=_convert_date_to_utc(
            update_date, source_context.timezone
        ) if update_date is not None else None,
    )
