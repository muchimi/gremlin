# configuration file for device IDs




'''
2019-03-16 13:48:37      DEBUG Added: name=T-Rudder windows_id=11 hardware_id=72332921
2019-03-16 13:48:37      DEBUG Added: name=vJoy Device windows_id=10 hardware_id=305446573
2019-03-16 13:48:37      DEBUG Added: name=vJoy Device windows_id=9 hardware_id=305446573
2019-03-16 13:48:37      DEBUG Added: name=vJoy Device windows_id=8 hardware_id=305446573
2019-03-16 13:48:37      DEBUG Added: name=DSD Flight Series Button Controller windows_id=7 hardware_id=81300029
2019-03-16 13:48:37      DEBUG Added: name=CH FLIGHT SIM YOKE USB  windows_id=6 hardware_id=109969663
2019-03-16 13:48:37      DEBUG Added: name=Throttle - HOTAS Warthog windows_id=5 hardware_id=72287236
2019-03-16 13:48:37      DEBUG Added: name=T.16000M windows_id=4 hardware_id=72331530
2019-03-16 13:48:37      DEBUG Added: name=Logitech G29 Driving Force Racing Wheel USB windows_id=3 hardware_id=74302031
2019-03-16 13:48:37      DEBUG Added: name=CH THROTTLE QUADRANT windows_id=2 hardware_id=109969658
2019-03-16 13:48:37      DEBUG Added: name=DSD Flight Series Button Controller windows_id=1 hardware_id=81300029
2019-03-16 13:48:37      DEBUG Added: name=Joystick - HOTAS Warthog windows_id=0 hardware_id=72287234


2019-07-07 14:37:32      DEBUG Added: name=T-Rudder guid={A5AA2B50-25E9-11E7-8001-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=Joystick - HOTAS Warthog guid={A60B8530-25E9-11E7-8004-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=CH THROTTLE QUADRANT guid={82B95310-3277-11E7-8001-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=Logitech G29 Driving Force Racing Wheel USB guid={DFEF1600-2876-11E8-8001-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=DSD Flight Series Button Controller guid={A4F58A50-2156-11E9-8001-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=T.16000M guid={A60B5E20-25E9-11E7-8002-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=CH FLIGHT SIM YOKE USB  guid={21C09900-4347-11E9-8001-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=Throttle - HOTAS Warthog guid={A60B8530-25E9-11E7-8003-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=DSD Flight Series Button Controller guid={0C2523B0-2158-11E9-8001-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=vJoy Device guid={2D3260A0-6FA6-11E7-8002-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=vJoy Device guid={705DC1A0-C170-11E7-8003-444553540000}
2019-07-07 14:37:32      DEBUG Added: name=vJoy Device guid={8245C100-2705-11E9-8002-444553540000}
'''



TM_STICK_ID = 1
TM_STICK_HWID = 72287234
TM_STICK_NAME = "Joystick - HOTAS Warthog"
TM_STICK_GUID = "{A60B8530-25E9-11E7-8004-444553540000}"

LEFT_DSD_ID = 4
LEFT_DSD_HWID = 81300029
LEFT_DSD_NAME = "DSD FLight Series Button Controller"
LEFT_DSD_GUID = "{A4F58A50-2156-11E9-8001-444553540000}"

CH_QUADRANT_ID = 2
CH_QUADRANT_HWID = 109969658
CH_QUADRANT_NAME = "CH THROTTLE QUADRANT"
CH_QUADRANT_GUID = "{82B95310-3277-11E7-8001-444553540000}"

G29_ID = 3
G29_HWID = 74302031
G29_NAME = "Logitech G29 Driving Force Racing Wheel USB"
G29_GUID = "{DFEF1600-2876-11E8-8001-444553540000}"

T16K_ID = 5
T16K_HWID = 72331530
T16K_NAME = "T.16000M"
T16K_GUID = "{A60B5E20-25E9-11E7-8002-444553540000}"

TM_THROTTLE_ID = 7
TM_THROTTLE_HWID = 72287236
TM_THROTTLE_NAME = "Throttle - HOTAS Warthog"
TM_THROTTLE_GUID = "{A60B8530-25E9-11E7-8003-444553540000}"

CH_YOKE_ID = 6
CH_YOKE_HWID = 109969663
CH_YOKE_NAME = "CH FLIGHT SIM YOKE USB"
CH_YOKE_GUID = "{21C09900-4347-11E9-8001-444553540000}"

RIGHT_DSD_HWID = 81300029
RIGHT_DSD_ID = 8
RIGHT_DSD_NAME = "DSD FLight Series Button Controller"
RIGHT_DSD_GUID = "{0C2523B0-2158-11E9-8001-444553540000}"

VJOY_INPUT_GUID = "{203C80E0-15C8-11EA-8002-444553540000}"
VJOY_INPUT_NAME = "vJoy Device"

# 9 vjoy
# 10 vjoy
# 11 vjoy

TM_RUDDER_ID = 0
TM_RUDDER_HWID = 72332921
TM_RUDDER_NAME = "T-Rudder"
TM_RUDDER_GUID = "{A5AA2B50-25E9-11E7-8001-444553540000}"


MODE_ALL = "Default"
MODE_A = "A"

# pulse length in seconds

PULSE_LENGTH = 0.1

# delay in seconds to determine slow rotation vs fast rotation pulses for rotary knobs - this is time in seconds between rotation pulses
LONG_PULSE = 0.1

''' REFERENCE AXES '''

'''
_AxisNames_to_enum_lookup = {
   1 "X Axis": AxisNames.X,
   2 "Y Axis": AxisNames.Y,
   3 "Z Axis": AxisNames.Z,
   4 "X Rotation": AxisNames.RX,
   5 "Y Rotation": AxisNames.RY,
   6 "Z Rotation": AxisNames.RZ,
   7 "Slider": AxisNames.SLIDER,
   8 "Dial": AxisNames.DIAL
}
'''
