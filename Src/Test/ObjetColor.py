import cv2
import numpy as np

class ColorDetector:
    def __init__(self, roi_coords=(100, 100, 200, 200)):
        self.roi_coords = roi_coords
        self.cap = cv2.VideoCapture(0)
        self.lower_red = np.array([0, 150, 100])
        self.upper_red = np.array([10, 255, 255])
        self.lower_negro = np.array([0, 0, 0])
        self.upper_negro = np.array([179, 245, 90])

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def get_color(self):
        ret, frame = self.cap.read()
        if not ret:
            print("No se pudo capturar ningún fotograma.")
            return None
        
        # Obtener las coordenadas del ROI
        x, y, w, h = self.roi_coords

        # Obtener el ROI del frame
        frame_roi = frame[y:y+h, x:x+w]
        hsv_roi = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)

        # Aplicar las máscaras de color al ROI
        mask_red = cv2.inRange(hsv_roi, self.lower_red, self.upper_red)
        mask_negro = cv2.inRange(hsv_roi, self.lower_negro, self.upper_negro)

        # Encontrar los contornos en las máscaras
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_negro, _ = cv2.findContours(mask_negro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Determinar el color dominante
        if contours_red:
            return "rojo"
        elif contours_negro:
            return "negro"
        else:
            return "desconocido"

# Ejemplo de uso
detector = ColorDetector()

color = detector.get_color()
if color is not None:
        if(color == "rojo"):
            print("robot derecha")
        elif(color == "negro"):
            print("robot izquierda")