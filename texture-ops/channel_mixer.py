#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
import argparse

def propose_name(channel, coincidences_list):
    """
    Proposes a name for a channel based on a list of coincidences.

    Args:
        channel (str): The original channel name.
        coincidences_list (list): A list of possible coincidences.

    Returns:
        str: The proposed name, either the original channel name or a coincidence.
    >>> propose_name('blue', ['blues', 'blue', 'blu'])
    'blue'
    >>> propose_name('rock_Emission', ['emission', 'emissive'])
    'emission'
    >>> propose_name('rock_Gloss', ['rough', 'roughness', 'gloss'])
    'gloss'
    >>> propose_name('rockao', ['ambient occlusion', 'specular', 'ao'])# Esto es un fallo
    'ao'
    """
    if coincidences_list == []:
        return channel
    else:
        for coincidence in coincidences_list:
            if channel.lower().find(coincidence) != -1:
                return coincidence
        return channel


def merge_channels(size:int = 512, red='', green='', blue='', alpha='', save_filename=''):
    """
    Merges channels of images into a single RGBA image and saves it as a PNG file.

    Args:
        size (int): The size of the output image.
        routes (List[str]): A list of file routes to the input images for each channel. If a route is empty, a white image will be used for that channel.
        save_filename (str): The filename of the output image.

    Returns:
        None

    Raises:
        FileNotFoundError: If any of the input image files cannot be found.
    """

    images = []

    for channel in (red,green,blue,alpha):
        if channel == '':
            images.append(Image.new('L',[size,size],'white'))
        else:
            img = Image.open(channel,'r')
            images.append(img.getchannel(0).resize([size,size]))
    
    result = Image.merge('RGBA',images)
    if save_filename == '':
        r = 'r-'+ propose_name(red,['rough','roughness','gloss'])
        g = 'g-'+ propose_name(green,['heigh','metal'])
        b = 'b-'+ propose_name(blue,['ao','specular'])
        a = 'a-'+ propose_name(alpha,['alpha','emission', 'emissive'])
        result.save(f'-{r}-{g}-{b}-{a}-{size}','png')
    else:
        result.save(save_filename,'png')
    result.show()

class App():
    def __init__(self, window) -> None:
        """
        Initializes the TextureChannelMixer class.

        Args:
            window: The main window object.

        Returns:
            None.
        """
        self.win = window
        self.win.config(width=800, height=600)
        self.win.title('Texture channel mixer')

        
        # Etiqueta y botones
        instructions = ttk.Label(self.win,text='Este programa combina 3 o 4 imágenes grises en uno solo RGBA')
        instructions.grid(column= 0,row= 0, sticky='WE', columnspan=2)
        instructions1 = ttk.Label(self.win,text='** Se creará un canal blanco por cada ruta faltante')
        instructions1.grid(column= 0,row= 11, sticky='WE', columnspan=2)

        filetypes = [('Texture files',r'*.png *.tif *.jpg'),('All files',r'*.*')]
        # Canal R

        r_filename = tk.StringVar()

        r_label = ttk.Label(self.win,text='R para rough o gloss')
        r_label.grid(column= 0,row= 1, sticky='WE')
        r_entry = ttk.Entry(self.win, textvariable=r_filename)
        r_entry.grid(column= 0, row= 2, sticky='WE',padx= 5)
        r_button = ttk.Button(self.win,text='Examine',command= lambda: r_filename.set(askopenfilename(filetypes=filetypes)))
        r_button.grid(column= 1, row= 2)
        
        # Canal G
        g_filename = tk.StringVar()
        g_label = ttk.Label(self.win,text='G para heigh o metallic')
        g_label.grid(column= 0, row= 3, sticky='WE')
        g_entry = ttk.Entry(self.win,textvariable=g_filename)
        g_entry.grid(column= 0, row= 4, sticky='WE',padx= 5)
        g_button = ttk.Button(self.win, text='Examine',command=lambda: g_filename.set(askopenfilename(filetypes=filetypes)))
        g_button.grid(column= 1, row= 4)
        
        # Canal B
        b_filename = tk.StringVar()
        b_label = ttk.Label(self.win,text='B para ao o specular si está en escala de grises')
        b_label.grid(column= 0, row= 5, sticky='WE')
        b_entry = ttk.Entry(self.win, textvariable=b_filename)
        b_entry.grid(column= 0, row= 6, sticky='WE',padx= 5)
        b_button = ttk.Button(self.win, text='Examine',command=lambda: b_filename.set(askopenfilename(filetypes=filetypes)))
        b_button.grid(column= 1, row= 6)
        
        # Canal A
        a_filename = tk.StringVar()
        a_label = ttk.Label(self.win,text='A para alpha o emission si el color depende de albedo')
        a_label.grid(column= 0, row= 7, sticky='WE')
        a_entry = ttk.Entry(self.win, textvariable=a_filename)
        a_entry.grid(column= 0, row= 8, sticky='WE',padx= 5)
        a_button = ttk.Button(self.win, text='Examine',command=lambda: a_filename.set(askopenfilename(filetypes=filetypes)))
        a_button.grid(column= 1, row= 8)
        
        # Aplicacion
        apply_label = ttk.Label(self.win,text='Ruta y nombre del nuevo archivo resultante')
        apply_label.grid(column= 0, row= 9, sticky='WE')
        apply_entry = ttk.Entry(self.win)
        apply_entry.grid(column= 0, row= 10, sticky='WE',padx= 5)
        # file_list = [r_filename.get(),g_filename.get(),b_filename.get(),a_filename.get()]
        apply_button = ttk.Button(self.win, text='Aplicar',command=lambda:merge_channels(512,[r_filename.get(),g_filename.get(),b_filename.get(),a_filename.get()],apply_entry.get())) # .save(f'{apply_entry.getvar()}.png', 'png')
        apply_button.grid(column= 1, row= 10)

parser = argparse.ArgumentParser()

def main():
    # Ventana
    root = tk.Tk()
    application = App(root)
    root.mainloop()

if __name__ == '__main__':

    parser.add_argument('-r', '--red', type=str, help='Path to the file for R channel')
    parser.add_argument('-g', '--green',type=str, help='Path to the file for G channel')
    parser.add_argument('-b', '--blue',type=str, help='Path to the file for B channel')
    parser.add_argument('-a', '--alpha',type=str, help='Path to the file for A channel')
    parser.add_argument('-o', '--output',type=str, help='Path to the output file')
    parser.add_argument('-s', '--size',type=int, help='Size of the texture')
    parser.description = 'Merge image files into one RGBA image, one for each channel'
    args = parser.parse_args()
    if hasattr(args, 'r') and hasattr(args, 'g') and hasattr(args, 'b') and hasattr(args, 'a') and hasattr(args, 'o') and hasattr(args, 's'):
        merge_channels(size=args.s,red=args.r,green=args.g,blue=args.b,alpha=args.a,save_filename=args.o)
    else:
        main()

