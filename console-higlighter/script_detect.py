#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os

def is_in_path(executable_name):
    # Obtener el valor de la variable de entorno PATH
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    
    # Iterar sobre cada directorio en PATH
    for directory in path_dirs:
        # Crear la ruta completa al archivo ejecutable
        executable_path = os.path.join(directory, executable_name)
        
        # Verificar si el archivo existe y es ejecutable
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return True
    
    return False

# Ejemplo de uso
executable_name = 'python3'  # Cambia por el nombre del archivo que quieres verificar
if is_in_path(executable_name):
    print(f"{executable_name} se encuentra en $PATH")
else:
    print(f"{executable_name} no se encuentra en $PATH")
