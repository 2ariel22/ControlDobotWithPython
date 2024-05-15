import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np
import keyboard
import time

# Variable global (coordenadas actuales)
#https://github.com/Dobot-Arm/TCP-IP-4Axis-Python-CMD
current_actual = None
point_Init = [223.74, 0, 41.13, 0 ,0 ,0]
move = None
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
if __name__ == '__main__':
    dashboard, move, feed = connect_robot()
    print("Empezar a habilitar...")
    ola = dashboard.EnableRobot()
    print("ola: ",ola)


    
    feed_thread = threading.Thread(target=get_feed, args=(feed,))
    feed_thread.setDaemon(True)
    feed_thread.start()
    
    #dashboard.SpeedFactor(10)
    print("Ejecución de bucle...")
    while True:
        keyboard.add_hotkey('w', increase_x_coordinate)
        keyboard.add_hotkey('s', decrease_x_coordinate)
        
        keyboard.add_hotkey('d', increase_y_coordinate)
        keyboard.add_hotkey('a', decrease_y_coordinate)

        keyboard.add_hotkey('q', increase_z_coordinate)
        keyboard.add_hotkey('e', decrease_z_coordinate)

        keyboard.add_hotkey('o', ola)
        
        time.sleep(1)

    
    
   

   