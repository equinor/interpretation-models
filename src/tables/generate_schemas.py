"""Registry of all intended table schemas.

Run this script to regenerate the serialized schemas under src/schemas/definitions:

    python -m tables.generate_schemas

Edit ``MODEL_TABLES`` and ``SUPPORT_TABLES`` in ``tables/table_definitions.py`` to change
which models are serialized or to add manually-defined support tables.
"""

from pathlib import Path

from tables import (
    ModelTableDef,
    TableSpec,
    model_to_tablespec,
    tablespec_to_json,
)
from tables.table_definitions import MODEL_TABLES, SCHEMA_VERSION, SUPPORT_TABLES


def generate_table_schemas(
    models: list[ModelTableDef],
    support_tables: list[TableSpec] | None = None,
) -> list[TableSpec]:
    """Build ``TableSpec`` list from model table definitions and optional support tables.

    Parameters
    ----------
    models:
        Each entry is a ``ModelTableDef`` describing the model, table name, and keys.
    support_tables:
        Manually defined support tables (not backed by a model).
    """
    specs: list[TableSpec] = [
        model_to_tablespec(defn)
        for defn in models
    ]
    if support_tables:
        specs.extend(support_tables)
    return specs


def serialize_table_schemas(
    specs: list[TableSpec],
    version: int,
    output_dir: str | Path = "schemas",
    overwrite: bool = False,
) -> Path:
    """Write each ``TableSpec`` as a JSON file under *output_dir*/v{version}/.

    Schemas are organized into version subfolders: ``v{version}/{name}.json``.
    Raises FileExistsError if a file already exists unless *overwrite* is True.

    Returns the resolved output directory.
    """
    output_path = Path(output_dir)
    version_dir = output_path / f"v{version}"
    version_dir.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        file_path = version_dir / f"{spec.name}.json"

        if file_path.exists() and not overwrite:
            raise FileExistsError(
                f"Schema files already exist for version {version} in {output_path}. "
                f"Re-run with --overwrite to regenerate."
            )
        
        json_model = tablespec_to_json(spec)
        file_path.write_text(
            data=json_model + "\n",
            encoding="utf-8",
        )

    return output_path


def build_all_specs() -> list[TableSpec]:
    return generate_table_schemas(MODEL_TABLES, support_tables=SUPPORT_TABLES)


def main() -> None:
    import sys

    specs = build_all_specs()
    overwrite = "--overwrite" in sys.argv
    output_dir = Path(__file__).resolve().parents[1] / "schemas" / "definitions"

    try:
        serialize_table_schemas(specs, version=SCHEMA_VERSION, output_dir=output_dir, overwrite=overwrite)
        print(f"Wrote {len(specs)} json file(s) to {output_dir} for schema version {SCHEMA_VERSION}.")
    except FileExistsError as e:
        print(f"{e}")


if __name__ == "__main__":
    main()
