import gremlin
import time
import uuid
from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants defining the devices connected to this PC

invert = False

# input stick
rudder = gremlin.input_devices.JoystickDecorator( TM_RUDDER_NAME,TM_RUDDER_GUID , MODE_ALL )

curve = CubicSpline([
	(-1.0, -1.0),
	(-0.5, -0.25),
	( 0.0,  0.0),
	( 0.5,  0.25),
	( 1.0,  1.0)
])

gremlin.util.log("Custom rudder strafe module enabled")



# values are (-1, +1) for each axis
def merge(left, right, vjoy):
	value = (left - right) / 2.0
	# gremlin.util.log("Left: %s  Right: %s  Merged value: %s" % (left, right, value))
	# output to vjoy #2 slider
	if invert:
		vjoy[2].axis(7).value = -value
	else:
		vjoy[2].axis(7).value = value
	
	
@rudder.axis(1)
def xaxis(event, vjoy, joy):
	guid = event.device_guid
	right = event.value
	left = joy[guid].axis(2).value
	rudder = joy[guid].axis(3).value
	merge(left,right, vjoy)
	vjoy[2].axis(8).value = right
	vjoy[2].axis(3).value = right
	vjoy[1].axis(3).value = (left - right) / 2.0
		
# pitch axis disconnect of nose wheel steer
@rudder.axis(2)
def xaxis(event, vjoy, joy):
	guid = event.device_guid
	right = joy[guid].axis(1).value
	left = event.value
	merge(left,right, vjoy)
	vjoy[2].axis(8).value = left
	vjoy[2].axis(2).value = left
	vjoy[1].axis(3).value = (left - right) / 2.0