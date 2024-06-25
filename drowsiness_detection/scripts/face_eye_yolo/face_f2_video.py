import os
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import uuid  # unique identifier
import time

model_path = '../YOLOv5/yolov5-master/runs/train/exp28/weights/last.pt'
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
print("Model loaded successfully.")

cap = cv2.VideoCapture(0)

# Assuming the class index for closed eyes is 0 (modify accordingly)
closed_eye_class_index = 0

while True:
    ret, frame = cap.read()
    results = model(frame)

    # Access the results to get bounding boxes, confidence scores, and class indices
    boxes = results.xyxy[0][:, :4]  # Bounding boxes
    confidences = results.xyxy[0][:, 4]  # Confidence scores
    class_indices = results.xyxy[0][:, 5]  # Class indices

    # Assuming there is only one closed eye in the frame 
    closed_eye_detected = any((class_idx.item() == closed_eye_class_index) and (conf > 0.2) for class_idx, conf in zip(class_indices, confidences))

    if closed_eye_detected:
        print("Eye closed")

    cv2.imshow('YOLO', np.squeeze(results.render()))

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()