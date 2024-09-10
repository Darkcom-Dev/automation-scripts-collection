#!/usr/bin/env python3
# -*-coding=UTF-8-*-

import argparse
import pytesseract
from PIL import Image

def main(path, binarize=False, invert=False):

    # Carga la imagen desde la que deseas extraer texto
    img = Image.open(path)
    if binarize:
        img = img.convert('1')
    if invert:
        img = img.point(lambda x: 255 if x == 0 else 0)

    # Utiliza pytesseract para realizar el OCR en la imagen
    text = pytesseract.image_to_string(img)

    # Sufijo
    sufijo = '_output.txt'
    sufijo = '_binarized' + sufijo if binarize else sufijo
    sufijo = '_inverted' + sufijo if invert else sufijo
    # Guarda el texto extraido
    with open(path+sufijo, 'w') as f:
        f.write(text)

def info():
    print('Img2Text', __version__)
    print('pytesseract', pytesseract.get_tesseract_version())
    print('pytesseract-languages', pytesseract.get_languages())
    print('pillow', Image.__version__)
    print('argparse', argparse.__version__)

if __name__ == "__main__":
    __version__ = '0.0.1'   
    parser = argparse.ArgumentParser(description='image to text ocr: Use white background and black text binarized images')
    parser.add_argument('path', type=str, help='Path to image')
    parser.add_argument('--binarize', action='store_true', help='Binarize image')
    parser.add_argument('--invert', action='store_true', help='Invert image')
    parser.add_argument('--info', action='store_true', help='Print info')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()
    if args.info:
        info()
    else:
        main(args.path, args.binarize, args.invert)