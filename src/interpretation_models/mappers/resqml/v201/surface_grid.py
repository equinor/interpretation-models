import math
import typing
import uuid
from datetime import datetime, timezone

import numpy as np
import resqml_objects.v201 as ro
from resqml_objects.surface_helpers import rotate_2d_vector
from interpretation_models.models import SurfaceGridRecord
from interpretation_models.tables import flatten_record


class CRSInfo(typing.NamedTuple):
    """Container with relevant CRS information (for our use-case) fetched from
    a `reference-data--CoordinateSystemReference:1.*`-object in OSDU core.
    """

    name: str
    record_id: str
    code_space: str
    code_as_number: int
    crs_type: str
    horizontal_units: str | None


def time_length_unit_mapper(unit: str) -> ro.TimeUom | ro.LengthUom:
    # Clean the units; make them lower and strip trailing whitespace.
    unit = unit.lower().strip()

    try:
        return ro.LengthUom(unit)
    except ValueError:
        pass

    try:
        return ro.TimeUom(unit)
    except ValueError:
        pass

    match unit:
        case "meter" | "meters":
            return ro.LengthUom.M

    raise ValueError(f"Unit {unit} does not have a mapping to RESQML units")


def zincreasing_downward_map(z_domain: str) -> bool:
    # Clean the domain text.
    z_domain = z_domain.upper().strip()

    if z_domain in ["TVD", "MD", "TVT", "TST", "TIME"]:
        return True
    elif z_domain in ["TVDSS", "SSTVD"]:
        return False

    raise ValueError(f"Domain {z_domain} is currently not covered")


class SurfaceGridResqmlObject(typing.NamedTuple):
    epc: ro.obj_EpcExternalPartReference
    crs: ro.AbstractLocal3dCrs
    gri: ro.obj_Grid2dRepresentation
    path_in_hdf_file: str


def surface_grid_record_to_resqml(
    surface: SurfaceGridRecord,
    uuid_namespace: uuid.UUID,
    crs_osdu_map: typing.Callable[[str], CRSInfo],
    originator: str | None = None,
    description: str | None = None,
) -> SurfaceGridResqmlObject:
    """Function mapping a `SurfaceGridRecord`-object to RESQML v2.0.1 objects.

    Parameters
    ----------
    surface
        A `SurfaceGridRecord`-object to be mapped to RESQML.
    uuid_namespace
        A `uuid.UUID`-object that can be used as a namespace in the
        `uuid.uuid5`-call. The purpose is to ensure reproducible uuid-strings
        within a shared namespace.
    crs_osdu_map
        A callback that takes in a crs-string (read from
        `SurfaceGridRecord.source.crs`) and returns a `CRSInfo`-object. The
        intention is to the delegate the connection details to the caller.
    originator
        An optional parameter (provided that the `SurfaceGridRecord`-object
        contains information on the original creator) to tell who created the
        objects. Ideally this should not be necessary as we store the creator
        (and updater) from the source, i.e., the `SurfaceGridRecord`.
    description
        An optional descriptive string that can be included. This string has no
        functional value, but can be useful for logging purposes.

    Returns
    -------
    SurfaceGridResqmlObject
        The three RESQML v2.0.1 objects needed to represent a regular surface
        grid, along with the `path_in_hdf_file`-string used to index the array.
    """
    if surface.id is None:
        raise ValueError("Missing surface id")

    if surface.geometry.left_handed is None:
        raise ValueError("Missing `geometry.left_handed`-field")

    if surface.geometry.nrow is None:
        raise ValueError("Missing `geometry.nrow`-field")

    if surface.geometry.ncol is None:
        raise ValueError("Missing `geometry.ncol`-field")

    if surface.geometry.rotation is None:
        raise ValueError("Missing `geometry.rotation`-field")

    # We should not process a surface if the `surface.source.crs` is missing.
    if surface.source.crs is None:
        raise ValueError("Missing source crs")

    if originator is None and surface.source.create_user is None:
        raise ValueError(
            "Missing `surface.source.create_user` and `originator`. Provide an "
            "`originator`."
        )

    # We currently don't process any other domains than `"TIME"` and `"DEPTH"`.
    if surface.z_domain == "OTHER":
        raise ValueError("Invalid domain")

    # Use repeatable uuuids.
    epc_uuid = uuid.uuid5(uuid_namespace, f"{surface.id}|epc")
    crs_uuid = uuid.uuid5(uuid_namespace, f"{surface.id}|crs")
    gri_uuid = uuid.uuid5(uuid_namespace, f"{surface.id}|grid")

    title = surface.source.name or surface.id
    now = datetime.now(tz=timezone.utc)

    shared_citation = ro.Citation(
        # Use the same title for all three objects. The type of the object will
        # distinguish them.
        title=title,
        # We use the source creator and editor for the originator and editor
        # fields. Same for creation and update datetimes.
        originator=surface.source.create_user or originator,
        creation=surface.source.create_date_utc
        or surface.processing.create_date_utc
        or now,
        editor=surface.source.update_user or originator or surface.source.create_user,
        # The `last_update`-field can be `None`.
        last_update=surface.source.update_date_utc
        or surface.processing.update_date_utc,
        description=description,
    )

    # No additional metadata on the epc-object. It is often ignored later on.
    epc = ro.obj_EpcExternalPartReference(citation=shared_citation, uuid=epc_uuid)

    # Put the raw CRS-string into an `ObjectAlias`-object.
    raw_crs_alias = ro.ObjectAlias(
        identifier=surface.source.crs,
        # Equinor is the authority for the `ST_`-strings.
        authority="Equinor",
    )

    z_unit = time_length_unit_mapper(surface.source.z_unit)

    # Check that the z-unit makes sense for the z-domain. A length-based
    # (`ro.LengthUom`) z-unit should have a z-domain of `"DEPTH"`. Similarly,
    # for the time-based units and domain. Otherwise the combination is
    # invalid.
    if not (
        isinstance(z_unit, ro.LengthUom)
        and surface.z_domain == "DEPTH"
        or isinstance(z_unit, ro.TimeUom)
        and surface.z_domain == "TIME"
    ):
        raise ValueError(
            f"Invalid combination of z-unit ({z_unit} from {surface.source.z_unit}) "
            f"and z-domain ({surface.z_domain})"
        )

    # We will look up the crs-string via OSDU core. From this we get (1) the
    # projected EPSG-code (if there is an EPSG-code), (2) the projected unit,
    # and (3) an id to the reference crs in OSDU core.
    # The `SurfaceGridRecord`-object currently only supports a single
    # crs-string, and this _must_ be a projected (horizontal) crs (otherwise we
    # don't support it).  In other words, we should not get any vertical
    # crs-strings.

    osdu_crs = crs_osdu_map(surface.source.crs)
    assert osdu_crs.name == surface.source.crs

    # Catch invalid crs types. We only deal with projected and bound crses.
    if osdu_crs.crs_type not in ["ProjectedCRS", "BoundCRS"]:
        raise NotImplementedError(
            f"Unsupported coordinate reference system type: {osdu_crs.crs_type}"
        )

    # If the horizontal units are missing (i.e., `None`), we are most likely
    # dealing with a vertical crs, which we do not support.
    if osdu_crs.horizontal_units is None:
        raise ValueError(f"Missing horizontal units for crs '{surface.source.crs}'")

    if osdu_crs.code_space.lower() == "epsg":
        projected_epsg_code = osdu_crs.code_as_number
        assert 1024 <= projected_epsg_code < 32767
        projected_crs = ro.ProjectedCrsEpsgCode(epsg_code=projected_epsg_code)
    elif osdu_crs.code_space.lower() == "equinor":
        # Add the EPSG-like code from Equinor as an unknown crs.
        projected_crs = ro.ProjectedUnknownCrs(
            unknown=f"Equinor code: {osdu_crs.code_as_number}",
        )

    # Hacky way to get the data partition id for comparing the projected uom
    # values.
    data_partition_id = osdu_crs.record_id.split(":")[0]
    projected_uom_map = {
        f"{data_partition_id}:reference-data--UnitOfMeasure:m:": ro.LengthUom.M,
    }
    projected_uom = projected_uom_map[osdu_crs.horizontal_units]

    vertical_crs = ro.VerticalUnknownCrs(unknown="missing")
    if isinstance(z_unit, ro.LengthUom):
        vertical_uom = z_unit
    else:
        # Here the data is in the time-domain, and we have a time-unit
        # (e.g., milliseconds) for the z-axis. However, this should be put
        # in the `time_uom`-field of the `ro.obj_LocalTime3dCrs`-object.
        # The `vertical_uom`-field should ideally be connected to a vertical
        # crs, but as this is missing we assume meters. The
        # `vertical_uom`-field is a little strange in this case.
        vertical_uom = ro.LengthUom.M

    osdu_crs_alias = ro.ObjectAlias(
        identifier=osdu_crs.record_id,
        authority="osdu",
    )

    shared_crs_parameters = {
        "citation": shared_citation,
        "uuid": crs_uuid,
        "vertical_crs": vertical_crs,
        "projected_crs": projected_crs,
        # Explictily set zero rotation for the crs. The rotation is kept in the
        # grid instead.
        "areal_rotation": ro.PlaneAngleMeasure(value=0.0, uom=ro.PlaneAngleUom.RAD),
        # Zero offset for the crs. Leave the local crs unaltered from the
        # global crs (the EPSG-code, or crs-references in the aliases).
        "xoffset": 0.0,
        "yoffset": 0.0,
        "zoffset": 0.0,
        # We leave the axis-order to be the "canonical" choice.
        "projected_axis_order": ro.AxisOrder2d.EASTING_NORTHING,
        "projected_uom": projected_uom,
        # See comments above on the strangeness of this field when we are
        # dealing with a `ro.obj_LocalTime3dCrs`-object.
        "vertical_uom": vertical_uom,
        # The direction of positive z-values is decided by the `source.z_domain`.
        "zincreasing_downward": zincreasing_downward_map(surface.source.z_domain),
        "aliases": [raw_crs_alias, osdu_crs_alias],
    }

    if isinstance(z_unit, ro.LengthUom):
        crs = ro.obj_LocalDepth3dCrs(**shared_crs_parameters)
    else:
        assert isinstance(z_unit, ro.TimeUom)
        crs = ro.obj_LocalTime3dCrs(time_uom=z_unit, **shared_crs_parameters)

    # The `geometry.left_handed`-field is the same as the `yflip`-parameter in
    # `xtgeo`, and should be interpreted as such (i.e., it is independent of
    # the direction of z). If `geometry.left_handed == True` we have that:
    #
    #   y[0] = y_0, y[1] = y_0 + dy, ..., y[n - 1] = y_0 + (n - 1) * dy,
    #
    # and for `geometry.left_handed == False` we get the opposite:
    #
    #   y[0] = y_0, y[1] = y_0 - dy, ..., y[n - 1] = y_0 - (n - 1) * dy,
    #
    # where we assume that `yinc` (called `dy` in this comment) is positive.
    # Handling this flag can be done two ways (not at the same time!!!):
    #
    #   1. Flip the sign of the y-unit vector.
    #   2. Flip the sign of `yinc`.
    #
    # Of these we will choose 1, as a negative value for the step-size seems
    # unorthodox.

    # Convert the rotation in degrees to radians.
    angle = math.radians(surface.geometry.rotation)

    # With `surface.geometry.left_handed == True` we have the first axis
    # rotated by an angle `angle` from "x-axis" ([1.0, 0.0]-direction), and the
    # second axis rotated an additional 90 degrees from the first axis (or
    # rotating by the same angle `angle` relative to "y-axis" (the [0.0,
    # 1.0]-direction)).
    #
    #   y
    #   ^
    #   |           with z pointing into the screen.
    #   |
    #   ----> x
    #
    # _If_ the z-axis points down (which it often does in our
    # case) this would constitute a left-handed three dimensional system (note
    # that the flag `surface.geometry.left_handed` is independent of the z-axis
    # set from the domain and should be seen as the handedness of a system with
    # a fixed z-axis pointing down). When `surface.geometry.left_handed ==
    # False` the second axis (the "y-axis") is mirrored over the first axis.
    # This corresponds to rotating the second axis by an angle `angle + pi`
    # relative to the "y-axis" ([0.0, 1.0]-direction).
    #
    #   ----> x
    #   |
    #   |           with z pointing into the screen.
    #   v
    #   y
    #
    unit_vec_1 = np.squeeze(rotate_2d_vector(np.array([1.0, 0.0]), angle=angle))
    unit_vec_2 = np.squeeze(rotate_2d_vector(np.array([0.0, 1.0]), angle=angle))

    if not surface.geometry.left_handed:
        # Right-handed system (when z is pointing down) so we rotate the second
        # axis by an angle `pi`, i.e., flip the sign of the unit vector.
        unit_vec_2 = -unit_vec_2

    gri = ro.obj_Grid2dRepresentation.from_regular_surface(
        citation=shared_citation,
        uuid=gri_uuid,
        crs=crs,
        epc_external_part_reference=epc,
        shape=(surface.geometry.ncol, surface.geometry.nrow),
        origin=np.array([surface.geometry.xori, surface.geometry.yori]),
        spacing=np.array([surface.geometry.xinc, surface.geometry.yinc]),
        unit_vec_1=unit_vec_1,
        unit_vec_2=unit_vec_2,
        extra_metadata=[
            ro.NameValuePair(name=k, value=str(v))
            for k, v in flatten_record(surface).items()
        ],
    )

    return SurfaceGridResqmlObject(
        epc=epc,
        crs=crs,
        gri=gri,
        path_in_hdf_file=gri.grid2d_patch.geometry.points.zvalues.values.path_in_hdf_file,
    )
