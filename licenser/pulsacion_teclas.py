import curses

def main(stdscr):
    # Configurar la pantalla
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    # Mostrar un mensaje en la pantalla
    stdscr.addstr(0, 0, "Presione una tecla para ver su código...")
    stdscr.refresh()

    while True:
        # Leer la tecla presionada
        c = stdscr.getch()

        # Mostrar el código de la tecla presionada
        stdscr.addstr(1, 0, f"Código de la tecla: {c}")
        stdscr.refresh()

        # Terminar la ejecución del programa si se presiona la tecla q
        if c == ord('q'):
            break

    # Restaurar la pantalla
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)

# Inicializar la pantalla y ejecutar la función main
curses.wrapper(main)