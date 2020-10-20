# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
import argparse
import datetime
import time
import imutils
from imutils.video import VideoStream
import cv2
import numpy as np

from motion_detection import motion_detection_background_substraction

background_refresh_rate = 2 * 60 # 2 min

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
background = None
start_time = time.time()
refresh_background = start_time + background_refresh_rate

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied text
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		break

	current_time = time.time()

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	
	height, width, channels = frame.shape
	mask = np.zeros((height, width, channels), dtype=np.uint8)
	mask[:] = (0,0,255)

	# if the first frame is None, initialize it
	
	if background is None or refresh_background <= current_time:
		background = gray
		refresh_background = current_time + background_refresh_rate
		print("Background refreshed")
		continue
	
	motion, min_area, max_area = motion_detection_background_substraction(background, gray, args["min_area"], True)
	
	if motion:
		frame =  cv2.addWeighted(frame,0.5,mask,0.5,0)

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Min Area: {} Max Area: {}".format(min_area, max_area), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()