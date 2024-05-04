# Webcam-based Security Camera
A basic security camera program using cheap webcams and opencv. Currently this camera will:
1. Save an image to the directory specified in the SECURITY_CAMERA_LOG_DIR environment variable once every 5 minutes.
2. Save an image to SECURITY_CAMERA_LOG_DIR when the program ends.
3. Do very basic motion detection, and save a video to SECURITY_CAMERA_LOG_DIR whenever motion is detected.

## Dependencies
* python 3
* python opencv2
* np
* dotenv

## Running the camera
1. Install the dependencies
```
pip install opencv-python python-dotenv numpy np
```
2. Set up your environment (you can specify SECURITY_CAMERA_LOG_DIR in a .env file if you want something more persistent than exporting the environment variable).
```
mkdir ~/security_camera_logs
export SECURITY_CAMERA_LOG_DIR=~/security_camera_logs
```
3. Run the program
```
python3 security_camera.py
```

## TODO
 - [ ] Allow the image save interval to be parameterized
 - [ ] Auto-detect available webcams
 - [x] Allow '~' or bash variables to be used in the SECURITY_CAMERA_LOG_DIR environment variable instead of requiring the full path.
 - [ ] Improve motion detection
 - [ ] Allow options to send images/videos via email, or save to AWS S3

