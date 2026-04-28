"""Declarative definitions of all table schemas.

This is the single place to define:
- Model-backed tables: model, table name, description, primary key, foreign keys (``MODEL_TABLES``)
- Manually defined support tables that don't map 1:1 to a model (``SUPPORT_TABLES``)

Primary keys and foreign keys are relational concerns and are therefore defined here,
not on the Pydantic model objects themselves.
"""

from models.interpretation import SurfaceGridRecord
from tables.tablespec import ModelTableDef, TableSpec

# ---------------------------------------------------------------------------
# Model tables
# ---------------------------------------------------------------------------

SURFACE_GRID_TABLE = ModelTableDef(
    model=SurfaceGridRecord,
    name="SurfaceGrid",
    primary_key=["id"],
    natural_key=["source_system", "source_database", "source_project", "source_id"],
)


MODEL_TABLES: list[ModelTableDef] = [
    SURFACE_GRID_TABLE,
]

# ---------------------------------------------------------------------------
# Support tables (manually defined)
# ---------------------------------------------------------------------------

SUPPORT_TABLES: list[TableSpec] = []
