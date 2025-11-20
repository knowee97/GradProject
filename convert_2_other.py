from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("/home/noe_ee/GradProject/runs/train_yolov8n.pt/weights/best.pt")

# Export the model to TFLite format
#model.export(format="tflite", int8=True, data="/home/noe_ee/GradProject/data_folder/detect/detect.yaml", device = 0)  # creates 'yolo11n_float32.tflite'

# Load the exported TFLite model
#tflite_model = YOLO("yolo11n_float32.tflite")

# Run inference
results = model("https://ultralytics.com/images/bus.jpg")