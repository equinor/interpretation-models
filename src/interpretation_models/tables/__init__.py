from interpretation_models.tables.tablespec import ColumnSpec, ForeignKeySpec, ModelTableDef, TableSpec
from interpretation_models.tables.model_to_table import (
    flatten_columns,
    flatten_record,
    model_to_tablespec,
    tablespec_to_json,
)

__all__ = [
    "ColumnSpec",
    "ForeignKeySpec",
    "ModelTableDef",
    "TableSpec",
    "flatten_columns",
    "flatten_record",
    "model_to_tablespec",
    "tablespec_to_json",
]
