import gremlin
import time
import uuid
from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants defining the devices connected to this PC

invert = False

# input stick

VJOY_INPUT_GUID = "{203C80E0-15C8-11EA-8002-444553540000}"
VJOY_INPUT_NAME = "vJoy Device"
vjin = gremlin.input_devices.JoystickDecorator(VJOY_INPUT_NAME, VJOY_INPUT_GUID , MODE_ALL )

gremlin.util.log("DCS spit module enabled")

class Values:
	INTERVAL = 0.2
	PERIODIC = 0.2
	STEP = 0.05
	trim_left_pressed = False
	trim_right_pressed = False
	trim_left_tick = 0
	trim_right_tick = 0


@gremlin.input_devices.periodic(Values.PERIODIC)
def tick_check(vjoy):
	tick = time.clock()
	if Values.trim_left_pressed and Values.trim_left_tick < tick:
		update_trim(vjoy,-Values.STEP)
		Values.trim_left_tick = tick + Values.INTERVAL
		
	if Values.trim_right_pressed and Values.trim_right_tick < tick:
		update_trim(vjoy,+Values.STEP)
		Values.trim_right_tick = tick + Values.INTERVAL

def update_trim(vjoy, step):
	value = vjoy[3].axis(1).value
	#gremlin.util.log("value: {}".format(value))
	value += step
	if value < -1.0:
		value = -1.0
	elif value > 1.0:
		value = 1.0
	vjoy[3].axis(1).value = value
	
@vjin.button(1)
def trim_left(event, vjoy):
	if event.is_pressed:
		update_trim(vjoy,-Values.STEP)	
		Values.trim_left_tick = time.clock() + Values.INTERVAL
		Values.trim_left_pressed = True
	else:
		Values.trim_left_pressed = False

@vjin.button(2)
def trim_center(event, vjoy):
	if event.is_pressed:
		vjoy[3].axis(1).value = 0
		
@vjin.button(3)
def trim_right(event, vjoy):
	if event.is_pressed:
		update_trim(vjoy, Values.STEP)
		Values.trim_right_tick = time.clock() + Values.INTERVAL
		Values.trim_right_pressed = True
	else:
		Values.trim_right_pressed = False