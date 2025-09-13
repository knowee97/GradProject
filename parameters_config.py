from ultralytics import YOLO


# Load YOLO model
model_path = r"/models/yolov8n.pt"
model = YOLO(model_path)


pixels_to_meters = 0.05
# Conversion factor: pixels to meters
# Function to calculate Euclidean distance


TARGETS = ['car', 'truck', 'person', 'bus']
MPS_2_MPH_FACTOR = 2.23694             # Conversion 3600s in 1 hour, 1609m in 1mi (3600/1609)
#converts meters per second to miles per hour.


# Initialize Webcam
WIDTH = 640
HEIGHT = 480


