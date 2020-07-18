"""
in verts_in      v d=[] n=1
in faces_in         s d=[] n=1
enum = identity kis dual ambo chamfer gyro propellor whirl 
out verts_out     v
out faces_out        s
"""

import bpy
conway = bpy.data.texts["conway.py"].as_module()

def ui(self, context, layout):
    layout.prop(self, 'custom_enum', expand=False)


if self.custom_enum == 'identity':
    faces_op = faces_in
    verts_op = verts_in
else:
    cw_op = getattr(conway, self.custom_enum)
    verts_op, faces_op = cw_op(verts_in, faces_in)


faces_out.append(faces_op) 
verts_out.append(verts_op) 