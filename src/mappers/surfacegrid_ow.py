import math

from models.metadata import SourceContext
from models.metadata import SourceMetadata, SourceSystem, OWMetadata, ProcessingMetadata
from models.interpretation import GridGeometry
from models.interpretation import SurfaceGridRecord
from mappers.metadata_ow import convert_date_to_utc
from dsis_model_sdk.models.common import SurfaceGrid, SurfaceGridProperties


def map_surfacegrid(
    ow_surface: SurfaceGrid | SurfaceGridProperties,
    source_context: SourceContext,
    processing_metadata: ProcessingMetadata | None = None,
) -> SurfaceGridRecord:
    """Map an OW SurfaceGrid to a SurfaceGridRecord.

    Args:
        ow_surface: DSIS CommonModel surface object to convert
        source_context: SourceContext with database/project info
        processing_metadata: optional processing metadata (UUIDs, timestamps, etc.)

    Returns:
        SurfaceGridRecord instance
    """
    if ow_surface.update_date is None:
        ow_surface.update_date = ow_surface.create_date
        ow_surface.update_user_id = ow_surface.create_user_id
    source_metadata = SourceMetadata(
        system=SourceSystem.OPENWORKS,
        database=source_context.database,
        project=source_context.project,
        
        id=ow_surface.native_uid,
        name=ow_surface.map_data_set_name,
        remark=ow_surface.remark,

        create_user=ow_surface.create_user_id,
        update_user=ow_surface.update_user_id,
        create_date=ow_surface.create_date,
        create_date_utc=convert_date_to_utc(
            ow_surface.create_date, source_context.timezone
        ),
        update_date=ow_surface.update_date,
        update_date_utc=convert_date_to_utc(
            ow_surface.update_date, source_context.timezone
        ),

        ow=OWMetadata(
            geo_name=ow_surface.geo_name,
            geo_type=ow_surface.geo_type,
            attribute=ow_surface.attribute,
        ),
    )

    geometry = GridGeometry(
        ncol=ow_surface.num_cols,
        nrow=ow_surface.num_rows,
        xori=ow_surface.rotation_origin_x,
        yori=ow_surface.rotation_origin_y,
        xinc=ow_surface.grid_interval_x,
        yinc=ow_surface.grid_interval_y,
        rotation=math.degrees(ow_surface.rotation_i)
        if ow_surface.rotation_i is not None
        else None,
        left_handed=True,
    )

    return SurfaceGridRecord(
        source=source_metadata,
        processing=processing_metadata,
        geometry=geometry,
        crs=ow_surface.crs or source_context.crs,
        z_domain=ow_surface.data_domain,
        z_unit=ow_surface.z_unit,
        extent=None,  # TODO: calculate from grid geometry
    )
