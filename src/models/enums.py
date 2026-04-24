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
