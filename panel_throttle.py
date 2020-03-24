import gremlin
import time
from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants defining the devices connected to this PC

leftPanel = gremlin.input_devices.JoystickDecorator( LEFT_DSD_NAME, gremlin.common.DeviceIdentifier(LEFT_DSD_HWID, LEFT_DSD_ID), MODE_ALL )
rightPanel = gremlin.input_devices.JoystickDecorator( RIGHT_DSD_NAME, gremlin.common.DeviceIdentifier(RIGHT_DSD_HWID, RIGHT_DSD_ID), MODE_ALL )



gremlin.util.log("Custom panel throttle module enabled")
throttle_delta = 0.2
output_axis = 6



@rightPanel.button(17)
def throttle_increase(event, vjoy):
	global throttle_delta
	global output_axis
	value = vjoy[1].axis(output_axis).value
	gremlin.util.log(value)
	value = value - throttle_delta
	if value < -1: 
		value = -1
	gremlin.util.log(value)		
	vjoy[1].axis(output_axis).value = value

@rightPanel.button(32)
def throttle_increase(event, vjoy):
	global throttle_delta
	global output_axis
	value = vjoy[1].axis(output_axis).value
	gremlin.util.log(value)
	value = value + throttle_delta
	if value > 1: 
		value = 1
	gremlin.util.log(value)
	vjoy[1].axis(output_axis).value = value