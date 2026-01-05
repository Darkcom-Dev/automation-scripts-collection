#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import numpy as np
from PIL import Image
from math import sin, cos, pi

def cubemap_to_equirect(faces, width, height):
    size = faces["px"].size[0]
    face_np = {k: np.array(v) for k, v in faces.items()}

    out = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        lat = (0.5 - y / height) * pi
        for x in range(width):
            lon = (x / width - 0.5) * 2 * pi

            vx = cos(lat) * cos(lon)
            vy = sin(lat)
            vz = cos(lat) * sin(lon)

            ax, ay, az = abs(vx), abs(vy), abs(vz)

            if ax >= ay and ax >= az:
                if vx > 0:
                    face = "px"
                    u, v = -vz/ax, -vy/ax
                else:
                    face = "nx"
                    u, v =  vz/ax, -vy/ax
            elif ay >= ax and ay >= az:
                if vy > 0:
                    face = "py"
                    u, v =  vx/ay,  vz/ay
                else:
                    face = "ny"
                    u, v =  vx/ay, -vz/ay
            else:
                if vz > 0:
                    face = "pz"
                    u, v =  vx/az, -vy/az
                else:
                    face = "nz"
                    u, v = -vx/az, -vy/az

            px = min(size - 1, max(0, int((u + 1) * 0.5 * size)))
            py = min(size - 1, max(0, int((v + 1) * 0.5 * size)))

            out[y, x] = face_np[face][py, px]

    return Image.fromarray(out)


def main():
	pass

if __name__ == "__main__":
	main()