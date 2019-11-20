from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, mavutil
from drone_ctrl import *
import datetime

#this depends from the pi, it needs to be a parameter
connection_string = '/dev/ttyACM0'
print("\nConnecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)
vehicle.wait_ready('autopilot_version')
print(" Autopilot Firmware version: %s" % vehicle.version)
vehicle.mode = VehicleMode("STABILIZE")

curr_pos = getGPS(vehicle)



print(" Global Location: %s" % vehicle.location.global_frame)
print(' Vehicle Time: %s'% vehicle.gps_0)


@vehicle.on_message('SYSTEM_TIME')
def listener(self,name,message):
    print(datetime.datetime.fromtimestamp(int(message.time_unix_usec/1E6)))

while True:
    pass
