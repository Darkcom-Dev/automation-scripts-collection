#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
import argparse
from pathlib import Path

def propose_name(channel, coincidences_list):
    """
    Proposes a name for a channel based on a list of coincidences.
    """
    for coincidence in coincidences_list:
        if coincidence.lower() in channel.lower():
            return coincidence
    return channel


def merge_channels(size=512, red='', green='', blue='', alpha='', save_filename=''):
    """
    Merges image channels into an RGBA image and saves it.
    """
    channels = [red, green, blue, alpha]
    images = []

    for channel in channels:
        if channel:
            img = Image.open(channel)
            images.append(img.getchannel(0).resize([size, size]))
        else:
            images.append(Image.new('L', [size, size], 'white'))

    result = Image.merge('RGBA', images)

    if not save_filename:
        r = 'r-' + propose_name(red, ['rough', 'roughness', 'gloss'])
        g = 'g-' + propose_name(green, ['heigh', 'metal'])
        b = 'b-' + propose_name(blue, ['ao', 'specular'])
        a = 'a-' + propose_name(alpha, ['alpha', 'emission', 'emissive'])
        save_filename = f'{r}-{g}-{b}-{a}-{size}.png'

    result.save(save_filename)
    result.show()


class App:
    def __init__(self, window):
        self.win = window
        self.win.config(width=800, height=600)
        self.win.title('Texture Channel Mixer')

        ttk.Label(self.win, text='Este programa combina 3 o 4 imágenes grises en un solo RGBA').grid(column=0, row=0, sticky='WE', columnspan=2)
        ttk.Label(self.win, text='** Se creará un canal blanco por cada ruta faltante').grid(column=0, row=11, sticky='WE', columnspan=2)

        filetypes = [('Texture files', '*.png *.tif *.jpg *.jpeg'), ('All files', '*.*')]

        self.r_filename = self.create_file_selector('R para rough o gloss', 1, filetypes)
        self.g_filename = self.create_file_selector('G para heigh o metallic', 3, filetypes)
        self.b_filename = self.create_file_selector('B para ao o specular si está en escala de grises', 5, filetypes)
        self.a_filename = self.create_file_selector('A para alpha o emission si el color depende de albedo', 7, filetypes)

        ttk.Label(self.win, text='Ruta y nombre del nuevo archivo resultante').grid(column=0, row=9, sticky='WE')
        self.save_filename = ttk.Entry(self.win)
        self.save_filename.grid(column=0, row=10, sticky='WE', padx=5)

        ttk.Button(self.win, text='Aplicar', command=self.apply).grid(column=1, row=10)

    def create_file_selector(self, label_text, row, filetypes):
        """
        Helper to create file selectors for each channel.
        """
        filename_var = tk.StringVar()
        ttk.Label(self.win, text=label_text).grid(column=0, row=row, sticky='WE')
        entry = ttk.Entry(self.win, textvariable=filename_var)
        entry.grid(column=0, row=row + 1, sticky='WE', padx=5)
        ttk.Button(self.win, text='Examine', command=lambda: filename_var.set(askopenfilename(filetypes=filetypes))).grid(column=1, row=row + 1)
        return filename_var

    def apply(self):
        """
        Apply the channel merging based on user input.
        """
        merge_channels(
            size=512,
            red=self.r_filename.get(),
            green=self.g_filename.get(),
            blue=self.b_filename.get(),
            alpha=self.a_filename.get(),
            save_filename=self.save_filename.get()
        )


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge image files into one RGBA image, one for each channel')
    parser.add_argument('-r', '--red', type=Path, help='Path to the file for R channel')
    parser.add_argument('-g', '--green', type=Path, help='Path to the file for G channel')
    parser.add_argument('-b', '--blue', type=Path, help='Path to the file for B channel')
    parser.add_argument('-a', '--alpha', type=Path, help='Path to the file for A channel')
    parser.add_argument('-o', '--output', type=Path, help='Path to the output file')
    parser.add_argument('-s', '--size', type=int, help='Size of the texture', default=512)

    args = parser.parse_args()

    if any([args.red, args.green, args.blue, args.alpha, args.output]):
        merge_channels(
            size=args.size,
            red=str(args.red) if args.red else '',
            green=str(args.green) if args.green else '',
            blue=str(args.blue) if args.blue else '',
            alpha=str(args.alpha) if args.alpha else '',
            save_filename=str(args.output) if args.output else ''
        )
    else:
        main()
