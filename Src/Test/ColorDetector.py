import cv2
import numpy as np

class ColorDetector:
    def _init_(self, video_source=0):
        self.cap = cv2.VideoCapture(video_source)

    def detect_colors(self):
        while True:
            ret, frame = self.cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_red = np.array([0, 150, 100])
            upper_red = np.array([10, 255, 255])

            lower_negro = np.array([0, 0, 0])
            upper_negro = np.array([179, 245, 90])
            
            mascara_negro = cv2.inRange(hsv, lower_negro, upper_negro)
            mask = cv2.inRange(hsv, lower_red, upper_red)
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
                    self.draw_and_print(max_contour, "Es rojo")
                elif max_contour_type == "negro":
                    self.draw_and_print(max_contour, "Es negro")
            
            cv2.imshow('Original', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def draw_and_print(self, contour, message):
        cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)
        if cv2.waitKey(1) & 0xFF == ord('i'):
            print(message)

if _name_ == "_main_":
    color_detector = ColorDetector(video_source=1)  # Puedes cambiar el número de video_source según tu cámara
    color_detector.detect_colors()