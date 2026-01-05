#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
import argparse
import os


def swap_channels(image, channel_from, channel_to):
    """
    Intercambia dos canales de una imagen.
    
    :param image: Objeto de la imagen cargada (Pillow Image).
    :param channel_from: Índice del canal de origen (0=R, 1=G, 2=B, 3=A si está presente).
    :param channel_to: Índice del canal de destino.
    :return: Imagen con los canales intercambiados.
    """
    # Separar los canales
    channels = list(image.split())

    # Intercambiar los canales
    channels[channel_from], channels[channel_to] = channels[channel_to], channels[channel_from]

    # Combinar los canales de nuevo
    return Image.merge(image.mode, channels)


def main(input_file, output_file, from_channel, to_channel):
    try:
        # Cargar la imagen
        img = Image.open(input_file).convert("RGBA")  # Aseguramos que tenga canales RGBA

        # Intercambiar los canales
        swapped_img = swap_channels(img, from_channel, to_channel)

        # Guardar la nueva imagen
        swapped_img.save(output_file, "PNG")
        print(f"Imagen guardada en: {output_file}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Intercambia dos canales de una textura PNG y guarda un nuevo archivo.")
    parser.add_argument("input_file", help="Ruta de la textura de entrada (.png)")
    parser.add_argument("output_file", help="Ruta para guardar la textura resultante (.png)")
    parser.add_argument(
        "from_channel",
        type=int,
        choices=[0, 1, 2, 3],
        help="Canal de origen (0=Rojo, 1=Verde, 2=Azul, 3=Alfa)"
    )
    parser.add_argument(
        "to_channel",
        type=int,
        choices=[0, 1, 2, 3],
        help="Canal de destino (0=Rojo, 1=Verde, 2=Azul, 3=Alfa)"
    )
    args = parser.parse_args()

    # Validar si los canales son diferentes
    if args.from_channel == args.to_channel:
        print("Los canales de origen y destino deben ser diferentes.")
    else:
        main(args.input_file, args.output_file, args.from_channel, args.to_channel)
