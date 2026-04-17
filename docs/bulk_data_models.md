## Gridded interpretations

In this repo we call gridded interpretations those which are represented relatively by:
- a set of parameters describing the grid  position (which will determin x,y values for each of its points)
- an array (2D or flattened to 1D) cotaining the values for each of these points following a specific order

In this scenario, for the arrays, it is important that all the values are represented, including NaNs, as the ordering will determine their position in the grid

For gridded interpretations, the arrays should follow the RegularSurface described in
https://xtgeo.readthedocs.io/en/latest/datamodels.html#description:

> A 2D array (masked numpy) of values, for a total of ncol * nrow entries. Undefined map nodes are masked.
> The 2D numpy array is stored in C-order (row-major). Default is 64 bit Float.

All of the parameters necessary to describe the surface in that model are stored in the Geometry class, composed into GriddedInterpretationRecord as an attribute.
(rotation, origin, increments, ncol and nrow)
In addition, left-handedness in the Geometry is a boolean that describes the relative orientation of the axis, equivalent to yflip in xtgeo.
For surface grids, this is not relevant due to the rows always being oriented clockwise from the cols.
For horizons, this plays a role, as with the extra alignment of inlines and crosslines, this relative orientation may be reversed.

### Array row orientation

Assume a 2D array with 3 cols and 4 rows for a gridded representation looks like this
(remember a numpy 2D array is a list of columns, each with a list of row values for that column):
```
[[00, 01, 02, 03], [10, 11, 12, 13], [20, 21, 22, 23]]
```

If oriented along the cols and rows as defined in a RegularSurface, with the origin at the bottom left of the local grid:
cols will count from left to right, and inside them, rows count from bottom to top.
This can be thought of as following the same representation of a cartesian grid.

```
03   13   23
02   12   22
01   11   21
00   10   20
```

#### A note on SurfaceGrids order in OW

In OpenWorks, the SurfaceGrid is represented in a LGCStructure, which has a different orientation referencing the local grid:
The columns also count to the left, but the rows count from top to bottom instead.
It can be thought of as following the same representation of a matrix or spreadsheet.
If the same 2D array above was the representation of an LGCStructure, the local grid would look like this:

```
00  10   20
01  11   21
02  12   22
03  13   23
```

This is why the parameter "cartesian_origin" is set to true when converting from OW to interpretation model.
The method and parameter are defined in
https://github.com/equinor/dsis-schemas/blob/d235aa983b4e0e945f4ff54e80e8537b787d8be5/dsis_model_sdk/utils/protobuf_decoders.py#L340

Notice this does NOT affect the grid geometry and origin —
the parameters representing the rotation origin still refer to the bottom left corner of the grid.
This affects ONLY the order in which the arrays are stored.

### IL/XL orientation on horizons (the "yflip" issue)

TODO: document this

### Representing grids as point sets

It is also possible to represent grids as a list of vectors (x, y, z points) for each of its non-null cells.
This is a good representation for objects that are sparsely interpreted over th grid, generating many null values, as only the non-null values get to be represented.
In RESQML, the HorizonIntepretation can be represented as a 2DGrid or a PointSet, so both representations are valid.
OpenWorks offers an option in Horizons, where the protobuf can be stored in "sample" mode (point set) or "full" mode (grid), ut not for SurfaceGrids.
In this repo, we will consider that all SurfaceGrids and Horizons are stored as regular grids (GriddedInterpretation).
When converting to RESQML we will also use the Grid2D representation for all SurfaceGrids and Horizons.

## Vector based Interpretations

In this repo we call Vector-based interpretations those which are represented by a list of points (x, y, z).
Each point can additionally contain one or more properties, being represented as (x, y, z, v1, v2, ..., vn).
For the context of interpretations, we will use such representations for polygons, point sets and fault planes.
As described above, it is possible converting a gridded representation to a vector-based one, but in this repo we are not using such representation.

### Format

Vectors can be represented in two ways:
- an array of points - each element of the main array consists of a 3D point (x, y, z)
- columnar format - a 2D array, where each of the elemens is a list of x, y, and z

In either case, the idea can be extended to the field with attributes, either an array of nD points or a 2D array with n lists.
The sources (OpenWorks and Petrel) differ on that. For this repo, we choose to follow the semantcis closest to OSDU.

TODO: choose and document this
