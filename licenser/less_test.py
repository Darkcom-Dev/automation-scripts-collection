
import curses

def mostrar_archivo(archivo):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)

    with open(archivo, 'r') as f:
        contenido = f.readlines()
    
    pagina = 0
    while True:
        stdscr.clear()

        # Obtener el tamaño actual de la ventana
        max_y, max_x = stdscr.getmaxyx()

        # Mostrar el contenido del archivo
        for i in range(min(curses.LINES - 1, max_y - 1)):
            try:
                if pagina * (curses.LINES - 1) + i < len(contenido):
                    # Recortar la línea si es más larga que la anchura de la ventana
                    linea = contenido[pagina * (curses.LINES - 1) + i].rstrip()
                    stdscr.addstr(i, 0, linea[:max_x - 1])
            except curses.error:
                pass  # Ignorar cualquier error si intentamos dibujar fuera de los límites

        # Mostrar el número de página
        try:
            stdscr.addstr(max_y - 1, 0, f"Página {pagina + 1}/{(len(contenido) + curses.LINES - 2) // (curses.LINES - 1)}")
        except curses.error:
            pass  # Ignorar si no puede mostrar el número de página

        stdscr.refresh()

        c = stdscr.getch()

        if (c == curses.KEY_UP or c == curses.KEY_PPAGE) and pagina > 0:
            pagina -= 1
        elif (c == curses.KEY_DOWN or c == curses.KEY_NPAGE) and pagina < (len(contenido) + curses.LINES - 2) // (curses.LINES - 1):
            pagina += 1
        elif c == ord('q'):
            break

    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()

archivo = 'readme.txt'
mostrar_archivo(archivo)
