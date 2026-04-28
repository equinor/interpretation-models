"""Declarative definitions of all table schemas.

This is the single place to define:
- Model-backed tables: model, table name, description, primary key, foreign keys (``MODEL_TABLES``)
- Manually defined support tables that don't map 1:1 to a model (``SUPPORT_TABLES``)

Primary keys and foreign keys are relational concerns and are therefore defined here,
not on the Pydantic model objects themselves.
"""

from models.interpretation import SurfaceGridRecord
from models.collection import Collection, CollectionItem
from tables.tablespec import ModelTableDef, TableSpec, ColumnSpec, ForeignKeySpec

# ---------------------------------------------------------------------------
# Model tables
# ---------------------------------------------------------------------------

SURFACE_GRID_TABLE = ModelTableDef(
    model=SurfaceGridRecord,
    name="SurfaceGrid",
    primary_key=["id"],
    natural_key=["source_system", "source_database", "source_project", "source_id"],
)

COLLECTION_TABLE = ModelTableDef(
    model=Collection,
    name="Collection",
    primary_key=["id"],
    natural_key=["source_system", "source_database", "source_project", "source_id"],
)

COLLECTION_ITEM_TABLE = ModelTableDef(
    model=CollectionItem,
    name="CollectionItem",
    primary_key=["source_system", "source_database", "source_project", "collection_id", "object_id"],
    natural_key=["source_system", "source_database", "source_project", "collection_id", "object_id"],
    foreign_keys=[
        ForeignKeySpec(
            columns=["collection_id"],
            references_table="Collection",
            references_columns=["id"],
        )
    ],
)

MODEL_TABLES: list[ModelTableDef] = [
    SURFACE_GRID_TABLE,
    COLLECTION_TABLE,
    COLLECTION_ITEM_TABLE,
]

# ---------------------------------------------------------------------------
# Support tables (manually defined)
# ---------------------------------------------------------------------------

SUPPORT_TABLES: list[TableSpec] = []
