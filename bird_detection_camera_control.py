# Handles video input from 4 directional cameras, applies DL detection

import cv2
import torch
import numpy as np
from torchvision import transforms
from models.yolov5_wrapper import YOLOv5

# Load pre-trained model for bird detection (YOLOv5)
model = YOLOv5("yolov5s.pt", device="cuda")

# Directions for cameras
CAMERAS = {
    "north": 0,
    "south": 1,
    "east": 2,
    "west": 3
}

def detect_birds():
    detections = {}
    for direction, cam_id in CAMERAS.items():
        cap = cv2.VideoCapture(cam_id)
        ret, frame = cap.read()
        if not ret:
            continue

        results = model.predict(frame)
        birds = [r for r in results if r['label'] == 'bird']
        if birds:
            # bird entry
            bird_pos = birds[0]['bbox']
            detections[direction] = bird_pos

        cap.release()
    return detections

if __name__ == "__main__":
    from messaging.send_to_controller import send_bird_detection
    det = detect_birds()
    send_bird_detection(det)
