import cv2
import keyboard
import time
import numpy as np
cap = cv2.VideoCapture(0)

def increase_x_y_coordinate():
    print("incrementando coordenadas")


def ola():    
    print("entre a ola")


while cap.isOpened():
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
            
        cv2.imshow('Original', frame)
        cv2.imshow('Mask', mask)

        keyboard.add_hotkey('m', increase_x_y_coordinate)
        

        keyboard.add_hotkey('i', ola)
        
      
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



cap.release()
cv2.destroyAllWindows()
