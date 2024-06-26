import flet as ft
import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np
import keyboard
import time


Width, Height = 550,700
Enable=False
class MyButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__()
        self.bgcolor = ft.colors.ORANGE_300
        self.color = ft.colors.GREEN_800
        self.text = text
        self.on_click = on_click
def clicked():
    pass


# Variable global (coordenadas actuales)
#https://github.com/Dobot-Arm/TCP-IP-4Axis-Python-CMD
current_actual = None
point_Init = [223.74, 0, 41.13, 0 ,0 ,0]
move = None
def connect_robot(e):
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
    move.MovL(point_list[0], point_list[1], point_list[2], point_list[3],point_list[4],point_list[5])

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
            #print(point_Init)
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
           

async def main(page: ft.Page):
    def ActivarRobot(e):
        global dashboard, move, feed,Enable
        dashboard, move, feed = connect_robot()
        if(Enable):
            print("Empezar a habilitar...")
            dashboard.EnableRobot()
            print("Terminado de habilitar :)")
            feed_thread = threading.Thread(target=get_feed, args=(feed,))
            feed_thread.setDaemon(True)
            feed_thread.start()

            if(ola[0]=="0"):
                Enable=True
            else:
                print("no se pudo a")
        else:
            print("Empezar a Deshabilitar...")
            aux=dashboard.DisableRobot()
            print("disable: ",aux)
            Enable=False
    

    page.window_height=Height
    page.window_width=Width
    page.padding=0
    page.adaptive = True

    ItemsSuperior =[
        ft.Slider(min=0, max=100, divisions=100, label="x:{value}"),
        ft.Slider(min=0, max=100, divisions=100, label="y:{value}"),
        ft.Slider(min=0, max=100, divisions=100, label="z:{value}"),
        ft.Slider(min=0, max=100, divisions=100, label="R:{value}")
    ]
    Sliders = [ft.Container(content=ft.Column(ItemsSuperior),width=250,height=300,margin=ft.margin.only(top=20)),
               ft.Container(width=265,height=300,border=ft.border.all(color="red"))]
    
    Superior = ft.Container(content=ft.Row(Sliders),width=530,height=300,margin=ft.margin.only(top=15))

    ItemsMedio =[ft.Row(spacing=120,controls=[MyButton(text="Disable",on_click=ActivarRobot),
        MyButton(text="Connect",on_click=connect_robot),
        MyButton(text="Boton3",on_click=clicked)],height=100),
        ft.Row(spacing=120,controls=[MyButton(text="Boton4",on_click=clicked),
        MyButton(text="Boton5",on_click=clicked),
        MyButton(text="Boton6",on_click=clicked)],height=100)]
    
    

    


    Medio = ft.Container(content=ft.Column(ItemsMedio),
                         width=530,height=200,margin=ft.margin.only(top=5),
                         border=ft.border.all(color="blue"))
    
    Inferior = ft.Container(width=530,height=100,margin=ft.margin.only(top=5),
                            border=ft.border.all(color="blue"))
   
    colum = ft.Column(spacing=0,controls=[
        Superior,
        Medio,
        Inferior
    ]

    )

    container = ft.Container(colum,height=Height,alignment=ft.alignment.top_center)
    page.add(
        container
        )

ft.app(target=main)