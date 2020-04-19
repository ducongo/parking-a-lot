from imageai.Detection import VideoObjectDetection
import os
import time
from filevideostream import FileVideoStream
import cv2
import threading
import sys
from imutils.video import FPS
# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue


execution_path = os.getcwd()

frames = Queue(maxsize=300)

fvs = FileVideoStream("./input/parking-lot.mp4", queue_size=300)

def forFrame(frame_number, output_array, output_count, frame):
    frames.put(frame)
    print("Running - Frame Number : " , frame_number)
    # print("Output for each object : ", output_array)
    # print("Output count for unique objects : ", output_count)
    # print("------------END OF A FRAME --------------")
    # print("Running")
    # cv2.imshow("Frame", frame)
    # cv2.waitKey(1)


def detection():
    video_detector = VideoObjectDetection()
    # video_detector.setModelTypeAsYOLOv3()
    # video_detector.setModelPath(os.path.join(execution_path, "./models/yolo.h5"))

    video_detector.setModelTypeAsTinyYOLOv3()
    video_detector.setModelPath(os.path.join(execution_path, "./models/yolo-tiny.h5"))
    video_detector.loadModel(detection_speed="fast")
    fvs.start()

    time.sleep(1)

    video_detector.detectObjectsFromVideo(camera_input=fvs, save_detected_video=False ,  frames_per_second=20, per_frame_function = forFrame, minimum_percentage_probability=30, return_detected_frame=True)


def display():
    print("Parking monitoring about to start......")
    # start the FPS timer
    fps = FPS().start()
    time.sleep(120)
    while True:

        if frames.qsize() > 10:
            print(f'QUEUE SUZE: {frames.qsize()}')
            # frame = imutils.resize(frames.get(), width=1200)
            frame = frames.get()
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            fps.update()

        time.sleep(0.001)
    
    cv2.destroyAllWindows()
    fvs.stop()
    

# print("Setting up model.....")

# video_detector = VideoObjectDetection()
# video_detector.setModelTypeAsYOLOv3()
# video_detector.setModelPath(os.path.join(execution_path, "./models/yolo.h5"))

# video_detector.setModelTypeAsTinyYOLOv3()
# video_detector.setModelPath(os.path.join(execution_path, "./models/yolo-tiny.h5"))
# video_detector.loadModel(detection_speed="fast")
# print("Model setup completed.....")

# print("Mounting video input")
# print("Mounting completed")

# time.sleep(1.0)
# video_detector.detectObjectsFromVideo(camera_input=fvs, save_detected_video=False ,  frames_per_second=20, per_frame_function = forFrame, minimum_percentage_probability=30, return_detected_frame=True)

# cv2.destroyAllWindows()

threads = []

detection_thread = threading.Thread( target=detection)
threads.append(detection_thread)
detection_thread.start()

display_thread = threading.Thread( target=display)
threads.append(display_thread)
display_thread.start()


for thread in threads:
    thread.join()

# print("Parking monitoring about to start......")
# time.sleep(20)
# thread.start()
# print("Parking monitoring about to started......")