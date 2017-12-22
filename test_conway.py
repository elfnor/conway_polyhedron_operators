#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_conway.py

tests for conway.py
uses standalaone version of mathutils
https://github.com/majimboo/py-mathutils

Created on Sat Nov 11 15:03:24 2017

@author: elfnor
"""
from collections import defaultdict
import random
import pytest
import mathutils
import conway

from plato_solid import source as solid

# ---- Face and edge functions


def random_unit_vector():
    """
    points uniformly distributed on unit sphere
    http://mathworld.wolfram.com/SpherePointPicking.html
    """
    x, y, z = [random.gauss(0.0, 1.0) for i in range(3)]
    r = (x * x + y * y + z * z)**0.5
    return mathutils.Vector([x/r, y/r, z/r])


def test_tri_face_center():
    """
    random triangular face with known center
    """
    center_given = random_unit_vector()       
    v1 = random_unit_vector()
    v2 = random_unit_vector()   
    v3 = -1.0 * (v1 + v2)   
    verts = [list(v1 + center_given), 
             list(v2 + + center_given), 
             list(v3 + center_given)]
    face = range(3)
    center_calc = conway.face_center(verts, face)
    assert list(center_given) == pytest.approx(center_calc, abs=1e-6)


def test_simple_face_center():
    """
    square face at origin
    """
    center_given = [0., 0., 0.]
    verts = [[1., 0., 0.], [0., 1., 0.], [-1., 0., 0.], [0., -1., 0.]]
    face = list(range(4))
    center_calc = conway.face_center(verts, face)
    assert center_given == pytest.approx(center_calc)   


def test_simple_edge_center():
    """
    square face at origin
    """
    verts = [[1., 1., 0.], [-1., 1., 0.], [-1., -1., 0.], [1., -1., 0.]]
    edge = [0, 1]
    center = conway.edge_center(verts, edge)
    assert center == pytest.approx([0., 1., 0.])


def test_simple_edge_third():
    """
    square face at origin
    """
    verts = [[1., 1., 0.], [-1., 1., 0.], [-1., -1., 0.], [1., -1., 0.]]
    edge = [0, 1]   
    third = conway.edge_third(verts, edge)
    assert third == pytest.approx([1/3., 1., 0.])


def test_simple_tangent_point():
    """
    quad face at origin
    """
    verts = [[2., 1., 0.], [-1., 1., 0.], [-1., -1., 0.], [1., -1., 0.]]
    edge = [0, 1]
    tangent = conway.tangent_point(verts, edge)
    assert tangent == pytest.approx([0., 1., 0.])
 
# ---- flag tag functions    


def face_sort(faces_in):
    """
    sorts each face so that lowest index is first but retaining face order
    then sorts all the faces
    used to compare equality of two face lists
    """
    faces_out = []
    for face in faces_in:
        argmin = face.index(min(face))
        face_out = []
        for v_ind, v1 in enumerate(face):
            face_out.insert(0, face[argmin - v_ind - 1])
        faces_out.append(tuple(face_out))
        
    return sorted(faces_out)


@pytest.mark.parametrize("plato_type", ["4", "6", "8", "12", "20"])
def test_faces_flags(plato_type):
    """
    convert to flags and back again
    should get same structure but different order or faces and verts within faces
    use face_sort to compare
    """
    verts, faces1 = solid(plato_type)
    flags, vert_tags = conway.faces_to_flags(faces1)
    faces2, face_tags = conway.flags_to_faces(flags, vert_tags)
    assert face_sort(faces1) == face_sort(faces2)
    
# ---- Conway Operators

# test each for correct number of verts, edges, faces after operator


def part_count(verts, faces):
    """
    :param verts: list of x, y, z coords of verticies
    :param faces: list of indcies of verts in each face
    :return: count of verticices,  edges and faces
    """
    edge_count = 0.5 * len([v for face in faces for v in face])
    vert_count = len(verts)
    face_count = len(faces)
    # check Euler characteristic
    assert vert_count + face_count - edge_count == 2
    return vert_count, edge_count, face_count


@pytest.mark.parametrize("plato_type, count", [
    ("4", (4, 6, 4)),
    ("6", (8, 12, 6)),
    ("8", (6, 12, 8)),
    ("12", (20, 30, 12)),
    ("20", (12, 30, 20)),
])
def test_part_count(plato_type, count):
    assert part_count(*solid(plato_type)) == count


def check_mesh(verts, faces):
    """
    :param verts: list of x, y, z coords of verticies
    :param faces: list of indcies of verts in each face
    :return:

    test verts and faces form a mesh as expected
    """
    # face normal directions?
    # intersections and collisions? mathutils.geometry

    nverts = len(verts)
    face_count = defaultdict(int)
    for face in faces:
        # no duplicate verts in each face
        assert len(face) == len(set(face))
        for v1, v2 in zip(face, face[1:] + face[:1]):
            # no vert indices in faces > len(verts)
            assert v1 < nverts
            edge_key = 'v{}v{}'.format(*sorted((v1, v2)))
            face_count[edge_key] += 1

    # every edge belongs to two and only two different faces
    assert list(face_count.values()) == [2] * len(face_count)

    # no duplicate faces
    assert len(faces) == len(set(face_sort(faces)))
    # 3 co-ords per vert
    for v_co in verts:
        assert len(v_co) == 3


@pytest.mark.parametrize("plato_type", ["4", "6", "8", "12", "20"])
def test_mesh_plato(plato_type):
    check_mesh(*solid(plato_type))


# this fixture and test applies each of the conway operators to each of the
# platonic solids, checks the v, e, f counts and mesh structure

@pytest.mark.parametrize("plato_type", ["4", "6", "8", "12", "20"])
@pytest.mark.parametrize("cw_op, count_fns", [
    (conway.kis, {'v': lambda v, e, f: v + f,
                  'e': lambda v, e, f: 3 * e,
                  'f': lambda v, e, f: 2 * e}),

    (conway.dual, {'v': lambda v, e, f: f,
                   'e': lambda v, e, f: e,
                   'f': lambda v, e, f: v}),

    (conway.ambo, {'v': lambda v, e, f: e,
                   'e': lambda v, e, f: 2 * e,
                   'f': lambda v, e, f: v + f}),

    (conway.chamfer, {'v': lambda v, e, f: v + 2 * e,
                      'e': lambda v, e, f: 4 * e,
                      'f': lambda v, e, f: e + f}),

    (conway.gyro, {'v': lambda v, e, f: v + 2 * e + f,
                   'e': lambda v, e, f: 5 * e,
                   'f': lambda v, e, f: 2 * e}),

    (conway.propellor, {'v': lambda v, e, f: v + 2 * e,
                        'e': lambda v, e, f: 5 * e,
                        'f': lambda v, e, f: 2 * e + f}),

    (conway.whirl, {'v': lambda v, e, f: v + 4 * e,
                    'e': lambda v, e, f: 7 * e,
                    'f': lambda v, e, f: 2 * e + f}),
])
def test_operator(plato_type, cw_op, count_fns):
    verts1, faces1 = solid(plato_type)
    v1, e1, f1 = part_count(verts1, faces1)
    verts2, faces2 = cw_op(verts1, faces1)
    check_mesh(verts2, faces2)
    v2, e2, f2 = part_count(verts2, faces2)
    assert v2 == count_fns['v'](v1, e1, f1)
    assert e2 == count_fns['e'](v1, e1, f1)
    assert f2 == count_fns['f'](v1, e1, f1)
