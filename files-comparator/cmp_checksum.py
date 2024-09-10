#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib

def calcular_checksum(file_path, algorithm='sha256'):
    """
    Calcula el checksum de un archivo.
    
    Args:
    file_path (str): Ruta al archivo.
    algorithm (str): Algoritmo de hash (por defecto 'sha256').
    
    Returns:
    str: Checksum del archivo.
    """
    hasher = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def comparar_archivos(file1, file2):
    """
    Compara los checksums de dos archivos.
    
    Args:
    file1 (str): Ruta al primer archivo.
    file2 (str): Ruta al segundo archivo.
    
    Returns:
    bool: True si los checksums son iguales, False de lo contrario.
    """
    checksum1 = calcular_checksum(file1)
    checksum2 = calcular_checksum(file2)
    return checksum1 == checksum2

# Ejemplo de uso
archivo1 = 'archivo1.txt'
archivo2 = 'archivo2.txt'

if comparar_archivos(archivo1, archivo2):
    print("Los archivos son iguales.")
else:
    print("Los archivos son diferentes.")
