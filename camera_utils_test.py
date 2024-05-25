#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 20:23:30 2024

@author: daniel
"""

import unittest
from unittest.mock import Mock, patch
from utils import CameraUtils
import cv2
import numpy as np


class TestCameraUtils(unittest.TestCase):
    def test_detect_motion(self):
        frame1 = cv2.imread('test_images/frame_1.png')
        frame2 = cv2.imread('test_images/frame_2.png')
        motion_detected, diff_frame = CameraUtils.detect_movement(frame1, frame2)
        self.assertEqual(motion_detected, True)
        self.assertIsInstance(diff_frame, np.ndarray)
        self.assertEqual(len(diff_frame), 666)
        self.assertEqual(len(diff_frame[0]), 929)

    def test_detect_no_motion(self):
        frame1 = cv2.imread('test_images/frame_1.png')
        motion_detected, diff_frame = CameraUtils.detect_movement(frame1, frame1)
        self.assertEqual(motion_detected, False)
        self.assertIsInstance(diff_frame, np.ndarray)
        self.assertEqual(len(diff_frame), 666)
        self.assertEqual(len(diff_frame[0]), 929)

    @patch('utils.camera_utils.cv2')
    def test_load_cameras(self, mock_cv2):
        dev1 = Mock()
        dev1.name = 'video1'
        dev2 = Mock()
        dev2.name = 'video2'
        with patch('utils.camera_utils.Path.iterdir', return_value=[dev1, dev2]):
            good_camera = Mock()
            good_camera.isOpened.return_value = True
            bad_camera = Mock()
            bad_camera.isOpened.return_value = False
            mock_cv2.VideoCapture.side_effect = [good_camera, bad_camera]
            cameras = [camera for camera in CameraUtils.scan_available_cameras()]
            self.assertEqual(len(cameras), 1)
            self.assertEqual(mock_cv2.VideoCapture.call_count, 2)

    @patch('utils.camera_utils.cv2')
    def test_save_image(self, mock_cv2):
        image = Mock()
        CameraUtils.save_image(image, '/tmp', 'fake_image')
        mock_cv2.imwrite.assert_called_with('/tmp/fake_image.png', image)


if __name__ == "__main__":
    unittest.main()
