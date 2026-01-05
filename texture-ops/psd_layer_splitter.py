#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from psd_tools import PSDImage
import argparse
import os


def save_layer(layer, output_dir, index):
    """Guarda una capa en un archivo PNG."""
    if layer.visible:
        layer_image = layer.composite()
        if layer_image:
            # Generar un nombre válido para el archivo
            layer_name = layer.name.replace(' ', '_').replace('/', '_') or f"layer_{index}"
            output_file = os.path.join(output_dir, f"{layer_name}.png")
            layer_image.save(output_file)
            print(f"Capa guardada: {output_file}")


def process_layers(layers, output_dir, index=0):
    """Procesa las capas recursivamente."""
    for layer in layers:
        if layer.is_group():
            # Si es un grupo, procesar recursivamente
            process_layers(layer, output_dir, index)
        else:
            save_layer(layer, output_dir, index)
            index += 1
    return index


def main(filename: str, output_dir: str):
    try:
        # Cargar el archivo PSD
        psd = PSDImage.open(filename)

        # Crear directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)

        # Procesar las capas
        process_layers(psd, output_dir)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split PSD layers into individual PNG files")
    parser.add_argument("filename", help="Path to the PSD file")
    parser.add_argument(
        "-o", "--output", default="output", help="Directory to save the PNG files"
    )
    args = parser.parse_args()
    main(args.filename, args.output)
