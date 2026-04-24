from enum import Enum


class SourceSystem(str, Enum):
    OPENWORKS = "OpenWorks R5000"
    PETREL = "Petrel Studio"


class DataType(str, Enum):
    SURFACE_GRID = "SurfaceGrid"
    HORIZON = "Horizon"
    POLYGON = "Polygon"
    FAULT = "Fault"
    POINT_SET = "PointSet"
    OTHERS = "Others"


class UpdateType(str, Enum):
    OBJECT_CREATE = "ObjectCreate"
    OBJECT_UPDATE = "ObjectUpdate"
    OBJECT_DELETE = "ObjectDelete"
    COLLECTION_INSERT = "CollectionInsert"
    COLLECTION_DELETE = "CollectionDelete"


class OWDataType(str, Enum):
    MAP2D = "Map2D"
    RGRID = "Rgrid"
    HORIZON3D = "HorizonAttributeCatalog"
    POLYGON_SET = "MappingPolySet"
    POINT_SET = "PointSet"
    OTHERS = "Others"
