import curses

# Definición de las opciones del menú principal y submenús
options = ['Software', 'Media', 'Documento', 'Fuente', 'Hardware', 'Mix', 'Salir']
software_licenses = ['GNU Affero General Public License', 'GNU General Public License', 'GNU Lesser General Public License', 'Mozilla Public License', 'Apache License', 'MIT License', 'Boost Software License', 'Unlicense']
hardware_licenses = ['CERN Open Hardware License - Permisive', 'CERN Open Hardware License - Weakly Reciprocal', 'CERN Open Hardware License - Strongly Reciprocal']
fonts_licenses = ['SIL Open Font License', 'Others']
media_licenses = ['Creative Commons 0', 'Creative Commons By Attribution', 'Creative Commons By ShareAlike', 'Others']

# Submenús
submenus = {
    'Software': software_licenses,
    'Hardware': hardware_licenses,
    'Fuente': fonts_licenses,
    'Media': media_licenses
}

def print_menu(stdscr, current_option_idx, options):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()

    # Mostrar opciones del menú
    for idx, row in enumerate(options):
        x = max_x // 2 - len(row) // 2
        y = max_y // 2 - len(options) // 2 + idx
        if idx == current_option_idx:
            stdscr.addstr(y, x, row, curses.A_REVERSE)  # Opción seleccionada en reversa
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def menu_principal(stdscr):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)



    current_option_idx = 0  # Índice de la opción seleccionada en el menú principal

    while True:
        print_menu(stdscr, current_option_idx, options)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_option_idx > 0:
            current_option_idx -= 1
        elif key == curses.KEY_DOWN and current_option_idx < len(options) - 1:
            current_option_idx += 1
        elif key == ord('\n'):  # Enter
            selected_option = options[current_option_idx]
            if selected_option == 'Salir':
                break  # Salir del programa
            elif selected_option in submenus:
                submenu(stdscr, submenus[selected_option])  # Mostrar submenú

    # Restaurar estado de la terminal
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def submenu(stdscr, submenu_options):
    generic_submenu = ['Crear archivo de licencia', 'Ver licencia']
    # Submenús
    submenus = {
        'GNU Affero General Public License': generic_submenu, 
        'GNU General Public License': generic_submenu, 
        'GNU Lesser General Public License': generic_submenu, 
        'Mozilla Public License': generic_submenu, 
        'Apache License': generic_submenu, 
        'MIT License': generic_submenu, 
        'Boost Software License': generic_submenu,
        'Unlicense': generic_submenu,
        'CERN Open Hardware License - Permisive': generic_submenu,
        'CERN Open Hardware License - Weakly Reciprocal': generic_submenu,
        'CERN Open Hardware License - Strongly Reciprocal': generic_submenu,
        'SIL Open Font License': generic_submenu,
        'Others': generic_submenu,
        'Creative Commons 0':generic_submenu, 
        'Creative Commons By Attribution': generic_submenu,
        'Creative Commons By ShareAlike': generic_submenu, 
        'Others':generic_submenu
    }

    license_features = {
        'GNU Affero General Public License': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Patent use', 'Private use'],
            'conditions':['Disclosure source', 'License and copyright notice', 'Network use is distribution', 'Same license', 'State changes'],
            'limitations': ['Liability', 'Warranty']
            }, 
        'GNU General Public License': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Patent use', 'Private use'],
            'conditions':['Disclosure source', 'License and copyright notice', 'Same license', 'State changes'],
            'limitations': ['Liability', 'Warranty']
            }, 
        'GNU Lesser General Public License': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Patent use', 'Private use'],
            'conditions':['Disclosure source', 'License and copyright notice', 'Same license (library)', 'State changes'],
            'limitations': ['Liability', 'Warranty']
            },
        'Mozilla Public License': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Patent use', 'Private use'],
            'conditions':['Disclosure source', 'License and copyright notice', 'Same license (file)'],
            'limitations': ['Liability', 'Warranty']
            },
        'Apache License': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Patent use', 'Private use'],
            'conditions':['License and copyright notice', 'State changes'],
            'limitations': ['Liability', 'Warranty', 'Trademark use']
            },
        'MIT License': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Private use'],
            'conditions':['License and copyright notice'],
            'limitations': ['Liability', 'Warranty']
            },
        'Boost Software License': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Private use'],
            'conditions':['License and copyright notice'],
            'limitations': ['Liability', 'Warranty']
            },
        'Unlicense': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Private use'],
            'conditions':['No conditions'],
            'limitations': ['Liability', 'Warranty']
            },
        'CERN Open Hardware License - Permisive': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Patent use', 'Private use'],
            'conditions':['License and copyright notice', 'State changes'],
            'limitations': ['Liability', 'Warranty']
            },
        'CERN Open Hardware License - Weakly Reciprocal': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Patent use', 'Private use'],
            'conditions':['Disclosure source','License and copyright notice', 'Same license (library)', 'State changes'],
            'limitations': ['Liability', 'Warranty']
            },
        'CERN Open Hardware License - Strongly Reciprocal': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Patent use', 'Private use'],
            'conditions':['Disclosure source', 'License and copyright notice', 'Same license', 'State changes'],
            'limitations': ['Liability', 'Warranty']
            },
        'SIL Open Font License': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Private use'],
            'conditions':['License and copyright notice', 'Same license'],
            'limitations': ['Liability', 'Warranty']
            },
        'Others': None,
        'Creative Commons 0':{
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Private use'],
            'conditions':['No conditions'],
            'limitations': ['Liability', 'Warranty']
            }, 
        'Creative Commons By Attribution': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Private use'],
            'conditions':['License and copyright notice', 'State changes'],
            'limitations': ['Liability', 'Warranty']
            },
        'Creative Commons By ShareAlike': {
            'permissions':['Comercial use', 'Distribution', 'Modification', 'Private use'],
            'conditions':['License and copyright notice', 'Same license', 'State changes'],
            'limitations': ['Liability', 'Warranty', 'Trademark use', 'Patent use']
            },
        'Others':None
    }

    current_option_idx = 0

    while True:
        print_menu(stdscr, current_option_idx, submenu_options + ['Volver'])

        key = stdscr.getch()

        if key == curses.KEY_UP and current_option_idx > 0:
            current_option_idx -= 1
        elif key == curses.KEY_DOWN and current_option_idx < len(submenu_options):
            current_option_idx += 1
        elif key == ord('\n'):  # Enter
            if current_option_idx == len(submenu_options):
                break  # Regresar al menú principal
            else:
                # Acción al seleccionar una licencia (puedes agregar más lógica aquí)
                submenu2(stdscr, submenus[submenu_options[current_option_idx]])
                stdscr.refresh()
                stdscr.getch()

        # Mostrar las caracteristicas de la licencia seleccionada
        stdscr.addstr(3, 0, f'Licencia seleccionada: {submenu_options[current_option_idx]}')



def submenu2(stdscr, submenu_options):
    current_option_idx = 0

    while True:
        print_menu(stdscr, current_option_idx, submenu_options + ['Volver'])

        key = stdscr.getch()

        if key == curses.KEY_UP and current_option_idx > 0:
            current_option_idx -= 1
        elif key == curses.KEY_DOWN and current_option_idx < len(submenu_options):
            current_option_idx += 1
        elif key == ord('\n'):  # Enter
            if current_option_idx == len(submenu_options):
                break  # Regresar al menú principal
            elif submenu_options[current_option_idx] == 'Crear archivo de licencia':
                # Crear archivo de licencia
                create_license(stdscr)
                stdscr.addstr(0, 0, 'Se ha creado el archivo de licencia')
                stdscr.refresh()
                stdscr.getch()
            elif submenu_options[current_option_idx] == 'Ver licencia':
                # Ver licencia
                view_license(stdscr)
                stdscr.addstr(0, 0, license)
                stdscr.refresh()
                stdscr.getch()
            else:
                # Acción al seleccionar una licencia (puedes agregar más lógica aquí)
                stdscr.addstr(0, 0, f"Seleccionaste: {submenu_options[current_option_idx]}")
                stdscr.refresh()
                stdscr.getch()

def view_license(stdscr):
    with open('license.txt', 'r') as f:
        license = f.read()
    stdscr.addstr(0, 0, license)
    stdscr.refresh()
    stdscr.getch()

def create_license(stdscr):
    license = """
Este es un texto de supuesta licencia.
Mas adelante hago una integracion en forma.
"""
    with open('license.txt', 'w') as f:
        f.write(license)
    stdscr.addstr(0, 0, 'Se ha creado el archivo de licencia')
    stdscr.refresh()
    stdscr.getch()
# Inicializar curses
curses.wrapper(menu_principal)
