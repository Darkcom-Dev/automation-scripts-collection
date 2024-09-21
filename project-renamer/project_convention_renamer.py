#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import argparse
import unicodedata
from urllib.parse import quote
import re

def remove_accents(text):
    """
    Remove accents from a given text.

    Parameters:
        text (str): The input text.

    Returns:
        str: The text with accents removed.

    >>> remove_accents("Canción")
    'Cancion'
    >>> remove_accents("niño")
    'nino'
    >>> remove_accents("ùòìèàǹçạïüü")
    'uoieancaiuu'
    >>> remove_accents("áéíóúüü")
    'aeiouuu'
    """
    # Normaliza el texto para separar los caracteres con acentos de sus marcas diacríticas
    normalized_text = unicodedata.normalize('NFD', text)
    # Utiliza una expresión regular para eliminar las marcas diacríticas (acentos)
    return re.sub(r'[\u0300-\u036f]', '', normalized_text)

def clean_name(name):
    """
    Removes leading and trailing whitespace from a filename, and removes spaces, 
    underscores, and hyphens before the file extension.

    Parameters:
        name (str): The filename to be cleaned.

    Returns:
        str: The cleaned filename.

    >>> clean_name("  hello world.txt  ")
    'hello world.txt'
    >>> clean_name("hello_world.txt")
    'hello_world.txt'
    >>> clean_name("hello-world.txt")
    'hello-world.txt'
    >>> clean_name("hello*world.txt")
    'hello_world.txt'
    >>> clean_name("hello world.txt")
    'hello world.txt'
    >>> clean_name("hello+world.txt")
    'hello_world.txt'
    >>> clean_name("hello world?.txt")
    'hello world.txt'
    >>> clean_name("   ") # Esto es un fallo
    '_no_name_'
    >>> clean_name("") # Esto es un fallo
    '_no_name_'
    >>> clean_name(" hello.txt")
    'hello.txt'
    >>> clean_name("CON")
    'CON_is_not_allowed_in_windows'
    """
    # Nombres de carpetas prohibidos en Windows
    forbidden_folders = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    # Reemplaza los nombres de carpetas prohibidos con un guion bajo
    if name in forbidden_folders:
        name = name + '_is_not_allowed_in_windows'

    name = name.replace('%20', '_')
    # Define los caracteres no permitidos
    forbidden_chars = '<>:"/\\|?*+#%&{}=¨^~[]@\'` \t\n\r\f\v'
    # Reemplaza los caracteres no permitidos con un guion bajo
    for char in forbidden_chars:
        name = name.replace(char, '_')

    # name = quote(name, safe=':/')
    # Elimina los acentos
    name = remove_accents(name)
    # Elimina los espacios al inicio y al final del nombre
    name = name.strip()
    # Elimina los espacios, guiones bajos y guiones antes de la extension
    name = name.replace(' .', '.').replace('_.', '.').replace('-.', '.')
    if name == '':
        name = '_no_name_'
    return name

def camel_to_kebab(name):
    """
    Converts a camelCase filename to kebab-case.

    Args:
        name (str): The camelCase filename.

    Returns:
        str: The kebab-case filename.

    >>> camel_to_kebab("helloWorld")
    'hello-world'
    >>> camel_to_kebab("HelloWorld")
    'hello-world'
    >>> camel_to_kebab("hello_world")
    'hello_world'
    >>> camel_to_kebab("hello-world")
    'hello-world'
    >>> camel_to_kebab("helloWorld123")
    'hello-world-123'
    >>> camel_to_kebab("hello")
    'hello'
    >>> camel_to_kebab("")
    ''
    """    
    
    # Buscar las transiciones de camelCase y separarlas con un guion
    kebab_case_name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    # Busca las transiciones de letras a numeros y los separa con un guion
    kebab_case_name = re.sub(r'([a-zA-Z])([0-9])', r'\1-\2', kebab_case_name.strip())
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

    >>> normalize_name("texto con espacio", snake_case=False)
    'texto-con-espacio'
    >>> normalize_name("texto con espacio convertido a snake case", snake_case=True)
    'texto_con_espacio_convertido_a_snake_case'
    >>> normalize_name("texto-en-kebab-case", snake_case=True)
    'texto_en_kebab_case'
    >>> normalize_name("texto_con_guiones_bajos", snake_case=False)
    'texto-con-guiones-bajos'
    >>> normalize_name("texto_con_guiones_bajos_convertido_a_snake_case", snake_case=True)
    'texto_con_guiones_bajos_convertido_a_snake_case'
    >>> normalize_name("hello")
    'hello'
    >>> normalize_name("")
    ''
    >>> normalize_name("hello.txt")
    'hello.txt'
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

    >>> generate_new_name("hello world.txt", snake_case_extensions=('.py','.cpp','.rs'))
    'hello-world.txt'
    >>> generate_new_name("hello world.rs", snake_case_extensions=('.py','.cpp','.rs'))
    'hello_world.rs'
    >>> generate_new_name("hello-world-folder")
    'hello-world-folder'
    >>> generate_new_name("hello world folder")
    'hello-world-folder'
    >>> generate_new_name("")
    '-no-name-'
    """
    """
    >>> generate_new_name("hello?.txt")
    'hello_.txt'
    
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
    import doctest

    doctest.run_docstring_examples(clean_name, globals(), verbose=True)
    """ 
    # Especifica el directorio que deseas renombrar
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Directorio que deseas renombrar")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"El directorio {args.directory} no existe.")
        exit(1)
    else:
        rename_files_and_folders(args.directory) """
 
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