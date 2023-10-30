import cv2
import numpy as np
from PIL import Image

from .model import load_model


def face_detection(input_path: str, model_name: str, ) -> bool:
    model_path = load_model(model_name)
    face_detector = cv2.CascadeClassifier(model_path)

    img = Image.open(input_path).convert("RGB")

    faces = face_detector.detectMultiScale(np.array(img))

    return len(faces) > 0
