import screen_brightness_control as sbcontrol
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume 
import pyautogui 
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume 
from ctypes import cast, POINTER 
from comtypes import CLSCTX_ALL
from file1 import Gest 

class Controller: 
	tx_old = 0
	ty_old = 0
	trial = True
	flag = False
	grabflag = False
	pinchmajorflag = False
	pinchminorflag = False
	pinchstartxcoord = None
	pinchstartycoord = None
	pinchdirectionflag = None
	prevpinchlv = 0
	pinchlv = 0
	framecount = 0
	prev_hand = None
	pinch_threshold = 0.3
	def getpinchylv(hand_result): 
		dist = round((Controller.pinchstartycoord - hand_result.landmark[8].y)*10,1) 
		return dist 
	def getpinchxlv(hand_result): 
		dist = round((hand_result.landmark[8].x - Controller.pinchstartxcoord)*10,1) 
		return dist 
	def changesystembrightness(): 
		print("brightness")
		currentBrightnessLv = sbcontrol.get_brightness()/100.0
		
		print(Controller.pinchlv)
		currentBrightnessLv += Controller.pinchlv/20.0
		print("brightness11")
		if currentBrightnessLv > 1.0: 
			currentBrightnessLv = 1.0
		elif currentBrightnessLv < 0.0: 
			currentBrightnessLv = 0.0
		print("brightness22",currentBrightnessLv)	
		sbcontrol.fade_brightness(int(100*currentBrightnessLv) , start = sbcontrol.get_brightness())
		print(sbcontrol.get_brightness())
	def changesystemvolume(): 
		print("volume")
		devices = AudioUtilities.GetSpeakers() 
		interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None) 
		volume = cast(interface, POINTER(IAudioEndpointVolume)) 
		currentVolumeLv = volume.GetMasterVolumeLevelScalar() 
		currentVolumeLv += Controller.pinchlv/20.0
		if currentVolumeLv > 1.0: 
			currentVolumeLv = 1.0
		elif currentVolumeLv < 0.0: 
			currentVolumeLv = 0.0
		volume.SetMasterVolumeLevelScalar(currentVolumeLv, None) 
	def scrollVertical(): 
		pyautogui.scroll(120 if Controller.pinchlv>0.0 else -120)	 
	def scrollHorizontal(): 
		pyautogui.keyDown('shift') 
		pyautogui.keyDown('ctrl') 
		pyautogui.scroll(-120 if Controller.pinchlv>0.0 else 120) 
		pyautogui.keyUp('ctrl') 
		pyautogui.keyUp('shift') 
	# Locate Hand to get Cursor Position 
	# Stabilize cursor by Dampening 
	def get_position(hand_result): 
		point = 9
		position = [hand_result.landmark[point].x ,hand_result.landmark[point].y] 
		sx,sy = pyautogui.size() 
		x_old,y_old = pyautogui.position() 
		x = int(position[0]*sx) 
		y = int(position[1]*sy) 
		if Controller.prev_hand is None: 
			Controller.prev_hand = x,y 
		delta_x = x - Controller.prev_hand[0] 
		delta_y = y - Controller.prev_hand[1] 
		distsq = delta_x**2 + delta_y**2
		ratio = 1
		Controller.prev_hand = [x,y] 
		if distsq <= 25: 
			ratio = 0
		elif distsq <= 900: 
			ratio = 0.07 * (distsq ** (1/2)) 
		else: 
			ratio = 2.1
		x , y = x_old + delta_x*ratio , y_old + delta_y*ratio 
		return (x,y) 
	def pinch_control_init(hand_result): 
		Controller.pinchstartxcoord = hand_result.landmark[8].x 
		Controller.pinchstartycoord = hand_result.landmark[8].y 
		Controller.pinchlv = 0
		Controller.prevpinchlv = 0
		Controller.framecount = 0
	# Hold final position for 5 frames to change status 
	def pinch_control(hand_result, controlHorizontal, controlVertical): 
		if Controller.framecount == 5: 
			Controller.framecount = 0
			Controller.pinchlv = Controller.prevpinchlv 

			if Controller.pinchdirectionflag == True: 
				controlHorizontal() #x 

			elif Controller.pinchdirectionflag == False: 
				controlVertical() #y 
		lvx = Controller.getpinchxlv(hand_result) 
		lvy = Controller.getpinchylv(hand_result)		 
		if abs(lvy) > abs(lvx) and abs(lvy) > Controller.pinch_threshold: 
			Controller.pinchdirectionflag = False
			if abs(Controller.prevpinchlv - lvy) < Controller.pinch_threshold: 
				Controller.framecount += 1
			else: 
				Controller.prevpinchlv = lvy 
				Controller.framecount = 0

		elif abs(lvx) > Controller.pinch_threshold: 
			Controller.pinchdirectionflag = True
			if abs(Controller.prevpinchlv - lvx) < Controller.pinch_threshold: 
				Controller.framecount += 1
			else: 
				Controller.prevpinchlv = lvx 
				Controller.framecount = 0
	def handle_controls(gesture, hand_result):		 
		x,y = None,None
		if gesture != Gest.PALM : 
			x,y = Controller.get_position(hand_result)	 
		# flag reset 
		if gesture != Gest.FIST and Controller.grabflag: 
			Controller.grabflag = False
			pyautogui.mouseUp(button = "left") 
		if gesture != Gest.PINCH_MAJOR and Controller.pinchmajorflag: 
			Controller.pinchmajorflag = False
		if gesture != Gest.PINCH_MINOR and Controller.pinchminorflag: 
			Controller.pinchminorflag = False
		# implementation 
		if gesture == Gest.V_GEST: 
			Controller.flag = True
			pyautogui.moveTo(x, y, duration = 0.1) 
		elif gesture == Gest.FIST: 
			if not Controller.grabflag : 
				Controller.grabflag = True
				pyautogui.mouseDown(button = "left") 
			pyautogui.moveTo(x, y, duration = 0.1) 
		elif gesture == Gest.MID and Controller.flag: 
			pyautogui.click() 
			Controller.flag = False
		elif gesture == Gest.INDEX and Controller.flag: 
			pyautogui.click(button='right') 
			Controller.flag = False
		elif gesture == Gest.TWO_FINGER_CLOSED and Controller.flag: 
			pyautogui.doubleClick() 
			Controller.flag = False
		elif gesture == Gest.PINCH_MINOR: 
			if Controller.pinchminorflag == False: 
				Controller.pinch_control_init(hand_result) 
				Controller.pinchminorflag = True
			Controller.pinch_control(hand_result,Controller.scrollHorizontal, Controller.scrollVertical)	 
		elif gesture == Gest.PINCH_MAJOR: 
			if Controller.pinchmajorflag == False: 
				Controller.pinch_control_init(hand_result) 
				Controller.pinchmajorflag = True
			Controller.pinch_control(hand_result,Controller.changesystembrightness, Controller.changesystemvolume)
