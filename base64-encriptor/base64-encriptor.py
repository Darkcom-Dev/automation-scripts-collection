import base64

# Hacer uso de argparse
# Ampliar a la posibilidad de encriptar y desencriptar archivos de texto

def encriptar_comando(command):
    return base64.b64encode(command.encode("utf-8"))

def ejecutar_comando(command):
    exec(base64.b64decode(command).decode("utf-8"))

def main():

    message = '''
    ¿Qué deseas hacer?
    1. Encriptar comando
    2. Ejecutar comando encriptado
'''

    print(message)
    menu_input = int(input("Ingresa una opción: "))

    if menu_input == 1:
        command = input("Comando a encriptar: ")
        print(encriptar_comando(command))
    
    else:
        command = input("Comando encriptado: ")
        print(ejecutar_comando(command))


if __name__ == "__main__":
    main()

