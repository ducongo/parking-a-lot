from filevideostream import FileVideoStream
from detectors import ParkingDetector
from imutils.video import FPS
import imutils
import cv2
import os
import time
from datetime import datetime
import sched
import threading
import sys
import pickle
from threading import RLock

lock = RLock()
vaccant_lots = {"vaccant":{}}
def main():
    
    fps = FPS().start()
    index = 0
    while fvs.isOpened():

        ret, frame = fvs.read()
        index += 1
        frame = imutils.resize(frame, width=1188)
        cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        # print(f'Main id for dict: {id(vaccant_lots)}')
        # print(f'Vaccant lots before: {vaccant_lots}')
        for lot, rect in vaccant_lots["vaccant"].items():
            cv2.rectangle(frame, (rect[0][0],rect[0][1]),(rect[0][2],rect[0][3]),(0,255,0),2)
            # print(f'Vaccant lots: {vaccant_lots}')
        cv2.imshow("Parking CTV camera", frame)
        cv2.waitKey(1)
        fps.update()
        # time.sleep(0.09)
    fps.stop()


def monitor_state():

    pickle_in = open("./parking_layout/parking_map.pickle","rb")
    parking_dict = pickle.load(pickle_in)[0]
    detector = ParkingDetector(parking_dict)
    # print("-----------------------------------------------------")
    # print(pickle.load(pickle_in)[0])
    # print("-----------------------------------------------------")
    while True:
        print(f'Time: {datetime.now().strftime("%H:%M:%S")}')
        time.sleep(1)
        frame = fvs.read()[1]
        # print(f"SHAPE BEFORE: {frame.shape}")
        frame = imutils.resize(frame,width=1188)
        lock.acquire()
        try:
            vaccant_lots["vaccant"] = detector.detect_vaccant_lots(frame, use_corner = False)
        finally:
            lock.release()
        # print(vaccant_lots)
        # print(f'monitor_state id for dict: {id(vaccant_lots)}')



fvs = FileVideoStream("./input/video.mp4")
# Start reading input video file   
fvs.start()

threads = []

main_thread = threading.Thread( target=main)
threads.append(main_thread)
main_thread.start()

monitor_state_thread = threading.Thread( target=monitor_state)
threads.append(monitor_state_thread)
monitor_state_thread.start()


for thread in threads:
    thread.join()



cv2.destroyAllWindows()
fvs.stop()