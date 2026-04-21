## Gridded interpretations

In this repo we call gridded interpretations those which are represented relatively by:
- a set of parameters describing the grid  position (which will determine x,y values for each of its points)
- an array (2D or flattened to 1D) containing the values for each of these points following a specific order

In this scenario, for the arrays, it is important that all the values are represented, including NaNs, as the ordering will determine their position in the grid

For gridded interpretations, the arrays should follow the RegularSurface described in
https://xtgeo.readthedocs.io/en/latest/datamodels.html#description:


All of the parameters necessary to describe the surface in that model are stored in the Geometry class, composed into GriddedInterpretationRecord as an attribute.

### Array values orientation

Values in grids can be represented by a 2D array, which are typically flattened into 1D for storage and transport purposes.

According to xtgeo docs:

> A 2D array (masked numpy) of values, for a total of ncol * nrow entries. Undefined map nodes are masked.
> The 2D numpy array is stored in C-order (row-major). Default is 64 bit Float.

The arrays referenced in this repo, as in OpenWorks and in xtgeo, all follow the C-order by default.
C-order, also called "row-major", just means that if the array has two axis and shape (i, j), the `j` values are stored sequentially for each `i`.
So the representaiton of the array would be:

[[x<sub>i0j0</sub>, ..., x<sub>i0jn</sub>], [x<sub>i1j0</sub>, ..., x<sub>i1jn</sub>], ... [x<sub>in j0</sub>, x<sub>in jn</sub>]]

This is why the locality principle says reading the array will perform better iterating over `i` as outer loop and `j` as inner loop.

Traditionally, in CS notation, especially in C-based languages, it is common to call the i axis as rows and j axis as cols. 
So if an array has shape (i, j), in the CS context typically it would mean it has shape (nrows, ncols).


However, for both xtgeo and OpenWorks, the representation of this 2D array is geometric.
In a local grid, the cols are vertical, and follow the i axis, while the rows are horizontal and follow the j axis.
This means the arrays manipulated in those software are represented as a list of columns, each of them containing a list of rows.
**So if an array has shape (i, j), in this context it means it has shape (ncols, nrows)**

Therefore, it may be useful to refer to the axis in the array as i and j positions, rather than cols and rows to avoid ambiguity.
i and j positions generalize both for the CS notation and the geometric notation, while cols and rows differ across those domains!

As an example, a 2D array with 3 cols and 4 rows for a gridded representation looks like this
```
[[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23]]
```
i.e. the shape of the array is (i, j) = (ncols, nrows) = (3,4)

If oriented along the cols and rows as defined in a RegularSurface, with the origin at the bottom left of the local grid:
cols will count from left to right (i axis), and inside them, rows count from bottom to top (j axis).
This can be thought of as following the same representation of a cartesian grid.
So this array would look like this in the local grid:

```
3   13   23
2   12   22
1   11   21
0   10   20
```

#### A note on SurfaceGrids order in OW

In OpenWorks, the SurfaceGrid is represented in a LGCStructure, which has a different orientation referencing the local grid:
The columns still count left to right, but the rows count from top to bottom instead.
It can be thought of as following the same order of a matrix or spreadsheet.
If the same 2D array above was the representation of an LGCStructure, the local grid would look like this:

```
0  10   20
1  11   21
2  12   22
3  13   23
```

Therefore, in order to read an object from OpenWorks and save it in xtgeo-compatible order, it is necessary to reverse the order of row values in each column.
The method to convert to np array in [dsis-schemas](
https://github.com/equinor/dsis-schemas/blob/d235aa983b4e0e945f4ff54e80e8537b787d8be5/dsis_model_sdk/utils/protobuf_decoders.py#L340)
uses the "cartesian_origin" flag to do that.

Notice this does NOT affect the grid geometry and origin.
The rotation origin still refers to the bottom left corner of the local grid in both cases.
This affects ONLY the order in which the arrays are stored.

### Rotation and local grids

In the section above, we reference i and j as the axis of the **local grid**.
In the local grid, `i` is always horizontal to the right and `j` is always vertical upwards (i.e. j is always 90 degrees counterclockwise from `i`).

The rotation parameter in the grid metadata describes how the local `i` and `j` axis relate to the global `x` and `y` axis of the coordinate system.
That rotation is always referenced by the origin of the grid (i.e., the bottom left corner). 
A good visual representation of this is found in the [xtgeo docs](https://xtgeo.readthedocs.io/en/latest/datamodels.html#description)

When applying rotation, it is important to keep in mind the spatial orientation changes in relation to the global coordinate system, but NEVER to the local grid.
For example, rotating a grid by 90 degrees means the i axis will now point North (y axis) and j axis will point West (-x axis).
However, from the local grid, i is still vertical (columns) and j is still horizontal (rows).

#### IL/XL orientation on horizons (the "yflip" issue)

In the Geometry class, left-handedness is a boolean that describes the relative orientation of the axis, equivalent to yflip in xtgeo.
For surface grids, this is not relevant due to the `j` axis always being oriented clockwise from the `i` axis as descried above.
For horizons, however, with the extra alignment of inlines and crosslines, this relative orientation may be reversed.

TODO: document this with example and images (currently in Miro board)

### Representing grids as point sets

It is also possible to represent grids as a list of vectors (x, y, z points) for each of its non-null cells.
This is a good representation for objects that are sparsely interpreted over the grid, generating many null values, as only the non-null values get to be represented.

In RESQML, the HorizonInterpretation can be represented as a 2DGrid or a PointSet, so both representations are valid.

OpenWorks offers an option in Horizons, where the protobuf can be stored in "sample" mode (point set) or "full" mode (grid), but not for SurfaceGrids.

In this repo, we will consider that all SurfaceGrids and Horizons are stored as regular grids (GriddedInterpretation).
When converting to RESQML we will also use the Grid2D representation for all SurfaceGrids and Horizons.

## Vector based Interpretations

In this repo we call Vector-based interpretations those which are represented by a list of points (x, y, z).
Each point can additionally contain one or more properties, being represented as (x, y, z, v1, v2, ..., vn).
As described above, it is possible converting a gridded representation to a vector-based one, but in this repo we are not using such representation.

### Format

Vectors can be represented in two ways:
- an array of points - each element of the main array consists of a 3D point (x, y, z)
- columnar format - a 2D array, where each of the elemens is a list of x, y, and z

In either case, the idea can be extended to the field with attributes, either an array of nD points or a 2D array with n lists.
The sources (OpenWorks and Petrel) differ on that. For this repo, we choose to follow the semantcis closest to OSDU.

TODO: choose and document this
