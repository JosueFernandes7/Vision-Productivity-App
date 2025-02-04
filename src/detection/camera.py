import cv2

class CameraController:
    def __init__(self, source=0, width=1280):
        self.cap = cv2.VideoCapture(source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        
        if not self.cap.isOpened():
            raise RuntimeError("Não foi possível abrir a câmera")

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            raise RuntimeError("Erro ao capturar frame")
        return frame

    def release(self):
        self.cap.release()
        print("Câmera liberada com sucesso")