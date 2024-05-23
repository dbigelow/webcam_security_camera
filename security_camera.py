import cv2
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import os
from configparser import ConfigParser
from pathlib import Path
from functools import reduce


def load_config(config_file_name):
    config = ConfigParser()
    config.read(config_file_name)
    return config


def camera_loader():
    p = Path('/dev')
    camera_indexes = sorted([
        int(x.name[5:])
        for x in p.iterdir()
        if 'video' in x.name
    ])
    for i in camera_indexes:
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            yield cap


def detect_movement(initial_image, next_image):
    diff_frame = cv2.subtract(initial_image, next_image)
    diff_frame = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)
    diff_frame = cv2.normalize(diff_frame, diff_frame, 0, 255, cv2.NORM_MINMAX)
    diff_frame = cv2.erode(diff_frame, kernel, iterations=2)
    diff_frame = cv2.dilate(diff_frame, kernel, iterations=2)

    frame_norm = cv2.norm(diff_frame, cv2.NORM_L2)
    if frame_norm > 1000:
        return True, diff_frame
    return False, diff_frame


config = load_config('security_camera.cfg')


camera_loader = camera_loader()
cameras = [camera for camera in camera_loader]
if len(cameras) < 1:
    raise RuntimeError("No available webcams")

total_width = reduce(lambda width1, width2: width1 + width2,
                     [
                         int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
                         for camera in cameras
                     ])
height = int(cameras[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (total_width, height)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

video_writer = None

log_config = config['Logging']
image_save_interval = timedelta(minutes=int(log_config['save_interval']))
timer_start = datetime.now()
frame_buffer = deque()
recording = False
video_frame_counter = 0

log_dir = config['Logging']['log_dir']
log_dir = log_dir if log_dir.endswith('/') else log_dir + '/'
log_dir = os.path.expanduser(os.path.expandvars(log_dir))
Path(log_dir).mkdir(parents=True, exist_ok=True)

kernel = np.ones((9, 9), np.uint8)

while True:
    frames = [camera.read()[1] for camera in cameras]
    combined = np.concatenate(frames, axis=1)
    frame_buffer.append(combined)

    if len(frame_buffer) > 5:

        old_frame = frame_buffer.popleft()
        movement_detected, diff_frame = detect_movement(old_frame, combined)

        cv2.imshow('webcam feed', combined)
        cv2.imshow('frame diff', diff_frame)

        if recording:
            video_writer.write(old_frame)
            print("continuing recording")

        if movement_detected:
            if not recording:
                now = datetime.now()
                timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
                videoName = log_dir + timestamp + '.avi'
                video_writer = cv2.VideoWriter(videoName, fourcc, 7.0, size)

                video_writer.write(old_frame)
                print("started recording")

            video_frame_counter = 0
            recording = True

        else:
            if video_frame_counter <= 10 and recording:
                video_frame_counter += 1
            elif video_frame_counter > 10 and recording:
                video_frame_counter = 0
                video_writer.release()
                recording = False
                print("Stopped recording")

    if (datetime.now() - timer_start) > image_save_interval:
        timer_start = datetime.now()
        timestamp = timer_start.strftime("%Y-%m-%d-%H-%M-%S")
        cv2.imwrite(log_dir + timestamp + ".png", combined)

    if cv2.waitKey(1) & 0xff == ord('q'):
        timer_start = datetime.now()
        timestamp = timer_start.strftime("%Y-%m-%d-%H-%M-%S")
        cv2.imwrite(log_dir + timestamp + ".png", combined)
        break

for camera in cameras:
    camera.release()
cv2.destroyAllWindows()
