import gremlin
import time
import threading
from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants from the configuration.py file

gremlin.util.log("Loading panel on/off buttons script==============================================")
gremlin.util.log("Pulse length: %s   Long pulse delay: %s" % (PULSE_LENGTH, LONG_PULSE))


leftPanel = gremlin.input_devices.JoystickDecorator( LEFT_DSD_NAME, gremlin.common.DeviceIdentifier(LEFT_DSD_HWID, LEFT_DSD_ID), MODE_ALL )
rightPanel = gremlin.input_devices.JoystickDecorator( RIGHT_DSD_NAME, gremlin.common.DeviceIdentifier(RIGHT_DSD_HWID, RIGHT_DSD_ID), MODE_ALL )
tmthrottle = gremlin.input_devices.JoystickDecorator( TM_THROTTLE_NAME, gremlin.common.DeviceIdentifier(TM_THROTTLE_HWID, TM_THROTTLE_ID), MODE_ALL )
tmstick = gremlin.input_devices.JoystickDecorator( TM_STICK_NAME, gremlin.common.DeviceIdentifier(TM_STICK_HWID, TM_STICK_ID), MODE_ALL )
g29 = gremlin.input_devices.JoystickDecorator( G29_NAME, gremlin.common.DeviceIdentifier(G29_HWID, G29_ID), MODE_ALL )

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
