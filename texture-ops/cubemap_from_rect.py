#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import numpy as np
from PIL import Image
from math import pi, atan2, asin, sqrt

def cubemap_faces(equi_img, size):
    w, h = equi_img.size
    equi = np.array(equi_img)

    def sample_dir(vx, vy, vz):
        norm = sqrt(vx*vx + vy*vy + vz*vz)
        vx, vy, vz = vx/norm, vy/norm, vz/norm

        lon = atan2(vz, vx)
        lat = asin(vy)

        u = int((lon / (2*pi) + 0.5) * w) % w
        v = int((0.5 - lat / pi) * h)
        return equi[v, u]

    faces = {}
    directions = {
        "px": lambda a,b: ( 1, -b, -a),
        "nx": lambda a,b: (-1, -b,  a),
        "py": lambda a,b: ( a,  1,  b),
        "ny": lambda a,b: ( a, -1, -b),
        "pz": lambda a,b: ( a, -b,  1),
        "nz": lambda a,b: (-a, -b, -1),
    }

    for name, fn in directions.items():
        img = np.zeros((size, size, 3), dtype=np.uint8)
        for y in range(size):
            for x in range(size):
                a = 2 * (x + 0.5) / size - 1
                b = 2 * (y + 0.5) / size - 1
                img[y, x] = sample_dir(*fn(a, b))
        faces[name] = Image.fromarray(img)

    return faces
