import json
import re

from models import SourceContext
from models import OWDataType, InterpretationDataType
from models import ProcessingMetadata, OWCollectionMetadata, OWCollectionItemMetadata, InterpretationProcessingMetadata
from models import Collection, CollectionItem
from mappers.openworks.metadata import source_metadata_from_ow, _id_generate
from dsis_model_sdk.models.native import InterpretationSet, ISetDataObject


def collection_from_ow(
    ow_iset: InterpretationSet,
    source_context: SourceContext,
    processing_metadata: InterpretationProcessingMetadata | None = None,
) -> Collection:
    """Map an OW InterpretationSet to a Collection.

    Args:
        ow_iset: DSIS CommonModel interpretation set object to convert
        source_context: SourceContext with database/project info
        processing_metadata: optional processing metadata (UUIDs, timestamps, etc.)

    Returns:
        Collection instance
    """
    source_metadata = source_metadata_from_ow(
        ow_object=ow_iset,
        source_context=source_context,
        id=_id_generate(source_context, ow_iset.interpretation_set_id),
        name=ow_iset.interpret_set_name,
    )

    source_ow_metadata = OWCollectionMetadata(
        field_prospect_name=ow_iset.field_prospect_name,
    )

    return Collection(
        id=_id_generate(source_context, ow_iset.interpretation_set_id),
        source=source_metadata,
        source_ow=source_ow_metadata,
        processing=processing_metadata
    )


def _map_dataobject_datatype(ow_datatype: OWDataType) -> InterpretationDataType:
    mapping = {
        OWDataType.MAP2D: InterpretationDataType.SURFACE_GRID,
        OWDataType.RGRID: InterpretationDataType.SURFACE_GRID,
        OWDataType.HORIZON3D: InterpretationDataType.HORIZON,
        OWDataType.POLYGON_SET: InterpretationDataType.POLYGON,
        OWDataType.POINT_SET: InterpretationDataType.POINT_SET,
    }
    return mapping.get(ow_datatype, InterpretationDataType.OTHERS)


def _resolve_map2d_grid_id(native_uid: str | None) -> str:
    if native_uid is None:
        return ""

    try:
        native_uid_data = json.loads(native_uid)
    except (TypeError, json.JSONDecodeError):
        return ""

    data_key = native_uid_data.get("data_key") if isinstance(native_uid_data, dict) else None
    if not isinstance(data_key, str):
        return ""

    match = re.search(r"(?:^|;)gridId=([^;]+)", data_key)
    return match.group(1).strip() if match and match.group(1).strip() else ""


def _resolve_id(ow_data_object: ISetDataObject) -> str:
    """
    SurfaceGrids in ISetDataObjects can be of type Map2D or RGrid.
    Rgrids are the simpler original grid type, which correponds to a simple grid, with the id set to the data object id.
    Map2D objects are created when the user drags a "Grid & Contour" object into the ISet.
    The Map2D is a container and contains a reference to the Rgrid object plus a polygon with its contour.
    Therefore, the data object id associated with it, is not the id of the grid, but of the container.
    For the Map2D objects, the grid_id of the internal surface is extracted from the native_uid, which is a json-like string.
    We thus have to first get the value of the key "data_key", which is itself a list of property=value pairs
    encoded in a colon-separated string.  We then extract the gridId property value from that list using a regexp.
    In the future, other dtataypes may need to be parsed for exceptions in their ids as well.
    """
    if ow_data_object.data_type == OWDataType.MAP2D.value:
        return _resolve_map2d_grid_id(ow_data_object.native_uid)

    # for objects other than Map2D, we assume the data object id is the direct id of the intended object
    if not ow_data_object.data_object_id:
        return ""
    return str(ow_data_object.data_object_id) 


def collection_item_from_ow(
    ow_data_object: ISetDataObject,
    source_context: SourceContext,
    processing_metadata: ProcessingMetadata | None = None,
) -> CollectionItem:
    """Map an OW ISetDataObject to a CollectionItem.

    Args:
        ow_data_object: DSIS native ISetDataObject to convert
        collection_id: processing_id of the parent Collection
        source_context: SourceContext with database/project info
        processing_metadata: optional processing metadata (UUIDs, timestamps, etc.)

    Returns:
        CollectionItem instance
    """
    ow_id: str = str(ow_data_object.data_object_id) if ow_data_object.data_object_id else ow_data_object.data_key
    source_metadata = source_metadata_from_ow(
        ow_object=ow_data_object, 
        source_context=source_context,
        id=ow_id,
        name=ow_data_object.data_object_name,
    )

    source_ow_metadata = OWCollectionItemMetadata(
        data_type=ow_data_object.data_type,
        data_key=ow_data_object.data_key,
        interpretation_set_id=ow_data_object.interpretation_set_id,
        iset_folder_id=ow_data_object.iset_folder_id,
    )

    ow_datatype: OWDataType = OWDataType(ow_data_object.data_type) if ow_data_object.data_type in OWDataType._value2member_map_ else OWDataType.OTHERS
    resolved_datatype: InterpretationDataType = _map_dataobject_datatype(ow_datatype)
    resolved_id = _resolve_id(ow_data_object)
    collection_id = ow_data_object.interpretation_set_id

    return CollectionItem(
        id = _id_generate(source_context, f"Collection:{collection_id}:{resolved_datatype.value}:{resolved_id}"),
        collection_id=_id_generate(source_context, collection_id),
        object_id=_id_generate(source_context, resolved_id),
        datatype=resolved_datatype,
        source=source_metadata,
        source_ow=source_ow_metadata,
        processing=processing_metadata,
    )
