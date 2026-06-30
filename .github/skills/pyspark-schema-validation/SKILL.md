---
name: pyspark-schema-validation
description: "Generate and validate PySpark table schemas from Pydantic models. Use when: regenerating schemas, validating StructType JSON, testing schema changes, adding new model tables."
---

# PySpark Schema Generation & Validation

## When to Use

- After modifying Pydantic models in `src/interpretation_models/models/`
- After changing table definitions in `src/interpretation_models/tables/table_definitions.py`
- To validate that generated JSON schemas are valid PySpark StructType definitions
- When adding a new model-backed table

## Generate Schemas

Run from the project root:

```bash
python -m interpretation_models.tables.generate_schemas
```

This reads `MODEL_TABLES` and `SUPPORT_TABLES` from `src/interpretation_models/tables/table_definitions.py` and writes versioned JSON files to `src/interpretation_models/schemas/definitions/`.

## Validate with PySpark

PySpark is not a project dependency. To validate, use any Python environment with pyspark installed (e.g. a WSL venv, a Databricks notebook, or a CI job).

From the project root:

```python
import json
from pathlib import Path
from pyspark.sql.types import StructType

for f in sorted(Path("src/interpretation_models/schemas/definitions").glob("*.json")):
    data = json.loads(f.read_text())
    schema = StructType.fromJson(data)
    print(f"{f.name}: {len(schema.fields)} fields")
```

Or using the `SchemaRegistry`:

```python
from interpretation_models.schemas import SchemaRegistry, SchemaName
from pyspark.sql.types import StructType

registry = SchemaRegistry()
for name in SchemaName:
    schema = StructType.fromJson(registry.get(name))
    print(f"{name}: {len(schema.fields)} fields")
```

## Create Empty DataFrame (Full Validation)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").appName("schema-test").getOrCreate()

schema = StructType.fromJson(data)
df = spark.createDataFrame([], schema=schema)
df.printSchema()

spark.stop()
```

## Adding a New Table

1. Create or update the Pydantic model in `src/interpretation_models/models/`
2. Add a `ModelTableDef` entry in `src/interpretation_models/tables/table_definitions.py`
3. Append it to the `MODEL_TABLES` list
4. Regenerate and validate
