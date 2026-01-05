#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import argparse
from PIL import Image, ImageOps
import numpy as np

def displacement_from_normal(normal_map_path, output_path):
    """
    Aproxima un mapa de desplazamiento (Displacement) desde un Normal Map.
    """
    # Abrir imagen y convertir a escala de grises
    normal_map = Image.open(normal_map_path).convert("RGB")
    width, height = normal_map.size

    # Extraer canales R y G para los gradientes
    normal_array = np.array(normal_map) / 255.0  # Normalizar valores a [0, 1]
    gradient_x = normal_array[..., 0]  # Canal R (x)
    gradient_y = normal_array[..., 1]  # Canal G (y)

    # Integrar gradientes para obtener alturas aproximadas
    displacement = np.zeros_like(gradient_x)
    for y in range(1, height):
        for x in range(1, width):
            displacement[y, x] = displacement[y - 1, x] + gradient_y[y, x]
            displacement[y, x] += displacement[y, x - 1] + gradient_x[y, x]

    # Normalizar el mapa de desplazamiento
    displacement = (displacement - np.min(displacement)) / (np.max(displacement) - np.min(displacement)) * 255
    displacement_map = Image.fromarray(displacement.astype(np.uint8))

    # Guardar resultado
    displacement_map.save(output_path)
    print(f"Displacement Map generado y guardado en: {output_path}")

def normal_from_displacement(displacement_map_path, output_path, scale=1.0):
    """
    Genera un Normal Map desde un mapa de desplazamiento (Displacement).
    """
    # Abrir imagen y convertir a escala de grises
    displacement_map = Image.open(displacement_map_path).convert("L")
    displacement_array = np.array(displacement_map, dtype=np.float32)

    # Calcular gradientes
    gradient_x = np.gradient(displacement_array, axis=1) * scale
    gradient_y = np.gradient(displacement_array, axis=0) * scale

    # Normalizar gradientes para construir Normal Map
    normal_map = np.zeros((*displacement_array.shape, 3), dtype=np.float32)
    normal_map[..., 0] = gradient_x
    normal_map[..., 1] = gradient_y
    normal_map[..., 2] = 1.0  # Z fijo

    # Normalizar vectores a [0, 1]
    length = np.sqrt(np.sum(normal_map**2, axis=-1, keepdims=True))
    normal_map /= length
    normal_map = (normal_map + 1.0) / 2.0 * 255  # Escalar a [0, 255]

    normal_map_image = Image.fromarray(normal_map.astype(np.uint8))
    normal_map_image.save(output_path)
    print(f"Normal Map generado y guardado en: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conversor entre Normal Map y Displacement Map.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando para convertir Normal a Displacement
    normal_to_disp = subparsers.add_parser("to_displacement", help="Convertir Normal Map a Displacement Map")
    normal_to_disp.add_argument("input", help="Ruta del archivo de Normal Map de entrada")
    normal_to_disp.add_argument("output", help="Ruta del archivo de Displacement Map de salida")

    # Subcomando para convertir Displacement a Normal
    disp_to_normal = subparsers.add_parser("to_normal", help="Convertir Displacement Map a Normal Map")
    disp_to_normal.add_argument("input", help="Ruta del archivo de Displacement Map de entrada")
    disp_to_normal.add_argument("output", help="Ruta del archivo de Normal Map de salida")
    disp_to_normal.add_argument("--scale", type=float, default=1.0, help="Escala de los gradientes (default: 1.0)")

    args = parser.parse_args()

    if args.command == "to_displacement":
        displacement_from_normal(args.input, args.output)
    elif args.command == "to_normal":
        normal_from_displacement(args.input, args.output, scale=args.scale)
