#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageChops
import argparse
import tkinter as tk
from tkinter.filedialog import askopenfilename


def convert_to_psx_texture(basecolor_path, ao_path, save_path, size, channel_option='RGBA'):
    basecolor = Image.open(basecolor_path).convert('RGBA').resize((size, size))
    
    if ao_path is None or ao_path == '' or ao_path.lower() == 'white':
        ao = Image.new("L", (size, size), 255)
    else:
        if channel_option in ['R', 'G', 'B', 'A']:
            ao = Image.open(ao_path).convert('RGBA').resize((size, size))
            ao = ao.getchannel(channel_option)
        else:
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
        self.win.config(width=1000, height=600)
        self.win.title('PSX Texture Converter')
        self.win.resizable(False, False)
        
        filetypes = [('Texture files', '*.png *.tif *.jpg *.jpeg'), ('All files', '*.*')] 
        tk.Label(self.win, text='Merge Albedo and Ambient Occlusion in multiply mode to 16-color indexed PSX texture').grid(column=0, row=0, columnspan=4, pady=10)
        # Basecolor
        tk.Label(self.win, text='Albedo, Basecolor').grid(column=0, row=1, sticky='W', columnspan=2)
        basecolor_path = tk.StringVar()
        tk.Entry(self.win, textvariable=basecolor_path).grid(column=0, row=2, sticky='WE', columnspan=3)
        tk.Button(self.win, text='Examine', command=lambda: basecolor_path.set(askopenfilename(filetypes=filetypes))).grid(column=3, row=2, sticky='E')
        
        # Ambient Occlusion
        tk.Label(self.win, text='Ambient Occlusion').grid(column=0, row=3, sticky='W', columnspan=2)
        ao_path = tk.StringVar()
        tk.Entry(self.win, textvariable=ao_path).grid(column=0, row=4, sticky='WE', columnspan=3)
        tk.Button(self.win, text='Examine', command=lambda: ao_path.set(askopenfilename(filetypes=filetypes))).grid(column=3, row=4, sticky='E')

        # Output filename
        tk.Label(self.win, text='Output filename').grid(column=0, row=5, sticky='W', columnspan=2)
        save_path = tk.StringVar()
        tk.Entry(self.win, textvariable=save_path).grid(column=0, row=6, sticky='WE', columnspan=3)
        
        # Size and Channel option
        tk.Label(self.win, text='Size (default 256)').grid(column=0, row=7, sticky='WE', columnspan=2)
        size_var = tk.StringVar(value='256')
        tk.Label(self.win, text='Channel (RGBA, R, G, B, A)').grid(column=2, row=7)
        tk.Entry(self.win, textvariable=size_var).grid(column=0, row=8, sticky='WE', columnspan=2)
        self.channel_option = tk.StringVar(value='RGBA')
        tk.OptionMenu(self.win, self.channel_option, 'RGBA','R', 'G', 'B', 'A').grid(column=2, row=8, sticky='WE')

        # Convert button
        tk.Button(self.win, text='Convert', command=lambda: convert_to_psx_texture(basecolor_path.get(), ao_path.get(), save_path.get(), int(size_var.get()), self.channel_option.get())).grid(column=3, row=8, sticky='E')

        

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
    parser.add_argument('--channel', '-c', type=str, default='RGBA', help='Channel to use for the PSX texture (default: RGBA).')

    args = parser.parse_args()
    if any([args.basecolor, args.ao, args.output]):
        convert_to_psx_texture(args.basecolor, args.ao, args.output, args.size, args.channel)
    else:
        main()