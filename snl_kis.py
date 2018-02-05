"""
in height        s d=0.1 n=1
in verts_in      v d=[] n=1
in faces_in         s d=[] n=1
out verts_out     v
out faces_out        s 
"""

from conway import kis 

verts_kis, faces_kis = kis(verts_in, faces_in, height)

faces_out.append(faces_kis) 
verts_out.append(verts_kis)  



