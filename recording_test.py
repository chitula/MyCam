import cv2
import sys

camera = cv2.VideoCapture(0)
video  = cv2.VideoWriter('output.avi', -1, 25, (640, 480));
while True:
   f,img = camera.read()
   video.write(img)
   cv2.imshow("webcam",img)
   if (cv2.waitKey(5) != -1):
       break
video.release()