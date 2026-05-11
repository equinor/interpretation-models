from pathlib import Path
from unittest.mock import patch

import pytest

from schemas.registry import SchemaName, SchemaRegistry


@pytest.fixture
def registry() -> SchemaRegistry:
    return SchemaRegistry()


class TestVersions:
    def test_returns_available_versions(self, registry: SchemaRegistry):
        versions = registry.versions()
        assert 1 in versions

    def test_versions_sorted_ascending(self, registry: SchemaRegistry):
        versions = registry.versions()
        assert versions == sorted(versions)


class TestLatestVersion:
    def test_returns_latest(self, registry: SchemaRegistry):
        latest = registry.latest_version()
        assert latest == registry.versions()[-1]

    def test_raises_when_no_schemas(self, tmp_path: Path):
        registry = SchemaRegistry()
        with patch.object(registry, "_definitions_path", tmp_path):
            with pytest.raises(FileNotFoundError):
                registry.latest_version()


class TestGetSchema:
    def test_returns_dict_with_fields(self, registry: SchemaRegistry):
        schema = registry.get_schema(SchemaName.SURFACE_GRID)
        assert schema["type"] == "struct"
        assert isinstance(schema["fields"], list)

    def test_explicit_version(self, registry: SchemaRegistry):
        schema = registry.get_schema(SchemaName.COLLECTION, version=1)
        assert schema["type"] == "struct"

    def test_raises_for_missing_version(self, registry: SchemaRegistry):
        with pytest.raises(FileNotFoundError):
            registry.get_schema(SchemaName.SURFACE_GRID, version=999)


class TestGetAllSchemas:
    def test_returns_all_schema_names(self, registry: SchemaRegistry):
        schemas = registry.get_all_schemas()
        assert set(schemas.keys()) == set(SchemaName)

    def test_all_schemas_are_struct_type(self, registry: SchemaRegistry):
        schemas = registry.get_all_schemas()
        for name, schema in schemas.items():
            assert schema["type"] == "struct", f"{name} is not a struct"
