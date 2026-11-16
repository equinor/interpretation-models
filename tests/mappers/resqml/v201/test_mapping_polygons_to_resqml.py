import datetime
import collections.abc

import numpy as np
import scipy.spatial
from dsis_model_sdk.models.common import MappingPolygon, MappingPolygonSet


def create_random_mapping_polygon(
    polygon_seq_no: int, mps: MappingPolygonSet, rng: np.random.Generator
) -> MappingPolygon:
    uid = (
        "{"
        + f'"polygon_set_id":{int(mps.native_uid)},"poly_seq_no":{polygon_seq_no}'
        + "}"
    )

    num_points = rng.integers(low=10, high=100)

    cx = rng.uniform(low=400_000, high=600_000)
    cy = rng.uniform(low=6_000_000, high=7_000_000)
    rand_x_coords = rng.normal(loc=cx, scale=100, size=num_points)
    rand_y_coords = rng.normal(loc=cy, scale=100, size=num_points)

    points = np.c_[rand_x_coords, rand_y_coords]

    hull = scipy.spatial.ConvexHull(points)

    polygon_x = np.zeros(len(hull.vertices) + 1)
    polygon_y = np.zeros_like(polygon_x)

    polygon_x[:-1] = points[hull.vertices, 0]
    polygon_y[:-1] = points[hull.vertices, 1]
    polygon_x[-1] = polygon_x[0]
    polygon_y[-1] = polygon_y[0]

    # For 2d-points, the `volume`-attribute gives the area, and the
    # `area`-attribute gives the perimeter of the polygon.
    polygon_area = hull.volume

    _z_data = np.random.rand(len(polygon_x) - 1)
    z_data = np.zeros_like(polygon_x)
    z_data[:-1] = _z_data
    z_data[-1] = z_data[0]

    mp = MappingPolygon(
        native_uid=uid,
        mappingpolygonset_native_uid=mps.native_uid,
        polygon_set_name=mps.polygon_set_name,
        data_source=mps.data_source,
        polygon_seq_no=polygon_seq_no,
        fault="fault",
        datum=mps.datum,
        depth_domain=mps.depth_domain,
        z_domain_qualifier=mps.z_domain_qualifier,
        unit_desc=mps.unit_desc,
        xy_unit=mps.xy_unit,
        datum_unit=mps.datum_unit,
        no_data_value=mps.no_data_value,
        polygon_type="pt",
        polygon_set_data_type=mps.polygon_set_data_type,
        area=polygon_area,
        color=None,
        poly_z_value=None,
        num_points=len(z_data),
        data={
            "x_coord": polygon_x.tolist(),
            "y_coord": polygon_y.tolist(),
            "z_value": z_data.tolist(),
            "throw_direction": [],
        },
        spatial=None,
        crs=mps.crs,
        z_value_unit="ms",
        area_unit="m2",
        poly_z_value_unit="ms",
        remark=None,
        create_date=mps.create_date,
        create_user_id=mps.create_user_id,
        update_date=mps.update_date,
        update_user_id=mps.update_user_id,
        alternate_uid=uid,
    )

    return mp


def create_random_mapping_polygons(
    mps: MappingPolygonSet, rng: np.random.Generator
) -> collections.abc.Sequence[MappingPolygon]:
    num_polygons = rng.integers(low=1, high=100)
    return [
        create_random_mapping_polygon(polygon_seq_no=i, mps=mps, rng=rng)
        for i in range(num_polygons)
    ]


def create_random_polygon_set(
    uid: int,
    rng: np.random.Generator,
) -> tuple[MappingPolygonSet, collections.abc.Sequence[MappingPolygon]]:
    now = datetime.datetime.now(tz=datetime.UTC)

    mps = MappingPolygonSet(
        native_uid=str(int(uid)),
        surface_name="surface-name",
        polygon_set_name="polygon-name",
        data_source="ds",
        datum=0,
        depth_domain="TIME",
        z_domain_qualifier=None,
        unit_desc="ms",
        max_x=0.0,
        max_y=0.0,
        min_x=0.0,
        min_y=0.0,
        no_data_value=None,
        crs="ST_ED50_UTM31N_P23031_T1133",
        polygon_set_data_type="FAULT",
        remark=None,
        xy_unit="meters",
        original_data_source="ods",
        datum_unit="meters",
        processing_parameter_nbytes=None,
        processing_parameter=None,
        create_date=now,
        create_user_id="foo-user-1",
        update_date=None,
        update_user_id=None,
        alternate_uid=str(int(uid)),
    )

    return mps, create_random_mapping_polygons(mps, rng)


class TestMappingPolygonsToResqml:
    pass
