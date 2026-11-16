import typing
import collections.abc

import numpy as np
import numpy.typing as npt

import resqml_objects.v201 as ro
from dsis_model_sdk.models.common import MappingPolygon, MappingPolygonSet


def map_line_role(polygon_set_data_type: str) -> ro.LineRole:
    match polygon_set_data_type:
        case "FAULT":
            return ro.INTERPRETATION_LINE

    raise NotImplementedError(
        f"Polygon set type `{polygon_set_data_type}` not mapped to a RESQML LineRole"
    )


class ResqmlPolygons(typing.NamedTuple):
    epc: ro.obj_EpcExternalPartReference
    crs: ro.AbstractLocal3dCrs
    pol: ro.obj_PolylineSetRepresentation
    data_arrays: collections.abc.Mapping[str, npt.NDArray[np.float64, np.bool_]]


def mapping_polygons_to_resqml(
    mapping_polygon_set: MappingPolygonSet,
    mapping_polygons: collections.abc.Sequence[MappingPolygon],
    crs_osdu_map: typing.Callable[[str], CRSInfo],
    originator: str | None = None,
    description: str | None = None,
) -> ResqmlPolygons:
    pass
