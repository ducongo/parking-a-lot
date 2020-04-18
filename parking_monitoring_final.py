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
from zipfile import ZipFile

lock = RLock()
vaccant_lots = {"vaccant":{}}
total_spots = 0
parking_dict = {}
stop_threads = False


#Stops components in use and sets values to stop threads
def endProgram():
    global fvs, stop_threads

    stop_threads = True
    cv2.destroyAllWindows()
    fvs.stop()
    exit()


def main():
    fps = FPS().start()
    while fvs.isOpened():
        ret, frame = fvs.read()
        if (frame is None):
            break
        frame = imutils.resize(frame, width=1188)
        frame = displayLabels(frame)    #Show all labels

        count = 0
        for lot, rect in vaccant_lots["vaccant"].items():
            count += 1
            cv2.rectangle(frame, (rect[0][0],rect[0][1]),(rect[0][2],rect[0][3]),(0,255,0),2)
            cv2.putText(frame, "{}".format(lot), (1095, 70 + (20 * count)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

        cv2.imshow("Parking CTV camera", frame)
        key = cv2.waitKey(1)
        if (key > 0):
            break
        fps.update()
        #time.sleep(0.05)

    fps.stop()
    endProgram()


def monitor_state():
    global total_spots, parking_dict

    with ZipFile('./parking_layout/parking_map_pickle.zip', 'r') as pickleZip:
        pickleZip.extractall('./parking_layout/')

    pickle_in = open("./parking_layout/parking_map.pickle","rb")
    parking_dict = pickle.load(pickle_in)[0]
    total_spots = len(parking_dict[0]) + len(parking_dict[1]) + len(parking_dict[2])
    detector = ParkingDetector(parking_dict)

    while not stop_threads:
        #print(f'Time: {datetime.now().strftime("%H:%M:%S")}')
        frame = fvs.read()[1]
        frame = imutils.resize(frame,width=1188)
        lock.acquire()
        try:
            vaccant_lots["vaccant"] = detector.detect_vaccant_lots(frame, use_corner = False)
        finally:
            lock.release()
        time.sleep(0.5)


#Shows labels for parking spots, as well as stats on the sides of the video
def displayLabels(frame):
    occupied_spots = total_spots - len(vaccant_lots["vaccant"].items())
    cv2.putText(frame, "Press any key to exit", (850, 620), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
    cv2.putText(frame, "Parking Lot Capacity: {}/{}".format(occupied_spots, total_spots), (130, 620), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
    cv2.putText(frame, "Vacant", (1080, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
    cv2.putText(frame, "Spots:", (1090, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

    #Label each parking spot
    for level in parking_dict:
        for lot, rect in parking_dict[level].items():
            x_value = rect[0] + 3
            y_value = rect[1] - 15
            if (int(lot[2:]) > 23):
                y_value = rect[3] + 15
            cv2.putText(frame, "{}".format(lot), (x_value, y_value), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 0), 1)
            
    return frame


# Start reading input video file   
fvs = FileVideoStream("./input/video_black_bars.mp4")
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