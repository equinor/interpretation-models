import datetime
import math

from models.origin import SourceSystem
from models.interpretation import (
    SourceMetadata,
    OWMetadata,
    PipelineMetadata
)
from models.surface import GridGeometry, Surface
from dsis_model_sdk.models.common import SurfaceGrid, SurfaceGridProperties


def ow_to_sid(
    ow_surface: SurfaceGrid | SurfaceGridProperties,
    pipeline_metadata: PipelineMetadata | None = None,
) -> Surface:
    """Map OW surface schema to the internal Surface model.

    Args:
        ow_surface: DSIS CommonModel surface object to convert
        pipeline_metadata: metadata calculated within or related to the run of the pipeline

    Returns:
        Surface instance
    """

    def convert_date_to_utc(
        date: datetime.datetime, timezone: str | None = None
    ) -> datetime.datetime | None:
        pass  # TODO: implement time conversion to UTC based on the timezone from Project table

    source_metadata = SourceMetadata(
        system=SourceSystem.OPENWORKS,
        native_uid=ow_surface.native_uid,
        name=ow_surface.map_data_set_name,
        crs=ow_surface.crs,
        z_domain=ow_surface.data_domain,
        z_unit=ow_surface.z_unit,
        create_user=ow_surface.create_user_id,
        update_user=ow_surface.update_user_id,
        remark=ow_surface.remark,
        create_date=ow_surface.create_date,
        create_date_utc=convert_date_to_utc(
            ow_surface.create_date,
            pipeline_metadata.database.timezone
        ),
        update_date=ow_surface.update_date,
        update_date_utc=convert_date_to_utc(
            ow_surface.update_date,
            pipeline_metadata.database.timezone
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
        left_handed=True,  # TODO: should this be default for surfaces from OW?
    )
    return Surface(
        source=source_metadata,
        pipeline=pipeline_metadata,
        geometry=geometry,
        extent=None,  # TODO: calculate from grid geometry
        collection=[],  # TODO
    )
