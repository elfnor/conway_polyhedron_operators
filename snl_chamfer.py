"""
in thickness        s d=0.34 n=1
in height        s d=0.22 n=1
in verts_in      v d=[] n=1
in faces_in         s d=[] n=1
out verts_out     v
out faces_out        s 
"""

from conway import chamfer

verts_chamfer, faces_chamfer = chamfer(verts_in, faces_in, thickness, height)

faces_out.append(faces_chamfer) 
verts_out.append(verts_chamfer)  
