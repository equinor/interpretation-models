"""Mappers for SurfaceGrid model conversions."""

from models.surface import Surface
from dsis_model_sdk.models.common import SurfaceGrid, SurfaceGridProperties


def ow_to_sid(ow_surface: SurfaceGrid | SurfaceGridProperties) -> Surface:
    """Map OW surface schema to the internal Surface model.
    
    Args:
        ow_surface: DSIS CommonModel surface object to convert
        
    Returns:
        Surface instance
    """
    return Surface(
        id=ow_surface.native_uid,
        source="OpenWorks",
        name=ow_surface.map_data_set_name,
        crs_identifier=ow_surface.crs,
        extent=None,  # TODO: calculate from grid geometry
        collection=[],  # TODO
        create_user_source=ow_surface.create_user_id,
        update_user_source=ow_surface.update_user_id,
        source_database=None,  # TODO: needs to come from the pipeline
        source_project=None,   # TODO: needs to come from the pipeline
        source_project_smda_uuid=None,  # TODO: needs to come from the pipeline
        create_date=None,  # TODO: needs to come from the pipeline
        create_date_source=ow_surface.create_date,
        create_date_source_utc=None,  # TODO: convert create_date_source to UTC
        update_date=None,  # TODO: needs to come from the pipeline
        update_date_source=ow_surface.update_date,
        update_date_source_utc=None,  # TODO: convert update_date_source to UTC
        ncol=ow_surface.num_cols,
        nrow=ow_surface.num_rows,
        xori=None,  # TODO: calculate from grid geometry
        yori=None,  # TODO: calculate from grid geometry
        xinc=None,  # TODO: calculate from grid geometry
        yinc=None,  # TODO: calculate from grid geometry
        rotation=None,  # TODO: calculate from grid geometry
        geo_name=ow_surface.geo_name,
        geo_type=ow_surface.geo_type,
        z_unit=ow_surface.z_unit,
        z_non=ow_surface.data_null_value,
        z_domain=ow_surface.data_domain,
        attribute_source=ow_surface.attribute,
        # interpreter_source=None,    # TODO: remove? interpreter not in LMK CM
        remark_source=ow_surface.remark,
        business_project_source=None,
        data_status_source=None,
        confidence_factor_source=None,
        file_availability=None,  # TODO: needs to come from the pipeline
        deleted=None,  # TODO: needs to come from the pipeline
        deleted_date=None,  # TODO: needs to come from the pipeline
    )