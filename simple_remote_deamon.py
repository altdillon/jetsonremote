import os
import evdev
import daemon
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# functions fur running the button
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

# setup the callbacks for mpqtt proccesses
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
	client.subscribe("/button")
	client.subscribe("/names")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    a = 1


def runLoop():
	# get the device
	device = find_device()
	

	# start up the mqtt client
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("192.168.1.14",1883,60)
	client.loop_start()

	while(True):
		if(get_key(device,"KEY_B")):
			publish.single("/button","pushed",hostname="192.168.1.14")

if(__name__ == "__main__"):
	with daemon.DaemonContext():
		runLoop()
