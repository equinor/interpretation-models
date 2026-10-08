import numpy as np
import uuid
from interpretation_models.mappers import surface_grid_record_to_resqml, CRSInfo
from interpretation_models.models import SurfaceGridRecord
from interpretation_models.tables import unflatten_record


class TestSurfaceGridRecordToResqml:
    def test_example_data_mapping(self, surface_grid_record) -> None:
        crs_info = CRSInfo(
            name=surface_grid_record.source.crs,
            record_id="dev:reference-data--CoordinateSystemReference:1.2.0:123456",
            code_space="EPSG",
            code_as_number=4567,
            crs_type="ProjectedCRS",
            horizontal_units="dev:reference-data--UnitOfMeasure:m:",
        )
        resqml_objs = surface_grid_record_to_resqml(
            surface_grid_record,
            uuid_namespace=uuid.uuid4(),
            crs_osdu_map=lambda s: crs_info,
        )
        crs = resqml_objs.crs
        assert surface_grid_record.source.create_user == crs.citation.originator
        assert surface_grid_record.source.update_user == crs.citation.editor
        equinor_crs_alias = next(
            filter(lambda a: a.authority == "Equinor", crs.aliases)
        )
        osdu_crs_alias = next(filter(lambda a: a.authority == "osdu", crs.aliases))
        assert surface_grid_record.source.crs == equinor_crs_alias.identifier
        assert crs_info.record_id == osdu_crs_alias.identifier
        assert (
            surface_grid_record.source.z_domain == "TVDSS"
            and not crs.zincreasing_downward
        )

        gri = resqml_objs.gri

        # Rebuild the surface grid record from the metadata.
        ret_surface_grid_record = unflatten_record(
            SurfaceGridRecord,
            {
                m.name: m.value if m.value != "None" else None
                for m in gri.extra_metadata
            },
        )
        assert surface_grid_record == ret_surface_grid_record

        assert surface_grid_record.geometry.ncol == gri.grid2d_patch.slowest_axis_count
        assert surface_grid_record.geometry.nrow == gri.grid2d_patch.fastest_axis_count
        offset1 = gri.grid2d_patch.geometry.points.supporting_geometry.offset[0]
        offset2 = gri.grid2d_patch.geometry.points.supporting_geometry.offset[1]
        origin = gri.grid2d_patch.geometry.points.supporting_geometry.origin
        uv1 = offset1.offset
        spacing1 = offset1.spacing
        uv2 = offset2.offset
        spacing2 = offset2.spacing
        angle_x = np.rad2deg(np.atan2(uv1.coordinate2, uv1.coordinate1))
        angle_y = np.rad2deg(np.atan2(uv2.coordinate2, uv2.coordinate1))

        assert abs(angle_x - surface_grid_record.geometry.rotation) < 1e-12
        assert (
            abs(
                angle_y + (-90)
                if surface_grid_record.geometry.left_handed
                else 90 - surface_grid_record.geometry.rotation
            )
            < 1e-12
        )
        assert abs(surface_grid_record.geometry.xori - origin.coordinate1) < 1e-12
        assert abs(surface_grid_record.geometry.yori - origin.coordinate2) < 1e-12
