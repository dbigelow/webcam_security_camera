import cv2
import np
from datetime import datetime, timedelta
from collections import deque
from dotenv import load_dotenv
import os

load_dotenv()

builtin = cv2.VideoCapture(0)
usb = cv2.VideoCapture(2)

width = int(builtin.get(cv2.CAP_PROP_FRAME_WIDTH) * 2)
height = int(usb.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = None

image_save_interval = timedelta(minutes=5)
timer_start = datetime.now()
frame_memory = deque()
recording = False
video_frame_counter = 0

while(True):
	ret1, builtinFrame = builtin.read()
	ret2, usbFrame = usb.read()
	combined = np.concatenate((builtinFrame, usbFrame), axis=1)
	frame_memory.append(combined)

	if(len(frame_memory) > 5):
		old_frame = frame_memory.popleft()
		diff_frame = cv2.subtract(old_frame, combined)
		frame_norm = cv2.norm(diff_frame, cv2.NORM_L2)
		
		combined2 = np.concatenate((combined, diff_frame), axis = 0);
		cv2.imshow('webcam feed', combined2)

		
		if(recording):
			out.write(old_frame)
			print("continuing recording")

		print(frame_norm)

		if(frame_norm > 9000):
			if(not recording) :
				now = datetime.now()
				timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
				videoName = os.getenv('SECURITY_CAMERA_LOG_DIR') + timestamp + '.avi'
				print(videoName)
				out = cv2.VideoWriter(videoName, fourcc, 7.0, size)
								
				out.write(old_frame)
				print("started recording")
			
			video_frame_counter = 0
			recording = True

		else:
			if(video_frame_counter <= 10 and recording):
				video_frame_counter += 1
			elif (video_frame_counter > 10 and recording):
				video_frame_counter = 0
				out.release()
				recording = False
				print("Stopped recording")

	
	if((datetime.now() - timer_start) > image_save_interval): 
		timer_start = datetime.now()
		timestamp = timer_start.strftime("%Y-%m-%d-%H-%M-%S")
		cv2.imwrite(os.getenv('SECURITY_CAMERA_LOG_DIR') + timestamp + ".png", combined)

	if cv2.waitKey(1) & 0xff == ord('q'):
		timer_start = datetime.now()
		timestamp = timer_start.strftime("%Y-%m-%d-%H-%M-%S")
		cv2.imwrite(os.getenv('SECURITY_CAMERA_LOG_DIR') + timestamp + ".png", combined)
		break

builtin.release()
usb.release()
cv2.destroyAllWindows()
