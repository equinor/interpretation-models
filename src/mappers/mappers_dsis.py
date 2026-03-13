import datetime
import math

from models.origin import Project
from models.interpretation import SourceMetadata, OWMetadata, PipelineMetadata
from models.surface import GridGeometry, Surface
from dsis_model_sdk.models.common import SurfaceGrid, SurfaceGridProperties


def normalize_surfacegrid_payload(payload: dict) -> dict:
    normalized = dict(payload)

    rotation_i = normalized.get("rotation_i")
    if rotation_i is not None:
        normalized["rotation_i"] = round(float(rotation_i), 4)

    rotation_j = normalized.get("rotation_j")
    if rotation_j is not None:
        normalized["rotation_j"] = round(float(rotation_j), 4)

    data_min = normalized.get("data_min")
    if data_min is not None:
        normalized["data_min"] = round(float(data_min), 3)

    data_max = normalized.get("data_max")
    if data_max is not None:
        normalized["data_max"] = round(float(data_max), 3)

    return normalized


def ow_to_sid(
    project: Project,
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
        date: datetime.datetime | None = None, timezone: str | None = None
    ) -> datetime.datetime | None:
        pass  # TODO: implement time conversion to UTC based on the timezone from Project table

    if ow_surface.crs is None:
        raise ValueError("SurfaceGrid.crs is required to map to SourceMetadata")

    source_metadata = SourceMetadata(
        project=project,
        native_uid=ow_surface.native_uid,
        name=ow_surface.map_data_set_name,
        crs=ow_surface.crs,
        z_domain=ow_surface.data_domain,
        z_unit=ow_surface.z_unit,
        create_user=ow_surface.create_user_id,
        update_user=ow_surface.update_user_id,
        remark=ow_surface.remark,
        create_date=ow_surface.create_date,
        create_date_utc=convert_date_to_utc(ow_surface.create_date, project.timezone),
        update_date=ow_surface.update_date,
        update_date_utc=convert_date_to_utc(ow_surface.update_date, project.timezone),
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
