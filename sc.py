import gremlin
import time
import uuid
import atexit
from gremlin.spline import CubicSpline
from gremlin.input_devices import keyboard, macro
from vjoy.vjoy import AxisName
from configuration import * # load constants defining the devices connected to this PC
from util import *
from hardware import *

bump_a_index = 0
bump_a_table = [-0.94, -0.9,-0.7,0.0,1.0]
bump_a_max = len(bump_a_table)

gremlin.util.log("Custom SC module enabled")

brake_threshold = 0.95 # value of deviation (+ or -) to reach to trigger brake action on twist
brake_on_macro = macro.Macro()
brake_off_macro = macro.Macro()
brake_on_macro.press("Z")
brake_off_macro.release("Z")
flip_trigger = False
repeat_trigger_a = False
repeat_trigger_b = False
trigger_a_pressed = False
trigger_b_pressed = False

def exit_handler():
	gremlin.util.log("sc exit!")
	repeat_fire_cancel_all()

atexit.register(exit_handler)


# gets a bracket value for a given joystick value - will be the low or high bracket depending on direction
def get_value(direction, current):
	old_value = bump_a_table[1] # smallest value possible
	gremlin.util.log("current joystick value: %s" % (current))
	for value in bump_a_table:
		gremlin.util.log("current bracket: [%s, %s]" % (old_value, value))
		if current >= old_value and ((direction > 0 and current < value) or (direction < 0 and current <= value)):
			if direction > 0:
				gremlin.util.log("return value: %s" % (value))	
				return value
			else:
				gremlin.util.log("return value: %s" % (old_value))
				return old_value
		old_value = value
	gremlin.util.log("no bracket found: return value: %s" % (value))	
	return value
	
		
# handle acceleration presets		
@t16k.hat(1)
def left_hat_management(event, vjoy):
	#gremlin.util.log("in hat management %s %s %s" % (event.value, event.value[0], event.value[1]))
	global bump_a_table, bump_a_index
	current = vjoy[1].axis(AxisName.RZ).value
	new_value = current
	if event.value == (0, 1):  # bracket up
		new_value = get_value(+1, current)
	elif event.value == (0, -1): # bracket down
		new_value = get_value(-1, current)
	'''
	elif event.value == (1, 0): # right
		# shield_macros["right"].run()
	elif event.value == (-1, 0): # left
		# shield_macros["left"].run()		
	'''

	gremlin.util.log("Current: %s  New value: %s" % (current, new_value))
	vjoy[1].axis(AxisName.RZ).value = new_value

last_rot_value = -2 # invalid value
brake_on = False # not braking by default


# stick z rotation (#6 is the rudder for some reason) = brake
@t16k.axis(6)
def speed_brake(event, vjoy):
	global last_rot_value, brake_on, brake_threshold
	if event.value != last_rot_value:
		last_rot_value = event.value
		value = abs(event.value) 
		if not brake_on and value >= brake_threshold: 
			brake_on = True
			gremlin.macro.MacroManager().queue_macro(brake_on_macro) 
			
		elif brake_on and value < brake_threshold:
			gremlin.macro.MacroManager().queue_macro(brake_off_macro) 
			brake_on = False
			
@tms.button(1)
def trigger_a(event, vjoy):
	global flip_trigger, trigger_a_pressed, trigger_b_pressed, repeat_trigger_a, repeat_trigger_b
	pressed = event.is_pressed
	gremlin.util.log("trigger A {} flipped: {}: repeat A: {}  repeat B: {}".format(pressed, flip_trigger, repeat_trigger_a, repeat_trigger_b))
	if flip_trigger:
		if repeat_trigger_b:
			trigger_b_pressed = pressed
		else:
			vjoy[1].button(2).is_pressed = pressed
	else:
		if repeat_trigger_a:
			trigger_a_pressed = pressed
		else:
			vjoy[1].button(1).is_pressed = pressed
		
@tms.button(2)
def trigger_b(event, vjoy):
	global flip_trigger, trigger_a_pressed, trigger_b_pressed, repeat_trigger_a, repeat_trigger_b
	pressed = event.is_pressed
	gremlin.util.log("trigger B {} flipped: {}: repeat A: {}  repeat B: {}".format(pressed, flip_trigger, repeat_trigger_a, repeat_trigger_b))
	if flip_trigger:
		if repeat_trigger_a:
			trigger_a_pressed = pressed
		else:
			vjoy[1].button(1).is_pressed = pressed
	else:
		if repeat_trigger_b:
			trigger_b_pressed = pressed
		else:
			vjoy[1].button(2).is_pressed = pressed
			

			
@tms.button(6)
def dual_trigger(event, vjoy):
	global flip_trigger, trigger_a_pressed, trigger_b_pressed, repeat_trigger_a, repeat_trigger_b
	trigger_a(event, vjoy)
	trigger_b(event, vjoy)
	
@tmthrottle.button(22)
def flip_a(event, vjoy):
	global flip_trigger, trigger_a_pressed, trigger_b_pressed
	if event.is_pressed:
		flip_trigger = False
	vjoy[1].button(1).is_pressed = False
	vjoy[1].button(2).is_pressed = False		
		
@tmthrottle.button(23)
def flip_b(event, vjoy):
	global flip_trigger, trigger_a_pressed, trigger_b_pressed
	flip_trigger = event.is_pressed
	vjoy[1].button(1).is_pressed = False
	vjoy[1].button(2).is_pressed = False
	gremlin.util.log("toggle flip {}".format(flip_trigger))
	
	
@tmthrottle.button(16)
def repeat_a(event, vjoy):
	global repeat_trigger_a
	repeat_trigger_a = event.is_pressed
	#gremlin.util.log("toggle repeat A {}".format(repeat_trigger_a))
	
@tmthrottle.button(17)
def repeat_b(event, vjoy):
	global repeat_trigger_b
	repeat_trigger_b = event.is_pressed
	#gremlin.util.log("toggle repeat B {}".format(repeat_trigger_b))
	

@gremlin.input_devices.periodic(0.5)
def periodic_function(vjoy):
	global flip_trigger, repeat_trigger_a, repeat_trigger_b, trigger_a_pressed, trigger_b_pressed

	# if flip_trigger:
		# index_a = 2
		# index_b = 1
	# else:
	index_a = 1
	index_b = 2
		
	if repeat_trigger_a:
		vjoy[1].button(index_a).is_pressed = trigger_a_pressed
		#gremlin.util.log("A")
		
	if repeat_trigger_b:
		vjoy[1].button(index_b).is_pressed = trigger_b_pressed
		#gremlin.util.log("B")
		
	#gremlin.util.log("C")
	
	if repeat_trigger_a or repeat_trigger_b: 
		time.sleep(0.2)
		
	#gremlin.util.log("D")	

	if repeat_trigger_a:
		vjoy[1].button(index_a).is_pressed = False
		
	if repeat_trigger_b:
		vjoy[1].button(index_b).is_pressed = False
		
	#gremlin.util.log("here repeat {} {}".format(repeat_trigger_a, repeat_trigger_b))		