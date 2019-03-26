import numpy as np
import cv2
import sys
import evdev
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# global values
recording = False # Inital value

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

def recordVideo(camPipe,fileName):
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

	# while the recording flag is true, record video 
	global recording
	while(recording):
		reg, frame = cap.read()
		out.write(frame)

#	while True:
#		ret, frame = cap.read()
#		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#		out.write(frame)
#		if(get_key(device,"KEY_B") == True):
#			print("quit key on button pressed")
#			break

	print("stopped recording")
	# clean up when we're done
	cap.release()
	out.release()

def on_connect(client, userdata,flags,rc):
	print("connected with code:",str(rc))
	client.subscribe("/button")

def on_message(client,userdata,msg):
	global recording
	#print(msg.topic," ",str(msg.payload))
	if(msg.topic == "/button" and str(msg.payload)):
		recording = not recording

if (__name__ == "__main__"):
	# setup the
	print("main")
#	remote = find_device()
	pipe = "nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
	count = 0;
	# setup the mqtt client
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("192.168.1.14",1883,60)
	client.loop_start() # non blocking start

	global recording
	#recording = False

	while(True):
		if(recording == True):
			#print("recording")
			fname = "video_" + str(count) + ".avi"
			recordVideo(pipe,fname)
			count = count + 1
		#else:
			#print("not recording")

#	while True:
#		if(get_key(remote,"KEY_B")):
#			print("started recording #",count)
#			fname = "video_"+str(count) + ".avi"
#			recordVideo(pipe,fname,remote)
#			count = count + 1
