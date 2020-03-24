

import gremlin
import time
import threading
from gremlin.spline import CubicSpline
from vjoy.vjoy import AxisName
from configuration import * # load constants from the configuration.py file
	

# input stick
t16k = gremlin.input_devices.JoystickDecorator( T16K_NAME, T16K_GUID , MODE_ALL )
tms = gremlin.input_devices.JoystickDecorator( TM_STICK_NAME, TM_STICK_GUID , MODE_ALL )
tmthrottle = gremlin.input_devices.JoystickDecorator( TM_THROTTLE_NAME, TM_THROTTLE_GUID, MODE_ALL )
rudder = gremlin.input_devices.JoystickDecorator( TM_RUDDER_NAME,TM_RUDDER_GUID , MODE_ALL )
leftPanel = gremlin.input_devices.JoystickDecorator( LEFT_DSD_NAME, LEFT_DSD_GUID, MODE_ALL )
rightPanel = gremlin.input_devices.JoystickDecorator( RIGHT_DSD_NAME, RIGHT_DSD_GUID, MODE_ALL )
g29 = gremlin.input_devices.JoystickDecorator( G29_NAME,G29_GUID, MODE_ALL )