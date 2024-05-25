import cv2
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import os
from configparser import ConfigParser
from pathlib import Path
from functools import reduce
from utils import CameraUtils
import logging


def load_config(config_file_name):
    config = ConfigParser()
    config.read(config_file_name)
    return config


config = load_config('security_camera.cfg')
logging.config.fileConfig(config)

cameras = [camera for camera in CameraUtils.scan_available_cameras()]
if len(cameras) < 1:
    raise RuntimeError("No available webcams")

total_width = reduce(lambda width1, width2: width1 + width2,
                     [int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)) for camera in cameras])
height = int(cameras[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
video_size = (total_width, height)
video_codec = cv2.VideoWriter_fourcc(*'XVID')

image_save_interval = timedelta(minutes=int(config['Logging']['save_interval']))
timer_start = datetime.now()
frame_buffer = deque()
recording = False

log_dir = Path(os.path.expanduser(os.path.expandvars(config['Logging']['log_dir'])))
log_dir.mkdir(parents=True, exist_ok=True)

while True:
    frames = [camera.read()[1] for camera in cameras]
    current_frame = np.concatenate(frames, axis=1)
    frame_buffer.append(current_frame)

    if len(frame_buffer) > 5:

        old_frame = frame_buffer.popleft()
        movement, diff_frame = CameraUtils.detect_movement(old_frame, current_frame)

        cv2.imshow('webcam feed', current_frame)
        if logging.root.handlers[0].level <= logging.DEBUG:
            cv2.imshow('frame diff', diff_frame)

        if movement:
            if not recording:
                now = datetime.now()
                videoName = "{}/{}.avi".format(log_dir, now.strftime("%Y-%m-%d-%H-%M-%S"))
                video_writer = cv2.VideoWriter(videoName, video_codec, 7.0, video_size)

                video_writer.write(old_frame)
                logging.debug("started recording")

            video_frame_counter = 0
            recording = True
        else:
            if recording and video_frame_counter <= 10:
                video_frame_counter += 1
            elif recording and video_frame_counter > 10:
                video_frame_counter = 0
                video_writer.release()
                recording = False
                logging.debug("Stopped recording")

        if recording:
            video_writer.write(old_frame)
            logging.debug("continuing recording")

    if (datetime.now() - timer_start) > image_save_interval:
        timer_start = datetime.now()
        CameraUtils.save_image(current_frame, log_dir, timer_start.strftime("%Y-%m-%d-%H-%M-%S"))

    if cv2.waitKey(1) & 0xff == ord('q'):
        timer_start = datetime.now()
        CameraUtils.save_image(current_frame, log_dir, timer_start.strftime("%Y-%m-%d-%H-%M-%S"))
        break

for camera in cameras:
    camera.release()
cv2.destroyAllWindows()
