from myo import Myo
import sys

last_pose = None

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
  
  if (pose_str == "fist") and (last_pose != myo.getPose()):
    myo.vibrate(Myo.VIBE_MEDIUM)
  
  last_pose = myo.getPose()

def detectPinkyData(myo, callback):
	global last_pose
  
	# Rotation is represented by number of stars (as in hello-myo.exe)
	# (roll_str, pitch_str, yaw_str) = ["*" * int(r) for r in myo.getRotationScaled(18.0)]

	# arm_str = myo.getArmString()

	current_pose = myo.getPoseString()
	if((current_pose == "thumbToPinky") and (last_pose) != myo.getPose()):
		callback();

	last_pose = myo.getPose()

def detectPinky(action_callback):
  myMyo = Myo(callback=detectPinkyData(self, action_callback))
  myMyo.daemon = True
  myMyo.start()

def main():
  myMyo = Myo(callback=printData)
  myMyo.daemon = True
  myMyo.start()
  raw_input(" ")