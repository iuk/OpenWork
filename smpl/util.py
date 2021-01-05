#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2021 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : util.py
#   Author      : YunYang1994
#   Created date: 2021-01-05 17:37:13
#   Description :
#
#================================================================


import cv2
import trimesh
import pyrender
import numpy as np
import chumpy as ch

class Rodrigues(ch.Ch):
    dterms = 'rt'

    def compute_r(self):
        return cv2.Rodrigues(self.rt.r)[0]

    def compute_dr_wrt(self, wrt):
        if wrt is self.rt:
            return cv2.Rodrigues(self.rt.r)[1].T

def posemap(p):
    if isinstance(p, np.ndarray):
        p = p.ravel()[3:]
        return np.concatenate([(cv2.Rodrigues(np.array(pp))[0]-np.eye(3)).ravel() for pp in p.reshape((-1,3))]).ravel()
    if p.ndim != 2 or p.shape[1] != 3:
        p = p.reshape((-1,3))
    p = p[1:]
    return ch.concatenate([(Rodrigues(pp)-ch.eye(3)).ravel() for pp in p]).ravel()

def render(vertices, faces):
    vertex_colors = np.ones([vertices.shape[0], 4]) * [0.3, 0.3, 0.3, 0.9]
    tri_mesh = trimesh.Trimesh(vertices, faces, vertex_colors=vertex_colors)

    # adding body meshs
    mesh = pyrender.Mesh.from_trimesh(tri_mesh)
    scene = pyrender.Scene()
    scene.add(mesh)

    # adding obeserving camera
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.414)
    camera_pose = np.eye(4)
    camera_pose[:3, 3] = np.array([0, 0, 5])
    scene.add(camera, pose=camera_pose)

    pyrender.Viewer(scene, use_raymond_lighting=True)


