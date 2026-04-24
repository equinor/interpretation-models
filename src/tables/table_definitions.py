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
    primary_key=["collection_id", "object_id"],
    natural_key=["collection_id", "object_id"],
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

COLLECTION_ACTIVITY_TABLE = TableSpec(
    name="CollectionActivity",
    description="""
    Activity log tracking changes to collections and their contained objects.
    Each row represents a single event either directly to a collection (insert or remove obbjects) 
    or to one of its objects (create, update, delete)
    Used for aggregation queries, for example:
    - determine when a collection was last updated (potentialy filtering only on a specific datatype of interest)
    - which collections had updates on surface grids in the last hour
    """,
    columns=[
        ColumnSpec(name="date", type="datetime", nullable=False, description="Timestamp of the activity event"),
        ColumnSpec(name="update_type", type="string", nullable=False, description="Type of update (e.g. ObjectCreate, ObjectUpdate, ObjectDelete, ISetInsert, ISetDelete)"),
        ColumnSpec(name="datatype", type="string", nullable=False, description="Type of the affected data object (e.g. SurfaceGrid)"),
        ColumnSpec(name="source_system", type="string", nullable=False, description="Source system identifier"),
        ColumnSpec(name="source_database", type="string", nullable=False, description="Source database identifier"),
        ColumnSpec(name="source_project", type="string", nullable=False, description="Source project identifier"),
        ColumnSpec(name="iset_id", type="string", nullable=False, description="Interpretation set identifier"),
        ColumnSpec(name="object_id", type="string", nullable=True, description="Identifier of the affected object within the ISet (null for ISet-level events)"),
    ],
    primary_key=["date", "update_type", "iset_id", "object_id"],
    natural_key=["date", "update_type", "iset_id", "object_id"],
    foreign_keys=[
        ForeignKeySpec(
            columns=["iset_id"],
            references_table="Collection",
            references_columns=["id"],
        ),
    ],
)

SURFACEGRID_COLLECTIONITEM_TABLE = TableSpec(
    name="SurfaceGrid_CollectionItem",
    description="""
    Bridge table for the many-to-many relationship between SurfaceGrid and CollectionItem.
    CollectionItem itself references objects of different types (SurfaceGrid, Horizon, Fault, ...)
    so a direct foreign key from CollectionItem to each type table is not possible.
    This bridge table provides a proper FK-backed link for SurfaceGrid specifically.
    """,
    columns=[
        ColumnSpec(name="collection_item_id", type="string", nullable=False, description="References the object_id in CollectionItem"),
        ColumnSpec(name="surface_grid_id", type="string", nullable=False, description="References the id in SurfaceGrid"),
    ],
    primary_key=["collection_item_id", "surface_grid_id"],
    foreign_keys=[
        ForeignKeySpec(
            columns=["collection_item_id"],
            references_table="CollectionItem",
            references_columns=["object_id"],
        ),
        ForeignKeySpec(
            columns=["surface_grid_id"],
            references_table="SurfaceGrid",
            references_columns=["id"],
        ),
    ],
)

SUPPORT_TABLES: list[TableSpec] = [
    COLLECTION_ACTIVITY_TABLE,
    SURFACEGRID_COLLECTIONITEM_TABLE,
]
