"""Registry of all intended table schemas.

Run this script to regenerate the serialized schemas under /schemas:

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
from tables.table_definitions import MODEL_TABLES, SUPPORT_TABLES


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
    output_dir: str | Path = "schemas",
) -> Path:
    """Write each ``TableSpec`` as a pretty-printed JSON file under *output_dir*.

    Returns the resolved output directory.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for spec in specs:
        file_path = output_path / f"{spec.name}.json"
        json_model = tablespec_to_json(spec)
        file_path.write_text(
            data=json_model + "\n",
            encoding="utf-8",
        )

    return output_path


def build_all_specs() -> list[TableSpec]:
    return generate_table_schemas(MODEL_TABLES, support_tables=SUPPORT_TABLES)


def main() -> None:
    specs = build_all_specs()
    output_dir = Path(__file__).resolve().parents[2] / "schemas"
    serialize_table_schemas(specs, output_dir=output_dir)
    print(f"Wrote {len(specs)} schema(s) to {output_dir}")


if __name__ == "__main__":
    main()
