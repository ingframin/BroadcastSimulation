from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, mavutil
from drone_ctrl import *

#this depends from the pi, it needs to be a parameter
connection_string = '/dev/ttyACM0'
print("\nConnecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)
vehicle.wait_ready('autopilot_version')
print(" Autopilot Firmware version: %s" % vehicle.version)
vehicle.mode = VehicleMode("STABILIZE")

curr_pos = getGPS(vehicle)



print(" Global Location: %s" % vehicle.location.global_frame)
