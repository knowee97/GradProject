import time
from ultralytics import YOLO
import cv2
import numpy as np
from collections import defaultdict

# Load YOLO model
model_path = r"/models/yolov8n.pt"
model = YOLO(model_path)


pixels_to_meters = 0.05                    # Conversion factor: pixels to meters
# Function to calculate Euclidean distance
def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

TARGETS = ['car', 'truck', 'person', 'bus']
MPS_2_MPH_FACTOR = 2.23694             # Conversion 3600s in 1 hour, 1609m in 1mi (3600/1609)
#converts meters per second to miles per hour.


# Initialize Webcam
WIDTH = 640
HEIGHT = 480