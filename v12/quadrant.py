import gremlin
import time
from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants defining the devices connected to this PC

# input stick
#leftPanel = gremlin.input_devices.JoystickDecorator( LEFT_DSD_NAME, gremlin.common.DeviceIdentifier(LEFT_DSD_HWID, LEFT_DSD_ID), MODE_ALL )
quadrant = gremlin.input_devices.JoystickDecorator( CH_QUADRANT_NAME, gremlin.common.DeviceIdentifier(CH_QUADRANT_HWID, CH_QUADRANT_ID) , MODE_ALL )


gremlin.util.log("Quadrant module enabled")
	
PROP_CUTOFF = 0.0	
PROP_CUTOFF_VALUE = 0.0
PROP_MIN = 0.2
PROP_MIN_VALUE = 0.15
PROP_START = 0.25
PROP_START_VALUE = 0.25
PROP_IDLE = 0.4
PROP_IDLE_VALUE = 1.0
PROP_MAX = 2.0
PROP_MAX_VALUE = 2.0

AXIS_MIN = -1.0
AXIS_MAX = 1.0

PROP_1_AXIS = 7
PROP_2_AXIS = 8
PROP_1_VJOY = 2
PROP_2_VJOY = 2

_cutoff_1_allowed = False
_cutoff_2_allowed = False

range = (PROP_MAX_VALUE - PROP_IDLE_VALUE)/(PROP_MAX-PROP_IDLE)
#range =(PROP_MAX_VALUE - PROP_MIN_VALUE)/(PROP_MAX-PROP_MIN)

# get a prop value axis that gates the value for low range CUTOFF/MIN/START/IDLE (variable) MAX
def getProp(event, cuttof_allowed):
	value = 1 - event.value # range 0 to 2	/ reversed
	prop = 0
	
	global range
	
	if value >= PROP_IDLE:
		prop =  value
	elif value >= PROP_IDLE:
		prop = PROP_IDLE_VALUE
	elif value >= PROP_START:
		prop = PROP_START
	elif value >= PROP_MIN:
		prop = PROP_MIN_VALUE
	elif cuttof_allowed:
		prop = PROP_CUTOFF_VALUE
	else:
		prop = PROP_MIN_VALUE
		
		
	'''
	if value >= PROP_MIN:
		prop = value * range
	elif cuttof_allowed:
		prop = PROP_CUTOFF_VALUE
	else:
		prop = PROP_MIN_VALUE	
	'''	
	
	# prop is now in range 0 .. 2
	
	prop = prop - 1 #range -1 to 1
	gremlin.util.log("value: %s   prop: %s" % (value,prop))
	return prop

		
# axis 3 sets the prop lever to minimum
@quadrant.axis(1)
def prop1(event, vjoy):
	global _cutoff_1_allowed
	prop = getProp(event,_cutoff_1_allowed)
	vjoy[PROP_1_VJOY].axis(PROP_1_AXIS).value = prop
	
@quadrant.axis(2)
def prop2(event, vjoy):
	global _cutoff_2_allowed
	prop = getProp(event,_cutoff_2_allowed)
	vjoy[PROP_2_VJOY].axis(PROP_2_AXIS).value = prop	

@quadrant.axis(3)
def mix1(event):
	global _cutoff_1_allowed
	if event.value > 0:
		_cutoff_1_allowed = True
	else:
		_cutoff_1_allowed = False
	gremlin.util.log("cuttof 1 %s" % (_cutoff_1_allowed))
	

@quadrant.axis(4)
def mix2(event):
	global _cutoff_2_allowed
	if event.value > 0:
		_cutoff_2_allowed = True
	else:
		_cutoff_2_allowed = False
	gremlin.util.log("cuttof 2 %s" % (_cutoff_2_allowed))