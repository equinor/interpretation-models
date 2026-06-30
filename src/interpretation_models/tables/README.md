# How to create or update a new schema

## Overview

Changes to the datamodels will not be reflected in the database schema automatically. A manual execution of the generate_schemas.py class is necessary. This will, in turn create a set of Spark readable json files that the pipeline will use to update the delta tables in the data lake used for user accessible data.

## Create or update schema

When a database changes has been performed and a new schema update is necessary then running one of the following commands from the project root folder will create or update the Spark readable json schema files stored in the */schemas* folder. Once completed the resulting schema json files must be checked in to version control and deployed within a new version of this library.

### Schema generator

The variable `SCHEMA_VERSION` in the source file `schema_versioning.py` will determine the schema version in use.

#### Create a new schema

Create a new schema using a new version determined by the SCHEMA_VERSION variable

```python
> python -m interpretation_models.tables.generate_schemas
```

#### Update the current schema

Update the current schema using the existing version number

```python
> python -m interpretation_models.tables.generate_schemas --overwrite
```
