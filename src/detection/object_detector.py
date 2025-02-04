import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path, classes_of_interest):
        self.model = YOLO(model_path)
        self.classes_of_interest = classes_of_interest  # [0, 67]
    
    def detect(self, frame):
        """Executa detecção e retorna classes detectadas"""
        results = self.model(frame)
        detected_classes = set()
        
        for result in results:
            classes = result.boxes.cls.cpu().numpy().astype(int)
            for cls in classes:
                if cls in self.classes_of_interest:
                    detected_classes.add(int(cls))
        
        return detected_classes