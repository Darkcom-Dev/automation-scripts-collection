#!/usr/bin/env python3

from PIL import Image
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
import argparse
from pathlib import Path

def pack_textures(size:int, paths:list, save_filename):
    """
    Generate a packed texture image from a list of image routes.

    Args:
        size (int): The size of each individual texture image.
        paths (list): A list of image routes. Each route represents the file path to an image.
        save_filename (str): The file name under which the packed texture image will be saved.

    Returns:
        None

    Raises:
        FileNotFoundError: If any of the image routes provided do not exist.

    Notes:
        - The packed texture image will have a size of size * 2 by size * 2.
        - Each individual texture image will be pasted onto the packed texture image at a position determined by the index of the image route in the routes list.
        - If an image route is an empty string, a blank texture image of size by size will be pasted at the corresponding position on the packed texture image.
        - The packed texture image will be saved as a PNG file under the provided save_filename.
        - The packed texture image will be displayed after it is saved.

    """
    print()
    result = Image.new('RGBA',[size * 2, size * 2])

    positions = ([0,0],[size,0],[0,size],[size, size])

    for i in range(0,4):
        if paths[i] == '':
            result.paste(Image.new('L',[size,size]),positions[i])
        else:
            result.paste(Image.open(paths[i],'r').resize([size,size]), positions[i])

    result.save(save_filename,'png')
    result.show()

class App():
    def __init__(self, window) -> None:
        """
        Initializes the class with a window object.

        Parameters:
            window (object): The window object to be used for the application.

        Returns:
            None
        """

        self.win = window
        self.win.config(width=800, height=600)
        self.win.title('Texture channel mixer')

        
        # Etiqueta y botones
        instructions = ttk.Label(self.win,text='Este programa combina de 1 a 4 imágenes como un pack')
        instructions.grid(column= 0,row= 0, sticky='WE', columnspan=2)
        instructions1 = ttk.Label(self.win,text='** Se creará una imagen blanca por cada ruta faltante')
        instructions1.grid(column= 0,row= 11, sticky='WE', columnspan=2)

        filetypes = [('texture files',r'*.png *.tif *.jpg *.jpeg'),('all files','*.*')]
        # Canal R

        r_filename = tk.StringVar()

        r_label = ttk.Label(self.win,text='Primera imagen - superior izquierda')
        r_label.grid(column= 0,row= 1, sticky='WE')
        r_entry = ttk.Entry(self.win, textvariable=r_filename)
        r_entry.grid(column= 0, row= 2, sticky='WE',padx= 5,columnspan=2)
        r_button = ttk.Button(self.win,text='Examine',command= lambda: r_filename.set(askopenfilename(filetypes= filetypes)))
        r_button.grid(column= 2, row= 2)
        
        # Canal G
        g_filename = tk.StringVar()
        g_label = ttk.Label(self.win,text='Segunda imagen - superior derecha')
        g_label.grid(column= 0, row= 3, sticky='WE')
        g_entry = ttk.Entry(self.win,textvariable=g_filename)
        g_entry.grid(column= 0, row= 4, sticky='WE',padx= 5, columnspan=2)
        g_button = ttk.Button(self.win, text='Examine',command=lambda: g_filename.set(askopenfilename(filetypes=filetypes)))
        g_button.grid(column= 2, row= 4)
        
        # Canal B
        b_filename = tk.StringVar()
        b_label = ttk.Label(self.win,text='Tercera imagen - inferior izquierda')
        b_label.grid(column= 0, row= 5, sticky='WE')
        b_entry = ttk.Entry(self.win, textvariable=b_filename)
        b_entry.grid(column= 0, row= 6, sticky='WE',padx= 5, columnspan=2)
        b_button = ttk.Button(self.win, text='Examine',command=lambda: b_filename.set(askopenfilename(filetypes=filetypes)))
        b_button.grid(column= 2, row= 6)
        
        # Canal A
        a_filename = tk.StringVar()
        a_label = ttk.Label(self.win,text='Cuarta imagen - inferior derecha')
        a_label.grid(column= 0, row= 7, sticky='WE')
        a_entry = ttk.Entry(self.win, textvariable=a_filename)
        a_entry.grid(column= 0, row= 8, sticky='WE',padx= 5, columnspan=2)
        a_button = ttk.Button(self.win, text='Examine',command=lambda: a_filename.set(askopenfilename(filetypes=filetypes)))
        a_button.grid(column= 2, row= 8)
        
        # Aplicacion
        apply_label = ttk.Label(self.win,text='Ruta y nombre del nuevo archivo resultante y tamaño')
        apply_label.grid(column= 0, row= 9, sticky='WE')
        apply_entry = ttk.Entry(self.win)
        apply_entry.grid(column= 0, row= 10, sticky='WE',padx= 5)
        sizes = [256,512,1024,2048,4096]
        size_drop = tk.Spinbox(self.win, values= sizes)
        size_drop.grid(column= 1, row= 10)
        apply_button = ttk.Button(self.win, text='Aplicar',command=lambda:pack_textures(int(size_drop.get()),[r_filename.get(),g_filename.get(),b_filename.get(),a_filename.get()],apply_entry.get())) # .save(f'{apply_entry.getvar()}.png', 'png')
        apply_button.grid(column= 2, row= 10)

def main():
    # Ventana
    root = tk.Tk()
    application = App(root)
    root.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Texture Atlas packer')
    parser.add_argument('-s', '--size', type=int, help='Size of the texture')
    parser.add_argument('-tl', '--top-left', type=Path, help='Path to the top-left image')
    parser.add_argument('-tr', '--top-right', type=Path, help='Path to the top-right image')
    parser.add_argument('-bl', '--bottom-left', type=Path, help='Path to the bottom-left image')
    parser.add_argument('-br', '--bottom-right', type=Path, help='Path to the bottom-right image')
    parser.add_argument('-o', '--output', type=Path, help='Name of the new texture')
    #
    args = parser.parse_args()
    if any([args.top_left, args.top_right, args.bottom_left, args.bottom_right, args.output]):
        path_list = [args.top_left,args.top_right,args.bottom_left,args.bottom_right]
        pack_textures(args.size,path_list,args.output)
    else:
        main()
    
    

