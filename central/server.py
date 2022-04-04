import socket
import threading

from models import Andar
from utils import clear_menu, play_alarme, define_on_off
from json_parser import set_gpio_values

from pynput import keyboard
from playsound import playsound

import time
import curses
from curses import wrapper

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 10048
ADDR = ("localhost", PORT)
FORMATO = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(ADDR)

stdscr_global = None

total_ocupacao = 0

connections = []
andares = []

def turn_off_outputs(andar: Andar, conn):
    conn.send(f"{andar.get_lampada1_gpio()}=0".encode(FORMATO))
    time.sleep(1)
    conn.send(f"{andar.get_lampada2_gpio()}=0".encode(FORMATO))
    time.sleep(1)
    conn.send(f"{andar.get_corredor_gpio()}=0".encode(FORMATO))
    time.sleep(1)
    conn.send(f"{andar.get_arcondicionado_gpio()}=0".encode(FORMATO))
    time.sleep(1)
    if(andar.get_name() == "Térreo"):
        conn.send(f"{andar.get_aspersor_gpio()}=0".encode(FORMATO))

def handle_input(key):
    if key == keyboard.Key.f1:
        andares[0].set_lampada1()
        if andares[0].get_lampada1():
            connections[0]["conn"].send(f"{andares[0].get_lampada1_gpio()}=1".encode(FORMATO))
        else:
            connections[0]["conn"].send(f"{andares[0].get_lampada1_gpio()}=0".encode(FORMATO))
        render_menu(stdscr_global)
    elif key == keyboard.Key.f2:
        andares[0].set_lampada2()
        if andares[0].get_lampada2():
            connections[0]["conn"].send(f"{andares[0].get_lampada2_gpio()}=1".encode(FORMATO))
        else:
            connections[0]["conn"].send(f"{andares[0].get_lampada2_gpio()}=0".encode(FORMATO))
        render_menu(stdscr_global)
    elif key == keyboard.Key.f3:
        andares[0].set_corredor()
        if andares[0].get_corredor():
            connections[0]["conn"].send(f"{andares[0].get_corredor_gpio()}=1".encode(FORMATO))
        else:
            connections[0]["conn"].send(f"{andares[0].get_corredor_gpio()}=0".encode(FORMATO))
        render_menu(stdscr_global)
    elif key == keyboard.Key.f4:
        andares[0].set_arcondicionado()
        if andares[0].get_arcondicionado():
            connections[0]["conn"].send(f"{andares[0].get_arcondicionado_gpio()}=1".encode(FORMATO))
        else:
            connections[0]["conn"].send(f"{andares[0].get_arcondicionado_gpio()}=0".encode(FORMATO))
        render_menu(stdscr_global)
    elif key == keyboard.Key.f5:
        andares[0].set_aspersor()
        if andares[0].get_aspersor():
            connections[0]["conn"].send(f"{andares[0].get_aspersor_gpio()}=1".encode(FORMATO))
        else:
            connections[0]["conn"].send(f"{andares[0].get_aspersor_gpio()}=0".encode(FORMATO))
        render_menu(stdscr_global)

    elif key == keyboard.Key.f6:
        andares[1].set_lampada1()
        if andares[1].get_lampada1():
            connections[1]["conn"].send(f"{andares[1].get_lampada1_gpio()}=1".encode(FORMATO))
        else:
            connections[1]["conn"].send(f"{andares[1].get_lampada1_gpio()}=0".encode(FORMATO))
        render_menu(stdscr_global)
    elif key == keyboard.Key.f7:
        andares[1].set_lampada2()
        if andares[1].get_lampada2():
            connections[1]["conn"].send(f"{andares[1].get_lampada2_gpio()}=1".encode(FORMATO))
        else:
            connections[1]["conn"].send(f"{andares[1].get_lampada2_gpio()}=0".encode(FORMATO))
        render_menu(stdscr_global)
    elif key == keyboard.Key.f8:
        andares[1].set_corredor()
        if andares[1].get_corredor():
            connections[1]["conn"].send(f"{andares[1].get_corredor_gpio()}=1".encode(FORMATO))
        else:
            connections[1]["conn"].send(f"{andares[1].get_corredor_gpio()}=0".encode(FORMATO))
        render_menu(stdscr_global)
    elif key == keyboard.Key.f9:
        andares[1].set_arcondicionado()
        if andares[1].get_arcondicionado():
            connections[1]["conn"].send(f"{andares[1].get_arcondicionado_gpio()}=1".encode(FORMATO))
        else:
            connections[1]["conn"].send(f"{andares[1].get_arcondicionado_gpio()}=0".encode(FORMATO))
        render_menu(stdscr_global)
    elif key == keyboard.Key.f10:
        andares[0].set_alarme()
        render_menu(stdscr_global)
        if andares[0].get_alarme():
            thread_sound = threading.Thread(target=play_alarme)
            thread_sound.start()

def handle_connection(conn, addr, stdscr, andar):
    global connections
    global total_ocupacao

    conn.send("start".encode(FORMATO))
    name = False

    while(True):
        msg = conn.recv(1024).decode(FORMATO)
        # render_menu(stdscr)
        if(msg):
            if(msg.startswith("name=")):
                mensagem_separada = msg.split("=")
                name = mensagem_separada[1]
                mapa_da_conexao = {
                    "conn": conn,
                    "addr": addr,
                    "nome": name,
                    "last": 0
                }
                connections.append(mapa_da_conexao)
                if "Térreo" in name:
                    andar.set_name("Térreo")
                    set_gpio_values(andar, "configuracao_andar_terreo.json")
                else:
                    set_gpio_values(andar, "configuracao_andar_1.json")
                turn_off_outputs(andar,conn)

            elif(msg.startswith("temp=")):
                try:
                    temperature = msg.split(";")[0].split("=")[1]
                    umidade = msg.split(";")[1].split("=")[1]
                    if float(temperature) != 0.0 and float(umidade) != 0.0:
                        andar.set_temperature(float(temperature))
                        andar.set_moisture(float(umidade))
                        render_menu(stdscr)
                    else:
                        pass
                except:
                    pass

            elif(msg.startswith("alarm=")):
                value = msg.split("=")[1]
                andar.set_alarme()
                render_menu(stdscr)
                if andar.get_alarme():
                    thread_sound = threading.Thread(target=play_alarme)
                    thread_sound.start()

            elif(msg.startswith("ocup=")):
                value = int(msg.split("=")[1])
                andar.set_ocupacao(value)
                if andar.get_name() == "Terreo":
                    total_ocupacao += value
                else:
                    andares[0].set_ocupacao(-1)
                render_menu(stdscr)

def render_menu(stdscr):
    global total_ocupacao
    clear_menu(stdscr)

    stdscr.addstr(4,0, f"Temperatura: {andares[0].get_temperature()}")
    stdscr.addstr(5,0, f"Umidade: {andares[0].get_moisture()}")
    stdscr.addstr(6,0, f"Alarme: {define_on_off(andares[0].get_alarme())}")
    stdscr.addstr(7,0, f"Ocupação Total: {total_ocupacao}")

    stdscr.addstr(9,0, f"ANDAR: {andares[0].get_name()}", curses.A_BOLD)
    stdscr.addstr(10,0, f"Ocupação: {andares[0].get_ocupacao()}")
    stdscr.addstr(11,0, f"Lampada T01: {define_on_off(andares[0].get_lampada1())}")
    stdscr.addstr(12,0, f"Lampada T02: {define_on_off(andares[0].get_lampada2())}")
    stdscr.addstr(13,0, f"Lampada Corredor: {define_on_off(andares[0].get_corredor())}")
    stdscr.addstr(14,0, f"Ar-condicionado: {define_on_off(andares[0].get_arcondicionado())}")
    stdscr.addstr(15,0, f"Aspersor: {define_on_off(andares[0].get_aspersor())}")
    stdscr.addstr(16,0, f"Janela T01: {define_on_off(andares[0].get_janela1())}")
    stdscr.addstr(17,0, f"Janela T02: {define_on_off(andares[0].get_janela2())}")
    stdscr.addstr(18,0, f"Porta: {define_on_off(andares[0].get_porta())}")
    stdscr.addstr(19,0, f"Fumaça: {define_on_off(andares[0].get_fumaca())}")

    stdscr.addstr(21,0, f"ANDAR: {andares[1].get_name()}", curses.A_BOLD)
    stdscr.addstr(22,0, f"Ocupação: {andares[1].get_ocupacao()}")
    stdscr.addstr(23,0, f"Lampada 101: {define_on_off(andares[1].get_lampada1())}")
    stdscr.addstr(24,0, f"Lampada 102: {define_on_off(andares[1].get_lampada2())}")
    stdscr.addstr(25,0, f"Lampada Corredor: {define_on_off(andares[1].get_corredor())}")
    stdscr.addstr(26,0, f"Ar-condicionado: {define_on_off(andares[1].get_arcondicionado())}")
    stdscr.addstr(27,0, f"Janela 101: {define_on_off(andares[1].get_janela1())}")
    stdscr.addstr(28,0, f"Janela 102: {define_on_off(andares[1].get_janela2())}")
    stdscr.addstr(29,0, f"Fumaça: {define_on_off(andares[1].get_fumaca())}")

    stdscr.noutrefresh()
    curses.doupdate()

def start(stdscr):
    global andares
    global stdscr_global

    stdscr_global = stdscr

    listener = keyboard.Listener(on_press=handle_input)
    listener.start()

    stdscr.clear()
    stdscr.addstr(0, 0, "[STARTED] Socket Iniciado!", curses.A_BOLD)
    stdscr.addstr(1, 0, "[WAITING] Aguardando conexões...", curses.A_BOLD)
    stdscr.refresh()
    server.listen()
    connection_count = 0

    threads = []

    while(connection_count != 2):
        conn, addr = server.accept()
        new_andar = Andar()
        andares.append(new_andar)

        # andares.append(new_andar) # TEMP

        thread = threading.Thread(target=handle_connection, args=(conn, addr, stdscr, new_andar))
        # thread.start()

        threads.append(thread)
        connection_count += 1

        stdscr.addstr(4, 0, f"Contador de conexões: {connection_count}", curses.A_BOLD)
        stdscr.refresh()

    for i in threads:
        i.start()

wrapper(start)
