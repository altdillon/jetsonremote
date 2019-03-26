

import numpy as np
import cv2
import sys
import evdev
#from inputmanager import *

def find_device(name="FM8PU83-Ver0E-0000"):
	device = None
	devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
	for device in devices:
		if(device.name.find(name) > -1):
			#print(device.path)
			device = evdev.InputDevice(device.path)
			break			

	return device 

def get_key(device,key):
		
	keyed = False

	if(device == None):
		print("no device connected")
		return False
	
	event = device.read_one()
	if(event != None):
		if(event.type == evdev.ecodes.EV_KEY):
			key_event=evdev.categorize(event)
			if(key_event.keystate == 1 and key_event.keycode == key):
				keyed = True

	return keyed

def recordVideo(camPipe,fileName,device):
	# open the camera 
	cap = cv2.VideoCapture(camPipe)
	
	# make sure that the camera is open 
	if(cap.isOpened() == False):
		print("camera did not start")
		return

	# define the output file
	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))
	out = cv2.VideoWriter(fileName,cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
	print("now recording...")
	
	while True:
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		out.write(frame)
		if(get_key(device,"KEY_B") == True):
			print("quit key on button pressed")
			break
	


	# clean up when we're done
	cap.release()
	out.release()



if (__name__ == "__main__"):
	print("main")
	remote = find_device()
	pipe = "nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
	count = 0;
	while True:
		if(get_key(remote,"KEY_B")):
			print("started recording #",count)
			fname = "video_"+str(count) + ".avi"
			recordVideo(pipe,fname,remote)
			count = count + 1
		
