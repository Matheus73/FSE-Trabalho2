#!/usr/bin/python
import socket
import threading

from models import Andar
from utils import clear_menu, play_alarme, define_on_off, define_aberto_fechado, append_log_file
from json_parser import set_gpio_values

from pynput import keyboard
from playsound import playsound

import time
from datetime import datetime
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
    time.sleep(0.5)
    conn.send(f"{andar.get_lampada2_gpio()}=0".encode(FORMATO))
    time.sleep(0.5)
    conn.send(f"{andar.get_corredor_gpio()}=0".encode(FORMATO))
    time.sleep(0.5)
    conn.send(f"{andar.get_arcondicionado_gpio()}=0".encode(FORMATO))
    time.sleep(0.5)
    if(andar.get_name() == "Térreo"):
        conn.send(f"{andar.get_aspersor_gpio()}=0".encode(FORMATO))

def handle_input(key):
    if key == keyboard.Key.f1:
        andares[0].set_lampada1()
        if andares[0].get_lampada1():
            connections[0]["conn"].send(f"{andares[0].get_lampada1_gpio()}=1".encode(FORMATO))
            append_log_file(f"ligou,lampadaT01,{datetime.now().time()}")
        else:
            connections[0]["conn"].send(f"{andares[0].get_lampada1_gpio()}=0".encode(FORMATO))
            append_log_file(f"desligou,lampadaT01,{datetime.now().time()}")
        render_menu(stdscr_global)
    elif key == keyboard.Key.f2:
        andares[0].set_lampada2()
        if andares[0].get_lampada2():
            connections[0]["conn"].send(f"{andares[0].get_lampada2_gpio()}=1".encode(FORMATO))
            append_log_file(f"ligou,lampadaT02,{datetime.now().time()}")
        else:
            connections[0]["conn"].send(f"{andares[0].get_lampada2_gpio()}=0".encode(FORMATO))
            append_log_file(f"desligou,lampadaT02,{datetime.now().time()}")
        render_menu(stdscr_global)
    elif key == keyboard.Key.f3:
        andares[0].set_corredor()
        if andares[0].get_corredor():
            connections[0]["conn"].send(f"{andares[0].get_corredor_gpio()}=1".encode(FORMATO))
            append_log_file(f"ligou,corredor terreo,{datetime.now().time()}")
        else:
            connections[0]["conn"].send(f"{andares[0].get_corredor_gpio()}=0".encode(FORMATO))
            append_log_file(f"desligou,corredor terreo,{datetime.now().time()}")
        render_menu(stdscr_global)
    elif key == keyboard.Key.f4:
        andares[0].set_arcondicionado()
        if andares[0].get_arcondicionado():
            connections[0]["conn"].send(f"{andares[0].get_arcondicionado_gpio()}=1".encode(FORMATO))
            append_log_file(f"ligou,arcondicionado terreo,{datetime.now().time()}")
        else:
            connections[0]["conn"].send(f"{andares[0].get_arcondicionado_gpio()}=0".encode(FORMATO))
            append_log_file(f"desligou,arcondicionado terreo,{datetime.now().time()}")
        render_menu(stdscr_global)
    elif key == keyboard.Key.f5:
        andares[0].set_aspersor()
        if andares[0].get_aspersor():
            connections[0]["conn"].send(f"{andares[0].get_aspersor_gpio()}=1".encode(FORMATO))
            append_log_file(f"ligou,aspersor,{datetime.now().time()}")
        else:
            connections[0]["conn"].send(f"{andares[0].get_aspersor_gpio()}=0".encode(FORMATO))
            append_log_file(f"desligou,aspersor,{datetime.now().time()}")
        render_menu(stdscr_global)

    elif key == keyboard.Key.f6:
        andares[1].set_lampada1()
        if andares[1].get_lampada1():
            connections[1]["conn"].send(f"{andares[1].get_lampada1_gpio()}=1".encode(FORMATO))
            append_log_file(f"ligou,lampada101,{datetime.now().time()}")
        else:
            connections[1]["conn"].send(f"{andares[1].get_lampada1_gpio()}=0".encode(FORMATO))
            append_log_file(f"desligou,lampada101,{datetime.now().time()}")
        render_menu(stdscr_global)
    elif key == keyboard.Key.f7:
        andares[1].set_lampada2()
        if andares[1].get_lampada2():
            connections[1]["conn"].send(f"{andares[1].get_lampada2_gpio()}=1".encode(FORMATO))
            append_log_file(f"ligou,lampada102,{datetime.now().time()}")
        else:
            connections[1]["conn"].send(f"{andares[1].get_lampada2_gpio()}=0".encode(FORMATO))
            append_log_file(f"desligou,lampada102,{datetime.now().time()}")
        render_menu(stdscr_global)
    elif key == keyboard.Key.f8:
        andares[1].set_corredor()
        if andares[1].get_corredor():
            connections[1]["conn"].send(f"{andares[1].get_corredor_gpio()}=1".encode(FORMATO))
            append_log_file(f"ligou,corredor 1 andar,{datetime.now().time()}")
        else:
            connections[1]["conn"].send(f"{andares[1].get_corredor_gpio()}=0".encode(FORMATO))
            append_log_file(f"desligou,corredor 1 andar,{datetime.now().time()}")
        render_menu(stdscr_global)
    elif key == keyboard.Key.f9:
        andares[1].set_arcondicionado()
        if andares[1].get_arcondicionado():
            connections[1]["conn"].send(f"{andares[1].get_arcondicionado_gpio()}=1".encode(FORMATO))
            append_log_file(f"ligou,arcondicionado 1 andar,{datetime.now().time()}")
        else:
            connections[1]["conn"].send(f"{andares[1].get_arcondicionado_gpio()}=0".encode(FORMATO))
            append_log_file(f"desligou,arcondicionado 1 andar,{datetime.now().time()}")
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

    name = False

    while(True):
        msg = conn.recv(1024).decode(FORMATO)
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
                    andar.set_name("1º Andar")
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
                try:
                    value = int(msg.split("=")[1])
                    andar.set_ocupacao(value)
                    if andar.get_name() == "Terreo":
                        total_ocupacao += value
                    else:
                        andares[0].set_ocupacao(-1)
                    render_menu(stdscr)
                except:
                    pass

            elif(msg.startswith("jan1=")):
                try:
                    value = int(msg.split("=")[1])
                    if value == 1:
                        andar.set_janela1(True)
                        append_log_file(f"abriu,janela t1,{datetime.now().time()}")
                    elif value == 0:
                        andar.set_janela1(False)
                        append_log_file(f"fechou,janela t1,{datetime.now().time()}")
                except:
                    pass

            elif(msg.startswith("jan2=")):
                try:
                    value = int(msg.split("=")[1])
                    if value == 1:
                        andar.set_janela2(True)
                        append_log_file(f"abriu,janela t2,{datetime.now().time()}")
                    elif value == 0:
                        andar.set_janela2(False)
                        append_log_file(f"fechou,janela t2,{datetime.now().time()}")
                except:
                    pass

            elif(msg.startswith("port=")):
                try:
                    value = int(msg.split("=")[1])
                    if value == 1:
                        andar.set_porta(True)
                        append_log_file(f"abriu,porta terreo,{datetime.now().time()}")
                    elif value == 0:
                        andar.set_porta(False)
                        append_log_file(f"fechou,porta terreo,{datetime.now().time()}")
                except:
                    pass

            elif(msg.startswith("fumaca=")):
                try:
                    value = int(msg.split("=")[1])
                    if value == 1:
                        andar.set_fumaca(True)
                        append_log_file(f"detectou,fumaca,{datetime.now().time()}")
                    elif value == 0:
                        andar.set_fumaca(False)
                        append_log_file(f"deixou de detectar,fumaca,{datetime.now().time()}")
                except:
                    pass

            render_menu(stdscr)

def render_menu(stdscr):
    global total_ocupacao
    clear_menu(stdscr)
    stdscr.addstr(0,0, f"----------- [INPUTS] -----------",curses.A_BOLD)
    stdscr.addstr(1,0, f"[F1] Lampada T01 [F2] Lampada T02 [F3] Lampada Corredor Terreo")
    stdscr.addstr(2,0, f"[F4] Ar-condicionado Terreo [F5] Aspersor Terreo [F6] Lampada 101")
    stdscr.addstr(3,0, f"[F7] Lampada 102 [F8] Lampada corredor 1º andar [F9] Ar-condicionado 1º andar")
    stdscr.addstr(4,0, f"----------- [F10] Alarme ----------")

    stdscr.addstr(6,0, f"Alarme: {define_on_off(andares[0].get_alarme())}")
    stdscr.addstr(7,0, f"Ocupação Total: {total_ocupacao}")

    stdscr.addstr(9,0, f"ANDAR: {andares[0].get_name()}", curses.A_BOLD)
    stdscr.addstr(10,0, f"Temperatura: {andares[0].get_temperature()}")
    stdscr.addstr(11,0, f"Umidade: {andares[0].get_moisture()}")
    stdscr.addstr(12,0, f"Ocupação: {andares[0].get_ocupacao()}")
    stdscr.addstr(13,0, f"Lampada T01: {define_on_off(andares[0].get_lampada1())}")
    stdscr.addstr(14,0, f"Lampada T02: {define_on_off(andares[0].get_lampada2())}")
    stdscr.addstr(15,0, f"Lampada Corredor: {define_on_off(andares[0].get_corredor())}")
    stdscr.addstr(16,0, f"Ar-condicionado: {define_on_off(andares[0].get_arcondicionado())}")
    stdscr.addstr(17,0, f"Aspersor: {define_on_off(andares[0].get_aspersor())}")
    stdscr.addstr(18,0, f"Janela T01: {define_aberto_fechado(andares[0].get_janela1())}")
    stdscr.addstr(19,0, f"Janela T02: {define_aberto_fechado(andares[0].get_janela2())}")
    stdscr.addstr(20,0, f"Porta: {define_aberto_fechado(andares[0].get_porta())}")
    stdscr.addstr(21,0, f"Fumaça: {define_on_off(andares[0].get_fumaca())}")

    stdscr.addstr(23,0, f"ANDAR: {andares[1].get_name()}", curses.A_BOLD)
    stdscr.addstr(24,0, f"Temperatura: {andares[1].get_temperature()}")
    stdscr.addstr(25,0, f"Umidade: {andares[1].get_moisture()}")
    stdscr.addstr(26,0, f"Ocupação: {andares[1].get_ocupacao()}")
    stdscr.addstr(27,0, f"Lampada 101: {define_on_off(andares[1].get_lampada1())}")
    stdscr.addstr(28,0, f"Lampada 102: {define_on_off(andares[1].get_lampada2())}")
    stdscr.addstr(29,0, f"Lampada Corredor: {define_on_off(andares[1].get_corredor())}")
    stdscr.addstr(30,0, f"Ar-condicionado: {define_on_off(andares[1].get_arcondicionado())}")
    stdscr.addstr(31,0, f"Janela 101: {define_aberto_fechado(andares[1].get_janela1())}")
    stdscr.addstr(32,0, f"Janela 102: {define_aberto_fechado(andares[1].get_janela2())}")
    stdscr.addstr(33,0, f"Fumaça: {define_on_off(andares[1].get_fumaca())}")

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

        thread = threading.Thread(target=handle_connection, args=(conn, addr, stdscr, new_andar))

        threads.append(thread)
        connection_count += 1

        stdscr.addstr(4, 0, f"Contador de conexões: {connection_count}", curses.A_BOLD)
        stdscr.refresh()

    for i in threads:
        i.start()

wrapper(start)
