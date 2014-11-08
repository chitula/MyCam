import cv2
import sys
import serial
import noah_test
from myo import Myo
from collections import deque

last_pose = None
imgCount = 0

def printData(myo):
	global last_pose

	# Rotation is represented by number of stars (as in hello-myo.exe)
	# (roll_str, pitch_str, yaw_str) = ["*" * int(r) for r in myo.getRotationScaled(18.0)]

	# arm_str = myo.getArmString()

	pose_str = myo.getPoseString()

	# Print out the rotation and arm state on the same line each update
	sys.stdout.write('\r[{:15s}]'.format(
		# roll_str,
		# pitch_str,
		# yaw_str,
		# arm_str, 
		pose_str,
	)
	)

	if((pose_str == "fist") and (last_pose != myo.getPose())):
		myo.vibrate(Myo.VIBE_MEDIUM)

	last_pose = myo.getPose()

def detectPinky(myo):
	global last_pose

	# Rotation is represented by number of stars (as in hello-myo.exe)
	# (roll_str, pitch_str, yaw_str) = ["*" * int(r) for r in myo.getRotationScaled(18.0)]

	# arm_str = myo.getArmString()

	pose_str = myo.getPoseString()

	if((pose_str == "thumbToPinky") and (last_pose) != myo.getPose()):
		myo.vibrate(Myo.VIBE_MEDIUM)
		main2()

	last_pose = myo.getPose()

def main():
	myMyo = Myo(callback=detectPinky)
	myMyo.daemon = True
	myMyo.start()
	raw_input(" ")

def main2():
	myMyo = Myo(callback=startRecording)
	myMyo.daemon = True
	myMyo.start()
	raw_input(" ")

def stopRecording():
	# When everything is done, release the capture
	video_capture.release()
	out.release()
	cv2.destroyAllWindows()

def startRecording(myo):

	# Capture frame-by-frame
	ret, frame = video_capture.read()   # frame is single frame, ignore ret

	# ---------- Myo stuff! ---------- #
	global last_pose
	global imgCount

	# Rotation is represented by number of stars (as in hello-myo.exe)
	# (roll_str, pitch_str, yaw_str) = ["*" * int(r) for r in myo.getRotationScaled(18.0)]

	# arm_str = myo.getArmString()

	pose_str = myo.getPoseString()
	sys.stdout.write('\r[{:15s}]'.format(
		# roll_str,
		# pitch_str,
		# yaw_str,
		# arm_str, 
		pose_str,
	)
	)

	if((pose_str == "waveOut") and (last_pose) != myo.getPose()):
		myo.vibrate(Myo.VIBE_SHORT)
		cv2.imwrite("img_" + str(imgCount) + ".jpg", frame)
		imgCount = imgCount + 1;

	if((pose_str == "fist") and (last_pose) != myo.getPose()):
		myo.vibrate(Myo.VIBE_MEDIUM)
		stopRecording()

	last_pose = myo.getPose()

	# --------- End Myo stuff ---------- #




	# print ser.readline()

	# Write frame to video file
	out.write(frame)

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(125, 125),
		flags=cv2.cv.CV_HAAR_SCALE_IMAGE		# CV_HAAR_SCALE_IMAGE
	)

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		x_face = x+w/2
		y_face = y+h/2


		x_queue.append(x_face)
		if( len(x_queue) > 10 ):
			x_queue.popleft()

		y_queue.append(y_face)
		if( len(y_queue) > 10 ):
			y_queue.popleft()

		x_total = 0
		y_total = 0

		for x_value in x_queue:
			x_total = x_total + x_value

		for y_value in y_queue:
			y_total = y_total + y_value

		x_avg = x_total/len(x_queue)
		y_avg = y_total/len(y_queue)

		# print x_avg, ", ", y_avg

		# detect leaving frame along x direction
		if( abs(x_ctr - x_face) > x_offset ):
			cv2.rectangle(frame, (x_ctr-x_offset, y_ctr-y_offset), (x_ctr+x_offset, y_ctr+y_offset), (0, 0, 255), 2)
			servoRotateDeg = ((x_face - x_ctr))/pixelToServoScale;
			# print servoRotateDeg

			if(servoRotateDeg > 0):
				# servoRotateString = '+' + str(servoRotateDeg);
				servoRotateString = '+1'
				ser.write(servoRotateString)
			elif(servoRotateDeg < 0):
				# servoRotateString = '-' + str(servoRotateDeg);
				servoRotateString = '-1'
				ser.write(servoRotateString)
			else:
				servoRotateString = '+0'
				ser.write(servoRotateString)


	# Display the resulting frame
	cv2.imshow('Video', frame)

	if (cv2.waitKey(5) != -1):
		stopRecording()

def CV_FOURCC(c1, c2, c3, c4):
	return (int(c1.encode("hex")) & 255) + ((int(c2.encode("hex")) & 255) << 8) + ((int(c3.encode("hex")) & 255) << 16) + ((int(c4.encode("hex")) & 255) << 24)

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)     # may want to change paramater number to get proper webcam
out = cv2.VideoWriter('output.avi',-1, 20, (640,480))

ser = serial.Serial(11, 9600)
x_queue = deque()
y_queue = deque()

pixelToServoScale = 20

x_ctr = 320
y_ctr = 240

x_offset = 100
y_offset = 100

main()