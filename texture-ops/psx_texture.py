#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageChops
import argparse
import tkinter as tk
from tkinter.filedialog import askopenfilename


def convert_to_psx_texture(basecolor_path, ao_path, save_path, size):
    basecolor = Image.open(basecolor_path).convert('RGBA').resize((size, size))
    
    ao = Image.open(ao_path).convert('L').resize((size, size))
        # Expandir AO a RGBA
    ao = Image.merge("RGBA", (ao, ao, ao, Image.new("L", ao.size, 255)))
    psx_texture = ImageChops.multiply(basecolor, ao)
    # Convert RGBA to Indexed color mode with a maximum of 16 colors, floid steiberg dithering
    psx_texture = psx_texture.convert('P', palette=Image.ADAPTIVE, colors=16, dither=Image.FLOYDSTEINBERG)
    psx_texture.save(save_path,'png')
    psx_texture.show()

class App:
    def __init__(self, window):
        self.win = window
        self.win.config(width=800, height=600)
        self.win.title('PSX Texture Converter')
        
        filetypes = [('Texture files', '*.png *.tif *.jpg *.jpeg'), ('All files', '*.*')] 

        tk.Label(self.win, text='Albedo, Basecolor').grid(column=0, row=0, sticky='WE', columnspan=2)
        basecolor_path = tk.StringVar()
        tk.Entry(self.win, textvariable=basecolor_path).grid(column=0, row=1, sticky='WE', padx=5, columnspan=2)
        tk.Button(self.win, text='Examine', command=lambda: basecolor_path.set(askopenfilename(filetypes=filetypes))).grid(column=2, row=1)
        tk.Label(self.win, text='Ambient Occlusion').grid(column=0, row=2, sticky='WE', columnspan=2)
        ao_path = tk.StringVar()
        tk.Entry(self.win, textvariable=ao_path).grid(column=0, row=3, sticky='WE', padx=5, columnspan=2)
        tk.Button(self.win, text='Examine', command=lambda: ao_path.set(askopenfilename(filetypes=filetypes))).grid(column=2, row=3)
        tk.Label(self.win, text='Save as').grid(column=0, row=4, sticky='WE', columnspan=2)
        save_path = tk.StringVar()
        tk.Entry(self.win, textvariable=save_path).grid(column=0, row=5, sticky='WE', padx=5, columnspan=2)
        tk.Button(self.win, text='Examine', command=lambda: save_path.set(askopenfilename(filetypes=filetypes))).grid(column=2, row=5)
        tk.Label(self.win, text='Size (default 256)').grid(column=0, row=6, sticky='WE', columnspan=2)
        size_var = tk.StringVar(value='256')
        tk.Entry(self.win, textvariable=size_var).grid(column=0, row=7, sticky='WE', padx=5, columnspan=2)
        tk.Button(self.win, text='Convert', command=lambda: convert_to_psx_texture(basecolor_path.get(), ao_path.get(), save_path.get(), int(size_var.get()))).grid(column=0, row=8, columnspan=3)

        

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Convert basecolor and ambient occlusion textures into a PSX-style texture.')
    parser.add_argument('--basecolor', '-b', type=str, help='Path to the basecolor texture image.')
    parser.add_argument('--ao', '-a', type=str, help='Path to the ambient occlusion texture image.')
    parser.add_argument('--output', '-o', type=str, help='Path to save the resulting PSX texture image.')
    parser.add_argument('--size', '-s', type=int, default=256, help='Size to which the textures will be resized (default: 256).')

    args = parser.parse_args()
    if any([args.basecolor, args.ao, args.output]):
        convert_to_psx_texture(args.basecolor, args.ao, args.output, args.size)
    else:
        main()