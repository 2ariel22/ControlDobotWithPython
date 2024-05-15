import cv2
import numpy as np

def rojo(max_contour):
    cv2.drawContours(frame_roi, [max_contour], -1, (0, 0, 255), 2)
    #print('Es rojo')

def negro(max_contour):
    cv2.drawContours(frame_roi, [max_contour], -1, (0, 255, 0), 2)
    #print('Es negro')

cap = cv2.VideoCapture(0)
colorFinal = None
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar ningún fotograma.")
        break

    # Definir las coordenadas del ROI
    x, y, w, h = 100, 100, 200, 200

    # Obtener el ROI del frame
    frame_roi = frame[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 150, 100])
    upper_red = np.array([10, 255, 255])

    lower_negro = np.array([0, 0, 0])
    upper_negro = np.array([179, 245, 90])

    mascara_negro = cv2.inRange(hsv_roi, lower_negro, upper_negro)
    mask = cv2.inRange(hsv_roi, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos, _ = cv2.findContours(mascara_negro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_contour = None
    max_area = 0
    max_contour_type = None

    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        max_area = cv2.contourArea(max_contour)
        max_contour_type = "rojo"

    if contornos:
        max_contornos = max(contornos, key=cv2.contourArea)
        if cv2.contourArea(max_contornos) > max_area:
            max_contour = max_contornos
            max_contour_type = "negro"

    if max_contour is not None:
        M = cv2.moments(max_contour)
        if max_contour_type == "rojo":
            rojo(max_contour)
        elif max_contour_type == "negro":
            negro(max_contour)
    
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow('Original', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w'):
        if max_contour_type is not None:
            
            if(max_contour_type == "negro"):
                print("R:", max_contour_type)

cap.release()
cv2.destroyAllWindows()
