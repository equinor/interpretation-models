"""Generation of TableSpec instances from Pydantic models and serialization to JSON."""

import types
from collections.abc import Iterator
from datetime import datetime
from enum import Enum
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from tables.tablespec import ColumnSpec, ModelTableDef, TableSpec

# ---------------------------------------------------------------------------
# Type helpers
# ---------------------------------------------------------------------------

_SCALAR_TYPE_MAP: dict[type, str] = {
    str: "string",
    int: "integer",
    float: "float",
    bool: "boolean",
    datetime: "datetime",
}


def _unwrap_optional(annotation: Any) -> tuple[bool, Any]:
    """Return (is_nullable, inner_type) — unwraps ``X | None`` to ``(True, X)``."""
    origin = get_origin(annotation)
    if origin is Union or origin is types.UnionType:
        args = get_args(annotation)
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1 and type(None) in args:
            return True, non_none[0]
    return False, annotation


def _map_scalar_type(tp: type) -> str:
    if tp in _SCALAR_TYPE_MAP:
        return _SCALAR_TYPE_MAP[tp]
    if isinstance(tp, type) and issubclass(tp, Enum):
        return "string"
    return "json"


# ---------------------------------------------------------------------------
# Shared model-field walk
# ---------------------------------------------------------------------------


def _walk_model_fields(
    model: type[BaseModel],
    col_prefix: str = "",
    source_prefix: str = "",
) -> Iterator[tuple[str, str, FieldInfo, type, bool]]:
    """Recursively walk a Pydantic model and yield info for each leaf field.

    Nested ``BaseModel`` fields are expanded with an underscore-separated
    prefix.  Non-flattenable types (lists, dicts, …) are treated as a
    single leaf with type ``"json"``.

    Parameters
    ----------
    model:
        Pydantic model class to walk.
    col_prefix:
        Accumulates the flattened column name while recursing into nested
        models (e.g. ``"source_ow"``).
    source_prefix:
        Accumulates the dot-separated model path while recursing
        (e.g. ``"source.ow"``), used for traceability back to the model.

    Yields
    ------
    col_name : str
        Flattened column name (e.g. ``source_ow_geo_name``).
    source_path : str
        Dot-separated original model path (e.g. ``source.ow.geo_name``).
    field_info : FieldInfo
        Pydantic field metadata (description, default, etc.).
    inner_type : type
        The unwrapped scalar type of the field.
    nullable : bool
        Whether the field's own annotation is Optional.
    """
    for field_name, field_info in model.model_fields.items():
        col_name = f"{col_prefix}_{field_name}" if col_prefix else field_name
        src_path = f"{source_prefix}.{field_name}" if source_prefix else field_name

        nullable, inner_type = _unwrap_optional(field_info.annotation)

        if isinstance(inner_type, type) and issubclass(inner_type, BaseModel):
            yield from _walk_model_fields(inner_type, col_prefix=col_name, source_prefix=src_path)
        else:
            yield col_name, src_path, field_info, inner_type, nullable


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def flatten_columns(model: type[BaseModel]) -> list[ColumnSpec]:
    """Generate a list of ``ColumnSpec`` from a Pydantic model class.

    Nested ``BaseModel`` fields are expanded with underscore-separated
    prefixes (e.g. ``source.ow.geo_name`` → column ``source_ow_geo_name``).
    Each column's nullability comes from its own type annotation.
    """
    return [
        ColumnSpec(
            name=col_name,
            type=_map_scalar_type(inner_type),
            nullable=nullable,
            description=field_info.description or "",
            source_field=src_path,
        )
        for col_name, src_path, field_info, inner_type, nullable in _walk_model_fields(model)
    ]


def flatten_record(instance: BaseModel) -> dict[str, object]:
    """Flatten a Pydantic model instance into a record dict matching the output of ``flatten_columns``.
    This is the record that would be inserted into the table defined by the corresponding ``TableSpec``.

    Values are serialized in JSON mode so that datetimes, enums, etc. are
    returned as JSON-compatible primitives.
    """
    nested = instance.model_dump(mode="json")
    result: dict[str, object] = {}
    for col_name, src_path, *_ in _walk_model_fields(type(instance)):
        parts = src_path.split(".")
        value: object = nested
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = None
                break
        result[col_name] = value
    return result


def model_to_tablespec(
    model_table: ModelTableDef,
    version: str = "0.1.0",
) -> TableSpec:
    """Generate a ``TableSpec`` by flattening a ``ModelTableDef`` model.

    Parameters
    ----------
    model_table:
        Declarative model-table definition containing model, table name, and keys.
    version:
        Design-time schema version (light semver recommended).
    """
    columns = flatten_columns(model_table.model)
    model_attributes = {column.name for column in columns}
    key_columns = [
        *model_table.primary_key,
        *model_table.natural_key,
        *(column for foreign_key in model_table.foreign_keys for column in foreign_key.columns),
    ]
    missing_columns = sorted({column for column in key_columns if column not in model_attributes})
    if missing_columns and len(missing_columns) > 0:
        raise ValueError(f"Key columns not defined in model: {missing_columns}")

    return TableSpec(
        name=model_table.name,
        description=model_table.model.__doc__ or "",
        model=model_table.model.__name__,
        columns=columns,
        primary_key=model_table.primary_key,
        natural_key=model_table.natural_key,
        foreign_keys=model_table.foreign_keys,
        version=version,
    )


def tablespec_to_json(spec: TableSpec) -> str:
    return spec.model_dump_json(indent=2, exclude={"columns": {"__all__": {"source_field"}}})

