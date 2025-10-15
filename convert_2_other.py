from ultralytics import YOLO

YOLO_PATH = r""
yaml_path = r""
model = YOLO(YOLO_PATH)

# Export the model to TFLite format
model.export(format="tflite", data=yaml_path, int8=True, half=False, device="cpu", save_dir="")  # creates 'yolo11n_float32.tflite'

# Load the exported TFLite model
tflite_model = YOLO("yolo11n_float32_int8.tflite")

# Run inference
results = tflite_model("https://ultralytics.com/images/bus.jpg")