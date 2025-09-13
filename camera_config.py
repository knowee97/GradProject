import time
import cv2
from vehicle_calculations import *
from parameters_config import *


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



def runWebCam(prev_positions, prev_frame_time):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise Exception("Error: Could not open webcam.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                raise Exception("Error: Couldn't read frame from Webcam.")

            # Capture time at start of frame
            new_frame_time = time.time()
            time_elapsed = new_frame_time - prev_frame_time
            fps = 1 / time_elapsed if time_elapsed > 0 else 1

            # Resize and preprocess
            frame_resized = cv2.resize(frame, (WIDTH, HEIGHT))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            # Inference
            results = model(frame_rgb)

            # Draw boxes and calculate speed
            draw_boxes(results, frame_resized, prev_positions, time_elapsed)

            # Display FPS
            cv2.putText(frame_resized, f"FPS: {fps:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show result
            cv2.imshow("Webcam YOLO Detection", frame_resized)

            # Update time after drawing
            prev_frame_time = new_frame_time

            # Break condition
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
