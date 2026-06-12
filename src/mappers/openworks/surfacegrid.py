import math

from models import SourceContext
from models import OWSurfaceGridMetadata, InterpretationProcessingMetadata
from models import GridGeometry
from models import SurfaceGridRecord
from models import InterpretationDataType
from mappers.openworks import metadata
from mappers.helpers import id_generate
from dsis_model_sdk.models.common import SurfaceGrid, SurfaceGridProperties


def _calculate_extent_from_geometry(geometry: GridGeometry) -> None:
    return None  # TODO: implement extent calculation based on grid geometry (bulk data)

def _classify_domain_from_unit_type(z_unit_type: str | None) -> str:
    _DEFAULT_VALUE = 'OTHER'

    _DOMAIN_BY_UNIT_TYPE = {
        'depth measure': 'DEPTH',
        'seismic time': 'TIME',
    }

    if z_unit_type is None:
        return _DEFAULT_VALUE
    
    return _DOMAIN_BY_UNIT_TYPE.get(z_unit_type.lower(), _DEFAULT_VALUE)

def _calculate_grid_ntotal(geometry: GridGeometry) -> int | None:
    return geometry.ncol * geometry.nrow if geometry.ncol is not None and geometry.nrow is not None else None

def _calculate_grid_nnan() -> int | None:
    return None  # TODO: implement grid nnan calculation based on grid values (bulk data), which are not yet included in the model

def surfacegrid_from_ow(
    ow_surface: SurfaceGrid | SurfaceGridProperties,
    source_context: SourceContext,
    processing_metadata: InterpretationProcessingMetadata | None = None,
) -> SurfaceGridRecord:
    """Map an OW SurfaceGrid to a SurfaceGridRecord.

    Args:
        ow_surface: DSIS CommonModel surface object to convert
        source_context: SourceContext with database/project info
        processing_metadata: optional processing metadata (UUIDs, timestamps, etc.)

    Returns:
        SurfaceGridRecord instance
    """
    # id is nullable, so we try to iterate through other unique attributes in case it is null
    native_id: str = ow_surface.native_uid or ow_surface.alternate_uid or ow_surface.map_data_set_name

    source_metadata = metadata.interpretation_source_metadata_from_ow(
        ow_object=ow_surface,
        source_context=source_context,
        id=native_id,
        name=ow_surface.map_data_set_name,
        crs=ow_surface.crs or source_context.crs,
        z_domain=ow_surface.data_domain,
        z_unit=ow_surface.z_unit,
    )

    source_ow_metadata = OWSurfaceGridMetadata(
        data_source=ow_surface.data_source,
        geo_name=ow_surface.geo_name,
        geo_type=ow_surface.geo_type,
        attribute=ow_surface.attribute,
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
        id=id_generate(source_context, f"{InterpretationDataType.SURFACE_GRID.value}:{native_id}"),
        source=source_metadata,
        source_ow=source_ow_metadata,
        processing=processing_metadata,
        grid_ntotal=_calculate_grid_ntotal(geometry),
        grid_nnan = _calculate_grid_nnan(),
        geometry=geometry,
        extent=_calculate_extent_from_geometry(geometry),
        z_domain=_classify_domain_from_unit_type(ow_surface.z_unit_type)
    )
