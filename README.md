# Webcam-based Security Camera
A basic security camera program using cheap webcams and opencv. Currently this camera will:
1. Save an image to the directory specified in the SECURITY_CAMERA_LOG_DIR environment variable once every X minutes, where X is defined by the environment variable IMAGE_SAVE_INTERVAL.
2. Save an image to SECURITY_CAMERA_LOG_DIR when the program ends.
3. Do very basic motion detection, and save a video to SECURITY_CAMERA_LOG_DIR whenever motion is detected.

## Dependencies
* python 3
* python opencv2
* np

## Running the camera
1. Install the dependencies
```
pip install opencv-python python-dotenv numpy np
```
2. Make any desired changes to the default config file
  * save_interval: the interval at which to save a snapshot of the security camera feed (in minutes).
  * log_dir: the directory in which the snapshots (and any motion-detected video) will be saved. This directory will be created if it does not already exist.
3. Run the program
```
python3 security_camera.py
```

## TODO
 - [x] Allow the image save interval to be parameterized
 - [X] Auto-detect available webcams
 - [x] Allow '~' or bash variables to be used in the SECURITY_CAMERA_LOG_DIR environment variable instead of requiring the full path.
 - [X] Improve motion detection
 - [ ] Allow options to send images/videos via email, or save to AWS S3
 - [ ] General code clean-up (abstract logical blocks into functions, add docstrings, etc)
 - [ ] Add unit tests

