import evdev

class remote(object):
	def __init__(self,name="FM8PU83-Ver0E-0000"):
		self.device = None
		devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
		for device in devices:
			if(device.name.find(name) > -1):
				#print(device.path)
				self.device = evdev.InputDevice(device.path)
				break		
	
	def show_device(self):
		print("device: ",self.device)	

	def monitor(self,callfunct,key):

		# if the defice is a none type then just notify the user and return 
		if(self.device == None):
			print("no device is connected")
			return

		# read keys, wait until desired key is found
		for event in self.device.read_loop():
			if event.type == evdev.ecodes.EV_KEY:
				key_event=evdev.categorize(event)
				if(key_event.keystate == 1 and key_event.keycode == key):
					callfunct() # call the callback	
					break			

	# run the callback until the key given in the key prarameter is set, then stop calling it.  
	def run_untilkey(self,callfunct,key):	
		
		# make sure there's a device connected 
		if(self.device == None):
			print("no device connected")
			return 

		#read keys, wait until the device is found 
		for event in self.device.read_loop():
			if(event.type == evdev.ecodes.EV_KEY):
				key_event=evdev.categorize(event)
				if(key_event.keystate == 1 and key_event.keycode == key):
					break
				else:
					callfunct()

	# Does a non blocking check for an event and returns true if there's a key pressed 
	def get_key(self,key):
		
		keyed = False

		if(self.device == None):
			print("no device connected")
			return

		if(event.type == evdev.ecodes.EV_KEY):
			key_event=evdev.categorize(event)
			if(key_event.keystate == 1 and key_event.keycode == key):
				keyed = True

		return keyed
		



