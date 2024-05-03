
import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():
        
        ret, frame = cap.read()
        if (ret == True):

            height, width, _ = frame.shape
            
            # Calculamos las coordenadas del centrom
            center_coordinates = (int(width / 2), int(height / 2))

            #print("Coordenadas del centro:", center_coordinates)
            
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
                    #print("Centro de la pieza:", piece_coordinates)
                    cv2.circle(frame, piece_coordinates, 5, (255, 255, 255), -1)
                    cv2.drawContours(frame, [max_contour], -1, (0,255,0), 2)


                    # Calculamos la diferencia en píxeles entre el centroide y el centro
                    diff_x = center_coordinates[0] - cx
                    diff_y = center_coordinates[1] - cy
                    #print("Diferencia en x:", diff_x)
                    #print("Diferencia en y:", diff_y)

                    point_a = [220, 12, -28, 200]
                    #point_b = [160, 260, -30, 170]

                    #RunPoint(move, point_a)############################
                    #WaitArrive(point_a)############################3

                    def coor():
                        print(point_a)


                    xx = 0
                    yy = 0

                    xx += diff_x
                    yy += diff_y
                    xx,yy =yy,xx

                    point_a[0] += xx
                    point_a[1] += yy

                    print('el valor es este: ')

                    #RunPoint(move, point_a)
                    #WaitArrive(point_a)

                

                    #keyboard.add_hotkey('m', coor())
                    time.sleep(1)
            
            cv2.imshow('Original', frame)
            cv2.imshow('Mask', mask)

        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #break

        

        cap.release()
        cv2.destroyAllWindows()
