from ultralytics import YOLO
import shutil
import os

data_yaml_path = r"/home/noe_ee/GradProject/data_folder/detect/detect.yaml"


model_names = [
    "yolov8n.pt",
    "yolo11n.pt"
]

output_dir = "runs"


for name in model_names:
    print(f"\nTraining model: {name}")

    model = YOLO(name)

    results = model.train(
        data=data_yaml_path,
        epochs=50,
        imgsz=640,
        project=output_dir,
        name=f"train_{name}",
        device = 0
    )

    run_path = os.path.join(output_dir, f"train_{name}")

    zip_path = shutil.make_archive(run_path, "zip", run_path)

