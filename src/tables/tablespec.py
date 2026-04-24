from pydantic import BaseModel
from typing import Any


class ColumnSpec(BaseModel):
    """Specification for a single table column."""

    name: str
    type: str
    nullable: bool
    description: str = ""
    source_field: str | None = None


class ForeignKeySpec(BaseModel):
    """A foreign key relationship to another table."""

    columns: list[str]
    references_table: str
    references_columns: list[str]


class TableSpec(BaseModel):
    """Minimal abstraction for an intended table definition.

    Captures name, columns, keys, version, and an optional link back
    to the Pydantic model it was generated from.
    """

    name: str
    description: str = ""
    model: str | None = None
    columns: list[ColumnSpec]
    primary_key: list[str] = []
    natural_key: list[str] = []
    foreign_keys: list[ForeignKeySpec] = []
    version: str = "0.1.0"


class ModelTableDef(BaseModel):
    """Input definition for generating a model-backed TableSpec."""

    model: Any  # type[BaseModel] — Any to avoid generic issues
    name: str
    primary_key: list[str] = []
    natural_key: list[str] = []
    foreign_keys: list[ForeignKeySpec] = []
