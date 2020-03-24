import gremlin
import time
import uuid
from gremlin.spline import CubicSpline
from gremlin.input_devices import keyboard, macro
from vjoy.vjoy import AxisName
from configuration import * # load constants defining the devices connected to this PC

# input stick
t16k = gremlin.input_devices.JoystickDecorator( T16K_NAME, T16K_GUID , MODE_ALL )
#tms = gremlin.input_devices.JoystickDecorator( TM_STICK_NAME, TM_STICK_GUID , MODE_ALL )
tmthrottle = gremlin.input_devices.JoystickDecorator( TM_THROTTLE_NAME, TM_THROTTLE_GUID, MODE_ALL )
rudder = gremlin.input_devices.JoystickDecorator( TM_RUDDER_NAME,TM_RUDDER_GUID , MODE_ALL )

toggle_light_macro = macro.Macro()
toggle_light_macro.tap("L")

curve = CubicSpline([
	(-1.0, -1.0),
	(-0.5, -0.25),
	( 0.0,  0.0),
	( 0.5,  0.25),
	( 1.0,  1.0)
])

gremlin.util.log("Custom scale module enabled v2")

y_invert = -1.0;
min_scale = 0.15
active_scale = 1.0
scale_axis = True
scale_axis_value = -2;
read_scale = True

def update_scale(v):
	global active_scale
	global scale_axis_value
	if scale_axis_value != v:
		active_scale =  (1.0 - v) / (2.0)
		scale_axis_value = v;	
		if min_scale > active_scale:
			active_scale = min_scale

# NOTE: the throttle on the T16K is axis #7 (rudder is #6)
@t16k.axis(7)
def scale_changed(event, joy, vjoy):
	global active_scale
	global scale_axis_value
	update_scale(event.value)
	
	#gremlin.util.log("new axis scale: %s" % active_scale)
	if scale_axis:
		j = joy[event.device_guid]
		x = j.axis(1).value
		y = j.axis(2).value
		vjoy[1].axis(4).value = curve(x*active_scale)
		vjoy[1].axis(5).value = curve(y*active_scale)
		
		# read throttle
		j = joy[tmthrottle.device_guid]
		v = -j.axis(7).value
		if v != 0:
			vjoy[1].axis(5).value = curve(v*active_scale)
			

#button 8 - turn on scaling = large button RIGHT of the stick on base
@t16k.button(8)
def toggle_on(event, vjoy):
	global scale_axis
	if event.is_pressed:
		gremlin.util.log("Toggle strafe scale ON")
		scale_axis = True
		gremlin.util.log("New scale: %s" % (active_scale))
	
#button 8 - turn off scaling - large button LEFT of the stick on base
@t16k.button(14)
def toggle_off(event, vjoy):
	global scale_axis
	if event.is_pressed:
		gremlin.util.log("Toggle strafe scale OFF")
		scale_axis = False
		gremlin.util.log("New scale: %s" % (active_scale))
		
# x axis
@t16k.axis(1)
def xaxis(event, joy, vjoy):
	global active_scale
	global read_scale
	# rotation x
	if scale_axis:
		if read_scale:
			read_scale = False
			j = joy[event.device_guid]
			update_scale(j.axis(7).value)
			
		vjoy[1].axis(4).value = curve(event.value*active_scale)
	else:
		vjoy[1].axis(4).value = curve(event.value)

# y axis
@t16k.axis(2)
def yaxis(event, joy, vjoy):
	global active_scale
	global read_scale
	# rotation y
	if scale_axis:
		if read_scale:
			read_scale = False
			j = joy[event.device_guid]
			update_scale(j.axis(7).value)
		vjoy[1].axis(5).value = curve(-event.value*active_scale)
	else:
		vjoy[1].axis(5).value = curve(-event.value)
		


'''			
# fixed throttle
# axis 7 = friction stick
# axis 6 = left throttle
@tmthrottle.axis(7)
def scale_throttle(event, joy, vjoy):
	global active_scale
	global read_scale
	v = event.value  # invert
	if scale_axis:
		if read_scale:
			read_scale = False
			j = joy[event.device_guid]
			update_scale(j.axis(7).value)
		vjoy[1].axis(5).value = curve(v*active_scale)
	else:
		vjoy[1].axis(5).value = curve(v)
'''

# set max acceleration on press, 50 on release, 5% on down
@tmthrottle.button(27)
def max_accel(event, joy, vjoy):
	if event.is_pressed:
		vjoy[2].axis(1).value = 1
	else:
		vjoy[2].axis(1).value = 0
		
# set acceleration to 5%
@tmthrottle.button(28)
def min_accel(event, joy, vjoy):
	if event.is_pressed:
		vjoy[2].axis(1).value = -0.9
	else:
		vjoy[2].axis(1).value = 0		
		



# toggle lights on press or release
@tmthrottle.button(24)
def min_accel(event, joy, vjoy):
	gremlin.macro.MacroManager().queue_macro(toggle_light_macro)


# values are (-1, +1) for each axis
def merge(left, right, joy, vjoy):
	global active_scale
	global read_scale
	
	value = (left - right) / 2.0
	# gremlin.util.log("Left: %s  Right: %s  Merged value: %s" % (left, right, value))
	# output to vjoy #2 slider
	scale = 1.0
	if scale_axis:
		if read_scale:
			read_scale = False
			j = joy[t16k.device_guid]
			update_scale(j.axis(7).value)
		vjoy[2].axis(7).value = value*active_scale
	else:
		vjoy[2].axis(7).value = value
	
	
@rudder.axis(1)
def rxaxis(event, vjoy, joy):
	guid = event.device_guid
	right = event.value
	left = joy[guid].axis(2).value
	merge(left,right, joy, vjoy)
		
# pitch axis disconnect of nose wheel steer
@rudder.axis(2)
def rxaxis(event, vjoy, joy):
	guid = event.device_guid
	right = joy[guid].axis(1).value
	left = event.value
	merge(left,right, joy, vjoy)