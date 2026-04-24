# Design Guidelines: Tables

This document describes how table schemas should be defined and maintained in the interpretation-models repository.

## Purpose and scope

The purpose of the tables package is to act as a **reference contract** for the tabular representation of the internal interpretation model.

The internal interpretation model already defines the semantic contract for interpretation data in the form of Pydantic models.
The tables package extends that contract into a tabular form.

This allows table documentation to be defined where domain knowledge already exists, rather than being recreated ad hoc wherever tables happen to be materialized.

It exists so that:

- there is a stable, well-described contract for interpretation metadata in tabular form
- table and column meanings and their descriptions are documented and can be further passed to downstream consumers
- the intended table schemas and conceptual model is visible and reviewable in Git
- schema evolution and versioning is easy to inspect in pull requests
- applications and pipelines can import the intended schema definitions and descriptions when creating or updating physical tables


### Separation of Concerns

This repository is authoritative for meaning and semantics. It is responsible for defining what each table and column represents, and how they are shaped.

This repository is not authoritative for deployment or migrations.
Schema migrations, release processes, and syncing of tables at runtime is the responsibility of processing clients such as pipelines.

This separation is intentional.

## Table categories

Tables in the internal tabular model fall into two categories.

### Model tables

Model tables are the authoritative tabular representation of internal semantic records.

Examples: SurfaceGrids, Horizons, Faults, Collections, CollectionItems

These tables are generated from Pydantic record classes using flattening rules

### Support tables

Support tables are non-authoritative helper tables created for usability or simplified querying. 
They are convenience structures and the model should be fully contained in the model tables without them.

These tables do not correspond 1:1 to a semantic record and should therefore be defined explicitly rather than generated automatically from a Pydantic model.

For the description and reasoning behind each support table, check [support tables](support_tables.md).

## TableSpec

TableSpec is the minimal abstraction used to define intended tables.
Its purpose is to:

- make table design explicit in code
- allow schema generation for model-backed model tables
- carry descriptions/comments

A TableSpec should capture at least:

- name
- description/comment
- model: If the table is based on a model record, empty if it is a support table
- columns: The intended columns of the table.
- keys: The intended identity or uniqueness rules and relationship FKs
- version: design-time schema version.

For each column, the table spec should also capture:

- name
- intended type
- nullability
- description/comment
- original semantic source field (for model-backed columns)

This is enough to make the table definitions useful without turning the package into a full schema framework.

### TableSpec generation

For model tables, schemas should be generated from the Pydantic record models rather than written by hand.
The generation process should:

- flatten nested model fields deterministically
- preserve descriptions from model fields
- allow explicit table naming

This keeps the semantic model as the source of truth for record-like tables while still allowing the physical table name and a few physical details to be explicit.

Support tables TableSpecs are defined manually in [src/tables/table_definitions.py](../../src/tables/table_definitions.py)
Primary keys and foreign keys for model tables are also defined explicitly in the same file, together with custom table names and descriptions.
The concepts of PK and FK are exclusive to the relational model, not being defined by Pydantic model objects.

#### Registry and schema generation


To generate or regenerate all table schemas:

1. If adding tables or updating PKs/FKs, edit `MODEL_TABLES` in `generate_schemas.py` to define which models to serialize and their keys.
2. If there are new anually generated helper tables, edit `SUPPORT_TABLES` to add them
3. Run: `python -m tables.generate_schemas`

A serialised snapshot of the generated table specs is stored under `/schemas` in the root of the repository, with one JSON file per table.

## Schema versioning and evolution

Each TableSpec should carry a version, and changes to table definitions should be visible in Git as normal code changes.
This supports:

- review of schema changes in pull requests
- traceability of table and column evolution
- clear communication between domain/model designers and implementation teams

Whenever a new change to the model is introduced that causes a schema change, the committer is expected to bump the versions of affected tables.

All changes are required to bump the version. We recommend (but do not enforce) a light semver:

Patch version (x.y.z -> x.y.z+1) for non-structural updates.
Examples: comment corrections, description updates, column reordering

Minor version (x.y.z -> x.y+1.0) for backward-compatible structural updates
Examples: adding optional columns, adding new support tables, 

Major version (x.y.z -> x+1.0.0) for breaking changes
Examples: removing columns, renaming columns, changing types, updating keys

We recommend versions are also bumped to indicate changes in mapping only, even if the schema does not change.

### CI enforcement

We intend to have a CI action (not implemented yet) to verify that the schemas are changed when a change happens.

The CI action should regenerate the schema snapshots using the same function and compare the output  to the committed version.
If the generated output differs from the committed files, the PR fails.
It should also check that if the schema content changed, the version must also have changed
The comparison should ignore the version field itself and compare the rest of the serialised schema.

CI should not verify semver meaning - any schema bump is enough.
The decision of how to version remains with the author of the change.

## How applications and pipelines should use this

1. Schema creation and updates

When creating or updating physical tables, implementations should import the relevant TableSpecs rather than inferring schemas from records ad hoc.
Relying on implicit schema creation makes the physical schema hard to review or document and vulnerable to accidental drift.
Developers should inspect changes in the /schemas folder and use them as the reference for updating physical table definitions and migrations.
The diff of that folder serves as a history of versions.

2. Export comments and documentation

Implementations should export table and column descriptions from the TableSpecs into the physical tables wherever supported.

3. Migrations

Systems that materialize the physical tables should implement actual physical migrations reflecting the diffs in the schemas.
A migration tool such as Flyway is a reasonable choice for that operational layer, but it should be used outside this repository.
