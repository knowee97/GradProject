from picamera2 import Picamera2
from camera_config import runWebCam
from collections import defaultdict
import time

def main():
    prev_frame_time = time.time()
    prev_positions = defaultdict(lambda: None)

    picam2 = Picamera2()
    picam2.start()

    try:
        runWebCam(prev_positions, prev_frame_time, VIDEO_PATH="", video=False, show_window=True, camera=picam2)
    finally:
        picam2.stop()

if __name__ == "__main__":
    main()
