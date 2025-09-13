import time
from collections import defaultdict

from parameters_config import *
from vehicle_calculations import *
from camera_config import *



def main():
    LIVE_VIDEO = False
    LOCAL_VIDEO = True
    
    if LIVE_VIDEO is True:
        prev_frame_time = time.time()
        prev_positions = defaultdict(lambda: None)
        runWebCam(prev_positions, prev_frame_time)

    elif LOCAL_VIDEO is True:
        VIDEO_PATH = r'Videos\BenchmarkVideo_Cut.mp4'
        prev_frame_time = time.time()
        prev_positions = defaultdict(lambda: None)
        emulate_webcam = True

        if emulate_webcam:
            runWebCam(prev_positions, prev_frame_time, VIDEO_PATH ,video = True, show_window=True)
        
        else:
            runWebCam(prev_positions, prev_frame_time, VIDEO_PATH ,video = True, show_window=False)

         
if __name__ == "__main__":
        main()
