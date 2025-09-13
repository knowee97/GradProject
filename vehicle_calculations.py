import time
import cv2
import numpy as np
from parameters_config import *

def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculateFPS(prev_frame_time):
    new_frame_time = time.time()
    time_elapsed = new_frame_time - prev_frame_time
    fps = 1 / time_elapsed if time_elapsed > 0 else 1
    return fps, new_frame_time

def trackMPH(prev_positions, track_id, center, time_elapsed, frame_resized,x1,y1):
    if prev_positions[track_id] is not None :
        prev_center = prev_positions[track_id]
        distance_pixels = euclidean_distance(center, prev_center)
        distance_meters = distance_pixels * pixels_to_meters

        speed_mps = distance_meters / time_elapsed
        speed_mph = speed_mps * MPS_2_MPH_FACTOR

        cv2.putText(frame_resized, f"Speed: {speed_mph:.2f} mph", (x1, y1 - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    prev_positions[track_id] = center