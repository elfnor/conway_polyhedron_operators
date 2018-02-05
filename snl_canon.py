"""
in iterations s d=20 n=1
in scale_factor s d=0.1 n=1
in verts_in      v d=[] n=1
in faces_in         s d=[] n=1
out verts_out     v
"""

import mathutils
from canon import canonize


verts_new = [mathutils.Vector(v_xyz) for v_xyz in verts_in]

verts_canon = canonize(verts_new, faces_in, iterations, scale_factor)

verts_canon = [list(verts_canon[v_i]) for v_i, v_xyz in enumerate(verts_new)]
verts_out.append(verts_canon)


