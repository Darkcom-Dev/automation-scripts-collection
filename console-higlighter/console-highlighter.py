#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import subprocess
import os
import argparse

def python(text):
    """
    Applies various formatting styles to the given text using regular expressions.
    
    Parameters:
        text (str): The text to be formatted.
    
    Returns:
        str: The formatted text.
    """
    formatos = [
        (r'\"\"\"(.*?)\"\"\"', '\"\"\"\x1b[90m\\1\"\"\"\x1b[0m'),  # comentario
        (r"\'\'\'(.*?)\'\'\'", "\'\'\'\x1b[90m\\1\'\'\'\x1b[0m"),  # comentario
        (r'\"(.*?)\"', '\"\x1b[92m\\1\"\x1b[0m'),  # strings
        (r"\'(.*?)\'", '\'\x1b[32m\\1\'\x1b[0m'),  # strings
        (r'\n# (.*?)', '\n# \x1b[90m\\1\n\x1b[0m'),  # Comentario

    ]

    # reservadas = 

    for patron, reemplazo in formatos:
        text = re.sub(patron, reemplazo, text)

    for palabra in ['elif ', 'if ', 'else:', 'while ', 'for ', 'def ', 'class ', 'try ', 'except ', 'finally:', 'with ', 'return ', 'from', 'import ']:
        text = text.replace(palabra, f'\x1b[1;34m{palabra}\x1b[0m')

    return text


def markdown(text):
    """
    Applies various formatting styles to the given text using regular expressions.

    Parameters:
        text (str): The text to be formatted.

    Returns:
        str: The formatted text.
    """
    formatos = [
        (r'\*\*(.*?)\*\*', '\x1b[1m\\1\x1b[0m'),  # Negrilla
        (r'\*(.*?)\*', '\x1b[3m\\1\x1b[0m'),     # Cursiva
        (r'~~(.*?)~~', '\x1b[9m\\1\x1b[0m'),     # Tachado
        (r'__(.*?)__', '\x1b[4m\\1\x1b[0m'),     # Subrayado
        (r'`(.*?)`', '\x1b[96m\\1\x1b[0m'),       # Código
        (r'`\n(.*?)`\n', '\x1b[96m\\1\x1b[0m'),       # Código
        (r'```\n(.*?)\n```', '\x1b[96m\\1\x1b[0m'),       # Código
        (r'\n## (.*?)\n', '\x1b[4;33m\\1\x1b[0m'),# SubTitulo
        (r'\n# (.*?)\n', '\x1b[1;4;93m\\1\x1b[0m'),# Titulo
        (r'\n- (.*?)\n', '\n- \x1b[96m\\1\x1b[0m\n'),       # Lista no numerada
        (r'\n1. (.*?)\n', '\n1. \x1b[96m\\1\x1b[0m\n'),     # Lista numerada
        (r'\n\t(.*?)', '\n\t\x1b[96m\\1\x1b[0m'),       # Tabula
        ]

    if type(text) == str:        

        for patron, reemplazo in formatos:
            text = re.sub(patron, reemplazo, text)

        return text
    else:
        return ("Text is not a string")

def main(path):
    """
    This function reads a file based on the provided path, 
    applies syntax highlighting if the file is a Python or Markdown file, 
    and then pipes the output to the 'less' command for viewing.

    Parameters:
        path (str): The path to the file to be read.

    Returns:
        int: The exit status of the function, which is always 0.
    """
    file_path = os.path.join(os.path.dirname(__file__), path)
    extension = os.path.splitext(file_path)[1]
    print(f'File: {file_path}')
    text = ""
    with open(file_path, 'r') as f:
        if extension == '.py':
            text = python(f.read())
        elif extension == '.md':
            text = markdown(f.read())
        else:
            text = f.read()
    
    process = subprocess.Popen(['less', '-R'], stdin=subprocess.PIPE)
    process.communicate(input=text.encode('utf-8'))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Path to the file')
    parser.description = 'Highlighter'
    args = parser.parse_args()
    main(args.path)