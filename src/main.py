# src/main.py

import time
import threading
import cv2 
from detection.camera import CameraController
from detection.object_detector import ObjectDetector
from data_processing.log_manager import LogManager
from gui.main_window import MainWindow

class Application:
    def __init__(self):
        # Inicializa componentes
        self.log_manager = LogManager()
        self.detector = ObjectDetector("yolo11x.pt", [0, 67])
        self.camera = CameraController()

        # Inicializa o estado de execução da detecção
        self.running = False

        # Interface
        self.gui = MainWindow(self.start_detection, self.stop_callback_and_close, self.detector, self.is_detection_running)

        # Variáveis de estado
        self.phone_present = False
        self.phone_start_time = None
        self.human_present = True
        self.human_start_time = None

        # Threads
        self.detection_thread = threading.Thread(target=self.detection_loop)

    def start(self):
        self.gui.mainloop()

    def start_detection(self):
        self.running = True
        if not self.detection_thread.is_alive():
            self.detection_thread = threading.Thread(target=self.detection_loop)
            self.detection_thread.start()
        print("Detecção iniciada")

    def stop_detection(self):
        self.running = False
        self.release_camera()
        print("Detecção finalizada")

    def is_detection_running(self):
        return self.running

    def detection_loop(self):
        while self.running:
            try:
                frame = self.camera.get_frame()
                detections = self.detector.detect(frame)
                self.process_detections(detections)
                time.sleep(0.1)
            except Exception as e:
                print(f"Erro na detecção: {str(e)}")
                break

    def process_detections(self, detections):
        current_time = time.time()

        # Lógica para celular
        if 67 in detections:
            if not self.phone_present:
                self.phone_present = True
                self.phone_start_time = current_time
                print("Celular detectado na mesa")
        else:
            if self.phone_present:
                duration = current_time - self.phone_start_time
                self.log_manager.save_log("Celular removido", duration)
                self.phone_present = False
                print(f"Log celular salvo: {duration}s")

        # Lógica para presença humana
        if 0 in detections:
            if not self.human_present:
                self.human_present = True
                duration = current_time - self.human_start_time
                self.log_manager.save_log("Humano ausente", duration)
                print(f"Log de ausência salvo: {duration}s")
        else:
            if self.human_present:
                self.human_present = False
                self.human_start_time = current_time
                print("Humano ausente detectado")

    def close_camera(self):
        cv2.destroyAllWindows()

    def release_camera(self):
        if self.camera and self.camera.cap:
            self.camera.cap.release()
            print("Câmera liberada")

    def stop_callback_and_close(self):
        self.stop_detection()
        self.close_camera()

if __name__ == "__main__":
    app = Application()
    app.start()