import time
import cv2
import os
from datetime import datetime
from collections import defaultdict

from vehicle_calculations import *
from parameters_config import *

# Picamera2 imports
from picamera2 import Picamera2
import numpy as np

# -----------------------------
# Utility functions
# -----------------------------

def create_unique_filename(folder_path, model_tag, extension=".mp4"):
    os.makedirs(folder_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{model_tag}{extension}"
    return os.path.join(folder_path, filename)


def draw_boxes(results, frame_resized, prev_positions, time_elapsed):
    for result in results:
        boxes = result.boxes
        for i in range(len(boxes)):
            box = boxes.xyxy[i].numpy().astype(int)
            confidence = float(boxes.conf[i].numpy())
            class_id = int(boxes.cls[i].numpy())
            label = model.names[class_id]

            if label in TARGETS:
                x1, y1, x2, y2 = box
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                track_id = (label, i)

                if label != "person":
                    trackMPH(prev_positions, track_id, center, time_elapsed, frame_resized, x1, y1)

                # Draw box and label
                color = (0, 0, 255)
                cv2.rectangle(frame_resized, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame_resized, f"{label} {confidence:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# -----------------------------
# Main webcam / camera loop
# -----------------------------

def runWebCam(prev_positions, prev_frame_time, VIDEO_PATH="", video=False, show_window=True, camera=None):
    """
    prev_positions: dict for tracking previous positions
    prev_frame_time: float
    VIDEO_PATH: path to video file (if video=True)
    video: bool, use video file instead of camera
    show_window: bool, display the output
    camera: Picamera2 object (optional)
    """

    if camera is not None:
        window_title = "YOLO Picamera2"
        video_fps = 30  # default FPS for Picamera2
        cap = None
    elif video:
        video_model = model(VIDEO_PATH)
        window_title = "YOLO Video"
        video_fps = 30  # default or get from metadata
        cap = None
    else:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Error: Could not open video stream or file.")
        window_title = "YOLO Webcam"
        video_fps = cap.get(cv2.CAP_PROP_FPS) or 30

    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_path = create_unique_filename(folder_path="output_video",
                                         model_tag=os.path.splitext(os.path.basename(model_path))[0])
    print("Video will be saved to:", output_path)
    out = cv2.VideoWriter(output_path, fourcc, video_fps, (WIDTH, HEIGHT))
    if not out.isOpened():
        raise Exception(f"Failed to open video writer with path: {output_path}")

    try:
        while True:
            # Capture frame
            if camera is not None:
                frame = camera.capture_array()  # returns BGR NumPy array
            elif video:
                # If using video file (YOLO dataset style)
                frame = video_model.next()  # adjust depending on your video model
                if frame is None:
                    print("End of video.")
                    break
            else:
                ret, frame = cap.read()
                if not ret:
                    print("End of webcam stream or failed to read frame.")
                    break

            # Calculate FPS
            new_frame_time = time.time()
            time_elapsed = new_frame_time - prev_frame_time
            fps = 1 / time_elapsed if time_elapsed > 0 else 1

            # Resize frame
            frame_resized = cv2.resize(frame, (WIDTH, HEIGHT))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            # YOLO inference
            results = model(frame_rgb)

            # Draw boxes and calculate speed
            draw_boxes(results, frame_resized, prev_positions, time_elapsed)

            # Display FPS
            cv2.putText(frame_resized, f"FPS: {fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Save output frame
            out.write(frame_resized)

            # Show window
            if show_window:
                cv2.imshow(window_title, frame_resized)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            prev_frame_time = new_frame_time

    finally:
        if cap is not None:
            cap.release()
        out.release()
        if show_window:
            cv2.destroyAllWindows()
