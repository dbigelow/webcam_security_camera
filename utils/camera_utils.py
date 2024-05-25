#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 20:10:54 2024

@author: daniel
"""

import cv2
import numpy as np
from pathlib import Path


class CameraUtils:

    def __init__(self):
        pass

    @classmethod
    def detect_movement(cls, frame1, frame2, threshold=1000, kernel=np.ones((9, 9), np.uint8)):
        diff_frame = cv2.subtract(frame1, frame2)
        diff_frame = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)
        diff_frame = cv2.normalize(diff_frame, diff_frame, 0, 255, cv2.NORM_MINMAX)
        diff_frame = cv2.erode(diff_frame, kernel, iterations=2)
        diff_frame = cv2.dilate(diff_frame, kernel, iterations=2)

        frame_norm = cv2.norm(diff_frame, cv2.NORM_L2)
        if frame_norm > threshold:
            return True, diff_frame
        return False, diff_frame

    @classmethod
    def scan_available_cameras(cls, device_path='/dev'):
        p = Path(device_path)
        camera_indexes = sorted([
            int(x.name[5:])
            for x in p.iterdir()
            if 'video' in x.name
        ])
        for i in camera_indexes:
            camera_capture = cv2.VideoCapture(i)
            if camera_capture.isOpened():
                yield camera_capture

    @classmethod
    def save_image(cls, image, directory, img_name, extension=".png"):
        cv2.imwrite("{}/{}{}".format(directory, img_name, extension), image)
