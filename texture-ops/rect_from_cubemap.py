#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import numpy as np
from PIL import Image
from math import sin, cos, pi
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox

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


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cubemap to Equirectangular Converter")
        self.root.resizable(False, False)
        self.filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.exr")]

        self.label = tk.Label(root, text="Select cubemap face images to convert:")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.px_path = tk.StringVar()
        self.nx_path = tk.StringVar()
        self.py_path = tk.StringVar()
        self.ny_path = tk.StringVar()
        self.pz_path = tk.StringVar()
        self.nz_path = tk.StringVar()

        self.px_label = tk.Label(root, text="Positive X (px):").grid(row=1, column=0, padx=10, pady=5, sticky='E')
        self.nx_label = tk.Label(root, text="Negative X (nx):").grid(row=2, column=0, padx=10, pady=5, sticky='E')
        self.py_label = tk.Label(root, text="Positive Y (py):").grid(row=3, column=0, padx=10, pady=5, sticky='E')
        self.ny_label = tk.Label(root, text="Negative Y (ny):").grid(row=4, column=0, padx=10, pady=5, sticky='E')
        self.pz_label = tk.Label(root, text="Positive Z (pz):").grid(row=5, column=0, padx=10, pady=5, sticky='E')
        self.nz_label = tk.Label(root, text="Negative Z (nz):").grid(row=6, column=0, padx=10, pady=5, sticky='E')


        self.px_entry = tk.Entry(root, textvariable=self.px_path, width=50)
        self.nx_entry = tk.Entry(root, textvariable=self.nx_path, width=50)
        self.py_entry = tk.Entry(root, textvariable=self.py_path, width=50)
        self.ny_entry = tk.Entry(root, textvariable=self.ny_path, width=50)
        self.pz_entry = tk.Entry(root, textvariable=self.pz_path, width=50)
        self.nz_entry = tk.Entry(root, textvariable=self.nz_path, width=50)

        self.px_entry.grid(row=1, column=1, padx=10, pady=5)
        self.nx_entry.grid(row=2, column=1, padx=10, pady=5)
        self.py_entry.grid(row=3, column=1, padx=10, pady=5)
        self.ny_entry.grid(row=4, column=1, padx=10, pady=5)
        self.pz_entry.grid(row=5, column=1, padx=10, pady=5)
        self.nz_entry.grid(row=6, column=1, padx=10, pady=5)

        self.px_button = tk.Button(root, text="Examine", command=lambda: self.px_path.set(filedialog.askopenfilename(filetypes=self.filetypes)))
        self.nx_button = tk.Button(root, text="Examine", command=lambda: self.nx_path.set(filedialog.askopenfilename(filetypes=self.filetypes)))
        self.py_button = tk.Button(root, text="Examine", command=lambda: self.py_path.set(filedialog.askopenfilename(filetypes=self.filetypes)))
        self.ny_button = tk.Button(root, text="Examine", command=lambda: self.ny_path.set(filedialog.askopenfilename(filetypes=self.filetypes)))
        self.pz_button = tk.Button(root, text="Examine", command=lambda: self.pz_path.set(filedialog.askopenfilename(filetypes=self.filetypes)))
        self.nz_button = tk.Button(root, text="Examine", command=lambda: self.nz_path.set(filedialog.askopenfilename(filetypes=self.filetypes)))

        self.px_button.grid(row=1, column=3, padx=10, pady=5, sticky='E')
        self.nx_button.grid(row=2, column=3, padx=10, pady=5, sticky='E')
        self.py_button.grid(row=3, column=3, padx=10, pady=5, sticky='E')
        self.ny_button.grid(row=4, column=3, padx=10, pady=5, sticky='E')
        self.pz_button.grid(row=5, column=3, padx=10, pady=5, sticky='E')
        self.nz_button.grid(row=6, column=3, padx=10, pady=5, sticky='E')

        tk.Label(root, text="Output filename base:").grid(row=7, column=0, padx=10, pady=10)
        self.output_file_value = tk.StringVar()
        self.output_entry = tk.Entry(root, textvariable=self.output_file_value, width=50)
        self.output_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=5)
        self.convert_button = tk.Button(root, text="Convert", command=self.convert_images)
        self.convert_button.grid(row=7, column=3, padx=10, pady=10, sticky='E')

    def convert_images(self):
        output_name = self.output_file_value.get()
        faces = {
            "px": Image.open(self.px_path.get()).convert("RGB"),
            "nx": Image.open(self.nx_path.get()).convert("RGB"),
            "py": Image.open(self.py_path.get()).convert("RGB"),
            "ny": Image.open(self.ny_path.get()).convert("RGB"),
            "pz": Image.open(self.pz_path.get()).convert("RGB"),
            "nz": Image.open(self.nz_path.get()).convert("RGB")
        }
        output = cubemap_to_equirect(faces, 1024, 512)
        output.save(f"{output_name}.png")
        output.show()

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Convert cubemap faces to an equirectangular image.')
    argparser.add_argument('--input', '-i', type=str, help='Input cubemap face filename base (e.g., "cubemap" for cubemap-px.png, cubemap-nx.png, etc.).')
    argparser.add_argument('--size', '-s', type=int, default=1024, help='Width of the output equirectangular image.')
    argparser.add_argument('--output', '-o', type=str, help='Output equirectangular image filename.')
    args = argparser.parse_args()

    if args.input:
        face_names = ["px", "nx", "py", "ny", "pz", "nz"]
        faces = {}
        for name in face_names:
            face_path = f"{args.input}-{name}.png"
            faces[name] = Image.open(face_path).convert("RGB")

        height = args.size // 2
        equirect_img = cubemap_to_equirect(faces, args.size, height)
        equirect_img.save(args.output)
    else:
        main()