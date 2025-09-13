import time
from collections import defaultdict

from parameters_config import *
from vehicle_calculations import *
from camera_config import *



def main():

    LIVE_VIDEO = True

    if LIVE_VIDEO is True:
        prev_frame_time = time.time()
        prev_positions = defaultdict(lambda: None)
        runWebCam(prev_positions, prev_frame_time)

if __name__ == "__main__":
        main()
