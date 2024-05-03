from tkinter import *
import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np
import keyboard
import time

# Variable global (coordenadas actuales)
#https://github.com/Dobot-Arm/TCP-IP-4Axis-Python-CMD
current_actual = None
point_Init = [223.74, 0, 41.13, 0]
move = None
RunState=False
Arrive = True


def on_slider_move(value):
    label.config(text="rotacion °: {}".format(value))

def connect_robot():
    try:
        ip = "192.168.0.11"
        dashboard_p = 29999
        move_p = 30003
        feed_p = 30004
        print("Se esta estableciendo la conexion...")
        dashboard = DobotApiDashboard(ip, dashboard_p)
        move = DobotApiMove(ip, move_p)
        feed = DobotApi(ip, feed_p)
        print(">.<conexión exitosa>!<")
        return dashboard, move, feed
    except Exception as e:
        print(":(La conexión falló:(")
        raise e

def run_point(move: DobotApiMove, point_list: list):
    move.MovL(point_list[0], point_list[1], point_list[2], point_list[3])

def get_feed(feed: DobotApi):
    global current_actual
    hasRead = 0
    while True:
        data = bytes()
        while hasRead < 1440:
            temp = feed.socket_dobot.recv(1440 - hasRead)
            if len(temp) > 0:
                hasRead += len(temp)
                data += temp
        hasRead = 0

        a = np.frombuffer(data, dtype=MyType)
        if hex((a['test_value'][0])) == '0x123456789abcdef':

            # Refresh Properties
            current_actual = a["tool_vector_actual"][0]
            print(point_Init)
            #print("tool_vector_actual:", current_actual)

        sleep(0.001)

def wait_arrive(point_list):
    global current_actual
    while True:
        is_arrive = True

        if current_actual is not None:
            for index in range(4):
                if (abs(current_actual[index] - point_list[index]) > 1):
                    is_arrive = False

            if is_arrive:
                return
            else:
                return not(Arrive)

        sleep(0.001)
def increase_x_coordinate():
    global point_Init
    point_Init[0] += 1
 
def decrease_x_coordinate():
    global point_Init
    point_Init[0] -= 1

def increase_y_coordinate():
    global point_Init
    point_Init[1] += 1
 
def decrease_y_coordinate():
    global point_Init
    point_Init[1] -= 1

def increase_z_coordinate():
    global point_Init
    point_Init[2] += 1
 
def decrease_z_coordinate():
    global point_Init
    point_Init[2] -= 1  

def ola():    
    global point_Init, move
    run_point(move, point_Init)
    wait_arrive(point_Init)


def change_text():
    global Arrive
    if(Arrive):
        pass

raiz = Tk()
raiz.title("interfaz perrona")

color = "lightblue"

raiz.geometry("500x500")
raiz.config(bg=color)

entry1 =  Scale(raiz, from_=0, to=100, orient=HORIZONTAL, command=on_slider_move)
text1 = Label(raiz,text="pocision en x")


entry2 =  Scale(raiz, from_=0, to=100, orient=HORIZONTAL, command=on_slider_move)
text2 = Label(raiz,text="pocision en y")


entry3 =  Scale(raiz, from_=0, to=100, orient=HORIZONTAL, command=on_slider_move)
text3 = Label(raiz,text="pocision en z")


text1.place(x=10,y=25)
entry1.place(x=10,y=50)


text2.place(x=190,y=25)
entry2.place(x=190,y=50)


text3.place(x=360,y=25)
entry3.place(x=360,y=50)


slider = Scale(raiz, from_=0, to=100, orient=VERTICAL, command=on_slider_move)
slider.place(x=10,y=210)

label = Label(raiz, text="Rotacion °: ")
label.place(x=10,y=180)

EnableButton = Button(text="Enable",width=10)
EnableButton.place(x=350,y=210)

DisableButton = Button(text="Disable",width=10)
DisableButton.place(x=350,y=260)

StopButton = Button(text="Stop",width=10)
StopButton.place(x=250,y=260)

RunButton = Button(text="Run",width=10)
RunButton.place(x=250,y=210)

ConnectButton = Button(text="Connect",width=24, command=lambda:connect_robot)
ConnectButton.place(x=250,y=310)

clearButton = Button(text="clear",width=24, command=lambda:connect_robot)
clearButton.place(x=250,y=310)


text3.config(bg=color)
text2.config(bg=color)
text1.config(bg=color)

change_text()

raiz.mainloop()
