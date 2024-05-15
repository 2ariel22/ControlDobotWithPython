import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np


# Variable global (coordenadas actuales)
#https://github.com/Dobot-Arm/TCP-IP-4Axis-Python-CMD

# rutina establecida para tomar un objeto y llevarlo de un punto A a un punto B

current_actual = None

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
            print("tool_vector_actual:", current_actual)

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

if __name__ == '__main__':
    dashboard, move, feed = connect_robot()
    print("Empezar a habilitar...")
    dashboard.EnableRobot()
    print("Terminado de habilitar :)")


    
    feed_thread = threading.Thread(target=get_feed, args=(feed,))
    feed_thread.setDaemon(True)
    feed_thread.start()
    print("Ejecución de bucle...")
   
    point_1 = [327, 0, 21, 0]
    point_2 = [327, 140, 21, 0]
    point_3 = [327, 158.12, -156.2, 0]

    #PUNTO DOS
    #PUNTO 1

    point_4 = [327, -160, 21, 0]
    point_5 = [339, -160, -154.9, 0]
    
    
    dashboard.SpeedFactor(50)
    while True:   
        run_point(move, point_1)
        wait_arrive(point_1)
        run_point(move, point_2)
        wait_arrive(point_2)
        run_point(move, point_3)
        wait_arrive(point_3)
        dashboard.DO(1,1)
        dashboard.DO(2,0)
        run_point(move, point_2)
        wait_arrive(point_2)
        run_point(move, point_1)
        wait_arrive(point_1)

        run_point(move, point_4)
        wait_arrive(point_4)
        run_point(move, point_5)
        wait_arrive(point_5)
        dashboard.DO(1,0)
        dashboard.DO(2,1)
        sleep(.5)
        dashboard.DO(2,0)

      
 



