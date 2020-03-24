import gremlin
import time
import threading
from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants from the configuration.py file

''' Definitions '''

# on/off button options
# if true, the buttons will pulse, if false, they will be steady
LEFT_B1_PULSE = True
LEFT_B2_PULSE = True
LEFT_B3_PULSE = True
LEFT_B4_PULSE = True
LEFT_B5_PULSE = True
LEFT_B6_PULSE = True
LEFT_B7_PULSE = True
LEFT_B8_PULSE = True

LEFT_B18_PULSE = True
LEFT_B19_PULSE = True
LEFT_B20_PULSE = True
LEFT_B21_PULSE = True
LEFT_B22_PULSE = True
LEFT_B23_PULSE = True
LEFT_B24_PULSE = True

RIGHT_B1_PULSE = True
RIGHT_B2_PULSE = True
RIGHT_B3_PULSE = True
RIGHT_B4_PULSE = True
RIGHT_B5_PULSE = True
RIGHT_B6_PULSE = True

# button names

LEFT_B1 = "lb1"
LEFT_B2 = "lb2"
LEFT_B3 = "lb3"
LEFT_B4 = "lb4"
LEFT_B5 = "lb5"
LEFT_B6 = "lb6"
LEFT_B7 = "lb7"
LEFT_B8 = "lb8"

LEFT_B18 = "lb18"
LEFT_B19 = "lb19"
LEFT_B20 = "lb20"
LEFT_B21 = "lb21"
LEFT_B22 = "lb22"
LEFT_B23 = "lb23"
LEFT_B24 = "lb24"
       
RIGHT_B1 = "rb1"
RIGHT_B2 = "rb2"
RIGHT_B3 = "rb3"
RIGHT_B4 = "rb4"
RIGHT_B5 = "rb5"
RIGHT_B6 = "rb6"




RIGHT_B11 = "rb11"
RIGHT_B12 = "rb12"
RIGHT_B13 = "rb13"
RIGHT_B14 = "rb14"
RIGHT_B15 = "rb15"
RIGHT_B16 = "rb16"
RIGHT_B17 = "rb17"
RIGHT_B18 = "rb18"
RIGHT_B19 = "rb19"
RIGHT_B20 = "rb20"
RIGHT_B21 = "rb21"
RIGHT_B22 = "rb22"
RIGHT_B23 = "rb23"
RIGHT_B24 = "rb24"
RIGHT_B25 = "rb25"
RIGHT_B26 = "rb26"
RIGHT_B27 = "rb27"
RIGHT_B28 = "rb28"
RIGHT_B29 = "rb29"
RIGHT_B30 = "rb30"
RIGHT_B31 = "rb31"
RIGHT_B32 = "rb32"

RIGHT_B11_PULSE = True
RIGHT_B12_PULSE = True
RIGHT_B13_PULSE = True
RIGHT_B14_PULSE = True
RIGHT_B15_PULSE = True
RIGHT_B16_PULSE = True
RIGHT_B17_PULSE = True
RIGHT_B18_PULSE = True
RIGHT_B19_PULSE = True
RIGHT_B20_PULSE = True
RIGHT_B21_PULSE = True
RIGHT_B22_PULSE = True
RIGHT_B23_PULSE = True
RIGHT_B24_PULSE = True
RIGHT_B25_PULSE = True
RIGHT_B26_PULSE = True
RIGHT_B27_PULSE = True
RIGHT_B28_PULSE = True
RIGHT_B29_PULSE = True
RIGHT_B30_PULSE = True
RIGHT_B31_PULSE = True
RIGHT_B32_PULSE = True



LEFT_R1_CW = "lr1cw"
LEFT_R2_CW = "lr2cw"
LEFT_R3_CW = "lr3cw"
LEFT_R4_CW = "lr4cw"
LEFT_R5_CW = "lr5cw"

LEFT_R1_CC = "lr1cc"
LEFT_R2_CC = "lr2cc"
LEFT_R3_CC = "lr3cc"
LEFT_R4_CC = "lr4cc"
LEFT_R5_CC = "lr5cc"

RIGHT_R1_CW = "rr1cw"
RIGHT_R2_CW = "rr2cw"
RIGHT_R1_CC = "rr1cc"
RIGHT_R2_CC = "rr2cc"

# tm throttle

TMT_FLAP1 = "tmtflap1"
TMT_FLAP2 = "tmtflap2"
TMT_FLAP1_PULSE = True
TMT_FLAP2_PULSE = True

TMT_GRAY_BOAT1 = "tmtGboat1"
TMT_GRAY_BOAT2 = "tmtGboat2"
TMT_GRAY_BOAT1_PULSE = True
TMT_GRAY_BOAT2_PULSE = True

TMT_RED_BOAT1 = "tmtRboat1"
TMT_RED_BOAT2 = "tmtRboat2"
TMT_RED_BOAT1_PULSE = True
TMT_RED_BOAT2_PULSE = True

TMT_BRAKE1 = "tmtbrake1"
TMT_BRAKE2 = "tmtbrake2"
TMT_BRAKE1_PULSE = True
TMT_BRAKE2_PULSE = True

TMT_PATH1 = "tmtPATH1"
TMT_PATH2 = "tmtPATH2"
TMT_RDRARM = "tmtRDRARM"
TMT_EAC = "tmtEAC"
TMT_PATH1_PULSE = True
TMT_PATH2_PULSE = True
TMT_RDRARM_PULSE = True
TMT_EAC_PULSE = True

# g29 wheel

G29_GEAR_3_UP = "g29_gear3_up"
G29_GEAR_3_DN = "g29_gear3_dn"
G29_GEAR_3_UP_PULSE = True
G29_GEAR_3_DN_PULSE = True


leftPanelJoy = None
rightPanelJoy = None

gremlin.util.log("Loading panel on/off buttons script==============================================")
gremlin.util.log("Pulse length: %s   Long pulse delay: %s" % (PULSE_LENGTH, LONG_PULSE))


leftPanel = gremlin.input_devices.JoystickDecorator( LEFT_DSD_NAME, gremlin.common.DeviceIdentifier(LEFT_DSD_HWID, LEFT_DSD_ID), MODE_ALL )
rightPanel = gremlin.input_devices.JoystickDecorator( RIGHT_DSD_NAME, gremlin.common.DeviceIdentifier(RIGHT_DSD_HWID, RIGHT_DSD_ID), MODE_ALL )
tmthrottle = gremlin.input_devices.JoystickDecorator( TM_THROTTLE_NAME, gremlin.common.DeviceIdentifier(TM_THROTTLE_HWID, TM_THROTTLE_ID), MODE_ALL )
g29 = gremlin.input_devices.JoystickDecorator( G29_NAME, gremlin.common.DeviceIdentifier(G29_HWID, G29_ID), MODE_ALL )

# holds the last button click time
last_click = {}

# holds button definitions
button_list = {}

# holds knob definitions
knob_list = {}

panel_initialized = False
_joy = None
_vjoy = None

# holds data for a two way switch
class OnOffData:
	def __init__(self, name, mode, unit, on_button, off_button, pulse_flag):
		self.name = name
		self.mode = mode
		self.unit = unit
		self.on_button = on_button
		self.off_button = off_button
		self.pulse_flag = pulse_flag
		
	def toString(self):
		return "[OnOffData] name: %s mode: %s unit: %s on: %s off: %s pulse: %s" %(self.name, self.mode, self.unit, self.on_button, self.off_button, self.pulse_flag)

# holds data for a 3 way switch
class ThreeWayData:
	def __init__(self, name, mode, unit, top_button, middle_button, bottom_button, pulse_flag):
		self.name = name
		self.mode = mode
		self.unit = unit
		self.top_button = top_button
		self.middle_button = middle_button
		self.bottom_button = bottom_button
		self.pulse_flag = pulse_flag
		
	def toString(self):
		return "[OnOffData] name: %s mode: %s unit: %s on: %s off: %s pulse: %s" %(self.name, self.mode, self.unit, self.on_button, self.off_button, self.pulse_flag)		
		
class KnobData:
	def __init__(self, name, mode, unit, slow_button, fast_button, use_fast = 0, repeat = 1):
		self.name = name
		self.mode = mode
		self.unit = unit
		self.slow_button = slow_button
		self.fast_button = fast_button
		self.repeat = repeat
		self.use_fast = use_fast
		
		
	def toString(self):
		return "[KnobData] name: %s mode: %s unit: %s slow: %s fast: %s  repeat: %s" %(self.name, self.mode, self.unit, self.slow_button, self.fast_button, self.repeat)
	
# gets the current Gremlin active mode (will be a text value)
def ActiveMode():
	eh = gremlin.event_handler.EventHandler()
	return eh.active_mode
	
	
# adds a button or knob definition		
def addDefinition(list, data):
	if not data.name in list:
		list[data.name] = {}
	if not data.mode in list[data.name]:
		list[data.name][data.mode] = {}
	list[data.name][data.mode] = data

# retrieves a definition for a button or knob based on current mode, defaults to the first definition if mode isn't found	
def getDefinition(list, name):
	mode = ActiveMode()
	# gremlin.util.log("active mode: '%s' button name: '%s'" % (mode,name) )
	if not name in list:
		gremlin.util.log("button name not found '%s' - ignoring event" % (name) )
		return
	'''
	gremlin.util.log("=============")
	gremlin.util.log(list[name])
	gremlin.util.log("=============")
	'''
	if not mode in list[name]:
		# gremlin.util.log("mode '%s' not found for button name '%s'" % (mode,name) )
		if MODE_ALL in list[name]:
			# gremlin.util.log("using mode '%s' for button name %s" % (MODE_ALL,name))
			data = list[name][MODE_ALL]		
		else:
			data = None
	else:
		data = list[name][mode]	
	return data
	

	
		
# async routine to pulse a button
def fire_pulse(vjoy, unit, button, repeat = 1, duration = 0.05):
	if repeat < 0:
		repeat = -repeat
		for i in range(repeat):
			# gremlin.util.log("Pulsing vjoy %s button %s on" % (unit, button) )	
			vjoy[unit].button(button).is_pressed = True
			time.sleep(duration)
			vjoy[unit].button(button).is_pressed = False
			time.sleep(duration)
	else:
		if repeat <= 1: 
			vjoy[unit].button(button).is_pressed = True
			time.sleep(duration)
			vjoy[unit].button(button).is_pressed = False
		else:
			vjoy[unit].button(button).is_pressed = True
			time.sleep(duration*repeat)
			vjoy[unit].button(button).is_pressed = False		
		
	# gremlin.util.log("Pulsing vjoy %s button %s off" % (unit, button) )

# pulses a button - unit is the vjoy output device number, button is the number of the button on the device to pulse
def pulse(vjoy, unit, button, repeat = 1):
	threading.Timer(0.01, fire_pulse, [vjoy, unit, button, repeat]).start()

	
# gets the last timer tick for a unit/button - creates entries if needed
def get_tick(unit,button):
	if not unit in last_click:
		last_click[unit] = {}
		
	if not button in last_click[unit]:
		last_click[unit][button] = 0
	
	return last_click[unit][button]
	
		
		
	
# performs a slow or fast click depending on the last time the button fired	
# ref_unit = source unit clicked
# ref_button = source button on unit
# unit = vjoy device to pulse
# slow_button = vjoy button to pulse for slow rotation
# fast_button = vjoy button to pulse for fast rotation
def speed_click(vjoy, ref_unit, ref_button, unit, slow_button, fast_button, use_fast, repeat):
	if use_fast:
		t1 = time.clock()
		t0 = get_tick(ref_unit,ref_button)
		gremlin.util.log("delta %s repeat %s " % (t1-t0, repeat) )
		last_click[ref_unit][ref_button] = t1
		if t1 - t0 < LONG_PULSE:
			pulse(vjoy, unit, fast_button, repeat)
			gremlin.util.log("fast")
		else:
			pulse(vjoy, unit, slow_button, repeat)
			gremlin.util.log("slow")
	else:
		pulse(vjoy, unit, slow_button, repeat)
		gremlin.util.log("use slow button")

# fires specified button - either stead or pulse
# event = gremlin event
# vjoy = gremlin vjoy devices
# unit = vjoy device number to output
# on_button = button to fire when button is in the ON position (steady or pulse)
# off_button = button to fire when button is in the OFF position (steady or pulse)
# pulse = flag, when true, pulses, when false, steady output
def fireButton(event, vjoy, unit, on_button, off_button, pulse_flag):
	if pulse_flag:
		if event.is_pressed:
			pulse(vjoy, unit, on_button)
			vjoy[unit].button(off_button).is_pressed = False
			gremlin.util.log("device %s button %s pulse" % (unit, on_button))
		else:
			pulse(vjoy, unit, off_button)
			vjoy[unit].button(on_button).is_pressed = False
			gremlin.util.log("device %s button %s pulse" % (unit, off_button))
	else:
		if event.is_pressed:
			vjoy[unit].button(on_button).is_pressed = True
			vjoy[unit].button(off_button).is_pressed = False
		else:
			vjoy[unit].button(on_button).is_pressed = False
			vjoy[unit].button(off_button).is_pressed = True
	
# fires a button based on current mode and button name	
def fire(event, vjoy, name):
	data = getDefinition(button_list, name)
	if not data is None:
		# gremlin.util.log(data.toString())
		fireButton(event, vjoy, data.unit, data.on_button, data.off_button, data.pulse_flag)
		

# rotates a knob based on current mode and knob name	
def rotate(event, vjoy, name, ref_unit, ref_button):
	if event.is_pressed:
		data = getDefinition(knob_list, name)
		if not data is None:
			pulse(vjoy, data.unit, data.slow_button, data.repeat)
			# gremlin.util.log(data.toString())
			# speed_click(vjoy, ref_unit, ref_button, data.unit, data.slow_button, data.fast_button, data.use_fast, data.repeat)
			# speed_click(vjoy, ref_unit, ref_button, unit, slow_button, fast_button):	
			
	
''' definitions for buttons and knobs for each supported mode '''
	

addDefinition(button_list, OnOffData(LEFT_B1, MODE_ALL,1,73,74,LEFT_B1_PULSE))
addDefinition(button_list, OnOffData(LEFT_B2, MODE_ALL,1,75,76,LEFT_B2_PULSE))
addDefinition(button_list, OnOffData(LEFT_B3, MODE_ALL,1,77,78,LEFT_B3_PULSE))	
addDefinition(button_list, OnOffData(LEFT_B4, MODE_ALL,1,79,80,LEFT_B4_PULSE))	
addDefinition(button_list, OnOffData(LEFT_B5, MODE_ALL,1,81,82,LEFT_B5_PULSE))	
addDefinition(button_list, OnOffData(LEFT_B6, MODE_ALL,1,83,84,LEFT_B6_PULSE))	
addDefinition(button_list, OnOffData(LEFT_B7, MODE_ALL,1,85,86,LEFT_B7_PULSE))	
addDefinition(button_list, OnOffData(LEFT_B8, MODE_ALL,1,87,88,LEFT_B8_PULSE))	

addDefinition(button_list, OnOffData(LEFT_B18, MODE_ALL,1,89,90,LEFT_B18_PULSE))
addDefinition(button_list, OnOffData(LEFT_B19, MODE_ALL,1,91,92,LEFT_B19_PULSE))
addDefinition(button_list, OnOffData(LEFT_B20, MODE_ALL,1,93,94,LEFT_B20_PULSE))	
addDefinition(button_list, OnOffData(LEFT_B21, MODE_ALL,1,95,96,LEFT_B21_PULSE))	
addDefinition(button_list, OnOffData(LEFT_B22, MODE_ALL,1,97,98,LEFT_B22_PULSE))	
addDefinition(button_list, OnOffData(LEFT_B23, MODE_ALL,1,99,100,LEFT_B23_PULSE))	
addDefinition(button_list, OnOffData(LEFT_B24, MODE_ALL,1,28,29,LEFT_B24_PULSE))	



addDefinition(button_list, OnOffData(RIGHT_B1, MODE_ALL,1,30,31,RIGHT_B1_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B2, MODE_ALL,1,32,33,RIGHT_B2_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B3, MODE_ALL,1,34,35,RIGHT_B3_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B4, MODE_ALL,1,36,37,RIGHT_B4_PULSE))	
addDefinition(button_list, OnOffData(RIGHT_B5, MODE_ALL,1,38,39,RIGHT_B5_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B6, MODE_ALL,1,40,41,RIGHT_B6_PULSE))

# right panel 3 way switch 1 from the left
addDefinition(button_list, OnOffData(RIGHT_B22, MODE_ALL,1,41,42,RIGHT_B22_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B23, MODE_ALL,1,43,42,RIGHT_B23_PULSE))

# right panel 3 way switch 2 from the left
addDefinition(button_list, OnOffData(RIGHT_B28, MODE_ALL,1,44,45,RIGHT_B28_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B21, MODE_ALL,1,46,45,RIGHT_B21_PULSE))

# right panel 3 way switch 3 from the left
addDefinition(button_list, OnOffData(RIGHT_B29, MODE_ALL,1,47,48,RIGHT_B29_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B20, MODE_ALL,1,49,48,RIGHT_B20_PULSE))

# right panel 3 way switch 4 from the left
addDefinition(button_list, OnOffData(RIGHT_B30, MODE_ALL,1,50,51,RIGHT_B30_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B19, MODE_ALL,1,52,51,RIGHT_B19_PULSE))

# right panel 3 way switch 5 from the left
addDefinition(button_list, OnOffData(RIGHT_B31, MODE_ALL,1,53,54,RIGHT_B31_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B18, MODE_ALL,1,55,54,RIGHT_B18_PULSE))

# right panel 3 way switch 6 from the left
addDefinition(button_list, OnOffData(RIGHT_B32, MODE_ALL,1,56,57,RIGHT_B32_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B17, MODE_ALL,1,58,57,RIGHT_B17_PULSE))

# right panel bottom row switches from the left
addDefinition(button_list, OnOffData(RIGHT_B13, MODE_ALL,1,59,60,RIGHT_B13_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B14, MODE_ALL,1,61,62,RIGHT_B14_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B15, MODE_ALL,1,63,64,RIGHT_B15_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B16, MODE_ALL,1,65,66,RIGHT_B16_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B25, MODE_ALL,1,67,68,RIGHT_B25_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B26, MODE_ALL,1,69,70,RIGHT_B26_PULSE))
addDefinition(button_list, OnOffData(RIGHT_B27, MODE_ALL,1,71,72,RIGHT_B27_PULSE))



#left panel buttons
addDefinition(knob_list, KnobData(LEFT_R1_CC,MODE_ALL,1,102,103))
addDefinition(knob_list, KnobData(LEFT_R1_CW,MODE_ALL,1,104,105))
addDefinition(knob_list, KnobData(LEFT_R2_CC,MODE_ALL,1,106,107))
addDefinition(knob_list, KnobData(LEFT_R2_CW,MODE_ALL,1,108,109))
addDefinition(knob_list, KnobData(LEFT_R3_CC,MODE_ALL,1,110,111))
addDefinition(knob_list, KnobData(LEFT_R3_CW,MODE_ALL,1,112,113))
addDefinition(knob_list, KnobData(LEFT_R4_CC,MODE_ALL,1,114,115))
addDefinition(knob_list, KnobData(LEFT_R4_CW,MODE_ALL,1,116,117))
addDefinition(knob_list, KnobData(LEFT_R5_CC,MODE_ALL,1,118,119))
addDefinition(knob_list, KnobData(LEFT_R5_CW,MODE_ALL,1,120,121))

addDefinition(knob_list, KnobData(RIGHT_R1_CC,MODE_ALL,1,121,122))
addDefinition(knob_list, KnobData(RIGHT_R1_CW,MODE_ALL,1,123,124))
addDefinition(knob_list, KnobData(RIGHT_R2_CC,MODE_ALL,1,125,126))
addDefinition(knob_list, KnobData(RIGHT_R2_CW,MODE_ALL,1,127,128))

addDefinition(knob_list, KnobData(LEFT_R1_CC,MODE_A,2,102,103))
addDefinition(knob_list, KnobData(LEFT_R1_CW,MODE_A,2,104,105))
addDefinition(knob_list, KnobData(LEFT_R2_CC,MODE_A,2,106,107))
addDefinition(knob_list, KnobData(LEFT_R2_CW,MODE_A,2,108,109))
addDefinition(knob_list, KnobData(LEFT_R3_CC,MODE_A,2,110,111))
addDefinition(knob_list, KnobData(LEFT_R3_CW,MODE_A,2,112,113))
addDefinition(knob_list, KnobData(LEFT_R4_CC,MODE_A,2,114,115))
addDefinition(knob_list, KnobData(LEFT_R4_CW,MODE_A,2,116,117))
addDefinition(knob_list, KnobData(LEFT_R5_CC,MODE_A,2,118,119))
addDefinition(knob_list, KnobData(LEFT_R5_CW,MODE_A,2,120,121))

addDefinition(knob_list, KnobData(RIGHT_R1_CC,MODE_A,2,121,122))
addDefinition(knob_list, KnobData(RIGHT_R1_CW,MODE_A,2,123,124))
addDefinition(knob_list, KnobData(RIGHT_R2_CC,MODE_A,2,125,126))
addDefinition(knob_list, KnobData(RIGHT_R2_CW,MODE_A,2,127,128))

''' tm throttle '''

# flap button - 2 positions to 3 (center)
addDefinition(button_list, OnOffData(TMT_FLAP1, MODE_ALL,1,10,11,TMT_FLAP1_PULSE))
addDefinition(button_list, OnOffData(TMT_FLAP2, MODE_ALL,1,12,11,TMT_FLAP2_PULSE))

# gray boat - 2 positions to 3 (center)
addDefinition(button_list, OnOffData(TMT_GRAY_BOAT1, MODE_ALL,1,13,14,TMT_GRAY_BOAT1_PULSE))
addDefinition(button_list, OnOffData(TMT_GRAY_BOAT2, MODE_ALL,1,15,14,TMT_GRAY_BOAT2_PULSE))

# red boat - 2 positions to 3 (center)
addDefinition(button_list, OnOffData(TMT_RED_BOAT1, MODE_ALL,1,16,17,TMT_RED_BOAT1_PULSE))
addDefinition(button_list, OnOffData(TMT_RED_BOAT2, MODE_ALL,1,18,17,TMT_RED_BOAT2_PULSE))

# brake - 2 positions to 3 (center)
addDefinition(button_list, OnOffData(TMT_BRAKE1, MODE_ALL,2,7,8,TMT_BRAKE1_PULSE))
addDefinition(button_list, OnOffData(TMT_BRAKE2, MODE_ALL,2,9,8,TMT_BRAKE2_PULSE))

# path/alt button - 2 positions to 3 
addDefinition(button_list, OnOffData(TMT_PATH1, MODE_ALL,2,11,12,TMT_PATH1_PULSE))
addDefinition(button_list, OnOffData(TMT_PATH2, MODE_ALL,2,13,12,TMT_PATH2_PULSE))

# rdt alt button
addDefinition(button_list, OnOffData(TMT_RDRARM, MODE_ALL,2,5,6,TMT_RDRARM_PULSE))
addDefinition(button_list, OnOffData(TMT_EAC, MODE_ALL,2,3,4,TMT_RDRARM_PULSE))

''' G29 wheel '''
# gear 3 up/down - 2 positions to 3 
addDefinition(button_list, OnOffData(G29_GEAR_3_UP, MODE_ALL,1,21,22,G29_GEAR_3_UP_PULSE))
addDefinition(button_list, OnOffData(G29_GEAR_3_DN, MODE_ALL,1,23,22,G29_GEAR_3_DN_PULSE))

			
''' LEFT PANEL On/Off switches ========================================================= '''

# on/off switch 1
@leftPanel.button(1)
def lb_1(event, vjoy):
	# fire(event, vjoy, 1, 69, 77, LEFT_B1_PULSE)
	if event.is_pressed:
		gremlin.util.log("switch to MODE A")
		gremlin.control_action.switch_mode(MODE_A)
	else:
		gremlin.util.log("switch to MODE DEFAULT")
		gremlin.control_action.switch_mode(MODE_ALL)
		
	fire(event, vjoy, LEFT_B1)

# on/off switch 2
@leftPanel.button(2)
def lb_2(event, vjoy):
	# fire(event, vjoy, 1, 70, 78, LEFT_B2_PULSE)
	fire(event, vjoy, LEFT_B2)
		
# on/off switch 3		
@leftPanel.button(3)
def lb_3(event, vjoy):
	# fire(event, vjoy, 1, 71, 79, LEFT_B3_PULSE)
	fire(event, vjoy, LEFT_B3)
		
# on/off switch 4		
@leftPanel.button(4)
def lb_4(event, vjoy):
	# fire(event, vjoy, 1, 72, 80, LEFT_B4_PULSE)
	fire(event, vjoy, LEFT_B4)

# on/off switch 5		
@leftPanel.button(5)
def lb_5(event, vjoy):
	# fire(event, vjoy, 1, 73, 81, LEFT_B5_PULSE)
	fire(event, vjoy, LEFT_B5)

# on/off switch 6		
@leftPanel.button(6)
def lb_6(event, vjoy):
	# fire(event, vjoy, 1, 74, 82, LEFT_B6_PULSE)
	fire(event, vjoy, LEFT_B6)

# on/off switch 7		
@leftPanel.button(7)
def lb_7(event, vjoy):
	# fire(event, vjoy, 1, 75, 83, LEFT_B7_PULSE)
	fire(event, vjoy, LEFT_B7)

# on/off switch 8		
@leftPanel.button(8)
def lb_8(event, vjoy):
	fire(event, vjoy, LEFT_B8)
	
	
# left push button 1
@leftPanel.button(18)
def lb_18(event, vjoy):
	fire(event, vjoy, LEFT_B18)	
	
# left push button 2
@leftPanel.button(19)
def lb_19(event, vjoy):
	fire(event, vjoy, LEFT_B19)	
	
# left push button 3
@leftPanel.button(20)
def lb_20(event, vjoy):
	fire(event, vjoy, LEFT_B20)	
	
# left push button 4
@leftPanel.button(21)
def lb_21(event, vjoy):
	fire(event, vjoy, LEFT_B21)	
	
# left push button 5
@leftPanel.button(22)
def lb_22(event, vjoy):
	fire(event, vjoy, LEFT_B22)	
	
# left push button 6
@leftPanel.button(23)
def lb_23(event, vjoy):
	fire(event, vjoy, LEFT_B23)	

# left push button 7
@leftPanel.button(24)
def lb_24(event, vjoy):
	fire(event, vjoy, LEFT_B24)	

		
''' RIGHT PANEL On/Off switches ========================================================= '''

# on/off switch 1		
@rightPanel.button(8)
def rb_1(event, vjoy):
	#gremlin.util.log("right panel button 8")
	#fire(event, vjoy, 1, 30, 31, RIGHT_B1_PULSE)
	fire(event, vjoy, RIGHT_B1)

# on/off switch 2		
@rightPanel.button(7)
def rb_2(event, vjoy):
	#gremlin.util.log("right panel button 7")
	# fire(event, vjoy, 1, 32, 32, RIGHT_B2_PULSE)
	fire(event, vjoy, RIGHT_B2)

# on/off switch 3		
@rightPanel.button(6)
def rb_3(event, vjoy):
	#gremlin.util.log("right panel button 6")
	# fire(event, vjoy, 1, 34, 35, RIGHT_B3_PULSE)
	fire(event, vjoy, RIGHT_B3)

# on/off switch 4		
@rightPanel.button(5)
def rb_4(event, vjoy):
	#gremlin.util.log("right panel button 5")
	# fire(event, vjoy, 1, 36, 37, RIGHT_B4_PULSE)
	fire(event, vjoy, RIGHT_B4)
	
# on/off switch 5		
@rightPanel.button(4)
def rb_5(event, vjoy):
	#gremlin.util.log("right panel button 4")
	# fire(event, vjoy, 1, 38, 39, RIGHT_B5_PULSE)
	fire(event, vjoy, RIGHT_B5)
	
# on/off switch 6		
@rightPanel.button(3)
def rb_6(event, vjoy):
	#gremlin.util.log("right panel button 3")
	# fire(event, vjoy, 1, 40, 41, RIGHT_B6_PULSE)
	fire(event, vjoy, RIGHT_B6)


# bottom button 1
@rightPanel.button(13)
def rb_13(event, vjoy):
	fire(event, vjoy, RIGHT_B13)
	
# bottom button 2
@rightPanel.button(14)
def rb_14(event, vjoy):
	fire(event, vjoy, RIGHT_B14)

# bottom button 3
@rightPanel.button(15)
def rb_15(event, vjoy):
	fire(event, vjoy, RIGHT_B15)
	
	
# 3 way button 6 bottom	
@rightPanel.button(17)
def rb_17(event, vjoy):
	fire(event, vjoy, RIGHT_B17)


# 3 way button 5 bottom
@rightPanel.button(18)
def rb_18(event, vjoy):
	fire(event, vjoy, RIGHT_B18)


#3 way button
@rightPanel.button(17)
def rb_22(event, vjoy):
	fire(event, vjoy, RIGHT_B17)
	
@rightPanel.button(18)
def rb_22(event, vjoy):
	fire(event, vjoy, RIGHT_B18)	
	
#3 way button 4 bottom
@rightPanel.button(19)
def rb_22(event, vjoy):
	fire(event, vjoy, RIGHT_B19)	
	
#3 way button 3 bottom
@rightPanel.button(20)
def rb_22(event, vjoy):
	fire(event, vjoy, RIGHT_B20)

#3 way button 2 bottom
@rightPanel.button(21)
def rb_22(event, vjoy):
	fire(event, vjoy, RIGHT_B21)

#3 way button 1 top
@rightPanel.button(22)
def rb_22(event, vjoy):
	fire(event, vjoy, RIGHT_B22)
	
#3 way button 1 bottom	
@rightPanel.button(23)
def rb_23(event, vjoy):
	fire(event, vjoy, RIGHT_B23)	
	
@rightPanel.button(24)
def rb_24(event, vjoy):
	fire(event, vjoy, RIGHT_B24)
	
@rightPanel.button(25)
def rb_25(event, vjoy):
	fire(event, vjoy, RIGHT_B25)
	
@rightPanel.button(26)
def rb_26(event, vjoy):
	fire(event, vjoy, RIGHT_B26)	
	
@rightPanel.button(27)
def rb_27(event, vjoy):
	fire(event, vjoy, RIGHT_B27)	
	
	
#3 way button 2 top	
@rightPanel.button(28)
def rb_28(event, vjoy):
	fire(event, vjoy, RIGHT_B28)

#3 way button 3 top
@rightPanel.button(29)
def rb_29(event, vjoy):
	fire(event, vjoy, RIGHT_B29)
	
#3 way button 4 top	
@rightPanel.button(30)
def rb_30(event, vjoy):
	fire(event, vjoy, RIGHT_B30)

#3 way button 5 top
@rightPanel.button(31)
def rb_31(event, vjoy):
	fire(event, vjoy, RIGHT_B31)	

# 3 way button 6 top (rightmost button)	
@rightPanel.button(32)
def rb_32(event, vjoy):
	fire(event, vjoy, RIGHT_B32)

''' LEFT PANEL rotation speed ========================================================= '''


# knob 1 (from the left)

@leftPanel.button(25)
def lb_25(event, vjoy):
	rotate(event, vjoy, LEFT_R1_CC, 1, 25)

@leftPanel.button(26)
def lb_26(event, vjoy):
	rotate(event, vjoy, LEFT_R1_CW, 1, 26)
		
# knob 2 (from the left)		

@leftPanel.button(15)
def lb_15(event, vjoy):
	rotate(event, vjoy, LEFT_R2_CC, 1, 15)
		
@leftPanel.button(16)
def lb_16(event, vjoy):
	rotate(event, vjoy, LEFT_R2_CW, 1, 16)
		
# knob 3 (from the left)		
		
@leftPanel.button(13)
def lb_13(event, vjoy):
	rotate(event, vjoy, LEFT_R3_CC, 1, 13)
		
@leftPanel.button(14)
def lb_14(event, vjoy):
	rotate(event, vjoy, LEFT_R3_CW, 1, 14)
		
		
# knob 4 (from the left)		
		
@leftPanel.button(11)
def lb_11(event, vjoy):
	rotate(event, vjoy, LEFT_R4_CC, 1, 11)
	
@leftPanel.button(12)
def lb_12(event, vjoy):
	rotate(event, vjoy, LEFT_R4_CW, 1, 12)


# knob 5 (from the left)		
		
@leftPanel.button(9)
def lb_9(event, vjoy):
	rotate(event, vjoy, LEFT_R5_CC, 1, 9)
		
@leftPanel.button(10)
def lb_10(event, vjoy):
	rotate(event, vjoy, LEFT_R5_CW, 1, 10)


''' RIGHT PANEL rotation speed ========================================================= '''


# knob 1 top

@rightPanel.button(11)
def rb_11(event, vjoy):
	rotate(event, vjoy, RIGHT_R1_CC, 2, 11)
		
@rightPanel.button(12)
def rb_12(event, vjoy):
	rotate(event, vjoy, RIGHT_R1_CW, 2, 12)
		
# knob 2 bottom	

@rightPanel.button(10)
def rb_10(event, vjoy):
	rotate(event, vjoy, RIGHT_R2_CC, 2, 10)
			
@rightPanel.button(9)
def rb_9(event, vjoy):
	rotate(event, vjoy, RIGHT_R2_CW, 2, 9)
	
	
''' TM Throttle ========================================================= '''

# flap button up
@tmthrottle.button(22)
def tmt_22(event, vjoy):
	fire(event, vjoy, TMT_FLAP1)

# flap button down
@tmthrottle.button(23)
def tmt_23(event, vjoy):
	fire(event, vjoy, TMT_FLAP2)	
	
# gray boat switch forward
@tmthrottle.button(9)
def tmt_9(event, vjoy):
	fire(event, vjoy, TMT_GRAY_BOAT1)	

# gray boat switch back
@tmthrottle.button(10)
def tmt_10(event, vjoy):
	fire(event, vjoy, TMT_GRAY_BOAT2)	
	
# red boat switch forward
@tmthrottle.button(11)
def tmt_11(event, vjoy):
	fire(event, vjoy, TMT_RED_BOAT1)	

# red boat switch back
@tmthrottle.button(12)
def tmt_12(event, vjoy):
	fire(event, vjoy, TMT_RED_BOAT2)	
	
# brake button forward (locks)
@tmthrottle.button(7)
def tmt_7(event, vjoy):
	fire(event, vjoy, TMT_BRAKE1)

# brake button back (temporary)
@tmthrottle.button(8)
def tmt_8(event, vjoy):
	fire(event, vjoy, TMT_BRAKE2)		
	
	
# path/alt button forward 
@tmthrottle.button(27)
def tmt_27(event, vjoy):
	fire(event, vjoy, TMT_PATH1)

# path/alt button back 
@tmthrottle.button(28)
def tmt_28(event, vjoy):
	fire(event, vjoy, TMT_PATH2)		
	
# EAC 2 way button
@tmthrottle	.button(24)
def tmt_24(event, vjoy):
	fire(event, vjoy, TMT_EAC)			
	
# rdr arm 2 way button	
@tmthrottle	.button(25)
def tmt_25(event, vjoy):
	fire(event, vjoy, TMT_RDRARM)		

''' G29 Throttle ========================================================= '''	
	
# gear lever center up
@g29.button(15)
def g29_15(event, vjoy):
	fire(event, vjoy, G29_GEAR_3_UP)
	
@g29.button(13)
def g29_13(event, vjoy):
	fire(event, vjoy, G29_GEAR_3_UP)
	
@g29.button(17)
def g29_17(event, vjoy):
	fire(event, vjoy, G29_GEAR_3_UP)	

# # gear lever center down
@g29.button(16)
def g29_16(event, vjoy):
	fire(event, vjoy, G29_GEAR_3_DN)
	
@g29.button(14)
def g29_14(event, vjoy):
	fire(event, vjoy, G29_GEAR_3_DN)			
	
@g29.button(18)
def g29_18(event, vjoy):
	fire(event, vjoy, G29_GEAR_3_DN)			