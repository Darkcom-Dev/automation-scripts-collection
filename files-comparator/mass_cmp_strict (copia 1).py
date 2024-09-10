#!/usr/bin/env python3

import os
import filecmp
import subprocess

def file_comparision(file_1,file_2):
    extensions_compare = os.path.splitext(file_1)[1] == os.path.splitext(file_2)[1]
    size_compare = os.path.getsize(file_1) == os.path.getsize(file_2)
    binary_compare = filecmp.cmp(file_1, file_2)
    return extensions_compare and size_compare and binary_compare
    
def main():
    # obtener el directorio actual
    file_list = os.listdir()

    if len(file_list) == 0:
        print("No hay archivos en el directorio actual")
        exit()
    elif len(file_list) == 1:
        print("Solo hay un archivo en el directorio actual")
        exit()
    else:

        for file in file_list:
            for file2 in file_list:
                if file != file2 and file_comparision(file, file2):
                    print(f'Los archivos "{file}" "{file2}" son iguales')
                
                # Aplicando el comando cmp 
                result = subprocess.run(["cmp", file, file2])
                if result.returncode == 0:
                    print(f'Los archivos "{file}" "{file2}" son iguales')

if __name__ == "__main__":
    main()
