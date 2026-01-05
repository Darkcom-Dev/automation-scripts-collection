#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import argparse
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, Entry, Label, Button
import os

def split_channels(image_path, red_file, green_file, blue_file, alpha_file):
    try:
        # Open the image
        image = Image.open(image_path)
        # Split the channels
        r, g, b, a = image.split()

        # Save the channels as grayscale images
        if red_file:
            r.save(red_file)
        if green_file:
            g.save(green_file)
        if blue_file:
            b.save(blue_file)
        if alpha_file and a:  # Save alpha channel if it exists
            a.save(alpha_file)

        # Get the directory where the files were saved
        output_dir = os.path.dirname(image_path)
        return output_dir
    except Exception as e:
        print(f"Error processing the image: {e}")
        return None

def gui_interface():
    def select_image():
        image_path = filedialog.askopenfilename(filetypes=[('Texture files', '*.png *.tif *.jpg *.jpeg'), ('All files', '*.*')])
        if image_path:
            entry_path.delete(0, tk.END)
            entry_path.insert(0, image_path)

    def process_image():
        image_path = entry_path.get()
        red_file = entry_red.get()
        green_file = entry_green.get()
        blue_file = entry_blue.get()
        alpha_file = entry_alpha.get()

        if not image_path:
            messagebox.showerror("Error", "You must select an image.")
            return

        # Ensure filenames have .png extension
        if red_file and not red_file.endswith(".png"):
            red_file += ".png"
        if green_file and not green_file.endswith(".png"):
            green_file += ".png"
        if blue_file and not blue_file.endswith(".png"):
            blue_file += ".png"
        if alpha_file and not alpha_file.endswith(".png"):
            alpha_file += ".png"

        output_dir = split_channels(image_path, red_file, green_file, blue_file, alpha_file)
        if output_dir:
            messagebox.showinfo("Success", f"Channels split and saved successfully in: {output_dir}")

    # Create the tkinter window
    window = tk.Tk()
    window.title("RGBA Channel Splitter")

    # Labels and text entries
    Label(window, text="Image path:").grid(row=0, column=0, padx=5, pady=5)
    entry_path = Entry(window, width=50)
    entry_path.grid(row=0, column=1, padx=5, pady=5)
    Button(window, text="Browse", command=select_image).grid(row=0, column=2, padx=5, pady=5)

    Label(window, text="Red channel file name:").grid(row=1, column=0, padx=5, pady=5)
    entry_red = Entry(window, width=50)
    entry_red.grid(row=1, column=1, padx=5, pady=5)

    Label(window, text="Green channel file name:").grid(row=2, column=0, padx=5, pady=5)
    entry_green = Entry(window, width=50)
    entry_green.grid(row=2, column=1, padx=5, pady=5)

    Label(window, text="Blue channel file name:").grid(row=3, column=0, padx=5, pady=5)
    entry_blue = Entry(window, width=50)
    entry_blue.grid(row=3, column=1, padx=5, pady=5)

    Label(window, text="Alpha channel file name:").grid(row=4, column=0, padx=5, pady=5)
    entry_alpha = Entry(window, width=50)
    entry_alpha.grid(row=4, column=1, padx=5, pady=5)

    # Button to process the image
    Button(window, text="Split Channels", command=process_image).grid(row=5, column=1, padx=5, pady=10)

    window.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Split RGBA channels from an image.")
    parser.add_argument("-i", "--image", help="Path to the texture to split channels", required=False)
    parser.add_argument("-r", "--red", help="File name for the Red channel", required=False)
    parser.add_argument("-g", "--green", help="File name for the Green channel", required=False)
    parser.add_argument("-b", "--blue", help="File name for the Blue channel", required=False)
    parser.add_argument("-a", "--alpha", help="File name for the Alpha channel", required=False)

    args = parser.parse_args()

    if args.image:
        # Command-line mode
        output_dir = split_channels(args.image, args.red, args.green, args.blue, args.alpha)
        if output_dir:
            print(f"Channels split and saved successfully in: {output_dir}")
    else:
        # GUI mode
        gui_interface()

if __name__ == "__main__":
    main()