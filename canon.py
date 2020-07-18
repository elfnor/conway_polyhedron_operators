

"""
functions used in 'canonicalization' of polyhedra

This canonical form of a polyhedron is where the verticies of the polyhedron are positioned such that:
    all the edges are tangent to the unit sphere,
    the origin is the center of gravity of the points at which the edges touch the sphere,
    the faces are flat (i.e. the vertices of each face lie in some plane), but are not necessarily regular.
"""

import copy
import mathutils
import bpy
cw = bpy.data.texts["conway.py"].as_module()


def tangentify(verts, faces, scale):
    """
    For each edge, find the closest point to the origin
    move the two end points of the edge so the edge is closer to tangent to
    the unit sphere
    """
    verts_tang = copy.deepcopy(verts)
    for face in faces:
        for v1, v2 in zip(face, face[1:] + face[:1]):
            if v1 < v2:
                va_xyz, s = mathutils.geometry.intersect_point_line(
                    mathutils.Vector(),
                    verts[v1], verts[v2])
                c = scale * 0.5 * (1 - va_xyz.length) * va_xyz

                verts_tang[v1] = verts_tang[v1] + c
                verts_tang[v2] = verts_tang[v2] + c

    return verts_tang


def recenter(verts, faces):
    """
    move verts so center of tangent points is at origin
    """
    nedges = 0
    vsum = mathutils.Vector()
    for face in faces:
        for v1, v2 in zip(face, face[1:] + face[:1]):
            if v1 < v2:
                nedges += 1
                va_xyz, s = mathutils.geometry.intersect_point_line(
                    mathutils.Vector(),
                    verts[v1], verts[v2])
                vsum = vsum + va_xyz

    center_xyz = vsum/nedges
    verts_cent = [v_xyz - center_xyz for v_xyz in verts]
    return verts_cent


def planarize(verts, faces, scale):
    """
    move verts in each face closer to a plane defined by the face normal
    direction and the face centroid
    """
    verts_plane = copy.deepcopy(verts)
    for face in faces:
        center_xyz = mathutils.Vector(cw.face_center(verts, face))
        norm = cw.face_normal(verts, face)
        for v1 in face:
            r1 = center_xyz - verts[v1]
            r2 = scale * norm
            r4 = r2.dot(r1) * norm
            verts_plane[v1] = verts_plane[v1] + r4
    return verts_plane

def canonize(verts_new, faces_in, iterations, scale_factor):
    """
    repeat tangentify, recenter, planarize for iterations
    """
    for i in range(iterations):
        verts_old = copy.deepcopy(verts_new)
        verts_new = tangentify(verts_new, faces_in, scale_factor)
        verts_new = recenter(verts_new, faces_in)
        verts_new = planarize(verts_new, faces_in, scale_factor)
        max_change = max([abs((verts_old[v1] - verts_new[v1]).length)
                          for v1, v_xyz in enumerate(verts_old)])
        if max_change < 1e-8:
            break
    return verts_new