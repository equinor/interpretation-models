"""Declarative definitions of all table schemas.

This is the single place to define:
- Model-backed tables: model, table name, description, primary key, foreign keys (``MODEL_TABLES``)
- Manually defined support tables that don't map 1:1 to a model (``SUPPORT_TABLES``)

Primary keys and foreign keys are relational concerns and are therefore defined here,
not on the Pydantic model objects themselves.
"""

from models.interpretation import SurfaceGridRecord
from models.collection import Collection, CollectionItem
from schemas.registry import SchemaName
from tables.tablespec import ModelTableDef, TableSpec, ColumnSpec, ForeignKeySpec

# Increment this value (int) when any table definition changes to generate a new versioned schema set.
# All tables will be part of the new version - individual tables don't have separate version numbers.
SCHEMA_VERSION = 1

# ---------------------------------------------------------------------------
# Model tables
# ---------------------------------------------------------------------------

SURFACE_GRID_TABLE = ModelTableDef(
    model=SurfaceGridRecord,
    name=SchemaName.SURFACE_GRID,
    primary_key=["id"],
    natural_key=["source_system", "source_database", "source_project", "source_id"],
)

COLLECTION_TABLE = ModelTableDef(
    model=Collection,
    name=SchemaName.COLLECTION,
    primary_key=["id"],
    natural_key=["source_system", "source_database", "source_project", "source_id"],
)

COLLECTION_ITEM_TABLE = ModelTableDef(
    model=CollectionItem,
    name=SchemaName.COLLECTION_ITEM,
    primary_key=["id"],
    natural_key=["collection_id", "object_id", "datatype"],
    foreign_keys=[
        ForeignKeySpec(
            columns=["collection_id"],
            references_table=SchemaName.COLLECTION,
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

COLLECTION_ITEM_ACTIVITY_TABLE = TableSpec(
    name=SchemaName.COLLECTION_ITEM_ACTIVITY,
    description="""
    Activity log tracking changes to collections and their contained objects.
    Each row represents a single event either directly to a collection (insert or remove objects)
    or to one of its objects (create, update, delete)
    Used for aggregation queries, for example:
    - determine when a collection was last updated (potentialy filtering only on a specific datatype of interest)
    - which collections had updates on surface grids in the last hour
    """,
    columns=[
        ColumnSpec(name="event_date", type="datetime", nullable=False, description="Timestamp of the activity event"),
        ColumnSpec(name="event_type", type="string", nullable=False, description="Type of update. Possible values: ObjectUpdate, CollectionInsert, CollectionRemove"),
        ColumnSpec(name="collection_item_id", type="string", nullable=True, description="Identifier of the affected collection item (combination of collection_id, object_id, and datatype)"),
    ],
    primary_key=["event_date", "event_type", "collection_item_id"],
    natural_key=["event_date", "event_type", "collection_item_id"],
    foreign_keys=[
        ForeignKeySpec(
            columns=["collection_item_id"],
            references_table=SchemaName.COLLECTION_ITEM,
            references_columns=["id"],
        ),
    ],
)

SUPPORT_TABLES: list[TableSpec] = [
    COLLECTION_ITEM_ACTIVITY_TABLE,
]
