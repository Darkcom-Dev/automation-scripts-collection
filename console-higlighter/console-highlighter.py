import re


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

    reservadas = ['elif ', 'if ', 'else:', 'while ', 'for ', 'def ', 'class ', 'try ', 'except ', 'finally:', 'return ']

    for patron, reemplazo in formatos:
        text = re.sub(patron, reemplazo, text)

    for palabra in reservadas:
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

def main():
    
    text2 = '''
    # Esto es un titulo

    esto es un ** texto en negrita ** y continua el texto con 
    *texto en cursiva * y luego continua el texto con `código`
    Agreguemos otro ** texto en negrita ** y * texto en cursiva * y
    otro ` texto en codigo`. A continuacion ~~ texto en tachado ~~ y luego
    una línea nueva

    - lista no numerada
    - lista numerada

    1. lista numerada
    2. lista numerada
    3. lista numerada

    ## Subtitulo

    por cierto me falto un __texto en subrayado__
        texto tabulado
    '''

    text = """
        # Esto es un comentario
        ''' Esto es un comentario '''
        'Esto es un string'

        elif True:
            print('hola')
        else:
            print('adios')

        if else: elif for while class try except return finally: def 
    """

    mark = markdown(text2)
    python_result = python(text)
    print(mark)
    print(python_result)

    return 0

if __name__ == '__main__':
    main()