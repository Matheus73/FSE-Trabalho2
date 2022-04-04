import curses
from playsound import playsound

def play_alarme():
    playsound('alarme.mp3')

def define_on_off(value):
    if value:
        return "Ligado(a)"
    else:
        return "Desligado(a)"

def define_aberto_fechado(value):
    if value:
        return "Aberto(a)"
    else:
        return "Fechado(a)"

def clear_menu(stdscr):

    stdscr.addstr(6,0, f"Alarme:                                         ")
    stdscr.addstr(7,0, f"Ocupação Total:                 ")

    stdscr.addstr(9,0, f"ANDAR:                        ", curses.A_BOLD)
    stdscr.addstr(10,0, f"Temperatura:                               ")
    stdscr.addstr(11,0, f"Umidade:                            ")
    stdscr.addstr(12,0, f"Ocupação:                            ")
    stdscr.addstr(13,0, f"Lampada T01:                                           ")
    stdscr.addstr(14,0, f"Lampada T02:                                           ")
    stdscr.addstr(15,0, f"Lampada Corredor:                                           ")
    stdscr.addstr(16,0, f"Ar-condicionado:                                                 ")
    stdscr.addstr(17,0, f"Aspersor:                                           ")
    stdscr.addstr(18,0, f"Janela T01:                                          ")
    stdscr.addstr(19,0, f"Janela T02:                                          ")
    stdscr.addstr(20,0, f"Porta:                                        ")
    stdscr.addstr(21,0, f"Fumaça:                                         ")

    stdscr.addstr(23,0, f"ANDAR:                        ", curses.A_BOLD)
    stdscr.addstr(24,0, f"Temperatura:                               ")
    stdscr.addstr(25,0, f"Umidade:                            ")
    stdscr.addstr(26,0, f"Ocupação:                            ")
    stdscr.addstr(27,0, f"Lampada 101:                                           ")
    stdscr.addstr(28,0, f"Lampada 102:                                           ")
    stdscr.addstr(29,0, f"Lampada Corredor:                                           ")
    stdscr.addstr(30,0, f"Ar-condicionado:                                                 ")
    stdscr.addstr(31,0, f"Janela 101:                                          ")
    stdscr.addstr(32,0, f"Janela 102:                                          ")
    stdscr.addstr(33,0, f"Fumaça:                                         ")
    stdscr.noutrefresh()
    curses.doupdate()

def append_log_file(value: str):
    with open("log.csv", "a") as f:
        f.write(value + "\n")
