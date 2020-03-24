import gremlin
import time
from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants defining the devices connected to this PC

# input stick
t16k = gremlin.input_devices.JoystickDecorator( T16K_NAME, gremlin.common.DeviceIdentifier(T16K_HWID,T16K_ID) , MODE_ALL )
tms = gremlin.input_devices.JoystickDecorator( TM_STICK_NAME, gremlin.common.DeviceIdentifier(TM_STICK__HWID,TM_STICK__ID) , MODE_ALL )

curve = CubicSpline([
	(-1.0, -1.0),
	(-0.5, -0.25),
	( 0.0,  0.0),
	( 0.5,  0.25),
	( 1.0,  1.0)
])

gremlin.util.log("Custom scale module enabled")

y_invert = -1.0
active_scale = 1.0
min_scale = 0.15
toggle_nose_wheel = False

@tms.button(4)
def toggle_nsw(event, vjoy):
	global toggle_nose_wheel
	toggle_nose_wheel = not(toggle_nose_wheel)
	
@tms.axis(1):	
def xaxis(event, vjoy):
	global active_scale
	global toggle_nose_wheel
	if toggle_nose_wheel:
		vjoy[1].axis(4).value = curve(event.value*active_scale)


@t16k.axis(1)
def xaxis(event, vjoy):
	global active_scale
	vjoy[1].axis(4).value = curve(event.value*active_scale)

@t16k.axis(2)
def yaxis(event, vjoy):
	global active_scale
	# gremlin.util.log("Y value: %s  curved: %s" % (event.value, curve(event.value*active_scale)))
	vjoy[1].axis(5).value = y_invert*curve(event.value*active_scale)
	
# scale axis = throttle on the left stick
@t16k.axis(4)
def scale(event, joy, vjoy):
	gremlin.util.log("scaling...")
	global active_scale
	global min_scale
	# get a value between 0 and 1, axis value will be between -1 and 1
	active_scale =  (1 - event.value) / (2.0)
	if active_scale < min_scale:
		active_scale = min_scale
	gremlin.util.log("New scale: %s" % (active_scale))
	j = joy["T.16000M"]
	x = j.axis(1).value
	y = j.axis(2).value
	vjoy[1].axis(4).value = curve(x*active_scale)
	vjoy[1].axis(5).value = y_invert*curve(y*active_scale)

