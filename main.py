import time
from collections import defaultdict

from parameters_config import *
from vehicle_calculations import *
from camera_config import *



def main():
    prev_frame_time = time.time()
    prev_positions = defaultdict(lambda: None)
    #VIDEO_PATH = r'Videos\BenchmarkVideo_Cut.mp4'
    ##VIDEO_PATH = r'/home/noe_ee/GradProject/Videos/BenchmarkVideo_Cut.mp4'
    VIDEO_PATH = ""
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        cap.release()
        runWebCam(prev_positions, prev_frame_time, VIDEO_PATH ,video = False, show_window=True)

    else:
        cap.release()
        #VIDEO_PATH = r'/home/noe_ee/GradProject/Videos/BenchmarkVideo_Cut.mp4'
        #runWebCam(prev_positions, prev_frame_time, VIDEO_PATH ,video = True, show_window=True)
        

if __name__ == "__main__":
        main()
