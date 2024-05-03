import threading
import cv2
import numpy as np
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import keyboard
import time

# Variable global (coordenadas actuales)
#https://github.com/Dobot-Arm/TCP-IP-4Axis-Python-CMD
current_actual = None
point_Init = [223.74, 0, 41.13, 0]
move = None
piece_coordinates = None

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
            #print(point_Init)
            #print("tool_vector_actual:", current_actual)

        sleep(0.001)



def detect_red_object():
    global piece_coordinates, diff_x, diff_y

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Obtenemos las dimensiones del fotograma
        height, width, _ = frame.shape
        
        # Calculamos las coordenadas del centro
        center_coordinates = (int(width / 2), int(height / 2))
        
        # Dibujamos un círculo en el centro del fotograma
        cv2.circle(frame, center_coordinates, 5, (255, 255, 255), -1)

        # Convertir el frame de BGR a HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
        # Definir el rango de colores a detectar en HSV
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
            
        # máscara para el color rojo y aplicarla al frame original
        mask = cv2.inRange(hsv, lower_red, upper_red)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(max_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                piece_coordinates = (cx, cy)
                cv2.circle(frame, piece_coordinates, 5, (255, 255, 255), -1)
                cv2.drawContours(frame, [max_contour], -1, (0,255,0), 2)

                # Calculamos la diferencia en píxeles entre el centroide y el centro
                diff_x = center_coordinates[0] - cx
                diff_y = center_coordinates[1] - cy
                print("Diferencia en x:", diff_x)
                print("Diferencia en y:", diff_y)

                increase_x_y_coordinate(diff_x, diff_y)
                #ola()
                print()
                print(point_Init)



                
            
        #mcv2.imshow('Original', frame)
        #cv2.imshow('Mask', mask)

        #keyboard.add_hotkey('m', increase_x_y_coordinate)
        

        #keyboard.add_hotkey('i', ola)
        
        time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



    cap.release()
    cv2.destroyAllWindows()

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

def increase_x_y_coordinate(a,b):
    global point_Init
    point_Init[0] += a
    point_Init[1] += b


def ola():    
    global point_Init, move
    run_point(move, point_Init)
    wait_arrive(point_Init)

if __name__ == '__main__':
    dashboard, move, feed = connect_robot()
    print("Empezar a habilitar...")
    dashboard.EnableRobot()
    print("Terminado de habilitar :)")


    
    feed_thread = threading.Thread(target=get_feed, args=(feed,))
    feed_thread.setDaemon(True)
    feed_thread.start()

    # Inicia la detección del objeto rojo
      
    #dashboard.SpeedFactor(10)
    print("Ejecución de bucle...") 
    detect_red_object()  
       

