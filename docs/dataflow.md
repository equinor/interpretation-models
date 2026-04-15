
For example, a flow for SurfaceGrids from OpenWorks to OSDU going through an intermediate data lake could look like this:

```mermaid
graph TD
    B[OW ISets]
    C[OW Objects Metadata]
    D[OW Protobuf]

    E[Interpretation Model Collections]
    F[Interpretation Model Objects Metadata]
    G[Arrays - ordered compatible with xtgeo]
    H[Validation Results]

    I[Table Storage]
    J[Bulk Storage]

    K[Filtered Interpretation Model Collections]
    L[Filtered Interpretation Model Objects Metadata]
    M[Arrays]

    N[OSDU WKS]
    O[OSDU PersistedCollection]
    P[RESQML with hdf5 arrays]

    Q[RDDMS]
    R[OSDU core]

    B -->|Mapper| E
    C -->|Mapper| F
    D -->|Decode and Convert| G

    F -->|Table Schema| I
    E -->|Table Schema| I
    H -->|Table Schema| I

    %% Invisible edges only for alignment, no semantic meaning
    H ~~~ J
    E ~~~ H

    F -->|Validate| H
    G -->|Validate| H

    G -->|Store| J

    I -->|Filter| K
    I -->|Filter| L
    J -->|Fetch| M

    K -->|Mapper| O
    L -->|Mapper| N
    L -->|rddms-io| P
    M -->|rddms-io| P

    O -->|Ingest| R
    N -->|Ingest| R
    P -->|pyetp| Q
   ```


- extract from DSIS protobuf arrays, SurfaceGrids metadata, ISets and ISetDataObjects metadata, all of which follow a source model (stored in source-oriented repos such as [dsis-schemas](https://github.com/equinor/dsis-schemas/)
- potentially store the initial values in an intermediate storage (e.g. raw or bronze layer)
- use the mappers in this repo to convert DSIS SurfaceGrids into internal SurfaceGrids, DSIS ISets into internal Collections, DSIS ISetDataObjects into CollectionItems
- decode the protobuf and convert/clean the arrays using a library like [dsis-schemas](https://github.com/equinor/dsis-schemas/)
- apply validations defined in this repo to the objects and arrays, which return a ValidationResults object
- store those objects in tables using the table schemas in this repo for SurfaceGrids, Collections, CollectionItems, ValidationResults
- use externally defined rules to filter from the tables, for example, only grids that belong to pre-determined ISets/Collections, or only grids that passed a specific validation (for example, geo_name is filled)
- use a library like rddms-io (included in [pyetp](https://github.com/equinor/pyetp)) to convert the grids(including metadata + arrays) into RESQML
- use a library like [pyetp](https://github.com/equinor/pyetp) to ingest the Grid2D into OSDU/RDDMS
- use the mappers in this repo to convert the filtered grids metadata from the internal model to OSDU WKS and internal collections into OSDU PersistedCollections. The generated WKS object can optionally include links to existing reference data such as CRS, Strat Columns, Field, etc, but that will require the client fetching their ids and reference strings from OSDU and informing them as parameters to the mappers.
- ingest the WKS objects and PersistedCollections to OSDU using its REST API or python client. 

Note: Some logic is required in the last steps to use the ids of the created WKS objects in the PersistedCollections and create links between the objects created in RDDMS and core.  This is outside the scope of this repo and should be done by the client doing the processing

### Alternate data flow

This is compatible with a processing pipeline for example, the raw DSIS objects, ISets and protobufs could be intermediately stored in the bronze layer and the transformed interpretation model objects, collections, arrays and validation results in the silver or gold layer of a data lake organized in the medallion architecture.

But it is not be required to follow such processing. It should be flexible enough to allow other strategies - for example, the data can be extracted from the source (with filters alredy applied to queries), converted in-memory all the way to the target system model, and then validation/QC can be performed in the target. So the steps for intermediate storage and validation would be eliminated.

 ```mermaid
graph TD
    B[OW ISets]
    C[OW Objects Metadata]
    D[OW Protobuf]

    E[Interpretation Model Collections]
    F[Interpretation Model Objects Metadata]
    G[Arrays - ordered compatible with xtgeo]

    N[OSDU WKS]
    O[OSDU PersistedCollection]
    P[RESQML with hdf5 arrays]

    Q[RDDMS]
    R[OSDU core]

    B -->|Mapper| E
    C -->|Mapper| F
    D -->|Decode and Convert| G

    E -->|Mapper| O
    F -->|Mapper| N
    F -->|rddms-io| P
    G -->|rddms-io| P

    O -->|Ingest| R
    N -->|Ingest| R
    P -->|pyetp| Q

   ```