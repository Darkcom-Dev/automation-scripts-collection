#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import argparse


import re

def clean_name(name):
    """
    Removes leading and trailing whitespace from a filename, and removes spaces, 
    underscores, and hyphens before the file extension.

    Parameters:
        name (str): The filename to be cleaned.

    Returns:
        str: The cleaned filename.
    """
    # Elimina los espacios al inicio y al final del nombre
    name = name.strip()
    # Elimina los espacios, guiones bajos y guiones antes de la extension
    name = name.replace(' .', '.').replace('_.', '.').replace('-.', '.')
    return name

def camel_to_kebab(name):
    """
    Converts a camelCase filename to kebab-case.

    Args:
        name (str): The camelCase filename.

    Returns:
        str: The kebab-case filename.
    """    
    # Buscar las transiciones de camelCase y separarlas con un guion
    kebab_case_name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    # Convertir a minúsculas
    return kebab_case_name.lower()


def normalize_name(name, snake_case=False):
    """
    Normalizes a given name by replacing spaces and dashes with underscores,
    and optionally converts the name to snake_case.

    Parameters:
        name (str): The name to be normalized.
        snake_case (bool, optional): If True, the name will be converted to snake_case.
                                    Defaults to False.

    Returns:
        str: The normalized name.
    """
    # Reemplazar espacios y guiones por guiones bajos
    
    if snake_case:
        name = name.replace(' ', '_').replace('-', '_')
        # Limpieza de dobles guiones bajos
        name = re.sub(r'__+', '_', name)
    else:
        name = name.replace(' ', '-').replace('_', '-')
        # Limpieza de dobles guiones medios
        name = re.sub(r'-+', '-', name)
    # Convertir a minúsculas
    return name.lower()

def rename_if_necessary(original_path, new_path, item_type):
    """
    Renames a file or directory if its name does not match a specified convention.

    Args:
        original_path (str): The current path of the file or directory.
        new_path (str): The desired path of the file or directory.
        item_type (str): The type of item being renamed (e.g. file, directory).

    Returns:
        None
    """
    if original_path == new_path:
        print(f'El {item_type}: \033[33m{original_path}\033[0m ya cumple con la convención')
    else:
        if os.path.exists(new_path):
            print(f'El {item_type}: {new_path} \033[41mya existe\033[0m. No se renombrará.')
        else:
            os.rename(original_path, new_path)
            print(f'\033[42mRenombrado {item_type}\033[0m: {original_path} -> \033[1m{new_path}\033[0m')

def generate_new_name(original_name, snake_case_extensions=None):
    """
    Generates a new name based on the provided original name, following specific conventions.

    Args:
        original_name (str): The original name to be converted.
        snake_case_extensions (tuple, optional): A tuple of extensions that should be converted to snake case. Defaults to None.

    Returns:
        str: The new name following the specified conventions.
    """
    original_name = clean_name(original_name)
    original_name = camel_to_kebab(original_name)

    if snake_case_extensions and original_name.endswith(tuple(snake_case_extensions)):
        return normalize_name(original_name, snake_case=True)
    else:
        return normalize_name(original_name)


def rename_files_and_folders(directory):
    """Renombra archivos y carpetas en el directorio especificado."""

    # Extensiones de archivo que se renombran con snake_case
    snake_case_extensions = [
        '.py', '.c', '.cpp', '.h', '.js', '.jsx', '.sh', '.rb', '.php',
        '.json', '.toml', '.yml', '.yaml', '.conf', '.cfg', '.mk',
        '.txt', '.csv', '.tsv', '.sql', '.jinja', '.tpl', '.md'
    ]

    # Archivos que no se renombran
    ignore_files = [
        '.DS_Store', 'Thumbs.db', '__MACOSX', 'README.md', '.gitignore',
        '.gitattributes', '__init__.py', '__main__.py', '.env', '.envrc',
        'requirements.txt', 'setup.py', 'Pipfile', 'Pipfile.lock',
        'pyproject.toml', 'LICENSE', 'README.md', 'README.rst'
    ]

    # Directorios que no se renombran
    ignore_directories = [
        '.git', '.github', '.vscode', '.idea', '.mypy_cache',
        '.pytest_cache', '__pycache__', '__cache__', 'venv', 'env',
        'node_modules'
    ]

    for root, dirs, files in os.walk(directory, topdown=False):
        for file_name in files:
            if file_name in ignore_files:
                print(f'\033[43mIgnorando archivo\033[0m: {file_name} por estar en la lista de ignorados')
                continue

            original_file_path = os.path.join(root, file_name)
            new_file_name = generate_new_name(file_name, snake_case_extensions)
            new_file_path = os.path.join(root, new_file_name)

            rename_if_necessary(original_file_path, new_file_path, 'archivo')

        for dir_name in dirs:
            if dir_name in ignore_directories:
                print(f'\033[43mIgnorando carpeta\033[0m: \033[31m{dir_name}\033[0m por estar en la lista de directorios ignorados')
                continue

            original_dir_path = os.path.join(root, dir_name)
            new_dir_name = generate_new_name(dir_name)
            new_dir_path = os.path.join(root, new_dir_name)

            rename_if_necessary(original_dir_path, new_dir_path, 'carpeta')

if __name__ == "__main__":
    # Especifica el directorio que deseas renombrar
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Directorio que deseas renombrar")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"El directorio {args.directory} no existe.")
        exit(1)
    else:
        rename_files_and_folders(args.directory)

"""
project_convention_renamer.py version 1.1

Este script renombra los archivos y carpetas en un directorio especificado, convirtiendo los nombres de archivos y carpetas en formato camelCase a kebab-case segun la convención establecida.
- Los nombres de archivos y carpetas no deben empezar o terminar con espacios.
- Los nombres de archivos y carpetas no deben contener doble guion bajo o doble guion entre los espacios.
- Los nombres de carpetas deben ser kebab-case excepto aquellos que estan en la lista de ignorados.
- Los nombres de archivos que sean parte de un módulo o libreria deben ser snake_case excepto aquellos que estan en la lista de ignorados.
- Los nombres de archivos comunes como imágenes, documentos, audios, videos, etc. deben ser kebab-case excepto aquellos que estan en la lista de ignorados.

Ejemplo de uso:
    python project_convention_renamer.py "/path/to/directory"
    ./project_convention_renamer.py "/path/to/directory"

Para ejecutarlo, asegúrate de tener el archivo project_convention_renamer.py en la misma carpeta que el script o que el script se encuentre en una carpeta incluida dentro de las variables de entorno.

- En caso de que el directorio no exista, el script muestra un mensaje de error y termina.
- En caso de que el nombre directorio al ser comparado con un directorio que ya tiene el mismo nombre, no será renombrado y envia una advertencia.
- En caso que el nombre de archivo o directorio inicialmente cumpla con la convención, no se renombra y envia una advertencia.
- En caso que el nombre de archivo o directorio inicialmente se encuentre dentro de las listas de ignoraos, no se renombra y envia una advertencia.

Ejemplo de salida:
    Renombrado archivo: /path/to/directory/CamelCaseFile.txt -> /path/to/directory/camel-case-file.txt
    Renombrado archivo: /path/to/directory/AnotherExample.txt -> /path/to/directory/another-example.txt
    Renombrada carpeta: /path/to/directory/CamelCaseFolder -> /path/to/directory/camel-case-folder
    Renombrada carpeta: /path/to/directory/AnotherExampleFolder -> /path/to/directory/another-example-folder

# Problemas conocidos:
- Supongamos el nombre de los siguientes archivos: Carpeta 1, carpeta_1. Al renombrarse ambos nombres se convierten en carpeta-1.
- Supongase un nombre que inicie con espacios. ej: ' Archivo 1 .txt' se renombra a 'archivo_1_.txt'. el espacio antes de la extension debe ser eliminado.
- Si el nombre del archivo tiene sus espacios separados con '+', lo toma como un archivo que cumple con la convencion. Ej: 'archivo+1.txt' deberia renombrarse a 'archivo_1.txt'.
"""