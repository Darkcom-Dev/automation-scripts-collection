#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import numpy as np
from PIL import Image
from math import pi, atan2, asin, sqrt
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox

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


def prepare_to_cubemap(img: str, output_filename: str, size=512):
    equi = Image.open(img).convert("RGB")
    faces = cubemap_faces(equi, size)

    for k, img in faces.items():
        img.save(f"{output_filename}-{k}.png")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Equirectangular to Cubemap Converter")
        self.filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp"), ("HDR files", "*.hdr *.exr *.tif *.tiff"), ("All files", "*.*")]
        
        self.label = tk.Label(root, text="Select an equirectangular image to convert:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.input_file_value = tk.StringVar()
        self.input_entry = tk.Entry(root, textvariable=self.input_file_value, width=50)
        self.input_entry.grid(row=1, column=0, padx=10, pady=5)
        self.input_examine_button = tk.Button(root, text="Browse", command=self.browse_input_file)
        self.input_examine_button.grid(row=1, column=1, padx=10, pady=5)

        self.output_file_value = tk.StringVar()
        self.output_label = tk.Label(root, text="Output filename base:")
        self.output_label.grid(row=2, column=0, padx=10, pady=5)
        self.output_entry = tk.Entry(root, textvariable=self.output_file_value, width=50)
        self.output_entry.grid(row=3, column=0, padx=10, pady=5)

        self.size_file_value = tk.IntVar(value=512)
        self.size_label = tk.Label(root, text="Cubemap face size:")
        self.size_label.grid(row=4, column=0, padx=10, pady=5)
        self.size_entry = tk.Entry(root, textvariable=self.size_file_value, width=10)
        self.size_entry.grid(row=5, column=0, padx=10, pady=5)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_image)
        self.convert_button.grid(row=6, column=0, padx=10, pady=10)

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=self.filetypes)
        if file_path:
            self.input_file_value.set(file_path)

    def convert_image(self):
        file_path = self.input_file_value.get()
        output_filename = self.output_file_value.get()
        size = self.size_file_value.get()

        if file_path and output_filename:
            try:
                prepare_to_cubemap(file_path, output_filename, size)
                messagebox.showinfo("Success", "Cubemap faces saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                print(e)
        else:
            messagebox.showerror("Error", "Please provide both input and output paths.")
            print("Please provide both input and output paths.")


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Convert equirectangular image to cubemap faces.')
    argparser.add_argument('--input', '-i', type=str, help='Path to the input equirectangular image.')
    argparser.add_argument('--size', '-s', type=int, default=512, help='Size of each cubemap face (default: 512).')
    argparser.add_argument('--output', '-o', type=str, help='Output filename base for cubemap faces.')
    args = argparser.parse_args()

    if args.input:
        prepare_to_cubemap(args.input, args.output, args.size)
    else:
        main()

