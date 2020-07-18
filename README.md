# Conway Operators in python

Updated to Blender 2.83

[Conway Polyhedra](https://en.wikipedia.org/wiki/Conway_polyhedron_notation) are formed by applying various operators to a seed polyhedron such as one of the platonic solids.

from [Wikipedia](https://en.wikipedia.org/wiki/Conway_polyhedron_notation)

![conway operators](/images/conway_examples.png)

This repo includes python code *conway.py* to implement a subset of these operators.

The code is designed to be used with [Blender](https://www.blender.org/) and [Sverchok](https://github.com/nortikin/sverchok/) scripted nodes but the only dependency is Blender's mathutils library. This means the code can be run outside Blender using a [standalone version of the mathutils module](https://github.com/majimboo/py-mathutils).

## Usage Notes

Using the *conway.py*  module in Blender with Sverchok's *Scripted Node Lite*.
*  Install [Sverchok](https://github.com/nortikin/sverchok/) in [Blender](https://www.blender.org/).
*  Download the [zip file]() from github
*  Open *conway.py* as a text block in Blender.
*  Open *snl_plato.py* and *snl_conway_op.py*  as text blocks in Blender. These contain code for each Sverchok *Scripted Node Lite*.
*  In a *Node Editor* view create a new *Node Tree* and add two *Scripted Node Lite* nodes.
*  Use the notebook icon on the node to select *snl_plato.py* on the left node and *snl_comway_op.py* on the right node. Click the plug icon on each node to load the code.
* Wire up the nodes along with a *Viewer Draw* node as shown below.

![conway nodes](/images/conway_aD.png)

Wire up multiple copies of *snl_conway_op.py* in a row to produce more complex shapes.

![conway_aagD](/images/conway_aagD.png)

Two of the operators *kis* and *chamfer* can take parameters such as the height of the *kis* pyramid or the *height* and *thickness* of the *chamfer*. There is a separate *Scripted Node Lite* given for these two operators with sliders for the parameters.

Some operators, particularly *gyro*, *propellor* and *whirl* and *chamfer* give polyhedra that are not particularly smooth or convex, the faces may not be flat or symmetric.

![conway cgC](/images/conway_cgC.png)

The canonical form of a convex polyhedra has all faces planar and all edges tangential to the unit sphere. The centre of gravity of the tangential points is also at the centre of the same unit sphere.

The module *canon.py* contiains functions that attempt to shift the points of a polyhedron to satisfy these conditions. This is a iterative process and can take several hundred steps to converge.

To try this in Sverchok, add the *canon.py* and *snl_canon.py* files as text blocks in your Blender file and add *snl_canon.py* as a *Scripted Node Lite*. The node has two parameters *iterations* and *scale_factor*. At each iteration the vertices are moved a *scale_factor* fraction of the calculated distance. Setting this parameter too high may cause the shape to become unstable. Increasing the *iterations* will increase the calculation time.

![conway_CcgC.png](/images/conway_CcgC.png)

The canonicalization can also be applied after each operator. In the example below just enough iterations have been applied to form a pleasing shape. The proper canonical form of this polyhedra should be the same whether the canonicalization is performed once or twice.

![conway_CcCgC.png](/images/conway_CcCgC.png)

These Conway operators can be applied to any manifold (ie. a closed solid) mesh not just the platonic solids. They currently don't work on planar grids unless one applies a solidify node to the grid first.

![conway_kg_hexa_grid](/images/conway_kg_hexa_grid.png)

Other Sverchok nodes of course can be used interspersed with the Conway operators for other effects.

I've only implemented a subset of the operators defined on the Wikipedia page. Many of the operators are equivalent to a combination of other operators as shown in the chart

### Conversion chart
The operator order is given as the left to right node order. Note that this is the opposite to the order given in the Conway notation.

| Operator     | Description   | Implementation |
| :----------- | :------------ | :-----------   |
| kis          | poke face              | node           |
| dual         | faces become vertices, vertices become faces | node |
| ambo         | full vertex bevel      | node           |
| chamfer      | hexagons replace edges | node           |
| gyro         | faces divided into pentagons | node           |
| whirl        | insets a smaller rotated copy of the face  | node           |
| propellor    | insets a rotated copy of the face | node           |
| zip          | dual of kis           | kis dual       |
| expand       | edge bevel            | ambo ambo      |
| bevel        | vertex bevel applied twice  | ambo dual kis dual  |
| snub         | dual of gyro          | gyro dual      |
| join         | dual of ambo          | ambo dual      |
| needle       | dual of truncate    | dual kis       |
| ortho        | single subdivide | ambo ambo dual |
| meta         | poke face and subdivide edges     | ambo dual kis  |
| truncate     |  half vertex bevel| dual kis dual  |


See my [Look Think Make](http://elfnor.com/) blog for more info.

