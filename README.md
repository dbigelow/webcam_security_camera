# Webcam-based Security Camera
A basic security camera program using cheap webcams and opencv. Currently this camera will:
1. Save an image to a configured directory every X minutes
  - Save directory is specified in security_camera.cfg under [Logging].log_dir
  - Number of minutes between saves is specified in security_camera.cfg under [Logging].save_interval.
2. Save an image to the log dir when the program ends.
3. Do very basic motion detection, and save a video to the log dir whenever motion is detected.

## Dependencies
* python 3
* python opencv2
* np
(A conda environment definition is included in environment.yml for convenience).

## Running the camera
1. Install the dependencies
```
conda env create -f environment.yml 
```
2. Make any desired changes to the default config file
3. Run the program
```
python3 security_camera.py
```

## TODO
 - [x] Allow the image save interval to be parameterized
 - [X] Auto-detect available webcams
 - [x] Allow '~' or bash variables to be used in the log_dir config instead of requiring the full path.
 - [X] Improve motion detection
 - [ ] Allow options to send images/videos via email, or save to AWS S3
 - [ ] General code clean-up:
  - [X] abstract logical blocks into functions
  - [ ] add docstrings
 - [X] Add unit tests

