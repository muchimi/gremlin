

import gremlin
import time
import threading
from threading import Timer

from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants from the configuration.py file



timer_threads = {}

class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer     = None
		self.interval   = interval
		self.function   = function
		self.args       = args
		self.kwargs     = kwargs
		self.is_running = False
		# gremlin.util.log("init")
		# for n,arg in enumerate(args):
			# gremlin.util.log("arg: {}: {}".format(n,arg))
		# for n,arg in kwargs.items():
			# gremlin.util.log("kwarg: {}: {}".format(n,arg))			
			
		self.start()

	def _run(self):
		self.is_running = False
		gremlin.util.log("run 1")
		self.function(*self.args, **self.kwargs)
		gremlin.util.log("run 2")
		self.start()


	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self._timer.join()
		self.is_running = False
		gremlin.util.log("stop")

	
		
# async routine to pulse a button
def fire_pulse(vjoy, unit, button, repeat = 1, duration = 0.1):
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
			gremlin.util.log("Pulsing vjoy {} button {} on".format(unit, button) )  
			vjoy[unit].button(button).is_pressed = True
			time.sleep(duration)
			vjoy[unit].button(button).is_pressed = False
		else:
			vjoy[unit].button(button).is_pressed = True
			time.sleep(duration*repeat)
			vjoy[unit].button(button).is_pressed = False        
		
	# gremlin.util.log("Pulsing vjoy %s button %s off" % (unit, button) )

# pulses a button - unit is the vjoy output device number, button is the number of the button on the device to pulse
def pulse(vjoy, unit, button, repeat = 1, duration = 0.1):
	gremlin.util.log("pulsing: unit {} button {}".format(unit, button))
	threading.Timer(0.01, fire_pulse, [vjoy, unit, button, repeat, duration]).start()

	
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


def repeat_pulse(vjoy, unit, button, repeat, duration):
	gremlin.util.log("pulsing: unit {} button {}".format(unit, button))
	
	#threading.Timer(0.01, fire_pulse, [vjoy, unit, button, repeat, duration]).start()
	
def repeat_fire(name, vjoy, unit, button, repeat=1, interval = 0.5, duration = 0.2):
	global timer_threads
	repeat_fire_cancel(name)
	gremlin.util.log("repeat {} unit {} button {} repeat {} interval {} duration {}".format(name, unit, button, repeat, interval, duration))
	args = (vjoy, unit, button, repeat, duration)
	rt = RepeatedTimer(interval, pulse, vjoy, unit, button, repeat, duration )
	timer_threads[name] = rt
	
def repeat_fire_cancel(name):
	global timer_threads
	gremlin.util.log("cancel {}".format(name))	
	if name in timer_threads:
		rt = timer_threads[name]
		rt.stop()
		del timer_threads[name]
		
def repeat_fire_cancel_all():
	global timer_threads
	for name in timer_threads:
		rt = timer_threads[name]
		rt.stop()
