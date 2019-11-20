# -*- coding: utf-8 -*-
'''
License:
© Copyright 2018, Networked Systems group, ESAT-TELEMIC,KU Leuven.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
   must display the following acknowledgement:
   This product includes software developed by Networked Systems group,
   ESAT-TELEMIC,KU Leuven.
4. Neither the name of the Networked Systems group, ESAT-TELEMIC,KU Leuven nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY ESAT-TELEMIC-KU Leuven, ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Networked Systems group, ESAT-TELEMIC,KU Leuven
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
'''
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, mavutil
from time import sleep, perf_counter
from serial import Serial
from threading import Thread
from datetime import datetime
from drone_ctrl import *


start = perf_counter()

running = True
lg = []
sequence = 0
#this depends from the pi, it needs to be a parameter
connection_string = '/dev/ttyACM0'
print("\nConnecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, wait_ready=True)
vehicle.wait_ready('autopilot_version')
print(" Autopilot Firmware version: %s" % vehicle.version)
vehicle.mode = VehicleMode("STABILIZE")

curr_pos = getGPS(vehicle)

arm_and_takeoff(vehicle, 25)
vehicle.airspeed = 2


wifi1 = Serial("/dev/serial0",115200, xonxoff=True)
n = 1

while curr_pos is None:
    sleep(1)
    
    curr_pos = getGPS(vehicle)
    #print(curr_pos)

while running:
    try:
        coords = getGPS(vehicle)
        
        if coords is not None:
            curr_pos = coords
        s = wifi1.readline()
        
        if b'>' in s:

            ssid = ("%d-"%n+str(sequence)+'*')
            wifi1.write(ssid.encode())
            lg.append((curr_pos,s,'sent:'+ssid))
            sequence += 1

        else:
            lg.append((curr_pos,s))
    

        if len(lg)>20:
            with open('drone-%d.txt'%n,'a') as log:
                for l in lg:
                    print(l,file=log)
            lg = []

    except:
        running = False

with open('drone-%d.txt'%n,'a') as log:
    for l in lg:
        print(l,file=log)