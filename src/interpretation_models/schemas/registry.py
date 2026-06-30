"""Read-only access to versioned table schemas for pipeline consumers."""

import importlib.resources
import importlib.resources.abc
import json
import re
from enum import StrEnum
from typing import Self


class SchemaName(StrEnum):
    """Known table schema names."""

    SURFACE_GRID = "surface_grid"
    COLLECTION = "collection"
    COLLECTION_ITEM = "collection_item"
    COLLECTION_ACTIVITY = "collection_activity"


class SchemaRegistry:
    """Provides access to versioned PySpark-compatible table schemas.

    Schemas are discovered from the ``schemas/definitions/`` package directory.
    Versions are stored as subfolders: ``v{version}/{name}.json``.
    """

    _instance: Self | None = None
    _definitions_path: importlib.resources.abc.Traversable

    def __new__(cls) -> Self:
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._definitions_path = importlib.resources.files("interpretation_models.schemas") / "definitions"
            cls._instance = instance
            
        return cls._instance

    def versions(self) -> list[int]:
        """Return all available schema versions, sorted ascending."""
        found: set[int] = set()

        for item in self._definitions_path.iterdir():
            match = re.match(r"^v(\d+)$", item.name)

            if match:
                found.add(int(match.group(1)))

        return sorted(found)

    def latest_version(self) -> int:
        """Return the latest (highest) schema version."""
        all_versions = self.versions()

        if not all_versions:
            raise FileNotFoundError("No schema files found.")
        
        return all_versions[-1]

    def get_schema(self, name: SchemaName, version: int | None = None) -> dict:
        """Return a single schema as a dict (ready for ``StructType.fromJson()``).

        Parameters
        ----------
        name:
            The table schema to retrieve.
        version:
            Schema version. Defaults to the latest.
        """
        if version is None:
            version = self.latest_version()

        ref = self._definitions_path / f"v{version}" / f"{name.value}.json"

        try:
            content = ref.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Schema not found: v{version}/{name.value}.json. "
                f"Available versions: {self.versions()}"
            )
        
        return json.loads(content)

    def get_all_schemas(self, version: int | None = None) -> dict[SchemaName, dict]:
        """Return all table schemas for a given version.

        Parameters
        ----------
        version:
            Schema version. Defaults to the latest.
        """
        if version is None:
            version = self.latest_version()

        return {name: self.get_schema(name, version=version) for name in SchemaName}
