import gremlin
import time
import threading
from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants from the configuration.py file

gremlin.util.log("Loading panel on/off buttons script==============================================")
gremlin.util.log("Pulse length: %s   Long pulse delay: %s" % (PULSE_LENGTH, LONG_PULSE))


# V13 decorators
leftPanel = gremlin.input_devices.JoystickDecorator( LEFT_DSD_NAME, LEFT_DSD_GUID, MODE_ALL )
rightPanel = gremlin.input_devices.JoystickDecorator( RIGHT_DSD_NAME, RIGHT_DSD_GUID, MODE_ALL )
tmthrottle = gremlin.input_devices.JoystickDecorator( TM_THROTTLE_NAME, TM_THROTTLE_GUID, MODE_ALL )
tmstick = gremlin.input_devices.JoystickDecorator( TM_STICK_NAME, TM_STICK_GUID, MODE_ALL )
g29 = gremlin.input_devices.JoystickDecorator( G29_NAME,G29_GUID, MODE_ALL )


# hat 2 up
@tmstick.button(11)
def ts11(event, vjoy):
	if event.is_pressed:
		vjoy[1].hat(2).direction = (0,1)
	else:
		vjoy[1].hat(2).direction = (0,0)
	
# hat 2 right
@tmstick.button(12)
def ts12(event, vjoy):
	if event.is_pressed:
		vjoy[1].hat(2).direction = (1,0)
	else:
		vjoy[1].hat(2).direction = (0,0)	
		
# hat 2 bottom	
@tmstick.button(13)
def ts13(event, vjoy):
	if event.is_pressed:
		vjoy[1].hat(2).direction = (0,-1)
	else:
		vjoy[1].hat(2).direction = (0,0)
	
# hat 2 left
@tmstick.button(14)
def ts14(event, vjoy):
	if event.is_pressed:
		vjoy[1].hat(2).direction = (-1,0)		
	else:
		vjoy[1].hat(2).direction = (0,0)
