# from imageai.Detection import VideoObjectDetection
from imageai.Detection import ObjectDetection
from filevideostream import FileVideoStream
from imutils.video import FPS
import imutils
import cv2
import os
import time
from datetime import datetime
import sched
import threading
import sys

# # import the Queue class from Python 3
# if sys.version_info >= (3, 0):
#     from queue import Queue

# # otherwise, import the Queue class for Python 2.7
# else:
#     from Queue import Queue


def main():
    
    fps = FPS().start()
    while fvs.isOpened():

        ret, frame = fvs.read()
        frame = imutils.resize(frame, width=1200)
        cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Parking CTV camera", frame)
        cv2.waitKey(1)
        fps.update()
    fps.stop()


def monitor_state():
    
    
    while True:
        print(f'Time: {datetime.now().strftime("%H:%M:%S")}')
        time.sleep(5)
        detected_copy, output_objects_array, detected_objects_image_array = detector.detectObjectsFromImage(
            input_image=fvs.read()[1], input_type="array", output_type="array", extract_detected_objects=True)
        # print(type(detection))
        detected_copy = imutils.resize(detected_copy, width=900)
        cv2.imshow("Parking monitor detections", detected_copy)
        cv2.waitKey(1)


use_tinymodel = False
model_path ="./models/yolo-tiny.h5"
detector = ObjectDetection()

if not use_tinymodel:
    model_path = "./models/yolo.h5"
    detector.setModelTypeAsYOLOv3()
else:
    detector.setModelTypeAsYOLOv3()

detector.setModelPath(model_path)
detector.loadModel()

fvs = FileVideoStream("./input/parking-lot.mp4")
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