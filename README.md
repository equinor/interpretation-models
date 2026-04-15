# Interpretation models

## Purpose

The interpretation-models repository provides a shared and executable semantic model for subsurface interpretation data and
collections of interpretations. Its primary goal is to make it possible to exchange data from different source systems by
mapping and bridging their different formats and data models. The intention is to:

- Provide a neutral internal model with stable contracts and interface
- Provide explicit mappings between objects of different source system models and the internal model
- Provide table schemas for data storage based on the internal model
- Provide functions for structured validation and basic automated QC of data
- Preserve meaning and semantics while formats, schemas, and standards evolve

## Scope

All interpretation objects handled in this repo are expected to have a model with dict-style metadata (tabular) and
an array containing data points (values). An introduction to interpretations, the contents of these arrays,
and the different data types can be found [in this interpretations primer doc](./docs/interpretations.md).


### Data types

Interpretation objects expected to be supported:
- surface grids
- horizons
- faults
- polygons
- point sets


### Source systems

Source systems expected to be supported:
- OpenWorks (as exposed by DSIS, supporting users of DSG application in the Landmark ecossystem)
- Petrel Studio
- OSDU (Core metadata and Reservoir DDMS / RESQML / RDDMS)

### Collections

The models described here also assume grouping of interpretations into collections. The collections can map to different
representations in different systems, for example:
- OpenWorks InterpretationSet
- Petrel Studio business projects and folders
- OSDU PersistedCollection

This repository provides an internal representation of collections, explicit mappings from source system representations to it,
and consistently handling the relationships between collections and interpretation objects. This is crucial to many workflows
supported by the mapping, frequently to help users group and filter the data they wish to transfer from one system to another.

### Currently supported

Combinations of data type and source will be added here as they are progressively implemented in this repository. The current list of supported combinations is:

- Coming soon... :)


## Design

### Components

This repo is mostly separated into four major components based on the different objects:

#### Interpretation models (src/models)

Define the internal composable, hierarchical Python classes to describe interpretation metadata and structure.

Design rules in docs/models.md

#### Model mapping (src/mappers)

Provide deterministic mappers between source-system models and the internal interpretation model

Design rules in docs/mappers.md

#### Validation (src/validations)

Apply schema- and content-level validation and recording the results, without blocking data flow.

Design rules in docs/validation.md

#### Table schemas and relationships (src/tables)

This bridges the gap between pydantic models and the need to generate table schemas for representation
of the internal model in storage. It includes flattening rules for attribute names,
representing FKs, creating m:n relationship tables, especially for collections.
Design rules in docs/tables.md

### Data flow

At a high level, this repository is organised around models and mappings. Those components are put together to build 
data flows for each supported combination of system and datatype.
We encourage the reader to explore two of such suggested data flows [in this  data flows doc](./docs/dataflow.md) - one with a data lake
medallion architecture pipeline approach and another with a simple ETL directly from source to OSDU usinf the internal
model only as an in-memory bridge

## Considerations

###  The need for an internal model

Different systems represent interpretations differently. They expose different metadata, use different identifiers,
group interpretations using different concepts. Grid geometry, for example, can be represented in multiple different ways,
with parameters for rotation, with unit vectors, with corner points - all valid and different views of the same thing.

To map safely between them, we introduce an internal bridge model that captures the union of what we care about and
evolves independently of any single system, acting as a stable contract while mappings may change.
We do acknowledge that creating our own "canonical" model  leads effectively to yet another another standard

![Standards](https://imgs.xkcd.com/comics/standards.png)

However, we accept that with a disclaimer: OSDU is intended to be the long‑term canonical industry model. And the
motivation for creating this repo is to map the models to OSDU so all the interpretations can be stored there long term.
However, OSDU models are still evolving and currently do not cover everything we ingest from source systems or all the
metadata we need to identify an object from a source system and update it accordingly using data pipelines. Thus, mapping
directly between source systems and OSDU would be a difficult approach at this point in time. This internal model exists
as a bridge, not a replacement, allowing us to map safely while learning and iterating. It should be as close as possible
to the OSDU model, so that at some point it can be just replaced by it.

The internal interpretation model should be:

- authoritative only within this repository and storage based on its table schemas
- neutral with respect to source systems
- explicitly designed to be mapped to and from other models

### xtgeo compatibility

Many of the interpretation datatypes are also represented by [xtgeo](https://xtgeo.readthedocs.io/en/latest/index.html).
The aim is different, as xtgeo is mainly used for manipulation and transformations on the arrays of data points (such as
sampling, smoothing, etc) and their respecive bulk files, while this is aimed at mapping and validating the models.
Where applicable, we use xtgeo for transformations and aim to be compatible with it - it should be possible to generate,
for example, an xtgeo.RegularSurface from the internal model's SurfaceGrid representation, which can be then used for
plotting, validation and manual QC.

### Storage formats and processing tools

This repository is intentionally not tied to any specific storage or transfer technology, framework, or tools.
It is designed to be used anywhere interpretation data needs to be understood, transformed, validated, or exchanged.

That said, it is influenced by the design needs of data pipelines exchanging data between different source systems,
especially from legacy source systems into OSDU, so considerations regarding the data modelling and processing of this
type of workflow are front and center in the design, as is the case in the example of creating table schemas for intermediate storage.
