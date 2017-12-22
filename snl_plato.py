"""
in dummy  s
enum = tetra octa cube dodeca icosa
out vertices      v
out faces         v 
"""

plato = {'tetra': "4",'cube': '6', 'octa': '8', 'dodeca': '12', 'icosa': '20'}

from add_mesh_extra_objects.add_mesh_solid import source

def ui(self, context, layout):
    layout.prop(self, 'custom_enum', expand=False)


vectors, faces = source(plato[self.custom_enum])
vertices = [list(v) for v in vectors]
   
# match  nesting of other Sverchok generators
vertices = [vertices]
faces = [faces]