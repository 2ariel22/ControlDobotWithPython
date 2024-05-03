import flet as ft
import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np
import keyboard
import time
import asyncio

Width, Height = 550, 700
Enable = False
current_actual = None

class MyButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__()
        self.bgcolor = ft.colors.ORANGE_300
        self.color = ft.colors.GREEN_800
        self.text = text
        self.on_click = on_click

class Robot():
    def __init__(self):
        self.dashboard = None
        self.move = None
        self.feed = None
        self.current_actual= None
        self.feed_thread = None
        

    def connectRobot(self):
        try:
            ip = "192.168.0.11"
            dashboard_p = 29999
            move_p = 30003
            feed_p = 30004
            self.dashboard = DobotApiDashboard(ip, dashboard_p)
            self.move = DobotApiMove(ip, move_p)
            self.feed = DobotApi(ip, feed_p)
            print(">.<conexión exitosa>!<")

        except Exception as e:
            
            raise e

    def GetConexion(self):
        self.connectRobot()

    def run_point(self, point_list: list):
        self.move.MovL(point_list[0], point_list[1], point_list[2], point_list[3],point_list[4],point_list[5])


    def wait_arrive(self,point_list):
        
        while True:
            is_arrive = True

            if self.current_actual is not None:
                for index in range(4):
                    if (abs(self.current_actual[index] - point_list[index]) > 1):
                        is_arrive = False

                if is_arrive:
                    return

            sleep(0.001)

    def get_feed(self):
        
        hasRead = 0
        while True:
            data = bytes()
            while hasRead < 1440:
                temp = self.feed.socket_dobot.recv(1440 - hasRead)
                if len(temp) > 0:
                    hasRead += len(temp)
                    data += temp
            hasRead = 0

            a = np.frombuffer(data, dtype=MyType)
            if hex((a['test_value'][0])) == '0x123456789abcdef':

                # Refresh Properties
                self.current_actual = a["tool_vector_actual"][0]
                #print(point_Init)
                #print("tool_vector_actual:", current_actual)

            
    def setfeed(self):
        self.feed_thread = threading.Thread(target=self.get_feed, args=(self.feed,))
        self.feed_thread.setDaemon(True)
        self.feed_thread.start()

    def Mover():
        pass

async def main(page: ft.Page):
    page.window_height = Height
    page.window_width = Width
    page.padding = 0
    page.adaptive = True

    robot = Robot()
    robot.setfeed()

    def ActivarRobot(e):
        robot.dashboard.EnableRobot()
        

    async def connect_robot(e):
        try:
            await asyncio.run(robot.GetConexion())
        except:
            print(":(La conexión falló:(")

    def Mover(e):
        point_Init = [210, 9, -45, 1, 0, 0]
        robot.run_point(point_Init)
        robot.wait_arrive(point_Init)

    
    ItemsSuperior = [
        ft.Slider(min=0, max=100, divisions=100, label="x:{value}"),
        ft.Slider(min=0, max=100, divisions=100, label="y:{value}"),
        ft.Slider(min=0, max=100, divisions=100, label="z:{value}"),
        ft.Slider(min=0, max=100, divisions=100, label="R:{value}")
    ]

    Sliders = [ft.Container(content=ft.Column(ItemsSuperior), width=250, height=300, margin=ft.margin.only(top=20)),
               ft.Container(width=265, height=300, border=ft.border.all(color="red"))]

    Superior = ft.Container(content=ft.Row(Sliders), width=530, height=300, margin=ft.margin.only(top=15))

    ItemsMedio = [ft.Row(spacing=120, controls=[
        MyButton(text="Active", on_click=ActivarRobot),
        MyButton(text="Connect", on_click=connect_robot),
        MyButton(text="Boton3",on_click=Mover)],height=100)
        #ft.Row(spacing=120,controls=[MyButton(text="Boton4",on_click=clicked),
        #MyButton(text="Boton5",on_click=clicked),
        #MyButton(text="Boton6",on_click=clicked)
        #],height=100)
        ]

    Medio = ft.Container(content=ft.Column(ItemsMedio),
                         width=530, height=200, margin=ft.margin.only(top=5),
                         border=ft.border.all(color="blue"))

    Inferior = ft.Container(width=530, height=100, margin=ft.margin.only(top=5),
                            border=ft.border.all(color="blue"))

    colum = ft.Column(spacing=0, controls=[
        Superior,
        Medio,
        Inferior
    ])

    container = ft.Container(colum, height=Height, alignment=ft.alignment.top_center)
    page.add(
        container
    )

ft.app(target=main)