## Gridded interpretations

For gridded interpretations, the arrays should follow the RegularSurface described in 
https://xtgeo.readthedocs.io/en/latest/datamodels.html#description: 

> A 2D array (masked numpy) of values, for a total of ncol * nrow entries. Undefined map nodes are masked. 
> The 2D numpy array is stored in C-order (row-major). Default is 64 bit Float.

All of the parameters necessary to describe the surface in that model (rotation, origin x and y, increments, ncol and nrow)
are stored in the Geometry class, which is composed into GriddedInterpretationRecord as anattribute.
In addition, left-handedness is a boolean that describes the relative orientation of the axis, equivalent to yflip in xtgeo.
For surface grids, this is not relevant due to the rows always being oriented clockwise from the cols. For horizons, this
plays a role, as with the extra alignment of inlines and crosslines, this relative orientation may be reversed.

### Array row orientation

Assume a 2D array with 3 cols and 4 rows for a gridded representation looks like this (remember a np 2d aray is a list of
columns, each with a list of row values for that column):
```
[[00, 01, 02, 03], [10, 11, 12, 13], [20, 21, 22, 23]]
``` 

If oriented along the cols and rows as defined in a RegularSurface, with the origin at the bottom left of the local grid,
the cols will count from left to right, and inside them, rows count from bottom to top.
This can be thought of as following the same representation of a cartesian grid.

```
03   13   23
02   12   22
01   11   21
00   10   20
```

#### A note on SurfaceGrids order in OW

In OpenWorks, the SurfaceGrid is represented in a LGCStructure, which has a different orientation, where 
the columns also count to the left, but the rows count from top to bottom instead.
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

Notice this does NOT affect the grid geometry and origin - the parameters representing the rotation origin still refer
to the bottom left corner of the grid. This affects ONLY the order in which the arrays are stored. 

#### IL/XL orientation on horizons (the "yflip" issue)
